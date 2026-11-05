#!/usr/bin/env python3
"""A reference's format: its layout, captions, hook, emphasis and end card, as the record's `format`.

    python3 scripts/ref_format.py from-sheet sheet.json [more.json ...] --source own-brand
                                  [--canvas 1080x1920] [--fps 30] [--out format.json]
    python3 scripts/ref_format.py check format.json
    python3 scripts/ref_format.py feasibility format.json
    python3 scripts/ref_format.py plan-check format.json plan.json [--approvals approvals.json]

`from-sheet` drafts the block from one or more structure sheets (sheet.py): the `Layout` header,
or the beats' `Frame` cells, the `Caption position` cells and the caption style. With several
references, each keeps its own layout: the majority goes into `format`, and every other one becomes
an open feasibility row for the user to answer. What the sheets cannot say (the hook, the end
card, the brand files) stays out until it is read from the stills and written in.

`check` lists every schema problem. `feasibility` refuses a block whose elements are not each
answered as reproduced, approximated (with how, and the user's answer) or impossible (with the
user's answer): the reference stage is not done before. `plan-check` compares a plan (a cut list
with rows, or reel_cut.py's input with clips) with the format's layout and caption position; a
difference passes only with an approval scoped `format:<element>`.

Every command prints JSON. Exits 0 when clean, 1 with problems, 2 on unreadable input.
Python 3.9 or later, the standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from typing import Any, Dict, List, Optional, Tuple

Json = Dict[str, Any]

SOURCES = ('own-brand', 'third-party', 'described')
MODES = ('single', 'split-v', 'stacked', 'pip', 'full')
# Words a sheet may use for a layout mode.
MODE_WORDS = {
    'single': 'single', 'one person': 'single', 'crop': 'single', 'talking head': 'single',
    'split-v': 'split-v', 'split': 'split-v', 'split screen': 'split-v', 'split-screen': 'split-v',
    'top/bottom': 'split-v', 'top and bottom': 'split-v',
    'stacked': 'stacked', 'pip': 'pip', 'picture in picture': 'pip', 'picture-in-picture': 'pip',
    'full': 'full', 'full frame': 'full', 'full-frame': 'full', 'wide': 'full',
}
SLOTS = ('top', 'bottom', 'left', 'right', 'main', 'inset')
POSITIONS = ('seam', 'top', 'centre', 'center', 'bottom', 'lower third', 'above-seam', 'below-seam')
VERDICTS = ('reproduced', 'approximated', 'impossible')
# The elements a format can hold, each answered in feasibility when present.
ELEMENTS = ('layout', 'emphasis', 'captions', 'hook', 'endCard', 'brand')


class InputError(ValueError):
    """Input the format cannot be read from; the message says what to change."""


def unknown(value: Any) -> bool:
    return value is None or (isinstance(value, str) and (not value.strip() or value.strip().startswith('?')))


def read_mode(text: Any) -> Optional[str]:
    """The layout mode a cell or header names, or None when it names none."""
    if unknown(text):
        return None
    head = re.split(r'[(:,;]', str(text).lower(), maxsplit=1)[0].strip()
    if head in MODE_WORDS:
        return MODE_WORDS[head]
    for word in sorted(MODE_WORDS, key=len, reverse=True):
        if re.search(r'(?<![\w-])' + re.escape(word) + r'(?![\w-])', head):
            return MODE_WORDS[word]
    return None


def read_slots(text: Any) -> Json:
    """Who sits where: `split-v (top host, bottom guest)` gives {top: host, bottom: guest}."""
    inside = re.search(r'\(([^)]*)\)', str(text or ''))
    slots: Json = {}
    for part in (inside.group(1).split(',') if inside else []):
        words = part.strip().split(None, 1)
        if len(words) == 2 and words[0].lower() in SLOTS:
            slots[words[0].lower()] = words[1].strip()
    return slots


def frame_mode(cell: Any) -> Optional[str]:
    """A Frame cell's mode: `full: guest` is full, `split-v` is split-v."""
    return read_mode(cell)


def sheet_layout(sheet: Json) -> Tuple[Optional[str], Json, Dict[str, int]]:
    """A sheet's main layout mode, its slots, and how many beats each frame mode fills."""
    beats = [b for b in sheet.get('beats') or [] if isinstance(b, dict)]
    counts = Counter(m for m in (frame_mode(b.get('frame')) for b in beats) if m)
    header = read_mode(sheet.get('layout'))
    if header:
        return header, read_slots(sheet.get('layout')), dict(counts)
    if not counts:
        return None, {}, {}
    # A full-frame insert inside another layout is emphasis, not the layout.
    main = max((m for m in counts if m != 'full'), key=lambda m: counts[m], default='full')
    return main, {}, dict(counts)


