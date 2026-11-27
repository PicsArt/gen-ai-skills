# Tilt-shift town

A toy city seen from above at a slant, shot like a miniature: pastel blocks, a green park and a square with a cream clock tower with a terracotta-red pitched roof, tiny cars looping on the roads, a key light that sweeps across the whole city in eight seconds while a clock readout runs from 06:00 to 12:00. Only a strip across the middle is sharp; the top and bottom of the frame melt into blur, which is what makes it read as a model. It is calm, detailed and slightly dreamy: not an isometric vector town ([isometric-town](isometric-town.md)) and not a brick-toy macro ([brick-toy](brick-toy.md)).

## Palette and colour roles

| Role | Colour | Its one job |
|---|---|---|
| walls | peach `#f29a73`, yellow `#f5cf6a`, mint `#7cc7b6`, periwinkle `#8fa8e8`, pink `#ef8fa3`, cream `#f1e4c8`, green `#93cf86`, lilac `#b99be0` | the pastel houses |
| roofs | red `#c9473d`, blue `#3f67b5`, green `#2f8a66`, amber `#d68a2e` | a few roofs only |
| ground | slate `#6f7785` (roads and ground), sky `#c9d3db` and `#9fb6c9` | the quiet base |
| cars | red `#e05a4a`, blue `#4a7fd0`, yellow `#f2c14e`, white `#f4f2ea`, green `#4fa37a`, orange `#e88a3a`, violet `#8a6cd0` | ten small moving dots of colour, two to six of them on screen at a time: seven colours across ten cars (red, blue and yellow twice) |
| light | warm key `#fff0d8`, cool fill `#cfe2ff`, ambient `#dfeaff` over `#a89f8e` | morning to evening |
| land | lots `#e3dccb`, square `#e9dcc3`, parks `#6cc35a`, trees `#3f9c4a`, tower `#f0e6d4` with a four-sided pyramid roof `#8e1f19` (the light lifts it to a terracotta red) | the calm ground between the houses |
| readout | cream card `#fbf7ef` at 92%, text `#2b2f38` | the clock and caption |

Hero colour: the pastel walls against the grey roads.

## The medium

- **The town is a real 3D model:** a grid of 12 by 12 blocks (0.2 units pitch, 0.05 roads), each block a few chunky pastel buildings with bevelled edges, small trees on park blocks and a square in the middle with a tall cream clock tower with a terracotta-red pitched roof, whose two hands are separate nodes.
- **Ten small cars** run along the roads in straight loops on position expressions, in both directions, each at its own phase.
- **The camera** looks down at a steep slant (the eye about 0.62 up and 0.95 back, looking at a point 0.08 up, a 38 degree vertical lens) and orbits slowly (about 0.1 units sideways and 0.08 closer over the 8 s, so the tower slides across the frame and the town turns a little); the shutter is 180 degrees with a few samples of motion blur.
- **The key light** swings from one side to the other (its direction's x runs from +0.75 to −0.75 across the eight seconds), with a soft shadow, so every shadow sweeps across the streets.
- **The signature effect is a miniature blur, built from two parts:**
  1. a depth of field (`depth_of_field`, with `ambient_occlusion` beside it) on the 3D camera, a very open aperture, which blurs by real distance;
  2. six masked blurred copies of the rendered picture laid over the sharp one: three bands at the top and three at the bottom, each a Gaussian blur of 16, 10 and 5 px from the edge inward (top bands 100, 80 and 60 px, bottom bands 330, 220 and 170 px, outer to inner, so the sharp strip is 390 px tall, from y 240 to y 630 of 1350, around the clock face and the back of the square). The blur effects sit on 2D layers over the baked video, not on the 3D scene: a 3D object refuses `effects`.
  The depth of field alone is too gentle to read as tilt-shift; the bands alone look flat. Use both.
- **The readout** is a flat 2D card and a caption laid over the picture, not part of the 3D scene. It sits at the lower left, from y 1000 to y 1130 of 1350, over the 10 and 16 px bottom bands; it is a solid cream card, so it stays legible over the blur.

## Rates

| Held rate | Root rate |
|---|---|
| none | everything: the camera, the light, the cars, the hands and the clock |

## Boil

None.

## Line width under a zoom

There are no lines; the clock hands are 3D parts.

## Motion habits, and the transitions

- **The camera orbits slowly,** about 0.1 units sideways and 0.08 closer over the 8 s, never stopping.
- **The sun sweeps** from one side to the other, and the shadows turn with it.
- **The cars loop** one to two laps in 8 s, each at its own phase so the streets are never empty.
- **The tower's clock hands** turn (the minute hand 270 degrees and the hour hand 22.5 degrees per second of clip time) in step with the readout, which counts a morning from 06:00 to 12:00.
- **The readout card** is there at full strength from the first frame.
- Transitions: a hard cut; none are built into the proof (see Not proven).

## Type

A monospaced semibold for the time (about 56 px) and a bold sans for the caption (about 34 px), dark on a cream card about 540 by 150 px. The caption is one short line of your own, short enough to fit the card.

## Scene features used

Hints, not rules: the look depends on a depth of field on the 3D camera plus masked, blurred copies of the render; playing a baked 3D render as a video with a matte is one way to make the blurred copies. Model parameters turn the clock hands, and position expressions loop the cars.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. The middle of the frame is sharp, and the top and bottom edges are visibly softer, in steps (the masks are hard-edged: 16, 10, 5 px, then sharp), and no band edge should read as a line.
2. The clock face and the back of the square sit in the sharp strip; the tower's roof and the near streets melt into the bands.
3. The cars are small, whole and on the roads; none drives through a building.
4. The clock readout is fully legible and its hands match the tower's.
5. The readout is fully visible from the first frame, legible over the blurred bottom bands, and the last frame reads about 12:00.

QC: a contact sheet every 1.5 s, and the viewer's pass at normal speed for the shadows' sweep and the car loops.

## Build with the tools (a hint, optional)

Any construction that keeps the look is fine. Bake the 3D scene first (with the depth of field on), then stack the blurred copies; the model and cars can be one parametric model plus ten copies of one car with different paints.

**Cost on a phone:** the six blurred bands are six full Gaussian blurs of the picture on every frame, and their frame cost has not been measured on a phone. To cut it on a phone, use fewer bands: one at the top and one at the bottom (about 10 px, two blurs in all) or the 16 and 5 px pair at each edge (four), and lean on the camera's depth of field for the rest, or bake the blur into the video, and check the draw time on a phone before shipping. The look is softer but still reads as a model.

## Do / don't

- **Do** keep a steep slant and a narrow sharp strip: that is what shrinks the town into a toy.
- **Do** keep colours pastel and the roads quiet.
- **Do** write your own town, caption and cars.
- **Don't** add outlines, hard shadows or neon.
- **Don't** let the sharp strip cover the whole frame.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Rate split: everything runs at the root rate.
  - Nothing fades.
  - Height is shadow: real soft shadows from the sweeping key light.
  - Boil: none.

## Originality guard

Design your own city, tower, caption and palette. Do not copy a real city, landmark, or video. A slanted miniature town with a sharp middle strip, soft top and bottom and a time-lapse morning is the style.

## Proven on

An 8 s portrait clip (1080 by 1350, 24 fps): a 12 by 12 town with a clock tower, ten cars, a sweeping key light, a depth of field plus six blur bands and a running clock; baked frame by frame locally, not on the hosted renderer.

**Not proven:** smooth playback of the six blurred copies on a phone (their frame cost is not measured); the stage editor, a landscape frame, a camera that turns or tilts, rain or night, and a transition in or out.
