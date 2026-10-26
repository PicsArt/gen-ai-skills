"""
The script's input, read and checked: `{kind, spec, moments}`. A field the builder reads that is
missing or of the wrong type stops the build here, with one line naming it, rather than as a
traceback from deep in the build.

Numbers are read as JavaScript reads them, every one a float, so the arithmetic lands on the digits
the TypeScript builder printed. A field set to `null` reads as left out.
"""
from __future__ import annotations

import json
import math
import re
from typing import Any, Dict, List, Optional
from urllib.parse import urlsplit

from _js import dumps
from style import StyleError, resolve

KINDS = ('promo', 'timelapse')


class InputError(ValueError):
    """Input the builder cannot build from; the message is the one line the script prints."""


def parse(text: str) -> Dict[str, Any]:
    """The input, parsed and checked."""
    try:
        data = json.loads(text, parse_int=float, parse_constant=_constant)
    except ValueError as err:
        raise InputError(f'the input is not JSON: {err}') from None
    check(data)
    return data


def _constant(name: str) -> float:
    raise InputError(f'the input is not JSON: {name} is not a JSON number')


def check(data: Any) -> None:
    _object(data, 'the input')
    kind = data.get('kind')
    if kind not in KINDS:
        raise InputError(f"kind: must be 'promo' or 'timelapse', not {_shown(kind)}")
    _moments(_object(data.get('moments'), 'moments'), kind)
    spec = _object(data.get('spec'), 'spec')
    _style(spec)
    if kind == 'promo':
        _promo(spec, data['moments'])
    else:
        _timelapse(spec)


def _moments(m: Dict[str, Any], kind: str) -> None:
    source = _object(m.get('source'), 'moments.source')
    for k in ('w', 'h', 'duration'):
        _number(source.get(k), f'moments.source.{k}', positive=True)
    _number(_object(m.get('analysis'), 'moments.analysis').get('fps'), 'moments.analysis.fps', positive=True)
    info = m.get('input')
    if info is None:
        raise InputError('moments.input: missing; pass the picsart_media_screen_moments result whole, not the activity alone')
    _object(info, 'moments.input')
    if info.get('orientation') not in ('landscape', 'portrait', 'square'):
        raise InputError(f"moments.input.orientation: must be 'landscape', 'portrait' or 'square', not {_shown(info.get('orientation'))}")
    _boolean(info.get('edited'), 'moments.input.edited')
    _numbers(info.get('cuts'), 'moments.input.cuts')
    _string(m.get('tier'), 'moments.tier')
    _string(m.get('tierReason'), 'moments.tierReason')
    _box(m.get('content'), 'moments.content')
    if m.get('work') is not None:
        _box(m['work'], 'moments.work')
    events = _list(m.get('events'), 'moments.events')
    for i, e in enumerate(events):
        where = f'moments.events[{i}]'
        _object(e, where)
        if e.get('index') != i:
            raise InputError(f'{where}.index: must be {i}, its place in events')
        if e.get('kind') not in ('cut', 'scroll', 'reveal', 'progressive'):
            raise InputError(f"{where}.kind: must be 'cut', 'scroll', 'reveal' or 'progressive', not {_shown(e.get('kind'))}")
        for k in ('start', 'settle', 'mass', 'luma'):
            _number(e.get(k), f'{where}.{k}')
        _box(e.get('box'), f'{where}.box')
        _box(e.get('core'), f'{where}.core')
    for i, d in enumerate(_list(m.get('dead'), 'moments.dead')):
        _object(d, f'moments.dead[{i}]')
        _number(d.get('end'), f'moments.dead[{i}].end')
        _string(d.get('kind'), f'moments.dead[{i}].kind')
    steps = _list(m.get('steps'), 'moments.steps')
    if kind == 'promo':
        for i, s in enumerate(steps):
            where = f'moments.steps[{i}]'
            _object(s, where)
            _indices(s.get('events'), f'{where}.events', len(events))
            _indices(s.get('leadIn'), f'{where}.leadIn', len(events))
            _index(s.get('result'), f'{where}.result', len(events))
            if s.get('boundary') is not None:
                _index(s['boundary'], f'{where}.boundary', len(events))
            if s.get('subject') is not None:
                _box(s['subject'], f'{where}.subject')


