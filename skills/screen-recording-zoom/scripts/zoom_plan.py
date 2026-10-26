#!/usr/bin/env python3
"""
Plan where a screen recording zooms: which actions get a push, which share one, and when each
starts, holds and lets go. It decides; `zoom.py` keyframes what it decides.

    python3 scripts/zoom_plan.py input.json
    python3 scripts/zoom_plan.py < input.json

The input is one JSON object:

    {"source": {"w": 1920, "h": 1080}, "duration": 42, "view": {"w": 1920, "h": 1080},
     "intensity": "balanced",
     "events": [{"at": 3.2, "kind": "click", "box": {"x": 120, "y": 80, "w": 60, "h": 30},
                 "reveal": {"x": 120, "y": 110, "w": 420, "h": 300}, "luma": 70}]}

- `source` is the recording's size, and `duration` the layer's length, in seconds.
- `view` is the size, in frame px, of what shows the recording at rest: its panel, or the frame.
  It caps the push so the recording is never drawn larger than 1:1 (`maxScale`).
- `rest`, optional: the part of the source shown at rest, in source px; the whole source when left
  out. It is framed at rest as `zoom.py` frames its `content`: it fills the view's width, unless
  the recording would then leave the view's height uncovered.
- `intensity`: `subtle`, `balanced` (the default) or `punchy`; the table below.
- `events`, in layer seconds: each `at` a measured click (`kind: "click"`) or a measured change
  (`kind: "change"`, a reveal's settle), its `box` in source px, and optionally `reveal`, the
  bounding box of what it revealed, and `luma`, that box's mean luma.
- `options` overrides the intensity's numbers, by name.

The rules, each a number in `INTENSITY`:

- **Zoom to what was revealed**: the box is `reveal` when there is one, else `box`, padded by
  `pad` per side and never smaller than `minRegion` of the rest width.
- **No zoom on a wide change**: a box wider or taller than `wide` of the rest gets none.
- **No upscale**: the push stops where the recording would draw past `maxScale`, frame px per
  source px, and at `peak` over rest. A push that would gain less than `minGain` is none.
- **Merge**: actions closer than `merge` seconds share one held zoom. When their boxes fit in
  one window it holds still; otherwise it pans from one to the next at the peak, one pan at a
  time, as `zoom.py` keys them: a pan waits for the one before it to land.
- **Lead**: a push onto a click starts `lead` before it; onto a change, `delay` after it, as the
  house zoom does. It ramps in over `rampIn`.
- **Hold** `hold` seconds once the last action is in frame (after it, and after the push onto it
  lands), then zoom out over `rampOut`, slower than in.
- **Never back to rest for less than `minRest`**: two zooms that close merge into one.
- A zoom whose peak shows for less than `minPeak` is dropped.

It prints one JSON line, `{intensity, zooms, dropped, foci, options}`:

- `zooms`: each `{start, peak, until, end, factor, box, pans, events}`: when it starts, reaches
  its peak and starts to zoom out, and when it is back at rest (`null` when it holds to the end);
  `factor` over rest; `box` in source px; `pans`, each `{at, box}`; and the events it covers, by
  index.
- `dropped`: each event no zoom covers, with the `reason`: `no_box`, `too_wide`, `would_upscale`,
  `no_gain`, `too_late` or `too_short`.
- `foci` and `options`: the plan as `zoom.py`'s input, so the keyframes come from it unchanged:
  add the recording's `source`, `panel`, `content` and `duration`, and run `zoom.py`. Each focus's
  `at` is when its push starts (`options.delay` is 0).

Input it cannot plan exits 1, with one line on stderr that says what is wrong.

Python 3.9 or later, the standard library only, offline.
"""
from __future__ import annotations

import json
import sys
from typing import Any, Dict, List, Optional

from framing import InputError as FramingError
from zoom import moved, peak_framing, pose, rest_framing

Box = Dict[str, float]

