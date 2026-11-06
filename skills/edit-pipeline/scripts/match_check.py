"""A plan's pace against the reference's, and a scene's colours against the brand's palette.

Both are numbers a draft can drift from without anyone saying so: a cut that holds each shot 2.2 s
when the reference holds 3.6 s, or a caption in a colour the brand guide keeps off text.
record.py lock-check runs the pace check; `record.py palette-check <record> <scene>` the palette.
"""
from __future__ import annotations

import re

# a plan within this share of the reference's cuts per 10 s keeps its pace
DENSITY_TOLERANCE = 0.25
HEX = re.compile(r'^#([0-9a-fA-F]{6})([0-9a-fA-F]{2})?$')
COLOUR_KEYS = ('color', 'colour', 'background', 'fill', 'stroke')
TEXT_KINDS = ('captions', 'text')
NEUTRALS = ('#000000', '#FFFFFF')


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
