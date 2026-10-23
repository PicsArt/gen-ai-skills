#!/usr/bin/env python3
"""
Review a short's script before anything is built or paid for: is it worth making, what is its why,
and where it can improve. Each item is yes, no or open, with the words it read.

    python3 scripts/script_review.py input.json
    python3 scripts/script_review.py < input.json

The input is one JSON object, the plan as written:

    {"kind": "how-to", "length": 20,
     "why": {"problem": "Re-framing a shot list card by card takes forever",
             "able": "change every shot with one line in chat",
             "proof": "after"},
     "takeaway": "Ask in chat: faces go close, the action stays wide",
     "beats": [
       {"id": "hook", "role": "hook", "words": ["I typed 4 words.", "Close-ups everywhere."],
        "dur": 2.4, "shows": "the revised list, the coffee shot now a close-up", "result": true},
       {"id": "ask", "role": "step", "words": ["One line in chat", "rewrites every shot"],
        "dur": 2.6, "shows": "the request typed in chat", "reason": "one line, not a card each"}],
     "cta": "Follow for more",
     "answers": {"insight": {"yes": false, "evidence": "no line says the jumps stay wide",
                             "fix": "after: 'Faces go close. / The jumps stay wide.'"}}}

- `kind`: `how-to` (the default), `explainer`, `tutorial` or `promo`. A promo sells rather than
  teaches, so it has no `takeaway` item.
- `length`, optional: the target in seconds.
- `why`: the viewer's `problem`, what they will be `able` to do after watching, and the `proof`,
  the id of the beat whose still shows the result.
- `takeaway`: the rule or tip a viewer would save, in the words a beat near the end shows.
- `beats`, in order. Each: `id`; `role`, `hook`, `step`, `payoff` or `ending`; `words`, a line or
  a list of lines; `dur`, seconds on screen; `shows`, what the still at that moment shows;
  `result`, true when that still shows the task's result; `reason`, why the beat is there.
- `cta`, optional: the call to action.
- `answers`, optional: your answer to each `look` item, as checklist.py takes them: `yes`,
  `evidence` (the line and the still you read it from) and, for a no, `fix`, the rewritten line.
  An answer with no evidence stays open.

The items:

| id | by | the question |
|---|---|---|
| `result_shown` | plan | does a beat's still show the result? |
| `why` | plan | are the problem, what the viewer can do after, and a result beat as proof all there? |
| `payoff` | plan | does a result beat come after the hook, so the ending shows what the hook promised? |
| `grounded` | plan | does every beat with words say what its still shows? |
| `step_reasons` | plan | does every step's words give a reason, not only the click? |
| `reads_in_time` | plan | is every beat on screen 0.3 s a word, and at least 1 s? |
| `lesson_time` | plan | do the steps and the payoff take at least half the length? |
| `length` | plan | is it within 15% of the target? |
| `takeaway` | plan | does a beat near the end, or the call to action, show the takeaway? |
| `insight` | look | does it teach the one thing a viewer would not guess, not only the clicks? |
| `promise` | look | is everything the hook and the lines promise on a beat's still? |

`lesson_time` and `length` are graded only when every beat has its `dur`, and `reads_in_time`
stays open while a beat with words has none.

It prints one JSON line, `{verdict, why, rescue, items, failed, open, summary}`. `verdict` is
`drop` when no beat shows the result, `open` while an item is open, `change` when an item says
no, and `make` when every item says yes. `why` is the one sentence, problem to proof, or null.
`rescue`, for a drop, says what footage would save it. Input it cannot read exits 1, with one line
on stderr that says what is wrong.

Python 3.9 or later, the standard library only, offline.
"""
from __future__ import annotations

import json
import re
import sys
from typing import Any, Dict, List, Optional

from timing import MIN_HOLD, PER_WORD

