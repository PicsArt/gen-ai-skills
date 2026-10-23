"""
Numbers and JSON as JavaScript has them. The builder was first written in TypeScript, and its
golden outputs in `__tests__/fixtures/` came from that builder, so this script rounds, prints and
adds the way it did, to the last digit:

- `Math.round` rounds a half up (`-2.5` gives `-2`); Python's `round` rounds a half to even.
- `toFixed` rounds the exact binary value, a half up, so `(0.25).toFixed(1)` is `0.3`; Python's
  `format(0.25, '.1f')` is `0.2`.
- A number prints as JavaScript prints it: `1`, not `1.0`, and `1e-7`, not `1e-07`.
- `Math.min()` and `Math.max()` of nothing are `Infinity` and `-Infinity`; Python's raise.
- A sum adds left to right. Python 3.12's `sum` compensates, and lands on other last digits.
"""
from __future__ import annotations

import math
from decimal import ROUND_HALF_UP, Decimal
from typing import Any, Iterable, List

INF = math.inf


def math_round(x: float) -> float:
    """`Math.round`: the nearest integer, a half rounded up."""
    if not math.isfinite(x):
        return x
    f = math.floor(x)
    return f + 1 if x - f >= 0.5 else f


def to_fixed(x: float, digits: int) -> str:
    """`Number.prototype.toFixed`."""
    if not math.isfinite(x) or abs(x) >= 1e21:
        return number(x)
    if x == 0:
        x = 0.0  # -0 prints as 0
    return format(Decimal(x).quantize(Decimal(1).scaleb(-digits), rounding=ROUND_HALF_UP), 'f')


def number(x: float) -> str:
    """A number as `String(x)` writes it, in a template string or in JSON."""
    x = float(x)
    if math.isnan(x):
        return 'NaN'
    if math.isinf(x):
        return 'Infinity' if x > 0 else '-Infinity'
    if x == 0:
        return '0'
    # repr gives the shortest digits that read back as x, as JavaScript does; only the layout differs.
    mantissa, _, exponent = repr(abs(x)).partition('e')
    whole, _, fraction = mantissa.partition('.')
    digits = whole + fraction
    n = len(whole) + (int(exponent) if exponent else 0)
    s = digits.lstrip('0')
    n -= len(digits) - len(s)
    s = s.rstrip('0')
    k = len(s)
    if k <= n <= 21:
        out = s + '0' * (n - k)
    elif 0 < n <= 21:
        out = s[:n] + '.' + s[n:]
    elif -6 < n <= 0:
        out = '0.' + '0' * -n + s
    else:
        e = n - 1
        out = (s if k == 1 else s[0] + '.' + s[1:]) + 'e' + ('+' if e >= 0 else '-') + str(abs(e))
    return ('-' if x < 0 else '') + out


def js_min(xs: Iterable[float]) -> float:
    """`Math.min(...xs)`."""
    m = INF
    for x in xs:
        if x != x:
            return math.nan
        if x < m:
            m = x
    return m


def js_max(xs: Iterable[float]) -> float:
    """`Math.max(...xs)`."""
    m = -INF
    for x in xs:
        if x != x:
            return math.nan
        if x > m:
            m = x
    return m


def total(xs: Iterable[float]) -> float:
    """`xs.reduce((sum, x) => sum + x, 0)`: left to right, uncompensated."""
    s = 0
    for x in xs:
        s = s + x
    return s


_ESCAPES = {'"': '\\"', '\\': '\\\\', '\b': '\\b', '\f': '\\f', '\n': '\\n', '\r': '\\r', '\t': '\\t'}


def _string(s: str) -> str:
    out = ['"']
    for ch in s:
        c = ord(ch)
        if ch in _ESCAPES:
            out.append(_ESCAPES[ch])
        elif c < 0x20 or 0xD800 <= c <= 0xDFFF:
            out.append('\\u%04x' % c)
        else:
            out.append(ch)
    out.append('"')
    return ''.join(out)


def dumps(value: Any, indent: int = 0) -> str:
    """`JSON.stringify(value)`, or with `indent`, `JSON.stringify(value, null, indent)`."""
    return _encode(value, indent, 0)


def _encode(v: Any, indent: int, depth: int) -> str:
    if v is None:
        return 'null'
    if v is True:
        return 'true'
    if v is False:
        return 'false'
    if isinstance(v, (int, float)):
        return number(v) if math.isfinite(v) else 'null'
    if isinstance(v, str):
        return _string(v)
    if isinstance(v, dict):
        items: List[str] = [_string(str(k)) + (': ' if indent else ':') + _encode(x, indent, depth + 1) for k, x in v.items()]
        return _join(items, '{', '}', indent, depth)
    if isinstance(v, (list, tuple)):
        return _join([_encode(x, indent, depth + 1) for x in v], '[', ']', indent, depth)
    raise TypeError(f'cannot write {type(v).__name__} as JSON')


def _join(items: List[str], open_: str, close: str, indent: int, depth: int) -> str:
    if not items:
        return open_ + close
    if not indent:
        return open_ + ','.join(items) + close
    inner = '\n' + ' ' * (indent * (depth + 1))
    return open_ + ','.join(inner + i for i in items) + '\n' + ' ' * (indent * depth) + close
