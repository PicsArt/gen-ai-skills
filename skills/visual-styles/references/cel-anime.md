# Cel anime

A bright summer sky drawn like hand-painted cels: flat colour, one hard-edged shade tone, a few held poses and
a lot of small ambient movement. For a painted place with part-sheet characters walking through it, see
[painted anime](painted-anime.md).

The background is made of SVG shapes in the scene, or of an SVG band layout painted over once ([painted
anime](painted-anime.md)); it is never a text-to-image background.

## Finish

The characters held on threes: `fps` 8 under a 24 fps root, 10 under 30, in a nested composition (see Motion habits); no film look.

## Palette

Sky gradient `#1f6fd1` to `#6fb3ee` to `#d8eefa`; cloud light `#ffffff`, shade `#b4c9ea`, rim `#8ea6d4`; hills
`#5f9fb3`; field greens `#56b04f` and `#3f9446`; train white `#e9edf2` with a blue band `#2b72c9`; silhouettes
`#24303f`. **The hero colour is blossom pink `#ffd3e2` with an edge `#f4a6c1`**, reserved for the subject and
the drifting petals. Three to four values per object.

## The medium

- A sky is one rectangle with a `gradientFill`; the sun is a radial `gradientFill` with `alphaStops` fading
  to 0, pulsing a few percent.
- A cloud is three stacked groups in one shape layer (first listed is on top): light blobs, the shade body
  under them (the same blobs, larger and lower), then a rim group offset down-right. Hard edges only.
- Ground is layered closed paths with straight or lightly curved edges, a darker band in front.
- A character: a dark outline about 2 px at 1080 wide (a shade darker than the fill, never black), flat skin
  and hair with one hard shade tone each, a tiny highlight in the hair and eyes, large eyes with a lit top
  lid. Light comes from one side and every shade falls the same way.

## Motion habits

- Held poses with ambient loops: grass blades and cloth swing with a sine about their base (anchor and
  position both on the base), each with its own phase; use `wiggle` on hair and blades with a different
  `seed` per part.
- Clouds drift on `linear` easing at different speeds (6-12 px/s); one hero move on a gentle ease
  (`[0.3, 0, 0.7, 1]`), such as a train crossing.
- Hold the camera; let the sky move. A slow push on a face for a beat is the only camera move.
- Cued layers use `timeMode: "layer"`.

## Motion on threes

Hold each pose for three frames: under a 24 fps root the stepped rate is 8, under a 30 fps root 10 (a divisor of
the root, as in [film-flow](film-flow.md)). Pieces keyed with plain keys go in a nested composition at that
`composition.fps`; a layer whose motion is one expression reads time through `math.floor(time*8)/8` (`*10)/10`
under 30 fps) so every value changes together on the held frame. The poses hold on threes, but a root that
travels (a walk, a run, a vehicle) under a following camera stays continuous: key its position on the placed
layer or carrier, outside the held composition and with no floored time, and hold only the poses (`picsart_scene_recipe scene-animation-reference`, held drawings: "Hold the pose, not the travel").

- Key poses, with smoothstep in-betweens (`mp.ease`) between them, spaced rather than evenly timed.
- An anticipation hold before the move, a one-frame smear (ghost copies of the limb) at its fastest, and a short
  decaying shake on contact (`6*math.sin(f*90)*(end-f)/length`).

## Impact frame

Two frames of an adjustment layer carrying `black_white` then `negative` give the inverted flash of a hit. Start
it on the contact frame, with a duration of two frames (`0.0833` at 24 fps).

## Expressions

Every expression on a shape group defines its own locals (`local f = math.floor(time*R)/R` at the top of each, `R`
the stepped rate: 8 under a 24 fps root, 10 under 30).
A name that is not defined in that expression is nil, and the scene validates anyway: it fails only when the
expression runs.

## Type

One short caption in a bold grotesque (about 40 px), white, bottom centre, fading in late.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. The shade tone is hard-edged on every object: no blur, no soft shadow.
2. Sky, far hills, field and a foreground silhouette are all present (a full-bleed world).
3. Pink appears on the subject and petals only.
4. Three movers at least: clouds, grass, petals, a bird, a wire swaying.
5. One light direction across character and place.

## Build with the tools

Build sky, clouds and ground as shape layers in one scene; a train is a row of car groups in one layer (roof
light, window strip, band, body, under-shade) moved as one layer. Rig the character as usual: the style is in
the fills and lines. Place any finish look on a `scene_ref` of the drawn scene.

## Do / don't

- **Do** share the outline weight and the sky's colour in the shade tone between character and place.
- **Don't** add gradients to skin, blur to clouds or a second shade tone.

## On a part sheet

When a character comes through the SVG part-sheet flow (the `character-rigging` skill), every arm and leg is two pieces, an upper and a lower, each its own group, overlapping at the elbow or knee. That is a rig requirement no style overrides: the builder refuses a sheet whose limb is one piece. Draw each limb as two pieces, upper and lower, with the same fill, overlapping at the joint; the inner shade line stops at the joint rather than crossing it.

## Originality guard

Invent the place and the cast. It must not resemble the characters, hair or uniforms of a known anime, a
studio's signature sky-and-train framing, a famous film's station, bathhouse, castle or flying machine, or a
named series' title lettering. A generic sunset-sky-and-train composition is fine; a copy of a famous shot's
framing and props is not.

## Proven on

The summer sky and train scene (sky, clouds, grass in wind, petals, a crossing train).