KINDS = ('how-to', 'explainer', 'tutorial', 'promo')
ROLES = ('hook', 'step', 'payoff', 'ending')
LENGTH_TOLERANCE = 0.15
LESSON_SHARE = 0.5
TAKEAWAY_MATCH = 0.6
CLICKS = re.compile(r"^(?:click|tap|select|press|choose|pick|type|drag|open|send|approve|submit|scroll|enter|hit|go to|navigate(?: to)?)\b")
PREFIX = re.compile(r"^(?:(?:\d+[.)]|(?:then|now|next|first|finally)[,:]?|in\s+[^,]+,)\s+)+")
REASON = re.compile(r"\b(?:so|to|because|keeps?|stays?|without|instead|only|never|no|until|which|saves?|or)\b")
# A control's label runs up to its noun ("Keep only this clip option"), and never
# through a clause: a reason opener or "to" plus a purpose verb ends it,
# even with a bare noun or gerund as its object. "Without formatting" and "or" can be label words.
CONTROL_NOUN = r"(?:button|option|menu|tab|link|icon|checkbox|field)\b"
LABEL_STOP = (r"(?:so|because|until|which|instead|since|it|that|these|those|them|they|you|we"
              r"|without\s+\w+ing\s+(?!" + CONTROL_NOUN + r"))\b")
PURPOSE_VERB = r"(?:keep|preserve|retain|avoid|prevent|continue|protect|reduce|improve|link)\b"
TARGET = re.compile(r"\s*(?:(?:the|a|an|your)\s+)?(?!(?:so|to|because|until|which|without|instead|or)\b)"
                    r"(?:(?:(?!\b" + LABEL_STOP + r"|\bwhen\b"
                    r"|\bto\s+(?:" + PURPOSE_VERB + r"|\w+\s+(?:your|our|its|the|a|an|this|that|it|them|every|all)\b))[^,.;!?])+?"
                    r"\b" + CONTROL_NOUN + r"|[^\W_]+(?:['’][^\W_]+)?)")
TITLE_TARGET = re.compile(r"\s*(?:(?:the|a|an|your)\s+)?[A-Z][a-z]+"
                          r"(?:\s+(?!(?i:" + LABEL_STOP + r"))[A-Z][a-z]+)+\b")
# A label runs through a reason word to its noun only as a name is written: after an article
# ("Tap the Save to your device button"), capitalized on ("Tap Save to Drive button"), or on
# to its noun with no place on the way ("Tap Add to cart button", "Select Keep only the
# selected shots option", "Tap Paste without formatting option at the top"). A clause runs
# to a place before the noun: "to" and a verb with its object ("Tap Export to save time in the
# next tab", "Tap Export to share with clients from the menu"), or "without" and a word no
# label uses there ("Tap Save without any loss in the tab"). The target is then the name alone
# and the clause is the reason. Only these: "to cloud drive in the next tab" and "to save time
# in the next tab" differ only in the verb, and a label can go on with "only", "or" or
# "without an account" before its place ("Tap Continue without an account in the next tab").
NAME_TARGET = re.compile(r"\s*[^\W_]+(?:['’][^\W_]+)?")
PLACE = r"(?:in|on|at|from|of|for|with|into|onto|by|near|under|over|inside|below|above|beside)\b"
DETERMINER = r"(?:your|our|its|the|a|an|this|that|these|those|my|their)\b"
CLAUSE_VERB = (r"(?:accept|access|add|adjust|align|allow|animate|annotate|apply|approve|archive|arrange|attach|"
               r"avoid|back|blur|boost|bring|browse|build|bump|calculate|cancel|capture|change|check|choose|clean|"
               r"clear|clip|close|collect|color|combine|comment|compare|compress|confirm|connect|continue|control|"
               r"convert|copy|correct|count|create|crop|cut|darken|decide|delete|deliver|describe|design|detect|"
               r"disable|discard|display|download|drag|draw|drop|duplicate|edit|email|enable|enhance|enter|erase|"
               r"expand|explore|export|extend|extract|fade|fetch|fill|filter|find|finish|fit|fix|flag|flip|follow|"
               r"format|frame|free|gather|generate|get|give|grab|group|guide|handle|hear|help|hide|highlight|hold|"
               r"import|improve|include|increase|insert|inspect|install|invite|join|jump|keep|label|launch|layer|"
               r"learn|lighten|limit|link|list|load|locate|lock|log|loop|lower|make|manage|mark|match|measure|"
               r"merge|mix|move|mute|name|narrate|navigate|note|notify|open|order|organize|outline|paste|pause|"
               r"pick|pin|place|plan|play|polish|post|prepare|present|preserve|prevent|preview|print|process|"
               r"produce|protect|publish|pull|push|queue|reach|read|rearrange|receive|record|recover|redo|reduce|"
               r"refine|reframe|refresh|remove|rename|render|reorder|repeat|replace|reply|request|reset|resize|"
               r"restore|resume|retain|retouch|return|reuse|review|revise|rewind|rotate|run|sample|save|scale|scan|"
               r"schedule|score|scroll|search|see|select|send|set|share|sharpen|show|shrink|sign|skip|slow|smooth|"
               r"snap|sort|speed|split|stabilize|start|stop|store|straighten|stream|submit|subscribe|swap|switch|"
               r"sync|tag|take|test|tidy|time|tint|toggle|track|transcribe|transfer|translate|trim|try|tune|turn|"
               r"type|undo|unlock|update|upload|use|verify|view|watch|wrap|write|zoom)\b")
