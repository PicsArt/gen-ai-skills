#!/usr/bin/env python3
"""
Lint a scene's timing from its JSON: every block of words held long enough to read, short enough
to read at a glance, and no long stretch where nothing on screen changes.

    python3 scripts/timing.py input.json
    python3 scripts/timing.py < input.json

The input is one JSON object:

    {"scene": {...}, "labels": ["s1_label"], "changes": [4.2, 9.8]}

- `scene`: the scene (a builder's whole output is read too, and its `timeline`'s beats count as
  changes).
- `labels`, optional: the ids of the step labels, the short lines that name a step. Without it,
  a text layer whose id ends in `_label` or `_line` (a digit may follow) is one.
- `changes`, optional: more moments the picture changes, in scene seconds, that the JSON does not
  show: a measured reveal inside a clip, a cut inside the recording.

The rules:

- **Readable holds**: a block of words stays on screen at least 0.3 s per word, and never under
  1 s. A typed block adds its typing time.
- **Short blocks**: at most 10 words in a block, and at most 6 in a step label. A typed request
  is the user's own words, so it has no cap.
- **No dead air**: nothing goes more than 8 s without a change on screen: a layer in or out, a
  keyframed move (all the time it moves, not only its ends), a beat, or one of `changes`. Sound
  is not a change: an audio layer or a `volume` fade counts for nothing.

A layer inside a nested scene counts at its time in the scene, and a track's clips each at its
time in the track. A hold is what the viewer sees: a layer is cut at the end of its composition
and of every scene around it.

It prints one JSON line, `{ok, findings}`; `ok` is true when there is none. Each finding has a
`code` (`short_hold`, `too_many_words` or `dead_air`), the `layer` or the `from`-`to` range, a
`message` and a `fix`. Input it cannot read exits 1, with one line on stderr that says what is
wrong.

Python 3.9 or later, the standard library only, offline.
"""
from __future__ import annotations

import json
import math
import re
import sys
from typing import Any, Dict, Iterator, List, Optional, Set, Tuple

PER_WORD = 0.3
MIN_HOLD = 1.0
MAX_WORDS = 10
MAX_LABEL_WORDS = 6
DEAD_AIR = 8.0
LABEL = re.compile(r'_(label|line)\d*$')

USAGE = 'usage: timing.py [input.json]; with no file, the input is read from stdin'


class InputError(ValueError):
    """Input the script cannot read, with the reason."""


