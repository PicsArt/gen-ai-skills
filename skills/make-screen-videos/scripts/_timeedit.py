"""
Time edit: which source seconds play, how fast, and where the jumps are.

A recording is mostly waiting. The finished shorts in the corpus never show more than about a
second of it: they cut it or speed through it. So each step of the promo becomes a list of
pieces, source windows with a constant speed, that a scene plays back to back.

A piece is `{srcIn, srcOut, speed, outIn, outOut, role}`, its role `event`, `pause`, `speedup` or
`hold`, and its out times step-relative output seconds. A step's edit is `{id, pieces, duration,
resultAt, eventAt, jumped, settleAt, settle, bounds}`:
- `resultAt`: where the result appears, step-relative output seconds;
- `eventAt`: the output time of each shown event's start;
- `jumped`: the source seconds jump cuts removed inside the step;
- `settleAt`: where the push onto the result starts, earlier when reserving its hold;
- `settle`: the source second it settles at, after the step's bounds: the hook's and the grid's
  frame is taken just after it;
- `bounds`: how the step's hard ends bound its result (see `plan_step`).
"""
from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Set

from _geometry import round
from _js import INF, js_min, number, total
from _moments import Event, Moments, event, input_of
from _steps import CUT_GUARD, shot_at

Piece = Dict[str, Any]


class StepEdit(dict):
    """An edit's JSON fields, with event aliases for in-process source queries."""

    source_aliases: Dict[str, float]


StepChoice = Dict[str, Any]


def story_events(m: Moments, step: Dict[str, Any], before: Optional[float] = None, retyped: bool = False) -> List[float]:
    """
    The events of a proposed step worth showing: the lead-in, the page change, and whatever lands in
    the last `before` seconds before the result settles (the reply arriving). The wait between is left
    out, so the planner cuts it.

    `retyped`: a bubble above the panel re-types the request, so the recording of it being typed and
    sent is left out too. In a chat that footage is a still panel (the input box sits below the
    content column) and then a near-empty page as the new message scrolls to the top.
    """
    before = 2.5 if before is None else before
    result = event(m, step['result'])
    near = [i for i in step['events'] if event(m, i)['start'] >= result['start'] - before and event(m, i)['start'] <= result['settle']]
    opening = [] if retyped else [*step['leadIn'], *([] if step.get('boundary') is None else [step['boundary']])]
    picked = dict.fromkeys([*opening, *near, step['result']])
    return sorted(picked)


# Source seconds shown before an event starts (preRoll) and after it settles (postRoll); output
# seconds the result is held after it settles (resultHold). A gap up to pauseMax plays at 1x: it
# reads as a natural pause. A longer gap is sped up to last gapShown, unless that needs more than
# maxSpeed, and then it is cut. Progressive work (typing, streaming) plays sped up, by `speeds`.
# cutGuard: source seconds kept clear after a cut, so a trim at the cut never shows the shot before.
DEFAULT_EDIT: Dict[str, Any] = {
    'preRoll': 0.3,
    'postRoll': 0.3,
    'resultHold': 1.8,
    'pauseMax': 0.5,
    'gapShown': 0.4,
    'maxSpeed': 6,
    'speeds': {'cut': 1, 'reveal': 1, 'scroll': 1.5, 'progressive': 2},
    'cutGuard': CUT_GUARD,
}


