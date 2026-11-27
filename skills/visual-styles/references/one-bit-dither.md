# One-bit dither

A shaded night harbour crushed to two colours: soft gradients are drawn first, then an adjustment chain turns
every pixel black or white through noise, so the shading becomes a dither pattern. A lighthouse beam sweeps over
a bobbing boat.

## Palette

Black and white only, after the chain. Before it, the picture is drawn in greys from `#050505` to `#ffffff`.
**No hue is used. The hero is the white of the moon and the beam**, the two lightest things in the frame.

## The medium

- **Draw in grey, finish in two.** The scene is ordinary shape layers with gradient fills: a sky from `#101010`
  to `#8a8a8a`, a sea from `#5a5a5a` down to `#0a0a0a`, a moon (a radial glow plus a solid disc), a rock, a
  tower with a lighter lit side and a lamp room, a boat with a lit sail and a mid-grey hull, a few glint
  stripes under the moon.
- **The beam** is a long triangle with a white-to-clear gradient in `screen` blend, anchored at the lamp.
- **The two-ink pass** is one adjustment layer over everything with three effects in order: `black_white`, a
  `noise` (about 60, fixed seed), then `levels` with `inputBlack` 0.49 and `inputWhite` 0.51. The noise decides
  which side of the threshold each pixel falls on, so a mid grey becomes a scatter of dots and the picture
  dithers.
- Fixed seed, so the dither does not crawl between frames unless you want it to.

## Motion habits

- The beam **turns**: key the beam layer's x scale along a cosine (as keyed values from 1 to -1 and back), so it
  sweeps past the viewer as a lamp would. The boat bobs (a keyed y loop of 6 px) and rocks 3 degrees; the glint
  stripes drift sideways a few pixels on keyed loops.
- Put the moving parts in a nested `composition` with `fps` 15 (12 under a 24 fps root) for a stepped look, and use the `wiggle`
  preset on the stripes at a small amount.
- Cued layers use `timeMode: "layer"`.

## Type

Usually none. If a title is needed, set it as white on a dark area before the adjustment layer so the dither
treats it like everything else, in a heavy face large enough to survive the threshold.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. The final frame has only two colours.
2. The adjustment layer is the topmost layer and covers the frame.
3. Shading under it comes from gradients, never from texture assets.
4. Detail is large enough to read after dithering (nothing under about 6 px).
5. The beam is the brightest element and crosses the boat.

## Build with the tools

Draw the grey picture first and check it, then add the adjustment layer with the three effects in that order.
Verify with a render (`picsart_scene_contact_sheet`) that only the two colours remain.

## Do / don't

- **Do** use soft gradients; the dither is only as good as the grey it starts from.
- **Don't** use a colour layer under the chain, or a threshold narrower than the noise; don't add outlines.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Print family: one plate, black ink on white: no registration offset, halo or overprint; the `noise` keeps `seedMode` fixed (as above) so the dots do not crawl.

## Originality guard

Compose your own harbour and tower. It must not copy a known one-bit game's art, a named photographer's
lighthouse, or a recognisable real lighthouse's shape. The two-colour dithered shading is the style.

## Proven on

The harbour-one-bit film (a shaded night harbour: moon, sea, rock, lighthouse with a turning beam, a bobbing
boat, all crushed to black and white).
