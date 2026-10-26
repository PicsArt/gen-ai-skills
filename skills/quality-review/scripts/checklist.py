#!/usr/bin/env python3
"""
Turn the brief into yes-or-no questions, and grade a scene against them, one item at a time.

    python3 scripts/checklist.py input.json
    python3 scripts/checklist.py < input.json

The input is one JSON object:

    {"brief": {"message": "Making a film with AI is easy", "destination": ["reels"], "length": 20,
               "hook": "One chat. Six scenes.", "cta": "Try it in Picsart",
               "steps": ["Type the idea", "Pick a style"]},
     "scene": {...},
     "answers": {"result_first": {"yes": true, "evidence": "contact sheet, 0.0 s: the storyboard"}}}

- `brief`: what was agreed. Every field is optional, and an item is made only for a field that is
  there: `message`, one sentence; `destination`, the screen-recording-layouts skill's safe-zone profile ids;
  `length`, the target in seconds; `hook`, the hook's words (`""` for a hook with no words); `cta`, the call to action (leave it
  out for a video that loops); `steps`, each step's line, in order.
- `scene`, optional: the built scene (a builder's whole output is read too, and its `timeline`'s
  beats count as changes for `timing`). The items marked `scene` are graded from it; without it
  they stay open. Words count while they are on screen: inside nested scenes and track clips too,
  and only while their opacity is above 0.
- `measured`, optional: a captions layer's box by layer id, `{x, y, w, h}` in frame px, from
  `picsart_scene_query_layout`, as the screen-recording-layouts skill's `safe_zone.py` takes it. The renderer places
  captions, so without a box `words_safe` stays open.
- `changes`, optional: measured moments the picture changes inside footage, in scene seconds,
  as `timing.py` takes them. These count alongside a builder's timeline beats.
- `answers`, optional: your answer to each `look` item, by id: `yes`, true or false, and
  `evidence`, the frame's time or the tool's line you read it from, and for a no, the `fix`. An
  answer with no evidence does not count: the item stays open.

The items:

| id | by | the question |
|---|---|---|
| `length` | scene | is it within 15% of the target length? |
| `hook_on_time` | scene | are words on screen by 0.5 s? |
| `hook_words` | scene | do the first words on screen say the hook, in its order, from the start of a block? |
| `cta` | scene | is the call to action on screen in the last 3 s, in its order, from the start of a block? |
| `words_safe` | scene | is every word inside the destination's safe zone? |
| `timing` | scene | is every block of words readable in its time, with a change at least every 8 s (`timing.py`)? |
| `result_first` | look | does the first frame show a real moment (the result, or the problem it solves), not a login screen, an empty app or a title card? |
| `message` | look | would a viewer who saw only the hook and the ending say the message? |
| `step_<n>` | look | does step n end on its result, on screen? |
| `readable` | look | is every word readable at phone size? |

It prints one JSON line, `{ok, items, failed, open, summary}`. Each item has its `id`, the
`question`, `by`, its `status` (`yes`, `no` or `open`), its `evidence`, and for a no, the `fix`.
`ok` is true when every item is yes. `summary` is one line for the review: how many pass, and
which are no or open. Input it cannot read exits 1, with one line on stderr that says what is
wrong.

Python 3.9 or later, the standard library only, offline.
"""
from __future__ import annotations

import json
import math
import re
import sys
from typing import Any, Dict, List, Optional

from panel import word_blocks
from safe_zone import check as safe_check
from timing import InputError as UncheckedWords, lint as timing_lint, scene_duration

LENGTH_TOLERANCE = 0.15
HOOK_BY = 0.5
CTA_WITHIN = 3.0

USAGE = 'usage: checklist.py [input.json]; with no file, the input is read from stdin'


class InputError(ValueError):
    """Input the script cannot read, with the reason."""


