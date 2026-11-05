"""
The split layout for reel_cut.py (PI-11892): two people stacked, one above the seam and one below,
each a fixed crop of the source chosen by the shot type on screen, with full-frame emphasis
pieces on the lines the locked map names. reel_cut.py calls it when its input has a `layout`
whose mode is `split-v` or `stacked`; it is not run on its own.

The input adds, beside `sources` and `clips`:

    "layout": {"mode": "split-v", "seam": 960},
    "shots": {"ep": [[2916, 2917.688, "host"], [2917.688, 3054.921, "two"]]},
    "crops": {"annie": [110, 90, 500, 444], "cameron": [590, 0, 500, 444],
              "preston": [110, 40, 540, 480], "inset": [796, 84, 382, 338],
              "annie_full": [170, 0, 405, 720], "cameron_full": [640, 0, 405, 720]},
    "halves": {"two": ["annie", "cameron"], "host": ["preston", "inset"]},
    "full": {"annie": "annie_full", "cameron": "cameron_full"},
    "emphasis": [{"source": "ep", "in": 2936.3, "out": 2939.1, "who": "cameron", "from": "map"}],
    "speakers": {"ep": [[2930.0, 2940.0, "cameron"]]}

- `shots`: per source, its shots in its own seconds with their type (picsart_media_segment_shots,
  each type named by eye from one still). Every clip second needs a shot.
- `crops`: `[x, y, w, h]` in source pixels, each checked with reframe_fix.py check-crops first.
- `halves`: per shot type, the crops above and below the seam.
- `full`: per person, their full-frame crop.
- `emphasis`: full-frame pieces. `who` and `from` (`map` or `transcript`) are required: who
  speaks comes from the locked map or the transcript, never from the reframe. With `speakers`,
  an emphasis whose `who` is not the one speaking over most of it is refused.

Each clip is cut into pieces at every shot edge and emphasis edge inside it; a piece takes the
layout at its middle. Two tracks are built in lockstep, the same durations piece for piece: `top`
carries the sound (its half, or the full frame), `bottom` is muted, and under a full-frame piece
it plays a black colour clip. `transform.position` is each box's centre.
"""
from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Tuple

Json = Dict[str, Any]
SPLITS = ('split-v', 'stacked')
BLACK = '#000000'


def build(data: Json, sources: Dict[str, Json], clips: List[Tuple[Json, Json]], width: float, height: float,
          number: Callable[..., float], error: Callable[[str], Exception]) -> Tuple[List[Json], List[Json], List[str]]:
    """The two tracks' clips, bottom and top, and the source ids used."""
    layout = data['layout']
    seam = number(layout.get('seam', height / 2), 'layout seam')
    if not 0 < seam < height:
        raise error(f'layout seam must be inside the frame, between 0 and {height:g}')
    crops = read_crops(data.get('crops'), number, error)
    halves = data.get('halves')
    if not isinstance(halves, dict) or not halves:
        raise error('a split needs "halves": per shot type, the crops above and below the seam')
    for kind, pair in halves.items():
        if not (isinstance(pair, list) and len(pair) == 2 and all(p in crops for p in pair)):
            raise error(f'halves "{kind}" must name two crops from "crops", the top one first')
    full = data.get('full') or {}
    if not isinstance(full, dict) or any(v not in crops for v in full.values()):
        raise error('full maps a person to the name of their full-frame crop in "crops"')
    shots = read_shots(data.get('shots'), sources, number, error)
    speakers = read_shots(data.get('speakers') or {}, sources, number, error, 'speakers')
    emphasis = read_emphasis(data.get('emphasis') or [], sources, full, speakers, number, error)

    top: List[Json] = []
    bottom: List[Json] = []
    used: List[str] = []
    for i, (source, clip) in enumerate(clips):
        sid = source['id']
        if source['type'] != 'video':
            raise error(f'clips[{i}]: a split cuts video, and "{sid}" is a photo')
        sw, sh = source['size']

        def crop(name: str) -> List[float]:
            # Only the crops this source plays are checked against it: two cameras of different
            # sizes each keep crops the other could not hold.
            x, y, w, h = crops[name]
            if x < 0 or y < 0 or x + w > sw + 0.5 or y + h > sh + 0.5:
                raise error(f'crops "{name}" runs outside source "{sid}" ({sw:g}x{sh:g})')
            return crops[name]
        a, b = clip['in'], clip['out']
        edges = {a, b}
        edges |= {x for s, e, _ in shots.get(sid, []) for x in (s, e) if a < x < b}
        edges |= {x for em in emphasis if em['source'] == sid for x in (em['in'], em['out']) if a < x < b}
        cuts = sorted(edges)
        for s, e in zip(cuts, cuts[1:]):
            if e - s < 1e-3:
                continue
            mid = (s + e) / 2
            d = round(e - s, 3)
            em = next((x for x in emphasis if x['source'] == sid and x['in'] <= mid < x['out']), None)
            if em is not None:
                top.append(piece(sid, s, e, crop(full[em['who']]), (width, height), height / 2, False, width))
                bottom.append({'duration': d, 'content': {'kind': 'color', 'color': BLACK}})
                continue
            kind = next((k for s0, e0, k in shots.get(sid, []) if s0 <= mid < e0), None)
            if kind is None:
                raise error(f'clips[{i}]: no shot of "{sid}" covers {mid:.2f}s; give its shots')
            if kind not in halves:
                raise error(f'clips[{i}]: the shot type "{kind}" at {mid:.2f}s has no halves')
            up, down = halves[kind]
            top.append(piece(sid, s, e, crop(up), (width, seam), seam / 2, False, width))
            bottom.append(piece(sid, s, e, crop(down), (width, height - seam), seam + (height - seam) / 2, True, width))
        if sid not in used:
            used.append(sid)
    return bottom, top, used


