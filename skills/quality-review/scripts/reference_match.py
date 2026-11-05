#!/usr/bin/env python3
"""
Check a built scene against the reference's format (PI-11891): the layout, the caption position
and size, the hook's place, size and length, and the end card, read from the scene JSON alone.

    python3 scripts/reference_match.py scene.json edit-footage.json
    python3 scripts/reference_match.py scene.json format.json

The second file is the project record (its `format` is read) or the format itself, as the
reel-structure skill's `references/format.md` holds it. An approval in the record scoped
`format:<element>` lets that element differ.

The scene is read as the tools build it: picture tracks whose media clips carry `content.bounds`
[w, h] and a `transform.position` at the box's centre, and media layers placed on their own (a
stacked stretch above the reel's track); any two panels playing at once in part of the frame
are a split. A panel spans about the canvas's width and a quarter of its height or more: a corner
logo or another small overlay is ignored. A track with its own `duration` ends there. A `captions` layer's `style.offset` moves it from the frame's centre (or its
`style.position` names a place); a height answers to every name of its place (y 1440 of 1920 is
below the seam, the lower third and the bottom). A hook is the layers whose id names it (a
`color` box, a `text` layer); the end card is a media clip or layer of its asset, and the last
thing the reel shows. `assets` may be a list or a map by id.

It prints `{ok, findings, open, pairs}`. A finding is `{severity, check: "reference-match",
element, at, what, method, confidence, fix}`, the shape the QC inspector reports: a wrong layout
is critical, any other drift major. `open` lists what the scene cannot show. `pairs` lists each
reference still with its time, for the inspector to set beside the render's frame. Exits 0 when
nothing is found, 1 when something is, 2 on input it cannot read.

Python 3.9 or later, the standard library only, offline.
"""
from __future__ import annotations

import json
import sys
from typing import Any, Dict, List, Optional, Tuple

from timing import _assets, _clip_length

Json = Dict[str, Any]

TWO_TRACKS = ('split-v', 'stacked')
SIZE_DRIFT = 0.15  # a caption or hook size more than this far off the format's is drift
LENGTH_DRIFT = 0.5  # seconds a hook may run off the format's length
SEAM_BAND = 0.04  # share of the height around the seam that counts as on it
PANEL_WIDTH = 0.9  # a split panel spans about the canvas's width...
PANEL_HEIGHT = 0.25  # ...and at least this share of its height; anything smaller is an overlay


class InputError(ValueError):
    pass


def load(path: str) -> Any:
    try:
        with open(path, encoding='utf-8-sig') as f:
            return json.load(f)
    except (OSError, ValueError) as err:
        raise InputError(f'cannot read {path}: {err}')


def read_format(data: Any) -> Tuple[Json, List[str]]:
    """The format and the elements the user approved leaving."""
    if not isinstance(data, dict):
        raise InputError('the record or format must be a JSON object')
    fmt = data.get('format') if isinstance(data.get('format'), dict) else data
    approved = [str(a.get('scope'))[len('format:'):] for a in data.get('approvals') or []
                if isinstance(a, dict) and str(a.get('scope', '')).startswith('format:')]
    return fmt, approved


def read_scene(data: Any) -> Json:
    scene = data.get('scene', data) if isinstance(data, dict) else None
    if not isinstance(scene, dict) or not isinstance(scene.get('layers'), list):
        raise InputError('the scene must be a JSON object with layers')
    return scene


def num(v: Any) -> Optional[float]:
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def content(x: Json) -> Json:
    return x.get('content') if isinstance(x.get('content'), dict) else {}


def tracks(scene: Json) -> List[Json]:
    """The picture tracks: track layers with a media clip."""
    return [layer for layer in scene['layers'] if isinstance(layer, dict) and content(layer).get('kind') == 'track'
            and any(isinstance(c, dict) and content(c).get('kind') == 'media' for c in content(layer).get('clips') or [])]


def media_layers(scene: Json) -> List[Json]:
    """The picture layers placed straight on the scene, not in a track: a stacked stretch is often two."""
    return [layer for layer in scene['layers'] if isinstance(layer, dict) and content(layer).get('kind') == 'media']


def asset_ids(scene: Json, uri: str) -> set:
    """The ids of the scene's assets with this uri, whether `assets` is a list or a map by id."""
    raw = scene.get('assets')
    items = raw.items() if isinstance(raw, dict) else ((None, a) for a in raw or [])
    return {(a.get('id') or key) for key, a in items if isinstance(a, dict) and a.get('uri') == uri}


