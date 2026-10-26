"""
Compile a screen promo into one scene: a hook on the final result, one prompt-over-result beat
per step, and a results grid with the call to action.

Every recording panel is a `fit: "contain"` media layer clipped by a rounded-rect shape mask,
framed with the screen-recording-layouts skill's framing formula (`framing.py`, which says why not `cover`). A step
with several pieces is a `track` of clips, so one zoom and one mask apply across all of its jumps
and speed changes. With `clip: "nest"` each masked panel is instead its own panel-sized nested
scene, which clips at its edge: square corners, no mask.

A panel that is the whole frame (a portrait source, see `FULL_FRAME`) needs no clip at all: the
composition clips it. It gets no mask, no rim and no backdrop, and a scrim shades the top band
wherever words sit on the video without a bubble: black under light ink, the canvas under dark.

A step here is `{id, prompt?, label?, edit, zoom, result, labels?, panel?, backdrop?}`:
- `prompt`: the request, re-typed large, one entry per line (about 30 characters at 42 px);
- `label`: a feature line, for a step with no typed request: shown on the prompt's bubble, sliding
  up rather than typed, and ignored when there is a prompt;
- `result`: the moment its hook and grid cell show (`Shown`, below);
- `labels`: words in the top band while it plays, `{at, until, text}` in step-relative seconds;
- `panel`: by default the prompt layout's when there are words, else the tall panel;
- `backdrop`: fill the frame behind the panel with the same clips, blurred and darkened.

A `Shown` is `{box, settle, subject?, at?, length?}`: a source-px box and the second it settles; its
subject, whose margin is already grown over flat pixels, so it is framed as it is (padding it
again reaches into the card's header and buttons); and the source second shown (default 0.2 s
after `settle`), which in an edited input stays inside the result's own shot. A short settled tail
shortens the still's source `length` from 0.15 s.
"""
from __future__ import annotations

import math
from typing import Any, Dict, List, Optional

from _geometry import Box, Size, Vec2, center, pad, round
from _js import js_max, math_round
from framing import RECORDING_FIT, fit_scale, min_scale, pose
from panels import bubble, nest_panel, panel_mask, rim_layer
from safe_zone import CHAR_EM, LINE_EM, rail_boxes, safe_box, wrapped, zone
from style import contrast
from zoom import HOUSE_EASING, clamp_focus

Layer = Dict[str, Any]

COMP: Size = {'w': 1080, 'h': 1920}
# Promos ship to all three short-video destinations; use their strictest margins.
SAFE = safe_box(zone(['reels', 'tiktok', 'shorts']), COMP['w'], COMP['h'])

# The screen-recording-layouts skill's prompt-over-result frame.
PROMPT_LAYOUT = {
    'bubble': {'x': 60, 'y': 280, 'w': 960, 'h': 210},
    'panel': {'x': 40, 'y': 600, 'w': 1000, 'h': 1280},
}
TALL_PANEL: Box = {'x': 40, 'y': 480, 'w': 1000, 'h': 1400}
# A portrait source's panel: it fills the frame, and the words sit over it.
FULL_FRAME: Box = {'x': 0, 'y': 0, 'w': COMP['w'], 'h': COMP['h']}
# A square source's panel: the frame's width, under the text band.
SQUARE_PANEL: Box = {'x': 0, 'y': 640, 'w': COMP['w'], 'h': COMP['w']}


def is_full_frame(b: Box) -> bool:
    return b['x'] <= 0 and b['y'] <= 0 and b['x'] + b['w'] >= COMP['w'] and b['y'] + b['h'] >= COMP['h']


def card_panel(focus: Box, width: float = 1000, center_y: float = 1180) -> Box:
    """
    A floating card: full panel width, as tall as the focus's aspect needs, centred where the tall
    panel sits. For a landscape result a vertical panel could only show a slice of.
    """
    h = math_round(min(1400, max(560, (width * focus['h']) / focus['w'])))
    return {'x': (COMP['w'] - width) / 2, 'y': math_round(center_y - h / 2), 'w': width, 'h': h}


GRID = {'cell': {'w': 470, 'h': 700}, 'gap': 24, 'top': 220}
# A still is never shown larger than this many output px per source px: past it, it goes soft.
STILL_MAX_SCALE = 1.2


