"""
The loudest stretches of a gameplay stream: where a play happened and the player reacted.

picsart_media_analyze_audio returns its energy curves as URLs, each a per-frame JSON array, with
`frameRateHz`. Save the `rms` curve as a file and run:

    python3 scripts/stream_peaks.py rms.json --rate 10 --count 6 --length 30

It prints JSON: `{"moments": [{"peak", "in", "out", "score"}, ...]}`, loudest first. Each window
puts the peak about two thirds of the way in, so the play leads up to it and the reaction lands
after it. Windows never overlap, and none starts before 0 or ends after the stream. `score` is
the window's mean loudness over the stream's median: above 1 is louder than usual.

The windows are candidates, not cuts: the transcript snaps each edge to a whole word, and a still
at each peak confirms the play (a menu, a loading screen or an ad read can be loud too).
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import List


def smooth(values: List[float], width: int) -> List[float]:
    """A centred moving average over `width` frames, so one spike does not outrank a loud stretch."""
    if width <= 1:
        return list(values)
    half = width // 2
    sums = [0.0]
    for v in values:
        sums.append(sums[-1] + v)
    out = []
    for i in range(len(values)):
        a, b = max(0, i - half), min(len(values), i + half + 1)
        out.append((sums[b] - sums[a]) / (b - a))
    return out


def moments(curve: list, rate: float, count: int, length: float) -> List[dict]:
    if rate <= 0 or length <= 0 or count <= 0:
        raise ValueError('rate, length and count must be positive')
    if not isinstance(curve, list) or not all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in curve):
        raise ValueError('the curve must be a JSON array of numbers')
    values = [float(v) for v in curve]
    if not values:
        return []
    total = len(values) / rate
    if total <= length:
        return [{'peak': round(total / 2, 2), 'in': 0.0, 'out': round(total, 2), 'score': 1.0}]
    level = smooth(values, max(1, int(rate * 2)))
    median = sorted(values)[len(values) // 2] or 1e-9
    taken: List[tuple] = []
    found = []
    for i in sorted(range(len(level)), key=lambda k: -level[k]):
        if len(found) >= count:
            break
        peak = i / rate
        a = min(max(0.0, peak - length * 2 / 3), total - length)
        b = a + length
        if any(a < tb and ta < b for ta, tb in taken):
            continue
        window = values[int(a * rate):int(b * rate)] or [0.0]
        taken.append((a, b))
        found.append({'peak': round(peak, 2), 'in': round(a, 2), 'out': round(b, 2),
                      'score': round(sum(window) / len(window) / median, 2)})
    return found


def main(argv: List[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    p.add_argument('curve', help='the energy curve JSON file: a per-frame array')
    p.add_argument('--rate', type=float, required=True, help="the curve's frameRateHz")
    p.add_argument('--count', type=int, default=6)
    p.add_argument('--length', type=float, default=30.0, help='seconds per window')
    args = p.parse_args(argv)
    with open(args.curve, encoding='utf-8') as f:
        curve = json.load(f)
    try:
        print(json.dumps({'moments': moments(curve, args.rate, args.count, args.length)}))
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
