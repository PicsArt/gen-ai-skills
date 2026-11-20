# Pen plotter

An engraving drawn by a machine: a lit sphere and a cube made only of parallel hatch lines, tight where it is
dark and open where it is light, laid down pass by pass in one blue-black ink on cream paper.

## Palette

Paper `#f4efe3`, one ink `#1d2a44`. **No other colour is used; the hero is the ink itself**, and tone is only
the spacing and the crossing of lines.

## The medium

- **Hatch is a repeater.** One horizontal line (a two-point path) in a group with a `repeater` that offsets each
  copy by a gap (8-16 px), long enough to cover the shape when rotated. Stroke 1.6 px, ink.
- **Each pass is a layer, rotated to its angle and clipped to its area** by a `mask.clip` of shape content: the
  whole disc for the lightest pass at one angle, then a crescent facing away from the light for a second pass
  at a crossing angle and a tighter gap, then a smaller crescent for a third at yet another angle and a tighter
  gap still. The crescent is the intersection of two circles (a `merge` item in `intersect` mode).
- **The cube** is three faces, each hatched on its own: the top face open (16 px gap), the left face denser
  (9 px, vertical), the right face darkest (7 px, then crossed by a second pass at another angle).
- **Contours:** an outline stroke (2.2 px) of the sphere and the cube edges, drawn on with `trim` before the
  hatching, plus a ground line at the end.
- The plotter's order of work matters: outlines, light passes, dark passes, ground.

## Motion habits

- Everything is **drawn on**: each hatch pass's `trim` runs 0 to 1 in `parallel` mode over about a second, so
  all lines of the pass draw together as if a multi-pen plotter drew them, a pass starting as the last ends.
- The outlines draw first (0.6-1 s), the sphere's three passes next, then the cube's faces in order light to
  dark. The whole piece takes about eight seconds, then holds.
- No jitter: a plotter is exact. Do not add `wiggle` or `line_boil`.
- Cued layers use `timeMode: "layer"`.

## Type

Usually none. A caption, if needed, is a small monospaced or technical face in the same ink, set at one corner.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. One ink only; tone comes from spacing and crossing.
2. Hatch lines never leave their shape (they are clipped).
3. Darker tones have tighter gaps and a second angle.
4. The light direction is the same on the sphere and the cube.
5. The drawing is built outline-first, light-to-dark.

## Build with the tools

Build each hatch pass as a shape layer (a line plus `repeater`) with the clip as `mask.clip` shape content, the
rotation as the layer's transform, and a keyed `trim`. Keep one repeater per group. Check tone with
`picsart_scene_contact_sheet` at the end.

## Do / don't

- **Do** keep the gaps in simple ratios (16, 10, 8, 7) so the tones step cleanly.
- **Don't** add grey fills, gradients or a second ink; don't hatch outside the clip.

## Originality guard

Choose your own solids and light. It must not copy a famous engraving, a named plotter artist's piece, or a
recognisable logo made of hatch. The single ink, the clipped hatching and the pass-by-pass drawing are the
style.

## Proven on

The plotter-hatch film (a hatched sphere with three passes and a three-face cube, drawn outline-first, then
light to dark, then a ground line).
