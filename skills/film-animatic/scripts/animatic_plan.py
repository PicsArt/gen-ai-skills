#!/usr/bin/env python3
"""
Time an animatic from its shot cards and the real length of its voice lines, and check the cards
before any panel is bought.

    python3 scripts/animatic_plan.py input.json
    python3 scripts/animatic_plan.py < input.json

The input is one JSON object:

    {"shots": [{"id": "A", "seconds": 2.5, "mode": "observed", "eyeline": "the phone",
                "lines": [{"who": "@bev", "text": "I'll just send the chat a picture.", "sec": 1.9}]},
               {"id": "B", "seconds": 3, "mode": "observed", "eyeline": "@dot",
                "decides": true, "cause": "A", "peak": true,
                "lines": [{"who": "@bev", "text": "It's only a chat."}]}],
     "lead": 0.15, "gap": 0.2, "tail": 0.3}

- `shots`: the approved cards, in story order. `seconds` is the card's planned length. `mode` is
  the camera's relation (`lens`, `observed`, `pov` or `voice-over`); `eyeline` is who or what the
  person on screen looks at or speaks to. `switch: true` marks a shot that shows a change of mode.
  `decides: true` marks a shot where someone decides; `cause` is the id of the earlier shot that
  shows why. `peak: true` marks the film's one peak.
- `lines`, optional per shot: what is heard in it, in order. `sec` is the line's real length from
  `picsart_media_probe`; without it the length is estimated at three words a second.
- `lead` (0.15 s), `gap` (0.2 s) and `tail` (0.3 s), optional: the silence before the first line,
  between lines and after the last.

A shot keeps its planned length unless its lines need more: then the still holds longer, and the
words are never cut. It prints one JSON line, `{timeline, total, findings, ok}`. `timeline` has
each shot's `start`, `end` and `seconds`, and each line's `start` and `end` in animatic seconds,
ready for the scene's audio layers. Each finding has a `code`, a `level` (`error`, `warn` or
`info`), the `shot`, a `message` and a `fix`. `ok` is false while any `error` stands.

- `no-mode`, `no-eyeline` (error): a card that does not say the camera's relation or who is
  addressed, so the viewer cannot tell who is spoken to.
- `mode-switch` (error): the camera's relation changes from the shot before with no shown switch.
- `no-cause` (error): a decision with no earlier shot showing its cause.
- `peak` (error): the film has no peak or more than one.
- `opening` (warn): the first shot is shorter than 1.5 s, so the opening cannot hold one thing.
- `unprobed` (warn): a line timed from its word count, not its real length.
- `stretched` (info): a shot held longer than its card to fit its real lines.
"""
from __future__ import annotations

import json
import sys
from typing import Any, Dict, List, Optional

USAGE = 'usage: python3 scripts/animatic_plan.py [input.json]   (or JSON on stdin)'
MODES = ('lens', 'observed', 'pov', 'voice-over')
WORDS_PER_SEC = 3.0
OPENING_SEC = 1.5


class InputError(ValueError):
    pass


