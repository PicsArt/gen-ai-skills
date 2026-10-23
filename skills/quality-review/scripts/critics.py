#!/usr/bin/env python3
"""
The critic panel's arithmetic: which frames the critics see, and their notes laid side by side.

    python3 scripts/critics.py input.json
    python3 scripts/critics.py < input.json

The input is one JSON object with one or both of:

    {"scene": {...}, "every": 0.5, "per_sheet": 8,
     "notes": [{"critic": "growth", "verdict": "...",
                "problems": [{"at": [0, 1.5], "what": "...", "fix": "..."}],
                "drops": [3.5]}]}

- `scene`: the built scene (a builder's whole output is read too). Out comes `frames`:
  `sheets`, the times every `every` seconds (0.5 by default) from 0 to the last frame, split into
  one list per `picsart_scene_contact_sheet` call of at most `per_sheet` times (8 by default);
  and `words`, every block of words on screen, with when it starts and ends.
- `notes`: each critic's note. `critic` is one of `roots`, `radical`, `interface`, `story`,
  `growth` or `art`. Every note has a one-line `verdict` and `problems`, each with `at` (a time,
  a `[from, to]` range in seconds, or `"whole"` for the whole video), `what` and `fix`, and
  `fidelity: true` when the draft differs from the source stills. Then, by critic:
  - `roots`: `core`, the one sentence the video is built around (required); `decoration` and
    `missing`, lists; `wrong_problem`, when the stated goal is the wrong problem;
  - `radical`: `concepts`, 2 or 3 alternative concepts (required);
  - `story`: `script`, the rewritten script;
  - `growth`: `drops`, the times a viewer is predicted to leave.

It prints one JSON line: `frames` when there was a scene, and with notes:

- `core`: the first-principles critic's sentence, the yardstick for every fix;
- `verdicts`: each critic's one line, in panel order;
- `agree`: each stretch of time two or more critics flagged, with every problem in it. The
  critics may name one problem there or two different ones: you read which;
- `fidelity`: every problem marked `fidelity`, from any critic: each is a must-fix;
- `single`: each problem only one critic flagged at its time; `whole`: the problems with no time;
- `choices`: what goes to the user as an ASK and is never applied silently: each radical concept,
  and a `wrong_problem`;
- `drops`, `script`, `decoration` and `missing`, as the critics gave them;
- `long`: the critics whose note runs over 350 words; `absent`: the critics with no note;
- `summary`: one line for the review.

Input it cannot read exits 1, with one line on stderr that says what is wrong.

Python 3.9 or later, the standard library only, offline.
"""
from __future__ import annotations

import json
import sys
from typing import Any, Dict, List, Optional, Tuple

from panel import _blocks, _duration, _last, _num

CRITICS = ('roots', 'radical', 'interface', 'story', 'growth', 'art')
NAMES = {
    'roots': 'the first-principles critic',
    'radical': 'the radical',
    'interface': 'the interface designer',
    'story': 'the story editor',
    'growth': 'the growth strategist',
    'art': 'the art director',
}
EVERY = 0.5
PER_SHEET = 8
NEAR = 0.5
MAX_WORDS = 350

USAGE = 'usage: critics.py [input.json]; with no file, the input is read from stdin'


class InputError(ValueError):
    """Input the script cannot read, with the reason."""


def _scene(data: Dict[str, Any]) -> Dict[str, Any]:
    scene = data['scene']
    if isinstance(scene, dict) and 'scene' in scene and 'layers' not in scene:
        scene = scene['scene']
    if not isinstance(scene, dict) or not isinstance(scene.get('layers'), list):
        raise InputError('scene must be the scene document, with its layers')
    return scene


def _positive(data: Dict[str, Any], key: str, default: float) -> float:
    v = data.get(key, default)
    if not _num(v) or v <= 0:
        raise InputError(f'{key} must be a number above 0')
    return float(v)


