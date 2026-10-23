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
  1 s. A typed block adds only the typing still to come while it is on screen, including
  in retimed scenes. A caption is read a segment at a time, or a word at a
  time when its `style.reveal.window` is `active`.
- **Short blocks**: at most 10 words in a block, and at most 6 in a step label (10 in a landscape
  frame, where a step line is a lower third). A typed request is the user's own words, so it has no
  cap.
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
MAX_LANDSCAPE_LABEL_WORDS = 10
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
    record = content.get('asset') or assets.get(content.get('assetId')) or {}
    return float(record['duration']) / speed if _num(record.get('duration')) else None


class _Placed(dict):
    """A visited layer with its inherited visibility, on the outer scene's clock."""


def _visible_layer(layer: Dict[str, Any], start: float, zero: float, end: float,
                   visible: List[Tuple[float, float]], rate: float = 1.0, opacity: bool = True) -> _Placed:
    """Place the layer on the outer clock; duration inference never reads opacity."""
    out = _Placed(layer)
    out.rate = rate
    if math.isfinite(end):
        out['duration'] = end - start
    own = shown(out, start, zero) if opacity else [(start, end)]
    out.spans = [(max(a, c), min(b, d)) for a, b in own
                 for c, d in visible if min(b, d) > max(a, c) + 1e-6]
    return out


def shown(layer: Dict[str, Any], start: float, zero: float = 0.0) -> List[Tuple[float, float]]:
    """
    The spans a layer is on screen, in scene seconds: its lifetime less the stretches its opacity
    holds at 0. Opacity keyframes use the composition clock unless the track says otherwise; a ramp up from
    0 shows from its first key, and a `step` from 0 only from its second.
    """
    if isinstance(layer, _Placed) and hasattr(layer, 'spans'):
        return layer.spans
    end = start + float(layer['duration']) if _num(layer.get('duration')) else math.inf
    track = (layer.get('animations') or {}).get('opacity') or {}
    if track.get('expression'):
        raise InputError('expression-driven opacity needs rendered visibility; cannot determine words offline')
    keys = [k for k in track.get('keyframes') or [] if isinstance(k, dict) and _num(k.get('time')) and _num(k.get('value'))]
    if not keys:
        still = (layer.get('transform') or {}).get('opacity')
        return [(start, end)] if not _num(still) or still > 0 else []
    mode = track.get('timeMode', layer.get('timeMode', 'composition'))
    if mode not in ('composition', 'layer'):
        raise InputError(f'unsupported opacity timeMode: {mode}')
    base = zero if mode == 'composition' else start
    rate = getattr(layer, 'rate', 1.0)
    pts = [(base + float(k['time']) * rate, float(k['value']), k.get('easing')) for k in keys]
    spans = [(-math.inf, pts[0][0])] if pts[0][1] > 0 else []
    for (t0, v0, easing), (t1, v1, _) in zip(pts, pts[1:]):
        if v0 > 0 or (v1 > 0 and easing != 'step'):
            spans.append((t0, t1))
    if pts[-1][1] > 0:
        spans.append((pts[-1][0], math.inf))
    out: List[Tuple[float, float]] = []
    for a, b in spans:
        a, b = max(a, start), min(b, end)
        if b <= a + 1e-6:
            continue
        if out and a <= out[-1][1] + 1e-6:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out


def _check_container(layer: Dict[str, Any]) -> None:
    content = layer.get('content') or {}
    if content.get('kind') != 'scene_ref' and isinstance((content.get('asset') or {}).get('scene'), dict):
        raise InputError('unsupported inline scene asset: timing was not checked')
    mask_spec = layer.get('mask') or {}
    mask = mask_spec.get('clip') or mask_spec.get('layer')
    if isinstance(mask, dict):
        if (mask.get('content') or {}).get('kind') in ('text', 'captions', 'composition', 'scene_ref', 'track'):
            raise InputError('unsupported text mask: timing was not checked')
        _check_container(mask)


