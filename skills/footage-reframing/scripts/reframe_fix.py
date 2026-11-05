#!/usr/bin/env python3
"""
Check a reframe's camera path, and correct it by hand where the tool got it wrong.

    python3 scripts/reframe_fix.py check framing.json
    python3 scripts/reframe_fix.py fix framing.json
    python3 scripts/reframe_fix.py check-crops crops.json

The input is one JSON object, every time in the source's own seconds:

    {
      "reframe": "reframe-talk.json",
      "width": 1080,
      "subjects": {
        "ana":  {"boxes": [{"t": 0, "box": [310, 120, 260, 520]}]},
        "ben":  {"boxes": [{"t": 0, "box": [1250, 140, 250, 500]}, {"t": 30, "box": [1300, 140, 250, 500]}]},
        "logo": {"boxes": [{"t": 0, "box": [900, 40, 120, 60]}]}
      },
      "speakers": [{"who": "ana", "start": 0.4, "end": 6.1}, {"who": "ben", "start": 6.5, "end": 12.0}],
      "keep": ["logo"],
      "spans": [{"start": 20, "end": 24, "hold": 0.3}, {"start": 30, "end": 34, "static": true}],
      "out": "reframe-talk.fixed.json"
    }

- `reframe` is the saved `picsart_media_reframe_video` result (or its path, relative to this file).
- `width` is the delivery frame's width, to say how far a soft stretch is blown up; default the
  reframe's own.
- `subjects` are boxes `[x, y, w, h]` in source pixels around what must stay in frame: a person's
  head and hands, a product, a sign. Read them from stills or `picsart_media_track_motion`. One
  box holds for the whole source; several are joined in a line, and hold 0.5 s past each end.
- `speakers` come from the transcript: who speaks, from when to when. With them, the camera holds
  on the speaker and cuts at each change of speaker, a turn shorter than `min_shot` excepted.
- `keep` names subjects kept inside the safe area whenever their box is known.
- `spans` override a stretch: `follow` a subject, `hold` a still window centred 0 to 1 across the
  source, `static` (the tool's own median window, held), or `auto` (the tool's path as it is,
  unsmoothed). With no speakers and no span, the tool's path is kept, smoothed.
- Tunables, all optional: `safe` ({"x": 0.06, "top": 0.08, "bottom": 0.12}, shares of the frame),
  `smooth` (0.6 s), `min_shot` (1.2 s), `lead` (0.1 s before a new speaker), `max_zoom` (1.5 times
  the zoom that just covers the frame), `tolerance_px` (2).

`check` prints `{"ok", "findings"}`: each finding has a `kind` (`cut-off`, `wrong-person`,
`late-cut`, `jumpy-cut`, `jitter`, `wander`, `soft`), its `start` and `end` and what it concerns.
`fix` builds a new camera path, smoothed, held during speech, cut on each change of speaker,
clamped to the safe area and to the source, and prints `{"before", "after", "notes"}` with the
corrected result written to `out` (or printed as `reframe` without `out`). The corrected result has
the tool's shape, so `scripts/reel_cut.py` cuts from it as it does from the original.

`check-crops` checks a split's fixed crops (reel_cut.py's `crops`) before anything is built:
`{"crops": {"annie": [110, 90, 500, 444]}, "faces": {"annie": [180, 130, 200, 230]}}`, each face a
box (or a list of boxes, one per still) in source pixels, read from a still of each shot type. A
face must sit inside its crop less 8 % of its height at the top, 6 % of its width at each side and
12 % of its height at the bottom. It prints `{"ok", "findings"}`, each finding naming the crop, the
edge and how many pixels to move it. A crop with no face given is a finding too: check it on a still.

Python 3.9 or later, the standard library only, offline. It reads no media.
"""
from __future__ import annotations

import copy
import json
import math
import os
import sys
from typing import Any, Dict, List, Optional, Set, Tuple

from reel_cut import InputError, evaluate, number, read_json_file, read_reframe

USAGE = 'usage: reframe_fix.py check|fix|check-crops input.json'
# A face's margin inside a fixed crop, as shares of the crop: the top, each side, the bottom.
CROP_MARGIN = {'top': 0.08, 'x': 0.06, 'bottom': 0.12}