CLAUSE_IN_LABEL = re.compile(r"\b(?:to\s+" + CLAUSE_VERB + r"|without\s+(?:any|extra|further|more|much|another))\s+(?:"
                             + PLACE + r"\s+(?!" + DETERMINER + r")"
                             r"|(?!" + PLACE + r"|" + CONTROL_NOUN + r"))[a-z][\w'’]*\b"
                             r"(?:\s+(?!" + CONTROL_NOUN + r")[\w'’]+)*?\s+" + PLACE)
QUOTED = re.compile(r'\s*(?:(?:the|a|an|your)\s+)?(?:"[^"]*"|“[^”]*”|‘[^’]*’|\'[^\']*\')')
NEGATION = {'not', 'no', 'never', 'nothing', 'none', 'without', 'cannot'}
GENERIC_CTA = re.compile(r"^(?:follow|like|subscribe|share|comment|save)\b")
STOP = {'a', 'an', 'the', 'it', 'its', 'is', 'are', 'and', 'or', 'of', 'to', 'in', 'on', 'for', 'with', 'you', 'your'}

USAGE = 'usage: script_review.py [input.json]; with no file, the input is read from stdin'


class InputError(ValueError):
    """Input the script cannot read, with the reason."""


def words_of(s: str) -> List[str]:
    return re.findall(r"[^\W_]+(?:['’][^\W_]+)?", s.lower())


def content(s: str) -> List[str]:
    return [w for w in words_of(s) if w not in STOP]


def negated(s: str) -> bool:
    """True when the words say not, never or no, so a matching line may mean the opposite."""
    return any(w in NEGATION or w.endswith(("n't", "n’t")) for w in words_of(s))


def line(beat: Dict[str, Any]) -> str:
    return ' / '.join(beat['words'])


def item(id_: str, by: str, question: str) -> Dict[str, Any]:
    return {'id': id_, 'by': by, 'question': question, 'status': 'open', 'evidence': ''}


def settle(it: Dict[str, Any], yes: bool, evidence: str, fix: str = '') -> None:
    it['status'] = 'yes' if yes else 'no'
    it['evidence'] = evidence
    if not yes and fix:
        it['fix'] = fix


