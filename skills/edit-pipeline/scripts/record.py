"""The edit pipeline's project record: which stages are done, stale or next, the version list,
and the locked meaning map.

Usage (the record is a JSON file; every command prints JSON):
  record.py init <record> --use-case <name> --job <job> --stages <id,id,...>
  record.py check <record>                     the record against the core schema
  record.py status <record>                    each stage done, stale or to do, and the next one
  record.py done <record> <stage> [--artifact <file>]
  record.py invalidate <record> <stage>        the stage and everything after it are to be redone
  record.py add <record> <list> <json>         append to standing, approvals, rejected, locked, keepers, openDecisions
  record.py version <record> <json>            append a version (name, scene, render, parent, changed, gates)
  record.py lock-check <record> <plan>         a plan against the locked meaning map, the format and the pace
  record.py palette-check <record> <scene>     every colour a scene sets against the brand's palette
  record.py length-check <record> <scene>      the reel ends at the recipe's length, no held last clip
  record.py migrate <old record> [--out edit-footage.json]
                                               a client-edit, cut-footage-into-reel or remix-reel-structure
                                               record as edit-footage's, its done stages kept

A stage is done when it was marked done and the inputs it read are unchanged: the record keys it
reads, and what the stages before it produced. A change upstream makes every stage after it stale.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

# The core stages, in order: the record keys each reads and writes, and the stages it builds on.
STAGES = [
    # Standing decisions and the finish path are read only by the stages that use them, so a note
    # added at review never makes the log or the story stale.
    {'id': 'intake', 'reads': ['brief', 'job'], 'writes': [], 'after': []},
    {'id': 'reference', 'reads': ['reference'], 'writes': [], 'after': ['intake']},
    {'id': 'proxies', 'reads': ['footage'], 'writes': [], 'after': ['intake']},
    {'id': 'log', 'reads': ['footage'], 'writes': ['sources'], 'after': ['proxies']},
    {'id': 'takes', 'reads': [], 'writes': ['takes'], 'after': ['log']},
    {'id': 'look', 'reads': ['taste'], 'writes': [], 'after': ['log', 'reference', 'takes']},
    # The story writes the beats (an arc inferred from footage with no words included), never into
    # `brief`, which intake reads. The map is locked when the user approves it, at review, with the
    # first draft: review owns `locked`, so recording that approval leaves the draft current.
    {'id': 'story', 'reads': [], 'writes': ['story'], 'after': ['reference', 'takes']},
    {'id': 'plan', 'reads': ['cutPace', 'standing'], 'writes': [], 'after': ['story', 'look']},
    {'id': 'build', 'reads': [], 'writes': [], 'after': ['plan']},
    {'id': 'qc', 'reads': ['standing'], 'writes': [], 'after': ['build']},
    {'id': 'critics', 'reads': ['standing'], 'writes': [], 'after': ['qc']},
    {'id': 'review', 'reads': [], 'writes': ['locked', 'approvals'], 'after': ['critics']},
    {'id': 'finish', 'reads': ['finish'], 'writes': [], 'after': ['review']},
    {'id': 'deliver', 'reads': [], 'writes': [], 'after': ['finish']},
]
BY_ID = {s['id']: s for s in STAGES}
# What the reel and remix jobs' stages also write: the picked moments and the script's mapping are
# their story, the sheet their reference, the route and the planned takes their plan. Each counts
# only when the record holds it, and `takes` only for a job with no takes stage of its own, so a
# record kept before the merge hashes as it did then (job_writes).
JOB_WRITES = {'reference': ['sheet'], 'story': ['moments', 'mapping'], 'plan': ['route', 'takes']}
# Keys a stage reads only when the record holds them, so a record without one hashes as before:
# the reference's format (reel-structure's `references/format.md`) and the brand guide's palette and
# fonts bind the plan and all after it.
OPTIONAL_READS = {'plan': ['format', 'brand']}
# Keys a stage writes only when the record holds them, so a record kept before the stage wrote one
# hashes as before: the look stage's board, spec and check (edit-footage's `references/film-look.md`).
OPTIONAL_WRITES = {'look': ['look']}
# What `done deliver` needs, for every job: the map approved, then the check, the critics and the
# review done. A job that leaves one out of its pipeline cannot deliver.
DELIVER_NEEDS = ['story', 'qc', 'critics', 'review']
# The checks only the user may skip, never the agent on its own. A skip is recorded on the stage as
# `skipped: user` with the risk said, and delivery accepts it.
USER_SKIPPABLE = ('qc', 'critics', 'review')
# What story and review wrote before review owned `locked`: a record saved then still resumes as done.
LEGACY_WRITES = {'story': ['locked'], 'review': ['approvals']}
ORDER = [s['id'] for s in STAGES]

LISTS = ['standing', 'approvals', 'rejected', 'locked', 'keepers', 'openDecisions', 'versions']
# Required fields of each list's entries.
FIELDS = {
    'standing': ['text', 'words', 'date'],
    'approvals': ['what', 'by', 'date'],
    'rejected': ['what', 'date'],
    'locked': ['phrase', 'job', 'shot'],
    'keepers': ['kind', 'what', 'version'],
    'versions': ['name'],
}
# What each kind of keeper must say: a word and its picture, a moment, or the user's praise in their words.
KEEPER_KINDS = {'pair': ['phrase', 'shot'], 'moment': ['shot'], 'praise': ['words']}
# The motion data a camera writes beside the picture, as edit-on-your-computer's `scripts/gyro.py` names it.
GYRO_KINDS = ('sony-rtmd', 'gopro-gpmf', 'dji', 'insta360')
# A source's gyro fields: written at the proxies (also on a resume, after the log) and at the conform,
# so no stage's fingerprint counts them and a stabilised copy leaves the log and all after it current.
GYRO_FIELDS = ('gyro', 'gyroKind', 'stabilised')
# Which way is up (edit-footage's log): `yes`, a quarter turn either way, a half turn, or `open`. A source
# found turned after the log (a sign seen sideways in a draft) gets it then, so no fingerprint counts it
# either: the turn changes the picture, not the takes or the story, and the build is redone on purpose
# (`invalidate <record> build`).
UPRIGHT = ('yes', 'rot90', 'rot270', 'rot180', 'open')
# `stream` is the data stream `gyro.py` prints beside `gyro`: saved with them, it counts no more than they do.
UNHASHED_SOURCE_FIELDS = GYRO_FIELDS + ('stream', 'upright')
# The fields left out before `stream` was: a stage marked done in a record saved then, with `stream`
# in a source, still matches its inputs hashed this way.
STREAM_HASHED_SOURCE_FIELDS = GYRO_FIELDS + ('upright',)
# What the conform keeps of each used range: the stabilised copy, or the original when it is not steadier.
STABILISED_USES = ('stabilised', 'original')


def job_edit_error(record: dict, entry: dict) -> str | None:
    """A locked row's job is the contract: a new job for a locked phrase needs the user's approval of that job."""
    if not isinstance(entry, dict):
        return None
    for lock in record.get('locked', []):
        if lock.get('phrase') == entry.get('phrase') and lock.get('job') != entry.get('job'):
            ok = any(isinstance(a, dict) and a.get('scope') == f'meaning:{lock["phrase"]}' and a.get('job') == entry.get('job')
                     for a in record.get('approvals', []))
            if not ok:
                return (f'"{lock["phrase"]}" is locked to "{lock["job"]}"; its job changes only with the user\'s '
                        f'approval of "{entry.get("job")}" (an approval with scope "meaning:{lock["phrase"]}" and that job)')
    return None


def now() -> str:
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def digest(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()[:16]


def file_digest(path: str) -> str | None:
    if not path or not os.path.isfile(path):
        return None
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 16), b''):
            h.update(chunk)
    return h.hexdigest()[:16]


def load(path: str) -> dict:
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def save(path: str, record: dict) -> None:
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(record, f, indent=1, ensure_ascii=False)
        f.write('\n')
    os.replace(tmp, path)


def schema_errors(record: dict) -> list[str]:
    errors = []
    for key in ('useCase', 'job', 'pipeline', 'stages'):
        if key not in record:
            errors.append(f'missing "{key}"')
    for stage in record.get('pipeline', []):
        if stage not in BY_ID:
            errors.append(f'pipeline names "{stage}", which is not a core stage ({", ".join(ORDER)})')
    if [s for s in ORDER if s in record.get('pipeline', [])] != record.get('pipeline', []):
        errors.append('pipeline must list its stages in core order')
    brief = record.get('brief')
    if brief is not None and not (isinstance(brief, dict) and set(brief) <= {'said', 'read', 'assumed'}):
        errors.append('brief holds only "said", "read" and "assumed", kept apart')
    for name in LISTS:
        value = record.get(name, [])
        if not isinstance(value, list):
            errors.append(f'"{name}" must be a list')
            continue
        for i, entry in enumerate(value):
            need = FIELDS.get(name, [])
            if need and not isinstance(entry, dict):
                errors.append(f'{name}[{i}] must be an object with {", ".join(need)}')
                continue
            for field in need:
                if field not in entry:
                    errors.append(f'{name}[{i}] is missing "{field}"')
            if name == 'keepers':
                kind = entry.get('kind')
                if kind not in KEEPER_KINDS:
                    errors.append(f'keepers[{i}] kind must be one of {", ".join(KEEPER_KINDS)}')
                for field in KEEPER_KINDS.get(kind, []):
                    if not entry.get(field):
                        errors.append(f'keepers[{i}] is a {kind} and needs "{field}"')
            if name == 'approvals' and entry.get('session') and not entry.get('words'):
                errors.append(f'approvals[{i}] was relayed from {entry["session"]} without the person\'s "words": a yes in a session\'s own words is not an approval')
    errors.extend(look_errors(record.get('look')))
    for i, row in enumerate(record.get('sources', []) or []):
        errors.extend(gyro_errors(record, i, row))
        if isinstance(row, dict) and 'upright' in row and row['upright'] not in UPRIGHT:
            errors.append(f'sources[{i}].upright must be one of {", ".join(UPRIGHT)}')
        for r, rng in enumerate(row.get('ranges', []) if isinstance(row, dict) else []):
            for field in ('verdict', 'method', 'confidence'):
                if field not in rng:
                    errors.append(f'sources[{i}].ranges[{r}] is missing "{field}": every gate verdict says how it was measured')
            if rng.get('verdict') == 'pass' and rng.get('confidence') == 'none':
                errors.append(f'sources[{i}].ranges[{r}] passes with no confidence: what could not be measured is "open"')
    return errors


def gyro_errors(record: dict, i: int, row) -> list[str]:
    """A source's gyro fields: what its camera recorded, and a stabilised copy only on the user's yes."""
    if not isinstance(row, dict):
        return []
    errors = []
    if 'gyro' in row and not isinstance(row['gyro'], bool):
        errors.append(f'sources[{i}].gyro is true or false')
    if 'gyroKind' in row:
        if row.get('gyro') is not True:
            errors.append(f'sources[{i}] names a gyroKind without "gyro": true')
        elif row['gyroKind'] not in GYRO_KINDS:
            errors.append(f'sources[{i}].gyroKind must be one of {", ".join(GYRO_KINDS)}')
    stab = row.get('stabilised')
    if stab is None:
        return errors
    if not isinstance(stab, dict) or not stab.get('file'):
        return errors + [f'sources[{i}].stabilised needs its "file", a copy in the work folder']
    if stab['file'] in (row.get('file'), row.get('url')):
        errors.append(f'sources[{i}].stabilised.file is the original: stabilise into a copy, never over the original')
    crop = stab.get('crop')
    if isinstance(crop, bool) or not isinstance(crop, (int, float)) or crop < 1:
        errors.append(f'sources[{i}].stabilised needs its "crop", the zoom applied (1 or more), so framing checks allow for it')
    chosen = stab.get('ranges', [])
    if not isinstance(chosen, list):
        errors.append(f'sources[{i}].stabilised.ranges must be a list')
        chosen = []
    for r, rng in enumerate(chosen):
        at = f'sources[{i}].stabilised.ranges[{r}]'
        if not isinstance(rng, dict):
            errors.append(f'{at} must be an object with in, out, use and shake')
            continue
        for field in ('in', 'out', 'use', 'shake'):
            if field not in rng:
                errors.append(f'{at} is missing "{field}"')
        if 'use' in rng and rng['use'] not in STABILISED_USES:
            errors.append(f'{at}.use must be one of {", ".join(STABILISED_USES)}')
        shake = rng.get('shake')
        if 'shake' in rng and not (isinstance(shake, list) and len(shake) == 2
                                   and all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in shake)):
            errors.append(f'{at}.shake is the two measurements [plain, stabilised]')
        elif rng.get('use') == 'stabilised' and isinstance(shake, list) and len(shake) == 2 and not shake[1] < shake[0]:
            errors.append(f'{at} uses the stabilised copy, which is not steadier: keep it as shot ("use": "original")')
    if not any(isinstance(a, dict) and a.get('scope') == 'stabilise:gyro' for a in record.get('approvals', []) or []):
        errors.append(f'sources[{i}] is stabilised without the user\'s yes: an approval with the scope "stabilise:gyro"')
    return errors


LOOK_CHECKS = ('pass', 'flag', 'open')


def look_errors(look) -> list[str]:
    """The look stage's record: its board, its spec and the check against the board (edit-footage's
    `references/film-look.md`). A number nobody could read is `open`, never a pass."""
    if look is None:
        return []
    if not isinstance(look, dict):
        return ['"look" must be an object with "board", "spec" and "check"']
    errors = []
    if not isinstance(look.get('board'), list) or not look['board']:
        errors.append('look.board must list the reference stills the look was chosen from')
    if not isinstance(look.get('spec'), dict) or not look['spec']:
        errors.append('look.spec must say what the board shows (blacks, highlights, palette, ...)')
    check = look.get('check')
    # look_check.py prints {"ok", "items"}; film-look.md says to store that result as printed, so the
    # object form is the items it carries. A bare list of items is the same check written by hand.
    if isinstance(check, dict) and isinstance(check.get('items'), list):
        check = check['items']
    if not isinstance(check, list):
        errors.append('look.check must be a list of items, or look_check.py\'s result ({"ok", "items"}): '
                      'each item against the board, or [] when nothing was compared')
        check = []
    for i, item in enumerate(check):
        if not isinstance(item, dict) or item.get('verdict') not in LOOK_CHECKS:
            errors.append(f'look.check[{i}] needs a verdict: {", ".join(LOOK_CHECKS)}')
    return errors


def hand_keys(record: dict, stage: str) -> list[str]:
    """The keys a stage marked done by hand keeps in `reads`: its own reads, then what every stage it
    builds on reads and writes (a revised story or cut pace makes the plan and what follows stale)."""
    keys = stage_reads(record, stage)
    todo, seen = list(effective_after(record, stage)), set()
    while todo:
        dep = todo.pop()
        if dep in seen:
            continue
        seen.add(dep)
        keys.extend(k for k in stage_reads(record, dep) + job_writes(record, dep) if k not in keys)
        todo.extend(effective_after(record, dep))
    return keys


def effective_after(record: dict, stage: str) -> list[str]:
    """The stages this one builds on, looking through stages the job leaves out."""
    on = set(record['pipeline'])
    out: list[str] = []
    for dep in BY_ID[stage]['after']:
        if dep in on:
            out.append(dep)
        else:
            out.extend(d for d in effective_after(record, dep) if d not in out)
    return out


def stage_reads(record: dict, stage: str) -> list[str]:
    """A stage's reads, with the optional ones the record holds."""
    return list(BY_ID[stage]['reads']) + [k for k in OPTIONAL_READS.get(stage, []) if k in record]


