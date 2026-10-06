# Scenes — the shooting period

This is where the money goes, so it runs as a seven-step conveyor per scene, in
order, because each step is more expensive than the one before it. The gate behind
you is real: **no run generates until the assets of every scene it spans are
locked** (the matrix in `picsart-film`) — a run that crosses a production-block boundary
waits for both blocks, so where the film works block by block, the run pass cuts
runs at block boundaries. The gate ahead: every shot `final`, in selects, logged.

**Nothing charged in video goes out on a number the user has not seen and said
yes to.** Video is the film's largest spend, so
every charged video call — the pilot run, the batch, a re-roll, an edit, an
extend, the final-resolution pass — happens in three steps in this order:
`picsart_preflight` (free) returns a number, the number goes to the user in one
line, and the dispatch **waits for their yes**. One quote per dispatch, never per
shot: a run of five shots is one number and one yes.

What does NOT count as that yes — the forecast below (a plan, not a purchase),
the shot list's approval (that is the list's yes, and its board figure prices
per-card generations, which a run is not), the sheets' lock, the yes that opened
this stage, and the yes that covered an earlier dispatch. **Express pace changes nothing here.** When
preflight cannot price the call, say so in the same line — the rate arithmetic,
named an estimate — and still wait; an unpriced call never reads as free. Record
the figure in `film.json`'s `credits.nextActionQuote` before the call, so the
yes has a number on record.

**Before the money phase, state the film's forecast once.** Convert the
shotlist into numbers before anything renders: runs × expected takes × each
run's `genSec` × the model's per-second rate, plus a regeneration buffer
(~20%), the edit passes you can foresee (one per risky stretch, at the edit
model's rate — quote it once), and the charged QC
frames (take QC, cut-point checks). **A
per-shot keep rate does not transfer to a run**: a run passes only when every
cut in it passes — so plan two takes per run, say the number is an estimate,
and correct it out loud after the first run lands. One honest range — "this
film will cost roughly X–Y credits" — before the first dispatch; track
actual-vs-forecast in `film.json`'s `credits` and say so when the pace will
blow it.

## The unit of generation is the run, not the shot

**Repair exception:** this section governs initial production, not permission
to replace accepted footage. A user-approved connecting insert between existing
clips may generate alone under `../../picsart-film-edit/references/join-repair.md`. Preserve
both originals and verify both joins; do not merge the insert into their run and
re-roll it merely to satisfy the packing rule.

**Shots are authored one at a time and bought together.** A film generated
shot by shot — one `picsart_generate`
per card, the takes cut together at the edit — loses to the same shots
generated as ONE multi-shot take with the cards written in as its cut list. The
loss is not subtle and it is not one thing: identity holds across the cuts
because the model never re-reads the descriptor from cold, the light and grade
are less likely to step at every join, voices face fewer independent generation
decisions, and the cuts *land* — a match on action that one generation authored
into both halves actually matches, where two independent renders only ever
approximated it.

So the **run** is the unit: **as much of the film as fits inside a single
generation at the model's live ceiling** (`picsart_model_params` — Seedance 2.5
goes to 30s), scenes included. A short that fits is ONE generation — garage
scene and street scene together; a film that does not is the fewest runs that
cover it, split where the last paragraph of this section says. A scene change
inside a run is a cut like any other: a shot block whose first frame is the new
place, with the new scene's geography line stated where its first shot is
(`prompt-blocks.md`).

**“Fewest runs” is a quality rule, not merely a cost preference.** The
continuity advantage above increases with the amount of consecutive film the
model authors together. Therefore a payoff, climax, close-up, long hold,
different emotional beat, scene boundary, or a belief that a shot will “hold up
better alone” is **never** a reason to start another generation. Those facts
shape the shot header and its seconds; they do not shape the run boundary. A
partition is invalid if the same ordered shots can fit in fewer runs at the live
ceiling while keeping every necessary run edge valid. Before dispatch, merge
every adjacent pair of planned runs that fits as one generation; scene changes
inside the merged run remain ordinary internal cuts.

Nothing about *authoring* changes. The shot cards, the cut-by-cut pass,
sizes, who is in frame, the geography line, the silence after every line — all
of it is still written per shot; the user still sees short cards on
`picsart_shotlist_board` and still sets each one with the presets. What
changes is where it lands: one prompt per run in the handbook's two-part shape
— a setup once (the tagging header, the tone, the camera line, the cut list),
then one short block per shot that opens with its shot type and camera move
(`prompt-blocks.md`).

