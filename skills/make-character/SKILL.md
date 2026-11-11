---
name: make-character
description: Make one AI character with no film - a person or an animal drawn as one photoreal reference sheet, the canvas's strip (full-body front, side and back, and a large face close-up, in one row), its look picked from Picsart's ready-made characters, a person and an outfit, or the user's own words, approved, then saved to their Picsart Assets where Picsart's canvas finds it too. A character maker for an AI influencer, a mascot or a recurring face. Use when the user wants an AI character, a character sheet or a consistent face of their own, with no story around it. Not for a film's cast (movie-producer), nor for a single picture of someone (generate-media).
metadata:
  uses: film-cast-design
  title: Make a character
  short-description: Design one consistent character and save it to your Assets
  argument-hint: '[who they are, or a photo of them]'
  starter-prompt: Make me an AI character.
argument-hint: '[who they are, or a photo of them]'
---

# Make a character

Read picsart-video-rules first. One job: one character, with no film, as one approved sheet saved to
the user's Assets. A film's cast is movie-producer's; a single picture of someone is generate-media's.

Before acting on a stage, load the skills in its row that apply to this job, also when the work resumes there.

| Stage | Gate | Skills |
|---|---|---|
| 1. Who they are | — | film-cast-design |
| 2. Their look | ASK | film-cast-design |
| 3. The quote | SPEND | film-cast-design |
| 4. The sheet | REVIEW | film-cast-design |
| 5. Save it | DELIVER | film-cast-design |

## 1. Who they are

Draft the character's descriptor from the user's words, as film-cast-design's Descriptors says:
line-keyed, concrete, what you invented marked as a proposal. Give them a name and an @tag from it.
They have no voice line: this character is not cast to speak.

When the user brings a photo of the real person, the photo is the character, as film-cast-design's
`references/own-photos.md` says: skip stage 2, and keep the photo's own style.

## 2. Their look

ASK with `picsart_asset_choose_characters`, with no `film` and this one character: their @tag as `id`,
`name`, who they are as `role`, and the descriptor's lines as `story`. The card opens on the
ready-made characters, with the look you `suggested` picked, and keeps your lines on its story tab.
Then act on `character_chooser_feedback` as film-cast-design's The starting point says:
`story` keeps your draft. A `preset` with `saved` reuses that asset without compiling or spending; deliver the saved character and skip the quote and generation steps below.
For an unsaved `preset`, quote the sheet’s credit cost, compile with `sheetModel`, and save under
the preset’s own name so the next pick reuses it. An unsaved `preset` and `person` pass their `reference` on unchanged with only the
`fromStory` paths added from your draft, and `describe` rewrites the draft from their words.

## 3. The quote

1. Use picsart-video-rules's image default unless the user chose another model; check its inputs
   and supported ratios with `picsart_model_params`.
2. Compile the sheet with `picsart_film_compile_prompt`, `kind: "sheet"`, that model as `model`,
   and the descriptor in `reference`. The look is the Picsart canvas's style line:
   `look: { "customTone": "clean photoreal reference sheet — realistic materials, soft even light ~5500K" }`.
   With a photo, the photo's style is the style: add
   `"usePhoto": true, "customMedium": "the reference image's own medium, kept as it is"` to
   `reference`, and pass
   `look: { "customTone": "the exact art style of the reference image — its medium, rendering, linework, shading, palette and level of detail, with no realism added" }`.
   Put the supplied original photo URL in `verifyWith.request.imageUrls` and in the actual
   generation's `imageUrls`, including on replacements. `usePhoto` alone attaches no image.
   Never leave `look` out: a sheet with no style line is refused. Send the prompt and supported
   `aspectRatio` as returned, at the model's highest resolution. Send `negativePrompt` only
   when the model supports it.
3. `picsart_preflight` the call and quote it, then SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says).

## 4. The sheet

Generate it with `picsart_generate` and follow the job. Then REVIEW it in
`picsart_asset_approve`, and read the review as film-cast-design's Reading the review says: a
change is surgical, and a new picture is quoted on its own.

## 5. Save it

Cut the approved sheet into its four views, as film-cast-design's `references/views.md` says, and
look at each. Save with `picsart_asset_save`: `tag`, `assetType: "character"`, `name`,
`descriptor`, `sheetVersion: "v1"`, `voice: { "nonSpeaking": true }`, the whole sheet as
`portraitUrl`, the views as `referenceImages` (the close-up first), `status: "locked"`, and no
`projectFolderUid`. Also save `identityReferences` with the supplied originals (`[]` for an
entirely generated identity). It lands in their Assets under
`Assets/Library/Characters`, where Picsart's canvas finds it too. Read `locked`, never `saved`.

DELIVER the sheet's `downloadUrl` and say in one line where the character is kept. Offer one next
step in a sentence (a film with them, another outfit as a new version), and do it only on a yes.
