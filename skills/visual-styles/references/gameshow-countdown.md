# Gameshow countdown

A quiz-show countdown: a ring of lights runs round a clock face, the number in the middle changes each second
with a punch, a buzzer flash ends it and the answer reveals with confetti.

## Palette

Stage `#1b0f3a` to `#3b1d6e`, gold `#ffcf3f`, white `#ffffff`, light bulbs warm `#fff1b8`. **The hero colour is
the ring pink `#ff4fa3`, reserved for the countdown ring and the final flash.**

## The medium

- A **ring** (an ellipse stroke, 18 px) with a keyed `trim` that unwinds as time runs out, with 24 bulbs around
  it: small circles on a repeater is fine (one per group); each bulb lights in turn.
- **The number** in the middle in a heavy display face, white with a gold outline.
- **A buzzer flash:** a full-frame pink wash with a short life.
- **Confetti:** small coloured rectangles from a particle field on a shape layer.
- **The answer:** a gold rounded panel with dark text.

## Motion habits

- **The ring unwinds:** `trim` end keys 1 to 0 over the whole count, linear, so the pace is steady.
- **Each second punches the number:** scale keys `[1.5, 0.9, 1]` over 0.35 s with a fade of the previous digit;
  the number is one text layer whose `text` is an expression returning the whole second (`mp.formatNumber`), so
  it changes exactly on each second; use a face with tabular figures so the digits keep their width.
- **Bulbs chase:** each bulb's opacity pulses in turn, with offsets 1/24 of the period, looping.
- **Buzzer:** the flash keys 0 to 0.8 to 0 over 0.25 s; the number shakes with the `wiggle` preset for 0.4 s.
- **Reveal:** the answer panel scales in with an overshoot while the confetti fires.
- Cued layers use `timeMode: "layer"`.

## Type

A heavy display face for numbers and the answer; a clean grotesque for the question.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. The number changes exactly on each second.
2. The ring finishes at the buzzer, not before.
3. Pink is the ring and the flash only.
4. The answer is readable the moment it lands.
5. Confetti never covers the answer.

## Build with the tools

Write the number as one counting text layer (an expression on `text`); key the ring `trim` linearly; apply `wiggle` to the
number layer for the shake; build confetti with the particle field. Check each second with `picsart_scene_contact_sheet`.

## Do / don't

- **Do** keep the ring thick enough to read on a phone.
- **Don't** reuse a real show's set, logo, sound cues or format name.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Height is shadow: no cast shadows on this stage; the number and the answer panel read as nearer only by the scale punch and the overshoot above, and nothing sits on a surface that would shade it.

## Originality guard

Invent your own quiz, stage and wording. It must not copy a real game show's set design, logo or catchphrase.
The ring of lights, the punching numbers and the buzzer are generic conventions.

## Proven on

The countdown-gameshow film (a pink ring unwinding round a clock, punching numbers, a chasing bulb ring, a buzzer
flash and an answer reveal with confetti).