def _visits(scene: Dict[str, Any], offset: float, until: float, seen: Set[int], visible: Optional[List[Tuple[float, float]]] = None, cameras: bool = False, rate: float = 1.0, inherited_assets: Optional[Dict[str, Any]] = None, opacity: bool = True, containers: Tuple[Any, ...] = ()) -> Iterator[Tuple[Dict[str, Any], float, float, float]]:
    """
    Every layer the viewer can see, with its start, its scene's zero and the last moment it can be
    seen, in the outer scene's seconds. A layer's `duration` is cut to what is seen of it: the end of
    its composition and of every scene around it. A track's clips come as layers of their own, at
    their time in the track. With `opacity` false, no layer's opacity is read (see `_visible_layer`).
    """
    visible = visible if visible is not None else [(offset, until)]
    seen = seen | {id(scene)}
    assets = _assets(scene) if inherited_assets is None else inherited_assets
    comp = scene.get('composition') or {}
    scope = object()
    if _num(comp.get('duration')):
        until = min(until, offset + float(comp['duration']) * rate)
    if cameras and isinstance(comp.get('camera'), dict):
        camera = {**comp['camera'], 'content': {'kind': 'camera'}}
        camera['depth'] = any('z' in (l.get('transform') or {}) or 'z' in (l.get('animations') or {})
                              for l in scene.get('layers') or [] if isinstance(l, dict))
        yield _visible_layer(camera, offset, offset, until, visible, rate, opacity), offset, offset, until

    def visit(layer: Dict[str, Any], start: float, bound: float,
              inherited: List[Tuple[float, float]], owners: Tuple[Any, ...] = containers) -> Iterator[Tuple[Dict[str, Any], float, float, float]]:
        """Layers and sequential clips share the same container traversal and clocks."""
        _check_container(layer)
        if start >= bound - 1e-6:
            return
        length = _clip_length(layer, assets)
        end = min(bound, start + length * rate) if length is not None else bound
        seen_layer = _visible_layer(layer, start, offset, end, inherited, rate, opacity)
        seen_layer.assets = assets
        seen_layer.scope = scope
        seen_layer.containers = owners
        yield seen_layer, start, offset, end
        content = layer.get('content') or {}
        if content.get('kind') == 'track':
            at = start
            for i, clip in enumerate(content.get('clips') or []):
                if isinstance(clip, dict):
                    _check_container(clip)
                length = _clip_length(clip, assets) if isinstance(clip, dict) else None
                if length is None or at >= end - 1e-6:
                    break
                # A clip's keyframe times are its own seconds, from where it starts.
                placed_clip = {**clip, 'id': clip.get('id', f"{layer.get('id', '')}.clips[{i}]"), 'timeMode': 'layer'}
                yield from visit(placed_clip, at, end, seen_layer.spans, owners + (seen_layer,))
                at += length * rate
        if content.get('kind') == 'composition' and id(content) not in seen:
            # Inline groups share this scene's assets, but their children start on the group's clock.
            yield from _visits(content, start, end, seen, seen_layer.spans, cameras, rate, assets, opacity, owners + (seen_layer,))
        ref = content.get('assetId') if content.get('kind') == 'scene_ref' else None
        inner = (content.get('asset') or assets.get(ref) or {}).get('scene') if content.get('kind') == 'scene_ref' else None
        if isinstance(inner, dict) and id(inner) not in seen:
            speed = content.get('speed', 1)
            trim = content.get('trim') or {}
            trim_in, trim_out = trim.get('in', 0), trim.get('out')
            if (not _num(speed) or not math.isfinite(speed) or speed <= 0 or content.get('loop')
                    or not _num(trim_in) or not math.isfinite(trim_in) or trim_in < 0
                    or (trim_out is not None and (not _num(trim_out) or not math.isfinite(trim_out) or trim_out <= trim_in))):
                raise InputError('unsupported scene_ref speed, trim or loop: timing was not checked')
            child_rate = rate / speed
            child_zero = start - trim_in * child_rate
            if trim_out is not None:
                end = min(end, child_zero + trim_out * child_rate)
            yield from _visits(inner, child_zero, end, seen, seen_layer.spans, cameras, child_rate, opacity=opacity, containers=owners + (seen_layer,))

    for layer in scene.get('layers') or []:
        if isinstance(layer, dict):
            start = offset + (float(layer['start']) if _num(layer.get('start')) else 0.0) * rate
            yield from visit(layer, start, until, visible)