RATE = 10.0                 # camera samples per second
SAFE = {'x': 0.06, 'top': 0.08, 'bottom': 0.12}
SMOOTH = 0.6                # s, the moving average inside one shot
MIN_SHOT = 1.2              # s, a shorter speaker turn gets no cut of its own
LEAD = 0.1                  # s, a cut lands this far before the new speaker's first word
MAX_ZOOM = 1.5              # times the zoom that just covers the frame
TOLERANCE_PX = 2.0          # keyframe decimation, frame px
DEADBAND = 0.02             # a shot whose camera moves less than this share of the source is held
LATE = 0.4                  # s, a camera that reaches the new speaker later than this is late
JUMP = 0.15                 # share of the source the camera crosses in one sample to count as a cut
NEAR_CHANGE = 0.3           # s, a cut this close to a change of speaker is on it
REVERSALS = 3               # direction changes in one second that read as jitter
WANDER = 0.08               # share of the source the camera drifts over a still speaker
STILL = 0.03                # share of the source a speaker may move and still count as still
BOX_REACH = 0.5             # s a subject's first and last box hold past their time

Json = Dict[str, Any]
Box = Tuple[float, float, float, float]
Cam = Tuple[float, float, float]   # centre x, centre y in source px, and zoom


# --- Reading the input ----------------------------------------------------------------------


def read_input(data: Any, base: str) -> Json:
    if not isinstance(data, dict):
        raise InputError('the input must be a JSON object')
    raw = data.get('reframe')
    if isinstance(raw, str):
        raw = read_json_file(os.path.join(base, raw), 'reframe')
    if not isinstance(raw, dict):
        raise InputError('reframe must be the picsart_media_reframe_video result, or the path of its file')
    path = read_reframe('input', raw)
    subjects = read_subjects(data.get('subjects') or {})
    speakers = read_speakers(data.get('speakers') or [], subjects)
    keep = data.get('keep') or []
    if not isinstance(keep, list) or any(k not in subjects for k in keep):
        raise InputError('keep must list subjects named in subjects')
    safe = dict(SAFE, **(data.get('safe') or {}))
    for k in ('x', 'top', 'bottom'):
        v = number(safe[k], f'safe {k}', positive=False)
        if not 0 <= v < 0.4:
            raise InputError(f'safe {k} is a share of the frame, from 0 to 0.4')
        safe[k] = v
    fw = path['frame'][0]
    return {
        'raw': raw, 'path': path, 'subjects': subjects, 'speakers': speakers, 'keep': keep,
        'spans': read_spans(data.get('spans') or [], subjects, path['duration']),
        'safe': safe,
        'width': number(data.get('width', fw), 'width'),
        'smooth': number(data.get('smooth', SMOOTH), 'smooth', positive=False),
        'min_shot': number(data.get('min_shot', MIN_SHOT), 'min_shot', positive=False),
        'lead': number(data.get('lead', LEAD), 'lead', positive=False),
        'max_zoom': max(1.0, number(data.get('max_zoom', MAX_ZOOM), 'max_zoom')),
        'tolerance': number(data.get('tolerance_px', TOLERANCE_PX), 'tolerance_px'),
        'out': data.get('out'),
    }


def read_subjects(raw: Any) -> Dict[str, List[Tuple[float, Box]]]:
    if not isinstance(raw, dict):
        raise InputError('subjects must be an object of named subjects')
    out = {}
    for name, s in raw.items():
        boxes = (s or {}).get('boxes') if isinstance(s, dict) else None
        if not isinstance(boxes, list) or not boxes:
            raise InputError(f'subjects "{name}" needs boxes: [{{"t": seconds, "box": [x, y, w, h]}}]')
        rows = []
        for i, b in enumerate(boxes):
            box = b.get('box') if isinstance(b, dict) else None
            if not isinstance(box, list) or len(box) != 4:
                raise InputError(f'subjects "{name}" boxes[{i}] needs a box [x, y, w, h] in source pixels')
            x, y = (number(v, f'subjects "{name}" boxes[{i}] box', positive=False) for v in box[:2])
            w, h = (number(v, f'subjects "{name}" boxes[{i}] box size') for v in box[2:])
            rows.append((number(b.get('t', 0), f'subjects "{name}" boxes[{i}] t', positive=False), (x, y, w, h)))
        out[name] = sorted(rows, key=lambda r: r[0])
    return out


def read_speakers(raw: Any, subjects: Json) -> List[Json]:
    if not isinstance(raw, list):
        raise InputError('speakers must be a list of {who, start, end}')
    turns = []
    for i, t in enumerate(raw):
        if not isinstance(t, dict) or t.get('who') not in subjects:
            raise InputError(f'speakers[{i}] names who speaks, a subject with boxes')
        start = number(t.get('start'), f'speakers[{i}] start', positive=False)
        end = number(t.get('end'), f'speakers[{i}] end')
        if end <= start:
            raise InputError(f'speakers[{i}] needs start < end')
        turns.append({'who': t['who'], 'start': start, 'end': end})
    turns.sort(key=lambda t: t['start'])
    merged: List[Json] = []
    for t in turns:
        if merged and merged[-1]['who'] == t['who'] and t['start'] <= merged[-1]['end']:
            merged[-1]['end'] = max(merged[-1]['end'], t['end'])
        else:
            merged.append(dict(t))
    return merged


