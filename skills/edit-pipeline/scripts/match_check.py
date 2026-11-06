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
COLOUR_KEYS = ('color', 'colour', 'background', 'fill')
TEXT_KINDS = ('captions', 'text')
NEUTRALS = ('#000000', '#FFFFFF')


def holds(plan: dict) -> list[tuple[int, float]]:
    """(row, seconds) for every planned shot that says where it sits in the cut."""
    out = []
    for i, r in enumerate(plan.get('rows') or []):
        if not isinstance(r, dict):
            continue
        for a, b in (('sceneStart', 'sceneEnd'), ('start', 'end')):
            if isinstance(r.get(a), (int, float)) and isinstance(r.get(b), (int, float)):
                out.append((i, float(r[b]) - float(r[a])))
                break
    return out


def pace_check(cut_pace: dict, plan: dict, approvals: list | None = None) -> dict:
    """Every shot at or above minHold fails the plan when it is not. The cuts per 10 s far from
    cutPace's density are reported `open`, never failed: cutPace is also the job's default when no
    reference was read, and a standing note ("keep shots longer") is the user's say on the pace
    without being a `format:pace` approval. The open line is said to the user before the build."""
    problems: list[dict] = []
    opened: list[str] = []
    timed = holds(plan)
    rows = [r for r in plan.get('rows') or [] if isinstance(r, dict)]
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


def rhythm_check(rhythm, plan: dict, approved: set | None = None) -> dict:
    """The cut's shape, beyond its average: the median hold, runs of fast shots, one long hold in
    each section, and a breath with no voice between sections. A finding is `open`, said to the user
    before the build, unless `register` quotes the brief's own style words ("cinematic, atmospheric"):
    then the brief asked for this shape, and a plan that breaks it fails. A shape the user chose
    instead (an approval scoped `format:rhythm`) passes."""
    if not isinstance(rhythm, dict) or 'format:rhythm' in (approved or set()):
        return {'problems': [], 'open': []}
    rows = [r for r in plan.get('rows') or [] if isinstance(r, dict)]
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
                if a.get('phrase') and b.get('phrase'):
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


def colours(node, path: str = '', text: bool = False):
    """(path, hex, alpha, on text) for every colour a scene sets."""
    if isinstance(node, dict):
        kind = (node.get('content') or {}).get('kind') if isinstance(node.get('content'), dict) else node.get('kind')
        text = text or kind in TEXT_KINDS
        for k, v in node.items():
            if k == 'effects':  # an edge or shadow is not the text's colour
                continue
            p = f'{path}.{k}' if path else k
            if k in COLOUR_KEYS and isinstance(v, str) and HEX.match(v):
                m = HEX.match(v)
                yield p, '#' + m.group(1).upper(), m.group(2), text
            else:
                yield from colours(v, p, text)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from colours(v, f'{path}[{i}]', text)


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
    for path, hexcode, alpha, on_text in colours(scene.get('layers', scene)):
        e = by_hex.get(hexcode)
        see_through = alpha is not None and alpha.upper() != 'FF'
        if e is None and neutrals_ok and not on_text and (hexcode in NEUTRALS or see_through):
            continue
        if e is None:
            problems.append({'path': path, 'colour': hexcode, 'problem': 'not in the brand palette'})
        elif on_text and e.get('text') is False:
            problems.append({'path': path, 'colour': hexcode, 'name': e.get('name'),
                             'problem': 'the brand guide keeps this colour off text'})
    return {'ok': not problems, 'problems': problems, 'open': []}
