#!/usr/bin/env python3
"""
The viewer panel's arithmetic: which frames the viewers see, and whether their answers pass.

    python3 scripts/panel.py input.json
    python3 scripts/panel.py < input.json

The input is one JSON object with one or more of:

    {"scene": {...},
     "hook": [{"viewer": "teen", "stop": "yes", "why": "...", "thinks": "...", "ad": "no",
               "expects": "...", "matches": true}],
     "draft": [{"viewer": "teen", "learned": "...", "learned_matches": true, "could_do": "yes",
                "keep": "send"}]}

- `scene`: the built scene (a builder's whole output is read too, and its `timeline` sets the
  draft's frames). Out comes `frames`: `hook.times`, the hook's frames at 0, 0.5, 1 and 2 s;
  `hook.words`, every block of words on screen in those 2 s, with when it starts; `draft.times`,
  one frame in the middle of each beat (or every 2.5 s with no timeline), at most 12; and
  `draft.script`, every block of words in the order it appears. A block is on screen while its
  layer is and its opacity is above 0, nested scenes' and track clips' blocks included.
- `hook`: each viewer's answers about the first 2 s. `stop` is `yes`, `maybe` or `no`; `ad` is
  `no`, `a bit` or `yes`; `matches` is your reading, true when what they think the video is and
  what they expect next is what the payoff gives.
- `draft`: each viewer's answers about the whole draft. `learned_matches` is your reading, true
  when what they learned is the message; `could_do` is `yes`, `maybe` or `no`; `keep` is `save`,
  `send`, `both` or `neither`.

The bar, for a panel of n viewers (at least 3), "most" meaning at least two in three:

| id | passes when |
|---|---|
| `stop` | most would stop scrolling |
| `ad` | no one says it is an ad, and at most one in three says "a bit" |
| `promise` | most read the promise the payoff keeps |
| `message` | most learned the message |
| `could_do` | most could do it now (a promo: would try it) |
| `keep` | most would save or send it |

It prints one JSON line: `frames` when there was a scene, and for each panel graded, `{ok,
failed}`, each failure with its `id`, the viewers' own words that explain it (`why`) and the
`fix`; then `ok` and `summary`, one line for the review. Input it cannot read exits 1, with one
line on stderr that says what is wrong.

Python 3.9 or later, the standard library only, offline.
"""
from __future__ import annotations

import json
import math
import sys
from typing import Any, Dict, List, Optional, Tuple

from timing import placed

HOOK_TIMES = (0.0, 0.5, 1.0, 2.0)
HOOK_SPAN = 2.0
DRAFT_EVERY = 2.5
DRAFT_MAX = 12

STOP = ('yes', 'maybe', 'no')
AD = ('no', 'a bit', 'yes')
COULD = ('yes', 'maybe', 'no')
KEEP = ('save', 'send', 'both', 'neither')

FIX = {
    'stop': 'open sooner on the moment or the problem the viewer already feels; cut whatever comes before it',
    'ad': 'take out the ad tells the viewers named (story-loops, Ad tells): say it the way a creator would, and show the moment, not the product',
    'promise': 'make the picture, the words and the payoff one promise: change the hook to what the payoff shows, or the payoff to what the hook promised',
    'message': 'make the payoff show the message itself, and say why it matters in the task beat',
    'could_do': 'show the one thing to do as plainly as the recording allows: the step a viewer would miss, held longer',
    'keep': 'give the viewer something worth keeping: the exact words to type, the setting, the before and after',
}

USAGE = 'usage: panel.py [input.json]; with no file, the input is read from stdin'


class InputError(ValueError):
    """Input the script cannot read, with the reason."""