# One knob, three settings. Times in seconds; `pad`, `minRegion` and `wide` are fractions;
# `peak` and `minGain` are over rest; `maxScale` is frame px per source px.
INTENSITY: Dict[str, Dict[str, float]] = {
    'subtle': {'peak': 1.2, 'merge': 4.0, 'lead': 0.8, 'delay': 0.1, 'rampIn': 1.0, 'rampOut': 1.5, 'hold': 1.8, 'minRest': 1.0,
               'minPeak': 0.7, 'pad': 0.12, 'minRegion': 0.5, 'wide': 0.6, 'minGain': 1.08, 'maxScale': 1.0, 'minRamp': 0.4},
    'balanced': {'peak': 1.33, 'merge': 2.5, 'lead': 0.5, 'delay': 0.1, 'rampIn': 1.0, 'rampOut': 1.5, 'hold': 1.8, 'minRest': 1.0,
                 'minPeak': 0.7, 'pad': 0.1, 'minRegion': 0.4, 'wide': 0.6, 'minGain': 1.08, 'maxScale': 1.0, 'minRamp': 0.4},
    'punchy': {'peak': 1.5, 'merge': 1.5, 'lead': 0.3, 'delay': 0.1, 'rampIn': 0.6, 'rampOut': 0.9, 'hold': 1.8, 'minRest': 1.0,
               'minPeak': 0.7, 'pad': 0.08, 'minRegion': 0.3, 'wide': 0.6, 'minGain': 1.08, 'maxScale': 1.0, 'minRamp': 0.4},
}

# zoom.py starts a ramp no sooner than this long after the one before it lands.
PAN_GAP = 0.05

USAGE = 'usage: zoom_plan.py [input.json]; with no file, the input is read from stdin'


class InputError(ValueError):
    """Input the script cannot plan from, with the reason."""


def r3(v: float) -> float:
    return float(f'{v:.3f}')


def union(boxes: List[Box]) -> Box:
    x0 = min(b['x'] for b in boxes)
    y0 = min(b['y'] for b in boxes)
    x1 = max(b['x'] + b['w'] for b in boxes)
    y1 = max(b['y'] + b['h'] for b in boxes)
    return {'x': x0, 'y': y0, 'w': x1 - x0, 'h': y1 - y0}


def window(box: Box, rest: Box, aspect: float, o: Dict[str, float], src: Dict[str, float]) -> Box:
    """The box padded, grown to the least region, shaped like the view, and kept inside the source."""
    w = max(box['w'] * (1 + 2 * o['pad']), rest['w'] * o['minRegion'])
    h = max(box['h'] * (1 + 2 * o['pad']), w / aspect)
    w = max(w, h * aspect)
    w, h = min(w, rest['w']), min(h, rest['h'])
    cx, cy = box['x'] + box['w'] / 2, box['y'] + box['h'] / 2
    x = min(max(cx - w / 2, 0), src['w'] - w)
    y = min(max(cy - h / 2, 0), src['h'] - h)
    return {'x': round(x, 1), 'y': round(y, 1), 'w': round(w, 1), 'h': round(h, 1)}


def is_wide(box: Box, rest: Box, o: Dict[str, float]) -> bool:
    return box['w'] > rest['w'] * o['wide'] or box['h'] > rest['h'] * o['wide']


