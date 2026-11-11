#!/usr/bin/env python3
"""
Check a film's cut from its scene alone, before the cut is reviewed: the joins, moves and overlays
a viewer reads as a glitch.

    python3 scripts/cut_check.py input.json [--allow START-END ...] [--slides]
    python3 scripts/cut_check.py < input.json

The input is one JSON object:

    {"scene": {...}, "allowed": [{"start": 4.2, "end": 7.9, "file": "screens/inbox.mp4"}],
     "shots": {"clip-3": "s2", "clip-4": {"shot": "s3", "size": "close", "angle": "eye"}},
     "places": {"take-03": "kitchen", "take-04": "kitchen"}, "stage": "slides"}

- `scene`: the cut's scene document (a bare scene is read too).
- `allowed`, optional: the allowed spans, in seconds on the cut's timeline, as the
  `allowed-spans.json` the cut was built with lists them (`start`, `end`, and optionally the
  screen clip's `file`). `--allow START-END` adds one more; both may be given. Every check skips
  what is inside a span, except `screen-still`, which reads only inside them.
- `shots`, optional: the shot each clip shows, from the project record's shot list, keyed by its
  layer or clip id, its asset id or its asset's uri: a shot id, or `{shot, size?, angle?}`. A run's
  file holds several shots, so key its clips by clip id. Without it the takes are not compared.
- `places`, optional: the place each clip shows, keyed the same way. It only tells
  `hidden-take-change` that a quick move or a transition sits over a cut inside one place; a hard
  cut between different shots of one place is coverage, and passes.
- `stage`, optional: `"slides"` for an animatic of held stills (`--slides` says the same). Its
  stills hold on purpose, so the motion rules (`still`, `idle-hold`, `held-frame`, `zoom-idle`) are
  not run on it: they are listed in `skipped`, to be run on the cut. The joins, overlays, moves and
  screens are checked as usual.

The checks, each an `error` (FAIL: fix it before the review) or a `warning` (WARN: say it):

- `screen-still` (warning): inside an allowed span, a screen clip holds one picture for 1.8 s or
  more (a still image, or a video past the end of its source), so the viewer may think the video
  paused;
- `pop-move` (error): a code move on the camera, or on a layer covering 40% of the frame or more
  (footage, or a big tracked card; a smaller overlay is exempt whatever its easing), starts from
  rest or stops at full speed in one frame, or jumps on a `step` key (position, scale, rotation,
  crop, depth). A run of linear keys is one sampled move: it starts or stops abruptly only when its
  first or last segment is already at 90% or more of the run's peak speed;
- `same-scene-cut` (error): a hard cut joins two takes of one shot, jumps inside one shot of one
  file, or joins two shots of the same size and angle (the record gives both); the picture barely
  changes, so it reads as a glitch;
- `hidden-take-change` (error): a short move (3 to 15 frames) or a non-dissolve transition hides
  such a cut, or a cut inside one place;
- `ghost` (error): a dissolve of 0.3 s or less between two takes shows both at once;
- `blink` (error): an overlay (a caption, a title, a sticker) vanishes for one or two frames and
  comes back;
- `zoom-idle` (error): only a code zoom moves for 0.8 s or more, over a picture the scene holds still
  (a still image, or a video past the end of its source).

What the scene cannot answer is listed in `unchecked`, with why: the other cut rules need pixels
decoded by a tool, and a still stretch inside a video is only on its frames.

It prints one JSON line, `{ok, errors, warnings, checked, unchecked, skipped}`; `ok` is true when there is
no error. Each finding has a `code`, its `start` and `end` in seconds, the `layers` it is on, a
`message` and a `fix`. Input it cannot check exits 1, a bad command line exits 2, each with one
line on stderr that says what is wrong.

Python 3.9 or later, the standard library only, offline.
"""
from __future__ import annotations

import copy
import json
import math
import re
import sys
from typing import Any, Dict, Iterable, Iterator, List, Optional, Tuple

from timing import InputError, _clip_length, _num, _visits, caption_blocks, shown, scene_duration

Span = Tuple[float, float]

DEFAULT_FPS = 30.0
# A screen held this long can look paused, even with a bar or a cursor moving on it.
SCREEN_SECONDS = 1.8
# Only the zoom moves for at least this long.
ZOOM_IDLE_SECONDS = 0.8
# A move hiding a take switch is a short burst: 3 to 15 frames.
TAKE_MIN_FRAMES, TAKE_MAX_FRAMES = 3, 15
# A dissolve shorter than this shows two takes at once and reads as a double exposure.
GHOST_SECONDS = 0.3
# An overlay may vanish for one or two frames.
BLINK_FRAMES = 2
# An eased start or stop moves at no more than half the move's average speed.
EASED_SLOPE = 0.5
# A sampled run of linear keys starts or stops abruptly when its end segment is this near its peak speed.
SAMPLED_PEAK = 0.9
# A layer moves the picture when it covers this share of the frame (the channel team's 8 of 20 grid cells).
POP_COVER = 0.4
EPS = 1e-6

# Transitions that show both clips at once.
DISSOLVES = {'crossfade', 'blur_dissolve', 'light_leak_burst', 'zoom_through'}
# Transitions whose own motion can hide a change of take.
MASKING = {'zoom_through', 'glitch_cut', 'slide', 'diagonal_slide', 'card_flip',
           'page_curl', 'iris', 'shape_reveal', 'manga_page', 'flash_cut'}

# What a geometric track must change by to be seen, per property.
MOVES = {'position': 2.0, 'translation': 2.0, 'anchor': 2.0, 'crop': 2.0, 'z': 2.0, 'distance': 2.0,
         'scale': 0.01, 'zoom': 0.01, 'rotation': 0.5, 'rotationX': 0.5, 'rotationY': 0.5}
ZOOMS = {'scale', 'zoom', 'z', 'distance'}
# Content that is the picture itself: a move on it moves the whole frame.
FOOTAGE = {'media', 'track', 'composition', 'scene_ref'}
# Content that sits over the picture.
DEPTH_PROPS = ('z', 'rotationX', 'rotationY', 'distance')
OVERLAYS = {'text', 'captions', 'shape', 'color'}

# The 19 cut-check rules: what each detects, and whether this script checks it.
RULES: Dict[str, Dict[str, str]] = {
    'still': {'level': 'FAIL', 'status': 'planned', 'detector': 'picsart_media_segment_shots holds of 0.25 s or more'},
    'screen-still': {'level': 'WARN', 'status': 'implemented', 'detector': 'scene: screen clips held still inside allowed spans'},
    'zoom-idle': {'level': 'FAIL', 'status': 'implemented', 'detector': 'scene: zoom keys over still pictures',
                  'planned': 'zoom keys over footage that holds, from picsart_media_segment_shots'},
    'idle-hold': {'level': 'WARN', 'status': 'planned', 'detector': 'picsart_media_track_motion area and zoom keys'},
    'held-frame': {'level': 'WARN', 'status': 'planned', 'detector': 'picsart_media_segment_shots one-frame holds'},
    'flash': {'level': 'FAIL', 'status': 'planned', 'detector': 'picsart_media_segment_shots transitions and brightness'},
    'pop': {'level': 'FAIL', 'status': 'planned', 'detector': 'picsart_media_flow_diff one-frame jumps'},
    'pop-move': {'level': 'FAIL', 'status': 'implemented', 'detector': 'scene: easing on moves of the footage and the camera'},
    'same-scene-cut': {'level': 'FAIL', 'status': 'implemented', 'detector': 'scene: adjacent takes of one shot, from the shot list'},
    'jump-cut': {'level': 'FAIL', 'status': 'planned', 'detector': 'picsart_media_inventory_diff across the join'},
    'hidden-take-change': {'level': 'FAIL', 'status': 'implemented', 'detector': 'scene: a short move or transition over a take switch'},
    'ghost': {'level': 'FAIL', 'status': 'implemented', 'detector': 'scene: transition type and length'},
    'edge-bar': {'level': 'FAIL', 'status': 'planned', 'detector': 'contact-sheet edge strips'},
    'mid-move-duplicate': {'level': 'FAIL', 'status': 'planned', 'detector': 'picsart_media_segment_shots repeated frames in motion'},
    'dark-dip': {'level': 'FAIL', 'status': 'planned', 'detector': 'brightness curve from stills'},
    'blink': {'level': 'FAIL', 'status': 'implemented', 'detector': 'scene: overlay gaps of one or two frames'},
    'whip': {'level': 'WARN', 'status': 'planned', 'detector': 'picsart_media_track_motion speed outliers'},
    'silence': {'level': 'WARN', 'status': 'planned', 'detector': 'picsart_media_analyze_audio energy'},
    'loudness': {'level': 'WARN', 'status': 'implemented', 'detector': 'qc.py loudness, on the export'},
}
CHECKED = [code for code, rule in RULES.items() if rule['status'] == 'implemented' and code != 'loudness']
# An animatic's stills hold on purpose: these rules judge motion, so they run on the cut instead.
SLIDES_MOTION = ('still', 'idle-hold', 'held-frame', 'zoom-idle')
SLIDES_SKIP = "slides: the animatic's stills hold on purpose; run it on the cut"

FIX = {
    'screen-still': 'start the screen clip later, shorten its hold, or let something on it move',
    'pop-move': 'ease the move in from rest and out to rest (ease_in_out), or start it on a cut',
    'same-scene-cut': 'play the shot from one take, or cut to a different shot between the two takes',
    'hidden-take-change': 'cut hard where the shot changes; a move or a transition does not hide a change of take',
    'ghost': 'cut hard between the takes',
    'blink': 'close the gap, so the overlay stays up or the next one starts as it ends',
    'zoom-idle': 'cut to a moving moment, or drop the zoom over the still',
}

USAGE = 'usage: cut_check.py [input.json] [--allow START-END ...] [--slides]; with no file, the input is read from stdin'


