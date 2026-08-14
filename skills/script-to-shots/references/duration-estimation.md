# Duration estimation

How to get a number out of a page. Dialogue is the only part of this with a reliable basis, so
everything else names its method and admits it is an estimate.

Every estimate is written with its method in brackets. `5 seconds` on its own is a guess wearing
a number.

## Dialogue, the reliable anchor

Spoken English runs at roughly 150 words per minute, so about 2.5 words per second.

**Count the words.** Not the characters, not the lines, not the feel of it. Counting is the whole
method and it takes 5 seconds.

| words in the line | speech alone | with a beat at each end |
|---|---|---|
| up to 9 | under 4 seconds | fits 5 |
| 10 to 12 | around 5 seconds | needs 10 |
| 13 to 22 | 5 to 9 seconds | fits 10 |
| more than 22 | over 9 seconds | split the line |

Write it as: `5 seconds [dialogue, 8 words at 2.5 per second plus 1 second of beats]`.

### Beats at each end

Add roughly 0.5 seconds before the line and 0.5 seconds after, every time.

A clip that starts mid-word is unusable, and there is no fix in the edit. A clip that ends on the
final consonant of the last word has nothing to trim, so it cannot be cut against the next clip
without a hard join that reads as a mistake.

So a 5 second chunk holds about 4 seconds of speech, which is about 9 words. That is the number
that drives most of the splitting decisions in this skill.

### Pace that is not 150 words per minute

Adjust when the script tells you to, and say that you did:

| the line is | words per second | note |
|---|---|---|
| Conversational, the default | 2.5 | Use this unless something says otherwise |
| Energetic, a feed edit, a hard sell | 3 | Roughly 180 words per minute |
| Slow, weighted, a reveal, grief | 2 | Roughly 120 words per minute |
| Broken by an explicit pause in the script | 2.5 plus the pause | Count the pause separately, and say how long you allowed |

A parenthetical such as `(beat)` or `(long pause)` is time on the page. Allow 1 second for a
beat and 2 for a long pause, and put that in the brackets.

### Overlapping dialogue

2 characters talking over each other is not 2 lines of time, it is roughly the length of the
longer line plus 1 second. It is also 1 of the hardest things to generate, so flag it and offer
to make it consecutive instead.

## Action without dialogue

There is no word count, so pick a method, use its number, and name it. These are estimates and
you say so.

| what happens | allow | write it as |
|---|---|---|
| 1 completed gesture: a head turn, a hand reaching, a door opening, a lid closing | 2 to 3 seconds | `[action, 1 gesture]` |
| 2 gestures in sequence in the same frame | 5 seconds | `[action, 2 gestures at about 2.5 seconds each]` |
| A held image with nothing moving | 2 to 3 seconds | `[held frame, reads as a still past 3 seconds]` |
| A facial reaction, no words | 2 seconds | `[reaction, 2 seconds]` |
| A character walking a distance | distance in metres divided by 1.4 | `[travel, 7 metres at walking pace]` |
| A character running | distance divided by 4 | `[travel, 20 metres at running pace]` |
| A vehicle crossing frame | frame width in metres divided by the speed in metres per second | `[travel, vehicle crosses a 12 metre frame at 8 metres per second]` |
| A slow camera push or pull across a room | 4 to 5 seconds | `[camera, slow push across a 6 metre room]` |
| A pan or a tilt onto a subject | 3 seconds | `[camera, pan onto the subject]` |
| An orbit of a quarter turn | 4 seconds | `[camera, quarter turn orbit]` |
| On screen text a viewer has to read | words divided by 4, minimum 2 seconds | `[reading, 9 words of silent reading]` |
| A transformation, a build, an assembly | 5 seconds, and split it if the script describes stages | `[process, 1 stage]` |

Two things these numbers assume. The action is unhurried, because a rushed gesture in a
generation reads as a glitch. And there is 1 action per chunk, because 2 actions in a 5 second
clip is the reliable way to get a subject that morphs halfway through.

## Estimating a scene

1. Split the scene into its spoken lines and its unspoken actions.
2. Time each line by counting words.
3. Time each action by the table above, and name the method.
4. Add the beats: 0.5 seconds at the head and 0.5 at the tail of the scene, plus 0.5 between a
   line and an action that follows it.
5. Sum, and round up to the nearest half second. Rounding down is how a line gets clipped.

Then hand the total to stage 4 of this skill's `SKILL.md`, which chooses the unit.

## When the estimate is uncertain

Say so, and put it in `<shots>/manifest.json` as an open question rather than picking a number
and hoping. The cases that come up:

- **The script says something vague.** `They argue for a while` is not a duration. Ask how long,
  or propose a beat count and say it is a proposal.
- **The scene describes a state, not an action.** `The city is quiet` holds for 3 seconds and
  then needs something to happen. Say that.
- **A montage.** Each item is its own chunk of 2 to 3 seconds, but generators do not reliably
  make a clip shorter than their minimum unit, so plan each item as a 5 second chunk to be
  trimmed in the edit, and say that is what the extra seconds are for.
- **Dialogue that will be recorded separately.** Time it from the words anyway, because the
  picture still has to cover it, but note that the picture can be cut on the action instead if
  the recording comes in shorter.

## Do not do this

- Do not write a duration with no bracket.
- Do not estimate a spoken line by eye. Count it.
- Do not round a total down to hit a unit. If a scene is 5.5 seconds it does not fit 5, and
  pretending it does produces a clip with the last word missing.
- Do not add seconds to a chunk to make it feel more substantial. Empty time at the end of a
  clip is where a model puts drift.
