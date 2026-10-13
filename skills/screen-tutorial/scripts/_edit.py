"""
The tutorial's time edit: which source seconds each step plays, how fast, and how long it holds.

A tutorial keeps every step and gives the viewer time to follow it. So, unlike a promo, a step is
never squeezed to fit a target: it plays its actions, holds the response, then zooms back out.

A step's edit is `{pieces, duration, holdAt, holdEnd, at, wait?, srcStart, srcEnd}`:
- `pieces`, played back to back: `{srcIn, srcOut, speed, outIn, outOut, role}`, role `event`,
  `pause`, `speedup`, `wait` or `hold`, the out times step-relative;
- `at`, each action's start in step output seconds, by action index;
- `holdAt` and `holdEnd`: where the hold starts and ends (then the zoom out plays);
- `wait`: the real length of a wait shown as a sped beat, in the recording, so the voice can say it;
- `srcStart`, `srcEnd`: the source seconds the step spans, which the next step never shows again;
- `spans`: the user's speech ran over this step's action, so it played in the step before.

The numbers below are the tutorial's pacing rules (references/outline.md, Pacing).
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from framing import round

# pre: source seconds before a step's first action, at 1x: the push starts 0.5 s before the
# action, after a moment at rest. preRoll and postRoll: around each later action. hold: output
# seconds the response holds with no voice line (a starting number, no source). zoomOut: the ramp
# back to rest after the hold. pauseMax: a gap played at 1x; gapShown: a longer one sped to this,
# unless that needs more than maxSpeed, and then it is cut. waitShown: a wait the user will also
# face, as a sped beat. lineTail: output seconds after a voice line ends before the step may end.
EDIT: Dict[str, Any] = {
    'pre': 0.8,
    'preRoll': 0.3,
    'postRoll': 0.3,
    'hold': 1.5,
    'zoomOut': 1.0,
    'pauseMax': 0.5,
    'gapShown': 0.4,
    'maxSpeed': 6,
    'waitShown': 0.8,
    'lineTail': 0.3,
    'speeds': {'cut': 1, 'reveal': 1, 'scroll': 1.5, 'typing': 2, 'progressive': 2},
}


def _merge(windows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Overlapping windows join; the joined window plays at the slower speed."""
    out: List[Dict[str, Any]] = []
    for w in sorted(windows, key=lambda x: x['srcIn']):
        last = out[-1] if out else None
        if last is not None and w['srcIn'] <= last['srcOut'] + 1e-9:
            last['srcOut'] = max(last['srcOut'], w['srcOut'])
            last['speed'] = min(last['speed'], w['speed'])
        else:
            out.append(dict(w))
    return out


def plan_step(actions: List[Dict[str, Any]], step: Dict[str, Any], lo: float, hi: float, dead: List[Dict[str, Any]], speech: List[Dict[str, float]], line: Optional[float]) -> Dict[str, Any]:
    """
    One step, inside its source region `[lo, hi]`: its actions' windows, every span of the user's
    own voice that starts in the region whole at 1x, the gaps between them paused, sped or cut, a
    wait shown when the step asks for it, then the hold. With `line`, the voice line's length, the
    hold grows until the step outlasts the line.
    """
    o = EDIT
    windows: List[Dict[str, Any]] = []
    for k, a in enumerate(actions):
        kind = a['kind']
        speed = 1 if (kind in ('typing', 'progressive') and step.get('typed')) else o['speeds'][kind]
        lead = o['pre'] if k == 0 else o['preRoll']
        windows.append({'srcIn': min(hi, max(lo, a['at'] - lead)), 'srcOut': min(hi, max(lo, a['settle'] + o['postRoll'])), 'speed': speed, 'role': 'event'})
    voiced = [{'srcIn': max(lo, sp['start']), 'srcOut': min(hi, sp['end']), 'speed': 1, 'role': 'event'} for sp in speech if sp['start'] >= lo - 1e-6 and sp['start'] < hi - 1e-6]
    windows = _merge([w for w in windows + voiced if w['srcOut'] > w['srcIn'] + 1e-9]) or [{'srcIn': lo, 'srcOut': min(hi, lo + 0.1), 'speed': 1, 'role': 'event'}]
    settle = min(hi, max(a['settle'] for a in actions))
    wait = None
    if step.get('wait'):
        after = next((d for d in dead if d['kind'] == 'waiting' and d['start'] >= settle - 0.5 and d['start'] <= settle + 1.0), None)
        if after is not None and not any(sp['start'] < after['end'] and sp['end'] > after['start'] for sp in speech):
            wait = {'srcIn': max(after['start'], lo), 'srcOut': min(after['end'], hi), 'real': after['end'] - after['start']}

    pieces: List[Dict[str, Any]] = []
    for i, w in enumerate(windows):
        if i > 0:
            prev = windows[i - 1]
            gap = w['srcIn'] - prev['srcOut']
            if gap > 1e-9 and gap <= o['pauseMax']:
                pieces.append({'srcIn': prev['srcOut'], 'srcOut': w['srcIn'], 'speed': 1, 'role': 'pause'})
            elif gap > 1e-9 and gap / o['gapShown'] <= o['maxSpeed']:
                pieces.append({'srcIn': prev['srcOut'], 'srcOut': w['srcIn'], 'speed': gap / o['gapShown'], 'role': 'speedup'})
        pieces.append(dict(w))
    hold_from = max(pieces[-1]['srcOut'], settle)
    if hold_from > pieces[-1]['srcOut']:
        pieces[-1]['srcOut'] = hold_from
    wait_length = None
    if wait is not None and wait['srcOut'] > hold_from + 1e-9:
        start = max(wait['srcIn'], hold_from)
        if start > hold_from + 1e-9:
            pieces.append({'srcIn': hold_from, 'srcOut': start, 'speed': 1, 'role': 'pause'})
        wait_length = wait['real']
        pieces.append({'srcIn': start, 'srcOut': wait['srcOut'], 'speed': max(1, (wait['srcOut'] - start) / o['waitShown']), 'role': 'wait'})
        hold_from = wait['srcOut']

    played = 0.0
    for p in pieces:
        played += (p['srcOut'] - p['srcIn']) / p['speed']
    hold = o['hold']
    if line is not None:
        hold = max(hold, line + o['lineTail'] - played - o['zoomOut'])
    out_len = hold + o['zoomOut']
    # The hold plays on from the settle at 1x while the region allows: the next step's first second
    # is never shown twice. With less, it slows to a near freeze on the settled frame.
    available = max(0.05, min(hi - hold_from, out_len))
    # A near freeze holds the settled frame itself, even when the region ends there.
    hold_in = max(0.0, min(hold_from, src_end(hi, hold_from, available)))
    pieces.append({'srcIn': hold_in, 'srcOut': hold_in + available, 'speed': available / out_len, 'role': 'hold'})

    t = 0.0
    timed: List[Dict[str, Any]] = []
    for p in pieces:
        if p['srcOut'] - p['srcIn'] <= 1e-6:
            continue
        length = (p['srcOut'] - p['srcIn']) / p['speed']
        timed.append({'srcIn': round(p['srcIn'], 3), 'srcOut': round(p['srcOut'], 3), 'speed': round(p['speed'], 4), 'outIn': round(t, 3), 'outOut': round(t + length, 3), 'role': p['role']})
        t += length
    edit = {'pieces': timed, 'duration': round(t, 3), 'holdEnd': round(t - o['zoomOut'], 3)}
    edit['holdAt'] = round(edit['holdEnd'] - hold, 3)
    edit['at'] = {str(a['index']): _first_output(timed, a['at']) for a in actions}
    if wait_length is not None:
        edit['wait'] = round(wait_length, 1)
    edit['srcStart'] = timed[0]['srcIn']
    edit['srcEnd'] = timed[-1]['srcOut']
    return edit


