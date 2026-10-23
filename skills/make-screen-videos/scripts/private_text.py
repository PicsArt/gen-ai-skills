#!/usr/bin/env python3
"""
Find private data in the text a recording shows or says: emails, keys and tokens, phone numbers
and card numbers.

    python3 scripts/private_text.py input.json
    python3 scripts/private_text.py < input.json

The input is one JSON object:

    {"texts": [{"text": "Signed in as ana@studio.io", "at": 12.4, "box": {"x": 1210, "y": 18, "w": 260, "h": 28}, "from": "still"},
               {"text": "my key is sk-live-...", "at": 40.2, "from": "transcript"}]}

- `texts`: every piece of text you read, one entry each: `text`, and where it was, as you know it:
  `at` (the recording's second), `box` (its box in source px, from the still), `from` (`still`,
  `transcript`, or what you read it in). A plain string is an entry with only its text.

The patterns:

- `email`: an address, name@domain.tld;
- `key`: an API key or secret by its known shape: `sk-`, `sk_live_`, `pk_live_`, `ghp_`,
  `github_pat_`, `glpat-`, `xoxb-`, `AKIA`, `AIza`, `hf_`, a private key block, or a value after
  `key`, `token`, `secret` or `password`, quoted or not (`"password": "..."`);
- `token`: a JSON web token, or a long run of letters and digits that looks random;
- `card`: 13 to 19 digits that pass the Luhn check;
- `phone`: 9 to 15 digits with a leading + or with separators, as a phone number is written.

A run of digit groups can hold several fields (a card and its expiry, two phone numbers side by
side): each one is found on its own. Cards are read twice, as written and with dates as field
boundaries, and every card either reading finds is masked: a neighbouring number may be masked
with a card, but no card digit is left out.

It prints one JSON line, `{ok, hits, counts}`; `ok` is true when there is no hit. Each hit has the
`kind`, the `entry` it was found in (its index in `texts`), that entry's `at`, `box` and `from`,
and the match `masked`, with only its first and last two characters kept, so the secret is not
repeated. Patterns miss things and flag a few that are not private: what it finds is checked on
the still, and what it does not find is not proof. Input it cannot read exits 1, with one line on
stderr that says what is wrong.

Python 3.9 or later, the standard library only, offline.
"""
from __future__ import annotations

import json
import re
import sys
from typing import Any, Dict, List, Tuple

EMAIL = re.compile(r'(?<![\w.+-])[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}(?![\w-])')
KEYS = [re.compile(p) for p in (
    r'\bsk-(?:proj-|live-|test-)?[A-Za-z0-9_-]{16,}',
    r'\b[spr]k_(?:live|test)_[A-Za-z0-9]{10,}',
    r'\bgh[pousr]_[A-Za-z0-9]{20,}',
    r'\bgithub_pat_[A-Za-z0-9_]{20,}',
    r'\bglpat-[A-Za-z0-9_-]{20,}',
    r'\bxox[abprs]-[A-Za-z0-9-]{10,}',
    r'\b(?:AKIA|ASIA)[0-9A-Z]{16}\b',
    r'\bAIza[0-9A-Za-z_-]{35}',
    r'\bhf_[A-Za-z0-9]{30,}',
    r'-----BEGIN [A-Z ]*PRIVATE KEY-----',
    r'(?i)\b(?:api[_ -]?key|access[_ -]?key|key|secret|token|password|passwd|pwd)\b["\']?\s*[:=]\s*'
    # A quoted value may hold spaces; a cut-off one (no closing quote) is still a value.
    r'(?:"(?:\\.|[^"\\]){8,}(?:"|$)|\'(?:\\.|[^\'\\]){8,}(?:\'|$)|["\']?[^\s"\']{8,})',
)]
JWT = re.compile(r'\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}')
RANDOM = re.compile(r'(?<![\w/.-])[A-Za-z0-9_+/=-]{32,}(?![\w/.-])')
# Between digits: horizontal whitespace, and at most one line break or hyphen, so a run never swallows a table.
CARD = re.compile(r'(?<!\d)(?:\d(?:[^\S\r\n]*(?:(?:\r?\n|[\r-])[^\S\r\n]*)?)){12,}\d(?!\d)')
# A real date: one separator used twice, month and day in range, and no digit group hyphen-joined to
# either side, so a card's last group is never read as its year.
DATE = re.compile(r'(?<!\d)(?<!\d[-/.])(?:\d{4}([-/.])(?:0?[1-9]|1[0-2])\1(?:0?[1-9]|[12]\d|3[01])'
                  r'|(?:0?[1-9]|[12]\d|3[01])([/.])(?:0?[1-9]|[12]\d|3[01])\2\d{4})(?!\d)(?![-/.]\d)')