def _promo(spec: Dict[str, Any], m: Dict[str, Any]) -> None:
    _common(spec)
    _number(spec.get('target'), 'spec.target', positive=True)
    hook = _object(spec.get('hook'), 'spec.hook')
    _strings(hook.get('title'), 'spec.hook.title')
    _string(hook.get('step'), 'spec.hook.step')
    _optional_number(hook.get('duration'), 'spec.hook.duration', positive=True)
    steps = _list(spec.get('steps'), 'spec.steps')
    if not steps:
        raise InputError('spec.steps: must have at least one step')
    count = len(m['events'])
    seen = set()
    for i, s in enumerate(steps):
        where = f'spec.steps[{i}]'
        _object(s, where)
        _string(s.get('id'), f'{where}.id')
        if s['id'] in ('hook', 'outro'):
            raise InputError(f'{where}.id: "{s["id"]}" names the promo\'s own {s["id"]}; give the step another id')
        if s['id'] in ('grid_0', 'grid_1', 'grid_2', 'grid_3'):
            raise InputError(f'{where}.id: "{s["id"]}" names the promo\'s own outro grid; give the step another id')
        if s['id'] in seen:
            raise InputError(f'{where}.id: "{s["id"]}" is already used by another step; give the step another id')
        seen.add(s['id'])
        if s.get('step') is not None:
            _number(s['step'], f'{where}.step')
        if s.get('events') is not None:
            _indices(s['events'], f'{where}.events', count)
        if s.get('result') is not None:
            _index(s['result'], f'{where}.result', count)
        for k in ('prompt', 'label'):
            if s.get(k) is not None:
                _strings(s[k], f'{where}.{k}')
        for k in ('from', 'to'):
            _optional_number(s.get(k), f'{where}.{k}')
    if spec.get('sfx') is not None:
        _sfx(_object(spec['sfx'], 'spec.sfx'))
    outro = _object(spec.get('outro'), 'spec.outro')
    _strings(outro.get('cta'), 'spec.outro.cta')
    for i, id_ in enumerate(_list(outro.get('steps'), 'spec.outro.steps')):
        _string(id_, f'spec.outro.steps[{i}]')
    _optional_number(outro.get('duration'), 'spec.outro.duration', positive=True)


def _sfx(sfx: Dict[str, Any]) -> None:
    for name in ('push', 'outro'):
        if sfx.get(name) is None:
            continue
        sound = _object(sfx[name], f'spec.sfx.{name}')
        url = sound.get('url')
        if not isinstance(url, str) or not url.startswith('https://') or not urlsplit(url).hostname:
            raise InputError(f'spec.sfx.{name}.url: must be an https:// URL a Picsart tool returned, not {_shown(url)}')
        _number(sound.get('duration'), f'spec.sfx.{name}.duration', positive=True)
    volume = sfx.get('volume')
    if volume is not None:
        _number(volume, 'spec.sfx.volume')
        if not 0 <= volume <= 100:
            raise InputError(f'spec.sfx.volume: must be a volume percent from 0 to 100, not {_shown(volume)}')


def _timelapse(spec: Dict[str, Any]) -> None:
    _common(spec)
    if spec.get('sfx') is not None:
        raise InputError('spec.sfx: only a promo places sound effects; leave it out of a timelapse')
    _optional_number(spec.get('target'), 'spec.target', positive=True)
    process = _object(spec.get('process'), 'spec.process')
    for k in ('from', 'to', 'count'):
        _number(process.get(k), f'spec.process.{k}')
    for k in ('shown', 'speed'):
        _optional_number(process.get(k), f'spec.process.{k}', positive=True)
    if process.get('box') is not None:
        _box(process['box'], 'spec.process.box')
    labels = _list(spec.get('labels'), 'spec.labels')
    if not labels:
        raise InputError('spec.labels: must have at least one chapter')
    for i, label in enumerate(labels):
        where = f'spec.labels[{i}]'
        _object(label, where)
        _number(label.get('from'), f'{where}.from')
        _strings(label.get('text'), f'{where}.text')
        if label.get('box') is not None:
            _box(label['box'], f'{where}.box')
    reveal = _object(spec.get('reveal'), 'spec.reveal')
    _number(reveal.get('at'), 'spec.reveal.at')
    _optional_number(reveal.get('until'), 'spec.reveal.until')
    _optional_number(reveal.get('hold'), 'spec.reveal.hold', positive=True)
    if reveal.get('box') is not None:
        _box(reveal['box'], 'spec.reveal.box')
    hook = _object(spec.get('hook'), 'spec.hook')
    _strings(hook.get('title'), 'spec.hook.title')
    _optional_number(hook.get('duration'), 'spec.hook.duration', positive=True)
    outro = _object(spec.get('outro'), 'spec.outro')
    _strings(outro.get('cta'), 'spec.outro.cta')
    _numbers(outro.get('at'), 'spec.outro.at')
    _optional_number(outro.get('duration'), 'spec.outro.duration', positive=True)


