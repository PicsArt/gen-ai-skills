# Seams: cuts inside a run, and the edge between two runs

Every boundary is one of two things. An **internal cut** sits inside one run: one generation makes
both halves, so the cut is written into two consecutive shot blocks and the model honours it. A
**run edge** is where two generations meet, and nothing on one side knows about the other. A film
that fits one run has no edges.

For a join that already exists and looks wrong, diagnose it first, as film-edit's join repair says.
This file is for planning.

## Internal cuts: the grammar goes in the blocks

A cut rule says how shot A's last second meets shot B's first, and both halves are written into the
two blocks as a pair.

| Rule | Shot A's last second | Shot B's first second |
|---|---|---|
| **Match on action** | ends mid-movement, never at rest: "he starts turning his head" | "his head is already turning", picked up a beat earlier than A stopped. Resuming from the identical pose reads as a skip |
| **Eyeline** | "looks off frame-right" | the thing is frame-left. Opposite sides, always; the height carries too |
| **Screen direction** | "walks left to right, exits right" | "enters from the left, still moving right". A real reversal gets a shot toward or away from camera between |
| **Motivation** | ends on the cause: a knock, a name, someone entering | opens on the answer: the door, the face that heard it |

Three habits make internal cuts invisible:

1. **The scene picture opens the scene's first run**, as picture 1 labelled `START FRAME`. The
   model photographs who stands where and holds it through the cuts.
2. **One geography line, identical in every prompt of the scene**: who is left, who is right, what
   is behind each, and the side of the room the camera never crosses.
3. **Silence after every line.** The cut ends on a quiet beat, never on the word.

**Across a line, glue the exchange, inside a run only.** The block after a line opens on its tail
on the right lips, and emotion carries: after a heavy beat the next block starts with the residue.
Never split one spoken line across two generations.

Hard cut is the only join inside a run. A dissolve or a whip between coverage smears what the blocks
paid for.

## The run edge: the camera changes, the action carries

- **Where it falls:** where the ceiling falls, on a movement. Never at a rest, and never forced onto a
  scene change. A scene longer than the ceiling says where inside it the edge falls.
- **Run A's last block ends mid-movement.** Run B opens with that movement already under way, from a
  clearly different size and angle, often a detail or a close-up, with its own camera move. No
  camera move crosses the edge.
- **The same pictures travel on both sides, in the same order**, but B has no `START FRAME` from the
  scene picture: reusing A's opening still asks for A's composition and undoes the new angle.
- This is what lets every run of the film dispatch at once.

## The carried frame: the named exception

A frame of run A's take goes into run B only when:

1. A changed a place or a person in a way none of the approved pictures shows (a torn coat, a
   wrecked room, dust on a face); or
2. the scene is one unbroken shot that cannot change angle at the edge.

Before dispatch, name in one sentence what is in A's pixels that no picture shows, and say what it
costs: B waits for A, a re-roll of A voids the frames, and a frame carries only the people visible
in it. If the sentence names nothing, there is no exception. The frame replaces the picture it
contradicts; it never sits beside it. Everyone not in the frame keeps their identity and wardrobe
views. A frame does not carry light, off-frame clothing or unseen geography: say them again, and
check them on the take.

## Bridges

A short video between two runs is an experiment, not a seam softener. It needs a story purpose.
Return its cost for the use case to quote. film-edit's join repair says how it is judged.

At an edge, expect to trim both the outgoing tail and the incoming head in the edit. No crossfade,
no fade to black. An ambience bed can carry sound across an edge; it cannot fix a face.
