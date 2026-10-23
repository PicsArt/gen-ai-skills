#!/usr/bin/env python3
"""
Check that every word of a scene sits inside the safe zone of where it will be watched.

    python3 scripts/safe_zone.py input.json
    python3 scripts/safe_zone.py < input.json

The input is one JSON object:

    {"scene": {...}, "destination": ["reels", "tiktok"],
     "measured": {"outro_cta": {"x": 300, "y": 880, "w": 480, "h": 70}}}

- `scene` is the scene document (a builder's whole output is read too: its `scene`).
- `destination` is one profile id, or a list of them: then the strictest of them holds, side by
  side, and every rail of each. An id it does not know falls back to `ebu`.
- `measured`, optional: a layer's box in frame px, by layer id, as `picsart_scene_query_layout`
  measured it at the first visible sampled time. A measured box replaces the static estimate;
  moving words carry that box through the sampled transforms and keep estimated text checks too.

The profiles, as fractions of the frame, so they hold at any size. `top`, `bottom`, `left` and
`right` are the margins words keep out of; a `rail` is a box the app draws its buttons over:

- `reels`: Instagram Reels as most posts are seen, about 250 px at the top and 480 px at the
  bottom of 1920, with the like and comment rail on the right.
- `reels-ads`: the strict Reels profile, 14% at the top and 35% at the bottom.
- `tiktok`: the top 10%, the caption and buttons at the bottom, and the right rail.
- `shorts`: YouTube Shorts: the top 10%, the bottom 20%, and the right rail.
- `landscape`: a 16:9 video for a site, YouTube or a course: the EBU graphics-safe area, 5% on
  every side.
- `ebu`: the same 5%, for anywhere else.

These are starting defaults from the platforms' published overlays and the guides that measure
them, not measured by us. The apps change their overlays, so check a hit on a real phone when it
matters.

A text layer's box is estimated from its words, unless `measured` gives it: each line is about
0.56 of the font size per character wide and 1.2 tall, scaled by the layer's `scale`, and placed
by its `alignment` (`center` centres it on `position`, `left` starts it there, `right` ends it
there; it is always centred vertically). Position, anchor, scale, rotation, parent chains and
composition cameras are evaluated at shared times, honoring cameraExempt. Key times, midpoints and
curve samples are clipped to visible lifetimes; zero effective opacity skips a sample. Nested
scenes, and inline compositions with their own `composition` size block, apply their fit and
canvas clipping before their enclosing transforms; an inline composition without one is collapsed
into its host's coordinates. Trim and speed map source clocks. Track clips play sequentially.
ParentId links carry transforms only, using each sized parent's intrinsic centre as its default
anchor. Masks in `mask.clip` keep their owner's opacity, lifetime and depth, with independent placement
and keys counted from the owner's start; their own z is ignored and the camera keeps its clock.
Legacy `mask.layer` is also read, with `clip` taking precedence. Sampling keeps geometric keys and segment curve samples;
the remaining grid is bounded to 96 times per layer and subsampled evenly. Layers with unknown
playback clocks are listed in `unmeasured` and their boxes are skipped. A captions layer is placed
by the renderer, so without a measured box it is listed in `unmeasured`. Only tracks that place
checked words are evaluated. An expression on any property except opacity or volume of a
text/captions layer, its parent chain, a containing composition/track/scene_ref layer or its
composition camera lists that text layer in `unmeasured` and skips its estimated boxes; an opacity
expression counts as visible. A box passed in `measured` is always checked, and takes the layer
out of `unmeasured`. `ok` is false while any layer is unmeasured or has a finding; expressions
on unrelated layers are ignored.

It prints one JSON line, `{ok, profiles, safe, rails, findings, unmeasured}`: `safe` and `rails`
in frame px. Each finding has a `code`, the `layer`, its `box`, `over` (how far it crosses each
side, in px), a `message` and a `fix`:

- `outside_safe_zone`: the words cross a margin;
- `under_rail`: the words sit under the app's buttons.

Input it cannot check exits 1, with one line on stderr that says what is wrong.

Python 3.9 or later, the standard library only, offline.
"""
from __future__ import annotations

import json
import math
import sys
from typing import Any, Callable, Dict, FrozenSet, Iterable, Iterator, List, Optional, Set, Tuple, Union

Box = Dict[str, float]

# Margins and rails as fractions of the frame. A rail is {x0, y0, x1, y1}.
PROFILES: Dict[str, Dict[str, Any]] = {
    'reels': {'top': 0.13, 'bottom': 0.25, 'left': 0.06, 'right': 0.06, 'rails': [{'x0': 0.86, 'y0': 0.5, 'x1': 1.0, 'y1': 0.75}]},
    'reels-ads': {'top': 0.14, 'bottom': 0.35, 'left': 0.06, 'right': 0.06, 'rails': [{'x0': 0.86, 'y0': 0.45, 'x1': 1.0, 'y1': 0.65}]},
    'tiktok': {'top': 0.10, 'bottom': 0.22, 'left': 0.06, 'right': 0.06, 'rails': [{'x0': 0.85, 'y0': 0.45, 'x1': 1.0, 'y1': 0.78}]},
    'shorts': {'top': 0.10, 'bottom': 0.20, 'left': 0.06, 'right': 0.06, 'rails': [{'x0': 0.85, 'y0': 0.5, 'x1': 1.0, 'y1': 0.8}]},
    'landscape': {'top': 0.05, 'bottom': 0.05, 'left': 0.05, 'right': 0.05, 'rails': []},
    'ebu': {'top': 0.05, 'bottom': 0.05, 'left': 0.05, 'right': 0.05, 'rails': []},
}
FALLBACK = 'ebu'

# The estimate of a line of text: per character, and per line, in font sizes.
CHAR_EM = 0.56
LINE_EM = 1.2

USAGE = 'usage: safe_zone.py [input.json]; with no file, the input is read from stdin'


class InputError(ValueError):
    """Input the script cannot check, with the reason."""


def zone(ids: List[str]) -> Dict[str, Any]:
    """The strictest of several profiles: the widest margin on each side, and every rail."""
    known = [i if i in PROFILES else FALLBACK for i in ids] or [FALLBACK]
    out: Dict[str, Any] = {side: max(PROFILES[i][side] for i in known) for side in ('top', 'bottom', 'left', 'right')}
    rails: List[Dict[str, float]] = []
    for i in known:
        for r in PROFILES[i]['rails']:
            if r not in rails:
                rails.append(r)
    out['rails'] = rails
    out['ids'] = list(dict.fromkeys(known))
    return out


