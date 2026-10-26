"""
Shots and the push: the part of the screen tools' `steps.ts` the builder reads. The steps
themselves come proposed in the moments, so nothing here proposes one.
"""
from __future__ import annotations

from typing import Dict

from _geometry import round
from _moments import Moments, input_of
from zoom import DEFAULT_ZOOM

# The push onto a result, source seconds: it starts `delay` after the result settles and ramps for
# `ramp`. Both are the screen-recording-zoom skill's house zoom, `DEFAULT_ZOOM` in its `zoom.py`.
PUSH = {'delay': DEFAULT_ZOOM['delay'], 'ramp': DEFAULT_ZOOM['ramp']}

# The shortest shot the moments propose as a step, source seconds: the push onto its result takes
# this long.
MIN_SHOT = PUSH['delay'] + PUSH['ramp']

# Source seconds kept clear after a cut, so a trim at the cut never shows the shot before: the
# analysed frame at the cut is already the new shot, but the source frame there may not be.
CUT_GUARD = 0.04


def shot_at(m: Moments, t: float, guard: float = CUT_GUARD) -> Dict[str, float]:
    """
    The shot around source second `t` of an edited input: from just after the cut before it to the
    last analysed frame before the cut after it. The whole recording when the input is raw.
    """
    info = input_of(m)
    if not info['edited']:
        return {'start': 0, 'end': m['source']['duration']}
    before = [c for c in info['cuts'] if c <= t + 1e-6]
    after = next((c for c in info['cuts'] if c > t + 1e-6), None)
    start = before[-1] + guard if before else 0
    end = after - 1 / m['analysis']['fps'] if after is not None else m['source']['duration']
    return {'start': round(start, 3), 'end': round(max(start, end), 3)}
