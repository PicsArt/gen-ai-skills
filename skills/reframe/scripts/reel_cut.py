#!/usr/bin/env python3
"""
Cut a reel: clips of the user's own footage, back to back, each framed on its own.

    python3 scripts/reel_cut.py input.json
    python3 scripts/reel_cut.py < input.json

The input is one JSON object:

    {
      "width": 1080, "height": 1920, "fps": 30,
      "sources": [
        {"id": "talk", "url": "https://...", "reframe": { the picsart_media_reframe_video result }},
        {"id": "broll", "url": "https://...", "width": 1920, "height": 1080, "duration": 31.5},
        {"id": "photo", "type": "image", "url": "https://...", "width": 1600, "height": 1200}
      ],
      "clips": [
        {"source": "talk", "in": 12.0, "out": 18.5},
        {"source": "talk", "in": 40.2, "out": 44.0, "hold": 0.42},
        {"source": "broll", "in": 3.0, "out": 6.0, "frame": "full", "dim": 0.3},
        {"source": "photo", "duration": 2.0}
      ],
      "transition": {"id": "crossfade", "duration": 0.3}
    }

- `width`, `height` and `fps` default to 1080, 1920 and 30.
- A source with `reframe` carries its whole `picsart_media_reframe_video` result (or that
  result's `scene`), or the path of a file that holds it, relative to the input file (or to the
  working directory, for stdin): its size, length and the subject's camera path come from there.
  A video without one gives `width`, `height` and `duration` itself, from
  `picsart_media_probe_media`. A photo is `"type": "image"`, with `width` and `height` only.
- A clip is `in` to `out`, in the source's own seconds. A photo's clip gives its `duration`
  instead: `full` (its default) shows the whole photo, `crop` fills the frame from its centre.
  - `frame` is `crop` (the camera follows the subject; the default for a reframed source) or
    `full` (the whole frame; the default otherwise).
  - `crop` with `hold`, a centre across the source from 0 to 1, holds a still window there
    instead of following the subject.
  - `full` takes `background`: `blur` (the default, a blurred copy fills the margins; `dim`
    darkens it) or `black`.
- `transition` is optional and plays on every seam. Without it, every seam is a hard cut.

It prints one JSON line, `{scene, duration, clips, notes}`. `notes` says, per clip, where the
camera path swings across more of the source than one person would, with the centre to `hold`
instead. Input it cannot cut from exits 1, with one line on stderr that says what is wrong.

Python 3.9 or later, the standard library only, offline. It reads no media: the reframe result
already holds the camera path, measured once per source, so any number of cuts of one source
cost no further reframing.
"""
from __future__ import annotations

import json
import math
import os
import sys
from typing import Any, Dict, List, Optional, Tuple

USAGE = 'usage: reel_cut.py [input.json]; with no file, the input is read from stdin'

DEFAULT_WIDTH = 1080
DEFAULT_HEIGHT = 1920
DEFAULT_FPS = 30
BACKGROUND = '#000000ff'
# A camera centre that moves across more than this share of the source is following more than
# one person: the reel would swing between them.
SWING_SPREAD = 0.25

Json = Dict[str, Any]
Vec = Tuple[float, float]


class InputError(ValueError):
    """Input the reel cannot be cut from; the message says what to change."""


# --- Keyframe tracks ------------------------------------------------------------------------
#
# A track is the reframe's `[{time, value: [x, y], easing?}]`. `easing` is the segment's, from
# that keyframe to the next: `step` holds the value and jumps at the next keyframe, which is how
# the reframe marks a cut where it found the subject again. Anything else is linear.


def evaluate(track: List[Json], t: float) -> Vec:
    """The track's value at `t`, as the reframe tool's own `evaluateTrack` reads it."""
    if t <= track[0]['time']:
        return tuple(track[0]['value'])
    if t >= track[-1]['time']:
        return tuple(track[-1]['value'])
    for a, b in zip(track, track[1:]):
        if a['time'] <= t < b['time']:
            if a.get('easing') == 'step':
                return tuple(a['value'])
            f = (t - a['time']) / (b['time'] - a['time'])
            return (a['value'][0] + f * (b['value'][0] - a['value'][0]),
                    a['value'][1] + f * (b['value'][1] - a['value'][1]))
    return tuple(track[-1]['value'])


