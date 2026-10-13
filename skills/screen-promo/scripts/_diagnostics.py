"""
What a built scene gets wrong that its spec can put right. The builder returns these beside the
scene, and every `fix` names the spec field to change ("set steps[2].to to 38.0"), never a scene
edit: the scene is rebuilt from the spec, so an edit to it is lost on the next build.

An `error` is a flaw a viewer sees: the next shot flashing at the end of a step, a panel on the
wrong part of the screen. A `warning` is a risk worth a look: small text, a long stretch with
nothing to read, a length off target, sound that will not play.

A diagnostic is `{level, code, layer?, message, fix}`: `layer` is the scene layer it is about,
when there is one, and `fix` the spec field to change, and to what.

A checked step is a dict:
- `field`: the spec path fixes name: `steps[2]`, `process`, `reveal`;
- `id`: the step's id in the scene: its panel layer is `<id>_panel`;
- `edit`; `words` (words over the whole step: a prompt or a feature line); `labels` (words over
  part of it, `{at, until}` in step-relative output seconds);
- `textPx`: UI text at rest, frame px, for a step that is read on screen;
- `settle`: the source second its result settles;
- `cutFix(cut, after)`: the fix for a piece that shows the cut at `cut`; `after` when the cut is
  after the result; `wordsFix(from_)`: the fix for a stretch with nothing to read, starting
  `from_` output seconds into the step; `contentFix`: the fix for a panel window outside the
  content box; `audioFix`: the fix for its sped-up clips muted under `sourceAudio: 'keep'`;
- `pushSkipped` (`{at, room}`, the push onto its result that did not fit) and `pushFix`;
- `settleCut` (`{to, settles}`: its `to`, and the source second its result really settles, when
  that `to` moved the push before it) and `settleFix`; `holdFix`, for a hold slower than
  `LIMITS['holdSpeed']`.

A result sample is a still taken from the recording, the hook's and each grid cell's: `layer`,
`at` (source second), `length` (source seconds it plays: a still is a 0.15 s trim), `step` (the
checked step whose result it shows, when it shows one) and `fix`.

A panel check is a panel the content check covers besides the steps' own, the hook's and the
outro grid's: `layer`, `span` (the timeline span it plays in), `name` (how the message names it,
by spec field: `hook (setup)`, `outro.at[1] (636 s)`) and `fix`.

A checked line of words is `{field, kind, lines}`: `kind` is `hook`, `label` (a feature line or a
chapter's words), `cta` or `prompt`. A prompt is the user's own typed request and is never checked.
The word checks read English only, and are warnings: spec.md, The words, says why each one costs.
"""
from __future__ import annotations

import re
from typing import Any, Callable, Dict, List, Optional

from _geometry import Box, area, round
from _js import js_max, js_min, math_round, number, to_fixed
from _moments import Moments, input_of
from _preview import panel_shots
from _scene import COMP
from _steps import shot_at
from zoom import DEFAULT_ZOOM

Diagnostic = Dict[str, Any]
CheckedStep = Dict[str, Any]

LIMITS = {
    # UI text at rest below this, frame px, is hard to read on a phone.
    'textPx': 24,
    # Output seconds a step may run with nothing to read.
    'silent': 4,
    # Share of the target the length may be off by.
    'target': 0.2,
    # Share of a panel's window that must lie in the content box.
    'inside': 0.5,
    # A result's hold below this speed reads as a freeze: each source frame lasts more than two
    # frames of the promo. Holds with 1.0 s of source or more play at 0.56x or faster, and flash
    # shots chosen by from/to held at 0.11x to 0.28x (yt-IpP3AemLsbo, 2026-10-01).
    'holdSpeed': 0.5,
}


def cuts_inside(span: Dict[str, float], cuts: List[float], fps: float) -> List[float]:
    """The cuts a source span shows: a cut at `c` (analysed) happened within the frame before it."""
    return [c for c in cuts if c > span['srcIn'] + 1e-3 and c - 1 / fps < span['srcOut'] - 1e-3]


def _intersect(a: Box, b: Box) -> Optional[Box]:
    x = max(a['x'], b['x'])
    y = max(a['y'], b['y'])
    w = min(a['x'] + a['w'], b['x'] + b['w']) - x
    h = min(a['y'] + a['h'], b['y'] + b['h']) - y
    return {'x': x, 'y': y, 'w': w, 'h': h} if w > 0 and h > 0 else None


