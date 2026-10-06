# Assets — casting, location scouting, and the prop shop, on images

Before preparing image prompts or scheduling work, read
[asset-efficiency.md](asset-efficiency.md): task-scoped reference
styling, per-asset readiness and content-based dependency checks. These qualify
the scheduling and review rules below without weakening approvals.

**One sheet per generated character; review each ready asset.** Compile one
T-cut sheet with `picsart_film_compile_asset_prompt`, `kind: "sheet"`, a face
in `faceAndOutfit` and/or all six `identity` fields, and the outfit by item.
Generate it from the descriptor without uploaded pictures. The front face,
profile and full-body outfit share one image. Use a live-schema-confirmed 4K
image model and probe the result: the identity panel must clear 1024 px.

The portrait → profile → sheet chain remains the route for a supplied real
photograph. Preserve that photo and check dependent images against it.
Pass the film's locked camera and colour choices to the compiler alongside
`tone`: `tone: "auto"` alone supplies no rendering style. If the look is still
entirely Auto, resolve its camera on the setup console before compiling. A
compiler error is a request to fix the input or report the block, not a reason
to switch a generated character to the photograph chain.

Quote every ready independent asset together, then dispatch their approved
`picsart_generate` calls asynchronously in one batch. Show each finished
asset immediately and open `picsart_asset_review` for the ready subset;
unrelated renders and retries do not hold it. Approval plus a completed
visual check locks that asset. Scene work may start when that scene's own
cast and props are ready.

At lock, cut each sheet into one image per view. Videos receive the approved
full-resolution views, never the multi-panel sheet. The sheet remains the
archive. See `asset-sheets.md` for grids, descriptors and cropping.

**An asset is still a pair: text + image.** The descriptor is the sheet's prompt
and the asset's record, and it is never pasted into a video prompt
(`../../picsart-film-scenes/references/prompt-blocks.md`); its **views** travel in
`imageUrls`, numbered and labelled to its shots, and the pictures are the
consistency mechanism. Say the
stage to the user in one sentence the first time — *"one picture per character
and place; approve them and we shoot"* — never through the vocabulary of these
docs.

## Every person and prop gets its pictures

- **A character**: one generated T-cut sheet; for a supplied photograph, its profile and sheet
  (`asset-sheets.md`). **Locations are not generated here**: every place gets its descriptor at step 1 and its pictures —
  scene picture, wide, a room map when the scene needs one — from
  the scene in `picsart-film-scenes` step 3, the handbook's order
  (`asset-sheets.md`, *The location*).
- **A prop**: one plate, judged on the same board, and carried into every video
  the prop appears in as `IMAGE n — PROP: <name>` (rule 7) — a
  plate nobody attaches was paid for nothing, and words alone turn a round
  canteen into a flat flask.
- A background figure or an object nobody handles has no row; it is two or
  three descriptor lines inside the shot that shows it.

