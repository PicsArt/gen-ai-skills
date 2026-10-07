# Widget spec — `picsart_asset_review`

Review board. **One question: is this asset good?** A grid of the assets you just
generated, one tile each, and two actions per tile — **Approve** or **Change**.
Approved assets are saved and never asked about again; changed ones come back on
a fresh board as a new version. The board is done when nothing is left to change.

The board has one job. It does not cast between candidates, it does not run a
consistency battery, and an untouched tile never means anything: every tile
gets an explicit verdict.

## Tool input

```ts
{
  purpose: string,                 // 'the assets sc01–sc03 needs'
  assets: Array<{                  // 1..12 — ONE ENTRY PER ASSET
    url: string,                   // Picsart-hosted https only
    label?: string,                // 'The diner'  (falls back to 'Asset N')
    tag?: string,                  // '@diner' — film flow has one, video flow does not
    version?: string,              // 'v1', 'v2' …
    previousUrl?: string,          // the version this one replaces
    prompt?: string,
    model?: string,
    info?: string[],               // ≤4 lines: ['location', 'serves sc01–sc03']
    why?: string,                  // one sentence: what THIS asset has to carry
  }>,
  judge?: string,                  // 'the face and the light, not the clothes'
  notes?: string,                  // one line of guidance above the grid
  imageModels?: Array<{ id: string, why?: string }>,  // from a live catalog read
}
```

`why` is `judge` per asset — "every shot cuts back to this face, get it right
first" — on its own line under the info. `imageModels` never hardcodes an id;
read the catalog, and omit the field when you have not.

**One tile per asset.** These are different things — a character, a location, a
prop — not variants of one thing. Generate **one** version of each asset and let
the user iterate on it; do not fan out candidates and ask them to pick. Two tiles
sharing a `tag` is flagged in the UI, because "approve @cal" cannot name two
images.

**The one exception is a multi-model retry.** When a previous board's change
carried `models`, the next board legitimately shows several tiles of the SAME
asset, one per model, each with its `model` badge — the user asked to compare.
That is the only case where a shared tag is expected rather than an error.

**Batching.** One board per scene block, assets deduped — an asset appears in the
batch of its first scene and never again, so a lead is reviewed once rather than
once per scene. Split a block that exceeds 12 tiles.

**`previousUrl` earns its place on iteration boards.** Serial iteration is
cheaper than parallel candidates but it loses side-by-side comparison, so a v2
tile carries a thumbnail of the v1 it replaces. That is what keeps "go back to
the first one" available without a pick mode.

## Layout

- **Header**: *"Approve the cast, or send any back"* with `notes` beneath it
  (default: *"Approve what works. Anything you send back comes straight to a new
  board."*). The counter and the approve-all button live in the progress bar and
  footer respectively, not here.
- **`Judge by:` line** under the header when `judge` is passed. Without it users
  judge everything and stall on nothing.
- **Grid**, always **two up** (one when there is a single asset), in a centred
  column so a tile stays big enough to judge a face on. Per tile: the square
  image, `version` + `model` badges together **top-left** (on a retry board
  those two badges are the only thing telling sibling tiles apart), the
  `previousUrl` "was" thumbnail, then tag · `info` on one line and `why` under
  it.
- **Two actions per tile, and they are not peers.** `Approve` is a pill;
  `Change this` is a text button with a pencil. One is the answer most tiles
  get, the other opens work. Approving turns the pill green, badges the image
  `✓ Approved` and rings the card; `Change this` becomes `✕ Never mind`.
- **The change panel** — note (**required**) plus `Try it on`: the models this
  asset may be re-tried on, **up to three**, each returning one new version. A
  line under it says what the picks buy in the count chosen ("you get 3 versions
  of this asset on the next board, one from each model"). Chips come from
  `imageModels`; absent, no model choice is offered and the same model tries
  again.
- **Progress bar** under the header with `N of M decided`, turning green when
  nothing is left.
- **Footer**: optional overall comment, a hint naming what is pending, `Start
  over` once anything is touched, and ONE primary that says what pressing it
  does — `Approve all N remaining` while tiles are undecided (the fastest true
  answer for a clean batch, never a disabled Send the user has to earn), then
  `Send N back` if anything is going back, or `Approved` if nothing is.
- The board carries no edit shortcuts (cut out, enhance). It is a verdict
  surface; an edit is its own tool call after the verdict.
- **Nothing is decided by silence.** An untouched tile is *pending*, and the
  board holds its own send until every tile has a verdict and every change has
  its note.

## Feedback → `asset_review_feedback` version 3

Full contract in
`../../picsart-film/references/review-feedback.md`.

```json
{
  "type": "asset_review_feedback", "version": 3,
  "purpose": "the assets sc01 needs", "total": 3,
  "approved": [ { "id": "a-1", "tag": "@cal", "label": "Cal", "url": "…",
                  "version": "v1" } ],
  "changes":  [ { "id": "a-2", "tag": "@diner", "label": "The diner", "url": "…",
                  "version": "v1", "note": "colder light, and lose the neon",
                  "models": ["flux-2-pro", "nano-banana-2"] } ],
  "generalComment": null
}
```

A change may carry **`models`** — at most 3, omitted when empty (empty would
mean the same thing as absent, so the reader never has to tell them apart).

**`models` is the one sanctioned fan-out on this board.** Normally a tag names
exactly one image, which is why two tiles sharing a tag is flagged. A multi-model
retry deliberately returns several versions of the SAME asset on the next board —
sibling tiles sharing its tag, each badged with the model that made it — and
approving one discards the rest. **Scope the duplicate-tag warning accordingly:
it is an error on a first-round board and expected on a retry board.** The
feedback message says this explicitly whenever `models` is present, and says
nothing about it otherwise.

- **`approved.length + changes.length === total`, always.** That one checkable
  line is the whole rule for untouched tiles: there are none.
- **There is no `verdict` field.** The two arrays are the verdict: `changes`
  empty means the batch is done.
- **There is no reject action.** "None of this works" is a `Change` with a note
  that says what to try instead.
- Approved → save it. Film: `picsart_save_asset` with `projectFolderUid` and
  `status: "locked"`, no `stressTest` — the approve click *is* the lock, and the
  views are cut at that moment (`workflow.md`, *The conveyor*, step 4). Read
  `locked` in the result. Video: record the URL in the plan's `assets`.
- Changed → regenerate **that one asset** with its `note` folded in surgically,
  then open a **fresh board** with only those, `version` bumped and
  `previousUrl` set. Approved assets are never re-boarded.
- The board publishes in-progress state silently while the user decides, so a
  typed "the diner is fine" can be resolved. In-progress state is never a
  decision.
