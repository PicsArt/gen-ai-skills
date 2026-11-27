# Retro-futurism

The space-age future as a 1950s-60s cartoon drew it: a dusk sky that burns from violet to apricot, a ringed
planet, a boomerang-roofed house with an atom sign, a saucer and a rocket. Heavy ink outline, flat colour, a
wink in every prop.

## Finish

The stepped parts (stars, flame, smoke) at `fps` 12 under a 24 fps root in a nested composition, with a flame flicker (see Motion habits).

## Palette

Ink `#1d1630`, cream `#fff3dc`, teal `#3fc1b0`, orange `#f2a65a`, lilac `#9b7fd1`, ground `#2a1f47` and `#21183a`.
The sky is the one gradient: `#1b1440` to `#4a2f7a` to `#d9677a` to `#f7b267`, top to the horizon. **The hero
colour is the signal red `#e5484d`, reserved for the craft** (rocket fins, the sign's ball) and used nowhere in
the world.

## The medium

- Every solid has an ink outline of one weight (5-6 px) and a flat fill. Nothing is shaded; the gradient sky is
  the only blend.
- Stars are four-point `star` items of cream, small and many. A planet is a disc with a lighter blob inside it
  and a ring drawn twice, a back arc behind the disc and a front arc over it, so the ring passes round it.
- Googie shapes: a boomerang roof (an open two-segment stroke), a house of one tilted slab with square lit
  windows, a pole with a ball and three thin orbit ellipses (the atom sign), a launch pad on two struts.
- A rocket is a cream body with a glass porthole, two red fins and a flame (a yellow teardrop with an orange
  line). A saucer is a lilac lens, a glass dome and a row of yellow lights. Smoke is cream discs with an outline.
- A place is a horizon band of dark violet shapes under the sky; the title sits in cream over the dark ground.

## The character

Drawn from the style's own shapes, not a generated sheet (the mechanism, saving and talking are in [shapes-character](shapes-character.md)); build once, save once to the library, place it by its `uri` in every shot.

- **Proportions:** about 5.5 heads tall: a round helmet on a boxy suit.
- **Shapes:** a circle helmet with a darker visor oval, a trapezoid suit and **puffy bodied limbs**: each sleeve and trouser leg is one closed tapered shape that grows out of the suit's outline (a sleeve about half the torso's width at the shoulder), the glove is the sleeve's own rounded end and the boot the leg's own end, one outline per limb, no tube laid across the suit; flat colour, an ink outline.
- **Face:** two dot eyes inside the visor and a brow tick; `mouth` rest, `aa`, `oh` as a small slab, an oval and a square inside the visor.
- **Controls:** the base set; the arm dials point at the rocket or the planet.

## Motion habits

- Put the stepped parts (stars, flame, smoke) in a nested composition layer with `fps` 15 (12 under a 24 fps root) and key them with
  plain keys; the larger moves (saucer, rocket) stay on the full rate. No time-floor expressions.
- **Twinkle** is the `random_hold` preset on each star's scale (a different `seed` per star). **Rumble** before
  lift-off is the `wiggle` preset on the rocket for a second, then a long ease-in rise (`[0.6, 0, 0.9, 0.5]`):
  slow, slow, gone. **Flame flicker** is `wiggle` on the flame's scale.
- The saucer swoops in on a wave (position keys with an ease-out, a rotation that settles), hovers with a small
  bob, then streaks off along a rising curve after the rocket.
- Smoke puffs bloom one after another from the pad: scale up with an ease-out, drift apart, fade late.
- Cued layers use `timeMode: "layer"`.

## Type

A condensed all-caps display face in cream, spaced wide, set low on the frame and faded in late.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. The craft is the only thing in the hero red.
2. Dusk gradient sky, a ringed planet and at least five stars.
3. Two googie props on the ground (a roofline and a sign).
4. One outline weight on every solid.
5. Something is leaving or arriving: a saucer, a rocket, a trail.

## Build with the tools

Draw each prop as one shape layer; build the planet as three layers (back ring, disc, front ring). Nest the
stepped pieces in a `composition` layer with `fps` 15 and apply `random_hold` and `wiggle` with
`picsart_scene_apply_preset` to the layer ids inside it. Place the whole picture in a `scene` asset with one
`scene_ref` and a light grain look.

## Do / don't

- **Do** let the craft overlap the planet or the sign so the depth reads.
- **Don't** shade the planet or add a glow to the flame; a second gradient breaks the flat look. Don't use red
  on the ground or the title.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Line width under a zoom: no zoom, width fixed at 5-6 px (see The medium).

## Originality guard

Invent the world and the craft. It must not resemble a known space-age family's cast, house or flying car, a
famous robot, a known series' saucer or rocket design, or a studio's logo or title card. Keep the googie shapes,
the dusk and the flat ink-and-colour; change the silhouettes.

## Proven on

The orbit-avenue film (dusk planet, atom-sign house, a saucer that swoops in, a rocket that lifts off, smoke, a
late title).