def placed(scene: Dict[str, Any]) -> Iterator[Tuple[Dict[str, Any], float]]:
    """Every layer with its start in the outer scene's seconds: nested scenes' and tracks' clips included."""
    for layer, start, _, _ in _visits(scene, 0.0, math.inf, set()):
        yield layer, start


def seen(scene: Dict[str, Any]) -> Iterator[Tuple[Dict[str, Any], float, float]]:
    """
    Every layer with its start and the last moment it can be seen, in the outer scene's seconds: a
    layer with no `duration` is still cut at the end of its composition and of every scene around it.
    """
    for layer, start, _, end in _visits(scene, 0.0, math.inf, set()):
        yield layer, start, end


def scene_duration(scene: Dict[str, Any]) -> Optional[float]:
    """
    How long the scene plays: its composition's `duration`, else the latest end of what is in it,
    a track's clips included (the footage-reframing skill says when a scene has none).
    """
    d = (scene.get('composition') or {}).get('duration')
    if _num(d):
        return float(d) if d > 0 else None
    ends = []
    for layer, start, _, bound in _visits(scene, 0.0, math.inf, set(), opacity=False):
        content = layer.get('content') or {}
        if content.get('kind') == 'track' and not _num(layer.get('duration')):
            continue  # its clips come as layers of their own
        # Never past the scenes around it: a long clip in a 5 s nested scene is seen for 5 s.
        end = min(bound, start + float(layer['duration'])) if _num(layer.get('duration')) else bound
        if math.isfinite(end):
            ends.append(end)
    end = max(ends, default=0.0)
    return round(end, 3) if end > 0 else None


