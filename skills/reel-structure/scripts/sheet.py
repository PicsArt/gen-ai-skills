#!/usr/bin/env python3
"""The structure sheet: a reference reel's beats, as Markdown and as JSON.

    python3 scripts/sheet.py parse breakdown.md [--out sheet.json]
    python3 scripts/sheet.py validate sheet.json
    python3 scripts/sheet.py markdown sheet.json [--out sheet.md]
    python3 scripts/sheet.py draft --shots shots.json [--transcript t.json] [--describe d.json]
                                   [--audio a.json] [--probe p.json] [--out sheet.json]

The Markdown is one table, one row per beat, in the channel format:

    | Time (s) | Beat | What happens (picture) | Voice | On screen | Shot | Move | Caption | Sound |

A shorter breakdown (`| Time | Beat | What happens |`) parses too: the quoted lines in What
happens become Voice, or On screen when the words before them name a caption or a title. Header
lines above the table (`- Format: talking head`, `- Length: 65.1 s`, `- Cut rate: ~19 cuts/min
(note)`, `- Caption style: ...`, `- Bed: ...`, `- Loudness: ...`, `- Source: RB-44 (...)`) fill the
sheet's header; an indented line continues the one above it. Length, cut rate and loudness keep
their number, and the line as written as `<key>_note`. A document may hold several sheets
(`parse --all`): each table with a Time column, with the header lines since the table before it.

`?` is unknown, never a value and never malformed: a `?` time is a beat with null start and end,
a `?` cell (or "? (a note)") is kept as written and read as no words, and `?` in the header is
null. Mapping needs every beat timed and named, and says which are not.

A beat is named by its Beat cell: hook, stake, twist, joke run, feeling, reveal, turn, payoff,
CTA, intensifier or rehook, several joined by "+", or a name of the sheet's own ("Steps"). The
word `soft` in the cell marks a beat that starts mid-shot with no line: its edges are checked
within 1 s instead of 0.5 s. Consecutive rows with the same name ("reveal", "reveal (soft)",
"reveal") stay rows in the sheet and are one beat to the mapping and the report (merge_beats).

`draft` builds a sheet from the JSON the MCP tools returned, with no decoding here:
picsart_media_segment_shots' fragments set the shots (a short transition is a cut, a long one a
move inside the shot), picsart_media_transcribe's words fill Voice and split a long shot at its
sentences, picsart_media_describe_video's shots fill the picture, and picsart_media_analyze_audio's
tempo names the bed. Every field the tools cannot know is "?", and the beats are left to name.

Exits 0 when the sheet is valid, 1 with its problems, 2 on unreadable input. Standard library only.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

Json = Dict[str, Any]

# Column order and labels are the channel team's agreed structure-sheet format.
COLUMNS = (("Time (s)", "time"), ("Beat", "beat"), ("What happens (picture)", "picture"),
           ("Voice", "voice"), ("On screen", "on_screen"), ("Shot", "shot"), ("Move", "move"),
           ("Caption", "caption"), ("Sound", "sound"))
TEXT_FIELDS = ("picture", "voice", "on_screen", "shot", "move", "caption", "sound")
# Header labels a breakdown may use for each column, compared lower-case without markup.
ALIASES = {
    "time": "time", "time (s)": "time", "#": "id", "row": "id",
    "beat": "beat", "what happens (picture)": "picture", "what happens": "picture",
    "picture": "picture", "visual": "picture",
    "voice": "voice", "says": "voice",
    "on screen": "on_screen", "shot": "shot", "move": "move", "caption": "caption", "sound": "sound",
}
# The beat vocabulary: the channel's names and the retention-hooks skill's. Phrases map to one role.
ROLES = ("hook", "stake", "twist", "joke run", "feeling", "reveal", "turn", "payoff", "cta",
         "intensifier", "rehook")
ROLE_ALIASES = {"call to action": "cta", "re-hook": "rehook"}
HEADER_KEYS = {
    "format": "format", "total length": "total_length", "length": "total_length",
    "cut rate": "cut_rate", "caption style": "caption_style", "captions": "caption_style",
    "bed": "bed", "sound bed": "bed", "loudness": "loudness", "source": "source",
}
# A beat's edges are checked within this many seconds; a soft beat within the wider one.
TOLERANCE = 0.5
SOFT_TOLERANCE = 1.0
# A segment_shots transition at most this long is a cut; a longer one is a move inside the shot.
CUT_SECONDS = 0.25
# A shot longer than this may carry several spoken beats, split at its sentences.
LONG_SHOT_SECONDS = 4.0
# A pause this long ends a sentence even without punctuation.
SENTENCE_PAUSE = 0.8

NUMBER = r"\d+(?:\.\d+)?"
CLOCK = r"(?:\d+:)?\d+(?:\.\d+)?"
TIME_RANGE = re.compile(r"^~?\s*(" + CLOCK + r")\s*(?:s\b)?\s*[–—-]\s*~?\s*(" + CLOCK + r")\s*s?\s*$", re.I)
QUOTED = re.compile(r"\"([^\"]+)\"|“([^”]+)”")
ON_SCREEN_CUE = re.compile(r"\b(caption|captioned|title|text|on screen|plate|card)\b", re.I)
# A cell that says it holds no words: "none", alone or with a note ("none (voice only)", "none —
# music only"). A sentence that starts with the word ("None of these work") is words.
NO_WORDS = re.compile(r"^\s*none\s*[.!]?\s*(?:(?:\(.*\)|[—–].*)\s*)?$", re.I | re.S)


class InputError(ValueError):
    """Input the sheet cannot be read from; the message says what to change."""


# --- Markdown tables -------------------------------------------------------------------------

def split_cells(line: str) -> List[str]:
    """The cells of one Markdown table line, with `\\|` kept as a literal bar."""
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", body)]


def plain(text: str) -> str:
    """Cell text without bold or italic markers, with whitespace collapsed."""
    return " ".join(re.sub(r"(\*\*|__|(?<!\w)[*_]|[*_](?!\w))", "", text).split())


def tables(text: str) -> List[Tuple[int, List[str], List[List[str]]]]:
    """Every Markdown table: (line index of its header, header cells, body rows)."""
    lines, found, i = text.splitlines(), [], 0
    while i < len(lines):
        if (lines[i].lstrip().startswith("|") and i + 1 < len(lines)
                and re.match(r"^\s*\|?\s*:?-{2,}", lines[i + 1])):
            header, body, j = split_cells(lines[i]), [], i + 2
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                body.append(split_cells(lines[j]))
                j += 1
            found.append((i, header, body))
            i = j
        else:
            i += 1
    return found


def column_key(label: str) -> Optional[str]:
    name = plain(label).lower()
    if name in ALIASES:
        return ALIASES[name]
    if name.startswith("beat"):
        return "beat"
    if name.startswith("time"):
        return "time"
    return None


def parse_clock(value: str) -> float:
    if ":" in value:
        minutes, seconds = value.split(":", 1)
        return int(minutes) * 60 + float(seconds)
    return float(value)


def unknown(value: Any) -> bool:
    """A cell the sheet does not know: `?`, or `?` with a note ("? (unseen)"), or no value at all."""
    return value is None or (isinstance(value, str) and re.match(r"^\s*\?(\s|\(|$)", value) is not None)


def said(value: Any) -> bool:
    """A cell that holds words: neither unknown nor "none" (NO_WORDS)."""
    return isinstance(value, str) and bool(value.strip()) and not unknown(value) and not NO_WORDS.match(value)


def parse_time(cell: str, where: str) -> Tuple[Optional[float], Optional[float]]:
    """A row's start and end; (None, None) when its time is `?`."""
    if unknown(plain(cell)):
        return None, None
    match = TIME_RANGE.match(plain(cell))
    if not match:
        raise InputError(f"{where}: time {cell!r} is not a range like 1.9–8.7 s, or ?")
    return parse_clock(match.group(1)), parse_clock(match.group(2))


