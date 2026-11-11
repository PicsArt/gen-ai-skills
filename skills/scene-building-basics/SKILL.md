---
name: scene-building-basics
description: Build and edit a scene with the scene tools - declaring media, audio and fonts as assets, layer trims, audio layers and transitions, reading the schema once before patching. Use whenever a use case composes or changes a scene document.
user-invocable: false
---

# Composing a scene

Read the scene schema once before your first edit (`picsart_scene_capabilities` with sections
`["schemaSummary"]`, then `["schema:<Name>"]` for each definition you need, never `["schema"]` whole), then build and change the scene with `picsart_scene_patch`. For a first scene,
the `quick-merge-and-export` recipe (`picsart_scene_recipe`) holds a working tool-call sequence to start
from.

## Media

A layer declares its file once in `assets` as `{ id, type: "video", uri: <url> }` and points at it
by id: `content: { kind: "media", assetId: "<id>", fit, trim }`. The scene document has no
`assetType` field and no `video` kind, and an `assetId` holding a URL is `unknown_asset_ref`. Keep
each layer's `trim` in its own source's seconds, with BOTH `in` and `out`. Skip dead ranges: trim
around them rather than speeding through them.

## Audio

Voice-over plays as `audio` layers (`content: { kind: "audio", assetId, trim: { in, out } }`), each
with its layer's `start` at the moment it is heard. A step's line starts 0.15 s after its panel
appears, so the picture lands first. Every `trim` needs BOTH `in` and `out`; a trim
with only `in` is a `missing_field` error. Mute a recording's own track (`muted: true` on its media
content) unless its sound is being kept. **If the scene schema ever lists no audio
layer, say so and stop** — do not export a silent video and do not invent a mix.

## Fonts

**Fonts are declared assets.** Declare the font once in `assets` (`{ id, type: "font", uri }`) and
reference that `id` as `font.family` in every text and caption style; a family name the scene does
not declare fails to resolve at export. If a font cannot be found or does not resolve, name it to
the user; never swap in another font without saying so.

**Name the weight in the face, not in `font.weight`.** `font.weight` renders only where the scene
is resolved natively; a runtime that draws a translated scene ignores it and draws the face
`font.family` names at its own weight (`validate_scene` warns `font_weight_no_op`). For bold text,
use a bold face, such as a catalog key like `acumin-pro-bold`, or a declared font asset of that
weight, and leave `weight` out.

**The face must draw every character.** A face that lacks a character draws nothing or a box in
its place, and no font tool says which scripts a face covers. For words in basic Latin, most faces
will do. For accents or another script (Cyrillic, Greek, Arabic, Devanagari, Chinese, Japanese,
Korean …), prefer a face whose name names that script, or search by the name of a family made for
it. Then prove it on the first frame that carries the rarest characters; if any is missing, pick
another face, build again, and tell the user which face you used.

## Overlays

**An overlay never blinks.** When a caption, a title or a sticker follows another in the same
place, start it where the last one ends, and never let an overlay's opacity drop to 0 for a frame
or two: a gap that short reads as a blink.

## Transitions

When a panel replaces the one before it, a hard cut is fine and keeps the energy; a soft seam
(`'crossfade'`, 0.3–0.5 s) suits a change of layout. Check the live catalog with
`picsart_scene_capabilities` (`sections: ["transitions"]`) before naming any other transition.

## Coordinates

A scene built by hand goes wrong first in its coordinates:
- **A shape layer inside a composition starts at that composition's centre.** Set its position to
  `[0, 0]` and draw the shape in the composition's own pixels, or it lands half a frame off.
- **A mask is in the pixels of the composition that holds its layer**, not the layer's own: draw it
  where it shows, never shifted by the layer's position, and it does not follow the layer when the
  layer moves. A photo inside a card is masked in the card's pixels; a title wipe, in the frame's.
- **A composition placed as a layer needs its `bounds`** (`[width, height]` of its own pixels), or
  it is fitted to its host: a 1000×1500 card comes out 1080×1620. `picsart_scene_validate` warns
  `composition_fitted_to_host`.
- **A group's `scale` is a ratio**: 1 is full size, never 100.

Check the first build with `picsart_scene_query_layout` at a few times before you export: a
layer 76,000 px wide or half a frame off shows there.

**A scene written as a file** can go directly to tools that accept an inline `scene`: read the
file's JSON and pass that object. When an actual scene edit returns a `sceneUrl`, use that URL
for later calls. Do not make an unchanged edit just to obtain a URL.

## Reusable parts

When you build a custom character or a part the user may want to adjust, declare root `parameters` for the knobs they will want (pose, expression, timing, strength): plain names in their terms, tight `min`/`max` (not 0..4000), a `default`, a `group` per body part or concern, a `description`. A draggable point is `type: "vec2"` with `frame: "composition"`, or `frame: {"layer": "<id>"}`. Motion goes in root `actions` whose `parameters` tracks key only number, boolean, text, color, vec2 or vec3 parameters, with no `$eval` (`scene-animation-reference`, `references/named-actions.md`). `picsart_scene_tune` (see `motion-design-craft`) tunes what is declared, plus root layers' position.
