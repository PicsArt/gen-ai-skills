#!/usr/bin/env python3
"""
Check an exported file against the scene it was exported from, before the user gets the link.

    python3 scripts/qc.py input.json
    python3 scripts/qc.py < input.json

The input is one JSON object:

    {"scene": {...}, "probe": {...}, "audio": {"integratedLufs": -15.2, "truePeak": -1.1}}

- `scene`: the scene that was exported (a builder's whole output is read too). Its composition
  gives the planned size, fps and length, and its audio layers, or a media layer that is not
  muted (a media layer is unmuted unless it says `"muted": true`, and a still is silent), say the
  file should have sound, nested scenes included where a `scene_ref` plays them. `plan` instead gives them by hand:
  `{width, height, fps, duration, audio}`, and a `plan` field overrides the scene's.
- `probe`: what `picsart_media_probe` returned for the exported file, exactly as returned.
- `audio`, optional, only what a tool measured: `integratedLufs`, `truePeak` (dBTP), `duration`
  (the sound's own length, in seconds), and `energy`, the loudness over time as `[[t, dB], ...]`
  or `{times, values}`. Values from 0 to 1 are read as linear amplitude.

The checks, each an `error` (fix it before delivering) or a `warning` (say it):

- `size`: the file's width and height are the plan's (error);
- `fps`: its frame rate is the plan's (error);
- `length`: its length is the plan's, within a quarter second (error);
- `no_audio`: the plan has sound and the file has no audio track (error);
- `av_drift`: the sound and the picture differ in length by more than 0.5 s (error);
- `true_peak`: the sound peaks above -0.5 dBTP, so the platform's encoder may clip it (error);
- `loudness`: the sound is outside -16 to -12 LUFS; the feeds play near -14 (warning);
- `silent_tail`: the sound ends more than 1.2 s before the picture does (warning).

What the inputs cannot answer is listed in `unchecked`, with why: a check is never passed on a
guess.

It prints one JSON line, `{ok, errors, warnings, checked, unchecked}`; `ok` is true when there is
no error. Each finding has a `code`, a `message` and a `fix`. Input it cannot check exits 1, with
one line on stderr that says what is wrong.

Python 3.9 or later, the standard library only, offline.
"""
from __future__ import annotations

import json
import math
import sys
from typing import Any, Dict, List, Tuple

from timing import _clip_length, scene_duration

LENGTH_TOLERANCE = 0.25
FPS_TOLERANCE = 0.05
DRIFT = 0.5
TRUE_PEAK = -0.5
LOUDNESS = (-16.0, -12.0)
SILENCE_DB = -50.0
SILENT_TAIL = 1.2

USAGE = 'usage: qc.py [input.json]; with no file, the input is read from stdin'


class InputError(ValueError):
    """Input the script cannot check, with the reason."""


