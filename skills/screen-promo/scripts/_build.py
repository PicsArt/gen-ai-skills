"""
Build a scene from a spec and its moments: a promo or a timelapse, with the diagnostics on it.

The layout follows the input's shape. A landscape recording sits on a card in the portrait frame.
A portrait one fills the frame, with no card, and its words sit on a bubble or a scrim over it. A
square one fills the frame's width under the text band. The push applies to all three.

A promo spec is `uri`, `font`, `target`, `hook` ({title, step, duration?}), `steps` and `outro`
({cta, steps, duration?}), and optionally `duration` (the uploaded copy's, when it is shorter than
the analysed file's), `clip`, `product`, `audience`, `language`, `sourceAudio` and `sfx`
({push?, outro?, volume?}: each sound `{url, duration}`). Each of its
steps is `{id, prompt?, label?, from?, to?}` and one of: `step`, a proposed step by index; `events`
and `result`; or `from`/`to` alone.

A timelapse spec is `uri`, `font`, `process` ({from, to, count, shown?, speed?, box?}), `labels`
([{from, text, box?}]: chapter names by source time), `reveal` ({at, until?, box?, hold?}), `hook`
({title, duration?}) and `outro` ({cta, at, duration?}), and optionally `target` and the promo's
optional fields but `sfx`.
"""
from __future__ import annotations

import math
from typing import Any, Dict, List, Optional

from _diagnostics import diagnose
from _geometry import Box, Size, pad, round
from _js import INF, dumps, js_max, js_min, math_round, number, to_fixed
from _moments import Moments, event, index, input_of
from _scene import COMP, FULL_FRAME, PROMPT_LAYOUT, SQUARE_PANEL, TALL_PANEL, card_panel, compile_promo
from _stages import chapter_stages, plan_timelapse
from _steps import MIN_SHOT, shot_at
from _timeedit import fit_steps, story_events
from zoom import rest_framing, zoom_track

Spec = Dict[str, Any]


def layout_for(orientation: str, words: bool, m: Moments) -> Dict[str, Box]:
    """Where a step's panel sits, and what its rest framing fits."""
    full: Box = {'x': 0, 'y': 0, 'w': m['source']['w'], 'h': m['source']['h']}
    if orientation == 'portrait':
        return {'panel': FULL_FRAME, 'content': full}
    if orientation == 'square':
        return {'panel': SQUARE_PANEL, 'content': full}
    return {'panel': PROMPT_LAYOUT['panel'] if words else TALL_PANEL, 'content': m['content']}


def on_content(b: Box, content: Box, share: float = 0.25) -> Box:
    """
    `b` cut to the content box. When little of it is on the content (a change that is mostly the
    presenter's face under the screen), the content box itself: a sliver of `b` is no focus.
    """
    x = max(b['x'], content['x'])
    y = max(b['y'], content['y'])
    w = min(b['x'] + b['w'], content['x'] + content['w']) - x
    h = min(b['y'] + b['h'], content['y'] + content['h']) - y
    return {'x': x, 'y': y, 'w': w, 'h': h} if w > 0 and h > 0 and w * h >= share * b['w'] * b['h'] else content


# Source seconds a still plays: a near-frozen 0.15 s.
STILL = 0.15


def sample_at(m: Moments, edit: Dict[str, Any], settle: float) -> float:
    """
    The source second a result's still is taken at: just after it settles, and inside both the
    seconds its step plays and, in an edited input, its shot. A still just past a shot's end is the
    next shot.
    """
    shot = shot_at(m, settle)
    lo = max(shot['start'], js_min(p['srcIn'] for p in edit['pieces']))
    hi = min(shot['end'], js_max(p['srcOut'] for p in edit['pieces'])) - STILL
    return round(min(max(settle + 0.2, lo), max(lo, hi)), 3)


