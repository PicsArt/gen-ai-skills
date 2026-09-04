# Worked examples

How a page becomes a set of chunk files, including what to ask and what to say back.

## From prose

**In**, pasted with no other instruction:

> Maya comes into the kitchen early. It is barely light. She sees a folded note on the table,
> picks it up and reads it out loud: "I have gone to the coast for a few days, do not worry about
> the shop, I have asked Tomas to open up." She puts it down and looks out of the window for a
> long time.

### Stage 0, ask

```
5 things and I can cut this up:
1. Which model is generating? (decides the chunk lengths available)
2. What durations does it offer? (suggest 5 and 10, and I will avoid 20)
3. Aspect ratio? (suggest 9:16 for a feed, 16:9 otherwise)
4. Audience, and anything that must never appear?
5. Is the dialogue generated with the picture, or recorded and laid over afterwards?
```

Answered: `seedance, 5 and 10, 16:9, general audience, dialogue is generated`. No style guide, so
you say once that `style-guide-builder` would fix consistency properly, and then ask the 3 things
the prose does not give you: what Maya looks like, what she is wearing, and what the kitchen looks
like.

### Stage 2, boundaries, then STOP

```
I read this as 2 scenes. Say continue, or tell me to merge or split:
1. Kitchen, dawn, Maya alone. She enters, finds the note, reads it aloud
2. Kitchen, continuous. She puts the note down and looks out of the window
```

The reading and the looking are 1 location and 1 character, so they could be 1 scene. They are 2
because the subject of attention changes, from the note to the window, and that is a boundary.

### Stage 3, estimate

The spoken line is 24 words. 24 divided by 2.5 is 9.6 seconds, plus 1 second of beats is 10.6,
which does not fit 10. So the line has to be split, and it splits at the comma after `few days`
because that closes a complete clause.

| scene | element | estimate |
|---|---|---|
| 1 | She enters and crosses to the table | 5 seconds [action, 2 gestures at about 2.5 seconds each] |
| 1 | She picks up the note and unfolds it | 5 seconds [action, 2 gestures at about 2.5 seconds each] |
| 1 | "I have gone to the coast for a few days," | 5 seconds [dialogue, 10 words at 2.5 per second plus 1 second of beats, so 5 exactly, rounded to the 10 second unit] |
| 1 | "do not worry about the shop, I have asked Tomas to open up." | 10 seconds [dialogue, 14 words at 2.5 per second plus 1 second of beats] |
| 2 | She puts the note down | 5 seconds [action, 1 gesture] |
| 2 | She looks out of the window | 5 seconds [held frame with a slow push, reads as a still past 3 seconds without the camera move] |

The third row is the interesting one. 10 words at 2.5 per second is 4 seconds, plus 1 second of
beats is 5 seconds exactly, and exactly 5 does not fit 5, because there is no trim handle. So it
takes the 10 second unit. Say that in the file rather than leaving a reader to wonder why a short
line got a long clip.

### Stage 4, running order, then STOP

```
6 chunks, 40 seconds total, 4 at 5s and 2 at 10s.
The spoken line is 24 words so it splits at the comma after "few days".
Both halves take 10s because a line that fills 5s exactly has no trim handle.
Say continue, or name a chunk to change.
```

### Stage 7, one of the 6 files

`<shots>/003-note-line-one.md`:

```markdown
# 003 Maya reads the first half of the note

## Duration

10 seconds

## Prompt

<the fenced prompt, in the clause order from `references/output-files.md`, carrying the setting, the wardrobe,
the light and the exclusion line copied from `<shots>/shared.md`>

## Motion only prompt

<the fenced short version, for when the last frame of 002 is passed as the first frame>

## Continuity in

- Pose: standing at the table, both hands holding the unfolded note at chest height
- Position: frame left, 1 metre from the table edge, window behind her right shoulder
- Expression: reading, eyes down at the paper
- Framing: medium shot, eye level, camera at rest

## Continuity out

- Pose: standing at the table, both hands holding the unfolded note at chest height
- Position: frame left, 1 metre from the table edge, window behind her right shoulder
- Expression: reading, eyes down at the paper
- Framing: medium shot, eye level, camera at rest

## Estimate basis

10 words at 2.5 words per second is 4 seconds, plus 0.5 seconds of beat at each end is 5 seconds
exactly. Exactly 5 leaves no trim handle, so this takes the 10 second unit and holds on the
reading at the end.

## Inherited from

Scene 1. Setting, wardrobe, time of day, lighting, palette, mood and exclusions from
`<shots>/shared.md`. Maya's description was not in the script and was asked for in stage 0.

## Notes

The line continues into 004. Do not generate an opening breath or a closing pause here, and do
not let her look up at the end. First frame: the last frame of `<shots>/002-picks-up-note.md`. When using
the motion only prompt, do not redescribe the kitchen or the wardrobe.
```

Note that Continuity out repeats Continuity in word for word, because nothing moves except the
mouth. That is not laziness, it is the point: chunk 004 opens on those same 4 sentences.

## From a script that is already split

**In**: 8 scenes with headings, and durations already written on them.

Do not trust the durations. Re-estimate every scene from the words on the page and compare:

```
I re-timed all 8. 5 match what you had. 3 do not:
- Scene 2 is marked 5s and the line is 15 words, which needs 10
- Scene 4 is marked 8s, and 8 is not a unit your model offers, so it is 10 or 2 chunks of 5
- Scene 7 is marked 20s. That is 4 failed 5s clips in 1 billing event. It splits into 4
```

Scene 7 is the case this skill exists for. The user had a working plan that would have cost 4
times as much on every retry.

## From a complaint about the joins

**In**: "I generated 12 chunks and they do not cut together."

Do not re-split. Read `references/splitting.md` and check the copying first, because that is the
cause more often than the boundaries are:

1. Compare the style line in all 12 chunk files against `<shots>/shared.md`, character by
   character. A single reworded line is enough.
2. Check whether every chunk states the wardrobe and the time of day, or whether some inherited
   them and some assumed them.
3. Check each boundary against the Continuity out of the chunk before it. If those 2 sentences
   differ, that join was never going to work.

**Report**: `3 chunks had the lighting line reworded, so the key light moves at those joins.
Fixed in <shots>/shared.md and recopied. Those 3 need regenerating, the other 9 do not.`

Naming which chunks need regenerating is the useful part of that report, because it is the part
that has a cost attached.