def share_inside(window: Box, content: Box) -> float:
    """The share of `window` that lies inside `content`."""
    i = _intersect(window, content)
    return area(i) / area(window) if i else 0


def longest_gap(duration: float, covered: List[Dict[str, float]]) -> Dict[str, float]:
    """The longest stretch of [0, duration] no interval covers."""
    spans = sorted(covered, key=lambda s: s['at'])
    best = {'from': 0, 'to': 0}
    t = 0
    for s in [*spans, {'at': duration, 'until': duration}]:
        if s['at'] - t > best['to'] - best['from']:
            best = {'from': t, 'to': min(s['at'], duration)}
        t = max(t, s['until'])
    return best


# Each script by the code points of its block, and the languages that write in it.
SCRIPTS = [
    {'name': 'Cyrillic', 'range': (0x0400, 0x04FF), 'languages': ['ru', 'uk', 'be', 'bg', 'sr', 'mk', 'kk', 'ky', 'mn', 'tg']},
    {'name': 'Armenian', 'range': (0x0530, 0x058F), 'languages': ['hy']},
    {'name': 'Georgian', 'range': (0x10A0, 0x10FF), 'languages': ['ka']},
    {'name': 'Greek', 'range': (0x0370, 0x03FF), 'languages': ['el']},
    {'name': 'Arabic', 'range': (0x0600, 0x06FF), 'languages': ['ar', 'fa', 'ur', 'ps']},
    {'name': 'Hebrew', 'range': (0x0590, 0x05FF), 'languages': ['he', 'yi']},
    {'name': 'Devanagari', 'range': (0x0900, 0x097F), 'languages': ['hi', 'mr', 'ne']},
    {'name': 'Thai', 'range': (0x0E00, 0x0E7F), 'languages': ['th']},
    {'name': 'Japanese', 'range': (0x3040, 0x30FF), 'languages': ['ja']},
    {'name': 'Korean', 'range': (0xAC00, 0xD7AF), 'languages': ['ko']},
    {'name': 'Chinese', 'range': (0x4E00, 0x9FFF), 'languages': ['zh']},
]


def script_of(language: Optional[str], texts: List[str]) -> Optional[str]:
    """The non-Latin script a spec writes in, from its `language` (BCP-47) or its text."""
    primary = language.lower().split('-')[0] if language is not None else None
    named = next((s for s in SCRIPTS if primary and primary in s['languages']), None)
    if named:
        return named['name']
    text = '\n'.join(texts)
    for s in SCRIPTS:
        lo, hi = s['range']
        if any(lo <= ord(ch) <= hi for ch in text):
            return s['name']
    return None


def s1(t: float) -> str:
    return to_fixed(t, 1)


# What stops a hold's source, as a message says it.
HOLD_ENDS = {
    'to': 'its to stops it',
    'shot': 'its shot ends',
    'recording': 'the recording ends',
    'next_step': 'a later step starts showing the recording',
}