def _num(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def words(s: str) -> List[str]:
    return re.findall(r"[^\W_]+(?:'[^\W_]+)?", s.lower())


def says(blocks: List[Dict[str, Any]], line: str) -> bool:
    """The line's words, in order, starting where a block starts: "Do not try it" does not say "Try it"."""
    want, seq, starts = words(line), [], []
    for b in blocks:
        if 'context' not in b or b.get('context_first'):
            starts.append(len(seq))
        seq += words(b['words'])
    return any(seq[i:i + len(want)] == want for i in starts)


def compile_items(brief: Dict[str, Any]) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []

    def add(id_: str, by: str, question: str) -> None:
        items.append({'id': id_, 'by': by, 'question': question})

    if brief.get('length') is not None:
        add('length', 'scene', f"Is it within 15% of {brief['length']:g} s?")
    # `hook: ""` is a hook with no words: the picture alone carries it, so nothing has to be read.
    if brief.get('hook'):
        add('hook_on_time', 'scene', f'Are words on screen by {HOOK_BY:g} s?')
        add('hook_words', 'scene', f"Do the first words on screen say \"{brief['hook']}\"?")
    if brief.get('cta'):
        add('cta', 'scene', f"Is \"{brief['cta']}\" on screen in the last {CTA_WITHIN:g} s?")
    if brief.get('destination'):
        add('words_safe', 'scene', 'Is every word inside the safe zone of ' + ', '.join(brief['destination']) + '?')
    add('timing', 'scene', 'Is every block of words readable in its time, with a change on screen at least every 8 s?')
    add('result_first', 'look', 'Does the first frame show a real moment (the result, or the problem it solves), not a login screen, an empty app or a title card?')
    if brief.get('message'):
        add('message', 'look', f"Would a viewer who saw only the hook and the ending say: \"{brief['message']}\"?")
    for n, step in enumerate(brief.get('steps') or [], 1):
        add(f'step_{n}', 'look', f'Does step {n}, "{step}", end on its result, on screen?')
    add('readable', 'look', 'Is every word readable at phone size?')
    return items


def grade_scene(item: Dict[str, Any], brief: Dict[str, Any], scene: Dict[str, Any], beats: List[float], measured: Dict[str, Any]) -> None:
    duration = scene_duration(scene) or 0.0

    def verdict(yes: Optional[bool], evidence: str, fix: Optional[str] = None) -> None:
        item['status'] = 'open' if yes is None else 'yes' if yes else 'no'
        item['evidence'] = evidence
        if not yes and fix:
            item['fix'] = fix

    i = item['id']
    if i == 'length':
        target = float(brief['length'])
        verdict(abs(duration - target) <= target * LENGTH_TOLERANCE, f'the scene is {duration:.1f} s',
                'cut or hold beats to land within 15% of the target, or agree a new length with the user')
    elif i == 'hook_on_time':
        visible = word_blocks(scene, ('text', 'captions'), completed=False)
        first = min((b['at'] for b in visible if (b['words'] or '').strip()), default=None)
        verdict(first is not None and first <= HOOK_BY, 'no words on screen' if first is None else f'the first words appear at {first:g} s',
                f'start the hook\'s words by {HOOK_BY:g} s')
    elif i == 'hook_words':
        early = [b for b in word_blocks(scene, ('text', 'captions'), completed=False) if b['at'] <= 1.0 and b['words']]
        said = ' '.join(b['words'] for b in early if b['words'])
        want = words(brief['hook'])
        opening, count = [], 0
        for b in early:
            if count >= len(want):
                break
            opening.append(b)
            count += len(words(b['words']))
        ready, remaining = True, len(want)
        for b in opening:
            tokens = list(re.finditer(r"[^\W_]+(?:'[^\W_]+)?", b['words']))
            take = min(remaining, len(tokens))
            if take:
                revealed = b.get('reveal_start', b['at']) + b.get('typing', 0) * tokens[take - 1].end() / max(1, len(b['words']))
                ready = ready and max(b['at'], revealed) <= 1.0 and revealed < b['end']
            remaining -= take
        evidence = f'the first words say "{said}"' if said else 'no words in the first second'
        if not ready:
            evidence += '; their reveal is not complete while visible in the first second'
        verdict(bool(early) and ready and words(said)[:len(want)] == want, evidence,
                'put the hook\'s words on screen in the first second')
    elif i == 'cta':
        late = [b for b in word_blocks(scene, ('text', 'captions')) if b['end'] > duration - CTA_WITHIN and b['at'] < duration]
        said = ' '.join(b['words'] for b in late if b['words'])
        verdict(says(late, brief['cta']), f'the last {CTA_WITHIN:g} s say "{said}"' if said else f'no words in the last {CTA_WITHIN:g} s',
                'put the call to action on the ending, over the payoff')
    elif i == 'words_safe':
        out = safe_check(scene, list(brief['destination']), measured)
        bad = [f['layer'] for f in out['findings']]
        evidence = 'safe_zone.py: ' + (', '.join(f"{f['layer']} {f['code']}" for f in out['findings']) or 'no findings')
        if out['unmeasured']:
            # The renderer places captions: no finding on them is no evidence either way.
            evidence += '; not measured: ' + ', '.join(out['unmeasured']) + ': give their boxes from picsart_scene_query_layout in `measured`'
        verdict(False if bad else None if out['unmeasured'] else True, evidence,
                '; '.join(f"{f['layer']}: {f['fix']}" for f in out['findings']))
    elif i == 'timing':
        found = timing_lint(scene, None, beats)['findings']
        where = [f.get('layer') or f"{f['from']:g}-{f['to']:g} s" for f in found]
        verdict(not found, 'timing.py: ' + (', '.join(f"{w} {f['code']}" for w, f in zip(where, found)) or 'no findings'),
                '; '.join(f"{w}: {f['fix']}" for w, f in zip(where, found)))


def grade(brief: Dict[str, Any], scene: Optional[Dict[str, Any]], answers: Dict[str, Any],
          beats: Optional[List[float]] = None, measured: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    items = compile_items(brief)
    for item in items:
        item['status'] = 'open'
        item['evidence'] = ''
        if item['by'] == 'scene':
            if scene is not None:
                try:
                    grade_scene(item, brief, scene, beats or [], measured or {})
                except UncheckedWords as err:
                    # Words the scripts cannot read (a text mask) need the frames to answer.
                    item['by'] = 'look'
                    item['status'] = 'open'
                    item['evidence'] = f'{err}: check it on the frames'
                    item.pop('fix', None)
            else:
                item['evidence'] = 'no scene given'
            if item['by'] == 'scene':
                continue
        a = answers.get(item['id'])
        if not isinstance(a, dict) or not isinstance(a.get('yes'), bool):
            item['evidence'] = item['evidence'] or 'not answered yet: look at the frames'
            continue
        evidence = str(a.get('evidence') or '').strip()
        if not evidence:
            item['evidence'] = 'answered with no evidence: name the frame\'s time or the tool\'s line'
            continue
        item['status'] = 'yes' if a['yes'] else 'no'
        item['evidence'] = evidence
        if not a['yes']:
            item['fix'] = str(a.get('fix') or 'fix what the evidence shows, then answer again')
    failed = [i['id'] for i in items if i['status'] == 'no']
    still = [i['id'] for i in items if i['status'] == 'open']
    passed = len(items) - len(failed) - len(still)
    summary = f'{passed} of {len(items)} checks pass'
    if failed:
        summary += '; no: ' + ', '.join(failed)
    if still:
        summary += '; open: ' + ', '.join(still)
    return {'ok': not failed and not still, 'items': items, 'failed': failed, 'open': still, 'summary': summary}


def run(data: Any) -> Dict[str, Any]:
    """The script's whole job: the checked input in, the line it prints out."""
    if not isinstance(data, dict):
        raise InputError('the input must be one JSON object')
    brief = data.get('brief')
    if not isinstance(brief, dict):
        raise InputError('brief must be an object: message, destination, length, hook, cta, steps')
    if brief.get('length') is not None and (not isinstance(brief['length'], (int, float)) or isinstance(brief['length'], bool) or brief['length'] <= 0):
        raise InputError('brief.length must be a positive number of seconds')
    dest = brief.get('destination')
    if isinstance(dest, str):
        brief = {**brief, 'destination': [dest]}
    elif dest is not None and (not isinstance(dest, list) or not all(isinstance(d, str) for d in dest)):
        raise InputError('brief.destination must be a profile id or a list of them')
    steps = brief.get('steps')
    if steps is not None and (not isinstance(steps, list) or not all(isinstance(s, str) for s in steps)):
        raise InputError('brief.steps must be a list of the steps\' lines')
    for key in ('message', 'hook', 'cta'):
        if brief.get(key) is not None and not isinstance(brief[key], str):
            raise InputError(f'brief.{key} must be words')
    scene, beats = data.get('scene'), []
    if isinstance(scene, dict) and 'scene' in scene and 'layers' not in scene:
        # A builder's timeline beats are changes on screen, as timing.py counts them.
        beats = [float(b['start']) for b in scene.get('timeline') or [] if isinstance(b, dict) and _num(b.get('start'))]
        scene = scene['scene']
    if scene is not None and (not isinstance(scene, dict) or not isinstance(scene.get('layers'), list)):
        raise InputError('scene must be the scene document, with its layers')
    changes = data.get('changes', [])
    if not isinstance(changes, list) or not all(_num(t) and math.isfinite(t) for t in changes):
        raise InputError('changes must be a list of finite seconds')
    beats += [float(t) for t in changes]
    answers = data.get('answers') or {}
    if not isinstance(answers, dict):
        raise InputError('answers must be an object of answers by item id')
    measured = data.get('measured') or {}
    if not isinstance(measured, dict):
        raise InputError('measured must be an object of boxes by layer id')
    for k, v in measured.items():
        if not isinstance(v, dict) or not all(_num(v.get(x)) for x in ('x', 'y', 'w', 'h')):
            raise InputError(f'measured.{k} must be a box {{x, y, w, h}} in frame px')
    return grade(brief, scene, answers, beats, {k: {x: float(v[x]) for x in ('x', 'y', 'w', 'h')} for k, v in measured.items()})


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
    sys.stderr.write('checklist.py: ' + ' '.join(reason.split()) + '\n')
    return code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
