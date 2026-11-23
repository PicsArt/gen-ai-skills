# Mid-century toon

Flat colour blocks printed slightly off register, angular figures, atomic starbursts and boomerang clouds,
animated on twos and fours like limited-animation shorts.

## Finish

The off-register print on every solid object, the figure and foreground on twos (`fps` 12 under a 24 fps root) and the clouds, sun and stars on fours (`fps` 6), in nested compositions (see Motion habits).

## Palette

Mustard `#e9b84e` ground, teal `#2f7c78`, cream `#f5ead2`, olive `#8a9a3c`, ink `#2a2622`. Backdrop colour
blocks are rectangles at 0.35-0.9 opacity that deliberately miss every edge. **The hero colour is coral
`#e0644d`, reserved for the subject's clothing and the title** and never used on blocks or props.

## The medium

- **Off-register print.** Draw the ink outline once and the flat colour as a second copy shifted `(9, -7)`:
  a group of the geometry with a 4 px stroke, then a group of the same geometry with a fill at
  `position [9, -7]`. Use it on every solid object, characters included, with the same offset.
- Figures are rectangles and quads, not curves: a trapezoid torso, a box or wedge head with a triangle nose, a
  hat of two rectangles, two-tone clothes. Limbs are bodied wedges, not strokes: each sleeve grows out of the torso at the shoulder and tapers, the forearm and hand are one shape, the legs are slim wedges that grow out of the torso's bottom edge. Eyes
  are two dots and a brow line; the mouth is a slash.
- Props are shapes, not detail: skinny lollipop and cone trees on a stick, boomerang clouds as an eight-point
  closed path, atomic stars as an 8-point `polystar` with a tiny inner radius (0.25) and a 2 px stroke, a ground
  band of ink with a thin cream line on top.

## The character

Drawn from the style's own shapes, not a generated sheet (the mechanism, saving and talking are in [shapes-character](shapes-character.md)); build once, save once to the library, place it by its `uri` in every shot.

- **Proportions:** about 6 heads tall, lanky: a box head on a trapezoid torso, tapered wedge limbs.
- **Shapes:** a trapezoid torso, a box or wedge head with a triangle nose, a hat of two rectangles, and bodied limbs: a sleeve wedge from each shoulder (about 0.39 of the torso's width at its root, narrowing to the elbow), forearm and hand as ONE tapered closed shape with one outline, slim leg wedges that start inside the torso and grow out of its bottom edge, no strokes; each solid shape is the ink outline plus a flat copy shifted (9, -7), the style's off-register print.
- **Face:** two dots for eyes, a brow line each, a slash mouth; `mouth` rest (a thin slab), `aa` (a trapezoid), `oh` (a square).
- **Controls:** the base set; the walk is `stride` with the arms opposed. A gentleman who runs, points or picks something up is built as a cut-out instead ([shapes-character](shapes-character.md#a-figure-that-runs-points-or-picks-up-build-it-as-a-cut-out)): the same wedges drawn as named SVG parts (a side view with joint markers, the forearm and hand as two pieces), and the catalogue `run`, `point` and `pick_up` drive it; the flat ink-and-offset look survives the build.

## Motion habits

- **Time is stepped by nesting**: the figure and foreground in a nested composition layer at `fps` 15 (twos; 12 under a 24 fps root),
  the clouds, sun and stars in another at `fps` 6 (fours). Plain keys inside; no time-floor expressions. A walker that
  travels under a moving camera keeps its root travel continuous, outside the held composition; only its poses hold (`picsart_scene_recipe scene-animation-reference`, held drawings: "Hold the pose, not the travel").
- A walk: arms and legs are groups with their `anchor` at the shoulder or hip and a rotation of about plus and
  minus 24 degrees in alternation; the body bobs a few pixels on each step. The sun wobbles a few degrees, stars
  pulse in scale.
- A pan is the backdrop sliding on fours; cuts between flat colour fields are hard.
- Cued layers use `timeMode: "layer"`.

## Type

A heavy display serif or slab for the title, about 64 px, rotated about minus 3 degrees and wobbling a degree
or two on fours (the title sits in the fours composition), ink on the mustard.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. A figure with a face acting, the only place coral appears.
2. Colour blocks fill the frame and none lines up with its outline.
3. The same off-register offset on every object.
4. Three or more movers on fours: clouds, stars, a sun, a bird, a car.
5. Shapes are angular; a curve is allowed only on a cloud or a sun.

## Build with the tools

One shape layer per object so the off-register copy travels with it. Draw back to front: blocks, sun, clouds,
stars, trees, ground, walker, title. Group by step rate into nested compositions, then validate and look at a
contact sheet across a full walk.

## Do / don't

- **Do** make the offset visible at phone size.
- **Don't** add gradients, soft shadows or a second outline weight.

## On a part sheet

The shapes character above is the route for this style; this note is only for a user who brings a generated sheet. When a character comes through the SVG part-sheet flow (the `character-rigging` skill), every arm and leg is two pieces, an upper and a lower, each its own group, overlapping at the elbow or knee. That is a rig requirement no style overrides: the builder refuses a sheet whose limb is one piece. Draw each limb as two round-cap strokes, upper and lower, of the same width and colour, overlapping at the joint, so the pair reads as one two-point limb.

## Originality guard

Design your own gentleman. It must not resemble a known 1950s studio's pink panther, spy-versus-spy duo,
bespectacled old man or other series lead, a known cartoon's hat, nose, walk or silhouette, or a studio card or
title-sequence layout. The off-register blocks and angular construction are the style; the cast is new.

## Proven on

The off-register walker scene (mustard field, boomerang clouds, atomic stars, a walking figure, a title).
