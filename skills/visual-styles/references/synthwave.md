# Synthwave

An eighties night-drive poster in motion: a violet-to-magenta sky, a striped sun on the horizon, neon wire
mountains, a perspective grid rolling toward the viewer, and a chrome title.

## Palette

Sky gradient `#0b0326` to `#3a0b5e` to `#b0246a` at the horizon; ground `#2a0845` to `#0b0326`. Sun gradient
`#ffe45e` to `#ff7b54` to `#ff3cac`, its bands `#5a1270`. Neon pink `#ff3cac` for the grid, neon cyan `#2de2e6`
for the mountain ridges and the subtitle, a pale pink `#ff9ad5` horizon line. **The hero colour is the sun's warm
yellow**; nothing else in the frame is yellow.

## The medium

- **Neon is two strokes:** a thin bright stroke over a wide faint one (`opacity` about 0.18, five times the width)
  of the same colour. First listed draws on top, so list the thin stroke first.
- **The sun** is a disc with a vertical linear `gradientFill`, half sunk below the horizon. Its **bands** are thin
  rectangles in a deep violet, each as wide as the sun's chord at its height
  (`2·sqrt(R² − dy²)`) so nothing sticks out past the disc, thickening toward the horizon.
- **Mountains** are filled dark silhouettes with a neon ridge drawn as an open path along their top.
- **The grid**: vertical lines are fixed paths from the vanishing point to the bottom edge; horizontal lines are
  one layer each at depth `z`, drawn at `y = horizon + k / z`.
- **Chrome title.** The face is metal: a shape layer with a vertical linear `gradientFill` (white at the top, pale
  steel blue to the middle, then a hard dark violet line just under the middle, a warm orange to cream at the
  bottom). It is seen through the word, which is its `mask` (`mask.clip` holding the same text). Write two
  stops a hundredth apart to make the horizon line hard. The mask clip sits in the parent's space, so give it the
  title's position and the same scale keys as the face. Under the face sit a pink copy of the word blurred for
  the neon glow, the cyan and pink copies nudged left and right, and a dark shadow offset down and right.

## Motion habits

- **The grid rolls toward the viewer:** each horizontal line's `z = i + 1 − (time·speed % 1)`, so lines are
  born at the horizon and leave at the bottom on a seamless loop; fade each in over its first few depths.
- **The sun's bands drift down** and thicken as they near the horizon, looped the same way.
- **The title** drops in once: scale `1.2 → 1` with opacity `0 → 1` over 0.6 s (`ease_out`); the subtitle
  flickers like a failing tube (`floor(time·6) % 7 == 0` dims it).
- The camera holds. The world moves.

## Type

A tall condensed display face (`bebas-neue-regular`) for the chrome title, about 120 px at 1280 wide; the
subtitle in the same face in neon cyan, away from the sun so it reads.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Every line on the ground and ridge glows: a bright core and a faint wide halo. The title reads as metal, with
   a hard horizon line through its letters.
2. The sun's bands never extend past its disc.
3. The grid moves toward the viewer in every frame, with no jump at the loop.
4. Yellow appears in the sun only.
5. Type sits on the sky, never on the bright sun.

## Build with the tools

Build sky, sun, bands, mountains, ground and grid as shape layers with position and scale expressions; the title is
a gradient face masked by the word over stacked text layers. No images are needed.

## Do / don't

- **Do** keep the camera still and let the grid and the bands carry the motion.
- **Don't** add photographic textures or a second hot colour; don't put type over the sun.

## Originality guard

Invent the title and any vehicle or skyline. Never copy a known album cover, film poster, game title screen or
logo, and never name one in a prompt. The striped sun, the neon grid and the chrome type are the style.

## Proven on

A night-drive title card (8 s): a striped sun, neon mountains, a grid rolling toward the viewer, and a chrome
title with a flickering subtitle.
