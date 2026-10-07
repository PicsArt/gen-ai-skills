# Seams — cuts inside a video, and the join between two videos

Every boundary in the cut list is one of two things. An **internal cut** sits
inside one video (`overview.md`, *The unit of generation is the run*): one
generation makes both halves, so the cut is written into two consecutive shot
blocks of one prompt and the model honours it. A
**video edge** is where two generations meet: nothing the model did on one
side knows about the other. The edge is joined the handbook's way — **the camera
changes, the action carries** — and the story decides where scenes change, not
the edge. A film that fits one video has no edges at all.

**For existing clips, diagnose before applying this planning recipe.** Read
`../../picsart-film-edit/references/join-repair.md` when the user asks to improve a join.
It governs repair choice and focused comparisons: a missing arrival or reaction
is a story gap, not something an angle change alone necessarily fixes.

## Internal cuts — the grammar goes in the shot blocks

**A cut rule is never a statement about one shot.** It says how shot A's last
second meets shot B's first second, and both halves are written into the two
shot blocks as a pair: the end of A's action, the start of B's. In live action
the matching frames exist because both shots came off one set; here they exist
because one generation made both, and the pair of blocks is what tells it to.

| Rule | Shot A's last second | Shot B's first second |
|---|---|---|
| **Match on action** | ends **mid-movement**, never at rest — "he starts turning his head" | "his head is **already** turning", picked up a beat *earlier* than A stopped. The overlap is the rule: B resuming from the identical pose reads as a skip |
| **Eyeline** | "looks off frame-**right**, out of frame" | the thing is on frame-**left**. Opposite sides, always — look right and place it right and it reads as being behind him. Eyeline height carries too: looking down means it is lower |
| **Screen direction** | "walks left to right, exits **right**" | "enters from the **left**, still moving right". A reversal reads as having turned around; when a reversal is real, put a shot moving toward or away from camera between |
| **Motivation** | ends on the **cause** — a knock, a name spoken, someone entering frame | opens on the **answer** — the door, the face that heard it |

**Three silent checks, read off the shot list before anything generates.**
Nothing is written into a block for them and nothing is recorded; a failure is
fixed on the card.

- **Two shots of the same subject in a row are two shot sizes apart** — WS→MS
  yes, MS→MCU no — or the cut reads as a stutter. (The classical form is ≥30°
  of camera movement around the subject; the card records no horizontal angle,
  so the size step is the half that can be checked.)
- **Eyelines agree** wherever a look answers a thing: opposite sides of frame.
- **Screen direction holds** inside the scene, shot to shot.

**Continuity is supported, not guaranteed.** Inside a video, one generation
authors both sides; still check the delivered frames. Across an edge use
**the same numbered reference images in
both calls**, in the same order, plus the geography line wherever a place
recurs. Do not restate it per boundary.

**Across a line of dialogue, glue the exchange — inside a video only.** The
block after a line opens with that line's *tail* on the right lips, so the
actor answers the right thing in the right tone; emotion does not switch off at
a cut, so after a heavy beat the next block starts with the residue — breath
still uneven, hands not yet steady. Do not split a generated line across separate
generations. At the edit, intact recorded speech may lead or trail the picture
as a J/L cut when lip-sync, speaker visibility and story meaning permit.

**Three habits make the internal cuts invisible:**

1. **The scene picture opens the video.** The first shot opens on the approved
   scene picture (`step-3-scene-pictures.md` step 3), labelled `START FRAME` in
   `imageUrls` — the `startFrame` *field* would lock the references out; the
   role in words does not (user-verified). The model photographs who
   stands where and holds it through every cut.
2. **One geography line, identical in every prompt of the scene**: who is
   left, who is right, what is behind them, and the side of the room the
   camera never crosses. The model does not carry the previous cut's geometry
   unless told, even inside one generation.
3. **Silence after every spoken line** — the handbook's sentence, pasted by
   the compiler after each block's dialogue. The cut ends on a quiet beat,
   never on the word; without it the model fills the cut's end with invented
   sound.

Hard cut is the only join inside a video. A dissolve or a whip between coverage
smears what the blocks paid for.

## The video edge — the handbook's join

**Where the edge falls.** *"Seedance 2.5 can now generate up to 30 seconds, so
only split the scene when it actually makes sense."* The story is written as a
story; the videos are its 30-second pieces, and the edge falls where the
ceiling falls. It is moved to the nearest moment where something is *moving* —
a turn, a step, a reach — never to a rest, and never dragged to a scene change:
a scene change at every edge makes a film jump between places for no story
reason. Two adjacent videos that fit as one are one.

**Three things help conceal the seam** — not a guarantee; the handbook's words, and all three
go into the two shot blocks either side of the edge:

1. **Different angle.** *"Never medium shot into the same medium shot."* *"If
   the previous generation ended on a wide shot, do not open the next one on a
   wide shot. Open on a close up, side angle, over-the-shoulder, high angle, or
   extreme close up."* *"It does not matter which angle you choose, as long as
   it is clearly different from the one before it."*
