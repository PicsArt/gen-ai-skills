# Getting the design out of Figma

## Contents

- Read the tree once, fetch in batches
- Bring each element in as its own layer
- Convert shapes and their paint — don't bake them
- Properties of exports you must design around
- Match assets to boxes by aspect
- Image fills
- Resolution: match the source to the largest displayed size

## Read the tree once, fetch in batches

Everything in this reference applies when the user has shared the design through their Figma
connector: it describes what to ask that connector for. Without one, work from the files the user provides.

1. Read the page's frame tree once: it returns the **entire tree** — frames, layers, names,
   boxes. Everything below is derived from it. Do not walk the board frame by frame to explore.
2. Batch every frame capture and asset export you ask the connector for into one round, so a later
   beat does not send you back for one more asset.

A frame capture will not upscale past a node's natural size; ask the connector for a 2× or 3× export
when you need more.

## Bring each element in as its own layer

The scene is a composite of movable layers, never a montage of flat screens. So the **default is to
reconstruct each element in the medium that keeps it movable and editable** — match the design layer
for layer:

| element kind | bring it in as |
|---|---|
| a shape or vector | author editable shape geometry from the user-shared design; apply CSS paint to that existing layer with `picsart_scene_import_figma_paint` |
| text | live text, from the layer's string + font in the metadata |
| a photo / raster fill | the original bitmap, at its largest available size, placed by its `scaleMode` ("Image fills" below) — **never a node export or a screenshot**, which flatten its transparency |

## Convert shapes and their paint — don't bake them

A panel is geometry plus paint. Keep the geometry editable so corners, paths and placement can change. From the design the user shared, construct the shape from measured geometry, then apply supported CSS fill, outer shadow or gradient paint with `picsart_scene_import_figma_paint`. That tool edits an existing layer here; it does not accept a complete design node.

The hosted paint importer takes CSS strings, not design-file color profiles. Preserve the actual source colors through the user's design/export workflow and inspect rendered output; do not pass unsupported profile or node arguments or claim automatic profile conversion.