def _common(spec: Dict[str, Any]) -> None:
    _string(spec.get('uri'), 'spec.uri')
    _font(spec.get('font'), 'spec.font')
    _optional_number(spec.get('duration'), 'spec.duration', positive=True)
    if spec.get('clip') not in (None, 'mask', 'nest'):
        raise InputError(f"spec.clip: must be 'mask' or 'nest', not {_shown(spec['clip'])}")
    if spec.get('sourceAudio') not in (None, 'mute', 'keep'):
        raise InputError(f"spec.sourceAudio: must be 'mute' or 'keep', not {_shown(spec['sourceAudio'])}")
    for k in ('product', 'audience', 'language'):
        if spec.get(k) is not None:
            _string(spec[k], f'spec.{k}')


def _shown(v: Any) -> str:
    return 'missing' if v is None else dumps(v)[:60]


def _object(v: Any, where: str) -> Dict[str, Any]:
    if not isinstance(v, dict):
        raise InputError(f'{where}: must be an object, not {_shown(v)}')
    return v


def _list(v: Any, where: str) -> List[Any]:
    if not isinstance(v, list):
        raise InputError(f'{where}: must be a list, not {_shown(v)}')
    return v


def _string(v: Any, where: str) -> None:
    if not isinstance(v, str):
        raise InputError(f'{where}: must be a string, not {_shown(v)}')


FONT_URL = re.compile(r'https://([a-z0-9-]+\.)*picsart\.com/\S+\.(ttf|otf)(\?\S*)?', re.IGNORECASE)


def _font(v: Any, where: str) -> None:
    """A catalog key, or a live face's file on a Picsart host: the scene editor loads no other font URL."""
    _string(v, where)
    if '/' in v and not FONT_URL.fullmatch(v):
        raise InputError(f'{where}: a font URL must be an https .ttf or .otf file on a picsart.com host, not {_shown(v)}')


def _strings(v: Any, where: str) -> None:
    if not isinstance(v, list) or not all(isinstance(x, str) for x in v):
        raise InputError(f'{where}: must be a list of strings, one per line, not {_shown(v)}')


def _boolean(v: Any, where: str) -> None:
    if not isinstance(v, bool):
        raise InputError(f'{where}: must be true or false, not {_shown(v)}')


def _number(v: Any, where: str, positive: bool = False) -> None:
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        raise InputError(f'{where}: must be a number, not {_shown(v)}')
    if positive and v <= 0:
        raise InputError(f'{where}: must be more than 0, not {_shown(v)}')


def _optional_number(v: Optional[Any], where: str, positive: bool = False) -> None:
    if v is not None:
        _number(v, where, positive)


def _numbers(v: Any, where: str) -> None:
    for i, x in enumerate(_list(v, where)):
        _number(x, f'{where}[{i}]')


def _index(v: Any, where: str, count: int) -> None:
    _number(v, where)
    if v != int(v) or not 0 <= v < count:
        raise InputError(f'{where}: no event {_shown(v)} (there are {count})')


def _indices(v: Any, where: str, count: int) -> None:
    for i, x in enumerate(_list(v, where)):
        _index(x, f'{where}[{i}]', count)


def _box(v: Any, where: str) -> None:
    _object(v, where)
    for k in ('x', 'y'):
        _number(v.get(k), f'{where}.{k}')
    for k in ('w', 'h'):
        _number(v.get(k), f'{where}.{k}', positive=True)


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