def job_writes(record: dict, stage: str) -> list[str]:
    """A stage's writes, with the reel and remix jobs' own keys when the record holds them."""
    writes = list(BY_ID[stage]['writes'])
    writes.extend(k for k in OPTIONAL_WRITES.get(stage, []) if k in record and k not in writes)
    for key in JOB_WRITES.get(stage, []):
        owner = next((s['id'] for s in STAGES if key in s['writes']), None)
        if key in record and key not in writes and owner not in record.get('pipeline', []):
            writes.append(key)
    return writes


# What review writes into a reel job's takes: the approved scene and render. They are not the
# plan's output, so a review pass leaves the build, the check and the critics current.
BUILT_KEYS = ('scene', 'render', 'url')


def value(record: dict, key: str, unhashed: tuple = UNHASHED_SOURCE_FIELDS):
    """A record key as its stages compare it: a reel job's takes as the planned clip lists only, and
    the sources without their gyro fields and `upright`, which may be written after the log."""
    v = record.get(key)
    if key == 'sources' and isinstance(v, list):
        return [{k: x for k, x in s.items() if k not in unhashed} if isinstance(s, dict) else s for s in v]
    if key != 'takes' or 'takes' in record.get('pipeline', []):
        return v
    if isinstance(v, list):
        return [{k: x for k, x in t.items() if k not in BUILT_KEYS} if isinstance(t, dict) else t for t in v]
    if isinstance(v, dict):
        return {n: {k: x for k, x in t.items() if k not in BUILT_KEYS} if isinstance(t, dict) else t
                for n, t in v.items()}
    return v