def frames(scene: Dict[str, Any], every: float, per_sheet: int) -> Dict[str, Any]:
    duration = _duration(scene)
    if not duration:
        raise InputError('the scene has no length: no composition.duration, and nothing in it is timed, so there is no timeline to sample')
    last = _last(scene, duration)
    times, i = [], 0
    while round(i * every, 3) <= last:
        times.append(round(i * every, 3))
        i += 1
    if times[-1] < last:
        times.append(last)
    sheets = [times[k:k + per_sheet] for k in range(0, len(times), per_sheet)]
    words = [{'at': b['at'], 'end': round(min(b['end'], duration), 3), 'words': b['words']} for b in _blocks(scene)]
    return {'sheets': sheets, 'words': words}


def _line(v: Any, where: str) -> str:
    if not isinstance(v, str) or not v.strip():
        raise InputError(f'{where} must be a sentence')
    return ' '.join(v.split())


def _strings(v: Any, where: str) -> List[str]:
    if v is None:
        return []
    if not isinstance(v, list) or not all(isinstance(s, str) and s.strip() for s in v):
        raise InputError(f'{where} must be a list of sentences')
    return [' '.join(s.split()) for s in v]


def _span(v: Any, where: str, duration: Optional[float]) -> Optional[Tuple[float, float]]:
    if v == 'whole':
        return None
    if _num(v):
        span = (float(v), float(v))
    elif isinstance(v, list) and len(v) == 2 and all(_num(x) for x in v) and v[0] <= v[1]:
        span = (float(v[0]), float(v[1]))
    else:
        raise InputError(f'{where}.at must be a time, a [from, to] range in seconds, or "whole"')
    if span[0] < 0 or (duration is not None and span[0] > duration):
        raise InputError(f'{where}.at is outside the video')
    return span


def _count(v: Any) -> int:
    if isinstance(v, str):
        return len(v.split())
    if isinstance(v, list):
        return sum(_count(x) for x in v)
    if isinstance(v, dict):
        return sum(_count(x) for k, x in v.items() if k != 'critic')
    return 0


def _plural(n: int, word: str) -> str:
    return f'{n} {word}' + ('' if n == 1 else 's')


def _note(note: Dict[str, Any], i: int, out: Dict[str, Any], timed: List[Dict[str, Any]],
          duration: Optional[float]) -> str:
    """Check one critic's note, and file its parts into `out` and `timed`."""
    critic = note.get('critic')
    if critic not in CRITICS:
        raise InputError(f'notes[{i}].critic must be one of ' + ', '.join(CRITICS))
    raw = note.get('verdict')
    if isinstance(raw, str) and '\n' in raw.strip():
        raise InputError(f'{critic}.verdict must be one line')
    out['verdicts'].append({'critic': critic, 'verdict': _line(raw, f'{critic}.verdict')})
    problems = note.get('problems')
    if not isinstance(problems, list) or not all(isinstance(p, dict) for p in problems):
        raise InputError(f'{critic}.problems must be a list, empty when nothing is wrong')
    for k, p in enumerate(problems):
        where = f'{critic}.problems[{k}]'
        item = {'critic': critic, 'what': _line(p.get('what'), f'{where}.what'), 'fix': _line(p.get('fix'), f'{where}.fix')}
        if p.get('fidelity', False) not in (True, False):
            raise InputError(f'{where}.fidelity must be true or false')
        if p.get('fidelity'):
            item['fidelity'] = True
        span = _span(p.get('at'), where, duration)
        if span is None:
            out['whole'].append(item)
        else:
            timed.append(dict(item, at=[round(span[0], 3), round(span[1], 3)]))
    if _count(note) > MAX_WORDS:
        out['long'].append(critic)
    if critic == 'roots':
        out['core'] = _line(note.get('core'), 'roots.core')
        out['decoration'] = _strings(note.get('decoration'), 'roots.decoration')
        out['missing'] = _strings(note.get('missing'), 'roots.missing')
        if note.get('wrong_problem') is not None:
            out['choices'].append({'critic': 'roots', 'choice': _line(note['wrong_problem'], 'roots.wrong_problem')})
    elif critic == 'radical':
        concepts = _strings(note.get('concepts'), 'radical.concepts')
        if not 2 <= len(concepts) <= 3:
            raise InputError(f'radical.concepts must hold 2 or 3 concepts, not {len(concepts)}')
        out['choices'].extend({'critic': 'radical', 'choice': c} for c in concepts)
    elif critic == 'story' and note.get('script') is not None:
        out['script'] = _line(note['script'], 'story.script')
    elif critic == 'growth' and note.get('drops') is not None:
        drops = note['drops']
        if not isinstance(drops, list) or not all(_num(t) and t >= 0 for t in drops):
            raise InputError('growth.drops must be a list of times in seconds')
        out['drops'] = sorted(round(float(t), 3) for t in drops)
    return critic


