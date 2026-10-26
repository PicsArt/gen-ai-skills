#!/usr/bin/env python3
"""
Build a screen tutorial's scene from its outline and the recording's moments.

    python3 scripts/tutorial_scene.py input.json [--explain]
    python3 scripts/tutorial_scene.py < input.json

The input is one JSON object, `{spec, moments, transcript?, lines?}` (references/outline.md):
`spec` the approved outline, `moments` the result of `picsart_media_screen_moments`, whole,
`transcript` the `picsart_media_transcribe` result when the user's own voice is kept, and `lines`
the generated voice lines, `{step, url, duration}`, when a voice-over is.

It prints one JSON line, `{scene, duration, timeline, chapters, diagnostics}`, and exits 0, also
when a diagnostic is an error: the diagnostics say what to change in the outline.
- `scene`: a 1920x1080 scene: the finished result on a card, then a title card at each chapter
  and its steps, each step the whole recording pushed in on every action and zoomed back out;
- `timeline`: the intro, each chapter card and each step, in scene seconds, a step with the band
  its line sits in (`bottom` or `top`, where its captions go too), its voice line's span, and the
  real length of a wait it shows sped up;
- `chapters`: the lines to paste into a video description, `MM:SS Title`, the first at `00:00`;
- `diagnostics`: each `{level, code, step?, message, fix}`, the fix naming the outline field.
With `--explain` the line also carries `explain`: the actions, and each step's edit and zoom.

It groups the events into actions with the screen-recording-analysis skill's `actions.py`, frames and pushes
with the screen-recording-layouts skill's `framing.py` and `panels.py` and the screen-recording-zoom skill's `zoom.py`, all
of which ship beside it. Input it cannot build from exits 1, with one line on stderr that says
what is wrong.

Python 3.9 or later, the standard library only, offline.
"""
from __future__ import annotations

import json
import math
import sys
from typing import Any, Dict, List

from _tutorial_edit import EDIT, _first_output, plan
from _tutorial_input import InputError, parse, segments_of
from _tutorial_layout import FRAME, band_for, compose, whole_source
from actions import check as check_moments
from actions import DEFAULT_ACTIONS, group
from framing import fit_base
from zoom import DEFAULT_ZOOM, zoom_track

USAGE = 'usage: tutorial_scene.py [input.json] [--explain]; with no file, the input is read from stdin'

# The tutorial's pacing (references/outline.md, Pacing). intro: the finished result, the first
# 5 s. card: a chapter's title card (a starting number, no source). The zoom: the push starts
# 0.5 s before each action, a 1.0 s zoom out after its hold, and a peak that reads the response's
# text at 30 px or more.
INTRO = 5.0
CARD = 2.0
ZOOM = {'delay': -0.5, 'zoomOut': EDIT['zoomOut'], 'textFloor': 30, 'crop': 0}
# What a video description's chapters need: at least three, each at least 10 s.
CHAPTERS_MIN = 3
CHAPTER_MIN_LENGTH = 10
# A chapter title's words and a step line's characters: the screen-recording-layouts skill's landscape reference.
TITLE_WORDS = 5
LINE_CHARS = 60
LONGEST = 300


def page_wide(box: Dict[str, float], content: Dict[str, float]) -> bool:
    """A box over most of the content: the page itself changed (the actions' own chapter rule)."""
    return box['w'] * box['h'] >= DEFAULT_ACTIONS['boundaryCover'] * content['w'] * content['h']


def stamp(t: float) -> str:
    s = int(math.floor(t + 1e-6))
    return f'{s // 60:02d}:{s % 60:02d}'


