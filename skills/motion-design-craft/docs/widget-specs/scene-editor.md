# Widget spec — `picsart_scene_editor`

The motion-review surface. It opens a **scene document
played in the user's browser by the scene engine, exactly as authored** — masks, per-keyframe
easing, corner radii, vector art and real glyph layout render as the format specifies, not as a
translation approximates — with a verdict bar (**Approve** / **Send with notes**) and an
edit-request layer (pins on the frame, marked stretches of the timeline).

Replaces the old scene inspector for pair review. It is the panel the designer watches
each pair in and approves or sends back.

## What we pass — a scene document, never video

For motion design we always open a **scene document**, not clips:

```ts
picsart_scene_editor({
  scene:  <the WHOLE scene built so far — the parsed JSON object, never a URL or string>,
  purpose: "motion",                 // ALWAYS for motion design — the motion tool set, see below
  title:  "f2 → f3",                 // heading — names the pair under review
  notes:  "Tell me what to change."  // one line under the title
})
```

**Always pass `purpose: "motion"`.** It gives the designer the motion tools and hides the footage
tools (trim, split, speed and the rest), which have nothing to act on in a scene with no video.
Left out, a scene with no video in it still opens as motion, but say it: a scene that carries a
video layer would otherwise open as a cut.

## What the designer can do in the editor

Besides commenting, the designer edits the scene by hand, and the edit comes back in `documentUrl`:

- **Transform** — pick any element on the picture, drag it to move it, drag a corner to resize it.
  The edit is **for the moment the playhead is on**: on an animated element it changes the keyframe
  at that moment, or adds one there, and the other keyframes keep their values, so the path now
  passes through the new point. An element with no position or scale keyframes moves or resizes
  for its whole span.
- **Add image** — upload a picture, or pick one from their saved assets or Drive. It arrives as a
  new top-level `media` layer over an `image` asset, drawn above everything, with no motion.

So an edited document can hold keyframes you did not write and a layer you did not make. See
"Reading the designer's own edits" below for what to do with them.

**Open on the whole scene built so far, positioned at the current pair — not a 2-frame sub-scene.**
The editor plays a timeline with a playhead, so the whole scene lets the designer watch the pair
*in context* (how it flows in and out) and scrub to it; `title` names the pair so they know where to
look. "Whole scene so far" = every composed frame up to now (later, uncomposed frames aren't there
yet). This matches the skill's rule that a shown result is always the reel, never one seam alone.

- **Pass `sceneUrl` whenever you hold one** — the `sceneUrl` a tool returned, or the reply's
  `documentUrl` — so the document is not written out again; otherwise pass `scene`. `scene` takes
  precedence over `sceneUrl`, `media` and `videoUrl` (`media`/`videoUrl` are the film/clip path —
  not ours).
- **Open the scene as it is.** A `scene_ref` stays a reference; change a placed scene through its
  parameters at the call site, and expand it (`picsart_scene_expand_ref`) only when the user asks
  to edit inside it. The engine resolves `assets[]` and `track` layers itself, and rejects a scene
  it can't open, naming each skipped layer.
- A **sealed** document is rejected, not repaired. Author/edit as an open scene.
- Every layer kind in the scene must be one the widget's engine build knows — a kind newer than
  that build boots to *"content kind X has no component"* (see `MOTION-TROUBLESHOOTING.md`).

## It renders NOTHING, and there is NO video file

The scene plays and is edited **in the browser, through the scene engine**. It is **free**,
spends no credits, and **produces no file**. Do **not** look for a `videoUrl`, do **not** claim
anything was saved, and do **not** save anything to Drive on the strength of the reply. (An older
film-review contract returned a rendered mp4 to save before it expired — that is a *different*
widget; this one does not.) When the designer wants a file, render the reply's `documentUrl` with
`picsart_scene_export`, as its `scene`.

## Feedback — `scene_editor_feedback` (v2)

Sent when the designer files a verdict:

```json
{
  "type": "scene_editor_feedback", "version": 2,
  "title": "f2 → f3",
  "duration": 3.8,
  "verdict": "needs_changes",
  "edited": false,
  "stateHash": "…",
  "documentUrl": "https://… the scene AS THE DESIGNER LEFT IT, as a hosted JSON file",
  "comments": [
    { "instruction": "make the button slide in from the right", "…": "a spot + its moment" }
  ],
  "timelineComments": [
    { "text": "hold this longer before the zoom", "start": 1.2, "end": 2.0 }
  ]
}
```

- **`verdict`** — `"approved"`: the pair is accepted → flip that seam `approved: true` in
  `motion.json` and advance to the next pair. `"needs_changes"`: another pass; the comments say
  what and where.
- **`documentUrl` supersedes your copy when `edited` is true.** It is the scene as the designer
  left it, with any edits they committed applied, as a hosted JSON file. Use *it*, not the scene you
  opened, for everything after — pass the URL, never the document: apply further changes with
  `picsart_scene_patch` **to `documentUrl`** (as its `scene`), then reopen the editor on the
  result. When `edited` is false, it is unchanged from what you opened.
- **`document` arrives instead of `documentUrl` only when the copy could not be stored** — the same
  scene inline. Pass that as `scene` to the same tools, and to the editor.
- **`comments` = pins on the picture; `timelineComments` = marked stretches** — the edit-request
  channels. A pin carries its own **`instruction`** (the designer's words) and its moment; a stretch
  its own **`text`** and its `start`/`end` seconds, so they say *where* a change goes. Fold each
  into the motion via `patch_scene`.
- **Either comment set may be absent** = the designer placed none. **Both absent on
  `needs_changes`** = they edited the scene without saying anything more (Submit needs an edit or a
  comment) → treat their document as the answer.
- **`stateHash`** names the committed edit, so re-opening the same state round-trips as the same
  edit, not a new one.
- **`generalComment` is legacy** — the Comments panel replaced the single free-text note; treat it
  as optional/absent and read `comments`/`timelineComments` instead.

## Model protocol

- **Opening the editor is the whole turn** — no prose above or below; it states its own ask
  (`title` + `notes`). After opening, **stop and wait**; the decision arrives on the send.
- **Author motion ONE pair at a time**, and advance only on an explicit `approved`. Author with
  `patch_scene`; the editor is the *review/preview/approval* surface, not where per-element motion
  is picked. (There is no per-element "click a layer, choose from motion candidates" ladder here —
  that was the old inspector; motion is authored by you and shown here to be judged.)
- **On `needs_changes`**, apply each comment (a pin's `instruction`, a stretch's `text`) to
  `documentUrl` via `patch_scene`, then reopen the editor on the new scene.
- **Reading the designer's own edits** (`edited: true`): the positions, sizes and keyframes in
  `documentUrl` are the designer's decision. Build on them; never put an element back where your
  copy had it, and never drop a keyframe or a layer because you did not author it. A layer that is
  new to you is an image they added: keep it where they placed it, record it in `motion.json` as an
  element of that frame, and ask what it should do only if no comment says. If a comment and a
  hand edit disagree about the same element, the comment is the newer intent: apply it on top of
  the edited document.
- **Never re-export to "show" a result** — the editor already plays the scene live and free.
  Reserve `picsart_scene_export` for the final deliverable and the error fallback.

## When the editor is not available

If the call errors (a 503, a transport failure, or an exception), fall back exactly as before:
`picsart_scene_export` the scene and show the **result video** so the motion is still visible,
dropping to `contact_sheet` frames + an ASK only if the export ALSO fails. Write the
same `motion.json` either way. The fallback is a degraded last resort, not the intended surface —
always call the editor first.