def time_tables(text: str) -> List[Tuple[int, int, List[Json], List[str]]]:
    """Every table with a Time column: (first line, line after it, rows keyed by field, warnings).

    Each row has `start` and `end` in seconds (None when `?`) and a string for every column it names.
    """
    found = []
    for line, header, body in tables(text):
        keys = [column_key(label) for label in header]
        if "time" not in keys:
            continue
        warnings = [f"column {label!r} is not part of the sheet and was left out"
                    for label, key in zip(header, keys) if key is None and plain(label)]
        rows = []
        for n, cells in enumerate(body, 1):
            row: Json = {}
            for key, cell in zip(keys, cells):
                if key and key not in row:
                    row[key] = cell
            row["start"], row["end"] = parse_time(row.pop("time", ""), f"row {n}")
            rows.append(row)
        found.append((line, line + 2 + len(body), rows, warnings))
    return found


def read_rows(text: str) -> Tuple[List[Json], List[str], int]:
    """The first table with a Time column, its warnings, and the line it starts on."""
    found = time_tables(text)
    if not found:
        raise InputError("no Markdown table with a Time column; a breakdown is one row per beat")
    line, _, rows, warnings = found[0]
    return rows, warnings, line


# --- Beat names ------------------------------------------------------------------------------

def phrase_in(phrase: str, text: str) -> bool:
    return re.search(r"(?<![\w-])" + re.escape(phrase) + r"(?![\w-])", text) is not None


