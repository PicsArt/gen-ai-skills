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


def _caption_segments(content: Dict[str, Any], assets: Dict[str, Any]) -> List[Tuple[Dict[str, Any], Dict[str, Any]]]:
    """Resolve caption styles and split stacked segments into visible runs."""
    preset = content.get('stylePreset')
    asset = assets.get(preset) if preset else None
    # A preset the scene declares lies under the content's style. A shipped one lives in the engine's
    # catalog, out of reach here, so the content's own style is read as before.
    declared = isinstance(asset, dict) and asset.get('type') == 'caption_style'
    definition = (asset.get('captionStyle') or {}) if declared else {}
    base = {**definition.get('style', {}), **(content.get('style') or {})}
    styles = {**definition.get('styles', {}), **(content.get('styles') or {})}
    tags = {**definition.get('tagStyles', {}), **(content.get('tagStyles') or {})}
    segments = (content.get('transcript') or {}).get('segments') or []
    result = []
    for index, seg in enumerate(segments):
        if not isinstance(seg, dict):
            continue
        style = dict(base)
        cycle = base.get('cycle') or []
        if cycle:
            style.update(styles.get(cycle[index % len(cycle)], {}))
        for tag in seg.get('tags') or []:
            style.update(styles.get(tags.get(tag, tag), {}))
        segment = dict(seg)
        hold = base.get('hold')
        if _num(hold) and hold > 0 and _num(seg.get('start')) and _num(seg.get('end')):
            next_starts = [s['start'] for s in segments if isinstance(s, dict) and _num(s.get('start')) and s['start'] > seg['start']]
            if next_starts:
                segment['end'] = max(seg['end'], min(min(next_starts), seg['end'] + hold))
        tokens = text_of(segment).split()
        marks = {i for i in (segment.get('emphasize') or []) if isinstance(i, int) and not isinstance(i, bool) and 0 <= i < len(tokens)}
        if not style.get('stacked') or not marks:
            result.append((segment, style, segment, False))
            continue
        words = segment.get('words') or []
        first = 0
        for last in range(1, len(tokens) + 1):
            if last < len(tokens) and (last in marks) == (first in marks):
                continue
            stressed = first in marks
            slot = style.get('emphasized') or {}
            if (slot.get('visible', True) if stressed else style.get('visible', True)) is not False:
                run = {**segment, 'text': ' '.join(tokens[first:last]), 'words': words[first:last]}
                run_style = dict(style)
                if stressed:
                    if 'reveal' in slot:
                        run_style['reveal'] = slot['reveal']
                    if first < len(words) and isinstance(words[first], dict) and _num(words[first].get('start')):
                        lead = slot.get('lead', 0)
                        run['start'] = max(segment['start'], words[first]['start'] - (lead if _num(lead) else 0))
                result.append((run, run_style, segment, True))
            first = last
    return result


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
                # A stacked segment's runs are one line read in its authored order: they sort together,
                # at the first run's time, and only the first starts the line (checklist.says).
                groups: Dict[int, int] = {}
                for segment, style, source, split in _caption_segments(content, getattr(layer, 'assets', {})):
                    reveal = style.get('reveal')
                    needs_words = completed and isinstance(reveal, dict) and reveal.get('window', 'sustain') == 'sustain'
                    if needs_words and not segment.get('words'):
                        continue
                    # caption_blocks treats the presence of reveal as enabled.
                    display_style = {k: v for k, v in style.items() if k != 'reveal' or v is not False}
                    display = {**content, 'style': display_style, 'transcript': {'segments': [segment]}}
                    for index, (a, b, words) in enumerate(caption_blocks(display, start)):
                        a, b = start + (a - start) * rate, start + (b - start) * rate
                        a, b = max(a, at), min(b, end)
                        if b > a + 1e-6:
                            group = groups.setdefault(id(source), len(out)) if split else len(out)
                            out.append({'at': round(a, 3), 'end': b, 'layer': lid, 'kind': 'captions', 'words': words,
                                        'context': text_of(source), 'context_first': index == 0 and group == len(out),
                                        '_group': group})
                continue
            out.append({'at': round(at, 3), 'end': end, 'layer': lid, 'kind': content['kind'], 'words': text_of(content),
                        'reveal_start': start, 'typing': max(0.0, typed or 0) * rate, '_group': len(out)})
    first_at: Dict[int, float] = {}
    for b in out:
        first_at[b['_group']] = min(first_at.get(b['_group'], b['at']), b['at'])
    # Stable: a group keeps its authored order.
    out.sort(key=lambda b: first_at[b['_group']])
    for b in out:
        del b['_group']
    return out


def _blocks(scene: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [b for b in word_blocks(scene, ('text', 'captions')) if b['words']]
