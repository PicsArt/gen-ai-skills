"""
A timelapse's stages and its stepped edit: the part of the screen tools' `stages.ts` the builder
uses. The stages a spec's chapters get depend on the spec, so the moments cannot carry them.
"""
from __future__ import annotations

import math
from typing import Any, Dict, List, Optional

from _geometry import round
from _js import math_round, total

Stage = Dict[str, float]


def chapter_stages(chapters: List[float], to: float, count: float, minimum: int = 2) -> List[Stage]:
    """
    Stages allotted per chapter: each named chapter [from_i, from_i+1) gets at least `minimum`
    stages, so its label stays up long enough to read, and the rest of `count` is shared by chapter
    length.
    """
    bounds = [*chapters, to]
    lengths = [max(0, bounds[i + 1] - c) for i, c in enumerate(chapters)]
    weights = lengths if total(lengths) else [1 for _ in chapters]
    whole = total(weights) or 1
    remaining = max(0, math_round(count) - minimum * len(chapters))
    shares = [remaining * length / whole for length in weights]
    slots = [int(share) for share in shares]
    order = sorted(range(len(chapters)), key=lambda i: shares[i] - slots[i], reverse=True)
    for i in order[:remaining - sum(slots)]:
        slots[i] += 1
    out: List[Stage] = []
    for i, start in enumerate(chapters):
        n = minimum + slots[i]
        step = lengths[i] / n
        for k in range(int(n)):
            out.append({'t': round(start + step * (k + 0.5), 2), 'novelty': 0})
    return out


def plan_timelapse(
    stages: List[Stage],
    duration: float,
    shown: Optional[float] = None,
    speed: Optional[float] = None,
    hold: Optional[float] = None,
    hold_last: Optional[bool] = None,
    cuts: Optional[List[float]] = None,
    fps: Optional[float] = None,
    start: Optional[float] = None,
) -> Dict[str, Any]:
    """
    A stepped timelapse: each stage plays `shown` output seconds at `speed`, centred on the stage,
    with a jump cut to the next. With `hold_last`, the last stage plays at 1x and holds, because it
    is the result.

    `cuts` (source seconds, as analysed at `fps`): a stage window stays inside the stage's shot,
    moved off a cut or shortened to the shot, so a piece never shows a cut inside itself: the jump
    between pieces is the only cut a timelapse has.

    `start` and `duration` bound every window: a process shows nothing before its `from` or after its
    `to`, the result's reveal.
    """
    shown = 0.7 if shown is None else shown
    speed = 6 if speed is None else speed
    hold = 2.2 if hold is None else hold
    hold_last = True if hold_last is None else hold_last
    frame = 1 / (10 if fps is None else fps)
    cuts = [] if cuts is None else cuts
    start = 0 if start is None else math.ceil(max(0, start) * 1000 - 1e-6) / 1000
    # Source windows are rounded to milliseconds; rounding must not extend the recording.
    duration = math.floor(duration * 1000) / 1000
    pieces: List[Dict[str, Any]] = []
    t = 0
    for i, s in enumerate(stages):
        last = hold_last and i == len(stages) - 1
        length = hold if last else shown
        v = 1 if last else speed
        window = length * v
        # The stage's shot: from just after the cut before it to the frame before the cut after it.
        before = [c for c in cuts if c <= s['t'] + 1e-6]
        after = next((c for c in cuts if c > s['t'] + 1e-6), None)
        lo = start if last or not before else max(start, before[-1] + 0.04)
        hi = duration if last or after is None else after - frame
        src_in = max(start, duration - window - 0.05) if last else s['t'] - window / 2
        src_in = min(max(lo, src_in), max(lo, min(hi, duration) - window))
        # Stages closer than a window share the seconds between them: each plays up to the midpoint
        # with the next, from where the last piece stopped, slowed to keep its output length. No
        # second plays twice and stages with usable source are kept.
        nxt = None if last or i + 1 >= len(stages) else stages[i + 1]['t']
        cap = hi if nxt is None else min(hi, (s['t'] + nxt) / 2)
        # Reserve a millisecond for each later stage in this shot, even beside a cut's guard.
        remaining = sum(1 for later in stages[i + 1:] if after is None or later['t'] < after - 1e-6)
        hi = min(hi, duration)
        previous = pieces[-1]['srcOut'] if pieces else start
        cap = min(hi - remaining * 0.001, max(cap, max(lo, previous) + 0.001))
        src_in = max(lo, min(src_in, cap - 0.001))
        if pieces and src_in < pieces[-1]['srcOut']:
            src_in = pieces[-1]['srcOut']
        src_out = min(duration, hi, src_in + window, max(cap, src_in))
        # A cut's guard can leave no source for this stage; never borrow it before the lower bound.
        if round(src_out, 3) <= round(src_in, 3):
            continue
        if src_out - src_in < window - 1e-9 and not last:
            v = max(1, (src_out - src_in) / length)
        actual = (src_out - src_in) / v
        pieces.append({'srcIn': round(src_in, 3), 'srcOut': round(src_out, 3), 'speed': round(v, 4), 'outIn': round(t, 3), 'outOut': round(t + actual, 3), 'stage': i})
        t += actual
    return {'pieces': pieces, 'duration': round(t, 3)}