def choose_steps(spec: Spec, m: Moments) -> List[Dict[str, Any]]:
    """Each spec step as events and a result, by proposed index, by events, or by its from/to alone."""
    proposed = m['steps']
    out = []
    for i, s in enumerate(spec['steps']):
        base = {'id': s['id'], 'prompt': s.get('prompt'), 'label': s.get('label'), 'from': s.get('from'), 'to': s.get('to'), 'field': f'steps[{i}]'}
        if s.get('step') is not None:
            try:
                p = proposed[index(s['step'], len(proposed), 'proposed step')]
            except ValueError as err:
                raise ValueError(f'steps[{i}]: {err}') from None
            events = s['events'] if s.get('events') is not None else story_events(m, p, retyped=s.get('prompt') is not None)
            result = _or(s.get('result'), p['result'])
            chosen = {**base, 'events': events, 'result': result}
            # The moments found the subject of the proposed step's result, and of no other event.
            if p.get('subject') is not None and result == p['result']:
                chosen['subject'] = p['subject']
            out.append(chosen)
            continue
        if s.get('events'):
            out.append({**base, 'events': s['events'], 'result': _or(s.get('result'), s['events'][-1])})
            continue
        if s.get('result') is not None:
            out.append({**base, 'events': [s['result']], 'result': s['result']})
            continue
        if s.get('from') is None and s.get('to') is None:
            raise ValueError(f'steps[{i}]: give step, events and result, or from and to')
        start = _or(s.get('from'), 0)
        to = _or(s.get('to'), m['source']['duration'])
        inside = [e for e in m['events'] if e['kind'] != 'cut' and e['settle'] >= start and e['start'] <= to]
        candidates = [e for e in inside if e['kind'] != 'scroll']
        if not candidates:
            raise ValueError(f'steps[{i}]: no event between {number(start)} and {number(to)} s')
        result = candidates[0]
        for e in candidates[1:]:
            if e['mass'] > result['mass']:
                result = e
        out.append({**base, 'events': [e['index'] for e in inside], 'result': result['index']})
    return out


def f1(t: float) -> str:
    return to_fixed(t, 1)


def up1(t: float) -> float:
    """One decimal, rounded up, so a least value printed this way still holds."""
    return math.ceil(t * 10 - 1e-6) / 10


def down1(t: float) -> float:
    """One decimal, rounded down, so a most value printed this way still holds."""
    return math.floor(t * 10 + 1e-6) / 10


def box_text(b: Box) -> str:
    return f"{number(math_round(b['x']))},{number(math_round(b['y']))} {number(math_round(b['w']))}x{number(math_round(b['h']))}"


def about_of(spec: Spec, m: Moments) -> Dict[str, Any]:
    """What the spec says about the promo, and what the moments say the input is."""
    about = {k: spec[k] for k in ('product', 'audience', 'language') if spec.get(k) is not None}
    about['sourceAudio'] = _or(spec.get('sourceAudio'), 'mute')
    info = input_of(m)
    return {**about, 'tier': m['tier'], 'tierReason': m['tierReason'], 'orientation': info['orientation'], 'edited': info['edited']}


