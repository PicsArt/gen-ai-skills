#!/usr/bin/env python3
"""The matched / changed report: each reference beat against the user's rows, and the content rules.

    python3 scripts/structure_report.py sheet.json mapping.json [--transcript reference.json]
                                        [--media media.json] [--allow "get ready with me"] [--json]

`sheet` is the reference's structure sheet and `mapping` is map_structure.py's output. The
table has one row per reference beat (matched, changed or dropped, with the reason) and one per
row of ours that copies no beat (added).

The content rules, each passed, failed or not checked:
1. words: no run of 4 or more words of the reference's speech in our voice lines, matched across
   the rows as one script (a run may cross from one row into the next). The reference is
   `--transcript` (picsart_media_transcribe's result) or else the sheet's Voice cells;
2. captions: our on-screen words are our own; only the reference's caption pattern is copied.
   Compared with every word of the reference (voice and on screen, and the transcript's speech
   when given). A run of 4 or more words fails, and so does a shorter one when it is a whole
   caption line (2 or more words) of ours, or of the reference's On screen. A format label nobody
   owns (reuse_guard.GENRE_PHRASES: "get ready with me", "POV", ...) passes and is listed as
   "genre phrase, allowed"; `--allow` exempts any other phrase the user chose to keep;
3. pictures: no still or clip of the reference is a generation input;
4. sound: no audio or music of the reference is used.
Rules 3 and 4 read `--media`, a JSON object: {"reference": [the reference's URL and every still,
sheet or clip made from it], "generation_inputs": [every URL given to a generation],
"audio": [every audio URL in the cut]}. Without it, or without the list a rule reads, they are
not checked, and say so; only an explicit empty list says nothing was used. The reference list
must identify the reference. Words and captions are not checked while the corresponding
reference cells are unknown and no transcript covers the speech.

Prints Markdown, or JSON with --json. Exits 1 when a content rule fails, 0 otherwise, 2 for bad
input. Standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

import reuse_guard
import sheet as sheets

Json = Dict[str, Any]


def line_of(text: str) -> str:
    """One line of text, so a row is one line of the script find_hits reads."""
    return " ".join(str(text or "").split())


def row_hit(hit: Json, ids: List[str]) -> Json:
    """A shared run with the row it starts in, and every row it runs through."""
    rows = list(dict.fromkeys(ids[hit["line"] - 1:hit["end_line"]]))
    return {"row": rows[0], "rows": rows, "words": hit["words"], "text": hit["text"], "pieces": hit["pieces"]}


# A speaker's label before a quoted line ('Dot: "…"'), and a timing note ('from 63.7 s').
SPEAKER = re.compile(r'^\s*[^\s"“:]{1,30}(?:\s[^\s"“:]{1,30})?:\s*(?=["“])')
TIMING = re.compile(r"\b(?:from|at|to|until)\s+\d+(?:\.\d+)?\s*s\b", re.I)
# Only these closed note items are metadata; every other bracket is prose.
TIME_POINT = r"(?:\d+:[0-5]\d(?:\.\d+)?|\d+(?:\.\d+)?)"
TIME = rf"(?:{TIME_POINT}\s*s?\s*[-–]\s*)?(?:\d+(?:\.\d+)?\s*s|\d+:[0-5]\d(?:\.\d+)?(?:\s*s)?)"
PRESENTATION = (r"(?:top|bottom|middle|center|centre|left|right|white|black|red|yellow|blue|green|"
                r"pink|orange|purple|grey|gray|bold|italic|caps|uppercase|lowercase)")
NOTE_ITEM = re.compile(rf"(?:{TIME}|\d+\s+(?:words?|shots?)|{PRESENTATION}(?:\s+{PRESENTATION})*)", re.I)
NOTES = re.compile(r"\(([^()]*)\)|" + TIMING.pattern, re.I)


def without_notes(text: str, pattern: re.Pattern = NOTES) -> str:
    """Strip known notes, keeping prose brackets whole (including any timing words inside)."""
    def replace(match: re.Match) -> str:
        content = match.group(1)
        if content is None or all(NOTE_ITEM.fullmatch(item.strip()) for item in content.split(",")):
            return " "
        return match.group(0)
    return pattern.sub(replace, text)


def spoken_text(text: Any, speaker: bool = False, notes: re.Pattern = NOTES) -> str:
    """A cell's words without what is not said or shown, line by line: notes in brackets
    ('(white, top)', '(0–2 s, 3 words)') from the closed grammar and timing notes outside its quotes, and, for speech
    (`speaker`), a speaker's label before a quote. What a quote holds is kept whole, and so are
    words outside quotes."""
    lines = []
    for line in str(text or "").splitlines():
        if speaker:
            line = SPEAKER.sub("", line)
        pieces, at = [], 0
        for quote in list(sheets.QUOTED.finditer(line)) + [None]:
            end = quote.start() if quote else len(line)
            pieces.append(without_notes(line[at:end], notes))
            if quote:
                pieces.append(quote.group(0))
                at = quote.end()
        lines.append(" ".join("".join(pieces).split()))
    return "\n".join(lines)


# Pass A: copied verbatim from main at the supplied baseline. Keep its raw cells
# and its quoted-text handling independent of the cleaned comparison below.
def quoted_text(text: str) -> str:
    """Quoted words without their presentation or timing notes, as '"part 2 soon" (white, top)
    from 63.7 s' writes them; a line with words outside its quotes is kept whole."""
    text = str(text or "")
    quotes = [m.group(1) or m.group(2) for m in sheets.QUOTED.finditer(text)]
    rest = re.sub(r"\([^)]*\)", " ", sheets.QUOTED.sub(" ", text))
    rest = re.sub(r"\b(?:from|at|to|until)\s+\d+(?:\.\d+)?\s*s\b", " ", rest, flags=re.I)
    return " ".join(quotes) if quotes and not re.search(r"\w", rest) else text