def diagnose(c: Dict[str, Any]) -> List[Diagnostic]:
    """
    `c`: `a` (the moments), `scene`, `timeline`, `steps` (checked steps), `samples` (result
    samples), `panels` (panel checks), `duration`, `target`, `lengthFix(duration, target)`,
    `sourceAudio`, `language`, `font`, `texts` (every line of text the scene shows) and `words`
    (checked lines of words).
    """
    out: List[Diagnostic] = []
    a: Moments = c['a']
    info = input_of(a)
    fps = a['analysis']['fps']
    cut_level = 'error' if info['edited'] else 'warning'

    # Cuts: no piece may show one, and no hold may play into the next shot.
    for step in c['steps']:
        for p in step['edit']['pieces']:
            for cut in cuts_inside(p, info['cuts'], fps):
                hold = p['role'] == 'hold'
                after = cut > (p['srcIn'] if step.get('settle') is None else step['settle'])
                if hold:
                    message = f"{step['field']} ({step['id']}): its hold plays {s1(p['srcIn'])}–{s1(p['srcOut'])} s, past the cut at {s1(cut)} s, so it ends on the next shot"
                else:
                    message = f"{step['field']} ({step['id']}): a {p['role']} clip plays {s1(p['srcIn'])}–{s1(p['srcOut'])} s, across the cut at {s1(cut)} s"
                out.append({
                    'level': cut_level,
                    'code': 'hold_past_cut' if hold else 'trim_crosses_cut',
                    'layer': f"{step['id']}_panel",
                    'message': message,
                    'fix': step['cutFix'](cut, after),
                })
    for s in c['samples']:
        for cut in cuts_inside({'srcIn': s['at'], 'srcOut': s['at'] + s['length']}, info['cuts'], fps):
            out.append({'level': cut_level, 'code': 'trim_crosses_cut', 'layer': s['layer'], 'message': f"{s['layer']}: its still at {s1(s['at'])} s runs across the cut at {s1(cut)} s", 'fix': s['fix']})

    # A result's still must come from its own step, and in an edited input from its own shot.
    for s in c['samples']:
        step = s.get('step')
        if not step:
            continue
        pieces = step['edit']['pieces']
        lo = js_min(p['srcIn'] for p in pieces)
        hi = js_max(p['srcOut'] for p in pieces)
        settle = hi if step.get('settle') is None else step['settle']
        in_step = s['at'] >= lo - 1e-3 and s['at'] + s['length'] <= hi + 1e-3
        shot = shot_at(a, settle)
        in_shot = not info['edited'] or (s['at'] >= shot['start'] - 1e-3 and s['at'] + s['length'] <= shot['end'] + 1e-3)
        if in_step and in_shot:
            continue
        where = f", shot {s1(shot['start'])}–{s1(shot['end'])} s" if info['edited'] else ''
        out.append({
            'level': 'error',
            'code': 'result_sample_outside_step',
            'layer': s['layer'],
            'message': f"{s['layer']}: its still at {s1(s['at'])} s is outside {step['field']} ({s1(lo)}–{s1(hi)} s{where})",
            'fix': s['fix'],
        })

    # Each panel's window stays mostly on the content, at rest and at the step's end (a step never
    # zooms back out). A panel that fills the frame shows the whole source by design. The hook's and
    # the outro grid's panels are checked the same way.
    panels = [
        *({'layer': f"{s['id']}_panel", 'span': s['id'], 'name': f"{s['field']} ({s['id']})", 'fix': s['contentFix']} for s in c['steps']),
        *(c.get('panels') or []),
    ]
    for p in panels:
        span = next((x for x in c['timeline'] if x['id'] == p['span']), None)
        if not span:
            continue
        worst = None
        for t in (span['start'] + 0.02, span['end'] - 0.02):
            shot = next((x for x in panel_shots(c['scene'], t) if x['id'] == p['layer']), None)
            if not shot or (shot['panel']['w'] >= COMP['w'] and shot['panel']['h'] >= COMP['h']):
                continue
            share = share_inside(shot['window'], a['content'])
            if not worst or share < worst['share']:
                worst = {'share': share, 'window': shot['window'], 'at': t}
        if worst and worst['share'] < LIMITS['inside']:
            w = worst['window']
            b = a['content']
            out.append({
                'level': 'error',
                'code': 'panel_outside_content',
                'layer': p['layer'],
                'message': (
                    f"{p['name']}: at {s1(worst['at'])} s the panel shows {number(math_round(w['x']))},{number(math_round(w['y']))} "
                    f"{number(math_round(w['w']))}x{number(math_round(w['h']))}, only {number(math_round(worst['share'] * 100))}% of it on the content box "
                    f"{number(b['x'])},{number(b['y'])} {number(b['w'])}x{number(b['h'])}"
                ),
                'fix': p['fix'],
            })

    # A step too short after its result settles to lean in on it.
    for step in c['steps']:
        if not step.get('pushSkipped'):
            continue
        at = step['pushSkipped']['at']
        room = step['pushSkipped']['room']
        out.append({
            'level': 'warning',
            'code': 'push_skipped',
            'layer': f"{step['id']}_panel",
            'message': f"{step['field']} ({step['id']}): the push onto its result was due at {s1(at)} s with {s1(room)} s of the step left, under the {number(DEFAULT_ZOOM['minRamp'])} s the shortest push takes, so the step never leans in",
            'fix': _or(step.get('pushFix'), f"set {step['field']}.from/to so its result settles earlier in the step"),
        })

    # A `to` before the result has settled and held: the push lands on it still arriving.
    for step in c['steps']:
        if not step.get('settleCut'):
            continue
        to = step['settleCut']['to']
        settles = step['settleCut']['settles']
        out.append({
            'level': 'warning',
            'code': 'to_before_settle',
            'layer': f"{step['id']}_panel",
            'message': f"{step['field']} ({step['id']}): its to at {s1(to)} s stops before its result settles ({s1(settles)} s) and holds, so the push lands at source {s1(_or(step.get('settle'), to))} s, before the result has finished appearing",
            'fix': _or(step.get('settleFix'), f"set {step['field']}.to later"),
        })

    # A hold with little source left after the result plays so slowly it reads as a freeze. A step
    # whose `to` cut its settle is reported once, above: that fix gives the hold its source too.
    for step in c['steps']:
        hold = next((p for p in reversed(step['edit']['pieces']) if p['role'] == 'hold'), None)
        if not hold or hold['speed'] >= LIMITS['holdSpeed'] or step.get('settleCut'):
            continue
        bounds = step['edit'].get('bounds')
        end = bounds.get('holdEnd') if bounds else None
        source = hold['srcOut'] - hold['srcIn']
        stops = f": {HOLD_ENDS[end]} at {s1(hold['srcOut'])} s" if end else ''
        out.append({
            'level': 'warning',
            'code': 'hold_slow',
            'layer': f"{step['id']}_panel",
            'message': f"{step['field']} ({step['id']}): its hold plays {to_fixed(source, 2) if source < 0.1 else s1(source)} s of source over {s1(hold['outOut'] - hold['outIn'])} s, at {number(round(hold['speed'], 2))}×, so it reads as a freeze{stops}",
            'fix': _or(step.get('holdFix'), f"set {step['field']}.from/to so more of the recording follows its result"),
        })

    # UI text at rest. One diagnostic: every step of a layout rests at the same scale.
    small = [s for s in c['steps'] if s.get('textPx') is not None and s['textPx'] < LIMITS['textPx']]
    if small:
        px = js_min(s['textPx'] for s in small)
        unlabelled = [f"{s['field']}.label" for s in small if not s['words']]
        also = f", or set {', '.join(unlabelled)} to a line that says what the screen shows" if unlabelled else ''
        out.append({
            'level': 'warning',
            'code': 'ui_text_small',
            'layer': f"{small[0]['id']}_panel",
            'message': f"UI text at rest is ≈ {number(px)} px in {', '.join(s['field'] for s in small)}, under {number(LIMITS['textPx'])} px: the screen's own words will not read on a phone",
            'fix': f'set uri and video to a sharper copy of the recording{also}',
        })

    # Nothing to read for too long.
    for step in c['steps']:
        covered = [{'at': 0, 'until': step['edit']['duration']}] if step['words'] else _or(step.get('labels'), [])
        gap = longest_gap(step['edit']['duration'], covered)
        if gap['to'] - gap['from'] <= LIMITS['silent']:
            continue
        out.append({
            'level': 'warning',
            'code': 'nothing_to_read',
            'layer': f"{step['id']}_panel",
            'message': f"{step['field']} ({step['id']}): {s1(gap['to'] - gap['from'])} s with no prompt or label, from {s1(gap['from'])} s into the step",
            'fix': step['wordsFix'](gap['from']),
        })

    # Length.
    target = c.get('target')
    duration = c['duration']
    if target and abs(duration - target) > LIMITS['target'] * target:
        length_fix: Optional[Callable[[float, float], str]] = c.get('lengthFix')
        fix = length_fix(duration, target) if length_fix else None
        out.append({
            'level': 'warning',
            'code': 'length_off_target',
            'message': f"the promo runs {s1(duration)} s against a target of {number(target)} s, {number(math_round((abs(duration - target) / target) * 100))}% {'over' if duration > target else 'under'}",
            'fix': _or(fix, f'set target to {number(round(duration, 0))}'),
        })

    # Sound.
    if c.get('sourceAudio') == 'keep':
        if a.get('input') and not a['input'].get('hasAudio'):
            out.append({'level': 'warning', 'code': 'no_source_audio', 'message': 'sourceAudio is keep, but the recording has no audio track', 'fix': "set sourceAudio to 'mute'"})
        for step in c['steps']:
            pitched = [p for p in step['edit']['pieces'] if abs(p['speed'] - 1) > 1e-3]
            if not pitched:
                continue
            muted = 0
            for p in pitched:
                muted = muted + p['outOut'] - p['outIn']
            speeds = ', '.join(dict.fromkeys(f"{number(p['speed'])}×" for p in pitched))
            out.append({
                'level': 'warning',
                'code': 'audio_pitched',
                'layer': f"{step['id']}_panel",
                'message': f"{step['field']} ({step['id']}): {len(pitched)} of {len(step['edit']['pieces'])} clips play at {speeds}, so {s1(muted)} of its {s1(step['edit']['duration'])} s stay muted under sourceAudio keep",
                'fix': step['audioFix'],
            })

    # Glyphs.
    language = c.get('language')
    script = script_of(language, c['texts'])
    if script:
        named = f' (language {language})' if language else ''
        out.append({
            'level': 'warning',
            'code': 'font_coverage',
            'message': f"the text is in {script}{named}: check that the font {c['font']} has {script} glyphs (picsart_media_list_fonts)",
            'fix': f"set font to a face that covers {script}{'' if language else ', and set language'}",
        })
    out += word_checks(_or(c.get('words'), []), language)
    return out


