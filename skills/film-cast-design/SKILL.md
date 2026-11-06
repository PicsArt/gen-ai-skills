---
name: film-cast-design
description: Make a film's people, props and places consistent on pictures - line-keyed descriptors, one sheet per person and one plate per prop compiled by the server, reading an asset review, cutting each panel into its own view, locking the approved asset, and the user's own photos kept as they came. Use when a film needs its cast, props or places designed, pictured, locked or repaired.
user-invocable: false
---

# Film cast

The model has no memory. What keeps a face the same across forty shots is a locked picture of it,
cut into single views, passed to every video that shows that person. Read these before the step:

| File | Read it before you… |
|---|---|
| `references/views.md` | cut a view out of a sheet, or check one |
| `references/own-photos.md` | use a photo the user brought of a person, a product or a place |

## What each asset gets

| Asset | Pictures | Compiled with |
|---|---|---|
| A person you generate | one sheet, the strip of Picsart's canvas: full-body front, side and back and a large face close-up in one row, in one generation | `picsart_film_compile_prompt`, `kind: "sheet"` |
| A person the user photographed | the photo itself; a profile and a sheet only for views the photo lacks | `kind: "profile"`, then `kind: "sheet"`, from the photo |
| A prop | one plate: the object alone on a neutral ground, and the object beside an everyday thing for scale; no people, no hands | `kind: "plate"` |
| A place | a descriptor now; its pictures come from its scene (film-shot-generation) | — |
| A crowd | one plate with the dress code, the age spread and what they carry; each shot states the exact count | `kind: "plate"` |

Every person and every prop the story handles gets its pictures; nothing is tiered. A figure in the
background, or an object nobody touches, gets no asset: the shot that shows it describes it.

A state (wet, bloodied, coat off) is **a panel on the person's sheet with its own tag**
(`@cal_wet`), generated from the approved sheet so it stays the same person. A change that lasts
most of the film may earn a sheet of its own; that is a craft call. A place at night, or after a
fire, is a scene with its own pictures, never a state.

## The starting point

Draft every descriptor first, as below. Then OFFER the cast board once: `picsart_film_choose_cast`
with the whole cast (at most 12 a board), each character's descriptor lines as `story`. Every card
opens on those lines, so a board sent untouched changes nothing. It is an offer, not a gate: it
spends nothing, and a reply that ignores it keeps every character as the story has them.

Its answer, `film_cast_chooser_feedback`, has one entry per @tag:

- **`story`** — keep your descriptor.
- **`preset`** or **`person`** — the answer carries the look as `reference`: pass it unchanged as
  that character's `reference` on `picsart_film_compile_prompt`. It holds who they are, how they
  look (an animal's species and coat, the face, the build) and what they wear and hold. Add from
  your descriptor only the paths `fromStory` names: `identity.<field>` for what the preset leaves
  open — no preset names an origin, and a Person pick names no hair — and `outfit` when nothing was
  picked to wear. A field you add replaces the preset's. Presets carry no voice: the voice line
  stays yours. The descriptor you save is that `reference` in your own line keys, plus the voice.
- **`describe`** — rewrite the descriptor from the user's words. Keep your voice line and every line
  the words leave unsaid.

A person the user photographed is not on the board: the photo is the asset. Then carry on: one plan,
every sheet together.

## Descriptors

Draft every descriptor in one turn, from the story, the cards and the references; mark what you
invented as a design proposal. They are **line-keyed** (`face`, `hair`, `jacket`, `shoes`, …), so a
change is one line, and they are **concrete**: no evaluative words.

- **A person:** sex, build, face shape, eyes, hair and facial hair; costume item by item with
  material and condition; shoes; accessories; posture, gait, hand habits, tempo. Age goes in the
  compiler's `identity` fields, never as a number in prose. The base costume is what most scenes
  show; scene gear is a state.
- **A place:** architecture, materials, key objects, condition, atmosphere, one motivated light per
  time of day, the look's colour, and **one memorable anchor object**. With a colour scheme, the
  look's colour is the film's palette line, verbatim; with the scheme on Auto, each place names its
  own colours.
- **A prop:** shape, material, condition, distinguishing details, and size relative to a known
  object, never a bare number.
- **A voice line for everyone who speaks**, before their first spoken shot: accent, register,
  timbre, habitual cadence. Chosen from the character and frozen once saved; film-shot-generation' Voice says
  how the prompts carry it.
- When the tone is an era, generated people are dressed and groomed to it. If the story's period
  and the tone's era disagree, flag it with both options and restyle nothing until it is settled.

The descriptor is the sheet's prompt and the asset's record. In a video the views carry identity
instead, as film-shot-generation says.

## Pictures

1. Choose the image model once per film with `picsart_model_catalog`, filtered by the film's frame
   (a model whose ratios lack it is out) and by image input when a photo feeds it. Record it; one
   film never changes image model midway.
2. Compile every picture with `picsart_film_compile_prompt` and its reference `kind`, passing the
   film's `look`, the same object the shots get, and the descriptor's lines in `reference`
   (`identity` or `faceAndOutfit`, `outfit`, a plate's `descriptor` and `anchor`, `assetPalette`).
   Keep `look.scheme` and `look.hue` in it: left off, the cast comes back in no colour while the
   shots compile to the film's hue. Pass the film's image model as `model`: a picture sent with
   reference images then gets a ratio that model takes with them. It returns the prompt, the
   `negativePrompt`, the `aspectRatio` and a `promptToken`. Send all of them as returned; never
   type or retype a template.
3. Compile with `verifyWith` (`request` with the `imageUrls` you will send, `film` with the saved
   assets and their views, `limits` from `picsart_model_params`) and read each result's `check`:
   `picsart_film_verify_prompt` already run on that prompt. A failure is fixed in the inputs and
   compiled again; a `skipped` reference budget or view check has not run. Never retype a compiled
   prompt into verify.
4. Sheets are generated at the model's highest resolution, so every panel has pixels to spare.
5. Every independent picture goes in the same batch. A failed one blocks only what depends on it.

## Reading the review

Every tile comes back approved, changed or discarded.

- **A change is surgical**: the named line or panel, nothing else. A point defect on an otherwise
  sound sheet is a masked edit with an image edit model, not a re-roll.
- **Approved** is locked: cut the views the cards need (`references/views.md`) from the approved
  full-resolution sheet, look at each, and save with `picsart_film_save_asset`: `tag`, `assetType`,
  `name`, `descriptor`, `sheetVersion` (`"v1"`; a new version is a new save, never an overwrite),
  `voice` (an object: `mode` `preset` or `design`, or `nonSpeaking: true`; `voiceId`, `model`,
  `description`, `language`, `accent`, `sampleUrl`), `portraitUrl` (the sheet, or the user's photo),
  the views as `referenceImages` (the close-up first, as `references/views.md` orders them), the `scenes` it serves, `projectFolderUid`, `status: "locked"`. The result's `locked`, not its
  `saved`, says it is done.
  A locked save lands in the project's "Library", anything else under its "Assets"; with no project
  folder it goes to the flat global "Film Assets" folder. Only a save registers an asset for
  `picsart_film_list_assets`. A draft or review save returns `locked: false` with a `remaining`
  list. `stressTest` is recorded only, never a lock condition: pass it when the user asked for a
  spot-check and it ran; a battery with failures blocks the lock until fixed or noted in `waived`.
- **Discarded** siblings are never used.

## Check the cast on the scene pictures

No separate still test is bought. A face locked on one good picture can drift on real shots, and
the scene pictures (film-shot-generation) are where the cast first appears in its rooms, light and
company: check every face you can read there against its locked views, as you would a take, and
**beside the people they share a frame with**, since someone who holds up alone often breaks in a
two-shot. A person who drifts has an under-written descriptor: tighten the lines the picture got
wrong, record them on the row, and they go into every later prompt. Say what you saw in the
pictures' review; a new sheet or picture is generated only when the user asks for the change,
quoted on its own.

## The gate into a run

Before any video, for every scene the run spans: every tag it names has a locked row
(`picsart_film_list_assets` with the project folder, read back), and every tag that needs a panel, a
state or a profile resolves to a single-view file. A photo-only row cannot answer a view it lacks.
Read the places in story order: after a fire, later scenes need frames from the run that burned the
room, not its clean pictures.

## Repairs after a run

- **A drifting face: check the view first.** A wrong crop, a neighbour's edge in the box, or a sheet
  sent whole explains most drift, and the fix is a re-cut, not a generation.
- **Repair from the locked views, never from the last take.** A take made from a take inherits its
  drift and adds its own.
- If the view is sound, the take is repaired (film-shot-generation). After the same face drifts twice, tighten
  its face lines and re-roll. A sheet whose face is too small is regenerated and re-cut.
- **Two faces blending in a two-shot:** only each person's identity and wardrobe views, a medium
  two-shot rather than a wide, and never a composite of two solo pictures.
- A descriptor changed after takes exist does not silently regenerate them. Name the takes it
  affects and flag them for review.
- When a source changes, check only what depends on it, by the job it did (identity, wardrobe,
  geometry, light) and record `reuse`, `recrop`, `repair` or `rebuild`. A version bump alone does
  not cascade.

## Efficiency

- A reference picture is scoped to its job: a neutral ground, no location, no scene light. The
  compiler's asset style line carries the look without the staging; never paste the scenic one on.
- Fix a contradiction in a prompt (a neutral ground and a location; a tight face and a full body)
  by changing the clause, never by stacking negatives.
- Record a failure's defect separately from its likely cause. Two failures of the same kind mean
  the input or the method changes; never send a third identical attempt.

## Traps

- A sheet or a user's composite sent whole to a video model, with the panel named in words. No
  pointer works: cut the panel.
- Cutting before approval, or from a preview instead of the full picture.
- Guessing the grid instead of reading the boxes from the pixels.
- A sheet on a scenic background; two people on one sheet; faces too small to cut.
- Saying an asset is locked because the save came back `saved`.
- Asking the user to approve their own photo, or retouching it in place.