def review(plan: Dict[str, Any], answers: Dict[str, Any]) -> Dict[str, Any]:
    beats: List[Dict[str, Any]] = plan['beats']
    kind = plan.get('kind') or 'how-to'
    by_id = {b['id']: b for b in beats}
    results = [b['id'] for b in beats if b.get('result') is True and (b.get('shows') or '').strip()]
    last = beats[-1]
    items: List[Dict[str, Any]] = []

    it = item('result_shown', 'plan', "Does a beat's still show the result?")
    settle(it, bool(results),
           'the result is on ' + ', '.join(results) if results else
           f'no beat shows the result; the last still shows "{(last.get("shows") or "nothing named").strip()}"',
           'record the result appearing on screen and add it as a beat, or drop the video')
    items.append(it)

    why = plan.get('why') or {}
    it = item('why', 'plan', 'Are the problem, what the viewer can do after, and a result beat as proof all there?')
    proof: Optional[Dict[str, Any]] = by_id.get(str(why.get('proof') or ''))
    missing = [k for k in ('problem', 'able') if not str(why.get(k) or '').strip()]
    if proof is None:
        missing.append('proof, the id of a result beat')
    elif proof['id'] not in results:
        missing.append(f'proof: "{proof["id"]}" does not show the result')
    settle(it, not missing, 'missing ' + '; '.join(missing) if missing else 'problem, able and proof are there',
           "write the why: the viewer's problem, what they can do after watching, and the beat that shows it")
    items.append(it)

    it = item('payoff', 'plan', 'Does a result beat come after the hook, so the ending shows what the hook promised?')
    after = [i for i in results if i != beats[0]['id']]
    settle(it, bool(after), 'the result again on ' + ', '.join(after) if after else 'no result after the hook',
           "end on the result, held: the beat that answers the hook's question")
    items.append(it)

    it = item('grounded', 'plan', 'Does every beat with words say what its still shows?')
    bare = [b['id'] for b in beats if b['words'] and not (b.get('shows') or '').strip()]
    settle(it, not bare, 'no still named for ' + ', '.join(bare) if bare else 'every beat names its still',
           'read the still at each of these beats and say what it shows, or cut the beat')
    items.append(it)

    it = item('step_reasons', 'plan', "Does every step's words give a reason, not only the click?")
    clicks = []
    for b in beats:
        if b['role'] != 'step' or not b['words']:
            continue
        original = ' '.join(b['words'])
        text = original.lower()
        text = re.sub(r"^[^a-z0-9]+", '', text)
        text = PREFIX.sub('', text)
        click = CLICKS.match(text)
        # The reason is in what follows the click and its target: "Tap Save" names a button, not a why.
        rest = text[click.end():] if click else ''
        target = QUOTED.match(rest) or TARGET.match(rest)
        if target and not QUOTED.match(rest) and not re.match(r"\s*(?:the|a|an|your)\b", rest) \
                and CLAUSE_IN_LABEL.search(original[len(original) - len(rest):][:target.end()]):
            target = NAME_TARGET.match(rest)
        title = TITLE_TARGET.match(original[len(original) - len(rest):]) if click else None
        if title and (target is None or title.end() > target.end()):
            target = title
        if click and not REASON.search(rest[target.end():] if target else rest):
            clicks.append(b)
    settle(it, not clicks, '; '.join(f'{b["id"]}: "{line(b)}"' for b in clicks) if clicks else 'every step says why',
           '; '.join(f'{b["id"]}: say what the click gets done' + (f', as the plan says: {b["reason"]}' if b.get('reason') else '') for b in clicks))
    items.append(it)

    it = item('reads_in_time', 'plan', f'Is every beat on screen {PER_WORD:g} s a word, and at least {MIN_HOLD:g} s?')
    short, untimed = [], []
    for b in beats:
        if not b['words']:
            continue
        if b.get('dur') is None:
            untimed.append(b['id'])
            continue
        need = max(MIN_HOLD, PER_WORD * len(words_of(' '.join(b['words']))))
        if b['dur'] < need:
            short.append(f'{b["id"]}: {b["dur"]:g} s for {need:.1f} s of words')
    if untimed:
        it['evidence'] = ('no dur for ' + ', '.join(untimed) + ': give each beat with words its seconds on screen'
                          + ('; already short: ' + '; '.join(short) if short else ''))
    elif short:
        settle(it, False, '; '.join(short), 'hold each of these longer, or cut its words')
    else:
        settle(it, True, 'every beat reads in time')
    items.append(it)

    if all(b.get('dur') is not None for b in beats):
        total = sum(b['dur'] for b in beats)
        lesson = sum(b['dur'] for b in beats if b['role'] in ('step', 'payoff'))
        it = item('lesson_time', 'plan', f'Do the steps and the payoff take at least {LESSON_SHARE:.0%} of the length?')
        settle(it, total > 0 and lesson >= LESSON_SHARE * total, f'the lesson takes {lesson:g} s of {total:g} s',
               'give the lesson more time: one more step with its reason, or a shorter hook and ending')
        items.append(it)
        if plan.get('length') is not None:
            target = float(plan['length'])
            it = item('length', 'plan', f'Is it within {LENGTH_TOLERANCE:.0%} of {target:g} s?')
            settle(it, abs(total - target) <= target * LENGTH_TOLERANCE + 1e-9, f'the beats add up to {total:g} s',
                   'add or cut a step so the length fits the lesson, or agree a new length')
            items.append(it)

    if kind != 'promo':
        it = item('takeaway', 'plan', 'Does a beat near the end, or the call to action, show the takeaway?')
        take = str(plan.get('takeaway') or '').strip()
        cta = str(plan.get('cta') or '').strip()
        if not take:
            settle(it, False, 'no takeaway; ' + (f'the ending is "{cta}"' if cta else 'there is no ending'),
                   'write the rule or tip a viewer would save, and put it on the payoff or the ending')
        else:
            want = set(content(take))
            near = [line(b) for b in beats[-2:] if b['words']] + ([cta] if cta else [])
            hits = [t for t in near if want and len(want & set(content(t))) >= TAKEAWAY_MATCH * len(want)]
            displayed = [(t, t) for t in near] + [(t, line(b)) for b in beats[-2:] for t in b['words']]
            matches = [(t, context) for t, context in displayed if words_of(t) == words_of(take)]
            exact = next((m for m in matches if negated(m[1]) == negated(take)), matches[0] if matches else None)
            hit = (exact[0] if negated(exact[1]) == negated(take) else exact[1]) if exact else (hits[0] if hits else None)
            before = f', before "{cta}"' if cta and GENERIC_CTA.match(cta.lower()) else ''
            if hit is not None and negated(hit) != negated(take):
                it['evidence'] = f'"{hit}" shares the words of "{take}" but not its sense: one says not or never. Read it'
            elif hit is not None and exact is None:
                it['evidence'] = f'"{hit}" shares words with "{take}"; read it to verify the intended instruction'
            else:
                settle(it, hit is not None, f'shown as "{hit}"' if hit else f'"{take}" is in none of the last lines: ' + '; '.join(f'"{t}"' for t in near),
                       f'put "{take}" on the payoff or the ending{before}')
        items.append(it)

    for id_, question in (('insight', 'Does it teach the one thing a viewer would not guess, not only the clicks?'),
                          ('promise', "Is everything the hook and the lines promise on a beat's still?")):
        it = item(id_, 'look', question)
        a = answers.get(id_)
        if not isinstance(a, dict) or not isinstance(a.get('yes'), bool):
            it['evidence'] = 'not answered yet: quote the line and the still'
        elif not str(a.get('evidence') or '').strip():
            it['evidence'] = 'answered with no evidence: quote the line and the still'
        else:
            settle(it, a['yes'], str(a['evidence']).strip(), str(a.get('fix') or 'rewrite the line, then answer again'))
        items.append(it)

    failed = [i['id'] for i in items if i['status'] == 'no']
    still = [i['id'] for i in items if i['status'] == 'open']
    if 'result_shown' in failed:
        verdict = 'drop'
    elif still:
        verdict = 'open'
    elif failed:
        verdict = 'change'
    else:
        verdict = 'make'
    sentence = None
    if not missing and proof is not None:
        parts = (why['problem'], why['able'], proof['shows'])
        sentence = ' → '.join(str(p).strip().rstrip('.') for p in parts)
    rescue = None
    if verdict == 'drop':
        end = f', after "{last["shows"].strip()}"' if (last.get('shows') or '').strip() else ''
        rescue = f'footage of the result appearing on screen{end}; without it, teach the request itself, or drop the video'
    passed = len(items) - len(failed) - len(still)
    summary = f'{verdict}: {passed} of {len(items)} pass'
    if failed:
        summary += '; no: ' + ', '.join(failed)
    if still:
        summary += '; open: ' + ', '.join(still)
    return {'verdict': verdict, 'why': sentence, 'rescue': rescue, 'items': items, 'failed': failed, 'open': still, 'summary': summary}