def read_spans(raw: Any, subjects: Json, duration: float) -> List[Json]:
    if not isinstance(raw, list):
        raise InputError('spans must be a list')
    spans = []
    for i, s in enumerate(raw):
        if not isinstance(s, dict):
            raise InputError(f'spans[{i}] must be an object')
        start = number(s.get('start'), f'spans[{i}] start', positive=False)
        end = min(number(s.get('end'), f'spans[{i}] end'), duration)
        if end <= start:
            raise InputError(f'spans[{i}] needs start < end, inside the source')
        modes = [k for k in ('follow', 'hold', 'static', 'auto') if s.get(k) is not None and s.get(k) is not False]
        if len(modes) != 1:
            raise InputError(f'spans[{i}] takes exactly one of follow, hold, static or auto')
        mode = modes[0]
        if mode == 'follow' and s['follow'] not in subjects:
            raise InputError(f'spans[{i}] follows "{s["follow"]}", which is not in subjects')
        if mode == 'hold':
            hold = number(s['hold'], f'spans[{i}] hold', positive=False)
            if not 0 <= hold <= 1:
                raise InputError(f'spans[{i}] hold is a centre across the source, from 0 to 1')
            spans.append({'start': start, 'end': end, 'mode': ('hold', hold)})
        else:
            spans.append({'start': start, 'end': end, 'mode': (mode, s[mode]) if mode == 'follow' else (mode,)})
    return sorted(spans, key=lambda s: s['start'])


# --- Geometry -------------------------------------------------------------------------------


def camera(path: Json, t: float) -> Cam:
    """The source point at the frame's centre, and the zoom, at `t`."""
    fw, fh = path['frame']
    sw, sh = path['size']
    px, py = evaluate(path['position'], t)
    s = evaluate(path['scale'], t)[0]
    return (sw / 2 + (fw / 2 - px) / s, sh / 2 + (fh / 2 - py) / s, s)


def position_of(path: Json, cam: Cam) -> List[float]:
    fw, fh = path['frame']
    sw, sh = path['size']
    cx, cy, s = cam
    return [round(fw / 2 - (cx - sw / 2) * s, 3), round(fh / 2 - (cy - sh / 2) * s, 3)]


def view(path: Json, cam: Cam) -> Box:
    """The source rectangle the frame shows."""
    fw, fh = path['frame']
    cx, cy, s = cam
    return (cx - fw / s / 2, cy - fh / s / 2, fw / s, fh / s)


def safe_view(path: Json, cam: Cam, safe: Json) -> Box:
    x, y, w, h = view(path, cam)
    return (x + safe['x'] * w, y + safe['top'] * h, w * (1 - 2 * safe['x']), h * (1 - safe['top'] - safe['bottom']))


def cover(path: Json) -> float:
    fw, fh = path['frame']
    sw, sh = path['size']
    return max(fw / sw, fh / sh)


def inside(box: Box, area: Box, slack: float = 0.5) -> bool:
    return (box[0] >= area[0] - slack and box[1] >= area[1] - slack
            and box[0] + box[2] <= area[0] + area[2] + slack and box[1] + box[3] <= area[1] + area[3] + slack)


def box_at(rows: List[Tuple[float, Box]], t: float) -> Optional[Box]:
    """A subject's box at `t`: one box holds throughout; several are joined in a line."""
    if len(rows) == 1:
        return rows[0][1]
    if t < rows[0][0] - BOX_REACH or t > rows[-1][0] + BOX_REACH:
        return None
    if t <= rows[0][0]:
        return rows[0][1]
    for (ta, a), (tb, b) in zip(rows, rows[1:]):
        if ta <= t <= tb:
            f = 0 if tb == ta else (t - ta) / (tb - ta)
            return tuple(a[i] + f * (b[i] - a[i]) for i in range(4))
    return rows[-1][1]


def centre(box: Box) -> Tuple[float, float]:
    return (box[0] + box[2] / 2, box[1] + box[3] / 2)


def median(values: List[float]) -> float:
    v = sorted(values)
    n = len(v)
    return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2