def compile_promo(spec: Dict[str, Any]) -> Dict[str, Any]:
    """
    `spec`: `source` ({uri, w, h, duration}), `font` (a font key naming the face itself, e.g. a bold
    face: the translators ignore `font.weight`; or a live face's https file URL on a picsart.com host), `hook` ({title, step, duration?}), `steps`, `outro`
    ({cta, steps, stills?, duration?}: the grid shows each named step's result, or the `stills`
    when given), `clip` and `sourceAudio`, and optionally `sfx` (see `sound_effects`) and `style`, a
    style's resolved tokens (`canvas`, `surface`: bubbles and panel rims, `ink`, `accent`: the call to
    action, and `entrance` per role). Without a style, `background`, `surface` and `text` still set
    the old palette.

    `clip`: how a panel clips its recording. `mask` (default): a rounded-rect mask, the look. `nest`:
    a panel-sized nested scene, square-cornered, for when masked layers do not render (the Dev
    exporter on 2026-09-30 refused every mask: "the authored mask carries no clip").
    `sourceAudio`: `mute` (default), or `keep`: clips that play at 1x are unmuted. A sped-up or
    slowed clip stays muted, because its speech would be pitched. A step's `sourceAudio: mute`
    silences that step independently.
    """
    # A style's tokens (the visual-style skill's style.py) colour the promo and pick its entrances.
    # Without one, the promo keeps the palette it was built with before styles.
    style = spec.get('style') or {}
    entrance = style.get('entrance') or {}
    bg = style.get('canvas') or spec.get('background') or '#0b0c10'
    surface = style.get('surface') or spec.get('surface') or '#1d2029'
    ink = style.get('ink') or spec.get('text') or '#f4f5f7'
    accent = style.get('accent') or ink
    shade = scrim_color(ink, bg)
    title_in = entrance.get('title', 'slide_up_lines')
    line_in = entrance.get('line', 'slide_up_lines')
    cta_in = entrance.get('cta', 'slide_up_lines')
    source = spec['source']
    src: Size = {'w': source['w'], 'h': source['h']}
    nest = spec.get('clip') == 'nest'

    def rim(id_: str, panel: Box, color: str, start: float, duration: float) -> Layer:
        return rim_layer(id_, panel, color, start, duration, 8 if nest else 42)

    layers: List[Layer] = []
    timeline: List[Dict[str, Any]] = []
    t = 0
    steps = spec['steps']

    # Hook: the final result, held, with the title in the top band — on the same card as its step.
    hook = spec['hook']
    hook_step = _or(next((s for s in steps if s['id'] == hook.get('step')), None), steps[-1])
    hook_duration = _or(hook.get('duration'), 2.2)
    hook_panel = _or(hook_step.get('panel'), TALL_PANEL)
    hook_full = is_full_frame(hook_panel)
    hook_still = still_panel('hook', spec, src, hook_panel, hook_step['result'], t, hook_duration, 1.0)
    if hook_step.get('backdrop') and not hook_full:
        plain = {k: v for k, v in hook_still.items() if k not in ('mask', 'transform')}
        layers.append({**plain, 'id': 'hook_backdrop', 'content': {**plain['content'], 'fit': 'cover'}, 'effects': BACKDROP_EFFECTS})
    if not hook_full:
        layers.append(rim('hook_rim', hook_panel, surface, t, hook_duration))
    layers.append(hook_still)
    # A hook with no words (`title: []`) is the picture alone: no title, and no scrim to read it on.
    if hook['title']:
        if hook_full:
            layers.append(scrim('hook_scrim', t, hook_duration, shade))
        layers.append(text_layer('hook_title', hook['title'], spec['font'], 76, ink, [540, 300], t, hook_duration, title_in))
    timeline.append({'id': 'hook', 'start': t, 'end': round(t + hook_duration, 3)})
    t += hook_duration

    for step in steps:
        d = step['edit']['duration']
        words = step['prompt'] if step.get('prompt') is not None else step.get('label')
        panel = _or(step.get('panel'), PROMPT_LAYOUT['panel'] if words is not None else TALL_PANEL)
        full = is_full_frame(panel)
        if step.get('backdrop') and not full:
            layers.append(backdrop(step, t))
        if not full:
            layers.append(rim(f"{step['id']}_rim", panel, surface, t, d))
        layers.append(recording_panel(step, panel, t, spec.get('sourceAudio') == 'keep' and step.get('sourceAudio') != 'mute'))
        if full and step.get('labels'):
            layers.append(scrim(f"{step['id']}_scrim", t, d, shade))
        for i, label in enumerate(step.get('labels') or []):
            layers.append(text_layer(f"{step['id']}_label{i}", label['text'], spec['font'], 64, ink, [540, 300], t + label['at'], label['until'] - label['at'], line_in))
        if words is not None:
            # A typed request is re-typed; a feature line slides up, as a caption would.
            typed = step.get('prompt') is not None
            bubble_box = PROMPT_LAYOUT['bubble']
            layers.append(bubble(f"{step['id']}_bubble", bubble_box, surface, t, d))
            layers.append(text_layer(f"{step['id']}_{'prompt' if typed else 'label'}", words, spec['font'], 42, ink, center(bubble_box), t + 0.1, d - 0.1, 'typewriter' if typed else line_in))
        timeline.append({'id': step['id'], 'start': round(t, 3), 'end': round(t + d, 3)})
        t += d

    # Outro: every chosen result side by side, then the call to action.
    outro = spec['outro']
    outro_duration = _or(outro.get('duration'), 2.5)
    if outro.get('stills') is not None:
        candidates = outro['stills']
    else:
        candidates = [next((s['result'] for s in steps if s['id'] == id_), None) for id_ in outro['steps']]
    shown = [r for r in candidates if r is not None][:4]
    cols = 1 if len(shown) == 1 else 2
    rows = math.ceil(len(shown) / cols)
    cta_half = text_height(outro['cta'], 64) / 2
    # Leave room for each card's 6 px rim and for rounded positions.
    grid_h = SAFE['h'] - 150 - cta_half - 14
    slot = {
        'w': min(GRID['cell']['w'], (SAFE['w'] - 14 - (cols - 1) * GRID['gap']) / cols),
        'h': min(GRID['cell']['h'], (grid_h - (rows - 1) * GRID['gap']) / max(1, rows)),
    }
    grid_w = cols * slot['w'] + (cols - 1) * GRID['gap']
    # Cells take their content's shape, so a row is as tall as its tallest cell, and the rows sit
    # together, centred where full-height slots would have been.
    sized = [subject_cell({'x': 0, 'y': 0, **slot}, s.get('subject') or pad(s['box'], 0.06, src)) for s in shown]
    row_h = [js_max(c['h'] for c in sized[r * cols:r * cols + cols]) for r in range(rows)]
    block_h = _sum(row_h) + (rows - 1) * GRID['gap']
    grid_top = SAFE['y'] + 7 + (rows * slot['h'] + (rows - 1) * GRID['gap'] - block_h) / 2
    for i, s in enumerate(shown):
        r = i // cols
        inner = sized[i]
        above = 0
        for h in row_h[:r]:
            above = above + h + GRID['gap']
        cell: Box = {
            'x': (COMP['w'] - grid_w) / 2 + (i % cols) * (slot['w'] + GRID['gap']) + inner['x'],
            'y': math_round(grid_top + above + (row_h[r] - inner['h']) / 2),
            'w': inner['w'],
            'h': inner['h'],
        }
        layers.append(rim(f'grid_{i}_rim', cell, surface, t + i * 0.08, outro_duration - i * 0.08))
        layers.append(still_panel(f'grid_{i}', spec, src, cell, s, t + i * 0.08, outro_duration - i * 0.08, 1))
    cta_y = grid_top + block_h + 150
    layers.append(text_layer('outro_cta', outro['cta'], spec['font'], 64, accent, [540, cta_y], t + 0.3, outro_duration - 0.3, cta_in))
    timeline.append({'id': 'outro', 'start': round(t, 3), 'end': round(t + outro_duration, 3)})
    t += outro_duration

    duration = round(t, 3)
    rec = {'type': 'video', 'uri': source['uri'], 'width': source['w'], 'height': source['h'], 'duration': source['duration']}
    assets: Dict[str, Any] = {'rec': rec}
    sounds = sound_effects(spec.get('sfx'), steps, timeline, duration)
    for name in ('push', 'outro'):
        if any(l['content']['assetId'] == f'sfx_{name}' for l in sounds):
            assets[f'sfx_{name}'] = {'type': 'audio', 'uri': spec['sfx'][name]['url'], 'duration': spec['sfx'][name]['duration']}
    layers += sounds
    placed = [nest_panel(l, src, rec, assets, COMP) if l.get('mask') else l for l in layers] if nest else layers
    return {
        'scene': {
            'version': '1.0',
            'composition': {'width': COMP['w'], 'height': COMP['h'], 'fps': 30, 'duration': duration, 'background': bg},
            'assets': assets,
            'layers': placed,
        },
        'duration': duration,
        'timeline': timeline,
    }