**State and scenario variants are panels on the sheet, and views in the run.**
`@cal_wet`, `@cal_armed` — each is a panel of a states
sheet, generated from the portrait and the approved sheet so it is the same
person, then **cut out as its own image** and numbered in the references header like any other reference (*"@cal_wet — IMAGE
3"*). The tag resolves to a file, not to a region of a picture: given a panel
pointer inside a multi-panel image, the model guesses which face to use. A variant gets its own
*sheet* only when it is a different picture for most of the film — a costume
change that lasts an act, an injury that rewrites the face — and that is a craft
call, not a rule. A place at night is not a state here at all: it is a scene of
its own with its own pictures (`picsart-film-scenes` step 3).

## When the user brings the asset — the photo is the identity

A photo of a real person, a real product, a real place is not a reference for
a sheet; it **is** the asset, and it beats any generated image at the one thing
this stage exists for. No generative model holds a face at 100% — the only
100% face is the photograph — so the flow keeps the photograph in the video
model's hands and generates *around* it, never instead of it.

1. **Save it exactly.** The upload URL is temporary; the durable copy goes to
   the project's Drive folder as the bytes the user sent — `picsart_drive
   action=upload` with the upload URL, the original name kept; read
   `durability` in the result. Probe both (`picsart_media_probe_media`, free):
   `bytes`, `width`, `height`, `contentType` must match, or the save is not a
   copy. No re-encode, no crop, no enhance, no cutout on the way in. That file
   is `assets[].original`, and it is the identity source of every run the
   asset is in. This happens the moment the photo arrives (Stage 1); the
   registry row is written at Stage 4, step 4, once the cards are known.
2. **Identity or inspiration — decide by looking, never by asking**
   (`picsart_view_image`). A person, product or place the film is about is
   identity: this section. A film still, an artwork, a mood photo is
   inspiration: a reference caption, and it never enters `imageUrls` — a still's
   actors would join the cast. One short question only when an image genuinely
   reads both ways.
   **Then a second question of the same picture: one view, or a composite?**
   People hand over one file with four pictures in it — life stages, outfit
   options, a phone contact sheet. A composite is still the asset and is still
   saved byte-for-byte, but it **never enters `imageUrls` whole**: read the
   panels off the pixels, cut each view the cards need from a *copy*, and
   record them in `derived[]` with the position in the `op` and in `views[]`
   like any other view (`asset-sheets.md`, *A composite the user
   supplied is cut before it is used*). A composite passed whole with its panel
   named in words renders the wrong face.
3. **Generate an angle sheet only when the cards need one — and ask for photos
   first.** Count what was given against what the cards need:
   every angle in hand, nothing is generated. One or two views and a card asks
   for an angle or a state the photo does not have — profile, back, soaked, a
   different coat — ask for those photos first, and offer the generation as
   the alternative, with its price. When it is generated, it is the handbook's chain **from the photo** — the
   profile (the compiler writes it), then the T-cut sheet from
   photo, profile and outfit — with the photograph in the portrait's place and
   the four photo standards checked first (`asset-sheets.md`, *The
   user's photograph*), in the same batch as the generated sheets. It goes on the review board like any sheet,
   `judge`: *"the same person as the photo — face, build. Ignore the pose."*
   It is the asset's `sheet`, never its `original`, and in the run it rides
   **second**, labelled *wardrobe and angles — face from IMAGE 1*. A photo
   that already shows what every cut needs gets no sheet at all: that is one
   fewer image against the run's budget.

   **When the console's Tone is one of the six era tones and the photo is plainly of today,
   offer an era-adapted portrait once — never apply it unasked.**
   Hair, make-up, wardrobe and grooming restyled to the era, the face kept;
   the trade-off said in the offer — the identity is then a generated image,
   not the photograph. Chosen, it is judged on the board and becomes IMAGE 1
   as a recorded derived file; declined, nothing changes
   (`asset-sheets.md`, *The user's photograph*).
4. **One save, locked, no board for the photo.** `picsart_save_asset` once per
   photo-sourced asset, at the same moment the generated sheets lock:
   `portraitUrl` = the original, `turnaroundUrl` = the approved angle sheet
   when one exists, `status: "locked"`, no `stressTest`; the `film.json` row
   carries `source: "user"`, `original`, and `sheet` when there is one. The user gave
   the picture; asking them to approve it is a stop with no decision in it —
   only the sheet, if any, was a question, and it was answered on the board.
   The descriptor is **minimal and written from the pixels**: tag, role,
   behaviour, and costume only where a scene departs from what the photo
   shows — a descriptor that misreads the hair fights the photo in every cut.
   Show the line once; no round. A sheet approved later is a **new version, a
   new save** (`sheetVersion` v2, same `portraitUrl`), never an overwrite.
5. **In the run the photograph goes first, as a photograph.** The references header:
   *"IMAGE 1 — IDENTITY: a photograph of the real @cal. Match this face
   exactly — face, hair, build."* Untouched when the original is a single
   view; when it is a composite, IMAGE 1 is the identity view cut from it and
   the line says so — *"the adult-in-formalwear view, cut from the four-panel
   reference she supplied"*. When the photo's background is not one of
   the film's places, the same line says so: *"the background of IMAGE 1 is
   not a location in this film"* — words first, that is how a kitchen behind a
   portrait stays out of the desert. A **derived copy** (`assets[].derived[]`,
   a new file with its `op` recorded) exists for four hard reasons and one
   repair, never as an intake step: **a composite cut into its views** (the
   only one that is routine, above); a format the model does not accept (a
   phone's HEIC — a JPEG copy, same pixels); the run's byte ceiling (JPEG
   re-encode, then downscale while the face stays ≥ 600 px); the model's size
   floor (a photo with either side under 300 px — `picsart_enhance` a copy); and a
   background that leaked into the first run despite the words (a
   neutral-grey cutout of a copy, `picsart_remove_bg`). The original in the
   library is never the file that changes.

The same shape for a **product** (the photo is the object; an angle sheet only
when the cards turn it) and a **real location** (the user's photographs are
`SPACE` in every run there; the scene picture is generated with them attached
and the room map is made from the best wide photograph —
`asset-sheets.md`, *The location*).

## The conveyor — four steps, one board, then go

1. **Draft every descriptor in one turn**, from the story, the reference
   captions and the setup console — all of the block's characters, locations
   and props. This is where the text portraits and location descriptions are
   written.
   Exhaustive and concrete: costume by item with materials and condition ("a
   worn dark-blue work jacket", never "a jacket"); anything invented beyond the
   script carries a `design proposal` note. **There is no separate approval
   round for the text**: the descriptor rides onto the review board as each
   tile's `prompt`, its key lines as `info`, and the user approves picture and
   words together. A note that comes back on a tile lands on one descriptor line
   and one panel. **If the user supplied an image, look at it first**
   with `picsart_view_image` (free) — a URL is a link, not pixels — and decide
   what it is: a photo of the thing itself is the asset (*When the user brings
   the asset*, above), and no sheet is drafted for it here; a reference
   informs the descriptor and stays a reference. **When the console's Tone is
   not Auto, write the cast to the tone's era** — hair, grooming, make-up,
   wardrobe, screen archetype: the sheet inherits grain and colour
   through the style prefix, but a 2024 haircut inside an 80s tone is a render
   fighting itself. When the story's period disagrees with the tone's era, say
   it **once** and let the user decide — dress the cast to the tone, or set
   Tone to Auto; never restyle silently, and never touch a real person's photo
   for it (the offer in *When the user brings the asset*, step 3).
2. **Generate every ready independent asset in one approved batch.** Compile
   one sheet per generated character and one plate per prop. Read the live
   image catalog once and record the model ids in `film.json.model.pictures`.
   For a one-shot sheet, choose a model whose schema supports 4K on either
   style path; preserve the locked era and medium in its compiled prompt.
   Use the maximum supported resolution and verify that every identity panel
   clears 1024 px on its short side. Split an overcrowded grid into another
   sheet only with the additional generation priced and approved. A supplied
   photograph uses the chain in `asset-sheets.md` instead.
   Preflight each concrete request with `picsart_preflight`, show the combined
   quote, and dispatch only the authorized calls via `picsart_generate` with
   `async: true`. A dependent call waits for the actual checked input URL.
   Put all returned handles on `picsart_render_monitor` and reconcile each
   with `picsart_job_status`; a timeout is not permission to generate again.

   **Every asset prompt opens with the task-scoped asset style prefix and one medium
   line for the film** (`asset-sheets.md`, *Every image prompt
   carries the film*) — a portrait, a sheet or a plate that comes back in
   another medium, a drawing on a live-action film, is a re-dispatch inside
   the batch, never a tile. **Every sheet prompt is the handbook's T-cut prompt for the path** (grey for white;
   on the vintage path the film's stock word for *Technicolor*), and a states sheet declares its grid — one
   figure per panel, nothing crossing a gutter, no captions — because a sheet
   that cannot be cut cleanly cannot reach a run. Keep the monitor current
   while the approved batch runs, and show ready previews as they land. If a call under-delivers (a panel missing, two people on the
   sheet, the wrong medium), diagnose and correct that asset within authorized
   spend; do not resend identical failing instructions or hold ready siblings
   (`asset-efficiency.md`).

   **Show each asset as soon as it lands; check it before use.** Use the
   lightweight preview from `picsart-film` rule 4, and inspect it with
   `picsart_view_image`. Check identity across panels, age, medium, one person
   per panel, clear gutters and absence of burnt-in captions. The preview may
   be shown before the check finishes; explain a defect under it and offer
   the bounded repair. Locking, cropping and using it wait for the check and
   user approval. Use full-size originals for crops and generation inputs.

3. **Review the ready subset immediately, one tile per asset, deduped**: `picsart_asset_review`
   with the ready sheets and plates (split past 12 tiles); pending assets wait for their own review, each tile's
   `tag`, `prompt` (the descriptor), `info` (type, scenes served), and a
   `judge` line that names the question — *"the same person in every panel:
   face, build, costume. Ignore the pose."* — one question per tile, chosen
   from the handbook's checklists for a portrait, a sheet, an angle sheet and
   an era-adapted portrait, which are what you check yourself before the asset
   is locked or used (`asset-sheets.md`, *What the board judges*). Pass `imageModels` from a live
   catalog read so a change can be re-tried on another model. Feedback per
   `../../picsart-film/references/widget-feedback.md`: `approved[]` and `changes[]`,
   `approved.length + changes.length === total`, nothing decided by silence.
   - **Every `approved` sheet is locked on the spot, silently** — see step 4.
   - **Every `changes` sheet is one surgical repair**: the note folded
     into its own prompt (one descriptor line, or one panel named), nothing else
     touched; a **fresh board with only the returned tiles**, `version` bumped,
     `previousUrl` set so "go back to the first one" is a click. Approved sheets
     never reappear. Loop until `changes` is empty. Up to three named `models`
     → one version per model as sibling tiles on that next board, the only
     sanctioned case of two tiles sharing a tag.
     Before rebuilding dependents, check which content actually changed under
     `asset-efficiency.md`; a version bump alone is not a cascade.
   - **A point fix is a mask, not a re-roll.** A collar, a scar, a wrong buckle
     on an otherwise right sheet goes to an image **edit** model (the newest on
     the catalog that takes a mask, `purpose: "edit"`) as an
     inpaint of that panel; a full re-render re-rolls the 95% that was right.
4. **The approval IS the lock — and the lock is where the sheet is cut.** Per
   approved asset, in one step: probe the sheet, read the panel boxes off it,
   crop the
   views the cards name (the identity view always; the wardrobe view; one per
   tagged panel) — **cut at
   the sheet's full pixels and scaled down to the 2048 px delivery cap in the
   same export**, because the video model renders at 1080p and declares no
   input pixel limit of its own — then probe and eyeball each crop, and save.
   **No view leaves this step under 320 px on its short side** — width counts as
   much as height, a narrow panel is scaled *up* until it clears the floor, and
   a panel that needs it means the sheet was too small (say so). Width is the
   side that gets missed: a 252×508 wardrobe view clears a height check and is
   refused by the provider mid-run. The recipe, the mandatory `content.bounds`
   and the three checks are in `asset-sheets.md`, *The crop* — and
   the sheet arithmetic that catches an undersized sheet before any of it is
   *Before the first cut*. An
   export costs render time, not credits, so cut every view the
   cards name — but cut them **here and not before the board**, because a sheet
   the user sends back changes its panels. One state is one box and one file,
   reused by every run that names it.

   One `picsart_save_asset` per approved asset, with `status: "locked"`,
   `projectFolderUid`, tag, type, name, descriptor lines and `sheetVersion`.
   For a one-shot character, `portraitUrl` is the cropped front-face identity
   view and `turnaroundUrl` is the approved sheet; crop the profile from its
   panel. For a supplied photograph, preserve that original as `portraitUrl`,
   with the derived sheet as `turnaroundUrl`. A prop uses its plate as
   `portraitUrl`; the location uses its map when saved at `picsart-film-scenes` step 3.
   **`referenceImages` =
   the view URLs** (that is the field the library keeps them in; `film.json`'s
   `views[]` carries the richer `{ panel, position, box, url, bytes }` map),
   `scenes`. No `stressTest`:
   the save tool locks on the approval alone, and there is no repeatability
   battery anywhere in this flow. Read `locked` in the result, never `saved`.
   Run independent save calls in parallel; report each ready cast subset in one line: *"These assets are locked; their scenes can begin."* — and route to `picsart-film-scenes`. Writing `film.json`
   (`assets[]`, `bible`, `gates`) is silent.

   **The film uses the URLs the save hands back, never the ones the export gave
   you.** `picsart_save_asset` saves `portraitUrl`,
   `turnaroundUrl`, `referenceImages[]` and the voice sample into the project
   folder, and the result's `manifest` carries what it settled on
   (`manifest.portrait.url`, `manifest.referenceImages`) — those are the URLs
   `film.json` records and a run's `imageUrls` carries.
   `picsart_list_assets` is the same truth later. When the result comes back
   with an expiring warning, say it in one plain line and keep the sheet's prompt, grid and panel boxes, because those are what
   lets a view be re-made. A `picsart_drive` upload of the same image adds
   nothing the save did not already do.

   **A URL that 404s later is a re-cut, not a re-generation.** The views come
   off the archived sheet at boxes `film.json` already holds; the crop is free
   and deterministic, so the file that comes back is the same pixels. Only a
   lost *sheet* is a re-generation, from its saved prompt — and that is
   charged, so it gets a quote and a yes like any other purchase.

   **Approving the sheets locks the descriptors** (the look itself was locked on
   the console at Stage 1). The style prefix was compiled
   from the setup console at Stage 1 and is what every sheet was generated
   under; the text portraits are the descriptors on the tiles. Nothing is
   re-approved in words — `bible.stylePrefix` was recorded verbatim at the
   console's Lock (`picsart-film-development`, Stage 1 step 2) and is read from there.

   **When a descriptor is amended to match what the model will render, record
   what it replaced and why** — *"cardigan — the uniform tunic would not
   reproduce on flux-2-pro across 4 attempts"* — in the descriptor's notes.
   Say it to the user; never rewrite a locked line silently to match an output.

## What the library holds, and the gate into Stage 6

- **Registry**: `film.json.assets[]` — tag, type, version, sheet URL,
  the grid, the panel map **with each panel's position**, `views[]` with each
  view's box and URL, scenes, status — updated on every lock and every new
  version. `picsart_save_asset` is the ONLY writer of the library
  `picsart_list_assets` reads (the views go in its `referenceImages`); a sheet
  or a view uploaded as a plain `picsart_drive` file is a picture nobody can
  find. Read the library, do not remember it: `byStatus` is the truth.
- **Views×tags check**: every tag a run's cards name resolves to **one view
  file**, not to a panel of a sheet. A tag with a panel but no view is a cut
  with no pixels for it, and the fix is one crop. Same arithmetic as the check
  below, one level finer, and run at the same moment.
- **Scene×assets check**: every tag a scene names has a
  `locked` row (a place's row locks with its pictures at `picsart-film-scenes` step 3), and every tag whose card uses a **panel** (`@cal_wet`, a
  profile) has a `sheet` — a photo-sourced row without one passes the first
  test and fails the second. This is arithmetic on `film.json`, run silently
  before the first run dispatches; a hole is a sheet nobody generated, and the
  fix is to generate it — not a board, not a conversation. **A run generates only when
  every scene it spans is covered**, and that is the one gate here.
- **Read the location column in script order** for state the story changed: a
  scene after the fire is a dependent run that carries **frames from the run
  that burnt it**, never the clean pictures (`picsart-film-scenes` step 6). The
  check cannot see it; only reading can.

## After the run — repairs

- **A face that drifts in the run** is a re-roll or an edit pass
  (`picsart-film-scenes` step 5), judged on the review board — one generation, not a
  battery. If it drifts twice on the same face, tighten the descriptor's face
  lines and re-roll; if the sheet itself is the problem (face panel too small,
  two panels disagreeing), regenerate the sheet and re-cut its views. **Check
  the view before blaming the model**: a crop with a neighbour's shoulder in it,
  or a run that went out carrying a whole sheet, explains a drifting face on its
  own, and costs one re-crop rather than a generation.
- **A two-shot that blends two faces**: fewer references — each person's
  identity and wardrobe view and nothing else — a medium two-shot rather than
  a wide; try the alternate pictures model from the live catalog (`../../picsart-film-scenes/references/step-3-scene-pictures.md`, step 3).
  Not a composite of two solo renders: a tight reference set makes one
  unnecessary.
- **There is no repeatability battery.** The run is the check. A user who wants to see a face hold before
  the run gets it the cheap way: one extra still on the review board beside the
  sheet, judged by eye.
- **Every speaking character gets a voice description.** Choose it from the
  character and story without an extra user question; save it in the character's
  `voice` field before their first speaking generation. Follow the VOICE row in
  `asset-sheets.md`. Native audio still uses this description in every
  speaking prompt; it does not require a voice picker, sample or cloning pass.

## Costs

| Free | Charged |
|---|---|
| descriptors, the review board, the registry and the scene check, preflight, reading panel boxes off a sheet (`picsart_view_image`, `picsart_media_probe_media`), saving and locking a user's own photo, and **cutting the views** — `picsart_media_export` costs render time and a Drive file, not credits, so views are never rationed; they are cut at lock only because a sheet must be approved before its boxes are final | one sheet or plate per generated character or prop (`picsart_generate`, image rates — quote the batch once; a place's pictures are charged at `picsart-film-scenes` step 3), an angle sheet from a user's photo when the cards need one, a profile and sheet derived from a supplied photograph, an era-adapted portrait when the user chose it, any change round |

## Traps

- Generating a passport, a battery and a matrix out of habit. One sheet, one
  approval; the run is the check.
- Boarding a picture nobody looked at because the viewer said "too large".
  Use the preview path in `picsart-film` rule 4 and look; a defect nobody saw
  travels into every shot built on that picture.
- A sheet with two people on it, a face panel too small to read, or figures
  spilling across the gutters. A weak face panel is a weak film, and a sheet
  that cannot be cut into clean views cannot reach a run at all.
- **Passing a multi-panel image to the video model at all** — a sheet, or a
  composite the user supplied — and trusting a worded pointer to pick the
  panel. With four faces in one picture and the right one named, the model
  renders a different wrong one on each call — and sometimes a blend of two
  panels, a face not in the cast. Cut it. There is no wording that fixes it
  and no fallback pointer; if the crop path is down, the run waits
  (`asset-sheets.md`, *A panel pointer is a dispatch error*).
- Two adult states of one character on one sheet, unflagged. It is the pair
  most likely to blend; separate them on the grid, keep them as two view
  files, and say so when the sheet is designed.
- A character sheet with a scenic background. Neutral grey is not aesthetic —
  a location behind a reference leaks into every shot that reference touches.
- Generating a location here, empty, from its descriptor. The handbook's order
  is scene first, place from it — an empty place renders unreal.
- Evaluative descriptor words ("beautiful", "stylish"). If a costume department
  could not buy it from the description, the model cannot hold it.
- Re-approving in words what the user already approved as a picture — a
  descriptor round, a bible round, a "gate passed" round.
- Descriptor edits that rewrite instead of touching one line.
- Re-encoding, enhancing or cutting out a user's photo on the way in — or
  generating a lookalike from a descriptor when the user gave the real face.
  The original is saved byte-for-byte and is what IMAGE 1 comes from; every
  changed copy is a new derived file with its reason recorded, and only for a
  composite cut into views, the byte ceiling, the size floor, or a leak the
  first run proved. **Cutting a composite is not an exception to this** — the
  original is untouched and the views are cut from a copy.
- Putting a user's own photo on the review board. They gave it; only a sheet
  generated from it is a question.
- Redrawing a state panel from scratch on a new sheet because i2i is down. A
  from-scratch `@seneb_swollen` is a different man than `@seneb`; hold it and
  retry when image-to-image is available again.
- Restyling a user's photograph to the tone's era without being asked, or
  dressing a generated cast in today's hair and wardrobe under a vintage tone
  without saying so. The era offer is made once and answered; the mismatch is
  said once and decided.
- An asset prompt without the film's medium and compatible visual styling. Use
  `bible.assetStylePrefix` for neutral references, not scene staging. The picture otherwise
  belongs to no film, and a cartoon on a live-action drama is what comes back
  — and it is a re-dispatch, never something the user is asked to regenerate.
- A back panel on every sheet by habit — face pixels spent on a shoulder; the
  four-panel sheet only when a card needs the back. Swapping a step's model for
  resolution's sake: the handbook's model for each step stands.
