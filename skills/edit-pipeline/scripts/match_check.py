"""A plan's pace against the reference's, and a scene's colours against the brand's palette.

Both are numbers a draft can drift from without anyone saying so: a cut that holds each shot 2.2 s
when the reference holds 3.6 s, or a caption in a colour the brand guide keeps off text.
record.py lock-check runs the pace check; `record.py palette-check <record> <scene>` the palette;
`record.py length-check <record> <scene>` the reel's end against the recipe's length.
"""
from __future__ import annotations

import math
import re

# a plan within this share of the reference's cuts per 10 s keeps its pace
DENSITY_TOLERANCE = 0.25
HEX = re.compile(r'^#([0-9a-fA-F]{6})([0-9a-fA-F]{2})?$')
COLOUR_KEYS = ('color', 'colour', 'background', 'fill', 'stroke')
TEXT_KINDS = ('captions', 'text')
NEUTRALS = ('#000000', '#FFFFFF')
# the reel may run this far past the recipe's length (a seam's rounding), and its last clip hold
# this much longer than the recipe's last beat
END_TOLERANCE = 0.5
TAIL_LIMIT = 1.5
# A reel this much shorter than its length (a share of it, at least END_TOLERANCE) is short.
SHORT_SHARE = 0.1
FRAME = 1 / 30
PICTURE_KINDS = ('media', 'composition', 'image', 'video')


def holds(plan: dict) -> list[tuple[int, float]]:
    """(row, seconds) for every planned shot that says where it sits in the cut."""
    out = []
    for i, r in enumerate(plan.get('rows') or plan.get('clips') or []):
        if not isinstance(r, dict):
            continue
        for a, b in (('sceneStart', 'sceneEnd'), ('start', 'end'), ('in', 'out')):
            if isinstance(r.get(a), (int, float)) and isinstance(r.get(b), (int, float)):
                out.append((i, float(r[b]) - float(r[a])))
                break
        else:
            if isinstance(r.get('duration'), (int, float)):
                out.append((i, float(r['duration'])))
    return out


def pace_check(cut_pace: dict, plan: dict, approvals: list | None = None) -> dict:
    """Every shot at or above minHold fails the plan when it is not. The cuts per 10 s far from
    cutPace's density are reported `open`, never failed: cutPace is also the job's default when no
    reference was read, and a standing note ("keep shots longer") is the user's say on the pace
    without being a `format:pace` approval. The open line is said to the user before the build."""
    problems: list[dict] = []
    opened: list[str] = []
    timed = holds(plan)
    rows = [r for r in plan.get('rows') or plan.get('clips') or [] if isinstance(r, dict)]
    if not timed:
        return {'problems': [], 'open': ['pace: no row says its sceneStart and sceneEnd'] if rows else []}
    min_hold = cut_pace.get('minHold')
    if isinstance(min_hold, (int, float)):
        for i, d in timed:
            if d < min_hold - 1e-6:
                problems.append({'element': 'pace', 'row': i, 'problem': 'hold under minHold',
                                 'hold': round(d, 2), 'minHold': min_hold})
    density = cut_pace.get('density')
    approved = {a.get('scope') for a in approvals or [] if isinstance(a, dict)}
    span = sum(d for _, d in timed)
    if isinstance(density, (int, float)) and density > 0 and span > 0 and 'format:pace' not in approved:
        planned = 10 * max(len(timed) - 1, 0) / span
        if abs(planned - density) > DENSITY_TOLERANCE * density:
            opened.append(f'pace: {planned:.2f} cuts per 10 s against cutPace {density} '
                          f'(average hold {span / len(timed):.2f} s); say it, or keep the pace')
    rhythm = rhythm_check(cut_pace.get('rhythm'), plan, approved)
    problems += rhythm['problems']
    opened += rhythm['open']
    return {'problems': problems, 'open': opened}


# A shot this short or under is fast; more of them in a row than maxFastRun reads as "eventy".
FAST_HOLD, MAX_FAST_RUN = 1.2, 3


