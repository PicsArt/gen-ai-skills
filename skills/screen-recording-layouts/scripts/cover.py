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
  times, easings and track timeMode (`zoom.py` writes them so). Static rotation and common
  content bounds are supported; anchors, animated rotation, transform expressions, clip-local
  transforms and mismatched clip bounds are rejected. Position tangents require constant scale;
  scale tangents are rejected.
- `source`: the recording's size; `box`: what to cover, in source px; `pad`, optional, how much
  wider than the box the card is per side, in source px (8 by default).
- `color`: the card's fill, an opaque hex (#RRGGBB or #RRGGBBff); other colours are rejected. Use
  the style's `surface`, so the card belongs to the video.
- `from` and `to`, optional, in the scene's seconds: when the card shows. The whole layer when
  left out.
- `frame`: the composition's size, 1080x1920 by default; for a recording inside a nested panel,
  the nested scene's size.
- `id`: the card's layer id, unique in the scene.

It prints one JSON line, `{layer}`: a `shape` layer to add right after the recording layer, in the
same scene. It has the recording's start, length and scale keyframes; its position keyframes put
the box's centre where the recording draws it, at the same times on the same easing, so it stays
on the box exactly. A recording with a `mask` gives the card a copy of the mask, with its own id,
so the card is clipped to the panel too; only a static, opaque shape mask (panels.py's) is copied,
as a see-through mask would leave the recording showing through the card. Outside `from`-`to` the card is at opacity 0. Input it
cannot cover exits 1, with one line on stderr that says what is wrong.

Python 3.9 or later, the standard library only, offline.
"""
from __future__ import annotations

import copy
import json
import math
import re
import sys
from typing import Any, Dict, List, Optional

from framing import FRAME, InputError, _box, _size, fit_base

USAGE = 'usage: cover.py [input.json]; with no file, the input is read from stdin'
STEP = 0.01
# What a recording layer and its media may carry: what the builders write, and the card follows.
LAYER_KEYS = {'id', 'start', 'duration', 'timeMode', 'transform', 'animations', 'content', 'mask', 'parentId', 'cameraExempt'}
MEDIA_KEYS = {'kind', 'assetId', 'fit', 'bounds', 'trim', 'speed', 'muted'}


def _vec(v: Any, where: str) -> List[float]:
    if isinstance(v, (list, tuple)) and len(v) == 2 and all(isinstance(n, (int, float)) and not isinstance(n, bool) and math.isfinite(n) for n in v):
        return [float(v[0]), float(v[1])]
    raise InputError(f'{where} must be [x, y]')


def cover(id_: str, layer: Dict[str, Any], src: Dict[str, float], comp: Dict[str, float], box: Dict[str, float], color: str,
          pad: float = 8, t0: Optional[float] = None, t1: Optional[float] = None) -> Dict[str, Any]:
    if not isinstance(color, str) or not re.fullmatch(r'#[0-9a-fA-F]{6}(?:[fF]{2})?', color):
        raise InputError('color must be an opaque hex colour')
    content = layer.get('content') or {}
    # A step of several playback pieces is a track: every clip plays the recording, drawn by the layer's transform.
    if content.get('kind') == 'track':
        clips = content.get('clips') or []
        # A transition moves or fades the recording between clips, where a still card would not follow it.
        if set(content) - {'kind', 'clips'}:
            raise InputError('a recording track with transitions or other track settings is not supported')
        if not isinstance(clips, list) or any(not isinstance(c, dict) for c in clips):
            raise InputError('a recording track must contain clips with media content')
        if any(set(c) - {'id', 'content', 'start', 'duration', 'timeMode'} for c in clips):
            raise InputError('a track clip with its own transform is not supported')
        played = [c.get('content') or {} for c in clips]
    else:
        played = [content]
    if not played or any(c.get('kind') != 'media' or c.get('fit', 'contain') != 'contain' for c in played):
        raise InputError('layer must be the recording: a media layer with fit "contain", or a track of them')
    extra = sorted({k for c in played for k in c} - MEDIA_KEYS)
    if extra:
        # A crop or any other media setting moves the recording's pixels where the card does not follow.
        raise InputError(f"recording media with {', '.join(extra)} is not supported")
    bases = []
    for c in played:
        if 'bounds' in c:
            w, h = _vec(c['bounds'], 'content.bounds')
            bases.append(_size({'w': w, 'h': h}, 'content.bounds'))
        else:
            bases.append(None)
    if any(b != bases[0] for b in bases[1:]):
        raise InputError('all recording track clips must have the same content.bounds or none')
    C = fit_base(src, bases[0] if bases[0] is not None else comp)
    cx = box['x'] + box['w'] / 2 - src['w'] / 2
    cy = box['y'] + box['h'] / 2 - src['h'] / 2
    if layer.get('transforms'):
        raise InputError('a recording with a transforms list is not supported; use one transform')
    transform = layer.get('transform') or {}
    if 'anchor' in transform:
        raise InputError('a recording with transform.anchor is not supported; remove it')
    rotation = transform.get('rotation', 0)
    if not isinstance(rotation, (int, float)) or isinstance(rotation, bool) or not math.isfinite(rotation):
        raise InputError('layer.transform.rotation must be a finite number of degrees')
    angle = math.radians(rotation % 360)
    cos, sin = math.cos(angle), math.sin(angle)
    p0 = _vec(transform.get('position', [comp['w'] / 2, comp['h'] / 2]), 'layer.transform.position')
    s0 = _vec(transform.get('scale', [1, 1]), 'layer.transform.scale')

    def at(p: List[float], s: List[float]) -> List[float]:
        x, y = s[0] * C * cx, s[1] * C * cy
        return [round(p[0] + x * cos - y * sin, 2), round(p[1] + x * sin + y * cos, 2)]

    anims = layer.get('animations') or {}
    for name in ('position', 'scale', 'rotation', 'anchor'):
        if 'expression' in (anims.get(name) or {}):
            raise InputError(f'animations.{name} with an expression is not supported')
    if 'rotation' in anims:
        raise InputError('a recording with animations.rotation is not supported')
    if 'anchor' in anims:
        raise InputError('a recording with animations.anchor is not supported')
    # Anything else that moves, crops, mirrors or warps the recording's pixels (looks, effects, a
    # skew) would leave a still card off the box: only what the card follows is accepted.
    if set(layer) - LAYER_KEYS:
        raise InputError(f"a recording with {', '.join(sorted(set(layer) - LAYER_KEYS))} is not supported")
    if set(transform) - {'position', 'scale', 'rotation', 'opacity'}:
        raise InputError(f"a recording transform with {', '.join(sorted(set(transform) - {'position', 'scale', 'rotation', 'opacity'}))} is not supported")
    if set(anims) - {'position', 'scale', 'opacity'}:
        raise InputError(f"a recording with animations.{', animations.'.join(sorted(set(anims) - {'position', 'scale', 'opacity'}))} is not supported")
    time_mode = layer.get('timeMode', 'composition')
    if 'position' in anims and 'scale' in anims and (anims.get('position') or {}).get('timeMode', time_mode) != (anims.get('scale') or {}).get('timeMode', time_mode):
        raise InputError('the position and scale animation tracks must share their timeMode')
    sk = (anims.get('scale') or {}).get('keyframes') or []
    pk = (anims.get('position') or {}).get('keyframes') or []
    if any('inTangent' in k or 'outTangent' in k for k in sk):
        raise InputError('scale keyframes with spatial tangents are not supported')
    scale_values = [_vec(k['value'], 'a scale keyframe') for k in sk]
    if any(s != scale_values[0] for s in scale_values[1:]) and any('inTangent' in k or 'outTangent' in k for k in pk):
        raise InputError('position tangents with animated scale are not supported')
    out: Dict[str, Any] = {
        'id': id_,
        'start': layer.get('start', 0),
        'duration': layer.get('duration'),
        'transform': {'position': at(p0, s0), 'scale': s0},
        'content': {'kind': 'shape', 'items': [
            {'type': 'rect', 'size': [round((box['w'] + 2 * pad) * C, 2), round((box['h'] + 2 * pad) * C, 2)], 'roundness': round(min(6, pad) * C, 2)},
            {'type': 'fill', 'color': color},
        ]},
    }
    if layer.get('timeMode'):
        out['timeMode'] = layer['timeMode']
    for name in ('parentId', 'cameraExempt'):
        if name in layer:
            out[name] = copy.deepcopy(layer[name])
    animations: Dict[str, Any] = {}
    if sk or pk:
        times_s = [k.get('time') for k in sk]
        times_p = [k.get('time') for k in pk]
        if times_s and times_p and times_s != times_p:
            raise InputError('the scale and position keyframes must share their times, as zoom.py writes them')
        # The card's position is one curve, so it stays on the box only when both move on the same easing.
        if sk and pk and any(a.get('easing', 'linear') != b.get('easing', 'linear') for a, b in zip(sk[:-1], pk[:-1])):
            raise InputError('the scale and position keyframes must move on the same easing, as zoom.py writes them')
        keys = pk or sk
        values_p = [_vec(k['value'], 'a position keyframe') for k in pk] if pk else [p0] * len(keys)
        values_s = scale_values if sk else [s0] * len(keys)
        pos = []
        for k, p, s in zip(keys, values_p, values_s):
            kf = {'time': k['time'], 'value': at(p, s)}
            if 'easing' in k:
                kf['easing'] = k['easing']
            if pk:
                for name in ('inTangent', 'outTangent'):
                    if name in k:
                        kf[name] = copy.deepcopy(k[name])
            pos.append(kf)
        animations['position'] = {'keyframes': pos}
        position_track = (anims.get('position') if pk else anims.get('scale')) or {}
        if 'timeMode' in position_track:
            animations['position']['timeMode'] = copy.deepcopy(position_track['timeMode'])
        if sk:
            animations['scale'] = {'keyframes': copy.deepcopy(sk)}
            if 'timeMode' in anims['scale']:
                animations['scale']['timeMode'] = copy.deepcopy(anims['scale']['timeMode'])
        out['transform'] = {'position': pos[0]['value'], 'scale': values_s[0]}
    if 'rotation' in transform:
        out['transform']['rotation'] = rotation
    start = float(layer.get('start') or 0)
    length = float(layer['duration']) if isinstance(layer.get('duration'), (int, float)) else None
    if t0 is not None or t1 is not None:
        # Layer-relative opacity: 0, then 1 from `from` to `to`, a hundredth of a second each way.
        base = 0.0 if layer.get('timeMode', 'composition') == 'composition' else start
        a = max(0.0, (t0 if t0 is not None else start) - base)
        b = (t1 - base) if t1 is not None else None
        # To the millisecond, the card is fully on early and off late, never late on or early off:
        # a frame at `from` (2/30 s is 0.0666...) is already covered.
        on = math.floor(a * 1000 + 1e-6) / 1000
        ops: List[Dict[str, Any]] = []
        if a > STEP:
            ops += [{'time': 0, 'value': 0, 'easing': 'linear'}, {'time': round(on - STEP, 3), 'value': 0, 'easing': 'linear'}]
        ops.append({'time': on, 'value': 1, 'easing': 'linear'})
        end = None if length is None else start - base + length
        if b is not None and (end is None or b < end - STEP):
            off = math.ceil(b * 1000 - 1e-6) / 1000
            ops += [{'time': off, 'value': 1, 'easing': 'linear'}, {'time': round(off + STEP, 3), 'value': 0, 'easing': 'linear'}]
        del ops[-1]['easing']
        if len(ops) > 1:
            animations['opacity'] = {'keyframes': ops}
    if animations:
        out['animations'] = animations
    mask = layer.get('mask')
    if mask is not None:
        _opaque_mask(mask)
        m = copy.deepcopy(mask)
        m['layer']['id'] = f'{id_}_mask'
        out['mask'] = m
    return out


def _opaque_mask(mask: Any) -> None:
    """
    Refuse a mask the card cannot copy and stay opaque: the card shares the recording's mask, so a
    see-through mask would leave the private pixels showing through the card. Only a static shape
    filled with an opaque colour (panels.py's `mask`) is copied.
    """
    if not isinstance(mask, dict) or set(mask) != {'layer'} or not isinstance(mask['layer'], dict):
        raise InputError('layer.mask must be {"layer": {...}} only')
    m = mask['layer']
    if set(m) - {'id', 'transform', 'content'}:
        raise InputError('a mask layer with animations, effects, timing or opacity is not supported')
    if set(m.get('transform') or {}) - {'position', 'scale', 'rotation'}:
        raise InputError('a mask transform with opacity or an anchor is not supported')
    content = m.get('content') or {}
    items = content.get('items')
    if set(content) - {'kind', 'items'} or content.get('kind') != 'shape' or not isinstance(items, list):
        raise InputError('the mask must be a shape layer')
    fills = [i for i in items if isinstance(i, dict) and i.get('type') == 'fill']
    rects = [i for i in items if isinstance(i, dict) and i.get('type') == 'rect' and not set(i) - {'type', 'size', 'roundness', 'position'}]
    if not fills or len(fills) + len(rects) != len(items):
        raise InputError('the mask must be rects with an opaque fill')
    for f in fills:
        if set(f) - {'type', 'color'} or not isinstance(f.get('color'), str) or not re.fullmatch(r'#[0-9a-fA-F]{6}(?:[fF]{2})?', f['color']):
            raise InputError('the mask fill must be one opaque #rrggbb colour')


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