def fingerprint(record: dict, stage: str, cache: dict, legacy: bool = False,
                unhashed: tuple = UNHASHED_SOURCE_FIELDS) -> str:
    """What a stage produced: its record keys and its artifact file, as they are now."""
    if stage in cache:
        return cache[stage]
    entry = record['stages'].get(stage, {})
    writes = job_writes(record, stage)
    if legacy:
        # as a record saved before review owned `locked` hashed it, plus the keys no such record held
        # (the look): one added since is a change, so the stages after it go stale
        writes = list(LEGACY_WRITES.get(stage, BY_ID[stage]['writes']))
        writes.extend(k for k in OPTIONAL_WRITES.get(stage, []) if k in record and k not in writes)
    parts = {k: value(record, k, unhashed) for k in writes}
    parts['artifact'] = file_digest(entry.get('artifact', '')) or entry.get('artifactHash')
    parts['inputs'] = inputs_hash(record, stage, cache, legacy, unhashed)
    cache[stage] = digest(parts)
    return cache[stage]


def inputs_hash(record: dict, stage: str, cache: dict, legacy: bool = False,
                unhashed: tuple = UNHASHED_SOURCE_FIELDS) -> str:
    parts = {'reads': {k: record.get(k) for k in stage_reads(record, stage)}}
    parts['after'] = {d: fingerprint(record, d, cache, legacy, unhashed) for d in effective_after(record, stage)}
    return digest(parts)