def merge(notes: Any, duration: Optional[float]) -> Dict[str, Any]:
    if not isinstance(notes, list) or not notes or not all(isinstance(n, dict) for n in notes):
        raise InputError("notes must be a list of each critic's note")
    out: Dict[str, Any] = {'core': None, 'verdicts': [], 'choices': [], 'drops': [], 'script': None,
                           'decoration': [], 'missing': [], 'whole': [], 'long': []}
    timed: List[Dict[str, Any]] = []
    seen = set()
    for i, note in enumerate(notes):
        critic = _note(note, i, out, timed, duration)
        if critic in seen:
            raise InputError(f'{critic} has two notes; give one each')
        seen.add(critic)

    # Only problems within NEAR of another critic's problem count as agreement.
    timed.sort(key=lambda p: (p['at'][0], p['at'][1]))
    agreed, single = [], []
    for p in timed:
        if any(p['critic'] != q['critic'] and p['at'][0] <= q['at'][1] + NEAR
               and q['at'][0] <= p['at'][1] + NEAR for q in timed):
            agreed.append(p)
        else:
            single.append(p)

    # Sweep the agreeing problems into stretches within NEAR of the stretch's end.
    groups: List[List[Dict[str, Any]]] = []
    end = -1.0
    for p in agreed:
        if groups and p['at'][0] <= end + NEAR:
            groups[-1].append(p)
            end = max(end, p['at'][1])
        else:
            groups.append([p])
            end = p['at'][1]
    agree = []
    for g in groups:
        critics = sorted({p['critic'] for p in g}, key=CRITICS.index)
        if len(critics) >= 2:
            agree.append({'at': [g[0]['at'][0], max(p['at'][1] for p in g)], 'critics': critics, 'problems': g})
        else:
            single.extend(g)
    fidelity = [p for p in timed if p.get('fidelity')] + [p for p in out['whole'] if p.get('fidelity')]
    out.update(agree=agree, single=single, fidelity=fidelity, absent=[c for c in CRITICS if c not in seen])
    out['verdicts'].sort(key=lambda v: CRITICS.index(v['critic']))

    parts = [f'{len(seen)} of {len(CRITICS)} critics', _plural(len(agree), 'moment') + ' two or more flag']
    if fidelity:
        parts.append(_plural(len(fidelity), 'difference') + ' from the source')
    if out['choices']:
        parts.append(_plural(len(out['choices']), 'choice') + ' for the user')
    if out['absent']:
        parts.append('no note from ' + ', '.join(NAMES[c] for c in out['absent']))
    if out['core'] is None:
        parts.append('no core sentence')
    out['summary'] = 'Critic panel: ' + '; '.join(parts)
    return out


def run(data: Any) -> Dict[str, Any]:
    """The script's whole job: the checked input in, the line it prints out."""
    if not isinstance(data, dict):
        raise InputError('the input must be one JSON object')
    if 'scene' not in data and 'notes' not in data:
        raise InputError("give a scene, the critics' notes, or both")
    out: Dict[str, Any] = {}
    duration = None
    if 'scene' in data:
        scene = _scene(data)
        per_sheet = _positive(data, 'per_sheet', PER_SHEET)
        if per_sheet != int(per_sheet):
            raise InputError('per_sheet must be a whole number')
        out['frames'] = frames(scene, _positive(data, 'every', EVERY), int(per_sheet))
        duration = _duration(scene)
    if 'notes' in data:
        out.update(merge(data['notes'], duration))
    return out


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
    sys.stdout.buffer.write((json.dumps(out, separators=(',', ':'), ensure_ascii=False) + '\n').encode('utf-8'))
    return 0


def fail(reason: str, code: int = 1) -> int:
    sys.stderr.write('critics.py: ' + ' '.join(reason.split()) + '\n')
    return code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
