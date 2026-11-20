# Woodcut

A black ink block cut with white gouge marks: concentric rings for the sun, short tapered dashes for the sky,
wavy lines for the sea, and a paper-white boat on top. The picture is carved in, a few marks at a time.

## Finish

A fixed paper-grain noise layer on top (not animated) and carving stepped at `fps` 6 (see Motion habits).

## Palette

Ink `#141414`, paper `#efe6d2`. Two colours only. **No hue is used. The hero is the paper white left in the
boat**, the only solid that is paper-coloured rather than cut into the ink.

## The medium

- A paper-coloured layer under a **black rectangle with small rounded corners** (the block), inset from the
  frame so a border of paper shows.
- Every mark is a **paper-coloured stroke with a taper**: `taper` with `startLength` and `endLength` about 0.35
  and widths 0 at both ends, so each gouge swells in the middle like a chisel cut. Line weights 4-9 px; heavier
  nearer the bottom.
- **Sun rings:** one circle with a `repeater` of 6 copies, each scaled 1.45, stroked as a gouge.
- **Sky:** 40 short, almost horizontal strokes of random length (60-160 px) scattered, none inside the sun's
  area, as one path group with one gouge stroke.
- **Sea:** nine long lines with a smooth `zigZag` (amplitude 6 growing to 14, frequency falling from 14 to 6
  down the rows) so the rows get bolder and longer toward the viewer.
- **The boat** is two paper-coloured closed paths (a sail and a hull) with no outline.
- A **paper-grain** adjustment layer over everything: a noise effect with a fixed seed.

## The character

Drawn from the style's own shapes, not a generated sheet (the mechanism, saving and talking are in [shapes-character](shapes-character.md)); build once, save once to the library, place it by its `uri` in every shot.

- **Proportions:** about 5 heads tall: a black block.
- **Shapes:** one black silhouette per part with tapered white gouge strokes carved into it for folds, the face a few white gouges; no other colour.
- **Face:** two white gouge eyes; no mouth chart, so no talking.
- **Controls:** drop `mouth`; `blink` scales the two gouges; the acting is the silhouette.

## Motion habits

- **Carving is stepped.** Reveal each group with a keyed `trim` end (0 to 1 over a second or so), later
  groups starting 0.1-0.2 s after the last (sun, sky, then the sea rows from top to bottom). Put the carved
  layers in a nested `composition` with `fps` 6 so the marks arrive in jerks like cuts.
- **Hand shake:** the `wiggle` preset on each sea line (small amount, `frequency` 8), a different `seed` per
  line. **Tremble** of the sun is the `line_boil` preset at a low amplitude.
- The boat enters from beyond the frame edge on position keys (no opacity key); the entry ends on the point the drift track already passes at that moment, so the boat neither jumps nor pauses, and it keeps moving on the drift; its rotation follows its path with
  the layer's `positionDirection()` expression (the one layer-level expression this style needs), and it bobs.
- Cued layers use `timeMode: "layer"`.

## Type

A title, if any, is a heavy slab or blackletter in paper colour, cut into the block's lower corner; never
anti-aliased soft.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Two colours only, with a margin of paper around the block.
2. Every mark tapers at both ends.
3. Sun rings, sky dashes and sea lines each carved in order.
4. The boat is the only paper-white solid.
5. The grain layer sits on top and is fixed, not animated.

## Build with the tools

Make the marks as shape layers with `taper` on the stroke, the rings with one `repeater`, and the waves with a
`zigZag` item on a straight path; key their `trim`. Nest them in a `composition` with `fps` 6, apply `wiggle`
and `line_boil` to the inner layer ids with `picsart_scene_apply_preset`, and add the grain as an adjustment layer
above the nested composition.

## Do / don't

- **Do** vary line weight and length; uniform marks look like a pattern, not a cut.
- **Don't** use grey, soft edges or a blur; don't animate the grain's seed.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Rate split: the carved marks step at 6 inside the nested composition; the boat's travel and the grain layer run at
    the root rate.
  - Nothing fades: marks and the title arrive carved, by a keyed `trim`; shots join on hard cuts only.
  - Finish: the grain is one fixed layer, added once; there is no pan in this style, so it stays on the frame (if a
    camera move is added, the grain moves into the moved group).
  - Hatch rides the object: gouges carved into a character's silhouette are parented to its part; the sun, sky and sea
    marks are background and stay put.

## Originality guard

Cut your own scene. It must not reproduce a famous woodcut or linocut, a named printmaker's wave or figure, or
a known book's illustration. The ink block, the tapered gouge and the stepped carving are the style.

## Proven on

The sea-woodcut film (gouged sun rings, scattered sky marks, nine wave rows carved in, a boat that turns to
its motion, paper grain on top).

**Not proven:** the boat's entry from beyond the edge was shown on a plain page with one boat, not in the full scene.