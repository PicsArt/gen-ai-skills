"""
The moments: the result of `picsart_media_screen_moments`, as it returned it. The recording's activity
(`source`, `analysis`, `events`, `dead`, `content`, `work`), what the input is (`input`), the tier
it suggests (`tier`, `tierReason`) and the proposed steps (`steps`, each with its `subject` when
one was found).

The builder reads them and never recomputes them: the tool decoded the recording, and this script
cannot. Field names are the tool's, so the builder's code reads like the screen tools' TypeScript.
"""
from __future__ import annotations

import math
from typing import Any, Dict

from _js import number

Moments = Dict[str, Any]
Event = Dict[str, Any]

EVENT_KINDS = ('cut', 'scroll', 'reveal', 'progressive')


def input_of(m: Moments) -> Dict[str, Any]:
    """What the input is: `width`, `height`, `orientation`, `edited`, `cutsPerMinute`, `cuts`, `hasAudio`."""
    return m['input']


def index(i: float, length: int, what: str) -> int:
    """`i` as a list index. JavaScript reads a missing entry as undefined and fails later; this fails here."""
    numeric = isinstance(i, (int, float)) and not isinstance(i, bool)
    if numeric and math.isfinite(i) and i == int(i) and 0 <= i < length:
        return int(i)
    raise ValueError(f'no {what} {number(i) if numeric else repr(i)} (there are {length})')


def event(m: Moments, i: float) -> Event:
    """Event `i` of the recording: `events[i].index` is `i`."""
    return m['events'][index(i, len(m['events']), 'event')]
