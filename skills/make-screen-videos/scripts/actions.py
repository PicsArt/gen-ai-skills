#!/usr/bin/env python3
"""
Group a screen recording's events into actions, the things a viewer would name ("open the menu",
"type the title"), and suggest where its chapters start.

    python3 scripts/actions.py moments.json
    python3 scripts/actions.py < moments.json

The input is the result of `picsart_media_screen_moments`, whole, exactly as it returned it. To
change a number below, pass `{"moments": <that result>, "options": {...}}` instead.

It prints one JSON line, `{actions, chapters, waits}`:

- `actions`, in time order. Each is `{index, events, kind, at, settle, box, luma, chapter}`:
  - `events`, the event indices it plays, a scroll that leads to it included;
  - `kind`: `reveal` (drawn at once: a menu, a dialog), `cut` (a new page), `typing` (drawn over
    time in a small box: a field being typed into) or `progressive` (drawn over time in a large
    one: a page loading, a render);
  - `at` and `settle`, source seconds: where its first event starts, and where its last settles;
  - `box`, source px: where the screen responded, the union of its events' boxes, leaving out a
    scroll, and a cut when something else changed after it. It is what a push leans in on, since
    no event says where the pointer clicked;
  - `luma`, the mean luma of its largest change, 0-255;
  - `chapter`, the index of the suggested chapter it falls in.
- `chapters`, each `{index, at, action}`: a suggested start, at the first action and at each action
  that changes the whole page (a `cut`, or a change over `boundaryCover` of the content box: the
  rule the moments' proposed steps split on).
- `waits`, each `{start, end, after}`: a `waiting` dead range (a spinner, a caret blinking) and
  the action it follows, or -1 before the first. Marked, not dropped: the use case decides how
  much of each to show.

How events become actions:
- every `reveal`, `cut` and `progressive` event is an action of its own;
- a `scroll` joins the action that follows it, or the one before when nothing follows;
- an event that starts within `merge` seconds of the action before settling, in a box that
  overlaps that action's, joins it: one action, one push. A change of the whole page never joins
  the action before it: it opens the next one.

What it cannot know: where the pointer was, and whether a change is the user's action or the
app's own animation. Both are read on stills before the actions are shown to the user, and so is
whether two small actions are one thing the user would name.

Input it cannot group exits 1, with one line on stderr that says what is wrong.

Python 3.9 or later, the standard library only, offline.
"""
from __future__ import annotations

import json
import math
import sys
from typing import Any, Dict, List, Optional

from zoom import MERGE_WINDOW_S

Box = Dict[str, float]

# merge: seconds between an action settling and the next event starting, within which overlapping
# boxes share one action: the screen-recording-zoom skill's merge window, read from its zoom.py. boundaryCover: the share of the
# content box a change must cover to start a chapter (the moments' own step boundary). typingArea:
# the largest share of the content box a progressive event may cover and still be typing.
DEFAULT_ACTIONS = {'merge': MERGE_WINDOW_S, 'boundaryCover': 0.8, 'typingArea': 0.1}

EVENT_KINDS = ('cut', 'scroll', 'reveal', 'progressive')

USAGE = 'usage: actions.py [moments.json]; with no file, the input is read from stdin'


class InputError(ValueError):
    pass


def area(b: Box) -> float:
    return b['w'] * b['h']


def overlaps(a: Box, b: Box) -> bool:
    return min(a['x'] + a['w'], b['x'] + b['w']) > max(a['x'], b['x']) and min(a['y'] + a['h'], b['y'] + b['h']) > max(a['y'], b['y'])


def union(a: Box, b: Box) -> Box:
    x = min(a['x'], b['x'])
    y = min(a['y'], b['y'])
    return {'x': x, 'y': y, 'w': max(a['x'] + a['w'], b['x'] + b['w']) - x, 'h': max(a['y'] + a['h'], b['y'] + b['h']) - y}


def r3(v: float) -> float:
    """Three decimals, a half rounded up, as the screen tools round."""
    return math.floor(v * 1000 + 0.5) / 1000


def kind_of(e: Dict[str, Any], content: Box, o: Dict[str, float]) -> str:
    if e['kind'] != 'progressive':
        return e['kind']
    small = e.get('shape') == 'line' or area(e['box']) <= o['typingArea'] * area(content)
    return 'typing' if small else 'progressive'


def is_boundary(e: Dict[str, Any], content: Box, o: Dict[str, float]) -> bool:
    """A change of the whole page: a cut, or anything but a scroll over `boundaryCover` of the content."""
    return e['kind'] == 'cut' or (e['kind'] != 'scroll' and area(e['box']) >= o['boundaryCover'] * area(content))


