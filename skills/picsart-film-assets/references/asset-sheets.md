# Asset sheets — the one-image sheet, descriptor formats, and the record

A sheet is the set of reference images for one character, prop or location.
Each is compiled with `picsart_film_compile_asset_prompt`, generated with
`picsart_generate`, reviewed on `picsart_asset_review` and locked with
`picsart_save_asset`.

> **The prompt templates live in the compiler.** This file
> decides *what* a reference must be and *why* — the rules about the neutral
> grey ground, the medium line, the era the cast is written to, what the board
> judges, how a sheet is cut into views. That judgement is the part that needs a
> reader.
>
> It does not carry the templates themselves. Build one with
> `picsart_film_compile_asset_prompt`: pass the look ids — the tone, camera, lens,
> and the film's `scheme` / `hue` whenever the setup has one — and the descriptor
> fields, and it pastes the template, the rendering clauses and the house lines,
> and returns the `negativePrompt` and `aspectRatio` with them.
>
> Some fields in the long portrait shape are still yours to write — the colour
> tints, the light temperature, the grade. The handbook writes those with an
> "e.g." because the writer decides them, and the tool takes them verbatim. What
> it will not do is invent one: a field left empty is dropped from the prompt
> and named in `notes`.

Read `asset-efficiency.md` before prompt assembly, scheduling or changing an
upstream image. Its scoped asset prefix, per-item readiness and impact checks
govern style prefixes, scheduling and rebuild scope.

## The asset record — unified format

Every asset, whatever its type, is recorded in this shape (the
`film.json.assets[]` row):

| Field | Contents |
|---|---|
| TAG | short unique name: `@cal`, `@main_street`. How the asset is named in every card and prompt |
| TYPE | character / location / prop |
| SCENES | scene ids where the asset is used (from the breakdown) |
| GRID | the layout the sheet was generated to — *"T-cut triptych: left column two stacked face panels, right tall full-body panel"* (a states sheet: *"1 row, 3 equal cols"*) — declared in the sheet's prompt so the panel boxes are readable afterwards |
| PANELS | what each panel shows **and where it sits**, in reading order — *"1 front face (top-left) · 2 side face (bottom-left) · 3 full body front (right tall) · 4 full body back (far right, four-panel version only)"*; a states sheet: *"1 wet (leftmost) · 2 armed · 3 coat off (rightmost)"*. Position is not decoration: it is how a view is cut and what each crop is checked against (it never travels into a prompt — *A panel pointer is a dispatch error*, below) |
| VIEWS | **one file per panel the film actually needs**, cut from the approved sheet: `{ id, panel, position, box, url, bytes }`, `box` as `[x, y, w, h]` in the sheet's own pixels. These, not the sheet, are what a run's `imageUrls` carries (*How an asset reaches the run*, below). A variant tag resolves to a view: `@cal_wet → views[3]` |
| VISUAL LOCK | the final descriptor — the sheet's prompt and this record; **never pasted into a video prompt** (the pictures carry identity) |
| SOURCE | `generated` (the default) or `user` — the asset is a photograph the user supplied. A generated character is one one-shot sheet; a photographed one is three chained images: the photo as portrait, a profile generated from it, a T-cut sheet compiled from both (*The three generations*, below) |
| PORTRAIT (chained route) | the approved face portrait, one file. Its head-to-neck crop is the `identity` view (`views[]`, `box` read off its pixels). Upload 1 of the profile and of the sheet. Saved as `portraitUrl`; the sheet is `turnaroundUrl`, the same shape as a photo-sourced asset |
| PROFILE (chained route) | the side view generated from the portrait, one file, saved as `profile`; its head-to-neck crop is the `profile` view. Upload 2 of the sheet |
| ORIGINAL (user only) | the upload saved **byte-for-byte** (probe-matched); IMAGE 1 in every run; never edited, never replaced |
| SHEET | the sheet's URL (one file). The generation and approval artifact, and the archive the views are cut from — **not** what a run carries. Optional for a user-sourced asset: generated from the photo only when the cards need an angle or state the photo lacks |
| DERIVED (user only) | copies of the original with what was done — `{ url, op }` — made only for a format the model refuses (HEIC → JPEG), the run's byte ceiling, the model's size floor, a proven background leak, or **a composite the user supplied cut into its views** (`op: "crop — panel 4 of 4, rightmost"`), or **an era-adapted portrait the user chose** (`op: "era adaptation — 80s American Drama"`) — the one derived file that then stands as IMAGE 1 in the photograph's place (*The user's photograph*, below) |
| VERSION / STATUS | v1, v2… / draft → review → locked |
| NOTES | specifics; anything not in the script marked `design proposal`; amended lines with what they replaced and why |
| BEHAVIOR (characters) | gait, resting posture, hand habits, tempo — carried in the shot blocks' action words so the same person *moves* the same |
| VOICE (anyone who speaks) — **frozen once saved** | Save a canonical text description in the character's `voice` field: accent, register, timbre and habitual cadence. Choose it from the character and story without an extra approval step, respecting any user-specified voice. **From the moment it is saved it never changes** — every speaking prompt reproduces it **byte for byte** (`../../picsart-film-scenes/references/prompt-blocks.md`), and scene emotion, shouting volume and momentary speaking speed are kept out of it, in the delivery clause. Rewriting it is a **version bump that re-opens every shot that character has already spoken in**, never a quiet in-place edit. A supported `voiceId` may be stored additionally; it does not replace the text for native-video prompts. Holding the text rigid reduces drift; it is not an exact voice lock — the discipline is absolute precisely because the mechanism is not, so the one variable we control is removed from the experiment. |

**The side view is an angle and a framing, not five words.** The handbook's
bare profile prompt — *Create a side view of the person.* — is satisfied
honestly by a three-quarter view. The profile is an INPUT to the T-cut sheet,
whose side panel wants a true lateral, so a three-quarter makes the sheet model
extrapolate the angle and the identity stops travelling.
`picsart_film_compile_asset_prompt kind=profile` writes the rotation, the
far-eye occlusion and the head's framing, each one a clause a profile fails
without.

