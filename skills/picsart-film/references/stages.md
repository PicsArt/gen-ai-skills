# Film — stages

## The pipeline — 11 stages, 5 working phases, gates between them

Stage numbers are the shared vocabulary; use them even though skills group them.

| Phase | Stages | Skill | Gate to pass |
|---|---|---|---|
| A · Development | 1 Breakdown · 2 References · 3 Bible | `picsart-film-development` | descriptors drafted, style prefix compiled (the lock itself is the sheet approval in B) |
| B · Assets | 4 Asset sheets · 5 Library | `picsart-film-assets` | every sheet approved on one board = `locked`; every scene's tags covered |
| C · Scenes | 6 Generation | `picsart-film-scenes` | all shots `final`, in selects |
| D · Edit | 7 Edit · 8 Cleanup (run together) | `picsart-film-edit` | the cut the user called final |
| E · Finishing | 9 Color · 10 Sound · 11 Master | `picsart-film-finishing` | masters exported, archive saved |

**Stage 1 runs in a fixed order:** idea → look console with frame and
runtime pre-set, locked → story and video-model choice in one response when
the host supports it → one shot list board carrying the video plan's run
assignments and joins. The submitted board approves both together.
`picsart_film_setup` comes before a word of story because genre
decides how the story is told, and because every shot inherits the locked
style prefix, lens family and colour scheme. The model board comes after the story and before
the video plan because the plan is written against the model's ceiling and
reference budget. A note about what happens, at any stage, is answered with a
rewritten story paragraph, never a board (`picsart-film-development`). Store the returned
`duration` seconds in `film.json.target.duration`. When the user has said
anything about format — vertical, TikTok, square, scope — pass it as
`suggested.selections.ratio`, in whatever words they used (`vertical`, `9:16`
and `vert` all resolve); the console cannot infer it and opens on 16:9. If the
genre changes at any point, the story is rewritten first
(`picsart-film-development`).

**Gates are the product.** The most expensive mistake in AI film production is
generating video for a scene whose assets are not locked — half the material gets
redone. A gate is passed only when its checklist (in `pipeline.md`) is
met, or when the user consciously overrides it — record the override in `film.json`
with a reason. Never override silently on their behalf.

**A stage is never finished by assertion.** Before you say a stage is done, or
name the next one, print its gate checklist from `pipeline.md` with a
✓ or ✗ per line and the evidence beside each ✓ — a status a tool returned, a
recorded waiver, a user's yes. If any line is ✗ the stage is not done, and the
sentence to write is which line and what closes it, not the next stage's name.
Skipping is allowed when the user says so; skipping *silently* is not, and
neither is a stage nobody mentioned: if the path from here to there passes a
stage, name it, even to say it is being skipped and why.

**Never call an asset locked, or the asset stage done, until each save
returned `locked: true`** — a save at `status: "review"` succeeds without
refusing anything, so a summary can upgrade `review` to `locked` without anyone
noticing. **A tool's own
answer outranks your recollection of it** — `picsart_save_asset` returns
`locked`, `picsart_list_assets` returns `byStatus`, and both exist so this
sentence can be checked instead of composed.

**The override unit is the requirement, not just the stage** — but be exact
about which side of the line a decision sits on, because getting this wrong in
either direction is a failure. The boundary: **choosing HOW to satisfy a rule is
your craft call (which model, which order); choosing to spend or
risk money against a closed gate is never yours.**

So: which model, whether a face needs a crop beside its sheet — craft, decided and recorded, never asked. The lock's evidence is
the approval itself: the save tool locks on `status: "locked"` with no
`stressTest` block, and there is no battery to ask about; a
question to the user about it inverts the
economics (a skip spends *less*, and permission is for spending more). What
genuinely IS the user's: **every charged video dispatch — the quote goes out and
the call waits for the yes, forecast or no forecast** — generating
charged video for a scene whose sheets are not approved, exceeding the quoted
plan, and any call that trades quality for money. And the scene check enforces it mechanically: a run dispatches only when
every tag its scenes name has a `locked` row — from the save's own result,
never from a summary.