def status(record: dict) -> dict:
    cache: dict = {}
    old: dict = {}  # the same, hashed as a record saved before review owned `locked` (never had `story`)
    streamed: dict = {}  # the same, hashed with `stream` counted, as a record saved before 2026-11-06
    states: dict = {}
    for stage in record['pipeline']:
        entry = record['stages'].get(stage, {})
        if entry.get('status') != 'done':
            states[stage] = 'stale' if entry.get('status') == 'stale' else 'todo'
        elif any(states[d] != 'done' for d in effective_after(record, stage)):
            states[stage] = 'stale'
        elif entry.get('artifactHash') and not file_digest(entry.get('artifact', '')):
            states[stage] = 'stale'  # its artifact is gone, however it was marked done
        elif 'inputsHash' not in entry and 'reads' in entry:
            # marked done by hand, where no script ran: stale when a key it reads, or one a stage it
            # builds on read or wrote, has changed since
            changed = any(value(record, k) != value({**record, k: entry['reads'].get(k)}, k)
                          for k in hand_keys(record, stage))
            states[stage] = 'stale' if changed else 'done'
        elif entry.get('inputsHash') != inputs_hash(record, stage, cache) and (
                'story' in record or entry.get('inputsHash') != inputs_hash(record, stage, old, True)) and (
                entry.get('inputsHash') != inputs_hash(record, stage, streamed, unhashed=STREAM_HASHED_SOURCE_FIELDS)):
            states[stage] = 'stale'
        else:
            states[stage] = 'done'
    nxt = next((s for s in record['pipeline'] if states[s] != 'done'), None)
    why = None
    if nxt and states[nxt] == 'stale':
        why = 'it was done, but what it builds on changed since'
    result = {'stages': states, 'next': nxt, 'why': why}
    skipped = {s: e['skipped'] for s, e in record['stages'].items()
               if isinstance(e, dict) and e.get('skipped') and states.get(s) == 'done'}
    if skipped:
        result['skipped'] = skipped
    return result