def build_promo(spec: Spec, m: Moments) -> Dict[str, Any]:
    """
    A promo: its scene, duration, timeline and diagnostics, and `explain`: `about`, `overBy` (output
    seconds still over the target after fitting), `textPx` (UI text at rest, frame px), `restScale`
    and the built `steps`.
    """
    hook_length = _or(spec['hook'].get('duration'), 2.2)
    outro_length = _or(spec['outro'].get('duration'), 2.5)
    info = input_of(m)
    chosen = choose_steps(spec, m)
    fit = fit_steps(m, chosen, spec['target'] - hook_length - outro_length)
    src: Size = {'w': m['source']['w'], 'h': m['source']['h']}
    promo_steps: List[Dict[str, Any]] = []
    for i, s in enumerate(chosen):
        edit = fit['edits'][i]
        words = _or(s['prompt'], s['label']) is not None
        layout = layout_for(info['orientation'], words, m)
        panel = layout['panel']
        r = event(m, s['result'])
        # A result's box can reach past the content (a face under the screen): keep what is on it.
        core = on_content(r['core'], m['content'])
        box = on_content(r['box'], m['content'])
        settle = _or(edit.get('settle'), r['settle'])
        at = sample_at(m, edit, settle)
        # The subject the moments found for the proposed step, when the spec step is one.
        subject = s.get('subject')
        # Push when the result has finished arriving, onto its subject when there is one, and keep
        # its card's header out of the window.
        focus = {'at': _or(edit.get('settleAt'), edit['resultAt']), 'box': _or(subject, core), 'luma': r['luma'], 'card': core}
        zoom = zoom_track(src, COMP, panel, layout['content'], [focus], edit['duration'])
        result = {'box': box, 'settle': settle, **({'subject': subject} if subject is not None else {}), 'at': at}
        step: Dict[str, Any] = {'id': s['id']}
        if s['prompt'] is not None:
            step['prompt'] = s['prompt']
        elif s['label'] is not None:
            step['label'] = s['label']
        step['edit'] = edit
        step['zoom'] = zoom
        # A landscape step leaves its panel to the compiler, so the hook keeps its tall panel.
        if info['orientation'] != 'landscape':
            step['panel'] = panel
        step['result'] = result
        promo_steps.append(step)
    source_duration = min(m['source']['duration'], _or(spec.get('duration'), INF))
    compiled = compile_promo({
        'source': {'uri': spec['uri'], **src, 'duration': source_duration},
        'font': spec['font'],
        'clip': spec.get('clip'),
        'sourceAudio': spec.get('sourceAudio'),
        'sfx': spec.get('sfx'),
        'hook': spec['hook'],
        'steps': promo_steps,
        'outro': spec['outro'],
    })
    scene = compiled['scene']
    duration = compiled['duration']
    timeline = compiled['timeline']

    def field(id_: str) -> str:
        return next((c['field'] for c in chosen if c['id'] == id_), 'steps')

    checked: List[Dict[str, Any]] = []
    for i, s in enumerate(promo_steps):
        c = chosen[i]
        r = event(m, c['result'])
        # plan_step sets bounds on every step it plans.
        b = s['edit']['bounds']
        # A `to` inside a progressive result plays the first part of a long event, on purpose.
        cut = b.get('movedBy') == 'to' and c['to'] is not None and not (r['kind'] == 'progressive' and c['to'] > r['start'])
        checked.append({
            'field': c['field'],
            'id': s['id'],
            'edit': s['edit'],
            'words': _or(s.get('prompt'), s.get('label')) is not None,
            'labels': s.get('labels'),
            'textPx': s['zoom']['textPx'],
            'settle': s['result']['settle'],
            'cutFix': _cut_fix(c['field']),
            'wordsFix': _words_fix(c['field']),
            'contentFix': f"set {c['field']}.result to an event inside the content box {box_text(m['content'])}, or {c['field']}.from/to around one",
            'audioFix': f"set {c['field']}.from/to around a moment that plays at 1×, or set sourceAudio to 'mute'",
            'pushSkipped': s['zoom'].get('skipped'),
            'pushFix': (
                f"leave {c['field']} out, or give it a from/to on a shot that runs at least {f1(MIN_SHOT)} s past its result"
                if info['edited']
                else f"set {c['field']}.to at least {f1(MIN_SHOT)} s after its result settles ({f1(s['result']['settle'])} s)"
            ),
            **({'settleCut': {'to': c['to'], 'settles': b['settles']}, 'settleFix': settle_fix(c['field'], b, m)} if cut else {}),
            'holdFix': hold_fix(i, chosen, fit['edits'], m),
        })
    hook_index = next((k for k, s in enumerate(promo_steps) if s['id'] == spec['hook'].get('step')), len(promo_steps) - 1)
    hook_step = promo_steps[hook_index]

    def sample_fix(id_: str) -> str:
        settled = next((s['result']['settle'] for s in promo_steps if s['id'] == id_), None)
        return f'set {field(id_)}.from/to so the step plays its result settling (it settles at {f1(_or(settled, 0))} s)'

    samples: List[Dict[str, Any]] = [{'layer': 'hook_panel', 'at': hook_step['result']['at'], 'length': STILL, 'step': checked[hook_index], 'fix': sample_fix(hook_step['id'])}]
    for j, id_ in enumerate(spec['outro']['steps'][:4]):
        k = next((k for k, s in enumerate(promo_steps) if s['id'] == id_), -1)
        if k >= 0:
            samples.append({'layer': f'grid_{j}_panel', 'at': promo_steps[k]['result']['at'], 'length': STILL, 'step': checked[k], 'fix': sample_fix(id_)})
    lies_inside = f"lies inside the content box {box_text(m['content'])}"
    panels = [
        {'layer': 'hook_panel', 'span': 'hook', 'name': f"hook ({hook_step['id']})", 'fix': f'set hook.step to a step whose result {lies_inside}'},
        *({'layer': f'grid_{j}_panel', 'span': 'outro', 'name': f'outro.steps[{j}] ({id_})', 'fix': f'set outro.steps[{j}] to a step whose result {lies_inside}'} for j, id_ in enumerate(spec['outro']['steps'][:4])),
    ]
    longest = 0
    for k, s in enumerate(promo_steps):
        if s['edit']['duration'] > promo_steps[longest]['edit']['duration']:
            longest = k

    def length_fix(d: float, t: float) -> str:
        if d > t:
            return f"remove {chosen[longest]['field']} ({promo_steps[longest]['id']}, {number(promo_steps[longest]['edit']['duration'])} s) from steps, or set target to {number(math_round(d))}"
        return f'add a step to steps, or set target to {number(math_round(d))}'

    texts = [*spec['hook']['title'], *spec['outro']['cta']]
    for s in promo_steps:
        texts += _or(s.get('prompt'), _or(s.get('label'), []))
        for label in _or(s.get('labels'), []):
            texts += label['text']
    words = [{'field': 'hook.title', 'kind': 'hook', 'lines': spec['hook']['title']}]
    for k, s in enumerate(promo_steps):
        field = chosen[k]['field']
        if s.get('prompt'):
            words.append({'field': f'{field}.prompt', 'kind': 'prompt', 'lines': s['prompt']})
        if s.get('label'):
            words.append({'field': f'{field}.label', 'kind': 'label', 'lines': s['label']})
        for j, label in enumerate(_or(s.get('labels'), [])):
            words.append({'field': f'{field}.labels[{j}].text', 'kind': 'label', 'lines': label['text']})
    words.append({'field': 'outro.cta', 'kind': 'cta', 'lines': spec['outro']['cta']})
    diagnostics = diagnose({
        'a': m,
        'scene': scene,
        'timeline': timeline,
        'steps': checked,
        'samples': samples,
        'panels': panels,
        'duration': duration,
        'target': spec['target'],
        'lengthFix': length_fix,
        'sourceAudio': spec.get('sourceAudio'),
        'language': spec.get('language'),
        'font': spec['font'],
        'texts': texts,
        'words': words,
    })
    rest_layout = layout_for(info['orientation'], True, m)
    first_panel = promo_steps[0].get('panel') if promo_steps else None
    rest = rest_framing(src, _or(first_panel, rest_layout['panel']), rest_layout['content'])
    explain = {
        'about': about_of(spec, m),
        'overBy': fit['overBy'],
        'textPx': promo_steps[0]['zoom']['textPx'] if promo_steps else 0,
        'restScale': rest['S'],
        'steps': promo_steps,
    }
    return {'scene': scene, 'duration': duration, 'timeline': timeline, 'diagnostics': diagnostics, 'explain': explain}


