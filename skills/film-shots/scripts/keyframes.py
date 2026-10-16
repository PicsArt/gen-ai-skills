#!/usr/bin/env python3
"""
Plan a video's key frames, the stills drafted before any footage is bought, and check them before
the video is quoted.

    python3 scripts/keyframes.py input.json
    python3 scripts/keyframes.py < input.json

The input is one JSON object:

    {"frame": {"width": 1080, "height": 1920},
     "beats": [{"id": "hook", "start": 0, "end": 3, "source": "generated"},
               {"id": "steps", "start": 3, "end": 12, "source": "recording", "at": 188.5},
               {"id": "payoff", "start": 12, "end": 17, "source": "generated"},
               {"id": "outro", "start": 17, "end": 19, "source": "card"}],
     "stills": {"hook": {"width": 1080, "height": 1920, "approved": true}}}

- `frame`: the video's frame in pixels.
- `beats`: the plan, in order, in video seconds. `source` is `generated` (footage to be bought),
  `recording` (the user's own footage; `at` is the source time it shows) or `card` (words or
  graphics only, which need no key frame).
- `stills`, optional: the key frames made so far, by beat id, each with its `width`, `height` and
  whether the user `approved` the idea it shows.

The key points are the hook (the first beat that is not a card), the payoff (the last one) and the
turn (the beat between them at the middle of the time). Every generated beat also gets a key frame
at its opening, because its generation starts from it. Each key frame says how the video reuses it:
a generated beat's still is its generation's start frame, picture 1 of `imageUrls`; a recording
beat's still is the recording itself at `at`, shown and never generated.

It prints one JSON line, `{keyframes, generate, findings, ready}`. `generate` counts the stills to
buy. `ready` is true when every generated beat has an approved still, so its video may be quoted.
Each finding has a `code`, the `beat`, a `message` and a `fix`:

- `missing`, `unapproved`: a generated beat without an approved still. These keep `ready` false.
- `small`: a still smaller than the frame, which caps how sharp the video can be.
- `aspect`: a still in another shape than the frame, which the model crops or pads.
- `unused`: a still for a beat that is not a key frame, which nothing in the video would use.
- `too_many`: more than four key frames, more than a concept can show at once.

Input it cannot read exits 1, with one line on stderr that says what is wrong.

Python 3.9 or later, the standard library only, offline.
"""
from __future__ import annotations

import json
import sys
from typing import Any, Dict, List, Optional

SOURCES = ('generated', 'recording', 'card')
MAX_KEYFRAMES = 4
ASPECT_TOLERANCE = 0.02

USAGE = 'usage: keyframes.py [input.json]; with no file, the input is read from stdin'


class InputError(ValueError):
    """Input the script cannot read, with the reason."""