# A sound effect's level, as the scene's volume percent: under a voice, over a music bed.
SFX_VOLUME = 35


def sound_effects(sfx: Optional[Dict[str, Any]], steps: List[Dict[str, Any]], timeline: List[Dict[str, Any]], duration: float) -> List[Layer]:
    """
    The promo's sound effects, each tied to something the picture does: `push` as each step's push
    onto its result starts, and `outro` as the grid comes in. Each sound is `{url, duration}`, and
    `volume` sets their level. None plays past the end.
    """
    if not sfx:
        return []
    starts = {s['id']: s['start'] for s in timeline}
    volume = _or(sfx.get('volume'), SFX_VOLUME)
    cues = []
    if sfx.get('push'):
        for step in steps:
            ramp = next((k for k in step['zoom']['scale'] if k.get('easing') == HOUSE_EASING), None)
            if ramp is not None:
                cues.append((f"sfx_{step['id']}", 'push', starts[step['id']] + ramp['time']))
    if sfx.get('outro'):
        cues.append(('sfx_outro', 'outro', starts['outro']))
    out: List[Layer] = []
    for id_, name, at in cues:
        at = round(at, 3)
        length = round(min(sfx[name]['duration'], duration - at), 3)
        if length <= 0:
            continue
        out.append({'id': id_, 'start': at, 'duration': length, 'content': {'kind': 'audio', 'assetId': f'sfx_{name}', 'trim': {'in': 0, 'out': length}, 'volume': volume}})
    return out