def beat_roles(label: str, extra: Tuple[str, ...] = ()) -> List[str]:
    """The vocabulary roles a label names, in the order they appear in it."""
    text = plain(label).lower()
    found = []
    for phrase in ROLES + tuple(ROLE_ALIASES) + tuple(extra):
        for match in re.finditer(r"(?<![\w-])" + re.escape(phrase) + r"(?![\w-])", text):
            found.append((match.start(), ROLE_ALIASES.get(phrase, phrase)))
    roles = []
    for _, role in sorted(found):
        if role not in roles:
            roles.append(role)
    return roles


def name_beat(label: str) -> Tuple[List[str], bool]:
    """A Beat cell's roles and whether it is soft. A name outside the vocabulary is kept as its own role.

    An unknown cell names no role, whatever its note guesses ("? (hook or payoff)")."""
    text = plain(label)
    soft = phrase_in("soft", text.lower())
    if unknown(text):
        return [], soft
    roles = []
    for part in re.sub(r"\([^)]*\)", " ", text).split("+"):
        names = beat_roles(part)
        if not names:
            own = re.sub(r"\([^)]*\)", " ", part).lower()
            own = " ".join(re.sub(r"\bsoft\b", " ", own).replace("?", " ").split())
            names = [own] if own else []
        roles.extend(name for name in names if name not in roles)
    return roles, soft


def tolerance(beat: Json) -> float:
    return SOFT_TOLERANCE if beat.get("soft") else TOLERANCE


def merge_beats(beats: List[Json]) -> List[Json]:
    """The sheet's beats with consecutive rows of the same name joined into one.

    A reference often runs one beat over several rows (reveal, reveal (soft), reveal): the rows
    stay in the sheet, and the mapping and the report treat them as one beat from the first
    row's start to the last row's end. `rows` lists the sheet rows it joins, 1-based.
    """
    merged: List[Json] = []
    for n, beat in enumerate(beats, 1):
        last = merged[-1] if merged else None
        if last is not None and last["roles"] == beat["roles"]:
            last["end"] = beat["end"]
            last["rows"].append(n)
            last["soft"] = last["soft"] and bool(beat.get("soft"))
            continue
        name = beat.get("beat") or " + ".join(beat["roles"])
        merged.append({"start": beat["start"], "end": beat["end"], "roles": list(beat["roles"]),
                       "beat": " ".join(re.sub(r"\(\s*soft\s*\)|\bsoft\b", " ", name, flags=re.I).split()),
                       "soft": bool(beat.get("soft")), "rows": [n]})
    return merged


# --- Parsing a breakdown ---------------------------------------------------------------------

def split_quotes(picture: str) -> Tuple[str, str]:
    """Quoted lines of a What-happens cell: (spoken, on screen), by the words just before each."""
    voice, screen, last = [], [], 0
    for match in QUOTED.finditer(picture):
        quote = match.group(1) or match.group(2)
        before = re.split(r"[;.!?]\s|\)\s*", picture[last:match.start()])[-1]
        (screen if ON_SCREEN_CUE.search(before) else voice).append(quote.strip())
        last = match.end()
    return " ".join(voice), " ".join(screen)


