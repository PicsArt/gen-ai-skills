#!/usr/bin/env python3
"""
Check that a scene keeps to its style: every colour it draws comes from the style's roles, and
its text does not all enter the same way.

    python3 scripts/adherence.py <input.json>

The input is `{scene, style, brand?}`: the built scene, and the style id (or tokens) and brand it
was built with. It prints one JSON line, `{ok, findings}`. Each finding has a `code`, the `layer`
it is about when there is one, a `message` and a `fix`:

- `off_palette`: a layer draws a colour that is not one of the style's roles;
- `one_entrance`: every text layer enters the same way, which reads as a template;
- `linear_move`: a keyframed move of position or scale on a linear easing, which reads as a
  machine: a move eases in and out;
- `overshoot`: a curve that overshoots (a cubic-bezier control below 0 or above 1) on a panel,
  a position or an opacity. A bounce belongs only to a payoff pop: the scale of a word or a shape.

What is not a drawn colour is skipped: a mask's own fill (it only cuts the shape) and a scrim's
black (it darkens the recording under words).

Python 3.9 or later, the standard library only, offline.
"""
from __future__ import annotations

import json
import re
import sys
from typing import Any, Dict, Iterator, List, Tuple

from style import colors, resolve

HEX = re.compile(r'^#[0-9a-fA-F]{6}(?:[0-9a-fA-F]{2})?$')


def color(value: str) -> str:
    return value[:7].lower() if HEX.fullmatch(value) else value.lower()


def drawn_colors(layer: Dict[str, Any]) -> Iterator[str]:
    """The colours a layer draws, its mask left out."""
    def walk(node: Any) -> Iterator[str]:
        if isinstance(node, dict):
            for k, v in node.items():
                # A nested scene's own layers and frame are checked as that scene's, not this layer's.
                if k in ('mask', 'layers', 'clips', 'scene'):
                    continue
                if k in ('color', 'fill', 'stroke', 'background'):
                    if isinstance(v, str) and HEX.fullmatch(v):
                        yield color(v)
                    elif isinstance(v, dict):
                        for key in v.get('keyframes') or []:
                            value = key.get('value') if isinstance(key, dict) else None
                            if isinstance(value, str) and HEX.fullmatch(value):
                                yield color(value)
                yield from walk(v)
        elif isinstance(node, list):
            for v in node:
                yield from walk(v)
    yield from walk(layer)


def local_layers(scene: Dict[str, Any], masks: bool = False) -> Iterator[Tuple[str, Dict[str, Any]]]:
    """Every layer in this scene, including inline groups and track clips."""
    def walk(layer: Dict[str, Any], fallback: str = '') -> Iterator[Tuple[str, Dict[str, Any]]]:
        lid = layer.get('id', fallback)
        yield lid, layer
        content = layer.get('content') or {}
        for key in ('layers', 'clips'):
            for child in content.get(key) or []:
                if isinstance(child, dict):
                    yield from walk(child, lid)
        mask_spec = layer.get('mask') or {}
        mask = mask_spec.get('clip') or mask_spec.get('layer')
        if masks and isinstance(mask, dict):
            yield from walk(mask, lid)
    for layer in scene.get('layers') or []:
        if isinstance(layer, dict):
            yield from walk(layer)


def scenes_of(scene: Dict[str, Any], seen: Tuple[int, ...] = (), masks: bool = False) -> Iterator[Dict[str, Any]]:
    """The root and referenced scenes, with cycles stopped at the current path."""
    if id(scene) in seen:
        return
    yield scene
    assets = scene.get('assets') or {}
    if isinstance(assets, list):
        assets = {a.get('id'): a for a in assets if isinstance(a, dict)}
    for _, layer in local_layers(scene, masks):
        content = layer.get('content') or {}
        for decoration in (content.get('style') or {}).get('decorations') or []:
            spec = decoration.get('content') or {}
            ref = spec.get('sceneRef')
            if spec.get('kind') == 'scene' and isinstance(ref, str) and ref.startswith('mpscene://'):
                asset = assets.get(ref[len('mpscene://'):]) or {}
                inner = asset.get('scene')
                if isinstance(inner, dict):
                    yield from scenes_of(inner, seen + (id(scene),), masks)
        if content.get('kind') == 'scene_ref':
            asset = content.get('asset') or assets.get(content.get('assetId')) or {}
            inner = asset.get('scene') if isinstance(asset, dict) else None
            if isinstance(inner, dict):
                yield from scenes_of(inner, seen + (id(scene),), masks)


def layers_of(scene: Dict[str, Any], masks: bool = False) -> Iterator[Tuple[str, Dict[str, Any]]]:
    """Every layer, nested scenes' included, by id."""
    for inner in scenes_of(scene, masks=masks):
        yield from local_layers(inner, masks)


def overshoots(easing: Any) -> bool:
    if not isinstance(easing, dict) or easing.get('kind') != 'cubic_bezier':
        return False
    c = easing.get('control') or []
    return len(c) == 4 and any(isinstance(y, (int, float)) and (y < 0 or y > 1) for y in (c[1], c[3]))


