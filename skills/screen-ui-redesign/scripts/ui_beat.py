#!/usr/bin/env python3
"""
Recreate a moment of an app's UI as designed motion: the app's own cards, chat bubbles, chips,
lists and buttons, in its own colours and words, redrawn larger for 9:16 and moving from one state
the recording showed to the next.

    python3 scripts/ui_beat.py input.json
    python3 scripts/ui_beat.py < input.json

The input is one JSON object:

    {"id": "s2", "box": {"x": 40, "y": 600, "w": 1000, "h": 1280}, "start": 6.4, "duration": 6,
     "style": {"canvas": "#ffffff", "surface": "#f4f4f6", "ink": "#16161a", "accent": "#e3127a"},
     "font": "acumin-pro-bold",
     "elements": {
       "shot1": {"kind": "card", "title": "Shot 1", "image": "https://.../still-1.jpg", "chip": "Shot size Medium"},
       "shot2": {"kind": "card", "title": "Shot 2", "image": "https://.../still-2.jpg", "chip": "Shot size Medium"},
       "ask": {"kind": "bubble", "text": "Make shot 2 a close-up"}},
     "states": [
       {"at": 0, "seen": 312.4, "source": "stills/312.4.jpg", "show": ["shot1", "shot2"]},
       {"at": 1.6, "seen": 318.0, "source": "stills/318.0.jpg", "show": ["shot1", "shot2", "ask"]},
       {"at": 3.6, "seen": 326.0, "source": "stills/326.0.jpg", "show": ["shot1", "shot2"], "tap": "ask",
        "set": {"shot2": {"chip": "Shot size Close-up", "zoom": 1.5}, "shot1": {"tag": "kept wide"}}}]}

- `id` prefixes every layer and asset; `box` is where the beat sits, in frame px (default the
  whole 1080x1920 frame); `start` its scene second; `duration` its length.
- `style` is the app's own colours, read from the stills: `canvas` its background, `surface` its
  cards and bubbles, `ink` its text, `accent` its highlight (the primary button's colour); `font`
  the scene's font family.
- `elements`, by name, each one thing the recording shows, with its words exactly as shown:
  - `card`: `title`, `chip` (a value on a pill), and optionally `image` (a still's URL, shown as a
    thumbnail; or `{uri, width, height}` in source pixels), `zoom` (how far the thumbnail is pushed
    in, 1 by default), `focus` (`[x, y]`, 0-1, the point of the still it pushes toward; a focused zoom
    requires image width and height) and `tag` (a few words under the chip);
  - `bubble`: `text`, a message typed into a chat box, with a send button;
  - `chip`: `text`, a value on its own pill;
  - `list`: `items`, rows of words;
  - `button`: `label`.
- `states`, in time order, each one screen the recording showed: `at`, its second in the beat;
  `seen`, **the recording second that shows it** (required: a state the recording does not show
  is not drawn); `source`, the still of that second, to put beside the designed frame and compare
  (a state without one is reported); `show`, the elements on screen, top to bottom; `set`, values that change from
  here on (`chip`, `tag`, `zoom`, `focus` on a card, `text` on a chip); `tap`, the element pressed
  to cause this change.

How it moves (the motion-design-craft skill's craft, fixed here so every beat reads the same):
- an element in two states is the same element: it moves to its new place on the house curve
  and is never cut or faded;
- elements new to a state enter after the moves start, sliding up, staggered 0.1 s apart; an
  element a state drops leaves upward;
- a tapped element dips to 0.92 and back just before its state, a bubble's send button for a
  bubble; a bubble's text types out once it has risen;
- a changed value pops: the old pill fades, the new one scales 0.6 to 1.1 to 1 in the accent; a
  pushed thumbnail moves in over 0.9 s.

It prints one JSON line, `{layers, assets, duration, states, diagnostics}`: layers in frame px,
starting at `start`, to add to the scene in place of what they replace, and the nested scenes
the thumbnails play, to add to its `assets`. No layer has a mask. A diagnostic is
`{level, code, message}`; `no_source` names a state never compared with its still. Input it cannot build exits 1, with one line on stderr that says which
field is wrong.

Python 3.9 or later, the standard library only, offline.
"""
from __future__ import annotations

import json
import math
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

FRAME = {'x': 0, 'y': 0, 'w': 1080, 'h': 1920}
FPS = 30
# Entrances: fast, then a long settle. Moves of a matched element: the motion-design-craft skill's house curve.
OUT = {'kind': 'cubic_bezier', 'control': [0.16, 1, 0.3, 1]}
MOVE = {'kind': 'cubic_bezier', 'control': [0.65, 0, 0.2, 1]}
EXIT = {'kind': 'cubic_bezier', 'control': [0.4, 0, 1, 1]}

