# Isometric town

A picture-book town seen from a fixed isometric angle: tiles fade in, small blocks rise from the ground back to
front, trees pop up, and a car loops the ring road.

## Palette

Grass `#9fd27f` and `#94c974` in a checker, road `#c9c1b3`, trees `#3f9a52` over trunks `#7a5233`. Each building
has a light top, a mid left face and a dark right face of one hue: yellow (`#ffd27a`, `#e8a33c`, `#c9822a`), blue
(`#9ad0ff`, `#5a9ad6`, `#3d78b3`), pink, violet and white. **The hero colour is the car's red-orange `#ff5a3c`,
reserved for the one moving thing.**

## The medium

- **A grid, projected.** Choose a grid (eight by eight) and a projection in a script: a cell (gx, gy) at height z
  maps to x = ox + (gx - gy) * s, y = oy + (gx + gy) * s * 0.5 - z. Ground tiles are diamonds from this
  mapping; a ring road is the tiles along columns 1 and 6 and rows 1 and 6.
- **A block is three faces**: a top diamond and two side parallelograms, each a flat fill of its hue's three
  tones, no outline. Heights vary (60-170 px).
- **Draw order is depth.** Sort buildings by gx + gy ascending (back first) and give each layer a `z` equal to
  gx + gy plus its size, so layers never swap places under a camera or a rotation.
- Trees are a green ellipse over a short brown trunk; the car is a small rounded rectangle.

## Motion habits

- **Rise from the ground:** each block's `scale` y keys from 0 to 1 with an overshoot (`[0.3, 1.45, 0.5, 1]`)
  anchored at its base, starting 0.45 s after the last, back to front; trees pop in with the same easing at the
  corners, 0.15 s apart.
- **The car** follows the ring: position keys at the four corners, 1.1 s a side with a constant pace, and its
  `z` keyed so it passes in front of or behind buildings as the diagonal changes. Make its rotation follow
  its heading.
- Hold the rest still; the town is a diorama.
- Cued layers use `timeMode: "layer"`.

## Type

Usually none; a small sans title in the corner at most.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. One projection for everything, with edges at 2:1 slopes.
2. Every block has three tones of one hue and no outline.
3. Layers' `z` follow depth so nothing draws in the wrong order.
4. Blocks rise back to front.
5. The car is the only warm accent.

## Build with the tools

Compute vertex positions in a script from the projection; one shape layer per block with `anchor` at its base,
and a `z`; keys as above. Do not leave two layers at exactly the same `z` in 2.5D: see the coplanar line in the
pop-up recipe.

## Do / don't

- **Do** keep the tops lighter than the sides, left lighter than right.
- **Don't** mix a perspective camera with this projection or outline the blocks.

## Originality guard

Plan your own town. It must not copy a known isometric game's buildings, a city-builder's tile set or a named
artist's pixel town. The fixed projection, three-tone blocks and rising build are the style.

## Proven on

The iso-town film (an eight-by-eight ground, five blocks rising back to front, trees popping, a car on the ring
road).
