# Woodblock print

A coast in the manner of a Japanese colour woodblock: a graded sky that fades to paper, a red sun, layered
hills with mist bands, a wind-bent pine on a cliff, a sail and a sea of scale waves. A few flat blues and one
red, every shape lined.

## Finish

The bokashi sky gradient on paper; the cranes' wings and the boat's bob on twos (`fps` 12 under a 24 fps root); no film look.

## Palette

Paper `#efe3c8`, deep blue `#1f3c6b`, light blue `#4f74a3`, pale blue `#8fa9c8`, indigo `#2b2b3a`, snow
`#fbf7ec`, line `#2a2420`, needles `#2f4a2a`, trunk `#5a3b28`, cliff `#7c6a52`. **The hero colour is the red
`#c8402e`, reserved for the sun and the artist's seal** and used nowhere else.

## The medium

- The whole picture sits on the paper colour; the sky is a **vertical gradient fill** (the bokashi) from deep
  blue through light blue to the paper, so the sky fades into the page.
- Shapes are flat fills with a thin line (2-3 px, `#2a2420`): hills as two overlapping closed paths in two
  blues, mist as paper-coloured rounded bars with a line, a cliff as a closed path with a few short hatch strokes.
- **The sea is a repeated scale pattern**: one row is a group of nested circles (diameters 80, 60, 40, 20; strokes
  alternate snow and light blue) with a `repeater` of 19 copies, 72 px apart; stack nine rows 30 px apart, odd
  rows shifted 36 px, back row first, over a deep-blue block.
- The pine is flat clumps of needles (two ellipses each, a lighter one above a darker outlined one) on a thick
  trunk stroke that leans with the wind.
- A **cartouche** (a tall pale strip with a few black bars for writing) and a red seal square sit at the edge.

## The character

Drawn from the style's own shapes, not a generated sheet (the mechanism, saving and talking are in [shapes-character](shapes-character.md)); build once, save once to the library, place it by its `uri` in every shot.

- **Proportions:** about 6 heads tall: robed figure.
- **Shapes:** a robe as one tall trapezoid of flat colour, a round head with one black hair mass, sleeves as wedges; no outline, colour meets colour with a thin paper gap between shapes.
- **Face:** two short ink strokes for eyes, one for the mouth; `mouth` rest and `oh` as two strokes.
- **Controls:** the base set slowed, with `stride` small: a print figure glides.

## Motion habits

- Everything drifts slowly and independently: the sun a few pixels up over the shot, mist bands sliding
  sideways at different speeds (some left, some right), the boat crossing right to left with a gentle bob and a
  small rocking, the pine swaying a couple of degrees about the base of the trunk, a few cranes flapping
  across.
- **Sea drift** is a slow horizontal loop of the sea group by one pattern width (72 px), keyed linearly and
  looping so the pattern lines up at the seam.
- Put the cranes' wing flaps and the boat's bob in a nested `composition` with `fps` 15 (12 under a 24 fps root) for the stepped hand of
  a print brought to life, and apply a small `wiggle` to the cranes' rotation.
- Cued layers use `timeMode: "layer"`.

## Type

No live type: writing is suggested by black bars in the cartouche. A real caption, if one is needed, is a
vertical brush face in line colour, in the cartouche only.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Paper, blue and one red; no other hue except the muted green and brown of the pine and cliff.
2. The sky is graded to the paper at the horizon.
3. A repeated scale-wave sea, drifting.
4. Mist bands, a wind-bent tree and one boat.
5. A red sun and a red seal, both the same red.

## Build with the tools

Build each element as a shape layer, with the sea row as one group plus a `repeater`. Use
`picsart_scene_capabilities` for the repeater and gradient fields. Keep one repeater per group. Check the sea's loop
seam at the drift's end with `picsart_scene_contact_sheet` on two frames a pattern width apart.

## Do / don't

- **Do** line every shape, including the mist; the line is what separates it from a poster.
- **Don't** use more than the one red, soft shadows, or a photographic glow; don't make the sun an ellipse with a
  gradient.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Rate split: as above; sea drift, mist, the boat's travel and the pine's sway stay at the root rate.
  - Boil: none, a print holds a clean contour; the cranes' `wiggle` is keyed to amount 0 whenever they are not
    flying, and the figure, boat and pine never boil.
  - Print family: flat opaque inks, a later block covers an earlier one, hard edges (the sky gradient is the only
    soft thing); each colour block is a plate with a fixed offset of 1-2 px per shot plus a 3 px kick that decays over
    six frames at each cut (ours, tune by render); never per-frame jitter; no dots; no subtitle strip, writing stays
    in the cartouche.
  - Finish: no film look (see Finish); if a paper tooth is added it is one fixed `noise` inside the page group, so it
    travels with the page.

## Originality guard

Compose your own coast: an invented shoreline, a generic peak, your own sun placement. Never the famous
great-wave composition (a curling wave claw over small boats with a peak framed beneath it), and never a named
print series' views, a named master's signature subject, or a real seal. The graded sky, flat blues, the scale
sea and the single red are the style.

## Proven on

The pine-coast film (a graded sky, a red sun, two-tone hills, drifting mist, a swaying pine, a boat, a scale sea,
cranes, a cartouche and seal).
