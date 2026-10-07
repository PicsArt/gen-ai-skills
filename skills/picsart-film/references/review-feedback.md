# Reading the review boards' feedback

This is the base contract for the shared review boards —
`model_choice_feedback`, `asset_review_feedback`, `scene_editor_feedback` — and
`widget-feedback.md` beside it carries the film-only boards and the film's deltas
on these.

**Film workflow precedence:** discover the live tool schema before using these
fields. For film repair routing and preview promotion, follow
`../../picsart-film-edit/references/workflow.md`; focused join work follows
`../../picsart-film-edit/references/join-repair.md`. A comparison reel's
approval selects a candidate, not a new full-film timeline: it is not the
movie, and its cut feedback never replaces the accepted film wholesale.

The three review tools open a UI in the chat. Nothing comes back from the tool call
itself beyond the payload you passed in — the user's decisions arrive **later, once
they press the send button**.

So: after calling a review tool, stop and wait. Do not start regenerating on
speculation, and do not ask the user to describe in prose what the board is already
collecting.

**Where the decisions arrive.** A send is one event on two channels: a short
**message from the user** naming what they decided in one human sentence that ends
with the board's own cue that the decision is in the widget context, and the
**payload** delivered silently as widget context — the same sentence, the fenced
JSON block, then one line of instruction. Before replying, read that context:
where the host attaches it to the turn, read it there; otherwise call the host's
widget-context tool, if it has one, and act on what it returns. The sentence is
your cue that a board was sent; the payload is where the decisions are. Do not
expect the JSON inside the user's message, never ask them to paste it, and never
say the board sent nothing until the attached context and any widget-context
tool have both come back empty; if neither is available, ask for the missing
decision. On a host with no silent channel the two arrive fused into that one
message instead; the content is identical either way.

That silent channel also carries **work-in-progress state** while the user is still
marking up, so if they abandon the board and just type "go with the second one", you
will usually have enough context to resolve that — but never treat in-progress state
as a decision. It stops updating once a board is sent, so a send's payload is never
overwritten by a half-finished markup behind it.

Every payload carries `type` and `version`; if `version` differs from the one in
the example, read the block on its own terms rather than assuming these names.

## `model_choice_feedback`

```json
{
  "type": "model_choice_feedback",
  "version": 1,
  "purpose": "9:16 hero video, 4 shots, character must stay consistent",
  "chosen": { "id": "seedance-2.5", "name": "Seedance 2.5" },
  "comment": "prefer the longer take even at 720p"
}
```

What to do: record `chosen.id` as the plan's `model.id` and treat it as settled —
do not re-litigate the pick unless the project's constraints change (in which case
open a fresh board and say what changed). Validate parameters with
`picsart_model_params` and preflight before the first generation.

## Storyboard review — an edit in the scene editor

A cut's trims and splits are made by the user in the scene editor and arrive as its edited `document`
(`scene_editor_feedback`, below). Everything in that document is **free** —
carry it forward and never re-render on its account. Direction (a camera move,
a colour, the light, a performance) arrives as the user's own words in a
comment; the editor has no preset panel.

## `asset_review_feedback`

```json
{
  "type": "asset_review_feedback",
  "version": 3,
  "purpose": "the assets sc01 needs",
  "total": 3,
  "approved": [
    { "id": "a-1", "tag": "@cal", "label": "Cal", "url": "https://…", "version": "v1" },
    { "id": "a-3", "tag": "@mug", "label": "The mug", "url": "https://…", "version": "v1" }
  ],
  "changes": [
    { "id": "a-2", "tag": "@diner", "label": "The diner", "url": "https://…",
      "version": "v1", "note": "colder light, and lose the neon",
      "models": ["flux-2-pro", "nano-banana-2"] }
  ],
  "generalComment": "keep the boots muddy"
}
```

The board asks one question of each asset — approve it, or send it back with a
note — so the payload has one shape and no modes.

**`models` asks for a comparison, and it is the one time a tag may appear
twice.** Each named model returns ONE new version of that asset, and they all
belong on the SAME next board as sibling tiles sharing the tag, each badged with
the model that made it — the user approves one and the rest are discarded.
Omitted or empty means re-try on the model that made it. Everywhere else, two
tiles sharing a tag is still an error, because "approve @cal" cannot name two
images.

