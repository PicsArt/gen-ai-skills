# Silkscreen

A two-or-three-ink screen print: flat inks overprint by multiply, each plate sits a few pixels off register
and jitters like a hand-pulled sheet, and the edges break up with grain. A gig poster that moves.

## Palette

Paper `#f3ead7`, pink `#f0508c`, blue `#2e6fd9`, yellow `#ffcc33`. **The hero colour is the yellow, reserved
for the moon disc**, the large first plate; pink and blue carry the owls, the sea and the type.

## The medium

- **Each ink is a plate**: every shape layer of one ink is set to the `multiply` blend, so where two plates
  cross a third colour appears with no extra drawing.
- A subject is drawn twice, once per ink, **off register**: the pink owl at its place and the blue owl 11 px
  right and 8 px down, so a blue edge shows. Each owl is a flat silhouette with two pale eye discs and a dark
  pupil in the plate's colour.
- **Grain** on every plate: a `gaussian_blur` of about 0.6 followed by `alpha_dissolve` (size 2, density 0.9,
  fixed seed, a different seed per plate) breaks the edge into a stipple (ink grain, not brushwork: keep the dissolve).
- A sun or moon plate behind, a wave band of thick wavy lines (stroke 10 px) scrolling, a title in two plates
  (blue offset 4 px from pink) and a sub-title on a paper band.

## Motion habits

- **Plates jitter**: the `wiggle` preset on each plate's position (about 2 px, `frequency` 4, a different
  `seed` per plate) so the registration breathes. Step the whole print on fours or twos by putting the plates in
  a nested `composition` with `fps` 6 or 15 (12 under a 24 fps root).
- The moon grows from 20 % to full over 0.8 s; the owls pop in with an ease-out scale, 0.2 s apart; owls rock a
  few degrees on alternate steps.
- The waves scroll sideways by one wave period and loop.
- Cued layers use `timeMode: "layer"`.

## Type

A condensed display face, two plates (blue under pink) with a small offset, upper case, typed on with a short
typewriter animation; the sub-title is smaller and in blue only.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Every plate is multiply on paper; none is a normal-blend fill.
2. Two inks of one subject are visibly off register.
3. Grain breaks every shape's edge.
4. No gradients; tone comes from overprint only.
5. The registration moves, but never by more than a few pixels.

## Build with the tools

Build each ink as shape layers with the `multiply` blend and the grain effects, apply `wiggle` with
`picsart_scene_apply_preset` to the plates, and nest them for the stepped rate. Put the paper band above the plates
that must not overprint it.

## Do / don't

- **Do** let the overprint colour happen where plates overlap.
- **Don't** add a third or fourth ink to every shape, a drop shadow, or a smooth blur; don't register the plates
  exactly.

## Originality guard

Draw your own owls and wording. They must not copy a known gig-poster artist's creature, a venue's or a band's
logo, or a famous screen-print's composition. The multiplied plates, the off register and the grain are the
style.

## Proven on

The silkscreen-night-owls film (a yellow moon, a scrolling blue sea, two off-register owls, a two-plate title,
a sub-title band).