def sample_times(t0: float, t1: float) -> List[float]:
    n = max(1, int(math.floor((t1 - t0) * RATE + 1e-9)))
    ts = [round(t0 + i / RATE, 4) for i in range(n)]
    return [t for t in ts if t < t1] or [t0]


# --- Who the camera should be on -------------------------------------------------------------


def shots(inp: Json) -> List[Json]:
    """The source cut into shots, each with what the camera does in it."""
    duration = inp['path']['duration']
    base: List[Json] = []
    turns = [t for t in inp['speakers'] if t['end'] - t['start'] >= inp['min_shot']]
    if turns:
        start = 0.0
        for a, b in zip(turns, turns[1:]):
            cut = b['start'] if b['start'] <= a['end'] else max(a['end'], b['start'] - inp['lead'])
            base.append({'start': start, 'end': cut, 'mode': ('follow', a['who'])})
            start = cut
        base.append({'start': start, 'end': duration, 'mode': ('follow', turns[-1]['who'])})
    else:
        base.append({'start': 0.0, 'end': duration, 'mode': ('tool',)})   # the tool's path, smoothed
    for span in inp['spans']:
        cut: List[Json] = []
        for b in base:
            if b['end'] <= span['start'] or b['start'] >= span['end']:
                cut.append(b)
                continue
            if b['start'] < span['start']:
                cut.append(dict(b, end=span['start']))
            if b['end'] > span['end']:
                cut.append(dict(b, start=span['end']))
        cut.append(dict(span, span=True))
        base = sorted(cut, key=lambda b: b['start'])
    merged: List[Json] = []
    for b in base:
        if b['end'] - b['start'] <= 1e-6:
            continue
        if (merged and merged[-1]['mode'] == b['mode'] and abs(merged[-1]['end'] - b['start']) < 1e-6
                and not (merged[-1].get('span') and b.get('span'))):
            merged[-1]['end'] = b['end']
        else:
            merged.append(dict(b))
    for m in merged:
        m.pop('span', None)
    return merged


def tool_cuts(path: Json, t0: float, t1: float) -> List[float]:
    """Where the tool itself cut inside a stretch: its `step` keyframes."""
    return sorted({b['time'] for keys in (path['position'], path['scale'])
                   for a, b in zip(keys, keys[1:]) if a.get('easing') == 'step' and t0 < b['time'] < t1})


def ends_in_step(path: Json, t: float) -> Set[str]:
    """The tracks ('position', 'scale') whose own `step` keyframe hands over exactly at `t`."""
    return {track for track in ('position', 'scale')
            if any(a.get('easing') == 'step' and abs(b['time'] - t) < 1e-6
                   for a, b in zip(path[track], path[track][1:]))}


# --- Correcting -----------------------------------------------------------------------------


def fit(path: Json, cam: Cam, box: Box, safe: Json, lo: float) -> Tuple[Cam, bool]:
    """Move (and if need be widen) the window the least so `box` sits in the safe area."""
    fw, fh = path['frame']
    cx, cy, s = cam
    need = max(box[2] / (fw * (1 - 2 * safe['x'])), box[3] / (fh * (1 - safe['top'] - safe['bottom'])))
    fits = True
    if need > 1 / s:
        s = max(lo, 1 / need)
        fits = 1 / s >= need - 1e-9
    sx, sy, sw_, sh_ = safe_view(path, (cx, cy, s), safe)
    if box[2] <= sw_:
        if box[0] < sx:
            cx -= sx - box[0]
        elif box[0] + box[2] > sx + sw_:
            cx += box[0] + box[2] - sx - sw_
    else:
        cx = centre(box)[0]
    if box[3] <= sh_:
        if box[1] < sy:
            cy -= sy - box[1]
        elif box[1] + box[3] > sy + sh_:
            cy += box[1] + box[3] - sy - sh_
    else:
        cy = box[1] - safe['top'] * fh / s + fh / s / 2   # too tall: keep its top, the head
    return (cx, cy, s), fits


def clamp(path: Json, cam: Cam, lo: float, hi: float) -> Cam:
    """No edge of the source inside the frame, and no zoom past `hi`."""
    fw, fh = path['frame']
    sw, sh = path['size']
    cx, cy, s = cam
    s = min(max(s, lo), hi)
    hw, hh = fw / s / 2, fh / s / 2
    cx = sw / 2 if hw * 2 >= sw else min(max(cx, hw), sw - hw)
    cy = sh / 2 if hh * 2 >= sh else min(max(cy, hh), sh - hh)
    return (cx, cy, s)


