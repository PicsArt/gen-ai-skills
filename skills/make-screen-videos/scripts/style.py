#!/usr/bin/env python3
"""
A video's style as tokens: the colours by role and the text entrance per role, for a builder to
take instead of a palette of its own.

    python3 scripts/style.py                       every style, one JSON line each: {id, feel, tokens}
    python3 scripts/style.py <id> [brand.json]     one style, resolved, as one JSON line

A brand file is `{"accent": "#rrggbb", "canvas"?: ..., "surface"?: ..., "ink"?: ...}`: the colours
read in the recording or given by the user. Each goes onto its role, and a role that would lose
its contrast is refused with one line naming it. The style keeps its bones (the entrances);
the brand gives its colours.

Roles:
- `canvas`: the frame behind everything;
- `surface`: cards, bubbles and panel rims, one step off the canvas;
- `ink`: every word, on the canvas and on a surface alike, so it must read on both;
- `accent`: the one colour that marks the payoff and the call to action;
- `entrance`: the renderer's text entrance preset for `title` (the hook, chapter and intro
  titles), `line` (feature lines, step lines, chapter words) and `cta`.

Python 3.9 or later, the standard library only, offline.
"""
from __future__ import annotations

import json
import re
import sys
from typing import Any, Dict, List, Optional

# The renderer's entrance presets (picsart_scene_capabilities, `textAnimations`, 2026-10-13).
ENTRANCES = ('slide_up_lines', 'fade_in_chars', 'flicker_chars', 'typewriter')

STYLES: Dict[str, Dict[str, Any]] = {
    'studio-dark': {
        'feel': 'premium and cinematic: a deep plum stage, warm off-white words, a coral payoff',
        'canvas': '#17111f', 'surface': '#2b2238', 'ink': '#f6f0e8', 'accent': '#ff7a59',
        'entrance': {'title': 'fade_in_chars', 'line': 'slide_up_lines', 'cta': 'slide_up_lines'},
    },
    'paper-ink': {
        'feel': 'calm and editorial: warm paper, near-black ink, a red pencil mark for the payoff',
        'canvas': '#f3ede2', 'surface': '#fffdf8', 'ink': '#1d1b18', 'accent': '#c8402a',
        'entrance': {'title': 'slide_up_lines', 'line': 'fade_in_chars', 'cta': 'slide_up_lines'},
    },
    'pop-block': {
        'feel': 'loud and social: a flat sunflower block, black words, a hot pink payoff',
        'canvas': '#ffd23f', 'surface': '#fff6d1', 'ink': '#141414', 'accent': '#d6246e',
        'entrance': {'title': 'slide_up_lines', 'line': 'fade_in_chars', 'cta': 'flicker_chars'},
    },
    'keynote': {
        'feel': 'clean product launch: a light grey stage, the result big, one electric blue',
        'canvas': '#e8eaee', 'surface': '#fbfbfd', 'ink': '#101318', 'accent': '#2456e8',
        'entrance': {'title': 'fade_in_chars', 'line': 'slide_up_lines', 'cta': 'fade_in_chars'},
    },
    'sticky-note': {
        'feel': 'a friendly how-to: notepad yellow, soft charcoal, an orange marker',
        'canvas': '#fff1a8', 'surface': '#fffbe6', 'ink': '#2a2723', 'accent': '#c2410c',
        'entrance': {'title': 'typewriter', 'line': 'slide_up_lines', 'cta': 'slide_up_lines'},
    },
    'terminal': {
        'feel': 'technical: near-black green-tinted, mint text, a signal green payoff',
        'canvas': '#0b100d', 'surface': '#18201b', 'ink': '#e3f3e8', 'accent': '#3ddc84',
        'entrance': {'title': 'typewriter', 'line': 'fade_in_chars', 'cta': 'flicker_chars'},
    },
    'bloom': {
        'feel': 'warm and creative: a berry stage, blush words, a peach payoff',
        'canvas': '#3a1030', 'surface': '#56203f', 'ink': '#fdeef4', 'accent': '#ffb38a',
        'entrance': {'title': 'fade_in_chars', 'line': 'slide_up_lines', 'cta': 'fade_in_chars'},
    },
    'native': {
        'feel': 'made by a creator, not an ad: the recording near full frame, minimal chrome',
        'canvas': '#121212', 'surface': '#242424', 'ink': '#f7f7f5', 'accent': '#ff3b5c',
        'entrance': {'title': 'fade_in_chars', 'line': 'slide_up_lines', 'cta': 'slide_up_lines'},
    },
}