def from_sheets(sheets: List[Json], source: str, canvas: Tuple[int, int] = (1080, 1920), fps: float = 30) -> Json:
    if source not in SOURCES:
        raise InputError(f'--source is one of {", ".join(SOURCES)}')
    if not sheets:
        raise InputError('give at least one sheet')
    layouts = [sheet_layout(s) for s in sheets]
    votes = Counter(mode for mode, _, _ in layouts if mode)
    fmt: Json = {'source': source, 'canvas': list(canvas), 'fps': fps, 'evidence': [], 'feasibility': []}
    if votes:
        mode, _ = votes.most_common(1)[0]
        slots = next((s for m, s, _ in layouts if m == mode and s), {})
        layout: Json = {'mode': mode, 'slots': slots}
        if mode == 'split-v':
            layout['seam'] = canvas[1] // 2
        fmt['layout'] = layout
        for n, (other, _, _) in enumerate(layouts, 1):
            if other and other != mode:
                fmt['feasibility'].append({'element': 'layout', 'verdict': 'open',
                                           'how': f'reference {n} is {other}, the others {mode}: which to follow'})
        full = sum(c.get('full', 0) for m, _, c in layouts if m == mode and m != 'full')
        length = sum(float(s.get('total_length') or 0) for s, (m, _, _) in zip(sheets, layouts) if m == mode)
        if full and length > 0:
            fmt['emphasis'] = {'kind': 'full-frame', 'per10s': round(full * 10 / length, 2)}
    positions = Counter()
    for s in sheets:
        for b in s.get('beats') or []:
            cell = b.get('caption_position') if isinstance(b, dict) else None
            if not unknown(cell):
                positions[str(cell).strip().lower()] += 1
    styles = [s.get('caption_style') for s in sheets if not unknown(s.get('caption_style'))]
    if positions or styles:
        captions: Json = {'style': {'note': styles[0]} if styles else {}}
        if positions:
            captions['position'] = positions.most_common(1)[0][0]
        fmt['captions'] = captions
    return fmt


def number_list(value: Any, n: int) -> bool:
    return isinstance(value, list) and len(value) == n and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in value)


def check(fmt: Any) -> List[str]:
    """Every schema problem in a format block, one sentence each."""
    if not isinstance(fmt, dict):
        return ['the format must be a JSON object']
    problems = []
    if fmt.get('source') not in SOURCES:
        problems.append(f'source is one of {", ".join(SOURCES)}')
    if not number_list(fmt.get('canvas'), 2) or min(fmt['canvas']) <= 0:
        problems.append('canvas is [width, height] in pixels')
    if not isinstance(fmt.get('fps'), (int, float)) or fmt['fps'] <= 0:
        problems.append('fps is a positive number')
    layout = fmt.get('layout')
    if layout is not None:
        if not isinstance(layout, dict) or layout.get('mode') not in MODES:
            problems.append(f'layout.mode is one of {", ".join(MODES)}')
        elif layout['mode'] == 'split-v':
            seam = layout.get('seam')
            if not isinstance(seam, (int, float)) or not number_list(fmt.get('canvas'), 2) or not 0 < seam < fmt['canvas'][1]:
                problems.append('a split-v layout gives its seam, in pixels from the top, inside the canvas')
        if isinstance(layout, dict) and not isinstance(layout.get('slots', {}), dict):
            problems.append('layout.slots maps a slot (top, bottom, main, inset) to who fills it')
    emphasis = fmt.get('emphasis')
    if emphasis is not None:
        if not isinstance(emphasis, dict) or emphasis.get('kind') not in ('full-frame', 'zoom', 'none'):
            problems.append('emphasis.kind is full-frame, zoom or none')
        elif 'hold' in emphasis and not number_list(emphasis['hold'], 2):
            problems.append('emphasis.hold is [shortest, longest] in seconds')
    captions = fmt.get('captions')
    if captions is not None:
        if not isinstance(captions, dict):
            problems.append('captions is an object with style and position')
        elif 'position' in captions and captions['position'] not in POSITIONS:
            problems.append(f'captions.position is one of {", ".join(POSITIONS)}')
        elif isinstance(captions.get('style'), dict) and 'words' in captions['style'] and not number_list(captions['style']['words'], 2):
            problems.append('captions.style.words is [fewest, most] words a card')
    hook = fmt.get('hook')
    if hook is not None:
        if not isinstance(hook, dict):
            problems.append('hook is an object with style, position, lines and length')
        else:
            if 'length' in hook and (not isinstance(hook['length'], (int, float)) or hook['length'] <= 0):
                problems.append('hook.length is seconds on screen')
            if 'lines' in hook and not number_list(hook['lines'], 2):
                problems.append('hook.lines is [fewest, most] lines')
    end = fmt.get('endCard')
    if end is not None:
        if not isinstance(end, dict):
            problems.append('endCard is an object with asset, duration and copy')
        else:
            if 'duration' in end and (not isinstance(end['duration'], (int, float)) or end['duration'] <= 0):
                problems.append('endCard.duration is seconds')
            if 'copy' in end and not (isinstance(end['copy'], list) and all(isinstance(c, str) for c in end['copy'])):
                problems.append('endCard.copy is the card\'s lines, word for word')
    for key in ('evidence', 'feasibility'):
        if key in fmt and not isinstance(fmt[key], list):
            problems.append(f'{key} is a list')
    for n, e in enumerate(fmt.get('evidence') or [], 1):
        if not isinstance(e, dict) or e.get('element') not in ELEMENTS or not isinstance(e.get('still'), str):
            problems.append(f'evidence {n} names an element ({", ".join(ELEMENTS)}) and the reference still that shows it')
    for n, row in enumerate(fmt.get('feasibility') or [], 1):
        if not isinstance(row, dict) or row.get('element') not in ELEMENTS:
            problems.append(f'feasibility {n} names an element ({", ".join(ELEMENTS)})')
        elif row.get('verdict') not in VERDICTS + ('open',):
            problems.append(f'feasibility {n} ({row["element"]}): verdict is {", ".join(VERDICTS)}, or open')
    if fmt.get('source') == 'third-party' and isinstance(fmt.get('brand'), dict) and fmt['brand']:
        problems.append("a third-party reference lends no brand: its logo, fonts and end card stay its own")
    return problems


