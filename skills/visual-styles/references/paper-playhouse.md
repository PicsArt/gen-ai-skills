# Paper playhouse

A paper theatre seen through its proscenium: teal curtains frame and part on a snowy night, cut-paper flats slide in
from the wings, a puppet on a visible rod crosses the stage and a warm pool of light follows it. Every piece is a flat
sheet standing at its own depth under a slowly pushing camera, with a soft contact shadow behind it and a pale paper
edge on it. It is a stage built of card, not a painted landscape and not a flat parallax scene.

It differs from [layered-lightbox](layered-lightbox.md) (sheets lit from behind, depth told by darkness, no hero) and
from [cut-paper](cut-paper.md) (textured paper acting on one plane, stop-motion bounce): here depth is real distance
under a camera, the light is a warm pool that follows the hero, and the frame is a theatre with curtains.

## Palette and colour roles

| Role | Colour | Its one job |
|---|---|---|
| ground | `#0d1020` | the dark behind the stage, the frame background |
| sky | `#222c55` | the back sheet, the night |
| field, far to near | far hills `#4a5d94`; mid snow hill `#a9bcd8`; house walls `#d9ccb0`, roof `#8a3f3a`, door and chimney `#5d4a4a`; pines `#2d5b5c` with snow caps `#eef2f7` and trunks `#5a4038`; front snowbank `#e7edf5` | the planes of the stage, the far ones cool and blue, the near ones whiter |
| haze | `#8ea6d2`, `#9fb4dc` | two soft bands between the planes, lighter than what they sit on |
| moon, stars, snowflakes | moon `#efe4c0`, stars `#f2e7c4`, snowflakes `#f6f3ea` | the only pale lights in the sky |
| curtain | `#17474b`, `#1f5c60`, trim `#d6a446` | the frame that opens the film and stays at both edges |
| hero | `#d9733a`, `#b85a2c`, `#a8502a` | the puppet fox: the one saturated body |
| accent | `#ffbf5e` | the warm pool of light that follows the hero, and the lit window, nothing else |
| paper edge | `#f4efe3` at 55 % | a thin pale edge on every flat (the paper tone; also the title) |
| shadow | `#070a16` at 42 % | every contact shadow |
| title bar, title | `#121626`, `#f4efe3` | the bar under the stage and its line of capitals |

Hero colour: warm amber (the pool of light and the fox it follows). Saturated amber and orange are spent only on the
hero, its light and the lit window; the gold trim is a thin line and the roof a muted brick red; everything else is
cool.

## The medium

- Every flat is a closed paper cut-out in one fill, a pale edge (a 3 px stroke at 55 %) and a soft shadow copy behind
  it. No gradients on a flat; the only gradients are the light pool and the two haze bands.
- Depth is real: each plane has its own `z` between the far sky (about -420) and the valance (about +70), and each
  is scaled by `1 - z / 1500` so it fills the same frame at rest. The camera then separates them: a slow push (zoom
  1.0 to 1.07 over the film) and a pan that starts after the curtains have opened.
- The shadow is a copy of the flat in the shadow tone, offset about 9 px right and 12 px down, scaled 0.4 % larger, and
  blurred more the farther the plane: about 29 px for the moon, 19 px for the mid snow hill and house plane (z -180),
  15 to 16 px for the pines, 8 to 11 px for the nearest pieces and the curtains (ours, tune by render). The farthest
  hill sheet takes no shadow: the haze covers it and its shadow read as a floating outline.
- The puppet is one cut-out fox with a thin rod running from its body down past the stage floor; it hops and sways on
  the rod, it does not walk with its legs.
- The light pool is a soft radial ellipse (620 px wide, squashed to 72 % high), peak alpha 0.42, on a layer whose blend
  is additive (`blendMode: "add"` on the layer, not on the gradient item, which has no paint under it); it sits under
  the hero and moves with it.
- Two haze bands (a tall rectangle with a vertical alpha ramp up to 0.32) sit between hills and pines so the far planes
  lose contrast.
- Falling snow and the stars are small shapes driven by expressions: snow falls 70 to 130 px/s with a sideways sway and
  a slow turn; the stars hang on threads, swaying about 4 px and turning about 9 degrees.

## Rates

| Held rate | Root rate |
|---|---|
| none | everything: curtains, flats, puppet, light pool, snow, camera |

## Boil

Nothing boils: paper is clean. The only constant motion is the puppet's hop and rod sway, the snow, the stars swaying on
their threads and the camera push.

## Line width under a zoom

The paper edge is a 3 px stroke in the flat's own space, so it grows with the world as the camera pushes; the push is
small (7 %), so the edge stays a thin line. Nothing else has an outline.

## Motion habits, and the transitions

- The film opens on closed curtains that part (0.1 s to 0.95 s, an in-out ease, then an ease-out back-settle of about
  11 px at 1.15 s) and stay at the two edges. The valance and the title bar are the fixed frame.