def _num(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def has_sound(scene: Dict[str, Any]) -> bool:
    """
    An audio layer, or a media layer that is not muted and is not a still, anywhere the scene
    plays: its layers, inline groups, tracks and nested scenes, within their playback bounds.
    A nested scene no layer plays is not heard.
    """
    def assets_of(s: Dict[str, Any], outer: Dict[str, Any]) -> Dict[str, Any]:
        declared = s.get('assets') or {}
        # The builders key assets by id; a list of assets with ids is read too.
        if isinstance(declared, dict):
            own = {k: a for k, a in declared.items() if isinstance(a, dict)}
        else:
            own = {a.get('id'): a for a in declared if isinstance(a, dict)}
        return {**outer, **own}

    def heard(s: Dict[str, Any], outer: Dict[str, Any], seen: frozenset,
              begin: float = 0.0, end: float = math.inf) -> bool:
        if id(s) in seen:
            return False
        seen = seen | {id(s)}
        assets = assets_of(s, outer)
        duration = (s.get('composition') or {}).get('duration')
        if _num(duration):
            end = min(end, duration)

        def plays(item: Dict[str, Any], at: float, until: float) -> bool:
            c = item.get('content') or {}
            if c.get('muted') is True:
                return False
            asset = c['asset'] if isinstance(c.get('asset'), dict) else assets.get(c.get('assetId')) or {}
            resolved = {**item, 'content': {**c, 'assetId': '_resolved'}}
            length = _clip_length(resolved, {'_resolved': asset})
            stop = min(until, at + length) if length is not None else until
            if stop <= max(begin, at):
                return False
            kind = c.get('kind')
            if kind == 'audio' or kind == 'media' and asset.get('type') != 'image':
                return True
            speed = c['speed'] if _num(c.get('speed')) and c['speed'] > 0 else 1.0
            trim = c.get('trim') or {}
            source_in = trim['in'] if _num(trim.get('in')) else 0.0
            first = source_in + max(0.0, begin - at) * speed
            last = source_in + (stop - at) * speed
            if _num(trim.get('out')) and not c.get('loop'):
                last = min(last, trim['out'])
            if last <= first:
                return False
            if kind == 'track':
                cursor = 0.0
                clips = []
                for clip in c.get('clips') or []:
                    if not isinstance(clip, dict):
                        continue
                    clips.append({**clip, 'start': cursor})
                    span = _clip_length(clip, assets)
                    if span is not None:
                        cursor += span
                return heard({'layers': clips}, assets, seen, first, last)
            inner = asset.get('scene') if kind == 'scene_ref' else None
            if kind == 'composition':
                inner = c
            if isinstance(inner, dict) and c.get('loop'):
                duration = scene_duration(inner)
                if duration and duration > 0:
                    source_end = trim.get('out', duration)
                    cycle = source_end - source_in
                    if cycle > 0:
                        if last - first >= cycle:
                            return heard(inner, assets, seen, source_in, source_end)
                        a = source_in + (first - source_in) % cycle
                        b = a + last - first
                        return heard(inner, assets, seen, a, min(b, source_end)) or (b > source_end and heard(inner, assets, seen, source_in, source_in + b - source_end))
            return isinstance(inner, dict) and heard(inner, assets, seen, first, last)

        for layer in s.get('layers') or []:
            if isinstance(layer, dict):
                start = layer['start'] if _num(layer.get('start')) else 0.0
                if plays(layer, start, end):
                    return True
        return False

    return heard(scene, {}, frozenset())


def plan_of(data: Dict[str, Any]) -> Dict[str, Any]:
    scene = data.get('scene')
    if isinstance(scene, dict) and 'scene' in scene and 'layers' not in scene:
        scene = scene['scene']
    plan: Dict[str, Any] = {}
    if isinstance(scene, dict):
        comp = scene.get('composition') or {}
        given = data.get('plan') or {}
        duration = given.get('duration') if 'duration' in given else comp.get('duration') if 'duration' in comp else scene_duration(scene)
        plan = {'width': comp.get('width'), 'height': comp.get('height'), 'fps': comp.get('fps'), 'duration': duration, 'audio': has_sound(scene)}
    elif scene is not None:
        raise InputError('scene must be the scene document')
    given = data.get('plan')
    if given is not None:
        if not isinstance(given, dict):
            raise InputError('plan must be an object: {width, height, fps, duration, audio}')
        plan.update(given)
    if not plan:
        raise InputError('give the scene that was exported, or a plan')
    return plan


def energy_series(v: Any) -> List[Tuple[float, float]]:
    if isinstance(v, dict):
        pairs = list(zip(v.get('times') or [], v.get('values') or []))
    elif isinstance(v, list):
        pairs = [tuple(p) for p in v if isinstance(p, (list, tuple)) and len(p) == 2]
    else:
        raise InputError('audio.energy must be [[t, dB], ...] or {times, values}')
    pairs = [(float(t), float(x)) for t, x in pairs if _num(t) and _num(x)]
    if pairs and all(0 <= x <= 1 for _, x in pairs):
        pairs = [(t, 20 * math.log10(x) if x > 0 else -120.0) for t, x in pairs]
    return sorted(pairs)


def check(plan: Dict[str, Any], probe: Dict[str, Any], audio: Dict[str, Any]) -> Dict[str, Any]:
    errors: List[Dict[str, str]] = []
    warnings: List[Dict[str, str]] = []
    checked: List[str] = []
    unchecked: List[Dict[str, str]] = []

    def skip(name: str, why: str) -> None:
        unchecked.append({'check': name, 'why': why})

    def err(code: str, message: str, fix: str) -> None:
        errors.append({'code': code, 'message': message, 'fix': fix})

    def warn(code: str, message: str, fix: str) -> None:
        warnings.append({'code': code, 'message': message, 'fix': fix})

    w, h = probe.get('width'), probe.get('height')
    if _num(w) and _num(h) and _num(plan.get('width')) and _num(plan.get('height')):
        checked.append('size')
        if (round(w), round(h)) != (round(plan['width']), round(plan['height'])):
            err('size', f"the file is {w:g}x{h:g}, the scene {plan['width']:g}x{plan['height']:g}", "export again; if it repeats, say the export changes the size")
    else:
        skip('size', 'the probe or the plan has no width and height')

    fps = probe.get('fps')
    if _num(fps) and _num(plan.get('fps')):
        checked.append('fps')
        if abs(fps - plan['fps']) > FPS_TOLERANCE:
            err('fps', f"the file plays at {fps:g} fps, the scene at {plan['fps']:g}", 'export again at the scene\'s fps')
    else:
        skip('fps', 'the probe gave no fps' if not _num(fps) else 'the plan has no fps')

    length = probe.get('durationSeconds')
    if _num(length) and _num(plan.get('duration')):
        checked.append('length')
        if abs(length - plan['duration']) > LENGTH_TOLERANCE:
            err('length', f"the file is {length:.2f} s, the scene {plan['duration']:.2f} s", 'export again; if it repeats, check the last layer ends where the composition does')
    else:
        skip('length', 'the probe gave no duration' if not _num(length) else 'the plan has no duration')

    wants_sound = plan.get('audio')
    if wants_sound is True:
        if probe.get('hasAudio') is False:
            checked.append('no_audio')
            err('no_audio', 'the scene has sound and the file has no audio track', 'check the audio layers are not muted, and export again')
        elif probe.get('hasAudio') is True:
            checked.append('no_audio')
        else:
            skip('no_audio', 'the probe did not say whether the file has sound')

    a_len = audio.get('duration')
    if _num(a_len) and _num(length):
        checked.append('av_drift')
        if abs(a_len - length) > DRIFT:
            err('av_drift', f'the sound is {a_len:.2f} s and the picture {length:.2f} s', 'trim the audio layers to the composition and export again')
    elif wants_sound:
        skip('av_drift', 'no tool measured the sound\'s own length')

    peak = audio.get('truePeak')
    if _num(peak):
        checked.append('true_peak')
        if peak > TRUE_PEAK:
            err('true_peak', f'the sound peaks at {peak:g} dBTP, above {TRUE_PEAK:g}', 'lower the loudest layer\'s volume and export again')
    elif wants_sound:
        skip('true_peak', 'no tool measured the true peak')

    lufs = audio.get('integratedLufs')
    if _num(lufs):
        checked.append('loudness')
        if not LOUDNESS[0] <= lufs <= LOUDNESS[1]:
            louder = lufs < LOUDNESS[0]
            warn('loudness', f'the sound is {lufs:g} LUFS; the feeds play near -14', 'raise the voice and the bed together' if louder else 'lower the voice and the bed together')
    elif wants_sound:
        skip('loudness', 'no tool measured the loudness')

    if audio.get('energy') is not None and wants_sound:
        series = energy_series(audio['energy'])
        end = length if _num(length) else plan.get('duration')
        if series and _num(end):
            checked.append('silent_tail')
            loud = [t for t, db in series if db > SILENCE_DB]
            last = loud[-1] if loud else 0.0
            if end - last > SILENT_TAIL:
                warn('silent_tail', f'the sound stops at {last:.1f} s and the picture runs to {end:.1f} s', 'end the picture closer to the last sound, or carry the bed to the end')
        else:
            skip('silent_tail', 'the energy curve is empty')
    elif wants_sound:
        skip('silent_tail', 'no energy curve was given')

    return {'ok': not errors, 'errors': errors, 'warnings': warnings, 'checked': checked, 'unchecked': unchecked}


def run(data: Any) -> Dict[str, Any]:
    """The script's whole job: the checked input in, the line it prints out."""
    if not isinstance(data, dict):
        raise InputError('the input must be one JSON object')
    probe = data.get('probe')
    if not isinstance(probe, dict):
        raise InputError('probe must be what picsart_media_probe returned, as one object')
    audio = data.get('audio') or {}
    if not isinstance(audio, dict):
        raise InputError('audio must be an object')
    return check(plan_of(data), probe, audio)


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
    sys.stderr.write('qc.py: ' + ' '.join(reason.split()) + '\n')
    return code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