def scene_end(scene: Json, width: float, height: float) -> float:
    ends = [e for track in tracks(scene) for _, e, _ in pieces(track, width, height, _assets(scene))]
    ends += [(num(x.get('start')) or 0) + (num(x.get('duration')) or 0) for x in scene['layers']
             if isinstance(x, dict) and content(x).get('kind') != 'track']
    comp = num((scene.get('composition') or {}).get('duration'))
    return comp if comp else max(ends or [0.0])


def box(clip: Json, width: float, height: float) -> Tuple[float, float]:
    """A media clip's top and bottom on the frame: its bounds height around its centre."""
    b = content(clip).get('bounds')
    h = num(b[1]) if isinstance(b, list) and len(b) == 2 else None
    pos = (clip.get('transform') or {}).get('position') if isinstance(clip.get('transform'), dict) else None
    y = num(pos[1]) if isinstance(pos, list) and len(pos) == 2 else None
    h = height if h is None else h
    y = height / 2 if y is None else y
    return y - h / 2, y + h / 2


def panel(item: Json, width: float, height: float) -> Optional[Tuple[float, float]]:
    """A media clip or layer's box when it is a panel of the frame: about the canvas's width and at
    least a quarter of its height. A corner logo or another small overlay is no panel: None."""
    if content(item).get('kind') != 'media':
        return None
    b = content(item).get('bounds')
    w = num(b[0]) if isinstance(b, list) and len(b) == 2 else None
    top, bottom = box(item, width, height)
    if (w is not None and w < PANEL_WIDTH * width) or bottom - top < PANEL_HEIGHT * height:
        return None
    return top, bottom


def track_length(track: Json) -> Optional[float]:
    """A track's own `duration`, when it sets one: its clips play no further."""
    d = num(track.get('duration'))
    return d if d and d > 0 else None


def pieces(track: Json, width: float, height: float, assets: Json) -> List[Tuple[float, float, Optional[Tuple[float, float]]]]:
    """Each clip of a track as (start, end, box), box None for a clip that is no panel of the frame.
    A track with its own `duration` cuts its clips there."""
    out, t = [], num(track.get('start')) or 0.0
    length = track_length(track)
    stop = None if length is None else t + length
    for c in content(track).get('clips') or []:
        if not isinstance(c, dict):
            continue
        # a length that neither the clip, its trim nor its asset gives counts as zero, as it always has
        d = _clip_length(c, assets) or 0.0
        end = t + d if stop is None else min(t + d, stop)
        if end - t > 1e-9:
            out.append((t, end, panel(c, width, height)))
        t += d
    return out


def pictures(scene: Json, width: float, height: float) -> List[List[Tuple[float, float, Optional[Tuple[float, float]]]]]:
    """Every picture source as its pieces: each track, and each media layer placed on its own."""
    assets = _assets(scene)
    out = [pieces(t, width, height, assets) for t in tracks(scene)]
    for layer in media_layers(scene):
        start = num(layer.get('start')) or 0.0
        # like a track clip, a layer without its own duration plays its trim or its asset
        out.append([(start, start + (_clip_length(layer, assets) or 0.0), panel(layer, width, height))])
    return out


def split_pieces(scene: Json, width: float, height: float) -> List[Tuple[float, float, List[Tuple[float, float]]]]:
    """The stretches where two pictures playing at once each show a part of the frame: a split. Any
    two of them count, so a full-frame base track under the two halves does not hide it. The larger
    panel leaves the other at least a panel's height, so a 25/75 split still counts."""
    found = []
    sources = pictures(scene, width, height)
    for i, a in enumerate(sources):
        for b in sources[i + 1:]:
            for s0, e0, b0 in a:
                for s1, e1, b1 in b:
                    if (b0 and b1 and min(e0, e1) - max(s0, s1) > 1e-6
                            and max(b0[1] - b0[0], b1[1] - b1[0]) <= (1 - PANEL_HEIGHT) * height + 1e-6):
                        found.append((max(s0, s1), min(e0, e1), [b0, b1]))
    return sorted(found)


ALIASES = {'center': 'centre', 'middle': 'centre', 'lower-third': 'lower third', 'lower_third': 'lower third',
           'lowerthird': 'lower third', 'above seam': 'above-seam', 'below seam': 'below-seam'}


def name_of(place: Any) -> Optional[str]:
    """A place's one spelling: `center` is `centre`, `lower-third` is `lower third`."""
    if not isinstance(place, str):
        return None
    named = place.strip().lower()
    return ALIASES.get(named, named)


