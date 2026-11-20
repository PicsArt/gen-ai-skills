# Neon tubes

A brick wall at night with glass-tube signs: a pink cat outline, a cyan LATE NIGHT sign and an amber OPEN sign
buzz on at different moments, flicker, and a green chevron arrow chases beside them. Dark ground, hot light.

## Palette

Wall `#2a1d24` with bricks `#3a2830`, street `#141018` to `#0b090d`, ground `#1a1218`. Tubes: pink `#ff4fd8`,
cyan `#7febff`, amber `#ffc65a`, green `#7dff6a`. **The hero colour is the pink `#ff4fd8`, reserved for the
cat**; the other tubes support it. Every tube has a near-white `#ffffff` core.

## The medium

- **A tube is two strokes**: a thin white core (3 px) over a coloured tube (7-9 px) of the same path. Text
  tubes are an outline-only letter set (a transparent fill and an 8 px stroke in the tube colour).
- The **cat** is an original sitting outline with a curling tail and two short eye strokes, drawn as one open
  path in pink.
- **Glow:** every sign layer has the `glow` effect (threshold 20, radius about 56, intensity about 2.5-2.9).
  Behind each sign a **haze** layer repeats the path as a wide, low-opacity stroke blurred by 40 px, so the
  wall takes the colour.
- The **wall** is rows of rounded rectangles in a darker tone, half-offset on alternate rows.
- A **street** band at the bottom with a vertical gradient for the wet reflection.

## Motion habits

- **Buzz on:** each sign starts dark, stutters between 10 % and 100 % for about half a second, then holds with
  a rare dip. Use the `random_hold` preset on the sign's opacity (a different `seed` per sign) for the stutter,
  and start each sign later than the last (about 1 s apart); the haze layer takes the same preset with the same
  `seed`.
- The chevrons light in turn: three open "V" strokes, one at full opacity at a time, stepped on fours by
  nesting them in a `composition` with `fps` 6.
- Nothing else moves; the point is the light.
- Cued layers use `timeMode: "layer"`.

## Type

A tall condensed display face drawn as outline tubes only, in two or three colours; one short word each.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Every sign is a white core over a coloured tube with the same glow.
2. Each sign has a haze layer on the wall behind it.
3. Signs light at different moments and flicker differently.
4. The pink cat is the only pink.
5. The ground is dark enough that no sign is lost.

## Build with the tools

Build each sign's tube with two stroked copies of one path, add the `glow` effect to the layer and a blurred
haze layer behind. Apply `random_hold` to opacity with `picsart_scene_apply_preset`. Check the glow on a render.

## Do / don't

- **Do** let one sign flicker harder than the rest.
- **Don't** fill the lettering, or use one global glow for all signs; don't add a lit window or a spotlight.

## Originality guard

Draw your own cat and signs. They must not copy a real shop's or bar's neon, a known chain's logo, or a
famous neon artwork. The glass-tube core and glow, the buzz-on flicker and the brick night wall are the style.

## Proven on

The late-night-neon film (a brick wall, a pink neon cat, LATE NIGHT and OPEN signs buzzing on, a chasing
chevron arrow, a wet street).
