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

Full contract: `mp-scene-editor-widget.md` (the `picsart_scene_editor` widget —
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
  "timelineComments": [ { "text": "hold longer before the zoom", "start": 1, "end": 2 } ]
}
```

- **`verdict`** — `"approved"` (Accept without edits/comments): flip that seam `approved: true` in `motion.json` and open the
  editor on the next pair. `"needs_changes"` (Submit after edits/comments): use the returned document and apply any
  comments for another pass.
- **`document` supersedes your copy when `edited: true`** — it is the scene as the designer left
  it. Apply further changes with `patch_scene` **to `document`**, then reopen on the result; when
  `edited` is false it is unchanged from what you opened.
- **`comments` (pins on the frame) / `timelineComments` (marked stretches)** are the edit-request
  channels: frame pins carry **`instruction`**; timeline stretches carry **`text`**, **`start`** and
  **`end`** seconds. Fold each
  into the motion via `patch_scene` — the designer's words, don't restate before acting.
- **Both comment sets absent on `needs_changes` with `edited: true`** = the returned
  `document` is the requested change; use it. Ask for clarification only when there is no edit
  or usable requested change. Absent on `approved` is normal.
- **It renders NOTHING — there is no `videoUrl`.** Do not look for a file, claim a save, or save to
  Drive from this reply. Export with `picsart_media_export` only when the designer wants a file.

## Format is decided directly — no setup widget

This workflow decides format directly and does not use `picsart_motion_setup`. Ratio/resolution, fps and energy are inferred and stated to the designer (see `picsart-motion-import` *Set the format*); **total
duration stays derived** by default (total = sum of the holds, each grown to fit its motion; a
designer who wants it tighter says "punchier"). Store the chosen values into `motion.json.target`.
This workflow requires no `motion_setup_feedback` payload.

**When any panel's attached context conflicts with the designer's typed message, the MESSAGE wins.**
The typed instruction is the current intent (a panel's state can lag a click or a send); **act on
the message, note the discrepancy in one line, and move on** — don't stall asking them to re-click.
(This is the reverse of the normal case where the *silent payload carries the decision*; it applies
only when the two genuinely disagree.)

## Reviewing the whole reel

The storyboard's running order is Figma's, taken silently (see `picsart-motion-import`) — a markdown
table is the fallback for *optional* edits, never a question that confirms the order. To review
the finished reel end-to-end, open the editor on the **whole-scene document** (or export the
whole-reel video); reordering stays designer-initiated only.

## When a panel is not available

The editor has a tier-1 fallback so the flow never stalls: when `picsart_scene_editor` errors
(a 503, a transport failure, or an exception), export the scene with `picsart_media_export` and
show the **result video** so the motion is still visible — dropping to contact-sheet frames +
questions only if the export ALSO fails; the storyboard stays a markdown table. Format needs no
panel at all — it's decided directly (above). Write the same `motion.json` either way.

**The editor fallback is a degraded last resort, not the intended experience.** The real review
surface is the panel (`picsart_scene_editor`); a
question in the host question interface standing in for the *editor* means its call errored. Format questions are
different — a question in the host question interface for a genuinely open output-scale choice is the right surface,
not a fallback. Always call the editor first for review; fall back only when it actually fails.