def easing_at(track: List[Json], t: float) -> Optional[str]:
    """The easing of the segment `t` falls in, so a keyframe inserted there keeps its motion."""
    for a, b in zip(track, track[1:]):
        if a['time'] <= t < b['time']:
            return a.get('easing')
    return None


def window(track: List[Json], t_in: float, t_out: float) -> List[Json]:
    """The track from `t_in` to `t_out`, its times from 0 at `t_in`, with a keyframe on each end."""
    inside = [k for k in track if t_in < k['time'] < t_out]
    first = {'time': t_in, 'value': list(evaluate(track, t_in))}
    ease = easing_at(track, t_in)
    if ease is not None:
        first['easing'] = ease
    last = {'time': t_out, 'value': list(evaluate(track, t_out))}
    out = []
    for k in [first] + inside + [last]:
        item = {'time': k['time'] - t_in, 'value': list(k['value'])}
        if k is not last and k.get('easing') is not None:
            item['easing'] = k['easing']
        out.append(item)
    return out


def constant(track: List[Json]) -> bool:
    return all(k['value'] == track[0]['value'] for k in track)


# --- The reframe result ---------------------------------------------------------------------


def number(value: Any, what: str, positive: bool = True) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise InputError(f'{what} must be a number')
    if positive and value <= 0:
        raise InputError(f'{what} must be more than 0')
    return float(value)


def read_reframe(source_id: str, reframe: Json) -> Json:
    """The camera path out of a reframe result: frame size, source size and length, both axes."""
    where = f'sources "{source_id}" reframe'
    scene = reframe.get('scene', reframe) if isinstance(reframe, dict) else None
    if not isinstance(scene, dict):
        raise InputError(f'{where} must be the picsart_media_reframe_video result, or its scene')
    comp = scene.get('composition') or {}
    layers = scene.get('layers') or []
    if not layers or not isinstance(layers[0], dict):
        raise InputError(f'{where}: its scene has no layer; pass the result as the tool returned it')
    layer = layers[0]
    assets = scene.get('assets') or []
    asset = assets[0] if isinstance(assets, list) and assets else {}
    src_w = reframe.get('srcW', asset.get('width'))
    src_h = reframe.get('srcH', asset.get('height'))
    duration = reframe.get('duration', asset.get('duration', comp.get('duration')))
    transform = layer.get('transform') or {}
    animations = layer.get('animations') or {}
    axes = {}
    for axis in ('position', 'scale'):
        keyframes = (animations.get(axis) or {}).get('keyframes')
        if keyframes:
            axes[axis] = sorted(keyframes, key=lambda k: k['time'])
        elif axis in transform:
            axes[axis] = [{'time': 0, 'value': list(transform[axis])}]
        else:
            raise InputError(f'{where}: its layer has no {axis}; pass the result as the tool returned it')
    return {
        'frame': (number(comp.get('width'), f'{where} composition width'),
                  number(comp.get('height'), f'{where} composition height')),
        'size': (number(src_w, f'{where} srcW'), number(src_h, f'{where} srcH')),
        'duration': number(duration, f'{where} duration'),
        'uri': asset.get('uri'),
        'position': axes['position'],
        'scale': axes['scale'],
    }


def read_json_file(path: str, what: str) -> Any:
    try:
        with open(path, encoding='utf-8-sig') as f:
            return json.load(f)
    except (OSError, UnicodeDecodeError) as err:
        raise InputError(f'{what}: cannot read {path}: {err}')
    except json.JSONDecodeError as err:
        raise InputError(f'{what}: {path} is not JSON: {err}')