ENTER = 0.5      # an entrance's length
STAGGER = 0.1    # between two entrances of one state
MOVE_S = 0.5     # a matched element's move
LEAVE = 0.3      # an exit
TAP = (0.35, 0.25, 0.1)  # the dip starts, bottoms and ends this long before its state
DIP = 0.92
POP_AT = 0.5     # a changed value pops this long after its state starts
PUSH = (0.2, 0.9)  # a thumbnail's push: its delay and length
MIN_GAP = 1.5    # between two states: time to read one before the next moves
CHAR_EM = 0.56   # a character's width, in ems, for wrapping
MIN_SIZE = 36    # text never shrinks below this, frame px

# Sizes for a 1000 px wide box; a beat in another box scales them all.
WIDTH = 900
GAP = 40
CARD_H, THUMB = 400, 340
BUBBLE_H, SEND = 140, 96
PILL_W, PILL_H = 460, 96
ROW_H, ROW_GAP = 96, 16
BUTTON_W, BUTTON_H = 520, 120

HEX = re.compile(r'^#[0-9a-fA-F]{6}$')
KINDS = ('card', 'bubble', 'chip', 'list', 'button')
CHANGES = {'card': ('chip', 'tag', 'zoom', 'focus'), 'chip': ('text',)}

USAGE = 'usage: ui_beat.py [input.json]; with no file, the input is read from stdin'


class InputError(ValueError):
    pass


def r3(v: float) -> float:
    return math.floor(v * 1000 + 0.5) / 1000


def r1(v: float) -> float:
    return math.floor(v * 10 + 0.5) / 10


def on_frame(t: float) -> float:
    """`t` on the 30 fps frame grid, so a layer starts and ends on a frame."""
    return math.floor(t * FPS + 0.5) / FPS


# --- tracks: [(t, value, easing to the next key)] -------------------------------------------------

Track = List[Tuple[float, Any, Any]]


def _lerp(a: Any, b: Any, f: float) -> Any:
    if isinstance(a, list):
        return [x + (y - x) * f for x, y in zip(a, b)]
    return a + (b - a) * f


def sample(track: Track, t: float) -> Any:
    """The track's value at `t`: held before the first key and after the last, linear between."""
    if t <= track[0][0]:
        return track[0][1]
    for (t0, v0, _), (t1, v1, _) in zip(track, track[1:]):
        if t <= t1:
            return v0 if t1 - t0 < 1e-9 else _lerp(v0, v1, (t - t0) / (t1 - t0))
    return track[-1][1]


def easing_at(track: Track, t: float) -> Optional[Any]:
    """The easing of the ramp that starts at `t`, or None when the track holds there."""
    for (t0, v0, e), (_, v1, _) in zip(track, track[1:]):
        if abs(t0 - t) < 1e-6 and v0 != v1:
            return e
    return None


def keys(times: List[float], value, tracks: List[Track], offset: float = 0.0, fmt=r3) -> Dict[str, Any]:
    """Keyframes at `times`, layer-relative, the easing of whichever track ramps from each key."""
    out = []
    for i, t in enumerate(times):
        v = value(t)
        k = {'time': r3(t - offset), 'value': [fmt(x) for x in v] if isinstance(v, list) else fmt(v)}
        if i < len(times) - 1:
            k['easing'] = next((e for e in (easing_at(tr, t) for tr in tracks) if e is not None), 'linear')
        out.append(k)
    # A key inside a hold says nothing: drop it.
    kept = [k for i, k in enumerate(out) if i in (0, len(out) - 1) or not (k['value'] == out[i - 1]['value'] == out[i + 1]['value'])]
    return {'keyframes': kept}


def times_of(tracks: List[Track], lo: float, hi: float) -> List[float]:
    ts = sorted({t for tr in tracks for t, _, _ in tr if lo < t < hi} | {lo, hi})
    return ts


# --- text ----------------------------------------------------------------------------------------

def wrap(text: str, size: float, width: float) -> List[str]:
    per = max(1, int(width / (size * CHAR_EM)))
    lines: List[str] = []
    for word in text.split():
        if lines and len(lines[-1]) + 1 + len(word) <= per:
            lines[-1] += ' ' + word
        else:
            lines.append(word)
    return lines or ['']


