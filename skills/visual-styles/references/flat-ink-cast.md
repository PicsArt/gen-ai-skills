# Flat ink cast

A cast of calm people and animals drawn in one thick, even black line over flat muted fills, held and
changed every second frame, acting in long quiet shots on a plain wall and floor. Graphic shots (a
lettered object, a serif title, a field of dots, a morph) cut in between.

## Palette

Wall `#e7e4dc`; floor `#8a8a55`; ink `#1d1c1b` (never pure black). Cast colours: lilac `#b995ce`, salmon
`#ef7d71`, mustard `#d1a73f`, slate blue `#5b7a99`, warm browns, skin from `#edbf99` to `#8a5a3c`.
**The hero colour is the loud red `#d8382b`**, kept for one object per shot (a balloon, a field, a mark).
Everything else stays muted.

## The medium

- **One even black outline about 7 px at 1280x720**, closed round every shape, the same width on every part
  and on props. Fills are flat: no shading, no gradient, no texture.
- **Drawn on twos:** build the shot's people, animals and props in a `composition` layer with `fps` 12 inside the 24 fps
  root, so every drawn move steps; the dot-grid transition runs at the root rate. Do not add easing blur or overshoot.
- Shots run long (4 to 9 s) and hold. Acting is small: `breath`, a slow `headTilt`, one blink, one reach.
- Cuts and graphic transitions are hard, flat and fast; the style never uses soft fades between shots.

## Characters

One part sheet per cast member through the SVG part-sheet flow (`character-rigging`), built as the
three-quarter view for two-person shots, the front view for a close-up and the side view for an animal. Fill only the description slot of the prompt with:

> {subject} drawn as a flat-colour cut-out cast member with a thick, even black outline: about 7 heads tall,
> long neck, long slim limbs of even width, narrow sloping shoulders, bigger hands with clear fingers, flat
> shoes; a calm face: almond eyes with a white eye shape and a small dark pupil, each upper lid drawn as one
> black closed-eyelid line, thin dark brows, a simple nose line, small lips; {hair}; {outfit}; every shoulder
> joint sits inside the torso outline; every shape is flat muted colour with one thick even black outline, no
> shading, no highlights, no stray marks or specks inside any part; {skin}; muted warm palette with one loud
> accent colour

Do not write joint-end sentences in the prompt; they make the picture worse.

**A second person is a recolour of the first sheet**, not a second generation: swap the hair, top, trousers
and skin fills in the SVG, rebuild, and the new rig has the same controls and the same drawn face.

**On a part sheet** the limbs are two pieces each, as in every style. The builder caps and joins outlined
elbows and knees itself, so draw nothing extra at a joint: no cuffs, rings or overlap marks.

## Per-shot how-tos

Each line below was proven on a render (see Proven on).

- **Face close-up acting:** the front rig at scale about 3.4, anchored at the head, framed at the shoulders;
  a `blink` at about 1 s, `surprised` then `happy` as keyframed values, and a `headTilt` sway under 0.1.
- **Two people interacting:** the three-quarter rig twice, the second one a recolour and mirrored (`flip`),
  about 240 px apart at scale 0.72, both reaching with the near arm (`rightUpperArmRaise`, then the hand IK)
  so the hands meet at the middle; the free arm hangs with its hand clear of the thigh, in front or beside it,
  never tucked behind (`leftUpperArmRaise` 0.05 to 0.1, the two free hands apart).
- **An animal:** the four-legged part-sheet flow and its family. It walks, idles, wags and sits with the
  family's own actions (`content.animation` entries `idle`, `sit`, `wag`, each with a `fade`). The sit leans
  the body back and drops the tail below the feet: stand the animal on a ledge or step with the rest of the
  frame below it, so the tail hangs over the edge. Keep the sit for the whole shot (`duration` to the end); a
  short sit stands up again, and no wag plays while sitting.
- **A metaphor object with lettering:** one shape layer (a balloon, a key, a lid) in the hero red with the
  one ink outline, a serif word on it in the wall colour, and a wavering ink line for its string; sway it
  with a slow `rotation`.
- **A title card:** a flat mustard field, a small serif caps line above a large serif title, a wave line
  drawn under it with `trim`; the title is written on with `typewriter` over 0.4 s and holds.
- **The dot-grid transition:** a field of red circles in one grid, each growing from a point with a delay by
  its column, until they overlap and fill the frame; the next shot is already under them. 0.8 s, no easing, at the root rate (it is a wipe, not a drawn piece).
- **A morph between shots:** a circle becomes a rectangle by animating the `vertices` of one path: both with
  12 vertices, the same winding, corners matched (start the circle at -135 degrees so its four corner
  vertices meet the rectangle's); the new shot's wall colour is the shape's final fill.

## Motion habits

- Hold the pose, then change it in one step; on twos, never in-betweens beyond what the rig makes.
- One action per shot: a reach, a blink, a sit, a wag.
- Hands meet or stop short; they never pass through a face or each other.

## Type

A serif face (Georgia style) in caps for small lines and in sentence case for titles, ink black on the mustard
field and wall colour on red.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. One black outline of the same width on every part and prop; no shading.
2. The hero red appears on one object only.
3. No line crosses a bent elbow or knee; hands do not overlap into a blob.
4. Every drawn move steps on twos, transitions run at the root rate; no smooth tweens, no blur.
5. An animal's tail never hangs through the floor: stand it on a ledge.

## Build with the tools

Wall, floor, props and graphic shots are shape and text layers; each person or animal is a `scene_ref` of a
built rig (`picsart_scene_build_model` `character`, `family` for the animal) with `fit` `none`; the shot's drawn content sits in a
`composition` at 12 fps and the dot-grid transition sits outside it at the root rate.

## Do / don't

- **Do** keep the camera still and the cast cut at the floor line.
- **Don't** add a second hot colour, a glow, a gradient or smooth easing.
- **Don't** draw a joint cap, cuff or ring into the part sheet; the builder joins it.
- **Template rules, this style's choices** (the rules every recipe holds):
  - Rate split: the people, animals, props and the morph step on twos inside the shot composition as above; the dot-grid transition runs at the root rate; the camera is still, so there is nothing to judder, and no film finish is added.
  - Boil: nothing boils; the outline holds and a pose changes in one step, which is what keeps the shots calm.

## Originality guard

Invent the people, the animals, the words and the metaphors. Never imitate a known film, its maker or its
characters, and never name one in a prompt. The thick even ink line, flat muted fills, held acting on twos
and the graphic cuts are the style.

## Proven on

A close-up, a two-person handshake (recolour), a hound that stands then sits on a ledge, a labelled balloon, a
title card, a dot-grid transition and a circle-to-rectangle morph, all 16:9 and 3 to 6 s, previewed locally.
**Not proven, so not in this recipe:** a seated person (the shirt hem frays and the trousers show patches at the
hip when the hips bend), a wagging animal, crowds.
**Not proven:** the root-rate dot grid was shown on six dots over a flat wall, sampled between 12 fps steps, not between two full shots.