def _cut_fix(field: str):
    return lambda cut, after: f'set {field}.to to {f1(cut - 0.1)}' if after else f'set {field}.from to {f1(cut + 0.1)}'


def _words_fix(field: str):
    return lambda _from: f'set {field}.label to a feature line (or {field}.prompt to the request it answers)'


def settle_fix(field: str, b: Dict[str, Any], m: Moments) -> str:
    """
    The fix for a `to` that moved the push before its result settles: the least `to` that lets it
    settle and hold, from `plan_step`'s bounds. When the shot or the recording ends before that, no
    `to` reaches it.
    """
    tail = b['leastTo']['settle'] - b['settles']
    least = up1(b['leastTo']['settle'])
    # The result's shot; in a raw input, the whole recording.
    end = shot_at(m, b['settles'])['end']
    edited = input_of(m)['edited']
    if least <= end + 1e-6:
        upto = f", up to its shot's end at {f1(end)} s" if edited else ''
        return f'set {field}.to to {f1(least)} or later, {f1(tail)} s after its result settles{upto}'
    short = f"{f1(end - b['settles'])} s after the result settles, under the {f1(tail)} s its post-roll and hold need"
    return f'leave {field} out, or set {field}.to to {f1(end)}: its shot ends {short}' if edited else f'leave {field}.to out: the recording ends {short}'


