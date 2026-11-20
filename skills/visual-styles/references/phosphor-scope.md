# Phosphor scope

An oscilloscope screen: a dark graticule, a glowing green trace that sweeps and changes waveform, readouts that
settle, and a faint afterglow that fades behind the beam.

## Palette

Screen `#050a07`, graticule `#16301f`, trace `#7dffa8` with core `#d9ffe6`, readout text `#7dffa8` at 80 %, bezel
`#1a1d1b`. **The hero colour is the trace green `#7dffa8`**; nothing else in the frame is saturated.

## The medium

- A **graticule:** an 8 by 6 grid of 1 px lines with finer ticks on the centre axes, in dark green.
- **The trace:** one open path, 5 px, in the trace green with a bright core stroke on top (2 px) and a `glow`
  effect.
- **The afterglow:** a second copy of the trace, wider and fainter, delayed by two frames.
- **Readouts:** small mono text at the corners (a frequency, an amplitude) and a trigger marker on the left edge.
- A rounded **bezel** and a slight vignette.

## Motion habits

- **Change the wave:** the path is a set of points whose y values are keyed per waveform (sine, square, a
  burst); interpolate between keys over 0.8 s with an ease-in-out so the shape morphs smoothly.
- **Sweep:** a trim window travels left to right, a short bright head with a fading tail (`trim` start and end both
  keyed), repeating with `ctx:loopOut("cycle")`.
- **Flicker:** the `wiggle` preset on the glow's opacity at a low amount, plus `random_hold` for a few frames of
  dimmer trace.
- **Readouts** change on whole-frame steps, never a tween.
- Cued layers use `timeMode: "layer"`.

## Type

Cutive Mono, in the trace green at reduced opacity; the single mono face fits the screen.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. The trace stays inside the graticule.
2. The glow is soft and does not wash out the grid.
3. Waveforms morph without tearing.
4. Readouts match the waveform shown.
5. One saturated colour only.

## Build with the tools

Build the trace as a polyline from computed samples (about 120 points); key the point sets per waveform with
`picsart_scene_apply_preset` only for the flicker. Compare frames with `picsart_scene_contact_sheet`.

## Do / don't

- **Do** let the afterglow lag the beam by a small, fixed amount.
- **Don't** add a rainbow of channels or a reflection of the room on the glass.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Line width under a zoom: no zoom, width fixed (5 px trace, 2 px core); a timebase or amplitude change resamples the points and never scales the stroke.
  - True data: the readouts (frequency, amplitude) are written by counter text from the same generator values that compute the trace samples, never typed; a small `SIM` tag in a corner says the signal is synthetic (ours); check readout against trace with `picsart_scene_query_layout`.

## Originality guard

Design your own scope face and readouts. It must not copy a real instrument maker's front panel, logo, model
name or menu. The green trace on a dark graticule is the style.

## Proven on

The phosphor-scope film (a graticule, a glowing green trace sweeping and morphing between waveforms, settling
readouts, an afterglow).
