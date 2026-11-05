"""What a new plan changes in meaning, against the last version the user saw and the keepers ledger.

Usage:
  meaning_diff.py <shown plan> <new plan> [--record <record>] [--lines <map.json>]

A plan is the edit-pipeline's ({"rows": [{"phrase", "job", "shot"}]}), a plan of shots per line
({"shots": {"V4": [{"clip", "in", "job"}]}}), or a cut list CSV (proxy filename, in (s), out (s),
voiceover line). --lines maps line ids to their words ({"V4": "With precision."}), so plans that
name lines and cut lists that quote them compare. A shot is known by its clip number: FX3_2396.mp4,
2396 and 2396g are one clip; a name with spaces (Interview 01.mp4, even with a range after it) is
kept whole. One clip used at two ranges is two shots, matched by where each starts, else in order.
A keeper that names a range (or an `in`) is held only by a use starting within a second of it.

Prints JSON: every change, one line per change for the message to the user, and what blocks.
Blocking: a keeper dropped, a shot's meaning changed or left unsaid (a shot swapped, added, restored or
kept with no job), or a job rewritten for the same
shot, unless the record holds the user's approval of exactly that: "scope": "meaning:<phrase>" with
the new `job`, or "scope": "keeper:<phrase>" naming the keeper's `shot` or `what` (a phrase by its
line id or its words). A moment keeper counts wherever it sits in the plan. A carried-over entry
({"job": "2391 carries over"}) holds that clip on its line, with the job of its last use. A cut list has no jobs, so against one
the meaning is not compared, and its lines say so.
Exit 0 when nothing blocks, 1 when something does, 2 when a file cannot be read.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys

BLOCKING = {'KEEPER_DROPPED', 'KEEPER_STILL_DROPPED', 'MEANING_CHANGED', 'MEANING_UNKNOWN', 'JOB_REWRITTEN'}


MEDIA = ('.mp4', '.mov', '.m4v', '.mxf', '.avi', '.mkv', '.webm', '.mts', '.wav', '.mp3', '.m4a', '.jpg', '.jpeg', '.png')
RANGE = re.compile(r'^(.+?)\s+(\d+(?:\.\d+)?)\s*-\s*\d+(?:\.\d+)?$')


def clip_id(value) -> str:
    """The clip's name: 'FX3_2396.mp4', '2396 37.5-39.0' and '2396g' are all '2396'.

    A name with spaces ('Interview 01.mp4', 'Interview 01.mp4 1-3') is kept whole: only a trailing
    range is split off."""
    text = str(value or '').strip()
    ranged = RANGE.match(text)
    if ranged:
        text = ranged.group(1)
    name = os.path.basename(text)
    if name.lower().endswith(MEDIA):
        name = os.path.splitext(name)[0]
    if re.search(r'\s', name):
        return name
    m = re.search(r'(\d+)[a-z]*$', name, re.I)
    return m.group(1) if m else name


HELD = 1.0  # seconds: a use starting this close to a keeper's start is the keeper, trimmed


def start_of(entry: dict, name: str) -> float | None:
    """Where a shot starts in its clip: its `in`, else the 37.5 of '2396 37.5-39.0'; None when the
    plan names only the clip."""
    value = entry.get('in')
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    if value not in (None, ''):
        try:
            return float(str(value).strip())
        except ValueError:
            pass
    ranged = RANGE.match(str(entry.get(name) or '').strip())
    return float(ranged.group(2)) if ranged else None


def holds(shots: list, clip: str, at: float | None) -> bool:
    """A keeper is on this list: its clip, at its start when it names one (within HELD seconds)."""
    return any(s['clip'] == clip and (at is None or s.get('at') is None or abs(s['at'] - at) <= HELD)
               for s in shots)


def pair_by_clip(old: list, cur: list):
    """Each use of a clip in the new plan matched to one use in the old: one clip used at two ranges
    is two shots. A use is matched to the old use of that clip starting at the same point, else the
    nearest one, else the next in order. Returns (matched pairs, old shots unmatched, new unmatched)."""
    left = list(old)
    matched: dict = {}
    for i, b in enumerate(cur):  # the same clip at the same start: the same shot
        a = next((s for s in left if s['clip'] == b['clip'] and b.get('at') is not None and s.get('at') == b['at']), None)
        if a is not None:
            left.remove(a)
            matched[i] = a
    for i, b in enumerate(cur):
        if i in matched:
            continue
        same = [s for s in left if s['clip'] == b['clip']]
        if not same:
            continue
        timed = [s for s in same if s.get('at') is not None]
        a = min(timed, key=lambda s: abs(s['at'] - b['at'])) if b.get('at') is not None and timed else same[0]
        left.remove(a)
        matched[i] = a
    pairs = [(matched[i], b) for i, b in enumerate(cur) if i in matched]
    came = [b for i, b in enumerate(cur) if i not in matched]
    return pairs, left, came


def unsaid(shot: dict) -> bool:
    """A shot whose plan says no job, where the plan has jobs at all (a cut list has none)."""
    return shot.get('jobs', True) is not False and not shot.get('job')


def load_plan(path: str, lines: dict) -> dict:
    """{phrase: [{clip, job}]}, in plan order."""
    def key(phrase: str) -> str:
        return lines.get(phrase, phrase).strip()

    plan: dict = {}
    if path.endswith('.csv'):
        with open(path, encoding='utf-8') as f:
            for row in csv.DictReader(f):
                plan.setdefault(key(row.get('voiceover line', '')), []).append(
                    {'clip': clip_id(row.get('proxy filename')), 'at': start_of({'in': row.get('in (s)')}, 'in'), 'job': None, 'jobs': False})
        return plan
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data.get('rows'), list):
        for row in data['rows']:
            if isinstance(row, dict):
                plan.setdefault(key(str(row.get('phrase', ''))), []).append(
                    {'clip': clip_id(row.get('shot')), 'at': start_of(row, 'shot'), 'job': row.get('job')})
    elif isinstance(data.get('shots'), dict):
        last = None  # the shot that ends the line before: a carried-over entry continues it
        latest: dict = {}  # each clip's last use so far, for a carried-over entry naming an earlier one
        for line, shots in data['shots'].items():
            for shot in shots:
                if not isinstance(shot, dict):
                    continue
                if shot.get('clip'):
                    entry = {'clip': clip_id(shot['clip']), 'at': start_of(shot, 'clip'), 'job': shot.get('job')}
                else:  # {"job": "2391 carries over"}: the named clip, else the last one, held onto this line
                    said = str(shot.get('job') or '')
                    whole = re.match(r'\s*(.+?)\s+carries over', said)  # 'Interview 01.mp4 carries over'
                    clip = clip_id(whole.group(1)) if whole else None
                    if clip not in latest:  # not a clip used before: a numbered name, else the last one
                        named = re.match(r'\s*([\w.-]*\d[\w.-]*)\s+carries over', said)
                        clip = clip_id(named.group(1)) if named else (last or {}).get('clip')
                    if not clip:
                        continue
                    held = last if last and last['clip'] == clip else latest.get(clip)
                    entry = {'clip': clip, 'at': held.get('at') if held else None, 'job': held['job'] if held else None}
                plan.setdefault(key(line), []).append(entry)
                last = latest[entry['clip']] = entry
    else:
        raise ValueError('not a plan: expected "rows", "shots" or a cut list CSV')
    return plan


def approved(record: dict, change: dict, lines: dict | None = None) -> bool:
    """The user's approval of exactly this change: the meaning they chose, or the keeper they let go.

    A scope names its phrase by line id or by its words, as the plans do. A moment keeper sits on
    no phrase, so any keeper approval naming its shot or what lets it go."""
    lines = lines or {}

    def scoped(scope, prefix: str) -> str | None:
        if not isinstance(scope, str) or not scope.startswith(prefix):
            return None
        phrase = scope[len(prefix):]
        return lines.get(phrase, phrase).strip()

    for a in record.get('approvals', []):
        if not isinstance(a, dict):
            continue
        if change['kind'].startswith('KEEPER'):
            phrase = scoped(a.get('scope'), 'keeper:')
            if phrase is not None and (change.get('moment') or phrase == change['phrase']) and (
                    (a.get('shot') and clip_id(a['shot']) == change['shot'] and
                     (start_of(a, 'shot') is None or (change.get('at') is not None and
                      abs(start_of(a, 'shot') - change['at']) <= HELD))) or (a.get('what') and a['what'] == change.get('what'))):
                return True
        elif scoped(a.get('scope'), 'meaning:') == change['phrase'] and a.get('job') and a['job'] == change.get('toJob'):
            return True
    return False


def diff(shown: dict, new: dict, record: dict | None = None, lines: dict | None = None) -> dict:
    record = record or {}
    lines = lines or {}
    keepers = [(lines.get(k.get('phrase', ''), k.get('phrase', '')).strip(), clip_id(k.get('shot')), k)
               for k in record.get('keepers', []) if isinstance(k, dict) and k.get('kind') == 'pair']
    starts = {id(k): start_of(k, 'shot') for _, _, k in keepers}
    restored = {(phrase, clip) for phrase, clip, _ in keepers}
    changes = []
    for phrase in list(dict.fromkeys(list(shown) + list(new))):
        old = shown.get(phrase, [])
        cur = new.get(phrase, [])
        pairs, gone, came = pair_by_clip(old, cur)
        for a, b in zip(gone, came):
            if (phrase, b['clip']) in restored and b['clip'] not in [s['clip'] for s in old] and not unsaid(b):
                continue  # a keeper back on its phrase is reported as restored below
            if a.get('jobs', True) is False or b.get('jobs', True) is False:
                kind = 'NOT_COMPARED'  # a cut list says no job
            elif not a['job'] or not b['job']:
                kind = 'MEANING_UNKNOWN'
            else:
                kind = 'SHOT_SWAPPED' if a['job'] == b['job'] else 'MEANING_CHANGED'
            changes.append({'kind': kind, 'phrase': phrase,
                            'from': a['clip'], 'to': b['clip'], 'fromJob': a['job'], 'toJob': b['job']})
        for a in gone[len(came):]:
            changes.append({'kind': 'SHOT_REMOVED', 'phrase': phrase, 'from': a['clip'], 'fromJob': a['job']})
        for b in came[len(gone):]:
            kind = 'MEANING_UNKNOWN' if unsaid(b) else 'SHOT_ADDED'  # an added shot must say what it shows
            changes.append({'kind': kind, 'phrase': phrase, 'from': None, 'to': b['clip'], 'toJob': b['job']})
        for a, b in pairs:
            if a.get('jobs', True) is False or b.get('jobs', True) is False:
                continue  # a cut list says no job
            if a['job'] and b['job'] and a['job'] != b['job']:
                changes.append({'kind': 'JOB_REWRITTEN', 'phrase': phrase, 'shot': b['clip'],
                                'fromJob': a['job'], 'toJob': b['job']})
            elif not b['job']:
                changes.append({'kind': 'MEANING_UNKNOWN', 'phrase': phrase, 'from': a['clip'], 'to': b['clip'],
                                'fromJob': a['job'], 'toJob': None})

    for phrase, clip, keeper in keepers:
        at = starts[id(keeper)]
        was = holds(shown.get(phrase, []), clip, at)
        now = holds(new.get(phrase, []), clip, at)
        if was and not now:
            changes.append({'kind': 'KEEPER_DROPPED', 'phrase': phrase, 'shot': clip, 'what': keeper.get('what'), 'at': at})
        elif not was and not now:
            changes.append({'kind': 'KEEPER_STILL_DROPPED', 'phrase': phrase, 'shot': clip, 'what': keeper.get('what'), 'at': at})
        elif now and not was:
            changes.append({'kind': 'KEEPER_RESTORED', 'phrase': phrase, 'shot': clip, 'what': keeper.get('what')})
        # where else its clip sits, at any range: said to the user, never blocking
        placed_before = sorted(p for p, shots in shown.items() if p != phrase and holds(shots, clip, None))
        placed_now = sorted(p for p, shots in new.items() if p != phrase and holds(shots, clip, None))
        if placed_now and placed_now != placed_before:
            changes.append({'kind': 'KEEPER_MOVED', 'phrase': phrase, 'shot': clip, 'to': placed_now})

    def where(plan: dict, clip: str, at: float | None) -> list:
        return [p for p, shots in plan.items() if holds(shots, clip, at)]

    for keeper in record.get('keepers', []):  # a moment counts wherever it sits
        if not isinstance(keeper, dict) or keeper.get('kind') != 'moment' or not keeper.get('shot'):
            continue
        clip = clip_id(keeper['shot'])
        at = start_of(keeper, 'shot')
        was, now = where(shown, clip, at), where(new, clip, at)
        if now:
            continue
        changes.append({'kind': 'KEEPER_DROPPED' if was else 'KEEPER_STILL_DROPPED', 'phrase': (was or [''])[0],
                        'shot': clip, 'what': keeper.get('what'), 'moment': True, 'at': at})

    blocking = []
    for c in changes:
        if c['kind'] not in BLOCKING:
            continue
        c['approved'] = approved(record, c, lines)
        if not c['approved']:
            blocking.append(c)
    return {'changes': changes, 'lines': [say(c) for c in changes], 'blocking': blocking}


def say(c: dict) -> str:
    """One line for the message to the user."""
    p = f'"{c["phrase"]}"'
    kind = c['kind']
    if kind == 'KEEPER_DROPPED':
        return f'{p}: the {c.get("what") or c["shot"]} you saw is gone from this version.'
    if kind == 'KEEPER_STILL_DROPPED':
        return f'{p}: still without the {c.get("what") or c["shot"]} you saw.'
    if kind == 'KEEPER_RESTORED':
        return f'{p}: the {c.get("what") or c["shot"]} is back.'
    if kind == 'KEEPER_MOVED':
        return f'{p}: its {c.get("what") or c["shot"]} now also sits on {", ".join(c["to"])}.'
    if kind == 'MEANING_CHANGED':
        return f'{p}: {c["from"]} -> {c["to"]}, and what it shows changed ({c["fromJob"]} -> {c["toJob"]}).'
    if kind == 'MEANING_UNKNOWN' and not c.get('from'):
        return f'{p}: {c["to"]} added, and the plan does not say what it shows.'
    if kind == 'MEANING_UNKNOWN' and c['from'] == c['to']:
        return f'{p}: shot {c["to"]} kept, but the plan no longer says what it shows.'
    if kind == 'MEANING_UNKNOWN':
        return f'{p}: {c["from"]} -> {c["to"]}, and the plan does not say what the new shot shows.'
    if kind == 'NOT_COMPARED':
        return f'{p}: {c["from"]} -> {c["to"]} (meaning not compared: the cut list gives no job).'
    if kind == 'SHOT_SWAPPED':
        return f'{p}: {c["from"]} -> {c["to"]}, showing the same thing.'
    if kind == 'JOB_REWRITTEN':
        return f'{p}: shot {c["shot"]} kept, but its job was rewritten ({c["fromJob"]} -> {c["toJob"]}).'
    if kind == 'SHOT_REMOVED':
        return f'{p}: {c["from"]} removed.'
    return f'{p}: {c["to"]} added.'


def read_json(path: str):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description='The meaning diff of a new plan against the last shown version.')
    p.add_argument('shown')
    p.add_argument('new')
    p.add_argument('--record')
    p.add_argument('--lines')
    args = p.parse_args(argv)
    try:
        lines = read_json(args.lines) if args.lines else {}
        record = read_json(args.record) if args.record else {}
        out = diff(load_plan(args.shown, lines), load_plan(args.new, lines), record, lines)
    except (OSError, ValueError) as e:
        print(json.dumps({'error': str(e)}))
        return 2
    print(json.dumps(out, indent=1, ensure_ascii=False))
    return 1 if out['blocking'] else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