def plan(src: Dict[str, float], duration: float, view: Dict[str, float], rest: Box, events: List[Dict[str, Any]], o: Dict[str, float]) -> Dict[str, Any]:
    aspect = view['w'] / view['h']
    # Rest as zoom.py frames it, the height's limit included: the push is capped over that.
    panel = {'x': 0.0, 'y': 0.0, 'w': view['w'], 'h': view['h']}
    rest_frame = rest_framing(src, panel, rest)
    rest_scale = rest_frame['S']
    cap = min(o['peak'], o['maxScale'] / rest_scale)
    dropped: List[Dict[str, Any]] = []
    live: List[Dict[str, Any]] = []
    for i, e in sorted(enumerate(events), key=lambda p: p[1]['at']):
        target = e.get('reveal') or e.get('box')
        if not target:
            dropped.append({'event': i, 'reason': 'no_box'})
        elif is_wide(target, rest, o):
            dropped.append({'event': i, 'reason': 'too_wide'})
        elif cap < o['minGain']:
            dropped.append({'event': i, 'reason': 'would_upscale'})
        else:
            b = window(target, rest, aspect, o, src)
            try:
                peak_framing(src, panel, rest_frame, b, e.get('luma', 128),
                             {'peak': r3(cap), 'whitePeak': r3(min(cap, 1.1)), 'crop': 0})
            except FramingError:
                dropped.append({'event': i, 'reason': 'no_gain'})
                continue
            start = e['at'] - o['lead'] if e.get('kind', 'change') == 'click' else e['at'] + o['delay']
            live.append({'i': i, 'at': e['at'], 'start': max(0.0, start), 'box': target, 'luma': e.get('luma', 128)})

    # Actions closer than `merge` share one zoom.
    groups: List[List[Dict[str, Any]]] = []
    for e in live:
        if groups and e['at'] - groups[-1][-1]['at'] <= o['merge']:
            groups[-1].append(e)
        else:
            groups.append([e])

    def framed(g: List[Dict[str, Any]]) -> List[Any]:
        """One window for the group when its boxes fit in one, else one per event, in event order."""
        whole = union([e['box'] for e in g])
        if len(g) > 1 and not is_wide(whole, rest, o):
            b = window(whole, rest, aspect, o, src)
            if min(view['w'] / b['w'], view['h'] / b['h']) / rest_scale >= o['minGain']:
                return [(g[0], b)]
        frames: List[Any] = []
        for e in g:
            b = window(e['box'], rest, aspect, o, src)
            # zoom.py keys no ramp for a pan that goes nowhere, so it takes no time.
            if not frames or frames[-1][1] != b:
                frames.append((e, b))
        return frames

    def timed(g: List[Dict[str, Any]]) -> Dict[str, Any]:
        # zoom.py runs one ramp at a time: a pan starts when it asked to or once the one before
        # it has landed, whichever is later. So the starts only ever increase.
        frames = framed(g)
        options = {'peak': r3(cap), 'whitePeak': r3(min(cap, 1.1)), 'crop': 0}
        try:
            shared = min(peak_framing(src, panel, rest_frame, b, e['luma'], options)['S'] for e, b in frames)
            options.update(peak=shared / rest_scale, whitePeak=shared / rest_scale)
            targets = [pose(src, view, panel, peak_framing(src, panel, rest_frame, b, e['luma'], options)) for e, b in frames]
        except FramingError:
            # A window that cannot cover the panel any closer than rest has nothing to gain: no_gain drops it.
            shared, targets = 0.0, None
        starts: List[float] = []
        held = pose(src, view, panel, rest_frame)
        landed = 0.0
        for k, (e, b) in enumerate(frames):
            start = max(landed + PAN_GAP, e['start'], starts[-1] if starts else 0)
            starts.append(start)
            if targets is None or moved(held, targets[k]):
                landed = start + o['rampIn']
                held = targets[k] if targets else held
        start = starts[0]
        peak = start + o['rampIn']
        last = g[-1]
        until = max(last['at'], landed) + o['hold']
        end: Optional[float] = until + o['rampOut']
        if end > duration:
            if duration - until >= o['minRamp']:
                end = duration
            else:
                until, end = duration, None
        return {'events': g, 'frames': frames, 'starts': starts, 'start': start, 'peak': peak, 'landed': landed, 'until': until, 'end': end, 'factor': shared / rest_scale}

    # Never back to rest for less than `minRest`: merge until no gap is that short.
    zooms = [timed(g) for g in groups]
    merged = True
    while merged:
        merged = False
        for k in range(len(zooms) - 1):
            a, b = zooms[k], zooms[k + 1]
            if a['end'] is None or b['start'] - a['end'] < o['minRest']:
                zooms[k:k + 2] = [timed(a['events'] + b['events'])]
                merged = True
                break

    out = []
    for z in zooms:
        g = z['events']
        # Keep only the prefix whose last pan can land and hold before the layer ends.
        while len(g) > 1 and z['until'] - z['landed'] < o['minPeak'] - 1e-9:
            reason = 'too_late' if z['landed'] > duration else 'too_short'
            dropped.append({'event': g[-1]['i'], 'reason': reason})
            g = g[:-1]
            z = timed(g)
        if z['peak'] > duration:
            dropped += [{'event': e['i'], 'reason': 'too_late'} for e in g]
            continue
        if z['until'] - z['peak'] < o['minPeak'] - 1e-9:
            dropped += [{'event': e['i'], 'reason': 'too_short'} for e in g]
            continue
        frames, starts = z['frames'], z['starts']
        factor = z['factor']
        if factor < o['minGain']:
            dropped += [{'event': e['i'], 'reason': 'no_gain'} for e in g]
            continue
        out.append({
            'start': r3(z['start']), 'peak': r3(z['peak']), 'until': r3(z['until']),
            'end': None if z['end'] is None else r3(z['end']), 'factor': r3(factor),
            'box': frames[0][1], 'pans': [{'at': r3(t), 'box': b} for t, (_, b) in zip(starts[1:], frames[1:])],
            'events': [e['i'] for e in g], '_frames': list(zip(starts, frames)),
        })

    foci = []
    for z in out:
        frames = z.pop('_frames')
        for k, (t, (e, b)) in enumerate(frames):
            focus: Dict[str, Any] = {'at': r3(t), 'box': b, 'luma': e['luma']}
            if k == len(frames) - 1 and z['end'] is not None:
                focus['until'] = z['until']
            foci.append(focus)
    options = {'peak': r3(cap), 'whitePeak': r3(min(cap, 1.1)), 'crop': 0, 'ramp': o['rampIn'], 'zoomOut': o['rampOut'], 'delay': 0, 'minRamp': o['minRamp']}
    return {'zooms': out, 'dropped': sorted(dropped, key=lambda d: d['event']), 'foci': foci, 'options': options}