def plan_step(m: Moments, step: StepChoice, options: Optional[Dict[str, Any]] = None) -> StepEdit:
    """
    Plan one step (`id`, `events`, `result`, and `holdUntil`, `from`, `to` when set): the chosen
    events at their speeds, the gaps between them paused, sped or cut.

    Nothing crosses a hard boundary: the step's `from`/`to`, and in an edited input each cut. A
    pre-roll starts no earlier than its event's shot, a post-roll and the hold stop at its end, and a
    gap with a cut in it is jumped. A hard end also moves the push back far enough for the
    hold to play at 1x before it, instead of freezing on the shot's last frame. `bounds` says which
    end did that, and which ended the hold. The measured settle stays separate for stills:
    - `settles`: where the result really settles;
    - `movedBy`: the hard end (`to`, `shot` or `recording`) that moved the push before it;
    - `holdEnd`: where the hold's source has to stop: a hard end, or `next_step`, a later step
      showing the recording;
    - `leastTo`: the least step `to` that holds the result at 1x (`hold`: its start, the post-roll
      and the hold), and the least that also lets it settle before the push (`settle`).
    """
    options = options or {}
    o = {**DEFAULT_EDIT, **options, 'speeds': {**DEFAULT_EDIT['speeds'], **(options.get('speeds') or {})}}
    duration = m['source']['duration']
    info = input_of(m)
    start_at = max(0, step['from'] if step.get('from') is not None else 0)
    to = min(duration, step['to'] if step.get('to') is not None else duration)
    hard = info['edited'] or step.get('to') is not None
    hold_until = step['holdUntil'] if step.get('holdUntil') is not None else INF

    def bounds(e: Event) -> Dict[str, float]:
        shot = shot_at(m, e['settle'], o['cutGuard'])
        return {'lo': max(start_at, shot['start']), 'hi': min(to, shot['end'])}

    # An event cut to the step's bounds; None when it lies wholly outside them.
    def clip(e: Event, keep: bool = False) -> Optional[Event]:
        if not keep and (e['settle'] < start_at or e['start'] > to):
            return None
        b = bounds({**e, 'settle': min(max(e['settle'], start_at), to)})
        start = min(max(e['start'], b['lo']), b['hi'])
        settle = min(max(e['settle'], start), b['hi'])
        return {**e, 'start': start, 'settle': settle}

    result = clip(event(m, step['result']), True)
    measured_settle = result['settle']
    if hard:
        result = {**result, 'settle': max(result['start'], min(measured_settle, bounds(result)['hi'] - o['postRoll'] - o['resultHold']))}
    # The result is always shown, whether or not `events` names it.
    chosen = [result if i == step['result'] else clip(event(m, i)) for i in dict.fromkeys([*step['events'], step['result']])]
    chosen = sorted((e for e in chosen if e), key=lambda e: e['start'])
    windows = []
    for e in chosen:
        b = bounds(e)
        windows.append({
            'srcIn': max(0, b['lo'], e['start'] - o['preRoll']),
            'srcOut': min(duration, b['hi'], hold_until, e['settle'] + o['postRoll']),
            'speed': o['speeds'][e['kind']],
            'role': 'event',
        })

    def cut_between(x: float, y: float) -> bool:
        return info['edited'] and any(c > x + 1e-6 and c <= y + 1e-6 for c in info['cuts'])

    # Overlapping windows merge; every source second plays at the slowest speed of the windows on it.
    merged: List[Dict[str, Any]] = []
    edges = sorted({x for w in windows for x in (w['srcIn'], w['srcOut'])})
    for a, b in zip(edges, edges[1:]):
        on = [w['speed'] for w in windows if w['srcIn'] <= a and b <= w['srcOut']]
        if not on:
            continue
        last = merged[-1] if merged else None
        if last is not None and last['srcOut'] == a and last['speed'] == min(on):
            last['srcOut'] = b
        else:
            merged.append({'srcIn': a, 'srcOut': b, 'speed': min(on), 'role': 'event'})

    pieces: List[Dict[str, Any]] = []
    jumped = 0
    for i, w in enumerate(merged):
        prev = merged[i - 1] if i > 0 else None
        if prev is not None:
            gap = w['srcIn'] - prev['srcOut']
            if gap > 0 and cut_between(prev['srcOut'], w['srcIn']):
                jumped += gap
            elif gap > 0 and gap <= o['pauseMax']:
                pieces.append({'srcIn': prev['srcOut'], 'srcOut': w['srcIn'], 'speed': 1, 'role': 'pause'})
            elif gap > 0 and gap / o['gapShown'] <= o['maxSpeed']:
                pieces.append({'srcIn': prev['srcOut'], 'srcOut': w['srcIn'], 'speed': gap / o['gapShown'], 'role': 'speedup'})
            elif gap > 0:
                jumped += gap
        if w['srcOut'] > w['srcIn']:
            pieces.append(w)

    # Hold the result: play on past its settle, slowing down if the recording ends first, the
    # next step starts (the same seconds shown twice read as a glitch), or its shot ends.
    hold_bounds = bounds(result)
    hi = hold_bounds['hi']
    hold_end = min(duration, hold_until, hi)
    before_hold = [p for p in pieces if p['srcOut'] <= hold_end]
    last_piece = before_hold[-1] if before_hold else None
    hold_from = max(last_piece['srcOut'] if last_piece is not None else result['settle'], result['settle'])
    hold_in, hold_out = hold_from, hold_from + min(hold_end - hold_from, o['resultHold'])
    if hold_out - hold_in < 0.05:
        # Too little source before the hard end: hold its last frames, never the seconds past it.
        hold_out = hold_end
        hold_in = max(0, hold_bounds['lo'], hold_end - 0.05)
    available = max(0, hold_out - hold_in)
    if last_piece is not None and hold_from > last_piece['srcOut']:
        last_piece['srcOut'] = hold_from
    # Reserve the hold's source once, in chronological order even when later shots are selected.
    reserved = []
    for p in pieces:
        if p['srcOut'] <= hold_in or p['srcIn'] >= hold_out:
            reserved.append(p)
        else:
            if p['srcIn'] < hold_in:
                reserved.append({**p, 'srcOut': hold_in})
            if p['srcOut'] > hold_out:
                reserved.append({**p, 'srcIn': hold_out})
    reserved.append({'srcIn': hold_in, 'srcOut': hold_out, 'speed': available / o['resultHold'], 'role': 'hold'})
    pieces = sorted(reserved, key=lambda p: p['srcIn'])

    # An extended piece can reach another shot. End each shot on its last analysed frame, and
    # resume past the cut guard.
    if info['edited']:
        split = []
        for p in pieces:
            start = p['srcIn']
            for cut in info['cuts']:
                if cut <= start or cut - 1 / m['analysis']['fps'] >= p['srcOut']:
                    continue
                end = min(p['srcOut'], cut - 1 / m['analysis']['fps'])
                if end > start:
                    split.append({**p, 'srcIn': start, 'srcOut': end})
                start = max(start, cut + o['cutGuard'])
            if start < p['srcOut'] - 1e-3:
                split.append({**p, 'srcIn': start})
            elif p['speed'] > 0 and step.get('_resultFrameEnd') is not None and abs(start - p['srcOut']) < 1e-6:
                # Reconciliation reserved this frame beyond its provisional trim, within
                # the user's hard bounds, and moved the neighbouring step past it.
                split.append({**p, 'srcIn': start, 'srcOut': step['_resultFrameEnd']})
        pieces = split

    # Contiguous pieces at one speed play as one clip.
    joined: List[Dict[str, Any]] = []
    for p in (x for x in pieces if x['srcOut'] - x['srcIn'] > 1e-3):
        last = joined[-1] if joined else None
        if last is not None and abs(last['srcOut'] - p['srcIn']) < 1e-6 and abs(last['speed'] - p['speed']) < 1e-6:
            last['srcOut'] = p['srcOut']
        else:
            joined.append({**p})

    t = 0
    timed: List[Piece] = []
    for p in joined:
        length = (p['srcOut'] - p['srcIn']) / p['speed']
        timed.append({'srcIn': round(p['srcIn'], 3), 'srcOut': round(p['srcOut'], 3), 'speed': floor_speed(p['speed'], 3), 'outIn': round(t, 3), 'outOut': round(t + length, 3), 'role': p['role']})
        t += length

    edit = StepEdit(id=step['id'], pieces=timed, duration=round(t, 3), resultAt=0, eventAt={}, jumped=round(jumped))
    _event_aliases(m, step, edit, o['cutGuard'])
    event_at: Dict[float, float] = {}
    for e in chosen:
        at = to_output(edit, e['start'])
        if at is not None:
            event_at[e['index']] = at
    edit['eventAt'] = _object_keys(event_at)
    result_at = to_output(edit, result['start'])
    if result_at is None:
        result_at = to_output(edit, result['settle'])
    edit['resultAt'] = 0 if result_at is None else result_at
    settle_at = to_output(edit, result['settle'])
    edit['settleAt'] = edit['resultAt'] if settle_at is None else settle_at
    edit['settle'] = round(measured_settle, 3)

    # Which hard end `hi` is, for the build's diagnostics, and the least `to` that would leave the
    # result its whole hold, and its settle too.
    r = event(m, step['result'])
    shot_end = shot_at(m, result['settle'], o['cutGuard'])['end']
    if info['edited'] and shot_end <= to + 1e-6 and shot_end < duration - 1e-6:
        end = 'shot'
    else:
        end = 'to' if to < duration - 1e-6 else 'recording'
    tail = o['postRoll'] + o['resultHold']
    edit['bounds'] = {
        'settles': r['settle'],
        'holdEnd': 'next_step' if hold_until < hi - 1e-6 else end,
        'leastTo': {'hold': round(max(start_at, shot_at(m, r['settle'], o['cutGuard'])['start'], r['start']) + tail, 3), 'settle': round(r['settle'] + tail, 3)},
    }
    if result['settle'] < r['settle'] - 1e-6:
        edit['bounds']['movedBy'] = end
    return edit