# Header values that hold a number: the number is kept, and the line as written is its note.
NUMERIC_HEADERS = ("total_length", "cut_rate", "loudness")


def header_value(sheet: Json, key: str, value: str) -> None:
    if key not in NUMERIC_HEADERS:
        sheet[key] = value
        return
    match = re.match(r"^\s*~?\s*(-?" + NUMBER + r")\s*(.*)$", value)
    sheet[key] = float(match.group(1)) if match else None
    rest = match.group(2).strip() if match else value
    if rest and not re.fullmatch(r"(s|sec|seconds)", rest, re.I):
        sheet[key + "_note"] = value


def ident_of(text: str) -> Optional[str]:
    match = re.match(r"^([A-Za-z]+-?\d+)\s*[·:—-]", text)
    return match.group(1) if match else None


def read_header(lines: List[str], sheet: Json) -> None:
    """Title, id and `- Key: value` lines; an indented line continues the line above it."""
    pairs: List[List[str]] = []
    for raw in lines:
        heading = re.match(r"^#+\s*(.+?)\s*$", raw) or re.match(r"^\*\*(.+?)\*\*\s*$", raw)
        if heading:
            title = plain(heading.group(1))
            if ident_of(title):
                sheet["title"], sheet["id"] = title, ident_of(title)
            pairs.append([])
            continue
        pair = re.match(r"^\s*[-*]?\s*\**([A-Za-z ]+?)\**\s*:\s*(.+?)\s*$", raw)
        if pair and pair.group(1).strip().lower() in HEADER_KEYS and not raw.startswith("  "):
            pairs.append([HEADER_KEYS[pair.group(1).strip().lower()], pair.group(2)])
        elif raw.startswith("  ") and raw.strip() and pairs and pairs[-1]:
            pairs[-1][1] += " " + raw.strip()
        else:
            pairs.append([])
    for pair in pairs:
        if pair:
            header_value(sheet, pair[0], plain(pair[1]))
    if "id" not in sheet and isinstance(sheet.get("source"), str):
        source = re.match(r"^([A-Za-z]+-?\d+)\b", sheet["source"])
        if source:
            sheet["id"] = source.group(1)


def build_sheet(rows: List[Json], warnings: List[str], above: List[str], inherit: Json) -> Json:
    sheet: Json = {}
    read_header(above, sheet)
    # The sheet's own title or Source names it first; only a sheet with neither takes the first sheet's.
    if "id" not in sheet:
        sheet.update({k: inherit[k] for k in ("title", "id") if k in inherit and k not in sheet})
    beats = []
    for row in rows:
        label = row.get("beat", "")
        roles, soft = name_beat(label)
        beat: Json = {"start": row["start"], "end": row["end"], "beat": plain(label),
                      "roles": roles, "soft": soft}
        for field in TEXT_FIELDS:
            beat[field] = plain(row.get(field, ""))
        if "voice" not in row and beat["picture"] and unknown(beat["picture"]):
            # A picture nobody has seen says nothing of its words: they stay unread, never empty.
            beat["voice"] = "?"
            if not beat["on_screen"]:
                beat["on_screen"] = "?"
        elif "voice" not in row and beat["picture"]:
            voice, screen = split_quotes(beat["picture"])
            beat["voice"] = voice
            if not beat["on_screen"]:
                beat["on_screen"] = screen
        beat["pace"] = pace("" if unknown(beat["voice"]) else beat["voice"], beat["start"], beat["end"])
        beats.append(beat)
    sheet["beats"] = beats
    ends = [b["end"] for b in beats if finite(b["end"])]
    if "total_length" not in sheet and ends:
        sheet["total_length"] = max(ends)
    sheet["warnings"] = warnings
    return sheet


def parse_sheets(text: str) -> List[Json]:
    """Every sheet in a document: each table with a Time column, with the header lines above it."""
    lines, sheets, previous, inherit = text.splitlines(), [], 0, {}
    for start, end, rows, warnings in time_tables(text):
        sheet = build_sheet(rows, warnings, lines[previous:start], inherit)
        if not sheets:
            inherit = {k: sheet[k] for k in ("title", "id") if k in sheet}
        sheets.append(sheet)
        previous = end
    if not sheets:
        raise InputError("no Markdown table with a Time column; a breakdown is one row per beat")
    return sheets