def _num(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _box(v: Any, where: str) -> Box:
    if not isinstance(v, dict) or not all(_num(v.get(k)) for k in ('x', 'y', 'w', 'h')) or v['w'] <= 0 or v['h'] <= 0:
        raise InputError(f'{where} must be a box {{x, y, w, h}} in source px, with a positive size')
    return {k: float(v[k]) for k in ('x', 'y', 'w', 'h')}


def _size(v: Any, where: str) -> Dict[str, float]:
    if not isinstance(v, dict) or not _num(v.get('w')) or not _num(v.get('h')) or v['w'] <= 0 or v['h'] <= 0:
        raise InputError(f'{where} must be a size {{w, h}} with positive numbers')
    return {'w': float(v['w']), 'h': float(v['h'])}


def run(data: Any) -> Dict[str, Any]:
    """The script's whole job: the checked input in, the line it prints out."""
    if not isinstance(data, dict):
        raise InputError('the input must be one JSON object')
    src = _size(data.get('source'), 'source')
    view = _size(data.get('view'), 'view')
    duration = data.get('duration')
    if not _num(duration) or duration <= 0:
        raise InputError('duration must be a positive number of seconds')
    rest = _box(data['rest'], 'rest') if data.get('rest') is not None else {'x': 0.0, 'y': 0.0, 'w': src['w'], 'h': src['h']}
    intensity = data.get('intensity', 'balanced')
    if intensity not in INTENSITY:
        raise InputError('intensity must be one of: ' + ', '.join(INTENSITY))
    options = data.get('options') or {}
    if not isinstance(options, dict) or not all(k in INTENSITY['balanced'] and _num(v) for k, v in options.items()):
        raise InputError('options must be an object of numbers named as in INTENSITY: ' + ', '.join(INTENSITY['balanced']))
    events = data.get('events')
    if not isinstance(events, list):
        raise InputError('events must be a list')
    checked = []
    for i, e in enumerate(events):
        where = f'events[{i}]'
        if not isinstance(e, dict) or not _num(e.get('at')) or e['at'] < 0:
            raise InputError(f'{where}: at must be a number of seconds, 0 or more')
        if e.get('kind', 'change') not in ('click', 'change'):
            raise InputError(f'{where}: kind must be "click" or "change"')
        c: Dict[str, Any] = {'at': float(e['at']), 'kind': e.get('kind', 'change')}
        for key in ('box', 'reveal'):
            if e.get(key) is not None:
                c[key] = _box(e[key], f'{where}: {key}')
        if e.get('luma') is not None:
            if not _num(e['luma']):
                raise InputError(f'{where}: luma must be a number, 0-255')
            c['luma'] = e['luma']
        checked.append(c)
    o = {**INTENSITY[intensity], **{k: float(v) for k, v in options.items()}}
    return {'intensity': intensity, **plan(src, float(duration), view, rest, checked, o)}


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
    sys.stderr.write('zoom_plan.py: ' + ' '.join(reason.split()) + '\n')
    return code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
