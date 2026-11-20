# Firefly night

A dark meadow under a pale moon: lit insects drift up from the grass and fade, a layer of hills and foreground
blades makes the depth, and one glow lifts the swarm. Quiet, slow and mostly dark.

## Palette

Sky `#0b1026` to `#22304f`, hills `#0f1a24`, foreground grass `#05090d`, moon `#f3efd6`. **The hero colour is
the firefly lime `#e9ff8a`, reserved for the swarm**; nothing else in the frame is lit.

## The medium

- A **gradient sky**, a pale **moon** (a solid disc with a very faint larger halo disc at 8 % opacity), a set of
  **hills** as one closed path in a near-black blue, and **foreground blades** as thin triangles in an even
  darker tone along the bottom edge.
- **The swarm is a particle emitter**, not many layers: one shape layer whose content is the sprite (a 10 px
  ellipse in lime) and a `particles` field on the layer: a box origin across the meadow (about 1200 by 120), a
  rate of about 14 a second, a life of 2.5-4.5 s, direction straight up with a spread, a slow speed (15-45), a
  slight upward gravity, a size range, and an opacity-over-life curve that fades in, holds and fades out.
- The layer carries the `glow` effect (threshold about 20, radius about 30, intensity about 2.5), so the bright
  sprites bloom and the dark ground does not.

## Motion habits

- Particle motion is the swarm's motion; set the `seed` so it repeats. Start it before 0 (a negative `start`)
  so the meadow is already alive in the first frame.
- Grass blades **sway**: hand-keyed alternating rotations of 4 degrees about their base, each blade's period a
  little different, rather than a shared sway.
- The moon is still. Add a very slow `wiggle` to the halo's opacity if the sky needs a pulse.
- Cued layers use `timeMode: "layer"`.

## Type

Usually none. A title, if used, is a small light serif in a pale tone low in the frame, fading in and out.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. The swarm's lime is the only light in the frame besides the moon.
2. The glow sits on the swarm layer only.
3. The swarm is already running at the first frame.
4. Three depths: sky, hills, foreground blades.
5. Particles fade in and out; none pops on or off.

## Build with the tools

Build the layers and add the `particles` field to the swarm layer with the sprite as its content; use the
schema (`picsart_scene_capabilities`) for the particle fields. Add the `glow` effect to that layer. Check a frame
for a swarm that is neither bare nor a cloud.

## Do / don't

- **Do** keep the swarm sparse; fifty small lights beat two hundred.
- **Don't** add a second glow to the moon, a bright horizon or a lit window; don't draw each insect as a layer.

## Originality guard

Design your own meadow and moon. It must not copy a known film's firefly scene, a game's menu art or a named
photographer's long exposure. The dark gradient, the drifting lights and the single glow are the style.

## Proven on

The firefly-meadow film (a gradient night sky, a moon, hills, a lime firefly particle swarm with glow, swaying
foreground grass).
