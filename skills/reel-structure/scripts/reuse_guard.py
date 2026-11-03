#!/usr/bin/env python3
"""Report every run of 4 or more words the user's script shares with the reference.

    python3 scripts/reuse_guard.py reference script.md [--n 4]

The reference is the reference's words in any of these forms:
- picsart_media_transcribe's result (or its `transcript`);
- a JSON list of {start, end, text} entries;
- a structure sheet, JSON or Markdown: its Voice, On screen and Caption cells;
- plain text.
The script is Markdown or plain text, read whole: every table cell, with wrapped lines kept
consecutive. Quotes are straightened, case and punctuation dropped and whitespace collapsed
before comparing. Each shared run is reported once, at its longest, with the script line it
starts on.

Exits 1 for any shared run, 0 for none, 2 for bad input. Standard library only.
Ported from the channel team's tools/reuse_guard.py at commit 3f064f0.
"""
from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from collections import defaultdict
from typing import Any, Dict, List, Optional, Set, Tuple

import sheet as sheets

# Four shared consecutive words are the channel team's reuse limit.
DEFAULT_N = 4
# Apostrophes are dropped after straightening, so curly and straight contractions agree.
QUOTES = str.maketrans({"‘": "'", "’": "'", "ʼ": "'", "“": '"', "”": '"'})
# The sheet fields that hold the reference's own words. Caption is a style and timing, the
# pattern a copy may keep, so it is not compared.
WORD_FIELDS = ("voice", "on_screen")


def normalise(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).translate(QUOTES).lower().replace("'", "")
    return " ".join("".join(c if c.isalnum() or c.isspace() else " " for c in text).split())


def sheet_words(sheet: Dict[str, Any], fields: Tuple[str, ...] = WORD_FIELDS) -> str:
    """The reference's words in a sheet, field by field and a cell per line, so consecutive Voice
    cells stay one stream of speech with no on-screen text between them; a `?` or "none" cell is
    no words. A NUL separates fields so a shared run cannot cross between them."""
    return "\n\0\n".join("\n".join(b[f] for b in sheet["beats"] if sheets.said(b.get(f))) for f in fields)


def reference_text(value: Any) -> str:
    """The reference's words from a transcript, a transcript list, a sheet or text."""
    if isinstance(value, str):
        return value
    if isinstance(value, dict) and isinstance(value.get("beats"), list):
        return sheet_words(value)
    try:
        return " ".join(w["text"] for w in sheets.read_words(value))
    except sheets.InputError:
        raise ValueError("the reference must be a transcript, a list of {start, end, text}, a sheet or text")


def read_reference(path: str) -> str:
    with open(path, encoding="utf-8-sig") as handle:
        text = handle.read()
    if path.lower().endswith(".json"):
        return reference_text(json.loads(text))
    if path.lower().endswith((".md", ".markdown")):
        try:
            return sheet_words(sheets.parse_markdown(text))
        except sheets.InputError:
            return text
    return text


def find_hits(reference: str, script: str, n: int = DEFAULT_N) -> List[Dict[str, Any]]:
    if n < 1:
        raise ValueError("n must be at least 1")
    # A NUL is a field boundary, kept as a token that no normalised script word can match.
    original = [word for field in reference.split("\0") for word in normalise(field).split() + ["\0"]]
    words, lines = [], []
    for line, text in enumerate(script.splitlines(), 1):
        tokens = normalise(text).split()
        words.extend(tokens)
        lines.extend([line] * len(tokens))
    positions: Dict[Tuple[str, ...], List[int]] = defaultdict(list)
    for i in range(len(original) - n + 1):
        positions[tuple(original[i:i + n])].append(i)
    spans: Set[Tuple[int, int]] = set()
    for i in range(len(words) - n + 1):
        for j in positions.get(tuple(words[i:i + n]), ()):
            # A matching predecessor means this alignment was already extended from its start.
            if i and j and words[i - 1] == original[j - 1]:
                continue
            length = n
            while (i + length < len(words) and j + length < len(original)
                   and words[i + length] == original[j + length]):
                length += 1
            spans.add((i, i + length))
    hits, furthest = [], 0
    for start, end in sorted(spans, key=lambda span: (span[0], -span[1])):
        # A shorter run inside one already reported comes from another occurrence in the reference.
        if end <= furthest:
            continue
        furthest = end
        pieces: Dict[int, List[str]] = {}
        for k in range(start, end):
            pieces.setdefault(lines[k], []).append(words[k])
        hits.append({"line": lines[start], "end_line": lines[end - 1], "words": end - start,
                     "text": " ".join(words[start:end]), "pieces": [" ".join(p) for p in pieces.values()]})
    return hits


# Format labels nobody owns, shared by a genre: allowed on screen, and reported as such, never
# silently (channel team, 2026-11-02). Anything else a caption shares with the reference fails.
GENRE_PHRASES = ("get ready with me", "grwm", "pov", "storytime", "story time", "day in my life",
                 "what i eat in a day", "come with me")


def genre(hit: Dict[str, Any]) -> bool:
    """A hit that lies inside one of GENRE_PHRASES."""
    return allowed(hit, list(GENRE_PHRASES))


def allowed(hit: Dict[str, Any], phrases: List[str]) -> bool:
    """A hit that lies inside a phrase the user allowed (a genre's ritual line, say), word for word.

    A hit that runs across script lines is allowed when its part on each line is: two rows that
    each show an allowed phrase make one run, and each is still allowed."""
    wanted = [f" {normalise(p)} " for p in phrases if normalise(p)]
    return all(any(f" {piece} " in p for p in wanted) for piece in hit.get("pieces") or [hit["text"]])


def positive_int(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("n must be at least 1")
    return number


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("reference")
    parser.add_argument("script")
    parser.add_argument("--n", type=positive_int, default=DEFAULT_N)
    args = parser.parse_args(argv)
    try:
        reference = read_reference(args.reference)
        with open(args.script, encoding="utf-8-sig") as handle:
            script = handle.read()
        hits = find_hits(reference, script, args.n)
    except (OSError, ValueError) as exc:
        print("error: " + " ".join(str(exc).splitlines()), file=sys.stderr)
        return 2
    for hit in hits:
        print(f'{args.script}:{hit["line"]}: {hit["words"]} words: {hit["text"]}')
    if not hits:
        print(f"No shared runs of {args.n} or more words.")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
