"""
Compose the tutorial's scene in the 16:9 frame, as the layouts skill's landscape reference lays it
out: the finished result on a card first, then for each chapter a title card and its steps, each
step the whole recording with a push onto every action and a zoom back out, its line in the lower
third (or the top band when the push lands there), and its voice line when there is one.
"""
from __future__ import annotations

import math
from typing import Any, Dict, List

from framing import center, fit_base, fit_scale, min_scale, pose, round
from panels import bubble, nest_panel, panel_mask, rim_layer
from zoom import clamp_focus

Layer = Dict[str, Any]

FRAME = {'w': 1920, 'h': 1080}
WHOLE = {'x': 0, 'y': 0, 'w': 1920, 'h': 1080}
# The step line's bubble: a lower third inside the title-safe area, and the top band it moves to
# when a push lands in the lower third (layouts, references/landscape.md).
LINE_BOX = {'x': 192, 'w': 1536, 'bottom': 930, 'top': 150}
LINE_PX = 40
TITLE_PX = 72
# The result card: at most this box, centred under the title; a still never shown larger than
# STILL_MAX output px per source px, past which it goes soft.
CARD = {'x': 320, 'y': 240, 'w': 1280, 'h': 720}
STILL_MAX = 1.2
BACKDROP_EFFECTS = [
    {'id': 'gaussian_blur', 'params': {'blur': 60}},
    {'id': 'adjust', 'params': {'brightness': -0.35, 'saturation': -0.1}},
]


def audible_at(speed: float) -> bool:
    """A clip plays its own sound only at 1x: a sped-up clip's speech is pitched and chopped."""
    return abs(speed - 1) <= 1e-3


def media(src_in: float, src_out: float, speed: float, fit: str = 'contain', audible: bool = False) -> Dict[str, Any]:
    """A recording clip; the speed is floored, so the layer never outlasts its trim."""
    content = {'kind': 'media', 'assetId': 'rec', 'fit': fit, 'muted': not (audible and audible_at(speed)), 'trim': {'in': round(src_in, 3), 'out': round(src_out, 3)}}
    if not audible_at(speed):
        content['speed'] = math.floor(speed * 1e4) / 1e4
    return content


def line_box(lines: int, band: str) -> Dict[str, float]:
    h = 60 + 50 * lines
    y = LINE_BOX['top'] if band == 'top' else LINE_BOX['bottom'] - h
    return {'x': LINE_BOX['x'], 'y': y, 'w': LINE_BOX['w'], 'h': h}


def text_layer(id_: str, lines: List[str], font: str, size: float, color: str, at: List[float], start: float, duration: float) -> Layer:
    return {
        'id': id_,
        'start': round(start, 3),
        'duration': round(duration, 3),
        'transform': {'position': at},
        'content': {'kind': 'text', 'text': lines, 'font': {'family': font, 'size': size}, 'color': color, 'alignment': 'center', 'animations': [{'preset': 'slide_up_lines', 'params': {'duration': 0.5}}]},
    }


def kf(k: Dict[str, Any]) -> Dict[str, Any]:
    out = {'time': k['time'], 'value': k['value']}
    if k.get('easing'):
        out['easing'] = k['easing']
    return out


def still(src_in: float, duration: float, src_len: float, fit: str = 'cover') -> Dict[str, Any]:
    """A near-frozen 0.15 s of the recording, played over `duration`."""
    a = max(0, min(src_in, src_len - 0.2))
    b = min(a + 0.15, src_len)
    return media(a, b, (b - a) / duration, fit)


def backdrop(id_: str, src_in: float, start: float, duration: float, src_len: float) -> Layer:
    return {'id': id_, 'start': round(start, 3), 'duration': round(duration, 3), 'content': still(src_in, duration, src_len), 'effects': BACKDROP_EFFECTS}


def card_box(box: Dict[str, float]) -> Dict[str, float]:
    s = min(STILL_MAX, fit_scale(box, CARD))
    w = round(box['w'] * s, 0)
    h = round(box['h'] * s, 0)
    return {'x': round(CARD['x'] + (CARD['w'] - w) / 2, 0), 'y': round(CARD['y'] + (CARD['h'] - h) / 2, 0), 'w': w, 'h': h}


