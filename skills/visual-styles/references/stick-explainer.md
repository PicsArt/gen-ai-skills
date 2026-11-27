# Whiteboard explainer

A hand-drawn whiteboard explainer: a stick figure walks in, has an idea, and an arrow and a growing chart draw
themselves on before the figure jumps for joy. Plain lines, one accent, a short line of caption. (For stick figures acting a story on a coloured ground, with
no drawing-on, use [stick figure](stick-figure.md).)

## Finish

No finish: ink lines on paper at the scene's own rate; the draw-on is the motion.

## Palette

Paper `#fbfbf7`, ink `#1b1b1b`, chart bars `#d9e8ff`, bulb and star `#ffe066`. **The hero colour is the accent
`#ff6b3d`, reserved for the idea's rays and the rising line**, the two things the viewer should follow.

## The medium

- **Everything is an ink line of one weight** (6 px, round caps) on paper; the only fills are pale, flat and
  few (the bulb, the bars, a star).
- The figure is a circle head (r 30, paper fill, ink outline), a straight body, two arms and two legs, each limb
  a stroke in its own group pivoted at the shoulder or hip so it can swing. No face.
- The ground is a single horizontal line drawn first.
- **Charts are drawn, not shown:** axes are an open two-segment path, the rising line a polyline in the accent,
  and bars are rounded rectangles with an ink outline growing from the baseline.
- An idea is a bulb (ellipse and a base of two short strokes) with five short accent rays.
- An arrow is a curved stroke with a separate chevron head that appears when the shaft finishes.
- A caption is one lowercase line in a bold grotesque at the foot of the frame.

## The character

Drawn from the style's own shapes, not a generated sheet (the mechanism, saving and talking are in [shapes-character](shapes-character.md)); build once, save once to the library, place it by its `uri` in every shot.

- **Proportions:** about 5 heads tall to the circle, drawn in marker.
- **Shapes:** a circle head, stroke body and limbs in the marker colour on the board, a round-cap line of one width.
- **Face:** two dots and one curved mouth stroke; `mouth` rest (a thin slab), `aa`, `oh`.
- **Controls:** the base set; arm dials point at the chart and the lean leans in.

## Motion habits

- **Draw on with `trim`:** key `end` from 0 to 1 on each line with an ease-in-out (`[0.45, 0, 0.25, 1]`). Order
  them so the story reads: the ground, the arrow, the axes, the bars, then the accent line.
- **Pops** use scale from 0 with an overshoot easing (`[0.3, 1.6, 0.5, 1]`): the bulb, each bar (scale y only,
  anchored on the baseline, 0.15 s apart) and the star at the peak.
- The figure walks with alternating keyed rotations on the limb groups and a small bob on the body, stops
  while the idea appears, and jumps with the arms thrown up (limb rotation keys and one arc in position).
- Hold the pose between beats; a stick figure needs stillness to read.
- Cued layers use `timeMode: "layer"`.

## Type

One lowercase caption in a bold grotesque, ink, fading in at the end. No other text.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. One line weight; round caps on every stroke.
2. The accent is on the rays and the rising line only.
3. At least two things draw on and at least two things pop.
4. The figure has a clear setup, an idea beat and a reaction beat.
5. The message could be read with the sound off.

## Build with the tools

Build the figure as one layer of limb groups and animate the groups' rotation; add `trim` to each drawn path
and key it; use the pop easing on bars and bulb. Use `picsart_scene_contact_sheet` at the end of the draw-ons to check
that the chart reads.

## Do / don't

- **Do** let each drawn line start where the last one ended so the eye is led along.
- **Don't** add faces, gradients or shadows; don't draw everything on at once.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Line width: no zoom, the 6 px line stays fixed.
  - Arrivals: the closing caption is written on with `typewriter` (nothing fades); lines draw on with `trim`, the bulb, bars and star pop by scale, the figure walks in; the only transition is a hard cut.

## On a part sheet

The shapes character above is the route for this style; this note is only for a user who brings a generated sheet. When a character comes through the SVG part-sheet flow (the `character-rigging` skill), every arm and leg is two pieces, an upper and a lower, each its own group, overlapping at the elbow or knee. That is a rig requirement no style overrides: the builder refuses a sheet whose limb is one piece. Draw each limb as two ink strokes, upper and lower, of the same width with round caps, overlapping at the elbow or knee, so the joint reads as one bent stroke.

## Originality guard

Draw your own figure and your own idea. It must not copy a known explainer channel's character, its logo or
its hand, or a famous chart. The plain line, the draw-on and one accent are the style.

## Proven on

The idea-stick film (a figure walks in, a bulb pops, an arrow and a chart draw on, a star pops at the peak, the
figure jumps, a caption is written on).

**Not proven:** the written-on arrival was shown on a plain page with one label, not under the walking figure and the chart.