def smooth(values: List[float], radius: int) -> List[float]:
    if radius <= 0 or len(values) < 3:
        return list(values)
    out = []
    for i in range(len(values)):
        a, b = max(0, i - radius), min(len(values), i + radius + 1)
        out.append(sum(values[a:b]) / (b - a))
    return out


def plan_shot(inp: Json, shot: Json, notes: List[str]) -> List[Tuple[float, Cam]]:
    path, safe = inp['path'], inp['safe']
    sw = path['size'][0]
    lo, hi = cover(path), cover(path) * inp['max_zoom']
    ts = sample_times(shot['start'], shot['end'])
    tool = [camera(path, t) for t in ts]
    zoom = min(max(median([c[2] for c in tool]), lo), hi)
    mode = shot['mode']
    followed = None
    if mode[0] in ('auto', 'tool'):
        cams = [clamp(path, c, lo, hi) for c in tool]
    elif mode[0] == 'static':
        cams = [(median([c[0] for c in tool]), median([c[1] for c in tool]), zoom)] * len(ts)
    elif mode[0] == 'hold':
        cams = [(mode[1] * sw, median([c[1] for c in tool]), zoom)] * len(ts)
    else:
        followed = mode[1]
        boxes = [box_at(inp['subjects'][followed], t) for t in ts]
        known = [centre(b)[0] for b in boxes if b is not None]
        if not known:
            notes.append(f'{fmt(shot["start"])}-{fmt(shot["end"])}: no box for "{followed}" there; the tool\'s path is kept')
            cams = [clamp(path, c, lo, hi) for c in tool]
            followed = None
        else:
            cy = median([c[1] for c in tool])
            width = path['frame'][0] / zoom
            if max(known) - min(known) <= width / 2:
                hold = median(known)
                cams = [(hold, cy, zoom)] * len(ts)
            else:
                last = known[0]
                cams = []
                for b in boxes:
                    last = centre(b)[0] if b is not None else last
                    cams.append((last, cy, zoom))
    # An explicit `auto` span keeps the tool's own motion: no smoothing and no deadband.
    radius = 0 if mode[0] == 'auto' else int(round(inp['smooth'] * RATE / 2))
    xs, ys, ss = (smooth([c[i] for c in cams], radius) for i in range(3))
    for values, scale in (((xs, sw), (ys, path['size'][1]), (ss, None)) if mode[0] != 'auto' else ()):
        spread = max(values) - min(values)
        if spread < DEADBAND * (scale if scale else median(values)):
            m = median(values)
            values[:] = [m] * len(values)
    cams = list(zip(xs, ys, ss))
    out = []
    lost = []
    for t, cam in zip(ts, cams):
        cam = clamp(path, cam, lo, hi)
        wanted = []
        if followed is not None and box_at(inp['subjects'][followed], t) is not None:
            wanted.append((followed, box_at(inp['subjects'][followed], t)))
        wanted += [(k, box_at(inp['subjects'][k], t)) for k in inp['keep'] if k != followed]
        # A subject with no box at this moment is skipped, so the first one kept is a known one.
        wanted = [(k, box) for k, box in wanted if box is not None]
        for k, box in wanted:
            if box is None:
                continue
            moved, fits = fit(path, cam, box, safe, lo)
            moved = clamp(path, moved, lo, hi)
            first = wanted[0][1]
            if k != wanted[0][0] and not inside(first, safe_view(path, moved, safe)):
                lost.append(k)
                continue
            if not fits or not inside(box, safe_view(path, moved, safe)):
                lost.append(k)
            cam = moved
        out.append((t, cam))
    for k in sorted(set(lost)):
        notes.append(f'{fmt(shot["start"])}-{fmt(shot["end"])}: "{k}" does not fit the safe area with what the '
                     'camera must hold; hold one subject, or stack the two for this stretch')
    return out


