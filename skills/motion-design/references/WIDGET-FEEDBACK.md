# Reading the motion panels' feedback

**HARD RULE — read app context on every panel-triggered turn.** Before interpreting the
short visible sentence, replying, updating `motion.json`, or acting, read the latest
widget/app context attached to that turn. Treat the visible sentence and the silent
payload as **one message**: the sentence is the trigger; the payload carries the decision.
A trigger with no JSON in the transcript is normal — never claim the panel sent nothing,
and never ask the designer to repeat, re-click, or paste JSON until you've checked the
attached context.

- **Opening a panel is the whole turn** — no prose above or below it; it states its own ask.
- **After opening, stop and wait.** The decision arrives on the send.
- **Speak after they act** — the readback, what changed, the cost, the next step all go
  in the turn *after* their send.

## `scene_editor_feedback` (v1)

Full contract: `docs/widget-specs/mp-scene-editor.md` (the `picsart_scene_editor` widget —
the pair-review surface; **we always open it with a `scene` document, never video/media**). Shape:

```json
{
  "type": "scene_editor_feedback", "version": 1,
  "title": "f2 → f3",
  "duration": 3.8,
  "verdict": "needs_changes",
  "edited": false,
  "stateHash": "…",
  "document": { "…": "the MP Scene AS THE DESIGNER LEFT IT" },
  "comments": [ { "instruction": "make the button slide in from the right" } ],
  "timelineComments": [ { "instruction": "hold longer before the zoom" } ]
}
```

- **`verdict`** — `"approved"`: flip that seam `approved: true` in `motion.json` and open the
  editor on the next pair. `"needs_changes"`: another pass — the comments say what and where.
- **`document` supersedes your copy when `edited: true`** — it is the scene as the designer left
  it. Apply further changes with `patch_scene` **to `document`**, then reopen on the result; when
  `edited` is false it is unchanged from what you opened.
- **`comments` (pins on the frame) / `timelineComments` (marked stretches)** are the edit-request
  channels; each carries its own **`instruction`** and the moment/stretch it is about. Fold each
  into the motion via `patch_scene` — the designer's words, don't restate before acting.
- **Both comment sets absent on `needs_changes`** = a redo was asked for without saying where → ask
  what to change. Absent on `approved` is normal.
- **It renders NOTHING — there is no `videoUrl`.** Do not look for a file, claim a save, or save to
  Drive from this reply. Export with `picsart_media_export` only when the designer wants a file.
  (`generalComment` is legacy and typically absent — read the comment arrays.)

## `motion_setup_feedback` (v1)

The `picsart_motion_setup` console (the Motion Setup panel) sets the video-wide format once, at
the start of a project — how to open it prefilled is in `motion-import` *Set the format*. While
the designer adjusts it, the panel publishes the current pick as silent context; **nothing is
decided until they lock it** — never store a target from that in-progress context. The lock
arrives as:

```json
{
  "type": "motion_setup_feedback", "version": 1,
  "selections": {
    "ratio": "9:16", "fps": 30, "energy": "standard",
    "hold": 2, "transition": "slide", "transitionDuration": 0.5,
    "duration": { "mode": "derived" }
  },
  "summary": "…",
  "verdict": "locked"
}
```

- **Store `selections` into `motion.json.target`**: `ratio` → width/height, `fps`; `hold`,
  `transition` (`""` = a hard cut) and `transitionDuration` are the project's hold and seam
  defaults; `energy` is the register (`MOTION-PRINCIPLES.md` §6).
- **Quote `summary` verbatim** — don't reassemble it from the fields.
- **`duration.mode: "derived"`** (the default) = total is the sum of the holds, each grown to fit
  its motion. **`"target"`** (with `seconds`) is a **soft** budget: never clip a hold below its
  motion-minimum, so a too-short target lengthens the video rather than cutting an animation.
- A designer who wants a new format later says so; reopen the console with the locked
  `selections` as `current`.

**When any panel's attached context conflicts with the designer's typed message, the MESSAGE wins.**
The typed instruction is the current intent (a panel's state can lag a click or a send); **act on
the message, note the discrepancy in one line, and move on** — don't stall asking them to re-click.
(This is the reverse of the normal case where the *silent payload carries the decision*; it applies
only when the two genuinely disagree.)

## Reviewing the whole reel

The storyboard's running order is Figma's, taken silently (see `motion-import`) — a markdown
table is the fallback for *optional* edits, never a question that confirms the order. To review
the finished reel end-to-end, open the editor on the **whole-scene document** (or export the
whole-reel video); reordering stays designer-initiated only.

## When a panel is not available

The editor has a tier-1 fallback so the flow never stalls: when `picsart_scene_editor` errors
(a 503, a transport failure, or an exception), export the scene with `picsart_media_export` and
show the **result video** so the motion is still visible — dropping to contact-sheet frames +
questions only if the export ALSO fails; the storyboard stays a markdown table. When
`picsart_motion_setup` is not in your list or errors, decide the format directly instead —
infer ratio/fps/energy from the frames, state them in one line, and let the designer adjust in
plain conversation (`motion-import` *Set the format*). Write the same `motion.json` either way.

**The editor fallback is a degraded last resort, not the intended experience.** The real review
surface is the **Cascade-styled panel** (`picsart_scene_editor`, live on the gen-ai server); a
bare ASK standing in for the *editor* means its call errored. Format questions are
different — a plain ASK for a genuinely open output-scale choice is the right surface,
not a fallback. Always call the editor first for review; fall back only when it actually fails.