def motion(scene: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Moves on a linear curve, and bounces where a bounce does not belong."""
    findings: List[Dict[str, Any]] = []
    for lid, layer in layers_of(scene, masks=True):
        kind = (layer.get('content') or {}).get('kind')
        for prop, track in (layer.get('animations') or {}).items():
            keys = [k for k in (track or {}).get('keyframes') or [] if isinstance(k, dict)]
            for a, b in zip(keys, keys[1:]):
                easing = a.get('easing', 'linear')
                if prop in ('position', 'scale') and a.get('value') != b.get('value') and easing == 'linear':
                    findings.append({'code': 'linear_move', 'layer': lid, 'message': f"{lid}'s {prop} moves on a linear curve at {a.get('time')} s",
                                     'fix': 'ease it: the house curve is cubic-bezier(0.16, 1, 0.3, 1)'})
                    break
                pop = prop == 'scale' and kind in ('text', 'shape')
                if overshoots(easing) and not pop:
                    findings.append({'code': 'overshoot', 'layer': lid, 'message': f"{lid}'s {prop} overshoots at {a.get('time')} s",
                                     'fix': 'use a curve that settles without a bounce; keep bounces for a payoff pop'})
                    break
    return findings


def text_entrances(scene: Dict[str, Any], inherited: Tuple[str, ...] = (), seen: Tuple[int, ...] = ()) -> Iterator[str]:
    """Text presets or changing layer tracks, including those carried by a container."""
    if id(scene) in seen:
        return
    seen += (id(scene),)
    assets = scene.get('assets') or {}
    if isinstance(assets, list):
        assets = {a.get('id'): a for a in assets if isinstance(a, dict)}

    def walk(layer: Dict[str, Any], parent: Tuple[str, ...]) -> Iterator[str]:
        content = layer.get('content') or {}
        moved = list(parent)
        for prop in ('opacity', 'position', 'scale'):
            track = (layer.get('animations') or {}).get(prop) or {}
            keys = [k for k in track.get('keyframes') or [] if isinstance(k, dict)]
            if prop not in moved and (track.get('expression') or any(a.get('value') != b.get('value') for a, b in zip(keys, keys[1:]))):
                moved.append(prop)
        if content.get('kind') == 'text':
            presets = [a['preset'] for a in content.get('animations') or [] if isinstance(a, dict) and a.get('preset')]
            yield from presets
            if not presets and moved:
                yield 'a layer ' + ' and '.join(p for p in ('opacity', 'position', 'scale') if p in moved) + ' move'
        for key in ('layers', 'clips'):
            for child in content.get(key) or []:
                if isinstance(child, dict):
                    yield from walk(child, tuple(moved))
        if content.get('kind') == 'scene_ref':
            inner = (content.get('asset') or assets.get(content.get('assetId')) or {}).get('scene')
            if isinstance(inner, dict):
                yield from text_entrances(inner, tuple(moved), seen)

    for layer in scene.get('layers') or []:
        if isinstance(layer, dict):
            yield from walk(layer, inherited)


def check(scene: Dict[str, Any], tokens: Dict[str, Any]) -> List[Dict[str, Any]]:
    allowed = {color(c) for c in colors(tokens)}
    findings: List[Dict[str, Any]] = []
    for inner in scenes_of(scene):
        background = color((inner.get('composition') or {}).get('background') or '')
        if background and background not in allowed:
            findings.append({'code': 'off_palette', 'message': f'the frame is {background}, not the style\'s canvas',
                             'fix': f"build with the style, so the background is {tokens['canvas']}"})
    entrances = set(text_entrances(scene))
    for lid, layer in layers_of(scene):
        for c in sorted(set(drawn_colors(layer))):
            # A scrim's black darkens the recording under words; any other colour it draws is checked.
            if c not in allowed and not ('scrim' in lid and c == '#000000'):
                findings.append({'code': 'off_palette', 'layer': lid, 'message': f'{lid} draws {c}, which is not in the style',
                                 'fix': f"use one of the style's colours: {', '.join(sorted(allowed))}"})
    findings += motion(scene)
    if len(entrances) == 1:
        findings.append({'code': 'one_entrance', 'message': f'every text layer enters with {next(iter(entrances))}',
                         'fix': "give the titles and the lines the style's own entrances (style.py `entrance`)"})
    return findings


def main(argv: List[str]) -> int:
    if len(argv) != 1:
        sys.stderr.write('usage: adherence.py <input.json>\n')
        return 2
    try:
        with open(argv[0], encoding='utf-8-sig') as f:
            data = json.load(f)
        tokens = resolve(data['style'], data.get('brand'))
        findings = check(data['scene'], tokens)
    except (OSError, ValueError, KeyError, TypeError) as err:
        sys.stderr.write('adherence.py: ' + ' '.join(str(err).split()) + '\n')
        return 1
    print(json.dumps({'ok': not findings, 'findings': findings}))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
