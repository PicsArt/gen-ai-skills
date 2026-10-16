---
name: evaluate
description: Check a scene before the user sees it - validate it, lint its layout, measure where layers sit, look at contact-sheet frames at the moments that matter and across the timeline, a polish pass for what looks generic, then fix and check again; a short's script reviewed with scripts/script_review.py (worth making, its why, better lines); a simulated viewer panel on a hook and draft (scripts/panel.py); six critics, each with one lens, merged with scripts/critics.py; a challenger who asks "why this?" at each decision; the brief graded with scripts/checklist.py; an export checked against its scene with scripts/qc.py. Use after a script is written and before it is built or paid for, after building or changing a scene, before REVIEW or an export, before handing over an export, and at each decision a use case names.
metadata:
  imports: layouts
user-invocable: false
---

# Evaluate

1. **Validate.** A successful `picsart_media_patch_scene` has already validated its result, so call
   `picsart_media_validate_scene` only after changes made any other way. Zero errors; fix the
   warnings too.
2. **Lint the layout.** `picsart_media_layout_lint` over the timeline; on a long scene, narrow
   `t0`/`t1` to the part in question. Each of its `findings` is a sustained overlap between layers
   that should not touch. For a pair placed together on purpose, pass `allow: ["idA:idB"]`. A clean
   lint is not proof: on the `jet` engine it never measures text, and on `v3` a text box is the
   font's line box, so it can flag empty space. If the tool is not in your list, or fails because
   the query build is unavailable, skip to the frames.
3. **Measure.** For a flagged pair, or a use-case question about where something sits (inside a
   panel, inside a mask), `picsart_media_query_layout` at that moment gives each layer's box. It
   reads layer geometry, not painted pixels, and has no box for text on `jet`.
4. `picsart_media_contact_sheet` at each moment the use case names. Look at every frame and answer
   the use case's questions about it.
5. `picsart_media_contact_sheet` once across the whole timeline — order, seams, nothing blank.
   Then, for every cut, its `times` at the cut and one frame either side (`cut − 1/fps`, `cut`,
   `cut + 1/fps`): a one-frame black gap falls between evenly spaced samples.
6. **Polish**, once the frames are right. A correct video can still look machine-made, and the
   user notices that first:
   - when the use case built it in a style, run the art-direction skill's `adherence.py` on it,
     and check the frames against that skill's list of defaults that look machine-made;
   - **the first frame is a real moment**: the payoff, or the problem it solves, as the
     story-loops skill's hook rules say. Not a login screen, an empty app or a title on a plain
     canvas;
   - **every second has something new**: no stretch over 3 s where nothing moves, appears or
     changes, unless it is a hold the use case asked for. First run `scripts/timing.py` on
     `{ scene }`, from this skill's folder: from the JSON alone it flags every stretch over 8 s
     with no change (`dead_air`), every block of words held under 0.3 s a word or 1 s
     (`short_hold`), and every block over 10 words, or a step label over 6 (`too_many_words`).
     Pass the measured reveals inside a clip as `changes`; the JSON cannot see them. Then look
     at the frames for the 3 s: motion inside a clip is only on them;
   - **not one move everywhere**: when every beat has the same push or the same entrance, vary
     what the use case's skills allow;
   - **words inside the safe zone** of the destination the use case names: run the layouts skill's
     `safe_zone.py` with its profile, and fix each finding. Readable at the frame's width.

   Fix each finding, or keep it and say why in the review line ("the app itself is navy, so the
   canvas follows it").
7. Fix the layers and check again. Building is free.

**The brief, item by item.** When the use case has a brief (the message, the destinations, the
length, the hook, the call to action, the steps), grade the build against it one item at a time,
never as one judgement of the whole. From this skill's folder, run
`python3 scripts/checklist.py <file>` on `{ brief, scene }`, with the destinations as the layouts
skill's safe-zone profiles. It turns the brief into yes-or-no questions and grades the ones the
scene answers: the length, words by 0.5 s, the hook's words, the call to action at the end, the
safe zone, and `timing.py`. The rest are `look` items. Answer each from the frames of steps 4-6, with the frame's
time or the tool's line as `evidence`, and run it again with your `answers`; an answer without
evidence stays open. Fix only the items that say no, then grade again: never rebuild what passed.
Its `summary` goes with the review.

**The viewer panel.** On a short, before the user sees its hook or its draft, three simulated
viewers (a 15-year-old scrolling, a creator new to the topic, someone who already uses the
product) look at the first 2 s and then at the whole draft. Their answers are graded against a
pass bar with `scripts/panel.py`. It catches a hook that reads as an ad or promises the wrong
thing. It is not a measure of retention, and it says so.

**The critic panel.** After the viewer panel, before the user sees a draft, six simulated critics
with taste each look at it through one lens: the first-principles critic (the core problem the
video solves), the radical (the concept), the interface designer (the UI on screen), the story
editor (the message and the script), the growth strategist (the stop, the drops, the ending) and
the art director (the look). Each sees only frames every 0.5 s, the source stills (the real UI or
footage the video depicts), the words, the goal and the destination, and returns a verdict, problems with their times, and fixes. `scripts/critics.py`
picks the frames and lays the notes side by side. Where critics agree it is a must-fix, weighed
against the first-principles critic's core sentence; a new concept goes to the user as a choice,
never applied silently. A draft that looks different from its source is a must-fix.

**The challenger.** A seventh critic who does not wait for the draft. At each decision the use case
names (the idea, the plan, the key frames and each image picked, the UI, and every SPEND before
its quote) it asks "why this?" and tries to show that the direction is wrong before more work is
spent on it. It returns `keep`, `rethink` or `stop`, with the reason and the cheaper alternative.
It also gets the source stills, so a design that drifts from the real app is caught as it is made.

| Read this | Before you |
|---|---|
| `references/viewer-panel.md` | run the viewer panel on a hook or a draft |
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
   the layouts skill's nested panel). Never reshape the
   whole scene to guess past it.

**Before you hand over an export.** An export can differ from its scene: another size, a dropped
frame rate, a missing sound track, a silent last second. Probe the file with
`picsart_media_probe_media`, which is free, and from this skill's folder run
`python3 scripts/qc.py <file>` on `{ scene, probe, audio? }`: the scene you exported, the probe as
it returned, and in `audio` only what a tool measured (loudness, true peak, the sound's length, an
energy curve). It prints `{ ok, errors, warnings, unchecked }`:

- an `error` (the size, the fps or the length is not the scene's, the sound is missing, drifts or
  peaks above -0.5 dBTP): make its `fix` and export again, once. Still there: deliver, and name it;
- a `warning` (loudness away from -14 LUFS, a silent tail over 1.2 s): say it in the delivery
  line;
- `unchecked`: what no tool measured. Never call it checked.

Frames show framing, not motion: the user judges timing and easing in REVIEW.

How many rounds you get, and what to do when they run out, is in video-core (Evaluation). Never
export to "show" a draft that the user can review live; video-core (Preview and export) says when
to export.

## The script, before the build

Before a short is built, voiced or generated, review its script: is it worth making, what is its
why, and which lines to rewrite. A video whose footage never shows its result is dropped before it
costs anything.

| Read this | Before you |
|---|---|
| `references/script-review.md` | review a script, or report its verdict |
