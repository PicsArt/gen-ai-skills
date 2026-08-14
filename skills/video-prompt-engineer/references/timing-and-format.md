# Timing and format

Settle these before anything else. Both change what a composition can hold.

## Aim for 5 seconds, accept 10, avoid longer

Generation is billed per clip and fails often, so the length you ask for is a bet on how much
you are willing to lose. A failed 20 second clip costs four times a failed 5 second one, and
the odds of failure rise with duration because there is more time for a subject to drift, a
hand to deform or a style to wander.

So the default is **5 seconds**, and the question is not "how long should this be" but "what is
the smallest unit that still makes sense".

| the shot contains | ask for |
|---|---|
| One gesture, one camera move, no speech | 5 seconds |
| A single short spoken line | 5 seconds if the line fits, see below |
| A spoken line that will not fit in 5 | 10 seconds |
| Two actions, or a line plus a reaction | Two chunks of 5, not one of 10 |
| Anything you estimate above 10 seconds | Split it. Do not ask for 20 |

**Longer is not more efficient.** One 20 second clip that fails costs more than four 5 second
clips of which one fails, and the four can be regenerated individually.

## When one long generation beats several short ones

The 5 second default assumes the usual case: dialogue, or an action that has to land at a
particular moment. Some work has neither, and for that work the arithmetic reverses.

The reason to chunk is that a failure is cheap and a long clip drifts. But chunking has a cost
that is easy to forget: **every boundary between separately generated clips is a place where
the style, the cast or the light can fail to match**, and nothing carries across a boundary
except the words you repeat. A piece with no dialogue and a forgiving style is exactly the case
where one generation removes that whole class of problem at a stroke.

So ask what actually forces a cut, and if nothing does, consider generating the lot in one pass.

### What forces chunking

Any one of these and you chunk. They all need something to happen at a precise moment.

- **Spoken dialogue**, because lip sync has to match a specific waveform.
- **On-screen text** appearing or changing at a set point.
- **Music sync**, where a cut or a movement lands on a beat.
- **A plot beat that must be readable**, such as an object being handed over or a door opening
  at the moment someone arrives.
- **A change of location or cast**, which is a new setting to describe.
- **The model's maximum duration**, which is a hard limit rather than a judgment.

### What does not force chunking

- **Non-verbal sound.** A sigh, a gasp, a laugh, "uhh", "ohh", humming, an animal noise. None
  of these needs frame-accurate lip sync, so none of them forces a cut. Describe the sound and
  when it happens, and let it fall where it falls.
- **Several beats of action**, as long as no single one has to land on a specific frame.
- **Camera changes.** These are cheap to describe inside one prompt and are not a reason to
  split, which is the thing most people get wrong here.

### The judgment

| the piece has | do |
|---|---|
| No dialogue, one location, small cast, forgiving style | One generation, up to the model's limit |
| No dialogue but several locations | One generation per location |
| Non-verbal sound only, simple action | One generation |
| Any spoken line | Chunk, 5 or 10 seconds each |
| A beat that must land precisely | Chunk around that beat |
| Photoreal human faces held in close-up | Chunk, because drift is most visible there |
| The user cannot afford a failed long render | Chunk, and say that is why |

**A children's cartoon of animals playing, with no dialogue, is the clearest case for one
generation.** One setting, forgiving style, nothing that has to land on a frame, and the thing
that would otherwise be hardest, keeping the animals looking like themselves across shots,
becomes free because there are no shots to match.

Ask about the budget for a failure before committing to a long render. One 60 second attempt
that fails costs what twelve 5 second clips would have cost, and the user may or may not mind.

### Writing the long one

A single long prompt is not one shot held for a minute. Without internal structure a generator
gives you one slow drift, which is worse than any chunked version.

State the beats inside the prompt, and change the camera at each one. Aim for a change every 5
to 10 seconds, exactly as if you were chunking, but express it as a sequence within one prompt:

- Give each beat its **duration**, its **action**, and its **camera**, in that order.
- **Change something visible at every beat**: shot size, angle, or the direction of movement.
  Two consecutive beats at the same shot size read as one long shot with something wandering
  through it.
- Keep the style, palette, lighting and cast description **once at the top**, applying to the
  whole clip. That is the advantage you are buying, so do not repeat them per beat.
- Name the transitions as cuts if you want cuts. A generator will otherwise dissolve or drift
  between beats.

See `references/structure.md` for the form.

## Timing a spoken line

Count the words. Spoken English runs at roughly 150 words per minute, so about 2.5 words per
second, and that is the only estimate here with a reliable basis.

| words | speech alone | with a beat either side |
|---|---|---|
| up to 9 | under 4 seconds | fits 5 |
| 10 to 12 | around 5 seconds | needs 10 |
| 13 to 22 | 5 to 9 seconds | fits 10 |
| more than 22 | over 9 seconds | split the line |

Always add roughly half a second before the line and half a second after. A clip that starts
mid-word is unusable, and a clip that ends on the final consonant cannot be cut against
anything.

Count the words rather than guessing at the duration. "It sounds like about five seconds" is
how a 12 second line ends up in a 5 second clip with the end cut off.

## Write the text so it can be split

When you are writing or rewriting dialogue and narration for generation, write it to be
divisible. This costs nothing at the writing stage and saves a re-write later.

- **One idea per sentence**, and keep sentences under about 12 words so each one fits a single
  chunk.
- **Break at natural pauses.** A full stop, a question, or a change of who is speaking is a free
  chunk boundary. A subordinate clause in the middle of a sentence is not.
- **Avoid a sentence that must be heard whole** to make sense, because it cannot be split at
  any price.
- **Do not carry a gesture across a boundary.** If a line is delivered while pouring a drink,
  either the pour completes inside the chunk or the line moves.
- **Put the emphasis early.** If the clip has to be trimmed, the end is what goes.

If the user hands you a paragraph of narration, offer to rewrite it into divisible lines and
say what you changed. If they hand you a long script, that is `script-to-shots`, and say so
rather than doing it inline.

## Duration

How long the clip runs. Models hold a shot for a fixed span. Naming the length stops a model compressing a three beat idea into one, or padding a single beat with drift.

**Vocabulary.** 6 seconds, 8 seconds, 10 seconds, 15 seconds, 30 seconds, 60 seconds, 4-15s, 2-15s, 3-15s, 4, 6, 8, 10, 12, 15, 5, 4 s, ~15s, one to ten whole minutes

**Examples.**

- `15-second cinematic clip.`
- `Six seconds, one continuous take, no cuts.`
- `30 seconds in three beats of roughly ten seconds each.`

## Aspect ratio

Frame shape. Decides whether the subject can breathe. A vertical crop of a wide composition loses the sides, so the ratio has to be chosen before the composition is described.

**Vocabulary.** 16:9, 9:16, 1:1, 4:3, 3:4, 21:9, auto, 3:2, 2:3, 9:21, 4:5, 5:4, 1.91:1

**Examples.**

- `Framed 16:9 for landscape playback.`
- `Vertical 9:16, composed for a phone held upright.`
- `Square 1:1 with the subject centred.`
