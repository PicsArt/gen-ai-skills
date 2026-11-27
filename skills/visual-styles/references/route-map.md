# Route map

A made-up coastline map: the camera pushes in and pans, a dashed route draws between towns, pins drop with a
bounce, and a marker rides the route. Soft sea and sand colours and a thin lettered title.

## Palette

Sea `#9ccbe0`, land `#f1e6c8`, coast line `#c9b98f`, hills `#d9c99e`, ink `#3a3a3a`, white. **The hero colour is
the red `#d1495b`, reserved for the route and its pins**; the traveller marker is the dark blue `#2e4057`.

## The medium

- A **sea** rectangle larger than the frame, a **land** shape (a closed path with a wavy coast, a darker coast
  stroke on its sea edge only), **hills** as small overlapping triangles in a darker land tone, and a **river**
  as one thick stroke in the sea colour that runs to the coast.
- **The route:** an open polyline through the towns, a 6 px red stroke with a **dash** (length 16, gap 10), a
  keyed `trim` to draw it on.
- **Pins:** a red teardrop (a circle on a triangle) with a white dot, anchored on its tip so it drops onto the
  town. **Labels** beside each town in a condensed face in ink.
- The **title** is fixed to the screen, not the map: give it `cameraExempt` so the camera does not move or scale
  it.

## Motion habits

- **The camera is the motion.** Key the composition camera's `zoom` (about 0.8 up to 1.25 and back to 0.9) and
  `position` (a pan along the coast) with the ease in and out easing (`[0.45, 0, 0.25, 1]`), pushing in as each
  new town is reached.
- The route draws on over 2.6 s; each pin **drops** with a scale-in overshoot (`[0.3, 1.6, 0.5, 1]`) as the line
  reaches its town, and its label fades in 0.2 s after.
- **The traveller** rides the route on position keys at the vertices, constant speed, repeating by looping the
  keys (a position track with `ctx:loopOut("cycle")`); keep it after the draw-on.
- Cued layers use `timeMode: "layer"`.

## Type

A condensed display face for the title and town names, ink on land, never on the sea.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. The title does not move with the camera.
2. The route is the only red and the dashed line.
3. Each pin lands as the route reaches it.
4. The camera moves in one direction at a time.
5. Labels stay readable at every zoom level.

## Build with the tools

Build the map as shape layers; set the camera in `composition.camera` (use `picsart_scene_capabilities` for its fields)
and `cameraExempt` on the title; compute pin times from the route length in a script.

## Do / don't

- **Do** let the coast cross the frame edge so the map feels larger than the shot.
- **Don't** use satellite textures, drop shadows or a compass that spins; don't scale labels with zoom.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Line width: constant on screen. One shared zoom parameter drives the camera `zoom`, the route stroke
    (`6 / zoom`, with the dash and gap divided the same way) and the label sizes; the coast line and hills scale with
    the world; hills and minor labels take an opacity keyed to that parameter, and a label leaves before the camera
    moves on from its town.
  - True data: pin times and positions come from the route polyline in the script; towns, pins and labels match one
    to one; the coast is invented, so a small "not to scale" tag stays in frame.

## Originality guard

Invent your own coast, towns and names. It must not copy a real country's map or a known fantasy map. The
soft land and sea, the dashed route and the camera push are the style.

## Proven on

The coast-road-map film (a fictional coast, a camera push and pan, a dashed route drawing between three towns,
dropping pins, a travelling marker).