def floor_speed(v: float, places: int) -> float:
    """
    A piece's speed, rounded down, never up: a clip played faster than its length assumes runs out of
    trim before the length ends, and then one engine holds the last frame and the other wraps.
    """
    k = 10 ** places
    return math.floor(v * k + 1e-6) / k


def _object_keys(by_index: Dict[float, float]) -> Dict[str, float]:
    """A JavaScript object keyed by event index: its keys are strings, in ascending order."""
    return {number(k): by_index[k] for k in sorted(by_index)}


def to_output(edit: StepEdit, src: float) -> Optional[float]:
    """Map a source time (or an event's first safe frame); None when cut."""
    src = getattr(edit, 'source_aliases', {}).get(number(src), src)
    for p in edit['pieces']:
        if src >= p['srcIn'] - 1e-6 and src <= p['srcOut'] + 1e-6:
            return round(p['outIn'] + (src - p['srcIn']) / p['speed'], 3)
    return None


def _event_aliases(m: Moments, step: StepChoice, edit: StepEdit, guard: float) -> None:
    """A guard or reserved handoff maps an event to its first shown safe frame.

    This query metadata stays in process; the edit's JSON and eventAt describe playback.
    """
    edit.source_aliases = {}
    if input_of(m)['edited']:
        for i in dict.fromkeys([*step['events'], step['result']]):
            for src in (event(m, i)['start'], event(m, i)['settle']):
                for cut in input_of(m)['cuts']:
                    safe = round(cut + guard, 3)
                    if cut <= src < safe and to_output(edit, safe) is not None:
                        edit.source_aliases[number(src)] = safe
            # A reserved handoff frame can cover the beginning of an event that
            # continues into this step. It first appears when playback resumes.
            e = event(m, i)
            resume = step.get('from')
            if (step.get('_handoffFrom') is not None and resume is not None and
                    step['_handoffFrom'] <= e['start'] < resume <= e['settle'] and
                    to_output(edit, resume) is not None):
                edit.source_aliases[number(e['start'])] = resume