def read_sources(raw: Any, base: str) -> Dict[str, Json]:
    if not isinstance(raw, list) or not raw:
        raise InputError('sources must be a list with at least one source')
    sources: Dict[str, Json] = {}
    for i, s in enumerate(raw):
        if not isinstance(s, dict) or not isinstance(s.get('id'), str) or not s['id']:
            raise InputError(f'sources[{i}] needs an id')
        sid = s['id']
        if sid in sources:
            raise InputError(f'sources[{i}]: the id "{sid}" is used twice')
        url = s.get('url')
        kind = s.get('type', 'video')
        if kind not in ('video', 'image'):
            raise InputError(f'sources "{sid}" type is "video" or "image"')
        source: Json = {'id': sid, 'type': kind}
        if kind == 'image':
            if s.get('reframe') is not None:
                raise InputError(f'sources "{sid}" is an image, which has no reframe')
            source.update(
                path=None,
                size=(number(s.get('width'), f'sources "{sid}" width'), number(s.get('height'), f'sources "{sid}" height')),
                duration=None,
            )
        elif s.get('reframe') is not None:
            reframe = s['reframe']
            if isinstance(reframe, str):
                reframe = read_json_file(os.path.join(base, reframe), f'sources "{sid}" reframe')
            path = read_reframe(sid, reframe)
            source.update(path=path, size=path['size'], duration=path['duration'])
            url = url or path['uri']
        else:
            source.update(
                path=None,
                size=(number(s.get('width'), f'sources "{sid}" width'), number(s.get('height'), f'sources "{sid}" height')),
                duration=number(s.get('duration'), f'sources "{sid}" duration'),
            )
        if not isinstance(url, str) or not url.lower().startswith(('https://', 'http://')):
            raise InputError(f'sources "{sid}" needs its url, as an http(s) URL')
        source['url'] = url
        sources[sid] = source
    return sources


# --- Framing --------------------------------------------------------------------------------


def to_reel(path: Json, width: float, height: float) -> Tuple[float, Vec, Vec]:
    """How the reframe's frame maps into the reel's: one zoom, the two centres."""
    fw, fh = path['frame']
    k = max(width / fw, height / fh)
    return k, (fw / 2, fh / 2), (width / 2, height / 2)


def map_position(value: List[float], k: float, old: Vec, new: Vec) -> List[float]:
    return [round((value[0] - old[0]) * k + new[0], 3), round((value[1] - old[1]) * k + new[1], 3)]


def map_scale(value: List[float], k: float) -> List[float]:
    return [round(value[0] * k, 5), round(value[1] * k, 5)]


def camera_centre(position: List[float], scale: List[float], size: Vec, width: float, height: float) -> Vec:
    """Where in the source, 0 to 1 on each axis, the reel's centre falls."""
    sw, sh = size
    return ((sw / 2 + (width / 2 - position[0]) / scale[0]) / sw,
            (sh / 2 + (height / 2 - position[1]) / scale[1]) / sh)