def fix(inp: Json) -> Tuple[Json, List[str]]:
    path = inp['path']
    notes: List[str] = []
    plan = shots(inp)
    fps = float((inp['raw'].get('scene', inp['raw']).get('composition') or {}).get('fps') or 30)
    position: List[Json] = []
    scale: List[Json] = []
    for n, shot in enumerate(plan):
        bounds = [shot['start']] + (tool_cuts(path, shot['start'], shot['end']) if shot['mode'][0] in ('auto', 'tool') else []) + [shot['end']]
        for a, b in zip(bounds, bounds[1:]):
            samples = plan_shot(inp, dict(shot, start=a, end=b), notes)
            last = b >= path['duration'] - 1e-6
            # An auto span that ends on the tool's own step keeps that step: the hold before it stays put, then jumps.
            steps = ends_in_step(path, b) if last and shot['mode'][0] == 'auto' else set()
            step_end = bool(steps)
            eps = min(1 / fps, (b - a) / 2)
            if not last or step_end:
                samples = [s for s in samples if s[0] < b - eps] or samples[:1]
                hold = samples[-1][1]
                if step_end:
                    # The planned camera at b - eps, whole: a track that steps at b still has its pre-step value
                    # there, and the other one has carried on. Its centre and zoom only make sense together.
                    hold = plan_shot(inp, dict(shot, start=round(b - eps, 4), end=round(b - eps, 4)), [])[-1][1]
                samples.append((round(b - eps, 4), hold))
            if step_end:
                samples.extend(plan_shot(inp, dict(shot, start=path['duration'], end=path['duration']), []))
            elif last and shot['mode'][0] == 'auto':
                samples.extend(plan_shot(inp, dict(shot, start=path['duration'], end=path['duration']), []))
            elif last:
                samples.append((path['duration'], samples[-1][1]))
            keys = decimate(path, samples, inp['tolerance'])
            if step_end and keys[-2][0] != round(b - eps, 4):
                keys.insert(-1, samples[-2])
            for i, (t, cam) in enumerate(keys):
                end_step = i == len(keys) - 1 and not last
                hold_key = step_end and i == len(keys) - 2
                position.append({'time': round(t, 4), 'value': position_of(path, cam),
                                 'easing': 'step' if end_step or (hold_key and 'position' in steps) else 'linear'})
                scale.append({'time': round(t, 4), 'value': [round(cam[2], 6)] * 2,
                              'easing': 'step' if end_step or (hold_key and 'scale' in steps) else 'linear'})
    position[-1].pop('easing', None)
    scale[-1].pop('easing', None)
    result = copy.deepcopy(inp['raw'])
    scene = result.get('scene', result)
    layer = scene['layers'][0]
    for axis in ('position', 'scale'):
        (layer.get('transform') or {}).pop(axis, None)
    layer.setdefault('animations', {})
    layer['animations']['position'] = {'keyframes': position}
    layer['animations']['scale'] = {'keyframes': scale}
    if 'keyframeCount' in result:
        result['keyframeCount'] = len(position) + len(scale)
    result['corrected'] = {'by': 'reframe_fix.py', 'shots': [
        {'start': round(s['start'], 3), 'end': round(s['end'], 3), 'camera': ':'.join(str(m) for m in s['mode'])} for s in plan]}
    return result, notes


def decimate(path: Json, samples: List[Tuple[float, Cam]], tol: float) -> List[Tuple[float, Cam]]:
    """The fewest keyframes whose straight lines stay within `tol` frame px of every sample."""
    if len(samples) <= 2:
        return samples
    half = path['frame'][0] / 2

    def err(i: int, a: int, b: int) -> float:
        ta, tb, t = samples[a][0], samples[b][0], samples[i][0]
        f = 0 if tb == ta else (t - ta) / (tb - ta)
        start, end, here = (position_of(path, samples[k][1]) for k in (a, b, i))
        line = [start[j] + f * (end[j] - start[j]) for j in range(2)]
        sa, sb, s = samples[a][1][2], samples[b][1][2], samples[i][1][2]
        return max(math.hypot(line[0] - here[0], line[1] - here[1]), abs(sa + f * (sb - sa) - s) * half)

    keep = {0, len(samples) - 1}
    stack = [(0, len(samples) - 1)]
    while stack:
        a, b = stack.pop()
        worst, at = 0.0, None
        for i in range(a + 1, b):
            e = err(i, a, b)
            if e > worst:
                worst, at = e, i
        if at is not None and worst > tol:
            keep.add(at)
            stack += [(a, at), (at, b)]
    return [samples[i] for i in sorted(keep)]


# --- Checking -------------------------------------------------------------------------------


def fmt(t: float) -> str:
    return f'{t:.1f}s'


def spans_of(hits: List[Tuple[float, bool]], gap: float = 0.25) -> List[Tuple[float, float]]:
    out: List[List[float]] = []
    for t, hit in hits:
        if not hit:
            continue
        if out and t - out[-1][1] <= gap:
            out[-1][1] = t
        else:
            out.append([t, t])
    return [(round(a, 2), round(b + 1 / RATE, 2)) for a, b in out]


