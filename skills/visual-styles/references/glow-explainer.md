# Glow explainer

A flat science explainer that glows: saturated vector shapes with no outlines on a deep navy space, soft light
around every bright object, and one continuous zoom across scales (a planet, its star's neighbourhood, the
galaxy) instead of cuts.

## Palette

Space is a radial gradient from `#1b1f5e` at the centre to `#0a0b26` at the edges; small stars `#cfe3ff` at 0.25
to 0.8 opacity. Ocean `#4fb8ff` to `#1d4fc4`, land `#3ddc84`, clouds white at 0.85. Star light `#fff7c2` to
`#ffb347`; the galaxy is violet `#7a5cff` with a cream core `#fff1c9` and dots in `#9fd3ff`, `#ffc6ec`,
`#bfa8ff` and white. **The hero colour is the warm yellow `#ffd23f`**, kept for the "you are here" mark and the
city and satellite lights. Every bright object has its own glow in its own hue.

## The medium

- **No outlines.** Edges are colour against colour. A sphere is a disc with a radial `gradientFill` lit from
  the upper left (start point about a third of the radius up and left of centre), plus one night shade on the
  lower right.
- **Glow is a gradient, not a blur.** A glow is an ellipse with a radial `gradientFill` in the object's hue whose
  `alphaStops` fall to 0 before the edge: offset 0 at alpha 0.8, 0.3 at 0.36, 0.85 at 0, 1 at 0. Reaching 0 at
  0.85 keeps the ellipse's edge invisible. List it after the body in the shape's items, because the first item
  listed draws on top.
- **Place, squash or tilt a glow with the layer's transform, never a group's.** The galaxy's disc glow is its own
  child layer with `position` on the core, `scale` `[1, 0.52]` and `rotation` -20.
- **Detail is many small things**: about 140 small stars, a few satellites with their own glow, drifting dust,
  and about 1,300 seeded dots in two log-spiral arms (`r = 30·e^(0.21θ)`, flattened to half height, scattered
  about 0.1 rad).
- A detailed planet or creature can be one generated flat-vector SVG (no outlines, one hard night-side shape,
  an atmosphere rim) rasterised as a media layer. Hand-built discs read as plain next to the galaxy.

## Characters

Small, simple people in a crowd, never one detailed hero. Make one through the SVG part-sheet flow
(`character-rigging`): fill only the description slot of the frozen part-sheet template with:

> {subject} drawn in a flat glowing science-explainer style: about 3 heads tall, a soft rounded bean-shaped torso
> as wide as the head, a very short neck, short stubby arms and legs with rounded ends, small round hands, small
> rounded feet in simple dark shoes; a simple face: two small solid black dot eyes each with one tiny white
> highlight dot, short level dark eyebrows, no nose, no ears, a small closed mouth; one small rounded tuft of dark
> hair on top of the head; wears one plain saturated {colour} jumpsuit (the sleeves in the arm groups, the
> trouser legs in the leg groups) with a small yellow round badge on the chest; NO outlines anywhere: every shape
> is flat colour meeting flat colour; flat shading: every part has a flat saturated base colour plus ONE soft
> lighter highlight shape of the same hue on the side toward a light at the upper left and one slightly darker
> flat shade shape on the opposite side; skin a warm peach, the whole palette bright, simple and friendly

- **One sheet makes the crowd.** Recolour each copy's jumpsuit with `color_replace` on its layer (`selectedHue1`
  at the suit's hue, `minHue1`/`maxHue1` 25, `replaceHue1` the new hue); the skin keeps its colour.
- **Walking round a small planet.** A walk that travels on its own refuses a parented layer
  (`travel_needs_plain_layer`); with `travel` `in_place` the layer may be carried by a parent. On a planet the
  carrier turns, so walk each character `in_place`, standing on the planet's top inside its own nested
  composition. Make that nested layer a child of
  the planet's level, with its anchor on the planet's centre and a rotation of `a0 + ω·time` degrees, where
  `ω = stride × scale / stepDuration / R × 180 / π` in degrees per second (the rotation takes degrees; without the 180 / π the carrier turns 57 times too slowly and the feet slide). Give each walker its own `stepDuration` (0.42 to 0.5 s) and
  its own ω, so they never step in unison and their feet stay planted.

## Motion habits

- **One continuous zoom across scales.** Draw each scale as an `empty` level layer at the frame centre, with its
  content as child layers in that level's own units. Level *i* is drawn 12 times smaller than level *i+1*
  (the planet's radius 150 in level 1 is 12.5 in level 2), and the thing you zoom from sits at every level's
  origin. Each level's `scale` is `z·12^(i-1)` from one shared expression:
  `local u = 0.5*ss(1.3,3.9,time) + 0.5*ss(5.0,7.6,time)`, `local z = math.exp(-math.log(144)*u)`, with `ss`
  a smoothstep. Easing `u`, not the scale, keeps the zoom even in log space: each push moves one level and then
  holds.
- **Levels hand over by opacity on the same `u`**: a level fades in while it is still large (u 0.22 to 0.42 for the
  orbits), and a level's detail fades out before it becomes sub-pixel (satellites by u 0.25, the moon by 0.5,
  the planet by 0.95).
- **Ambient life never stops**: planets on orbits by position expression, clouds swaying a few pixels, dust
  drifting slowly in screen space, and the "you are here" ring growing once on arrival.
- A caption per held level, in a rounded bold sans, fading in on the hold and out before the next push.

## Type

Short caps captions in a rounded geometric bold (`gilroy-bold`), about 40 px, white, bottom centre: one per scale.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. No object has an outline; every bright object has a soft glow with no visible edge.
2. The zoom never cuts: each level is already on screen before the previous one is gone.
3. The thing you zoom from stays at the same screen point through every level.
4. The hero yellow appears only on the marks and lights.
5. Something small is moving in every frame.

## Build with the tools

Build the levels as `empty` layers with a `scale` expression, and their content as child shape layers
(`parentId`); give orbiting bodies a `position` expression. Generate one detailed hero object as a flat-vector
SVG when the frame needs more than discs. Check the zoom on a contact sheet at the holds and mid-push.

## Do / don't

- **Do** give every scale its own hue family (blue planet, amber star, violet galaxy) so a level reads at once.
- **Don't** blur for glow, outline a shape, or cut between scales.

## Originality guard

Invent the subjects and the characters. Use this palette's own colour values and characters made from the part
sheet above. Never imitate any studio's or channel's characters, mascots, title cards, palette or recognisable
frames, and never name one in a prompt. Flat glowing shapes on navy, small people and the continuous scale zoom
are the style; a particular studio's look is not.

## Proven on

The planet-to-galaxy zoom (9 s): four part-sheet characters walking round a small home planet with moon and satellites, a push out to its star and orbits, and a
push out to a spiral galaxy with a "you are here" mark.