def parse_markdown(text: str) -> Json:
    """A breakdown's first sheet, with its warnings under `warnings`."""
    return parse_sheets(text)[0]


def pace(voice: str, start: Optional[float], end: Optional[float]) -> Optional[float]:
    """Spoken words a second over the beat, or None when nothing is said or the time is unknown."""
    if not said(voice) or not finite(start) or not finite(end) or end <= start:
        return None
    return round(len(re.findall(r"[\w’']+", voice)) / (end - start), 2)


# --- Validation ------------------------------------------------------------------------------

def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def validate(sheet: Any) -> List[str]:
    """Every problem with a sheet, as one sentence each; empty when it is valid.

    `?` is unknown, not malformed: a beat whose time is unknown has start and end null, and
    its text cells may read `?`. Only what is written must be well formed.
    """
    if not isinstance(sheet, dict):
        return ["the sheet must be a JSON object with a beats list"]
    beats = sheet.get("beats")
    if not isinstance(beats, list) or not beats:
        return ["the sheet has no beats; it needs one row per beat"]
    problems = []
    for key in ("format", "caption_style", "bed", "title", "id", "source") + tuple(k + "_note" for k in NUMERIC_HEADERS):
        if key in sheet and not isinstance(sheet[key], (str, int, float)):
            problems.append(f"header {key} must be text or a number")
    for key in ("cut_rate", "loudness"):
        if sheet.get(key) is not None and not isinstance(sheet[key], (str, int, float)):
            problems.append(f"header {key} must be a number, or null when unknown")
    total = sheet.get("total_length")
    if total is not None and (not finite(total) or total <= 0):
        problems.append("total_length must be a positive number of seconds, or null when unknown")
    previous = None
    for n, beat in enumerate(beats, 1):
        where = f"beat {n}"
        if not isinstance(beat, dict):
            problems.append(f"{where} must be an object")
            continue
        start, end = beat.get("start"), beat.get("end")
        known = start is not None or end is not None
        if known and (not finite(start) or not finite(end) or not 0 <= start < end):
            problems.append(f"{where}: start and end must be seconds with 0 <= start < end, or both null")
            continue
        when = f" ({start:g}–{end:g} s)" if known else ""
        roles = beat.get("roles")
        if not isinstance(roles, list) or not all(isinstance(r, str) and r.strip() for r in roles):
            problems.append(f"{where}{when}: roles must be a list of beat names (empty when `?`)")
        if "soft" in beat and not isinstance(beat["soft"], bool):
            problems.append(f"{where}: soft must be true or false")
        for field in TEXT_FIELDS + ("beat",):
            if field in beat and not isinstance(beat[field], str):
                problems.append(f"{where}: {field} must be text")
        if beat.get("pace") is not None and (not finite(beat["pace"]) or beat["pace"] < 0):
            problems.append(f"{where}: pace must be words a second")
        if not known:
            continue
        if previous is not None and start < previous - 1e-6:
            problems.append(f"{where} starts at {start:g} s, before the beat before it ends at {previous:g} s;"
                            " beats run in order and never overlap")
        if finite(total) and end > total + 1e-6:
            problems.append(f"{where} ends at {end:g} s, after the total length {total:g} s")
        previous = end
    return problems


def check(sheet: Any) -> Json:
    problems = validate(sheet)
    if problems:
        raise InputError("; ".join(problems))
    return sheet


def timed(sheet: Json) -> Json:
    """A valid sheet whose every beat has a time: what mapping and comparing need."""
    check(sheet)
    missing = [n for n, b in enumerate(sheet["beats"], 1) if b.get("start") is None]
    if missing:
        raise InputError(f"beats {', '.join(map(str, missing))} have no time (?); "
                         "time them from the reference before mapping onto it")
    unnamed = [n for n, b in enumerate(sheet["beats"], 1) if not b["roles"]]
    if unnamed:
        raise InputError(f"beats {', '.join(map(str, unnamed))} have no beat name (?); "
                         "name each, e.g. hook or payoff, before mapping onto it")
    return sheet