def compose(spec: Dict[str, Any], src: Dict[str, float], src_len: float, steps: List[Dict[str, Any]], chapters: List[Dict[str, Any]], lines: Dict[str, Dict[str, Any]], intro_length: float, card_length: float) -> Dict[str, Any]:
    """
    `steps`: each `{id, text, edit, zoom, band, chapter}`; `chapters`: each `{title, step}`, the index
    of the step it opens on. Returns `{scene, duration, timeline}`.
    """
    bg = spec.get('background') or '#0b0c10'
    surface = spec.get('surface') or '#1d2029'
    ink = spec.get('text') or '#f4f5f7'
    font = spec['font']
    nest = spec.get('clip') == 'nest'
    keep = spec['narration'] == 'own'
    layers: List[Layer] = []
    audio: List[Layer] = []
    assets: Dict[str, Any] = {}
    timeline: List[Dict[str, Any]] = []
    t = 0.0

    # The finished result first, on a card over its own blurred footage, under the title.
    intro = spec['intro']
    box = intro['box']
    card = card_box(box)
    layers.append(backdrop('intro_backdrop', intro['at'], t, intro_length, src_len))
    layers.append(rim_layer('intro_rim', card, surface, t, intro_length, 8 if nest else 42))
    S = max(min_scale(src, card), min(STILL_MAX, fit_scale(box, card)))
    p = pose(src, FRAME, card, {'S': S, 'F': clamp_focus(src, card, S, center(box))})
    layers.append({'id': 'intro_panel', 'start': 0, 'duration': round(intro_length, 3), 'transform': {'position': p['position'], 'scale': p['scale']}, 'content': still(intro['at'], intro_length, src_len, 'contain'), 'mask': panel_mask('intro_mask', card, 28)})
    layers.append(text_layer('intro_title', spec['title'], font, TITLE_PX, ink, [960, 130], t + 0.2, intro_length - 0.2))
    timeline.append({'id': 'intro', 'kind': 'intro', 'start': 0, 'end': round(intro_length, 3)})
    t += intro_length

    opens = {c['step']: (j, c['title']) for j, c in enumerate(chapters)}
    for k, s in enumerate(steps):
        if k in opens:
            j, title = opens[k]
            cid = f'chapter_{j}'
            layers.append(backdrop(f'{cid}_backdrop', s['edit']['srcStart'], t, card_length, src_len))
            layers.append(text_layer(f'{cid}_title', [title], font, TITLE_PX, ink, [960, 540], t + 0.1, card_length - 0.1))
            timeline.append({'id': cid, 'kind': 'chapter', 'title': title, 'start': round(t, 3), 'end': round(t + card_length, 3)})
            t += card_length
        d = s['edit']['duration']
        clips = [{'id': f"{s['id']}_clip{i}", 'duration': round(pc['outOut'] - pc['outIn'], 3), 'content': media(pc['srcIn'], pc['srcOut'], pc['speed'], 'contain', keep)} for i, pc in enumerate(s['edit']['pieces'])]
        zoom = s['zoom']
        rec: Layer = {'id': f"{s['id']}_rec", 'start': round(t, 3), 'duration': d, 'timeMode': 'layer', 'transform': {'position': zoom['position'][0]['value'], 'scale': zoom['scale'][0]['value']}}
        if len(zoom['scale']) > 1:
            rec['animations'] = {'scale': {'keyframes': [kf(x) for x in zoom['scale']]}, 'position': {'keyframes': [kf(x) for x in zoom['position']]}}
        rec['content'] = clips[0]['content'] if len(clips) == 1 else {'kind': 'track', 'clips': clips}
        layers.append(rec)
        lb = line_box(len(s['text']), s['band'])
        layers.append(bubble(f"{s['id']}_bubble", lb, surface, t, d))
        layers.append(text_layer(f"{s['id']}_line", s['text'], font, LINE_PX, ink, center(lb), t + 0.1, d - 0.1))
        entry = {'id': s['id'], 'kind': 'step', 'chapter': s['chapter'], 'start': round(t, 3), 'end': round(t + d, 3), 'band': s['band']}
        voice = lines.get(s['id'])
        if voice is not None:
            asset = f"line_{s['id']}"
            assets[asset] = {'type': 'audio', 'uri': voice['url'], 'duration': voice['duration']}
            audio.append({'id': f"{s['id']}_voice", 'start': round(t, 3), 'duration': round(voice['duration'], 3), 'content': {'kind': 'audio', 'assetId': asset, 'trim': {'in': 0, 'out': round(voice['duration'], 3)}}})
            entry['line'] = {'start': round(t, 3), 'end': round(t + voice['duration'], 3)}
        if s['edit'].get('wait') is not None:
            entry['wait'] = s['edit']['wait']
        timeline.append(entry)
        t += d

    duration = round(t, 3)
    rec_asset = {'type': 'video', 'uri': spec['uri'], 'width': src['w'], 'height': src['h'], 'duration': src_len}
    assets = {'rec': rec_asset, **assets}
    all_layers = layers + audio
    if nest:
        all_layers = [nest_panel(l, src, rec_asset, assets, FRAME) if l.get('mask') else l for l in all_layers]
    scene = {
        'version': '1.0',
        'composition': {'width': FRAME['w'], 'height': FRAME['h'], 'fps': 30, 'duration': duration, 'background': bg},
        'assets': assets,
        'layers': all_layers,
    }
    return {'scene': scene, 'duration': duration, 'timeline': timeline}


def frame_rect(src: Dict[str, float], box: Dict[str, float], scale: List[float], position: List[float]) -> Dict[str, float]:
    """Where a source box lands in the frame, under a layer's scale and position."""
    S = scale[0] * fit_base(src, FRAME)
    return {'x': position[0] + S * (box['x'] - src['w'] / 2), 'y': position[1] + S * (box['y'] - src['h'] / 2), 'w': S * box['w'], 'h': S * box['h']}


def band_for(src: Dict[str, float], boxes: List[Dict[str, float]], zoom: Dict[str, Any], lines: int) -> str:
    """
    The lower third, unless an action's box covers more of it at the push's peak than of the top
    band: then the top band.
    """
    peak = max(range(len(zoom['scale'])), key=lambda i: zoom['scale'][i]['value'][0])
    rects = [frame_rect(src, b, zoom['scale'][peak]['value'], zoom['position'][peak]['value']) for b in boxes]

    def covered(band: str) -> float:
        lb = line_box(lines, band)
        total = 0.0
        for r in rects:
            w = min(r['x'] + r['w'], lb['x'] + lb['w']) - max(r['x'], lb['x'])
            h = min(r['y'] + r['h'], lb['y'] + lb['h']) - max(r['y'], lb['y'])
            total += max(0.0, w) * max(0.0, h)
        return total

    return 'top' if covered('bottom') > covered('top') + 1e-6 else 'bottom'


def whole_source(src: Dict[str, float], content: Dict[str, float]) -> Dict[str, float]:
    """The box the rest framing fits: the whole recording, centred on its content."""
    cx, cy = center(content)
    return {'x': cx - src['w'] / 2, 'y': cy - src['h'] / 2, 'w': src['w'], 'h': src['h']}
