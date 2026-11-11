#!/usr/bin/env python3
"""
Compare a chosen look with its reference board, on the numbers a still can give.

    python3 scripts/look_check.py board.json look.json

Each file is a JSON list of stills, one object per still, with ffmpeg signalstats' 8-bit
readings: `YLOW` (the black point), `YHIGH` (the white point) and `SATAVG` (mean saturation).
A file may instead be an object with those stills under `stills`. The board is the reference
stills (references/film-look.md, the board), the look is the same frames graded with the chosen
look. It compares their medians and prints one JSON line:

    {"ok": bool, "items": [{"item", "board", "look", "gap", "tolerance", "verdict"}]}

`verdict` is `pass` within the tolerance, `flag` beyond it, and `open` when either side has no
reading for that item. It exits 0 when nothing is flagged and 1 when something is; input it
cannot read exits 2, with one line on stderr.

Python 3.9 or later, the standard library only, offline. It reads no media.
"""
from __future__ import annotations

import json
import sys
from statistics import median
from typing import Any, Dict, List, Optional

# item, signalstats key, tolerance in 8-bit levels, what a gap means
ITEMS = [
    ('blacks', 'YLOW', 8, 'the black point'),
    ('whites', 'YHIGH', 10, 'the white point'),
    ('saturation', 'SATAVG', 8, 'the mean saturation'),
]


class InputError(Exception):
    pass


def stills(data: Any, name: str) -> List[Dict[str, Any]]:
    if isinstance(data, dict):
        data = data.get('stills')
    if not isinstance(data, list) or not data:
        raise InputError(f'{name}: expected a non-empty list of stills, or an object with "stills"')
    if not all(isinstance(s, dict) for s in data):
        raise InputError(f'{name}: every still must be an object of signalstats readings')
    return data


def reading(values: List[Dict[str, Any]], key: str) -> Optional[float]:
    nums = [float(s[key]) for s in values if isinstance(s.get(key), (int, float)) and not isinstance(s.get(key), bool)]
    return round(median(nums), 2) if nums else None


def check(board: List[Dict[str, Any]], look: List[Dict[str, Any]]) -> Dict[str, Any]:
    items = []
    for item, key, tol, _ in ITEMS:
        b, l = reading(board, key), reading(look, key)
        if b is None or l is None:
            items.append({'item': item, 'board': b, 'look': l, 'gap': None, 'tolerance': tol, 'verdict': 'open'})
            continue
        gap = round(l - b, 2)
        items.append({'item': item, 'board': b, 'look': l, 'gap': gap, 'tolerance': tol,
                      'verdict': 'pass' if abs(gap) <= tol else 'flag'})
    return {'ok': not any(i['verdict'] == 'flag' for i in items), 'items': items}


def load(path: str) -> Any:
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError) as e:
        raise InputError(f'{path}: {e}') from e


def main(argv: List[str]) -> int:
    if len(argv) != 2:
        print('usage: look_check.py board.json look.json', file=sys.stderr)
        return 2
    try:
        result = check(stills(load(argv[0]), 'board'), stills(load(argv[1]), 'look'))
    except InputError as e:
        print(str(e), file=sys.stderr)
        return 2
    print(json.dumps(result))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
