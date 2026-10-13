#!/usr/bin/env python3
"""
Lay a music bed under a scene's speech: one audio layer, faded in and out, that dips under every
spoken stretch and comes back between them.

    python3 scripts/music_bed.py input.json
    python3 scripts/music_bed.py < input.json

The input is one JSON object:

    {
      "scene": { the scene, as it was approved } or "scene.json",
      "transcripts": {"talk": "transcript-talk.json", "vo-1": "transcript-vo-1.json"},
      "music": {"url": "https://cdn.picsart.com/...", "duration": 32.0},
      "level": 30,
      "duck": 15
    }

- `scene` is the scene the user approved. Speech is read from it where it plays: a clip of a
  `track` layer, an `audio` layer, or a `media` layer with a `duration` (a presenter's take over
  the picture), whose asset has a transcript, at that clip's or layer's place and trim. So a clip the user retrimmed in the editor is read as they left it.
- `transcripts` maps an asset id in the scene to its `picsart_media_transcribe` result (or that
  result's `transcript`), or to the path of a file that holds it.
- `music` is the generated bed: its hosted `url`, and its `duration` in seconds, as the
  generation or `picsart_media_probe_media` reports it. It must be at least as long as the scene.
- `level` is the bed's volume between lines and `duck` its volume under speech, as the scene's
  volume percent (0 to 100). Both are optional: 30 and 15 by default.
- `fadeIn` and `fadeOut`, in seconds, are optional: 1 and 2 by default.

Speech closer than 0.8 s to the next speech is one stretch, so the bed does not pump between
words. The bed reaches `duck` as a stretch starts, from 0.15 s before it, and returns to `level`
over 0.6 s after it ends. It prints one JSON line, `{scene, speech, notes}`: the scene with the
bed's asset and its `music` audio layer added, the spoken stretches it ducked under on the
scene's clock, and `notes`. Input it cannot place a bed from exits 1, with one line on stderr that
says what is wrong.

Python 3.9 or later, the standard library only, offline.
"""
from __future__ import annotations

import copy
import json
import math
import os
import sys
from typing import Any, Dict, List, Tuple

USAGE = 'usage: music_bed.py [input.json]; with no file, the input is read from stdin'

LEVEL = 30
DUCK = 15
FADE_IN = 1.0
FADE_OUT = 2.0
ATTACK = 0.15
RELEASE = 0.6
MERGE_GAP = 0.8
LAYER_ID = 'music'

Json = Dict[str, Any]
Span = Tuple[float, float]


class InputError(ValueError):
    """Input a bed cannot be placed from; the message says what to change."""