- **`approved.length + changes.length === total`, always.** Every asset on the
  board is in exactly one array. The widget blocks its own send until every tile
  has a verdict, so there is no third state to interpret and **nothing is ever
  decided by silence**. If the arithmetic does not hold, the payload is
  truncated — say so rather than guessing at the remainder.
- **There is no `verdict` field.** The two arrays are the verdict: an empty
  `changes` means the batch is finished.
- `approved[]` — record each one as settled **per your skill's archive step**
  (film: `picsart_save_asset`; other flows: the plan's `assets`). Never re-board
  or re-ask about an approved asset. `note` may ride along as an optional remark.
  A kept asset that needs its background cut gets `picsart_remove_bg` as its own
  call, not as a rider on a verdict.
- `changes[]` — each carries a **`note`, always non-empty** (the widget refuses
  to send a change without one). Regenerate **that one asset**, folding its note
  into its own prompt and changing nothing else. Several assets flagged is
  several independent regenerations, never one blended prompt. A change may also
  carry **`models`** (≤3): then that asset returns ONE version per named model,
  all on the SAME next board as sibling tiles sharing its tag, each badged with
  the model that made it — the only case where two tiles legitimately share a
  tag.
- Then open a **fresh board with only the changed assets**, `version` bumped and
  `previousUrl` set to the URL just rejected — the widget cannot update itself
  after a send, and the "was" thumbnail is what lets the user say "go back".
  Loop until `changes` is empty.
- `tag` is present when the caller had one (the film flow); otherwise the
  board sends `label` only.

**One version per asset, not a pick.** Generate a single still of each asset and
let the user iterate on it. Do not fan out 2–4 candidates of one thing and ask
them to choose — passing variants of one asset as
separate tiles makes "approve @cal" name two images (the widget flags a
duplicated `tag` for exactly this reason).

## `scene_editor_feedback`

Takes and cuts are reviewed in the scene editor, `picsart_scene_editor`.
Open it on a **scene
document**: the montage the assembly builds and validates
(`../../picsart-film-edit/references/assembly.md`), passed as `scene` — the parsed
object, never a URL or a string. `videoUrl` is only for a film that has exactly
one video. `title` and `notes` are the only other inputs: the editor carries no
per-shot prompt, cast or segment, so the link from a moment back to its shot is
your own bookkeeping (below). The document plays in the user's browser, and on
it they can trim a clip's edges, split, delete, duplicate, adjust, change speed,
effects, volume and size, pin comments on the picture and mark stretches of the
timeline. They end it with the one send button: **Accept** (`approved`, nothing
edited or commented) or **Submit** (`needs_changes`, once they edit or comment).

**It is free and renders nothing.** Edits are applied to the document in the
browser; no file is produced and no credits are spent. There is no `videoUrl`
in the reply: do not look for a file, do not claim anything was saved, and do
not save anything to Drive on the strength of it. When a file is wanted, render
`document` with `picsart_media_export` — render time and a Drive file, not
credits.

The payload's shape and every field are in `widget-feedback.md` beside this
file (`scene_editor_feedback`). How to act on it:

- **`verdict`** — `approved` is permission to move to the next pass; do not
  re-review the same cut. `needs_changes` is another pass, and the comments say
  what and where.
- **`edited` and `document` are an EDIT THE USER ALREADY MADE**, not a request.
  When `edited` is true, `document` is the cut as they left it and it
  **supersedes the scene you opened** — use it, not your copy, for everything
  after, and never re-render on its account. Read the cut back off it: its clips
  in playback order — the clips of the montage's `track` layer, or top-level
  media layers in a scene built by hand — each over its source (`assetId` into `assets[]`, or an
  inline `asset`) with `content.trim` in that source's seconds. That is each
  shot's piece and keep-window; write it to the shot's `trim` with
  `trimSource: "user"`. A split is two clips on one source with adjacent
  windows; a deleted shot is a clip that is no longer there. When `edited` is
  false, `document` is the scene you opened.
- Either set may be absent, which means the user placed none. **Both absent on
  `needs_changes`** means they asked for another pass without saying where — ask
  them. There is no separate general note.

**The comments are the only part that can spend.** Diagnose each note before
choosing compositor work or generation — a join note goes through
`../../picsart-film-edit/references/join-repair.md` first, and a note the timeline can
answer (tighter, later, shorter, drop this stretch) is a free compositor edit
on `document` with `picsart_media_patch_scene`, never a regeneration. Fold every
note on one shot into **one** new take of that shot, changing only what the
notes ask, and run the prompt-verify step
(`../../picsart-film-scenes/references/prompt-verify.md`) before a generative repair. A
paid repair is quoted and waits for the yes like any other purchase.

- **A note that asks only for a different camera move is a CAMERA-CHANGE
  RETAKE — anchor it, do not re-prompt the shot.** The editor has no preset
  panel, so read the words; a move named in them is the shot list's own
  vocabulary (`Slow push-in` means what that shot's plan meant by it). Take a
  frame from the start of that shot's source and send it as a **reference image
  alongside the shot's locked asset references**, all of them as references
  together, then name the opening frame in the prompt. Recompile only the
  camera-move block. Cast, wardrobe, set and light survive because they arrive
  as pixels; only the camera changes.
  - Do **not** put the frame in a first-frame / start-frame role. A frame role
    and reference images are alternatives on these models, and a payload holding
    both is rejected *after* the wait.
  - Do **not** pass the old take as a reference **video**. A reference video
    supplies camera motion, so it would reinstate the very move being changed —
    the user pays and sees nothing move.
  - A note that changes the move **and** something else is an ordinary
    regeneration: an opening-frame anchor would fight a new lighting or colour
    note.
- **A pin that asks to keep what is on screen is a KEPT FRAME — a constraint on
  regenerating, not a note** (*"keep this face"*, *"this frame is right"*). The
  editor has no keep-frame button, so the pin's words are the signal and its
  `time` is the moment. It survives **pixel-for-pixel**: map the time to the
  shot's source second (below), export that frame at native size (a frame
  extraction, not a re-render) and feed it back as a frame anchor, so only the
  motion BETWEEN kept frames is made again.
  - **Two consecutive kept frames bound ONE generation** — first frame and last
    frame. So N kept frames inside a shot means **N-1 generations**, not one, and
    a model taking exact start/end frames takes no reference media beside them.
  - A single kept frame at the head of a shot is just its start frame.
  - Kept frames do **not** by themselves mean the cut needs changing: they can
    ride on `verdict: "approved"`, where they are simply on the record for
    whatever gets regenerated later.
- **A stretch nobody commented on is kept.** There is no "keep" reply.

### Mapping a comment back to a shot

A pin whose `layerId` resolves to a clip names it directly; match the clip to the shot by
its source and window in your `film.json` record. Every other time — a pin on a
bare frame, a marked stretch — is measured on the **assembled** scene, not in a
shot's own seconds. Walk the clips in playback order, accumulating each one's
played length (`trim.out - trim.in`, or its full duration), and the clip whose
accumulated span contains the time is the shot; the second inside it, plus its
`trim.in`, is the source second. Do the arithmetic when a stretch straddles a
seam, and when it does, treat it as touching **both** shots rather than guessing
one.

### The chain-invalidation decision

If a regeneration lands on shot *k*, it changes *k*'s last frame, so any
downstream shot that took a frame from it as a reference must be rechecked, not
silently regenerated. Inspect the new boundary and follow
`../../picsart-film-edit/references/join-repair.md`: existing trims or coverage may work;
a missing beat may need an insert; genuinely changed state may require rebuilding
dependent footage. Explain the affected clips and quote any charged work. Neither
re-chaining nor covering the seam with a transition guarantees continuity.

## When the boards are not available

If a connected server does not expose these tools, the loop still works, just blind:
render a few frames with `picsart_media_contact_sheet` around the ranges you suspect
(render time only, so target the needed frames), show them, and ask directly which stretches to
redo. Keep the same plan bookkeeping either way.