def caption_lines(texts: List[str]) -> List[str]:
    """Each line of each text, normalised: a caption line is compared alone, never its whole cell."""
    return [line for text in texts for line in
            (reuse_guard.normalise(quoted_text(l)) for l in str(text).splitlines()) if line]


def whole_captions(units: List[str], ours: List[Json], screen: List[str]) -> List[Json]:
    """Short verbatim copies of a caption, which the four-word speech limit misses: one of our
    on-screen lines of 2 or more words that is a run of the reference's words (`units`), or one
    whole on-screen caption line of the reference (`screen`, 2 or more words) inside ours. Each
    reference line is compared alone so a run never straddles two lines or cells; a Voice cell
    is speech, not a caption, so it is never a whole caption of its own."""
    words, captions = caption_lines(units), [c for c in caption_lines(screen) if len(c.split()) >= 2]
    found = []
    for row in ours:
        mine = caption_lines([row.get("on_screen") or ""])
        if not mine:
            continue
        padded = f" {' '.join(mine)} "
        texts = [c for c in captions if f" {c} " in padded]
        texts += [m for m in mine if len(m.split()) >= 2 and m not in texts
                  and any(f" {m} " in f" {unit} " for unit in words)]
        found += [{"row": row["id"], "rows": [row["id"]], "words": len(t.split()), "text": t} for t in texts]
    return found


def guard(reference: str, ours: List[Json], field: str, allow: List[str],
          genres: Optional[List[Json]] = None, units: Optional[List[str]] = None,
          screen: Optional[List[str]] = None) -> List[Json]:
    """Shared runs between the reference and one field of our rows, each with its row ids. The
    rows are matched as one script, so a run that crosses from one row into the next is found,
    and reported at the row it starts in. With `genres`, a run inside a genre phrase is let
    through and appended there instead. With `units` (and the on-screen ones, `screen`), short
    verbatim caption copies count too."""
    lines = [(row["id"], line_of(line)) for row in ours
             for line in ((quoted_text(row.get(field)) if field == "voice" else str(row.get(field) or ""))
                          .splitlines() or [""])]
    script = "\n".join(line for _, line in lines)
    ids = [ident for ident, _ in lines]
    candidates = [row_hit(h, ids) for h in reuse_guard.find_hits(reference, script)]
    if units is not None:
        known = {(h["row"], h["text"]) for h in candidates}
        candidates += [h for h in whole_captions(units, ours, screen or [])
                       if (h["row"], h["text"]) not in known
                       and not any(h["row"] == c["row"] and f" {h['text']} " in f" {c['text']} "
                                   for c in candidates)]
    hits = []
    for found in candidates:
        # Exemptions hold per line: each piece may be user-allowed or a genre phrase.
        exempt = reuse_guard.allowed(found, allow)
        is_genre = (not exempt and genres is not None
                    and reuse_guard.allowed(found, allow + list(reuse_guard.GENRE_PHRASES)))
        found = {k: v for k, v in found.items() if k != "pieces"}
        if exempt:
            continue
        (genres if is_genre else hits).append(found)
    return hits


