#!/usr/bin/env python3
"""
Build a layout's panel pieces as scene JSON: a panel's mask, the rim behind it, the prompt bubble,
and a masked panel turned into a nested scene.

    python3 scripts/panels.py input.json
    python3 scripts/panels.py < input.json

The input is one JSON object, `{items: [...]}`, and each item is one piece:

    {"kind": "mask",   "id": "s1_mask",   "box": {x, y, w, h}, "roundness": 36}
    {"kind": "rim",    "id": "s1_rim",    "box": {x, y, w, h}, "color": "#1d2029", "start": 2.2, "duration": 4, "roundness": 42}
    {"kind": "bubble", "id": "s1_bubble", "box": {x, y, w, h}, "color": "#1d2029", "start": 2.2, "duration": 4}
    {"kind": "nest",   "layer": { a media layer with a mask }, "source": {w, h}, "asset": { the recording's asset }}

- `box` is the panel (or the bubble) in frame px, top-left.
- `mask` gives the value of a media layer's `mask`; `roundness` is 36 by default.
- `rim` gives a shape layer 6 px larger on every side, to go under the panel; `roundness` is 42 by
  default.
- `bubble` gives the prompt bubble, a shape layer that fades in over 0.2 s.
- `nest` gives `{layer, assets}`: the panel as a `scene_ref` layer placed on its mask, and the nested
  scene to add to the scene's `assets`. The media layer's asset is `rec` inside the nest.
- `frame`, beside `items`, is the composition's size, 1080x1920 by default.

It prints one JSON line, `{items: [...]}`, one result per input item, in order. Input it cannot
build from exits 1, with one line on stderr that says what is wrong.

Python 3.9 or later, the standard library only, offline.
"""
from __future__ import annotations

import json
import sys
from typing import Any, Dict, List

from framing import FRAME, Box, InputError, Size, Vec2, _box, _number, _size, center, fit_base, round

Layer = Dict[str, Any]

USAGE = 'usage: panels.py [input.json]; with no file, the input is read from stdin'


def panel_mask(id_: str, panel: Box, roundness: float = 36) -> Dict[str, Any]:
    """A media layer's `mask`: a white rounded rect the panel's size, centred on it."""
    return {
        'layer': {
            'id': id_,
            'transform': {'position': center(panel)},
            'content': {'kind': 'shape', 'items': [{'type': 'rect', 'size': [panel['w'], panel['h']], 'roundness': roundness}, {'type': 'fill', 'color': '#ffffff'}]},
        },
    }


def rim_layer(id_: str, panel: Box, color: str, start: float, duration: float, roundness: float) -> Layer:
    """A rounded shape 6 px larger than the panel on every side, behind it, so the panel reads as a card."""
    return {
        'id': id_,
        'start': round(start, 3),
        'duration': round(duration, 3),
        'transform': {'position': center(panel)},
        'content': {'kind': 'shape', 'items': [{'type': 'rect', 'size': [panel['w'] + 12, panel['h'] + 12], 'roundness': roundness}, {'type': 'fill', 'color': color}]},
    }


def as_rec(content: Dict[str, Any]) -> Dict[str, Any]:
    """The content playing the nested scene's one asset, `rec`: a media layer's, or each of a track's clips'."""
    if 'clips' in content:
        return {**content, 'clips': [{**c, 'content': as_rec(c['content'])} for c in content['clips']]}
    return {**content, 'assetId': 'rec'} if 'assetId' in content else content


def _duration(layer: Layer, rec: Dict[str, Any]) -> float:
    duration = layer.get('duration')
    if duration is None:
        content = layer['content']
        if content.get('kind') == 'track':
            duration = sum(_duration(clip, rec) for clip in content['clips'])
        else:
            trim = content.get('trim') or {}
            end = trim.get('out', rec.get('duration'))
            speed = content.get('speed', 1)
            if not _number(end) or not _number(speed) or speed <= 0:
                raise InputError('nest: duration needs a finite asset duration or trim out, and positive speed')
            duration = (end - _seconds(trim, 'in', 'trim', 0)) / speed
    return _seconds({'duration': duration}, 'duration', 'layer')


