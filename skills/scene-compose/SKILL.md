---
name: scene-compose
description: Build and edit an MP Scene with the scene tools - declaring media, audio and fonts as assets, layer trims, audio layers and transitions, reading the schema once before patching. Use whenever a use case composes or changes a scene document.
user-invocable: false
---

# Composing a scene

Read `picsart_media_get_scene_schema` once before your first edit, then build and change the scene
with `picsart_media_patch_scene`. For a first scene, `picsart_media_quickstart` returns a working
tool-call sequence to start from.

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
content) unless its sound is being kept. **If `picsart_media_get_scene_schema` ever lists no audio
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

## Transitions

When a panel replaces the one before it, a hard cut is fine and keeps the energy; a soft seam
(`'crossfade'`, 0.3–0.5 s) suits a change of layout. Check the live catalog with
`picsart_media_get_capabilities` (`sections: ["transitions"]`) before naming any other transition.
