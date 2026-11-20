# Deco title

A 1920s-30s grand title card: gold sunburst rays fan open behind an arch, a stepped double frame draws itself
round the edge, chevrons cascade down both sides and a widely spaced title tracks in under a gold shimmer.

## Palette

Navy `#0e1b2c`, gold `#e9c46a` and deep gold `#b8862f`, pale gold highlight `#fff1c1`. **The hero colour is the
gold, reserved for line work, rays and the title**; navy is the only ground. Rays use gold at about 30 % opacity,
alternating the two golds.

## The medium

- **Sunburst:** fifteen narrow triangles fanning from the bottom centre (12 degrees apart, from -84 to +84),
  each its own shape layer anchored at the apex so it can rotate open.
- **Arch:** two concentric circles at the fan's centre, a navy-filled one outlined in gold (6 px) and a thin
  inner ring (2 px).
- **Stepped frame:** a closed path with ziggurat corners (steps of 22 px, then 18 px for the inner frame), one
  at 4 px and one at 1.5 px, both in gold.
- **Chevrons:** five gold open "V" strokes (6 px) down each side.
- **Title:** a tall condensed display face in gold, centred, with wide letter spacing; a one-line sub-title in
  the same face, smaller.
- **Shimmer:** a narrow tilted white-gold bar in `add` blend, clipped by a `mask.clip` to the title's own text
  so it only shows on the letters.

## Motion habits

- Rays **fan open**: each rotates from 0 to its angle over 1.2 s with an ease in and out while fading in. The
  frame lines **draw on** with a keyed `trim`, the outer first, the inner 0.3 s later.
- Chevrons drop in 20 px and fade, 0.12 s apart. The title's letter spacing tightens from 60 to 14 over 1.4 s
  while it fades in, then the shimmer crosses it every three seconds.
- Hold everything else still; deco is symmetrical and stately.
- Cued layers use `timeMode: "layer"`.

## Type

A tall condensed display face in gold, upper case, spaced wide; the sub-title is the same face with dot
separators.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Perfect bilateral symmetry about the vertical centre.
2. Gold on navy only; the highlight is the one pale tone.
3. A frame with stepped corners encloses the whole card.
4. The title's tracking settles to a fixed value.
5. The shimmer is clipped to the letters.

## Build with the tools

Generate the ray, frame and chevron coordinates in a script and add each as a shape layer with its keys. Key
the text's `letterSpacing`. Add the shimmer as its own layer with `mask.clip` content set to the same text.

## Do / don't

- **Do** let rays run behind the frame so the frame crosses them.
- **Don't** add a third metal colour, a lens flare or a drop shadow.

## Originality guard

Choose your own name, date and crest. It must not copy a real hotel's, cinema's or studio's logo or title card.
The sunburst, stepped frame, chevrons and gold-on-navy are the style.

## Proven on

The grand-hotel-deco film (a fifteen-ray sunburst, an arch, a stepped double frame, side chevrons, a tracking
title with a shimmer).
