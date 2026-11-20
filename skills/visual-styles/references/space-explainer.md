# Space explainer

A flat science explainer on a deep blue sky: a ringed planet, a field of stars, and a small rocket that lifts
off, spirals out and settles into an elliptical orbit with its nose always along the path.

## Palette

Sky `#14163a`, planet `#ff8a5c` with darker patches `#e86a3e`, ring `#ffd9a0`, stars `#ffffff` at varied
opacity, rocket body `#f2f2f2`, window `#5bc0eb`, flame `#ffd23f`. **The hero colour is the rocket's red
`#e84855`, reserved for its fins**; nothing else in the frame is red.

## The medium

- A flat navy sky with about ninety stars (3-6 px circles, seeded random positions and opacities 0.4-1).
- **The planet** is a disc with two darker round patches; **its ring** is an ellipse (460 by 90) tilted -12 degrees,
  drawn twice: a back half behind the planet and a front half in front (each a half-length `trim` of the same
  ellipse), so the rocket can pass between them.
- **The rocket** is a nose-up group of flat shapes: a cream body path, a round window, two red fin triangles and a
  flame triangle. Make two copies, one behind the planet and one in front, and switch between them at the half
  orbit by opacity steps.
- A path to follow: a faint orbit ellipse, an invisible **leader** layer that the rocket follows.

## Motion habits

- The rocket **follows the leader**: give it an `attach` constraint to the leader with a small lag (about 0.08 s)
  and an `aim` constraint along its nose axis, so it banks round the curve by itself. Alternatively set
  its rotation to `positionDirection()` of its own motion.
- The leader runs a **spiral out to an ellipse**: position keys on a smooth curve from the planet's surface,
  radius growing over about 2.5 s to the orbit, then circling. Keep keys on whole frames; ease in and out on the
  launch.
- **Flame flicker** is the `wiggle` preset on the flame's scale at a high frequency. Stars twinkle with
  `random_hold` on their opacity, a few at a time.
- Cued layers use `timeMode: "layer"`.

## Type

Labels in a clean grotesque in white; one number or name per label, with a thin leader line.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. The rocket's nose points along its path at every frame.
2. The ring passes behind and in front of the planet.
3. The rocket is the only red.
4. Stars are many and small and never brighter than the labels.
5. Three or more labels or marks explain what the viewer is seeing.

## Build with the tools

Build the planet, ring halves, stars and two rocket copies as shape layers; give the leader a position track; add
the `attach` and `aim` constraints to the rocket (see the constraint schema with `picsart_scene_capabilities`).

## Do / don't

- **Do** switch rocket copies on a frame when the rocket is hidden by the planet.
- **Don't** shade the planet or add a glow to the flame; don't use perspective.

## Originality guard

Design your own planet and craft. They must not copy a known mission patch, a space agency's logo or rocket, or
a famous explainer channel's character. The flat planet, the half-and-half ring and the path-following craft are
the style.

## Proven on

The orbit-space-explainer film (a ringed planet and stars, a rocket launching and spiralling into an elliptical
orbit with its nose forward).