def _or(value: Any, default: Any) -> Any:
    """`value ?? default`: only a missing value takes the default."""
    return default if value is None else value


def _sum(xs: List[float]) -> float:
    s = 0
    for x in xs:
        s = s + x
    return s


def text_height(lines: List[str], size: float) -> float:
    return max(1, len(wrapped(lines, size, COMP['w']))) * size * LINE_EM


def text_layer(id_: str, lines: List[str], font: str, size: float, color: str, at: Vec2, start: float, duration: float, preset: str) -> Layer:
    lines = wrapped(lines, size, COMP['w'])
    chars = max(1, max((len(line) for line in lines), default=0))
    size = min(size, (SAFE['w'] - 2) / (chars * CHAR_EM), (SAFE['h'] - 2) / (max(1, len(lines)) * LINE_EM))
    half = text_height(lines, size) / 2
    at = [at[0], max(SAFE['y'] + half + 1, min(at[1], SAFE['y'] + SAFE['h'] - half - 1))]
    right = SAFE['x'] + SAFE['w']
    for rail in rail_boxes(zone(['reels', 'tiktok', 'shorts']), COMP['w'], COMP['h']):
        if at[1] + half > rail['y'] and at[1] - half < rail['y'] + rail['h']:
            right = min(right, rail['x'])
    size = min(size, (right - SAFE['x'] - 2) / (chars * CHAR_EM))
    width = chars * size * CHAR_EM
    at[0] = max(SAFE['x'] + width / 2 + 1, min(at[0], right - width / 2 - 1))
    return {
        'id': id_,
        'start': round(start, 3),
        'duration': round(duration, 3),
        'transform': {'position': at},
        'content': {
            'kind': 'text',
            'text': lines,
            'font': {'family': font, 'size': size},
            'color': color,
            'alignment': 'center',
            'animations': [{'preset': preset, 'params': {'duration': 0.9 if preset == 'typewriter' else 0.5}}],
        },
    }


def audible_at(speed: float) -> bool:
    """A clip plays its own sound only at 1x: a sped-up clip's speech is pitched and chopped."""
    return abs(speed - 1) <= 1e-3


def media(src_in: float, src_out: float, speed: float, fit: str = RECORDING_FIT, audible: bool = False) -> Dict[str, Any]:
    """
    A recording clip. The speed is floored, never rounded: the layer must not outlast
    `(out - in) / speed`, or one engine holds the last frame and the other wraps to the trim start.
    `audible` unmutes it, and only takes effect at 1x.
    """
    content = {
        'kind': 'media',
        'assetId': 'rec',
        'fit': fit,
        'muted': not (audible and audible_at(speed)),
        'trim': {'in': round(src_in, 3), 'out': round(src_out, 3)},
    }
    if not audible_at(speed):
        content['speed'] = math.floor(speed * 1e4) / 1e4
    return content


def recording_panel(step: Dict[str, Any], panel: Box, start: float, audible: bool = False) -> Layer:
    sid = step['id']
    clips = [
        {'id': f'{sid}_clip{i}', 'duration': round(p['outOut'] - p['outIn'], 3), 'content': media(p['srcIn'], p['srcOut'], p['speed'], RECORDING_FIT, audible)}
        for i, p in enumerate(step['edit']['pieces'])
    ]
    zoom = step['zoom']
    layer: Layer = {
        'id': f'{sid}_panel',
        'start': round(start, 3),
        'duration': step['edit']['duration'],
        'timeMode': 'layer',
        'transform': {'position': zoom['position'][0]['value'], 'scale': zoom['scale'][0]['value']},
    }
    if len(zoom['scale']) > 1:
        layer['animations'] = {'scale': {'keyframes': [kf(k) for k in zoom['scale']]}, 'position': {'keyframes': [kf(k) for k in zoom['position']]}}
    layer['content'] = clips[0]['content'] if len(clips) == 1 else {'kind': 'track', 'clips': clips}
    if not is_full_frame(panel):
        layer['mask'] = panel_mask(f'{sid}_mask', panel)
    return layer


