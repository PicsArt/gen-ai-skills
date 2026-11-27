# Manga panels

A page of black-and-white panels that draw on one after another: screentone, close-ups of eyes, speed lines and a
sound effect in a hand-lettered face.

## Finish

Speed lines on twos (`fps` 12 under a 24 fps root) and the panel border drawn on (see Motion habits); no film look.

## Palette

Ink `#111111`, paper `#fbfaf6`, mid grey `#5a5a5a` for an iris. No colour. **The hero is the pure ink black on
the subject's hair and outline**, kept heavier than any other black on the page. Tone is ink at partial opacity
(0.25-0.55), never grey fills.

## The medium

- **Screentone** is a dot grid: a row group (a 4 px ellipse with a `repeater`, `position [11, 0]`) inside a column
  group (that row with a `repeater`, `position [0, 11]`); one repeater per group, so two directions are two nested
  groups. Vary opacity for light and dark tone; the dot size is the same everywhere.
- A **panel** is a rectangle: a composition layer clipped by `mask.clip` (a colour rectangle at the panel's
  place), plus a separate 6 px rectangle border with `trim` end 0 to 1 over 0.5 s so the frame draws on.
- A character: ink outline in two weights (heavy outer contour, light inside), tone for shade and hair, large eyes
  (an almond lid with a 7 px outline, an iris disc, a pupil, two white shine dots), an invented hairstyle and
  outfit. Emotion lives in the eyes and effect marks (sweat drops, veins, sparkles).
- A place is a few ink lines for perspective, hatching for depth, a blank white sky with speed lines for action,
  and one detailed background panel to establish the setting.
- Speed lines: one long thin triangle repeated 60 times at 6 degrees about the centre; surprise lines a short
  stroke repeated 7 times at 22 degrees.

## Motion habits

- Panels enter in sequence (a layer `start`, the panel wiped in over 0.25 s by a clip rectangle whose keyed `position` slides in from the panel's near edge, and the border drawing on a snap curve
  `[0.7, 0, 0.15, 1]`). Inside a panel motion is sharp: an eye opens by scaling 0.25 to 1 in 0.4 s, a pupil slides
  on an ease, a final object scales 0.4 to 5.5 on an ease-in.
- Speed lines flicker by living in a nested composition at `fps` 15 (12 under a 24 fps root) with a rotation key per frame step; a hit
  shakes with the `wiggle` preset (6 px `amount`).
- Child layers of a composition layer run on local time: every key counts from the layer's `start`
  (`timeMode: "layer"` on cued layers). Nothing past the composition's end is drawn.

## Type

Captions in a plain bold sans inside a white box with a 2.5 px outline. The sound effect in a heavy comic face,
about 130 px, filled paper with a 10 px ink outline drawn over the fill (`stroke.order: "stroke-over-fill"`),
rotated about minus 9 degrees, popping in with an overshoot.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. A face acting in the close-up panel; the eyes carry the emotion.
2. Panels tile the page edge to edge with even gutters; the establishing panel shows the place.
3. Tone dots and border weight are identical across panels.
4. Three or more details of life: tone gradients, speed lines, falling petals, a bird, effect marks.
5. No colour anywhere; the sound effect is the heaviest type on the page.

## Build with the tools

Build one panel as a composition layer with its `mask.clip`, then repeat for each panel with its own `start`.
Write inner keys in the layer's own time. Check the page on a contact sheet at the moment all panels are in.

## Do / don't

- **Do** vary panel size to pace the reading: wide, close, tilted, full-bleed.
- **Don't** fill with grey, mix dot sizes, or add colour.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Nothing fades: a panel border draws on with `trim`, an eye opens by `scale`, the sound effect pops by `scale`,
    speed lines are cut in on twos; the only transition is a hard cut between pages.

## On a part sheet

When a character comes through the SVG part-sheet flow (the `character-rigging` skill), every arm and leg is two pieces, an upper and a lower, each its own group, overlapping at the elbow or knee. That is a rig requirement no style overrides: the builder refuses a sheet whose limb is one piece. Draw each limb as two pieces, upper and lower, in the same tone with the outline broken at the joint, so the pair reads as one limb.

## Originality guard

Use your own story, character and setting. It must not resemble a known battle manga's spiky-haired hero, masked
ninja, straw-hatted pirate or giant-eating-wall scene, any series' name, sound-effect lettering or logo, or a page
layout or splash panel copied from a known chapter. Tones, panels and lines are technique; faces and plots are not.

## Proven on

The three-panel page (rooftops, an eye close-up, a rushing hit with speed lines and a sound effect).

**Not proven:** the clip wipe was shown on one panel, not on a full page of panels.