def _num(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _frame(data: Dict[str, Any]) -> Dict[str, float]:
    frame = data.get('frame')
    if not isinstance(frame, dict) or not all(_num(frame.get(k)) and frame[k] > 0 for k in ('width', 'height')):
        raise InputError('frame: must be {"width": <px>, "height": <px>}, both above 0')
    return {'width': frame['width'], 'height': frame['height']}


def _beats(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    beats = data.get('beats')
    if not isinstance(beats, list) or not beats:
        raise InputError("beats: must be a list of the plan's beats, in order")
    seen = set()
    end = 0.0
    for i, b in enumerate(beats):
        where = f'beats[{i}]'
        if not isinstance(b, dict):
            raise InputError(f'{where}: must be an object')
        if not isinstance(b.get('id'), str) or not b['id']:
            raise InputError(f'{where}.id: must be a non-empty string')
        if b['id'] in seen:
            raise InputError(f'{where}.id: "{b["id"]}" is used twice')
        seen.add(b['id'])
        if not (_num(b.get('start')) and _num(b.get('end')) and b['end'] > b['start'] >= 0):
            raise InputError(f'{where}: start and end must be seconds, with end after start')
        if b['start'] < end - 1e-6:
            raise InputError(f'{where}: starts at {b["start"]} s, before the beat before it ends ({end} s)')
        end = b['end']
        if b.get('source') not in SOURCES:
            raise InputError(f'{where}.source: must be one of {", ".join(SOURCES)}')
        if b['source'] == 'recording' and not _num(b.get('at')):
            raise InputError(f'{where}.at: a recording beat needs the source time it shows')
    return beats


def _points(beats: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """The key points in video order, each a beat with its role."""
    shown = [b for b in beats if b['source'] != 'card']
    if not shown:
        return []
    roles: Dict[str, str] = {shown[0]['id']: 'hook'}
    if len(shown) > 1:
        roles[shown[-1]['id']] = 'payoff'
        middle = shown[1:-1]
        if middle:
            mid = (shown[0]['end'] + shown[-1]['start']) / 2
            turn = min(middle, key=lambda b: (0 if b['start'] <= mid < b['end'] else 1, abs((b['start'] + b['end']) / 2 - mid)))
            roles[turn['id']] = 'turn'
    for b in shown:
        if b['source'] == 'generated' and b['id'] not in roles:
            roles[b['id']] = 'opening'
    return [{'beat': b, 'role': roles[b['id']]} for b in shown if b['id'] in roles]


def _keyframe(point: Dict[str, Any]) -> Dict[str, Any]:
    b = point['beat']
    out: Dict[str, Any] = {'beat': b['id'], 'role': point['role'], 'at': b['start']}
    if b['source'] == 'generated':
        out['source'] = 'generate'
        out['use'] = f"the start frame of {b['id']}'s generation: picture 1 of imageUrls"
    else:
        out['source'] = 'recording'
        out['recordingAt'] = b['at']
        out['use'] = f"{b['id']} itself: the recording at {b['at']} s, shown as a still, never generated"
    return out


def _finding(code: str, beat: Optional[str], message: str, fix: str) -> Dict[str, Any]:
    return {'code': code, 'beat': beat, 'message': message, 'fix': fix}


def run(data: Any) -> Dict[str, Any]:
    if not isinstance(data, dict):
        raise InputError('input: must be a JSON object with frame and beats')
    frame = _frame(data)
    beats = _beats(data)
    stills = data.get('stills') or {}
    if not isinstance(stills, dict):
        raise InputError('stills: must be an object keyed by beat id')

    keyframes = [_keyframe(p) for p in _points(beats)]
    generated = [k for k in keyframes if k['source'] == 'generate']
    findings: List[Dict[str, Any]] = []

    if len(keyframes) > MAX_KEYFRAMES:
        findings.append(_finding('too_many', None, f'{len(keyframes)} key frames; a concept is seen at once in three or four',
                                 'plan fewer generated beats, or join neighbouring ones into one shot'))

    keyed = {k['beat'] for k in keyframes}
    for beat_id, still in stills.items():
        if not isinstance(still, dict) or not (_num(still.get('width')) and _num(still.get('height'))):
            raise InputError(f'stills.{beat_id}: must carry width and height in pixels')
        if beat_id not in keyed:
            findings.append(_finding('unused', beat_id, f'a still for {beat_id}, which is not a key frame, so nothing in the video uses it',
                                     'make stills only for the key frames this script lists'))

    fw, fh = frame['width'], frame['height']
    for k in generated:
        still = stills.get(k['beat'])
        if still is None:
            findings.append(_finding('missing', k['beat'], f"{k['beat']} is bought as footage but has no key frame yet",
                                     'generate its still with the other key frames, on one quote, and SHOW them together'))
            continue
        if still.get('approved') is not True:
            findings.append(_finding('unapproved', k['beat'], f"the user has not approved the idea {k['beat']}'s still shows",
                                     'SHOW the key frames together and ASK about the idea before the video is quoted'))
        w, h = still['width'], still['height']
        if abs(w / h - fw / fh) > ASPECT_TOLERANCE * (fw / fh):
            findings.append(_finding('aspect', k['beat'], f"{k['beat']}'s still is {w}x{h}, another shape than the {fw}x{fh} frame",
                                     "generate the still at the video's frame, so the model does not crop or pad its start"))
        elif w < fw or h < fh:
            findings.append(_finding('small', k['beat'], f"{k['beat']}'s still is {w}x{h}, smaller than the {fw}x{fh} frame",
                                     "say in the quote that it caps sharpness, or make it at the frame's size; never upscale it silently"))

    ready = bool(generated) and not any(f['code'] in ('missing', 'unapproved') for f in findings)
    return {'keyframes': keyframes, 'generate': len(generated), 'findings': findings, 'ready': ready}


def main(argv: List[str]) -> int:
    if len(argv) > 2 or (len(argv) == 2 and argv[1] in ('-h', '--help')):
        print(USAGE, file=sys.stderr)
        return 1
    try:
        if len(argv) == 2:
            with open(argv[1], encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = json.load(sys.stdin)
        out = run(data)
    except (OSError, ValueError) as err:
        print(f'keyframes.py: {err}', file=sys.stderr)
        return 1
    print(json.dumps(out))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
