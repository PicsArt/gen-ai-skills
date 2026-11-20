# Recipe template

The shape every style recipe follows. Write a new recipe from it, and bring an existing one up to it when you
next touch that recipe. Every number in a recipe is a starting point of ours; mark one that is not yet proven
with "(ours, tune by render)".

## Rules that hold for every recipe

Each is said once here; a recipe points to it in one line and gives only its own choice. Every number is ours, tune by
render.

- **Rate split.** Only drawn pieces step (twos or threes, in a nested composition at that rate). The camera, light
  sweeps, glow, flicker, weave, particles, wipes and text slides run at the root rate: a stepped camera judders. The
  film finish goes on the outer `scene_ref` at the root rate, never inside the stepped asset. Pick a tempo whose beat
  is a whole number of frames and key on whole frames; `frame_grid` snaps only layer start and end times.
- **Boil.** A recipe says what boils. Default: only the contour of characters and hand props, at a held rate near
  twelve, a few drawings cycled, small amplitude, a fixed `line_boil` seed; fills, hatch, tone, text, backgrounds, a
  finished page and the camera stay still.
- **Line width under a zoom.** Zoom is the composition camera's, and expressions cannot read the camera, so one shared
  parameter drives both the zoom and the stroke width: constant on screen is `width = base / zoom`, sub-linear is
  `base / zoom^k`, and a style that scales with the world leaves the width alone. Detail groups (small text, minor
  marks) take an opacity keyed to the same parameter so a pull-back is not sub-pixel noise. Check the widest frame.
- **Nothing fades.** Content in a drawn style appears by being made: drawn on (`trim`), written (`typewriter`, a
  clipped rise), printed, lit, scanned, uncovered or slid in; never an opacity ramp on drawn content (`fade_in_chars`
  is not for these styles). A subtitle on a paper slip may fade lightly. A recipe lists the transitions it allows and
  forbids; a morph happens on blank ground; a film reuses a few transition kinds.
- **A finish belongs to the page.** Paper tooth, hatch grain and dots sit inside the panned group so they travel
  with the page (a rolling finish on a `scene_ref` crawls). Grain is added once and held steady; film damage and
  grain go on the picture layer, while type and cards stay sharp. A touch of fixed `noise` under a dark gradient keeps
  H.264 from banding. Coarsen fine detail that shimmers rather than rendering large and downscaling.
- **Height is shadow.** A lifted piece throws a larger, softer, farther shadow; once down, only a thin paper-edge
  shadow; one light direction for the film. A print or cartoon style uses a flat offset duplicate of the silhouette,
  not a blur. `drop_shadow` offset, blur and opacity key to the lift (two keys per hop); `hard_shadow_card` serves media.
- **Print family.** Registration is a fixed offset per plate for the whole shot and is never jittered per frame; it
  moves only as an event, an accent kick that decays or a slow drift that snaps back on the beat. Every fill and line
  says knockout or overprint (multiply), so no colour is left to the blend by accident: overprint is the default,
  knockout only where the design says so. Halftone dots and stipple grain are different things; a recipe says which
  it has.
- **Hatch and texture ride the object.** Parent hatch and tone layers to the object, or put them in its group, so the
  strokes stay on the surface under a camera or limb move; a screen-space overlay swims. A screen-locked effect chain
  is for the static background only.
- **Arrivals settle.** Anything that arrives settles on a `spring`, `settle` or a small back-ease; a tracker or a
  drawn line is linear. A recipe names its easing set (a precise ease with no overshoot, or `[0.3, 1.5, 0.5, 1]`,
  or hard frames). A big move anticipates (a small pull-back), holds, then snaps.
- **Stop time.** To freeze on the key beat, put the subject layers in a nested composition whose keys end at the
  freeze time while the light and sky layers keep theirs; a media layer freezes with `content.speed` 0 and reverses
  with a negative speed. There is no single global pause.
- **True data.** Every number on screen comes from the same numbers that draw the picture, so any frozen frame checks
  out; a source tag stays in frame from first reading to summary; counts add up (rows, parts, bars); one unit is one
  object, stated once; a schematic thing is labelled schematic; record each asset's licence and use no generated
  stand-in for a real archive object.

**Exceptions.** A style whose look is a film (a whole-frame finish, grain over type and cards included) puts its
finish over the whole frame by design, and says so. A recipe may state its own boil, shadow offset, ease or stepped
draw-on where its proven look needs it, and names the choice in its "Template rules" bullet; an unstated choice
follows the rule.

## Sections, in order

1. **Opening paragraph.** What the style is in two or three sentences, and what it is not.
2. **Palette and colour roles.** A table, one row per colour:

   | Role | Colour | Its one job |
   |---|---|---|
   | ground | `#…` | what sits behind everything |
   | line | `#…` | outlines and rules |
   | field | `#…` | large flat areas (one row per field colour) |
   | ink | `#…` | type and fine marks |
   | accent | `#…` | **one** reserved colour, with the single thing it means |

   An accent never decorates and never sits on itself. A colour that flags a problem exists only while the
   problem does. Where the style is light, avoid pure black and neutral dark grounds: a warm near-black ink, an
   outline in its own colour, a tinted dark ground.
3. **The medium.** What makes the picture read as this style at the size a viewer sees it.
4. **Rates.** A short table: what runs at the held rate (drawn pieces, boil, cel offsets) and what stays at
   the root rate (camera, light sweeps, glow, flicker, weave, particles, wipes, text slides). A stepped camera
   judders, so the camera is never in the held group. The film finish goes on the outer `scene_ref`.
5. **Boil.** One line saying what boils and what stays still. The default is the contour of characters and hand
   props only, at a held rate, with a fixed `line_boil` seed; fills, hatch, tone, text, backgrounds, a finished
   page and the camera stay still, and stopping the boil is an event.
6. **Line width under a zoom.** One line choosing: constant on screen, sub-linear, or scaling with the world.
   The composition camera does the zoom, so one shared parameter drives both the zoom and the stroke width.
7. **Motion habits, and the transitions.** Which transitions the style allows and which it forbids. Things
   appear by being made; the transition grows out of the medium, not a stock dissolve.
8. **Type.** Where text lives, how long it holds (see the reading-time rule in [FRAME.md](FRAME.md)), and which
   face does which job.
9. **Scene features used.** A list naming the effects, looks, presets and shape items the recipe relies on
   (`screentone`, `$each`, `offsetPaths`, a counting text track, `roughen_edges` at a constant `evolution`), so
   an author reaches for the feature and not for a hand-built workaround. Check each name against
   `picsart_scene_capabilities` before writing it.
10. **Frame checklist** (on top of [FRAME.md](FRAME.md)), ending with a QC line: which of the QC pass's steps
    this style leans on most.
11. **Build with the tools.**
12. **Do / don't.**
13. **Originality guard.**
14. **Proven on.** What was rendered, at what size. Beside it, **Not proven**: what the recipe describes but no
    render has yet shown, so the next author knows where to look first.
