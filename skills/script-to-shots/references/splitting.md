# Splitting and continuity

Where to put the cut, where never to put it, and what has to carry across it. A split in the
wrong place produces 2 clips that are individually fine and cannot be edited together, which is
worse than 1 long clip that failed, because it is not obvious until the joins are watched.

## Where to cut, best first

| boundary | why it works |
|---|---|
| A full stop at the end of a spoken line | The pause is already there. Nothing has to be manufactured |
| A change of who is speaking | The handover is the cut. This is the cheapest boundary in any dialogue scene |
| A beat or a breath marked in the script | The script has already given you the gap |
| A scripted cut or a change of shot | The edit was always going to be here |
| A change of subject or of who is being looked at | Attention moves, so the frame can too |
| The completion of a gesture | The hand is at rest, so the next chunk can start from rest |
| A change of camera framing | 1 move per chunk, so a second move is a second chunk |

## Where never to cut

| never | what happens |
|---|---|
| Mid-word | The chunk is unusable. There is no fix in the edit |
| Mid-gesture | The hand is in a different place at the start of the next chunk, so it teleports |
| Mid-turn of the head or body | The subject snaps back to the previous angle |
| Mid-camera-move | The move restarts from a different speed and it reads as a stutter |
| Mid-clause, inside a sentence | The line stops making sense, and a generated delivery cannot carry a suspended clause |
| Between a question and its answer, when both are in the same frame | The reaction lands in a clip that never saw the question |
| Inside a transformation or a build | The object is at a different stage of assembly on either side |

When a scene has no safe boundary, say so rather than forcing one. The answer is usually to
rewrite the line so it becomes divisible, and that is worth offering.

## Splitting a line of dialogue

Avoid it. A line under 22 words fits 10 seconds and should stay in 1 chunk.

When a line has to be split because it runs past 22 words:

1. Split at a full stop first. A sentence boundary inside a speech is a free cut.
2. Failing that, split at a comma that closes a complete clause.
3. Never split at a conjunction that leaves the first half hanging.
4. Repeat the last 2 or 3 words of the first chunk as lead-in context in the second chunk's
   notes, so whoever generates it knows what the mouth was doing.
5. Say in both chunk files that the line is continuous across the boundary, so nobody generates
   an opening breath in the second chunk.

If the dialogue is being recorded separately and laid over the picture, none of this applies to
the audio, only to the picture, and the picture can be cut on the action instead. Ask which it is
in stage 0, because it changes where the cut goes.

## Continuity across a boundary

Every chunk file carries a **Continuity in** and a **Continuity out** heading. 4 things go in
each:

- **Pose**: what the body is doing. `Standing, weight on the left foot, right hand at the table
  edge.`
- **Position**: where the subject is in the frame and in the space. `Frame left, 2 metres from
  the window.`
- **Expression**: the face at that instant. `Neutral, eyes down at the note.`
- **Framing**: shot size, angle and where the camera has come to rest. `Medium shot, eye level,
  camera at rest after the push.`

**The continuity out of chunk N and the continuity in of chunk N plus 1 are the same sentence,
word for word.** Not the same idea in different words. Copy it.

Write both even for the first and last chunk of a scene. The first chunk's continuity in tells a
generator what state to open on rather than inventing one, and the last chunk's continuity out is
what the next scene has to match if it is continuous.

## Last frame as first frame

Where the model supports image to video, this is the most reliable join available.

1. Generate chunk N.
2. Export its last frame.
3. Pass that frame as the first frame of chunk N plus 1.

Then chunk N plus 1's prompt **must not redescribe the frame.** The model already has the
setting, the wardrobe, the light and the face. Redescribing them fights the frame and produces a
subject that shifts in the first few frames of the clip. Prompt the motion only, and keep the
shared style and exclusion lines, because those still apply.

State this in the chunk file, under Notes, in the form:

```
First frame: the last frame of <shots>/004-maya-reads.md. Do not redescribe the frame. Motion only.
```

The chunk file still contains a complete standalone prompt for the case where the frame is not
available, and a shortened motion only version underneath it. Someone should never have to
reconstruct either one.

Not every model supports it. When the target does not, say so once and lean harder on the
continuity sentences instead.

## A camera move that continues across a boundary

Sometimes a single slow push has to run for 8 seconds. Do not split the move in the middle if
you can avoid it; use a 10 second chunk instead, which is what 10 second units are for.

When it genuinely has to span 2 chunks:

- Name the same move, in the same words, in both chunks.
- Give the first chunk `camera begins the push and does not arrive` and the second
  `camera continues the push already in progress and comes to rest`.
- Match the speed by naming a distance in each: `moves 2 metres closer` and
  `moves the final 2 metres`.
- Expect to trim a few frames at the join. That is normal and is why the beats exist.

An orbit or a whip pan cannot be split this way. Change the shot instead.

## Overlap for the editor

Where the generator allows it, ask for roughly 0.5 seconds of extra time at each end of a chunk
beyond what the action needs, and say in the chunk file that it is trim handle rather than
content. An editor with 12 frames to play with can hide a small mismatch. An editor with a frame
accurate clip cannot hide anything.

Do not push this past 0.5 seconds at each end. Empty time inside a generated clip is where a
model puts drift, and a 5 second chunk with 2 seconds of nothing in it is a worse bet than a
tight one.

## Diagnosing joins that do not work

| the complaint | almost always |
|---|---|
| "the character changes between chunks" | A shared line was paraphrased rather than copied from `<shots>/shared.md` |
| "the light jumps" | The lighting line was not in the inherited set, or the time of day was not stated per chunk |
| "the clothing changes" | Wardrobe was in the scene heading and never copied into the chunks |
| "the hand teleports" | Split mid-gesture. Move the boundary to where the gesture completes |
| "it stutters at the join" | Split mid-camera-move, or 2 different moves named across a boundary |
| "the second clip starts with a breath" | The split inside a continuous line was not flagged in both files |
| "the join is hard and obvious" | No beats at the ends, so there is nothing to trim |
| "the background is different" | The setting was described in prose in 1 chunk and in different prose in the next |

Every 1 of these is a copying failure or a boundary failure, and both are cheaper to fix in the
files than in the edit.