**Everything travels as a reference image; the prompt says what each one is
for.** The `startFrame` *field* and reference media are exclusive (step 2), and
that field anchors exactly one frame — the first — while a run has many shots
that each need identity pixels. The way round it: the run's call carries `imageUrls` only — the **views** of every
character and location the run uses *and* every approved still — in a fixed
order, and
**the tagging header gives each image its role in words**: a face and an
outfit (*"100% matched based exactly on IMAGE n"*), `START FRAME` (the run
opens on exactly this image), `FRAME REFERENCE for shot N` (that shot opens on
this framing), `SPACE` (the wide, the map). The model honours the role it is
told; after the header, names only. That is the anchoring a run gets — identity
pixels for every character in every shot, *and* a photographed first frame for
any cut that has one. A character the user supplied as a **photograph** goes
first and untouched — *"Cal face 100% matched based exactly on IMAGE 1 — a
photograph of the real person"* — with one view of its generated angle sheet, when one
exists, second as *wardrobe and angles, face from IMAGE 1* (`picsart-film-assets`, *When
the user brings the asset*).

**One image, one thing — never a multi-panel sheet.** Every entry
in `imageUrls` shows exactly one view of exactly one asset. An asset's sheet is
cut into single-view files at lock, and those are what a run carries; the sheet
itself stays in the library as the approved archive. This is not tidiness: a
multi-panel reference of one person at several ages, even with the references
header correctly naming the wanted panel, renders the wrong version of that
person — a different wrong version on each identical prompt, sometimes a blend
of two panels into a face not in the cast. Each generation is an independent draw
against the same ambiguity, so it fails differently every time, never appears in
a prompt diff, and holds *within* a run while moving *between* runs. Panel
labels rendered into the sheet's own pixels do not fix it either. **There is no
fallback pointer**: a prompt naming a panel or a position is a dispatch error
(the lint in step 2). And every run that needs a state passes the **same view
file**, so identity rests on byte-identical input rather than on a guess
repeating. The method and the crop recipe are in
`../../picsart-film-assets/references/asset-sheets.md`, *How an asset reaches the run*.

**What you are accepting, stated once so nobody rediscovers it mid-film:**

- **A repair is an edit or an extend before it is ever a re-roll.**
  The model ships two siblings for exactly this, recorded at the pick as
  `shoot.editModel` and `shoot.extendModel` (never a version named here): the
  **edit** sibling
  changes something *inside* a clip (the clip + the change in words + the same
  numbered references → the same clip, changed), and the **extend** sibling
  makes a clip *longer* (the clip + what happens next → the clip continued).
  The note's *meaning*, read against what was selected on the board, routes
  the call (step 5): a note about how the marked stretch plays → the edit
  model; a note asking for something that has not happened yet in the clip →
  the extend model; only "regenerate / redo", or a note about the whole run →
  a fresh roll. A clip selected with the note "expand" is an extend call, never
  a regeneration. The first call of
  each sibling is a test, judged in the
  cut in the scene editor, and a clip that will not take an edit in two tries
  is re-rolled.
- **Handles exist only at the run's two ends.** Inside the run the model's cut
  is the cut; the trim room at an internal boundary is the silence after a line, and
  nothing else.
- **The declared cut times are a request.** The model cuts near them, not on
  them, and will occasionally fold two declared cuts into one or add one nobody
  asked for. The delivered take is split where it *actually* cut (step 6), never
  at the planned times, and a wrong cut count is a failed take.
- **Length can cost resolution on some models.** A model whose long takes cap
  below the finish format makes every run a resolution decision — which is why
  native multi-shot *at the finish resolution* is a hard filter at the model
  pick (`picsart-film`, model policy), not a trade-off discussed per scene.

**What you are not losing — and say so when it comes up:** per-shot *editing*.
The run comes back as one file and is split at its delivered cuts into
shot-shaped clips before anyone sees it — compositor bookkeeping, free — so
trims, reorders, drops, the scene editor's clips, the final cut and the join QC all
stay per shot. "We lose shot editing" is imprecise: a shot
is edited in place with the edit model, lengthened with the extend model, and
only re-rolled — with its run — when the user says so.

**There are no exceptions at planning.** No shot shoots alone, no film shoots
shot by shot: a risky stretch is a risk the run carries, a shot whose
composition matters gets a longer header and a labelled composition reference.
*Repair* is the edit model, the extend model, or a re-roll of the run (step 5).
The planning decision is made once for the pipeline, so it is not re-made per
scene.

**One primary action per CUT is still the rule** — it moved from the
generation to the cut header. A header with five unrelated beats smears exactly
as a five-beat shot did; a scene of eleven cards is eleven headers of one action
each, with beats inside a header legitimate at roughly one per 2–3 seconds when
they are one continuous movement (a hand reaching, a head turning, a line
landing). Sequence structure is built by the generation, not by the edit,
because the generation builds it better.

