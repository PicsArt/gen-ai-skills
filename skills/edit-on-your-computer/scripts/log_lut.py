"""A .cube LUT that turns S-Log3 footage into Rec.709, with an optional gentle look baked in.

Usage:
  log_lut.py <out.cube> [--gamut s-gamut3.cine|s-gamut3] [--exposure 0.85] [--warmth 0.0]
             [--saturation 1.0] [--size 33]

Apply it to the picture decoded WITHOUT range expansion, so the LUT sees the camera's own code
values (S-Log3 is defined on them, 18% grey at 420 of 1023, whatever the file's range flag says):

  scale=in_color_matrix=bt709:in_range=pc:out_range=pc,format=rgb48le,lut3d=<out.cube>:interp=tetrahedral

`--exposure` scales scene light before the tone curve (0.85 puts 18% grey near 44% on screen);
raise it for one shot that is under, rather than lifting the whole edit. `--warmth` moves red up and
blue down by that fraction in linear light; `--saturation` scales colour around luma on screen.
"""
from __future__ import annotations

import argparse
import sys

PRIMARIES = {
    's-gamut3.cine': [(0.766, 0.275), (0.225, 0.800), (0.089, -0.087)],
    's-gamut3': [(0.730, 0.280), (0.140, 0.855), (0.100, -0.050)],
}
REC709 = [(0.64, 0.33), (0.30, 0.60), (0.15, 0.06)]
D65 = (0.3127, 0.3290)


def slog3(x: float) -> float:
    """Code value 0..1 to scene-linear reflectance (Sony's published S-Log3 curve)."""
    cv = x * 1023
    if cv >= 171.2102946929:
        return (10 ** ((cv - 420) / 261.5)) * 0.19 - 0.01
    return (cv - 95) * 0.01125 / (171.2102946929 - 95)


def inv(m: list[list[float]]) -> list[list[float]]:
    a, b, c = m[0]
    d, e, f = m[1]
    g, h, i = m[2]
    det = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
    return [[(e * i - f * h) / det, (c * h - b * i) / det, (b * f - c * e) / det],
            [(f * g - d * i) / det, (a * i - c * g) / det, (c * d - a * f) / det],
            [(d * h - e * g) / det, (b * g - a * h) / det, (a * e - b * d) / det]]


def mul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def to_xyz(prim: list[tuple]) -> list[list[float]]:
    cols = [[x / y, 1.0, (1 - x - y) / y] for x, y in prim]
    m = [[cols[j][i] for j in range(3)] for i in range(3)]
    w = [D65[0] / D65[1], 1.0, (1 - D65[0] - D65[1]) / D65[1]]
    mi = inv(m)
    s = [sum(mi[r][k] * w[k] for k in range(3)) for r in range(3)]
    return [[m[i][j] * s[j] for j in range(3)] for i in range(3)]


def gamut_matrix(gamut: str) -> list[list[float]]:
    return mul(inv(to_xyz(REC709)), to_xyz(PRIMARIES[gamut]))


def tone(x: float) -> float:
    """Scene to display light: a filmic curve with a soft shoulder (Narkowicz's ACES fit)."""
    x = max(x, 0.0)
    return min(max((x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14), 0.0), 1.0)


def oetf(v: float) -> float:
    return 4.5 * v if v < 0.018 else 1.099 * v ** 0.45 - 0.099


def convert(rgb: tuple, m: list[list[float]], exposure: float, warmth: float, saturation: float) -> list[float]:
    lin = [slog3(c) for c in rgb]
    lin = [sum(m[i][k] * lin[k] for k in range(3)) for i in range(3)]
    lin[0] *= 1 + warmth
    lin[2] *= 1 - warmth
    d = [oetf(tone(c * exposure)) for c in lin]
    y = 0.2126 * d[0] + 0.7152 * d[1] + 0.0722 * d[2]
    return [min(max(y + (c - y) * saturation, 0.0), 1.0) for c in d]


def build(gamut: str, exposure: float, warmth: float, saturation: float, size: int) -> str:
    m = gamut_matrix(gamut)
    lines = [f'TITLE "S-Log3 {gamut} to Rec.709 e{exposure} w{warmth} s{saturation}"', f'LUT_3D_SIZE {size}']
    n = size - 1
    for b in range(size):  # .cube order: red changes fastest
        for g in range(size):
            for r in range(size):
                lines.append('%.6f %.6f %.6f' % tuple(convert((r / n, g / n, b / n), m, exposure, warmth, saturation)))
    return '\n'.join(lines) + '\n'


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser()
    p.add_argument('out')
    p.add_argument('--gamut', default='s-gamut3.cine', choices=sorted(PRIMARIES))
    p.add_argument('--exposure', type=float, default=0.85)
    p.add_argument('--warmth', type=float, default=0.0)
    p.add_argument('--saturation', type=float, default=1.0)
    p.add_argument('--size', type=int, default=33)
    a = p.parse_args(argv)
    with open(a.out, 'w') as f:
        f.write(build(a.gamut, a.exposure, a.warmth, a.saturation, a.size))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