def compare(expected: Json, actual: Json) -> List[Json]:
    """Each expected beat against the actual beat with the same name in order, edge by edge.

    Rows of one name are joined first (merge_beats). A beat matches when both its edges land
    within its tolerance: 0.5 s, or 1 s when either side is soft.
    """
    results, pointer = [], 0
    beats = merge_beats(timed(actual)["beats"])
    for n, beat in enumerate(merge_beats(timed(expected)["beats"]), 1):
        found = next((j for j in range(pointer, len(beats))
                      if set(beats[j]["roles"]) & set(beat["roles"])), None)
        if found is None:
            results.append({"beat": n, "name": beat["beat"], "found": False, "within": False})
            continue
        pointer = found + 1
        other = beats[found]
        limit = max(tolerance(beat), tolerance(other))
        off = max(abs(other["start"] - beat["start"]), abs(other["end"] - beat["end"]))
        results.append({"beat": n, "name": beat["beat"], "found": True, "off": round(off, 3),
                        "tolerance": limit, "within": off <= limit + 1e-9})
    return results


# --- Writing Markdown ------------------------------------------------------------------------

def seconds(value: float) -> str:
    return f"{round(value, 2):g}"


def escape(text: str) -> str:
    return " ".join(str(text).split()).replace("|", "\\|")


def markdown(sheet: Json) -> str:
    lines = []
    if sheet.get("title"):
        lines += [f"## {sheet['title']}", ""]
    header = [("Format", "format"), ("Length", "total_length"), ("Cut rate", "cut_rate"),
              ("Caption style", "caption_style"), ("Bed", "bed"), ("Loudness", "loudness"), ("Source", "source")]
    shown = []
    for label, key in header:
        value = sheet.get(key + "_note", sheet.get(key))
        if key == "total_length" and key + "_note" not in sheet and finite(value):
            value = f"{seconds(value)} s"
        elif key in NUMERIC_HEADERS and key + "_note" not in sheet and finite(value):
            value = seconds(value)
        if value is None and key in NUMERIC_HEADERS and key in sheet:
            value = "?"
        if value not in (None, ""):
            shown.append(f"- {label}: {value}")
    lines += shown + ([""] if shown else [])
    lines.append("| " + " | ".join(label for label, _ in COLUMNS) + " |")
    lines.append("|" + "---|" * len(COLUMNS))
    for beat in sheet["beats"]:
        name = beat.get("beat") or " + ".join(beat.get("roles") or []) or "?"
        if beat.get("soft") and not phrase_in("soft", name.lower()):
            name += " (soft)"
        time = "?" if beat.get("start") is None else f"{seconds(beat['start'])}–{seconds(beat['end'])}"
        cells = [time, name] + [beat.get(field, "") for field in TEXT_FIELDS]
        lines.append("| " + " | ".join(escape(c) for c in cells) + " |")
    return "\n".join(lines) + "\n"


# --- A draft from the tools' results ---------------------------------------------------------

def unwrap(value: Any, key: str) -> Any:
    """A tool's result as returned, or the same result inside a job status's `result`."""
    if isinstance(value, dict) and key not in value and isinstance(value.get("result"), dict):
        return value["result"]
    return value


def read_fragments(shots: Any) -> List[Json]:
    shots = unwrap(shots, "fragments")
    fragments = shots.get("fragments") if isinstance(shots, dict) else shots
    if not isinstance(fragments, list) or not fragments:
        raise InputError("shots must be the picsart_media_segment_shots result, with fragments")
    out = []
    for n, f in enumerate(fragments, 1):
        if not isinstance(f, dict) or not finite(f.get("t0")) or not finite(f.get("t1")) or f["t0"] >= f["t1"]:
            raise InputError(f"fragment {n} needs numeric t0 < t1")
        out.append({"t0": float(f["t0"]), "t1": float(f["t1"]), "kind": str(f.get("kind", "hold"))})
    return sorted(out, key=lambda f: f["t0"])


