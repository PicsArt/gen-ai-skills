---
name: quality-review
description: Check work before the user sees it - a scene validated, linted and looked at in contact-sheet frames, then fixed and checked again; a draft watched cold by model viewers against its viewer track, then reviewed by critics; the brief graded; an export checked against its scene. Use after a script is written and before it is built or paid for, after building or changing a scene, before REVIEW or an export, before handing over an export, and at each decision a use case names.
metadata:
  imports: screen-recording-layouts
user-invocable: false
---

# Evaluate

1. **Validate.** A successful `picsart_scene_patch` has already validated its result, so call
   `picsart_scene_validate` only after changes made any other way. Zero errors; fix the
   warnings too.
2. **Lint the layout.** `picsart_scene_lint_layout` over the timeline; on a long scene, narrow
   `t0`/`t1` to the part in question. Each of its `findings` is a sustained overlap between layers
   that should not touch. For a pair placed together on purpose, pass `allow: ["idA:idB"]`. A text
   box is the font's line box, so a clean lint is not proof and it can flag empty space. If the tool is not in your list, or fails because the
   query build is unavailable, skip to the frames.
3. **Measure.** For a flagged pair, or a use-case question about where something sits (inside a
   panel, inside a mask), `picsart_scene_query_layout` at that moment gives each layer's box. It
   reads layer geometry, not painted pixels.
4. `picsart_scene_contact_sheet` at each moment the use case names. Look at every frame and answer
   the use case's questions about it.
5. `picsart_scene_contact_sheet` once across the whole timeline — order, seams, nothing blank.
   Then, for every cut, its `times` at the cut and one frame either side (`cut − 1/fps`, `cut`,
   `cut + 1/fps`): a one-frame black gap falls between evenly spaced samples.
6. **Polish**, once the frames are right. A correct video can still look machine-made, and the
   user notices that first:
   - when the use case built it in a style, run the visual-style skill's `adherence.py` on it,
     and check the frames against that skill's list of defaults that look machine-made;
   - **the first frame is a real moment**: the payoff, or the problem it solves, as the
     retention-hooks skill's hook rules say. Not a login screen, an empty app or a title on a plain
     canvas;
   - **every second has something new**: no stretch over 3 s where nothing moves, appears or
     changes, unless it is a hold the use case asked for. First run `scripts/timing.py` on
     `{ scene }`, from this skill's folder: from the JSON alone it flags every stretch over 8 s
     with no change (`dead_air`), every block of words held under 0.3 s a word or 1 s
     (`short_hold`), and every block over 10 words, or a step label over 6 (`too_many_words`).
     Typed holds add only the typing remaining in each visible span, including after retiming or
     trimming. Text and caption masks in `mask.clip` or legacy `mask.layer` need rendered review;
     the script rejects them.
     Pass the measured reveals inside a clip as `changes`; the JSON cannot see them. Then look
     at the frames for the 3 s: motion inside a clip is only on them;
   - **not one move everywhere**: when every beat has the same push or the same entrance, vary
     what the use case's skills allow;
   - **words inside the safe zone** of the destination the use case names: run the screen-recording-layouts skill's
     `safe_zone.py` with its profile, and fix each finding. Readable at the frame's width.

   Fix each finding, or keep it and say why in the review line ("the app itself is navy, so the
   canvas follows it").
7. Fix the layers and check again. Building is free.

**The brief, item by item.** When the use case has a brief (the message, the destinations, the
length, the hook, the call to action, the steps), grade the build against it one item at a time,
never as one judgement of the whole. From this skill's folder, run
`python3 scripts/checklist.py <file>` on `{ brief, scene }`, with the destinations as the screen-recording-layouts
skill's safe-zone profiles. It turns the brief into yes-or-no questions and grades the ones the
scene answers: the length, words by 0.5 s, the hook's words, the call to action at the end, the
safe zone, and `timing.py`. Checks the scene cannot answer for a text mask become `look` items,
alongside the remaining checks. Answer each from the frames of steps 4-6, with the frame's
time or the tool's line as `evidence`, and run it again with your `answers`; an answer without
evidence stays open. Fix only the items that say no, then grade again: never rebuild what passed.
Its `summary` goes with the review.

**The cold watch.** Before the critics, and before the user sees a draft that has a viewer track,
three model viewers who know nothing of it watch it forward, a few seconds at a time, from its
frames and its heard words, each keeping only their own notes, and say what they make of it. A
comparer that never saw the plan marks their words against the track.
`scripts/cold_watch.py` writes every call, checks the marks and says whether the floor is met:
every must-know hit in time by two of the three, and no wrong ending. It is the one check of
whether a stranger follows the video: nobody who knows the plan, you included, can judge that.
Its viewer calls cost credits unless their quote shows 0 for every one: quote them as
`references/cold-watch.md` says and SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says) before the first round; a credit or storage error
stops it, never retried. It is not a measure of retention, and it says so.

**The critic panel.** After the cold watch, before the user sees a draft, six simulated critics
with taste each look at it through one lens: the first-principles critic (the core problem the
video solves), the radical (the concept), the interface designer (the UI on screen), the story
editor (the message and the script), the growth strategist (the stop, the drops, the ending) and
the art director (the look). Each sees only frames every 0.5 s, the source stills (the real UI or
footage the video depicts), the words, the goal, the destination and the cold watch's gap list, and returns a verdict, problems with their times, and fixes. `scripts/critics.py`
picks the frames and lays the notes side by side. Where critics agree it is a must-fix, weighed
against the first-principles critic's core sentence; a new concept goes to the user as a choice,
never applied silently. So does a shot a critic would swap in an edit of the user's footage: it
is a proposal, shown to the user as a rendered A/B, never a silent change to the plan. A draft that looks different from its source is a must-fix.

