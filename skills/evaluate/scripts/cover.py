#!/usr/bin/env python3
"""
Cover a box of a recording with an opaque card that moves with the recording: through every push
and pan, so private data stays hidden.

    python3 scripts/cover.py input.json
    python3 scripts/cover.py < input.json

The input is one JSON object:

    {"id": "s2_cover", "layer": {...}, "source": {"w": 2556, "h": 1410},
     "box": {"x": 1210, "y": 18, "w": 260, "h": 28}, "color": "#2a2233", "from": 4.0, "to": 9.5}

- `layer`: the recording layer, exactly as it is in the scene: `fit: "contain"`, or a `track` whose
  clips all are, with its
  `transform` and, when it pushes, its `scale` and `position` keyframes, which must share their
  times and easings (`zoom.py` writes them so).
- `source`: the recording's size; `box`: what to cover, in source px; `pad`, optional, how much
  wider than the box the card is per side, in source px (8 by default).
- `color`: the card's fill. Use the style's `surface`, so the card belongs to the video.
- `from` and `to`, optional, in the scene's seconds: when the card shows. The whole layer when
  left out.
- `frame`: the composition's size, 1080x1920 by default; for a recording inside a nested panel,
  the nested scene's size.
- `id`: the card's layer id, unique in the scene.

It prints one JSON line, `{layer}`: a `shape` layer to add right after the recording layer, in the
same scene. It has the recording's start, length and scale keyframes; its position keyframes put
the box's centre where the recording draws it, at the same times on the same easing, so it stays
on the box exactly. A recording with a `mask` gives the card a copy of the mask, with its own id,
so the card is clipped to the panel too. Outside `from`-`to` the card is at opacity 0. Input it
cannot cover exits 1, with one line on stderr that says what is wrong.

Python 3.9 or later, the standard library only, offline.
"""
from __future__ import annotations

import copy
import json
import sys
from typing import Any, Dict, List, Optional

from framing import FRAME, InputError, _box, _size, fit_base

USAGE = 'usage: cover.py [input.json]; with no file, the input is read from stdin'
STEP = 0.01


def _vec(v: Any, where: str) -> List[float]:
    if isinstance(v, (list, tuple)) and len(v) == 2 and all(isinstance(n, (int, float)) and not isinstance(n, bool) for n in v):
        return [float(v[0]), float(v[1])]
    raise InputError(f'{where} must be [x, y]')