def safe_box(z: Dict[str, Any], w: float, h: float) -> Box:
    x, y = z['left'] * w, z['top'] * h
    return {'x': round(x, 1), 'y': round(y, 1), 'w': round(w - x - z['right'] * w, 1), 'h': round(h - y - z['bottom'] * h, 1)}


def rail_boxes(z: Dict[str, Any], w: float, h: float) -> List[Box]:
    return [{'x': round(r['x0'] * w, 1), 'y': round(r['y0'] * h, 1), 'w': round((r['x1'] - r['x0']) * w, 1), 'h': round((r['y1'] - r['y0']) * h, 1)} for r in z['rails']]


def _vec(v: Any) -> Optional[List[float]]:
    if isinstance(v, (list, tuple)) and len(v) == 2 and all(isinstance(n, (int, float)) and not isinstance(n, bool) for n in v):
        return [float(v[0]), float(v[1])]
    return None


def _track(layer: Dict[str, Any], prop: str) -> List[List[float]]:
    """Every value a transform property takes: its keyframes, or its static value."""
    keys = ((layer.get('animations') or {}).get(prop) or {}).get('keyframes') or []
    values = [v for v in (_vec(k.get('value')) for k in keys if isinstance(k, dict)) if v]
    if values:
        return values
    static = _vec((layer.get('transform') or {}).get(prop))
    return [static] if static else []


# How far apart, in px, the checked points on a moving layer's path are.
PATH_STEP = 8.0
TRANSFORM_SAMPLES = 16
BOX_SAMPLES = 96


def _bounded_boxes(boxes: Iterable[Box]) -> List[Box]:
    """Dedupe at pixel precision, retaining exact side extremes even within a pixel bucket."""
    unique = {}
    extremes = [None] * 4
    scores = [math.inf] * 4
    for b in boxes:
        edges = (b['x'], b['y'], -b['x'] - b['w'], -b['y'] - b['h'])
        for i, edge in enumerate(edges):
            if edge < scores[i]:
                scores[i], extremes[i] = edge, b
        unique.setdefault(tuple(round(b[k]) for k in ('x', 'y', 'w', 'h')), b)
    values = list(unique.values())
    # Reserve room for exact extrema, which must survive both deduplication and subsampling.
    limit = BOX_SAMPLES - 4
    if len(values) > limit:
        values = [values[round(i * (len(values) - 1) / (limit - 1))] for i in range(limit)]
    for b in extremes:
        if b is not None and b not in values:
            values.append(b)
    return values


def _roots(a: float, b: float, c: float) -> List[float]:
    """Real roots of a quadratic (or linear derivative)."""
    if abs(a) < 1e-12:
        return [-c / b] if abs(b) > 1e-12 else []
    d = b * b - 4 * a * c
    return [(-b - math.sqrt(d)) / (2 * a), (-b + math.sqrt(d)) / (2 * a)] if d >= 0 else []


def _bezier_range(easing: Any) -> Tuple[float, float]:
    """The least and greatest progress an easing reaches: past 0 and 1 when it overshoots."""
    if not isinstance(easing, dict) or easing.get('kind') != 'cubic_bezier':
        return 0.0, 1.0
    c = easing.get('control') or []
    if len(c) != 4 or not all(isinstance(n, (int, float)) and not isinstance(n, bool) for n in c):
        return 0.0, 1.0
    y1, y2 = float(c[1]), float(c[3])
    ys = [3 * (1 - t) ** 2 * t * y1 + 3 * (1 - t) * t ** 2 * y2 + t ** 3 for t in (i / 200 for i in range(201))]
    return min(0.0, min(ys)), max(1.0, max(ys))