LONGEST = 19
PHONE = re.compile(r'(?<![\w+])\+?\(?\d[\d ().-]{7,}\d(?!\w)')

USAGE = 'usage: private_text.py [input.json]; with no file, the input is read from stdin'


class InputError(ValueError):
    """Input the script cannot read, with the reason."""


def luhn(digits: str) -> bool:
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2:
            d = d * 2 - 9 if d > 4 else d * 2
        total += d
    return total % 10 == 0


def looks_random(s: str) -> bool:
    """Letters and digits mixed, many distinct, not one word repeated: a token, not a path."""
    has_digit = any(c.isdigit() for c in s)
    has_alpha = any(c.isalpha() for c in s)
    return has_digit and has_alpha and len(set(s)) >= 12


def mask(s: str) -> str:
    s = s.strip()
    return s[:2] + '*' * max(3, len(s) - 4) + s[-2:] if len(s) > 6 else '*' * len(s)


def card_digits(s: str) -> bool:
    digits = re.sub(r'\D', '', s)
    return 13 <= len(digits) <= 19 and luhn(digits)


def is_card(s: str) -> bool:
    """Luhn-valid digits written as a card is: unbroken, in fours (the last group shorter), or 4-6-5."""
    groups = [len(g) for g in re.split(r'[\s-]+', s)]
    written = len(groups) == 1 or all(g == 4 for g in groups[:-1]) and 1 <= groups[-1] <= 4 or groups in ([4, 6, 5], [4, 6, 4])
    return written and card_digits(s)


def is_phone(s: str) -> bool:
    digits = re.sub(r'\D', '', s)
    written = s.startswith('+') or bool(re.search(r'[ ().-]', s))
    return 9 <= len(digits) <= 15 and written and not re.fullmatch(r'\d{4}[-./]\d{1,2}[-./]\d{1,2}', s.strip())


def pieces(text: str, m: 're.Match[str]', ok: Any) -> List[Tuple[int, int]]:
    """
    The cards inside one greedy run of digit groups, of any length. The run can hold several fields,
    a card and its expiry or two phone numbers side by side, so each window of whole groups is
    tried at each starting group, longest first, rather than only the run as a whole: a card's expiry
    stays out of the card.
    """
    runs = [(m.start() + g.start(), m.start() + g.end()) for g in re.finditer(r'\d+', m.group(0))]
    found: List[Tuple[int, int]] = []
    i = 0
    while i < len(runs):
        # No card has more than LONGEST digits: longer windows are never tried, so this stays linear.
        last, digits = i, runs[i][1] - runs[i][0]
        while last + 1 < len(runs) and digits + runs[last + 1][1] - runs[last + 1][0] <= LONGEST:
            last += 1
            digits += runs[last][1] - runs[last][0]
        for j in range(last, i - 1, -1):
            if digits < 13:
                break
            a, b = runs[i][0], runs[j][1]
            while a > m.start() and text[a - 1] in '+(':
                a -= 1
            if b < m.end() and text[b] == ')' and '(' in text[a:b]:
                b += 1
            if ok(text[a:b]):
                found.append((a, b))
                break
            digits -= runs[j][1] - runs[j][0]
        i += 1
    return found


