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

## `scene_editor_feedback` (v2)

Full contract: `docs/widget-specs/scene-editor.md` (the `picsart_scene_editor` widget —
the pair-review surface; **we always open it on a scene document — by `sceneUrl`, or inline as
`scene` — never video/media**). Shape:

```json
{
  "type": "scene_editor_feedback", "version": 2,
  "title": "f2 → f3",
  "duration": 3.8,
  "verdict": "needs_changes",
  "edited": false,
  "stateHash": "…",
  "documentUrl": "https://… the scene AS THE DESIGNER LEFT IT, as a hosted JSON file",
  "comments": [ { "instruction": "make the button slide in from the right" } ],
  "timelineComments": [ { "text": "hold longer before the zoom", "start": 1.2, "end": 2.0 } ]
}
```

- **`verdict`** — `"approved"`: flip that seam `approved: true` in `motion.json` and open the
  editor on the next pair. `"needs_changes"`: another pass — the comments say what and where.
- **`documentUrl` supersedes your copy when `edited: true`** — it is the scene as the designer
  left it. Pass the URL on, never the document: as `scene` to `patch_scene` and
  `picsart_scene_export`, as `sceneUrl` to reopen. Apply further changes with `patch_scene` **to
  it**, then reopen on the result; when `edited` is false it is unchanged from what you opened.
  Only when it could not be stored does the reply carry the scene inline as `document` — pass that
  as `scene` instead.
- **`comments` (pins on the frame) / `timelineComments` (marked stretches)** are the edit-request
  channels: a pin carries its own **`instruction`** and its moment, a stretch its own **`text`** and
  its `start`/`end` seconds. Fold each into the motion via `patch_scene` — the designer's words,
  don't restate before acting.
- **Both comment sets absent on `needs_changes`** = they edited the scene without saying anything
  more (Submit needs an edit or a comment) → their document is the answer. Absent on `approved` is
  normal.
- **It renders NOTHING — there is no `videoUrl`.** Do not look for a file, claim a save, or save to
  Drive from this reply. Export with `picsart_scene_export` only when the designer wants a file.
  (`generalComment` is legacy and typically absent — read the comment arrays.)

**When any panel's attached context conflicts with the designer's typed message, the MESSAGE wins.**
The typed instruction is the current intent (a panel's state can lag a click or a send); **act on
the message, note the discrepancy in one line, and move on** — don't stall asking them to re-click.
(This is the reverse of the normal case where the *silent payload carries the decision*; it applies
only when the two genuinely disagree.)

## Reviewing the whole reel

The storyboard's running order is Figma's, taken silently (see `design-layer-import`) — a markdown
table is the fallback for *optional* edits, never a question that confirms the order. To review
the finished reel end-to-end, open the editor on the **whole-scene document** (or export the
whole-reel video); reordering stays designer-initiated only.

## When a panel is not available

The editor has a tier-1 fallback so the flow never stalls: when `picsart_scene_editor` errors
(a 503, a transport failure, or an exception), export the scene with `picsart_scene_export` and
show the **result video** so the motion is still visible — dropping to contact-sheet frames +
questions only if the export ALSO fails; the storyboard stays a markdown table. The format has
no panel: it is asked in chat (`design-layer-import` *Set the format*).

**The editor fallback is a degraded last resort, not the intended experience.** The real review
surface is the **Cascade-styled panel** (`picsart_scene_editor`, live on the gen-ai server); a
bare ASK standing in for the *editor* means its call errored. Format questions are
different — a plain ASK for a genuinely open output-scale choice is the right surface,
not a fallback. Always call the editor first for review; fall back only when it actually fails.
