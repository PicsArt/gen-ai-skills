#!/usr/bin/env python3
"""
Will a moment of a screen recording read in its panel? Measured before anything is built.

    python3 scripts/readability.py input.json
    python3 scripts/readability.py < input.json

The input is one JSON object:

    {"source": {"w": 2560, "h": 1440}, "canvas": "#3a1030",
     "panel": {"x": 40, "y": 600, "w": 1000, "h": 1280},
     "moments": [{"id": "shot-cards", "box": {"x": 900, "y": 300, "w": 1400, "h": 900},
                  "textPx": 22, "words": 30, "luma": 236}]}

- `source` is the recording's size; `panel` the panel the moments show in, in frame px, by
  default the prompt-over-result panel. A moment may carry its own `panel`.
- `canvas` is the style's canvas colour, `#rrggbb` (the visual-style skill's `style.py`).
- Each moment is one thing a video will show: `box`, what the viewer must read, in source px;
  `textPx`, the height of the smallest line of text in it the viewer must read, in source px,
  measured on a still; `words`, how many words of UI are in the box; `luma`, the box's mean luma
  (0-255), as `picsart_media_screen_moments` gives it for the event that settles there.

It prints one JSON line, `{moments, failing, recommend}`. Each moment gets `textPx` (its text at
the panel, in frame px, with the box fitted as large as the panel allows), `fill` (the share of
the panel the box covers at that fit), `lumaJump` (how far its luma is from the canvas's),
`reads`, and `findings`. `failing` lists the moments that do not read; `recommend` is
`recreate` when one does not, else `keep`. Input it cannot measure exits 1, with one line on
stderr that says what is wrong.

What each finding means:
- `text_small` (fails): even with the box fitted to the panel, its text is under `TEXT_PX`.
- `dense` (fails): more than `MAX_WORDS` words of UI for the viewer to read in one moment.
- `shape` (warns): the box's shape is far from the panel's, so it fills under `MIN_FILL` of it;
  the rest is other UI or empty panel.
- `luma_jump` (warns): the UI is far brighter or darker than the canvas around it, so the cut
  to it reads as a jump out of the style.

Python 3.9 or later, the standard library only, offline.
"""
from __future__ import annotations

import json
import re
import sys
from typing import Any, Dict, List

from framing import Box, InputError, _box, _number, _positive, _size, fit_scale, round

# UI text under this many frame px does not read on a phone. The make-screen-videos builders warn on the
# same floor after a build.
TEXT_PX = 24
# More words of UI than this in one moment is more than a viewer reads while the video moves on.
MAX_WORDS = 12
# A box that covers less of its panel than this is a strip in a frame of something else.
MIN_FILL = 0.5
# Mean luma (0-255) between the UI and the canvas past which the cut reads as a jump.
LUMA_JUMP = 140

# The screen-recording-layouts skill's prompt-over-result panel.
PANEL: Box = {'x': 40, 'y': 600, 'w': 1000, 'h': 1280}

HEX = re.compile(r'^#[0-9a-fA-F]{6}$')

USAGE = 'usage: readability.py [input.json]; with no file, the input is read from stdin'


def luma(color: str) -> float:
    """Mean luma (0-255) of `#rrggbb`, Rec. 601 weights."""
    r, g, b = (int(color[i:i + 2], 16) for i in (1, 3, 5))
    return 0.299 * r + 0.587 * g + 0.114 * b


def measure(moment: Dict[str, Any], panel: Box, canvas: str) -> Dict[str, Any]:
    """One moment's measures and findings."""
    box = moment['box']
    S = fit_scale(box, panel)
    text = moment['textPx'] * S
    fill = (box['w'] * S) * (box['h'] * S) / (panel['w'] * panel['h'])
    jump = moment['luma'] - luma(canvas)
    findings = []
    if text < TEXT_PX:
        findings.append({'code': 'text_small', 'level': 'fails', 'message': f"its text reads at about {round(text, 1)} px at most, under {TEXT_PX}"})
    if moment['words'] > MAX_WORDS:
        findings.append({'code': 'dense', 'level': 'fails', 'message': f"{moment['words']} words of UI to read, more than {MAX_WORDS}"})
    if fill < MIN_FILL:
        findings.append({'code': 'shape', 'level': 'warns', 'message': f"the box fills {round(fill * 100, 0):.0f}% of its panel; the rest is other UI or empty"})
    if abs(jump) > LUMA_JUMP:
        tone = 'brighter' if jump > 0 else 'darker'
        findings.append({'code': 'luma_jump', 'level': 'warns', 'message': f"the UI is far {tone} than the canvas ({round(abs(jump), 0):.0f} of 255)"})
    return {
        'id': moment['id'],
        'textPx': round(text, 1),
        'fill': round(fill, 2),
        'lumaJump': round(jump, 0),
        'reads': not any(f['level'] == 'fails' for f in findings),
        'findings': findings,
    }


def _moment(v: Any, i: int) -> Dict[str, Any]:
    where = f'moments[{i}]'
    if not isinstance(v, dict):
        raise InputError(f'{where} must be an object')
    if not isinstance(v.get('id'), str) or not v['id']:
        raise InputError(f'{where}.id must be a name')
    if not _positive(v.get('textPx')):
        raise InputError(f'{where}.textPx must be the smallest text\'s height in source px, measured on a still')
    if not isinstance(v.get('words'), int) or isinstance(v['words'], bool) or v['words'] < 0:
        raise InputError(f'{where}.words must be a count of words, 0 or more')
    if not _number(v.get('luma')) or not 0 <= v['luma'] <= 255:
        raise InputError(f'{where}.luma must be the box\'s mean luma, 0-255')
    out = {'id': v['id'], 'box': _box(v.get('box'), f'{where}.box'), 'textPx': v['textPx'], 'words': v['words'], 'luma': v['luma']}
    if v.get('panel') is not None:
        out['panel'] = _box(v['panel'], f'{where}.panel')
    return out


def run(data: Any) -> Dict[str, Any]:
    """The script's whole job: the checked input in, the line it prints out."""
    if not isinstance(data, dict):
        raise InputError('the input must be one JSON object')
    src = _size(data.get('source'), 'source')
    canvas = data.get('canvas')
    if not isinstance(canvas, str) or not HEX.match(canvas):
        raise InputError('canvas must be the style\'s canvas colour, #rrggbb')
    panel = _box(data['panel'], 'panel') if data.get('panel') is not None else PANEL
    moments = data.get('moments')
    if not isinstance(moments, list) or not moments:
        raise InputError('moments must be a list of the moments the video will show')
    checked = [_moment(m, i) for i, m in enumerate(moments)]
    for i, m in enumerate(checked):
        b = m['box']
        if b['x'] < 0 or b['y'] < 0 or b['x'] + b['w'] > src['w'] + 0.5 or b['y'] + b['h'] > src['h'] + 0.5:
            raise InputError(f'moments[{i}].box must lie inside the source, {src["w"]}x{src["h"]}')
    out = [measure(m, m.get('panel', panel), canvas) for m in checked]
    failing = [m['id'] for m in out if not m['reads']]
    return {'moments': out, 'failing': failing, 'recommend': 'recreate' if failing else 'keep'}


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
    sys.stderr.write('readability.py: ' + ' '.join(reason.split()) + '\n')
    return code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