def check(inp: Json, path: Json) -> List[Json]:
    """What is wrong with a camera path: each finding a kind, a stretch and what it concerns."""
    duration = path['duration']
    ts = sample_times(0, duration) + [duration]
    cams = [camera(path, t) for t in ts]
    sw = path['size'][0]
    findings: List[Json] = []
    turns = [t for t in inp['speakers'] if t['end'] - t['start'] >= inp['min_shot']]

    def speaking(t: float) -> Optional[str]:
        for turn in inp['speakers']:
            if turn['start'] <= t < turn['end']:
                return turn['who']
        return None

    # Cut off: what must be kept inside the safe area; the speaker, once the camera is on them.
    for name in inp['subjects']:
        hits = []
        for t, cam in zip(ts, cams):
            box = box_at(inp['subjects'][name], t)
            if box is None:
                hits.append((t, False))
            elif name in inp['keep']:
                hits.append((t, not inside(box, safe_view(path, cam, inp['safe']))))
            else:
                hits.append((t, speaking(t) == name and inside_point(centre(box), view(path, cam))
                             and not inside(box, safe_view(path, cam, inp['safe']))))
        for a, b in spans_of(hits):
            findings.append({'kind': 'cut-off', 'who': name, 'start': a, 'end': b})

    # Wrong person, and late cuts, from the transcript.
    for turn in turns:
        who = turn['who']
        on = []
        for t, cam in zip(ts, cams):
            box = box_at(inp['subjects'][who], t) if turn['start'] <= t < turn['end'] else None
            if box is not None:
                on.append((t, inside_point(centre(box), view(path, cam))))
        reached = next((t for t, hit in on if hit), None)
        if reached is None:
            wrong = [(t, t >= turn['start'] + LATE) for t, _ in on]
        else:
            # Late only when the camera was seen off the speaker first, not when their boxes start later.
            if not on[0][1] and reached - turn['start'] > LATE:
                findings.append({'kind': 'late-cut', 'who': who, 'start': round(turn['start'], 2),
                                 'end': round(reached, 2), 'late': round(reached - turn['start'], 2)})
            wrong = [(t, t > reached and not hit) for t, hit in on]
        for a, b in spans_of(wrong):
            findings.append({'kind': 'wrong-person', 'who': who, 'start': a, 'end': b})

    # Motion, on both axes: a portrait source reframed to landscape moves the camera up and down.
    sizes = path['size']
    changes = [t['start'] for t in turns[1:]]
    pairs = list(zip(zip(ts, cams), zip(ts[1:], cams[1:])))

    # Jumpy cuts: the camera leaps where nobody new starts to speak.
    jumps = sorted({t1 for (t0, c0), (t1, c1) in pairs for ax in (0, 1) if abs(c1[ax] - c0[ax]) > JUMP * sizes[ax]})
    for t in jumps:
        if not any(abs(t - c) <= NEAR_CHANGE + LATE for c in changes):
            findings.append({'kind': 'jumpy-cut', 'start': round(t - 1 / RATE, 2), 'end': round(t, 2)})

    # Jitter: the camera turning back and forth within a second.
    flips: List[float] = []
    for ax in (0, 1):
        moves = [(t1, c1[ax] - c0[ax]) for (t0, c0), (t1, c1) in pairs
                 if 0.003 * sizes[ax] < abs(c1[ax] - c0[ax]) <= JUMP * sizes[ax]]
        flips += [m[0] for n, m in zip(moves, moves[1:]) if (n[1] > 0) != (m[1] > 0) and m[0] - n[0] <= 2 / RATE]
    # A diagonal reversal turns both axes at once: count it once.
    flips = sorted(set(flips))
    jittery = [(t, sum(1 for f in flips if t <= f < t + 1) >= REVERSALS) for t in ts]
    for a, b in spans_of(jittery, gap=1.0):
        findings.append({'kind': 'jitter', 'start': a, 'end': round(min(b + 1, duration), 2)})

    # Wander: the camera drifting over a speaker who sits still.
    for turn in turns:
        if turn['end'] - turn['start'] < 2:
            continue
        inside_turn = [(t, c) for t, c in zip(ts, cams) if turn['start'] + LATE <= t < turn['end']]
        boxes = [box_at(inp['subjects'][turn['who']], t) for t, _ in inside_turn]
        if not inside_turn or any(b is None for b in boxes) or any(turn['start'] < j < turn['end'] for j in jumps):
            continue
        for ax in (0, 1):
            cs = [c[ax] for _, c in inside_turn]
            bs = [centre(b)[ax] for b in boxes]
            if max(cs) - min(cs) > WANDER * sizes[ax] and max(bs) - min(bs) < STILL * sizes[ax]:
                findings.append({'kind': 'wander', 'who': turn['who'], 'start': round(turn['start'], 2),
                                 'end': round(turn['end'], 2), 'drift': round((max(cs) - min(cs)) / sizes[ax], 3)})
                break

    # Soft: zoomed in past the window that just covers the frame, so far the picture turns soft.
    # The upscale (delivery px per source px) is said with it; at the covering zoom it cannot drop.
    lo = cover(path)
    soft = [(t, c[2] > lo * inp['max_zoom'] + 1e-6) for t, c in zip(ts, cams)]
    for a, b in spans_of(soft):
        worst = max(c[2] for t, c in zip(ts, cams) if a <= t <= b)
        findings.append({'kind': 'soft', 'start': a, 'end': b, 'zoom': round(worst / lo, 2),
                         'upscale': round(inp['width'] / (path['frame'][0] / worst), 2)})
    return sorted(findings, key=lambda f: (f['start'], f['kind']))