def build(data: Dict[str, Any], explain: bool = False) -> Dict[str, Any]:
    spec = data['spec']
    m = data['moments']
    src = {'w': m['source']['w'], 'h': m['source']['h']}
    src_len = min(m['source']['duration'], spec['duration']) if spec.get('duration') is not None else m['source']['duration']
    check_moments(m)
    grouped = group(m)
    actions = grouped['actions']
    steps_in = spec['steps']
    for i, s in enumerate(steps_in):
        bad = [a for a in s['actions'] if a >= len(actions)]
        if bad:
            raise InputError(f'spec.steps[{i}].actions: no action {bad[0]} (scripts/actions.py found {len(actions)})')
        late = [a for a in s['actions'] if actions[a]['at'] >= src_len]
        if late:
            raise InputError(f"spec.steps[{i}].actions: action {late[0]} starts at {actions[late[0]]['at']:g} s, past the uploaded copy's end at {src_len:g} s")
        truncated = [a for a in s['actions'] if actions[a]['settle'] > src_len + 1e-6]
        if truncated:
            a = truncated[0]
            raise InputError(f"spec.steps[{i}].actions: action {a} settles at {actions[a]['settle']:g} s, past the uploaded copy's end at {src_len:g} s")
    flat = [a for s in steps_in for a in s['actions']]
    if len(set(flat)) != len(flat) or flat != sorted(flat):
        raise InputError('spec.steps: each action belongs to one step, and the steps keep the recording\'s order')

    narration = spec['narration']
    speech = segments_of(data['transcript']) if narration == 'own' else []
    lines = {l['step']: l for l in data.get('lines') or []}
    edits = plan(actions, steps_in, src_len, m.get('dead') or [], speech, {k: v['duration'] for k, v in lines.items()})

    rest_box = whole_source(src, m['content'])
    contained = fit_base(src, FRAME)
    panel = {'x': (FRAME['w'] - src['w'] * contained) / 2, 'y': (FRAME['h'] - src['h'] * contained) / 2, 'w': src['w'] * contained, 'h': src['h'] * contained}
    built = []
    chapter_of = {}
    for j, c in enumerate(spec['chapters']):
        chapter_of[[s['id'] for s in steps_in].index(c['from'])] = j
    chapter = 0
    for k, (s, edit) in enumerate(zip(steps_in, edits)):
        chapter = chapter_of.get(k, chapter)
        acts = [actions[i] for i in s['actions']]
        # A change of the whole page ends the preceding push before the new page appears.
        foci = []
        resets = []
        for a in acts:
            at = edit['at'][str(a['index'])]
            events = [e for e in m['events'] if e['index'] in a['events']]
            boundaries = [e for e in events if e['kind'] == 'cut' or page_wide(e['box'], m['content'])]
            if not s.get('box'):
                resets.extend(_first_output(edit['pieces'], e['start']) for e in boundaries)
            if s.get('box') or not page_wide(a['box'], m['content']):
                response = [e for e in events if e not in boundaries and e['kind'] != 'scroll']
                if boundaries and response:
                    at = _first_output(edit['pieces'], response[0]['start'])
                foci.append({'at': at, 'box': s.get('box') or a['box'], 'luma': a['luma']})
        zoom = tutorial_zoom(src, panel, rest_box, foci, resets, edit)
        band = band_for(src, [f['box'] for f in foci] or [a['box'] for a in acts], zoom, len(s['text']), foci)
        built.append({'id': s['id'], 'text': s['text'], 'edit': edit, 'zoom': zoom, 'band': band, 'chapter': chapter})
    chapters = [{'title': c['title'], 'step': [s['id'] for s in steps_in].index(c['from'])} for c in spec['chapters']]
    composed = compose(spec, src, src_len, built, chapters, lines, INTRO, CARD)
    timeline = composed['timeline']
    description = describe(timeline, composed['duration'])
    diagnostics = diagnose(spec, actions, built, edits, timeline, description, composed['duration'], speech, lines)
    out = {'scene': composed['scene'], 'duration': composed['duration'], 'timeline': timeline, 'chapters': [d['line'] for d in description], 'diagnostics': diagnostics}
    if explain:
        out['explain'] = {'actions': actions, 'waits': grouped['waits'], 'steps': [{'id': b['id'], 'edit': b['edit'], 'zoom': b['zoom']} for b in built]}
    return out