def src_end(hi: float, hold_from: float, available: float) -> float:
    """Where the hold may start: its settled frame, unless that runs it past the region's end by more than a near freeze."""
    return hold_from if hold_from + available <= hi + 0.05 + 1e-9 else hi - available


def _first_output(pieces: List[Dict[str, Any]], src: float) -> float:
    """A source second's step-relative output time; one cut away is the next second shown."""
    for p in pieces:
        if src <= p['srcOut'] + 1e-6:
            s = max(src, p['srcIn'])
            return round(p['outIn'] + (s - p['srcIn']) / p['speed'], 3)
    return pieces[-1]['outOut']


def regions(actions: List[Dict[str, Any]], steps: List[Dict[str, Any]], src_end: float, speech: List[Dict[str, float]]) -> List[Dict[str, Any]]:
    """
    The source each step may show, back to back: from just before its first action to the next
    step's start. A start that falls inside the user's speech moves to where the speech starts,
    when the step before has settled by then; otherwise past the speech, and the step's action
    then plays in the step before (`spans`), at 1x under the voice.
    """
    o = EDIT
    starts: List[float] = []
    spans: List[bool] = []
    for k, s in enumerate(steps):
        acts = [actions[i] for i in s['actions']]
        at = acts[0]['at']
        start = max(0.0, at - o['pre'])
        span = False
        if k > 0:
            before = [actions[i] for i in steps[k - 1]['actions']]
            settled = max(a['settle'] for a in before)
            start = min(max(start, settled + o['postRoll']), at)
            inside = next((sp for sp in speech if sp['start'] < start - 1e-6 and sp['end'] > start + 1e-6), None)
            if inside is not None:
                if inside['start'] >= settled - 1e-6:
                    start = inside['start']
                else:
                    start = inside['end']
                    span = start > at + 1e-6
            start = max(start, starts[-1])
        else:
            inside = next((sp for sp in speech if sp['start'] < start - 1e-6 and sp['end'] > start + 1e-6), None)
            if inside is not None:
                start = inside['start']
        starts.append(start)
        spans.append(span)
    return [{'lo': starts[k], 'hi': starts[k + 1] if k + 1 < len(starts) else src_end, 'spans': spans[k]} for k in range(len(starts))]


def plan(actions: List[Dict[str, Any]], steps: List[Dict[str, Any]], src_end: float, dead: List[Dict[str, Any]], speech: List[Dict[str, float]], lines: Dict[str, float]) -> List[Dict[str, Any]]:
    """Every step's edit, in order, each inside its own region of the recording."""
    edits = []
    for s, r in zip(steps, regions(actions, steps, src_end, speech)):
        edit = plan_step([actions[i] for i in s['actions']], s, r['lo'], r['hi'], dead, speech, lines.get(s['id']))
        if r['spans']:
            edit['spans'] = True
        edits.append(edit)
    return edits
