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
- `measured`, optional: a layer's box in frame px, by layer id, as `picsart_media_query_layout`
  measured it. A measured box replaces the estimate.

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
there; it is always centred vertically). Every keyframed position is checked, and the path
between two of them too, every 8 px along it and past either end where its curve overshoots. Words
inside a track's clips and inside a nested scene (`scene_ref`) are checked where the containing
layer puts them, the nested scene scaled by its `fit`. A scale is taken at its largest, past its
keyframes where its curve overshoots. A captions layer is placed by the renderer, so without a measured box it is listed
in `unmeasured`.

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
import sys
from typing import Any, Callable, Dict, FrozenSet, Iterator, List, Optional, Tuple

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
        if pa == pb or a.get('easing') == 'step':
            out.append(pb)
            continue
        lo, hi = _bezier_range(a.get('easing', 'linear'))
        dist = ((pb[0] - pa[0]) ** 2 + (pb[1] - pa[1]) ** 2) ** 0.5 * (hi - lo)
        n = max(1, int(dist // PATH_STEP) + 1)
        for i in range(n + 1):
            t = lo + (hi - lo) * i / n
            out.append([pa[0] + (pb[0] - pa[0]) * t, pa[1] + (pb[1] - pa[1]) * t])
        out.append(pb)
    return out


def _scale_reach(layer: Dict[str, Any]) -> Tuple[float, float]:
    """The largest scale a layer reaches on each axis: its keyframes, and past them where a curve overshoots."""
    keys = [k for k in ((layer.get('animations') or {}).get('scale') or {}).get('keyframes') or [] if isinstance(k, dict) and _vec(k.get('value'))]
    values = [_vec(k['value']) for k in keys] or _track(layer, 'scale') or [[1.0, 1.0]]
    for a, b in zip(keys, keys[1:]):
        if a.get('easing') == 'step':
            continue
        sa, sb = _vec(a['value']), _vec(b['value'])
        for t in _bezier_range(a.get('easing', 'linear')):
            values.append([sa[0] + (sb[0] - sa[0]) * t, sa[1] + (sb[1] - sa[1]) * t])
    return max(abs(v[0]) for v in values), max(abs(v[1]) for v in values)


def text_lines(content: Dict[str, Any]) -> List[str]:
    t = content.get('text')
    if isinstance(t, str):
        return t.split('\n')
    if isinstance(t, list):
        return [str(x) for x in t]
    return []


def text_boxes(layer: Dict[str, Any], comp: Tuple[float, float]) -> List[Box]:
    """The estimated box of a text layer at each position it takes or passes through, in frame px."""
    content = layer.get('content') or {}
    lines = text_lines(content)
    size = float(((content.get('font') or {}).get('size')) or 48)
    sx, sy = _scale_reach(layer)
    w = max((len(line) for line in lines), default=0) * size * CHAR_EM * sx
    h = max(1, len(lines)) * size * LINE_EM * sy
    align = content.get('alignment', 'center')
    out = []
    for p in _path(layer) or [[comp[0] / 2, comp[1] / 2]]:
        x = p[0] - w / 2 if align == 'center' else (p[0] if align == 'left' else p[0] - w)
        out.append({'x': round(x, 1), 'y': round(p[1] - h / 2, 1), 'w': round(w, 1), 'h': round(h, 1)})
    return out


def _overlap(a: Box, b: Box) -> bool:
    return a['x'] < b['x'] + b['w'] and b['x'] < a['x'] + a['w'] and a['y'] < b['y'] + b['h'] and b['y'] < a['y'] + a['h']


Place = Callable[[Box], List[Box]]


def _same(b: Box) -> List[Box]:
    return [b]


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


def _placed_by(ref: Dict[str, Any], inner: Tuple[float, float], host: Tuple[float, float], outer: Place) -> Place:
    """
    Where a box in a nested scene lands: the scene is scaled by its fit and its layer's scale, and
    centred on its layer's position.
    """
    positions = _path(ref) or [[host[0] / 2, host[1] / 2]]
    fx, fy = _fit_scale(ref.get('content') or {}, inner, host)
    rx, ry = _scale_reach(ref)
    sx, sy = fx * rx, fy * ry

    def place(b: Box) -> List[Box]:
        out = []
        for p in positions:
            moved = {'x': round(p[0] + (b['x'] - inner[0] / 2) * sx, 1), 'y': round(p[1] + (b['y'] - inner[1] / 2) * sy, 1),
                     'w': round(b['w'] * sx, 1), 'h': round(b['h'] * sy, 1)}
            out += outer(moved)
        return out
    return place


def _assets(scene: Dict[str, Any]) -> Dict[str, Any]:
    declared = scene.get('assets') or []
    if isinstance(declared, dict):
        return {k: a for k, a in declared.items() if isinstance(a, dict)}
    return {a.get('id'): a for a in declared if isinstance(a, dict)}


def words_layers(scene: Dict[str, Any], place: Place = _same, comp: Optional[Tuple[float, float]] = None, seen: FrozenSet[str] = frozenset()) -> Iterator[Tuple[Dict[str, Any], Place, Tuple[float, float]]]:
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
        content = layer.get('content') or {}
        kind = content.get('kind')
        if kind in ('text', 'captions'):
            yield layer, place, size
        elif kind == 'track':
            for clip in content.get('clips') or []:
                if isinstance(clip, dict) and (clip.get('content') or {}).get('kind') in ('text', 'captions'):
                    # A clip has no transform of its own: its layer's carries it.
                    yield {**layer, 'id': clip.get('id', layer.get('id', '')), 'content': clip['content']}, place, size
        elif kind == 'scene_ref':
            ref = content.get('assetId')
            inner = (assets.get(ref) or {}).get('scene')
            if isinstance(inner, dict) and ref not in seen:
                ic = inner.get('composition') or {}
                inner_size = (float(ic.get('width') or size[0]), float(ic.get('height') or size[1]))
                yield from words_layers(inner, _placed_by(layer, inner_size, size, place), inner_size, seen | {ref})


def check(scene: Dict[str, Any], destination: List[str], measured: Optional[Dict[str, Box]] = None) -> Dict[str, Any]:
    comp = scene.get('composition') or {}
    w, h = float(comp.get('width') or 1080), float(comp.get('height') or 1920)
    z = zone(destination)
    safe = safe_box(z, w, h)
    rails = rail_boxes(z, w, h)
    findings: List[Dict[str, Any]] = []
    unmeasured: List[str] = []
    measured = measured or {}
    for layer, place, size in words_layers(scene, comp=(w, h)):
        lid = layer.get('id', '')
        if lid in measured:
            boxes = [measured[lid]]
        elif layer['content']['kind'] == 'captions':
            unmeasured.append(lid)
            continue
        else:
            boxes = [p for b in text_boxes(layer, size) for p in place(b)]
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
    return {'ok': not findings, 'profiles': z['ids'], 'safe': safe, 'rails': rails, 'findings': findings, 'unmeasured': unmeasured}


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