def tutorial_zoom(src, panel, rest_box, foci, resets, edit):
    """Push between page changes, returning to rest before each new page appears."""
    track = {'scale': [], 'position': []}
    start = 0
    for end in sorted(set(resets)) + [edit['duration']]:
        if end <= start:
            continue
        duration = end - start
        options = dict(ZOOM)
        selected = [dict(f, at=f['at'] - start) for f in foci if start <= f['at'] < end]
        requested = selected
        if end != edit['duration']:
            # Leave room for both ramps; a brief action is safer shown whole.
            selected = [f for f in selected if max(0.05, f['at'] + ZOOM['delay']) + 2 * DEFAULT_ZOOM['minRamp'] <= duration]
            if selected:
                # Each ramp waits for the preceding one to land, then leaves 0.05 s before
                # the next; reserve one more ramp for the return to rest.
                n = len(selected)
                ramp = min([1.0] + [(duration - max(0.05, f['at'] + ZOOM['delay']) - 0.05 * (n - i - 1)) / (n - i + 1)
                                    for i, f in enumerate(selected)])
                if ramp >= DEFAULT_ZOOM['minRamp'] - 1e-9:
                    options['ramp'] = options['zoomOut'] = math.floor((ramp + 1e-9) * 1000) / 1000
                else:
                    selected = []
        if selected:
            selected[-1]['until'] = (edit['holdEnd'] - start if end == edit['duration'] else duration - options['zoomOut'])
        part = zoom_track(src, FRAME, panel, rest_box, selected, duration, options)
        if end != edit['duration'] and any(part[name][-1]['value'] != part[name][0]['value'] for name in ('scale', 'position')):
            part = zoom_track(src, FRAME, panel, rest_box, [], duration, options)
            selected = []
        if requested and len(selected) < len(requested):
            part['skipped'] = {'at': requested[-1]['at'], 'room': round(duration - requested[-1]['at'], 3)}
        for name in ('scale', 'position'):
            for key in part[name]:
                key['time'] = round(key['time'] + start, 3)
                if track[name] and track[name][-1]['time'] == key['time']:
                    track[name].pop()
                track[name].append(key)
        track['textPx'] = part['textPx']
        if part.get('skipped'):
            track['skipped'] = dict(part['skipped'], at=round(part['skipped']['at'] + start, 3))
        start = end
    if all(k['value'] == track['scale'][0]['value'] for k in track['scale']) and all(k['value'] == track['position'][0]['value'] for k in track['position']):
        track['scale'] = [{'time': 0, 'value': track['scale'][0]['value']}]
        track['position'] = [{'time': 0, 'value': track['position'][0]['value']}]
    return track


def describe(timeline: List[Dict[str, Any]], duration: float) -> List[Dict[str, Any]]:
    """
    The description's chapters, one per chapter card. The first starts at 00:00 and covers the
    intro: at 5 s the intro is too short to be a chapter of its own.
    """
    cards = [e for e in timeline if e['kind'] == 'chapter']
    out = [{'title': c['title'], 'at': 0 if k == 0 else c['start']} for k, c in enumerate(cards)]
    for k, d in enumerate(out):
        end = out[k + 1]['at'] if k + 1 < len(out) else duration
        d['length'] = round(end - d['at'], 3)
        d['line'] = f"{stamp(d['at'])} {d['title']}"
    return out