2. **A distractor at the seam.** *"An extreme close up or a detail shot breaks
   the eye, so any small difference between the two generations does not
   register."* The next video's first shot is a hand, an object, a face filling
   the frame.
3. **Continuous action.** *"The previous clip ends mid-movement, the next clip
   picks that same movement up from the new angle. The motion carries, the
   framing distracts."*

**The angle change is a new framing, not a travelling move across the join.**
"Different angle" means video B *starts* somewhere else — a
close-up, an OTS, a low angle — with its own move once it is there. It does not
mean one continuous camera move that begins in A and lands in B: a camera
move that spans two generations rarely lands and burns takes, and a much
simpler prompt does. Ask for a new place to stand, not a move that spans two
generations.

So the last shot block of video A ends with one line — *ends in the middle of
the movement* — and the first shot block of video B carries one line — *picks
that movement up from this new angle*. That is the whole record of the join;
nothing else is filed — the video plan (`../../picsart-film-development/references/workflow.md`, Stage 1
step 5) named it in one sentence, and the two blocks carry it. Nothing about
the join is written into video B's prompt as history: the model never sees
video A, so the prompt says what is in B's first frame now, never "continuing
from" (`prompt-blocks.md`, *Language laws*, first law).

**Both videos get the same pictures — but not the same OPENING picture.** The
same faces and the same scene pictures, in the same order. What differs is which
anything is labelled `START FRAME`: video A opens on the scene picture, and
video B carries **no `START FRAME` at all** — its opening angle comes from its
own block's words, against the same identity views, wide and map. A reference image is a
contract about framing, not just about content: handed a whole scene image,
the model returns the same shot, and in an interpolation the end frame
reproduces the start frame until the prompt forces the angle apart.
So handing video B the still video A opened on asks for the angle change in
words while the pixels ask for A's framing, and the pixels win. No frame is
copied from one video into the next, so every video of the film dispatches
together. This deliberately departs from the
handbook's *"Use the best frame from a previous generation as the next Start
Frame"* as a routine habit: a copied frame makes the next video wait for the one
before it, and the angle change hides the seam without it.

**The angle change is not a preference, it is the order of precedence.** A
frame carried when it is not needed makes a video wait for nothing. Before any
video that follows another, the two paths are tried in this order and the first
one that works is the one used:

1. **Change the angle.** Can video B open on a clearly different angle or shot
   size than A ended on? For everything but the two cases below the answer is
   yes, and that is the join — both videos dispatch together, carrying the same
   pictures.
2. **Carry a frame.** Only when step 1 is genuinely impossible, by one of the two
   tests below.

**A frame is taken only when a sentence can be said out loud, before dispatch,
naming what is in A's pixels and in none of the approved pictures.** *"The room
is wrecked and dust is on her face; no approved picture shows either."* If that
sentence names nothing — if it comes out as *"it continues the action"* or *"it
is the next video in the scene"* — **there is no exception**: continuing the
action is what the carried movement and the angle change already do, and every
video that follows another continues something. The two tests, and there are no
others:

- **The place or the people changed inside video A** (the paragraph below).
- **The scene is written as one unbroken shot**, so there is no cut to hide and
  the angle cannot change (the paragraph after it).

Say the sentence to the user with the trade-off in the same breath: video B now
waits for A, regenerating A stales the frame, and the frame carries only the
people visible in it — everyone else needs their own pictures beside it.

**What a carried frame does NOT carry.** A continuation generated from a
frame off the end of a clip joins the geometry but *not the light*: a frame is
pixels of one moment, not a lighting rig, so the continuation re-decides the
light, and a day scene can turn to night. The lighting on a person carried into
a new shot has to be re-stated in words, and anything outside the frame, such as
the rest of a costume, is invented fresh. A carried frame also costs realism:
the less the frame pins down, the more natural the movement and background
the model generates.

So when the exception does apply, video B's prompt carries the light and the
time of day explicitly — the same words video A had — because the frame will not
carry them, and the first thing to check on the take is whether the light
matches, not whether the action lines up.

**The first test — the earlier video changed the place or the people.**
*"When a generation changes the scene, the screenshot from that generation
becomes the base image of the next one."* A wrecked room, dust on a face, torn
clothes exist only in that video's frames, and the approved scene pictures now
*"fight the screenshot"*. Then, and only then, video B waits for video A's
accepted take, and its pictures of that place are frames from video A
(`step-6-7-selects.md` step 6): *"One frame is one camera angle. It carries the state
of the scene, not the geography of the room."* — so one frame for every angle
video B will show; *"if any angle has no screenshot, either hold the previous
generation on that angle for a beat so a usable frame exists, or you are not
ready to continue."* *"The screenshots replace the original stills. Do not
attach both."* Say out loud that regenerating video A stales those frames.
The frames travel in `imageUrls` — the one video B opens on as picture 1,
`START FRAME` — and the identity and wardrobe views of everyone in video B
ride beside them: a frame shows only who is in it, and the `startFrame` field would
shut the rest out (rule 7, `../../picsart-film/references/overview.md`).