def beat_of(raw: Any, n: int) -> Dict[str, Any]:
    if not isinstance(raw, dict):
        raise InputError(f'beats[{n}] must be an object')
    b = dict(raw)
    if not isinstance(b.get('id'), str) or not b['id']:
        b['id'] = f'beat_{n + 1}'
    w = b.get('words')
    if w is None:
        w = []
    elif isinstance(w, str):
        w = [w]
    if not isinstance(w, list) or not all(isinstance(x, str) for x in w):
        raise InputError(f'beats[{n}].words must be a line or a list of lines')
    b['words'] = [x for x in w if x.strip()]
    if b.get('role') is None:
        b['role'] = 'hook' if n == 0 else 'step'
    if b['role'] not in ROLES:
        raise InputError(f'beats[{n}].role must be one of ' + ', '.join(ROLES))
    d = b.get('dur')
    if d is not None and (not isinstance(d, (int, float)) or isinstance(d, bool) or d < 0):
        raise InputError(f'beats[{n}].dur must be seconds')
    for key in ('shows', 'reason'):
        if b.get(key) is not None and not isinstance(b[key], str):
            raise InputError(f'beats[{n}].{key} must be words')
    return b


def run(data: Any) -> Dict[str, Any]:
    """The script's whole job: the checked input in, the line it prints out."""
    if not isinstance(data, dict):
        raise InputError('the input must be one JSON object')
    kind = data.get('kind')
    if kind is not None and kind not in KINDS:
        raise InputError('kind must be one of ' + ', '.join(KINDS))
    beats = data.get('beats')
    if not isinstance(beats, list) or not beats:
        raise InputError("beats must be the plan's beats, in order")
    length = data.get('length')
    if length is not None and (not isinstance(length, (int, float)) or isinstance(length, bool) or length <= 0):
        raise InputError('length must be a positive number of seconds')
    if data.get('why') is not None and not isinstance(data['why'], dict):
        raise InputError('why must be an object: problem, able, proof')
    for key in ('takeaway', 'cta'):
        if data.get(key) is not None and not isinstance(data[key], str):
            raise InputError(f'{key} must be words')
    answers = data.get('answers') or {}
    if not isinstance(answers, dict):
        raise InputError('answers must be an object of answers by item id')
    checked = [beat_of(b, n) for n, b in enumerate(beats)]
    seen = set()
    for n, b in enumerate(checked):
        if b['id'] in seen:
            raise InputError(f'beats[{n}].id "{b["id"]}" is used by an earlier beat; each beat needs its own id')
        seen.add(b['id'])
    return review({**data, 'beats': checked}, answers)


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
    sys.stdout.buffer.write((json.dumps(out, ensure_ascii=False, separators=(',', ':')) + '\n').encode('utf-8'))
    return 0


def fail(reason: str, code: int = 1) -> int:
    sys.stderr.write('script_review.py: ' + ' '.join(reason.split()) + '\n')
    return code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