# Pass B: both sides use spoken_text; never apply main's broader quote stripping.
def cleaned_caption_lines(texts: List[str]) -> List[str]:
    """Each line of each text, normalised: a caption line is compared alone, never its whole cell."""
    return [line for text in texts for line in
            (reuse_guard.normalise(spoken_text(l)) for l in str(text).splitlines()) if line]


def cleaned_whole_captions(units: List[str], ours: List[Json], screen: List[str]) -> List[Json]:
    """Short verbatim copies of a caption, which the four-word speech limit misses: one of our
    on-screen lines of 2 or more words that is a run of the reference's words (`units`), or one
    whole on-screen caption line of the reference (`screen`, 2 or more words) inside ours. Each
    reference line is compared alone so a run never straddles two lines or cells; a Voice cell
    is speech, not a caption, so it is never a whole caption of its own."""
    words = [reuse_guard.normalise(l) for u in units for l in u.splitlines()]
    captions = [c for c in (reuse_guard.normalise(l) for t in screen for l in t.splitlines())
                if len(c.split()) >= 2]
    found = []
    for row in ours:
        mine = cleaned_caption_lines([row.get("on_screen") or ""])
        if not mine:
            continue
        padded = f" {' '.join(mine)} "
        texts = [c for c in captions if f" {c} " in padded]
        texts += [m for m in mine if len(m.split()) >= 2 and m not in texts
                  and any(f" {m} " in f" {unit} " for unit in words)]
        found += [{"row": row["id"], "rows": [row["id"]], "words": len(t.split()), "text": t} for t in texts]
    return found


def cleaned_guard(reference: str, ours: List[Json], field: str, allow: List[str],
                  genres: Optional[List[Json]] = None, units: Optional[List[str]] = None,
                  screen: Optional[List[str]] = None) -> List[Json]:
    """Shared runs between the reference and one field of our rows, each with its row ids. The
    rows are matched as one script, so a run that crosses from one row into the next is found,
    and reported at the row it starts in. With `genres`, a run inside a genre phrase is let
    through and appended there instead. With `units` (and the on-screen ones, `screen`), short
    verbatim caption copies count too."""
    lines = [(row["id"], line_of(line)) for row in ours
             for line in spoken_text(row.get(field), field == "voice").splitlines() or [""]]
    script = "\n".join(line for _, line in lines)
    ids = [ident for ident, _ in lines]
    candidates = [row_hit(h, ids) for h in reuse_guard.find_hits(reference, script)]
    if units is not None:
        known = {(h["row"], h["text"]) for h in candidates}
        candidates += [h for h in cleaned_whole_captions(units, ours, screen or [])
                       if (h["row"], h["text"]) not in known
                       and not any(h["row"] == c["row"] and f" {h['text']} " in f" {c['text']} "
                                   for c in candidates)]
    hits = []
    for found in candidates:
        # Exemptions hold per line: each piece may be user-allowed or a genre phrase.
        exempt = reuse_guard.allowed(found, allow)
        is_genre = (not exempt and genres is not None
                    and reuse_guard.allowed(found, allow + list(reuse_guard.GENRE_PHRASES)))
        found = {k: v for k, v in found.items() if k != "pieces"}
        if exempt:
            continue
        (genres if is_genre else hits).append(found)
    return hits


def where(hit: Json) -> str:
    rows = hit.get("rows") or [hit["row"]]
    return ("row " if len(rows) == 1 else "rows ") + ", ".join(rows)


def unknown_cells(sheet: Json, field: str) -> int:
    """Count reference cells whose words have not been read."""
    return sum(1 for beat in sheet["beats"] if sheets.unknown(beat.get(field)))


def urls(media: Json, key: str) -> List[str]:
    value = media.get(key)
    if value is None:
        raise sheets.InputError(f"media {key} is missing: list every URL, or give an empty list when there are none")
    if not isinstance(value, list) or not all(isinstance(u, str) for u in value):
        raise sheets.InputError(f"media {key} must be a list of URLs")
    return [u.strip() for u in value]