def nest_panel(layer: Layer, src: Size, rec: Dict[str, Any], assets: Dict[str, Any], comp: Size = FRAME) -> Layer:
    """
    A masked panel as a nested scene the size of its mask, placed on the mask: the nest clips at its
    edge, so no mask is needed. Inside, the same source point lands on the same composition point:
    positions shift by the panel's origin, and the scale changes with the fit base of the smaller box.
    The nested scene goes into `assets`.
    """
    mx, my = layer['mask']['layer']['transform']['position']
    mw, mh = layer['mask']['layer']['content']['items'][0]['size']
    ox = mx - mw / 2
    oy = my - mh / 2
    content = layer['content']
    # Unbounded clips refit to the panel just like single media, so compensate in
    # the layer's scale. Explicit clip bounds need their original fit boxes instead.
    preserve_bounds = content.get('bounds') is not None or any(
        clip['content'].get('bounds') is not None for clip in content.get('clips', [])
    )
    k = 1 if preserve_bounds else fit_base(src, comp) / fit_base(src, {'w': mw, 'h': mh})
    start = _seconds(layer, 'start', 'layer', 0)
    duration = _duration(layer, rec)

    def at(p: Vec2) -> Vec2:
        return [round(p[0] - ox, 1), round(p[1] - oy, 1)]

    def sized(s: Vec2) -> Vec2:
        return [round(s[0] * k, 4), round(s[1] * k, 4)]

    spatial = {k_: layer[k_] for k_ in ('parentId', 'cameraExempt') if k_ in layer}
    inner = {k_: v for k_, v in layer.items() if k_ not in ('mask', 'parentId', 'cameraExempt')}
    inner['id'] = f"{layer['id']}_rec"
    inner['start'] = 0
    inner['duration'] = duration
    inner['content'] = as_rec(content)

    def clip_at(p: Vec2) -> Vec2:
        return [round((p[0] - comp['w'] / 2) / k + mw / 2, 1),
                round((p[1] - comp['h'] / 2) / k + mh / 2, 1)]

    for clip in inner['content'].get('clips', []):
        if preserve_bounds and clip['content'].get('bounds') is None and clip['content'].get('fit') != 'none':
            clip['content'] = {**clip['content'], 'bounds': [comp['w'], comp['h']]}
        # Clips are placed about the track's centre; its fit compensation also scales their offsets.
        transform = clip.get('transform') or {}
        if 'position' in transform:
            clip['transform'] = {**transform, 'position': clip_at(transform['position'])}
        animations = clip.get('animations') or {}
        moved = {}
        for channel, track in animations.items():
            if track and 'expression' in track:
                raise InputError('nest: expression tracks need their original scene context and cannot be converted')
            if channel != 'position' or not track or 'keyframes' not in track:
                moved[channel] = track
                continue
            frames = []
            for frame in track['keyframes']:
                f = {**frame, 'value': clip_at(frame['value'])}
                for tangent in ('inTangent', 'outTangent'):
                    if tangent in frame:
                        f[tangent] = [round(v / k, 4) for v in frame[tangent]]
                frames.append(f)
            moved[channel] = {**track, 'keyframes': frames}
        if animations:
            clip['animations'] = moved
    transform = layer.get('transform', {})
    inner['transform'] = {**transform, 'position': at(transform.get('position', [comp['w'] / 2, comp['h'] / 2])), 'scale': sized(transform.get('scale', [1, 1]))}
    fitted = content.get('kind') == 'media' and content.get('fit') != 'none' and not preserve_bounds
    if (content.get('kind') == 'track' or fitted) and 'anchor' in transform:
        inner['transform']['anchor'] = [round(v / k, 4) for v in transform['anchor']] if fitted else clip_at(transform['anchor'])
    animations = layer.get('animations')
    if animations:
        moved = {}
        for channel, track in animations.items():
            if track and 'expression' in track:
                raise InputError('nest: expression tracks need their original scene context and cannot be converted')
            if not track or 'keyframes' not in track:
                moved[channel] = track
                continue
            offset = start if track.get('timeMode', layer.get('timeMode', 'composition')) == 'composition' else 0
            frames = []
            for frame in track['keyframes']:
                f = {**frame, 'time': frame['time'] - offset}
                if channel in ('position', 'scale'):
                    f['value'] = at(frame['value']) if channel == 'position' else sized(frame['value'])
                if channel == 'anchor' and (content.get('kind') == 'track' or fitted):
                    f['value'] = [round(v / k, 4) for v in frame['value']] if fitted else clip_at(frame['value'])
                if channel == 'scale':
                    for tangent in ('inTangent', 'outTangent'):
                        if tangent in frame:
                            f[tangent] = sized(frame[tangent])
                frames.append(f)
            moved[channel] = {**track, 'keyframes': frames}
        inner['animations'] = moved
    asset_id = f"{layer['id']}_view"
    assets[asset_id] = {
        'type': 'scene',
        'scene': {'version': '1.0', 'composition': {'width': mw, 'height': mh, 'fps': 30, 'duration': duration}, 'assets': {'rec': rec}, 'layers': [inner]},
    }
    return {'id': layer['id'], 'start': start, 'duration': duration, **spatial, 'transform': {'position': [mx, my]}, 'content': {'kind': 'scene_ref', 'assetId': asset_id, 'fit': 'none'}}


