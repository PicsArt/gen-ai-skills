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

from timing import InputError, _clip_length, _num, _visits, caption_blocks, shown

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
MASKING = {'zoom_through', 'movement_camera', 'glitch_cut', 'slide', 'diagonal_slide', 'card_flip',
           'page_curl', 'iris', 'shape_reveal', 'manga_page', 'flash_cut'}

# What a geometric track must change by to be seen, per property.
MOVES = {'position': 2.0, 'translation': 2.0, 'anchor': 2.0, 'crop': 2.0, 'z': 2.0, 'distance': 2.0,
         'scale': 0.01, 'zoom': 0.01, 'rotation': 0.5, 'rotationX': 0.5, 'rotationY': 0.5}
ZOOMS = {'scale', 'zoom', 'z', 'distance'}
# Content that is the picture itself: a move on it moves the whole frame.
FOOTAGE = {'media', 'track', 'composition', 'scene_ref'}
# Content that sits over the picture.
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
            return (float(trim['out']) - float(trim['in'])) / speed * self.rate
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


def all_still(shots: List[_Shot]) -> List[Span]:
    """Where at least one of the shots is on screen and every one on screen holds still."""
    cuts = sorted({t for s in shots for t in (s.start, s.end)} | {t for s in shots for span in s.still() for t in span})
    out = []
    for a, b in zip(cuts, cuts[1:]):
        if b <= a + EPS:
            continue
        mid = (a + b) / 2
        on = [s for s in shots if s.start <= mid < s.end]
        if on and all(any(x <= mid < y for x, y in s.still()) for s in on):
            out.append((a, b))
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
        return any(m and slope(e) > EASED_SLOPE for e, m in zip(easing, moving))
    return slope(easing) > EASED_SLOPE


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
            tracks += list(_tracks(component['animations'], MOVES))
    for prop, value in shot_like.items():
        if prop in MOVES and isinstance(value, dict) and 'keyframes' in value:
            tracks.append((prop, value))  # a camera field written as a track
    out: List[_Move] = []
    frame = 1.0 / fps
    for prop, track in tracks:
        if track.get('expression'):
            unchecked.append({'code': 'pop-move', 'why': f'{where} {prop} is driven by an expression; only its frames show how it moves'})
            continue
        keys = [k for k in track.get('keyframes') or [] if isinstance(k, dict) and _num(k.get('time'))
                and _vector(k.get('value')) is not None]
        if len(keys) < 2:
            continue
        base = _key_zero(shot_like, track, start, zero)
        times = [base + float(k['time']) * rate for k in keys]
        values = [_vector(k['value']) for k in keys]
        changes = [_changes(prop, a, b) for a, b in zip(values, values[1:])]
        for i, moving in enumerate(changes):
            if not any(moving):
                continue
            before = (times[i] > start + frame - EPS) if i == 0 else not any(changes[i - 1])
            last = i + 1 == len(keys) - 1
            after = (times[i + 1] < end - frame + EPS) if last else not any(changes[i + 1])
            span = times[i + 1] - times[i]
            speed = math.dist(values[i], values[i + 1]) / span if span > EPS and len(values[i]) == len(values[i + 1]) else 0.0
            easing = keys[i].get('easing', 'linear')
            a, b = max(start, times[i]), min(end, times[i + 1])
            if easing == 'step':
                if not start <= times[i + 1] < end:
                    continue
            elif b <= a + EPS:
                continue
            out.append(_Move(prop, a, b, easing, moving,
                             before and times[i] >= start, after and times[i + 1] < end, speed))
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
        if len(run) < 2 or any(m.easing not in ('linear', None) for m in run):
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
    return {'code': code, 'start': round(start, 3), 'end': round(end, 3), 'layers': layers,
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


def _track_at(track: Any, key_zero: float, rate: float, t: float) -> Optional[List[float]]:
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
        if t0 <= t < t1:
            if len(v0) != len(v1):
                return v0
            f = _ease(easing, (t - t0) / (t1 - t0))
            return [x + (y - x) * f for x, y in zip(v0, v1)]
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


def _viewport_extent(layer: Dict[str, Any], canvas: Tuple[float, float], extent: Tuple[float, float],
                     zero: float, rate: float, t: float) -> Tuple[float, float]:
    """Intersect the placed box with its viewport; anchors are in the box's own pixels."""
    position = _value_at(layer, 'position', zero, rate, t) or [canvas[0] / 2, canvas[1] / 2]
    anchor = _value_at(layer, 'anchor', zero, rate, t) or [extent[0] / 2, extent[1] / 2]
    scale = ((_value_at(layer, 'scale', zero, rate, t) or [1.0]) * 2)[:2]
    components = [c for c in layer.get('transforms') or [] if isinstance(c, dict)]
    for prop in ('rotation', 'rotationX', 'rotationY'):
        values = [_value_at(layer, prop, zero, rate, t)] + [_component_at(layer, c, prop, zero, rate, t) for c in components]
        if any(abs(v) > EPS for value in values if value for v in value):
            raise InputError('rotated coverage needs rendered geometry')
    edges = [[pos - pivot * k, pos + (size - pivot) * k]
             for size, pos, pivot, k in zip(extent, position, anchor, scale)]
    # Components are parent-space wrappers, in order, pivoting about the current placement
    # anchor unless they declare a fixed parent-space anchor of their own.
    for component in components:
        pivot = _component_at(layer, component, 'anchor', zero, rate, t) or position
        scale = ((_component_at(layer, component, 'scale', zero, rate, t) or [1.0]) * 2)[:2]
        translation = _component_at(layer, component, 'translation', zero, rate, t) or [0.0, 0.0]
        edges = [[p + (v - p) * k + d for v in edge] for edge, p, k, d in zip(edges, pivot, scale, translation)]
        position = [p + (v - p) * k + d for v, p, k, d in zip(position, pivot, scale, translation)]
    shown_size = []
    for edge, bound in zip(edges, canvas):
        a, b = sorted(edge)
        shown_size.append(max(0.0, min(b, bound) - max(a, 0.0)))
    return tuple(shown_size)


def _cover(shot: _Shot, frame_size: Optional[Tuple[float, float]], t: float) -> float:
    """
    The share of the frame a layer covers at time t: its shown extent times its scale, or all of its
    scene with no extent (footage), carried out through every nested scene's fit and scale.
    """
    if not frame_size:
        return 1.0 if shot.kind in FOOTAGE else 0.0
    canvases = [frame_size]
    chain = [c for c in shot.containers if (c.get('content') or {}).get('kind') in ('composition', 'scene_ref')]
    for c in chain:
        canvases.append(_native_extent(c) if (c.get('content') or {}).get('fit') == 'none' else _canvas(c, canvases[-1]))
    extent = _extent(shot.content)
    if not extent and shot.kind in FOOTAGE and shot.content.get('fit') == 'none':
        extent = _native_extent(shot.layer)
    if not extent:
        if shot.kind in FOOTAGE or shot.kind == 'color':
            extent = canvases[-1]
        else:
            return 0.0
    w, h = _viewport_extent(shot.layer, canvases[-1], extent, shot.zero, shot.rate, t)
    for i in range(len(chain) - 1, -1, -1):
        w, h = _placed_extent(chain[i], canvases[i], canvases[i + 1], (w, h), t)
    return w * h / (frame_size[0] * frame_size[1])


def _camera_shots(shots: List[_Shot]) -> List[_Shot]:
    return [s for s in shots if s.kind in {'media'} | OVERLAYS
            and not any(c.get('cameraExempt') for c in s.containers + (s.layer,))]


def _identity_pivot(camera: Dict[str, Any], shots: List[_Shot], t: float, unit_zoom: bool = True) -> bool:
    """A pivot at unit zoom, or distance at any zoom, has no effect on the unrotated z=0 plane."""
    identity = True
    # A roll turns the picture in its own plane, so it changes what a pivot does but not what
    # distance does: only a tilt gives distance a projection effect.
    props = [('rotationX', 0), ('rotationY', 0)] + ([('rotation', 0), ('zoom', 1)] if unit_zoom else [])
    for prop, default in props:
        value = camera.get(prop, default)
        if isinstance(value, dict):
            if value.get('expression'):
                raise InputError(f'camera {prop} expression needs rendered movement')
            value = (_track_at(value, 0.0, 1.0, t) or [default])[0]
        if abs(value - default) > EPS:
            identity = False
    for shot in shots:
        if not shot.start <= t < shot.end:
            continue
        for layer in shot.containers + (shot.layer,):
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


def pop_move(shots: List[_Shot], camera: Optional[Dict[str, Any]], duration: float, fps: float,
             unchecked: List[Dict[str, str]], frame_size: Optional[Tuple[float, float]] = None) -> List[Dict[str, Any]]:
    out = []
    frame = 1.0 / fps
    sources = [(s.id, s.layer, s.zero, s.rate, s.start, s.end, lambda t, s=s: _cover(s, frame_size, t))
               for s in shots if s.kind in FOOTAGE | OVERLAYS]
    participating = _camera_shots(shots)
    if camera and participating:
        sources.append(('camera', camera, 0.0, 1.0, 0.0, duration,
                        lambda t: any(s.start <= t < s.end for s in participating)))
    for where, layer, zero, rate, start, end, coverage in sources:
        for m in moves(layer, zero, rate, start, end, fps, unchecked, where):
            def covers(t: float) -> bool:
                try:
                    if where == 'camera' and m.prop in ('position', 'distance') and \
                            _identity_pivot(camera, participating, t, unit_zoom=m.prop == 'position'):
                        return False
                    visible = coverage(t)
                    # A pan belongs to a big card if either endpoint qualifies; an endpoint wholly
                    # outside the viewport still cannot pop. Keep that classification over the pan.
                    share = max(coverage(m.start), coverage(m.end)) if m.prop == 'position' else visible
                except InputError as err:
                    unchecked.append({'code': 'pop-move', 'why': f'{where}: {err}'})
                    return False
                return visible > EPS and share >= POP_COVER - EPS
            if m.easing == 'step':
                # A jump shows on both sides of it: a big layer that shrinks away pops as much as one that grows.
                if covers(max(m.start, m.end - frame)) or covers(m.end):
                    out.append(finding('pop-move', m.end - frame, m.end, [where],
                                       f'{m.prop} jumps in one frame at {m.end:.2f} s (a step key)'))
                continue
            if m.rest_before and not m.ramped_in and covers(m.start) and _abrupt(m.easing, m.moving, _slope_start):
                out.append(finding('pop-move', m.start, m.start + frame, [where],
                                   f'{m.prop} move starts abruptly at {m.start:.2f} s (easing {json.dumps(m.easing)})'))
            if m.rest_after and not m.ramped_out and covers(m.end) and _abrupt(m.easing, m.moving, _slope_end):
                out.append(finding('pop-move', m.end - frame, m.end, [where],
                                   f'{m.prop} move stops abruptly at {m.end:.2f} s (easing {json.dumps(m.easing)})'))
    return out


class _Seam:
    def __init__(self, a: _Shot, b: _Shot, time: float, transition: Optional[Dict[str, Any]], overlap: float) -> None:
        self.a, self.b, self.time, self.transition, self.overlap = a, b, time, transition, overlap


def seams(shots: List[_Shot], fps: float) -> List[_Seam]:
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
    loose = [s for s in shots if s.media == 'video' and not (s.containers and (s.containers[-1].get('content') or {}).get('kind') == 'track')]
    for a in loose:
        for b in loose:
            if a is b or a.scope is not b.scope or b.start <= a.start + EPS:
                continue
            overlap = a.end - b.start
            if abs(overlap) <= frame / 2:
                out.append(_Seam(a, b, b.start, None, 0.0))
            elif EPS < overlap < min(a.end - a.start, b.end - b.start) and _fades(a, b):
                out.append(_Seam(a, b, (a.end + b.start) / 2, None, overlap))
    return [s for s in out if s.a.media == 'video' and s.b.media == 'video']


def _fades(a: _Shot, b: _Shot) -> bool:
    """A hand-made dissolve: the incoming layer fades up, or the outgoing one fades out, as they overlap."""
    cuts = {b.start, a.end}
    for shot in (a, b):
        track = (shot.layer.get('animations') or {}).get('opacity') or {}
        if track.get('expression'):
            return False
        base = _key_zero(shot.layer, track, shot.start, shot.zero)
        cuts.update(base + float(k['time']) * shot.rate for k in track.get('keyframes') or []
                    if isinstance(k, dict) and _num(k.get('time')) and b.start < base + float(k['time']) * shot.rate < a.end)

    def opacity(shot: _Shot, t: float) -> float:
        return (_value_at(shot.layer, 'opacity', shot.zero, shot.rate, t) or [1.0])[0]
    times = sorted(cuts)
    for x, y in zip(times, times[1:]):
        t, u = x + (y - x) / 3, x + 2 * (y - x) / 3
        av, bv = opacity(a, t), opacity(b, t)
        if av > 0 and bv > 0 and ((av < 1 and abs(av - opacity(a, u)) > EPS)
                                  or (bv < 1 and abs(bv - opacity(b, u)) > EPS)):
            return True
    return False


def _continuous(a: _Shot, b: _Shot, fps: float) -> bool:
    """One file split with nothing changed: the picture plays on through the seam."""
    if a.source() != b.source() or (a.layer.get('transform') or {}) != (b.layer.get('transform') or {}):
        return False
    ta, tb = a.content.get('trim') or {}, b.content.get('trim') or {}
    return (_num(ta.get('out')) and _num(tb.get('in')) and abs(float(ta['out']) - float(tb['in'])) <= 1.0 / fps
            and a.content.get('speed', 1) == b.content.get('speed', 1))


def joins(shots: List[_Shot], shot_ids: Dict[str, Any], places: Dict[str, Any], fps: float,
          unchecked: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    out = []
    frame = 1.0 / fps
    unknown_shot = False
    for seam in seams(shots, fps):
        a, b, t = seam.a, seam.b, seam.time
        ids = [a.id, b.id]
        transition = seam.transition or {}
        name, length = transition.get('id'), transition.get('duration')
        if seam.overlap:
            name, length = 'opacity fade', seam.overlap
        if name and _num(length) and (name in DISSOLVES or name == 'opacity fade') and length <= GHOST_SECONDS + EPS:
            out.append({**finding('ghost', t - length / 2, t + length / 2, ids,
                                  f'a {length:.2f} s {name} shows both takes at once'), 'at': t})
            continue
        if name and name not in DISSOLVES and name not in MASKING and name != 'opacity fade':
            unchecked.append({'code': 'ghost', 'why': f'transition {name!r} between {a.id} and {b.id} is not in the catalog this script knows'})
        if _continuous(a, b, fps):
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
        if not one_place or name in DISSOLVES - MASKING or name == 'opacity fade':
            continue
        burst = None
        if name and _num(length):
            burst = (t - length / 2, t + length / 2, f'a {length:.2f} s {name} transition')
        else:
            for shot in (a, b):
                for m in moves(shot.layer, shot.zero, shot.rate, shot.start, shot.end, fps, [], shot.id):
                    frames = (m.end - m.start) * fps
                    if m.easing != 'step' and m.start - frame <= t <= m.end + frame and TAKE_MIN_FRAMES - EPS <= frames <= TAKE_MAX_FRAMES + EPS:
                        burst = (m.start, m.end, f'a {frames:.0f}-frame {m.prop} move')
                        break
                if burst:
                    break
        if burst:
            out.append({**finding('hidden-take-change', burst[0], burst[1], ids,
                                  f'{burst[2]} hides a cut: {why or "a cut inside one place"}'), 'at': t})
        elif why:
            out.append(finding('same-scene-cut', t, t + frame, ids, f'hard cut: {why}'))
    if unknown_shot:
        unchecked.append({'code': 'same-scene-cut', 'why': 'no `shots` for some clips: which takes show one shot is in the shot list, not the scene'})
    return out


def blink(shots: List[_Shot], fps: float, unchecked: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    out = []
    limit = BLINK_FRAMES / fps + EPS

    def overlay(s: _Shot) -> bool:
        return s.kind in OVERLAYS or (s.kind == 'media' and s.media != 'video')

    def slot(s: _Shot) -> Any:
        position = (s.layer.get('transform') or {}).get('position')
        return (s.kind, s.asset if s.kind == 'media' else None, json.dumps(position))

    slots: Dict[Any, List[Tuple[float, float, str]]] = {}
    for shot in shots:
        if not overlay(shot):
            continue
        try:
            spans = _visibility(shot)
            if shot.kind == 'captions':
                spans = intersect(spans, _caption_spans(shot))
        except InputError as err:
            unchecked.append({'code': 'blink', 'why': f'{shot.id}: {err}'})
            continue
        slots.setdefault((shot.scope, slot(shot)), []).extend((a, b, shot.id) for a, b in spans)
    for occupancy in slots.values():
        spans = merge((a, b) for a, b, _ in occupancy)
        for (_, end), (start, _) in zip(spans, spans[1:]):
            if EPS < start - end <= limit:
                ids = sorted({lid for a, b, lid in occupancy if abs(b - end) <= EPS or abs(a - start) <= EPS})
                out.append(finding('blink', end, start, ids,
                                   f'the overlay vanishes for {round((start - end) * fps)} frame(s) and returns'))
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
                 for a, b, _ in caption_blocks(shot.content, shot.start, readable=True))


def _distance_spans(camera: Dict[str, Any], shots: List[_Shot], move: _Move,
                    unchecked: List[Dict[str, str]]) -> List[Span]:
    """Distance moves only where the camera sees depth or tilt; split at keys and picture changes."""
    cuts = {move.start, move.end}
    tracks = [(camera, camera, 0.0, 1.0, ('rotation', 'rotationX', 'rotationY'))]
    for shot in shots:
        cuts.update((shot.start, shot.end))
        for layer in shot.containers + (shot.layer,):
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
            if not all(_identity_pivot(camera, shots, t, unit_zoom=False) for t in (a + EPS, (a + b) / 2, b - EPS)):
                out.append((a, b))
        except InputError as err:
            unchecked.append({'code': 'zoom-idle', 'why': f'camera: {err}'})
    return out


def zoom_idle(shots: List[_Shot], camera: Optional[Dict[str, Any]], duration: float, fps: float,
              unchecked: List[Dict[str, str]], allowed: Optional[List[Span]] = None) -> List[Dict[str, Any]]:
    out = []
    footage = [s for s in shots if s.kind == 'media']
    sources: List[Tuple[str, List[_Move], List[_Shot]]] = []
    for s in footage:
        sources.append((s.id, moves(s.layer, s.zero, s.rate, s.start, s.end, fps, [], s.id), [s]))
    for s in shots:
        if s.kind in ('track', 'composition', 'scene_ref'):
            inside = [f for f in footage if any(c is s.layer for c in f.containers)]
            sources.append((s.id, moves(s.layer, s.zero, s.rate, s.start, s.end, fps, [], s.id), inside))
    if camera:
        sources.append(('camera', moves(camera, 0.0, 1.0, 0.0, duration, fps, [], 'camera'),
                        _camera_shots(footage)))
    for where, found, covered in sources:
        zooming = merge(span for m in found if m.prop in ZOOMS and m.easing != 'step'
                        for span in (_distance_spans(camera, _camera_shots(shots), m, unchecked)
                                     if where == 'camera' and m.prop == 'distance' else [(m.start, m.end)]))
        # Allowed spans come off before the length is measured, so a zoom that runs just past a
        # span leaves no sliver to fail.
        zooming = subtract(zooming, allowed or [])
        if not zooming or not covered:
            continue
        for a, b in (piece for still in all_still(covered) for piece in intersect(zooming, [still])):
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
    shots = [_Shot(layer, start, zero, end) for layer, start, zero, end in _visits(scene, 0.0, math.inf, set(), opacity=False)
             if (layer.get('content') or {}).get('kind') != 'audio' and math.isfinite(end)]
    duration = max([s.end for s in shots], default=0.0)
    if _num(comp.get('duration')) and comp['duration'] > 0:
        duration = float(comp['duration'])
    camera = comp.get('camera') if isinstance(comp.get('camera'), dict) else None
    if camera and isinstance(camera.get('animations'), dict):
        camera = {**{k: v for k, v in camera.items() if k != 'animations'}, **camera['animations']}

    unchecked: List[Dict[str, str]] = []
    # Picture checks read only what shows; joins keep whole layers, so an opacity dip is no cut
    # and a track's transitions keep their clip indices.
    visible = []
    for shot in shots:
        try:
            for a, b in _visibility(shot):
                view = copy.copy(shot)
                view.start, view.end = a, b
                visible.append(view)
        except InputError as err:
            for code in ('pop-move', 'screen-still', 'zoom-idle'):
                unchecked.append({'code': code, 'why': f'{shot.id}: {err}'})
    found = screen_still(visible, spans, fps)
    frame_size = (float(comp['width']), float(comp['height'])) if _num(comp.get('width')) and _num(comp.get('height')) \
        and comp['width'] > 0 and comp['height'] > 0 else None
    for check in (pop_move(visible, camera, duration, fps, unchecked, frame_size), joins(shots, shot_ids, places, fps, unchecked),
                  blink(shots, fps, unchecked), [] if slides else zoom_idle(visible, camera, duration, fps, unchecked, allowed)):
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