def main_reuse(sheet: Json, ours: List[Json], transcript: Any,
               allow: List[str]) -> Tuple[List[Json], List[Json], List[Json]]:
    """Pass A: main's rules() comparison path, with its original text forms."""
    spoken = (reuse_guard.reference_text(transcript) if transcript is not None
              else reuse_guard.sheet_words(sheet, ("voice",)))
    words = guard(spoken, ours, "voice", [])
    genres: List[Json] = []
    # Every word the reference says or shows, its transcript's speech included, one text per cell,
    # field by field so consecutive Voice cells stay one stream of speech.
    cells = [[b[f] for b in sheet["beats"] if sheets.said(b.get(f))] for f in reuse_guard.WORD_FIELDS]
    units = [cell for field in cells for cell in field]
    screen = [b["on_screen"] for b in sheet["beats"] if sheets.said(b.get("on_screen"))]
    if transcript is not None:
        units.append(spoken)
        cells.append([spoken])
    # A NUL keeps each field, and the transcript, its own stream: no run crosses between them.
    reference = "\n\0\n".join("\n".join(field) for field in cells)
    hits = guard(reference, ours, "on_screen", allow, genres, units, screen)
    return words, hits, genres


def cleaned_reuse(sheet: Json, ours: List[Json], transcript: Any,
                  allow: List[str]) -> Tuple[List[Json], List[Json], List[Json]]:
    """Pass B: remove the closed annotation grammar from both sides."""
    spoken = spoken_text(reuse_guard.reference_text(transcript) if transcript is not None
                         else reuse_guard.sheet_words(sheet, ("voice",)), True)
    words = cleaned_guard(spoken, ours, "voice", [])
    genres: List[Json] = []
    cells = [[spoken_text(b[f], f == "voice") for b in sheet["beats"] if sheets.said(b.get(f))]
             for f in reuse_guard.WORD_FIELDS]
    units = [cell for field in cells for cell in field]
    screen = [spoken_text(b["on_screen"]) for b in sheet["beats"] if sheets.said(b.get("on_screen"))]
    if transcript is not None:
        units.append(spoken)
        cells.append([spoken])
    reference = "\n\0\n".join("\n".join(field) for field in cells)
    captions = cleaned_guard(reference, ours, "on_screen", allow, genres, units, screen)
    return words, captions, genres


def union_hits(first: List[Json], second: List[Json]) -> List[Json]:
    """Pass A's hits and pass B's, once each by (row, text)."""
    found: Dict[Any, Json] = {}
    for hit in first + second:
        found.setdefault((hit["row"], hit["text"]), hit)
    return list(found.values())


def rules(sheet: Json, mapping: Json, transcript: Any = None, media: Optional[Json] = None,
          allow: Optional[List[str]] = None) -> List[Json]:
    allow = allow or []
    ours = mapping["rows"]
    a_words, a_captions, a_genres = main_reuse(sheet, ours, transcript, allow)
    b_words, b_captions, b_genres = cleaned_reuse(sheet, ours, transcript, allow)
    # Each pass applies its own genre and allow exemptions; a hit either one keeps counts.
    words = union_hits(a_words, b_words)
    captions = union_hits(a_captions, b_captions)
    genres = [g for g in union_hits(a_genres, b_genres)
              if not any(g["row"] == h["row"] and g["text"] == h["text"] for h in captions)]
    unread_voice = 0 if transcript is not None else unknown_cells(sheet, "voice")
    unread_screen = unknown_cells(sheet, "on_screen")
    hits = words
    results = []
    if hits:
        result, detail = "failed", "; ".join(f"{where(h)}: \"{h['text']}\"" for h in hits)
    elif unread_voice:
        result = "not checked"
        detail = (f"{unread_voice} of the reference's Voice cells are unknown (?) and no transcript was given; "
                  "give --transcript, or fill the cells (none when nothing is said)")
    else:
        result, detail = "passed", "no run of 4 or more of the reference's spoken words"
    results.append({"rule": "words", "result": result, "hits": hits, "detail": detail})
    hits = captions
    let_through = [f"{where(g)}: \"{g['text']}\" (genre phrase, allowed)" for g in genres]
    if hits:
        result, detail = "failed", "; ".join([f"{where(h)}: \"{h['text']}\"" for h in hits] + let_through)
    elif unread_voice or unread_screen:
        result = "not checked"
        detail = (f"{unread_voice + unread_screen} of the reference's Voice and On screen cells are unknown (?); "
                  "fill the cells, or give --transcript to cover the speech"
                  + ("; " + "; ".join(let_through) if let_through else ""))
    else:
        result = "passed"
        detail = ("; ".join(let_through) or "our on-screen words are our own"
                  + (f" (allowed: {', '.join(allow)})" if allow else ""))
    results.append({"rule": "captions", "result": result, "hits": hits, "genre": genres, "detail": detail})
    if media is None:
        for rule in ("pictures", "sound"):
            results.append({"rule": rule, "result": "not checked", "hits": [],
                            "detail": "no media list given; list the reference's URLs and ours to check it"})
        return results
    reference = set(urls(media, "reference"))
    if not reference:
        raise sheets.InputError("media reference must list the reference video's URL and what was made from it")
    for rule, key, what in (("pictures", "generation_inputs", "generation input"), ("sound", "audio", "audio")):
        if media.get(key) is None:
            results.append({"rule": rule, "result": "not checked", "hits": [],
                            "detail": f"media has no {key} list; give [] when there is none"})
            continue
        reused = [u for u in urls(media, key) if u in reference]
        results.append({"rule": rule, "result": "failed" if reused else "passed", "hits": reused,
                        "detail": ", ".join(reused) + f" is the reference's, used as {what}" if reused
                        else f"no {what} comes from the reference"})
    return results


