#!/usr/bin/env python3
"""
Keyframe the house zoom on a recording in a panel: rest, then a push onto each result.

    python3 scripts/zoom.py input.json
    python3 scripts/zoom.py < input.json

The input is one JSON object:

    {"source": {"w": 2556, "h": 1410}, "panel": {"x": 40, "y": 600, "w": 1000, "h": 1280},
     "content": {"x": 895, "y": 64, "w": 767, "h": 1342}, "duration": 6,
     "foci": [{"at": 3, "box": {"x": 959, "y": 703, "w": 703, "h": 575}, "luma": 60}]}

- `source` is the recording's size, `panel` its panel in frame px, and `content` the content
  column in source px: at rest it fills the panel.
- `duration` is the layer's length in seconds, and each focus is a moment to lean in on: `at`, the
  measured reveal in layer seconds; `box`, the result in source px; `luma`, its mean luma (0-255),
  and `card`, the box of the card the result sits in, when there is one. With `zoomOut` on, a
  focus may also carry `until`: the layer second its hold ends and the zoom back out starts.
- `frame` is the composition's size, 1080x1920 by default. `options` overrides `DEFAULT_ZOOM`
  below, and `sourceTextPx`, the UI's text height in source px.

It prints one JSON line, `{scale, position, textPx, skipped?}`: the layer's `scale` and `position`
keyframes, layer-relative (`timeMode: "layer"`), with the easing on the keyframe that starts each
ramp and none on the terminal one. `textPx` is how tall the UI's text reads at rest, in frame px.
`skipped` says which push had too little of the step left to ramp, and how much it had. Input it
cannot keyframe exits 1, with one line on stderr that says what is wrong.

The house zoom: rest fills the panel with the content column; the peak is at most 1.33x over rest
(1.1x on a mostly white result); a 1.0 s ramp on cubic-bezier(0.16, 1, 0.3, 1) starts 0.1 s after
the reveal; a second focus pans at the peak, and the step never zooms back out. The framing is the
screen-recording-layouts skill's formula, in `framing.py`.

Two options leave the house zoom for footage that stays on one screen for a long time, and are off
by default. `zoomOut`, seconds: after a focus with `until`, the frame ramps back to rest over that
long on the same curve, so the viewer has the context back before the next push. `textFloor`,
frame px: the peak is raised until the UI's text reads at least that tall, past 1.33x if it must,
and still never crops the focus box past `crop`.

Python 3.9 or later, the standard library only, offline.
"""
from __future__ import annotations

import json
import math
import sys
from typing import Any, Dict, List, Optional

from framing import FRAME, Box, InputError, Size, Vec2, _box, _number, _size, center, fit_scale, min_scale, pose, round

HOUSE_EASING = {'kind': 'cubic_bezier', 'control': [0.16, 1, 0.3, 1]}

# Two focus events within this many seconds share one push, panning between them at the peak (the
# Merge row of the house zoom). zoom.py keys the pushes it is given; the screen-recording-analysis skill's
# actions.py imports this to group events into those pushes.
MERGE_WINDOW_S = 2.5

Framing = Dict[str, Any]  # {S: total scale, source px to frame px; F: source point on the panel centre}
Keyframe = Dict[str, Any]
ZoomTrack = Dict[str, Any]

USAGE = 'usage: zoom.py [input.json]; with no file, the input is read from stdin'


def clamp_focus(src: Size, panel: Box, S: float, F: Vec2) -> Vec2:
    """Keep the visible window inside the recording: move F rather than show the panel's empty edge."""
    half_w = panel['w'] / 2 / S
    half_h = panel['h'] / 2 / S

    def clamp(v: float, half: float, most: float) -> float:
        return most / 2 if half * 2 >= most else min(most - half, max(half, v))

    return [round(clamp(F[0], half_w, src['w']), 1), round(clamp(F[1], half_h, src['h']), 1)]


def rest_framing(src: Size, panel: Box, content: Box) -> Framing:
    """Rest framing: the content column fills the panel width, centered on the column."""
    S = max(min_scale(src, panel), min(panel['w'] / content['w'], panel['h'] / content['h'] * 1.6))
    return {'S': round(S, 4), 'F': clamp_focus(src, panel, S, center(content))}


# peak: over rest. whitePeak: for a mostly white result (a logo on a white card), above whiteLuma
# mean luma. crop: how much of the focus box the peak may crop per side, as a fraction of its size:
# a result that already fills the panel still gets a push, and never loses more than this. ramp:
# the push's length. minRamp: the shortest ramp; a push with less of the step left is skipped, and
# reported. delay: from the reveal to the start of the push.
# zoomOut: the ramp back to rest after a focus with `until`, 0 for none. textFloor: the frame px the
# UI's text must reach at the peak, 0 for none. Both are off in the house zoom.
DEFAULT_ZOOM = {'peak': 1.33, 'whitePeak': 1.1, 'whiteLuma': 200, 'crop': 0.12, 'ramp': 1.0, 'minRamp': 0.4, 'delay': 0.1, 'zoomOut': 0, 'textFloor': 0}


