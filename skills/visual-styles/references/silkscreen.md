# Silkscreen

A two-or-three-ink screen print: opaque flat inks, each pulled over the last so a later ink covers an earlier one,
each plate a few pixels off register (so a thin edge of the ink beneath shows), hard clean edges, paper flat. A
gig poster that moves.

## Palette

Paper `#f3ead7`, pink `#f0508c`, blue `#2e6fd9`, yellow `#ffcc33`. **The hero colour is the yellow, reserved
for the moon disc**, the large first plate; pink and blue carry the owls, the sea and the type.

## The medium

- **Each ink is a plate, and an ink is opaque**: every shape layer is `normal` blend, drawn in plate order (yellow
  moon first, then blue, then pink on top). Every full-width plate (stripes, bands, the paper) overscans the frame by well over the kick distance (ours: stripes 1200 px wide on a 1080 px frame, so a 12 px slip with rounded ends still never shows paper or a cap at an edge). Where two plates cross, the later ink covers the earlier one; no third
  colour appears. A faint multiply ghost of the beneath ink is allowed at most (ours 0.15 opacity, tune by render) and is not needed.
- A subject is drawn twice, once per ink, **off register**: the pink owl at its place and the blue owl 11 px
  right and 8 px down, so a blue edge shows. Each owl is a flat silhouette with two pale eye discs and a dark
  pupil in the plate's colour.
- **Hard edges**: no blur and no stipple on any plate; a silkscreen edge is crisp. Texture, if any, is one fixed
  `noise` on the paper (ours low, tune by render), not a per-plate speckle.
- A sun or moon plate behind, a wave band of thick wavy lines (stroke 10 px) scrolling, a title in two plates
  (blue offset 4 px from pink) and a sub-title on a paper band.

## Motion habits

- **Registration is fixed per shot**: the blue plate sits at a constant offset from the pink (owls (11, 8) px,
  title (4, 4) px). It moves only as an event: a slip of about (12, 7) px that settles back over 0.45 s on a beat (ours,
  tune by render). Never a per-frame wiggle. Step the drawn pieces on twos by putting the plates in a nested `composition`
  with `fps` 12 (under a 24 fps root).
- The moon grows from 20 % to full over 0.8 s; the owls pop in with an ease-out scale, 0.2 s apart; owls rock a
  few degrees on alternate steps.
- The waves scroll sideways by one wave period and loop.
- Cued layers use `timeMode: "layer"`.

## Type

A condensed display face, two plates (blue under pink) with a small offset, upper case, typed on with a short
typewriter animation; the sub-title is smaller and in blue only.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Every ink is an opaque normal-blend fill; a later ink covers an earlier one.
2. Two inks of one subject are visibly off register, by a fixed amount.
3. Edges are hard; no grain breaks a shape.
4. No gradients; no overprint colours.
5. The registration moves only on an event, by a few pixels, and settles back.

## Build with the tools

Build each ink as shape layers at normal blend, in plate order, key the blue plates' `position` (a constant offset and one decaying slip),
and nest them at `fps` 12. Put the paper band above the plates that must be clean under the sub-title.

## Do / don't

- **Do** let the later ink cover the earlier one, and leave the thin off-register edge showing.
- **Don't** add a third or fourth ink to every shape, a drop shadow, a blur or a stipple; don't register the plates
  exactly, and don't jitter them.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Nothing fades: a plate arrives by the moon's growth, the owls' scale pop, the typewriter title and the scrolling waves above; no opacity ramps; between beats only a hard cut or a squeegee wipe (a `mask` edge at the root rate).
  - Print family: opaque inks (a later ink covers an earlier one, no multiply); the fixed offsets above are the registration, kicked only on an event; the knockout is the paper band under the sub-title; hard edges, no dots, screens or stipple on this poster.
  - Finish: paper flat, with at most one fixed `noise`; no film look and no camera, so nothing needs anchoring to a pan.

## Originality guard

Draw your own owls and wording. They must not copy a known gig-poster artist's creature, a venue's or a band's
logo, or a famous screen-print's composition. The opaque plates, the fixed off register and the hard edges are the
style.

## Proven on

The silkscreen-night-owls film (a yellow moon, a scrolling blue sea, two off-register owls, a two-plate title,
a sub-title band). The opaque plates, hard edges and fixed registration with its slip were also rendered on a 3 s test poster (1080 by 1350).
