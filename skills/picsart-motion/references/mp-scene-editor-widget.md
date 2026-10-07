# Widget spec — `picsart_scene_editor`

The motion-review surface. It opens an **MP Scene document
played in the user's browser by the scene engine, exactly as authored** — masks, per-keyframe
easing, corner radii, vector art and real glyph layout render as the format specifies, not as a
translation approximates — with a verdict bar (**Accept** / **Submit**) and an
edit-request layer (pins on the frame, marked stretches of the timeline).

It is the panel the designer watches each pair in and approves or sends back.

## What we pass — `scene`, never video

For motion design we always open a **scene document**, not clips:

```ts
picsart_scene_editor({
  scene:  <the WHOLE scene built so far — the parsed JSON object, never a URL or string>,
  title:  "f2 → f3",                 // heading — names the pair under review
  notes:  "Tell me what to change."  // one line under the title
})
```

**Open on the whole scene built so far, positioned at the current pair — not a 2-frame sub-scene.**
The editor plays a timeline with a playhead, so the whole scene lets the designer watch the pair
*in context* (how it flows in and out) and scrub to it; `title` names the pair so they know where to
look. "Whole scene so far" = every composed frame up to now (later, uncomposed frames aren't there
yet). This matches the skill's rule that a shown result is always the reel, never one seam alone.

- `scene` takes precedence over `media`/`videoUrl` (those are the film/clip path — not ours).
- **Expand any `scene_ref` layer first** (`picsart_media_expand_scene_ref`, or build with
  `picsart_media_apply_scene_template` mode `bootstrap`) — the engine resolves `assets[]` and
  `track` layers itself, but not a template reference, and rejects a scene it can't open, naming
  each skipped layer.
- A **sealed** document is rejected, not repaired. Author/edit as an open MP Scene.
- Every layer kind in the scene must be one the editor can play — an unknown kind fails with
  *"content kind X has no component"* (see `motion-troubleshooting.md`).

## It renders NOTHING, and there is NO video file

The scene plays and is edited **in the browser, through the MP Scene engine**. It is **free**,
spends no credits, and **produces no file**. Do **not** look for a `videoUrl`, do **not** claim
anything was saved, and do **not** save anything to Drive on the strength of the reply. When the designer wants a file, render `document` with
`picsart_media_export`.

## Feedback — `scene_editor_feedback` (v1)

Sent when the designer files a verdict:

```json
{
  "type": "scene_editor_feedback", "version": 1,
  "title": "f2 → f3",
  "duration": 3.8,
  "verdict": "needs_changes",
  "edited": false,
  "stateHash": "…",
  "document": { "…": "the scene document AS THE DESIGNER LEFT IT" },
  "comments": [
    { "instruction": "make the button slide in from the right", "…": "a spot + its moment" }
  ],
  "timelineComments": [
    { "text": "hold this longer before the zoom", "start": 1, "end": 2 }
  ]
}
```

- **`verdict`** — `"approved"` (Accept without edits/comments): the pair is accepted → flip that seam `approved: true` in
  `motion.json` and advance to the next pair. `"needs_changes"` (Submit after edits/comments): use the returned document and apply any
  comments for another pass.
- **`document` supersedes your copy when `edited` is true.** It is the scene as the designer left
  it, with any edits they committed applied. Use *it*, not the scene you opened, for everything
  after — apply further changes with `picsart_media_patch_scene` **to `document`**, then reopen the
  editor on the result. When `edited` is false, `document` is unchanged from what you opened.
- **`comments` = pins on the picture; `timelineComments` = marked stretches** — the edit-request
  channels. Frame pins carry **`instruction`** (the designer's words); timeline stretches carry
  **`text`**, **`start`** and **`end`** seconds, so they say *where* a change goes. Fold each into the motion via `patch_scene`.
- **Either comment set may be absent** = the designer placed none. **Both absent on
  `needs_changes` with `edited: true`** = use the returned `document` as their requested change.
  Ask for clarification only when there is no edit or usable requested change.
- **`stateHash`** names the committed edit, so re-opening the same state round-trips as the same
  edit, not a new one.

## Model protocol

- **Opening the editor is the whole turn** — no prose above or below; it states its own ask
  (`title` + `notes`). After opening, **stop and wait**; the decision arrives on the send.
- **Author motion ONE pair at a time**, and advance only on an explicit `approved`. Author with
  `patch_scene`; the editor is the *review/preview/approval* surface, not where per-element motion
  is picked. (There is no per-element "click a layer, choose from motion candidates" ladder here —
  motion is authored by you and shown here to be judged.)
- **On `needs_changes`**, use the returned `document`, apply each frame pin's `instruction` and each
  timeline stretch's `text` at its `start`/`end` via `patch_scene` when present, then
  reopen the editor on the new scene.
- **Never re-export to "show" a result** — the editor already plays the scene live and free.
  Reserve `picsart_media_export` for the final deliverable and the error fallback.

## When the editor is not available

If the call errors (a 503, a transport failure, or an exception), fall back:
`picsart_media_export` the scene and show the **result video** so the motion is still visible,
dropping to `contact_sheet` frames + the host question interface only if the export ALSO fails. Write the
same `motion.json` either way. The fallback is a degraded last resort, not the intended surface —
always call the editor first.