class _Shot:
    """One visual layer or track clip, placed on the cut's timeline."""

    def __init__(self, layer: Dict[str, Any], start: float, zero: float, end: float) -> None:
        self.layer = layer
        self.id = str(layer.get('id', ''))
        self.start, self.zero, self.end = start, zero, end
        self.rate = float(getattr(layer, 'rate', 1.0))
        self.containers = tuple(getattr(layer, 'containers', ()))
        self.scope = getattr(layer, 'scope', None)
        assets = getattr(layer, 'assets', {}) or {}
        self.content = layer.get('content') or {}
        self.kind = self.content.get('kind')
        record = self.content.get('asset') or assets.get(self.content.get('assetId')) or {}
        self.asset = self.content.get('assetId') if isinstance(self.content.get('assetId'), str) else None
        self.uri = record.get('uri') if isinstance(record.get('uri'), str) else None
        kind = record.get('type')
        self.media = ('video' if kind in ('video', 'video_with_matte') else 'image' if kind in ('image', 'svg')
                      else 'other') if self.kind == 'media' else None
        self.source_length = self._source_length(record)

    def _source_length(self, record: Dict[str, Any]) -> Optional[float]:
        """How long a video plays before it holds its last frame, on the cut's clock."""
        if self.media != 'video' or self.content.get('loop'):
            return None
        speed = abs(float(self.content['speed'])) if _num(self.content.get('speed')) and self.content['speed'] else 1.0
        trim = self.content.get('trim') or {}
        if _num(trim.get('in')) and _num(trim.get('out')):
            limit = float(record['duration']) if _num(record.get('duration')) else float(trim['out'])
            return max(0.0, min(float(trim['out']), limit) - max(0.0, float(trim['in']))) / speed * self.rate
        if _num(record.get('duration')):
            return max(0.0, float(record['duration']) - float(trim.get('in') or 0)) / speed * self.rate
        return None

    @property
    def key_zero(self) -> float:
        """Where this layer's keyframe times count from, on the cut's clock."""
        return _key_zero(self.layer, {}, self.start, self.zero)

    def still(self) -> List[Span]:
        """Where the scene alone says the picture holds: a still image, or a video past its source."""
        if self.media == 'image':
            return [(self.start, self.end)]
        if self.media == 'video' and self.source_length is not None:
            at = max(self.start, getattr(self.layer, 'placed_start', self.start) + self.source_length)
            if at < self.end - EPS:
                return [(at, self.end)]
        return []

    def place(self, places: Dict[str, Any]) -> Optional[str]:
        for key in (self.id, self.asset, self.uri):
            if key and key in places:
                return str(places[key])
        return None

    def shot(self, shots: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """The shot this clip shows, from the shot list: its id, and its size and angle when known."""
        for key in (self.id, self.asset, self.uri):
            if key and key in shots:
                value = shots[key]
                return {'shot': str(value.get('shot')), **{k: value[k] for k in ('size', 'angle') if k in value}} \
                    if isinstance(value, dict) else {'shot': str(value)}
        return None

    def source(self) -> Optional[str]:
        return self.uri or self.asset


# --- intervals --------------------------------------------------------------------------------


def merge(spans: Iterable[Span]) -> List[Span]:
    out: List[Span] = []
    for a, b in sorted(spans):
        if b <= a + EPS:
            continue
        if out and a <= out[-1][1] + EPS:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out


def outside(start: float, end: float, allowed: List[Span]) -> Iterator[Span]:
    """Subtract allowed spans, including spans that split a run."""
    for left, right in sorted(allowed):
        if right <= start:
            continue
        if left >= end:
            break
        if left > start:
            yield start, left
        start = max(start, right)
        if start >= end:
            return
    if start < end:
        yield start, end


def intersect(a: List[Span], b: List[Span]) -> List[Span]:
    return merge((max(x, y), min(p, q)) for x, p in a for y, q in b if min(p, q) > max(x, y) + EPS)


def subtract(a: List[Span], b: List[Span]) -> List[Span]:
    return merge(piece for x, y in a for piece in outside(x, y, merge(b)))


def all_still(shots: List[_Shot], layers=None) -> List[Span]:
    """Where at least one of the shots is on screen and every one on screen holds still."""
    cuts = sorted({t for s in shots for t in (s.start, s.end)} | {t for s in shots for span in s.still() for t in span})
    out = []
    previous = None
    for a, b in zip(cuts, cuts[1:]):
        if b <= a + EPS:
            continue
        mid = (a + b) / 2
        on = [s for s in shots if s.start <= mid < s.end]
        if on and all(any(x <= mid < y for x, y in s.still()) for s in on):
            def inherited(s):
                if layers is None:
                    return None
                try:
                    owners = s.containers + (s.layer,)
                    inherited_owners = [owner for item in owners
                                        for owner in ((item,) if item is not s.layer else ()) + tuple(_parent_layers(item, layers))]
                    if any(owner.get('animations') or any(c.get('animations') for c in owner.get('transforms') or [] if isinstance(c, dict)) for owner in inherited_owners):
                        return object()  # Animated inherited placement may differ across the join.
                    return [(owner.get('transform'), owner.get('transforms'), owner.get('content'), owner.get('mask'))
                            for owner in inherited_owners]
                except InputError:
                    return object()  # Unresolved placement must not merge separate pictures.
            picture = [(s.source(), s.content, s.layer.get('transform'), s.layer.get('animations'), s.layer.get('transforms'), s.layer.get('mask'), inherited(s)) for s in on]
            if out and previous == picture and all(s.media == 'image' and s.source() and not s.layer.get('animations') and not any(c.get('animations') for c in s.layer.get('transforms') or [] if isinstance(c, dict)) for s in on) and abs(out[-1][1] - a) <= EPS:
                out[-1] = (out[-1][0], b)
            else:
                out.append((a, b))
            previous = picture
        else:
            previous = None
    return out  # A change of visible pictures breaks a continuous still hold.


# --- moves --------------------------------------------------------------------------------------


def _vector(value: Any) -> Optional[List[float]]:
    if _num(value):
        return [float(value)]
    if isinstance(value, list) and value and all(_num(v) for v in value):
        return [float(v) for v in value]
    return None


def _changes(prop: str, a: List[float], b: List[float]) -> List[bool]:
    tol = MOVES.get(prop, 0.01)
    if len(a) != len(b):
        return [True]
    return [abs(x - y) > tol for x, y in zip(a, b)]


def _slope_start(easing: Any) -> float:
    """The speed a segment starts at, as a share of its average speed."""
    if isinstance(easing, dict) and easing.get('kind') == 'cubic_bezier':
        x1, y1, x2, y2 = (list(easing.get('control') or []) + [0, 0, 1, 1])[:4]
        if x1 > EPS:
            return y1 / x1
        if y1 > EPS:
            return math.inf
        return y2 / x2 if x2 > EPS else (math.inf if y2 > EPS else 1.0)
    return {'ease_in': 0.0, 'ease_in_out': 0.0}.get(easing, 1.0)


def _slope_end(easing: Any) -> float:
    if isinstance(easing, dict) and easing.get('kind') == 'cubic_bezier':
        x1, y1, x2, y2 = (list(easing.get('control') or []) + [0, 0, 1, 1])[:4]
        if x2 < 1 - EPS:
            return (1 - y2) / (1 - x2)
        if y2 < 1 - EPS:
            return math.inf
        return (1 - y1) / (1 - x1) if x1 < 1 - EPS else 1.0
    return {'ease_out': 0.0, 'ease_in_out': 0.0}.get(easing, 1.0)


def _abrupt(easing: Any, moving: List[bool], slope) -> bool:
    if isinstance(easing, list):
        return any(m and abs(slope(e)) > EASED_SLOPE for e, m in zip(easing, moving))
    return abs(slope(easing)) > EASED_SLOPE


class _Move:
    """One keyframe segment that changes a geometric value, on the cut's clock."""

    def __init__(self, prop: str, start: float, end: float, easing: Any, moving: List[bool],
                 rest_before: bool, rest_after: bool, speed: float = 0.0) -> None:
        self.prop, self.start, self.end, self.easing = prop, start, end, easing
        self.moving, self.rest_before, self.rest_after, self.speed = moving, rest_before, rest_after, speed
        # Set on a sampled run's first and last segments when the run's speed ramps there.
        self.ramped_in = self.ramped_out = False


def _tracks(holder: Dict[str, Any], props: Iterable[str]) -> Iterator[Tuple[str, Dict[str, Any]]]:
    for prop in props:
        track = holder.get(prop)
        if isinstance(track, dict):
            yield prop, track


def _key_zero(layer: Dict[str, Any], track: Dict[str, Any], start: float, zero: float) -> float:
    mode = track.get('timeMode', layer.get('timeMode', 'composition'))
    if mode not in ('composition', 'layer'):
        raise InputError(f'unsupported animation timeMode: {mode}')
    return getattr(layer, 'placed_start', start) if mode == 'layer' else zero


def moves(shot_like: Dict[str, Any], zero: float, rate: float, start: float, end: float,
          fps: float, unchecked: List[Dict[str, str]], where: str) -> List[_Move]:
    """Every geometric move a layer (or the camera) makes, with whether it starts and stops at rest."""
    tracks = list(_tracks(shot_like.get('animations') or {} if isinstance(shot_like.get('animations'), dict) else {}, MOVES))
    for component in shot_like.get('transforms') or []:
        if isinstance(component, dict) and isinstance(component.get('animations'), dict):
            component_tracks = list(_tracks(component['animations'], MOVES))
            if not any(k in component['animations'] for k in ('scale', 'rotation', 'rotationX', 'rotationY')) and component.get('scale', [1, 1]) == [1, 1] and all(not component.get(k, 0) for k in ('rotation', 'rotationX', 'rotationY')):
                component_tracks = [(p, t) for p, t in component_tracks if p != 'anchor']
            tracks += component_tracks
    for prop, value in shot_like.items():
        if prop in MOVES and isinstance(value, dict) and ('keyframes' in value or 'expression' in value):
            tracks.append((prop, value))  # a camera field written as a track
    if any(p == 'position' and len(t.get('keyframes') or []) >= 2 for p, t in tracks) and any(p == 'translation' and len(t.get('keyframes') or []) >= 2 for p, t in tracks):
        unchecked.append({'code': 'pop-move', 'why': f'{where}: composed position and translation motion needs rendered review'})
        tracks = [(p, t) for p, t in tracks if p not in ('position', 'translation')]
    out: List[_Move] = []
    frame = 1.0 / fps
    for prop, track in tracks:
        if track.get('expression'):
            unchecked.append({'code': 'pop-move', 'why': f'{where} {prop} is driven by an expression; only its frames show how it moves'})
            continue
        if any(k.get('inTangent') or k.get('outTangent') for k in track.get('keyframes') or [] if isinstance(k, dict)):
            for code in ('pop-move', 'zoom-idle'):
                unchecked.append({'code': code, 'why': f'{where} {prop} has spatial tangents; its motion needs rendered frames'})
            continue
        keys = [k for k in track.get('keyframes') or [] if isinstance(k, dict) and _num(k.get('time'))
                and _vector(k.get('value')) is not None]
        keys.sort(key=lambda k: float(k['time']))
        if len(keys) < 2:
            continue
        base = _key_zero(shot_like, track, start, zero)
        times = [base + float(k['time']) * rate for k in keys]
        values = [_vector(k['value']) for k in keys]
        changes = [_changes(prop, a, b) for a, b in zip(values, values[1:])]
        # Dense sampled keys may each fall below the visible threshold. Preserve their
        # nonzero segments when the track's total range is visibly significant.
        if values and all(len(v) == len(values[0]) for v in values):
            visible = ([_track_at(track, base, rate, start)]
                       + [_track_at(track, base, rate, t) for t in times if start < t < end]
                       + [_track_at(track, base, rate, end, step_left=True)])
            significant = [max(v[j] for v in visible) - min(v[j] for v in visible) > MOVES[prop]
                           for j in range(len(values[0]))]
            changes = [[significant[j] and abs(a[j] - b[j]) > EPS for j in range(len(a))]
                       for a, b in zip(values, values[1:])]
        for i, moving in enumerate(changes):
            if not any(moving):
                continue
            before = (times[i] > start + frame - EPS) if i == 0 else (not any(changes[i - 1]) or not _abrupt(keys[i - 1].get('easing', 'linear'), changes[i - 1], _slope_end))
            last = i + 1 == len(keys) - 1
            after = (times[i + 1] < end - frame + EPS) if last else (not any(changes[i + 1]) or not _abrupt(keys[i + 1].get('easing', 'linear'), changes[i + 1], _slope_start))
            span = times[i + 1] - times[i]
            speed = math.dist(values[i], values[i + 1]) / span if span > EPS and len(values[i]) == len(values[i + 1]) else 0.0
            easing = keys[i].get('easing', 'linear')
            a, b = max(start, times[i]), min(end, times[i + 1])
            if easing == 'step':
                if not start + EPS < times[i + 1] < end:
                    continue
            elif b <= a + EPS:
                continue
            move = _Move(prop, a, b, easing, moving,
                         before and times[i] >= start, after and times[i + 1] < end, speed)
            neighbors = [math.dist(values[j], values[j + 1]) / (times[j + 1] - times[j])
                         for j in (i - 1, i + 1) if 0 <= j < len(changes)
                         and times[j + 1] - times[j] > EPS and len(values[j]) == len(values[j + 1])]
            move.frame_jump = (span <= frame + EPS and any(_changes(prop, values[i], values[i + 1]))
                               and times[i] > start + EPS and times[i + 1] < end - EPS
                               and all(speed > 2 * neighbor + EPS for neighbor in neighbors))
            out.append(move)
    _ramps(out)
    return out


def _ramps(found: List[_Move]) -> None:
    """Mark the ends of each run of linear keys whose sampled speed ramps up or down there."""
    runs: List[List[_Move]] = []
    for m in found:
        if runs and runs[-1][-1].prop == m.prop and abs(runs[-1][-1].end - m.start) <= EPS and not runs[-1][-1].rest_after:
            runs[-1].append(m)
        else:
            runs.append([m])
    for run in runs:
        if len(run) < 2 or any(not all(e in ('linear', None) for e in (m.easing if isinstance(m.easing, list) else [m.easing])) for m in run):
            continue
        peak = max(m.speed for m in run)
        run[0].ramped_in = run[0].speed < SAMPLED_PEAK * peak
        run[-1].ramped_out = run[-1].speed < SAMPLED_PEAK * peak


# --- the input ----------------------------------------------------------------------------------


SPAN = re.compile(r'(\d+(?:\.\d*)?|\.\d+)-(\d+(?:\.\d*)?|\.\d+)')


def parse_span(text: str) -> Span:
    match = SPAN.fullmatch(text)
    if match:
        start, end = map(float, match.groups())
        if math.isfinite(end) and start < end:
            return start, end
    raise InputError(f'expected START-END with 0 <= START < END, got {text!r}')


def allowed_spans(value: Any) -> List[Tuple[float, float, Optional[str]]]:
    if value is None:
        return []
    if isinstance(value, dict):
        value = value.get('spans', value.get('allowed'))
    if not isinstance(value, list):
        raise InputError('`allowed` must be a list of {start, end} spans')
    out = []
    for item in value:
        if isinstance(item, dict):
            start, end, file = item.get('start'), item.get('end'), item.get('file')
        elif isinstance(item, list) and len(item) == 2:
            (start, end), file = item, None
        else:
            raise InputError(f'an allowed span must be {{start, end}}: {item!r}')
        if not (_num(start) and _num(end)) or not (0 <= start < end) or not math.isfinite(end):
            raise InputError(f'an allowed span needs 0 <= start < end: {item!r}')
        out.append((float(start), float(end), file if isinstance(file, str) and file else None))
    return out


# --- the checks ---------------------------------------------------------------------------------


def finding(code: str, start: float, end: float, layers: List[str], message: str) -> Dict[str, Any]:
    return {'code': code, 'start': start, 'end': end, 'layers': layers,
            'message': message, 'fix': FIX[code]}


def _same_file(shot: _Shot, file: str) -> bool:
    for name in (shot.uri, shot.asset):
        if name and (name == file or name.endswith('/' + file.rsplit('/', 1)[-1])):
            return True
    return False


def screen_still(shots: List[_Shot], spans: List[Tuple[float, float, Optional[str]]], fps: float) -> List[Dict[str, Any]]:
    """Inside each allowed span, the stretches where its screen clip holds one picture."""
    out = []
    frozen: List[Tuple[Span, List[str]]] = []
    for start, end, file in spans:
        screens = [s for s in shots if s.kind == 'media' and s.start < end and s.end > start
                   and (file is None or _same_file(s, file))]
        if not screens:
            continue
        still = [piece for span in all_still([_still_shot(s, fps) for s in screens])
                 for piece in intersect([span], [(start, end)])]
        frozen += [(span, sorted({s.id for s in screens if s.start < span[1] and s.end > span[0]})) for span in still]
    # Spans that touch or overlap join, so two halves of one hold count as one.
    joined: List[Tuple[Span, List[str]]] = []
    for (a, b), ids in sorted(frozen):
        if joined and ids == joined[-1][1] and a <= joined[-1][0][1] + EPS:
            (x, y), old = joined[-1]
            joined[-1] = ((x, max(y, b)), sorted(set(old) | set(ids)))
        else:
            joined.append(((a, b), ids))
    for (a, b), ids in joined:
        if b - a + EPS >= SCREEN_SECONDS:
            out.append(finding('screen-still', a, b, ids, f'screen holds still for {b - a:.2f} s; '
                               'the viewer may think the video paused'))
    return out


class _StillView(_Shot):
    """A shot whose still stretches leave out where it moves on screen."""

    def __init__(self, shot: _Shot, still: List[Span]) -> None:  # noqa: super is not called on purpose
        self.__dict__.update(shot.__dict__)
        self._still = still

    def still(self) -> List[Span]:
        return self._still


def _still_shot(shot: _Shot, fps: float) -> _Shot:
    moving = [(m.end, m.end + 1 / fps) if m.easing == 'step' else (m.start, m.end)
              for m in moves(shot.layer, shot.zero, shot.rate, shot.start, shot.end, fps, [], shot.id)]
    return _StillView(shot, subtract(shot.still(), moving))


def _ease(easing: Any, f: float) -> float:
    """How far along a segment its value is at share f of its time, under the key's easing."""
    if easing == 'step':
        return 0.0
    named = {'ease_in': [0.42, 0, 1, 1], 'ease_out': [0, 0, 0.58, 1], 'ease_in_out': [0.42, 0, 0.58, 1]}
    control = named.get(easing) if isinstance(easing, str) else \
        easing.get('control') if isinstance(easing, dict) and easing.get('kind') == 'cubic_bezier' else None
    if not isinstance(control, list) or len(control) != 4 or not all(_num(c) for c in control):
        return f
    x1, y1, x2, y2 = control
    lo, hi = 0.0, 1.0
    for _ in range(24):
        u = (lo + hi) / 2
        if 3 * (1 - u) ** 2 * u * x1 + 3 * (1 - u) * u ** 2 * x2 + u ** 3 < f:
            lo = u
        else:
            hi = u
    u = (lo + hi) / 2
    return 3 * (1 - u) ** 2 * u * y1 + 3 * (1 - u) * u ** 2 * y2 + u ** 3


def _track_at(track: Any, key_zero: float, rate: float, t: float, step_left: bool = False) -> Optional[List[float]]:
    """A keyframed value at time t on the cut's clock, eased as authored; None with no keys to read."""
    if not isinstance(track, dict) or track.get('expression'):
        return None
    keys = [(key_zero + float(k['time']) * rate, _vector(k.get('value')), k.get('easing', 'linear'))
            for k in track.get('keyframes') or [] if isinstance(k, dict) and _num(k.get('time')) and _vector(k.get('value')) is not None]
    keys.sort(key=lambda k: k[0])
    if not keys:
        return None
    if t <= keys[0][0]:
        return keys[0][1]
    for (t0, v0, easing), (t1, v1, _) in zip(keys, keys[1:]):
        if step_left and t0 < t == t1 and len(v0) == len(v1):
            return [x if (easing[i] if isinstance(easing, list) and i < len(easing) else easing) == 'step' else y
                    for i, (x, y) in enumerate(zip(v0, v1))]
        if t0 <= t < t1:
            if len(v0) != len(v1):
                return v0
            f = (t - t0) / (t1 - t0)
            return [x + (y - x) * _ease(easing[i] if isinstance(easing, list) and i < len(easing) else easing, f)
                    for i, (x, y) in enumerate(zip(v0, v1))]
    return keys[-1][1]


def _value_at(layer: Dict[str, Any], prop: str, zero: float, rate: float, t: float) -> Optional[List[float]]:
    track = (layer.get('animations') or {}).get(prop) or {}
    if track.get('expression'):
        raise InputError(f'{prop} expression needs rendered geometry')
    return (_track_at(track, _key_zero(layer, track, 0.0, zero), rate, t)
            or _vector((layer.get('transform') or {}).get(prop)))


def _component_at(layer: Dict[str, Any], component: Dict[str, Any], prop: str,
                  zero: float, rate: float, t: float) -> Optional[List[float]]:
    track = (component.get('animations') or {}).get(prop) or {}
    if track.get('expression'):
        raise InputError(f'{prop} expression needs rendered geometry')
    return (_track_at(track, _key_zero(layer, track, 0.0, zero), rate, t)
            or _vector(component.get(prop)))


def _size(value: Any) -> Optional[Tuple[float, float]]:
    if isinstance(value, list) and len(value) == 2 and all(_num(v) for v in value):
        return abs(float(value[0])), abs(float(value[1]))
    return None


def _extent(content: Dict[str, Any]) -> Optional[Tuple[float, float]]:
    """How big a layer is on its own canvas, from `bounds`, a color's `size`, or a shape's items."""
    for field in ('bounds', 'size'):
        got = _size(content.get(field))
        if got:
            return got
    items = [i for i in content.get('items') or [] if isinstance(i, dict)]
    sizes = [g for g in (_size(i.get('size')) for i in items) if g]
    if sizes:
        return max(w for w, _ in sizes), max(h for _, h in sizes)
    points = [v.get('point') for i in items for v in i.get('vertices') or [] if isinstance(v, dict)]
    points = [p for p in points if _size(p) is not None or (isinstance(p, list) and len(p) == 2 and all(_num(c) for c in p))]
    if len(points) >= 2:
        return (max(p[0] for p in points) - min(p[0] for p in points), max(p[1] for p in points) - min(p[1] for p in points))
    return None


def _canvas(container: Dict[str, Any], fallback: Optional[Tuple[float, float]]) -> Optional[Tuple[float, float]]:
    """The size of the scene a nested scene or group draws in."""
    content = container.get('content') or {}
    assets = getattr(container, 'assets', {}) or {}
    asset = content.get('asset') or assets.get(content.get('assetId')) or {}
    comp = content.get('composition') if content.get('kind') == 'composition' else (asset.get('scene') or {}).get('composition')
    if isinstance(comp, dict) and _num(comp.get('width')) and _num(comp.get('height')) and comp['width'] > 0 and comp['height'] > 0:
        return float(comp['width']), float(comp['height'])
    return fallback


def _native_extent(layer: Dict[str, Any]) -> Tuple[float, float]:
    """With fit:none there is no destination box: use the media or scene's intrinsic size."""
    content = layer.get('content') or {}
    if content.get('kind') in ('composition', 'scene_ref'):
        size = _canvas(layer, None)
    else:
        assets = getattr(layer, 'assets', {}) or {}
        asset = content.get('asset') or assets.get(content.get('assetId')) or {}
        size = _size([asset.get('width'), asset.get('height')])
    if not size or min(size) <= 0:
        raise InputError('fit:none intrinsic size is unknown; coverage needs rendered geometry')
    return size


def _placed_extent(container: Dict[str, Any], parent: Tuple[float, float], inner: Tuple[float, float],
                   extent: Tuple[float, float], t: float) -> Tuple[float, float]:
    """
    How big a box on a nested scene's canvas shows on its parent canvas: scaled by the scene's fit,
    clipped to its box, scaled by the scene's own scale at time t, and clipped to the parent.
    """
    content = container.get('content') or {}
    box = _extent(content) or (_native_extent(container) if content.get('fit') == 'none' else parent)
    fit = content.get('fit', 'contain')
    if fit == 'none':
        kx = ky = 1.0
    elif fit == 'stretch':
        kx, ky = box[0] / inner[0], box[1] / inner[1]
    else:
        kx = ky = (max if fit == 'cover' else min)(box[0] / inner[0], box[1] / inner[1])
    w, h = min(extent[0] * kx, box[0]), min(extent[1] * ky, box[1])
    return _viewport_extent(container, parent, (w, h), getattr(container, 'placed_zero', 0.0),
                            getattr(container, 'rate', 1.0), t)


def _parent_layers(layer, layers):
    """Resolve transform-only parents among siblings, rejecting unrenderable chains."""
    seen = {id(layer)}
    while layer.get('parentId') is not None:
        parent_id = layer['parentId']
        parent = layers.get((getattr(layer, 'scope', None), str(parent_id)))
        if parent is None:
            raise InputError(f'missing parent {parent_id!r} in this composition')
        if id(parent) in seen:
            raise InputError(f'parent cycle through {parent_id!r}')
        # An inline composition renders as a scene_ref, so neither lends a parent geometry.
        if (parent.get('content') or {}).get('kind') in ('scene_ref', 'composition', 'track') or parent.get('mask') is not None:
            raise InputError(f'parent {parent_id!r} is a scene_ref, composition, track or masked layer; no parent geometry')
        seen.add(id(parent))
        yield parent
        layer = parent


def _parent_extent(layer, canvas):
    # The renderer's parent pivot: an authored anchor, else the content box's
    # centre. Text, shapes and empty control layers (drawn as a 0x0 solid) have
    # no box, so they pivot at their own origin.
    content = layer.get('content') or {}
    if content.get('kind') in ('empty', 'text', 'shape'):
        return (0.0, 0.0)
    return _extent(content) or (_native_extent(layer) if content.get('fit') == 'none' else canvas)


def _place_edges(layer, canvas, extent, zero, rate, t, edges, depth=None):
    position = _value_at(layer, 'position', zero, rate, t) or [canvas[0] / 2, canvas[1] / 2]
    anchor = _value_at(layer, 'anchor', zero, rate, t) or [extent[0] / 2, extent[1] / 2]
    scale = ((_value_at(layer, 'scale', zero, rate, t) or [1.0]) * 2)[:2]
    components = [c for c in layer.get('transforms') or [] if isinstance(c, dict)]
    for prop in ('rotation', 'rotationX', 'rotationY'):
        values = []
        if prop == 'rotation' or prop in (layer.get('animations') or {}):
            values.append(_value_at(layer, prop, zero, rate, t))
        values += [_component_at(layer, c, prop, zero, rate, t) for c in components
                   if prop == 'rotation' or prop in (c.get('animations') or {})]
        if any(abs(v) > EPS for value in values if value for v in value):
            raise InputError('rotated coverage needs rendered geometry')
    edges = [[pos + (v - pivot) * k for v in edge]
             for edge, pos, pivot, k in zip(edges, position, anchor, scale)]
    def foreshorten(edges, values, pivot, record_depth=True):
        # Approximate static 3D turns orthographically about the transform pivot.
        for axis, prop in enumerate(('rotationY', 'rotationX')):
            angle = _vector(values.get(prop))
            if angle:
                centre = pivot[axis]
                if depth is not None and record_depth:
                    depth[0] = max(depth[0], max(abs(v - centre) for v in edges[axis]) * abs(math.sin(math.radians(angle[0]))))
                factor = math.cos(math.radians(angle[0]))
                edges[axis] = sorted(centre + (v - centre) * factor for v in edges[axis])
        return edges

    edges = foreshorten(edges, {prop: value for prop, value in (layer.get('transform') or {}).items()
                                if prop not in (layer.get('animations') or {})}, position)
    # Components are parent-space wrappers, in order, pivoting about the current placement
    # anchor unless they declare a fixed parent-space anchor of their own.
    for component in components:
        pivot = _component_at(layer, component, 'anchor', zero, rate, t) or position
        scale = ((_component_at(layer, component, 'scale', zero, rate, t) or [1.0]) * 2)[:2]
        translation = _component_at(layer, component, 'translation', zero, rate, t) or [0.0, 0.0]
        edges = [[p + (v - p) * k + d for v in edge] for edge, p, k, d in zip(edges, pivot, scale, translation)]
        position = [p + (v - p) * k + d for v, p, k, d in zip(position, pivot, scale, translation)]
        static = {prop: value for prop, value in component.items()
                  if prop not in (component.get('animations') or {})}
        centre = [p + d for p, d in zip(pivot, translation)]
        edges = foreshorten(edges, static, centre)
        position = [edge[0] for edge in foreshorten([[v, v] for v in position], static, centre, False)]
    return edges


def _viewport_extent(layer: Dict[str, Any], canvas: Tuple[float, float], extent: Tuple[float, float],
                     zero: float, rate: float, t: float, parents=(), offset=(0.0, 0.0)) -> Tuple[float, float]:
    """Intersect the placed box with its viewport; anchors are in the box's own pixels."""
    edges = _place_edges(layer, canvas, extent, zero, rate, t, [[d, d + w] for d, w in zip(offset, extent)])
    for parent in parents:
        parent_zero, parent_rate = getattr(parent, 'placed_zero', 0.0), getattr(parent, 'rate', 1.0)
        box = (0.0, 0.0) if _value_at(parent, 'anchor', parent_zero, parent_rate, t) is not None else _parent_extent(parent, canvas)
        edges = _place_edges(parent, canvas, box, parent_zero, parent_rate, t, edges)
    shown_size = []
    for edge, bound in zip(edges, canvas):
        a, b = sorted(edge)
        shown_size.append(max(0.0, min(b, bound) - max(a, 0.0)))
    return tuple(shown_size)


def _mask_intersection(edges, layer, canvas, t):
    """Intersect with a static shape matte in the host's parent canvas."""
    mask = layer.get('mask')
    if mask is None:
        return edges
    try:
        if not isinstance(mask, dict) or set(mask) - {'layer', 'clip'} or len(mask) != 1:
            raise ValueError()
        matte = mask.get('layer') or mask.get('clip')
        if not isinstance(matte, dict) or matte.get('animations') or matte.get('transforms') or matte.get('mask') or matte.get('parentId') is not None:
            raise ValueError()
        transform = matte.get('transform') or {}
        if not isinstance(transform, dict) or any(isinstance(v, dict) for v in transform.values()):
            raise ValueError()
        content = matte.get('content') or {}
        items = content.get('items') or []
        if content.get('kind') != 'shape' or not isinstance(items, list) or any(not isinstance(i, dict) or i.get('animations') for i in items):
            raise ValueError()
        shapes = [i for i in items if i.get('type') in ('rect', 'ellipse')]
        if len(shapes) != 1 or any(i.get('type') not in ('rect', 'ellipse', 'fill') for i in items):
            raise ValueError()
        opacity = transform.get('opacity', 1)
        fills = [i for i in items if i.get('type') == 'fill']
        alphas = []
        for fill in fills:
            color = fill.get('color', '#ffffff')
            alpha = fill.get('opacity', 1)
            if not _num(alpha) or not 0 <= alpha <= 1:
                raise ValueError()
            # The format's colours are RGB, with transparency in the item's opacity. A colour
            # that still carries an alpha channel counts too, and any other colour is opaque.
            color = color.strip().lower() if isinstance(color, str) else ''
            if re.fullmatch(r'#[0-9a-f]{8}', color):
                alpha *= int(color[-2:], 16) / 255
            elif re.fullmatch(r'#[0-9a-f]{4}', color):
                alpha *= int(color[-1], 16) / 15
            elif color == 'transparent':
                alpha = 0
            alphas.append(alpha)
        if not _num(opacity) or not 0 <= opacity <= 1:
            raise ValueError()
        if opacity == 0 or (alphas and all(alpha == 0 for alpha in alphas)):
            return [[0.0, 0.0], [0.0, 0.0]]
        if opacity < 1 or any(alpha < 1 for alpha in alphas):
            raise ValueError()
        shape = shapes[0]
        extent = _size(shape.get('size'))
        offset = _vector(shape.get('position')) if shape.get('position') is not None else [0, 0]
        if not extent or min(extent) <= 0 or not offset or len(offset) != 2:
            raise ValueError()
        box = _place_edges(matte, canvas, (0.0, 0.0), 0, 1, t,
                           [[d - w / 2, d + w / 2] for d, w in zip(offset, extent)])
        return [[max(min(a), min(b)), max(max(min(a), min(b)), min(max(a), max(b)))]
                for a, b in zip(edges, box)]
    except (ValueError, TypeError, InputError):
        raise InputError('masked coverage needs rendered geometry')


def _cover(shot: _Shot, frame_size: Optional[Tuple[float, float]], t: float, layers=None, camera=None,
           descendants=None, return_edges=False, perspective=False) -> float:
    """
    The share of the frame a layer covers at time t: its shown extent times its scale, or all of its
    scene with no extent (footage), carried out through every nested scene's fit and scale.
    """
    if shot.kind in ('composition', 'scene_ref', 'track'):
        if descendants is None or not frame_size:
            raise InputError('container descendant coverage needs rendered geometry')
        if shot.kind == 'scene_ref' and not isinstance((shot.content.get('asset') or
                (getattr(shot.layer, 'assets', {}) or {}).get(shot.content.get('assetId')) or {}).get('scene'), dict):
            raise InputError('container descendant coverage needs rendered geometry')
        inside = [s for s in descendants if any(c is shot.layer for c in s.containers)
                  and s.start <= t < s.end]
        for child in inside:
            if child.kind == 'scene_ref' and not isinstance((child.content.get('asset') or
                    (getattr(child.layer, 'assets', {}) or {}).get(child.content.get('assetId')) or {}).get('scene'), dict):
                raise InputError('container descendant coverage needs rendered geometry')
        for container in [shot] + inside:
            if container.kind not in ('composition', 'scene_ref'):
                continue
            content = container.content
            canvas = content if container.kind == 'composition' else (content.get('asset') or (getattr(container.layer, 'assets', {}) or {}).get(content.get('assetId')) or {}).get('scene') or {}
            background = (canvas.get('composition') or {}).get('background')
            if (isinstance(background, str) and background.strip().lower() not in ('', 'transparent')
                    and not re.fullmatch(r'#(?:[0-9a-f]{3}0|[0-9a-f]{6}00)', background.strip().lower())):
                raise InputError('container background coverage needs rendered geometry')
        children = [s for s in inside if s.kind not in ('composition', 'scene_ref', 'track')]
        boxes = []
        for child in children:
            if child.kind not in ('media', 'shape', 'color') or child.layer.get('parentId') is not None:
                raise InputError('container descendant coverage needs rendered geometry')
            try:
                boxes.append(_cover(child, frame_size, t, camera=camera if camera and _camera_affected(
                    child, getattr(camera, 'scope', shot.layer.scope), layers or {}) else None,
                    return_edges=True, perspective=perspective))
            except InputError as err:
                raise InputError(f'container descendant coverage: {err}')
        boxes = [box for box in boxes if all(edge[1] > edge[0] for edge in box)]
        xs = sorted({x for box in boxes for x in box[0]})
        area = 0.0
        for left, right in zip(xs, xs[1:]):
            intervals = sorted(box[1] for box in boxes if box[0][0] < right and box[0][1] > left)
            height = 0.0
            end = 0.0
            for start, stop in intervals:
                height += max(0.0, stop - max(start, end))
                end = max(end, stop)
            area += (right - left) * height
        return area / (frame_size[0] * frame_size[1])
    if layers is not None and shot.containers:
        raise InputError('inherited nested container coverage needs rendered geometry')
    if shot.layer.get('mask') is not None and shot.layer.get('parentId') is not None:
        raise InputError('masked coverage needs rendered geometry')
    if shot.kind == 'shape' and any(i.get('type') == 'group' for i in shot.content.get('items') or [] if isinstance(i, dict)):
        raise InputError('grouped shape coverage needs rendered geometry')
    if not frame_size:
        return 1.0 if shot.kind in FOOTAGE else 0.0
    canvases = [frame_size]
    chain = list(shot.containers)
    for c in chain:
        kind = (c.get('content') or {}).get('kind')
        canvases.append(canvases[-1] if kind == 'track' else
                        _native_extent(c) if (c.get('content') or {}).get('fit') == 'none' else _canvas(c, canvases[-1]))
    parents = list(_parent_layers(shot.layer, layers)) if layers is not None else []
    owners = [shot.layer] + parents + chain
    tilted = sum(1 for owner in owners
                 for holder in [owner.get('transform') or {}] + [c for c in owner.get('transforms') or [] if isinstance(c, dict)]
                 if any(abs(v) > EPS for prop in ('rotationX', 'rotationY')
                        for v in (_vector(holder.get(prop)) or [])))
    if tilted > 1:
        raise InputError('composed 3D coverage needs rendered geometry')
    extent = _extent(shot.content)
    contain_box = None
    if not extent and shot.kind in FOOTAGE and shot.content.get('fit') == 'none':
        extent = _native_extent(shot.layer)
    if not extent and shot.kind == 'media' and shot.content.get('fit') == 'contain':
        try:
            native = _native_extent(shot.layer)
        except InputError:
            raise InputError('contain-fit intrinsic size is unknown; coverage needs rendered geometry')
        factor = min(canvases[-1][0] / native[0], canvases[-1][1] / native[1])
        extent = (native[0] * factor, native[1] * factor)
        contain_box = canvases[-1]
    if not extent:
        if shot.kind in FOOTAGE or shot.kind == 'color':
            extent = canvases[-1]
        else:
            if shot.kind in ('text', 'captions'):
                raise InputError('text coverage needs rendered geometry')
            if return_edges:
                raise InputError('descendant box is unknown; coverage needs rendered geometry')
            return 0.0
    offset = tuple((b - e) / 2 for b, e in zip(contain_box, extent)) if contain_box else (0.0, 0.0)
    box = contain_box or extent
    if shot.kind == 'shape':
        items = [i for i in shot.content.get('items') or [] if isinstance(i, dict) and _size(i.get('size'))]
        positioned = [i for i in items if i.get('position') is not None]
        if positioned:
            if len(items) != 1 or len(_vector(positioned[0].get('position')) or []) != 2:
                raise InputError('multiple positioned shape items need rendered geometry')
            offset = positioned[0]['position'][:2]
            if positioned[0].get('type') in ('rect', 'ellipse'):
                offset = [p - w / 2 for p, w in zip(offset, extent)]
                box = (0.0, 0.0)
    depth = [0.0] if perspective else None
    edges = _place_edges(shot.layer, canvases[-1], box, shot.zero, shot.rate, t,
                         [[d, d + w] for d, w in zip(offset, extent)], depth)
    edges = _mask_intersection(edges, shot.layer, canvases[-1], t)
    for parent in parents:
        zero, rate = getattr(parent, 'placed_zero', 0.0), getattr(parent, 'rate', 1.0)
        box = (0.0, 0.0) if _value_at(parent, 'anchor', zero, rate, t) is not None else _parent_extent(parent, canvases[-1])
        edges = _place_edges(parent, canvases[-1], box, zero, rate, t, edges, depth)
    def clip(edges, bounds):
        return [[max(0.0, min(bound, min(edge))), max(0.0, min(bound, max(edge)))]
                for edge, bound in zip(edges, bounds)]
    for i in range(len(chain) - 1, -1, -1):
        container, parent, inner = chain[i], canvases[i], canvases[i + 1]
        content = container.get('content') or {}
        if content.get('kind') == 'track':
            box = parent
        else:
            edges = clip(edges, inner)
            box = _extent(content) or (_native_extent(container) if content.get('fit') == 'none' else parent)
            fit = content.get('fit', 'contain')
            if fit == 'none':
                kx = ky = 1.0
            elif fit == 'stretch':
                kx, ky = box[0] / inner[0], box[1] / inner[1]
            else:
                kx = ky = (max if fit == 'cover' else min)(box[0] / inner[0], box[1] / inner[1])
            edges = [[(v - size / 2) * k + dest / 2 for v in edge]
                     for edge, size, k, dest in zip(edges, inner, (kx, ky), box)]
            edges = clip(edges, box)
        edges = _place_edges(container, parent, box, getattr(container, 'placed_zero', 0.0),
                             getattr(container, 'rate', 1.0), t, edges, depth)
        edges = _mask_intersection(edges, container, parent, t)
    if camera:
        for prop in ('zoom', 'position', 'rotation', 'rotationX', 'rotationY', 'distance'):
            if isinstance(camera.get(prop), dict) or (camera.get('animations') or {}).get(prop):
                raise InputError('animated camera coverage needs rendered geometry')
        if any(abs(v) > EPS for prop in ('rotation', 'rotationX', 'rotationY')
               for v in (_vector(camera.get(prop)) or [])) or _has_depth(shot.layer):
            raise InputError('3D or rotated camera coverage needs rendered geometry')
        zoom = camera.get('zoom', 1.0)
        pivot = _vector(camera.get('position')) or [frame_size[0] / 2, frame_size[1] / 2]
        if not _num(zoom) or len(pivot) < 2:
            raise InputError('camera coverage needs rendered geometry')
        edges = [[p + zoom * (v - p) for v in edge] for edge, p in zip(edges, pivot)]
    unclipped = math.prod(abs(edge[1] - edge[0]) for edge in edges) / (frame_size[0] * frame_size[1])
    edges = clip(edges, frame_size)
    if perspective and depth[0] > EPS:
        share = math.prod(edge[1] - edge[0] for edge in edges) / (frame_size[0] * frame_size[1])
        distance = camera.get('distance', frame_size[0] * 50 / 36) if camera else frame_size[0] * 50 / 36
        if not _num(distance) or distance <= 0:
            raise InputError('camera distance needs rendered geometry')
        s_min = distance / (distance + depth[0])
        s_max = distance / (distance - depth[0]) if depth[0] < distance else math.inf
        if share * s_min ** 2 < POP_COVER and not (unclipped <= EPS or unclipped * s_max ** 2 < POP_COVER):
            raise InputError('3D-rotated coverage near the pop-move threshold needs perspective geometry')
    if return_edges:
        return edges
    return math.prod(edge[1] - edge[0] for edge in edges) / (frame_size[0] * frame_size[1])

def _camera_affected(shot: _Shot, scope: Any, parents: Dict[Any, Any]) -> bool:
    """A camera moves its scope's owners, stopping at a rendered canvas boundary."""
    owners = shot.containers + (shot.layer,)
    boundary = next((i for i, owner in enumerate(owners) if owner.scope == scope), -1)
    if boundary < 0:
        return False
    for owner in owners[boundary:]:
        node, chain = owner, set()
        while node is not None:
            if node.get('cameraExempt'):
                return False
            key = (node.scope, node.get('parentId'))
            if key in chain:
                break
            chain.add(key)
            node = parents.get(key)
        content = owner.get('content') or {}
        if content.get('kind') == 'scene_ref' or (
                content.get('kind') == 'composition' and isinstance(content.get('composition'), dict)):
            break
    return True


def _exempt_inside_canvas(shot: _Shot, scope: Any) -> bool:
    """Marked cameraExempt below the camera's own layer, where a canvas boundary overrides it."""
    owners = shot.containers + (shot.layer,)
    boundary = next((i for i, owner in enumerate(owners) if owner.scope == scope), -1)
    return boundary >= 0 and any(owner.get('cameraExempt') for owner in owners[boundary + 1:])


def _camera_shots(shots: List[_Shot], scope: Any, parents: Dict[Any, Any]) -> List[_Shot]:
    return [s for s in shots if s.kind in {'media'} | OVERLAYS and _camera_affected(s, scope, parents)]


def _projected(shot: _Shot, scope: Any, parents=None) -> Tuple[Dict[str, Any], ...]:
    """The shot's owners this camera projects: its canvas boundary and what sits inside it."""
    owners = shot.containers + (shot.layer,)
    boundary = next((i for i, owner in enumerate(owners) if owner.scope == scope), 0)
    projected = []
    for owner in owners[boundary:]:
        projected.append(owner)
        if parents is not None:
            projected.extend(_parent_layers(owner, parents))
        content = owner.get('content') or {}
        if content.get('kind') in ('scene_ref', 'composition'):
            break
    return tuple(projected)


def _identity_pivot(camera: Dict[str, Any], shots: List[_Shot], t: float, unit_zoom: bool = True,
                    scope: Any = None, parents=None) -> bool:
    """A pivot at unit zoom, or distance at any zoom, has no effect on the unrotated z=0 plane."""
    identity = True
    # A roll turns the picture in its own plane, so it changes what a pivot does but not what
    # distance does: only a tilt gives distance a projection effect.
    props = [('rotationX', 0), ('rotationY', 0)] + ([('rotation', 0), ('zoom', 1)] if unit_zoom else [])
    for prop, default in props:
        value = (camera.get('animations') or {}).get(prop, camera.get(prop, default))
        if isinstance(value, dict):
            if value.get('expression'):
                raise InputError(f'camera {prop} expression needs rendered movement')
            zero, rate = getattr(camera, 'placed_zero', 0.0), getattr(camera, 'rate', 1.0)
            value = (_track_at(value, _key_zero(camera, value, 0.0, zero), rate, t) or [default])[0]
        if abs(value - default) > EPS:
            identity = False
    for shot in shots:
        if not shot.start <= t < shot.end:
            continue
        for layer in _projected(shot, scope, parents):
            zero, rate = getattr(layer, 'placed_zero', shot.zero), getattr(layer, 'rate', shot.rate)
            for prop in ('z', 'rotationX', 'rotationY'):
                try:
                    values = [_value_at(layer, prop, zero, rate, t)] + [
                        _component_at(layer, c, prop, zero, rate, t) for c in layer.get('transforms') or [] if isinstance(c, dict)]
                except InputError:
                    raise InputError('depth expression needs rendered camera movement')
                if any(abs(v) > EPS for value in values if value for v in value):
                    identity = False
    return identity


def _has_depth(layer: Dict[str, Any]) -> bool:
    """Any depth, distance or 3D turn, static or keyframed, anywhere in the layer's transforms."""
    def walk(node: Any) -> bool:
        if isinstance(node, list):
            return any(walk(v) for v in node)
        if not isinstance(node, dict):
            return False
        for key, value in node.items():
            if key in DEPTH_PROPS and value is not None:
                vector = _vector(value)
                if vector is None or any(abs(v) > EPS for v in vector):
                    return True
            elif walk(value):
                return True
        return False
    return walk([layer.get('transform'), layer.get('animations'), layer.get('transforms')])


def pop_move(shots: List[_Shot], cameras: List[_Shot], fps: float,
             unchecked: List[Dict[str, str]], frame_size: Optional[Tuple[float, float]] = None,
             all_layers: Optional[Dict[Any, Any]] = None, seam_shots: Optional[List[_Shot]] = None) -> List[Dict[str, Any]]:
    out = []
    frame = 1.0 / fps
    layers = all_layers if all_layers is not None else {(s.scope, s.id): s.layer for s in shots}
    sources = []
    root_scope = next((s.scope for s in (seam_shots if seam_shots is not None else shots) if not s.containers), None)
    root_camera = next((c.layer for c in cameras if c.scope is root_scope), None)
    frozen = {}
    picture_joins = seams(seam_shots if seam_shots is not None else shots, fps, [], frame_size, root_camera)
    for seam in picture_joins:
        transition = seam.transition or {}
        length = transition.get('duration')
        if transition.get('id') and _num(length) and length > 0:
            window = (seam.time - length * seam.a.rate / 2, seam.time + length * seam.a.rate / 2)
            for shot in (seam.a, seam.b):
                frozen.setdefault(id(shot.layer), []).append(window)

    def inherited_cover(t: float, s: _Shot, return_edges=False) -> float:
        # Inherited geometry is proven only for flat empty rigs: with a camera, a boxed parent,
        # transform components, or depth or a 3D turn anywhere in the chain, it is not modelled,
        # and main reports none of it.
        if any(_camera_affected(s, camera.scope, layers) for camera in cameras):
            raise InputError('camera-projected coverage needs rendered geometry')
        chain = tuple(_parent_layers(s.layer, layers))
        if any((p.get('content') or {}).get('kind') != 'empty' for p in chain):
            raise InputError('coverage under a parent that is not an empty rig needs rendered geometry')
        if any(layer.get('transforms') for layer in (s.layer,) + chain):
            raise InputError('inherited coverage through transform components needs rendered geometry')
        if any(_has_depth(layer) for layer in (s.layer,) + chain):
            raise InputError('depth or 3D-rotated coverage needs rendered geometry')
        return _cover(s, frame_size, t, layers, return_edges=return_edges)

    def rig_cover(t, parent):
        if not frame_size:
            raise InputError('rig coverage needs frame dimensions')
        boxes = []
        for child in shots:
            if child.kind not in FOOTAGE | OVERLAYS or not child.start <= t < child.end:
                continue
            try:
                chain = tuple(_parent_layers(child.layer, layers))
            except InputError:
                continue  # An unrelated invalid chain is reported on its own source.
            if any(owner is parent for owner in chain):
                boxes.append(inherited_cover(t, child, return_edges=True))
        if not boxes:
            return 0.0
        # Union the axis-aligned visible rectangles without counting overlaps twice.
        xs = sorted({x for box in boxes for x in box[0]})
        area = 0.0
        for x0, x1 in zip(xs, xs[1:]):
            intervals = sorted(box[1] for box in boxes if box[0][0] < x1 and box[0][1] > x0)
            end = 0.0
            for y0, y1 in intervals:
                area += (x1 - x0) * max(0.0, y1 - max(y0, end))
                end = max(end, y1)
        return area / (frame_size[0] * frame_size[1])

    for s in shots:
        if s.kind not in FOOTAGE | OVERLAYS:
            continue
        try:
            parents = [p for owner in (s.layer,) + s.containers for p in _parent_layers(owner, layers)]
        except InputError as err:
            # Main's verdict, as if unparented; what the parents add goes unchecked.
            unchecked.append({'code': 'pop-move', 'why': f'{s.id}: {err}'})
            parents = []
        sources.append((s.id, s.layer, s.zero, s.rate, s.start, s.end,
                        lambda t, s=s, parents=parents: inherited_cover(t, s) if parents else _cover(s, frame_size, t, camera=root_camera if root_camera and any(c.layer is root_camera and _camera_affected(s, c.scope, layers) for c in cameras) else None, descendants=shots, perspective=True), False, None))
        for parent in parents:
            coverage = lambda t, parent=parent: rig_cover(t, parent)
            sources.append((s.id, parent, getattr(parent, 'placed_zero', 0.0), getattr(parent, 'rate', 1.0),
                            s.start, s.end, coverage, True, None))
    def picture_seam(a: _Shot, b: _Shot) -> bool:
        """A camera move is only interrupted by a picture cut: two video layers that meet, one covering the frame there.
        Overlay shapes that start or stop at the same time are not seams."""
        if a is b or abs(a.end - b.start) > EPS or a.media != 'video' or b.media != 'video':
            return False
        if any(join.a.layer is a.layer and join.b.layer is b.layer and abs(join.time - b.start) <= EPS and (join.overlap > EPS or
               ((join.transition or {}).get('id') and _num((join.transition or {}).get('duration'))
                and join.transition['duration'] > 0)) for join in picture_joins):
            return False
        try:
            if _continuous(a, b, fps, frame_size):
                return False
            return max(_cover(a, frame_size, a.end - frame / 2, perspective=True),
                       _cover(b, frame_size, b.start + frame / 2, perspective=True)) >= POP_COVER - EPS
        except InputError as err:
            unchecked.append({'code': 'pop-move', 'why': f'picture seam at {a.end:.2f} s: {err}'})
            return False
    for camera in cameras:
        participating = _camera_shots(shots, camera.scope, layers)
        for s in shots:
            if s.kind not in ('composition', 'scene_ref') or not _camera_affected(s, camera.scope, layers):
                continue
            content = s.content
            canvas = content if s.kind == 'composition' else (content.get('asset') or getattr(s.layer, 'assets', {}).get(content.get('assetId')) or {}).get('scene') or {}
            background = (canvas.get('composition') or {}).get('background')
            if (isinstance(background, str) and background.strip().lower() not in ('', 'transparent')
                    and not re.fullmatch(r'#(?:[0-9a-f]{3}0|[0-9a-f]{6}00)', background.strip().lower())
                    and moves(camera.layer, camera.zero, camera.rate, camera.start, camera.end, fps, [], 'camera')):
                unchecked.append({'code': 'pop-move', 'why': f'{s.id}: camera movement over a composition background needs rendered geometry'})
        def camera_visible(t, participants=participating):
            active = [s for s in participants if s.start <= t < s.end]
            for s in active:
                try:
                    if _cover(s, frame_size, t) > EPS:
                        return True
                except InputError:
                    pass
            if active:
                raise InputError('animated camera visibility needs rendered geometry')
            return False
        camera_seams = {a.end for a in participating for b in participating if picture_seam(a, b)}
        sources.append(('camera', camera.layer, camera.zero, camera.rate, camera.start, camera.end,
                        camera_visible, False, (camera.scope, participating, camera_seams)))
    for where, layer, zero, rate, start, end, coverage, inherited, projection in sources:
        for m in moves(layer, zero, rate, start, end, fps, unchecked, where):
            if inherited and m.prop not in ('position', 'scale', 'rotation', 'anchor', 'translation'):
                continue
            label = f'parent {layer.get("id")} {m.prop}' if inherited else m.prop
            def covers(t: float) -> bool:
                if any(a - EPS <= t <= b + EPS for a, b in frozen.get(id(layer), [])):
                    return False
                try:
                    if projection is not None and m.prop in ('position', 'distance') and \
                            _identity_pivot(layer, projection[1], t, unit_zoom=m.prop == 'position', scope=projection[0], parents=layers):
                        return False
                    visible = coverage(t)
                    # A pan belongs to a big card if either endpoint qualifies; an endpoint wholly
                    # outside the viewport still cannot pop. Keep that classification over the pan.
                    share = max(coverage(m.start), coverage(m.end)) if m.prop in ('position', 'translation') else visible
                except InputError as err:
                    unchecked.append({'code': 'pop-move', 'why': f'{where}: {err}'})
                    return False
                return visible > EPS and share >= POP_COVER - EPS
            if m.easing == 'step' or m.frame_jump:
                # A jump shows on both sides of it: a big layer that shrinks away pops as much as one that grows.
                if covers(max(m.start, m.end - frame)) or covers(m.end):
                    out.append(finding('pop-move', m.end, m.end + frame, [where],
                                       f'{label} jumps in one frame at {m.end:.2f} s (a step key)' if m.easing == 'step' else f'{label} jumps in one frame at {m.end:.2f} s'))
                continue
            if m.rest_before and not (projection is not None and any(abs(m.start - t) <= EPS for t in projection[2])) and not m.ramped_in and covers(m.start) and _abrupt(m.easing, m.moving, _slope_start):
                out.append(finding('pop-move', m.start, m.start + frame, [where],
                                   f'{label} move starts abruptly at {m.start:.2f} s (easing {json.dumps(m.easing)})'))
            if m.rest_after and not (projection is not None and any(abs(m.end - t) <= EPS for t in projection[2])) and not m.ramped_out and covers(m.end) and _abrupt(m.easing, m.moving, _slope_end):
                out.append(finding('pop-move', m.end - frame, m.end, [where],
                                   f'{label} move stops abruptly at {m.end:.2f} s (easing {json.dumps(m.easing)})'))
    return out


class _Seam:
    def __init__(self, a: _Shot, b: _Shot, time: float, transition: Optional[Dict[str, Any]], overlap: float) -> None:
        self.a, self.b, self.time, self.transition, self.overlap = a, b, time, transition, overlap


def seams(shots: List[_Shot], fps: float, unchecked: List[Dict[str, str]],
          frame_size=None, camera=None) -> List[_Seam]:
    """Every join between two consecutive takes: track clips side by side, and video layers that meet."""
    out: List[_Seam] = []
    frame = 1.0 / fps
    tracks: Dict[int, List[_Shot]] = {}
    for s in shots:
        if s.containers and ((s.containers[-1].get('content') or {}).get('kind') == 'track'):
            tracks.setdefault(id(s.containers[-1]), []).append(s)
    for clips in tracks.values():
        content = clips[0].containers[-1].get('content') or {}
        by_gap = {t.get('between'): t for t in content.get('transitions') or [] if isinstance(t, dict)}
        for i, (a, b) in enumerate(zip(clips, clips[1:])):
            out.append(_Seam(a, b, b.start, by_gap.get(i), 0.0))
    videos = [s for s in shots if s.media == 'video']
    for a in videos:
        for b in videos:
            if a is b or a.scope is not b.scope or b.start <= a.start + EPS:
                continue
            # Adjacent clips of one track were already paired with their transition.
            if a.containers and b.containers and a.containers[-1] is b.containers[-1] and (a.containers[-1].get('content') or {}).get('kind') == 'track':
                continue
            overlap = a.end - b.start
            # Unknown or animated geometry must retain the original pairing.
            try:
                owners = (a.layer,) + a.containers + (b.layer,) + b.containers
                if not frame_size or camera or any(
                        owner.get('parentId') is not None or owner.get('mask') is not None
                        or any(field in (owner.get('content') or {}) and _size(owner['content'][field]) is None
                               for field in ('bounds', 'size'))
                        or any((owner.get('animations') or {}).get(p) for p in MOVES)
                        or any(any((c.get('animations') or {}).get(p) for p in MOVES)
                               for c in owner.get('transforms') or [] if isinstance(c, dict))
                        for owner in owners):
                    raise InputError('unknown seam geometry')
                box_a = _cover(a, frame_size, min(a.end, b.start), return_edges=True)
                box_b = _cover(b, frame_size, b.start, return_edges=True)
                areas = [math.prod(edge[1] - edge[0] for edge in box) for box in (box_a, box_b)]
                shared = math.prod(max(0.0, min(x[1], y[1]) - max(x[0], y[0]))
                                   for x, y in zip(box_a, box_b))
                if min(areas) <= EPS or shared < 0.5 * min(areas) - EPS:
                    continue
            except InputError:
                pass
            if math.ceil(a.end * fps - EPS) == math.ceil(b.start * fps - EPS):
                out.append(_Seam(a, b, b.start, None, 0.0))
            elif EPS < overlap < min(a.end - a.start, b.end - b.start):
                fade = _fades(a, b)
                if fade:
                    out.append(_Seam(a, b, (fade[0] + fade[1]) / 2, None, fade[1] - fade[0]))
                else:
                    for code in ('same-scene-cut', 'hidden-take-change', 'ghost'):
                        unchecked.append({'code': code, 'why': f'{a.id}, {b.id}: overlapping videos need rendered review'})
    return [s for s in out if s.a.media == 'video' and s.b.media == 'video']


def _fades(a: _Shot, b: _Shot) -> Optional[Span]:
    """A hand-made dissolve: the incoming layer fades up, or the outgoing one fades out, as they overlap."""
    cuts = {b.start, a.end}
    for shot in (a, b):
        track = (shot.layer.get('animations') or {}).get('opacity') or {}
        if track.get('expression'):
            return None
        base = _key_zero(shot.layer, track, shot.start, shot.zero)
        cuts.update(base + float(k['time']) * shot.rate for k in track.get('keyframes') or []
                    if isinstance(k, dict) and _num(k.get('time')) and b.start < base + float(k['time']) * shot.rate < a.end)

    def opacity(shot: _Shot, t: float) -> float:
        return (_value_at(shot.layer, 'opacity', shot.zero, shot.rate, t) or [1.0])[0]
    times = sorted(cuts)
    fading = []
    for x, y in zip(times, times[1:]):
        t, u = x + (y - x) / 3, x + 2 * (y - x) / 3
        av, bv = opacity(a, t), opacity(b, t)
        if av > 0 and bv > 0 and ((av < 1 and abs(av - opacity(a, u)) > EPS)
                                  or (bv < 1 and abs(bv - opacity(b, u)) > EPS)):
            fading.append((x, y))
    return (fading[0][0], fading[-1][1]) if fading else None


def _continuous(a: _Shot, b: _Shot, fps: float, frame_size=None, seam_time=None) -> bool:
    """One file split with nothing changed: the picture plays on through the seam."""
    def transform(shot: _Shot) -> Dict[str, Any]:
        value = dict(shot.layer.get('transform') or {})
        for key in MOVES:
            value.pop(key, None)
        if value.get('opacity') == 1:
            value.pop('opacity')
        return value

    # a new crop or fit of the same file frames another part of it: the picture does not play on
    if a.source() != b.source() or transform(a) != transform(b) or any(
            a.content.get(field) != b.content.get(field) for field in ('bounds', 'fit', 'crop')):
        return False
    for prop in MOVES:
        av = _value_at(a.layer, prop, a.zero, a.rate, a.end)
        track = (a.layer.get('animations') or {}).get(prop) or {}
        if track and not track.get('expression'):
            av = _track_at(track, _key_zero(a.layer, track, 0.0, a.zero), a.rate, a.end, step_left=True) or av
        bv = _value_at(b.layer, prop, b.zero, b.rate, b.start)
        defaults = {'scale': [1.0, 1.0], 'rotation': [0.0], 'z': [0.0],
                    'rotationX': [0.0], 'rotationY': [0.0]}
        if frame_size:
            defaults['position'] = [frame_size[0] / 2, frame_size[1] / 2]
        if prop == 'anchor' and frame_size and (av is None) != (bv is None):
            extent = _parent_extent(a.layer if av is None else b.layer, frame_size)
            default_anchor = [extent[0] / 2, extent[1] / 2]
            av = av if av is not None else default_anchor
            bv = bv if bv is not None else default_anchor
        if (av or defaults.get(prop)) != (bv or defaults.get(prop)):
            return False
    ta, tb = a.content.get('trim') or {}, b.content.get('trim') or {}
    in_a = ta['in'] if 'in' in ta and ta['in'] is not None else 0.0
    in_b = tb['in'] if 'in' in tb and tb['in'] is not None else 0.0
    out_a = ta.get('out')
    speed = a.content.get('speed', 1)
    # _visits yields _Placed, a dict subclass whose placement predates clipping.
    placed_start = getattr(a.layer, 'placed_start', a.start)
    played = (a.end - placed_start) / a.rate
    incoming_played = ((b.start if seam_time is None else seam_time) - getattr(b.layer, 'placed_start', b.start)) / b.rate
    return (_num(in_a) and (out_a is None or _num(out_a)) and _num(in_b) and _num(speed) and speed > 0
            and abs((min(float(out_a), float(in_a) + played * speed) if out_a is not None else float(in_a) + played * speed)
                    - (float(in_b) + incoming_played * speed)) <= float(speed) / (fps * a.rate) + EPS
            and speed == b.content.get('speed', 1))


def joins(shots: List[_Shot], shot_ids: Dict[str, Any], places: Dict[str, Any], fps: float,
          unchecked: List[Dict[str, str]], camera: Optional[Dict[str, Any]] = None,
          duration: float = 0.0, frame_size=None, layers=None) -> List[Dict[str, Any]]:
    out = []
    frame = 1.0 / fps
    unknown_shot = False
    videos = [s for s in shots if s.media == 'video']
    # Scene references have separate traversal scopes, but their placed children already use
    # the outer clock. Compare only a single, unambiguously full-frame picture on each side.
    refs = [s for s in shots if s.kind == 'scene_ref']
    resolved = []
    uncertain = False

    def transition_at(track, t):
        clips = [s for s in shots if s.containers and s.containers[-1] is track]
        for transition in (track.get('content') or {}).get('transitions') or []:
            if not isinstance(transition, dict):
                continue
            index, length = transition.get('between'), transition.get('duration')
            if isinstance(index, int) and 0 <= index < len(clips) - 1 and _num(length) and length > 0:
                boundary = clips[index + 1].start
                if abs(t - boundary) <= length * getattr(track, 'rate', 1.0) / 2 + EPS:
                    return True
        return False
    for left in refs:
        for right in refs:
            if left is right or left.scope is not right.scope or abs(left.end - right.start) > EPS:
                continue
            t = right.start
            try:
                if not frame_size or camera:
                    raise InputError('unknown reference geometry')
                for ref in (left, right):
                    if (ref.content.get('loop') or ref.layer.get('mask') is not None
                            or ref.layer.get('parentId') is not None or ref.layer.get('transform')
                            or ref.layer.get('transforms') or ref.layer.get('animations')):
                        raise InputError('reference geometry needs rendered review')
                    if any(transition_at(c, t) for c in ref.containers if (c.get('content') or {}).get('kind') == 'track'):
                        raise InputError('reference transition needs rendered review')
                selected = []
                for ref, moment in ((left, t - min(EPS * 2, (left.end-left.start)/2)),
                                    (right, t + min(EPS * 2, (right.end-right.start)/2))):
                    inside = [s for s in shots if any(c is ref.layer for c in s.containers)
                              and s.start <= moment < s.end]
                    if any(s.kind == 'track' and transition_at(s.layer, t) for s in inside):
                        raise InputError('nested transition needs rendered review')
                    visible = [s for s in inside if s.media == 'video'
                               and any(a <= moment < b for a, b in _visibility(s))]
                    if len(visible) != 1:
                        raise InputError('reference footage needs rendered review')
                    video = visible[0]
                    if any(s is not video and s.kind not in ('track', 'composition', 'scene_ref', 'empty')
                           and any(a <= moment < b for a, b in _visibility(s)) for s in inside):
                        raise InputError('reference foreground needs rendered review')
                    if any((c.get('content') or {}).get('loop') or c.get('mask') is not None
                           or c.get('parentId') is not None or c.get('transform') or c.get('transforms')
                           or c.get('animations') for c in video.containers if c is not ref.layer):
                        raise InputError('nested geometry needs rendered review')
                    box = _cover(video, frame_size, moment, return_edges=True)
                    if any(edge[0] > EPS or edge[1] < size - EPS for edge, size in zip(box, frame_size)):
                        raise InputError('reference is not full frame')
                    selected.append(video)
                resolved.append(_Seam(selected[0], selected[1], t, None, 0.0))
            except InputError:
                uncertain = True
    if any(a.scope is not b.scope and abs(a.end - b.start) <= frame / 2
           and not any(s.a is a and s.b is b for s in resolved)
           for a in videos for b in videos if a is not b):
        uncertain = True
    if uncertain:
        for code in ('same-scene-cut', 'hidden-take-change', 'ghost'):
            unchecked.append({'code': code, 'why': 'joins across scene container boundaries need rendered review'})
    for seam in seams(shots, fps, unchecked, frame_size, camera) + resolved:
        a, b, t = seam.a, seam.b, seam.time
        ids = [a.id, b.id]
        try:
            visible_a, visible_b = _visibility(a), _visibility(b)
            if not any(x < t + EPS and y >= t - frame - EPS for x, y in visible_a) or not any(x <= t + frame + EPS and y > t - EPS for x, y in visible_b):
                continue
        except InputError as err:
            for code in ('same-scene-cut', 'hidden-take-change', 'ghost'):
                unchecked.append({'code': code, 'why': f'{a.id}, {b.id}: {err}'})
            continue
        transition = seam.transition or {}
        name, length = transition.get('id'), transition.get('duration')
        if _num(length):
            length *= a.rate
        if seam.overlap:
            name, length = 'opacity fade', seam.overlap
        if name == 'opacity fade' and length <= GHOST_SECONDS + EPS:
            # Only static, axis-aligned boxes can establish whether the two pictures meet.
            try:
                owners = [o for s in (a, b) for o in (s.layer,) + s.containers]
                parents = [p for o in owners for p in _parent_layers(o, layers)]
                if (not frame_size or camera or any(_has_depth(o) for o in owners + parents)
                        or any(s.layer.get('animations', {}).get(p) for s in (a, b) for p in MOVES)):
                    raise InputError('animated or unknown fade geometry needs rendered review')
                box_a = _cover(a, frame_size, t, layers, return_edges=True)
                box_b = _cover(b, frame_size, t, layers, return_edges=True)
                if any(min(x[1], y[1]) <= max(x[0], y[0]) + EPS for x, y in zip(box_a, box_b)):
                    continue
                # Later siblings draw above earlier ones. An opaque upper incoming picture
                # hides the outgoing fade where it fully covers the outgoing box.
                siblings = list(getattr(a.layer, 'siblings', {}).values())
                order = [str(x.get('id', '')) for x in siblings]
                incoming_opacity = _value_at(b.layer, 'opacity', b.zero, b.rate, t)
                if (a.id in order and b.id in order and order.index(b.id) > order.index(a.id)
                        and (incoming_opacity is None or incoming_opacity[0] >= 1 - EPS)
                        and not (b.layer.get('animations') or {}).get('opacity')
                        and all(y[0] <= x[0] + EPS and y[1] >= x[1] - EPS for x, y in zip(box_a, box_b))):
                    name, length, t = None, 0.0, b.start
            except InputError as err:
                for code in ('same-scene-cut', 'ghost', 'hidden-take-change'):
                    unchecked.append({'code': code, 'why': f'{a.id}, {b.id}: {err}'})
                continue
        if name and _num(length) and (name in DISSOLVES or name == 'opacity fade') and length <= GHOST_SECONDS + EPS:
            out.append({**finding('ghost', t - length / 2, t + length / 2, ids,
                                  f'a {length:.2f} s {name} shows both takes at once'), 'at': t})
            continue
        if name and name not in DISSOLVES and name not in MASKING and name != 'opacity fade':
            unchecked.append({'code': 'ghost', 'why': f'transition {name!r} between {a.id} and {b.id} is not in the catalog this script knows'})
        try:
            if _continuous(a, b, fps, frame_size, t):
                continue
        except InputError as err:
            unchecked.append({'code': 'same-scene-cut', 'why': f'{a.id}, {b.id}: {err}'})
            continue
        # Different shots, even of one place, are coverage: film-cutting's Seams. Only a cut where
        # the picture barely changes is a glitch: two takes of one shot, a jump inside one, or two
        # shots of the same size and angle.
        sa, sb = a.shot(shot_ids), b.shot(shot_ids)
        why = None
        if sa is None or sb is None:
            unknown_shot = True
        elif sa['shot'] == sb['shot']:
            why = (f'a jump inside shot {sa["shot"]}' if a.source() and a.source() == b.source()
                   else f'two takes of shot {sa["shot"]}')
        elif all(k in sa and k in sb and sa[k] == sb[k] for k in ('size', 'angle')):
            why = f'shots {sa["shot"]} and {sb["shot"]} have the same size and angle'
        pa, pb = a.place(places), b.place(places)
        one_place = why is not None or (pa is not None and pa == pb)
        # A long plain dissolve is a choice, not a hidden switch; a zoom or a whip over it hides one.
        if not one_place:
            continue
        unknown_transition = name and name not in DISSOLVES and name not in MASKING and name != 'opacity fade'
        if unknown_transition:
            unchecked.append({'code': 'hidden-take-change', 'why': f'transition {name!r} between {a.id} and {b.id} needs rendered review'})
        plain_dissolve = name in DISSOLVES - MASKING or name == 'opacity fade'
        burst = None
        if name in MASKING and _num(length):
            burst = (t - length / 2, t + length / 2, f'a {length:.2f} s {name} transition')
        else:
            sources = [(s.layer, s.zero, s.rate, s.start, s.end, s.id) for s in (a, b)]
            camera_scope = getattr(camera, 'scope', None) if camera else None
            camera_shots = _camera_shots([a, b], camera_scope, layers) if camera else []
            if camera_shots:
                sources.append((camera, 0.0, 1.0, 0.0, duration, 'camera'))
            for layer, zero, rate, start, end, label in sources:
                segments = moves(layer, zero, rate, start, end, fps, unchecked, label)
                runs = []
                for m in segments:
                    if layer is camera and m.prop in ('position', 'distance'):
                        try:
                            if all(_identity_pivot(camera, camera_shots, moment, unit_zoom=m.prop == 'position', scope=camera_scope, parents=layers)
                                   for moment in (m.start, (m.start + m.end) / 2, m.end)):
                                continue
                        except InputError as err:
                            unchecked.append({'code': 'hidden-take-change', 'why': f'camera: {err}'})
                            continue
                    if m.easing == 'step' or m.frame_jump:
                        continue
                    if runs and runs[-1][-1].prop == m.prop and abs(runs[-1][-1].end - m.start) <= EPS and not runs[-1][-1].rest_after:
                        runs[-1].append(m)
                    else:
                        runs.append([m])
                for run in runs:
                    start, end = run[0].start, run[-1].end
                    frames = (end - start) * fps
                    if start - frame <= t <= end + frame and TAKE_MIN_FRAMES - EPS <= frames <= TAKE_MAX_FRAMES + EPS:
                        burst = (start, end, f'a {frames:.0f}-frame {run[0].prop} move')
                        break
                if burst:
                    break
        if burst:
            out.append({**finding('hidden-take-change', burst[0], burst[1], ids,
                                  f'{burst[2]} hides a cut: {why or "a cut inside one place"}'), 'at': t})
        elif why and not plain_dissolve and not unknown_transition:
            out.append({**finding('same-scene-cut', t, t + frame, ids, f'hard cut: {why}'), 'at': t})
    if unknown_shot:
        unchecked.append({'code': 'same-scene-cut', 'why': 'no `shots` for some clips: which takes show one shot is in the shot list, not the scene'})
    return out


def _default_projection(shot: _Shot, owners: Tuple[Dict[str, Any], ...], frame_size: Tuple[float, float]) -> Optional[_Shot]:
    """A top-level overlay at depth z as the default camera draws it: scaled by D / (D - z) about the
    frame centre, D = W * 50 / 36. None where that is not all there is to it: a container or parent
    places it too, or it has a transform stack, a mask or a 3D turn."""
    transform = shot.layer.get('transform') or {}
    if (shot.containers or len(owners) != 1 or shot.layer.get('transforms') or shot.layer.get('mask')
            or any(transform.get(prop) for prop in ('rotationX', 'rotationY', 'distance'))):
        return None
    z = _vector(transform.get('z'))
    position = _vector(transform.get('position')) or [v / 2 for v in frame_size]
    distance = frame_size[0] * 50 / 36
    if not z or len(z) != 1 or len(position) != 2 or distance - z[0] <= EPS:
        return None
    factor = distance / (distance - z[0])
    scale = (_vector(transform.get('scale')) or [1.0]) * 2
    out = copy.copy(shot)
    out.layer = copy.copy(shot.layer)
    out.layer['transform'] = dict(transform, scale=[value * factor for value in scale[:2]], position=[
        centre + (value - centre) * factor for value, centre in zip(position, (v / 2 for v in frame_size))])
    return out


def blink(shots: List[_Shot], fps: float, unchecked: List[Dict[str, str]], frame_size=None, layers=None, cameras=None) -> List[Dict[str, Any]]:
    out = []
    limit = BLINK_FRAMES / fps + EPS

    def overlay(s: _Shot) -> bool:
        return s.kind in OVERLAYS or (s.kind == 'media' and s.media != 'video')

    def placement(s: _Shot, t: float, step_left: bool = False):
        # Where the overlay's origin lands on its canvas: its own position carried
        # through its parents, so titles under different parents are different slots.
        track = (s.layer.get('animations') or {}).get('position') or {}
        point = _value_at(s.layer, 'position', s.zero, s.rate, t)
        if step_left and track and not track.get('expression'):
            point = _track_at(track, _key_zero(s.layer, track, 0.0, s.zero), s.rate, t, step_left=True) or point
        canvas = frame_size
        for c in s.containers:
            content = c.get('content') or {}
            if canvas and content.get('kind') != 'track':
                canvas = _native_extent(c) if content.get('fit') == 'none' else _canvas(c, canvas)
        if point is None and canvas:
            point = [canvas[0] / 2, canvas[1] / 2]
        parents = list(_parent_layers(s.layer, layers)) if layers is not None else []
        if not parents:
            return point
        if not canvas:
            raise InputError('parented overlay placement needs the frame size')
        edges = [[point[0]] * 2, [point[1]] * 2]
        for parent in parents:
            zero, rate = getattr(parent, 'placed_zero', 0.0), getattr(parent, 'rate', 1.0)
            if step_left:
                owners = [parent] + [c for c in parent.get('transforms') or [] if isinstance(c, dict)]
                for owner in owners:
                    for _, track in _tracks(owner.get('animations') or {}, ('position', 'translation', 'anchor', 'scale', 'rotation', 'rotationX', 'rotationY', 'z')):
                        if not track.get('expression'):
                            base = _key_zero(parent, track, 0.0, zero)
                            if _track_at(track, base, rate, t, step_left=True) != _track_at(track, base, rate, t):
                                raise InputError('parent transform steps at overlay end; placement needs rendered review')
            box = (0.0, 0.0) if _value_at(parent, 'anchor', zero, rate, t) is not None else _parent_extent(parent, canvas)
            edges = _place_edges(parent, canvas, box, zero, rate, t, edges)
        return [round(edge[0], 6) for edge in edges]

    def same_slot(a: _Shot, ta: float, b: _Shot, tb: float, step_left: bool = False) -> bool:
        return a is b or (a.kind == b.kind and placement(a, ta, step_left=step_left) == placement(b, tb))

    occupancy = []
    for shot in shots:
        if not overlay(shot):
            continue
        try:
            owners = shot.containers + (shot.layer,)
            if layers is not None:
                owners += tuple(p for owner in owners for p in _parent_layers(owner, layers))
            animated = any(owner.get('animations') or any(c.get('animations') for c in owner.get('transforms') or [] if isinstance(c, dict)) for owner in owners)
            # A camera-exempt overlay is drawn flat, so its depth does not move it.
            projected = any(_has_depth(owner) for owner in owners) and not any(owner.get('cameraExempt') for owner in owners)
            if frame_size and shot.kind in ('media', 'color', 'shape') and not animated and not (projected and cameras):
                covered_shot = _default_projection(shot, owners, frame_size) if projected else shot
                # Depth this can't project stays in occupancy, as every overlay does on main.
                if covered_shot is not None and _cover(covered_shot, frame_size, (shot.start + shot.end) / 2, layers, perspective=projected) <= EPS and not cameras:
                    continue
            spans = _visibility(shot)
            if shot.kind == 'captions':
                spans = intersect(spans, _caption_spans(shot))
            occupancy.extend((a, b, shot) for a, b in spans)
        except InputError as err:
            unchecked.append({'code': 'blink', 'why': f'{shot.id}: {err}'})
    reported = set()
    for _, end, left in occupancy:
        for start, _, right in occupancy:
            missing = math.ceil(start * fps - EPS) - math.ceil(end * fps - EPS)
            if not (EPS < start - end <= limit and missing > 0):
                continue
            try:
                if not same_slot(left, end, right, start, step_left=True):
                    continue
                if left.scope is not right.scope:
                    unchecked.append({'code': 'blink', 'why': 'overlay continuity across scene containers needs rendered review'})
                    continue
                if any(s.scope is left.scope and a < start - EPS and b > end + EPS
                       and same_slot(left, end, s, max(a, end), step_left=True) for a, b, s in occupancy):
                    continue
                key = (end, start, left.id, right.id)
                if key not in reported:
                    reported.add(key)
                    out.append(finding('blink', end, start, sorted({left.id, right.id}),
                                       f'the overlay vanishes for {missing} frame(s) and returns'))
            except InputError as err:
                unchecked.append({'code': 'blink', 'why': f'{left.id}, {right.id}: {err}'})

    return out


def _visibility(shot: _Shot) -> List[Span]:
    """Recompute opacity without losing the placed layer's rate or its enclosing windows."""
    spans = [(shot.start, shot.end)]
    for layer in shot.containers + (shot.layer,):
        placed = copy.copy(layer)
        if hasattr(placed, 'spans'):
            del placed.spans
        start = getattr(layer, 'placed_start', shot.start)
        zero = getattr(layer, 'placed_zero', shot.zero)
        spans = intersect(spans, shown(placed, start, zero))
    return spans


def _caption_spans(shot: _Shot) -> List[Span]:
    # caption_blocks owns reveal semantics, including active words and sustained segments.
    return merge((shot.start + (a - shot.start) * shot.rate, shot.start + (b - shot.start) * shot.rate)
                 for a, b, _ in caption_blocks(shot.content, shot.start))


def _distance_spans(camera: Dict[str, Any], shots: List[_Shot], move: _Move,
                    unchecked: List[Dict[str, str]], scope: Any = None) -> List[Span]:
    """Distance moves only where the camera sees depth or tilt; split at keys and picture changes."""
    cuts = {move.start, move.end}
    tracks = [(camera, camera.get('animations') or {}, getattr(camera, 'placed_zero', 0.0),
               getattr(camera, 'rate', 1.0), ('rotation', 'rotationX', 'rotationY'))]
    for shot in shots:
        cuts.update((shot.start, shot.end))
        for layer in _projected(shot, scope):
            zero, rate = getattr(layer, 'placed_zero', shot.zero), getattr(layer, 'rate', shot.rate)
            holders = [layer.get('animations') or {}] + [c.get('animations') or {} for c in layer.get('transforms') or [] if isinstance(c, dict)]
            tracks.extend((layer, h, zero, rate, ('z', 'rotationX', 'rotationY')) for h in holders)
    for layer, holder, zero, rate, props in tracks:
        for _, track in _tracks(holder, props):
            base = _key_zero(layer, track, 0.0, zero)
            cuts.update(base + float(k['time']) * rate for k in track.get('keyframes') or []
                        if isinstance(k, dict) and _num(k.get('time')))
    cuts = sorted(t for t in cuts if move.start <= t <= move.end)
    out = []
    for a, b in zip(cuts, cuts[1:]):
        if b <= a + EPS:
            continue
        try:
            if not all(_identity_pivot(camera, shots, t, unit_zoom=False, scope=scope) for t in (a + EPS, (a + b) / 2, b - EPS)):
                out.append((a, b))
        except InputError as err:
            unchecked.append({'code': 'zoom-idle', 'why': f'camera: {err}'})
    return out


def zoom_idle(shots: List[_Shot], cameras: List[_Shot], fps: float,
              unchecked: List[Dict[str, str]], allowed: Optional[List[Span]] = None,
              all_layers: Optional[Dict[Any, Any]] = None, frame_size=None) -> List[Dict[str, Any]]:
    out = []
    layers = all_layers if all_layers is not None else {(s.scope, s.id): s.layer for s in shots}
    footage = []
    for s in (shot for shot in shots if shot.kind == 'media'):
        try:
            owners = s.containers + (s.layer,)
            if layers is not None:
                owners += tuple(p for owner in owners for p in _parent_layers(owner, layers))
            # A static offscreen layer cannot contribute playback. Moving geometry cannot be
            # classified from one sample, so retain it for the existing conservative check.
            animated = any(owner.get('animations') or any(c.get('animations') for c in owner.get('transforms') or [] if isinstance(c, dict)) for owner in owners)
            if (frame_size and not animated and not any(_camera_affected(s, camera.scope, layers) for camera in cameras)
                    and (not s.containers or (all((c.get('content') or {}).get('kind') == 'track' and not c.get('parentId') for c in s.containers) and not s.layer.get('parentId')))
                    and _cover(s, frame_size, (s.start + s.end) / 2, layers if not s.containers else None) <= EPS):
                continue
        except InputError:
            # Unknown geometry remains a possible contributor.
            pass
        footage.append(s)

    sources: List[Tuple] = []
    for s in footage:
        sources.append((s.id, [m for m in moves(s.layer, s.zero, s.rate, s.start, s.end, fps, [], s.id)
                               if not (m.prop == 'z' and not _camera_affected(s, s.scope, layers))], [s], None, []))
    for s in shots:
        if s.kind in ('track', 'composition', 'scene_ref'):
            inside = [f for f in footage if any(c is s.layer for c in f.containers)]
            sources.append((s.id, moves(s.layer, s.zero, s.rate, s.start, s.end, fps, [], s.id), inside, None, []))
    # Transform-only parent rigs are not containers, but their descendants inherit their zoom.
    for s in shots:
        if s.kind != 'empty':
            continue
        inside = []
        for f in footage:
            try:
                if any(parent is s.layer for owner in f.containers + (f.layer,)
                       for parent in _parent_layers(owner, layers)):
                    inside.append(f)
            except InputError as err:
                unchecked.append({'code': 'zoom-idle', 'why': f'{f.id}: {err}'})
        if inside:
            sources.append((s.id, [m for m in moves(s.layer, s.zero, s.rate, s.start, s.end, fps, [], s.id)
                                   if not (m.prop == 'z' and (not _camera_affected(s, s.scope, layers)
                                                              or not any(_camera_affected(f, s.scope, layers) for f in inside)))],
                            inside, None, []))
    root = next((s.scope for s in shots if not s.containers), None)
    for camera in cameras:
        participating = _camera_shots(shots, camera.scope, layers)
        media = [s for s in participating if s.kind == 'media']
        # A picture exempt in its own scope still moves with an outer camera through its canvas,
        # but whether it shows needs rendered geometry. Under the root camera it keeps main's
        # verdict and clears no hold; a nested camera, which main never read, adds no hold for it.
        held = [s for s in media if _exempt_inside_canvas(s, camera.scope)]
        if held:
            unchecked.append({'code': 'zoom-idle', 'why': 'camera: ' + ', '.join(sorted({s.id for s in held}))
                              + ': moved through its canvas; whether it shows needs rendered geometry'})
        sources.append(('camera', moves(camera.layer, camera.zero, camera.rate, camera.start, camera.end, fps, [], 'camera'),
                        [s for s in media if camera.scope is not root or s not in held], camera, participating))
    for where, found, covered, camera, participating in sources:
        zooming = merge(span for m in found if m.prop in ZOOMS and m.easing != 'step'
                        for span in (_distance_spans(camera.layer, participating, m, unchecked, camera.scope)
                                     if camera is not None and m.prop == 'distance' else [(m.start, m.end)]))
        # Allowed spans come off before the length is measured, so a zoom that runs just past a
        # span leaves no sliver to fail.
        zooming = intersect(zooming, merge((s.start, s.end) for s in covered))
        zooming = subtract(zooming, allowed or [])
        if not zooming or not covered:
            continue
        for a, b in (piece for still in all_still(covered if camera is not None else footage, layers) for piece in intersect(zooming, [still])):
            if b - a + EPS >= ZOOM_IDLE_SECONDS:
                ids = [where] if where == 'camera' else sorted({where} | {s.id for s in covered if s.start < b and s.end > a})
                out.append(finding('zoom-idle', a, b, ids, 'only the code zoom moves; the picture under it '
                                   f'is still for {b - a:.2f} s'))
    return out


def run(data: Any, extra: Optional[List[Span]] = None, slides: bool = False) -> Dict[str, Any]:
    if not isinstance(data, dict):
        raise InputError('the input must be a JSON object')
    if data.get('stage') not in (None, 'slides', 'cut'):
        raise InputError('`stage` must be "slides" or "cut"')
    slides = slides or data.get('stage') == 'slides'
    scene = data.get('scene') if isinstance(data.get('scene'), dict) else data if 'layers' in data else None
    if not isinstance(scene, dict) or not isinstance(scene.get('layers'), list):
        raise InputError('`scene` must be a scene document with `layers`')
    places = data.get('places') or {}
    if not isinstance(places, dict):
        raise InputError('`places` must map a layer, clip, asset id or uri to a place')
    shot_ids = data.get('shots') or {}
    if not isinstance(shot_ids, dict) or any(isinstance(v, dict) and 'shot' not in v for v in shot_ids.values()):
        raise InputError('`shots` must map a layer, clip, asset id or uri to a shot id or {shot, size?, angle?}')
    spans = allowed_spans(data.get('allowed')) + [(a, b, None) for a, b in extra or []]
    allowed = merge((a, b) for a, b, _ in spans)
    comp = scene.get('composition') or {}
    fps = float(comp['fps']) if _num(comp.get('fps')) and comp['fps'] > 0 else DEFAULT_FPS
    inferred_duration = scene_duration(scene)
    visits = list(_visits(scene, 0.0, inferred_duration or math.inf, set(), cameras=True, opacity=False))
    shots = [_Shot(layer, start, zero, end) for layer, start, zero, end in visits
             if (layer.get('content') or {}).get('kind') not in ('audio', 'camera') and math.isfinite(end)]
    parent_layers = {}
    for layer, _, _, _ in visits:
        for key, sibling in getattr(layer, 'siblings', {}).items():
            if (sibling.get('content') or {}).get('kind') != 'audio':
                parent_layers.setdefault((layer.scope, key), sibling)
    parent_layers.update({(layer.scope, str(layer.get('id', ''))): layer for layer, _, _, _ in visits
                          if (layer.get('content') or {}).get('kind') not in ('audio', 'camera')})
    duration = max([s.end for s in shots], default=0.0)
    if _num(comp.get('duration')) and comp['duration'] > 0:
        duration = float(comp['duration'])
    cameras = [_Shot(layer, start, getattr(layer, 'placed_zero', zero), min(end, duration))
               for layer, start, zero, end in visits if (layer.get('content') or {}).get('kind') == 'camera']

    unchecked: List[Dict[str, str]] = []
    for layer, _, _, _ in visits:
        content = layer.get('content') or {}
        kind = content.get('kind')
        if layer.get('looks'):
            for code in ('pop-move', 'zoom-idle'):
                unchecked.append({'code': code, 'why': f'{layer.get("id")}: named looks need rendered motion review'})
        if kind == 'scene_ref' and content.get('loop'):
            for code in ('pop-move', 'zoom-idle', 'screen-still'):
                unchecked.append({'code': code, 'why': f'{layer.get("id")}: looped scene reference repetitions need rendered review'})
        if kind == 'shape' and any(isinstance(item, dict) and item.get('animations') for item in content.get('items') or []):
            for code in ('pop-move', 'zoom-idle'):
                unchecked.append({'code': code, 'why': f'{layer.get("id")}: shape item motion needs rendered frames'})
        if getattr(layer, 'space_3d', False) and (
                (kind == 'camera' and any(isinstance(t, dict) and (t.get('keyframes') or t.get('expression'))
                                          for t in (layer.get('animations') or {}).values()))
                or (kind == 'model' and (layer.get('animations') or content.get('animation') or content.get('parameters')))):
            unchecked.append({'code': 'pop-move', 'why': '3D camera and model motion needs rendered review'})
    # Picture checks read only what shows; joins keep whole layers, so an opacity dip is no cut
    # and a track's transitions keep their clip indices.
    visible = []
    for shot in shots:
        try:
            color = shot.content.get('color')
            if shot.kind == 'color' and isinstance(color, str) and len(color) == 9 and color.startswith('#') and color[-2:].lower() == '00':
                continue
            for a, b in _visibility(shot):
                view = copy.copy(shot)
                view.start, view.end = a, b
                visible.append(view)
        except InputError as err:
            for code in ('pop-move', 'screen-still', 'zoom-idle'):
                unchecked.append({'code': code, 'why': f'{shot.id}: {err}'})
    found = [{**f, 'start': round(f['start'], 3), 'end': round(f['end'], 3)}
             for f in screen_still(visible, spans, fps)]
    frame_size = (float(comp['width']), float(comp['height'])) if _num(comp.get('width')) and _num(comp.get('height')) \
        and comp['width'] > 0 and comp['height'] > 0 else None
    root_scope = next((s.scope for s in shots if not s.containers), None)
    root_camera = next((c.layer for c in cameras if c.scope is root_scope), None)
    for check in (pop_move(visible, cameras, fps, unchecked, frame_size, parent_layers, shots), joins(shots, shot_ids, places, fps, unchecked, root_camera, duration, frame_size, parent_layers),
                  blink(shots, fps, unchecked, frame_size, parent_layers, cameras), [] if slides else zoom_idle(visible, cameras, fps, unchecked, allowed, parent_layers, frame_size)):
        for f in check:
            # A finding about a cut (`at`) stands or falls with the cut: an allowed cut leaves no
            # slivers of its dissolve or move to fail.
            at = f.pop('at', None)
            if at is not None and any(x - EPS <= at < y - EPS for x, y in allowed):
                continue
            for a, b in outside(f['start'], f['end'], allowed):
                found.append({**f, 'start': round(a, 3), 'end': round(b, 3)})
    found.sort(key=lambda f: (f['start'], f['end'], f['code']))
    errors = [f for f in found if RULES[f['code']]['level'] == 'FAIL']
    warnings = [f for f in found if RULES[f['code']]['level'] == 'WARN']
    for code, rule in RULES.items():
        if rule['status'] == 'planned':
            unchecked.append({'code': code, 'why': f'needs {rule["detector"]}; the scene alone cannot say'})
        elif 'planned' in rule:
            unchecked.append({'code': code, 'why': f'over footage, needs {rule["planned"]}'})
    if not spans:
        unchecked.append({'code': 'screen-still', 'why': 'no allowed spans were given, so no screen clip was read'})
    unchecked.append({'code': 'loudness', 'why': 'measured on the export by qc.py'})
    skipped = [{'code': code, 'why': SLIDES_SKIP} for code in SLIDES_MOTION] if slides else []
    unchecked = [u for u in unchecked if not (slides and u['code'] in SLIDES_MOTION)]
    seen_codes = set()
    unique = []
    for u in unchecked:
        key = (u['code'], u['why'])
        if key not in seen_codes:
            seen_codes.add(key)
            unique.append(u)
    checked = [c for c in CHECKED if not (slides and c in SLIDES_MOTION)]
    return {'ok': not errors, 'errors': errors, 'warnings': warnings, 'checked': checked, 'unchecked': unique, 'skipped': skipped}


def main(argv: List[str]) -> int:
    files: List[str] = []
    extra: List[Span] = []
    slides = False
    i = 0
    try:
        while i < len(argv):
            arg = argv[i]
            if arg == '--allow':
                i += 1
                if i >= len(argv):
                    return fail(USAGE, 2)
                extra.append(parse_span(argv[i]))
                i += 1
                while i < len(argv) and SPAN.fullmatch(argv[i]):
                    extra.append(parse_span(argv[i]))
                    i += 1
                continue
            if arg == '--slides':
                slides = True
                i += 1
                continue
            if arg.startswith('-'):
                return fail(USAGE, 2)
            files.append(arg)
            i += 1
    except InputError as err:
        return fail(str(err), 2)
    if len(files) > 1:
        return fail(USAGE, 2)
    try:
        if files:
            with open(files[0], encoding='utf-8-sig') as f:
                text = f.read()
        else:
            text = sys.stdin.buffer.read().decode('utf-8-sig')
    except (OSError, UnicodeDecodeError) as err:
        return fail(f'cannot read the input: {err}')
    try:
        out = run(json.loads(text), extra, slides)
    except json.JSONDecodeError as err:
        return fail(f'the input is not JSON: {err}')
    except InputError as err:
        return fail(str(err))
    sys.stdout.buffer.write((json.dumps(out, separators=(',', ':')) + '\n').encode('utf-8'))
    return 0


def fail(reason: str, code: int = 1) -> int:
    sys.stderr.write('cut_check.py: ' + ' '.join(reason.split()) + '\n')
    return code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
