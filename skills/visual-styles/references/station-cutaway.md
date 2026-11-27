# Station cutaway

A production line shown as a building with its front wall removed, one numbered room per step. The line is read by
following a colour from room to room, and each step lights up the moment its material reaches it. Small featureless
figures at the machines show the size of things. It is a working cross-section seen straight on, with nothing drawn from
above.

## Palette and colour roles

| Role | Colour | Its one job |
|---|---|---|
| ground | `#0f1722` | the dark between rooms and around the building |
| field | `#1b2838` | the room interiors |
| line | `#e9e4d4` | the outer wall, belt rails, plaques and cargo boxes |
| field | `#5b7089` | the featureless workers, a mid slate so they never merge with cream cargo |
| line | `#080c12` | pipe edges and the flat offset shadows |
| field | `#f0a030`, `#2fb8a8`, `#ee6a55` | one colour per output kind (dough, trays, heat in the proof), spent only on that output's pipe, machine, number tag and cargo edge |
| accent | none | the three output colours are the only saturated hues |
| highlight | `#f7f3e6` | the small lamp that lights when a station starts and the pipe's highlight stripe |

A colour never appears on a thing that belongs to a different output. Nothing is a gradient.

## The medium

- Rooms are flat rounded rectangles in the room tone, stacked with a clear strip of ground between them, inside one
  outer wall stroked 12 px (ours, tune by render).
- A pipe is three strokes on one path, stacked: the dark edge 30 px, the output colour 20 px, a 6 px highlight stripe.
- Height is a flat offset: a machine's shadow is a duplicate silhouette in the edge tone moved 10 px down and right,
  never blurred.
- A belt is a row of slats clipped to a thin band; the slats slide one pitch every half second and jump back, so the
  belt never stops. Cargo is a small cream box with an edge in the output's colour.
- Workers are featureless: a round head and a rounded body in the slate tone, one arm that works a lever.
- Text is sparse: a plaque with the machine's real name per room and a number tag; no paragraph.

## Rates

| Held rate | Root rate |
|---|---|
| none in the proof; a rigged worker, if used, steps at 12 fps in a nested composition | rooms, pipes, belts, cargo, lamps, number tags and the camera |

## Boil

Nothing boils: this is a clean diagram. The belt's continuous slide is the only constant motion.

## Line width under a zoom

The camera push is the world composition's own scale, so strokes thicken with it (a 2.3 times push makes the 12 px wall
about 28 px). Keep the wall and pipe widths at or above the figures above so the first, wide shot still reads.

## Motion habits, and the transitions

- A station starts when its cargo arrives: on the beat the box reaches the machine, the lamp pops (scale 0 to 1.4 to 1
  in 0.3 s) and the number tag fills from its drawn outline with a small overshoot.
- Rooms and plaques arrive with a back ease from just below their place; pipes draw on from the machine they leave.
- One camera push into a single room is the only transition; the neighbouring rooms are covered by ground sliding
  over them so no half room is left in frame, and a word each side fills the dark. The close-up keeps working: a new
  box arrives and lights the lamp about every second. No fades.

## Type

A heavy condensed face, cream on dark: plaques at 56 px, the title at 72 px, numbers 56 px in the ground tone on the
tag. Three words at most per room.

## Scene features used

Nested `composition` layer scaled as the camera, `trim` for the wall, tags and pipes, flat duplicate shapes, `mask.clip`
for the belts, sawtooth position keys, scale keys with `ease_out`, `timeMode: "layer"`.


## Frame checklist (on top of [FRAME.md](FRAME.md))

1. One colour per output kind, used only on that output's parts; workers are slate, never cream.
2. Pipes show three strokes; shadows are flat and unblurred.
3. Every station starts on the beat its cargo arrives.
4. The belts keep moving in every shot.
5. At most three words per room, and the camera never rests.

QC: lean on the viewer's pass at normal speed (does each station start when its box arrives), the colour count and the belt check on a contact sheet.

## Build with the tools

Build the world as shape layers in one nested composition (rooms, belts, machines, pipes, lamps, number tags, plaque
text), then animate that composition layer's scale and position as the camera. Draw each pipe as three stacked path
layers with the same `trim`. Check the belts and the lamps on a contact sheet taken either side of each arrival.

## Do / don't

- **Do** let the arrival of the cargo start the station, not a timer.
- **Do** keep a clear ground strip between rooms and outside the wall.
- **Don't** add a gradient, a blurred shadow, a fade, or a colour for something that is not an output.
- **Template rules, this style's choices** (the rules every recipe holds):
  - Rate split: the diagram runs at the root rate; a rigged worker, if used, steps.
  - Nothing fades: rooms, plaques and tags are made by sliding, drawing on or popping in.
  - Height is shadow: flat offset duplicates in the edge tone.

## Originality guard

Design your own line, outputs, wording and layout. It must not copy a known factory diagram or explainer. The cut-open
rooms, following one colour from room to room and starting on arrival are the style.

## Proven on

A 5 s portrait clip (1080 by 1350, 24 fps) of two shots: a three-room bread line (mixer, shaper, oven) drawn on, boxes
riding the belts and starting each station on arrival, pipes passing the output on; then a push into the second room,
framed alone (ground slides over the neighbouring rooms and a word sits on each side), where a featureless worker
squashes a dough lump and a second and third box arrive, each lighting the lamp; exported on the hosted renderer.

**Not proven:** the ground bars' leading edge is briefly visible as they slide over the neighbouring rooms (about
3 frames), an operator rigged with a walk cycle and arm reach (the proof's operator is a few shapes), a pipe light-up
along the whole line, a porthole point of view, plates printed slightly out of register, and the type at a thumbnail
size on a phone.