def bubble(id_: str, box: Box, color: str, start: float, duration: float) -> Layer:
    """The prompt bubble: a rounded shape that fades in over 0.2 s (the fade presets skip shapes)."""
    return {
        'id': id_,
        'start': round(start, 3),
        'duration': round(duration, 3),
        'timeMode': 'layer',
        'transform': {'position': center(box)},
        'content': {'kind': 'shape', 'items': [{'type': 'rect', 'size': [box['w'], box['h']], 'roundness': 44}, {'type': 'fill', 'color': color}]},
        'animations': {'opacity': {'keyframes': [{'time': 0, 'value': 0, 'easing': 'linear'}, {'time': 0.2, 'value': 1}]}},
    }


def _text(item: Dict[str, Any], key: str, where: str) -> str:
    v = item.get(key)
    if not isinstance(v, str) or not v:
        raise InputError(f'{where}: {key} must be a non-empty string')
    return v


def _seconds(item: Dict[str, Any], key: str, where: str, default: float = None) -> float:
    v = item.get(key, default)
    if not _number(v) or v < 0:
        raise InputError(f'{where}: {key} must be a number of seconds, 0 or more')
    return v


def build_item(item: Any, i: int, comp: Size) -> Any:
    where = f'items[{i}]'
    if not isinstance(item, dict):
        raise InputError(f'{where} must be an object')
    kind = item.get('kind')
    if kind == 'nest':
        layer = item.get('layer')
        if not isinstance(layer, dict) or not isinstance(layer.get('mask'), dict):
            raise InputError(f'{where}: layer must be a media layer with a mask')
        if not isinstance(item.get('asset'), dict):
            raise InputError(f'{where}: asset must be the recording\'s asset')
        assets: Dict[str, Any] = {}
        return {'layer': nest_panel(layer, _size(item.get('source'), f'{where}: source'), item['asset'], assets, comp), 'assets': assets}
    id_ = _text(item, 'id', where)
    box = _box(item.get('box'), f'{where}: box')
    if kind == 'mask':
        return panel_mask(id_, box, item.get('roundness', 36))
    if kind == 'rim':
        return rim_layer(id_, box, _text(item, 'color', where), _seconds(item, 'start', where, 0), _seconds(item, 'duration', where), item.get('roundness', 42))
    if kind == 'bubble':
        return bubble(id_, box, _text(item, 'color', where), _seconds(item, 'start', where, 0), _seconds(item, 'duration', where))
    raise InputError(f'{where}: kind must be mask, rim, bubble or nest')


def build(data: Any) -> Dict[str, Any]:
    """The script's whole job: the checked input in, the line it prints out."""
    if not isinstance(data, dict) or not isinstance(data.get('items'), list):
        raise InputError('the input must be one JSON object with an items list')
    comp = _size(data['frame'], 'frame') if data.get('frame') is not None else FRAME
    return {'items': [build_item(item, i, comp) for i, item in enumerate(data['items'])]}


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
        out = build(json.loads(text))
    except json.JSONDecodeError as err:
        return fail(f'the input is not JSON: {err}')
    except InputError as err:
        return fail(str(err))
    except (KeyError, IndexError, TypeError, ValueError, ZeroDivisionError) as err:
        return fail(f'cannot build from this input: {type(err).__name__} {err}')
    sys.stdout.buffer.write((json.dumps(out, separators=(',', ':'), ensure_ascii=False) + '\n').encode('utf-8'))
    return 0


def fail(reason: str, code: int = 1) -> int:
    sys.stderr.write('panels.py: ' + ' '.join(reason.split()) + '\n')
    return code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
