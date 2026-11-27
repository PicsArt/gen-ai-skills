# Pixel art

A pixel-art character hops across a scene in two eras: a four-shade handheld green look, then a sixteen-colour look
with finer pixels, joined by a circular iris. Every move is on twos and every pixel is a whole block.

## Finish

The whole scene on twos (`fps` 12 under a 24 fps root) with whole-pixel blocks and the circular iris between the eras (see Motion habits).

## Palette

**Era one uses four handheld greens**, darkest to lightest `#0f2a14`, `#2e8a4a`, `#8aac2a` and `#c4d870`, in the
style of a small monochrome screen; nothing else appears. The film's sixteen-colour era also draws on ink
`#14101e`, paper `#f4f0e6` and the accents yellow `#f6d64a` and orange `#f08a32`. **Era two uses sixteen colours** chosen once, shared by every sprite.
**The hero is the palette itself**: colour discipline is the style, so name your palette in a script once and
reuse its entries everywhere.

## The medium

- **Art is rasterised at a low resolution by a script and scaled by a whole number.** Era one is drawn at 90 by 160
  and scaled by 12, era two at 180 by 320 and scaled by 6, both filling the 1080 by 1920 frame. A nearest-neighbour
  raster is not available yet, so today the script writes each pixel as a filled square shape (or merges runs of
  the same colour into rectangles) at the scaled size; state this plainly, and switch to the raster when it lands.
- **Sprites** are small grids (16 by 16 or 24 by 24) held as strings or arrays in the script, one colour per cell.
- **Backgrounds** are a few flat bands and a repeating tile pattern.

## The character

Drawn from the style's own shapes, not a generated sheet (the mechanism, saving and talking are in [shapes-character](shapes-character.md)); build once, save once to the library, place it by its `uri` in every shot.

- **Proportions:** 16 pixels tall, 4 px head.
- **Shapes:** every part a `rect` on the whole-pixel grid; no part rotates, a pose is a different set of pixels (frames swapped by `step`).
- **Face:** two 1 px eyes; no mouth chart.
- **Controls:** the one control is `frame` (a step dial over the sprite's pose set: stand, step A, step B, hop); not proven in this style.

## Motion habits

- **On twos:** the whole scene sits in a nested composition at fps 12 so every key steps; the hop is five
  poses (crouch, rise, peak, fall, land) chosen by whole-frame position keys and a swapped sprite. A sprite that travels under a moving camera keeps its
  root travel continuous, outside the held composition; only its poses hold (`picsart_scene_recipe scene-animation-reference`, held drawings: "Hold the pose, not the travel").
- **Move by whole pixels:** position keys use multiples of the pixel size, so no sprite sits between pixels.
- **Parallax:** background bands scroll at different whole-pixel speeds.
- **The change of era:** a circular iris, a `mask.clip` circle shrinking to zero over the first era and growing in
  the second, hides the swap of palettes and resolution.
- Cued layers use `timeMode: "layer"`.

## Type

A pixel face exists: Press Start 2P (find it with `picsart_scene_fonts`, add its asset to the scene's `assets`);
set captions in it at a multiple of its 8 px grid, in the era's palette, or draw letter grids from the script.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Every pixel in an era is the same size.
2. Only the era's palette colours appear.
3. Sprites never sit between pixels.
4. The iris hides the era change completely.
5. The hop reads clearly on twos.

## Build with the tools

Write sprite grids and the palette in the script, emit merged rectangles per row of each colour, nest each era in
its own composition at fps 15, and join them with the iris. Verify a frame by counting distinct colours with
`picsart_scene_contact_sheet`.

## Do / don't

- **Do** keep silhouettes readable at three or four colours.
- **Don't** blend or smooth edges; no anti-aliasing and no half-pixel positions.

## Originality guard

Draw your own character and levels. They must not reproduce a known game's hero, enemies, level layout or music
motifs, or a console's boot screen. The limited palette, whole-pixel steps and twos timing are the style.

## Proven on

The robot-hop-pixel film (a robot hopping across a scene in a four-green era and a sixteen-colour era, on twos,
joined by an iris).