def held_window(path: Json, clip: Json, hold: float, width: float, height: float) -> Tuple[List[float], List[float]]:
    """A still window centred at `hold` across the source, as large as the clip's own path is."""
    k, old, new = to_reel(path, width, height)
    sw, sh = path['size']
    track = window(path['scale'], clip['in'], clip['out'])
    zooms = sorted(map_scale(f['value'], k)[0] for f in track)
    s = zooms[len(zooms) // 2]
    positions = window(path['position'], clip['in'], clip['out'])
    ys = sorted(camera_centre(map_position(p['value'], k, old, new), [s, s], path['size'], width, height)[1] for p in positions)
    centre_y = ys[len(ys) // 2]
    x = width / 2 - (hold * sw - sw / 2) * s
    y = height / 2 - (centre_y * sh - sh / 2) * s
    # Keep the source covering the whole reel: no edge of it may come inside the frame.
    half_w, half_h = sw * s / 2, sh * s / 2
    x = min(max(x, width - half_w), half_w) if half_w * 2 >= width else width / 2
    y = min(max(y, height - half_h), half_h) if half_h * 2 >= height else height / 2
    return [round(x, 3), round(y, 3)], [round(s, 5), round(s, 5)]


def crop_clip(source: Json, clip: Json, width: float, height: float, notes: List[str], i: int) -> Json:
    path = source['path']
    if path is None:
        raise InputError(f'clips[{i}] is "crop", but source "{source["id"]}" has no reframe; '
                         'reframe it, or frame the clip "full"')
    sw, sh = path['size']
    out: Json = {
        'duration': clip['duration'],
        'content': {'kind': 'media', 'assetId': source['id'], 'fit': 'none',
                    'trim': {'in': clip['in'], 'out': clip['out']}},
        'transform': {'anchor': [sw / 2, sh / 2]},
    }
    if clip.get('hold') is not None:
        hold = number(clip['hold'], f'clips[{i}] hold', positive=False)
        if not 0 <= hold <= 1:
            raise InputError(f'clips[{i}] hold is a centre across the source, from 0 to 1')
        position, scale = held_window(path, clip, hold, width, height)
        out['transform'].update(position=position, scale=scale)
        return out

    k, old, new = to_reel(path, width, height)
    tracks = {}
    for axis, fn in (('position', lambda v: map_position(v, k, old, new)), ('scale', lambda v: map_scale(v, k))):
        track = window(path[axis], clip['in'], clip['out'])
        tracks[axis] = [dict(f, time=round(f['time'], 4), value=fn(f['value'])) for f in track]
    animations = {}
    for axis, track in tracks.items():
        if constant(track):
            out['transform'][axis] = track[0]['value']
        else:
            animations[axis] = {'keyframes': track}
    if animations:
        out['animations'] = animations

    centres = [camera_centre(evaluate(tracks['position'], f['time']), evaluate(tracks['scale'], f['time']),
                             path['size'], width, height)[0] for f in tracks['position']]
    spread = max(centres) - min(centres)
    if spread > SWING_SPREAD:
        middle = sorted(centres)[len(centres) // 2]
        notes.append(f'clips[{i}]: the camera crosses {round(spread * 100)}% of the source, so it may be '
                     f'following two people; to hold one, cut it again with "hold": {round(middle, 3)}')
    return out


def still_clip(source: Json, clip: Json) -> Json:
    """A photo filling the frame, cropped around its centre."""
    return {'duration': clip['duration'], 'content': {'kind': 'media', 'assetId': source['id'], 'fit': 'cover'}}


def full_clip(source: Json, clip: Json, i: int) -> Json:
    background = clip.get('background', 'blur')
    content: Json = {'kind': 'media', 'assetId': source['id']}
    if source['type'] == 'video':
        content['trim'] = {'in': clip['in'], 'out': clip['out']}
    out: Json = {'duration': clip['duration'], 'content': content}
    if background == 'black':
        content['fit'] = 'contain'
    elif background == 'blur':
        look: Json = {'look': 'blur_fill'}
        if clip.get('dim') is not None:
            dim = number(clip['dim'], f'clips[{i}] dim', positive=False)
            if not 0 <= dim <= 1:
                raise InputError(f'clips[{i}] dim must be from 0 to 1')
            look['params'] = {'dim': dim}
        out['looks'] = [look]
    else:
        raise InputError(f'clips[{i}] background is "blur" or "black"')
    return out


# --- The reel -------------------------------------------------------------------------------


def read_clip(raw: Any, i: int, sources: Dict[str, Json]) -> Tuple[Json, Json]:
    if not isinstance(raw, dict):
        raise InputError(f'clips[{i}] must be an object')
    source = sources.get(raw.get('source'))
    if source is None:
        raise InputError(f'clips[{i}] names source "{raw.get("source")}", which is not in sources')
    if source['type'] == 'image':
        if raw.get('in') is not None or raw.get('out') is not None:
            raise InputError(f'clips[{i}] shows the image "{source["id"]}", which has no in or out; give it a duration')
        return source, dict(raw, duration=round(number(raw.get('duration'), f'clips[{i}] duration'), 3))
    t_in = number(raw.get('in'), f'clips[{i}] in', positive=False)
    t_out = number(raw.get('out'), f'clips[{i}] out')
    if t_in < 0 or t_out <= t_in:
        raise InputError(f'clips[{i}] needs 0 <= in < out')
    if t_out > source['duration'] + 0.05:
        raise InputError(f'clips[{i}] ends at {t_out}s, after source "{source["id"]}" ends ({source["duration"]}s)')
    if t_in >= source['duration']:
        raise InputError(f'clips[{i}] starts at {t_in}s, after source "{source["id"]}" ends ({source["duration"]}s)')
    t_out = min(t_out, source['duration'])
    return source, dict(raw, **{'in': t_in, 'out': t_out, 'duration': round(t_out - t_in, 3)})


def cut(data: Any, base: str = '.') -> Json:
    """The reel. A `reframe` given as a file path is read relative to `base`."""
    if not isinstance(data, dict):
        raise InputError('the input must be a JSON object')
    width = number(data.get('width', DEFAULT_WIDTH), 'width')
    height = number(data.get('height', DEFAULT_HEIGHT), 'height')
    fps = number(data.get('fps', DEFAULT_FPS), 'fps')
    sources = read_sources(data.get('sources'), base)
    raw_clips = data.get('clips')
    if not isinstance(raw_clips, list) or not raw_clips:
        raise InputError('clips must be a list with at least one clip')

    notes: List[str] = []
    clips = []
    used: List[str] = []
    for i, raw in enumerate(raw_clips):
        source, clip = read_clip(raw, i, sources)
        frame = clip.get('frame', 'crop' if source['path'] else 'full')
        if frame == 'crop' and source['type'] == 'image':
            clips.append(still_clip(source, clip))
        elif frame == 'crop':
            clips.append(crop_clip(source, clip, width, height, notes, i))
        elif frame == 'full':
            clips.append(full_clip(source, clip, i))
        else:
            raise InputError(f'clips[{i}] frame is "crop" or "full"')
        if source['id'] not in used:
            used.append(source['id'])

    track: Json = {'kind': 'track', 'clips': clips}
    transition = data.get('transition')
    if transition is not None:
        if not isinstance(transition, dict) or not isinstance(transition.get('id'), str) or not transition['id']:
            raise InputError('transition needs an id, from picsart_media_get_capabilities')
        length = number(transition.get('duration'), 'transition duration')
        if len(clips) > 1:
            track['transitions'] = [{'between': g, 'id': transition['id'], 'duration': length}
                                    for g in range(len(clips) - 1)]

    duration = round(sum(c['duration'] for c in clips), 3)
    assets = []
    for sid in used:
        s = sources[sid]
        asset = {'id': sid, 'type': s['type'], 'uri': s['url'], 'width': s['size'][0], 'height': s['size'][1]}
        if s['duration'] is not None:
            asset['duration'] = s['duration']
        assets.append(asset)
    scene = {
        'version': '1.0',
        'composition': {'width': int(width), 'height': int(height), 'fps': fps, 'duration': duration,
                        'background': BACKGROUND},
        'assets': assets,
        'layers': [{'id': 'reel', 'content': track}],
    }
    return {'scene': scene, 'duration': duration, 'clips': len(clips), 'notes': notes}


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
        out = cut(json.loads(text), os.path.dirname(os.path.abspath(argv[0])) if argv else os.getcwd())
    except json.JSONDecodeError as err:
        return fail(f'the input is not JSON: {err}')
    except InputError as err:
        return fail(str(err))
    except (KeyError, IndexError, TypeError, ZeroDivisionError, OverflowError) as err:
        return fail(f'cannot cut from this input: {type(err).__name__} {err}')
    sys.stdout.buffer.write((json.dumps(out, separators=(',', ':'), ensure_ascii=False) + '\n').encode('utf-8'))
    return 0


def fail(reason: str, code: int = 1) -> int:
    sys.stderr.write('reel_cut.py: ' + ' '.join(reason.split()) + '\n')
    return code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