def _num(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def word_count(content: Dict[str, Any]) -> int:
    t = content.get('text')
    s = ' '.join(t) if isinstance(t, list) else (t if isinstance(t, str) else '')
    return len(re.findall(r'\S+', s))


def typing_time(content: Dict[str, Any]) -> Optional[float]:
    for a in content.get('animations') or []:
        if isinstance(a, dict) and a.get('preset') == 'typewriter':
            d = (a.get('params') or {}).get('duration')
            return float(d) if _num(d) else 1.0
    return None


def _assets(scene: Dict[str, Any]) -> Dict[str, Any]:
    declared = scene.get('assets') or []
    # The builders key assets by id; a list of assets with ids is read too.
    if isinstance(declared, dict):
        return {k: a for k, a in declared.items() if isinstance(a, dict)}
    return {a.get('id'): a for a in declared if isinstance(a, dict)}


def _clip_length(clip: Dict[str, Any], assets: Dict[str, Any]) -> Optional[float]:
    """A track clip's length: its own `duration`, else its trim or its asset's, at its speed."""
    if _num(clip.get('duration')):
        return float(clip['duration'])
    content = clip.get('content') or {}
    speed = float(content['speed']) if _num(content.get('speed')) and content['speed'] > 0 else 1.0
    trim = content.get('trim') or {}
    if _num(trim.get('in')) and _num(trim.get('out')):
        return (float(trim['out']) - float(trim['in'])) / speed
    record = assets.get(content.get('assetId')) or {}
    return float(record['duration']) / speed if _num(record.get('duration')) else None


def _visits(scene: Dict[str, Any], offset: float, until: float, seen: Set[str]) -> Iterator[Tuple[Dict[str, Any], float, float]]:
    """
    Every layer the viewer can see, with its start and its scene's zero in the outer scene's seconds.
    A layer's `duration` is cut to what is seen of it: the end of its composition and of every scene
    around it. A track's clips come as layers of their own, at their time in the track.
    """
    assets = _assets(scene)
    comp = scene.get('composition') or {}
    if _num(comp.get('duration')):
        until = min(until, offset + float(comp['duration']))
    for layer in scene.get('layers') or []:
        if not isinstance(layer, dict):
            continue
        start = offset + (float(layer['start']) if _num(layer.get('start')) else 0.0)
        if start >= until - 1e-6:
            continue
        end = min(until, start + float(layer['duration'])) if _num(layer.get('duration')) else until
        seen_layer = layer if not _num(layer.get('duration')) or end >= start + float(layer['duration']) else {**layer, 'duration': end - start}
        yield seen_layer, start, offset
        content = layer.get('content') or {}
        if content.get('kind') == 'track':
            at = start
            for i, clip in enumerate(content.get('clips') or []):
                length = _clip_length(clip, assets) if isinstance(clip, dict) else None
                if length is None or at >= end - 1e-6:
                    break
                # A clip's keyframe times are its own seconds, from where it starts.
                yield {**clip, 'id': clip.get('id', f"{layer.get('id', '')}.clips[{i}]"), 'timeMode': 'layer',
                       'duration': min(length, end - at)}, at, offset
                at += length
        ref = content.get('assetId') if content.get('kind') == 'scene_ref' else None
        inner = (assets.get(ref) or {}).get('scene') if ref else None
        if isinstance(inner, dict) and ref not in seen:
            yield from _visits(inner, start, end, seen | {ref})


def placed(scene: Dict[str, Any]) -> Iterator[Tuple[Dict[str, Any], float]]:
    """Every layer with its start in the outer scene's seconds: nested scenes' and tracks' clips included."""
    for layer, start, _ in _visits(scene, 0.0, math.inf, set()):
        yield layer, start


def change_times(scene: Dict[str, Any], extra: List[float], moving: Optional[List[Tuple[float, float]]] = None) -> List[float]:
    """
    Every moment the picture changes, in scene seconds. `moving`, when given, collects each span a
    keyframed value moves through: the picture changes all through it, not only at its ends. Sound
    is not picture: an audio layer and a `volume` track change nothing on screen.
    """
    times = list(extra)
    for layer, start, zero in _visits(scene, 0.0, math.inf, set()):
        if (layer.get('content') or {}).get('kind') == 'audio':
            continue
        times.append(start)
        if _num(layer.get('duration')):
            times.append(start + float(layer['duration']))
        for prop, track in (layer.get('animations') or {}).items():
            if prop == 'volume':
                continue
            keys = [k for k in (track or {}).get('keyframes') or [] if isinstance(k, dict) and _num(k.get('time'))]
            # Layer-relative unless the track says otherwise; composition times run on the clock of
            # the scene the layer is in.
            base = zero if (track or {}).get('timeMode', layer.get('timeMode', 'composition')) == 'composition' else start
            for a, b in zip(keys, keys[1:]):
                if a.get('value') != b.get('value'):
                    times += [base + float(a['time']), base + float(b['time'])]
                    if moving is not None and a.get('easing') != 'step':
                        moving.append((base + float(a['time']), base + float(b['time'])))
    return sorted(times)


def lint(scene: Dict[str, Any], labels: Optional[List[str]], changes: List[float]) -> Dict[str, Any]:
    findings: List[Dict[str, Any]] = []
    for layer, start in placed(scene):
        content = layer.get('content') or {}
        if content.get('kind') != 'text':
            continue
        lid = str(layer.get('id', ''))
        n = word_count(content)
        if n == 0:
            continue
        typed = typing_time(content)
        is_label = lid in labels if labels is not None else bool(LABEL.search(lid))
        cap = MAX_LABEL_WORDS if is_label else MAX_WORDS
        if typed is None and n > cap:
            findings.append({'code': 'too_many_words', 'layer': lid,
                             'message': f"{lid} has {n} words; a {'step label' if is_label else 'block'} reads at a glance at {cap} or fewer",
                             'fix': f'cut it to {cap} words: the verb and what it gets done'})
        need = max(MIN_HOLD, PER_WORD * n) + (typed or 0.0)
        hold = float(layer['duration']) if _num(layer.get('duration')) else None
        if hold is not None and hold + 1e-6 < need:
            findings.append({'code': 'short_hold', 'layer': lid,
                             'message': f'{lid} shows {n} words for {hold:.1f} s; reading them takes {need:.1f} s',
                             'fix': f'hold it {need - hold:.1f} s longer, or cut it to {max(1, int(max(0.0, hold - (typed or 0.0)) / PER_WORD))} words'})
    comp = scene.get('composition') or {}
    end = float(comp['duration']) if _num(comp.get('duration')) else None
    moving: List[Tuple[float, float]] = []
    times = [t for t in change_times(scene, changes, moving) if end is None or t <= end + 1e-6]
    if end is not None:
        times = [0.0] + times + [end]
    times = sorted(set(round(t, 3) for t in times))
    for a, b in zip(times, times[1:]):
        # A move's ends are change times, so a gap is either wholly inside a move or outside every one.
        if any(s <= a + 1e-6 and b <= e + 1e-6 for s, e in moving):
            continue
        if b - a > DEAD_AIR + 1e-6:
            findings.append({'code': 'dead_air', 'from': a, 'to': b,
                             'message': f'nothing changes on screen from {a:g} s to {b:g} s ({b - a:.1f} s)',
                             'fix': 'cut or speed up the wait, or land a push, a line or the next beat inside it'})
    return {'ok': not findings, 'findings': findings}


def run(data: Any) -> Dict[str, Any]:
    """The script's whole job: the checked input in, the line it prints out."""
    if not isinstance(data, dict):
        raise InputError('the input must be one JSON object')
    scene = data.get('scene')
    extra: List[float] = []
    if isinstance(scene, dict) and 'scene' in scene and 'layers' not in scene:
        for beat in scene.get('timeline') or []:
            if isinstance(beat, dict) and _num(beat.get('start')):
                extra.append(float(beat['start']))
        scene = scene['scene']
    if not isinstance(scene, dict) or not isinstance(scene.get('layers'), list):
        raise InputError('scene must be the scene document, with its layers')
    labels = data.get('labels')
    if labels is not None and (not isinstance(labels, list) or not all(isinstance(x, str) for x in labels)):
        raise InputError('labels must be a list of layer ids')
    changes = data.get('changes') or []
    if not isinstance(changes, list) or not all(_num(t) for t in changes):
        raise InputError('changes must be a list of seconds')
    return lint(scene, labels, extra + [float(t) for t in changes])


def main(argv: List[str]) -> int:
    if len(argv) > 1 or any(a.startswith('-') for a in argv):
        return fail(USAGE, 2)
    try:
        if argv:
            with open(argv[0], encoding='utf-8-sig') as f:
                text = f.read()
        else:
            text = sys.stdin.buffer.read().decode('utf-8-sig')
    except (OSError, UnicodeDecodeError) as err:
        return fail(f'cannot read the input: {err}')
    try:
        out = run(json.loads(text))
    except json.JSONDecodeError as err:
        return fail(f'the input is not JSON: {err}')
    except InputError as err:
        return fail(str(err))
    sys.stdout.buffer.write((json.dumps(out, separators=(',', ':')) + '\n').encode('utf-8'))
    return 0


def fail(reason: str, code: int = 1) -> int:
    sys.stderr.write('timing.py: ' + ' '.join(reason.split()) + '\n')
    return code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