def add_missing_critics(record: dict) -> bool:
    """A remix record started or migrated before the remix ran the critics: its pipeline gains
    `critics` after `qc`, so delivery, which needs them, is reachable."""
    pipeline = record.get('pipeline')
    if record.get('job') != 'remix' or not isinstance(pipeline, list) or 'critics' in pipeline or 'qc' not in pipeline:
        return False
    pipeline.insert(pipeline.index('qc') + 1, 'critics')
    return True


def lock_check(record: dict, plan: dict) -> dict:
    """Every locked row keeps its picture's job; a shot may change only for one with the same job.
    A change of job passes only with an approval for that phrase and that job."""
    rows = {}
    for r in plan.get('rows', []):
        if isinstance(r, dict):
            rows.setdefault(r.get('phrase'), []).append(r)  # every row for a phrase is checked
    approved = {(a.get('scope'), a.get('job')) for a in record.get('approvals', [])
                if isinstance(a, dict) and a.get('job')}  # an approval names the job it allows
    problems, swaps = [], []
    for lock in record.get('locked', []):
        phrase = lock['phrase']
        if phrase not in rows:
            problems.append({'phrase': phrase, 'problem': 'missing', 'locked': lock['job']})
            continue
        for row in rows[phrase]:
            if not row.get('shot'):
                problems.append({'phrase': phrase, 'problem': 'no shot', 'locked': lock['job']})
            elif not row.get('job'):
                problems.append({'phrase': phrase, 'problem': 'no job', 'locked': lock['job']})
            elif row['job'] != lock['job']:
                if (f'meaning:{phrase}', row['job']) not in approved:
                    problems.append({'phrase': phrase, 'problem': 'meaning changed', 'locked': lock['job'], 'planned': row['job']})
            elif row['shot'] != lock['shot']:
                swaps.append({'phrase': phrase, 'from': lock['shot'], 'to': row['shot'], 'job': lock['job']})
    if isinstance(record.get('format'), dict):
        # the reference's layout and caption position bind the plan as the locked rows do; a
        # difference passes only with an approval scoped `format:<element>`
        try:
            from ref_format import plan_check
        except ImportError:
            problems.append({'problem': 'format unchecked', 'why': "reel-structure's ref_format.py is not beside record.py"})
        else:
            problems += plan_check(record['format'], plan, record.get('approvals'))['problems']
    opened = []
    if isinstance(record.get('cutPace'), dict):
        # the reference's pace binds the plan too: holds under minHold, or a density far from it
        from match_check import pace_check
        pace = pace_check(record['cutPace'], plan, record.get('approvals'))
        problems += pace['problems']
        opened += pace['open']
    result = {'ok': not problems, 'problems': problems, 'sameMeaningSwaps': swaps}
    if opened:
        result['open'] = opened
    return result