def fit_text(text: str, size: float, width: float, most: int, k: float) -> Tuple[List[str], float, bool]:
    """The largest size, down to MIN_SIZE, at which the text fits within `width` and `most` lines."""
    s = size * k
    while True:
        lines = wrap(text, s, width)
        ok = len(lines) <= most and all(len(line) * s * CHAR_EM <= width for line in lines)
        if ok or s <= MIN_SIZE * k:
            return lines, s, ok
        s = max(MIN_SIZE * k, s - 2 * k)


# --- input ---------------------------------------------------------------------------------------

def _num(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def _text(v: Any, where: str) -> str:
    if not isinstance(v, str) or not v.strip():
        raise InputError(f'{where} must be the words the recording shows')
    return v.strip()


def _box(v: Any, where: str) -> Dict[str, float]:
    if not isinstance(v, dict) or not all(_num(v.get(k)) for k in 'xywh') or v['w'] <= 0 or v['h'] <= 0:
        raise InputError(f'{where} must be {{x, y, w, h}} in frame px')
    return {k: v[k] for k in 'xywh'}


def _values(kind: str, v: Dict[str, Any], where: str, initial: bool) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for key, val in v.items():
        if initial and (key in ('kind', 'title', 'image', 'items', 'label') or (key == 'text' and kind == 'bubble')):
            continue
        if key not in CHANGES.get(kind, ()):
            raise InputError(f'{where}.{key}: a {kind} has no {key} that changes')
        if key == 'zoom':
            if not _num(val) or not 1 <= val <= 3:
                raise InputError(f'{where}.zoom must be a number from 1 to 3')
        elif key == 'focus':
            if not (isinstance(val, list) and len(val) == 2 and all(_num(x) and 0 <= x <= 1 for x in val)):
                raise InputError(f'{where}.focus must be [x, y], each 0-1')
        else:
            val = _text(val, f'{where}.{key}')
        out[key] = val
    if initial and kind == 'card' and 'chip' not in out:
        raise InputError(f'{where}.chip must be the value the card shows')
    if initial and kind == 'chip' and 'text' not in out:
        raise InputError(f'{where}.text must be the value the chip shows')
    return out


def check(data: Any) -> Dict[str, Any]:
    if not isinstance(data, dict):
        raise InputError('the input must be one JSON object')
    if not isinstance(data.get('id'), str) or not re.match(r'^[A-Za-z0-9_-]+$', data['id']):
        raise InputError('id must be a layer id prefix: letters, digits, _ and -')
    box = _box(data['box'], 'box') if data.get('box') is not None else dict(FRAME)
    if not _num(data.get('start')) or data['start'] < 0:
        raise InputError('start must be the scene second the beat starts')
    if not _num(data.get('duration')) or data['duration'] <= 0:
        raise InputError('duration must be the beat\'s length in seconds')
    style = data.get('style')
    if not isinstance(style, dict) or not all(isinstance(style.get(r), str) and HEX.match(style[r]) for r in ('canvas', 'surface', 'ink', 'accent')):
        raise InputError('style must be the app\'s own colours from the stills: canvas, surface, ink and accent as #rrggbb')
    font = _text(data.get('font'), 'font')
    raw = data.get('elements')
    if not isinstance(raw, dict) or not raw:
        raise InputError('elements must name each thing the recording shows')
    elements: Dict[str, Dict[str, Any]] = {}
    for name, e in raw.items():
        where = f'elements.{name}'
        if not re.match(r'^[A-Za-z0-9_-]+$', name):
            raise InputError(f'{where}: a name is letters, digits, _ and -')
        if not isinstance(e, dict) or e.get('kind') not in KINDS:
            raise InputError(f'{where}.kind must be one of {", ".join(KINDS)}')
        kind = e['kind']
        el: Dict[str, Any] = {'kind': kind, 'values': _values(kind, e, where, True)}
        if kind == 'card':
            el['title'] = _text(e.get('title'), f'{where}.title')
            if e.get('image') is not None:
                image = e['image']
                if isinstance(image, dict):
                    if not all(_num(image.get(key)) and image[key] > 0 for key in ('width', 'height')):
                        raise InputError(f'{where}.image must include positive width and height in source pixels')
                    el['image'] = {key: image[key] for key in ('width', 'height')}
                    el['image']['uri'] = _text(image.get('uri'), f'{where}.image.uri')
                else:
                    el['image'] = {'uri': _text(image, f'{where}.image')}
        elif kind == 'bubble':
            el['text'] = _text(e.get('text'), f'{where}.text')
        elif kind == 'list':
            if not isinstance(e.get('items'), list) or not e['items']:
                raise InputError(f'{where}.items must be the rows the recording shows')
            el['items'] = [_text(x, f'{where}.items[{i}]') for i, x in enumerate(e['items'])]
        elif kind == 'button':
            el['label'] = _text(e.get('label'), f'{where}.label')
        elements[name] = el
    states = data.get('states')
    if not isinstance(states, list) or not states:
        raise InputError('states must list each screen the recording showed, in order')
    out_states = []
    for i, s in enumerate(states):
        where = f'states[{i}]'
        if not isinstance(s, dict) or not _num(s.get('at')):
            raise InputError(f'{where}.at must be its second in the beat')
        if not _num(s.get('seen')) or s['seen'] < 0:
            raise InputError(f'{where}.seen must be the recording second that shows this state; a state the recording does not show is not drawn')
        if i == 0 and s['at'] != 0:
            raise InputError('states[0].at must be 0')
        if i > 0 and s['at'] - out_states[-1]['at'] < MIN_GAP - 1e-9:
            raise InputError(f'{where}.at must be at least {MIN_GAP} s after the state before')
        if s['at'] > data['duration'] - MIN_GAP + 1e-9:
            raise InputError(f'{where}.at must leave at least {MIN_GAP} s of the beat after it')
        show = s.get('show')
        if not isinstance(show, list) or not show or len(set(show)) != len(show):
            raise InputError(f'{where}.show must list the elements on screen, each once')
        for n in show:
            if n not in elements:
                raise InputError(f'{where}.show names {n!r}, which is not in elements')
        sets = s.get('set') or {}
        if not isinstance(sets, dict):
            raise InputError(f'{where}.set must map element names to their new values')
        checked_set = {}
        for n, v in sets.items():
            if n not in elements or not isinstance(v, dict):
                raise InputError(f'{where}.set names {n!r}, which is not in elements')
            if not out_states or n not in out_states[-1]['show']:
                raise InputError(f'{where}.set.{n}: only an element already on screen changes; give a new one its value in elements')
            checked_set[n] = _values(elements[n]['kind'], v, f'{where}.set.{n}', False)
        tap = s.get('tap')
        if tap is not None:
            if i == 0:
                raise InputError('states[0].tap: the first state has no change to cause')
            if tap not in elements or tap not in out_states[-1]['show']:
                raise InputError(f'{where}.tap must name an element on screen in the state before')
        source = s.get('source')
        if source is not None:
            source = _text(source, f'{where}.source')
        out_states.append({'at': s['at'], 'seen': s['seen'], 'source': source, 'show': show, 'set': checked_set, 'tap': tap})
    return {'id': data['id'], 'box': box, 'start': data['start'], 'duration': data['duration'], 'style': style, 'font': font, 'elements': elements, 'states': out_states}


# --- layout --------------------------------------------------------------------------------------

def height(el: Dict[str, Any]) -> float:
    kind = el['kind']
    if kind == 'card':
        return CARD_H
    if kind == 'bubble':
        return BUBBLE_H
    if kind == 'chip':
        return PILL_H
    if kind == 'list':
        return len(el['items']) * ROW_H + (len(el['items']) - 1) * ROW_GAP
    return BUTTON_H


def slots(spec: Dict[str, Any], k: float) -> List[Dict[str, List[float]]]:
    """Each state's element centres, stacked top to bottom and centred in the box."""
    box = spec['box']
    out = []
    for i, s in enumerate(spec['states']):
        hs = [height(spec['elements'][n]) * k for n in s['show']]
        total = sum(hs) + GAP * k * (len(hs) - 1)
        if total > box['h'] - 2 * GAP * k:
            raise InputError(f"states[{i}]: its elements stand {round(total)} px tall, more than the box's {round(box['h'] - 2 * GAP * k)}; show fewer")
        y = box['y'] + (box['h'] - total) / 2
        cx = box['x'] + box['w'] / 2
        placed = {}
        for n, h in zip(s['show'], hs):
            placed[n] = [cx, y + h / 2]
            y += h + GAP * k
        out.append(placed)
    return out


# --- the element's own motion: [x, y], scale, opacity --------------------------------------------

def element_tracks(name: str, spec: Dict[str, Any], places: List[Dict[str, List[float]]], k: float) -> Tuple[Track, Track, Track, List[Tuple[float, float]]]:
    """Its centre, its scale (the tap) and its opacity, and the spans it is on screen."""
    pos: Track = []
    scl: Track = [(0, 1, 'linear')]
    opa: Track = []
    spans: List[Tuple[float, float]] = []
    states = spec['states']
    shown_before = False
    cur: Optional[List[float]] = None
    entered = 0.0
    for i, s in enumerate(states):
        t = s['at']
        shown = name in s['show']
        new = [n for n in s['show'] if all(n not in st['show'] for st in states[i - 1:i])] if i else s['show']
        if s['tap'] == name and shown_before and spec['elements'][name]['kind'] != 'bubble':
            a, b, c = (t - x for x in TAP)
            scl += [(a, 1, OUT), (b, DIP, OUT), (c, 1, 'linear')]
        if shown and not shown_before:
            begin = t + (0.1 if i == 0 else MOVE_S * 0.5) + STAGGER * new.index(name)
            to = places[i][name]
            low = [to[0], to[1] + 60 * k]
            if not pos:
                pos.append((0, low, 'linear'))
                opa.append((0, 0, 'linear'))
            pos += [(begin, low, OUT), (begin + ENTER, to, 'linear')]
            opa += [(begin, 0, OUT), (begin + ENTER, 1, 'linear')]
            cur, entered = to, begin
        elif shown and shown_before:
            to = places[i][name]
            if to != cur:
                cur = sample(pos, t)
                pos = [key for key in pos if key[0] < t]
                pos += [(t, cur, MOVE), (t + MOVE_S, to, 'linear')]
                cur = to
        elif not shown and shown_before:
            # A late stagger may still be entering: leave from its current pose and opacity.
            cur, opacity = sample(pos, t), sample(opa, t)
            pos = [key for key in pos if key[0] < t]
            opa = [key for key in opa if key[0] < t]
            up = [cur[0], cur[1] - 40 * k]
            pos += [(t, cur, EXIT), (t + LEAVE, up, 'linear')]
            opa += [(t, opacity, EXIT), (t + LEAVE, 0, 'linear')]
            spans.append((entered, t + LEAVE))
            cur = up
        shown_before = shown
    if shown_before:
        spans.append((entered, spec['duration']))
    element = spec['elements'][name]
    delay = STAGGER * (len(element['items']) - 1) if element['kind'] == 'list' else 0.0
    for begin, end in spans:
        if begin + delay + ENTER > end + 1e-9:
            raise InputError(f'{name}: its entrance must finish within its visible span; show fewer elements or lengthen the beat')
    return pos, scl, opa, spans


def versions(name: str, key: str, spec: Dict[str, Any]) -> List[Tuple[float, Any]]:
    """Each value `key` takes, with the beat second it pops in (0 for the first)."""
    out = []
    v = spec['elements'][name]['values'].get(key)
    if v is not None:
        out.append((0.0, v))
    for s in spec['states'][1:]:
        nv = s['set'].get(name, {}).get(key)
        if nv is not None and nv != v:
            out.append((s['at'] + POP_AT, nv))
            v = nv
    return out


# --- layers --------------------------------------------------------------------------------------

def shape(w: float, h: float, r: float, color: str) -> Dict[str, Any]:
    return {'kind': 'shape', 'items': [{'type': 'rect', 'size': [r1(w), r1(h)], 'roundness': r1(r)}, {'type': 'fill', 'color': color}]}


def text(lines: List[str], size: float, color: str, font: str, preset: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    c = {'kind': 'text', 'text': lines, 'font': {'family': font, 'size': r1(size)}, 'color': color, 'alignment': 'center'}
    if preset:
        c['animations'] = [preset]
    return c


class Beat:
    def __init__(self, spec: Dict[str, Any]):
        self.spec = spec
        self.k = spec['box']['w'] / 1000
        self.layers: List[Dict[str, Any]] = []
        self.assets: Dict[str, Any] = {}
        self.diagnostics: List[Dict[str, str]] = []

    def piece(self, lid: str, content: Dict[str, Any], off: Tuple[float, float], el: Tuple[Track, Track, Track],
              own_opacity: Optional[Track] = None, own_scale: Optional[Track] = None, begin: float = 0.0, end: Optional[float] = None) -> None:
        """One layer of an element: it rides the element's centre, scale and opacity, times its own."""
        pos, scl, opa = el
        own_opacity = own_opacity or [(0, 1, 'linear')]
        own_scale = own_scale or [(0, 1, 'linear')]
        end = self.spec['duration'] if end is None else on_frame(end)
        begin = on_frame(begin)
        if end <= begin:
            raise InputError(f'{lid}: its entrance leaves no time for this layer; lengthen its visible span')
        k = self.k
        def ts(*tracks):
            # Each property keys only its own tracks' times, so no ramp is cut in two by another's.
            return [t for t in times_of(list(tracks), begin, end) if t <= end]

        def where(t):
            c, s = sample(pos, t), sample(scl, t)
            return [c[0] + off[0] * k * s, c[1] + off[1] * k * s]

        layer = {
            'id': lid, 'start': round(self.spec['start'] + begin, 4), 'duration': round(end - begin, 4), 'timeMode': 'layer',
            'transform': {'position': [r1(v) for v in where(begin)]},
            'content': content,
            'animations': {
                'position': keys(ts(pos, scl), where, [pos, scl], begin, r1),
                'opacity': keys(ts(opa, own_opacity), lambda t: sample(opa, t) * sample(own_opacity, t), [opa, own_opacity], begin),
            },
        }
        if len(scl) > 1 or len(own_scale) > 1:
            layer['animations']['scale'] = keys(ts(scl, own_scale), lambda t: [sample(scl, t) * sample(own_scale, t)] * 2, [own_scale, scl], begin)
        self.layers.append(layer)

    def popped(self, base: str, name: str, key: str, el, draw) -> None:
        """A value that changes: each version a piece, the old fading as the new one pops."""
        vs = versions(name, key, self.spec)
        for j, (at, v) in enumerate(vs):
            nxt = vs[j + 1][0] if j + 1 < len(vs) else None
            if at == 0:
                fade: Track = [(0, 1, 'linear')]
                grow: Track = [(0, 1, 'linear')]
            else:
                fade = [(0, 0, 'linear'), (at, 0, OUT), (at + 0.3, 1, 'linear')]
                grow = [(0, 0.6, 'linear'), (at, 0.6, OUT), (at + 0.3, 1.1, OUT), (at + 0.45, 1, 'linear')]
            if nxt is not None:
                fade = fade + [(nxt, 1, EXIT), (nxt + 0.15, 0, 'linear')]
            for suffix, content, off in draw(v, j > 0 or key == 'tag'):
                self.piece(f'{base}_{key}{j}{suffix}', content, off, el, fade, grow)

    def card(self, name: str, el, s: Dict[str, Any]) -> None:
        sp, k, e = self.spec, self.k, self.spec['elements'][name]
        base = f"{sp['id']}_{name}"
        self.piece(f'{base}_card', shape(WIDTH * k, CARD_H * k, 28 * k, s['surface']), (0, 0), el)
        # The words' column: right of the thumbnail when there is one, else the card's width.
        left = -WIDTH / 2 + 30 + (THUMB + 30 if e.get('image') else 0)
        right, col = (left + WIDTH / 2 - 30) / 2, WIDTH / 2 - 30 - left
        if e.get('image'):
            self.thumb(f'{base}_thumb', name, e['image'], el, (-WIDTH / 2 + 30 + THUMB / 2, 0))
        lines, size, ok = fit_text(e['title'], 52, col * k, 1, k)
        if not ok:
            self.warn('long_text', f'{name}.title wraps to {len(lines)} lines; shorten it to what the card shows first')
        self.piece(f'{base}_title', text(lines, size, s['ink'], sp['font']), (right, -110), el)

        def chip(v, changed):
            fill, ink = (s['accent'], s['canvas']) if changed else (s['canvas'], s['ink'])
            ls, sz, ok = fit_text(v, 40, (PILL_W - 40) * k, 1, k)
            if not ok:
                self.warn('long_text', f'{name}.chip does not fit; a pill holds one line')
            return [('', shape(PILL_W * k, PILL_H * k, PILL_H / 2 * k, fill), (right, 10)), ('_text', text(ls, sz, ink, sp['font']), (right, 10))]

        def tag(v, _):
            ls, sz, _ = fit_text(v, 38, col * k, 1, k)
            return [('', text(ls, sz, s['accent'], sp['font']), (right, 120))]

        self.popped(base, name, 'chip', el, chip)
        self.popped(base, name, 'tag', el, tag)

    def thumb(self, lid: str, name: str, image: Dict[str, Any], el, off: Tuple[float, float]) -> None:
        """A square window onto a still, as a nested scene; the still pushes in where the card's zoom changes."""
        sp, k = self.spec, self.k
        th = THUMB * k
        e = sp['elements'][name]
        zoom: Track = [(0, e['values'].get('zoom', 1), 'linear')]
        focus: Track = [(0, e['values'].get('focus', [0.5, 0.5]), 'linear')]
        for s in sp['states'][1:]:
            ch = s['set'].get(name, {})
            if 'zoom' in ch or 'focus' in ch:
                a, b = s['at'] + PUSH[0], s['at'] + PUSH[0] + PUSH[1]
                zoom += [(a, zoom[-1][1], MOVE), (b, ch.get('zoom', zoom[-1][1]), 'linear')]
                focus += [(a, focus[-1][1], MOVE), (b, ch.get('focus', focus[-1][1]), 'linear')]

        sized = 'width' in image and 'height' in image
        focused = 'focus' in e['values'] or any('focus' in s['set'].get(name, {}) for s in sp['states'])
        if focused and any(z > 1 for _, z, _ in zoom) and not sized:
            raise InputError(f'elements.{name}.image needs width and height for a focused zoom')
        size = [image['width'], image['height']] if sized else [th, th]
        base = max(th / v for v in size)

        def at(t):
            z, f = sample(zoom, t), sample(focus, t)
            out = []
            for i, v in enumerate(size):
                extent = v * base * z
                room = (extent - th) / 2
                out.append(min(th / 2 + room, max(th / 2 - room, th / 2 + (0.5 - f[i]) * extent)))
            return out

        ts = times_of([zoom, focus], 0, sp['duration'])
        pic = {'id': 'pic', 'start': 0, 'duration': sp['duration'], 'timeMode': 'layer',
               'transform': {'position': [r1(v) for v in at(0)], 'scale': [sample(zoom, 0) * base] * 2},
               'content': {'kind': 'media', 'assetId': 'img', 'fit': 'none' if sized else 'cover'}}
        if sized:
            pic['transform']['anchor'] = [v / 2 for v in size]
        if len(zoom) > 1 or len(focus) > 1:
            pic['animations'] = {'position': keys(ts, at, [zoom, focus], 0, r1), 'scale': keys(ts, lambda t: [sample(zoom, t) * base] * 2, [zoom])}
        self.assets[lid] = {'type': 'scene', 'scene': {
            'version': '1.0', 'composition': {'width': r1(th), 'height': r1(th), 'fps': FPS, 'duration': sp['duration'], 'background': sp['style']['canvas']},
            'assets': {'img': {'type': 'image', **image}}, 'layers': [pic]}}
        self.piece(lid, {'kind': 'scene_ref', 'assetId': lid, 'fit': 'none'}, off, el)

    def bubble(self, name: str, el, s: Dict[str, Any], spans: List[Tuple[float, float]]) -> None:
        sp, k, e = self.spec, self.k, self.spec['elements'][name]
        base = f"{sp['id']}_{name}"
        self.piece(f'{base}_bubble', shape(WIDTH * k, BUBBLE_H * k, BUBBLE_H / 2 * k, s['surface']), (0, 0), el)
        lines, size, ok = fit_text(e['text'], 48, (WIDTH - SEND - 100) * k, 2, k)
        if not ok:
            self.warn('long_text', f'{name}.text wraps to {len(lines)} lines; a bubble holds two')
        typing = min(1.6, max(0.6, 0.045 * len(e['text'])))
        # Each time the bubble is on screen its text types out again, once it has risen.
        begins = [span[0] + ENTER for span in spans]
        for j, (begin, span) in enumerate(zip(begins, spans)):
            self.piece(f'{base}_text{j or ""}', text(lines, size, s['ink'], sp['font'], {'preset': 'typewriter', 'params': {'duration': r3(typing)}}),
                       (-SEND / 2 - 20, 0), el, begin=begin, end=span[1])
            cuts = [st['at'] - TAP[0] for st in sp['states'][1:]
                    if st['tap'] == name and span[0] <= st['at'] <= span[1]]
            if on_frame(span[1]) < on_frame(begin) + typing - 1e-9 and not any(a < begin + typing + 0.2 for a in cuts):
                self.warn('typing_cut', f'{name} finishes typing at {r3(begin + typing)} s but leaves at {r3(span[1])} s; lengthen its visible span')
        press: Track = [(0, 1, 'linear')]
        for st in sp['states'][1:]:
            if st['tap'] == name:
                a, b, c = (st['at'] - x for x in TAP)
                press += [(a, 1, OUT), (b, DIP, OUT), (c, 1, 'linear')]
                begin = max((x for x in begins if x <= st['at']), default=begins[0])
                if a < begin + typing + 0.2:
                    self.warn('typing_cut', f'{name} finishes typing at {r3(begin + typing)} s and is sent at {r3(a)} s, with no beat to read it; move the state that sends it later')
        self.piece(f'{base}_send', shape(SEND * k, SEND * k, SEND / 2 * k, s['accent']), (WIDTH / 2 - 80, 0), el, own_scale=press)

    def rest(self, name: str, el, s: Dict[str, Any], span: Tuple[float, float]) -> None:
        sp, k, e = self.spec, self.k, self.spec['elements'][name]
        base = f"{sp['id']}_{name}"
        if e['kind'] == 'chip':
            def chip(v, changed):
                fill, ink = (s['accent'], s['canvas']) if changed else (s['surface'], s['ink'])
                ls, sz, ok = fit_text(v, 40, (PILL_W - 40) * k, 1, k)
                if not ok:
                    self.warn('long_text', f'{name}.text does not fit; a pill holds one line')
                return [('', shape(PILL_W * k, PILL_H * k, PILL_H / 2 * k, fill), (0, 0)), ('_text', text(ls, sz, ink, sp['font']), (0, 0))]
            self.popped(base, name, 'text', el, chip)
        elif e['kind'] == 'list':
            for j, item in enumerate(e['items']):
                y = -height(e) / 2 + ROW_H / 2 + j * (ROW_H + ROW_GAP)
                ls, sz, ok = fit_text(item, 40, (WIDTH - 60) * k, 1, k)
                if not ok:
                    self.warn('long_text', f'{name}.items[{j}] wraps; a row holds one line')
                # Rows after the first stagger in behind it.
                at = span[0] + STAGGER * j
                rise: Optional[Track] = [(0, 0, 'linear'), (at, 0, OUT), (at + ENTER, 1, 'linear')] if j else None
                self.piece(f'{base}_row{j}', shape(WIDTH * k, ROW_H * k, 20 * k, s['surface']), (0, y), el, rise)
                self.piece(f'{base}_row{j}_text', text(ls, sz, s['ink'], sp['font']), (0, y), el, rise)
        else:
            ls, sz, ok = fit_text(e['label'], 48, (BUTTON_W - 60) * k, 1, k)
            if not ok:
                self.warn('long_text', f'{name}.label wraps; a button holds one line')
            self.piece(f'{base}_button', shape(BUTTON_W * k, BUTTON_H * k, BUTTON_H / 2 * k, s['accent']), (0, 0), el)
            self.piece(f'{base}_label', text(ls, sz, s['canvas'], sp['font']), (0, 0), el)

    def warn(self, code: str, message: str) -> None:
        self.diagnostics.append({'level': 'warning', 'code': code, 'message': message})

    def build(self) -> Dict[str, Any]:
        sp = self.spec
        places = slots(sp, self.k)
        style = sp['style']
        box = sp['box']
        self.layers.append({
            'id': f"{sp['id']}_canvas", 'start': sp['start'], 'duration': sp['duration'], 'timeMode': 'layer',
            'transform': {'position': [box['x'] + box['w'] / 2, box['y'] + box['h'] / 2]},
            'content': shape(box['w'], box['h'], 0, style['canvas']),
        })
        order = []
        for s in sp['states']:
            order += [n for n in s['show'] if n not in order]
        for name in sp['elements']:
            if name not in order:
                self.warn('never_shown', f'{name} is in elements but no state shows it')
        for i, s in enumerate(sp['states']):
            if s['source'] is None:
                self.warn('no_source', f'states[{i}] (seen {s["seen"]} s) has no source: put the still of that second beside the designed frame, compare them, and name it')
        for name in order:
            pos, scl, opa, spans = element_tracks(name, sp, places, self.k)
            el = (pos, scl, opa)
            kind = sp['elements'][name]['kind']
            if kind == 'card':
                self.card(name, el, style)
            elif kind == 'bubble':
                self.bubble(name, el, style, spans)
            else:
                self.rest(name, el, style, spans[0])
        return {
            'layers': self.layers,
            'assets': self.assets,
            'duration': sp['duration'],
            'states': [{'at': s['at'], 'seen': s['seen'], 'source': s['source']} for s in sp['states']],
            'diagnostics': self.diagnostics,
        }


def run(data: Any) -> Dict[str, Any]:
    """The script's whole job: the checked input in, the line it prints out."""
    return Beat(check(data)).build()


def main(argv: List[str]) -> int:
    if len(argv) > 1 or any(a.startswith('-') for a in argv):
        return fail(USAGE, 2)
    try:
        if argv:
            with open(argv[0], encoding='utf-8-sig') as f:
                raw = f.read()
        else:
            raw = sys.stdin.buffer.read().decode('utf-8-sig')
    except (OSError, UnicodeDecodeError) as err:
        return fail(f'cannot read the input: {err}')
    try:
        out = run(json.loads(raw))
    except json.JSONDecodeError as err:
        return fail(f'the input is not JSON: {err}')
    except InputError as err:
        return fail(str(err))
    sys.stdout.buffer.write((json.dumps(out, ensure_ascii=False, separators=(',', ':')) + '\n').encode('utf-8'))
    return 0


def fail(reason: str, code: int = 1) -> int:
    sys.stderr.write('ui_beat.py: ' + ' '.join(reason.split()) + '\n')
    return code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