# The top band darkened, under words that sit on the video itself.
SCRIM: Box = {'x': 0, 'y': 0, 'w': COMP['w'], 'h': 640}
BLACK = '#000000'


def scrim_color(ink: str, canvas: str) -> str:
    """
    The shade a scrim washes the video with: black under light ink, and under a light style's dark
    ink its own canvas, which the style already checked the ink against.
    """
    return BLACK if contrast(ink, BLACK) >= contrast(ink, canvas) else canvas


def scrim(id_: str, start: float, duration: float, color: str = BLACK, box: Box = SCRIM) -> Layer:
    return {
        'id': id_,
        'start': round(start, 3),
        'duration': round(duration, 3),
        'timeMode': 'layer',
        'transform': {'position': center(box)},
        'content': {'kind': 'shape', 'items': [{'type': 'rect', 'size': [box['w'], box['h']], 'roundness': 0}, {'type': 'fill', 'color': color}]},
        'animations': {'opacity': {'keyframes': [{'time': 0, 'value': 0, 'easing': 'linear'}, {'time': 0.2, 'value': 0.55}]}},
    }


def backdrop(step: Dict[str, Any], start: float) -> Layer:
    """The step's own clips, cover-fit over the whole frame, blurred and darkened behind the card."""
    sid = step['id']
    clips = [
        {'id': f'{sid}_bg{i}', 'duration': round(p['outOut'] - p['outIn'], 3), 'content': media(p['srcIn'], p['srcOut'], p['speed'], 'cover')}
        for i, p in enumerate(step['edit']['pieces'])
    ]
    return {
        'id': f'{sid}_backdrop',
        'start': round(start, 3),
        'duration': step['edit']['duration'],
        'content': clips[0]['content'] if len(clips) == 1 else {'kind': 'track', 'clips': clips},
        'effects': BACKDROP_EFFECTS,
    }


BACKDROP_EFFECTS = [
    {'id': 'gaussian_blur', 'params': {'blur': 60}},
    {'id': 'adjust', 'params': {'brightness': -0.35, 'saturation': -0.1}},
]


def kf(k: Dict[str, Any]) -> Dict[str, Any]:
    out = {'time': k['time'], 'value': k['value']}
    if k.get('easing'):
        out['easing'] = k['easing']
    return out


def subject_cell(slot: Box, focus: Box) -> Box:
    """
    A grid cell the shape of what it shows (the subject, or else the padded box), centred in its
    slot, at the still's scale, and no more. A fixed portrait cell around a smaller subject shows the
    chat card's header and buttons at its edges, and a landscape subject in it zooms out to the chat
    around it.
    """
    S = min(STILL_MAX_SCALE, fit_scale(focus, slot))
    w = math_round(focus['w'] * S)
    h = math_round(focus['h'] * S)
    return {'x': math_round(slot['x'] + (slot['w'] - w) / 2), 'y': math_round(slot['y'] + (slot['h'] - h) / 2), 'w': w, 'h': h}


def still_panel(id_: str, spec: Dict[str, Any], src: Size, panel: Box, result: Dict[str, Any], start: float, duration: float, fill: float) -> Layer:
    """A panel on one result, near-frozen on the frames just after it settles."""
    focus = result.get('subject') or pad(result['box'], 0.06, src)
    S = max(min_scale(src, panel), min(STILL_MAX_SCALE, fit_scale(focus, panel) * fill))
    F = clamp_focus(src, panel, S, center(focus))
    p = pose(src, COMP, panel, {'S': S, 'F': F})
    shown_at = result['at'] if result.get('at') is not None else result['settle'] + 0.2
    src_in = min(shown_at, spec['source']['duration'] - result.get('length', 0.2))
    src_out = min(src_in + result.get('length', 0.15), spec['source']['duration'])
    layer: Layer = {
        'id': f'{id_}_panel',
        'start': round(start, 3),
        'duration': round(duration, 3),
        'transform': {'position': p['position'], 'scale': p['scale']},
        'content': media(src_in, src_out, (src_out - src_in) / duration),
    }
    if not is_full_frame(panel):
        layer['mask'] = panel_mask(f'{id_}_mask', panel, 28)
    return layer