def _num(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _text(content: Dict[str, Any]) -> str:
    t = content.get('text')
    s = ' '.join(t) if isinstance(t, list) else (t if isinstance(t, str) else '')
    return ' '.join(s.split())


def _duration(scene: Dict[str, Any]) -> Optional[float]:
    d = (scene.get('composition') or {}).get('duration')
    return float(d) if _num(d) and d > 0 else None


def _last(scene: Dict[str, Any], duration: float) -> float:
    """The last frame's time: a sample at the very end of the scene is past it."""
    fps = (scene.get('composition') or {}).get('fps')
    step = 1.0 / float(fps) if _num(fps) and fps > 0 else 1 / 30
    return round(max(0.0, duration - step), 3)


def shown(layer: Dict[str, Any], start: float) -> List[Tuple[float, float]]:
    """
    The spans a layer is on screen, in scene seconds: its lifetime less the stretches its opacity
    holds at 0. Opacity keyframes are layer-relative unless the track says otherwise; a ramp up from
    0 shows from its first key, and a `step` from 0 only from its second.
    """
    end = start + float(layer['duration']) if _num(layer.get('duration')) else math.inf
    track = (layer.get('animations') or {}).get('opacity') or {}
    keys = [k for k in track.get('keyframes') or [] if isinstance(k, dict) and _num(k.get('time')) and _num(k.get('value'))]
    if not keys:
        still = (layer.get('transform') or {}).get('opacity')
        return [(start, end)] if not _num(still) or still > 0 else []
    base = 0.0 if track.get('timeMode', layer.get('timeMode', 'composition')) == 'composition' else start
    pts = [(base + float(k['time']), float(k['value']), k.get('easing')) for k in keys]
    spans = [(-math.inf, pts[0][0])] if pts[0][1] > 0 else []
    for (t0, v0, easing), (t1, v1, _) in zip(pts, pts[1:]):
        if v0 > 0 or (v1 > 0 and easing != 'step'):
            spans.append((t0, t1))
    if pts[-1][1] > 0:
        spans.append((pts[-1][0], math.inf))
    out: List[Tuple[float, float]] = []
    for a, b in spans:
        a, b = max(a, start), min(b, end)
        if b <= a + 1e-6:
            continue
        if out and a <= out[-1][1] + 1e-6:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out


def word_blocks(scene: Dict[str, Any], kinds: Tuple[str, ...] = ('text',)) -> List[Dict[str, Any]]:
    """
    Every block of words while it is on screen, in the order it appears: nested scenes' and track
    clips' included, on the outer scene's clock, and once per span its opacity shows it.
    """
    out = []
    for layer, start in placed(scene):
        content = layer.get('content') or {}
        if content.get('kind') not in kinds:
            continue
        for at, end in shown(layer, start):
            out.append({'at': round(at, 3), 'end': end, 'layer': str(layer.get('id', '')), 'kind': content['kind'], 'words': _text(content)})
    return sorted(out, key=lambda b: b['at'])


def _blocks(scene: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [b for b in word_blocks(scene) if b['words']]


def frames(scene: Dict[str, Any], timeline: List[Any]) -> Dict[str, Any]:
    duration = _duration(scene)
    last = _last(scene, duration) if duration else None
    hook_times = sorted({min(t, last) if last is not None else t for t in HOOK_TIMES})
    blocks = _blocks(scene)
    hook_words = [{'at': b['at'], 'layer': b['layer'], 'words': b['words']} for b in blocks if b['at'] < HOOK_SPAN and b['end'] > 0]

    beats = [b for b in timeline if isinstance(b, dict) and _num(b.get('start')) and _num(b.get('end')) and b['end'] > b['start']]
    if beats:
        times = [round((float(b['start']) + float(b['end'])) / 2, 3) for b in beats]
    elif duration:
        times = [round(DRAFT_EVERY * (i + 0.5), 3) for i in range(int(duration // DRAFT_EVERY) + 1) if DRAFT_EVERY * (i + 0.5) < duration]
    else:
        times = []
    if len(times) > DRAFT_MAX:
        # Keep the first and the last; spread the rest evenly.
        times = [times[round(i * (len(times) - 1) / (DRAFT_MAX - 1))] for i in range(DRAFT_MAX)]
    if last is not None:
        times = [min(t, last) for t in times]
    script, seen = [], set()
    for b in blocks:
        if b['words'] not in seen:
            seen.add(b['words'])
            script.append({'at': b['at'], 'words': b['words']})
    return {'hook': {'times': hook_times, 'words': hook_words},
            'draft': {'times': times, 'script': script}}


def _most(n: int) -> int:
    return math.ceil(2 * n / 3)


def _choice(answer: Dict[str, Any], key: str, allowed: tuple, where: str) -> str:
    v = answer.get(key)
    v = v.strip().lower() if isinstance(v, str) else v
    if v not in allowed:
        raise InputError(f'{where}.{key} must be one of ' + ', '.join(f'"{a}"' for a in allowed) + f', not {json.dumps(v)}')
    return v


def _flag(answer: Dict[str, Any], key: str, where: str) -> bool:
    v = answer.get(key)
    if not isinstance(v, bool):
        raise InputError(f'{where}.{key} must be true or false: your reading of the answer')
    return v


def _panel(answers: Any, name: str) -> List[Dict[str, Any]]:
    if not isinstance(answers, list) or not all(isinstance(a, dict) for a in answers):
        raise InputError(f"{name} must be a list of each viewer's answers")
    if len(answers) < 3:
        raise InputError(f'{name} has {len(answers)} viewers; the panel needs at least 3')
    return answers


def _who(answers: List[Dict[str, Any]], i: int) -> str:
    v = answers[i].get('viewer')
    return v if isinstance(v, str) and v else f'viewer {i + 1}'


def _why(answers: List[Dict[str, Any]], idx: List[int], key: str) -> List[str]:
    out = []
    for i in idx:
        said = answers[i].get(key)
        out.append(f'{_who(answers, i)}: {said}' if isinstance(said, str) and said.strip() else _who(answers, i))
    return out


def grade_hook(answers: Any) -> Dict[str, Any]:
    answers = _panel(answers, 'hook')
    n = len(answers)
    stop, ad, match = [], [], []
    for i, a in enumerate(answers):
        where = f'hook[{i}]'
        stop.append(_choice(a, 'stop', STOP, where))
        ad.append(_choice(a, 'ad', AD, where))
        match.append(_flag(a, 'matches', where))
    failed = []
    if sum(s == 'yes' for s in stop) < _most(n):
        failed.append({'id': 'stop', 'why': _why(answers, [i for i, s in enumerate(stop) if s != 'yes'], 'why'), 'fix': FIX['stop']})
    if 'yes' in ad or sum(x == 'a bit' for x in ad) > n // 3:
        failed.append({'id': 'ad', 'why': _why(answers, [i for i, x in enumerate(ad) if x != 'no'], 'why'), 'fix': FIX['ad']})
    if sum(match) < _most(n):
        failed.append({'id': 'promise', 'why': _why(answers, [i for i, m in enumerate(match) if not m], 'thinks'), 'fix': FIX['promise']})
    return {'ok': not failed, 'failed': failed}


def grade_draft(answers: Any) -> Dict[str, Any]:
    answers = _panel(answers, 'draft')
    n = len(answers)
    learned, could, keep = [], [], []
    for i, a in enumerate(answers):
        where = f'draft[{i}]'
        learned.append(_flag(a, 'learned_matches', where))
        could.append(_choice(a, 'could_do', COULD, where))
        keep.append(_choice(a, 'keep', KEEP, where))
    failed = []
    if sum(learned) < _most(n):
        failed.append({'id': 'message', 'why': _why(answers, [i for i, m in enumerate(learned) if not m], 'learned'), 'fix': FIX['message']})
    if sum(c == 'yes' for c in could) < _most(n):
        failed.append({'id': 'could_do', 'why': _why(answers, [i for i, c in enumerate(could) if c != 'yes'], 'learned'), 'fix': FIX['could_do']})
    if sum(k != 'neither' for k in keep) < _most(n):
        failed.append({'id': 'keep', 'why': _why(answers, [i for i, k in enumerate(keep) if k == 'neither'], 'learned'), 'fix': FIX['keep']})
    return {'ok': not failed, 'failed': failed}


def run(data: Any) -> Dict[str, Any]:
    """The script's whole job: the checked input in, the line it prints out."""
    if not isinstance(data, dict):
        raise InputError('the input must be one JSON object')
    if not any(k in data for k in ('scene', 'hook', 'draft')):
        raise InputError("give a scene, the hook panel's answers, the draft panel's answers, or several")
    out: Dict[str, Any] = {}
    if 'scene' in data:
        scene, timeline = data['scene'], []
        if isinstance(scene, dict) and 'scene' in scene and 'layers' not in scene:
            timeline = scene.get('timeline') or []
            scene = scene['scene']
        if not isinstance(scene, dict) or not isinstance(scene.get('layers'), list):
            raise InputError('scene must be the scene document, with its layers')
        out['frames'] = frames(scene, timeline if isinstance(timeline, list) else [])
    parts = []
    for name, grade in (('hook', grade_hook), ('draft', grade_draft)):
        if name in data:
            out[name] = grade(data[name])
            ids = [f['id'] for f in out[name]['failed']]
            parts.append(f'{name} ' + ('passes' if not ids else 'fails on ' + ', '.join(ids)))
    if parts:
        out['ok'] = all(out[name]['ok'] for name in ('hook', 'draft') if name in out)
        out['summary'] = 'Viewer panel (simulated): ' + '; '.join(parts)
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
    sys.stderr.write('panel.py: ' + ' '.join(reason.split()) + '\n')
    return code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
