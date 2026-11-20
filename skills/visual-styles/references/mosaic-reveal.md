# Mosaic reveal

A picture assembled from a grid of colour tiles: tiles pop in as a ripple spreading from a point, settle into the
image and then flip to show the finished picture. Warm, cheerful, graphic.

## Palette

Tiles drawn from a small set sampled from the picture: sky `#7ec8e3`, sea `#2a7fba`, sand `#f6e2b3`, hill
`#e9a15c`, shadow `#8c5a3c`. **The hero colour is the sun yellow `#ffd166`, reserved for the sun tiles** at the
ripple's origin.

## The medium

- **A grid** of square tiles (24 by 36 on a portrait frame), each a rounded square with a 2 px gap, flat colour
  chosen from the picture by a script that samples the source at the tile's centre.
- **Tile layers** are kept cheap: one shape layer per row with a repeater is not possible (copy index is a gap
  today), so build one layer per tile in a script, or one layer per colour group.
- **The final picture** sits under the tiles at full resolution and is revealed as they flip.

## Motion habits

- **Ripple:** each tile's start time is its distance from the origin times 0.025 s, so a ring of tiles pops in at
  the same time. Compute it in the script and write it as a `start`.
- **Pop:** `scale` keys `[0, 1.25, 0.95, 1]` over 0.35 s with an ease-out and the tile's opacity from 0 to 1.
- **Flip to the picture:** after all tiles have landed, each flips (scale x to 0 and back) in the same ripple
  order, fading to the full-resolution picture beneath.
- **Hold** on the finished picture for a full second.
- Cued layers use `timeMode: "layer"`.

## Type

Usually none; an optional single line of lettering below the picture.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Tiles sit on an exact grid with equal gaps.
2. The ripple's origin is clear and the rings are even.
3. Tile colours come from the picture, not guessed.
4. The final picture shows no tile edges.
5. Yellow appears only near the origin.

## Build with the tools

Sample the picture and write one layer per tile (or per colour group) with the ripple start times; run a
validation to keep the layer count reasonable; verify the final frame against the source picture with
`picsart_scene_contact_sheet`.

## Do / don't

- **Do** keep the grid coarse enough that tiles read at phone size.
- **Don't** use a photo of a real person or a trademarked artwork.

## Originality guard

Use your own picture. It must not reproduce a famous mosaic, a brand's tile mark or a known viral reveal. The
sampled-tile grid, ripple pop and flip to the picture are the style.

## Proven on

The mosaic-ripple-reveal film (a grid of sampled colour tiles popping in a ripple from a sun, then flipping to
reveal the finished picture).
