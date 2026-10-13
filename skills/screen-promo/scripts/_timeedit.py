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
- `settleAt`: where the result settles, where the push onto it starts;
- `settle`: the source second it settles at, after the step's bounds: the hook's and the grid's
  frame is taken just after it;
- `bounds`: how the step's hard ends bound its result (see `plan_step`).
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from _geometry import round
from _js import INF, js_min, number, total
from _moments import Event, Moments, event, input_of
from _steps import CUT_GUARD, shot_at

Piece = Dict[str, Any]
StepEdit = Dict[str, Any]
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
    gap with a cut in it is jumped. A hard end also moves the result's settle back far enough for the
    hold to play at 1x before it, instead of freezing on the shot's last frame. `bounds` says which
    end did that, and which ended the hold:
    - `settles`: where the result really settles;
    - `movedBy`: the hard end (`to`, `shot` or `recording`) that moved the edit's settle before it;
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
        if e['index'] == step['result'] and hard:
            settle = max(start, min(settle, b['hi'] - o['postRoll'] - o['resultHold']))
        return {**e, 'start': start, 'settle': settle}

    result = clip(event(m, step['result']), True)
    chosen = [result if i == step['result'] else clip(event(m, i)) for i in dict.fromkeys(step['events'])]
    chosen = sorted((e for e in chosen if e), key=lambda e: e['start'])
    windows = []
    for e in chosen:
        b = bounds(e)
        windows.append({
            'srcIn': max(0, b['lo'], e['start'] - o['preRoll']),
            'srcOut': min(duration, b['hi'], e['settle'] + o['postRoll']),
            'speed': o['speeds'][e['kind']],
            'role': 'event',
        })

    def cut_between(x: float, y: float) -> bool:
        return info['edited'] and any(c > x + 1e-6 and c <= y + 1e-6 for c in info['cuts'])

    # Overlapping windows merge; the overlap plays at the slower of the two speeds.
    merged: List[Dict[str, Any]] = []
    for w in windows:
        last = merged[-1] if merged else None
        if last is not None and w['srcIn'] <= last['srcOut']:
            if w['speed'] == last['speed']:
                last['srcOut'] = max(last['srcOut'], w['srcOut'])
            elif w['speed'] < last['speed']:
                last['srcOut'] = w['srcIn']
                merged.append({**w})
            elif w['srcOut'] > last['srcOut']:
                merged.append({**w, 'srcIn': last['srcOut']})
        else:
            merged.append({**w})

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
    last_piece = pieces[-1] if pieces else None
    hold_from = max(last_piece['srcOut'] if last_piece is not None else result['settle'], result['settle'])
    hi = bounds(result)['hi']
    hold_end = min(duration, hold_until, hi)
    available = max(0.05, min(hold_end - hold_from, o['resultHold']))
    if last_piece is not None and hold_from > last_piece['srcOut']:
        last_piece['srcOut'] = hold_from
    pieces.append({'srcIn': hold_from, 'srcOut': hold_from + available, 'speed': available / o['resultHold'], 'role': 'hold'})

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
        timed.append({'srcIn': round(p['srcIn'], 3), 'srcOut': round(p['srcOut'], 3), 'speed': round(p['speed'], 3), 'outIn': round(t, 3), 'outOut': round(t + length, 3), 'role': p['role']})
        t += length

    edit: StepEdit = {'id': step['id'], 'pieces': timed, 'duration': round(t, 3), 'resultAt': 0, 'eventAt': {}, 'jumped': round(jumped)}
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
    edit['settle'] = round(result['settle'], 3)

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


def _object_keys(by_index: Dict[float, float]) -> Dict[str, float]:
    """A JavaScript object keyed by event index: its keys are strings, in ascending order."""
    return {number(k): by_index[k] for k in sorted(by_index)}


def to_output(edit: StepEdit, src: float) -> Optional[float]:
    """Map a source time to step-relative output time; None when the time was cut."""
    for p in edit['pieces']:
        if src >= p['srcIn'] - 1e-6 and src <= p['srcOut'] + 1e-6:
            return round(p['outIn'] + (src - p['srcIn']) / p['speed'], 3)
    return None


def fit_steps(m: Moments, steps: List[StepChoice], target: float, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Fit steps into a target length by trimming what the viewer loses least: sped-up gaps first, then
    the result holds down to `minHold`. Returns what is still over; the caller drops a step for that.
    """
    options = options or {}
    # Where each step starts showing the recording, after its bounds and shots.
    lead_in = []
    for s in steps:
        pieces = plan_step(m, s, options)['pieces']
        lead_in.append(pieces[0]['srcIn'] if pieces else INF)
    bounded = []
    for i, s in enumerate(steps):
        settle = event(m, s['result'])['settle']
        later = [t for j, t in enumerate(lead_in) if j != i and t > settle]
        if later:
            until = s['holdUntil'] if s.get('holdUntil') is not None else INF
            bounded.append({**s, 'holdUntil': js_min([until, *later])})
        else:
            bounded.append(s)

    def plan(o: Dict[str, Any]) -> List[StepEdit]:
        return [plan_step(m, s, {**options, **o}) for s in bounded]

    def length(edits: List[StepEdit]) -> float:
        return round(total(e['duration'] for e in edits), 3)

    edits = plan({})
    if length(edits) > target:
        edits = plan({'maxSpeed': 0})
    min_hold = options['minHold'] if options.get('minHold') is not None else 1.2
    hold = (options['resultHold'] if options.get('resultHold') is not None else DEFAULT_EDIT['resultHold']) - 0.2
    while length(edits) > target and hold >= min_hold - 1e-9:
        edits = plan({'maxSpeed': 0, 'resultHold': round(hold, 2)})
        hold -= 0.2
    t = length(edits)
    return {'edits': edits, 'total': t, 'overBy': round(max(0, t - target), 3)}
