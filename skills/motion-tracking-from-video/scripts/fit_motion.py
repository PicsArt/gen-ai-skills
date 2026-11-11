#!/usr/bin/env python3
"""Each move's timing curve, from picsart_media_track_motion's dense samples.

    python3 scripts/fit_motion.py moves track.json [--target ID] [--channel position|scale|rotation]
                                   [--tolerance PX] [--into sheet.json] [--out moves.json]
    python3 scripts/fit_motion.py compare ref.json ours.json [--target ID] [--target-b ID]
                                   [--channel ...] [--offset S] [--scale-b K] [--out report.json]
    python3 scripts/fit_motion.py speed track.json [--target ID] [--channel ...] [--out speed.csv]
    python3 scripts/fit_motion.py diff ref.json ours.json [--target ID] [--target-b ID] [--channel ...]
                                   [--offset S] [--scale-b K] [--out report.json]
    every command takes --min-confidence C (default 0.5) before the command name

`track.json` is the report saved from the tool's `resultUrl` (its `targets[].samples`, each
{t, x, y, rotation, scale, confidence, visible}), a list of such samples, or the output of
`moves` itself (for `compare`).

`moves` finds every move of each tracked target on each channel - a stretch where the channel
changes by more than its tolerance a frame - and reports, per move: the target, the channel,
from and to, its start (`delay` from the window's start, and `at` in source seconds), its
duration up to the frame it settles, the curve's shape (`linear`, `ease_in`, `ease_out`,
`ease_in_out`, or `spring` when it overshoots), a fitted `cubic_bezier` (the scene's own easing;
a y outside 0-1 is an overshoot), the overshoot as a share of the travel, how many times it swings
past its rest before it settles, a spring (stiffness and damping at mass 1) when it overshoots,
the hold after it, its speed profile (peak speed, when the peak comes) and `keyframes` the scene
can take as they are. `--into` adds the moves to a JSON object's `moves` list (the structure sheet),
replacing earlier ones for the same target and channel.

`compare` matches the reference's moves to ours in order, per target and channel, and checks the
feel, not only the end points: the start, the duration, where the peak speed comes and how big it
is, the overshoot, the swings and the curve's shape. `--offset` is added to our times;
`--scale-b` multiplies our positions (our render at another size).

`diff` is the deviation check, per channel, sample by sample over the time both cover: the starting
offset (where ours sits at the first shared sample, against the reference: the placement, which the
box you drew also shifts), `maxDev` raw, and `moveDev`, the deviation once that starting offset is
removed - the move itself. The move passes when `moveDev` is within the limit (24 px, 0.03 of scale,
3 degrees); the placement is reported beside it. Track ours with the same box as the reference: the
same part of the object, the same size against it.

`--min-confidence` keeps samples at or above it (default 0.5). A fast move smears, and its smeared
frames fall below 0.5: track it with `"estimator": "segmentation"`, whose centre stays on the smear,
and read it at 0.2. Every move reports how many of its samples were under 0.5 (`blurred`).

`speed` writes each target's speed over time as CSV (t in source seconds, speed in the channel's
unit a second), for a chart of the reference against ours.

Rotation stays in the tracker's convention (counter-clockwise positive); flip its sign for a scene.
Exits 0, 1 when a compare fails, 2 on unreadable input. Standard library only.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from typing import Any, Dict, List, Optional, Sequence, Tuple

Json = Dict[str, Any]

CHANNELS = ("position", "scale", "rotation")
# A channel's change below this is noise, not motion: a compressed reference's 1.5 px, and for
# scale and rotation about what 1.5 px is on the edge of a card a few hundred pixels wide.
TOLERANCE = {"position": 1.5, "scale": 0.003, "rotation": 0.3}
# Pauses shorter than this inside a move (an overshoot turning back) do not end it.
JOIN_GAP = 0.2
# Slow moves are found over this many seconds, not frame to frame.
SPAN = 0.1
# An overshoot, swing or anticipation counts from this share of the travel (or twice the tolerance).
SWING = 0.01
# The presets the scene engine names, as CSS defines them.
PRESETS = {"linear": (0.0, 0.0, 1.0, 1.0), "ease_in": (0.42, 0.0, 1.0, 1.0),
           "ease_out": (0.0, 0.0, 0.58, 1.0), "ease_in_out": (0.42, 0.0, 0.58, 1.0)}
# What `compare` lets pass: start and duration within max(2 frames, the share), the peak speed's
# place within 0.15 of the move, its size within 20 %, the overshoot within 5 % of the travel.
PASS = {"start_s": 0.1, "duration_share": 0.15, "peak_at": 0.15, "peak_speed": 0.2, "overshoot": 0.05}
# What `diff` lets pass, once the starting offset is removed: the use case's limits.
LIMIT = {"position": 24.0, "scale": 0.03, "rotation": 3.0}
# Samples below this confidence are not measurements; --min-confidence lowers it for a smeared move.
MIN_CONFIDENCE = 0.5
SURE = 0.5


class InputError(Exception):
    pass


# --- Reading the samples -----------------------------------------------------------------------

def load(path: str) -> Any:
    try:
        with open(path, encoding="utf-8-sig") as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:
        raise InputError(f"{path} is not JSON: {exc}")


def targets_of(report: Any) -> List[Json]:
    """Every target with samples: a tool report, a bare target, or a list of samples."""
    if isinstance(report, list) and report and isinstance(report[0], dict) and "t" in report[0]:
        return [{"id": "target", "samples": report, "start": 0.0, "origin": 0.0}]
    if not isinstance(report, dict):
        raise InputError("expected a picsart_media_track_motion report, a target or a list of samples")
    window = report.get("window")
    # origin: where the window starts; start: what is added to a sample's t to give source seconds
    # (0 when the samples are already absolute).
    origin = float(window[0]) if isinstance(window, list) and window else 0.0
    start = 0.0 if report.get("normalizeTime") == "absolute" else origin
    found = report.get("targets") if isinstance(report.get("targets"), list) else [report]
    out = []
    for n, target in enumerate(found):
        if isinstance(target, dict) and isinstance(target.get("samples"), list):
            out.append({"id": str(target.get("id") or f"target{n}"), "samples": target["samples"], "start": start,
                        "origin": origin})
    if not out:
        raise InputError("no target has samples: save the report at the tool's resultUrl, not its reply")
    return out


def pick(targets: List[Json], wanted: Optional[str]) -> List[Json]:
    if wanted is None:
        return targets
    chosen = [t for t in targets if t["id"] == wanted]
    if not chosen:
        raise InputError(f"no target {wanted!r}; the report has {', '.join(t['id'] for t in targets)}")
    return chosen


def series(target: Json, channel: str) -> Tuple[List[float], List[Tuple[float, ...]], int]:
    """(times in source seconds, values, samples dropped) for one channel, visible samples only."""
    times, values, dropped = [], [], 0
    for s in target["samples"]:
        if not isinstance(s, dict) or s.get("visible") is False or (s.get("confidence") is not None and s["confidence"] < MIN_CONFIDENCE):
            dropped += 1
            continue
        try:
            if channel == "position":
                value: Tuple[float, ...] = (float(s["x"]), float(s["y"]))
            else:
                raw = s[channel]
                value = (float(raw[0] if isinstance(raw, list) else raw),)
            times.append(float(s["t"]) + target["start"])
        except (KeyError, TypeError, ValueError):
            dropped += 1
            continue
        if channel == "rotation" and values:
            # Degrees wrap: 179 then -179 is a 2-degree turn, not 358.
            turns = round((values[-1][0] - value[0]) / 360.0)
            value = (value[0] + 360.0 * turns,)
        values.append(value)
    return times, values, dropped


def dist(a: Sequence[float], b: Sequence[float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def speeds(times: List[float], values: List[Tuple[float, ...]]) -> List[float]:
    """Speed at each sample, by central differences (one-sided at the ends)."""
    n = len(times)
    out = []
    for i in range(n):
        a, b = max(0, i - 1), min(n - 1, i + 1)
        dt = times[b] - times[a]
        out.append(dist(values[b], values[a]) / dt if dt > 0 else 0.0)
    return out


# --- Curves ------------------------------------------------------------------------------------

def bezier_param(x: float, x1: float, x2: float) -> float:
    """The curve parameter where a cubic-bezier easing reaches x (x1, x2 in 0-1, so x is monotone)."""
    lo, hi = 0.0, 1.0
    for _ in range(30):
        mid = (lo + hi) / 2
        bx = 3 * (1 - mid) ** 2 * mid * x1 + 3 * (1 - mid) * mid ** 2 * x2 + mid ** 3
        if bx < x:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def bezier_y(x: float, c: Sequence[float]) -> float:
    s = bezier_param(min(1.0, max(0.0, x)), c[0], c[2])
    return 3 * (1 - s) ** 2 * s * c[1] + 3 * (1 - s) * s ** 2 * c[3] + s ** 3


def fit_bezier(us: List[float], ps: List[float], lo: float = 0.0, hi: float = 1.0) -> Tuple[Tuple[float, float, float, float], float]:
    """The cubic-bezier (x1, y1, x2, y2) closest to progress ps at times us, and its RMS error.

    For fixed x1 and x2 the curve is linear in y1 and y2, so they are solved exactly, within lo-hi
    (0-1 unless the move overshoots or pulls back first); x1 and x2 are searched on a grid, then on
    a finer one around the best."""
    def best_y(x1: float, x2: float) -> Tuple[float, float, float]:
        a11 = a12 = a22 = b1 = b2 = 0.0
        rows = []
        for u, p in zip(us, ps):
            s = bezier_param(u, x1, x2)
            f1, f2, f0 = 3 * (1 - s) ** 2 * s, 3 * (1 - s) * s ** 2, s ** 3
            rows.append((f1, f2, f0, p))
            a11 += f1 * f1
            a12 += f1 * f2
            a22 += f2 * f2
            b1 += f1 * (p - f0)
            b2 += f2 * (p - f0)
        det = a11 * a22 - a12 * a12
        if abs(det) < 1e-12:
            y1 = y2 = 0.0
        else:
            y1 = (b1 * a22 - b2 * a12) / det
            y2 = (a11 * b2 - a12 * b1) / det
        if not lo <= y1 <= hi or not lo <= y2 <= hi:
            # The best within the bounds lies on one: fix that y, solve the other, clamp it.
            y1 = max(lo, min(hi, y1))
            y2 = max(lo, min(hi, (b2 - a12 * y1) / a22)) if a22 > 1e-12 else y2
            y1 = max(lo, min(hi, (b1 - a12 * y2) / a11)) if a11 > 1e-12 else y1
            y2 = max(lo, min(hi, y2))
        err = sum((f1 * y1 + f2 * y2 + f0 - p) ** 2 for f1, f2, f0, p in rows)
        return y1, y2, err

    best = (1e18, 0.0, 0.0, 0.0, 0.0)
    grid = [i / 20 for i in range(21)]
    for x1 in grid:
        for x2 in grid:
            y1, y2, err = best_y(x1, x2)
            if err < best[0]:
                best = (err, x1, y1, x2, y2)
    step = 0.05
    for _ in range(3):
        step /= 4
        cx1, cx2 = best[1], best[3]
        for i in range(-4, 5):
            for j in range(-4, 5):
                x1 = min(1.0, max(0.0, cx1 + i * step))
                x2 = min(1.0, max(0.0, cx2 + j * step))
                y1, y2, err = best_y(x1, x2)
                if err < best[0]:
                    best = (err, x1, y1, x2, y2)
    control = tuple(round(v, 3) for v in best[1:])
    return control, math.sqrt(best[0] / max(1, len(us)))  # type: ignore[return-value]


def shape(peak_at: float, peak_over_mean: float) -> str:
    """The curve's name from its measured speed profile: where the peak speed comes, and how far
    above the mean it is (a linear move has none)."""
    if peak_over_mean < 1.25:
        return "linear"
    if peak_at < 0.3:
        return "ease_out"
    if peak_at > 0.7:
        return "ease_in"
    return "ease_in_out"


def spring_progress(tau: float, zeta: float, omega: float) -> float:
    """An underdamped spring released from rest at 0 toward 1."""
    if tau <= 0:
        return 0.0
    wd = omega * math.sqrt(1 - zeta * zeta)
    return 1 - math.exp(-zeta * omega * tau) * (math.cos(wd * tau) + zeta / math.sqrt(1 - zeta * zeta) * math.sin(wd * tau))


def fit_spring(taus: List[float], ps: List[float], duration: float) -> Json:
    best = (1e18, 0.5, 1.0)
    for i in range(1, 39):
        zeta = i * 0.025
        for j in range(1, 81):
            period = duration * j / 40  # the damped period, from a fortieth of the move to twice it
            omega = 2 * math.pi / period / math.sqrt(1 - zeta * zeta)
            err = sum((spring_progress(t, zeta, omega) - p) ** 2 for t, p in zip(taus, ps))
            if err < best[0]:
                best = (err, zeta, omega)
    # Then finer, around the best.
    for scale in (0.2, 0.04):
        _, z0, w0 = best
        for i in range(-10, 11):
            zeta = min(0.98, max(0.01, z0 + i * 0.025 * scale))
            for j in range(-10, 11):
                omega = w0 * (1 + j * 0.05 * scale)
                err = sum((spring_progress(t, zeta, omega) - p) ** 2 for t, p in zip(taus, ps))
                if err < best[0]:
                    best = (err, zeta, omega)
    err, zeta, omega = best
    return {"stiffness": round(omega * omega, 2), "damping": round(2 * zeta * omega, 3), "mass": 1,
            "dampingRatio": round(zeta, 3),
            "overshoot": round(math.exp(-math.pi * zeta / math.sqrt(1 - zeta * zeta)), 3),
            "rmsError": round(math.sqrt(err / max(1, len(taus))), 4)}


# --- Moves -------------------------------------------------------------------------------------

def runs(times: List[float], values: List[Tuple[float, ...]], tol: float) -> List[Tuple[int, int]]:
    """(first, last) sample index of each stretch that moves more than tol a frame."""
    # A slow move changes less than tol a frame, so each frame is compared with the one SPAN before.
    step = (times[-1] - times[0]) / max(1, len(times) - 1) or 1 / 30
    span = max(1, round(SPAN / step))
    moving = [False] * len(times)
    for i in range(1, len(times)):
        k = max(0, i - span)
        if dist(values[i], values[k]) > tol:
            for j in range(k + 1, i + 1):
                if dist(values[j], values[j - 1]) > tol / span / 2:
                    moving[j - 1] = moving[j] = True
    found: List[List[int]] = []
    for i, m in enumerate(moving):
        if not m:
            continue
        if found and (i == found[-1][1] + 1 or times[i] - times[found[-1][1]] <= JOIN_GAP):
            found[-1][1] = i
        else:
            found.append([i, i])
    return [(a, b) for a, b in found if dist(values[b], values[a]) > 3 * tol or b - a >= 2]


def rest_profile(values: List[Tuple[float, ...]], first: int, last: int, rest_end: int, tol: float):
    """Shared rest evidence and spring estimate for splitting and parameter measurement."""
    start = values[first]
    far = max(range(first, last + 1), key=lambda i: dist(values[i], start))
    reach = dist(values[far], start)
    if reach <= 3 * tol:
        return None
    axis = tuple((b - a) / reach for a, b in zip(start, values[far]))
    line = [sum((v[k] - start[k]) * axis[k] for k in range(len(axis))) for v in values[first:last + 1]]
    gap = 3 * tol
    turns: List[int] = []
    heading, best = 0, 0
    for i in range(1, len(line)):
        if heading == 0:
            if abs(line[i] - line[0]) > gap:
                heading, best = (1 if line[i] > line[0] else -1), i
        elif (line[i] - line[best]) * heading >= 0:
            best = i
        elif (line[best] - line[i]) * heading > gap:
            turns.append(best)
            heading, best = -heading, i
    rest, settled = values[last], False
    after = values[last + 1:rest_end + 1]
    ends_track = rest_end == len(values) - 1
    target = line[-1]
    if after:
        middle = tuple(sorted(v[k] for v in after)[len(after) // 2] for k in range(len(start)))
        # Still: two or more frames within tol of each other's middle, or one frame that moved
        # under tol from the stretch's last frame.
        still = (all(dist(v, middle) <= tol for v in after) if len(after) >= 2
                 else dist(after[0], values[last]) <= tol)
        if still or not ends_track:
            target = sum((r - a) * x for r, a, x in zip(middle, start, axis))
            ends_track = False
            rest, settled = middle, True
    # Whether the stretch starts at rest: after an earlier stretch, or with a first step under tol.
    # A window that opens mid-move has no release point to measure the overshoot from.
    at_rest = first > 0 or dist(values[first + 1], values[first]) <= tol
    if ends_track and len(turns) >= (2 if at_rest else 3):
        p0, p1, p2 = (line[0], line[turns[0]], line[turns[1]]) if at_rest else (line[k] for k in turns[:3])
        bottom = p0 + p2 - 2 * p1
        if abs(p2 - p1) < 0.97 * abs(p1 - p0) and abs(bottom) > 1e-9:
            target = (p0 * p2 - p1 * p1) / bottom
            rest = tuple(a + target * x for a, x in zip(start, axis))
    return rest, settled, line, turns, target, at_rest


def move_of(times: List[float], values: List[Tuple[float, ...]], first: int, last: int, rest_end: int,
            tol: float, channel: str) -> Optional[Json]:
    # The span test flags a few frames early: the move starts at the last frame still within tol of
    # that rest. Measured from the rest, not frame to frame, so a slow move is kept.
    profile = rest_profile(values, first, last, rest_end, tol)
    if profile is None:
        return None
    rest, settled = profile[:2]
    origin = values[first]
    while first + 1 < last and dist(values[first + 1], origin) <= tol:
        first += 1
    start_value = values[first]
    travel = tuple(b - a for a, b in zip(start_value, rest))
    length = math.sqrt(sum(d * d for d in travel))
    if length <= 3 * tol:
        return None
    end = rest_end
    progress = [sum((v[k] - start_value[k]) * travel[k] for k in range(len(travel))) / (length * length)
                for v in values[first:end + 1]]
    band = tol / length
    swing = max(2 * band, SWING)
    # Settled: the first frame from which progress stays within the band of 1.
    settle = end
    for i in range(len(progress) - 1, -1, -1) if settled else []:
        if abs(progress[i] - 1) > band:
            break
        settle = first + i
    if settle <= first:
        settle = min(end, first + 1)
    t_start, t_settle = times[first], times[settle]
    duration = t_settle - t_start
    used = progress[:settle - first + 1]
    us = [(times[first + i] - t_start) / duration for i in range(len(used))]
    peak = max(used)
    overshoot = max(0.0, peak - 1)
    # Swings: each turn past the rest by more than the band, after it first reaches it.
    swings, side = 0, 0
    reached = next((i for i, p in enumerate(progress) if p >= 1 - band), None)
    for p in progress[reached:] if reached is not None else []:
        now = 1 if p > 1 + swing else (-1 if p < 1 - swing else 0)
        if now and now != side:
            swings += 1
            side = now
    anticipation = max(0.0, -min(used))
    control, error = fit_bezier(us, used, -1.0 if anticipation > swing else 0.0, 2.5 if overshoot > swing else 1.0)
    # A preset that fits about as well is named instead: the scene takes it by name.
    preset = None
    for key, curve in PRESETS.items():
        rms = math.sqrt(sum((bezier_y(u, curve) - p) ** 2 for u, p in zip(us, used)) / max(1, len(us)))
        if rms <= error + 0.01 and (preset is None or rms < preset[1]):
            preset = (key, rms)
    perp = 0.0
    if len(travel) == 2:
        for v in values[first:settle + 1]:
            dx, dy = v[0] - start_value[0], v[1] - start_value[1]
            perp = max(perp, abs(dx * travel[1] - dy * travel[0]) / length)
    raw = speeds(times[first:settle + 1], values[first:settle + 1])
    # Smoothed over three samples, so one noisy frame is not the peak.
    v = [sum(raw[max(0, i - 1):i + 2]) / len(raw[max(0, i - 1):i + 2]) for i in range(len(raw))]
    top = max(range(len(v)), key=lambda i: v[i])
    peak_at = (times[first + top] - t_start) / duration if duration else 0.0
    mean = length / duration if duration else 0.0
    name = shape(peak_at, v[top] / mean if mean else 0.0)
    move: Json = {
        "channel": channel,
        "from": [round(x, 3) for x in start_value] if channel == "position" else round(start_value[0], 4),
        "to": [round(x, 3) for x in rest] if channel == "position" else round(rest[0], 4),
        "at": round(t_start, 3), "end": round(t_settle, 3), "duration": round(duration, 3),
        "curve": "spring" if overshoot > swing and swings >= 1 else name,
        "cubicBezier": {"kind": "cubic_bezier", "control": list(control)}, "fitError": round(error, 4),
        "preset": preset[0] if preset else None,
        "overshoot": round(overshoot, 3), "swings": swings, "settled": settled,
        "peakSpeed": round(v[top], 3), "peakAt": round(peak_at, 3), "meanSpeed": round(mean, 3),
    }
    if anticipation > swing:
        move["anticipation"] = round(anticipation, 3)
    if len(travel) == 2:
        move["pathBend"] = round(perp, 2)
    if first == 0 and len(v) > 1 and v[0] > tol * 10:
        move["startsBeforeWindow"] = True
    if move["curve"] == "spring":
        taus = [times[first + i] - t_start for i in range(len(progress))]
        move["spring"] = fit_spring(taus, progress, duration)
    move["keyframes"] = keyframes(times, values, first, settle, progress, start_value, travel, control, move)
    return move


def keyframes(times: List[float], values: List[Tuple[float, ...]], first: int, settle: int, progress: List[float],
              start_value: Sequence[float], travel: Sequence[float], control: Sequence[float], move: Json) -> List[Json]:
    """Scene keyframes in source seconds: one curve, or the swings of an overshoot as their own segments."""
    def value(p: float) -> Any:
        v = [a + p * d for a, d in zip(start_value, travel)]
        if len(v) == 2:
            return [round(x, 3) for x in v]
        # The scene's scale is [x, y]; its rotation is one number.
        return [round(v[0], 4)] * 2 if move["channel"] == "scale" else round(v[0], 4)

    if move["curve"] != "spring":
        easing: Any = move["preset"] or {"kind": "cubic_bezier", "control": list(control)}
        return [{"time": move["at"], "value": value(0.0), "easing": easing},
                {"time": move["end"], "value": value(1.0)}]
    turns = [0]
    for i in range(1, settle - first):
        a, b, c = progress[i - 1], progress[i], progress[i + 1]
        if (b > a and b >= c) or (b < a and b <= c):
            if abs(b - 1) > 0.01:
                turns.append(i)
    turns.append(settle - first)
    out = []
    for n, i in enumerate(turns):
        frame: Json = {"time": round(times[first + i], 3), "value": value(1.0 if n == len(turns) - 1 and move["settled"] else progress[i])}
        if n == 0:
            seg = turns[1]
            ts = [(times[first + k] - times[first]) / (times[first + seg] - times[first]) for k in range(seg + 1)]
            target = progress[seg] or 1.0
            sub, _ = fit_bezier(ts, [progress[k] / target for k in range(seg + 1)])
            frame["easing"] = {"kind": "cubic_bezier", "control": list(sub)}
        elif n < len(turns) - 1:
            frame["easing"] = "ease_in_out"
        out.append(frame)
    return out


def moves_of(target: Json, channel: str, tol: Optional[float] = None) -> List[Json]:
    tol = TOLERANCE[channel] if tol is None else tol
    times, values, dropped = series(target, channel)
    if len(times) < 3:
        return []
    found = runs(times, values, tol)
    out = []
    for n, (first, last) in enumerate(found):
        start = max(0, first - 1)
        rest_end = (found[n + 1][0] - 1) if n + 1 < len(found) else len(times) - 1
        nxt = times[found[n + 1][0] - 1] if n + 1 < len(found) else times[-1]
        found_moves = split(times, values, start, last, rest_end, tol, channel)
        parts = [(m, found_moves[k + 1]["at"] if k + 1 < len(found_moves) else nxt) for k, m in enumerate(found_moves)]
        for move, until in parts:
            move["target"] = target["id"]
            move["hold"] = round(max(0.0, until - move["end"]), 3)
            finish(move, target, dropped)
            out.append(move)
    return out


def turn_at(values: List[Tuple[float, ...]], first: int, last: int, rest_end: int, tol: float) -> Optional[int]:
    """Where a stretch turns back as a trip of its own, or None when it is one move.

    Its turning points are read along its line of travel, each one where it falls back more than
    3 * tol from its furthest point. It is one move when those turns are a damped swing about its
    rest, as a spring's are however lightly damped:
    - the first turn goes past the rest, by less than the travel when it starts at rest (a spring's
      overshoot stays under 100 %: at most 95 % is read as one; a window that opens mid-move has no
      travel to measure it by), and each later one lands on the other side of it;
    - the second lands closer to the rest than the first (by 5 %: a spring damped even 0.02 does),
      and each swing from turn to turn is narrower than the one before (this part does not hang
      on where the rest is);
    - nothing after the last turn swings wider than that turn did.
    Turns from the first one within 3 * tol of the rest on are settling and say nothing. A small
    dip back before it sets off (anticipation, under half its travel) is part of the move. Any
    other turn, back to where it began or short of the rest, is a trip of its own: it splits at the
    first such turn.

    The rest, in this order:
    1. Measured: the frames after the stretch, when they hold still (two within tol, or one that
       moved under tol from the stretch's last frame), or when the next stretch starts after them.
       A measured rest always wins.
    2. Its last frame, when a split ended the stretch there.
    3. The track ends while it still moves: the centre its start and first two turns close in on
       (Aitken's estimate, exact for a spring released from rest; its first three turns when the
       window opens mid-move), when they close in; else its last frame.
    """
    profile = rest_profile(values, first, last, rest_end, tol)
    if profile is None:
        return None
    _, _, line, turns, target, at_rest = profile
    gap = 3 * tol
    length = target
    if length > gap and turns and line[turns[0]] < 0 and -line[turns[0]] < 0.5 * length:
        turns = turns[1:]  # anticipation
    if not turns:
        return None
    sides = [line[k] - target for k in turns]
    # From the first turn within noise of the rest on, it is settling: those turns say nothing.
    small = next((n for n, x in enumerate(sides) if abs(x) <= gap), len(sides))
    sides = sides[:max(1, small)]
    # After its last turn it swings no wider than that turn did.
    last_turn = turns[len(sides) - 1]
    beyond = max(abs(x - target) for x in line[last_turn:])
    # Shrinking is read from turn to turn, which does not hang on where the rest is.
    steps = [abs(line[b] - line[a]) for a, b in zip(turns[:len(sides)], turns[1:len(sides)])]
    swing = (length > gap and tol < sides[0] and (not at_rest or sides[0] <= 0.95 * length + tol)
             and all(a * b < 0 for a, b in zip(sides, sides[1:]))
             and (len(sides) < 2 or abs(sides[1]) <= 0.95 * abs(sides[0]) + tol)
             and all(b <= 0.97 * a + 2 * tol for a, b in zip(steps, steps[1:]))
             and beyond <= abs(line[last_turn] - target) + 2 * tol)
    if swing:
        return None
    return first + turns[0]


def split(times: List[float], values: List[Tuple[float, ...]], first: int, last: int, rest_end: int,
          tol: float, channel: str, depth: int = 0) -> List[Json]:
    """The moves of one stretch. One that comes back where it began is split at its farthest point,
    and one that turns back on itself as a trip of its own (see turn_at) at that turn, again and
    again, so every trip is its own move while a spring's swings stay one move."""
    if last - first < 1 or depth > 64:
        return []
    # The turn first: it is cheap, and a stretch that splits needs no curve of its own.
    turn = turn_at(values, first, last, rest_end, tol)
    if turn is not None and first < turn < last:
        return (split(times, values, first, turn, turn, tol, channel, depth + 1)
                + split(times, values, turn, last, rest_end, tol, channel, depth + 1))
    move = move_of(times, values, first, last, rest_end, tol, channel)
    if move is None:
        far = max(range(first, last + 1), key=lambda i: dist(values[i], values[first]))
        if far in (first, last) or dist(values[far], values[first]) <= 3 * tol:
            return []
        return (split(times, values, first, far, far, tol, channel, depth + 1)
                + split(times, values, far, last, rest_end, tol, channel, depth + 1))
    return [move]


def finish(move: Json, target: Json, dropped: int) -> None:
    """The fields every move gets: its delay from the window start, dropped and blurred samples."""
    move["delay"] = round(move["at"] - target.get("origin", target["start"]), 3)
    if dropped:
        move["droppedSamples"] = dropped
    blurred = sum(1 for x in target["samples"] if isinstance(x, dict) and x.get("confidence") is not None
                  and MIN_CONFIDENCE <= x["confidence"] < SURE and move["at"] <= float(x.get("t", -1)) + target["start"] <= move["end"])
    if blurred:
        move["blurred"] = blurred


def all_moves(report: Any, target: Optional[str], channel: Optional[str], tol: Optional[float]) -> List[Json]:
    out = []
    for t in pick(targets_of(report), target):
        for c in ([channel] if channel else CHANNELS):
            out.extend(moves_of(t, c, tol))
    out.sort(key=lambda m: (m["at"], m["target"], CHANNELS.index(m["channel"])))
    # The stagger: how long after the previous target's move each one starts.
    last: Optional[Json] = None
    for m in out:
        if last is not None and m["target"] != last["target"]:
            m["staggerAfter"] = {"target": last["target"], "seconds": round(m["at"] - last["at"], 3)}
        last = m
    return out


# --- Compare -----------------------------------------------------------------------------------

def moves_input(data: Any, target: Optional[str], channel: Optional[str], scale: float = 1.0, offset: float = 0.0) -> List[Json]:
    if isinstance(data, dict) and isinstance(data.get("moves"), list):
        found = [dict(m) for m in data["moves"] if (target is None or m.get("target") == target)
                 and (channel is None or m.get("channel") == channel)]
        if scale != 1.0:
            for m in found:
                if m.get("channel") != "position":
                    continue
                for key in ("from", "to"):
                    if isinstance(m.get(key), list):
                        m[key] = [round(x * scale, 3) for x in m[key]]
                for key in ("peakSpeed", "meanSpeed", "pathBend"):
                    if isinstance(m.get(key), (int, float)):
                        m[key] = round(m[key] * scale, 3)
    else:
        if scale != 1.0:
            for t in targets_of(data):
                for s in t["samples"]:
                    if isinstance(s, dict) and "x" in s:
                        s["x"], s["y"] = s["x"] * scale, s["y"] * scale
        found = all_moves(data, target, channel, None)
    for m in found:
        m["at"] = round(m["at"] + offset, 3)
    return found


def compare(ref: List[Json], ours: List[Json], frame: float) -> Json:
    groups: Dict[Tuple[str, str], Tuple[List[Json], List[Json]]] = {}
    for m in ref:
        groups.setdefault((m["target"], m["channel"]), ([], []))[0].append(m)
    targets = {m["target"] for m in ref}
    lone = len(targets) == 1 and len({m["target"] for m in ours}) == 1
    for m in ours:
        key = (next(iter(targets)) if lone else m["target"], m["channel"])
        groups.setdefault(key, ([], []))[1].append(m)
    rows, passed = [], True
    for (target, channel), (a_list, b_list) in sorted(groups.items()):
        for n in range(max(len(a_list), len(b_list))):
            a = a_list[n] if n < len(a_list) else None
            b = b_list[n] if n < len(b_list) else None
            row: Json = {"target": target, "channel": channel, "move": n + 1}
            if a is None or b is None:
                row["pass"] = False
                row["why"] = "ours has a move the reference does not" if a is None else "the reference's move is missing from ours"
                rows.append(row)
                passed = False
                continue
            checks: Json = {}
            checks["start"] = (round(b["at"] - a["at"], 3), abs(b["at"] - a["at"]) <= max(2 * frame, PASS["start_s"]))
            checks["duration"] = (round(b["duration"] - a["duration"], 3),
                                  abs(b["duration"] - a["duration"]) <= max(2 * frame, PASS["duration_share"] * a["duration"]))
            if not (a["curve"] == "linear" and b["curve"] == "linear"):
                # A linear move has no peak: its fastest frame is noise.
                checks["peakAt"] = (round(b["peakAt"] - a["peakAt"], 3), abs(b["peakAt"] - a["peakAt"]) <= PASS["peak_at"])
            ratio = b["peakSpeed"] / a["peakSpeed"] if a["peakSpeed"] else 1.0
            checks["peakSpeed"] = (round(ratio, 3), abs(ratio - 1) <= PASS["peak_speed"])
            checks["overshoot"] = (round(b["overshoot"] - a["overshoot"], 3), abs(b["overshoot"] - a["overshoot"]) <= PASS["overshoot"])
            checks["swings"] = (b["swings"] - a["swings"], b["swings"] == a["swings"])
            checks["curve"] = (f"{a['curve']} / {b['curve']}", a["curve"] == b["curve"])
            row.update({k: {"diff": v, "pass": ok} for k, (v, ok) in checks.items()})
            row["pass"] = all(ok for _, ok in checks.values())
            if not row["pass"]:
                row["why"] = "; ".join(k for k, (_, ok) in checks.items() if not ok)
                passed = False
            rows.append(row)
    return {"pass": passed, "moves": rows, "limits": PASS}


# --- Diff --------------------------------------------------------------------------------------

def value_at(times: List[float], values: List[Tuple[float, ...]], t: float) -> Optional[Tuple[float, ...]]:
    """The channel's value at t, linear between samples; None outside the samples."""
    if not times or t < times[0] - 1e-6 or t > times[-1] + 1e-6:
        return None
    for i in range(1, len(times)):
        if t <= times[i] + 1e-6:
            span = times[i] - times[i - 1]
            k = 0.0 if span <= 0 else (t - times[i - 1]) / span
            return tuple(a + (b - a) * k for a, b in zip(values[i - 1], values[i]))
    return values[-1]


def diff(ref: Json, ours: Json, channel: str, offset: float = 0.0, scale_b: float = 1.0) -> Json:
    """Ours against the reference sample by sample, over the time both cover: the starting offset,
    maxDev raw and moveDev once that offset is removed. Passes on moveDev."""
    ta, va, _ = series(ref, channel)
    tb, vb, _ = series(ours, channel)
    tb = [t + offset for t in tb]
    if channel == "position" and scale_b != 1.0:
        vb = [tuple(x * scale_b for x in v) for v in vb]
    # Both tracks at every sample time of either, within the time both cover.
    lo, hi = (max(ta[0], tb[0]), min(ta[-1], tb[-1])) if ta and tb else (0.0, -1.0)
    grid = sorted({round(t, 6) for t in ta + tb if lo - 1e-6 <= t <= hi + 1e-6})
    pairs = [(t, value_at(ta, va, t), value_at(tb, vb, t)) for t in grid]
    pairs = [(t, a, b) for t, a, b in pairs if a is not None and b is not None]
    row: Json = {"target": ref["id"], "channel": channel, "limit": LIMIT[channel]}
    if len(pairs) < 2:
        row.update({"pass": False, "why": "the two tracks share fewer than 2 samples: check --offset and both windows"})
        return row
    start = tuple(b - a for a, b in zip(pairs[0][1], pairs[0][2]))
    raw = [(t, dist(a, b)) for t, a, b in pairs]
    moved = [(t, dist(a, tuple(x - o for x, o in zip(b, start)))) for t, a, b in pairs]
    worst = max(moved, key=lambda x: x[1])
    places = 1 if channel == "position" else 4
    row.update({"samples": len(pairs), "from": round(pairs[0][0], 3), "to": round(pairs[-1][0], 3),
                "startOffset": [round(x, places) for x in start], "placement": round(dist(start, [0.0] * len(start)), places),
                "maxDev": round(max(d for _, d in raw), places), "moveDev": round(worst[1], places), "worstT": round(worst[0], 3)})
    row["pass"] = row["moveDev"] <= LIMIT[channel]
    # Whether either side changes from where it is at the first shared sample.
    row["changes"] = any(dist(a, pairs[0][1]) > LIMIT[channel] / 2 or dist(b, pairs[0][2]) > LIMIT[channel] / 2
                         for _, a, b in pairs)
    if not row["pass"]:
        row["why"] = f"the move differs by {row['moveDev']} at {row['worstT']} s once the starting offset is removed"
    return row


def diff_all(ref_report: Any, ours_report: Any, target: Optional[str], target_b: Optional[str], channel: Optional[str],
             offset: float, scale_b: float) -> Json:
    refs = pick(targets_of(ref_report), target)
    ours = pick(targets_of(ours_report), target_b or target)
    lone = len(refs) == 1 and len(ours) == 1
    rows = []
    checks = []
    for r in refs:
        mate = ours[0] if lone else next((o for o in ours if o["id"] == r["id"]), None)
        if mate is None:
            rows.append({"target": r["id"], "pass": False, "why": "ours has no target with this id"})
            checks.append(False)
            continue
        for ch in ([channel] if channel else CHANNELS):
            row = diff(r, mate, ch, offset, scale_b)
            checks.append(row["pass"])
            # Every channel is measured. One that passes while neither side changes over the shared
            # time says nothing about the move and is left out of the report.
            if not channel and row["pass"] and not row.get("changes"):
                continue
            rows.append(row)
    return {"pass": bool(checks) and all(checks), "channels": rows, "limits": LIMIT,
            "minConfidence": MIN_CONFIDENCE}


# --- Speed -------------------------------------------------------------------------------------

def speed_rows(report: Any, target: Optional[str], channel: str) -> List[str]:
    lines = ["target,channel,t,speed"]
    for t in pick(targets_of(report), target):
        times, values, _ = series(t, channel)
        for when, v in zip(times, speeds(times, values)):
            lines.append(f"{t['id']},{channel},{when:.4f},{v:.4f}")
    return lines


# --- Command line ------------------------------------------------------------------------------

def emit(text: str, out: Optional[str]) -> None:
    if out:
        with open(out, "w", encoding="utf-8") as handle:
            handle.write(text)
    else:
        sys.stdout.write(text)


def main(argv: Optional[List[str]] = None) -> int:
    global MIN_CONFIDENCE
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--min-confidence", type=float, default=MIN_CONFIDENCE,
                        help="keep samples at or above this confidence (0.2 for a smeared fast move)")
    sub = parser.add_subparsers(dest="command", required=True)
    m = sub.add_parser("moves", help="each move's curve from a tracking report")
    m.add_argument("track")
    m.add_argument("--target")
    m.add_argument("--channel", choices=CHANNELS)
    m.add_argument("--tolerance", type=float, help="change a frame below which a channel is still")
    m.add_argument("--into", help="add the moves to this JSON object's moves list")
    m.add_argument("--out")
    c = sub.add_parser("compare", help="the reference's moves against ours")
    c.add_argument("ref")
    c.add_argument("ours")
    c.add_argument("--target")
    c.add_argument("--target-b", help="our target's id, when it differs")
    c.add_argument("--channel", choices=CHANNELS)
    c.add_argument("--offset", type=float, default=0.0, help="seconds added to our times")
    c.add_argument("--scale-b", type=float, default=1.0, help="multiplies our positions")
    c.add_argument("--fps", type=float, default=30.0)
    c.add_argument("--out")
    d = sub.add_parser("diff", help="the deviation per channel, with the starting offset removed")
    d.add_argument("ref")
    d.add_argument("ours")
    d.add_argument("--target")
    d.add_argument("--target-b", help="our target's id, when it differs")
    d.add_argument("--channel", choices=CHANNELS, help="every channel that changes on either side, when left out")
    d.add_argument("--offset", type=float, default=0.0, help="seconds added to our times")
    d.add_argument("--scale-b", type=float, default=1.0, help="multiplies our positions")
    d.add_argument("--out")
    s = sub.add_parser("speed", help="speed over time as CSV")
    s.add_argument("track")
    s.add_argument("--target")
    s.add_argument("--channel", choices=CHANNELS, default="position")
    s.add_argument("--out")
    args = parser.parse_args(argv)
    MIN_CONFIDENCE = args.min_confidence
    try:
        if args.command == "moves":
            track = load(args.track)
            found = all_moves(track, args.target, args.channel, args.tolerance)
            if args.into:
                doc = load(args.into)
                if not isinstance(doc, dict):
                    raise InputError(f"{args.into} must be a JSON object")
                # Every target and channel this run measured is replaced, still ones included.
                keys = {(t["id"], c) for t in pick(targets_of(track), args.target)
                        for c in ([args.channel] if args.channel else CHANNELS)}
                doc["moves"] = [x for x in doc.get("moves") or [] if (x.get("target"), x.get("channel")) not in keys] + found
                with open(args.into, "w", encoding="utf-8") as handle:
                    handle.write(json.dumps(doc, ensure_ascii=False, indent=2) + "\n")
            emit(json.dumps({"moves": found}, ensure_ascii=False, indent=2) + "\n", args.out)
            return 0
        if args.command == "compare":
            ref = moves_input(load(args.ref), args.target, args.channel)
            ours = moves_input(load(args.ours), args.target_b or args.target, args.channel, args.scale_b, args.offset)
            report = compare(ref, ours, 1 / args.fps)
            emit(json.dumps(report, ensure_ascii=False, indent=2) + "\n", args.out)
            return 0 if report["pass"] else 1
        if args.command == "diff":
            report = diff_all(load(args.ref), load(args.ours), args.target, args.target_b, args.channel,
                              args.offset, args.scale_b)
            emit(json.dumps(report, ensure_ascii=False, indent=2) + "\n", args.out)
            return 0 if report["pass"] else 1
        emit("\n".join(speed_rows(load(args.track), args.target, args.channel)) + "\n", args.out)
        return 0
    except (OSError, InputError) as exc:
        print("error: " + " ".join(str(exc).splitlines()), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