def places_of(y: float, height: float, seam: Optional[float]) -> List[str]:
    """Every name a height on the frame answers to, the most specific first: y 1440 of 1920 is
    below the seam, in the lower third and at the bottom all at once."""
    band = SEAM_BAND * height
    out = []
    if seam is not None:
        if abs(y - seam) <= band:
            out.append('seam')
        elif y < seam:
            out.append('above-seam')
        else:
            out.append('below-seam')
    if y < height / 3:
        out.append('top')
    elif y > 2 * height / 3:
        out += ['lower third', 'bottom']
    else:
        out.append('centre')
    return out


def place_of(y: float, height: float, seam: Optional[float]) -> str:
    return places_of(y, height, seam)[0]


def caption_places(layer: Json, height: float, seam: Optional[float]) -> Optional[List[str]]:
    style = content(layer).get('style') if isinstance(content(layer).get('style'), dict) else {}
    if isinstance(style.get('position'), str):
        return [name_of(style['position'])]
    off = style.get('offset')
    if isinstance(off, list) and len(off) == 2 and num(off[1]) is not None:
        return places_of(height / 2 + num(off[1]), height, seam)
    pos = (layer.get('transform') or {}).get('position') if isinstance(layer.get('transform'), dict) else None
    if isinstance(pos, list) and len(pos) == 2 and num(pos[1]) is not None:
        return places_of(num(pos[1]), height, seam)
    return None


def caption_place(layer: Json, height: float, seam: Optional[float]) -> Optional[str]:
    got = caption_places(layer, height, seam)
    return got[0] if got else None


def font_size(layer: Json) -> Optional[float]:
    c = content(layer)
    style = c.get('style') if isinstance(c.get('style'), dict) else c
    font = style.get('font') if isinstance(style.get('font'), dict) else {}
    return num(font.get('size')) or num(style.get('size')) or num(style.get('fontSize'))


