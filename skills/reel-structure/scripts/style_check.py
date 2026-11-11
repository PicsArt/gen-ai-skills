"""Checks a style entry's catalog calls and times against the scene engine, free and local.

A catalog call in a style is written in backticks as `kind:id(name=value, name=value)`, the kind
one of look, motionPreset, effect, transition or textAnimation; the brackets are left out when the
defaults are kept. A value is a number, a keyframed run of numbers (`32→0`, `1.08→1.2→1.08`), an
enum word, a `#rrggbb` colour or a quoted text. Every name, enum word and number is checked
against the catalog snapshot the skill ships (`data/catalog-<build>.json`).

Every time in seconds lands on the 30 fps frame grid (a multiple of 1/30 s, to 1 ms).
"""
from __future__ import annotations

import glob
import json
import os
import re
from typing import Dict, List

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
KINDS = ("look", "motionPreset", "effect", "transition", "textAnimation")
CALL = re.compile(r"`(look|motionPreset|effect|transition|textAnimation):([a-z0-9_]+)(?:\(([^`]*)\))?`")
BARE = re.compile(r"`([a-z][a-z0-9_]*)`")
NUMBER = re.compile(r"-?\d+(?:\.\d+)?")
SECONDS = re.compile(r"(?<![\w.#-])(\d+(?:\.\d+)?)(?:\s?[–-]\s?(\d+(?:\.\d+)?))?\s?s\b")
# The track transition's own window length is set on the track, not in the definition's params.
TRACK_FIELDS = {"transition": {"duration"}}
FPS = 30


def catalog() -> Dict[str, Dict]:
    """The newest catalog snapshot in the skill's data folder."""
    found = sorted(glob.glob(os.path.join(SKILL, "data", "catalog-*.json")))
    if not found:
        raise SystemExit(f"no catalog snapshot in {os.path.join(SKILL, 'data')}")
    return json.load(open(found[-1], encoding="utf-8"))


def _check_value(where: str, name: str, spec: Dict, value: str, out: List[str]) -> None:
    value = value.strip()
    kind = spec.get("type")
    if "enum" in spec:
        # A number is checked as a number (the catalog stores `rows` as 1..12), each step of a keyframed run too.
        numbers = {float(e) for e in spec["enum"] if isinstance(e, (int, float)) and not isinstance(e, bool)}
        steps = [s.strip() for s in re.split(r"→|->", value)] if numbers else [value]
        for step in steps:
            if not (step.strip("\"'") in spec["enum"] or NUMBER.fullmatch(step) and float(step) in numbers):
                out.append(f"{where}: {name}={value} is not one of {spec['enum']}")
                return
        return
    if kind == "color":
        if not re.fullmatch(r"#[0-9a-fA-F]{6}([0-9a-fA-F]{2})?", value):
            out.append(f"{where}: {name}={value} is not a #rrggbb colour")
        return
    if kind in ("text", "string", "font"):
        return
    if kind == "boolean":
        if value not in ("true", "false"):
            out.append(f"{where}: {name}={value} is not true or false")
        return
    steps = [s.strip() for s in re.split(r"→|->", value)]
    for step in steps:
        if not NUMBER.fullmatch(step):
            if kind in ("number", "integer"):
                out.append(f"{where}: {name}={value} is not a number or a keyframed run of numbers")
            return
        n = float(step)
        if "min" in spec and n < spec["min"] or "max" in spec and n > spec["max"]:
            out.append(f"{where}: {name}={step} is outside {spec.get('min')}..{spec.get('max')}")


def check_calls(where: str, text: str, cat: Dict, bare_kind: str = "") -> List[str]:
    """Every `kind:id(params)` in the text exists with those params; bare catalog ids name their kind."""
    out: List[str] = []
    for kind, ident, args in CALL.findall(text):
        table = cat.get(kind, {})
        if ident not in table:
            out.append(f"{where}: {kind}:{ident} is not in the {cat.get('build')} catalog")
            continue
        for part in [p for p in re.split(r",\s*(?=[A-Za-z_]+\s*=)", args or "") if p.strip()]:
            if "=" not in part:
                out.append(f"{where}: {kind}:{ident} parameter '{part.strip()}' needs name=value")
                continue
            name, value = [s.strip() for s in part.split("=", 1)]
            if name in TRACK_FIELDS.get(kind, ()):
                continue
            spec = table[ident].get(name)
            if spec is None:
                out.append(f"{where}: {kind}:{ident} has no parameter '{name}' (it has {sorted(table[ident])})")
            else:
                _check_value(f"{where}: {kind}:{ident}", name, spec, value, out)
    for ident in BARE.findall(CALL.sub("", text)):
        if bare_kind and ident in cat.get(bare_kind, {}):
            continue
        kinds = [k for k in KINDS if ident in cat.get(k, {})]
        if kinds:
            out.append(f"{where}: `{ident}` must name its kind: " + " or ".join(f"`{k}:{ident}`" for k in kinds))
    return out


def off_grid(text: str) -> List[str]:
    """Times in seconds that do not land on the 30 fps frame grid."""
    bad = []
    for match in SECONDS.finditer(text):
        for t in [g for g in match.groups() if g]:
            frames = float(t) * FPS
            if abs(frames - round(frames)) > FPS * 0.001:
                bad.append(t)
    return bad


def main(paths: List[str]) -> int:
    """Check style files (default: every one in styles/): catalog calls and the 30 fps grid."""
    paths = paths or sorted(glob.glob(os.path.join(SKILL, "styles", "*.md")))
    cat = catalog()
    problems = []
    for path in paths:
        text = open(path, encoding="utf-8").read()
        problems += check_calls(path, text, cat, "transition")
        cells = [l for l in text.splitlines() if re.match(r"^\| (Motion|Seams|Ending|Text) \|", l)]
        problems += [f"{path}: {t} s is off the 30 fps grid" for t in off_grid("\n".join(cells))]
    print("\n".join(problems) or f"{len(paths)} styles OK")
    return 1 if problems else 0


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))