def number(value: Any, what: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise InputError(f'{what} must be a number')
    return float(value)


def read_json(value: Any, base: str, what: str) -> Any:
    if not isinstance(value, str):
        return value
    path = os.path.join(base, value)
    try:
        with open(path, encoding='utf-8-sig') as f:
            return json.load(f)
    except (OSError, UnicodeDecodeError) as err:
        raise InputError(f'{what}: cannot read {path}: {err}')
    except json.JSONDecodeError as err:
        raise InputError(f'{what}: {path} is not JSON: {err}')


def spoken(asset_id: str, transcript: Any) -> List[Span]:
    """Each stretch of speech on the source's clock: its words where timed, else its segments."""
    if isinstance(transcript, dict) and isinstance(transcript.get('transcript'), dict):
        transcript = transcript['transcript']
    segments = transcript.get('segments') if isinstance(transcript, dict) else None
    if not isinstance(segments, list):
        raise InputError(f'transcripts "{asset_id}" must be the picsart_media_transcribe result, or its transcript')
    spans = []
    for seg in segments:
        words = seg.get('words') or []
        if words:
            spans += [(float(w['start']), float(w['end'])) for w in words]
        else:
            spans.append((float(seg['start']), float(seg['end'])))
    return spans


def heard_until(at: float, length: float, trim: Any, speed: float) -> float:
    """When a source stops being heard: its place's end, or sooner where its trim runs out."""
    if not trim:
        return at + length
    return at + min(length, (number(trim['out'], 'trim out') - number(trim['in'], 'trim in')) / speed)


def windows(scene: Json) -> Tuple[List[Json], float]:
    """Where each source plays on the scene's clock, and when the scene ends."""
    out = []
    end = 0.0
    images = {a.get('id') for a in scene.get('assets') or [] if isinstance(a, dict) and a.get('type') == 'image'}
    for layer in scene.get('layers') or []:
        if not isinstance(layer, dict):
            continue
        content = layer.get('content') or {}
        at = number(layer.get('start', 0), f'layer "{layer.get("id")}" start')
        if content.get('kind') == 'track':
            for i, clip in enumerate(content.get('clips') or []):
                media = clip.get('content') or {}
                trim = media.get('trim')
                speed = number(media.get('speed', 1), f'clips[{i}] speed')
                if clip.get('duration') is not None:
                    length = number(clip['duration'], f'clips[{i}] duration')
                elif trim:
                    length = (number(trim['out'], 'trim out') - number(trim['in'], 'trim in')) / speed
                else:
                    raise InputError(f'clips[{i}] has no duration and no trim, so its length is unknown')
                if not media.get('muted') and media.get('assetId') not in images:
                    out.append({'asset': media.get('assetId'), 'start': at, 'end': heard_until(at, length, trim, speed),
                                'in': float(trim['in']) if trim else 0.0, 'speed': speed})
                at += length
            end = max(end, at)
        elif content.get('kind') == 'audio':
            trim = content.get('trim')
            if layer.get('duration') is not None:
                length = number(layer['duration'], f'layer "{layer.get("id")}" duration')
            elif trim:
                length = number(trim['out'], 'trim out') - number(trim['in'], 'trim in')
            else:
                continue
            if not content.get('muted'):
                speed = number(content.get('speed', 1), 'speed')
                out.append({'asset': content.get('assetId'), 'start': at, 'end': heard_until(at, length, trim, speed),
                            'in': float(trim['in']) if trim else 0.0, 'speed': speed})
            end = max(end, at + length)
        elif content.get('kind') == 'media' and layer.get('duration') is not None:
            # A clip over the picture that plays its own sound: a presenter's take, say.
            length = number(layer['duration'], f'layer "{layer.get("id")}" duration')
            trim = content.get('trim')
            if not content.get('muted') and content.get('assetId') not in images:
                speed = number(content.get('speed', 1), 'speed')
                out.append({'asset': content.get('assetId'), 'start': at, 'end': heard_until(at, length, trim, speed),
                            'in': float(trim['in']) if trim else 0.0, 'speed': speed})
            end = max(end, at + length)
        elif layer.get('duration') is not None:
            end = max(end, at + number(layer['duration'], f'layer "{layer.get("id")}" duration'))
    composed = (scene.get('composition') or {}).get('duration')
    return out, number(composed, 'the composition duration') if composed is not None else end


def speech_on_scene(plays: List[Json], spans: Dict[str, List[Span]]) -> List[Span]:
    heard = []
    for play in plays:
        for a, b in spans.get(play['asset'], []):
            a = play['start'] + (a - play['in']) / play['speed']
            b = play['start'] + (b - play['in']) / play['speed']
            a, b = max(a, play['start']), min(b, play['end'])
            if b > a:
                heard.append((a, b))
    merged: List[List[float]] = []
    for a, b in sorted(heard):
        if merged and a - merged[-1][1] < MERGE_GAP:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    return [(round(a, 3), round(b, 3)) for a, b in merged]


def envelope(speech: List[Span], end: float, level: float, duck: float, fade_in: float, fade_out: float) -> List[Json]:
    def ducked(t: float) -> float:
        gain = level
        for a, b in speech:
            if a - ATTACK <= t <= b:
                v = duck if t >= a else level - (level - duck) * (t - (a - ATTACK)) / ATTACK
            elif b < t < b + RELEASE:
                v = duck + (level - duck) * (t - b) / RELEASE
            else:
                continue
            gain = min(gain, v)
        return gain

    def faded(t: float) -> float:
        rise = min(1.0, t / fade_in) if fade_in > 0 else 1.0
        fall = min(1.0, (end - t) / fade_out) if fade_out > 0 else 1.0
        return max(0.0, min(rise, fall))

    times = {0.0, end, min(fade_in, end), max(end - fade_out, 0.0)}
    for a, b in speech:
        times.update({a - ATTACK, a, b, b + RELEASE})
    times = sorted(t for t in times if 0 <= t <= end)
    keys = [{'time': round(t, 3), 'value': round(ducked(t) * faded(t), 2)} for t in times]
    for k in keys[:-1]:
        k['easing'] = 'linear'
    return keys


def lay(data: Any, base: str = '.') -> Json:
    if not isinstance(data, dict):
        raise InputError('the input must be a JSON object')
    scene = read_json(data.get('scene'), base, 'scene')
    if not isinstance(scene, dict) or not isinstance(scene.get('layers'), list):
        raise InputError('scene must be the scene document, or the path of a file that holds it')
    scene = copy.deepcopy(scene)
    music = data.get('music')
    if not isinstance(music, dict) or not isinstance(music.get('url'), str) or not music['url'].startswith('https://'):
        raise InputError('music needs "url", the hosted bed, and "duration", its length in seconds')
    length = number(music.get('duration'), 'music duration')
    level = number(data.get('level', LEVEL), 'level')
    duck = number(data.get('duck', DUCK), 'duck')
    if not 0 <= duck <= level <= 100:
        raise InputError('level and duck are volume percent, with 0 <= duck <= level <= 100')
    fade_in = number(data.get('fadeIn', FADE_IN), 'fadeIn')
    fade_out = number(data.get('fadeOut', FADE_OUT), 'fadeOut')
    raw = data.get('transcripts') or {}
    if not isinstance(raw, dict):
        raise InputError('transcripts must map an asset id to its transcript')
    spans = {aid: spoken(aid, read_json(t, base, f'transcripts "{aid}"')) for aid, t in raw.items()}

    plays, end = windows(scene)
    if end <= 0:
        raise InputError('the scene has no length to lay a bed under')
    if length + 1e-6 < end:
        raise InputError(f'the bed is {length:g}s and the scene {end:g}s: generate one at least {math.ceil(end)}s long')
    assets = scene.setdefault('assets', [])
    taken = set(assets) if isinstance(assets, dict) else {a.get('id') for a in assets if isinstance(a, dict)}
    if LAYER_ID in taken or any(isinstance(l, dict) and l.get('id') == LAYER_ID for l in scene['layers']):
        raise InputError(f'the scene already has a "{LAYER_ID}" asset or layer: start from the scene without it')

    speech = speech_on_scene(plays, spans)
    notes = []
    if spans and not speech:
        notes.append('no transcribed speech plays in the scene, so the bed never ducks')
    if not spans:
        notes.append('no transcripts given, so the bed never ducks: pass every spoken source\'s transcript')
    asset = {'type': 'audio', 'uri': music['url'], 'duration': length}
    if isinstance(assets, dict):
        assets[LAYER_ID] = asset
    else:
        assets.append({'id': LAYER_ID, **asset})
    scene['layers'].append({
        'id': LAYER_ID, 'start': 0, 'duration': round(end, 3),
        'content': {'kind': 'audio', 'assetId': LAYER_ID, 'trim': {'in': 0, 'out': round(end, 3)}, 'volume': level},
        'animations': {'volume': {'keyframes': envelope(speech, round(end, 3), level, duck, fade_in, fade_out)}},
    })
    return {'scene': scene, 'speech': [list(s) for s in speech], 'notes': notes}


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
        out = lay(json.loads(text), os.path.dirname(os.path.abspath(argv[0])) if argv else os.getcwd())
    except json.JSONDecodeError as err:
        return fail(f'the input is not JSON: {err}')
    except InputError as err:
        return fail(str(err))
    except (KeyError, IndexError, TypeError, AttributeError, ZeroDivisionError) as err:
        return fail(f'cannot lay a bed from this input: {type(err).__name__} {err}')
    sys.stdout.buffer.write((json.dumps(out, separators=(',', ':'), ensure_ascii=False) + '\n').encode('utf-8'))
    return 0


def fail(reason: str, code: int = 1) -> int:
    sys.stderr.write('music_bed.py: ' + ' '.join(reason.split()) + '\n')
    return code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