def report(sheet: Json, mapping: Json, transcript: Any = None, media: Optional[Json] = None,
           allow: Optional[List[str]] = None) -> Json:
    table = []
    for beat in mapping["beats"]:
        rows = ", ".join(beat["rows"]) or "—"
        table.append({"reference": f"{beat['index']}. {beat['beat']}",
                      "time": f"{sheets.seconds(beat['start'])}–{sheets.seconds(beat['end'])} s",
                      "ours": rows, "status": beat["status"], "reason": beat["reason"]})
    for row in mapping["rows"]:
        if row["status"] == "added":
            table.append({"reference": "—", "time": "—", "ours": row["id"], "status": "added",
                          "reason": row["beat"] or row["reason"]})
    content = rules(sheet, mapping, transcript, media, allow)
    counts = {s: sum(1 for b in mapping["beats"] if b["status"] == s) for s in ("matched", "changed", "dropped")}
    counts["added"] = len(mapping["added"])
    return {"reference": mapping.get("reference", ""), "counts": counts, "beats": table, "rules": content,
            "passed": all(r["result"] != "failed" for r in content)}


def markdown(result: Json) -> str:
    c = result["counts"]
    lines = [f"Reference {result['reference']}: {c['matched']} matched, {c['changed']} changed, "
             f"{c['dropped']} dropped, {c['added']} added.", "",
             "| Reference beat | Time | Our rows | Status | Reason |", "|---|---|---|---|---|"]
    for b in result["beats"]:
        lines.append("| " + " | ".join(sheets.escape(b[k]) or "—" for k in
                                         ("reference", "time", "ours", "status", "reason")) + " |")
    lines += ["", "| Content rule | Result | Detail |", "|---|---|---|"]
    for r in result["rules"]:
        lines.append(f"| {r['rule']} | {r['result']} | {sheets.escape(r['detail'])} |")
    return "\n".join(lines) + "\n"


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("sheet")
    parser.add_argument("mapping")
    parser.add_argument("--transcript")
    parser.add_argument("--media")
    parser.add_argument("--allow", action="append", default=[])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        sheet = sheets.check(sheets.load_sheet(args.sheet))
        mapping = sheets.load_json(args.mapping)
        if not isinstance(mapping, dict) or not isinstance(mapping.get("beats"), list) or not isinstance(mapping.get("rows"), list):
            raise sheets.InputError("the mapping must be map_structure.py's output")
        transcript = sheets.load_json(args.transcript) if args.transcript else None
        media = sheets.load_json(args.media) if args.media else None
        if media is not None and not isinstance(media, dict):
            raise sheets.InputError("media must be a JSON object")
        result = report(sheet, mapping, transcript, media, args.allow)
    except (OSError, ValueError) as exc:
        print("error: " + " ".join(str(exc).splitlines()), file=sys.stderr)
        return 2
    sys.stdout.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n" if args.json else markdown(result))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