def has_url(value) -> bool:
    """A record value names a file by its link: a string, or one inside a list or an object."""
    if isinstance(value, str):
        return value.startswith(URL_PREFIXES)
    if isinstance(value, dict):
        return any(has_url(v) for v in value.values())
    if isinstance(value, list):
        return any(has_url(v) for v in value)
    return False


def map_approved(record: dict) -> bool:
    """The map was approved: its rows locked, or an approval scoped to the map, the moments or the
    mapping. Only the scope counts: words in `what` ("the bitmap logo") never approve the map."""
    if record.get('locked'):
        return True
    for a in record.get('approvals') or []:
        if not isinstance(a, dict):
            continue
        scope = str(a.get('scope', '')).lower()
        if scope in ('map', 'moments', 'mapping') or scope.startswith('meaning:'):
            return True
    return False


def done_error(record: dict, stage: str) -> str | None:
    """What keeps a gated stage from being marked done: the reference needs its sheet and an answered
    format; delivery needs the map approved and the check, the critics and the review done."""
    ref = record.get('reference')
    # a picked style ({"style": "<id>"}) is a reference like a reel's link
    given = has_url(ref) or (isinstance(ref, dict) and bool(ref.get('style')))
    if stage == 'reference' and (given or 'format' in record):
        # a reference reel was given (or its format written): with none, the job's default pace holds
        if given and record.get('job') == 'channel-clips':
            # channel clips copy a look, not a structure: the format alone, no sheet
            if 'format' not in record:
                return 'the reference is done with its format: write it into the record first'
        elif given and ('sheet' not in record or 'format' not in record):
            return 'the reference is done with its sheet and its format: write them into the record first'
        try:
            from sheet import validate
            from ref_format import feasibility
        except ImportError:
            return "reel-structure's sheet.py and ref_format.py are not beside record.py"
        if 'sheet' in record:
            problems = validate(record['sheet'])
            if problems:
                return 'the sheet does not pass sheet.py validate: ' + '; '.join(problems[:3])
        if isinstance(record.get('format'), dict):
            problems = feasibility(record['format'])
            if problems:
                return 'the format is still open: ' + '; '.join(problems[:3])
        elif 'format' in record:
            return 'the format must be an object'
    if stage == 'deliver':
        states = status(record)['stages']
        missing = [s for s in DELIVER_NEEDS if states.get(s) != 'done']
        if missing:
            return (f'delivery needs {", ".join(missing)} done first, for any job; only the user may skip '
                    'one (record.py skip ... --by user --risk ...)')
        if not map_approved(record):
            return ('delivery needs the map approved: its rows locked, or an approval with scope "map", '
                    '"moments" or "mapping"')
    return None


# The record stages each job runs, in the core order (edit-footage's references/jobs.md).
REEL_JOBS = ('reel', 'highlight', 'podcast-clips', 'split', 'montage', 'slideshow', 'lesson')
REEL_PIPELINE = ['intake', 'log', 'story', 'plan', 'build', 'qc', 'critics', 'review', 'deliver']
REMIX_PIPELINE = ['intake', 'reference', 'story', 'plan', 'build', 'qc', 'critics', 'review', 'finish', 'deliver']
# The use cases merged into edit-footage, and the file names their records were kept under.
MERGED = {'client-edit': 'client-edit', 'cut-footage-into-reel': 'reel', 'remix-reel-structure': 'remix'}


def merged_kind(record: dict, path: str) -> str | None:
    """Which merged use case an old record came from: its `useCase`, else its file name."""
    use_case = record.get('useCase')
    if use_case in MERGED:
        return MERGED[use_case]
    if use_case is None:
        name = os.path.splitext(os.path.basename(path))[0]
        return MERGED.get(name)
    return None


def as_notes(value):
    """A brief part as an object: a list or a line of notes is kept under `notes`, never dropped."""
    if isinstance(value, dict):
        return dict(value)
    if isinstance(value, list):
        return {'notes': list(value)}
    if isinstance(value, str) and value.strip():
        return {'notes': [value]}
    return {}


URL_PREFIXES = ('https:', 'http:')


def built(takes) -> bool:
    """A reel record's takes are built: every planned take has a scene or render URL."""
    items = takes if isinstance(takes, list) else list(takes.values()) if isinstance(takes, dict) else []
    return bool(items) and all(isinstance(t, dict) and any(
        isinstance(t.get(k), str) and t[k].startswith(URL_PREFIXES) for k in BUILT_KEYS) for t in items)


def sheet_approved(record: dict) -> bool:
    """A remix record's sheet was approved at its REVIEW: `sheet.approved`, or an approval of the sheet."""
    sheet = record.get('sheet')
    if isinstance(sheet, dict) and sheet.get('approved'):
        return True
    for a in record.get('approvals') or []:
        if isinstance(a, dict) and ('sheet' in str(a.get('scope', '')).lower() or 'sheet' in str(a.get('what', '')).lower()):
            return True
    return False


