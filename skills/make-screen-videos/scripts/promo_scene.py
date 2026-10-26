#!/usr/bin/env python3
"""
Build a screen promo's scene from its spec and the recording's moments.

    python3 scripts/promo_scene.py input.json [--explain]
    python3 scripts/promo_scene.py < input.json

The input is one JSON object, `{kind, spec, moments}`: `kind` is `promo` or `timelapse`, `spec` the
promo's spec (references/spec.md), and `moments` the result of `picsart_media_screen_moments`, whole. It
prints one JSON line, `{scene, duration, timeline, diagnostics}`, and exits 0, also when a
diagnostic is an error: the diagnostics say what to change in the spec, and the spec is built again.
With `--explain` the line also carries `explain`, what the build chose: the steps' edits and zoom
tracks, and the numbers the screen-promo lab prints.

Input it cannot build from exits 1, with one line on stderr that says what is wrong.

Python 3.9 or later, the standard library only, offline. It reads no media: whatever needs the
recording's pixels, the moments already carry.
"""
from __future__ import annotations

import sys
from typing import Any, Dict, List

from _build import build_promo, build_timelapse
from _input import InputError, parse
from _js import dumps

USAGE = 'usage: promo_scene.py [input.json] [--explain]; with no file, the input is read from stdin'


def build(data: Dict[str, Any], explain: bool = False) -> Dict[str, Any]:
    """The build of a checked input: `{scene, duration, timeline, diagnostics}`, and `explain` when asked."""
    built = build_promo(data['spec'], data['moments']) if data['kind'] == 'promo' else build_timelapse(data['spec'], data['moments'])
    if not explain:
        del built['explain']
    return built


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
        # A step the moments cannot give: a proposed step, an event or a window that is not there.
        return fail(str(err))
    except (KeyError, IndexError, TypeError, ZeroDivisionError, OverflowError) as err:
        return fail(f'cannot build from this input: {type(err).__name__} {err}')
    sys.stdout.buffer.write((dumps(out) + '\n').encode('utf-8'))
    return 0


def fail(reason: str, code: int = 1) -> int:
    sys.stderr.write('promo_scene.py: ' + ' '.join(reason.split()) + '\n')
    return code


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