def check(scene: Json, fmt: Json, approved: List[str]) -> Json:
    comp = scene.get('composition') or {}
    width, height = float(comp.get('width') or 1080), float(comp.get('height') or 1920)
    fps = float(comp.get('fps') or fmt.get('fps') or 30)
    layout = fmt.get('layout') if isinstance(fmt.get('layout'), dict) else {}
    seam = num(layout.get('seam'))
    findings: List[Json] = []
    opened: List[Json] = []

    def find(severity: str, element: str, what: str, fix: str, at: Any = None) -> None:
        findings.append({'severity': severity, 'check': 'reference-match', 'element': element,
                         'at': at if at is not None else 0, 'what': what, 'method': 'read from the scene JSON',
                         'confidence': 'high', 'fix': fix})

    mode = layout.get('mode')
    split = split_pieces(scene, width, height)
    assets = _assets(scene)
    if mode and 'layout' not in approved:
        n = len(pictures(scene, width, height))
        if mode in TWO_TRACKS and not split:
            find('critical', 'layout', f'the format is {mode}, the scene never splits the frame ({n} picture track(s) or layer(s))',
                 f'build it {mode}: two tracks in lockstep, as the footage-reframing skill says')
        elif mode in ('single', 'full') and split:
            find('critical', 'layout', f'the format is {mode}, the scene splits the frame', 'one picture track')
        if mode in TWO_TRACKS and split and seam is not None:
            off = [(s, e) for s, e, boxes in split if min(abs(bx[1] - seam) for bx in boxes) > SEAM_BAND * height / 2]
            if off:
                find('major', 'layout', f'{len(off)} split piece(s) do not meet at the seam, y {seam:g}',
                     f'size the halves to meet at y {seam:g}', [off[0][0], off[0][1]])

    captions = fmt.get('captions') if isinstance(fmt.get('captions'), dict) else {}
    want = name_of(captions.get('position'))
    caption_layers = [x for x in scene['layers'] if isinstance(x, dict) and content(x).get('kind') == 'captions'
                      and 'hook' not in str(x.get('id', '')).lower()]
    if 'captions' not in approved:
        if captions and not caption_layers:
            find('major', 'captions', 'the format has captions, the scene has none',
                 'add the captions as the format sets them, as the spoken-captions skill says')
        for layer in caption_layers if want else []:
            got = caption_places(layer, height, seam)
            if got is None:
                opened.append({'check': 'reference-match', 'why': f'{layer.get("id")}: the scene sets no caption position'})
            elif want not in got:
                find('major', 'captions', f'{layer.get("id")} sits {got[0]}, the format puts captions {want}',
                     f'move the captions {want}; a face under them is fixed in the layout, never by moving them',
                     num(layer.get('start')) or 0)
        style = captions.get('style') if isinstance(captions.get('style'), dict) else {}
        target = num(style.get('size'))
        for layer in caption_layers if target else []:
            size = font_size(layer)
            if size is not None and abs(size - target) > SIZE_DRIFT * target:
                find('major', 'captions', f'{layer.get("id")} is {size:g} px, the format {target:g}',
                     f'set the caption size to {target:g}')

    hook = fmt.get('hook') if isinstance(fmt.get('hook'), dict) else {}
    if hook and 'hook' not in approved:
        parts = [x for x in scene['layers'] if isinstance(x, dict) and 'hook' in str(x.get('id', '')).lower()]
        if not parts:
            find('major', 'hook', 'the format has a hook card, the scene has none', 'add the hook as the format sets it')
        else:
            length = num(hook.get('length'))
            dur = max(num(x.get('duration')) or 0 for x in parts)
            if length is not None and dur and abs(dur - length) > LENGTH_DRIFT:
                find('major', 'hook', f'the hook holds {dur:g} s, the format {length:g} s', f'hold it {length:g} s')
            pos = next(((x.get('transform') or {}).get('position') for x in parts
                        if isinstance(x.get('transform'), dict)), None)
            if hook.get('position') and isinstance(pos, list) and len(pos) == 2 and num(pos[1]) is not None:
                got = places_of(num(pos[1]), height, seam)
                if name_of(hook['position']) not in got:
                    find('major', 'hook', f'the hook sits {got[0]}, the format {hook["position"]}', f'place it {hook["position"]}')
            hstyle = hook.get('style') if isinstance(hook.get('style'), dict) else {}
            target = num(hstyle.get('size'))
            size = next((font_size(x) for x in parts if content(x).get('kind') in ('text', 'captions')), None)
            if target and size is not None and abs(size - target) > SIZE_DRIFT * target:
                find('major', 'hook', f'the hook is {size:g} px, the format {target:g}', f'set it to {target:g}')

    end = fmt.get('endCard') if isinstance(fmt.get('endCard'), dict) else {}
    if end.get('asset') and 'endCard' not in approved:
        ids = asset_ids(scene, end['asset'])
        # each place the end card plays: (start, length)
        held = [(num(x.get('start')) or 0.0, num(x.get('duration'))) for x in scene['layers']
                if isinstance(x, dict) and content(x).get('assetId') in ids]
        for layer in tracks(scene):
            t, length = num(layer.get('start')) or 0.0, track_length(layer)
            stop = None if length is None else t + length
            for c in content(layer).get('clips') or []:
                if not isinstance(c, dict):
                    continue
                d = _clip_length(c, assets) or 0.0
                if content(c).get('assetId') in ids and (stop is None or t < stop):
                    held.append((t, d if stop is None else min(d, stop - t)))
                t += d
        comp_end = num(comp.get('duration'))
        if comp_end:
            # the reel stops at the composition's end: a card plays no further, and one that starts after it never shows
            held = [(s, length if length is None else min(length, comp_end - s)) for s, length in held if s < comp_end - 1e-9]
        target = num(end.get('duration'))
        if not held:
            find('major', 'endCard', "the channel's end card is not in the scene", 'end on the end card asset, as given')
        else:
            # the closing use of the asset: one used earlier in the reel is not the end card
            start, length = max(held, key=lambda h: h[0] + (h[1] or 0))
            if target is not None and length is not None and abs(length - target) > 1 / fps + 1e-6:
                find('major', 'endCard', f'the end card holds {length:g} s, the format {target:g} s',
                     'hold it its own length, snapped to the frame grid')
            stop = scene_end(scene, width, height)
            if length is not None and start + length < stop - 1 / fps - 1e-6:
                find('major', 'endCard', f'the end card ends at {start + length:g} s, the scene runs to {stop:g} s',
                     'make the end card the last thing the reel shows', start)

    pairs = [{'element': e.get('element'), 'still': e.get('still'), 't': e.get('t')}
             for e in fmt.get('evidence') or [] if isinstance(e, dict) and e.get('still')]
    return {'ok': not findings, 'findings': findings, 'open': opened, 'pairs': pairs}


def main(argv: List[str]) -> int:
    if len(argv) != 2:
        sys.stderr.write('usage: reference_match.py <scene.json> <record or format.json>\n')
        return 2
    try:
        fmt, approved = read_format(load(argv[1]))
        out = check(read_scene(load(argv[0])), fmt, approved)
    except InputError as err:
        sys.stderr.write(f'reference_match.py: {err}\n')
        return 2
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return 0 if out['ok'] else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