def voiced(row: dict) -> bool:
    """Whether a voice runs under the shot: a row says `voice: false` when its phrase names a silent beat."""
    return row['voice'] if isinstance(row.get('voice'), bool) else bool(row.get('phrase'))


def rhythm_check(rhythm, plan: dict, approved: set | None = None) -> dict:
    """The cut's shape, beyond its average: the median hold, runs of fast shots, one long hold in
    each section, and a breath with no voice between sections. A finding is `open`, said to the user
    before the build, unless `register` quotes the brief's own style words ("cinematic, atmospheric"):
    then the brief asked for this shape, and a plan that breaks it fails. A shape the user chose
    instead (an approval scoped `format:rhythm`) passes."""
    if not isinstance(rhythm, dict) or 'format:rhythm' in (approved or set()):
        return {'problems': [], 'open': []}
    rows = plan.get('rows') or plan.get('clips') or []
    timed = holds(plan)
    if not timed:
        return {'problems': [], 'open': []}  # pace_check already says the rows carry no times
    found: list[dict] = []
    floor = rhythm.get('medianHold')
    if isinstance(floor, (int, float)):
        ds = sorted(d for _, d in timed)
        mid = ds[len(ds) // 2] if len(ds) % 2 else (ds[len(ds) // 2 - 1] + ds[len(ds) // 2]) / 2
        if mid < floor - 1e-6:
            found.append({'problem': 'median hold under the rhythm', 'median': round(mid, 2), 'medianHold': floor})
    fast = rhythm.get('fastHold', FAST_HOLD)
    most = rhythm.get('maxFastRun', MAX_FAST_RUN)
    run: list[int] = []
    for i, d in timed + [(-1, float('inf'))]:
        if d < fast - 1e-6:
            run.append(i)
            continue
        if len(run) > most:
            found.append({'problem': 'a run of fast shots', 'rows': [run[0], run[-1]], 'shots': len(run), 'fastHold': fast})
        run = []
    sections: dict = {}
    for i, d in timed:
        name = rows[i].get('section') if i < len(rows) else None
        if name:
            sections.setdefault(name, []).append((i, d))
    hold = rhythm.get('holdPerSection')
    opened: list[str] = []
    if (isinstance(hold, (int, float)) or rhythm.get('breaths')) and not sections:
        opened.append('rhythm: no row names its `section`, so its holds and breaths are unchecked')
    if isinstance(hold, (int, float)):
        for name, shots in sections.items():
            if max(d for _, d in shots) < hold - 1e-6:
                found.append({'problem': 'no long hold in the section', 'section': name, 'holdPerSection': hold})
    if rhythm.get('breaths') and sections:
        order = [rows[i].get('section') for i, _ in timed]
        for k in range(1, len(order)):
            if order[k] and order[k - 1] and order[k] != order[k - 1]:
                a, b = rows[timed[k - 1][0]], rows[timed[k][0]]
                if voiced(a) and voiced(b):
                    found.append({'problem': 'no breath between sections', 'sections': [order[k - 1], order[k]],
                                  'row': timed[k][0]})
    for f in found:
        f['element'] = 'rhythm'
    if rhythm.get('register'):
        return {'problems': found, 'open': opened}
    return {'problems': [], 'open': opened + [f"rhythm: {f['problem']} ({', '.join(f'{k} {v}' for k, v in f.items() if k not in ('problem', 'element'))}); say it, or keep the shape" for f in found]}


def palette(record: dict) -> list[dict]:
    """The brand's colours: `brand.palette` from the brand guide, else the own-brand format's."""
    brand = record.get('brand') if isinstance(record.get('brand'), dict) else {}
    entries = []
    for c in brand.get('palette') or []:
        if isinstance(c, dict) and HEX.match(str(c.get('hex', ''))):
            entries.append({'name': c.get('name'), 'hex': c['hex'][:7].upper(), 'text': c.get('text')})
    if not entries:
        fmt = record.get('format') if isinstance(record.get('format'), dict) else {}
        for c in (fmt.get('brand') or {}).get('colors') or []:
            if HEX.match(str(c)):
                entries.append({'name': None, 'hex': str(c)[:7].upper(), 'text': None})
    return entries


def colours(node, path: str = '', text: bool = False, translucent: bool = False,
            colour_value: bool = False, assets=None, seen=()):
    """(path, hex, translucent, on text) for colours drawn by the scene."""
    if isinstance(node, str):
        m = HEX.fullmatch(node) if colour_value else None
        if m:
            yield path, '#' + m.group(1).upper(), translucent or (m.group(2) is not None and m.group(2).upper() != 'FF'), text
    elif isinstance(node, dict):
        if id(node) in seen:
            return
        seen = seen + (id(node),)
        kind = (node.get('content') or {}).get('kind') if isinstance(node.get('content'), dict) else node.get('kind')
        text = text or kind in TEXT_KINDS
        opacity = node.get('opacity')
        transform = node.get('transform')
        if isinstance(transform, dict) and isinstance(transform.get('opacity'), (int, float)):
            translucent = translucent or transform['opacity'] < 1
        if isinstance(opacity, (int, float)):
            translucent = translucent or opacity < 1
        if node.get('place') == 'behind':
            text = False
        local_assets = node.get('assets', assets)
        if isinstance(local_assets, list):
            local_assets = {a.get('id'): a for a in local_assets if isinstance(a, dict)}
        if not isinstance(local_assets, dict):
            local_assets = {}
        if node.get('kind') == 'scene_ref':
            content = node
            asset = content.get('asset') or local_assets.get(content.get('assetId')) or {}
            inner = asset.get('scene') if isinstance(asset, dict) else None
            if isinstance(inner, dict):
                yield from colours(inner, f'{path}.scene' if path else 'scene', False, translucent, assets=None, seen=seen)
        for k, v in node.items():
            if k in ('mask', 'assets') or (kind == 'scene_ref' and k == 'asset'):
                continue
            p = f'{path}.{k}' if path else k
            # Keep the established paths for root layers.
            if not path and k == 'layers':
                p = ''
            child_text = False if k in ('effects', 'contentEffects') else text
            is_colour = k in COLOUR_KEYS or (colour_value and k in ('keyframes', 'value'))
            yield from colours(v, p, child_text, translucent, is_colour, local_assets, seen)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from colours(v, f'{path}[{i}]', text, translucent, colour_value, assets, seen)


def palette_check(record: dict, scene: dict) -> dict:
    """Every colour the scene sets is one of the brand's, and text only in a colour the guide allows
    on text. Away from text, pure black and white (a fade through black, a scrim) and any colour
    with transparency pass, unless the record's `brand.neutrals` is false: the guide forbids them."""
    entries = palette(record)
    if not entries:
        return {'ok': True, 'problems': [], 'open': ['palette: the record holds no brand.palette']}
    by_hex = {e['hex']: e for e in entries}
    brand = record.get('brand') if isinstance(record.get('brand'), dict) else {}
    neutrals_ok = brand.get('neutrals') is not False
    problems = []
    for path, hexcode, see_through, on_text in colours(scene):
        e = by_hex.get(hexcode)
        if e is None and neutrals_ok and not on_text and (hexcode in NEUTRALS or see_through):
            continue
        if e is None:
            problems.append({'path': path, 'colour': hexcode, 'problem': 'not in the brand palette'})
        elif on_text and e.get('text') is False:
            problems.append({'path': path, 'colour': hexcode, 'name': e.get('name'),
                             'problem': 'the brand guide keeps this colour off text'})
    return {'ok': not problems, 'problems': problems, 'open': []}


def asset_table(scene: dict) -> dict:
    """The scene's assets by id, from a list or a map."""
    assets = scene.get('assets') or []
    if isinstance(assets, dict):
        return {str(k): v for k, v in assets.items() if isinstance(v, dict)}
    return {str(a.get('id')): a for a in assets if isinstance(a, dict)} if isinstance(assets, list) else {}


def _num(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _asset(content: dict, assets: dict, scenes: dict | None = None) -> dict:
    inline = content.get('asset')
    if isinstance(inline, dict):
        return inline
    if content.get('sceneRef') is not None:
        inner = (scenes or {}).get(str(content['sceneRef']))
        return {'scene': inner} if isinstance(inner, dict) else {}
    return assets.get(str(content.get('assetId'))) or {}


def _speed(content: dict, item: dict) -> float:
    speed = content.get('speed', item.get('speed', 1))
    return float(speed) if _num(speed) and speed > 0 else 1.0


def scene_length(scene: dict, depth: int = 0, scenes: dict | None = None) -> float | None:
    """How long a scene (or a composition's content) plays: its composition's duration, else where
    its last layer ends."""
    composition = scene.get('composition') if isinstance(scene.get('composition'), dict) else {}
    if _num(composition.get('duration')) and composition['duration'] > 0:
        return float(composition['duration'])
    if _num(scene.get('duration')) and scene['duration'] > 0:
        return float(scene['duration'])
    assets = asset_table(scene)
    scenes = {**(scenes or {}), **(scene.get('scenes') or {})}
    ends = []
    for layer in scene.get('layers') or []:
        if not isinstance(layer, dict):
            continue
        length = own_length(layer, assets, depth + 1, scenes)
        start = layer.get('start', 0)
        if length is not None:
            ends.append((float(start) if _num(start) else 0.0) + length)
    return max(ends) if ends else None


def own_length(item: dict, assets: dict, depth: int = 0, scenes: dict | None = None) -> float | None:
    """How long a layer or a track clip plays, before what holds it cuts it: its `duration`; else
    its trim over its speed; else its asset's length (inline or by id) past the trim's in, over the
    speed; a track, its clips added up; a composition, its own length or its layers'; a scene_ref,
    its scene's, trimmed and at its speed."""
    if depth > 32:
        return None
    if _num(item.get('duration')):
        return float(item['duration'])
    content = item.get('content') if isinstance(item.get('content'), dict) else {}
    kind = content.get('kind')
    if kind == 'track':
        lengths = [own_length(c, assets, depth + 1, scenes) for c in content.get('clips') or [] if isinstance(c, dict)]
        return sum(x for x in lengths if x) or None
    if kind == 'composition':
        return scene_length({**content, 'assets': content.get('assets') or assets}, depth + 1, scenes)
    speed = _speed(content, item)
    trim = content.get('trim') if isinstance(content.get('trim'), dict) else {}
    t_in = float(trim['in']) if _num(trim.get('in')) else 0.0
    record = _asset(content, assets, scenes)
    source_length = (scene_length(record['scene'], depth + 1, scenes)
                     if kind == 'scene_ref' and isinstance(record.get('scene'), dict)
                     else float(record['duration']) if _num(record.get('duration')) else None)
    if source_length is not None:
        t_in = min(max(0.0, t_in), source_length)
    end = (float(trim['out']) if _num(trim.get('out')) else
           t_in + float(trim['duration']) if _num(trim.get('duration')) else source_length)
    if end is None:
        return None
    if source_length is not None:
        end = min(end, source_length)
    return max(0.0, end - t_in) / speed



def slots(scene: dict) -> list[tuple[str, float, float]]:
    """(id, start, end) in reel seconds for every picture slot: media, a track's clips and the
    pictures inside a composition or a scene_ref, at any depth. A composition with no picture
    inside is a slot itself. Each is cut to the time its parent layer, and the reel, show it."""
    out: list[tuple[str, float, float]] = []

    def place(name: str, at: float, length: float | None, window: tuple[float, float]) -> None:
        if length is None:
            return
        start, end = max(at, window[0]), min(at + length, window[1])
        if end > start + 1e-6:
            out.append((name, start, end))

    def holder(content: dict, at: float, length: float | None, window: tuple[float, float],
               assets: dict, scenes: dict, rate: float, depth: int) -> bool:
        """Walk what a composition or scene_ref holds; True when it holds a picture."""
        inside = (max(at, window[0]), min(at + length, window[1]) if length is not None else window[1])
        inner_count = len(out)
        if content.get('kind') == 'composition':
            walk(content.get('layers'), at, inside, content.get('assets') and asset_table(content) or assets,
                 content.get('composition'), {**scenes, **(content.get('scenes') or {})}, rate, depth + 1)
        else:
            inner = _asset(content, assets, scenes).get('scene')
            if isinstance(inner, dict):
                speed = _speed(content, {})
                trim = content.get('trim') if isinstance(content.get('trim'), dict) else {}
                t_in = float(trim['in']) if _num(trim.get('in')) else 0.0
                if _num(trim.get('out')):
                    inside = (inside[0], min(inside[1], at + (float(trim['out']) - t_in) * rate / speed))
                walk(inner.get('layers'), at - t_in * rate / speed, inside, asset_table(inner),
                     inner.get('composition'), {**scenes, **(inner.get('scenes') or {})}, rate / speed, depth + 1)
        return len(out) > inner_count

    def walk(layers, offset: float, window: tuple[float, float], assets: dict, comp, scenes: dict, rate: float, depth: int) -> None:
        if depth > 32:
            return
        if isinstance(comp, dict) and _num(comp.get('duration')):
            window = (window[0], min(window[1], offset + float(comp['duration']) * rate))
        for layer in layers or []:
            if not isinstance(layer, dict):
                continue
            content = layer.get('content') if isinstance(layer.get('content'), dict) else {}
            kind = content.get('kind')
            start = layer.get('start', 0)
            at = offset + (float(start) if _num(start) else 0.0) * rate
            if kind != 'track' and not _num(layer.get('duration')) and math.isfinite(window[1]):
                length = max(0.0, window[1] - at)
            else:
                length = own_length(layer, assets, scenes=scenes)
                length = length * rate if length is not None else None
            name = str(layer.get('id'))
            if kind == 'track':
                end = min(at + length, window[1]) if length is not None else window[1]
                clock = at
                for n, clip in enumerate(content.get('clips') or []):
                    if not isinstance(clip, dict):
                        continue
                    clip_length = own_length(clip, assets, scenes=scenes)
                    if clip_length is None:
                        break
                    clip_length *= rate
                    clip_content = clip.get('content') if isinstance(clip.get('content'), dict) else {}
                    clip_name = str(clip.get('id') or f'{name}[{n}]')
                    inner_window = (max(at, window[0]), end)
                    if clip_content.get('kind') in ('composition', 'scene_ref'):
                        if not holder(clip_content, clock, clip_length, inner_window, assets, scenes, rate, depth):
                            place(clip_name, clock, clip_length, inner_window)
                    elif clip_content.get('kind') in PICTURE_KINDS or 'kind' not in clip_content:
                        place(clip_name, clock, clip_length, inner_window)
                    clock += clip_length
                continue
            if kind in ('composition', 'scene_ref'):
                if holder(content, at, length, window, assets, scenes, rate, depth):
                    continue
                if kind == 'composition':
                    place(name, at, length, window)
                continue
            if kind in PICTURE_KINDS:
                place(name, at, length, window)

    walk(scene.get('layers'), 0.0, (0.0, scene_length(scene) or float('inf')), asset_table(scene),
         scene.get('composition'), scene.get('scenes') or {}, 1.0, 0)
    return out


def last_slot(placed: list[tuple[str, float, float]]) -> tuple[str, float, float]:
    """The slot on screen at the end: of those that end last, the one that came in last. Cards that
    stack, and a background under the whole reel, end with it but came in earlier."""
    end = max(x[2] for x in placed)
    return max((x for x in placed if x[2] >= end - FRAME), key=lambda x: x[1])


def beat_median(placed: list[tuple[str, float, float]], last: tuple[str, float, float]) -> float:
    """The usual time from one slot coming in to the next, before the last one."""
    starts = sorted({round(a, 3) for _, a, _ in placed if a < last[1] - FRAME} | {round(last[1], 3)})
    gaps = sorted(b - a for a, b in zip(starts, starts[1:]))
    return gaps[len(gaps) // 2] if gaps else last[2] - last[1]


def reel_length(scene: dict) -> float:
    """The composition's duration; without one, where its last layer ends, as the engine plays it:
    a track as long as its clips, a media layer as its trim or its asset, a composition as its
    layers, at any depth."""
    return scene_length(scene) or 0.0


def seconds(value) -> float | None:
    """A length as seconds: 25, 25.0, "25", "25 s", "25s", "0:25"."""
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value) if value > 0 else None
    if isinstance(value, str):
        m = re.fullmatch(r'\s*(?:(\d+):)?(\d+(?:\.\d+)?)\s*(?:s|sec|seconds)?\s*', value)
        if m:
            total = float(m.group(2)) + 60 * float(m.group(1) or 0)
            return total if total > 0 else None
    return None


def chosen_length(record: dict, sheet_length: float | None) -> tuple[float | None, str]:
    """The reel's length: the user's own (`brief.said.length`), else the cut pace's, else the sheet's."""
    brief = record.get('brief') if isinstance(record.get('brief'), dict) else {}
    said = brief.get('said') if isinstance(brief.get('said'), dict) else {}
    pace = record.get('cutPace') if isinstance(record.get('cutPace'), dict) else {}
    for value, where in ((said.get('length'), 'the user\'s length'), (pace.get('length'), 'the cut pace\'s length')):
        if seconds(value):
            return seconds(value), where
    return sheet_length, 'the recipe\'s length'


def length_check(record: dict, scene: dict) -> dict:
    """The reel ends at its length, and its last clip is not held past its beat. The length is the
    user's when they gave one (`brief.said.length`), else the cut pace's, else the sheet's
    `total_length`; the sheet's last beat stretches with it. A clip held 6 s at the end reads as a
    stalled reel."""
    sheet = record.get('sheet') if isinstance(record.get('sheet'), dict) else {}
    beats = [b for b in sheet.get('beats') or [] if isinstance(b, dict)
             and isinstance(b.get('start'), (int, float)) and isinstance(b.get('end'), (int, float))]
    recipe = seconds(sheet.get('total_length'))
    if not recipe and beats:
        recipe = max(b['end'] for b in beats)
    length, where = chosen_length(record, recipe)
    if not length:
        return {'ok': True, 'problems': [], 'open': ['length: the record holds no length (brief.said.length, cutPace.length or sheet.total_length)']}
    stretch = length / recipe if recipe else 1.0
    problems = []
    end = reel_length(scene)
    if end > length + END_TOLERANCE:
        problems.append({'problem': f'the reel runs {end:.2f} s, past {where} {length:g} s',
                         'over': round(end - length, 2)})
    elif end < length - max(END_TOLERANCE, SHORT_SHARE * length):
        problems.append({'problem': f'the reel runs {end:.2f} s, short of {where} {length:g} s',
                         'short': round(length - end, 2)})
    placed = slots(scene)
    if placed:
        last = last_slot(placed)
        held = last[2] - last[1]
        if beats:
            final = max(beats, key=lambda b: b['end'])
            beat = (final['end'] - final['start']) * stretch
        else:
            beat = beat_median(placed, last)
        if held - beat > TAIL_LIMIT:
            problems.append({'layer': last[0], 'problem': f'the last clip holds {held:.2f} s, {held - beat:.2f} s '
                             f'longer than its {beat:.2f} s beat (at most {TAIL_LIMIT:g} s longer)',
                             'tail': round(held - beat, 2)})
    return {'ok': not problems, 'problems': problems, 'open': [], 'length': length, 'lengthFrom': where}