**An option to offer: pass the last half-second of VIDEO, not a frame.**
`seedance-2.5` declares `videoUrls` beside `imageUrls`, and
reference media fields are exclusive only with `startFrame`/`endFrame`, never with
each other — so a short tail clip of video A can ride *with* everyone's identity
views. A single frame cannot show the motion in progress; a half-second tail
does, so the continuation picks it up more seamlessly. It is the one
configuration that answers the dead stop, the colour re-decide and the
missing-people problem at once. Preflight accepts and prices it; offer it to the
user as an option, never take it silently.

**The second test — a scene written as one unbroken shot.** *"In a continuous
shot you cannot change the angle at the seam, because the angle change is the
cut. There you hide the seam by matching the movement instead."* Then video B
opens on the frame exported from video A's last beat, and waits for it. That
frame is picture 1 in `imageUrls`, labelled `START FRAME`, beside the faces —
never the `startFrame` field.

**First+last frame will not bridge a real angle change.** Interpolation wants
two similar images; two dissimilar endpoints make the model insert **its own cut** somewhere
in the middle, which is neither the join that was designed nor a join anyone can
place. Interpolation is for a move inside one shot, not for an edge.

**A bridge clip needs a story purpose and two checked boundaries.** Offer one
when inspection shows missing connective action or a reaction that existing
coverage cannot supply, not as a generic seam softener. It may be a new insert,
not necessarily an extension or a re-roll of either accepted clip. Follow
`../../picsart-film-edit/references/join-repair.md` for agreement, reference selection,
credit approval and A → insert → B review. The normal identity and voice rules
apply: a bridge generated without everyone's wardrobe views adds a wardrobe jump
on both of its joins.

**An extend bridge that sees both sides uses excerpts, not whole runs.** Read
the extend sibling's live params, then follow the input
gate in `step-4-5-runs.md`, *Extend input gate — probe before preflight*. On the
Seedance 2.5 reference-to-video path, each reference video must be at least 1.8s and
their combined duration must not exceed 30.2s; preflight does not check either
limit. Probe first. Feed the outgoing take (or its shortest accepted
motion-bearing tail) plus a deterministic 2.0s opening excerpt of the incoming
take. The prompt identifies the first as the footage to continue and the second
as the target for identity, geography and motion. End the bridge while the
incoming action is still moving, then trim the bridge and incoming head on the
review board to one hard cut. Do not duplicate a static target frame and do not
crossfade it.

**The join is finished on the timeline, not in the prompt.** Expect
to trim **both** sides of every edge: the outgoing video's tail and the incoming
video's head. This is not a defect being patched — it is how the join is made,
and it is what the per-film `handles` switch (`step-2-shot-design.md`, the shot's `sec`
plus a handle at each end) exists to pay for. Even an extend designed to be
seamless leaves a slight overlap to trim, and the working habit is to drop the
last bit of the outgoing shot, cutting just before the next movement starts. A seam
that needs a trim is normal; a seam that needs a regeneration is the exception,
and the review board is where the difference is decided. Show full-cut context
or a focused join comparison under [join-repair.md](../../picsart-film-edit/references/join-repair.md), never the new bridge alone.

**No crossfade and no fade to black** at an edge. A film does not go dark every
thirty seconds; a black frame at the end of a take is a defect, trimmed on the
review board.

**Audio at an edge.** Each video is mastered on its own, so level, EQ and room
tone step at the edge. The finishing bed hides it, and the edit may J-cut the
incoming ambience under the outgoing tail silence. A video ends inside a
line's tail silence or on a held movement — never mid-word.

## No two adjacent cuts open on the same still

**A frame image outranks the words.** An identical still labelled as the frame
of two consecutive cuts — or as the `START FRAME` of two consecutive videos —
makes the second open back on that still's composition, whatever its block says
about where the action has moved since: the pixels are a contract and the prose
is a request. The result reads as a glitch: the film appears to jump back to a
frame it already played.

Before anything generates, check that no two adjacent cuts carry the same
still. Where two do, the second takes **no frame at all** — the numbered
identity references plus the block's blocking line, which still works. A still
is never authored just to fill that slot; the only frame that can
legitimately land there is one exported from an already-approved run
(`step-6-7-selects.md` step 6).

Reusing one still across two *non-adjacent* cuts is fine and often right — a
returning angle is a returning angle. The failure is only at a boundary.

## Special cases

- **Complex action opens mid-action.** A block that must break the door starts
  "ALREADY mid-swing, the door ALREADY cracking" — the approach to the door is
  its own block. Action buried mid-timing is where clips stall and shuffle.
- **A shot that needs more footage** is not chained by hand: it is an extend
  call on the model's extend sibling (`step-4-5-runs.md` step 5), which continues
  the clip itself.

## What we cannot check

The 30° form of the angle rule needs to know which *side* of the subject the
camera is on, and the shot card records size and height but no horizontal
angle — so nothing can measure it. The size-step check catches the ugly cases
without it.