def read_words(transcript: Any) -> List[Json]:
    """Timed words or phrases from picsart_media_transcribe's result, or from a list of {start, end, text}."""
    transcript = unwrap(transcript, "transcript")
    if isinstance(transcript, dict) and isinstance(transcript.get("transcript"), dict):
        transcript = transcript["transcript"]
    if isinstance(transcript, dict) and isinstance(transcript.get("segments"), list):
        entries = []
        for seg in transcript["segments"]:
            if not isinstance(seg, dict):
                raise InputError("transcript segments must be objects")
            tokens = str(seg.get("text") or "").split()
            timed = seg.get("words") or []
            if timed and len(timed) == len(tokens):
                entries += [{"start": w.get("start"), "end": w.get("end"), "text": t}
                            for t, w in zip(tokens, timed)]
            elif tokens:
                entries.append({"start": seg.get("start"), "end": seg.get("end"), "text": " ".join(tokens)})
    elif isinstance(transcript, list):
        entries = transcript
    else:
        raise InputError("transcript must be the picsart_media_transcribe result or a list of {start, end, text}")
    words = []
    for entry in entries:
        if (not isinstance(entry, dict) or not isinstance(entry.get("text"), str)
                or not finite(entry.get("start")) or not finite(entry.get("end"))
                or not 0 <= entry["start"] <= entry["end"]):
            raise InputError("transcript entries need numeric 0 <= start <= end and string text")
        if entry["text"].strip():
            words.append({"start": float(entry["start"]), "end": float(entry["end"]),
                          "text": " ".join(entry["text"].split())})
    return sorted(words, key=lambda w: w["start"])


def sentences(words: List[Json]) -> List[List[Json]]:
    groups: List[List[Json]] = []
    for word in words:
        if (not groups or re.search(r"[.!?][\"'’”]*$", groups[-1][-1]["text"])
                or word["start"] - groups[-1][-1]["end"] >= SENTENCE_PAUSE):
            groups.append([])
        groups[-1].append(word)
    return groups


def shots_from(fragments: List[Json], duration: float) -> List[Tuple[float, float, bool]]:
    """(start, end, moves) per shot: a short transition is a cut at its middle; a long one a move."""
    cuts, moving = [], []
    for f in fragments:
        if f["kind"] == "transition":
            if f["t1"] - f["t0"] <= CUT_SECONDS:
                cuts.append((f["t0"] + f["t1"]) / 2)
            else:
                moving.append((f["t0"], f["t1"]))
    start = fragments[0]["t0"]
    for left, right in zip(fragments, fragments[1:]):
        # Two holds that meet with no transition between them meet at a cut.
        if left["kind"] == "hold" and right["kind"] == "hold":
            cuts.append(right["t0"])
    bounds = [start] + sorted(c for c in set(round(c, 3) for c in cuts) if start < c < duration) + [duration]
    return [(a, b, any(m0 < b and m1 > a for m0, m1 in moving)) for a, b in zip(bounds, bounds[1:])]