**The ceiling is a packing limit, not a shot-length recommendation.** Author
coverage first, then pack those cards into a run. Default dramatic cuts are
3–8s and action may be shorter. A card over 8s needs
`design.durationReason`; over 12s is a deliberate long take. A scene longer
than 12s with one card must not pass silently: recommend a 2–4-shot coverage
version, warn that the long take
risks stretched motion and gives the edit no reaction/insert coverage, and keep
the one-card version only after the user explicitly chooses it. Model choice,
run grouping, visual rhyme, "restrained" tone, or spare seconds under the ceiling
do not constitute that choice. Several short shots still cost one generation
when they share a run — never merge their actions onto one card to save calls.

**Run length is arithmetic, not habit.** A run's `genSec` is the sum of its
shots' `sec` plus one handle at each end of the run, snapped **up** to a length
the model offers; the 3–8 seconds AI motion tolerates before it reads uncanny
(`picsart-film-edit`) is authored into each shot's `sec` rather than trimmed out of a
long take afterwards. Going to the ceiling is not an exception — it is
what a film costs — and the one trade-off that survives is the re-roll: a broken
second 22 of 30 re-rolls all 30, and the film has chosen to pay it.

Where the film outruns the ceiling, **the edge between two videos is joined the
handbook's way** (`seams.md`, *The video edge*): video A's
last shot ends in the middle of a movement, video B's first shot picks that
movement up from a clearly different angle and size — a close-up, a detail, an
over-the-shoulder, never the same framing twice — and both videos carry the
same pictures in the same order, so every video dispatches together. The edge
falls where the ceiling falls, moved to the nearest moment where something is
moving; the story decides where scenes change, and an edge is never dragged to
a scene change to make it "clean" — that makes films jump between places for
no story reason. The one exception is a video
that changed its place or its people: the videos after it there take their
pictures of that place from its frames and wait for it (step 6).
(The extend sibling can stitch several clips into one continuous video — read
the count off `picsart_model_params` — and may serve as a join between two
runs; treat its first use as a test, judged in the cut.)

**Inside a video the cuts are the model's, and the pair rules are written into
the shot blocks** — match on action, eyeline, screen direction, motivation
(`seams.md`, *Internal cuts*). Three habits carry: the scene picture
opens the video — **the FIRST video of the scene only; a second video of the
same scene carries no `START FRAME` at all: it opens on its block's words plus
the identity views, the wide and the map** (`seams.md`, *No two
adjacent cuts open on the same still*, and the reason it is a pixel contract);
one geography line,
identical in every prompt of the scene;
silence after every spoken line. Two uses of a frame image are opposites: an
**authored, approved still** labelled `START FRAME` in `imageUrls` is the
anchor (step 3); a **frame exported from an earlier video** is used only when
that video changed the place (step 6) or the scene is written as one unbroken
shot — it inherits the earlier video's drift and makes the next video wait.

## Which surface owns which decision

Every board answers about the artifact in front of it. Asking a question on a
surface that has nothing to show is what makes a console feel like a form.

| What exists | Surface | What the user decides there |
|---|---|---|
| nothing — a list | `picsart_shotlist_board` | story, coverage, shot **size**, **duration**, order, cuts |
| one run's take, split into its shots | `picsart_scene_editor` | is this the run, which cut (if any) failed, and what exactly is wrong |
| an assembled cut | `picsart_scene_editor` | watch it, trim, split, delete a stretch, and say in comments what to regenerate |
| a retake of a shot they already watched | `picsart_scene_editor` | the new take in the cut — keep it, or go back to the one in the log |

The shotlist board has **no modes**. It plans — one call, every scene of the
pass, one approval. Take triage is not a board job: a take is judged in the
scene editor, always.

**The board thinks in shots; generation thinks in runs.** Its rows,
`genSec` and "commit to video" are per shot, and it has no way to show which
rows share a generation — so the run grouping is said in chat when the list is
approved, and the board's per-shot `genSec` is read as "what this shot would
cost alone", never summed into the forecast. Never fake a run marker with row
labels.

**Camera has one author.** The shot's card on the shotlist board is where it is
chosen — the move pill, previewed by the board's own clip for that move — and
after a video exists it is re-asked exactly once, as the step-4 severity
routing. There is no separate design screen; a second surface asking the same
questions is duplication. Pass
takes with `kind` (`video` | `image`) so a still is never shown as a broken
player.

**The model is chosen BEFORE the durations.** A shot's length is only real if the
model accepts it — and what the model accepts is read off `picsart_model_params`
(`duration`: min, max, step), never from a remembered ladder: a schema that
says any whole second from 4 to 30 accepts a 7-second call. The run's `genSec`
is still preflighted before the board opens. A card planned
model-blind gets snapped afterwards, which is an approved
plan being quietly changed. Pass `model` on the `picsart_shotlist_board` call and
the board offers exactly that model's lengths; a length nobody was offered cannot
be snapped. Switching models later re-opens every duration, which is why the
pick sits in Stage 1 — after the look console, before the shot list ever opens
(`picsart-film-development`) — and not at the bible lock. **And the model is chosen
before the runs**, for the same reason one level up: its ceiling is what decides
how many generations the film is, so a film grouped model-blind is a grouping
that will be redone.