def change_times(scene: Dict[str, Any], extra: List[float], moving: Optional[List[Tuple[float, float]]] = None) -> List[float]:
    """
    Every moment the picture changes, in scene seconds. `moving`, when given, collects each span a
    keyframed value moves through: the picture changes all through it, not only at its ends. Sound
    is not picture: an audio layer and a `volume` track change nothing on screen.
    """
    times = list(extra)

    def movement(a: float, b: float, spans: List[Tuple[float, float]]) -> None:
        for s, e in spans:
            a0, b0 = max(a, s), min(b, e)
            if b0 > a0 + 1e-6:
                times.extend([a0, b0])
                if moving is not None:
                    moving.append((a0, b0))

    visits = list(_visits(scene, 0.0, math.inf, set(), cameras=True))
    parents = {(layer.scope, layer.get('id')): layer for layer, _, _, _ in visits
               if hasattr(layer, 'scope') and layer.get('id')}
    rig_spans: Dict[Tuple[Any, str], List[Tuple[float, float]]] = {}
    for child, start, _, _ in visits:
        if (child.get('content') or {}).get('kind') in ('empty', 'audio', 'camera', 'composition', 'scene_ref', 'track'):
            continue
        # A rig can parent a render container; only its visible contents make the rig move picture.
        for owner in (child,) + child.containers:
            parent, chain = owner.get('parentId'), set()
            while parent and parent not in chain:
                chain.add(parent)
                key = (owner.scope, parent)
                rig_spans.setdefault(key, []).extend(shown(child, start))
                parent = (parents.get(key) or {}).get('parentId')
    for layer, start, zero, _ in visits:
        if (layer.get('content') or {}).get('kind') == 'audio':
            continue
        content = layer.get('content') or {}
        spans = shown(layer, start)
        if content.get('kind') == 'empty':
            spans = rig_spans.get((layer.scope, layer.get('id')), [])
        if content.get('kind') not in ('empty', 'camera'):
            times.extend(t for span in spans for t in span if math.isfinite(t))
        rate = getattr(layer, 'rate', 1.0)
        if content.get('kind') == 'captions':
            for at, end, _ in caption_blocks(content, start):
                at, end = start + (at - start) * rate, start + (end - start) * rate
                for s, e in spans:
                    a, b = max(at, s), min(end, e)
                    if b > a + 1e-6:
                        times.extend([a, b])
        for animation in content.get('animations') or []:
            if not isinstance(animation, dict) or animation.get('preset') not in ('typewriter', 'slide_up_lines', 'fade_in_chars', 'flicker_chars'):
                continue
            duration = (animation.get('params') or {}).get('duration')
            duration = float(duration) if _num(duration) else 1.0
            movement(start, start + duration * rate, spans)
        if content.get('kind') == 'track':
            clips = content.get('clips') or []
            at = start
            seams = []
            for clip in clips:
                length = _clip_length(clip, layer.assets)
                if length is None:
                    break
                at += length * rate
                seams.append(at)
            for transition in content.get('transitions') or []:
                gap, duration = transition.get('between'), transition.get('duration')
                if isinstance(gap, int) and 0 <= gap < len(seams) - 1 and _num(duration) and duration > 0:
                    movement(seams[gap] - duration * rate / 2, seams[gap] + duration * rate / 2, spans)
        tracks = [(prop, track, layer.get('timeMode', 'composition'))
                  for prop, track in (layer.get('animations') or {}).items()]
        if content.get('kind') == 'shape':
            items = list(content.get('items') or [])
            while items:
                item = items.pop()
                tracks.extend((prop, track, 'layer') for prop, track in (item.get('animations') or {}).items())
                items.extend(item.get('items') or [])
        for prop, track, clock in tracks:
            if prop == 'volume':
                continue
            if (content.get('kind') == 'camera' and prop in ('position', 'pivot') and not layer.get('depth')
                    and not any(name in layer or name in (layer.get('animations') or {})
                                for name in ('z', 'distance', 'rotationX', 'rotationY'))):
                identity = True
                for name, default in (('zoom', 1), ('rotation', 0)):
                    value = layer.get(name, default)
                    other = (layer.get('animations') or {}).get(name) or {}
                    if value != default or other.get('expression') or any(
                            k.get('value') != default for k in other.get('keyframes') or []):
                        identity = False
                if identity:
                    continue
            if (track or {}).get('expression'):
                # Lua motion cannot be measured offline; its visible span is not known to be static.
                for a, b in spans:
                    movement(a, b, spans)
                continue
            keys = [k for k in (track or {}).get('keyframes') or [] if isinstance(k, dict) and _num(k.get('time'))]
            # Use the owner's clock unless the track says otherwise; composition times run on the clock of
            # the scene the layer is in.
            mode = (track or {}).get('timeMode', clock)
            if mode not in ('composition', 'layer'):
                raise InputError(f'unsupported animation timeMode: {mode}')
            base = zero if mode == 'composition' else start
            for a, b in zip(keys, keys[1:]):
                curved = prop in ('position', 'scale') and any(
                    _num(v) and v != 0 for tangent in (a.get('outTangent'), b.get('inTangent'))
                    if isinstance(tangent, list) for v in tangent)
                if a.get('value') != b.get('value') or curved:
                    at, end = base + float(a['time']) * rate, base + float(b['time']) * rate
                    if a.get('easing') == 'step':
                        if any(s <= end <= e for s, e in spans):
                            times.append(end)
                    else:
                        movement(at, end, spans)
    return sorted(times)


def text_of(content: Dict[str, Any]) -> str:
    t = content.get('text')
    s = ' '.join(t) if isinstance(t, list) else (t if isinstance(t, str) else '')
    return ' '.join(s.split())


