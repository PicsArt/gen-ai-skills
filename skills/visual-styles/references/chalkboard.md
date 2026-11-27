# Chalkboard

A classroom lesson drawn live on a green board: a plant in a pot, a sun, arrows and handwritten labels draw
themselves in chalk, with the dusty stipple of real chalk on every line.

A subject with named parts (an engine, a heart) is drawn as the same cutaway an explainer draws in any other
style, in chalk: the style changes the line, never the vocabulary or the parts.

## Palette

Board `#2c3d33`, chalk white `#f2f0e6`, sun yellow `#f3dc6b`, leaf green `#9fd8a2`, water blue `#9cc6ef`.
**The hero colour is the yellow `#f3dc6b`, reserved for the sun, its rays and the answer line** ("= sugar!").

## The medium

- A flat board colour with two huge, very faint white ovals (about 3-4 % opacity) as chalk-dust smudges.
- **Every line is a chalk stroke** (7 px, 6 px for fine ones) in a shape layer with a keyed `trim`. Every layer
  of chalk carries the same two effects: `gaussian_blur` (about 3) then `alpha_dissolve` (size 2, density 0.85,
  fixed seed). The blur softens the edge and the dissolve breaks it into specks, which is the chalk grain.
- Objects are open paths, not filled shapes: a pot (a closed four-point outline), a stem with two leaves in
  green, a sun (a circle outline) with eight short rays, an arrow with a separate head, a small water arrow in
  blue. Nothing is filled.
- **Handwriting** is a loose hand face at 80-120 px in chalk white (and yellow for the answer), with the same
  two effects, written on with `typewriter` as each label is reached (never an opacity ramp).
- **Big chalk lettering** (a title word over 150 px) takes a dry chalk `brush` on the text content instead of
  the dissolve: `{"tip": "chalk", "coverage": 0.95, "streaks": 0, "angle": -24}`, at the board's angle. A few thin
  breaks show the board through the letters; coverage under 0.9 cuts the word into stripes. A board
  painted as a fill takes `{"tip": "chalk", "size": 40, "angle": -24, "streaks": 0.14}` for its
  rubbed-in smear.

## Motion habits

- **Draw on in lesson order:** pot, stem, leaves, sun, rays, arrow, water. Each `trim` end runs 0 to 1 over
  0.5-0.8 s with an ease in and out, starting just before the last one ends; labels write on with `typewriter` over 0.3 s as the
  stroke they name finishes.
- The chalk is **still while it is not drawing**: no wobble on finished lines; if some life is wanted, a
  `line_boil` preset at a very low `amplitude` and a stepped rate (a nested composition at `fps` 6).
- The title appears first, large, at the top; the answer appears last.
- Cued layers use `timeMode: "layer"`.

## Type

A loose hand-lettered face, chalk white, upper and lower case; yellow only for the answer.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Every line is a chalk stroke with the same two grain effects.
2. Objects are outlines; nothing is filled.
3. Strokes draw on in the order a teacher would draw them.
4. Labels sit beside the thing they name.
5. Yellow is used for the sun and the answer only.

## Build with the tools

Build each chalk stroke as a shape layer with `trim`, stroke and the two effects; text layers get the same
effects. Stagger starts so the lesson reads in order, and check with `picsart_scene_contact_sheet`.

## Do / don't

- **Do** let strokes overlap a little at joins.
- **Don't** use a realistic chalk texture image, a gradient, or filled colour; don't draw everything at once.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - **Arrivals and transitions.** strokes are drawn on (`trim`) and title lettering is written (`typewriter` or a clipped rise), the answer last; allowed between beats: a hard cut or a wipe by a duster stroke; forbidden: crossfades. Labels arrive as the motion habits describe.
  - **Finish.** the dust smudges sit in the board group; the grain is the two chalk effects with their fixed seed, so it holds steady; no pan.

## Originality guard

Draw your own diagram and wording. It must not copy a known educational channel's board, a textbook figure or
a named teacher's lettering. The chalk stipple and the live draw-on are the style.

## Proven on

The chalkboard-plants film (a plant in a pot, a sun with rays, arrows, handwritten labels and an answer line, all
drawn on in chalk).

**Not proven:** the written-on arrival was shown on a plain page with one label, not on a board with a plant, arrows and an answer line.