def diagnose(spec, actions, built, edits, timeline, description, duration, speech, lines) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []

    def add(level: str, code: str, message: str, fix: str, step: str = None) -> None:
        d = {'level': level, 'code': code}
        if step is not None:
            d['step'] = step
        d['message'] = message
        d['fix'] = fix
        out.append(d)

    used = {a for s in spec['steps'] for a in s['actions']}
    left = [a['index'] for a in actions if a['index'] not in used]
    if left:
        add('warning', 'actions_left_out', f"actions {', '.join(str(a) for a in left)} are in no step; a tutorial keeps every step the recording shows",
            'add each to the step it belongs to in spec.steps, unless a still showed it is the app\'s own animation: then say so in the outline')
    for i, (s, b, edit) in enumerate(zip(spec['steps'], built, edits)):
        field = f'spec.steps[{i}]'
        if edit.get('holdWaitingRange'):
            add('error', 'hold_waiting_range', f"{s['id']}: no settled non-waiting frames are available in its source region; the hold uses the last available waiting frames",
                f'adjust {field}.actions to include a settled response outside the wait, or tell the user at REVIEW', s['id'])
        # The voice is never sped: a speech span inside a clip that plays at another speed.
        for p in edit['pieces']:
            overlapping = [sp for sp in speech if sp['start'] < p['srcOut'] - 1e-6 and sp['end'] > p['srcIn'] + 1e-6]
            replayed = p['role'] == 'hold' and all(any(abs(q['speed'] - 1) <= 1e-3 and q['role'] != 'hold'
                and q['srcIn'] <= max(p['srcIn'], sp['start']) + 1e-6 and q['srcOut'] >= min(p['srcOut'], sp['end']) - 1e-6
                for other in edits for q in other['pieces']) for sp in overlapping)
            if abs(p['speed'] - 1) > 1e-3 and overlapping and not replayed:
                add('error', 'speech_sped', f"{s['id']}: the user's voice plays at {p['speed']}x between {p['srcIn']} and {p['srcOut']} s", f'split {field}.actions so the speech falls inside one step', s['id'])
                break
        if edit.get('spans'):
            before = spec['steps'][i - 1]['id']
            add('warning', 'speech_spans', f"{s['id']}: the user's voice runs over its action, so the action plays at 1x under it, in step {before}", f"put {field}.actions into spec.steps[{i - 1}].actions, one step for both, or keep them and tell the user at REVIEW", s['id'])
        line = lines.get(s['id'])
        if line is not None and line['duration'] > edit['duration'] + 1e-6:
            add('error', 'line_cut', f"{s['id']}: its voice line runs {line['duration']} s, past the step's {edit['duration']} s", f"shorten the line for {s['id']} and generate it again", s['id'])
        peak = max(k['value'][0] for k in b['zoom']['scale']) / b['zoom']['scale'][0]['value'][0]
        reads = b['zoom']['textPx'] * peak
        if len(b['zoom']['scale']) > 1 and reads < ZOOM['textFloor'] - 0.5:
            add('warning', 'text_small', f"{s['id']}: the response's text reads at about {round(reads)} px at the push's peak, under {ZOOM['textFloor']}",
                f'set {field}.box to the part of the response the viewer must read, or check a still of it: a box that small may still read', s['id'])
        if b['zoom'].get('skipped'):
            add('warning', 'push_skipped', f"{s['id']}: the push onto its last action had no room", f'merge {field} into the step before it, or give it its own step', s['id'])
        if any(len(t) > LINE_CHARS for t in s['text']):
            add('warning', 'line_long', f"{s['id']}: a line of its text runs past about {LINE_CHARS} characters", f'shorten {field}.text, or split it into two lines', s['id'])
    for j, c in enumerate(spec['chapters']):
        if len(c['title'].split()) > TITLE_WORDS:
            add('warning', 'title_long', f"chapter {j}: its title runs past {TITLE_WORDS} words", f'shorten spec.chapters[{j}].title')
    if len(description) < CHAPTERS_MIN:
        add('warning', 'chapters_few', f'{len(description)} chapters; a description needs at least {CHAPTERS_MIN} for them to show as chapters', 'split a chapter in spec.chapters where the work changes')
    for d in description:
        if d['length'] < CHAPTER_MIN_LENGTH:
            add('warning', 'chapter_short', f"chapter \"{d['title']}\" lasts {d['length']} s; each needs at least {CHAPTER_MIN_LENGTH} s to show as one", 'merge it into the chapter before or after it in spec.chapters')
    if duration > LONGEST:
        add('warning', 'long', f'the tutorial runs {duration} s, past about {LONGEST // 60} min', 'tell the user, and offer to leave a chapter for a second video')
    return out


def main(argv: List[str]) -> int:
    explain = '--explain' in argv
    rest = [a for a in argv if a != '--explain']
    if len(rest) > 1 or any(a.startswith('-') for a in rest):
        return fail(USAGE, 2)
    try:
        if rest:
            with open(rest[0], encoding='utf-8-sig') as f:
                text = f.read()
        else:
            text = sys.stdin.buffer.read().decode('utf-8-sig')
    except (OSError, UnicodeDecodeError) as err:
        return fail(f'cannot read the input: {err}')
    try:
        out = build(parse(text), explain)
    except InputError as err:
        return fail(str(err))
    except ValueError as err:
        return fail(str(err))
    except (KeyError, IndexError, TypeError, ZeroDivisionError, OverflowError) as err:
        return fail(f'cannot build from this input: {type(err).__name__} {err}')
    sys.stdout.buffer.write((json.dumps(out, separators=(',', ':'), ensure_ascii=False) + '\n').encode('utf-8'))
    return 0


def fail(reason: str, code: int = 1) -> int:
    sys.stderr.write('tutorial_scene.py: ' + ' '.join(reason.split()) + '\n')
    return code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
