# Continuous line

A whole drawing made of a single unbroken ink line: it draws a seated cat and a sun, holds and breathes, then
draws itself away. Calm, sparse, on warm paper.

## Finish

No finish: warm paper, no grain look and no stepped rate; the line drawing itself is the motion.

## Palette

Paper `#f6f1e7`, ink `#1f1d1a`. **The hero colour is the accent `#e2674a`, reserved for one closed loop of the
same line (the sun)** and used on nothing else.

## The medium

- The picture is **one path** of 25-35 vertices, smoothed by giving every vertex an `inTangent` and
  `outTangent` of a sixth of the distance between its neighbours (a Catmull-Rom curve). It starts off the left
  edge, runs along a baseline, climbs into the subject and leaves off the right edge, so the baseline and the
  subject are one stroke.
- Stroke 6 px, round caps and joins, ink. No fill anywhere: the drawing is outline only.
- Small features that cannot be on the line (an eye) are their own short stroke, drawn after the face and
  blinking.
- The accent is a second path, a loop of the same weight, as if the line had been lifted once.
- A caption, if any, is small lowercase and is written on under the drawing with `typewriter`.

## The character

Drawn from the style's own shapes, not a generated sheet (the mechanism, saving and talking are in [shapes-character](shapes-character.md)); build once, save once to the library, place it by its `uri` in every shot.

- **Proportions:** loose, about 5 heads tall, drawn in one stroke.
- **Shapes:** there are no parts: the figure is one continuous path drawn with `trim`; its limbs are loops of the same line.
- **Face:** two dots drawn as tiny loops of the line; no mouth chart.
- **Controls:** the one control is `draw` (the trim end, 0 to 1); the line wobbles on the beat, and the figure erases itself last.

## Motion habits

- **Drawn on, then drawn off.** Key the path's `trim`: `end` from 0 to 1 over about 3 s with an ease-in-out
  (`[0.45, 0, 0.25, 1]`), then, after a hold, `start` from 0 to 1 over 2 s to erase it in the same direction.
  The line never reverses.
- **Breathing in the hold** is a very small scale in y (about 1.2 %) on the whole path, anchored on the baseline,
  as two eased keys that alternate; the eye blinks twice with `scale` y keys dipping to 0.2.
- The accent loop draws on after the cat is drawn and leaves with it.
- Nothing else moves; no camera, no parallax.
- Cued layers use `timeMode: "layer"`.

## Type

One short lowercase line in a plain grotesque, set small and low, fading in after the drawing and out before
the erase.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. The subject is one path with no gaps and no fills.
2. The line's width is the same everywhere and the ends run off the frame.
3. Exactly one thing is in the accent colour.
4. It draws on, holds and breathes, then draws off.
5. More than half the frame is empty paper.

## Build with the tools

Author the path with smooth tangents and add a `trim` item after it in the same group, then the stroke. Key the
`trim` start and end as above. Check with `picsart_scene_contact_sheet` at three times (half drawn, held, half erased) to
see that the line is continuous.

## Do / don't

- **Do** let the line cross itself where the body needs it; one stroke may overlap.
- **Don't** lift the pen (a second path for the cat), add shading, or taper the stroke; tapering is a different
  style.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Line width under a zoom: no zoom, width fixed at 6 px everywhere (see The medium).
  - Arrivals: the caption, if any, is written on under the drawing with `typewriter` (no fade, no exception); the drawing arrives by `trim` end and leaves by `trim` start; there are no transitions, and a next drawing starts on blank paper.
  - A finish belongs to the page: the paper is flat with no tooth or grain, and there is no camera, so nothing needs anchoring.

## On a part sheet

The shapes character above is the route for this style; this note is only for a user who brings a generated sheet. When a character comes through the SVG part-sheet flow (the `character-rigging` skill), every arm and leg is two pieces, an upper and a lower, each its own group, overlapping at the elbow or knee. That is a rig requirement no style overrides: the builder refuses a sheet whose limb is one piece. Draw each limb as two overlapping pieces whose line continues across the joint with no break, so the figure still reads as one continuous line.

## Originality guard

Choose your own subject and invent its outline. It must not trace a famous artist's one-line animal or figure,
or a well-known logo drawn in one stroke. The single continuous stroke and the draw-on are the style.

## Proven on

The one-line cat film (a seated cat and a sun in one line, a blinking eye, a held breath, a draw-off).

**Not proven:** the written-on arrival was shown on a plain page with one label, not beside the single-line cat.