def peak_framing(src: Size, panel: Box, rest: Framing, focus: Box, luma: float, options: Optional[Dict[str, Any]] = None, card: Optional[Box] = None, least: float = 0) -> Framing:
    """
    Peak framing on one focus box: at most `peak` over rest, cropping at most `crop` of the box per side.

    `card`, the result the focus sits in (a photo in a chat card): when the peak window is narrower
    than the card, the card's header line runs past both edges, and a centred window cuts it mid-word.
    So the window's top is set just above the focus instead, and the header leaves the frame whole.

    `least`: the least peak over rest, from the text floor; 0 leaves the house peak alone.
    """
    o = {**DEFAULT_ZOOM, **(options or {})}
    over = max(least, o['whitePeak'] if luma >= o['whiteLuma'] else o['peak'])
    crop = o['crop']
    kept = {'x': focus['x'] + focus['w'] * crop, 'y': focus['y'] + focus['h'] * crop, 'w': focus['w'] * (1 - 2 * crop), 'h': focus['h'] * (1 - 2 * crop)}
    cap = fit_scale(kept, panel)
    S = min(rest['S'] * over, cap)
    if cap < min_scale(src, panel) - 1e-9:
        raise InputError('focus cannot fit within crop and cover the panel')
    S = max(min_scale(src, panel), rest['S'] if S <= rest['S'] else min(round(S, 4), math.floor(cap * 10000) / 10000))
    half_h = panel['h'] / 2 / S
    cx, cy = center(focus)
    top_anchored = card is not None and panel['w'] / S < card['w'] and half_h * 2 > focus['h']
    fy = focus['y'] - min(focus['h'] * crop, half_h * 2 - focus['h']) / 2 + half_h if top_anchored else cy
    return {'S': S, 'F': clamp_focus(src, panel, S, [cx, fy])}


def moved(a: Dict[str, Vec2], b: Dict[str, Vec2]) -> bool:
    """Whether two poses differ enough to key a ramp between them."""
    return abs(a['scale'][0] - b['scale'][0]) > 1e-3 or math.hypot(a['position'][0] - b['position'][0], a['position'][1] - b['position'][1]) > 1


def zoom_track(src: Size, comp: Size, panel: Box, content: Box, foci: List[Dict[str, Any]], duration: float, options: Optional[Dict[str, Any]] = None) -> ZoomTrack:
    """
    The step's keyframes, layer-relative. `foci` are the moments to lean in on, in step output
    time (`at`, `box`, `luma`, and `card` when there is one); the first pushes from rest, later ones
    pan at peak, and the step never zooms back out. A push near the step's end ramps faster to end
    with it; with less room than `minRamp` it is skipped, and `skipped` says so.

    With `zoomOut`, a focus that carries `until` ramps back to rest from then, over `zoomOut`
    seconds or what is left of the layer, and the next focus pushes from rest again. A zoom-out with
    less room than `minRamp` is left out: the frame holds the peak, and the next focus pans.

    `textPx` is readability at rest: frame px per source px times the UI's text height.
    """
    options = options or {}
    o = {**DEFAULT_ZOOM, **options}
    rest = rest_framing(src, panel, content)
    rest_pose = pose(src, comp, panel, rest)
    source_text = options['sourceTextPx'] if options.get('sourceTextPx') is not None else (24 if src['w'] >= 2400 else 13)
    least = o['textFloor'] / (rest['S'] * source_text) if o['textFloor'] > 0 else 0
    scale: List[Keyframe] = [{'time': 0, 'value': rest_pose['scale'], 'easing': 'linear'}]
    position: List[Keyframe] = [{'time': 0, 'value': rest_pose['position'], 'easing': 'linear'}]
    t = 0
    skipped = None
    ordered = sorted(foci, key=lambda x: x['at'])
    peaks = [peak_framing(src, panel, rest, f['box'], f['luma'], o, f.get('card'), least)['S'] for f in ordered]
    shared = None
    for i, f in enumerate(ordered):
        start = max(t + 0.05, f['at'] + o['delay'])
        room = duration - start
        if room < o['minRamp'] - 1e-9:
            skipped = {'at': round(f['at'], 3), 'room': round(max(0, room), 3)}
            break
        end = start + min(o['ramp'], room)
        if shared is None:
            # Every focus held in this push uses the smallest of its permitted peaks.
            # Try lower permitted peaks before excluding foci using serialized pan times.
            # A candidate belongs to this push only if its limiting focus is reachable at it.
            for shared in sorted(set(peaks[i:])):
                group = []
                next_t = t
                next_pose = {'scale': scale[-1]['value'], 'position': position[-1]['value']}
                for j in range(i, len(ordered)):
                    future = ordered[j]
                    next_start = max(next_t + 0.05, future['at'] + o['delay'])
                    if duration - next_start < o['minRamp'] - 1e-9:
                        break
                    group.append(peaks[j])
                    future_framing = peak_framing(src, panel, rest, future['box'], future['luma'], {**o, 'peak': shared / rest['S'], 'whitePeak': shared / rest['S']}, future.get('card'))
                    future_pose = pose(src, comp, panel, future_framing)
                    if moved(next_pose, future_pose):
                        next_t = next_start + min(o['ramp'], duration - next_start)
                        next_pose = future_pose
                    if o['zoomOut'] > 0 and future.get('until') is not None:
                        if duration - max(next_t, future['until']) >= o['minRamp'] - 1e-9:
                            break
                if min(group) == shared:
                    break
        framing = peak_framing(src, panel, rest, f['box'], f['luma'], {**o, 'peak': shared / rest['S'], 'whitePeak': shared / rest['S']}, f.get('card'))
        target = pose(src, comp, panel, framing)
        held = {'scale': scale[-1]['value'], 'position': position[-1]['value']}
        # A push that goes nowhere is no push: skip it rather than key a still. Its `until` still
        # zooms back out from the pose held.
        if moved(held, target):
            scale += [{'time': round(start, 3), 'value': held['scale'], 'easing': HOUSE_EASING}, {'time': round(end, 3), 'value': target['scale'], 'easing': 'linear'}]
            position += [{'time': round(start, 3), 'value': held['position'], 'easing': HOUSE_EASING}, {'time': round(end, 3), 'value': target['position'], 'easing': 'linear'}]
            t = end
        else:
            target = held
        if o['zoomOut'] > 0 and f.get('until') is not None:
            out_start = max(t, f['until'])
            out_room = duration - out_start
            if out_room >= o['minRamp'] - 1e-9:
                out_end = out_start + min(o['zoomOut'], out_room)
                if moved(target, rest_pose):
                    scale += [{'time': round(out_start, 3), 'value': target['scale'], 'easing': HOUSE_EASING}, {'time': round(out_end, 3), 'value': rest_pose['scale'], 'easing': 'linear'}]
                    position += [{'time': round(out_start, 3), 'value': target['position'], 'easing': HOUSE_EASING}, {'time': round(out_end, 3), 'value': rest_pose['position'], 'easing': 'linear'}]
                    t = out_end
                shared = None
    # The terminal keyframe carries no easing.
    del scale[-1]['easing']
    del position[-1]['easing']
    track: ZoomTrack = {'scale': scale, 'position': position, 'textPx': round(rest['S'] * source_text, 1)}
    if skipped:
        track['skipped'] = skipped
    return track