## Costs

| Free | Charged |
|---|---|
| shotlist, shot design on the cards, run grouping, prompt assembly, preflight, splitting a delivered run at its cuts, splicing a repaired piece back, animatic review on the board when requested, the handoff frames of a changed place (contact-sheet thumbnails to choose, full-size exports to use — render time, not credits), the 1280 px check copies of every picture (`picsart_media_export`), frame exports for anchors (`picsart_media_export` — render time and a Drive file, not credits), `picsart_shotlist_board` / `picsart_scene_editor` (renders nothing) | every scene's pictures — scene picture, wide, coverage, a room map when needed (image rates, one board for all scenes), cut-point and take-QC contact-sheet frames (per frame), every draft and re-roll (`picsart_generate`, video rates — billed at the generated length, which is the reason everything upstream of this skill exists), every edit or extend call (each sibling's own rate — preflight first) |

## Traps

- Dispatching on a number the user never saw, or on a yes that covered an
  earlier call. Every charged video call carries its own quote and its own yes;
  the forecast is not a purchase.
- Generating a "quick test shot" for an unlocked scene. That is the gate, and it
  exists because half of early material gets redone.
- Pasting a descriptor into the prompt, whole or shortened. The pictures
  carry identity and the prompt names them by number
  (`prompt-blocks.md`); a paragraph beside the pictures makes the
  model average words and pixels.
- Dropping the geography line or the map to save tokens — characters swap
  sides between shots and the scene stops cutting.
- Dispatching a prompt that points at a panel of a bigger picture. That is a
  lint error, not a phrasing choice: the reference is wrong, and the crop that
  fixes it is free.
- A run without its scene's pictures, or a place generated empty from its
  descriptor. The handbook's order is scene first, place from it — an empty
  location renders unreal, and a run without the pictures asks the model to
  invent the room.
- Attaching the approved scene pictures beside frames from a run that changed
  the place. Two versions of one room; the frames replace the pictures.
- Cropping, mapping or using a wide before its visual check has passed.

- A third roll of the same two-shot after two failures on faces. Change the
  reference set or the model.
- Iterating two variables at once. When it improves you will not know why.
- Re-submitting a generation because the call "timed out". The render survived
  the severed call and already charged — poll `picsart_job_status` first,
  always.
- Letting accepted takes sit in the raw pile — the editor must only ever see
  selects.
- Generating a scene shot by shot out of habit. It loses continuity:
  the run is the initial-production unit; a scoped connecting insert between
  accepted clips is the repair exception, not a new production default.
- Treating the run ceiling as a reason to make one long shot. A 30s run should
  usually contain several 3–8s shots; one 30s shot is a long take with its
  reason on the card, not the default meaning of "one run."
- Filling the `startFrame` field on any video — a run, a five-second bridge, a
  one-shot reshoot. It locks out `imageUrls`, and a frame shows only the people
  in it: a person in the shot but not in the frame comes back in invented
  wardrobe. The start frame goes in *with* the
  references, labelled `START FRAME` in the tagging header — every image
  numbered with its role.
- A person in a shot block without their identity and wardrobe views in `imageUrls`, or
  an object named in two places ("on her strap" and "in her hand" is two
  flasks).
- A shot block that opens without its shot type and camera move. The model
  guesses both (the handbook: *"Tell it clearly."*).
- A prompt that refers to the video before it — "continuing from the previous
  scene", "as before", "again". The model never sees that video; write what is
  in the frame now (`prompt-blocks.md`, first language law).
- A contact-sheet thumbnail used as a reference, a descriptor's picture or a
  start frame. Thumbnails are 480 px previews for choosing; the frame is
  exported at full size first.
- Splitting a delivered run at its PLANNED cut times. The model cut near them,
  not on them — split where it actually cut, or every trim downstream is off by
  the drift.
- Regenerating when the note asked for a change or a continuation. "Make this
  more dynamic" on a marked stretch is an edit; "the copter must land" on a
  clip that ends mid-air is an extend — with or without the words *edit* and
  *expand*. A regeneration in their place throws away the clip they wanted to
  keep.
- Re-describing the whole shot in an edit prompt. An edit names the change and
  the seconds, nothing else; a re-described shot is a re-roll at an edit's
  price.
- Feeding the model a contact-sheet thumbnail as a frame. A frame the model
  reads is exported at the run's native size and probed before it goes.
- Polishing re-roll 8 of a run whose failing header should have been simplified
  at re-roll 4.