- Flats slide in from the wings, not up from below: left pines from off-screen left, right pines from off-screen
  right, each held a beat after the curtains start to part (0.55 s and 0.7 s), travelling about 0.45 s on an ease out,
  overshooting by about 25 px (4 % of the travel) and settling back.
- The puppet arrives after the stage is set (from 1.25 s), crosses over about four seconds on an in-out ease and slows
  to a stop over the last second; its hop is `abs(sin)` of about 5.5 rad/s at 24 px and its rod sway a few degrees (11
  rad/s, 5°).
- The light pool starts parked on the house, the puppet's goal, swings to the puppet (0.9 s to 1.6 s) and then follows
  it, slightly ahead.
- The title bar rises from below the frame (1.2 s to 1.7 s) and the line is set in capitals. No fades: things
  arrive by sliding in or by being uncovered.
- Transitions between scenes: close the curtains, or slide the next set in from the wings. A cut to another stage is
  by curtain. No dissolves.

## Type

One short line in capitals, widely tracked, on the dark bar under the stage: a geometric sans at weight 600, about 50
px, tracking 10 px, in the paper tone `#f4efe3`. It holds long enough to read at normal speed; the bar is exempt from
the camera so the line never drifts or scales.

## Scene features used

Closed paths with `fill` and `stroke` (opacity), per-layer `z` with the composition camera (`zoom`, `position` keyed),
`gaussian_blur` on the shadow copies, a radial `gradientFill` with `alphaStops` on an ellipse for the light pool on a
layer with `blendMode: "add"` (on the layer, not on the gradient item), a rectangle with a vertical `gradientFill` for
haze, position keys with `ease_in_out` and `ease_out` for the slides, expression-driven position and rotation for hop,
sway, snow and stars, `cameraExempt` on the title bar and line.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Each flat has a pale edge and a shadow whose softness grows with its distance.
2. The planes separate under the camera: the far ones move least, the curtains most.
3. Saturated amber and orange appear only on the hero, its light and the lit window (the gold trim stays a thin line).
4. The light pool is under the puppet at every frame, and the pool is not clipped by a plane in front of it.
5. The rod stays attached to the puppet and runs down out of the stage; the hop never separates them.
6. The curtains stay clear of the stage edge (no sliver of ground between curtain and valance).
7. The title reads against the bar and stays out of the camera.

QC: lean on the viewer's pass at normal speed (does it read as a stage with distance), the plane order and shadow
softness on a contact sheet, and the light pool's position against the puppet frame by frame.

## Build with the tools

Build each plane as a shape layer with its shadow copy beneath it (blur and offset as above) and give it the `z` and
the scale for its depth. Place the camera keys last and check the push on a contact sheet. Drive the puppet with a
position key plus the hop and sway expressions, and the light pool with its own position keys that end next to the
puppet's. Keep the curtain, valance and title bar as the top layers.

## Do / don't

- **Do** keep every flat flat: one fill, an edge, a shadow.
- **Do** soften the shadow of the farther planes more than the nearer ones.
- **Do** let the light pool, the puppet and the lit window be the only saturated warm things in the frame.
- **Don't** fade a flat in, add a gradient to a flat, or let the shadow be a hard offset copy.
- **Don't** raise the push past a few percent; the parallax is the camera's, not a zoom.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Rate split: everything runs at the root rate; nothing is held.
  - Nothing fades: curtains part, flats slide in from the wings, the title bar rises.
  - Height is shadow: a soft blurred shadow, softer for a farther plane, plus a pale paper edge; the shadow is a blur
    here, not a flat offset duplicate, because the pieces stand in depth and are not printed.
  - Boil: none.

## What this style does not do

The look is built from flat layers, so it has none of these:

- A volumetric beam with drifting dust: the light pool is a flat ellipse, so it never reads as a beam through air.
- Fog that thickens between planes: the haze bands are two fixed strips, not a density that grows with distance.
- Light that wraps the paper edges and softens the shadows near it: the edge is a constant pale stroke and the shadow
  a fixed blur.
- Paper curl: every flat is perfectly flat.

## Originality guard

Design your own stage, flats, puppet and wording. It must not copy a known paper-theatre, toy-theatre or shadow-box
artist's work, a published set or its characters. A curtained stage, flats in depth and a lit pool are the style.

## Proven on

A 6 s portrait clip (1080 by 1350, 24 fps): curtains part on a snowy night with a moon, stars, far hills, a house with a
lit window, two pine flats sliding in from the wings, a snow bank, falling snow, a puppet fox on a rod crossing the
stage with a warm pool of light following it, 13 depth planes under a slow push with soft shadows, two haze bands and a
title in capitals on a dark bar, exported locally, not on the hosted renderer.

**Not proven:** a seam between the two curtain halves where the fold lines double for a frame, an olive tint on the
pines under the light pool, scene-to-scene transitions (curtain close, slide from the wings), a second hero, a stage
longer than six seconds, and the limits above.