def _focus(v: Any, i: int) -> Dict[str, Any]:
    where = f'foci[{i}]'
    if not isinstance(v, dict) or not _number(v.get('at')) or v['at'] < 0:
        raise InputError(f'{where}: at must be a number of seconds, 0 or more')
    if not _number(v.get('luma')):
        raise InputError(f'{where}: luma must be a number, the result\'s mean luma')
    out = {'at': v['at'], 'box': _box(v.get('box'), f'{where}: box'), 'luma': v['luma']}
    if v.get('card') is not None:
        out['card'] = _box(v['card'], f'{where}: card')
    if v.get('until') is not None:
        if not _number(v['until']) or v['until'] < v['at']:
            raise InputError(f'{where}: until must be a number of seconds, at or after at')
        out['until'] = v['until']
    return out


def track(data: Any) -> ZoomTrack:
    """The script's whole job: the checked input in, the line it prints out."""
    if not isinstance(data, dict):
        raise InputError('the input must be one JSON object')
    src = _size(data.get('source'), 'source')
    panel = _box(data.get('panel'), 'panel')
    content = _box(data.get('content'), 'content')
    comp = _size(data['frame'], 'frame') if data.get('frame') is not None else FRAME
    duration = data.get('duration')
    if not _number(duration) or duration <= 0:
        raise InputError('duration must be a positive number of seconds')
    foci = data.get('foci', [])
    if not isinstance(foci, list):
        raise InputError('foci must be a list')
    options = data.get('options')
    if options is not None and (not isinstance(options, dict) or not all(_number(v) for v in options.values())):
        raise InputError('options must be an object of numbers')
    return zoom_track(src, comp, panel, content, [_focus(f, i) for i, f in enumerate(foci)], duration, options)


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
        out = track(json.loads(text))
    except json.JSONDecodeError as err:
        return fail(f'the input is not JSON: {err}')
    except InputError as err:
        return fail(str(err))
    except (KeyError, IndexError, TypeError, ZeroDivisionError, OverflowError) as err:
        return fail(f'cannot keyframe from this input: {type(err).__name__} {err}')
    sys.stdout.buffer.write((json.dumps(out, separators=(',', ':')) + '\n').encode('utf-8'))
    return 0


def fail(reason: str, code: int = 1) -> int:
    sys.stderr.write('zoom.py: ' + ' '.join(reason.split()) + '\n')
    return code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