def hold_fix(i: int, chosen: List[Dict[str, Any]], edits: List[Dict[str, Any]], m: Moments) -> str:
    """
    The fix for a hold slow enough to read as a freeze, by what stopped its source: a later `to`, a
    longer shot, or room before the step that shows the recording next.
    """
    field = chosen[i]['field']
    edit = edits[i]
    b = edit['bounds']
    tail = b['leastTo']['settle'] - b['settles']
    end = shot_at(m, b['settles'])['end']
    edited = input_of(m)['edited']
    hold = next((p for p in reversed(edit['pieces']) if p['role'] == 'hold'), None)
    if b['holdEnd'] == 'next_step' and hold:
        # fit_steps stops a hold at the first later step that starts after the result settles.
        starts_at = [{'k': k, 'at': e['pieces'][0]['srcIn'] if e['pieces'] else INF} for k, e in enumerate(edits)]
        later = sorted((x for x in starts_at if x['k'] != i and x['at'] > b['settles']), key=lambda x: x['at'])
        if later:
            nxt = later[0]
            other = chosen[nxt['k']]
            start_from = up1(hold['srcIn'] + hold['outOut'] - hold['outIn'])
            starts = f"{other['field']} starts showing the recording at {f1(nxt['at'])} s"
            if start_from <= event(m, other['result'])['start'] + 1e-6:
                return f"set {other['field']}.from to {f1(start_from)} or later, or leave {field} or {other['field']} out: {starts}"
            return f"leave {field} or {other['field']} out: {starts}"
    least = up1(b['leastTo']['hold'])
    if b['holdEnd'] == 'to' and least <= end + 1e-6:
        upto = f", up to its shot's end at {f1(end)} s" if edited else ''
        return f'set {field}.to to {f1(least)} or later, so the hold plays at 1×{upto}'
    if edited:
        return f"leave {field} out, or give it a from/to on a shot that runs at least {f1(tail)} s past its result's start"
    return f"set {field}.from/to around a result that settles at least {f1(tail)} s before the recording ends at {f1(m['source']['duration'])} s, or leave {field} out"


def _same_box(x: Optional[Box], y: Optional[Box]) -> bool:
    return dumps(x) == dumps(y)