def cover(id_: str, layer: Dict[str, Any], src: Dict[str, float], comp: Dict[str, float], box: Dict[str, float], color: str,
          pad: float = 8, t0: Optional[float] = None, t1: Optional[float] = None) -> Dict[str, Any]:
    content = layer.get('content') or {}
    # A step of several playback pieces is a track: every clip plays the recording, drawn by the layer's transform.
    played = [c.get('content') or {} for c in content.get('clips') or [] if isinstance(c, dict)] if content.get('kind') == 'track' else [content]
    if not played or any(c.get('kind') != 'media' or c.get('fit', 'contain') != 'contain' for c in played):
        raise InputError('layer must be the recording: a media layer with fit "contain", or a track of them')
    C = fit_base(src, comp)
    cx = box['x'] + box['w'] / 2 - src['w'] / 2
    cy = box['y'] + box['h'] / 2 - src['h'] / 2
    transform = layer.get('transform') or {}
    p0 = _vec(transform.get('position', [comp['w'] / 2, comp['h'] / 2]), 'layer.transform.position')
    s0 = _vec(transform.get('scale', [1, 1]), 'layer.transform.scale')

    def at(p: List[float], s: List[float]) -> List[float]:
        return [round(p[0] + s[0] * C * cx, 2), round(p[1] + s[1] * C * cy, 2)]

    anims = layer.get('animations') or {}
    sk = (anims.get('scale') or {}).get('keyframes') or []
    pk = (anims.get('position') or {}).get('keyframes') or []
    out: Dict[str, Any] = {
        'id': id_,
        'start': layer.get('start', 0),
        'duration': layer.get('duration'),
        'transform': {'position': at(p0, s0), 'scale': s0},
        'content': {'kind': 'shape', 'items': [
            {'type': 'rect', 'size': [round((box['w'] + 2 * pad) * C, 2), round((box['h'] + 2 * pad) * C, 2)], 'roundness': round(6 * C, 2)},
            {'type': 'fill', 'color': color},
        ]},
    }
    if layer.get('timeMode'):
        out['timeMode'] = layer['timeMode']
    animations: Dict[str, Any] = {}
    if sk or pk:
        times_s = [k.get('time') for k in sk]
        times_p = [k.get('time') for k in pk]
        if times_s and times_p and times_s != times_p:
            raise InputError('the scale and position keyframes must share their times, as zoom.py writes them')
        # The card's position is one curve, so it stays on the box only when both move on the same easing.
        if sk and pk and any(a.get('easing') != b.get('easing') for a, b in zip(sk[:-1], pk[:-1])):
            raise InputError('the scale and position keyframes must move on the same easing, as zoom.py writes them')
        keys = pk or sk
        values_p = [_vec(k['value'], 'a position keyframe') for k in pk] if pk else [p0] * len(keys)
        values_s = [_vec(k['value'], 'a scale keyframe') for k in sk] if sk else [s0] * len(keys)
        pos = []
        for k, p, s in zip(keys, values_p, values_s):
            kf = {'time': k['time'], 'value': at(p, s)}
            if 'easing' in k:
                kf['easing'] = k['easing']
            pos.append(kf)
        animations['position'] = {'keyframes': pos}
        if sk:
            animations['scale'] = {'keyframes': copy.deepcopy(sk)}
        out['transform'] = {'position': pos[0]['value'], 'scale': values_s[0]}
    start = float(layer.get('start') or 0)
    length = float(layer['duration']) if isinstance(layer.get('duration'), (int, float)) else None
    if t0 is not None or t1 is not None:
        # Layer-relative opacity: 0, then 1 from `from` to `to`, a hundredth of a second each way.
        base = 0.0 if layer.get('timeMode', 'composition') == 'composition' else start
        a = max(0.0, (t0 if t0 is not None else start) - base)
        b = (t1 - base) if t1 is not None else None
        ops: List[Dict[str, Any]] = []
        if a > STEP:
            ops += [{'time': 0, 'value': 0, 'easing': 'linear'}, {'time': round(a - STEP, 3), 'value': 0, 'easing': 'linear'}]
        ops.append({'time': round(a, 3), 'value': 1, 'easing': 'linear'})
        end = None if length is None else start - base + length
        if b is not None and (end is None or b < end - STEP):
            ops += [{'time': round(b, 3), 'value': 1, 'easing': 'linear'}, {'time': round(b + STEP, 3), 'value': 0, 'easing': 'linear'}]
        del ops[-1]['easing']
        if len(ops) > 1:
            animations['opacity'] = {'keyframes': ops}
    if animations:
        out['animations'] = animations
    mask = layer.get('mask')
    if isinstance(mask, dict) and isinstance(mask.get('layer'), dict):
        m = copy.deepcopy(mask)
        m['layer']['id'] = f'{id_}_mask'
        out['mask'] = m
    return out


def run(data: Any) -> Dict[str, Any]:
    """The script's whole job: the checked input in, the line it prints out."""
    if not isinstance(data, dict):
        raise InputError('the input must be one JSON object')
    id_ = data.get('id')
    if not isinstance(id_, str) or not id_:
        raise InputError('id must be the card\'s layer id')
    layer = data.get('layer')
    if not isinstance(layer, dict):
        raise InputError('layer must be the recording layer, as it is in the scene')
    color = data.get('color')
    if not isinstance(color, str) or not color.startswith('#'):
        raise InputError('color must be a hex colour, the style\'s surface')
    pad = data.get('pad', 8)
    if not isinstance(pad, (int, float)) or isinstance(pad, bool) or pad < 0:
        raise InputError('pad must be a number of source px, 0 or more')
    times = []
    for key in ('from', 'to'):
        v = data.get(key)
        if v is not None and (not isinstance(v, (int, float)) or isinstance(v, bool)):
            raise InputError(f'{key} must be a number of seconds')
        times.append(v)
    if times[0] is not None and times[1] is not None and times[1] <= times[0]:
        raise InputError('to must be after from')
    comp = _size(data['frame'], 'frame') if data.get('frame') is not None else FRAME
    return {'layer': cover(id_, layer, _size(data.get('source'), 'source'), comp, _box(data.get('box'), 'box'), color, pad, times[0], times[1])}


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
    except (KeyError, IndexError, TypeError) as err:
        return fail(f'cannot cover from this input: {type(err).__name__} {err}')
    sys.stdout.buffer.write((json.dumps(out, separators=(',', ':')) + '\n').encode('utf-8'))
    return 0


def fail(reason: str, code: int = 1) -> int:
    sys.stderr.write('cover.py: ' + ' '.join(reason.split()) + '\n')
    return code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
