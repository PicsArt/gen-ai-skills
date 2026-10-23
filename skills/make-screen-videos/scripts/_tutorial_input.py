"""
The script's input, read and checked: `{spec, moments, transcript?, lines?}`. A field the builder
reads that is missing or of the wrong type stops the build here, with one line naming it, rather
than as a traceback from deep in the build. A field set to `null` reads as left out.
"""
from __future__ import annotations

import json
import math
from typing import Any, Dict, List
from style import StyleError, resolve

NARRATION = ('text', 'voice-over', 'own')
CLIPS = ('mask', 'nest')
RESERVED = ('intro',)


class InputError(ValueError):
    """Input the builder cannot build from; the message is the one line the script prints."""


def parse(text: str) -> Dict[str, Any]:
    try:
        data = json.loads(text, parse_constant=_constant)
    except ValueError as err:
        raise InputError(f'the input is not JSON: {err}') from None
    check(data)
    return data


def _constant(name: str) -> float:
    raise InputError(f'the input is not JSON: {name} is not a JSON number')


def number(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def _num(v: Any, where: str, positive: bool = False) -> float:
    if not number(v) or v < 0 or (positive and v <= 0):
        raise InputError(f"{where}: must be a number{', more than 0' if positive else ', 0 or more'}")
    return v


def _obj(v: Any, where: str) -> Dict[str, Any]:
    if not isinstance(v, dict):
        raise InputError(f'{where}: must be an object')
    return v


def _str(v: Any, where: str) -> str:
    if not isinstance(v, str) or not v.strip():
        raise InputError(f'{where}: must be a non-empty string')
    return v


def _lines(v: Any, where: str, most: int) -> List[str]:
    if not isinstance(v, list) or not v or len(v) > most or not all(isinstance(x, str) and x.strip() for x in v):
        raise InputError(f'{where}: must be a list of 1 to {most} non-empty lines')
    return v


def _box(v: Any, where: str) -> Dict[str, float]:
    if not isinstance(v, dict) or not all(number(v.get(k)) for k in ('x', 'y')) or not all(number(v.get(k)) and v[k] > 0 for k in ('w', 'h')):
        raise InputError(f'{where}: must be {{x, y, w, h}}, with a positive width and height')
    return v


def check(data: Any) -> None:
    _obj(data, 'the input')
    m = _obj(data.get('moments'), 'moments')
    _moments(m)
    spec = _obj(data.get('spec'), 'spec')
    _spec(spec, m)
    narration = spec['narration']
    if narration == 'own':
        _transcript(data.get('transcript'))
    elif data.get('transcript') is not None:
        raise InputError("transcript: only with spec.narration 'own', the user's own voice kept")
    if narration == 'voice-over':
        _voice_lines(data.get('lines'), spec)
    elif data.get('lines') is not None:
        raise InputError("lines: only with spec.narration 'voice-over'")


def _moments(m: Dict[str, Any]) -> None:
    source = _obj(m.get('source'), 'moments.source')
    for k in ('w', 'h', 'duration'):
        _num(source.get(k), f'moments.source.{k}', positive=True)
    info = m.get('input')
    if info is None:
        raise InputError('moments.input: missing; pass the picsart_media_screen_moments result whole')
    _obj(info, 'moments.input')
    if info.get('orientation') != 'landscape':
        raise InputError(f"moments.input.orientation: a tutorial is built from a landscape recording, and this one is {info.get('orientation')!r}")
    if info.get('edited') is not False:
        raise InputError('moments.input.edited: a tutorial is built from a raw recording, and this one is already edited')
    _box(m.get('content'), 'moments.content')
    if not isinstance(m.get('events'), list) or not isinstance(m.get('dead', []), list):
        raise InputError('moments.events and moments.dead: must be lists; pass the picsart_media_screen_moments result whole')


def _spec(spec: Dict[str, Any], m: Dict[str, Any]) -> None:
    _style(spec)
    _str(spec.get('uri'), 'spec.uri')
    _str(spec.get('font'), 'spec.font')
    _lines(spec.get('title'), 'spec.title', 2)
    if spec.get('narration') not in NARRATION:
        raise InputError(f"spec.narration: must be one of {', '.join(repr(n) for n in NARRATION)}")
    if spec.get('clip') is not None and spec['clip'] not in CLIPS:
        raise InputError("spec.clip: must be 'mask' or 'nest'")
    if spec.get('duration') is not None:
        _num(spec['duration'], 'spec.duration', positive=True)
    intro = _obj(spec.get('intro'), 'spec.intro')
    _num(intro.get('at'), 'spec.intro.at')
    # The uploaded copy can end before the analysed file does.
    length = min(m['source']['duration'], spec['duration']) if spec.get('duration') is not None else m['source']['duration']
    if intro['at'] >= length:
        raise InputError(f"spec.intro.at: {intro['at']:g} s is past the uploaded copy's end at {length:g} s")
    _box(intro.get('box'), 'spec.intro.box')
    steps = spec.get('steps')
    if not isinstance(steps, list) or not steps:
        raise InputError('spec.steps: must be a list of at least one step')
    ids = []
    for i, s in enumerate(steps):
        where = f'spec.steps[{i}]'
        _obj(s, where)
        id_ = _str(s.get('id'), f'{where}.id')
        if id_ in RESERVED or id_.startswith('chapter_') or id_ in ids:
            raise InputError(f"{where}.id: {id_!r} is taken; use an id of your own, once")
        ids.append(id_)
        acts = s.get('actions')
        if not isinstance(acts, list) or not acts or not all(isinstance(a, int) and not isinstance(a, bool) and a >= 0 for a in acts):
            raise InputError(f'{where}.actions: must be a list of action indices from scripts/actions.py')
        _lines(s.get('text'), f'{where}.text', 2)
        if s.get('box') is not None:
            _box(s['box'], f'{where}.box')
        for k in ('typed', 'wait'):
            if s.get(k) is not None and not isinstance(s[k], bool):
                raise InputError(f'{where}.{k}: must be true or false')
    chapters = spec.get('chapters')
    if not isinstance(chapters, list) or not chapters:
        raise InputError('spec.chapters: must be a list of at least one chapter')
    froms = []
    for j, c in enumerate(chapters):
        where = f'spec.chapters[{j}]'
        _obj(c, where)
        _str(c.get('title'), f'{where}.title')
        if c.get('from') not in ids:
            raise InputError(f'{where}.from: must be the id of the step the chapter opens on')
        froms.append(ids.index(c['from']))
    if froms[0] != 0:
        raise InputError(f'spec.chapters[0].from: must be the first step, {ids[0]!r}')
    if any(b <= a for a, b in zip(froms, froms[1:])):
        raise InputError('spec.chapters: must open on steps in step order, one chapter per step at most')


def _transcript(t: Any) -> None:
    if isinstance(t, dict) and isinstance(t.get('transcript'), dict):
        t = t['transcript']
    segments = t.get('segments') if isinstance(t, dict) else None
    if not isinstance(segments, list):
        raise InputError("transcript: must be the picsart_media_transcribe result, or its transcript, with spec.narration 'own'")
    for k, seg in enumerate(segments):
        if not isinstance(seg, dict) or not number(seg.get('start')) or not number(seg.get('end')) or seg['end'] < seg['start']:
            raise InputError(f'transcript.segments[{k}]: must have a start and an end, in source seconds')


def _voice_lines(lines: Any, spec: Dict[str, Any]) -> None:
    if not isinstance(lines, list):
        raise InputError("lines: must be a list of voice lines, {step, url, duration}, with spec.narration 'voice-over'")
    ids = [s['id'] for s in spec['steps']]
    seen = set()
    for k, line in enumerate(lines):
        where = f'lines[{k}]'
        _obj(line, where)
        if line.get('step') not in ids or line['step'] in seen:
            raise InputError(f'{where}.step: must name a step in spec.steps, once')
        seen.add(line['step'])
        _str(line.get('url'), f'{where}.url')
        _num(line.get('duration'), f'{where}.duration', positive=True)
    missing = [i for i in ids if i not in seen]
    if missing:
        raise InputError(f"lines: no voice line for {', '.join(repr(i) for i in missing)}; every step has one")


def segments_of(t: Any) -> List[Dict[str, float]]:
    """The transcript's speech spans, source seconds, in time order."""
    if isinstance(t, dict) and isinstance(t.get('transcript'), dict):
        t = t['transcript']
    return sorted(({'start': s['start'], 'end': s['end']} for s in t['segments'] if s['end'] > s['start']), key=lambda s: s['start'])


def _style(spec: Dict[str, Any], where: str = 'spec') -> None:
    """A style id (the visual-style skill's style.py) and a brand, resolved to tokens in place."""
    if spec.get('style') is None:
        if spec.get('brand') is not None:
            raise InputError(f'{where}.brand: a brand goes onto a style; set {where}.style too')
        return
    if spec.get('brand') is not None and not isinstance(spec['brand'], dict):
        raise InputError(f'{where}.brand: must be an object of colours by role')
    try:
        spec['style'] = resolve(spec['style'], spec.get('brand'))
    except StyleError as err:
        raise InputError(f'{where}.{err}') from None