For a character missing `voice`, use an accepted performance as the basis
when it can be heard, then save the description once before the next generation.
Do not claim that description was present in earlier prompts. Do not create a
separate TTS or cloning workflow merely to fill this text field.

Naming that survives a long project: `portrait_<name>_v<N>.jpg`,
`profile_<name>_v<N>.jpg`, `sheet_<name>_v<N>.jpg`, and
`view_<name>_<panel>_v<N>.jpg` for each view cut from them. A new version is a
**new file** — never rename or overwrite; old prompts point at the old names.

## The character — one-shot sheet, or the photograph chain

**The one-shot sheet is the default for a generated character.**
`picsart_film_compile_asset_prompt` with `kind: "sheet"`, the outfit by item, and
the face in words — `faceAndOutfit` (the long shape's clause) and/or the six
`identity` fields — pass the locked camera and palette/scheme as well as the
tone, and **nothing uploaded**: the compiler puts the face in a
`THE PERSON —` block above the T-cut layout, and one render returns front
face, side face and full body. Square, at 4K (a panel is a third of the
image; only 4K clears the 1024 px identity floor), no `imageUrls`. On Nano
Banana 2 it holds the same person in all three panels, old or young, with face
panels near 2,000 px. Its typical miss is the chained route's too — an old face
drawn a decade young — so the age goes in
as a number in `identity` as well as in the words. The three chained images
below are the route for a **photograph**: the user's picture stands in the
portrait's place, and profile and sheet are built from it.

For a supplied photograph, the chain uses **three chained images, each made from the one
before it** (the handbook's method): a **portrait** —
the supplied face, preserved; a **profile** generated from the portrait (*"Create a
side view of the person."*); and a **sheet** compiled from both plus an outfit
reference — the handbook's T-cut triptych. Chaining is what makes them the same
person: every later image sees the approved face, where three separate
text-to-image draws would be three near-misses.

**The handbook has two versions of the chain, and the console's Tone picks
which.** The **vintage path** is for its six era tones —
`italian60`, `american80`, `summer80`, `hongkong80`, `neonhk90`, `american90`.
The **modern path** is the handbook's Digital / IMAX method: for *Modern
Digital / IMAX* (`imax`), and for Tone Auto, which names no era (the handbook
has no Auto; the era-less path is the one that fits). The two differ in the
portrait prompt's shape, the model per step, the ratios and the compile
prompt; everything below names the path, never "set tone".

**None of the three is what the video model reads.** They are generated,
approved, archived — and the run carries **single-view files**: the portrait's
head-to-neck crop as the identity view, the profile's as the profile view, the
sheet's full-body panel as the wardrobe view (*How an asset reaches the run*,
below). A multi-panel image in `imageUrls` asks the model to pick a face out of
three, and it picks wrong. So the sheet keeps the handbook's layout for the
handbook's reasons, and is cut for ours.

What the three must be:

- **The sheet is the handbook's T-cut triptych, at 1:1**: top-left the front
  face close-up, bottom-left the side face close-up, the right tall panel the
  full body standing, front view, in the outfit. **The back view only when a
  card shoots from behind or the costume has back details** — then the
  handbook's four-panel version at 4:3, the full-body back view beside the
  front at the same scale and height. **States** (`wet`, `armed`, `coat off`)
  are not on this sheet: a second sheet, generated from the portrait and the
  approved sheet, one full-body panel per state, no more than four in a row,
  on the declared-grid rules below — only when the script has states.
- **The sheet prompt is the handbook's for the path, verbatim, with two
  substitutions said here once**: *white* → *neutral grey* wherever the
  handbook names the backdrop (the ground rule below); and on the vintage path
  the handbook's *Technicolor* → **the film's stock word** — the Camera
  preset's stock when it names one (`italian60` Technicolor, `american80`
  Kodak 5294, `neonhk90` Fuji 500T, `american90` Kodak 5298), else the tone
  clause's own (`summer80` Kodachrome), else the handbook's word stands
  (`hongkong80` Technicolor). Each opens with the two film lines (*Every image
  prompt carries the film*, below) and closes with `EXACT 1 CHARACTER` and the
  descriptor.

  **Vintage path, 1:1:**

  *(The template — sheet, vintage path, 1:1 — is built by `picsart_film_compile_asset_prompt`. Pass the ids and the fields only you can write; it pastes the rest. Never retype it here.)*

  **Vintage path, four panels with the back view, 4:3:**

  *(The template — sheet, vintage path, four panels, 4:3 — is built by `picsart_film_compile_asset_prompt`. Pass the ids and the fields only you can write; it pastes the rest. Never retype it here.)*

  **Modern path, 1:1** (the handbook writes it for an outfit image; the
  descriptor's items stand in when there is none):

  *(The template — sheet, modern path, 1:1 — is built by `picsart_film_compile_asset_prompt`. Pass the ids and the fields only you can write; it pastes the rest. Never retype it here.)*

  **Modern path, with the back view, 4:3** (the handbook's text, its "Compile
  3 images" included):

  *(The template — sheet, modern path, four panels, 4:3 — is built by `picsart_film_compile_asset_prompt`. Pass the ids and the fields only you can write; it pastes the rest. Never retype it here.)*

  On the photograph chain, the three uploads are the approved portrait, the approved profile and the
  outfit reference — a clothing photo on a clean white ground with no one
  wearing it, or a worn outfit with the head cropped out of a **copy** (the
  handbook's rule for the outfit image).
- **The panel boxes are read off the pixels, never assumed from the grid.** The
  grid makes the reading easy and the crops clean; it does not make the model
  obey arithmetic. When the sheet lands, probe it for `width`/`height`, look at
  it (`picsart_view_image`, free — for you, not shown to the user), and write
  each needed panel's `box` into `views[]` as `[x, y, w, h]` in the sheet's own
  pixels, generous by a few pixels inward so a neighbour cannot bleed in. A
  grid the model drifted by 20 px is still perfectly croppable; you just have
  to look.
- **On the photograph chain, the portrait carries the identity, the profile the profile, the sheet the
  wardrobe.** Each later image is generated with the earlier ones uploaded and
  is checked against them before it goes anywhere — the handbook's Part B
  check: *the same face, same hair, same film grain and colour treatment; if
  the tone fidelity drops between the two images the sheet will look
  inconsistent*. A profile or sheet whose face drifts from the portrait is a
  re-dispatch, not a tile.
- **Neutral grey studio background, mandatory.** A location behind a reference
  leaks into every scene that reference touches.
- **`EXACT 1 CHARACTER — the same person in every panel`**, in the sheet's
  prompt, with the descriptor pasted whole. Two people on a sheet is a failed
  generation; re-dispatch, never bring it to the board.
- **Resolution follows the handbook's model for the step, and the floor is
  measured, not enforced.** On the modern path every step runs on
  the Nano Banana family (`film.json.model.pictures.modern`, the newest
  `gemini-*-flash-image` at the time — `../../picsart-film/references/pipeline.md`,
  *Image models are families*) at the top of its `resolution` enum (read it
  live; `4K` is the top today) — a 4K portrait, profile or 1:1 sheet clears the 1024 px
  short-side floor for every view cut from it. On the vintage path the portrait
  and the sheet run on the GPT Image family (`pictures.vintage`), which has **no resolution control** (only
  `quality` and `aspectRatio`): its output size is whatever comes back, so the
  views are **probed and their size recorded**, and one under the floor is
  **reported, not repaired** — there is **no upscale step** on this path. The
  floor itself stands: the video model renders at 1080p, and a full-frame face
  at native pixels is 1024 px on its short side. Quote the batch with
  `picsart_preflight` as always; a 4K image costs more than a 1K one and is the
  cheapest quality in this pipeline, spent once and read by every cut.
- **The resolution is passed explicitly, at the top of the enum, and never
  trimmed to save credits.** `gemini-3.1-flash-image` offers
  `0.5K · 1K · 2K · 4K` and **defaults to `1K`** — so a sheet comes back small
  either by leaving the parameter off or by choosing the bottom of the enum, and
  both are wrong. Preflight both ends of the enum if the cost is ever the
  question: the gap between the smallest and the largest sheet is a fraction of
  one video run, and the sheet is paid once and read by every cut, while an
  undersized sheet buys panels the provider refuses outright and a re-roll of
  the whole run. A 512×512 sheet cuts into 252 px views that stop a run
  mid-film. Log the resolution beside the sheet's
  prompt, because it is the first number to read when a face comes back soft.
- **Format: JPEG, quality ≥ 85, never PNG** — for the sheet and for every view
  cut from it. A few lossless PNGs overflow a run's 15 MB reference budget;
  a 2K JPEG is 1–2 MB where the same pixels as PNG are 8–10 MB.
- **Aspect ratios are the handbook's, with one named deviation.** On the vintage
  path the handbook makes the portrait and the profile at **16:9** — *film and
  television are 16:9, the models were trained on it, and at 16:9 the portrait
  crops are more accurate and grain and colour more convincing* (handbook).
  **Ours: 3:2**, the nearest landscape ratio to 16:9. If a provider rejects an
  aspect ratio that preflight accepted, use another aspect the model supports
  (the nearest landscape one, then 1:1) and say so, because preflight checks
  the listed values, not what the provider will render. The
  identity and profile views are the head-to-neck crops, boxes read off the
  pixels like any view. On the modern path they are **3:4**. The sheet is
  **1:1**, the four-panel back version **4:3**.
  Character images seed no frame, so the film's ratio binds none of them.
- **Believable beats beautiful.** Skin texture, asymmetry, tired eyes, a live
  catchlight. A too-perfect face is *less* repeatable — "generically
  beautiful" is a basin every seed falls into differently.
- **`negativePrompt` is a legitimate identity guardrail for IMAGE-model work**,
  where the model's schema declares it: the identity ban — the ways a face
  drifts between panels, from features and eye colour to hair length, facial
  structure and skin tone. `picsart_film_compile_asset_prompt` returns it in
  `negativePrompt`. Never as prose, never in video blocks.

**Descriptor** covers, in order: sex, age, ethnicity, build; face (shape, eyes,
hair, facial hair); costume **by item** with materials and condition; shoes;
accessories; posture and movement. Never write the age as a number — carry it
through role, build and condition (language laws in
`../../picsart-film-scenes/references/prompt-blocks.md`). Keep the base panels to what
the character carries in *most* scenes: anything visible on a reference
*happens* in the shots — a sword on the belt gets drawn, a cigarette gets
smoked — so scene-specific gear is its own panel, named by its tag.

**The cast is written to the tone's era.** When the console's Tone
is not Auto, the descriptor's hair, grooming, make-up, wardrobe and screen
archetype belong to that era — the sheet inherits grain and colour through the
style prefix, but a 2024 haircut inside an 80s tone is a render fighting itself
(the handbook's rule, and the one place *era* reaches a person). When the story's
period disagrees with the tone's era, say it **once** — *"the tone is 80s and
the story is now: dress the cast to 1985, or set Tone to Auto?"* — and let the
user decide. Never restyle silently, and never touch a real person's photograph
for it (the offer is in *The user's photograph*, below).

**Point changes are masks, never a second full pass.** A collar, a scar, a
buckle on an otherwise right sheet is an inpaint of that panel (an image
**edit** model — `picsart_model_catalog`, `mode: "image"`, `purpose: "edit"`,
the newest that takes a mask); a full re-render re-rolls the 95% that was right.

### Every image prompt carries the film

**And every one of them is verified before it dispatches**
(`../../picsart-film-scenes/references/prompt-verify.md`): a sheet, a
portrait, a profile and a plate each have a row in its governing-files table,
and the step is the same one a video run passes through — open those files,
derive what they require, check the literal tool arguments, write the verdict.
A picture costs less than a take; it is still a charged call that fails for the
same reason, which is a rule that was known and not checked.

A portrait, a sheet, a scene picture, a plate — each is a still *of this
film*, and its prompt says so before it says anything else. A prompt that does
not say which film it is for can return a cartoon sheet on a live-action drama.

- **Use the prefix appropriate to the image's job.** Scene pictures retain
  `bible.stylePrefix` verbatim. Neutral portraits, profiles, sheets and prop
  plates use `bible.assetStylePrefix` as defined in `asset-efficiency.md`:
  the locked rendering style without narrative staging, locations or film framing.
  Do not paste a scenic prefix and then ask the model to ignore it.
- **Then one medium line, read from the film.** For the films this pipeline
  makes: one sentence naming the picture as a frame of live-action film, with
  real people, fabric and light, and ruling out illustration, animation and
  rendering. A film set up as animated says its own medium here instead — the
  line is whatever the film is, never a fixed string, which is why the compiler
  reads it off the film rather than pasting a constant.
- **`negativePrompt` bans the other medium** wherever the image model's schema
  declares one — the medium ban, beside the identity ban above. Both come back
  from the compiler in `negativePrompt`; neither is written by hand.
- **A result in the wrong medium is a re-dispatch, not a tile.** Like two
  people on a sheet or a figure across a gutter: inspect it yourself, note what
  drifted in the row's grid notes, diagnose the cause and correct only that item
  within authorized spend. Follow `asset-efficiency.md`'s bounded retry rule;
  other ready chains continue.

Only then the task-specific body: face fields for a portrait, the view request
for a profile, or grid and wardrobe for a sheet; `EXACT 1 CHARACTER` and neutral
grey for character references. Full biography and movement notes stay in the
asset record, not a profile transformation prompt.

### The three generations — portrait, profile, sheet

Use this chain for a supplied photograph.
The default generated character is the one-shot sheet above.

1. **Portrait source.** Preserve the supplied photograph as the identity
   authority. An expressly requested era adaptation or approved fallback
   portrait is a separate, quoted generation with its own approval.

2. **Profile**, from the approved portrait: Nano Banana on both
   paths, the portrait uploaded, the handbook's five words after the two film
   lines — the compiled side view — 3:2 on the vintage path, 3:4
   on the modern. Check it against the portrait yourself (the Part B check above)
   and apply the bounded repair rule in `asset-efficiency.md` on failure;
   it reaches the board beside the sheet.
3. **Sheet**, from the approved portrait, the checked profile and the outfit
   reference: the GPT Image family on the vintage path (*it most reliably carries the
   film grain, analog texture and the specific colour grade through the
   compilation* — handbook), Nano Banana on the modern; the sheet
   prompt for the path, above, 1:1 (4:3 with the back). Profile and sheet share one board; a
   note on either triggers a content-impact check of the sheet. A changed face
   invalidates a conflicting face panel; a crop-only correction need not remake
   the sheet or unrelated views (`asset-efficiency.md`).
4. **Lock and cut.** `portraitUrl` = the portrait, `turnaroundUrl` = the
   sheet, the profile a view file like the others: `views[]` gets the
   portrait's head-to-neck crop as `identity`, the profile's as `profile`, the
   sheet's right panel as `wardrobe` (and `back` from the four-panel version),
   each `box` read off its own image's pixels and delivered at the 2048 px cap.
   the references header in the run: *"IMAGE 1 — IDENTITY: the approved portrait of @cal.
   Match this face exactly."*

Files: `portrait_<name>_v<N>.jpg`, `profile_<name>_v<N>.jpg`,
`sheet_<name>_v<N>.jpg` (`sheet_<name>_back_v<N>.jpg`,
`sheet_<name>_states_v<N>.jpg`), then `view_<name>_<panel>_v<N>.jpg` for every
cut — the handbook labels by character name and tone; the tone is the film's, so
the film folder carries it.

### The portrait prompt — the handbook's two shapes, filled from the film

The handbook writes a portrait two ways and the console's **Tone** picks which,
exactly as the handbook's two paths do. On the **vintage path** (the six era
tones) the prompt is short: the tone block, six identity fields, one framing
line. On the **modern path** (`imax`, and Auto) it is the long bracketed spec
covering the photographic dimensions. These are templates, not a requirement
to preserve contradictory or redundant clauses: use `asset-efficiency.md`'s
task-scope check, keeping the required identity, framing and rendering details. What
changes is where the values come from: the handbook types them; here the film
already decided most of them on the setup console, and the descriptor holds the
person. **A console pill on Auto leaves the handbook's value in place**, and a
dimension the console never sets (ISO, shutter, focal length, aperture) keeps the handbook's value
always. The values changed on purpose are these, all for rules of this file,
listed so the doc claims no more than it does: the **grey studio ground**
replaces the handbook's city street at golden hour — every background,
environment, location, time, weather, atmosphere and light field of the modern
template is filled for a studio (a location behind a reference leaks into
every scene), and *street* is dropped from *Cinematic street portrait
photography* for the same reason; the **focal length keeps the handbook's
85 mm** — the setup has no focal length, and a shot's wide lens is
a choice for rooms that on a face is a distortion no cut wants to inherit; and
`EXACT 1 CHARACTER` closes both shapes. Both prompts open with the two lines
from *Every image prompt carries the film*; `bible.stylePrefix` is the tone
block for scene work. For these neutral reference prompts use
`bible.assetStylePrefix` — the compatible visual clauses only.

**Shape 1 — the vintage path (the six era tones), 3:2** (the handbook's 16:9 is
refused by the provider — *Aspect ratios*, above)**.** The handbook's prompt,
verbatim in structure; the six fields are read off the descriptor. `[Age]` takes
the number here — an image-model field the handbook defined — while the
descriptor itself keeps carrying age in words for the run:

*(The template — portrait, vintage path (Shape 1), 3:2 — is built by `picsart_film_compile_asset_prompt`. Pass the ids and the fields only you can write; it pastes the rest. Never retype it here.)*

**Shape 2 — the modern path (`imax`, and Auto), 3:4.** The handbook's template;
angle-bracketed values are read from the film, scoped to the neutral reference
task. Remove redundant clauses when needed under `asset-efficiency.md`:

*(The template — portrait, modern path (Shape 2), 3:4 — is built by `picsart_film_compile_asset_prompt`. Pass the ids and the fields only you can write; it pastes the rest. Never retype it here.)*

`negativePrompt`, where the schema has one: the medium words and the identity
words from above. **The sheet prompt reuses its portrait's lighting, palette,
grading and texture lines after the grid**, so the angles are lit and graded
like the face they are generated from; a scene picture reuses the palette,
grading, texture and HEX values under its own light.

**The own-reference prompt — the handbook's, for a photograph.** When the
identity is a user's photo, the handbook's variant of Shape 1 opens every image
built on it — the era-adapted portrait when the user chose one, the profile and
the sheet otherwise (*The user's photograph*, below); the step's own line
(the compiled side view, then the sheet prompt) follows it:

*(The template — portrait from the user’s own photograph — is built by `picsart_film_compile_asset_prompt`. Pass the ids and the fields only you can write; it pastes the rest. Never retype it here.)*

### What the board judges

The tile's `judge` line stays **one short question** — the one that matters
for that tile (`asset-review-widget.md`, *Judge by:*).
The checklists below, from the handbook, are what *you* check before an asset
is locked or used and what a returned note is measured against; pick the tile's judge
line from them:

- **A portrait**: a photograph, not a render; skin with pores and
  imperfections, matte; natural depth and shadow across the face; hair as
  strands, not a mass; iris detail and a live catchlight; neutral grey, nothing
  else in frame.
- **A profile**: the same person as the portrait — same face, same hair, same
  grain and colour treatment; the full head from chin to top; lighting
  consistent with the portrait.
- **A sheet**: the same person in every panel — face, build, ignore the pose;
  the outfit matches the descriptor or the wardrobe reference; grey ground in
  every panel; the face lighting of the portrait preserved,
  not flattened or restyled; face panels cropped tight with no remnant of a
  different outfit; nothing crossing a gutter.
- **An angle sheet from a photograph**: the same person as the photo — face,
  build. Ignore the pose.
- **An era-adapted portrait**: still recognisably the person in the photograph;
  only hair, make-up, wardrobe, grooming and posture changed.

## The location — the descriptor here, the pictures at the scene

**A location is not generated at this stage.** The handbook makes the
location *after* the scene — *the model is trained on films with actors in
them; an empty location renders unreal, so generate the scene first and take
the location from it* — and that is the order: the scene picture with the
characters in it, the wide from it, the room map from the wide
(`../../picsart-film-scenes/references/step-3-scene-pictures.md`, step 3). The handbook's prompts for all three
are there.

What this stage still owns for a place:

- **The descriptor**, written at step 1 with the cast's: architecture,
  materials and textures, key objects, light, condition (new / decayed),
  atmosphere, the palette line — and **one anchor object** (the crooked palm,
  the copper kettle) named in it. It fills the *Setting* line of the scene
  picture's prompt and the references header of every run; frames without an anchor are
  "somewhere", and somewhere drifts. **One-light logic** — one motivated source
  per time of day — and **colour baked in** — `bible.palette`, written from
  the film's scheme and hue, verbatim — live in the descriptor. With scheme
  Auto, name the place's own colours and what carries them. Every scene
  inherits its tone from its place and Stage 9 refines instead of inventing.
- **The record.** `film.json.assets[]` keeps the location's row (tag, type,
  descriptor, scenes); its `views[]` are filled at `picsart-film-scenes` step 3
  when the pictures lock: `map` (one per place and time of day — the handbook's
  1:1 top-down sheet with sides A/B/C/D, read once and its sides written into
  the scene's location map) and `wide` (the film's ratio). The scene pictures
  belong to their scenes (`scenes[].pictures`), not to the place. Saved through `picsart_save_asset` like any asset: `portraitUrl` = the
  map, `referenceImages` = the map and the wide.
- **A real place** the user photographed: the photographs are the identity, as
  for a person (*The user's photograph*, below) — saved byte-for-byte, `SPACE`
  in every run there; the scene picture is generated with them attached, and
  the map is made from the best wide photograph with the handbook's map prompt,
  which works on any photo.

## Plates and props

A **plate** (2-shot locations, props) is one image, judged on the same board.

**Props: two panels, and no people in either.** The left
panel is the object alone on neutral ground; the right is the same object beside
a scale anchor, so its size can be read off something known. Both panels are
square to the camera. No hand holds the object: a plate carries no people, and
a hand is the most expensive thing to ask a model for. The anchor is an
everyday object: a coin, a matchbox, a hand-span
marked on a rule. `picsart_film_compile_asset_prompt kind=plate` takes the
descriptor (shape, material, size, condition, distinguishing details) and the
anchor, and writes both panels.

**The right panel is discarded at lock.** It exists so the board can judge
scale; what the film carries forward is the left panel alone, cut out of the
sheet the same way a portrait's views are. The cutter must know a plate has two
panels and that panel 2 is not an asset.

**The scale-anchor law** applies to every asset: sizes are stated relative to a
known object, never in bare numbers — "a jar the size of two fists", "a doorway
a head taller than @cal". The lead is the film's ruler.

## Crowds — one asset, exact counts

A crowd is designed once, as **one plate** with its own tag (`@market_crowd`):
a collective descriptor (who these people are, dress code, age spread, what
they carry), a palette that sits *behind* the leads', and the crowd texture in
the image. In prompts it is placed with an **exact count** ("EXACTLY 6
background figures") and a behaviour line — an uncounted crowd multiplies,
clones faces and steals focus. Named extras that act are promoted to sheets.

## The user's photograph as the asset

When the user supplies a photo of the real person, product or place, the
photo is the asset (`workflow.md`, *When the user brings the asset*). The rules
that differ from a generated sheet:

- **Byte-identical save, proven.** `picsart_media_probe_media` the upload URL,
  `picsart_drive action=upload` it into the project folder under its own
  name (read `durability` in the result), probe the Drive URL: `bytes`,
  `width`, `height`, `contentType` equal, or it was not a copy. Nothing else
  touches the file on the way in. The registry row is written once, at lock
  time: `portraitUrl` = the original, `turnaroundUrl` = the angle sheet when
  one was approved.
- **The descriptor is written from the pixels and stays short.** The photo is
  authoritative; words that disagree with it fight it in every cut. Tag, role,
  behaviour, and costume only where a scene departs from what the photo
  shows.
- **A composite the user supplied is cut before it is used.**
  People hand over one image with four pictures in it — life stages, outfit
  options, a contact sheet off their phone. The original is still saved
  byte-for-byte and is still the row's `original`; what changes is that **it
  never enters `imageUrls` whole**. Read the panels off the pixels, crop each
  view the film needs from a **copy** (*The crop*, below), and record them in
  `derived[]` with the position in the `op` — `"crop — panel 4 of 4,
  rightmost"` — and in `views[]` like any other view. The identity view of a
  composite is IMAGE 1, and the references header says where it came from: *"IMAGE 1 —
  IDENTITY: a photograph of the real @alina, the adult-in-formalwear view, cut
  from the four-panel reference she supplied. Match this face exactly."* The
  rest of the byte-for-byte doctrine is untouched, since
  the file that gets cut is a copy and the original in the library never
  changes.
- **No model holds a face at 100%.** The only 100% face is the photograph,
  which is why it rides as IMAGE 1 in every run and a generated sheet, when
  there is one, is labelled *face from IMAGE 1*. There is no face-similarity
  endpoint on this surface; the check is the user's eye on the review board,
  `judge`: *"the same person as the photo?"*
- **Angles from a photograph are the handbook's steps, and only when the cards
  need them — after asking for photos first.** Count what the user
  gave against what the cards need: every angle in hand, nothing is generated.
  One or two views and the cards want a profile, a full length or the back —
  ask for those photos first, and offer the generation as the alternative with
  its price; a phone photo settles for free what a generation only
  approximates. Before any of it, the handbook's four standards for the photo:
  *the face clearly visible and well lit; sharp and in focus; facing forward or
  close to it; high resolution* — a photo that fails one is still saved as the
  asset, and the user is asked for a better one in the same breath. When
  generation is chosen it is the chain above with the photograph in the
  portrait's place: the **profile** from the photo (the compiled side view, the
  own-reference lines in front), then the **sheet** compiled from
  photo, profile and outfit with the sheet prompt, the models per the film's
  tone. Each opens with the own-reference prompt (*The portrait prompt*), goes
  on the board (*What the board judges*), and in the run rides **second**,
  labelled *face from IMAGE 1*. No model holds a face at 100%; the board is the
  check.
- **An era-adapted portrait is offered, never applied.** When the
  console's Tone is one of the six era tones and the photograph's styling is plainly of today
  (decide by looking), offer **once**: keep the photograph as the identity
  (the default), or an era-adapted portrait — image-to-image from the photo,
  the handbook's adaptation prompt on our terms: *keep the facial identity and
  core proportions; change the hairstyle, make-up, wardrobe, accessories,
  grooming, posture and screen archetype completely to the era; a neutral film
  still, head to neck in frame, on neutral grey*, with the style prefix on top.
  Name the trade-off in the offer: **the identity is then a generated image,
  not the photograph.** If chosen, it goes on the board (*What the board
  judges*), and once approved it is a `derived[]` file with its `op`, it is the
  identity view and IMAGE 1, and the references header says so: *"IMAGE 1 — IDENTITY: an
  era-adapted portrait of the real @cal — hair and wardrobe restyled to the
  1980s, face from her photograph. Match this face exactly."* Any angle sheet
  is then generated from the adapted portrait, not the photo. The original
  stays saved byte-for-byte and never changes; declining leaves everything as
  it was.
- **Two slots, not one.** A photo-sourced lead with a sheet is two images in
  `imageUrls` — the photo (or its identity view, when the photo is a
  composite) and one view cut from the angle sheet; two such leads and a
  location view are already five or six. Skip the sheet whenever the photo
  shows what every cut needs.

## How an asset reaches the run — views, not sheets

**One image, one thing.** Every image in a run's `imageUrls` shows exactly one
view of exactly one asset — @cal's face, @cal in his coat, @garage_day at
night — and the references header names it in one clause because there is nothing in the
picture to disambiguate. The sheet stays in the library as the approved
archive; **the views are what travels.**

**Why a sheet never travels.** Hand the model one image carrying four panels
of the same woman — as a child, a teenager, a director, and in formalwear — and
let the references header name the panel the run needs, *"the
adult-formalwear panel"*, correctly. The model still has four faces in one
picture and nothing telling it where the named one sits, so it guesses, and the
wrong face comes back.

**It does not fail the same way twice, and that is what makes it lethal.** The
prompt is not wrong and does not change, so a diff shows nothing. Every
generation is an independent draw against the same ambiguous picture: two runs
from the *identical* prompt return two visibly different women, and a frame can
blend into a face matching **no** panel at all — a face that is not in the
cast. Within a single run a face usually holds; it is **across calls** that it
moves, which is exactly where nobody is looking. Panel labels rendered into the
pixels — *"PANEL 2: LATER YEARS"* — are not reliably obeyed either:
**baked-in labels are not a fix, and neither is wording.** The only fix is that the image handed to the model
contains one face.

**Two adult states of one character is the highest-risk pair, and worth a
warning when you see it.** The director panel and the formalwear panel are
alike enough to blend and different enough to look wrong. Say so while the
sheet is being designed, put them as far apart on the grid as the layout
allows, give them the clearest wardrobe and hair separation the story permits,
and never let both reach a run as anything but two distinct view files, each
assigned to its cuts by number.

### Cutting the views — after approval, and only what the cards name

Crops are `picsart_media_export` calls and **an export costs no credits**,
so nothing here is rationed by money — cut every panel the film
uses. They still happen **at lock, never on the way to the board** (the user
sees the monitor, each ready preview and its review), for a different reason: a
sheet the user sends back changes its panels, so a crop taken before the
approval is a crop of the wrong picture. What gets cut:

- **The identity view — every character, always.** For a one-shot sheet,
  crop its approved front-face panel head to neck. For a supplied photograph,
  use that original's head-to-neck crop. This view stays in every relevant run.
- **The profile view** — crop the one-shot sheet's side-face panel, or the
  checked separate profile on the photograph chain, when a shot needs it.
- **The wardrobe view — the sheet's full-body panel** in what the character
  wears in most scenes (the back panel too, from the four-panel version, when a
  card shoots from behind). Cut it; whether it *ships* is the budget ladder's
  call below.
- **One view per panel a shot card names by tag** — `@cal_wet`, `@maya_coat_off`,
  `@alina_child`. A tag with no view is a tag whose run has no pixels for it;
  this is the same arithmetic as the scene×assets check in `workflow.md`, one
  level finer.
- **A location: its map and its wide**, made at `picsart-film-scenes` step 3 from the
  first scene played there (*The location*, above); the scene pictures belong
  to the scenes.

For a one-shot sheet, its front and side face panels supply the identity and
profile views; the full-body panel supplies wardrobe. Save the front-face crop
as `portraitUrl` and the sheet as `turnaroundUrl`. For the photograph chain,
use the original portrait and separate profile as their view sources. Panels
nothing references remain uncut. A film that later needs
one cuts it then — the sheet is archived, the box is arithmetic, and the crop is
one call.

### Before the first cut — probe the sheet and do the arithmetic

**One probe, before any panel is cut.** `picsart_media_probe_media` the approved
sheet and read its real width and height, because the crop recipe needs the
native size anyway (`bounds`, and the asset's `width`/`height`). Then, from the
grid, the panel's short side is `min(sheet_w / cols, sheet_h / rows)` — and it
is compared with two numbers before a single export goes out:

| Panel short side | What it means | What to do |
| --- | --- | --- |
| ≥ 1024 px | a legal identity view | cut normally, `k` caps it down to 2048 |
| 320–1023 px | over the provider's floor, under our own | cut, and say the sheet was undersized: views ship but a face is soft |
| < 320 px | the provider refuses it | the clamp scales up to 320 to unblock the run, and **the sheet is regenerated at the model's maximum** |

**A 512×512 sheet cannot produce a legal view, and this is the arithmetic that
says so before the credits are spent.** Four columns of a 512 px sheet are 128
px each; even the whole 512 is half of the 1024 px identity floor. The rule is
*the model's MAXIMUM resolution*, and *the panel count follows from the view
floor* (`workflow.md`, the sheet step). **The probe is the moment that rule gets
enforced**, before any panel reaches a paid run, and it costs nothing.

### The crop — the recipe

**Cut at full pixels, ship capped.** A view is cropped out of the sheet's own
pixels and then scaled down to a **delivery cap of 2048 px on the long side**,
in one export. Both halves matter: the sheet is generated at the model's
maximum so the crop has pixels to spare, and the *delivered* image is bounded
because the video model renders at 1080p — anything past ~2K is size the model
never uses, and `seedance-2.5`'s schema declares no per-image pixel limit to
read, so the cap is ours to hold rather than something the API will tell us
about. Downsampling a 4K crop to 1536 px is *sharper* than cutting the same
view natively out of a 2K sheet: that is the whole reason for the big sheet.

A crop is a one-layer scene whose **composition is the delivered size**, with
the sheet placed at native pixels, offset so the panel's top-left corner lands
at the composition's origin, and scaled by the cap factor. Worked example (a
2400×640 source cut as a 1×4 grid): panel 4 of 4 comes back as exactly the
rightmost quarter, both at native `600×640` and, with `scale: [0.6, 0.6]` and a
composition scaled to match, at `360×384` — same region, resampled, one call.
The scale-**up** half of the clamp below behaves the same way.

```json
{ "version": "1.0",
  "composition": { "width": 600, "height": 640, "duration": 1, "fps": 30 },
  "layers": [{ "id": "panel",
    "content": { "kind": "media", "fit": "none", "bounds": [2400, 640],
      "asset": { "type": "image", "uri": "<the sheet>",
                 "width": 2400, "height": 640 } },
    "transform": { "anchor": [1800, 0], "position": [0, 0], "scale": [1, 1] } }] }
```

- `bounds` and the asset's `width`/`height` = the **sheet's native size**
  (probe it — never guess); `anchor` = the panel's `[x, y]` in sheet pixels;
  `position` = `[0, 0]`.
- **`k` = the cap factor, and it is clamped at both ends** =
  `max( min(1, 2048 / max(box_w, box_h)), 320 / min(box_w, box_h) )`. The inner
  `min` is the delivery cap; the outer `max` is the floor, and it can push `k`
  **above 1** — a narrow panel is scaled *up* until its short side clears the
  floor. Then `scale: [k, k]` and `composition` =
  `[round(box_w × k), round(box_h × k)]`. `anchor` is in the layer's
  **unscaled** pixels and the scale composes about it, so the box arithmetic
  never changes with `k`.
- **The floor is 320 px on BOTH sides, not on the height.** Seedance refuses a
  reference whose width *or* height is under 300 px, so a view ships at 320 or
  more on its short side — the 20 px is margin, not superstition, because the
  box arithmetic rounds. Example: a wardrobe view cut out of a 512×512 sheet
  at `{ x: 258, y: 2, width: 252, height: 508 }` is 508 px tall and clears a
  floor written as *"300 px tall"*, then is refused by the provider for its
  252 px width after the run is dispatched. Written as `min(box_w, box_h)`,
  that crop gets `k = 320 / 252 = 1.269841` and ships 320×645: a 252×508 box
  at `anchor: [1800, 0]`, `scale: [1.269841, 1.269841]` and a `320×645`
  composition come back exactly 320×645, `deterministic: true`. `scale` above 1 is a shape the crop
  path accepts; nothing clamps it back to the native box.
- **Landscape panels are where this bites.** A wide, shallow strip — a props
  row, a colour bar, a letterboxed still — has the height as its short side,
  and the same clamp catches it. Read `min`, never `height`.
- **Floors the cap must never cross**: the identity view stays **≥ 1024 px on
  its short side**, and no view ever ships under **320 px on its short side**.
  A panel whose capped short side would fall under 1024 px means the sheet was
  too small or the grid too dense; fix that upstream (*The character*),
  never by shipping a soft face.
- **When the two clamps fight, the box is wrong.** The floor clamp puts the long
  side at `320 × aspect`, so a panel narrower than about 1:6 is pushed past the
  2048 px delivery cap by the very scale that lifts it off the floor. No figure
  panel is that shape: a strip that long is a row of panels, a colour bar or a
  gutter caught in the box. Re-read the grid and re-cut — never ship a strip.
- **An upscale to reach the floor is a repair, not a recipe.** `k > 1` resamples
  pixels that were never there: it satisfies the provider and it does not make
  a soft face sharp. Whenever a panel needs it, the sheet was too small — say
  so, ship the clamped crop so the run is not blocked, and fix the sheet size
  before the next character.
- **`content.bounds` is mandatory here and validation will not tell you.**
  `picsart_media_validate_scene` returns `valid: true` without it, and the
  export then fails, asking for an explicit resolution box.
  Validation is not the gate on this path; the export is.
- `mediaType: "jpeg"`, `jpegQuality: 85`, `startTime: 0`, `fileName` set
  (`view_<tag>_<panel>_v<N>`). **Never pass `resolution`** — the cap belongs in
  the scene, as `scale` plus a matching composition, which keeps the crop and
  the resize in one export (charged in render time, not in credits). The export's `resolution` is a second,
  blunter downscale of whatever the scene already produced.
- **Record what shipped.** `views[].box` is the box in sheet pixels;
  `views[].delivered` is the capped `[w, h]` actually exported. When a face
  drifts in a run, those two numbers are the first thing to read.
- **Check every crop three times.** Probe it: `width`/`height` equal the box
  times `k`, or the offset or the scale was wrong. **Read the smaller of the two
  numbers and check it is ≥ 320** — a probe that measures correctly protects
  nothing until its width is compared with the floor. Then
  look at it (`picsart_view_image`, free, batched, not shown to the user):
  exactly one full view, nothing of the neighbouring panel, no gutter stripe. A
  wrong crop is a re-crop with a corrected box — never a re-generated sheet.
- Capped crops are **small** — a few hundred KB — so the byte ceiling stops
  being what binds a run. What binds is the image *count*.
- If the ladder ever downscales a view, that smaller file **becomes** the
  state's file — recorded in `views[]`, passed by every run after it. A view cut
  or shrunk for one run only would put two different files behind one state,
  which is the thing byte-identical input exists to prevent.

### A panel pointer is a dispatch error — there is no fallback form

No wording makes a multi-panel image safe, so there is no sanctioned fallback
and no exception. **A label that points into a reference image — *panel 4*,
*the rightmost panel*, *the bottom row of the sheet* — is a dispatch error, and
the fix is the crop, never a better sentence.** `picsart-film-scenes` runs this as a
lint at the same moment as its pre-dispatch probe, over the references header and the cut
headers' image references only: position words about the *frame being made* —
the location map, the blocking, where the camera sits — are staging, required,
and out of scope. A composite the user
supplied is cut before it is used; if the export path is genuinely down the run
**waits**, because a crop costs nothing and a wrong face costs the scene.

Position belongs to the `PANELS` record, `views[].position` and
`derived[].op`. Those describe the **crop box**: how a view
is cut and what it is checked against. They never travel into a prompt.

**One state, one box, one file — and every run passes that same URL.** A
state's view is cut once, from the approved sheet, at one box; identity holds
across calls because the input is byte-identical, not because a guess came out
the same way twice. Never re-cut a view per run, and never hand two runs two
different files for one state. The crop is deterministic, so a
re-cut after an expired URL — same sheet, same box — is the same pixels; log
which URL each run carried, so a drift can be traced to a file instead of to a
mood.

### The run's reference set, and the ladder when it binds

Per character: the identity view **and** the wardrobe view, both, always
(rule 7). Per location: the **map**, always (rule 10), plus the view for the time
of day this run visits, plus the **wide** whenever a cut opens the setting up
beyond a tight frame. Plus one approved still per cut that has one. **Probe
every URL before dispatch** (`picsart_media_probe_media`, free), read each
picture's short side against the 320 px floor, sum the bytes, and hold **under
15 MB**; the image count follows the scenes the run plays, up to the model's
declared limits — read them live off `picsart_model_params`, never from here
(`seedance-2.5`, for example, declares 30 images, 10 videos, 10 audio).

**The ladder below almost never fires, and reaching for it by habit is its own
bug.** A run with three characters and a place is about ten
pictures against a declared thirty, and views are capped JPEGs of a few hundred
KB each, so neither the count nor the 15 MB holds. Drop nothing unless a probe
says you are actually over. A location drifts when its map and wide are left
out of a run that no budget forced, and the ladder only makes that look
permissible. Over budget, in this order:

1. **Drop stills.** A composition still is the only wholly optional reference.
2. **Drop the wide — only if the map is still in the set and no cut in the run
   pulls back or reframes wider.** Where a cut does open the setting up, the
   wide is what anchors the skyline, the street and the far wall, and dropping
   it lets the location drift. The **map never goes.**
3. **Re-encode any PNG as JPEG** — same pixels, several times smaller
   (`picsart_media_export`, `mediaType: "jpeg"`, `jpegQuality: 85`).
4. **Downscale a view below its delivery cap** — a second reduction on top of
   the cap every view already carries, and a genuine last resort. Never take
   the identity view below **600 px on its short side** (against the 1024 px
   floor it shipped at); below that, identity is what you are throwing away.
   Prefer dropping an image to softening a face.

**What this ladder never drops.** No descriptor rides in the prompt, so the
wardrobe view is the costume's **only** carrier and rule 7 keeps it in every
call; the same reasoning keeps the map in (rule 10). A ladder that frees bytes
by removing the only anchor for a thing is not a saving, it is the next drift.
Splitting the face panel out is not a ladder step either: it already happened
at lock.

**Frames exported from a take** (`../../picsart-film-scenes/references/step-6-7-selects.md` step 6 — `START
FRAME` / `END FRAME` when requested, kept frames, references for an edit call)
count against the same budget and must be at the run's native size, never a
contact-sheet thumbnail: Seedance rejects a frame with **either side** under
300 px, and a small frame that gets through anchors a soft composition.

## No repeatability battery

Assets are not stress-tested before video, and not on request either. Identity
rides as pixels, so the first run is the check, and a face that drifts there is
one re-roll. The save tool locks on the review-board approval with no
`stressTest` block.

**When two faces blend in one frame** the repair is `workflow.md`, *After the
run*, *A two-shot that blends two faces*: fewer references, a medium two-shot,
the pictures' model. Never pass a composite of two solo renders as a frame
reference.