# Words that claim a quality instead of showing it. A viewer has heard them on every ad.
HYPE = ['amazing', 'awesome', 'incredible', 'game-changing', 'game-changer', 'revolutionary', 'revolutionize',
        'seamless', 'seamlessly', 'effortless', 'effortlessly', 'powerful', 'cutting-edge', 'next-level',
        'unleash', 'supercharge', 'ultimate', 'stunning', 'mind-blowing', 'best-in-class']
GREETING = re.compile(r"^(?:(?:hi|hey|hello|welcome|today)\b|in this video|let me show)")
CLICKS = re.compile(r"^(?:click|tap|select|press|choose|navigate|go to|scroll)\b")
LONGEST = {'hook': 8, 'cta': 5}


def word_checks(items: List[Dict[str, Any]], language: Optional[str]) -> List[Diagnostic]:
    """Warnings on words that tell instead of show, in English lines only; never on a prompt."""
    if language is not None and language.lower().split('-')[0] != 'en':
        return []
    if language is None and script_of(None, [l for i in items for l in i['lines']]):
        return []
    out: List[Diagnostic] = []
    for item in items:
        if item['kind'] == 'prompt':
            continue
        field = item['field']
        text = ' '.join(item['lines'])
        lower = text.lower()
        words = re.findall(r"[a-z0-9][a-z0-9'’-]*", lower)
        found = list(dict.fromkeys(w for w in words if w in HYPE))
        if '!' in text:
            found.append('!')
        for h in found:
            out.append({'level': 'warning', 'code': 'words_hype', 'message': f'{field} says "{h}": a claim the viewer has heard on every ad, where the screen could show the result', 'fix': f'rewrite {field} without "{h}": say what the screen shows instead'})
        start = re.sub(r"^[^a-z0-9]+", '', lower)
        if item['kind'] == 'hook' and GREETING.match(start):
            out.append({'level': 'warning', 'code': 'words_greeting', 'message': f'{field} opens with a greeting or an announcement, and the first second is the one that keeps a viewer', 'fix': f'set {field} to a result or a contrast the stills show'})
        if item['kind'] == 'label' and CLICKS.match(start):
            out.append({'level': 'warning', 'code': 'label_clicks', 'message': f'{field} narrates the clicks the panel already shows', 'fix': f'set {field} to what the step gets done, not the clicks: "The PDF is ready", not "Click Export"'})
        if re.search(r"\band then\b", lower):
            out.append({'level': 'warning', 'code': 'words_and_then', 'message': f'{field} joins its steps with "and then", which lists them without a reason to keep watching', 'fix': f'rewrite {field} with "so" or "but" in place of "and then", or split it into two lines'})
        longest = LONGEST.get(item['kind'])
        if longest is not None and len(words) > longest:
            out.append({'level': 'warning', 'code': 'words_long', 'message': f'{field} has {len(words)} words, more than a viewer reads in the time it shows', 'fix': f'cut {field} to {longest} words or fewer: it has {len(words)}'})
    return out


def _or(value: Any, default: Any) -> Any:
    """`value ?? default`: only a missing value takes the default."""
    return default if value is None else value