ROLES = ('canvas', 'surface', 'ink', 'accent')
HEX = re.compile(r'^#[0-9a-fA-F]{6}$')
# Words must read on the canvas and on a surface: WCAG AA for text.
MIN_CONTRAST = 4.5
# The accent marks the payoff on the canvas: large text.
MIN_ACCENT_CONTRAST = 3.0


class StyleError(ValueError):
    """A style or a brand that cannot be used; the message is the one line to print."""


def luminance(color: str) -> float:
    """WCAG relative luminance of `#rrggbb`."""
    def channel(c: int) -> float:
        v = c / 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (int(color[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast(a: str, b: str) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def problems(tokens: Dict[str, Any]) -> List[str]:
    """What keeps these tokens from being used: each a line naming the role."""
    out = []
    for role in ROLES:
        if not isinstance(tokens.get(role), str) or not HEX.match(tokens[role]):
            out.append(f'{role}: must be a #rrggbb colour, not {tokens.get(role)!r}')
    if out:
        return out
    for role in ('canvas', 'surface'):
        c = contrast(tokens['ink'], tokens[role])
        if c < MIN_CONTRAST:
            out.append(f'ink on {role}: contrast {c:.2f}, below {MIN_CONTRAST}; choose a darker or lighter ink')
    c = contrast(tokens['accent'], tokens['canvas'])
    if c < MIN_ACCENT_CONTRAST:
        out.append(f'accent on canvas: contrast {c:.2f}, below {MIN_ACCENT_CONTRAST}; choose a stronger accent')
    for role, preset in (tokens.get('entrance') or {}).items():
        if preset not in ENTRANCES:
            out.append(f'entrance.{role}: {preset!r} is not one of {", ".join(ENTRANCES)}')
    return out


def resolve(style: Any, brand: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    The tokens of `style`, a style id or tokens already resolved, with `brand`'s colours on their
    roles. Raises StyleError naming what cannot be used.
    """
    if isinstance(style, str):
        if style not in STYLES:
            raise StyleError(f'style: {style!r} is not a style; one of {", ".join(STYLES)}')
        base = {'id': style, **{k: v for k, v in STYLES[style].items() if k != 'feel'}}
    elif isinstance(style, dict):
        base = dict(style)
    else:
        raise StyleError(f'style: must be a style id or its tokens, not {style!r}')
    base['entrance'] = {'title': 'slide_up_lines', 'line': 'slide_up_lines', 'cta': 'slide_up_lines', **(base.get('entrance') or {})}
    tokens = {**base, **{k: v for k, v in (brand or {}).items() if k in ROLES}}
    found = problems(tokens)
    if found:
        raise StyleError('; '.join(found))
    return tokens


def colors(tokens: Dict[str, Any]) -> List[str]:
    """Every colour the style allows in a scene, lower-cased."""
    return sorted({tokens[r].lower() for r in ROLES})


def main(argv: List[str]) -> int:
    try:
        if not argv:
            for sid, s in STYLES.items():
                print(json.dumps({'id': sid, 'feel': s['feel'], 'tokens': resolve(sid)}))
            return 0
        brand = None
        if len(argv) > 1:
            with open(argv[1], encoding='utf-8-sig') as f:
                brand = json.load(f)
        print(json.dumps(resolve(argv[0], brand)))
        return 0
    except (OSError, ValueError) as err:
        sys.stderr.write('style.py: ' + ' '.join(str(err).split()) + '\n')
        return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