def migrate(record: dict, path: str) -> dict:
    """An old record as edit-footage's: the same project, its keys kept, its done stages marked done
    by hand with what each read, so `status` resumes it where it stopped."""
    kind = merged_kind(record, path)
    if kind is None:
        raise ValueError(f'{path} is not a record of client-edit, cut-footage-into-reel or remix-reel-structure')
    new = dict(record)
    new['useCase'] = 'edit-footage'
    if kind == 'client-edit':
        return new  # the core record already: only the name changes
    brief = record.get('brief') if isinstance(record.get('brief'), dict) else {}
    new['brief'] = {k: as_notes(brief.get(k, {})) for k in ('said', 'read', 'assumed')}
    # The reel record kept the destination, goal and the rest beside said/read/assumed: they join
    # `read`, and a key both hold keeps both values. Nothing the user said is dropped.
    read = new['brief']['read']
    for key, value in brief.items():
        if key in ('said', 'read', 'assumed'):
            continue
        if key not in read or read[key] == value:
            read[key] = value
        else:
            old = read[key] if isinstance(read[key], list) else [read[key]]
            read[key] = old + [v for v in (value if isinstance(value, list) else [value]) if v not in old]
    for name in LISTS:
        new.setdefault(name, [])
    if kind == 'reel':
        new.setdefault('job', 'reel')
        if new['job'] not in REEL_JOBS:
            raise ValueError(f'{path}: job "{new["job"]}" is not a reel job ({", ".join(REEL_JOBS)})')
        new['pipeline'] = list(REEL_PIPELINE)
        done = []
        if record.get('brief'):
            done.append('intake')
        if record.get('moments'):
            done += ['log', 'story']
            if record.get('takes'):
                done.append('plan')  # takes are planned at the plan; built only with a scene or render
                if built(record['takes']):
                    done.append('build')  # the check, the critics and the review run again: they are free
    else:
        new['job'] = 'remix'
        new['pipeline'] = list(REMIX_PIPELINE)  # with `critics`, which delivery needs
        done = []
        if record.get('reference'):
            done.append('intake')
            if record.get('sheet') and sheet_approved(record):
                done.append('reference')
                if record.get('mapping'):
                    done.append('story')
                    if record.get('route'):
                        done.append('plan')  # a built stage is shown again for its REVIEW
    new['stages'] = {}
    at = now()
    for stage in done:  # in core order, so each one's reads include what the ones before it wrote
        new['stages'][stage] = {'status': 'done', 'at': at, 'migrated': True,
                                'reads': {k: new.get(k) for k in hand_keys(new, stage)}}
    return new


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description='The edit pipeline project record.')
    sub = p.add_subparsers(dest='cmd', required=True)
    a = sub.add_parser('init'); a.add_argument('record'); a.add_argument('--use-case', required=True)
    a.add_argument('--job', required=True); a.add_argument('--stages', required=True)
    for name in ('check', 'status'):
        sub.add_parser(name).add_argument('record')
    a = sub.add_parser('done'); a.add_argument('record'); a.add_argument('stage'); a.add_argument('--artifact')
    a = sub.add_parser('skip'); a.add_argument('record'); a.add_argument('stage', choices=USER_SKIPPABLE)
    a.add_argument('--by', required=True, choices=['user']); a.add_argument('--risk', required=True)
    a = sub.add_parser('invalidate'); a.add_argument('record'); a.add_argument('stage')
    a = sub.add_parser('add'); a.add_argument('record'); a.add_argument('list', choices=LISTS[:-1]); a.add_argument('entry')
    a = sub.add_parser('version'); a.add_argument('record'); a.add_argument('entry')
    a = sub.add_parser('lock-check'); a.add_argument('record'); a.add_argument('plan')
    a = sub.add_parser('palette-check'); a.add_argument('record'); a.add_argument('scene')
    a = sub.add_parser('length-check'); a.add_argument('record'); a.add_argument('scene')
    a = sub.add_parser('migrate'); a.add_argument('record'); a.add_argument('--out', default='edit-footage.json')
    args = p.parse_args(argv)

    def out(value: dict, code: int = 0) -> int:
        print(json.dumps(value, indent=1, ensure_ascii=False))
        return code

    if args.cmd == 'migrate':
        target = os.path.join(os.path.dirname(args.record), args.out) if not os.path.isabs(args.out) else args.out
        if os.path.exists(target) and os.path.abspath(target) != os.path.abspath(args.record):
            return out({'ok': False, 'error': f'{target} exists; resume from it instead'}, 1)
        try:
            record = migrate(load(args.record), args.record)
        except ValueError as e:
            return out({'ok': False, 'error': str(e)}, 1)
        errors = schema_errors(record)
        if errors:
            return out({'ok': False, 'errors': errors}, 1)
        save(target, record)
        return out({'ok': True, 'record': target, **status(record)})

    if args.cmd == 'init':
        if os.path.exists(args.record):
            return out({'ok': False, 'error': 'the record exists; resume from it instead'}, 1)
        stages = [s.strip() for s in args.stages.split(',') if s.strip()]
        record = {'useCase': args.use_case, 'job': args.job, 'pipeline': stages, 'stages': {},
                  'brief': {'said': {}, 'read': {}, 'assumed': {}}, **{k: [] for k in LISTS}}
        errors = schema_errors(record)
        if errors:
            return out({'ok': False, 'errors': errors}, 1)
        save(args.record, record)
        return out({'ok': True, 'next': stages[0] if stages else None})

    record = load(args.record)
    upgraded = add_missing_critics(record)
    errors = schema_errors(record)
    if args.cmd == 'check':
        return out({'ok': not errors, 'errors': errors}, 0 if not errors else 1)
    if errors:
        return out({'ok': False, 'errors': errors}, 1)

    if upgraded and args.cmd != 'status':
        save(args.record, record)
    if args.cmd == 'status':
        return out(status(record))
    if args.cmd == 'skip':
        if args.stage not in record['pipeline']:
            return out({'ok': False, 'error': f'{args.stage} is not in this job\'s pipeline'}, 1)
        if not args.risk.strip():
            return out({'ok': False, 'error': 'say the risk of skipping it, in one line'}, 1)
        late = [d for d in effective_after(record, args.stage) if status(record)['stages'][d] != 'done']
        if late:
            return out({'ok': False, 'error': f'{args.stage} builds on {", ".join(late)}, which is not done'}, 1)
        record['stages'][args.stage] = {'status': 'done', 'at': now(), 'skipped': args.by, 'risk': args.risk.strip(),
                                        'inputsHash': inputs_hash(record, args.stage, {})}
        save(args.record, record)
        return out({'ok': True, **status(record)})
    if args.cmd == 'done':
        if args.stage not in record['pipeline']:
            return out({'ok': False, 'error': f'{args.stage} is not in this job\'s pipeline'}, 1)
        late = [d for d in effective_after(record, args.stage) if status(record)['stages'][d] != 'done']
        if late:
            return out({'ok': False, 'error': f'{args.stage} builds on {", ".join(late)}, which is not done'}, 1)
        gate = done_error(record, args.stage)
        if gate:
            return out({'ok': False, 'error': gate}, 1)
        artifact_hash = file_digest(args.artifact) if args.artifact else None
        if args.artifact and artifact_hash is None:
            return out({'ok': False, 'error': f'artifact not found: {args.artifact}'}, 1)
        entry = {'status': 'done', 'at': now(), 'inputsHash': inputs_hash(record, args.stage, {})}
        if args.artifact:
            entry['artifact'] = args.artifact
            entry['artifactHash'] = artifact_hash
        record['stages'][args.stage] = entry
        save(args.record, record)
        return out({'ok': True, **status(record)})
    if args.cmd == 'invalidate':
        if args.stage not in record['pipeline']:
            return out({'ok': False, 'error': f'{args.stage} is not in this job\'s pipeline'}, 1)
        start = record['pipeline'].index(args.stage)
        for stage in record['pipeline'][start:]:
            if stage in record['stages']:
                record['stages'][stage]['status'] = 'stale'
        save(args.record, record)
        return out({'ok': True, **status(record)})
    if args.cmd in ('add', 'version'):
        name = 'versions' if args.cmd == 'version' else args.list
        entry = json.loads(args.entry)
        if isinstance(entry, dict) and name not in ('locked', 'keepers'):
            entry.setdefault('date', now()[:10])
        if name == 'locked':
            error = job_edit_error(record, entry)
            if error:
                return out({'ok': False, 'error': error}, 1)
            # an approved new job replaces the old row, so the phrase keeps one contract
            record['locked'] = [r for r in record.get('locked', []) if r.get('phrase') != entry.get('phrase')]
        record.setdefault(name, []).append(entry)
        errors = schema_errors(record)
        if errors:
            return out({'ok': False, 'errors': errors}, 1)
        save(args.record, record)
        return out({'ok': True, 'count': len(record[name])})
    if args.cmd == 'lock-check':
        result = lock_check(record, load(args.plan))
        return out(result, 0 if result['ok'] else 1)
    if args.cmd == 'palette-check':
        from match_check import palette_check
        result = palette_check(record, load(args.scene))
        return out(result, 0 if result['ok'] else 1)
    if args.cmd == 'length-check':
        from match_check import length_check
        result = length_check(record, load(args.scene))
        return out(result, 0 if result['ok'] else 1)
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
