"""Read a QC inspector's report: check its shape, keep only critical and major findings, and
recompute its verdict, so nothing passes that was not checked.

    python3 scripts/inspection.py qc-v3-r1.json [--record edit-footage.json]

Prints {verdict, blocking, findings, conflicts, open, checked, problems, dropped}. Exits 0 on a
pass, 1 when there is anything to fix or check, 2 when the report itself is malformed.
"""
from __future__ import annotations

import argparse
import json
import sys

CHECKS = ['steadiness', 'lips', 'cut-word', 'shot-length', 'jump-cut', 'legible-text', 'captions', 'audio', 'end-card', 'meaning', 'keepers']
# Checks owed only when the record holds what they check: the reference's format.
FORMAT_CHECKS = ['reference-match']
KNOWN = CHECKS + FORMAT_CHECKS
SEVERITIES = ['critical', 'major']
BELOW = ['minor', 'nit']  # left out of the report on purpose: dropped and counted
CONFIDENCES = ['high', 'low']


def read(report: dict, locked: list[str] | None = None, has_format: bool = False) -> dict:
    problems: list[str] = []
    findings, dropped = [], 0
    for i, f in enumerate(report.get('findings') or []):
        if not isinstance(f, dict):
            problems.append(f'findings[{i}] is not an object')
            continue
        severity = str(f.get('severity', '')).lower()
        if severity in BELOW:
            dropped += 1
            continue
        if severity not in SEVERITIES:
            problems.append(f'findings[{i}] severity "{f.get("severity")}" is not critical or major')
            continue
        for field in ('check', 'at', 'what', 'method', 'confidence'):
            if field not in f:
                problems.append(f'findings[{i}] is missing "{field}"')
        if not isinstance(f.get('check'), str) or f.get('check') not in KNOWN:
            problems.append(f'findings[{i}] check "{f.get("check")}" is not one of {", ".join(KNOWN)}')
        if f.get('confidence') not in CONFIDENCES:
            problems.append(f'findings[{i}] confidence must be high or low')
        if not (f.get('fix') or f.get('alternative')):
            problems.append(f'findings[{i}] offers no fix or alternative: a check flags and offers, it never just drops')
        findings.append({**f, 'severity': severity})
    opened = []
    for i, o in enumerate(report.get('open') or []):
        if not isinstance(o, dict):
            problems.append(f'open[{i}] is not an object with check and why: {o!r}')
            opened.append({'check': None, 'why': str(o)})  # kept open, never dropped
            continue
        if not o.get('why'):
            problems.append(f'open[{i}] does not say why it could not be checked')
        opened.append(o)
    checked_input = report.get('checked', [])
    if not isinstance(checked_input, list):
        problems.append('checked must be a list')
        checked_input = []
    checked = [c for c in checked_input if isinstance(c, str) and c in KNOWN]
    accounted = set(checked) | {o.get('check') for o in opened if isinstance(o.get('check'), str)} \
        | {f.get('check') for f in findings if isinstance(f.get('check'), str)}
    for check in CHECKS + (FORMAT_CHECKS if has_format else []):
        if check not in accounted:
            opened.append({'check': check, 'why': 'the report neither ran it nor said why not'})
    locked_phrases = set(locked or [])
    conflicts = []
    for f in findings:
        phrase = f.get('locked')
        if phrase or f.get('check') == 'meaning':
            conflicts.append(f)
            if phrase and locked is not None and phrase not in locked_phrases:
                problems.append(f'a finding names the locked phrase "{phrase}", which the record does not lock')
    verdict = 'fix' if findings else ('open' if opened else 'pass')
    return {
        'version': report.get('version'),
        'verdict': verdict,
        'blocking': [f for f in findings if f['severity'] == 'critical'],
        'findings': [f for f in findings if f not in conflicts],
        'conflicts': conflicts,
        'open': opened,
        'checked': checked,
        'problems': problems,
        'dropped': dropped,
    }


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    p.add_argument('report')
    p.add_argument('--record')
    args = p.parse_args(argv)
    try:
        with open(args.report, encoding='utf-8') as f:
            text = f.read()
        if '```' in text:
            text = text.split('```json', 1)[-1].split('```', 1)[0] if '```json' in text else text.split('```')[1]
        report = json.loads(text)
    except (OSError, ValueError, IndexError) as err:
        print(json.dumps({'verdict': 'open', 'problems': [f'the report is not JSON: {err}']}))
        return 2
    locked, has_format = None, False
    if args.record:
        with open(args.record, encoding='utf-8') as f:
            record = json.load(f)
        locked = [row.get('phrase') for row in record.get('locked', []) if isinstance(row, dict)]
        has_format = isinstance(record.get('format'), dict)
    out = read(report, locked, has_format)
    print(json.dumps(out, indent=1, ensure_ascii=False))
    if out['problems']:
        return 2
    return 0 if out['verdict'] == 'pass' else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
