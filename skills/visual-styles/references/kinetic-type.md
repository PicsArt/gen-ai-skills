# Kinetic typography

One word per beat on a flash-cut ground: each beat flips the palette and the layout, the word punches in with a
zoom, and the last three words stack into a lockup. Loud, fast and made only of letters.

## Palette

Near-black `#111111`, off-white `#f5f5f0`, red `#ff3b30`, yellow `#ffd60a`. Four grounds in rotation, each with
a paired text colour (white on black, black on red, black on off-white, black on yellow). **The hero colour is
the red `#ff3b30`, which carries the first emphasised word in the lockup** and is the loudest ground in the cycle.

## The medium

- Portrait 1080 by 1920. **A beat is a layer pair:** a full-frame colour layer and a text layer, both starting
  on the beat and lasting one beat. At 120 bpm a beat is 0.5 s.
- **Words** are very large in a condensed heavy face (420 px for short words, 520 px for single syllables), centred
  on a layout rotated through five positions: centre, high and tilted, low and tilted the other way, and a quarter
  turn left and right.
- **Lockup:** the last three words (emphasised words with their full stop) stack on a black ground at 300 px,
  each in its own colour (red, yellow, off-white).
- Only type and flat ground colour. No shapes, no images.

## Motion habits

- **Punch zoom:** each word's scale keys from 1.25 down to 1 over 0.18 s with an ease-out, so it lands hard on the
  beat.
- **Hard cuts only.** Grounds and words change on the beat with no crossfade; the beat grid is the whole clock.
- The lockup lines **rise 60 px out of a clip band over 0.25 s** (`mask.clip`, a hard edge, no opacity ramp), one per beat.
- Add a slight overshoot or a `wiggle` on a final word only; a motion on every word would flatten the beat.
- Cued layers use `timeMode: "layer"`, so each word's keys count from its own start.

## Type

A condensed heavy face in upper case, at the largest size that fits; words are one syllable or short.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Exactly one word per beat; the cut lands on the beat.
2. Palette and layout change on every cut.
3. The word fills at least two thirds of the frame width.
4. The lockup shows the final message in full.
5. Text contrast is high on every ground.

## Build with the tools

Write the words and beat length in a script, generate each ground and word layer with its start and duration,
and key the punch scale. Check with `picsart_scene_contact_sheet` that no two adjacent beats share a ground.

## Do / don't

- **Do** repeat a phrase with one word changed; the change is the message.
- **Don't** add images, soft transitions or more than two lines on a beat.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Arrivals: a word arrives by a hard cut on the beat with its punch zoom, and the lockup lines rise out of a clip as the motion line says (a motion-type style, not a drawn one); the hard cut is the only transition.
  - Easing: hard frames, keyed on whole frames; the one ease is the ease-out of the 0.18 s punch, and a final word may
    overshoot as above.

## Originality guard

Write your own words. They must not copy a known ad campaign's slogan, a famous speech's line, a brand's
tagline or a music video's lyrics. The one-word beats, the flashing palettes and the punch zoom are the style.

## Proven on

The loud-fast-kinetic film (a 120 bpm sequence of nine words on flipping grounds, ending in a three-line
lockup).

**Not proven:** the clip-band rise was shown on a three-word lockup, not inside a full title sequence.