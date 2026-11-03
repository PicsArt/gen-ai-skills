"""
Write the picsart_scene_apply_template arguments that bootstrap a montage: clips played one
after another, from what picsart_media_probe returned for each.

Input: a JSON file (or `-` for stdin) holding a list of clips. Each clip has `uri`, `width`,
`height` and `duration` (seconds), and optionally `in` and `out` (the trim, seconds), `fit`
(cover, contain or fill) and `align` (one of the nine alignments). Output: the arguments, as JSON.

    python3 scripts/montage_params.py clips.json
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List, Optional

FITS = ('cover', 'contain', 'fill')
ALIGNS = ('top left', 'top', 'top right', 'left', 'center', 'right', 'bottom left', 'bottom', 'bottom right')


class InputError(ValueError):
    """A clip or an option the montage cannot take."""


def _number(clip: Dict[str, Any], key: str, index: int) -> float:
    value = clip.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise InputError(f'clip {index}: `{key}` must be a number')
    return float(value)


def _clip(clip: Any, index: int, fit: str, align: str) -> Dict[str, Any]:
    if not isinstance(clip, dict):
        raise InputError(f'clip {index}: must be an object')
    uri = clip.get('uri')
    if not isinstance(uri, str) or not uri.startswith(('https://', 'http://')):
        raise InputError(f'clip {index}: `uri` must be an http(s) URL; upload a local file first')
    width = _number(clip, 'width', index)
    height = _number(clip, 'height', index)
    duration = _number(clip, 'duration', index)
    if width <= 0 or height <= 0:
        raise InputError(f'clip {index}: `width` and `height` must be above 0')
    if duration <= 0:
        raise InputError(f'clip {index}: `duration` must be above 0; an unknown duration is not 0')
    start = float(clip['in']) if 'in' in clip else 0.0
    end = float(clip['out']) if 'out' in clip else duration
    if not 0 <= start < end <= duration:
        raise InputError(f'clip {index}: the trim must satisfy 0 <= in < out <= duration ({duration})')
    clip_fit = clip.get('fit', fit)
    clip_align = clip.get('align', align)
    if clip_fit not in FITS:
        raise InputError(f'clip {index}: `fit` must be one of {", ".join(FITS)}')
    if clip_align not in ALIGNS:
        raise InputError(f'clip {index}: `align` must be one of {", ".join(ALIGNS)}')
    return {
        'duration': round(end - start, 6),
        'content': {
            'kind': 'media',
            'asset': {'type': 'video', 'uri': uri, 'width': width, 'height': height, 'duration': duration},
            'trim': {'in': start, 'out': end},
            'fit': clip_fit,
            'align': clip_align,
        },
    }


def montage_arguments(clips: List[Any], width: Optional[int] = None, height: Optional[int] = None, transition: str = '',
                      transition_duration: float = 0.0, fit: str = 'cover', align: str = 'center') -> Dict[str, Any]:
    """The apply_scene_template arguments for `clips`, in order."""
    if not isinstance(clips, list) or not clips:
        raise InputError('give at least one clip')
    if (width is None) != (height is None):
        raise InputError('give both `width` and `height`, or neither')
    if width is not None and (width <= 0 or height <= 0):
        raise InputError('`width` and `height` must be above 0')
    if transition_duration < 0:
        raise InputError('`transition-duration` must not be negative')
    if transition == '' and transition_duration:
        raise InputError('a hard cut takes no transition duration')
    return {
        'uri': 'scene://montage',
        'mode': 'bootstrap',
        'parameters': {
            **({'width': width, 'height': height} if width is not None else {}),
            'transition': transition,
            'transitionDuration': transition_duration,
            'clips': [_clip(clip, i, fit, align) for i, clip in enumerate(clips)],
        },
    }


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument('clips', help='a JSON file holding the list of clips, or - for stdin')
    parser.add_argument('--width', type=int)
    parser.add_argument('--height', type=int)
    parser.add_argument('--transition', default='', help='crossfade, slide, or "" for a hard cut')
    parser.add_argument('--transition-duration', type=float, default=0.0)
    parser.add_argument('--fit', default='cover', choices=FITS)
    parser.add_argument('--align', default='center', choices=ALIGNS)
    args = parser.parse_args(argv)
    try:
        if args.clips == '-':
            clips = json.load(sys.stdin)
        else:
            with open(args.clips, encoding='utf-8') as f:
                clips = json.load(f)
        out = montage_arguments(clips, args.width, args.height, args.transition, args.transition_duration,
                                args.fit, args.align)
    except (InputError, ValueError, OSError) as e:
        print(f'montage_params: {e}', file=sys.stderr)
        return 2
    print(json.dumps(out, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
