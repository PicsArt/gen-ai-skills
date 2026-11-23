# Goo blobs

A lava-lamp of white blobs on black that merge and split like liquid: they are blurred and then thresholded,
so touching circles fuse into one skin, and a gradient tints the whole thing from gold to hot pink inside a
glass outline.

## Palette

Black ground, white blobs, gradient tint `#ffd23f` to `#ff3d6e`, glass outline `#3a3550`. **The hero colour is
the hot pink end of the tint `#ff3d6e`**; the gold above it is the supporting colour, and the glass is the
dark counterweight.

## The medium

- **Blobs:** nine white circles, radii 60-120, scattered in a narrow column near the centre of the frame, each
  its own shape layer with a seeded start phase.
- **The goo pass:** one adjustment layer over the blobs with `gaussian_blur` (about 28) then `levels` with
  `inputBlack` 0.45 and `inputWhite` 0.55. The blur makes neighbouring circles bleed together; the narrow
  levels window turns the blur back into a hard edge, so a close pair becomes one blob with a neck.
- **Tint:** a full-frame rectangle with a vertical gradient (gold top, hot pink bottom) in the `multiply` blend,
  above the goo pass, which colours only the white.
- **Glass:** a tall rounded rectangle outline (about 420 by 680, radius 190, 6 px stroke) over everything.
- The trick needs **white on black**: the threshold reads brightness. Over a photograph or a coloured ground it
  does not work yet, so keep the ground black.

## Motion habits

- Each blob rises and falls on its own: **vertical position keys** (a slow ease in and out over 4-8 s) with a
  different period per blob, plus a gentle sideways sway (about 20 px). Different periods mean the pattern never
  repeats within a short clip; to make a loop, give the periods a common multiple.
- Apply the `wiggle` preset at a very low frequency to the blobs' positions for the slow organic drift.
- Cued layers use `timeMode: "layer"`.

## Type

Usually none; if used, set it as white on the black before the goo pass (it melts with the blobs) or above the
tint (it stays crisp), never both.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Black ground, white blobs, goo pass above them.
2. The levels window is narrow (about 0.1 wide).
3. A gradient tint in `multiply` above the pass.
4. Blobs meet and part at least three times in the shot.
5. The glass shape contains all the action.

## Build with the tools

Make the blobs as layers with position keys, add the adjustment layer with `gaussian_blur` then `levels` above
them, then the tint and the glass. Check with `picsart_scene_contact_sheet` that blobs actually merge.

## Do / don't

- **Do** tune blur and the levels window together; widening one needs the other.
- **Don't** put coloured shapes under the goo pass or use a non-black ground.

## Originality guard

Choose your own vessel and palette. It must not copy a known lava lamp's product shape, a brand's gooey logo, or
a named music video's visuals. The blur-and-threshold fusion is the style.

## Proven on

The gooey-lava-lamp film (nine white blobs merging in a glass, a gold-to-pink tint, a long loop).