def phone_pieces(text: str, m: 're.Match[str]') -> List[Tuple[int, int]]:
    """
    The phone numbers in one greedy run. The run as a whole first, as it is written. When it is
    too long to be one number, the run is split at its spaces and each shortest stretch of whole
    pieces that is a number on its own is a hit: two numbers side by side, or a date before one.
    Such a stretch needs a dash, a dot or brackets in it, a leading + or a group that is not four
    digits, so digits in fours, as a card is written, are never read as phones.
    """
    if is_phone(m.group(0)):
        return [(m.start(), m.end())]
    chunks = [(m.start() + c.start(), m.start() + c.end()) for c in re.finditer(r'\S+', m.group(0))]
    found: List[Tuple[int, int]] = []
    i = 0
    while i < len(chunks):
        nxt = i + 1
        for j in range(i, len(chunks)):
            a, b = chunks[i][0], chunks[j][1]
            s = text[a:b]
            if sum(c.isdigit() for c in s) > LONGEST:
                break
            if (s.startswith('+') or re.search(r'[().-]', s) or any(len(g) != 4 for g in s.split())) and is_phone(s):
                found.append((a, b))
                nxt = j + 1
                break
        i = nxt
    return found


def scan(text: str) -> List[Tuple[str, str]]:
    """Each hit in one text, as (kind, match), without counting an identical span twice."""
    taken: List[Tuple[int, int]] = []
    hits: List[Tuple[int, str, str]] = []

    def free(a: int, b: int) -> bool:
        return all(b <= x or a >= y for x, y in taken)

    def add_span(kind: str, a: int, b: int) -> None:
        # Overlapping Luhn-valid cards are ambiguous: keep each candidate, once. A phone may
        # overlap them too, so that two readings of one run each mask their digits.
        overlap = kind in ('card', 'phone') and all(k in ('card', 'phone') or b <= x or a >= x + len(s) for x, k, s in hits)
        if (free(a, b) or overlap) and (a, kind, text[a:b]) not in hits:
            taken.append((a, b))
            hits.append((a, kind, text[a:b]))

    def add(kind: str, m: 're.Match[str]') -> None:
        add_span(kind, m.start(), m.end())

    for pattern in KEYS:
        for m in pattern.finditer(text):
            add('key', m)
    for m in JWT.finditer(text):
        add('token', m)
    for m in EMAIL.finditer(text):
        add('email', m)
    for m in RANDOM.finditer(text):
        if looks_random(m.group(0)):
            add('token', m)
    phones = [span for m in PHONE.finditer(text) for span in phone_pieces(text, m)]

    def phone_digits(a: int, b: int, strict: bool) -> bool:
        covering = [(x, y) for x, y in phones if x < b and a < y]
        # The permissive phone detector also finds chunks of unusually grouped cards.
        # In the strict pass only recognizable phone groups may veto a Luhn-valid card window.
        for x, y in covering if strict else []:
            s = text[x:y]
            groups = [len(g) for g in re.findall(r'\d+', s)]
            if max(groups) > 4 or not (s.startswith('+') or re.search(r'[().-]', s) or groups in ([3, 3, 4], [1, 3, 3, 4], [3, 4, 4], [4, 3, 4])):
                return False
        # Adjacent fields can join parts of separate phones into a Luhn-valid window. Only
        # suppress partial phone windows, never a complete card split into phone-shaped chunks.
        # When neither phone is wholly inside the window, require explicit phone punctuation
        # in each one: space-only chunks can instead be an OCR-merged card beside other fields.
        return len(covering) > 1 and (any(a <= x and y <= b for x, y in covering) or all(re.search(r'[().-]', text[x:y]) for x, y in covering)) and any(x < a or y > b for x, y in covering) and all(any(x <= i < y for x, y in covering) for i in range(a, b) if text[i].isdigit())

    # Two passes, and every card either finds is kept: masking more is safe, masking less leaks.
    # The first reads the text as written. The second treats dates as field boundaries, never
    # digits to borrow for a Luhn window (offsets unchanged, so windows still refer to the text),
    # and lets only recognizable phones veto a window.
    def masked(spans: List[Tuple[int, int]]) -> str:
        remaining = list(text)
        for a, b in spans:
            remaining[a:b] = '|' * (b - a)
        return ''.join(remaining)

    # Each pass reads the phones left beside its own cards, as if it ran alone: one pass's
    # cards can split a phone the other finds, and that phone may be what masks the rest of a card.
    others = list(taken)
    readings = []
    for card_text, strict in ((text, False), (DATE.sub(lambda m: '|' * len(m.group(0)), text), True)):
        own: List[Tuple[int, int]] = []
        for m in CARD.finditer(card_text):
            # OCR merges a card's groups ('41111111 11111111'): beside the card-shaped windows, any
            # other window of whole groups whose 13-19 digits pass Luhn is a card, however it is
            # grouped.
            complete = card_digits(m.group(0))
            for a, b in pieces(text, m, is_card) + [w for w in pieces(text, m, card_digits) if complete or not phone_digits(*w, strict)]:
                add_span('card', a, b)
                if (a, 'card', text[a:b]) in hits:
                    own.append((a, b))
        readings.append(masked(others + own))
    cards = [(a, a + len(s)) for a, k, s in hits if k == 'card']
    for remaining in readings:
        for a, b in [span for m in PHONE.finditer(remaining) for span in phone_pieces(text, m)]:
            # A phone that only repeats a card's digits adds nothing: the card already masks them.
            if any(text[i].isdigit() and not any(x <= i < y for x, y in cards) for i in range(a, b)):
                add_span('phone', a, b)
    return [(kind, match) for _, kind, match in sorted(hits)]


