"""
Boxes are top-left rectangles, `{x, y, w, h}`, in whatever pixel space the caller names; a size is
`{w, h}` and a point `[x, y]`. The screen tools' `geometry.ts`, the part the builder uses.
"""
from __future__ import annotations

from typing import Dict, List

from _js import math_round

Box = Dict[str, float]
Size = Dict[str, float]
Vec2 = List[float]


def area(b: Box) -> float:
    return b['w'] * b['h']


def center(b: Box) -> Vec2:
    return [b['x'] + b['w'] / 2, b['y'] + b['h'] / 2]


def pad(b: Box, pad_fraction: float, bounds: Size) -> Box:
    """Grow a box by `pad_fraction` of its own size on every side, then clip it to `bounds`."""
    dx = b['w'] * pad_fraction
    dy = b['h'] * pad_fraction
    x = max(0, b['x'] - dx)
    y = max(0, b['y'] - dy)
    return {'x': x, 'y': y, 'w': min(bounds['w'], b['x'] + b['w'] + dx) - x, 'h': min(bounds['h'], b['y'] + b['h'] + dy) - y}


def round(v: float, places: int = 2) -> float:  # noqa: A001 - every round here is this one
    """`Math.round(v * 10 ** places) / 10 ** places`: a half rounds up, never to even."""
    return math_round(v * 10 ** places) / 10 ** places