**The challenger.** A seventh critic who does not wait for the draft. At each decision the use case
names (the idea, the plan, the key frames and each image picked, the UI, and every SPEND before
its quote) it asks "why this?" and tries to show that the direction is wrong before more work is
spent on it. It returns `keep`, `rethink` or `stop`, with the reason and the cheaper alternative.
It also gets the source stills, so a design that drifts from the real app is caught as it is made.
Its `rethink` of a shot the user saw and kept is a proposal too: an A/B, never a silent swap.

**The QC inspector.** An edit of the user's own footage is checked from its render by an
inspector who did not make it and never sees why it was made that way: camera steadiness on every
used range, lips against the voice, each cut against its word, shot lengths, legible text,
captions, repeated or clipped lines, the locked meaning map, and every keeper of a version the
user saw: one dropped with no line the user will read fails the draft, and, when a reference's
format is in the record, the reference match (`scripts/reference_match.py` reads it from the
scene). It reports only critical and
major findings, each with its method and confidence, and marks what it could not see or hear as
open, never as a pass. `scripts/inspection.py` reads its report back.

| Read this | Before you |
|---|---|
| `references/qc-inspector.md` | check a draft of an edit of the user's footage, or a fix to one |
| `references/cold-watch.md` | write a viewer track, or run the cold watch on a draft |
| `references/cold-watch-comparer.md` | mark a cold watch's accounts against the track (the comparer's prompt) |
| `references/critic-panel.md` | run the critic panel on a draft |
| `references/challenger.md` | go on from a decision the use case names, or show a quote |

**When a frame or an export fails to render.** The scene validated, so the fault is in a feature
the renderer refuses, and the error names it rarely. Find it before changing anything:

1. Copy the error text exactly.
2. Cut a copy of the scene down to the one layer at the failing time, and sample that. Then take
   away one feature at a time (its mask, its effects, its animation) until it renders. Each sample is
   one frame.
3. Keep the scene as it is. Tell the user which feature fails, with the error and the smallest
   scene that shows it, and offer a way round it that keeps the look where one exists (for a mask,
   the screen-recording-layouts skill's nested panel). Never reshape the
   whole scene to guess past it.

**Before a film's cut is reviewed.** From this skill's folder, run
`python3 scripts/cut_check.py <file>` on `{ scene, allowed?, shots?, places? }`: the cut's scene,
its allowed spans (the screen clips placed in it, as film-cutting says), and from the project record
the shot each clip shows (keyed by clip id, with its size and angle when the shot list has them) and
the place each shows. From the scene alone it finds the joins, moves and overlays a viewer reads
as a glitch: two takes of one shot, or two shots of one size and angle, cut together
(`same-scene-cut`), or a cut hidden under a quick move (`hidden-take-change`); different shots of
one place are coverage and pass, a short dissolve between takes (`ghost`), a move of the picture, or of a layer covering 40% of the frame or more, that starts or stops in
one frame (`pop-move`), an overlay gone for a frame or two (`blink`), a zoom over a still picture
(`zoom-idle`), and a screen held still inside its span (`screen-still`). Nothing inside a span is
flagged except `screen-still`. It prints `{ ok, errors, warnings, unchecked, skipped }`: fix each error as
film-cutting says and run it again, say each warning in the review, and check what it lists as
`unchecked` on the frames of step 5, never calling it checked. On an animatic of held stills, add
`--slides`: its stills hold on purpose, so the motion rules move to `skipped` and run on the cut,
and the joins, overlays and screens are still checked.

**Before you hand over an export.** An export can differ from its scene: another size, a dropped
frame rate, a missing sound track, a silent last second. Probe the file with
`picsart_media_probe`, which is free, and from this skill's folder run
`python3 scripts/qc.py <file>` on `{ scene, probe, audio? }`: the scene you exported, the probe as
it returned, and in `audio` only what a tool measured (loudness, true peak, the sound's length, an
energy curve). It prints `{ ok, errors, warnings, unchecked }`:

- an `error` (the size, the fps or the length is not the scene's, the sound is missing, drifts or
  peaks above -0.5 dBTP): make its `fix` and export again, once. Still there: deliver, and name it;
- a `warning` (loudness away from -14 LUFS, a silent tail over 1.2 s): say it in the delivery
  line;
- `unchecked`: what no tool measured. Never call it checked.

Frames show framing, not motion: the user judges timing and easing in REVIEW.

How many rounds you get, and what to do when they run out, is in picsart-video-rules (Evaluation). Never
export to "show" a draft that the user can review live; picsart-video-rules (Preview and export) says when
to export.

## The script, before the build

Before a short is built, voiced or generated, review its script: is it worth making, what is its
why, and which lines to rewrite. A video whose footage never shows its result is dropped before it
costs anything. The review runs `scripts/script_review.py`; the reference below has its steps.

| Read this | Before you |
|---|---|
| `references/script-review.md` | review a script, or report its verdict |
| `references/readiness-verdict.md` | declare a generated video's decisive evidence before paying for it, or say whether a candidate is ready |