def fit_steps(m: Moments, steps: List[StepChoice], target: float, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Fit steps into a target length by trimming what the viewer loses least: sped-up gaps first, then
    the result holds down to `minHold`. Returns what is still over; the caller drops a step for that.
    """
    options = options or {}
    info = input_of(m)
    guard = options.get('cutGuard', CUT_GUARD)

    def at_guard_end(src: float) -> bool:
        return info['edited'] and any(abs(src - (c + guard)) < 1e-6 for c in info['cuts'])

    def on_guard(src: float) -> bool:
        return info['edited'] and any(c - 1e-6 <= src <= c + guard + 1e-6 for c in info['cuts'])

    def frame_end(src: float) -> float:
        return math.ceil((src + 1 / m['analysis']['fps']) * 1000 - 1e-6) / 1000

    def lead_of(edit: StepEdit) -> float:
        return edit['pieces'][0]['srcIn'] if edit['pieces'] else INF

    def shows_result(edit: StepEdit, s: StepChoice) -> bool:
        r = event(m, s['result'])
        return bool(edit['pieces']) and (to_output(edit, r['start']) is not None or to_output(edit, r['settle']) is not None)

    def keeps_events(before: StepEdit, after: StepEdit, s: StepChoice) -> bool:
        """A frame reservation must retain every event already shown in this step."""
        return all(not any(to_output(before, e[t]) is not None for t in ('start', 'settle')) or
                   any(to_output(after, e[t]) is not None for t in ('start', 'settle'))
                   for e in (event(m, j) for j in [*s['events'], s['result']]))

    def reconcile(strategy: str, retry: bool = False, blocked: Optional[Set[int]] = None) -> List[StepChoice]:
        """
        Steps with their `from` moved past the previous step where it would show the same seconds
        twice (a glitch), and each hold capped at a later step's lead-in. `result` reconciles only
        before the next result's start; `events` before the next step's first event, from the
        previous step's trimmed settle; `settle` also starts a next step that began before that
        settle just after the settle, unless that cuts its result, and then ends the previous step
        there.
        """
        lead_in: List[float] = []
        reconciled: List[StepChoice] = []
        planned: List[StepEdit] = []
        blocked = blocked or set()
        shifted: Set[int] = set()
        for i, s in enumerate(steps):
            edit = plan_step(m, s, options)
            lead = lead_of(edit)
            if planned:
                if strategy == 'result':
                    previous = event(m, reconciled[-1]['result'])['settle']
                    next_start = event(m, s['result'])['start']
                else:
                    previous = planned[-1]['settle']
                    lo = max(0, s.get('from') or 0)
                    hi = min(m['source']['duration'], s['to'] if s.get('to') is not None else INF)
                    selected = [event(m, j) for j in [*s['events'], s['result']]]
                    next_start = min(min(hi, max(lo, e['start'])) for e in selected
                                     if e['index'] == s['result'] or (e['settle'] >= lo and e['start'] <= hi))
                follows = event(m, s['result'])['start'] > event(m, reconciled[-1]['result'])['start']
                if lead <= previous < next_start:
                    # Keep a settled still before handing the source to the next action.
                    boundary = min(previous + 0.2, next_start - min(0.05, (next_start - previous) / 2))
                    s = {**s, 'from': max(s.get('from') or 0, boundary)}
                    edit = plan_step(m, s, options)
                    lead = lead_of(edit)
                elif strategy == 'settle' and follows and planned[-1]['pieces'] and lead < previous:
                    # Leave the next result's start, or its overlapping settle, in its own step.
                    result = event(m, s['result'])
                    available = min(edit['settle'], result['start']) if result['start'] > previous else edit['settle']
                    tail = min(0.2, max(0, (available - previous) / 2))
                    later = {**s, 'from': max(s.get('from') or 0, previous + tail)}
                    later_edit = plan_step(m, later, options)
                    earlier = {**reconciled[-1], 'to': min(reconciled[-1]['to'] if reconciled[-1].get('to') is not None else INF, lead)}
                    earlier_edit = plan_step(m, earlier, options)
                    safe_next = None
                    # A handoff at the guard's end leaves no safe frame for the earlier
                    # result. Reserve one analysed frame and hand the source over after it.
                    if to_output(earlier_edit, earlier_edit['settle']) is None:
                        if at_guard_end(lead):
                            boundary = frame_end(lead)
                            if boundary <= min(shot_at(m, lead, guard)['end'], steps[i - 1]['to'] if steps[i - 1].get('to') is not None else INF):
                                safe_earlier = {**earlier, '_resultFrameEnd': boundary}
                                next_choice = {**s, 'from': max(s.get('from') or 0, boundary), '_handoffFrom': lead}
                                safe_edit = plan_step(m, next_choice, options)
                                safe_earlier_edit = plan_step(m, safe_earlier, options)
                                if (shows_result(safe_edit, next_choice) and keeps_events(edit, safe_edit, s) and
                                        abs(lead_of(safe_earlier_edit) - lead_in[-1]) < 1e-6 and
                                        to_output(safe_earlier_edit, safe_earlier_edit['settle']) is not None):
                                    earlier = safe_earlier
                                    earlier_edit = safe_earlier_edit
                                    safe_next = next_choice
                                else:
                                    before_cut = {**earlier, 'to': round(lead - guard - 1 / m['analysis']['fps'], 3)}
                                    before_edit = plan_step(m, before_cut, options)
                                    if shows_result(before_edit, before_cut):
                                        earlier, earlier_edit = before_cut, before_edit
                    if i not in blocked and shows_result(dict(later_edit), later):
                        s, edit, lead = later, later_edit, lead_of(later_edit)
                        shifted.add(i)
                    elif earlier_edit['pieces'] and abs(lead_of(earlier_edit) - lead_in[-1]) < 1e-6 and (
                            to_output(earlier_edit, earlier_edit['settle']) is not None or
                            # Its settle falls on a cut guard and its trim leaves no frame past it:
                            # keep the trim when the result still plays.
                            (on_guard(earlier_edit['settle']) and shows_result(earlier_edit, earlier))):
                        reconciled[-1], planned[-1] = earlier, earlier_edit
                        # Commit both sides only when the earlier edit is accepted.
                        if safe_next is not None:
                            s, edit, lead = safe_next, safe_edit, lead_of(safe_edit)
                    elif retry and i - 1 in shifted:
                        # A moved start leaves no room to end this step before the next one.
                        # Reconcile it with its predecessor again, trimming the predecessor instead.
                        return reconcile(strategy, retry, blocked | {i - 1})
            # Normal reconciliation may already leave a legal result sliver.
            if at_guard_end(lead):
                for k, previous_step in enumerate(reconciled):
                    if event(m, previous_step['result'])['settle'] > lead + 1e-6:
                        continue
                    capped_choice = {**previous_step, 'holdUntil': min(previous_step.get('holdUntil', INF), lead)}
                    capped = plan_step(m, capped_choice, options)
                    if to_output(capped, capped['settle']) is None:
                        boundary = frame_end(lead)
                        # The reserved frame must stay inside the earlier step's shot and trim;
                        # otherwise keep the handoff as it is.
                        if boundary > min(shot_at(m, lead, guard)['end'], previous_step['to'] if previous_step.get('to') is not None else INF,
                                          steps[k]['to'] if steps[k].get('to') is not None else INF) + 1e-6:
                            break
                        safe_next = {**s, 'from': max(s.get('from') or 0, boundary)}
                        safe_edit = plan_step(m, safe_next, options)
                        if shows_result(safe_edit, safe_next) and keeps_events(edit, safe_edit, s):
                            s, edit, lead = safe_next, safe_edit, lead_of(safe_edit)
                            # Hold the earlier step up to the handoff, as it was, and give its
                            # result the reserved frame, so its progression before the cut stays.
                            reserved_choice = {**capped_choice, '_resultFrameEnd': boundary}
                            reserved = plan_step(m, reserved_choice, options)
                            if (to_output(reserved, reserved['settle']) is not None and keeps_events(planned[k], reserved, previous_step)
                                    and abs(lead_of(reserved) - lead_in[k]) < 1e-6):
                                reconciled[k], planned[k] = reserved_choice, reserved
                        break
            planned.append(edit)
            reconciled.append(s)
            lead_in.append(lead)
        bounded = []
        for i, s in enumerate(reconciled):
            settle = event(m, s['result'])['settle']
            later_leads = [t for j, t in enumerate(lead_in) if j != i and t >= settle]
            if later_leads:
                until = s['holdUntil'] if s.get('holdUntil') is not None else INF
                bounded.append({**s, 'holdUntil': js_min([until, *later_leads])})
            else:
                bounded.append(s)
        return bounded

    def shown_twice(edits: List[StepEdit]) -> float:
        return sum(max(0, min(p['srcOut'], q['srcOut']) - max(p['srcIn'], q['srcIn']))
                   for i, a in enumerate(edits) for b in edits[i + 1:] for p in a['pieces'] for q in b['pieces'])

    # Keep the gentlest reconciliation's results when it shows no source twice, and empty no
    # extra steps. Then prefer fewer seconds shown twice, followed by more events.
    base = None
    best = None
    for strategy, retry in (('result', False), ('events', False), ('settle', False), ('settle', True)):
        bounded = reconcile(strategy, retry)
        edits = [plan_step(m, s, options) for s in bounded]
        empty = {i for i, e in enumerate(edits) if not e['pieces']}
        twice = shown_twice(edits)
        shown = sum(len(e['eventAt']) for e in edits)
        # Judge results on played footage, as main does; a reserved result frame plays, and so
        # does the resumed frame after one.
        results = {i for i, (e, s, b) in enumerate(zip(edits, steps, bounded))
                   if shows_result(dict(e), s) or ((b.get('_resultFrameEnd') is not None or b.get('_handoffFrom') is not None)
                                                   and shows_result(e, s))}
        if base is None:
            base = (empty, twice, results)
        # Retrying a moved boundary must keep the selected edit's results and improve its overlap.
        if retry and not (empty <= best[2][0] and twice <= best[2][1] + 1e-6 and best[2][2] <= results):
            continue
        if empty <= base[0] and twice <= base[1] + 1e-6 and (base[1] > 1e-6 or base[2] <= results):
            key = (-round(twice, 2), shown)
            if best is None or key >= best[0]:
                best = (key, bounded, (empty, twice, results))
    bounded = best[1]

    late = {i for i, s in enumerate(steps)
            if any(event(m, later['result'])['settle'] < event(m, s['result'])['settle'] - 1e-6
                   for later in steps[i + 1:])}

    def plan(o: Dict[str, Any], recover: Set[int]) -> List[StepEdit]:
        fit_options = {**options, **o}
        edits = [plan_step(m, s, fit_options) for s in bounded]
        # Reconciliation can trim a result that settles after a later step's result. Keep all
        # planned footage, then append that result only in source seconds nobody already shows.
        # Use the user's bounds, rather than the provisional reconciliation trim, for this tail.
        for i, (s, edit) in enumerate(zip(steps, edits)):
            if i not in recover:
                continue
            result = event(m, s['result'])
            shot = shot_at(m, result['settle'], guard)
            start = max(result['settle'], shot['start'], s.get('from') or 0)
            end = min(shot['end'], s['to'] if s.get('to') is not None else INF,
                      s['holdUntil'] if s.get('holdUntil') is not None else INF)
            # Only recover the result in its own shot, within half a second of settling.
            if any(min(p['srcOut'], end, result['settle'] + 0.5) - max(p['srcIn'], start) > 1e-3
                   for p in edit['pieces']):
                continue
            occupied = sorted((p['srcIn'], p['srcOut']) for e in edits for p in e['pieces'])
            for lo, hi in occupied:
                if hi <= start:
                    continue
                if lo > start:
                    end = min(end, lo)
                    break
                start = hi
            if start >= min(end, result['settle'] + 0.5) - 1e-3:
                continue
            # Appending must jump forward; later selected footage is left as it was.
            if edit['pieces'] and start < edit['pieces'][-1]['srcOut']:
                continue
            tail = plan_step(m, {**s, 'events': [], 'from': start, 'to': end}, fit_options)
            if not tail['pieces']:
                continue
            offset = edit['duration']
            if edit['pieces']:
                edit['jumped'] = round(edit['jumped'] + start - edit['pieces'][-1]['srcOut'])
            edit['pieces'].extend({**p, 'outIn': round(offset + p['outIn'], 3),
                                   'outOut': round(offset + p['outOut'], 3)} for p in tail['pieces'])
            edit['duration'] = round(offset + tail['duration'], 3)
            edit['settle'], edit['bounds'] = tail['settle'], tail['bounds']
            if end < min(shot['end'], s['to'] if s.get('to') is not None else INF):
                edit['bounds']['holdEnd'] = 'next_step'
            _event_aliases(m, bounded[i], edit, guard)
            result_at = to_output(edit, result['start'])
            edit['resultAt'] = result_at if result_at is not None else round(offset + tail['resultAt'], 3)
            edit['settleAt'] = round(offset + tail['settleAt'], 3)
            for j in dict.fromkeys([*s['events'], s['result']]):
                at = to_output(edit, event(m, j)['start'])
                if at is not None:
                    edit['eventAt'][number(j)] = at
            if result_at is None:
                edit['eventAt'][number(s['result'])] = round(offset + tail['resultAt'], 3)
        return edits

    def length(edits: List[StepEdit]) -> float:
        return round(total(e['duration'] for e in edits), 3)

    def fit(recover: Set[int]) -> List[StepEdit]:
        edits = plan({}, recover)
        if length(edits) > target:
            edits = plan({'maxSpeed': 0}, recover)
        min_hold = options['minHold'] if options.get('minHold') is not None else 1.2
        hold = (options['resultHold'] if options.get('resultHold') is not None else DEFAULT_EDIT['resultHold']) - 0.2
        while length(edits) > target and hold >= min_hold - 1e-9:
            edits = plan({'maxSpeed': 0, 'resultHold': round(hold, 2)}, recover)
            hold -= 0.2
        return edits

    edits = fit(late)
    if late and length(edits) > target:
        # The no-recovery fit is the length ceiling when even it exceeds the target.
        # Retry tails individually, retaining earlier steps first. Refit each choice so
        # shortening holds and removing sped-up gaps always precede dropping a result.
        edits = fit(set())
        limit = max(target, length(edits))
        kept: Set[int] = set()
        for i in sorted(late):
            candidate = fit(kept | {i})
            if length(candidate) <= limit:
                edits = candidate
                kept.add(i)
    t = length(edits)
    return {'edits': edits, 'total': t, 'overBy': round(max(0, t - target), 3)}