def _num(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _finding(code: str, level: str, shot: Optional[str], message: str, fix: str) -> Dict[str, Any]:
    return {'code': code, 'level': level, 'shot': shot, 'message': message, 'fix': fix}


def _shots(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    shots = data.get('shots')
    if not isinstance(shots, list) or not shots:
        raise InputError('shots: must be a non-empty list of the approved cards, in story order')
    seen = set()
    for i, s in enumerate(shots):
        where = f'shots[{i}]'
        if not isinstance(s, dict):
            raise InputError(f'{where}: must be an object')
        if not isinstance(s.get('id'), str) or not s['id']:
            raise InputError(f'{where}.id: must be a non-empty string')
        if s['id'] in seen:
            raise InputError(f'{where}.id: "{s["id"]}" is used twice')
        seen.add(s['id'])
        if not _num(s.get('seconds')) or s['seconds'] <= 0:
            raise InputError(f'{where}.seconds: must be the card\'s length in seconds, above 0')
        lines = s.get('lines', [])
        if not isinstance(lines, list):
            raise InputError(f'{where}.lines: must be a list')
        for j, line in enumerate(lines):
            if not isinstance(line, dict) or not isinstance(line.get('text'), str):
                raise InputError(f'{where}.lines[{j}]: must be {{"who", "text", "sec"?}}')
            if 'sec' in line and (not _num(line['sec']) or line['sec'] <= 0):
                raise InputError(f'{where}.lines[{j}].sec: must be the probed length in seconds, above 0')
    return shots


def _r(x: float) -> float:
    return round(x + 1e-9, 2)


def run(data: Any) -> Dict[str, Any]:
    if not isinstance(data, dict):
        raise InputError('input: must be a JSON object with "shots"')
    shots = _shots(data)
    lead = data.get('lead', 0.15)
    gap = data.get('gap', 0.2)
    tail = data.get('tail', 0.3)
    for name, v in (('lead', lead), ('gap', gap), ('tail', tail)):
        if not _num(v) or v < 0:
            raise InputError(f'{name}: must be seconds, 0 or more')

    findings: List[Dict[str, Any]] = []
    timeline: List[Dict[str, Any]] = []
    order = {s['id']: i for i, s in enumerate(shots)}
    t = 0.0
    prev_mode: Optional[str] = None
    for i, s in enumerate(shots):
        sid = s['id']
        mode = s.get('mode')
        if mode not in MODES:
            findings.append(_finding('no-mode', 'error', sid, f'{sid} does not say the camera\'s relation',
                                     f'set its mode to one of {", ".join(MODES)}'))
        elif prev_mode and mode != prev_mode and not s.get('switch'):
            findings.append(_finding('mode-switch', 'error', sid, f'{sid} goes from {prev_mode} to {mode} with no shown switch',
                                     'keep one mode, or show the switch in the shot (a look to the lens, a cut to her eyes) and mark it'))
        if mode in MODES:
            prev_mode = mode
        if not isinstance(s.get('eyeline'), str) or not s['eyeline'].strip():
            findings.append(_finding('no-eyeline', 'error', sid, f'{sid} does not say who or what is looked at or spoken to',
                                     'name the eyeline: the lens, a person by tag, or a thing in frame'))
        if s.get('decides'):
            cause = s.get('cause')
            if not isinstance(cause, str) or cause not in order or order[cause] >= i:
                findings.append(_finding('no-cause', 'error', sid, f'{sid} holds a decision with no earlier shot showing why',
                                         'name the earlier shot that shows the cause, or add one before it'))

        need = 0.0
        placed = []
        lines = s.get('lines', [])
        if lines:
            cursor = lead
            for j, line in enumerate(lines):
                sec = line.get('sec')
                if sec is None:
                    words = len(line['text'].split())
                    sec = max(words / WORDS_PER_SEC, 0.5)
                    findings.append(_finding('unprobed', 'warn', sid, f'{sid} line {j + 1} is timed from its words, not its real length',
                                             'probe the voice line with picsart_media_probe and run this again'))
                if j:
                    cursor += gap
                placed.append({'who': line.get('who'), 'text': line['text'], 'start': _r(t + cursor), 'end': _r(t + cursor + sec)})
                cursor += sec
            need = cursor + tail
        seconds = max(float(s['seconds']), need)
        if seconds > s['seconds'] + 1e-9:
            findings.append(_finding('stretched', 'info', sid, f'{sid} holds {_r(seconds)} s, not its card\'s {s["seconds"]} s, to fit its lines',
                                     'keep the words; the still holds longer. Shorten the line only if the story asks for it'))
        timeline.append({'shot': sid, 'start': _r(t), 'end': _r(t + seconds), 'seconds': _r(seconds), 'planned': s['seconds'], 'lines': placed})
        t += seconds

    peaks = [s['id'] for s in shots if s.get('peak')]
    if len(peaks) != 1:
        findings.append(_finding('peak', 'error', None,
                                 'no shot is marked as the peak' if not peaks else f'{len(peaks)} shots are marked as the peak: {", ".join(peaks)}',
                                 'mark exactly one peak, as film-story-writing\'s peak rule says'))
    if timeline[0]['seconds'] < OPENING_SEC:
        findings.append(_finding('opening', 'warn', shots[0]['id'], f'the first shot holds {timeline[0]["seconds"]} s, under {OPENING_SEC} s',
                                 'hold the opening on one thing for at least 1.5 s'))

    ok = not any(f['level'] == 'error' for f in findings)
    return {'timeline': timeline, 'total': _r(t), 'findings': findings, 'ok': ok}


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
        print(f'animatic_plan.py: {err}', file=sys.stderr)
        return 1
    print(json.dumps(out))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