def group(m: Dict[str, Any], options: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """The moments in, `{actions, chapters, waits}` out."""
    o = {**DEFAULT_ACTIONS, **(options or {})}
    content = m['content']
    events = sorted(m['events'], key=lambda e: (e['start'], e['index']))
    groups: List[Dict[str, Any]] = []
    scrolls: List[Dict[str, Any]] = []
    for e in events:
        if e['kind'] == 'scroll':
            scrolls.append(e)
            continue
        last = groups[-1] if groups else None
        if last is not None and not scrolls and not is_boundary(e, content, o) and e['start'] - last['settle'] <= o['merge'] + 1e-9 and overlaps(e['box'], last['extent']):
            last['events'].append(e)
            last['settle'] = max(last['settle'], e['settle'])
            if len(last['events']) == 2 and last['events'][0]['kind'] == 'cut':
                last['extent'] = dict(e['box'])
            else:
                last['extent'] = union(last['extent'], e['box'])
            continue
        groups.append({'lead': scrolls, 'events': [e], 'settle': e['settle'], 'extent': dict(e['box'])})
        scrolls = []
    if scrolls:
        if groups:
            # Nothing follows the scroll: it ends the last action.
            groups[-1]['events'] += scrolls
            groups[-1]['settle'] = max([groups[-1]['settle']] + [s['settle'] for s in scrolls])
        else:
            # Only scrolls: each is its own action, since the page moving is all there is.
            groups = [{'lead': [], 'events': [s], 'settle': s['settle'], 'extent': dict(s['box'])} for s in scrolls]

    actions: List[Dict[str, Any]] = []
    chapters: List[Dict[str, Any]] = []
    for i, g in enumerate(groups):
        played = sorted(g['lead'] + g['events'], key=lambda e: (e['start'], e['index']))
        main = max([e for e in g['events'] if e['kind'] != 'scroll'] or g['events'], key=lambda e: e['mass'])
        # The push leans in on what the page showed after it changed, not on the whole new page.
        shown = [e for e in g['events'] if e['kind'] not in ('cut', 'scroll')] or g['events']
        box = dict(shown[0]['box'])
        for e in shown[1:]:
            box = union(box, e['box'])
        if not chapters or any(is_boundary(e, content, o) for e in g['events']):
            chapters.append({'index': len(chapters), 'at': r3(played[0]['start']), 'action': i})
        actions.append({
            'index': i,
            'events': [e['index'] for e in played],
            'kind': kind_of(main, content, o),
            'at': r3(played[0]['start']),
            'settle': r3(max(e['settle'] for e in played)),
            'box': box,
            'luma': main['luma'],
            'chapter': len(chapters) - 1,
        })

    waits = []
    for d in m.get('dead') or []:
        if d['kind'] != 'waiting':
            continue
        before = [a['index'] for a in actions if a['at'] <= d['start'] + 1e-6]
        waits.append({'start': d['start'], 'end': d['end'], 'after': before[-1] if before else -1})
    return {'actions': actions, 'chapters': chapters, 'waits': waits}


def _number(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def _box(v: Any, name: str) -> Box:
    if not isinstance(v, dict) or not all(_number(v.get(k)) for k in ('x', 'y')) or not all(_number(v.get(k)) and v[k] > 0 for k in ('w', 'h')):
        raise InputError(f'{name} must be {{x, y, w, h}}, with a positive width and height')
    return {'x': v['x'], 'y': v['y'], 'w': v['w'], 'h': v['h']}


def check(data: Any) -> Dict[str, Any]:
    """The input, checked: `{moments, options}`."""
    if not isinstance(data, dict):
        raise InputError('the input must be one JSON object: the picsart_media_screen_moments result')
    if 'moments' in data:
        m, options = data['moments'], data.get('options')
    else:
        m, options = data, None
    if not isinstance(m, dict):
        raise InputError('moments must be the picsart_media_screen_moments result, whole')
    if options is not None and (not isinstance(options, dict) or not all(k in DEFAULT_ACTIONS and _number(v) and v >= 0 for k, v in options.items())):
        raise InputError(f"options must be an object of numbers, 0 or more, among {', '.join(DEFAULT_ACTIONS)}")
    _box(m.get('content'), 'content')
    events = m.get('events')
    if not isinstance(events, list):
        raise InputError('events must be a list: pass the picsart_media_screen_moments result whole')
    for i, e in enumerate(events):
        where = f'events[{i}]'
        if not isinstance(e, dict):
            raise InputError(f'{where} must be an object')
        if e.get('kind') not in EVENT_KINDS:
            raise InputError(f"{where}.kind must be one of {', '.join(EVENT_KINDS)}")
        for k in ('index', 'start', 'settle', 'mass', 'luma'):
            if not _number(e.get(k)):
                raise InputError(f'{where}.{k} must be a number')
        _box(e.get('box'), f'{where}.box')
    dead = m.get('dead', [])
    if not isinstance(dead, list) or not all(isinstance(d, dict) and _number(d.get('start')) and _number(d.get('end')) and d.get('kind') in ('still', 'waiting') for d in dead):
        raise InputError("dead must be a list of {start, end, kind}, kind 'still' or 'waiting'")
    return {'moments': m, 'options': options}


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
        checked = check(json.loads(text))
        out = group(checked['moments'], checked['options'])
    except json.JSONDecodeError as err:
        return fail(f'the input is not JSON: {err}')
    except InputError as err:
        return fail(str(err))
    sys.stdout.buffer.write((json.dumps(out, separators=(',', ':')) + '\n').encode('utf-8'))
    return 0


def fail(reason: str, code: int = 1) -> int:
    sys.stderr.write('actions.py: ' + ' '.join(reason.split()) + '\n')
    return code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
