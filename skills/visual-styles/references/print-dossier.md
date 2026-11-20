# Print dossier

One printed sheet of archive paper. Tone comes only from the size of the dots, with no smooth shading; one dark ink and
up to three spot inks overprint on cream; the sheet carries the furniture of a filing system (a reference number, labelled
tabs, an official stamp, corner marks), and everything arrives by landing on the page with a little overshoot. It is a printed file, not a poster
(no single big picture) and not a comic (no panels).

## Palette and colour roles

| Role | Colour | Its one job |
|---|---|---|
| ground | `#ebe1c9` | the paper, under every plate |
| ink | `#1e1b2c` | the dark plate: type, outlines, the dot shading |
| field | `#2b8f8c` (teal) | tabs and chips, the headline's offset second print and a second shading plate; overprints the ink |
| field | `#f2b632` (yellow) | one marker highlight at a time, laid over the plate (not multiplied) so it reads on teal |
| accent | `#d4402f` (red) | **one** reserved colour, one job: the stamp, which is the flag of the sheet |

Red never decorates and never sits on itself. The ink is a violet-leaning near-black, not neutral black.

## The medium

- Tone is made of **dots**: a `screentone` dot effect on a grey-filled shape, `size` 14 or more at a 1080-wide frame
  so the dots survive a phone (ours, tune by render). A radial or linear grey gradient under the screen gives the
  dot ramp; the gradient never shows, only the dots do.
- Each plate has its own layer with the `multiply` blend and its own `angle` (ink 45, teal 15, red 75), and no
  colour is left to the blend by accident: overprint is the default, knockout only on the stamp's white lettering.
- **Misregistered headline:** the headline is two text layers, the ink one and a teal copy a few px off (6 to 10 px,
  ours) on `multiply`; the offset is fixed for the whole shot.
- **Furniture of the file:** a reference line, a tab or two (a rounded label with a number), short L-shaped marks in the
  four corners, and one stamp. Keep it sparse: it must still read at thumbnail size.
- Shadows are flat offset duplicates of the silhouette in the ink, never a blur.
- **Finish:** `analog_film_finish` on the outer `scene_ref` gives paper tone and a fold line; keep dust and vignette at 0
  (scratch lines and a gradient break the dots-only rule); the finish is laid over the picture only and type stays sharp.

## Rates

| Held rate | Root rate |
|---|---|
| a character or hand prop, if there is one (12 fps nested composition) | arrivals, stamp, camera push, dot wipe, flash, finish |

## Boil

Only the contour of a character or hand prop boils (`line_boil`, a fixed seed, `amplitude` 2, 12 a second). Dots,
type, chips, brackets, paper and the camera stay still.

## Line width under a zoom

Scales with the world: the dossier's camera moves are small (a push of at most 8 %), so the line width is left alone.

## Motion habits, and the transitions

- **Arrivals:** everything enters on a back ease `[0.3, 1.5, 0.5, 1]` over 0.3 s from off the sheet, a chip sliding
  from its edge, type rising out of a clip band; nothing fades in.
- **Stamp:** scale 1.6 to 1 over 0.25 s, then a `shake` for 3 frames, `roughen_edges` at a constant `evolution`
  on the stamp, and a one-frame warm amber flash (normal blend, 30 % strength) over the sheet (ours, tune by render); each sheet's stamp is its one red mark, and a highlighted ring on the second sheet pulses so the sheet is never still.
- **Transition:** a dot wipe: a grid of circles in the ink grows from nothing until they join, and the next sheet is
  already under them (an `$each` grid, or `tile_mosaic` / `grid_ripple`); 0.6 s at the root rate; the wipe layer must outlast the sheet switch, so the circles shrink away and reveal the next sheet rather than cutting. A hard cut on the
  beat is the other allowed transition. Never a dissolve or a blur.

## Type

A heavy condensed face for headlines and chips, the same face letter-spaced for the case line. Headlines hold for
the reading rule in [FRAME.md](FRAME.md); case numbers are decoration and may be small but are never under 28 px.

## Scene features used

`screentone` (dot, `angle`, `size`), `multiply`, `analog_film_finish` look, `roughen_edges`, `shake`,
`line_boil`, `$each`, `tile_mosaic` or `grid_ripple`, `mask.clip`, `timeMode: "layer"`.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Tone is dots; no smooth gradient shows anywhere.
2. One dark ink, at most three spot inks, every plate multiplied except the yellow highlight.
3. The headline's teal second print is offset by a fixed amount.
4. Red appears once per sheet, on the stamp.
5. Every arrival settles with an overshoot; nothing fades.
6. At thumbnail size the headline and the stamp still read.

QC: lean on the phone-size contact sheet (the dots must survive), the thumbnail read and the palette count.

## Build with the tools

One shape layer per plate item (`multiply`, its own `screentone` angle), headline as two text layers, the file furniture as
shapes and text; put any character in a nested `composition` at 12 fps and apply `line_boil` to its contour layers
with `picsart_scene_apply_preset`; wrap the sheet as a `scene` asset and place it as a `scene_ref` carrying
`analog_film_finish`. Check the dots at phone size with `picsart_scene_contact_sheet` before a longer render.

## Do / don't

- **Do** let the stamp be the loudest event of the sheet and arrive last.
- **Do** keep the furniture sparse and the numbers consistent (the same reference number everywhere).
- **Don't** add a smooth gradient, a soft shadow, a fade or a fourth ink.
- **Template rules, this style's choices** (the rules every recipe holds):
  - Rate split: characters step, everything else runs at the root rate.
  - Nothing fades: arrivals are made by sliding, rising out of a clip, slamming or the dot wipe.
  - Print family: every plate multiplied with its own angle (the yellow highlight is laid over the plate); registration fixed per shot; halftone dots, not stipple.
  - Height is shadow: flat offset duplicates in the ink.

## Originality guard

Design your own case, wording and layout. It must not copy a known agency's dossier, a film's file cards or a named
illustrator's stamp. The dot shading, the overprint, the file furniture and the overshoot arrivals are the style.

## Proven on

A 5 s portrait clip (1080 by 1350, 24 fps) of two sheets: a dot-shaded bust under a headline with its offset teal
print, a tab, corner marks drawn on, a red stamp that slams with a shake and a flash, a dot wipe whose circles join to solid ink and shrink away to open the second
sheet, with a teal dot patch that lands with an overshoot, a yellow ring drawn on that pulses, a second tab and a red stamp; exported on the hosted renderer.

**Not proven:** a character with `line_boil` (the proof has none), the `tile_mosaic` and `grid_ripple` wipes (the wipe
was an `$each`-style grid of circles), and the dot pitch on a real phone screen.
