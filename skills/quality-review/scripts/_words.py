"""
The words a built scene puts on screen, and when: every block of text or captions while its layer
is shown, nested scenes' and track clips' included, on the outer scene's clock.

A private module: `scripts/checklist.py` and `scripts/critics.py` import it. Python 3.9 or later, the standard
library only, offline.
"""
from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Tuple

from timing import _visits, caption_blocks, scene_duration, shown, text_of, typing_time


def _num(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _duration(scene: Dict[str, Any]) -> Optional[float]:
    return scene_duration(scene)


def _last(scene: Dict[str, Any], duration: float) -> float:
    """The last frame's time: a sample at the very end of the scene is past it."""
    fps = (scene.get('composition') or {}).get('fps')
    step = 1.0 / float(fps) if _num(fps) and fps > 0 else 1 / 30
    return round(max(0.0, duration - step), 3)


def word_blocks(scene: Dict[str, Any], kinds: Tuple[str, ...] = ('text',), completed: bool = True) -> List[Dict[str, Any]]:
    """
    Every block of words while it is on screen, in the order it appears: nested scenes' and track
    clips' included, on the outer scene's clock, and once per span its opacity shows it.
    With `completed` false, typed blocks count from the start of their reveal.
    """
    out = []
    for layer, start, zero, bound in _visits(scene, 0.0, math.inf, set(), words_only=True):
        content = layer.get('content') or {}
        rate = getattr(layer, 'rate', 1.0)
        if content.get('kind') not in kinds:
            continue
        for at, end in shown(layer, start, zero):
            # A layer with no `duration` shows until its scene ends, not forever.
            end = min(end, bound)
            typed = typing_time(content)
            if typed is not None and completed:
                # Count the whole block only after its typewriter reveal has finished.
                at = max(at, start + max(0.0, typed) * rate)
            if end <= at + 1e-6:
                continue
            lid = str(layer.get('id', ''))
            if content['kind'] == 'captions':
                # A caption's words are its transcript's segments, each on screen only while it is said.
                style = content.get('style') or {}
                needs_words = completed and 'reveal' in style and style['reveal'].get('window', 'sustain') == 'sustain'
                for segment in (content.get('transcript') or {}).get('segments') or []:
                    if needs_words and not segment.get('words'):
                        continue
                    display = {**content, 'transcript': {'segments': [segment]}}
                    for index, (a, b, words) in enumerate(caption_blocks(display, start)):
                        a, b = start + (a - start) * rate, start + (b - start) * rate
                        a, b = max(a, at), min(b, end)
                        if b > a + 1e-6:
                            out.append({'at': round(a, 3), 'end': b, 'layer': lid, 'kind': 'captions',
                                        'words': words, 'context': text_of(segment), 'context_first': index == 0})
                continue
            out.append({'at': round(at, 3), 'end': end, 'layer': lid, 'kind': content['kind'], 'words': text_of(content),
                        'reveal_start': start, 'typing': max(0.0, typed or 0) * rate})
    return sorted(out, key=lambda b: b['at'])


def _blocks(scene: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [b for b in word_blocks(scene, ('text', 'captions')) if b['words']]