There is no pipeline board. The project's state lives in the workspace files —
`film.json` and `docs/brief.md` (`workspace.md`) — and a second place to read it
would drift from them the moment anything moved. Render the map yourself when the
user asks where things stand: a stage list with ✓/✗ gates, then the
scene×assets matrix with its holes marked, both straight from `film.json`. It
is a markdown table, it costs nothing, and it cannot disagree with the state it
was read from.

**Name the stages in the map the way a person would, never by their internal
heading.** `pipeline.md`'s titles are filing labels — "Library → gate" tells a
user nothing, and "Bible lock" and "Breakdown" are barely better. Number them as
they are numbered, and title them by what actually happens:

| # | In the map | Not |
|---|---|---|
| 1 | The look, the story, the plan, the shot list | Director's breakdown |
| 2 | (part of 1 — references are optional inspiration) | Reference gathering |
| 3 | (part of 1 — the console's Lock is the look's lock) | Bible lock |
| 4 | Cast, places and props | Asset production |
| 5 | (part of 4 — the approval is the lock) | Library → gate |
| 6 | Shooting the shots | Generation |
| 7 | The cut | Edit |
| 8 | Fixes | Cleanup |
| 9 | Colour | Colour |
| 10 | Sound | Sound |
| 11 | Delivery | Master |

The status column follows the same rule: "waiting on the consistency checks",
not "blocked on locks"; "8 approved, none checked yet", not "8 approved, 0
locked". A stage nobody can name is a stage they cannot tell you is wrong.

Say where the film is at the start of a session — "you are here" — and again at
every milestone.

Three habits that keep the user oriented instead of lost:
- **The checklist is yours, the gate is theirs.** Every gate item is work *you*
  do and track in `film.json`; the user's only call is whether an open gate
  passes. Name what the next stage starts before asking them to open it, and on
  their yes, do exactly that.
- **A stage locator only when the stage actually changes** — one line, and only
  the locator: "📍 Stage 4 · Assets — locking @neferet (2 of 5 done)". With no
  pipeline board this line IS the map, and it stops the "wait, where are we?"
  message. On every other turn it is furniture. Never give it a subtitle
  explaining what the stage means or what the last one cost.
- **Write a board's `note` in plain language.** No pipeline jargon on first
  contact — "nothing renders until the bible is locked" means nothing to someone
  who just typed a logline; "first we plan on paper, then images, then video"
  does.

## Stage details, checklists, and mistakes

`pipeline.md` holds all 11 stage cards: goal, input, output, exit
checklist, and the documented common mistakes. Load it when opening a stage or
judging a gate. `presets-looks.md` holds the film-setup vocabulary
(genres, tones, the colour scheme and hue, the frame, the camera and the lens
family) — lighting, focal length, aperture, palettes, shot length, camera
movement and framing are deliberately not setup decisions, because none of them
can honestly be decided once per film; they are per-shot calls (the palette
table lives on there as the shot's colour). Grain is
not a control either: it is a property of the stock and rides in
the Camera preset's fragment. A **tone** is an era recipe: it sets the
camera and lens to a named period of cinema and adds one clause of its own,
while colour remains independent,
so when the story names a period or a cinema tradition, pass its id as
`suggested.selections.tone` and let the console expand it.
`widget-feedback.md` documents every film board's feedback payload.

## Cost ledger

| Free | Charged, no rollback |
|---|---|
| all planning, breakdown, prompts, presets, `picsart_model_catalog`, `picsart_model_params`, `picsart_preflight`, `picsart_media_validate_scene`, authoring and re-authoring the cut, **splitting a run at its cuts** (probe + bootstrap + validate; the scene editor plays the built scene, so it never exports), every board and console (`picsart_film_setup`, `picsart_shotlist_board`, `picsart_asset_review`, `picsart_scene_editor` — which renders nothing, `picsart_model_choice`), every `picsart_media_contact_sheet` and `picsart_media_export` (real GPU renders, so it costs time and leaves a file — **not credits**) | every `picsart_generate` (images and video) |