def inside_point(p: Tuple[float, float], area: Box) -> bool:
    return area[0] <= p[0] <= area[0] + area[2] and area[1] <= p[1] <= area[1] + area[3]


# --- The command ----------------------------------------------------------------------------


def check_crops(data: Any) -> Json:
    """Each face inside its fixed crop, with the margins a face needs."""
    if not isinstance(data, dict) or not isinstance(data.get('crops'), dict) or not data['crops']:
        raise InputError('check-crops needs "crops": named [x, y, w, h] boxes in source pixels')
    faces = data.get('faces') if isinstance(data.get('faces'), dict) else {}
    findings: List[Json] = []
    for name, crop in data['crops'].items():
        if not (isinstance(crop, list) and len(crop) == 4):
            raise InputError(f'crops "{name}" must be [x, y, w, h]')
        x, y, w, h = (number(v, f'crops "{name}"', positive=False) for v in crop)
        raw = faces.get(name)
        if raw is None:
            findings.append({'crop': name, 'problem': 'unchecked', 'what': 'no face given: check it on a still of its shot'})
            continue
        boxes = raw if raw and isinstance(raw[0], list) else [raw]
        left, right = x + CROP_MARGIN['x'] * w, x + w - CROP_MARGIN['x'] * w
        top, bottom = y + CROP_MARGIN['top'] * h, y + h - CROP_MARGIN['bottom'] * h
        for k, box in enumerate(boxes):
            fx, fy, fw, fh = (number(v, f'faces "{name}"', positive=False) for v in box)
            for edge, by in (('left', left - fx), ('right', fx + fw - right), ('top', top - fy), ('bottom', fy + fh - bottom)):
                if by > 0.5:
                    move = {'left': 'left', 'right': 'right', 'top': 'up', 'bottom': 'down'}[edge]
                    findings.append({'crop': name, 'face': k, 'problem': f'cut-off {edge}', 'by': round(by),
                                     'what': f'the face crosses the {edge} margin by {round(by)} px: move the crop {move}'})
    return {'ok': not findings, 'findings': findings}


def run(command: str, data: Any, base: str) -> Json:
    if command == 'check-crops':
        return check_crops(data)
    inp = read_input(data, base)
    before = check(inp, inp['path'])
    if command == 'check':
        return {'ok': not before, 'findings': before}
    result, notes = fix(inp)
    after = check(inp, read_reframe('corrected', result))
    out: Json = {'before': before, 'after': after, 'notes': notes}
    if inp['out']:
        target = os.path.join(base, inp['out'])
        with open(target, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False)
        out['out'] = inp['out']
    else:
        out['reframe'] = result
    return out


def main(argv: List[str]) -> int:
    if len(argv) != 2 or argv[0] not in ('check', 'fix', 'check-crops'):
        return fail(USAGE, 2)
    try:
        with open(argv[1], encoding='utf-8-sig') as f:
            data = json.load(f)
        out = run(argv[0], data, os.path.dirname(os.path.abspath(argv[1])))
    except json.JSONDecodeError as err:
        return fail(f'the input is not JSON: {err}')
    except (OSError, UnicodeDecodeError) as err:
        return fail(f'cannot read or write: {err}')
    except InputError as err:
        return fail(str(err))
    except (KeyError, IndexError, TypeError, ZeroDivisionError, OverflowError, ValueError) as err:
        return fail(f'cannot read this input: {type(err).__name__} {err}')
    sys.stdout.buffer.write((json.dumps(out, separators=(',', ':'), ensure_ascii=False) + '\n').encode('utf-8'))
    return 0


def fail(reason: str, code: int = 1) -> int:
    sys.stderr.write('reframe_fix.py: ' + ' '.join(reason.split()) + '\n')
    return code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