def _path(layer: Dict[str, Any]) -> List[List[float]]:
    """Every position a layer passes through: its keyframes, and points along the moves between them."""
    keys = [k for k in ((layer.get('animations') or {}).get('position') or {}).get('keyframes') or [] if isinstance(k, dict) and _vec(k.get('value'))]
    if not keys:
        return _track(layer, 'position')
    out = [_vec(keys[0]['value'])]
    for a, b in zip(keys, keys[1:]):
        pa, pb = _vec(a['value']), _vec(b['value'])
        ta, tb = _vec(a.get('outTangent')), _vec(b.get('inTangent'))
        if (pa == pb and not ta and not tb) or a.get('easing') == 'step':
            out.append(pb)
            continue
        lo, hi = _bezier_range(a.get('easing', 'linear'))
        dist = ((pb[0] - pa[0]) ** 2 + (pb[1] - pa[1]) ** 2) ** 0.5 * (hi - lo)
        ca = [pa[j] + (ta or [0, 0])[j] for j in range(2)]
        cb = [pb[j] + (tb or [0, 0])[j] for j in range(2)]
        if ta or tb:
            dist = 3 * max(math.hypot(v[0] - u[0], v[1] - u[1]) for u, v in ((pa, ca), (ca, cb), (cb, pb))) * (hi - lo) * max(abs(1 - lo) + abs(lo), abs(1 - hi) + abs(hi)) ** 2
        n = max(1, int(dist // PATH_STEP) + 1)
        for i in range(n + 1):
            t = lo + (hi - lo) * i / n
            if ta or tb:
                out.append([(1 - t) ** 3 * pa[j] + 3 * (1 - t) ** 2 * t * ca[j] + 3 * (1 - t) * t ** 2 * cb[j] + t ** 3 * pb[j] for j in range(2)])
            else:
                out.append([pa[0] + (pb[0] - pa[0]) * t, pa[1] + (pb[1] - pa[1]) * t])
        out.append(pb)
    return out


def _scale_values(layer: Dict[str, Any], reach: float = 0) -> List[List[float]]:
    """Scale states, including easing overshoot and steps along a nested scene's swept area."""
    keys = [k for k in ((layer.get('animations') or {}).get('scale') or {}).get('keyframes') or [] if isinstance(k, dict) and _vec(k.get('value'))]
    values = [_vec(k['value']) for k in keys] or _track(layer, 'scale') or [[1.0, 1.0]]
    for a, b in zip(keys, keys[1:]):
        if a.get('easing') == 'step':
            continue
        sa, sb = _vec(a['value']), _vec(b['value'])
        ta, tb = _vec(a.get('outTangent')), _vec(b.get('inTangent'))
        lo, hi = _bezier_range(a.get('easing', 'linear'))
        n = max(1, int(max(abs(sb[j] - sa[j]) for j in range(2)) * reach * (hi - lo) / PATH_STEP) + 1)
        if ta or tb:
            ca = [sa[j] + (ta or [0, 0])[j] for j in range(2)]
            cb = [sb[j] + (tb or [0, 0])[j] for j in range(2)]
            dist = 3 * max(math.hypot(v[0] - u[0], v[1] - u[1]) for u, v in ((sa, ca), (ca, cb), (cb, sb)))
            n = max(200, int(dist * reach * (hi - lo) * max(abs(1 - lo) + abs(lo), abs(1 - hi) + abs(hi)) ** 2 / PATH_STEP) + 1)
        n = min(n, max(1, (TRANSFORM_SAMPLES - 1) // max(1, len(keys) - 1)))
        times = {lo + (hi - lo) * i / n for i in range(n + 1)}
        if ta or tb:
            # Include exact spatial extrema; a uniform cap alone can miss a tangent peak.
            for j in range(2):
                aa = -sa[j] + 3 * ca[j] - 3 * cb[j] + sb[j]
                bb = 3 * sa[j] - 6 * ca[j] + 3 * cb[j]
                cc = -3 * sa[j] + 3 * ca[j]
                times.update(t for t in _roots(3 * aa, 2 * bb, cc) if lo <= t <= hi)
        for t in sorted(times):
            if ta or tb:
                values.append([(1 - t) ** 3 * sa[j] + 3 * (1 - t) ** 2 * t * ca[j] + 3 * (1 - t) * t ** 2 * cb[j] + t ** 3 * sb[j] for j in range(2)])
            else:
                values.append([sa[j] + (sb[j] - sa[j]) * t for j in range(2)])
    return [list(v) for v in dict.fromkeys(tuple(v) for v in values)]


def _scale_reach(layer: Dict[str, Any]) -> Tuple[float, float]:
    """The largest scale a layer reaches on each axis, including easing overshoot."""
    values = _scale_values(layer)
    return max(abs(v[0]) for v in values), max(abs(v[1]) for v in values)


def _rotations(layer: Dict[str, Any]) -> List[float]:
    """Static and animated angles, including the turns between keyframes."""
    keys = [k for k in ((layer.get('animations') or {}).get('rotation') or {}).get('keyframes') or [] if isinstance(k, dict) and isinstance(k.get('value'), (int, float))]
    angles = [float(k['value']) for k in keys] or [float((layer.get('transform') or {}).get('rotation') or 0)]
    for a, b in zip(keys, keys[1:]):
        if a.get('easing') == 'step':
            continue
        lo, hi = _bezier_range(a.get('easing'))
        start, end = (a['value'] + (b['value'] - a['value']) * t for t in (lo, hi))
        n = min(max(1, (TRANSFORM_SAMPLES - 1) // max(1, len(keys) - 1)), max(1, int(abs(end - start)) + 1))
        angles += [start + (end - start) * i / n for i in range(n + 1)]
    return list(dict.fromkeys(angles))


def _rotated(b: Box, pivot: List[float], angle: float) -> Box:
    """The enclosing frame rectangle after turning the four corners about the layer's position."""
    c, s = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    dx, dy = b['x'] + b['w'] / 2 - pivot[0], b['y'] + b['h'] / 2 - pivot[1]
    cx, cy = pivot[0] + dx * c - dy * s, pivot[1] + dx * s + dy * c
    w, h = abs(b['w'] * c) + abs(b['h'] * s), abs(b['w'] * s) + abs(b['h'] * c)
    return {'x': round(cx - w / 2, 1), 'y': round(cy - h / 2, 1), 'w': round(w, 1), 'h': round(h, 1)}


def text_lines(content: Dict[str, Any]) -> List[str]:
    t = content.get('text')
    if isinstance(t, str):
        return t.split('\n')
    if isinstance(t, list):
        return [str(x) for x in t]
    return []


def wrapped(lines: List[str], size: float, width: float) -> List[str]:
    """The lines as the renderer wraps them at `width` px, word by word, at the estimated glyph width."""
    most = max(1, int(width // (size * CHAR_EM))) if width > 0 else 0
    out: List[str] = []
    for line in lines:
        row = ''
        for word in line.split(' '):
            if row and most and len(row) + 1 + len(word) > most:
                out.append(row)
                row = word
            else:
                row = f'{row} {word}' if row else word
        out.append(row)
    return out


def text_boxes(layer: Dict[str, Any], comp: Tuple[float, float]) -> List[Box]:
    """The estimated box of a text layer at each position it takes or passes through, in frame px."""
    content = layer.get('content') or {}
    size = float(((content.get('font') or {}).get('size')) or 48)
    # A line wraps at the content's wrapWidth, else at the composition's full width.
    wrap = content.get('wrapWidth')
    lines = wrapped(text_lines(content), size, float(wrap) if isinstance(wrap, (int, float)) and wrap > 0 else comp[0])
    sx, sy = _scale_reach(layer)
    w = max((len(line) for line in lines), default=0) * size * CHAR_EM * sx
    h = max(1, len(lines)) * size * LINE_EM * sy
    align = content.get('alignment', 'center')
    out = []
    angles = _rotations(layer)
    for p in _path(layer) or [[comp[0] / 2, comp[1] / 2]]:
        x = p[0] - w / 2 if align == 'center' else (p[0] if align == 'left' else p[0] - w)
        b = {'x': round(x, 1), 'y': round(p[1] - h / 2, 1), 'w': round(w, 1), 'h': round(h, 1)}
        out += [_rotated(b, p, angle) for angle in angles]
    return _bounded_boxes(out)


def _overlap(a: Box, b: Box) -> bool:
    return a['x'] < b['x'] + b['w'] and b['x'] < a['x'] + a['w'] and a['y'] < b['y'] + b['h'] and b['y'] < a['y'] + a['h']


BoxBatch = Union[Box, List[Box]]
Place = Callable[[BoxBatch], List[Box]]


def _same(b: BoxBatch) -> List[Box]:
    return [b] if isinstance(b, dict) else b


def _fit_scale(content: Dict[str, Any], inner: Tuple[float, float], host: Tuple[float, float]) -> Tuple[float, float]:
    """How much a `scene_ref`'s fit scales its scene: into its `bounds`, or the host composition (`contain` by default)."""
    fit = content.get('fit', 'contain')
    box = _vec(content.get('bounds')) or list(host)
    if fit == 'none' or inner[0] <= 0 or inner[1] <= 0:
        return 1.0, 1.0
    fx, fy = box[0] / inner[0], box[1] / inner[1]
    if fit == 'fill':
        return fx, fy
    k = max(fx, fy) if fit == 'cover' else min(fx, fy)
    return k, k


def _placed_by(ref: Dict[str, Any], inner: Tuple[float, float], host: Tuple[float, float], outer: Place, clip: bool = False) -> Place:
    """
    Where a box in a nested scene lands: the scene is scaled by its fit and its layer's scale, and
    placed about its anchor at its layer's position.
    """
    positions = _path(ref) or [[host[0] / 2, host[1] / 2]]
    fx, fy = _fit_scale(ref.get('content') or {}, inner, host)
    scales = _scale_values(ref, max(inner[0] * abs(fx), inner[1] * abs(fy)))
    angles = _rotations(ref)
    anchor = _vec((ref.get('transform') or {}).get('anchor')) or [inner[0] / 2, inner[1] / 2]

    def place(boxes: BoxBatch) -> List[Box]:
        boxes = _same(boxes)
        if clip:
            clipped = []
            for b in boxes:
                x0, y0 = max(0.0, b['x']), max(0.0, b['y'])
                x1, y1 = min(inner[0], b['x'] + b['w']), min(inner[1], b['y'] + b['h'])
                if x1 > x0 and y1 > y0:
                    clipped.append({'x': x0, 'y': y0, 'w': x1 - x0, 'h': y1 - y0})
            boxes = _bounded_boxes(clipped)

        def shapes() -> Iterator[Box]:
            # Rotation about the position commutes with translation: sample shape first.
            for b in boxes:
                for rx, ry in scales:
                    sx, sy = fx * rx, fy * ry
                    x0, x1 = ((x - anchor[0]) * sx for x in (b['x'], b['x'] + b['w']))
                    y0, y1 = ((y - anchor[1]) * sy for y in (b['y'], b['y'] + b['h']))
                    moved = {'x': round(min(x0, x1), 1), 'y': round(min(y0, y1), 1),
                             'w': round(abs(x1 - x0), 1), 'h': round(abs(y1 - y0), 1)}
                    for angle in angles:
                        yield _rotated(moved, [0, 0], angle)

        shaped = _bounded_boxes(shapes())
        moved = _bounded_boxes({'x': round(b['x'] + p[0], 1), 'y': round(b['y'] + p[1], 1),
                                'w': b['w'], 'h': b['h']} for p in positions for b in shaped)
        return outer(moved)
    return place


def _assets(scene: Dict[str, Any]) -> Dict[str, Any]:
    declared = scene.get('assets') or []
    if isinstance(declared, dict):
        return {k: a for k, a in declared.items() if isinstance(a, dict)}
    return {a.get('id'): a for a in declared if isinstance(a, dict)}


def words_layers(scene: Dict[str, Any], place: Place = _same, comp: Optional[Tuple[float, float]] = None, seen: FrozenSet[int] = frozenset(), unmeasured: bool = False) -> Iterator[Tuple[Dict[str, Any], Place, Tuple[float, float]]]:
    """
    Every text and captions layer, with how its boxes land in the frame and the size of the scene it
    is in: a track's clips are placed by their layer, and a nested scene's layers by its `scene_ref`.
    """
    c = scene.get('composition') or {}
    size = comp or (float(c.get('width') or 1080), float(c.get('height') or 1920))
    assets = _assets(scene)
    for layer in scene.get('layers') or []:
        if not isinstance(layer, dict):
            continue
        unknown = unmeasured or any(isinstance(track, dict) and 'expression' in track for track in (layer.get('animations') or {}).values())
        mask_spec = layer.get('mask') or {}
        mask = mask_spec.get('clip') or mask_spec.get('layer')
        if isinstance(mask, dict):
            yield from words_layers({**scene, 'layers': [mask]}, place, size, seen, unknown)
        content = layer.get('content') or {}
        kind = content.get('kind')
        if kind in ('text', 'captions'):
            yield {**layer, '_unmeasured': True} if unknown else layer, place, size
        elif kind == 'composition':
            inner = {**scene, 'layers': content.get('layers') or []}
            yield from words_layers(inner, _placed_by({**layer, 'content': {'fit': 'none'}}, size, size, place), size, seen, unknown)
        elif kind == 'track':
            for clip in content.get('clips') or []:
                if isinstance(clip, dict) and isinstance(clip.get('content'), dict):
                    child = {**clip, 'id': clip.get('id', layer.get('id', ''))}
                    parent = _placed_by({**layer, 'content': {'fit': 'none'}}, size, size, place)
                    yield from words_layers({**scene, 'layers': [child]}, parent, size, seen, unknown)
        elif kind == 'scene_ref':
            ref = content.get('assetId')
            inner = (content.get('asset') or assets.get(ref) or {}).get('scene')
            if isinstance(inner, dict) and id(inner) not in seen:
                ic = inner.get('composition') or {}
                inner_size = (float(ic.get('width') or size[0]), float(ic.get('height') or size[1]))
                yield from words_layers(inner, _placed_by(layer, inner_size, size, place, clip=True), inner_size, seen | {id(inner)}, unknown)


def _timed(layer: Dict[str, Any], offset: float = 0, rate: float = 1) -> Dict[str, Any]:
    """Carry a placement source; compile its tracks only when checked words need it."""
    return {'layer': layer, 'tracks': None, 'offset': offset, 'rate': rate}


def _tracks(source: Dict[str, Any]) -> Dict[str, Any]:
    """Compile once, with key times in the outer composition's seconds."""
    if source['tracks'] is not None:
        return source['tracks']
    layer, offset, rate = source['layer'], source['offset'], source['rate']
    tracks = {}
    for prop, track in (layer.get('animations') or {}).items():
        if not isinstance(track, dict):
            continue
        base = offset + (float(layer.get('start') or 0) / rate if track.get('timeMode', layer.get('timeMode', 'composition')) == 'layer' else 0)
        keys = sorted([{**k, 'time': base + float(k.get('time', i)) / rate} for i, k in enumerate(track.get('keyframes') or []) if isinstance(k, dict)], key=lambda k: k['time'])
        if keys:
            tracks[prop] = keys
    source['tracks'] = tracks
    return tracks


# Tracks that never move or resize words: an expression on one leaves the geometry measurable.
NON_GEOMETRIC = ('opacity', 'volume')


def _spatial_expression(layer: Dict[str, Any]) -> bool:
    """Whether an expression can place or size this layer's words."""
    return any(isinstance(track, dict) and 'expression' in track and prop not in NON_GEOMETRIC
               for prop, track in (layer.get('animations') or {}).items())


def _opacity_expression(source: Dict[str, Any]) -> bool:
    track = (source['layer'].get('animations') or {}).get('opacity')
    return isinstance(track, dict) and 'expression' in track


def _ease(easing: Any, t: float) -> float:
    if easing == 'step':
        return 0.0
    named = {'ease_in': [0.42, 0, 1, 1], 'ease_out': [0, 0, 0.58, 1],
             'ease_in_out': [0.42, 0, 0.58, 1]}
    if isinstance(easing, str) and easing in named:
        control = named[easing]
    elif isinstance(easing, dict) and easing.get('kind') == 'cubic_bezier':
        control = easing.get('control') or []
    else:
        return t
    if len(control) != 4:
        return t
    x1, y1, x2, y2 = control
    lo, hi = 0.0, 1.0
    for _ in range(24):
        u = (lo + hi) / 2
        x = 3 * (1 - u) ** 2 * u * x1 + 3 * (1 - u) * u ** 2 * x2 + u ** 3
        if x < t:
            lo = u
        else:
            hi = u
    u = (lo + hi) / 2
    return 3 * (1 - u) ** 2 * u * y1 + 3 * (1 - u) * u ** 2 * y2 + u ** 3


def _value(source: Dict[str, Any], prop: str, time: float, default: Any) -> Any:
    """Evaluate one property at the same time as every other transform in the chain."""
    keys = _tracks(source).get(prop) or []
    if not keys:
        return (source['layer'].get('transform') or {}).get(prop, default)
    if time <= keys[0]['time']:
        return keys[0]['value']
    lo, hi = 0, len(keys)
    while lo < hi:
        mid = (lo + hi) // 2
        if time < keys[mid]['time']:
            hi = mid
        else:
            lo = mid + 1
    if lo == len(keys):
        return keys[-1]['value']
    a, b = keys[lo - 1], keys[lo]
    t = _ease(a.get('easing'), (time - a['time']) / (b['time'] - a['time']))
    va, vb = a['value'], b['value']
    if isinstance(va, (list, tuple)):
        ta, tb = _vec(a.get('outTangent')), _vec(b.get('inTangent'))
        if ta or tb:
            return [(1 - t) ** 3 * va[j] + 3 * (1 - t) ** 2 * t * (va[j] + (ta or [0, 0])[j]) + 3 * (1 - t) * t ** 2 * (vb[j] + (tb or [0, 0])[j]) + t ** 3 * vb[j] for j in range(2)]
        return [v + (vb[j] - v) * t for j, v in enumerate(va)]
    return va + (vb - va) * t


def _times(sources: List[Dict[str, Any]], start: float, end: float,
           required: Optional[Set[float]] = None) -> List[float]:
    """A bounded grid, collecting collision-bearing keys separately when requested."""
    times = {start, end}
    for source in sources:
        for prop, keys in _tracks(source).items():
            track_times = set()
            for a, b in zip(keys, keys[1:]):
                if a['time'] >= end or b['time'] <= start or a.get('easing') == 'step':
                    continue
                va, vb = _vec(a.get('value')), _vec(b.get('value'))
                ta, tb = _vec(a.get('outTangent')), _vec(b.get('inTangent'))
                if va and vb and (ta or tb):
                    progress = {i / 16 for i in range(1, 16)}
                    for j in range(2):
                        ca, cb = va[j] + (ta or [0, 0])[j], vb[j] + (tb or [0, 0])[j]
                        progress.update(t for t in _roots(3 * (-va[j] + 3 * ca - 3 * cb + vb[j]),
                                                         6 * (va[j] - 2 * ca + cb), 3 * (ca - va[j]))
                                        if 0 < t < 1)
                    # Keep extrema for linear curves and a local grid for eased curves.
                    track_times.update(t for p in progress for t in [a['time'] + (b['time'] - a['time']) * p]
                                       if start <= t <= end)
            for i, key in enumerate(keys):
                t = key['time']
                if start <= t <= end:
                    track_times.add(t)
                    # A step's departing value must also be checked immediately before the cut.
                    if start < t and i and keys[i - 1].get('easing') == 'step':
                        track_times.add(math.nextafter(t, start))
            times.update(track_times)
            if required is not None and prop not in NON_GEOMETRIC:
                required.update(track_times)
    ordered = sorted(times)
    times.update((a + b) / 2 for a, b in zip(ordered, ordered[1:]))
    if len(times) > BOX_SAMPLES:
        ordered = sorted(times)
        step = (len(ordered) - 1) / (BOX_SAMPLES - 1)
        return [ordered[round(i * step)] for i in range(BOX_SAMPLES)]
    room = BOX_SAMPLES - len(times)
    if any(_tracks(s) for s in sources):
        times.update(start + (end - start) * i / (room + 1) for i in range(1, room + 1))
    return sorted(times)


def _window(source: Dict[str, Any], window: Tuple[float, float]) -> Tuple[float, float]:
    layer = source['layer']
    start = source['offset'] + float(layer.get('start') or 0) / source['rate']
    end = start + float(layer['duration']) / source['rate'] if layer.get('duration') is not None else window[1]
    return max(window[0], start), min(window[1], end)


def _corners(points: List[List[float]], source: Dict[str, Any], time: float,
             position: List[float], anchor: List[float], fit: Tuple[float, float]) -> List[List[float]]:
    p = _value(source, 'position', time, position)
    a = _value(source, 'anchor', time, anchor)
    scale = _value(source, 'scale', time, [1, 1])
    angle = math.radians(_value(source, 'rotation', time, 0))
    c, s = math.cos(angle), math.sin(angle)
    out = []
    for x, y in points:
        dx, dy = (x - a[0]) * scale[0] * fit[0], (y - a[1]) * scale[1] * fit[1]
        out.append([p[0] + dx * c - dy * s, p[1] + dx * s + dy * c])
    return out


def _clip_polygon(points: List[List[float]], size: Tuple[float, float]) -> List[List[float]]:
    """Clip the transformed corners before the enclosing scene reference places them."""
    for axis, edge, sign in ((0, 0, 1), (0, size[0], -1), (1, 0, 1), (1, size[1], -1)):
        out = []
        for a, b in zip(points, points[1:] + points[:1]):
            inside_a, inside_b = (a[axis] - edge) * sign >= 0, (b[axis] - edge) * sign >= 0
            if inside_a != inside_b:
                t = (edge - a[axis]) / (b[axis] - a[axis])
                out.append([a[j] + t * (b[j] - a[j]) for j in range(2)])
            if inside_b:
                out.append(b)
        points = out
    return points


def _points(points: List[List[float]], ops: List[Any], time: float, clip: bool = True) -> List[List[float]]:
    """Apply the scoped transforms and camera, optionally clipping to nested canvases."""
    depth = 0.0
    for op in ops:
        if op[0] == 'transform':
            points = _corners(points, op[1], time, op[2], op[3], op[4])
            depth += _value(op[1], 'z', time, 0)
        elif op[0] == 'depth':
            depth += sum(_value(source, 'z', time, 0) for source in op[1])
        elif op[0] == 'flat':
            depth = 0.0
        elif op[0] == 'camera':
            source = op[1]
            pivot = _value(source, 'position', time, _value(source, 'pivot', time, [op[2][0] / 2, op[2][1] / 2]))
            zoom = _value(source, 'zoom', time, 1)
            distance = _value(source, 'distance', time, op[2][0] * 50 / 36)
            if depth >= distance:
                return []
            zoom *= distance / (distance - depth)
            depth = 0.0
            angle = math.radians(_value(source, 'rotation', time, 0))
            c, s = math.cos(angle), math.sin(angle)
            points = [[pivot[0] + zoom * ((x - pivot[0]) * c - (y - pivot[1]) * s),
                       pivot[1] + zoom * ((x - pivot[0]) * s + (y - pivot[1]) * c)] for x, y in points]
        elif clip:
            points = _clip_polygon(points, op[1])
    return points


def _measured_boxes(box: Box, placements: List[Any], ops: List[Any], times: List[float]) -> Optional[List[Box]]:
    """Move a frame measurement from the first visible placement through the sampled motion."""
    if not placements or (all(p == placements[0] for p in placements) and not any(op[0] == 'clip' for op in ops)):
        return [box]
    origin, xaxis, yaxis = placements[0]
    ax, ay = xaxis[0] - origin[0], xaxis[1] - origin[1]
    bx, by = yaxis[0] - origin[0], yaxis[1] - origin[1]
    det = ax * by - ay * bx
    if abs(det) < 1e-12:
        return None
    local = [((by * (x - origin[0]) - bx * (y - origin[1])) / det,
              (ax * (y - origin[1]) - ay * (x - origin[0])) / det)
             for x in (box['x'], box['x'] + box['w']) for y in (box['y'], box['y'] + box['h'])]
    local = [local[i] for i in (0, 2, 3, 1)]
    boxes = []
    for time in times:
        points = _points(local, ops, time)
        if points:
            xs, ys = [p[0] for p in points], [p[1] for p in points]
            boxes.append({'x': round(min(xs), 1), 'y': round(min(ys), 1),
                          'w': round(max(xs) - min(xs), 1), 'h': round(max(ys) - min(ys), 1)})
    return boxes


def _parent_anchor(layer: Dict[str, Any], size: Tuple[float, float], assets: Dict[str, Any]) -> List[float]:
    """The intrinsic centre of a sized parent; text, shapes and empty rigs use the origin."""
    content = layer.get('content') or {}
    kind = content.get('kind')
    if kind == 'scene_ref':
        inner = (content.get('asset') or assets.get(content.get('assetId')) or {}).get('scene') or {}
        dimensions = inner.get('composition') or {}
    elif kind == 'composition':
        dimensions = content.get('composition') or {}
    elif kind in ('color', 'track'):
        dimensions = content
    elif kind == 'media':
        bounds = _vec(content.get('bounds'))
        if bounds:
            return [v / 2 for v in bounds]
        dimensions = (content.get('asset') or assets.get(content.get('assetId')) or {}) if content.get('fit') == 'none' else {}
    else:
        return [0, 0]
    return [float(dimensions.get('width') or size[0]) / 2,
            float(dimensions.get('height') or size[1]) / 2]


def _sampled_layers(scene: Dict[str, Any], outer: Optional[List[Any]] = None,
                    sources: Optional[List[Dict[str, Any]]] = None, offset: float = 0,
                    window: Optional[Tuple[float, float]] = None,
                    seen: FrozenSet[int] = frozenset(), size: Optional[Tuple[float, float]] = None,
                    clipped: bool = False, rate: float = 1,
                    unmeasured: bool = False, camera_source: Optional[Dict[str, Any]] = None,
                    plane: Optional[List[Dict[str, Any]]] = None) -> Iterator[Tuple[Dict[str, Any], List[Box]]]:
    """Walk words with scoped transforms, carrying time through every enclosing scene."""
    comp = scene.get('composition') or {}
    size = size or (float(comp.get('width') or 1080), float(comp.get('height') or 1920))
    window = window if window is not None else (offset, math.inf)
    if comp.get('duration') is not None:
        window = (max(window[0], offset), min(window[1], offset + float(comp['duration']) / rate))
    outer, sources = outer or [], sources or []
    layers = [l for l in scene.get('layers') or [] if isinstance(l, dict)]
    by_id = {l.get('id'): l for l in layers if l.get('id')}
    assets = _assets(scene)
    camera = comp.get('camera') or {}
    if camera_source is None:
        camera_source = _timed({'transform': {k: v for k, v in camera.items() if not isinstance(v, dict)},
                                'animations': {**{k: v for k, v in camera.items() if isinstance(v, dict) and k != 'animations'}, **(camera.get('animations') or {})}}, offset, rate)
    for layer in layers:
        content = layer.get('content') or {}
        kind = content.get('kind')
        mask_spec = layer.get('mask') or {}
        mask = mask_spec.get('clip') or mask_spec.get('layer')
        if kind not in ('text', 'captions', 'composition', 'track', 'scene_ref') and not isinstance(mask, dict):
            continue
        chain, identities = [], set()
        node = layer
        while node is not None:
            if id(node) in identities:
                raise InputError(f"{layer.get('id', '')}: cyclic parentId chain")
            identities.add(id(node))
            source_layer = node if node is layer else {
                **node, 'transform': {k: v for k, v in (node.get('transform') or {}).items() if k != 'opacity'},
                'animations': {k: v for k, v in (node.get('animations') or {}).items() if k != 'opacity'}}
            chain.append(_timed(source_layer, offset, rate))
            parent = node.get('parentId')
            if parent and parent not in by_id:
                raise InputError(f"{layer.get('id', '')}: missing parentId {parent}")
            node = by_id.get(parent) if parent else None
        local_window = _window(chain[0], window)
        all_sources = sources + chain
        if isinstance(mask, dict):
            owner = _timed({**layer, 'transform': {'opacity': (layer.get('transform') or {}).get('opacity', 1)},
                            'animations': {k: v for k, v in (layer.get('animations') or {}).items() if k == 'opacity'}}, offset, rate)
            depth_sources = (plane or []) + [_timed({
                'transform': {k: v for k, v in (s['layer'].get('transform') or {}).items() if k == 'z'},
                'animations': {k: v for k, v in (s['layer'].get('animations') or {}).items() if k == 'z'},
                'start': s['layer'].get('start', 0), 'timeMode': s['layer'].get('timeMode', 'composition')},
                s['offset'], s['rate']) for s in chain]
            mask = {**mask, 'transform': {k: v for k, v in (mask.get('transform') or {}).items() if k != 'z'},
                    'animations': {k: v for k, v in (mask.get('animations') or {}).items() if k != 'z'},
                    'cameraExempt': mask.get('cameraExempt') or any(s['layer'].get('cameraExempt') for s in chain)}
            mask_offset = offset
            if mask_spec.get('clip'):
                mask_offset += float(layer.get('start') or 0) / rate
                mask = {**mask, 'start': 0, 'duration': layer.get('duration')}
            yield from _sampled_layers({**scene, 'layers': [mask]}, outer, sources + [owner], mask_offset,
                                       local_window, seen, size, clipped, rate, unmeasured,
                                       camera_source=camera_source, plane=depth_sources)
        if kind not in ('text', 'captions', 'composition', 'track', 'scene_ref'):
            continue
        ops = []
        for i, source in enumerate(chain):
            position = [size[0] / 2, size[1] / 2]
            anchor, fit = _parent_anchor(source['layer'], size, assets) if i else [0, 0], (1, 1)
            if i == 0 and kind in ('composition', 'track', 'scene_ref'):
                inner = (content.get('asset') or assets.get(content.get('assetId')) or {}).get('scene') if kind == 'scene_ref' else None
                # An inline composition with its own size block has a canvas, placed like a scene.
                canvas = kind == 'composition' and isinstance(content.get('composition'), dict)
                ic = ((inner or {}).get('composition') or {}) if kind == 'scene_ref' else (content.get('composition') if canvas else {})
                inner_size = (float(ic.get('width') or size[0]), float(ic.get('height') or size[1]))
                anchor = [inner_size[0] / 2, inner_size[1] / 2]
                fit = _fit_scale(content, inner_size, size) if kind == 'scene_ref' or canvas else (1, 1)
            ops.append(('transform', source, position, anchor, fit))
        if plane:
            ops.append(('depth', plane))
            all_sources += plane
        if not any(s['layer'].get('cameraExempt') for s in chain):
            ops.append(('camera', camera_source, size))
            all_sources = all_sources + [camera_source]
        else:
            ops.append(('flat',))
        if clipped:
            ops.append(('clip', size))
        ops += outer
        if kind in ('text', 'captions'):
            if local_window[1] <= local_window[0]:
                yield layer, []
                continue
            if unmeasured or any(_spatial_expression(source['layer']) for source in all_sources):
                yield {**layer, '_unmeasured': True}, []
                continue
            # No authored duration means the latest relevant key is the end of the checked span.
            end = local_window[1]
            if math.isinf(end):
                end = max([local_window[0]] + [k['time'] for s in all_sources for ks in _tracks(s).values() for k in ks])
            else:
                end = math.nextafter(end, local_window[0])
            required: Set[float] = set()
            times = _times(all_sources, local_window[0], end, required)
            # A bounded grid alone can miss a brief rail hold or curve excursion.
            times = sorted(required | set(times))
            boxes, placements, visible_times = [], [], []
            if kind == 'text':
                static = {**layer, 'transform': {'position': [0, 0]}, 'animations': {}}
                b = text_boxes(static, size)[0]
                corners = [[x, y] for x in (b['x'], b['x'] + b['w']) for y in (b['y'], b['y'] + b['h'])]
                corners = [corners[i] for i in (0, 2, 3, 1)]
            for time in times:
                # An opacity expression cannot be evaluated: assume the words are visible.
                if any(_value(s, 'opacity', time, 1) <= 0 for s in all_sources if not _opacity_expression(s)):
                    continue
                placement = _points([[0, 0], [1, 0], [0, 1]], ops, time, clip=False)
                if not placement:
                    continue
                placements.append(placement)
                visible_times.append(time)
                if kind == 'captions':
                    boxes.append({})
                    continue
                points = _points(corners, ops, time)
                if points:
                    xs, ys = [p[0] for p in points], [p[1] for p in points]
                    boxes.append({'x': round(min(xs), 1), 'y': round(min(ys), 1), 'w': round(max(xs) - min(xs), 1), 'h': round(max(ys) - min(ys), 1)})
            yield {**layer, '_placements': placements, '_ops': ops, '_times': visible_times}, boxes
        elif kind == 'composition':
            children = content.get('layers') or []
            if canvas:
                # Its own size, duration and camera, cropped to its canvas.
                inner_scene = {**scene, 'composition': ic, 'layers': children}
                yield from _sampled_layers(inner_scene, ops, all_sources, offset + float(layer.get('start') or 0) / rate,
                                           local_window, seen, inner_size, clipped=True, rate=rate, unmeasured=unmeasured)
            else:
                inner_scene = {**scene, 'composition': {'width': size[0], 'height': size[1]}, 'layers': children}
                yield from _sampled_layers(inner_scene, ops, all_sources, offset + float(layer.get('start') or 0) / rate,
                                           local_window, seen, size, rate=rate, unmeasured=unmeasured)
        elif kind == 'track':
            cursor = offset + float(layer.get('start') or 0) / rate
            clips = content.get('clips') or []
            unknown = unmeasured
            for child in clips:
                if not isinstance(child, dict):
                    continue
                inner_scene = {**scene, 'composition': {'width': size[0], 'height': size[1]},
                               'layers': [{**child, 'start': 0}]}
                yield from _sampled_layers(inner_scene, ops, all_sources, cursor, local_window, seen, size, rate=rate, unmeasured=unknown)
                unknown = unknown or child.get('duration') is None
                cursor += float(child.get('duration') or 0) / rate
        elif kind == 'scene_ref':
            inner = (content.get('asset') or assets.get(content.get('assetId')) or {}).get('scene')
            if isinstance(inner, dict) and id(inner) not in seen:
                speed = float(content.get('speed', 1))
                unknown = unmeasured
                if not math.isfinite(speed) or speed <= 0:
                    unknown, speed = True, 1
                child_rate = rate * speed
                trim = content.get('trim') or {}
                child_offset = offset + float(layer.get('start') or 0) / rate - float(trim.get('in') or 0) / child_rate
                if trim.get('out') is not None:
                    local_window = (local_window[0], min(local_window[1], child_offset + float(trim['out']) / child_rate))
                yield from _sampled_layers(inner, ops, all_sources, child_offset, local_window,
                                           seen | {id(inner)}, size=inner_size, clipped=True, rate=child_rate, unmeasured=unknown)


def check(scene: Dict[str, Any], destination: List[str], measured: Optional[Dict[str, Box]] = None) -> Dict[str, Any]:
    comp = scene.get('composition') or {}
    w, h = float(comp.get('width') or 1080), float(comp.get('height') or 1920)
    z = zone(destination)
    safe = safe_box(z, w, h)
    rails = rail_boxes(z, w, h)
    findings: List[Dict[str, Any]] = []
    unmeasured: List[str] = []
    measured = measured or {}
    for layer, estimates in _sampled_layers(scene):
        lid = layer.get('id', '')
        if layer.get('_unmeasured'):
            if lid not in measured:
                unmeasured.append(lid)
                continue
            # Its motion cannot be evaluated, but a measured box is still checked.
            boxes = [measured[lid]]
        elif not estimates:
            continue
        elif lid in measured:
            boxes = _measured_boxes(measured[lid], layer.get('_placements') or [], layer['_ops'], layer['_times'])
            if boxes is None:
                unmeasured.append(lid)
                boxes = [measured[lid]]
            # A snapshot stands in for the estimate unless these words' own placement moves.
            if layer['content']['kind'] == 'text' and any(b != estimates[0] for b in estimates):
                boxes += estimates
        elif layer['content']['kind'] == 'captions':
            unmeasured.append(lid)
            continue
        else:
            boxes = estimates
        worst: Optional[Tuple[float, Box, Dict[str, float]]] = None
        for b in boxes:
            over = {
                'top': safe['y'] - b['y'], 'bottom': b['y'] + b['h'] - (safe['y'] + safe['h']),
                'left': safe['x'] - b['x'], 'right': b['x'] + b['w'] - (safe['x'] + safe['w']),
            }
            over = {k: round(v, 1) for k, v in over.items() if v > 0.5}
            total = sum(over.values())
            if over and (worst is None or total > worst[0]):
                worst = (total, b, over)
        if worst:
            _, b, over = worst
            moves = []
            for side, px in over.items():
                moves.append(f"{'down' if side == 'top' else 'up' if side == 'bottom' else 'right' if side == 'left' else 'left'} {px:g} px")
            findings.append({
                'code': 'outside_safe_zone', 'layer': lid, 'box': b, 'over': over,
                'message': f'{lid} crosses the {", ".join(over)} of the safe zone',
                'fix': f'move it {" and ".join(moves)}, or shorten the line or make it smaller',
            })
            continue
        for b in boxes:
            hit = next((r for r in rails if _overlap(b, r)), None)
            if hit:
                into = round(b['x'] + b['w'] - hit['x'], 1)
                findings.append({
                    'code': 'under_rail', 'layer': lid, 'box': b, 'over': {'right': into},
                    'message': f"{lid} sits under the app's buttons on the right",
                    'fix': f'move it left {into:g} px, shorten the line, or move it above or below the buttons',
                })
                break
    # A layer nobody could place is not evidence that it fits.
    return {'ok': not findings and not unmeasured, 'profiles': z['ids'], 'safe': safe, 'rails': rails, 'findings': findings, 'unmeasured': unmeasured}


def _box(v: Any, where: str) -> Box:
    if not isinstance(v, dict) or not all(isinstance(v.get(k), (int, float)) and not isinstance(v.get(k), bool) for k in ('x', 'y', 'w', 'h')):
        raise InputError(f'{where} must be a box {{x, y, w, h}} in frame px')
    return {k: float(v[k]) for k in ('x', 'y', 'w', 'h')}


def run(data: Any) -> Dict[str, Any]:
    """The script's whole job: the checked input in, the line it prints out."""
    if not isinstance(data, dict):
        raise InputError('the input must be one JSON object')
    scene = data.get('scene')
    if isinstance(scene, dict) and 'scene' in scene and 'layers' not in scene:
        scene = scene['scene']
    if not isinstance(scene, dict) or not isinstance(scene.get('layers'), list):
        raise InputError('scene must be the scene document, with its layers')
    dest = data.get('destination', FALLBACK)
    dest = [dest] if isinstance(dest, str) else dest
    if not isinstance(dest, list) or not all(isinstance(d, str) for d in dest):
        raise InputError('destination must be a profile id or a list of them: ' + ', '.join(PROFILES))
    measured = data.get('measured') or {}
    if not isinstance(measured, dict):
        raise InputError('measured must be an object of boxes by layer id')
    return check(scene, [d.strip().lower() for d in dest], {k: _box(v, f'measured.{k}') for k, v in measured.items()})


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
    sys.stderr.write('safe_zone.py: ' + ' '.join(reason.split()) + '\n')
    return code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
