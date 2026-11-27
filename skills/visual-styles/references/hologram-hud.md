# Hologram HUD

A cyan scanning display: a wireframe object turns in the middle, a scan line sweeps up it, bracketed readouts
appear with thin leader lines, and the whole thing flickers like a projection.

## Palette

Deep blue-black `#030b14`, cyan `#5ff3ff` as the single line colour at several opacities (100 %, 60 %, 25 %),
white-hot core `#e8fdff`. **The hero colour is the hologram cyan `#5ff3ff`**; warnings, if any, are one amber
`#ffb347` used once.

## The medium

- **The object** is a wireframe: stroke-only paths in cyan, 2 px, no fills; a faint fill at 8 % cyan helps volume.
- **The scan line:** a horizontal band with a gradient fill (cyan, 0 to 60 % to 0 alpha) that moves up the object.
- **Brackets and readouts:** corner brackets around the object, small mono text, a hairline leader to each.
- **A ground ring:** an ellipse under the object, 2 px, with ticks around it.
- A subtle **scanline pattern** (horizontal lines at 4 % opacity) over the frame.

## Motion habits

- **Turn the object** with the composition camera or layer `rotationY` keys looping (`ctx:loopOut("cycle")`), slow,
  one turn in about 8 s.
- **Scan:** the band moves bottom to top in 1.4 s; wireframe segments brighten as it passes (a brighter copy of
  the paths clipped to the band with `mask.clip`).
- **Readouts:** brackets draw with `trim` (0.3 s), text types or fades in, values step on whole frames.
- **Flicker:** the `wiggle` preset on opacity and a tiny x offset, plus `random_hold` for occasional dropped frames.
- Cued layers use `timeMode: "layer"`.

## Type

Cutive Mono in cyan, small and capitalised; one size for all readouts.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Everything is the one cyan at different opacities.
2. The scan band only brightens the object.
3. Readouts do not cross the object.
4. Flicker is brief and never hides the object for more than two frames.
5. The ground ring stays flat while the object turns.

## Build with the tools

Build the wireframe as path layers; for the turn use `rotationY` on a layer group in a 3D-space composition or
fake it by scaling x of a symmetrical wireframe; add `glow` to the lines. Check legibility on a still.

## Do / don't

- **Do** keep readouts few and short.
- **Don't** copy a film's fictional interface, a known game HUD or its icon set.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - **Line width.** no zoom, the 2 px lines stay fixed; if a push-in is added, one shared parameter drives zoom and stroke width (constant on screen), and small readouts take an opacity keyed to it.
  - **True data.** each readout is computed from the numbers that move the picture (turn angle, scan height) with a text expression; invented values are tagged SIM in frame; the object is labelled schematic; counts add up.

## Originality guard

Invent your own object and data. It must not reproduce a named film's interface graphics, a game's HUD or a
company's sci-fi brand kit. The cyan wireframe, scan band and bracketed readouts are generic conventions.

## Proven on

The holo-hud-scan film (a cyan wireframe object turning, a scan band, bracketed readouts with leaders, a
flickering projection).