def build_timelapse(spec: Spec, m: Moments) -> Dict[str, Any]:
    """
    A timelapse: its scene, duration, timeline and diagnostics, and `explain`: `about`, `stages`
    (how many), `shownSource` (source seconds the process shows), `labels` (each chapter label,
    step-relative output seconds) and the built `steps`.
    """
    src: Size = {'w': m['source']['w'], 'h': m['source']['h']}
    full: Box = {'x': 0, 'y': 0, **src}
    work = _or(m.get('work'), m['content'])
    info = input_of(m)
    keep = spec.get('sourceAudio') == 'keep'
    process = spec['process']
    labels_in = spec['labels']
    reveal_in = spec['reveal']
    source_length = m['source']['duration']

    # Chapters that frame the same box play as one step, on one card.
    chapters = [max(l['from'], process['from']) if i == 0 else l['from'] for i, l in enumerate(labels_in)]
    process_box = _or(process.get('box'), pad(work, 0.25, src))

    def box_of(j: int) -> Box:
        return _or(labels_in[j].get('box'), process_box)

    groups: List[List[int]] = []
    for j, l in enumerate(labels_in):
        last = groups[-1] if groups else None
        if last and _same_box(labels_in[last[0]].get('box'), l.get('box')):
            last.append(j)
        else:
            groups.append([j])
    stages = chapter_stages(chapters, process['to'], process['count'])
    lapse = plan_timelapse(stages, source_length, shown=process.get('shown'), speed=process.get('speed'), hold_last=False, cuts=info['cuts'], fps=m['analysis']['fps'])

    def chapter_of(t: float) -> int:
        return max(0, len([c for c in chapters if c <= t + 1e-6]) - 1)

    process_steps = []
    for gi, g in enumerate(groups):
        id_ = 'process' if len(groups) == 1 else f'process_{gi + 1}'
        pieces = [p for p in lapse['pieces'] if chapter_of(stages[p['stage']]['t']) in g]
        t0 = pieces[0]['outIn'] if pieces else 0
        rebased = [{'srcIn': p['srcIn'], 'srcOut': p['srcOut'], 'speed': p['speed'], 'outIn': round(p['outIn'] - t0, 3), 'outOut': round(p['outOut'] - t0, 3), 'role': 'speedup'} for p in pieces]
        length = round(rebased[-1]['outOut'] if rebased else 0, 3)
        edit = {'id': id_, 'pieces': rebased, 'duration': length, 'resultAt': 0, 'eventAt': {}, 'jumped': 0}

        # A label shows from the first piece at or after its source time until the next label.
        def out_at(s: float, rebased: List[Dict[str, Any]] = rebased, length: float = length) -> float:
            return next((p['outIn'] for p in rebased if p['srcOut'] > s), length)

        shown_labels = []
        for k, j in enumerate(g):
            label = {
                'at': 0 if k == 0 else out_at(labels_in[j]['from']),
                'until': out_at(labels_in[g[k + 1]]['from']) if k + 1 < len(g) else length,
                'text': labels_in[j]['text'],
            }
            if label['until'] > label['at']:
                shown_labels.append(label)
        if rebased:
            process_steps.append({'id': id_, 'g': g, 'edit': edit, 'labels': shown_labels, 'box': box_of(g[0])})

    hold = _or(reveal_in.get('hold'), 3)
    # Recordings often end on a cut to black: stop where the last still span stops.
    last_still = next((d for d in reversed(m['dead']) if d['kind'] == 'still'), None)
    if reveal_in.get('until') is not None:
        until = reveal_in['until']
    elif last_still and source_length - last_still['end'] < 3:
        until = last_still['end'] - 0.1
    else:
        until = source_length - 0.05
    reveal_at = reveal_in['at']
    # Kept sound plays the reveal at 1x, from its start, rather than slowed or sped to the hold.
    reveal_out = min(until, reveal_at + hold) if keep else until
    reveal_length = round(reveal_out - reveal_at, 3) if keep else hold
    reveal = {
        'id': 'reveal',
        'pieces': [{'srcIn': reveal_at, 'srcOut': round(reveal_out, 3), 'speed': round((reveal_out - reveal_at) / reveal_length, 4), 'outIn': 0, 'outOut': reveal_length, 'role': 'hold'}],
        'duration': reveal_length,
        'resultAt': 0,
        'eventAt': {},
        'jumped': 0,
    }
    render_box = _or(reveal_in.get('box'), full)

    # A landscape process sits on a card the box's shape over its own blurred footage (a tall panel
    # shows the UI around it); a portrait or square one fills its layout's panel.
    def panel_for(box: Box) -> Box:
        return card_panel(box) if info['orientation'] == 'landscape' else layout_for(info['orientation'], False, m)['panel']

    reveal_settle = reveal_at + 4
    still_at = round(min(reveal_settle + 0.2, reveal_out - STILL), 3)
    steps: List[Dict[str, Any]] = []
    for s in process_steps:
        panel = panel_for(s['box'])
        steps.append({'id': s['id'], 'edit': s['edit'], 'panel': panel, 'backdrop': True, 'zoom': zoom_track(src, COMP, panel, s['box'], [], s['edit']['duration']), 'result': {'box': s['box'], 'settle': process['to']}, 'labels': s['labels']})
    steps.append({
        'id': 'reveal',
        'edit': reveal,
        'panel': panel_for(render_box),
        'backdrop': True,
        'zoom': zoom_track(src, COMP, panel_for(render_box), render_box, [{'at': 0.1, 'box': render_box, 'luma': 120}], reveal_length),
        'result': {'box': render_box, 'settle': reveal_settle, 'at': still_at},
    })

    def still_of(t: float) -> Dict[str, Any]:
        # Chosen boxes are framed as they are: a margin around one reaches into the UI beside it.
        box = render_box if t >= reveal_at else box_of(chapter_of(t))
        return {'box': box, 'subject': box, 'settle': t}

    hook = {'title': spec['hook']['title'], 'step': 'reveal'}
    if spec['hook'].get('duration') is not None:
        hook['duration'] = spec['hook']['duration']
    outro = {'cta': spec['outro']['cta'], 'steps': [], 'stills': [still_of(t) for t in spec['outro']['at']]}
    if spec['outro'].get('duration') is not None:
        outro['duration'] = spec['outro']['duration']
    compiled = compile_promo({
        'source': {'uri': spec['uri'], **src, 'duration': min(source_length, _or(spec.get('duration'), INF))},
        'font': spec['font'],
        'clip': spec.get('clip'),
        'sourceAudio': spec.get('sourceAudio'),
        'hook': hook,
        'steps': steps,
        'outro': outro,
    })
    scene = compiled['scene']
    duration = compiled['duration']
    timeline = compiled['timeline']

    def box_field(g: List[int]) -> str:
        return f'labels[{g[0]}].box' if labels_in[g[0]].get('box') else 'process.box'

    checked: List[Dict[str, Any]] = []
    for s in process_steps:
        checked.append({
            'field': 'process' if len(groups) == 1 else f"labels[{s['g'][0]}]",
            'id': s['id'],
            'edit': s['edit'],
            'words': False,
            'labels': s['labels'],
            'cutFix': lambda cut, after=False: f'lower process.speed or process.shown, so no stage window reaches the cut at {f1(cut)} s (a stage plays process.speed × process.shown source seconds)',
            'wordsFix': _near_fix(s['edit']['pieces'], process['from']),
            'contentFix': f"set {box_field(s['g'])} inside the content box {box_text(m['content'])}",
            'audioFix': "none needed for a timelapse: its process always plays at process.speed, and only reveal plays at 1× with sound; set sourceAudio to 'mute' to silence reveal too",
        })
    checked.append({
        'field': 'reveal',
        'id': 'reveal',
        'edit': reveal,
        'words': False,
        'settle': reveal_settle,
        'cutFix': lambda cut, after: f'set reveal.until to {f1(cut - 0.1)}' if after else f'set reveal.at to {f1(cut + 0.1)}',
        'wordsFix': lambda _from: 'set reveal.hold to 4 or less',
        'contentFix': f"set reveal.box inside the content box {box_text(m['content'])}",
        'audioFix': 'set reveal.hold to at most reveal.until − reveal.at, so reveal plays at 1×',
        'pushSkipped': steps[-1]['zoom'].get('skipped'),
        # The reveal's push is due 0.1 s in, so a full one needs MIN_SHOT after that.
        'pushFix': f"set reveal.hold to {f1(0.1 + MIN_SHOT)} or more{', and reveal.until at least that far past reveal.at' if keep else ''}",
        'holdFix': f'set reveal.hold to {f1(down1(reveal_out - reveal_at))} or less, or reveal.at earlier, so the reveal plays at 1×',
    })
    samples: List[Dict[str, Any]] = [
        {'layer': 'hook_panel', 'at': still_at, 'length': STILL, 'step': checked[-1], 'fix': f'set reveal.at and reveal.until so the render has finished by {f1(still_at)} s'},
        *({'layer': f'grid_{k}_panel', 'at': min(t + 0.2, source_length - 0.2), 'length': STILL, 'fix': f'set outro.at[{k}] to a second inside one shot'} for k, t in enumerate(spec['outro']['at'][:4])),
    ]

    # A tile frames the reveal's box from reveal.at on, and its chapter's box before.
    def tile_box(t: float) -> str:
        if t >= reveal_at:
            return 'reveal.box'
        j = chapter_of(t)
        return f'labels[{j}].box' if labels_in[j].get('box') else 'process.box'

    inside = f"inside the content box {box_text(m['content'])}"
    panels = [
        {'layer': 'hook_panel', 'span': 'hook', 'name': 'hook (reveal)', 'fix': f'set reveal.box {inside}'},
        *({'layer': f'grid_{k}_panel', 'span': 'outro', 'name': f'outro.at[{k}] ({number(t)} s)', 'fix': f'set {tile_box(t)} {inside}, or outro.at[{k}] to a time framed there'} for k, t in enumerate(spec['outro']['at'][:4])),
    ]

    def length_fix(d: float, t: float) -> str:
        shown = _or(process.get('shown'), 0.7)
        count = max(2, math_round(process['count'] + (t - d) / shown))
        return f'set process.count to {number(count)}, or set target to {number(math_round(d))}'

    texts = [*spec['hook']['title'], *spec['outro']['cta']]
    for l in labels_in:
        texts += l['text']
    words = [
        {'field': 'hook.title', 'kind': 'hook', 'lines': spec['hook']['title']},
        *({'field': f'labels[{j}].text', 'kind': 'label', 'lines': l['text']} for j, l in enumerate(labels_in)),
        {'field': 'outro.cta', 'kind': 'cta', 'lines': spec['outro']['cta']},
    ]
    diagnostics = diagnose({
        'a': m,
        'scene': scene,
        'timeline': timeline,
        'steps': checked,
        'samples': samples,
        'panels': panels,
        'duration': duration,
        'target': spec.get('target'),
        'lengthFix': length_fix,
        'sourceAudio': spec.get('sourceAudio'),
        'language': spec.get('language'),
        'font': spec['font'],
        'texts': texts,
        'words': words,
    })
    shown_source = 0
    for p in lapse['pieces']:
        shown_source = shown_source + p['srcOut'] - p['srcIn']
    explain = {
        'about': about_of(spec, m),
        'stages': len(stages),
        'shownSource': round(shown_source, 1),
        'labels': [{'step': s['id'], 'text': l['text'], 'at': l['at']} for s in process_steps for l in s['labels']],
        'steps': steps,
    }
    return {'scene': scene, 'duration': duration, 'timeline': timeline, 'diagnostics': diagnostics, 'explain': explain}


def _near_fix(pieces: List[Dict[str, Any]], process_from: float):
    def fix(from_: float) -> str:
        near = next((p['srcIn'] for p in pieces if p['outOut'] > from_), None)
        return f'add a labels entry that starts near source {f1(_or(near, process_from))} s'

    return fix


def _or(value: Any, default: Any) -> Any:
    """`value ?? default`: only a missing value takes the default."""
    return default if value is None else value
