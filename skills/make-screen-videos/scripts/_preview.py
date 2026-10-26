"""
What each recording panel of a compiled scene shows at a scene time: the source window and the
source second. The diagnostics read it to tell when a panel shows past the content column.

It reads both clip modes: a masked media layer in the composition, and a panel-sized nested scene
(`clip: "nest"`). It models only what the compiler emits: one recording asset, `contain` fit,
scale and position keyframes. Not a renderer: text, rims and backdrops are not drawn.
"""
from __future__ import annotations

import math
from typing import Any, Dict, List, Optional

from _geometry import Box, Size, Vec2
from framing import fit_base

Json = Dict[str, Any]
# A panel shot: `id` (the panel layer's id), `at` (scene time), `srcTime` (source second on
# screen), `window` (the source-px window the panel shows, which can run past the recording's
# edge) and `panel` (the panel's size in composition px).
PanelShot = Dict[str, Any]


def panel_shots(scene: Json, at: float) -> List[PanelShot]:
    """Every recording panel on screen at scene time `at`."""
    rec = scene['assets']['rec']
    src: Size = {'w': rec['width'], 'h': rec['height']}
    comp: Size = {'w': scene['composition']['width'], 'h': scene['composition']['height']}
    shots: List[PanelShot] = []
    for layer in scene['layers']:
        if at < layer['start'] or at >= layer['start'] + layer['duration']:
            continue
        tau = at - layer['start']
        transform = layer.get('transform')
        if layer.get('mask') and _is_recording(layer['content']):
            m = layer['mask']['layer']
            w, h = m['content']['items'][0]['size']
            shots.append(_shot(layer['id'], at, tau, layer, src, comp, m['transform']['position'], {'w': w, 'h': h}))
        elif _is_recording(layer['content']) and transform and transform.get('scale'):
            # A panel that fills the frame: no mask, the composition clips it. (A backdrop is
            # unmasked too, but has no transform: it is cover-fit to the frame.)
            shots.append(_shot(layer['id'], at, tau, layer, src, comp, [comp['w'] / 2, comp['h'] / 2], comp))
        elif layer['content'].get('kind') == 'scene_ref':
            asset = scene['assets'].get(layer['content'].get('assetId'))
            nested: Optional[Json] = asset.get('scene') if asset else None
            inner_layers = nested.get('layers') if nested else None
            inner: Optional[Json] = inner_layers[0] if inner_layers else None
            if not nested or not inner or not _is_recording(inner['content']):
                continue
            box: Size = {'w': nested['composition']['width'], 'h': nested['composition']['height']}
            inner_start = inner.get('start')
            shots.append(_shot(layer['id'], at, tau - (0 if inner_start is None else inner_start), inner, src, box, [box['w'] / 2, box['h'] / 2], box))
    return shots


def _is_recording(content: Json) -> bool:
    kind = content.get('kind')
    if kind == 'media':
        return True
    clips = content.get('clips')
    return kind == 'track' and clips is not None and all(c['content'].get('kind') == 'media' for c in clips)


def _shot(id_: str, at: float, tau: float, layer: Json, src: Size, space: Size, center: Vec2, panel: Size) -> PanelShot:
    """`layer` is drawn in a `space`-sized composition, and its panel is centred on `center` there."""
    animations = layer.get('animations') or {}
    scale = sample(animations['scale']['keyframes'], tau)[0] if animations.get('scale') else layer['transform']['scale'][0]
    position = sample(animations['position']['keyframes'], tau) if animations.get('position') else layer['transform']['position']
    S = scale * fit_base(src, space)
    F = [src['w'] / 2 + (center[0] - position[0]) / S, src['h'] / 2 + (center[1] - position[1]) / S]
    w = panel['w'] / S
    h = panel['h'] / S
    window: Box = {'x': F[0] - w / 2, 'y': F[1] - h / 2, 'w': w, 'h': h}
    return {'id': id_, 'at': at, 'srcTime': source_time(layer['content'], tau), 'window': window, 'panel': panel}


def source_time(content: Json, tau: float) -> float:
    """The source second a media or track content shows `tau` seconds into its layer."""
    clips = content['clips'] if content.get('kind') == 'track' else [{'duration': math.inf, 'content': content}]
    t0 = 0
    for i, c in enumerate(clips):
        if tau < t0 + c['duration'] or i == len(clips) - 1:
            speed = c['content'].get('speed')
            return c['content']['trim']['in'] + (tau - t0) * (1 if speed is None else speed)
        t0 += c['duration']
    return math.nan


def sample(frames: List[Dict[str, Any]], t: float) -> Vec2:
    """A keyframed value at `t`: each segment eases by its first keyframe's curve."""
    if t <= frames[0]['time']:
        return frames[0]['value']
    for i in range(1, len(frames)):
        a = frames[i - 1]
        b = frames[i]
        if t > b['time']:
            continue
        u = _ease(a.get('easing'), (t - a['time']) / ((b['time'] - a['time']) or 1))
        return [a['value'][0] + (b['value'][0] - a['value'][0]) * u, a['value'][1] + (b['value'][1] - a['value'][1]) * u]
    return frames[-1]['value']


def _ease(easing: Any, x: float) -> float:
    if not easing or easing == 'linear':
        return x
    x1, y1, x2, y2 = easing['control']

    def bez(p1: float, p2: float, s: float) -> float:
        return 3 * (1 - s) * (1 - s) * s * p1 + 3 * (1 - s) * s * s * p2 + s * s * s

    # x(s) is monotonic for control x in [0, 1]: bisect for s, then read y.
    lo = 0.0
    hi = 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if bez(x1, x2, mid) < x:
            lo = mid
        else:
            hi = mid
    return bez(y1, y2, (lo + hi) / 2)
