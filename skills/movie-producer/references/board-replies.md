# What each board sends back

How a decision reaches you depends on the host; the host notes say how. This file says what each
one holds and what to do with it. A board's first tool result is what the board will show, never
the user's decision. Nothing is decided by silence: a board that needs a verdict on every item
blocks its own send until it has one.

## The look: `film_setup_feedback`

| Field | Use |
|---|---|
| `verdict` | Always `locked`. The look is locked |
| `selections` | The console's picks as preset ids: `genre`, `tone`, `palette`, `ratio`, `duration` (whole seconds, as a string), `camera`, `lens`. `palette` is always `auto`: the console has no palette, and each shot picks its own. `lens` is a lens family, never a focal length. A `custom` genre or tone comes with `customGenre` / `customTone`, the user's own words. At compile time a custom genre goes as `look.customGenre` with no `genre`; a custom tone keeps `tone: "custom"` beside `customTone` |
| `selections.scheme`, `selections.hue` | Present when the user chose a colour scheme; absent means Auto, and the style line carries no colour. Pass them as `look.scheme` and `look.hue` on every `picsart_film_compile_prompt` call of this world, the cast's reference kinds included |
| `stylePrefix` | Store it verbatim. Never reword or rebuild it |
| `summary` | The console's one line; quote it back if you say anything |

The frame and the runtime in `selections` are the film's: every model pick and every run is made
against them.

## The model: `model_choice_feedback`

| Field | Use |
|---|---|
| `chosen` | `{ id, name }`, the model for the film |
| `comment` | Optional. A note about what happens is a story note: rewrite the story, show it, and open the model board again. A note about the model is answered on the model |

## The shot list: `shotlist_board_feedback`

| Field | Use |
|---|---|
| `verdict` | Always `approved` |
| `scope` | The scene ids the approval covers: exactly these |
| `scenes[]` | Per scene, the FINAL list in the user's order: `order` (live shot ids), `cut`, `reordered`, and `shots[]` |
| `shots[]` | Each shot whole: `id`, `action`, `line`, `feels`, `tags`, `values` (every decision, resolved), `genSec`, `recap`, and `cut`, `added` or `edited` when the user did that |
| `runs[]` | The grouping the user approved: `index`, `shots` (`sceneId:shotId`), `scenes`, `cutSec`, `genSec` (what to ask the model for), `overCeiling`, and `id` and `join` only while the run is still the one you planned |

- **Replace, never merge.** The board's list is the list. What the board does not carry
  (references, prompt versions, trims) stays attached by shot id.
- A shot marked `cut` is generated for nothing. A shot marked `added` has no design of yours yet:
  design it from its card.
- A run with no `id` has an edge the user made: its old join sentence describes a cut that is no
  longer there, so write a new one before the run is compiled.
- `overCeiling` means the run cannot be generated as one video. Say so, and propose the split.
- An `action` or `line` that changed what happens is a story note: rewrite the paragraph first.

## Pictures: `asset_review_feedback`

| Field | Use |
|---|---|
| `approved[]` | Each is locked: cut its views and save it with `picsart_film_save_asset`, `status: "locked"`. A `note` on an approved tile is kept on the asset's row |
| `changes[]` | Each carries a `note`, and `models` when the user asked to try other models. Regenerate THAT asset with the note folded into its own prompt, and change nothing else |
| `discarded[]` | The unchosen siblings of a same-tag, several-model comparison. Never save, use or regenerate them |
| `total` | `approved` + `changes` + `discarded` always equals it |
| a general note | Applies to the whole board; fold it into each change it concerns |

After changes, open a FRESH board with only the changed assets, each with `version` (`"v2"`) and
`previousUrl`, so the user can compare and ask to go back. Approved assets never reappear. Repeat
until `changes` is empty. A change is a new generation: its own SPEND.

## Renders: `render_monitor_feedback`

Posted by the batch's own card when every job of the call has finished. Match each row, `done` or
`failed`, to its run or asset by its `jobId`, against the `id` of the `job` each call returned.
Only a row without a `jobId` is matched by the `label` you gave it.

| Field | Use |
|---|---|
| `done[]` | `{ label, model, url, jobId }` per finished job, with `urls` too when it made several. Save them into the call's folder with one `picsart_drive_upload` (picsart-video-rules's SPEND rule 4), log each, look at it, and put it up for the user's verdict in this turn |
| `failed[]` | `{ label, model, error, jobId }`. Regenerate only these, each under a SPEND of its own, after reading the error |

## Footage: the scene editor

Its reply is picsart-video-rules's REVIEW: `approved`, or `needs_changes` with `edited`, `documentUrl`,
`comments` and `timelineComments`. For a film:

- **Trims and splits the user made are theirs.** Record each as a user trim on its shot; nothing
  automatic ever moves one.
- A comment on a take is a note to route: an edit, an extend or a re-roll (film-shot-generation).
- A comment on a seam is a join to diagnose before anything is bought (film-cutting).
- A comparison opened to choose between repair candidates is not the film: its reply picks a
  candidate and is never applied to the cut as an edit.