def draft(shots: Any, transcript: Any = None, describe: Any = None, audio: Any = None,
          probe: Any = None) -> Json:
    fragments = read_fragments(shots)
    words = read_words(transcript) if transcript is not None else []
    duration = fragments[-1]["t1"]
    probe = unwrap(probe, "durationSeconds")
    if isinstance(probe, dict) and finite(probe.get("durationSeconds")):
        duration = min(duration, float(probe["durationSeconds"])) if duration > fragments[0]["t0"] else duration
    groups = sentences(words)
    beats = []
    for shot, (start, end, moves) in enumerate(shots_from(fragments, duration), 1):
        breaks: List[float] = []
        if end - start > LONG_SHOT_SECONDS:
            spoken = [g for g in groups if any(start <= w["start"] < end for w in g)]
            # Sentences may start together (a zero-length word): one boundary each, never a zero-length beat.
            breaks = sorted({round(g[0]["start"], 3) for g in spoken[1:]} - {round(start, 3), round(end, 3)})
            breaks = [b for b in breaks if start < b < end]
        edges = [start] + breaks + [end]
        for left, right in zip(edges, edges[1:]):
            voice = " ".join(w["text"] for w in words if left <= w["start"] < right
                             or w["start"] == w["end"] == right == duration)
            beats.append({"start": round(left, 3), "end": round(right, 3), "beat": "?", "roles": [],
                          "soft": False, "picture": "?", "voice": voice, "on_screen": "?",
                          "shot": f"S{shot}", "move": "move" if moves else "static",
                          "caption": "?", "sound": "?", "pace": pace(voice, left, right)})
    described = unwrap(describe, "shots")
    for d in (described.get("shots") or []) if isinstance(described, dict) else []:
        if not isinstance(d, dict) or not finite(d.get("start")) or not finite(d.get("end")):
            continue
        for beat in beats:
            overlap = min(beat["end"], d["end"]) - max(beat["start"], d["start"])
            if overlap > (beat["end"] - beat["start"]) / 2 and beat["picture"] == "?":
                beat["picture"] = " ".join(str(d.get("description") or "?").split())
    shot_count = len({b["shot"] for b in beats})
    length = duration - fragments[0]["t0"]
    sheet: Json = {"format": "?", "total_length": round(duration, 3),
                   "cut_rate": round((shot_count - 1) * 60 / length) if length > 0 else None,
                   "cut_rate_note": f"{(shot_count - 1) * 60 / length:.0f} cuts/min" if length > 0 else "?",
                   "caption_style": "?", "bed": "?", "beats": beats}
    analysis = unwrap(audio, "tempo")
    tempo = analysis.get("tempo") if isinstance(analysis, dict) else None
    if isinstance(tempo, dict) and finite(tempo.get("bpm")):
        sheet["bed"] = f"? ({tempo['bpm']:.0f} bpm)"
    return sheet


# --- Command line ----------------------------------------------------------------------------

def load_json(path: str) -> Any:
    try:
        with open(path, encoding="utf-8-sig") as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:
        raise InputError(f"{path} is not JSON: {exc}")


def load_sheet(path: str) -> Json:
    if path.lower().endswith((".md", ".markdown", ".txt")):
        with open(path, encoding="utf-8-sig") as handle:
            return parse_markdown(handle.read())
    return load_json(path)


def emit(text: str, out: Optional[str]) -> None:
    if out:
        with open(out, "w", encoding="utf-8") as handle:
            handle.write(text)
    else:
        sys.stdout.write(text)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("parse", help="Markdown breakdown to JSON sheet")
    p.add_argument("breakdown")
    p.add_argument("--all", action="store_true", help="every sheet in the document, as a JSON list")
    p.add_argument("--out")
    v = sub.add_parser("validate", help="check a JSON or Markdown sheet")
    v.add_argument("sheet")
    m = sub.add_parser("markdown", help="JSON sheet to Markdown")
    m.add_argument("sheet")
    m.add_argument("--out")
    d = sub.add_parser("draft", help="a draft sheet from the MCP tools' JSON results")
    d.add_argument("--shots", required=True)
    for name in ("transcript", "describe", "audio", "probe", "out"):
        d.add_argument("--" + name)
    args = parser.parse_args(argv)
    try:
        if args.command == "parse" and args.all:
            with open(args.breakdown, encoding="utf-8-sig") as handle:
                found = parse_sheets(handle.read())
            emit(json.dumps(found, ensure_ascii=False, indent=2) + "\n", args.out)
            problems = [f"sheet {n}: {p}" for n, s in enumerate(found, 1) for p in validate(s)]
        elif args.command == "parse":
            sheet = load_sheet(args.breakdown)
            emit(json.dumps(sheet, ensure_ascii=False, indent=2) + "\n", args.out)
            problems = validate(sheet)
        elif args.command == "validate":
            problems = validate(load_sheet(args.sheet))
            if not problems:
                print("The sheet is valid.")
        elif args.command == "markdown":
            sheet = load_sheet(args.sheet)
            problems = validate(sheet)
            if not problems:
                emit(markdown(sheet), args.out)
        else:
            optional = {k: load_json(getattr(args, k)) for k in ("transcript", "describe", "audio", "probe")
                        if getattr(args, k)}
            sheet = draft(load_json(args.shots), **optional)
            emit(json.dumps(sheet, ensure_ascii=False, indent=2) + "\n", args.out)
            problems = []
    except (OSError, InputError) as exc:
        print("error: " + " ".join(str(exc).splitlines()), file=sys.stderr)
        return 2
    for problem in problems:
        print("problem: " + problem, file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