| Figma paint (as CSS) | → scene item |
|---|---|
| solid / alpha fill (`rgba(...)`, `#rrggbbaa`) | shape `fill` (alpha → the item's `opacity`) |
| outer `box-shadow` | `drop_shadow` effect |
| `linear-`/`radial-gradient(...)` | `gradientFill` (pass the element `size` — CSS carries only an angle) |
| **inset `box-shadow`** | **no scene equivalent** — returned in `skipped`; keep an SVG for *that glow only* |

Either way the tool returns `applied` and `skipped`, so you know precisely what converted and what
still needs a bake. Bake a panel's paint only for a `skipped` treatment (today: an inner shadow) or a
genuinely un-layered source — never as the default. This is the one narrow, disclosed place the "export a node
flat" habit below still applies to a panel.

**Flattening a node to a single image is the fallback only** — used when a design's layers genuinely
cannot be had (a rasterised source, no layer access). When you fall back, say so plainly. Never
export a parent group or frame in place of its children: the children are what move.

### Export a node flat only for one element you are importing whole

Once — and only once — you have decided an element goes in as a single piece, export **that node**
for a faithful appearance: the export is the composited result, including its crop, effects and
dimming, and needs no fitting.

- **Do not generalise this into "raster everything."** It buys fidelity for *one* element you have
  already chosen to bring in whole — it is not a licence to seal a frame, a parent group, or a
  vector into a PNG.
- **Exports are opaque and occlude what is behind them** (detail in the next section). If the
  element must sit over other layers, rebuild it as a shape layer or construct an alpha channel instead.
  An image with transparency is never exported: its original bitmap keeps the alpha.
- Reconstructing a *placement* from measurements is the trap the node export avoids: a designer's
  crop is often manual, not a fit rule, and fitting it back from renders is unreliable — bbox fits
  break on clipped search windows, correlation fits stall at low confidence, template matches return
  impossible answers. The node export is pixel-exact for the element it captures.

Asset URLs are short-lived. Download them in the same turn you request them, then bring each one in
through the user's available upload route and put
the URL it returns in the asset's `uri`. A Figma asset URL expires after the scene is written, and a
local path (`file:`) or an object URL (`blob:`) never renders anywhere: the validator refuses both.
Probe the uploaded URL with `picsart_media_probe` for the `width` and `height` to declare.

## Properties of exports you must design around

- **Exports are opaque.** A node's export, like a screenshot, is drawn over its frame's
  background colour, so every transparent pixel comes back opaque in that colour: a cutout photo on
  a dark frame arrives on a black box. Its original bitmap is the same picture with its alpha.
  Dropping an export over other content
  occludes whatever is behind it — including the invisible margin around a glowing element. If the
  element must sit over other layers, either rebuild it as a shape layer or construct an alpha channel
  (solid inside the body, derived from luminance outside).
- **Export bounds are the node's *render* bounds, not its layout box.** An element with a glow or
  shadow exports larger than its box. Compute the margin (`export_size / scale − box_size`) and
  place the layer by its **box centre**; do not assume the margin is symmetric — verify per axis.
- **A group export contains only that group's children.** An icon that is a *sibling* of the button
  group is not in the button's export, so the button renders as empty chrome unless you add the
  glyph as its own layer. Check the tree for siblings before assuming a control is self-contained.
- **Child coordinates are not consistently absolute.** Some groups store children in the parent's
  space, others relative to the group. Cross-check one child against the rendered frame before
  trusting a whole subtree of offsets.
- **Raw images come at several resolutions.** Dedupe by content hash and keep the largest. Two
  same-size variants of one asset are common — typically an opaque studio version and an alpha
  cutout. Check alpha before choosing: a cutout on a dark canvas reads full-bleed, the opaque one
  shows its own background.
- **A group that moves as one is one inline `composition` layer.** Put a card's backing, image,
  label and icon in `{ "kind": "composition", "layers": [...] }` and keyframe that layer only — the
  same keyframes copied onto each member drift apart. It is part of this scene (same asset table),
  not a `scene` asset, which is a separate document for reuse. Without a `composition` size block
  it takes the enclosing canvas's size and crops what falls outside that frame; a fade, mask or
  blend applies to the group as one.
  Its members' times are local to its `start`. `parentId` = the backing is the alternative when the
  members must stay separate layers; it carries the transform only.

## Match assets to boxes by aspect

When several images come back unnamed, their **own aspect identifies which box each belongs
to**. Compare `width/height` against each candidate box's ratio — a match to three decimals is
conclusive, and it catches a swapped pair immediately.

The same check finds shared assets: if one image's aspect fits two different frames' boxes, the
design is probably reusing it, which changes a "content change" into a "same picture, different
crop".

## Image fills

Media `crop` is a static or keyframed region of one image or video; `scene://crop` is for camera moves (centre + zoom) or framing a scene.

A node's IMAGE paint carries a `scaleMode`. Each one is a media layer on the image asset, with
`bounds` set to the node's size and the asset's `width`/`height` declared from the image itself:

| Figma `scaleMode` | Media content |
|---|---|
| `FILL` | `fit: "cover"` |
| `FIT` | `fit: "contain"` |
| `CROP` | `fit: "cover"` + `crop` |
| `TILE` | not expressible: a repeated image is a gap, so say so rather than approximate it |

For `CROP`, read the paint's `imageTransform` `[[a, 0, tx], [0, d, ty]]`, which is the node's box in
the image's unit square. With an image of W×H pixels:

    crop = [tx·W, ty·H, a·W, d·H]

Self-check: `(a·W)/(d·H)` must match the node's `width/height` to about two decimals. If it
doesn't, the numbers are off (the wrong image, or its size read at a different scale).

Example: a 1672×941 image on a 557×535 card with `a = 0.5138`, `d = 0.8778`, `tx = 0.1926`,
`ty = 0` gives `crop: [322, 0, 859, 826]`. Its aspect, 1.040, matches the card's 1.041.

A transform with non-zero off-diagonal terms is a rotated crop, which `crop` cannot express.
Export that node instead — unless the image has transparency, which the export loses: then the
rotated crop is a gap, so say so.

## Resolution: match the source to the largest displayed size

Crop from a source at least as large as the biggest size the asset is ever *displayed* at, not its
resting size. An asset that rests at 1:1 but flies in at 2.35× is being upscaled 2.35× for the
whole entrance. Export the frame at 2× and re-cut when an element is scaled up anywhere in its
life.

Do not crop rectangular regions out of a composed card to get its parts — the crop carries the
card's own fill as a visible box behind each part. Export the card.
