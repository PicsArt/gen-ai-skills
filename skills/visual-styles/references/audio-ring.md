# Audio ring

A music visualiser: a ring of bars pulses round a centre disc to a beat, a soft glow breathes with it, particles
drift outward and a thin title sits below. Dark ground, a cyan-to-violet ring.

## Palette

Ground `#0a0a14`, ring gradient from cyan `#22e0c8` through blue `#4a7bff` to violet `#a45cff`, white text.
**The hero colour is the cyan end `#22e0c8`, reserved for the loudest bars and the centre disc's rim.**

## The medium

- **A ring of bars:** 48 short rounded rectangles around a circle, each a layer or a repeater copy rotated by
  7.5 degrees; each bar's colour follows its angle round the gradient.
- **A centre disc:** a dark circle with a thin cyan rim holding a mark or a title initial.
- **Glow:** a soft radial gradient behind the ring and a `glow` effect on the bars.
- **Particles:** small dots from a particle field on a shape layer, moving outward and fading.

## Motion habits

- **No audio-reactive input exists today.** The bars cannot follow a sound file, so author the beat: a fixed
  pattern of bar-length keys on a 0.5 s period (120 beats a minute), with each bar's pattern offset by its
  index in a script, so the ring appears to ripple. State this plainly when the user expects a real analysis.
- **Beat pulse:** the disc scales `[1, 1.08, 1]` and the glow's opacity lifts on each beat, on a looping track.
- **Settle in:** at the start the bars grow from zero in a wave round the ring over 0.8 s.
- **Particles** emit on the beat (burst rate keyed) and drift outward.
- Cued layers use `timeMode: "layer"`.

## Type

A light-weight grotesque for the title and artist line, white at 80 %, small, below the ring.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Bars are evenly spaced and equal in width.
2. The loudest bars are the cyan ones.
3. The beat period is constant and the loop closes.
4. Glow never hides the bars.
5. The title does not overlap the ring.

## Build with the tools

Generate bar keys from a seeded pattern in a script, indexing the offset by bar number; keep the whole ring in one
nested composition so the loop period is set once. Check a beat on a contact sheet.

## Do / don't

- **Do** keep bar lengths at 40-100 % of the maximum so the ring never collapses.
- **Don't** claim the bars follow a track; they follow the authored pattern.

## Originality guard

Design your own ring, disc mark and title. It must not copy a streaming service's visualiser, a record label's
logo or a known music app's artwork. The ring of bars on a beat is a generic convention.

## Proven on

The visualizer-ring film (a ring of bars pulsing to an authored beat round a centre disc, glow, drifting
particles, a title).