def feasibility(fmt: Json) -> List[str]:
    """What keeps the reference stage open: an element with no answer, or an answer it lacks."""
    problems = check(fmt)
    if problems:
        return problems
    rows: Dict[str, List[Json]] = {}
    for row in fmt.get('feasibility') or []:
        rows.setdefault(row['element'], []).append(row)
    for element in ELEMENTS:
        if element not in fmt or element == 'brand':
            continue
        if element not in rows:
            problems.append(f'{element}: say whether it is reproduced, approximated or impossible with this footage')
    for element, found in rows.items():
        for row in found:
            verdict = row.get('verdict')
            if verdict == 'open':
                problems.append(f'{element}: still open ({row.get("how") or "no answer"}); ask the user, with a mock beside the reference still')
            elif verdict == 'approximated' and unknown(row.get('how')):
                problems.append(f'{element}: approximated, but not how')
            if verdict in ('approximated', 'impossible') and unknown(row.get('answer')):
                problems.append(f'{element}: {verdict} needs the user\'s answer to the ASK with a mock')
    return problems


PLACE_ALIASES = {'center': 'centre', 'middle': 'centre', 'lower-third': 'lower third', 'lower_third': 'lower third',
                 'above seam': 'above-seam', 'below seam': 'below-seam'}


def place_name(value: Any) -> Optional[str]:
    """A caption or hook place in its one spelling: `center` is `centre`."""
    if not isinstance(value, str) or not value.strip():
        return None
    named = value.strip().lower()
    return PLACE_ALIASES.get(named, named)


def plan_mode(item: Json) -> Optional[str]:
    """The layout an item names: its `layout`, else its `frame` or `mode` (reel_cut.py's clip frame,
    where `crop` is a single frame and `full` the whole one)."""
    value = next((item[k] for k in ('layout', 'frame', 'mode') if item.get(k) is not None), None)
    if isinstance(value, dict):
        value = value.get('mode')
    return read_mode(value) if value is not None else None