def caption_blocks(content: Dict[str, Any], start: float, readable: bool = False) -> List[Tuple[float, float, str]]:
    """
    Caption blocks shifted by the layer's start and timeOffset, before scene_ref rate scaling.
    Panel words follow their reveal (active or sustain). Readable holds check whole segments
    except for active words, whose timings and text must be known to check their holds.
    """
    transcript = content.get('transcript')
    segments = transcript.get('segments') if isinstance(transcript, dict) else None
    offset = float(content['timeOffset']) if _num(content.get('timeOffset')) else 0.0
    style = content.get('style') or {}
    reveal = style.get('reveal') or {}
    window = reveal.get('window', 'sustain') if 'reveal' in style else None
    out = []
    for seg in segments if isinstance(segments, list) else []:
        if not isinstance(seg, dict) or not _num(seg.get('start')) or not _num(seg.get('end')):
            continue
        if window == 'active' or (window == 'sustain' and not readable):
            tokens = text_of(seg).split()
            timed = seg.get('words') or []
            if readable and not timed:
                raise InputError('active captions need word timings to check readable holds')
            for i, word in enumerate(timed):
                if not isinstance(word, dict) or not _num(word.get('start')) or not _num(word.get('end')):
                    if readable:
                        raise InputError('active captions need word timings to check readable holds')
                    continue
                words = text_of(word) or (tokens[i] if len(tokens) == len(timed) else '')
                if readable and not words:
                    raise InputError('active captions need words paired with their word timings')
                a = max(float(seg['start']), float(word['start']))
                b = min(float(seg['end']), float(word['end'])) if window == 'active' else float(seg['end'])
                if words and b > a:
                    out.append((start + offset + a, start + offset + b, words))
            continue
        words = text_of(seg)
        if words:
            out.append((start + offset + float(seg['start']), start + offset + float(seg['end']), words))
    return out


def _readable(scene: Dict[str, Any]) -> Iterator[Tuple[Dict[str, Any], float, float]]:
    """
    Every block once per visible span, with only the typing still to come in that span.
    Typing and captions use the layer's rate on the outer scene's clock.
    """
    for layer, start in placed(scene):
        content = layer.get('content') or {}
        rate = getattr(layer, 'rate', 1.0)
        if content.get('kind') == 'text':
            typed = typing_time(content)
            for a, b in shown(layer, start):
                typing = max(0.0, min(b, start + typed * rate) - a) if typed is not None else 0.0
                yield {**layer, 'duration': b - a}, a, typing
        elif content.get('kind') == 'captions':
            for s, e, words in caption_blocks(content, start, readable=True):
                s, e = start + (s - start) * rate, start + (e - start) * rate
                for a, b in shown(layer, start):
                    a, b = max(a, s), min(b, e)
                    if b > a + 1e-6:
                        yield {**layer, 'duration': b - a, 'content': {'kind': 'text', 'text': words}}, a, 0.0


def lint(scene: Dict[str, Any], labels: Optional[List[str]], changes: List[float]) -> Dict[str, Any]:
    findings: List[Dict[str, Any]] = []
    comp = scene.get('composition') or {}
    landscape = _num(comp.get('width')) and _num(comp.get('height')) and comp['width'] > comp['height']
    for layer, start, typing in _readable(scene):
        content = layer.get('content') or {}
        if content.get('kind') != 'text':
            continue
        lid = str(layer.get('id', ''))
        n = word_count(content)
        if n == 0:
            continue
        typed = typing_time(content)
        is_label = lid in labels if labels is not None else bool(LABEL.search(lid))
        cap = (MAX_LANDSCAPE_LABEL_WORDS if landscape else MAX_LABEL_WORDS) if is_label else MAX_WORDS
        if typed is None and n > cap:
            findings.append({'code': 'too_many_words', 'layer': lid,
                             'message': f"{lid} has {n} words; a {'step label' if is_label else 'block'} reads at a glance at {cap} or fewer",
                             'fix': f'cut it to {cap} words: the verb and what it gets done'})
        need = max(MIN_HOLD, PER_WORD * n) + typing
        hold = float(layer['duration']) if _num(layer.get('duration')) else None
        if hold is not None and hold + 1e-6 < need:
            findings.append({'code': 'short_hold', 'layer': lid,
                             'message': f'{lid} shows {n} words for {hold:.1f} s; reading them takes {need:.1f} s',
                             'fix': f'hold it {need - hold:.1f} s longer, or cut it to {max(1, int(max(0.0, hold - typing) / PER_WORD))} words'})
    end = scene_duration(scene)
    moving: List[Tuple[float, float]] = []
    times = [t for t in change_times(scene, changes, moving) if end is None or t <= end + 1e-6]
    if end is not None:
        times = [0.0] + times + [end]
    times = sorted(set(times))
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
