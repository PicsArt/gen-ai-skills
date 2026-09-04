# The single pass form

For a piece that nothing forces you to split. One generation, one file, with the beat structure
inside the prompt.

Use this only after the stage 0c check says nothing requires a cut. If any beat needs a spoken
line, go back to separate chunks.

## Why the structure still matters

A single long prompt is not one shot held for a minute. Without internal structure a generator
gives you one slow drift, which is worse than any chunked version. The beats are what make it
read as a sequence, and the camera change at each beat is what makes the beats visible.

The advantage you are buying is that the shared description is stated once and applies
throughout, so the cast and the style cannot drift between beats the way they can between
separately generated clips. Do not throw that away by repeating the description per beat, which
invites the model to reinterpret it mid-clip.

## The form

```
STYLE: <one string for the whole clip>
CHARACTERS: <every character on screen, once, for the whole clip>
SETTING: <the one location>
AUDIO: <the theme first, then the ambience, then any non-verbal sounds and roughly where they
        fall. 1 string for the whole clip>
NEGATIVE: <one string for the whole clip>

BEAT 1, 0 to 6 seconds
ACTION: <one thing happening>
CAMERA: <shot size, angle, movement>

BEAT 2, 6 to 13 seconds
ACTION: ...
CAMERA: <a different shot size or angle from beat 1>
TRANSITION: cut

BEAT 3, 13 to 20 seconds
...
```

## Rules

- **Every beat changes the camera.** Two consecutive beats at the same shot size and angle read
  as one long shot with activity wandering through it. That is the failure this form exists to
  prevent, and it is the one thing most likely to be skipped.
- **Six to ten seconds per beat.** Shorter and the model will not complete the action. Longer
  and it starts inventing.
- **Name the transition** where a hard cut is wanted. Left unsaid, a generator dissolves or
  glides between beats.
- **Keep the running total in the beat headings**, as above, so it is obvious whether the whole
  thing fits the model's maximum duration. Check that before writing, not after.
- **Non-verbal sound goes in the AUDIO line** with a rough position, not in a beat. It does not
  need to land on a frame, which is why this piece qualified for one pass in the first place.
- **The theme music goes in the AUDIO line too, and this is the only form where it truly plays
  throughout.** There is 1 generation, so there is 1 take of the music and no join for it to
  restart at. A chunked set cannot do that, which is a real argument for one pass whenever the
  piece is short enough and has a score. State the theme as instruments, a tempo in numbers, a key
  and what the music is doing, and state it once.

## What goes in SHOTS.md

Say plainly that this is a single generation, give the total duration and the beat count, and
say why splitting was not needed: no dialogue, one location, nothing landing on a frame. Someone
opening the project later will otherwise assume the chunking step was skipped by mistake.

Do not also write per chunk files. Two versions of the same piece is how the wrong one gets
generated.
