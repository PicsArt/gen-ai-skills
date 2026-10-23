#!/usr/bin/env python3
"""
Frame a recording in a panel: the layer transform that shows source point F on the panel's centre
at total scale S.

    python3 scripts/framing.py input.json
    python3 scripts/framing.py < input.json

The input is one JSON object:

    {"source": {"w": 2556, "h": 1410}, "panel": {"x": 40, "y": 600, "w": 1000, "h": 1280},
     "S": 1.3, "F": [1200, 700]}

- `source` is the recording's size in px, `panel` a top-left box in frame px.
- `S` is the total scale, source px to frame px. Without it, the smallest scale at which the
  recording still covers the panel: for a panel the size of the frame, the full-frame rest.
- `F` is the source point to put on the panel's centre. Without it, the source's centre.
- `frame` is the composition's size, 1080x1920 by default.

It prints one JSON line, `{transform: {scale, position}, S, F, contain}`: the transform goes on the
recording layer, which is `fit: "contain"`; `contain` is how much that fit alone scales the source.
Input it cannot frame exits 1, with one line on stderr that says what is wrong.

The formula: the recording layer is `fit: "contain"` in the whole composition, so a source first
scales by CONTAIN = min(frame.w / src.w, frame.h / src.h). Showing it at total scale S with source
point F on frame point C means `scale = S / CONTAIN` and `position = C - S * (F - srcCenter)`.

Not `cover`: `cover` crops what overflows the composition-sized box before the layer is scaled and
moved, so a panel framed on a point off the source's centre shows an empty band. `contain` never
crops, so the whole source is there to frame.

Boxes are top-left rectangles, `{x, y, w, h}`; a size is `{w, h}` and a point `[x, y]`. Numbers
round as JavaScript's `Math.round` does, a half up, so a scene built here matches one built by the
TypeScript tools to the last digit.

Python 3.9 or later, the standard library only, offline.
"""
from __future__ import annotations

import json
import math
import sys
from typing import Any, Dict, List

Box = Dict[str, float]
Size = Dict[str, float]
Vec2 = List[float]
Framing = Dict[str, Any]  # {S: total scale, source px to frame px; F: source point on the panel centre}

# The vertical frame every layout is drawn in.
FRAME: Size = {'w': 1080, 'h': 1920}

# The fit every recording layer uses; `pose` scales by its `fit_base`.
RECORDING_FIT = 'contain'

USAGE = 'usage: framing.py [input.json]; with no file, the input is read from stdin'


def math_round(x: float) -> float:
    """`Math.round`: the nearest integer, a half rounded up."""
    if not math.isfinite(x):
        return x
    f = math.floor(x)
    return f + 1 if x - f >= 0.5 else f


def round(v: float, places: int = 2) -> float:  # noqa: A001 - every round here is this one
    """`Math.round(v * 10 ** places) / 10 ** places`: a half rounds up, never to even."""
    return math_round(v * 10 ** places) / 10 ** places


def center(b: Box) -> Vec2:
    return [b['x'] + b['w'] / 2, b['y'] + b['h'] / 2]


def fit_base(src: Size, comp: Size, fit: str = RECORDING_FIT) -> float:
    """How much the fit alone scales the source into the composition."""
    if fit == 'cover':
        return max(comp['w'] / src['w'], comp['h'] / src['h'])
    return min(comp['w'] / src['w'], comp['h'] / src['h'])


def drawn_rect(src: Size, comp: Size, p: Dict[str, Vec2], fit: str = RECORDING_FIT) -> Box:
    """
    Where the recording is actually drawn, in composition px. The fit pours the source into the
    composition-sized box, and `cover` crops what overflows it; the layer's scale and position then
    move that result. So a cover-fit layer never draws wider than `scale * comp.w`.
    """
    base = fit_base(src, comp, fit)
    w = min(src['w'] * base, comp['w']) if fit == 'cover' else src['w'] * base
    h = min(src['h'] * base, comp['h']) if fit == 'cover' else src['h'] * base
    k = p['scale'][0]
    return {'x': p['position'][0] - (k * w) / 2, 'y': p['position'][1] - (k * h) / 2, 'w': k * w, 'h': k * h}


def pose(src: Size, comp: Size, panel: Box, f: Framing) -> Dict[str, Vec2]:
    """The layer's `scale` and `position` that show `f['F']` on the panel's centre at total scale `f['S']`."""
    k = f['S'] / fit_base(src, comp)
    cx, cy = center(panel)
    return {
        'scale': [round(k, 4), round(k, 4)],
        'position': [round(cx - f['S'] * (f['F'][0] - src['w'] / 2), 1), round(cy - f['S'] * (f['F'][1] - src['h'] / 2), 1)],
    }


def min_scale(src: Size, panel: Box) -> float:
    """The smallest total scale at which the recording still covers the panel."""
    return max(panel['w'] / src['w'], panel['h'] / src['h'])


def fit_scale(box: Box, panel: Box) -> float:
    """The scale at which `box` just fits inside the panel."""
    return min(panel['w'] / box['w'], panel['h'] / box['h'])


class InputError(ValueError):
    pass


def _size(v: Any, name: str) -> Size:
    if not isinstance(v, dict) or not all(_positive(v.get(k)) for k in ('w', 'h')):
        raise InputError(f'{name} must be {{w, h}}, both positive numbers')
    return {'w': v['w'], 'h': v['h']}


def _box(v: Any, name: str) -> Box:
    if not isinstance(v, dict) or not all(_number(v.get(k)) for k in ('x', 'y')) or not all(_positive(v.get(k)) for k in ('w', 'h')):
        raise InputError(f'{name} must be {{x, y, w, h}}, with a positive width and height')
    return {'x': v['x'], 'y': v['y'], 'w': v['w'], 'h': v['h']}


def _number(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def _positive(v: Any) -> bool:
    return _number(v) and v > 0


def frame(data: Any) -> Dict[str, Any]:
    """The script's whole job: the checked input in, the line it prints out."""
    if not isinstance(data, dict):
        raise InputError('the input must be one JSON object')
    src = _size(data.get('source'), 'source')
    panel = _box(data.get('panel'), 'panel')
    comp = _size(data['frame'], 'frame') if data.get('frame') is not None else FRAME
    F = data.get('F')
    if F is None:
        F = [src['w'] / 2, src['h'] / 2]
    elif not (isinstance(F, list) and len(F) == 2 and all(_number(v) for v in F)):
        raise InputError('F must be a source point, [x, y]')
    S = data.get('S')
    if S is None:
        if not (0 < F[0] < src['w'] and 0 < F[1] < src['h']):
            raise InputError('F must be inside the source when S is omitted')
        S = max(panel['w'] / 2 / min(F[0], src['w'] - F[0]), panel['h'] / 2 / min(F[1], src['h'] - F[1]))
    elif not _positive(S):
        raise InputError('S must be a positive number')
    return {'transform': pose(src, comp, panel, {'S': S, 'F': F}), 'S': round(S, 4), 'F': F, 'contain': round(fit_base(src, comp), 6)}


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
        out = frame(json.loads(text))
    except json.JSONDecodeError as err:
        return fail(f'the input is not JSON: {err}')
    except InputError as err:
        return fail(str(err))
    sys.stdout.buffer.write((json.dumps(out, separators=(',', ':')) + '\n').encode('utf-8'))
    return 0


def fail(reason: str, code: int = 1) -> int:
    sys.stderr.write('framing.py: ' + ' '.join(reason.split()) + '\n')
    return code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