def plan_check(fmt: Json, plan: Json, approvals: Optional[List[Json]] = None) -> Json:
    """A plan against the format's layout and caption position. Only a layout that contradicts the
    format fails, and it passes with an approval scoped `format:<element>`. A plan or item that names
    no layout takes the format's when that is `single` (an edit's rows, plain reel clips); a split
    format needs the plan to say so, since an unmarked cut is built as one frame. A `full` item is a
    whole-frame shot: B-roll beside a single frame, or the emphasis of a split whose format has it."""
    approved = {a.get('scope') for a in approvals or [] if isinstance(a, dict)}
    problems: List[Json] = []
    layout = fmt.get('layout') if isinstance(fmt.get('layout'), dict) else None
    mode = layout.get('mode') if layout else None
    emphasis = (fmt.get('emphasis') or {}).get('kind') if isinstance(fmt.get('emphasis'), dict) else None
    if mode and 'format:layout' not in approved:
        top = plan_mode(plan)
        if top is not None and top != mode:
            problems.append({'element': 'layout', 'where': 'plan', 'format': mode, 'planned': top})
        items = [('rows', r) for r in plan.get('rows') or []] + [('clips', c) for c in plan.get('clips') or []]
        counts: Counter = Counter()
        unmarked: List[str] = []
        for n, (kind, item) in enumerate(items):
            if not isinstance(item, dict):
                continue
            got = plan_mode(item)
            if got is None:
                got = top
            if got is None and mode == 'single':
                got = 'single'
            if got is None:
                unmarked.append(f'{kind}[{n}]')
                continue
            counts[got] += 1
            if got == mode or (got == 'full' and (mode == 'single' or emphasis == 'full-frame')):
                continue
            problems.append({'element': 'layout', 'where': f'{kind}[{n}]', 'format': mode, 'planned': got})
        if top is None and mode != 'single':
            if not counts:
                problems.append({'element': 'layout', 'where': 'plan', 'format': mode, 'planned': None,
                                 'problem': 'the plan says no layout; give it the format\'s'})
            elif not problems:
                for where in unmarked:
                    problems.append({'element': 'layout', 'where': where, 'format': mode, 'planned': None,
                                     'problem': f'{where} says no layout; give it or the plan the format\'s'})
    captions = fmt.get('captions') if isinstance(fmt.get('captions'), dict) else {}
    position = place_name(captions.get('position'))
    planned = place_name((plan.get('captions') or {}).get('position')) if isinstance(plan.get('captions'), dict) else None
    if position and planned and planned != position and 'format:captions' not in approved:
        problems.append({'element': 'captions', 'where': 'plan', 'format': position, 'planned': planned})
    return {'ok': not problems, 'problems': problems}


def load(path: str) -> Any:
    try:
        with open(path, encoding='utf-8-sig') as f:
            return json.load(f)
    except json.JSONDecodeError as exc:
        raise InputError(f'{path} is not JSON: {exc}')


def load_sheet(path: str) -> Json:
    if path.lower().endswith(('.md', '.markdown', '.txt')):
        import sheet as sheet_module  # the structure sheet, beside this script
        with open(path, encoding='utf-8-sig') as f:
            return sheet_module.parse_markdown(f.read())
    return load(path)


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='cmd', required=True)
    a = sub.add_parser('from-sheet')
    a.add_argument('sheets', nargs='+')
    a.add_argument('--source', required=True, choices=SOURCES)
    a.add_argument('--canvas', default='1080x1920')
    a.add_argument('--fps', type=float, default=30)
    a.add_argument('--out')
    sub.add_parser('check').add_argument('format')
    sub.add_parser('feasibility').add_argument('format')
    a = sub.add_parser('plan-check')
    a.add_argument('format')
    a.add_argument('plan')
    a.add_argument('--approvals')
    args = p.parse_args(argv)

    def out(value: Json, code: int) -> int:
        print(json.dumps(value, indent=1, ensure_ascii=False))
        return code

    try:
        if args.cmd == 'from-sheet':
            match = re.fullmatch(r'(\d+)x(\d+)', args.canvas)
            if not match:
                raise InputError('--canvas is WIDTHxHEIGHT, like 1080x1920')
            fmt = from_sheets([load_sheet(s) for s in args.sheets], args.source,
                              (int(match.group(1)), int(match.group(2))), args.fps)
            if args.out:
                with open(args.out, 'w', encoding='utf-8') as f:
                    f.write(json.dumps(fmt, indent=1, ensure_ascii=False) + '\n')
            problems = check(fmt)
            return out({'ok': not problems, 'format': fmt, 'problems': problems}, 1 if problems else 0)
        fmt = load(args.format)
        if isinstance(fmt, dict) and isinstance(fmt.get('format'), dict):
            fmt = fmt['format']  # the whole record
        if args.cmd == 'check':
            problems = check(fmt)
            return out({'ok': not problems, 'problems': problems}, 1 if problems else 0)
        if args.cmd == 'feasibility':
            problems = feasibility(fmt)
            return out({'ok': not problems, 'problems': problems}, 1 if problems else 0)
        problems = check(fmt)
        if problems:
            return out({'ok': False, 'problems': problems}, 1)
        approvals = load(args.approvals) if args.approvals else []
        result = plan_check(fmt, load(args.plan), approvals if isinstance(approvals, list) else [])
        return out(result, 0 if result['ok'] else 1)
    except (OSError, InputError) as exc:
        print('error: ' + ' '.join(str(exc).split()), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
