# Stained glass

A circular window of jewel-coloured panes between heavy black lead, lit one ring at a time from the centre
while coloured beams fall on the stone below and a glare slides across the glass.

## Finish

No finish beyond the lit window (beams and glare); no stepped rate and no film look.

## Palette

Lead `#141218`, rim `#5d5466`, stone `#3a3442` to `#121016` (radial). Jewels: red `#b3122e`, blue `#1f4fa8`,
amber `#e2a21b`, green `#1d8a4e`, violet `#6a3fa0`; roundels and the core `#fff1c4`. **The hero colour is the
pale light `#fff1c4`, reserved for the star at the core and the roundels** so the window has a bright heart; the
jewels are the palette and each pane is one of them.

## The medium

- The window is a **radial** build in one group: a star at the centre, a disc of amber, eight petal wedges, then
  sixteen narrower wedges in two rings, each wedge a closed path (a ring segment) with a **flat jewel fill and a
  8-9 px lead stroke**. A round-cap lead ring at the rim (22 px) and a thinner stone ring outside it close the
  window.
- Petals carry a small pale roundel inset; the two outer rings alternate two jewels so neighbours differ.
- The ground is a radial stone gradient, lighter at the window's centre.
- **Beams** are five tall translucent quads in the jewel colours at about 30 % opacity, fanning from the window
  to the bottom of the frame.
- **Glare** is a soft white band (a gradient fill with alpha stops 0, 0.35, 0) tilted 20 degrees, clipped to the
  window by a `mask.clip` with a circle.

## The character

Drawn from the style's own shapes, not a generated sheet (the mechanism, saving and talking are in [shapes-character](shapes-character.md)); build once, save once to the library, place it by its `uri` in every shot.

- **Proportions:** about 5 heads tall, in panes.
- **Shapes:** every part a coloured polygon pane between thick black lead lines (stroke 8), the head a rounded pane, the robe one tall pane.
- **Face:** a face is two small black panes and one lead stroke; no mouth chart, so no talking.
- **Controls:** drop `mouth`; `headTurn` and `spineLean` are slow, a few degrees.

## Motion habits

- **Light up from the centre out.** Each pane's opacity keys from about 0.22 to 1 over 0.7 s with an ease in
  and out, starting later the further it is from the middle (about 0.07-0.1 s per step round a ring, 0.5 s per
  ring). Never light everything at once.
- The beams fade in after the window is lit; the glare then slides across the glass with an ease in and out over
  about 3 s and leaves.
- A very slow `wiggle` on the beams' opacity (small amount) lets the light breathe. Everything else holds still:
  glass does not move.
- Cued layers use `timeMode: "layer"`.

## Type

Usually none; a title is a spaced capital serif in `#fff1c4` on the stone below the window.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Every pane is one flat jewel with a lead line; no pane is shaded.
2. The lead is the darkest thing and is the same weight within a ring.
3. Neighbouring panes never share a jewel.
4. The window lights from the centre out; the glare crosses once.
5. The beams and the glare stay clear of the window's edge ring.

## Build with the tools

Generate the wedge paths in a script (polar to points) and add each to the window group; key each wedge's
`opacity` with the delays above. Add the glare as its own layer with a `mask.clip` of shape content. Use
`picsart_scene_contact_sheet` at early, middle and late times to check the order of lighting.

## Do / don't

- **Do** keep the lead consistent so the window reads as one object.
- **Don't** put gradients inside the panes (they read as plastic) or animate the lead.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - **Rate split.** as in Finish: nothing steps; the beams, glare and lighting all run at the root rate.
  - **Stop time.** optional on the key beat (the last ring lit): the window group keeps its keys in a nested composition that ends at that time while the beams and glare keep theirs, so the glare crosses a still window.

## Originality guard

Design your own pattern of panes. It must not copy a real cathedral's named window, a known rose window's
tracery, or a saint's figure from one. Keep the radial symmetry, the lead and the jewel set; change the count
and the shapes.

## Proven on

The rose-window film (a centre-out lighting, five coloured beams, a sweeping glare, in a 1280 x 720 frame).