def piece(sid: str, s: float, e: float, crop: List[float], bounds: Tuple[float, float], y: float, muted: bool,
          width: float) -> Json:
    return {'duration': round(e - s, 3),
            'content': {'kind': 'media', 'assetId': sid, 'trim': {'in': round(s, 3), 'out': round(e, 3)},
                        'crop': list(crop), 'fit': 'cover', 'bounds': [bounds[0], bounds[1]], 'muted': muted},
            'transform': {'position': [width / 2, y]}}


def read_crops(raw: Any, number: Callable[..., float], error: Callable[[str], Exception]) -> Dict[str, List[float]]:
    if not isinstance(raw, dict) or not raw:
        raise error('a split needs "crops": named [x, y, w, h] boxes in source pixels')
    out = {}
    for name, box in raw.items():
        if not (isinstance(box, list) and len(box) == 4):
            raise error(f'crops "{name}" must be [x, y, w, h]')
        x, y, w, h = (number(v, f'crops "{name}"', positive=False) for v in box)
        if w <= 0 or h <= 0:
            raise error(f'crops "{name}" needs a width and a height')
        out[name] = [x, y, w, h]
    return out


def read_shots(raw: Any, sources: Dict[str, Json], number: Callable[..., float], error: Callable[[str], Exception],
               what: str = 'shots') -> Dict[str, List[Tuple[float, float, str]]]:
    if not isinstance(raw, dict):
        raise error(f'{what} maps a source id to its [start, end, name] list')
    out = {}
    for sid, rows in raw.items():
        if sid not in sources:
            raise error(f'{what} names source "{sid}", which is not in sources')
        if not isinstance(rows, list):
            raise error(f'{what} "{sid}" must be a list of [start, end, name]')
        found = []
        for k, row in enumerate(rows):
            if not (isinstance(row, list) and len(row) >= 3 and isinstance(row[2], str)):
                raise error(f'{what} "{sid}"[{k}] must be [start, end, name]')
            s, e = number(row[0], f'{what} "{sid}"[{k}] start', positive=False), number(row[1], f'{what} "{sid}"[{k}] end')
            if e <= s:
                raise error(f'{what} "{sid}"[{k}] ends before it starts')
            found.append((s, e, row[2]))
        out[sid] = sorted(found)
    return out


def speaker_at(rows: List[Tuple[float, float, str]], a: float, b: float) -> Optional[str]:
    """Who speaks over most of [a, b]."""
    talk: Dict[str, float] = {}
    for s, e, who in rows:
        over = min(b, e) - max(a, s)
        if over > 0:
            talk[who] = talk.get(who, 0.0) + over
    return max(talk, key=talk.get) if talk else None


def read_emphasis(raw: Any, sources: Dict[str, Json], full: Dict[str, str], speakers: Dict[str, List[Tuple[float, float, str]]],
                  number: Callable[..., float], error: Callable[[str], Exception]) -> List[Json]:
    if not isinstance(raw, list):
        raise error('emphasis must be a list')
    only = next(iter(sources)) if len(sources) == 1 else None
    out = []
    for k, em in enumerate(raw):
        if not isinstance(em, dict):
            raise error(f'emphasis[{k}] must be an object')
        sid = em.get('source', only)
        if sid not in sources:
            raise error(f'emphasis[{k}] needs the source it is in')
        a, b = number(em.get('in'), f'emphasis[{k}] in', positive=False), number(em.get('out'), f'emphasis[{k}] out')
        if b <= a:
            raise error(f'emphasis[{k}] ends before it starts')
        who = em.get('who')
        if who not in full:
            raise error(f'emphasis[{k}] needs "who", a person with a full-frame crop in "full"')
        if em.get('from') not in ('map', 'transcript'):
            raise error(f'emphasis[{k}] needs "from": "map" or "transcript"; who speaks never comes from the reframe')
        if sid in speakers:
            said = speaker_at(speakers[sid], a, b)
            if said is not None and said != who:
                raise error(f'emphasis[{k}] shows {who}, but {said} speaks over most of {a:g}-{b:g}s')
        out.append({'source': sid, 'in': a, 'out': b, 'who': who})
    return out