def run(data: Any) -> Dict[str, Any]:
    """The script's whole job: the checked input in, the line it prints out."""
    if not isinstance(data, dict) or not isinstance(data.get('texts'), list):
        raise InputError('the input must be one JSON object with a texts list')
    hits: List[Dict[str, Any]] = []
    for i, entry in enumerate(data['texts']):
        if isinstance(entry, str):
            entry = {'text': entry}
        if not isinstance(entry, dict) or not isinstance(entry.get('text'), str):
            raise InputError(f'texts[{i}] must be a string, or an object with a text')
        for kind, match in scan(entry['text']):
            hit: Dict[str, Any] = {'kind': kind, 'entry': i, 'masked': mask(match)}
            for key in ('at', 'box', 'from'):
                if entry.get(key) is not None:
                    hit[key] = entry[key]
            hits.append(hit)
    counts: Dict[str, int] = {}
    for h in hits:
        counts[h['kind']] = counts.get(h['kind'], 0) + 1
    return {'ok': not hits, 'hits': hits, 'counts': counts}


def main(argv: List[str]) -> int:
    if len(argv) > 1 or any(a.startswith('-') for a in argv):
        return fail(USAGE, 2)
    try:
        if argv:
            with open(argv[0], encoding='utf-8-sig') as f:
                text = f.read()
        else:
            text = sys.stdin.buffer.read().decode('utf-8-sig')
    except (OSError, UnicodeDecodeError) as err:
        return fail(f'cannot read the input: {err}')
    try:
        out = run(json.loads(text))
    except json.JSONDecodeError as err:
        return fail(f'the input is not JSON: {err}')
    except InputError as err:
        return fail(str(err))
    sys.stdout.buffer.write((json.dumps(out, separators=(',', ':')) + '\n').encode('utf-8'))
    return 0


def fail(reason: str, code: int = 1) -> int:
    sys.stderr.write('private_text.py: ' + ' '.join(reason.split()) + '\n')
    return code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
