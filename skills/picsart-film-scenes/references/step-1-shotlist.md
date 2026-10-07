# Film scenes — step 1, final scene shotlist

## Step 1 — final scene shotlist

Sharpen the preliminary cards from `picsart-film-development` into the generation
shotlist. Per shot: id (`12A`), size, movement, FOV anchor, action (one),
line/sound, light/time of day, palette world, duration, and **the tags of every
asset in frame** — that last column is the prompt's checklist. The board's return replaces
the fields the board owns and leaves `design`, `refs`, `run` and `trim` on the
card by id (`../../picsart-film/references/widget-feedback.md`); an action that has stopped
telling the story's paragraph is a story note back to `picsart-film-development`: the
paragraph is rewritten and shown first, never answered with a board.
Coverage logic as
on a set: scene master → sizes → details; mind eye-lines, the action axis,
cutaways. Present via `picsart_shotlist_board`, feedback per
`../../picsart-film/references/widget-feedback.md`. The markdown-table fallback is for a
connection that does not expose the tool — never a shortcut when it does, and
never the answer to "show me the shot list". **Asked to see the shot list, open
the board again**, whatever stage the film is at: the board is where a shot list
is read and changed, and printing the rows instead hands back data the user then
has no way to edit.

### The cut-by-cut pass — write every cut as a pair, then read three checks

Shots are drafted one at a time, as a director drafts them. Then walk the scene
in adjacent pairs, **before any prompt is assembled**, and write each cut into
the two shot blocks as a pair — the end of A's action and the start of B's —
with one of the four pair rules in `seams.md` (match on action,
eyeline, screen direction, motivation). Nothing is recorded per boundary; the
pair lives in the prompt. A cut rule is a claim about two shots' *content*, and
content is decided in the prompt: an editor handed two shots that never shared
a movement cannot invent one.

**Three checks, free, read off the cards:**

- **No two adjacent shots of the same subject share a size.** Two sizes apart or
  the cut stutters. This is the checkable half of the 30° rule.
- **Eyelines agree.** Where a look answers a thing, A's gaze direction and B's
  subject placement are on opposite sides of frame. Same side reads as the
  thing being behind them.
- **Screen direction holds inside the scene**, shot to shot. A reversal is legal
  with a toward-or-away shot between it, and illegal silently.

Shot length is a habit, not a gate: dramatic shots run 3–8 seconds, action
shorter, a reaction shorter still (the handbook: *"Use the duration based on
what the shot needs."*). A shot over 8 seconds carries its reason in one line
on the card and nothing else — no approval, no alternative shown.

A failure here costs a keystroke. The same failure found after generation costs
a take.

### The run pass — the videos the plan named, filled to the ceiling

**The videos were decided in Stage 1, with the user's yes** — the video plan
(`../../picsart-film-development/references/workflow.md`, step 5) already says how many videos the film
is, which scenes each covers, its `genSec`, and one sentence for every join,
seeded into `film.json.runs[]`. The run pass does not plan videos; it fills
them. With the cuts written, walk the FILM in cut order and assign each card to
its planned video, **filling each one up to the model's live ceiling** (30 s on
Seedance 2.5; `picsart_model_params`). The edge falls where the plan put it —
on a movement, never a rest, never a scene change for its own sake
(`seams.md`, *The video edge*). At that edge the last shot block says
*ends in the middle of the movement* and the next video's first shot block
says *picks that movement up from this new angle*, and is a clearly different
size and angle — a detail or an extreme close-up by preference.

**A moved edge is shown, never re-cut in silence.** When the
cards' seconds do not sum to a video's `genSec`, or the plan's edge lands on a
rest, say so in one line with the fix — *"video 1 runs 33 s; the edge moves
from 1G to 1F, where Rasa's hand closes on the flask"* — and get the yes, the
way a story note gets one. Two adjacent planned videos that fit as one are one,
and that too is said, not done. Videos decided here, after the pictures and
unseen by the user, leave them unable to tell how one scene connects to the
next.

Record only what the dispatch needs: each shot carries `run` (`"r1"`), and
`film.json.runs[]` holds each video's shot ids in order (across scenes), its
planned `cutTimes` (the running sum of `sec`, in run seconds from the prompt's
0.0), its `genSec`, its `join` sentence from the plan, and its `refs` — the
ordered list of reference images every shot block numbers against.

Say the grouping in one line when the shot list is approved — *"the film is
three videos of 30 s as planned, the edges at 1F/2A and 2G/3A"* — because it is
the first thing that changes the invoice, and the one thing the board cannot
show.

### OTS is not a shot size — it is a two-body claim

Shot size is **one dial, and it means distance**: WS, MS, MCU, CU, ECU. Any of
them can be shot with one person alone in an empty room; none of them says who
else is present.

**Over-the-shoulder is a different kind of thing wearing the same label.** It
describes an arrangement: two people facing each other, the camera tucked behind
one of them, looking past their shoulder at the other. Recorded in the `size`
column it reads downstream as "how close is the camera", and three facts travel
nowhere:

- **whose shoulder** is in the foreground,
- **which side of frame** it sits on, and
- that a **second body must persist** — a close-up needs one person for six
  seconds; an OTS needs two people holding fixed positions for six seconds, one
  of whom is barely visible.

The third is what fails. A start frame where the near shoulder is an ambiguous
dark mass gives the model nothing to hold, and it stops treating that mass as a
person partway through the shot. It holds only when the near figure's ear, jaw,
shoulder line and garment texture are all legible.

So the rules, and none of them costs a render:

1. **The card names the near body.** `values.nearCharacter` (whose shoulder) and
   `values.nearSide` (left/right). `picsart_shotlist_board` refuses an OTS card
   that names neither, and refuses one that lists fewer than two assets in frame.
2. **Check the side against the location map** before generating. The map already
   says who sits where; if it says Maro sits right, an OTS over her shoulder puts
   her on the right. Put her left and the audience reads it as her having got up
   and moved.
3. **The prompt claims the near body as a person, not a silhouette** — named
   features, and holding position for the whole shot. See the foreground-body
   clause in `prompt-blocks.md`.

The board carries this as its own decision — **Who's in it**, separate from
size: `single` · `two-shot` · `dirty single` · `OTS` · `POV` · `insert` · `group`.
Three of them (two-shot, dirty single, OTS) are two-body claims and take the
`nearCharacter` + `nearSide` treatment above. Two more are easily mis-recorded
as sizes: a **POV** is about whose eyes the camera is — and the other actor must look
*into the lens*, which no size can say — and an **insert** is a thing rather than
a person, which is what an "ECU of the instrument on the table" actually is.
`group` is worth naming because three or more bodies is where models start
cloning people.

**Camera height is a decision too.** `eye level` ·
`low` · `high` · `top-down` · `dutch`. It is the second instruction a director
gives after size — low looks up and grants stature, high looks down and takes it
away — so a shot that never says it is a shot nobody framed. Set it per shot like
any other value.

An OTS also rarely travels alone: a conversation is covered as **two reverse
angles**, and the pair must match in everything except who is near — same lens,
same height, same distance, eyelines reversed. Nothing checks that pairing:
set the two shots' values identically by hand and look at them side by side.
