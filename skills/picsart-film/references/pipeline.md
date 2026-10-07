# The 11 stages — cards, gates, and documented mistakes

Distilled from the production pipeline this skill implements. Each stage: goal,
output, exit checklist (the gate), and the mistakes the pipeline's authors saw
teams actually make. Stages 1–5 are "pre-production in reverse" — instead of
casting and location scouting, you fix digital references. The tighter 1–5 close,
the cheaper and faster 6 is.

Production can run **block by block**: lock the assets of scene block 1, generate
block 1 while block 2's assets are being approved. A gate applies per block —
and since a generation is a *run* that may span scenes (Stage 6), a run cannot
start until every scene it covers is locked, so block-by-block work means
cutting runs at block boundaries.

## Stage 1 · Director's breakdown — `picsart-film-development`

**Goal:** idea → look console with frame and runtime pre-set, locked →
story and model choice together when supported → shot list board carrying
run assignments, lengths and joins. Its submission approves plan and shots.
A story change is answered with a rewritten paragraph before its board.
**Output:** the locked look, the story the user said yes to, the video plan,
the shot cards, the asset list (people, places, props).

> **The look console is step 2 — before a word of story is written.** Genre
> decides how the story is told, so it is locked first, pre-set from the idea;
> every shot sits under its style prefix, lens family and colour scheme.
> Focal length, aperture, light and any shot-specific palette are per-shot
> decisions, with that palette required to fit the film's scheme. Getting this
> backwards leaves a drama script under an action lock, and the story is rewritten.
>
> **Pass `suggested.selections.ratio` whenever the user has named a format** —
> vertical, portrait, phone, TikTok, Reels, Shorts, square, landscape, scope. The
> console opens on 16:9 and cannot infer it, so a user who said "vertical" and
> got landscape was handed the wrong answer, not a default. Say it however it came
> up: the id, the label and the plain word all resolve (`vert` / `9:16` /
> `vertical` / `tiktok`), so there is no vocabulary to look up first.

> **The video model is step 4 — after the story, before the video plan.** The
> plan is written against the model: its ceiling is what fills each video,
> its `imageUrls` max is the reference budget, and its video-edit sibling is
> the repair path. `picsart_model_choice`, two or three cards, one
> `recommended`.
>
> **The video plan is step 5, approved on the shot list board.** Save run
> lengths and joins in `film.json.runs[]`; send shot `run` and `join` fields
> plus the concise length summary in the board's `note`. One submission
> approves the run grouping and camera decisions together.

Gate checklist:
- The look locked on `picsart_film_setup` before the story was written;
  `bible.stylePrefix` stored verbatim.
- The story shown in chat in the viewer's words — ten lines, then every
  scene as what we see and hear — with the user's yes, written to the locked
  genre (`film.json.story`, `docs/story.md`); the thing the story is about is
  seen in the first scene; no camera words, no film vocabulary.
- The video plan shown on the shot list board with the user's approval:
  run lengths and a join sentence at every edge (`film.json.runs[]`).
- Video model chosen on `picsart_model_choice` and recorded — `film.json.model.id`,
  `shoot.ceilingSec`, `shoot.editModel` — before the shot list opened.
- Every shot a card with its action and line copied from the story, who is in
  frame by tag, seconds and camera; shots 3–8 s as a habit, a longer one with
  its reason on the card. The board changed camera and seconds, never the story.
- On a film longer than the ceiling: the story is written as a story, and the
  videos are its 30-second pieces; the edge between two videos is joined the
  handbook's way — the last shot ends mid-movement, the next video opens on a
  clearly different angle (`../../picsart-film-scenes/references/seams.md`). No scene change
  is required at an edge.
- Asset list complete: people, places, props, each with a tag; a durable
  change the story does to one of them is a row too.

Mistakes: the story written before the look is locked, then kept under a
genre it was not written for; a story the user never read, approved in one
word on a table of beats; a story note answered with a new board instead of a
rewritten paragraph; the story written in film words; the fight written soft to protect the render;
in-frame text (signs, screens) not moved to a separate task — models write
text poorly, it is never generated in-shot; using a 30s model ceiling as
permission to turn a whole scene into one 30s action, so the video contains
no coverage and the film plays as held tableaux.

## Stage 2 · Reference gathering — part of Stage 1

References are optional inspiration, never a stage with a gate: the look is
locked on the console at Stage 1 step 2, and a board of stills gathered
afterwards does not reopen it. When the user has images, look at each one,
caption it with *what exactly we take from it*, and carry the captions into
the descriptors at `picsart-film-assets` step 1. Counts and categories for the user who
wants a board are in `../../picsart-film-development/references/visual-bible.md`; **this
spends nothing** — a generated moodboard is never an automatic charge. The stage number stays
so the stage vocabulary is stable. What binds:

> **The user's own photo of the thing itself is not a reference — it is the
> asset.** A photo of the real person, product or place is saved
> byte-for-byte to Drive (probe-matched) as it arrives, registered locked at
> Stage 4 without a board, and passed to the video model untouched as IMAGE 1; an angle sheet is
> generated *from* it only when a shot card needs an angle or state the photo
> lacks (`picsart-film-assets`, *When the user brings the asset*). The one exception to
> "untouched" is a **composite** — one file carrying several pictures of the
> person: the original is still saved byte-for-byte, but IMAGE 1 is the identity
> view cut from a copy, because a multi-panel image makes the model guess.
> Film stills and
> mood images stay references and never enter `imageUrls`.

No gate. Mistakes: an uncaptioned reference (unreadable
in a week); a mood board put in front of the user as if it were a decision.

## Stage 3 · The visual bible — part of Stage 1

The bible is the console's output, and the console's Lock is its lock:
`bible.stylePrefix` is compiled by `picsart_film_setup` at Stage 1 step 2 and
stored verbatim, and there is no later lock and no prose put in front of the
user to approve. The text portraits and location descriptions are written at
`picsart-film-assets` step 1, when the sheets are about to be generated, and approved
with the sheets.

No gate. Mistake: tone not fixed in the location
descriptors → the film drifts.

## Stage 4 · Asset sheets — `picsart-film-assets`

**Goal:** one generated sheet per character; the chained portrait/profile/
sheet route for a supplied photograph; one plate per prop. Quote independent
assets together, review each ready subset immediately, and cut approved,
checked sheets into single-view references. Scene pictures use the wide-first
procedure in `picsart-film-scenes` step 3.
**Output:** every asset `locked` in the library, silently, and the film moving
to Stage 6 in the same turn.

**Image models are families, not ids.** At this stage's first call
read `picsart_model_catalog` (`mode: "image"`, `purpose: "generate"`) and take
the newest of each family the handbook names: **GPT Image** (OpenAI,
`gpt-image-*` — the vintage path's portrait and sheet, and the room map),
**Nano Banana** (Google, `gemini-*-flash-image`, never the `-lite` — the modern
path, and the profile on both paths), **Seedream Pro** (`seedream-*-pro` — an alternate when a wide fails identity;
use the 4K-capable family chosen in `picsart-film-scenes` step 3 for the default wide). Record the ids in
`film.json.model.pictures` (`vintage`, `modern`, `map`, `people`) and read them
from there for the rest of the film: the docs name the family so a newer
version is picked up the day it lands, the record names the version so one film
never changes model midway. Where a version ships in tiers (GPT Image 2.5 is
two ids, a premium tier and a fast tier), the premium tier is the one for
anything a face is cut from — portrait, sheet — and the fast tier for the map.
Read the family's limits live each time
(`picsart_model_params` — the `resolution` enum, `imageUrls` max, the aspect
list), never from a doc; a model id written in these docs is an example, not
the rule.

> **Identity travels as pixels.** One sheet per character, state panels on
> it, no repeatability battery: identity rides into every cut of the run as
> pixels, and the first run is the check. Sheets are reviewed on
> `picsart_asset_review`, and the save tool locks on that approval with no
> `stressTest` (`picsart-film-assets`, step 4).
>
> **The sheet is how identity is *generated*; a single-panel view is how it
> *travels*.** Sheets are generated to a
> declared grid, cut into views at lock, and a run's `imageUrls` carries views
> only — one image, one thing. A four-panel reference with the wanted panel
> correctly named in words still puts the wrong face in the shot — and the
> identical prompt can return a *different* wrong face, with one frame
> blending two panels into a face not in the cast. Each call is an independent
> draw, so the failure never shows in a prompt diff and never repeats the same
> way; labels baked into the sheet's pixels do not help. **A prompt that points
> at a panel is a dispatch error, not a fallback**
> (`../../picsart-film-assets/references/asset-sheets.md`, *How an asset reaches the run*).
> Cutting is free — `picsart_media_export` costs render time, not credits.

Gate checklist:
- Every character and prop approved on `picsart_asset_review` and saved
  `locked` in one call (read `locked` in the result, never `saved`).
- Characters: one approved T-cut sheet per generated character; the original
  photograph, checked profile and sheet for photo-sourced characters. Every
  panel shows the same person on neutral ground. State variants have declared
  positions; a back panel is included only when the shots need it. Save the
  one-shot front-face crop (or original photo) as `portraitUrl`, and the sheet
  as `turnaroundUrl`. Only single-view crops travel to video generation.

- Every view is probed and its size recorded; the floor is **1024 px on the
  short side** — met by construction on the modern path (`imax` or Auto: Nano
  Banana at 4K), and **reported, not repaired** on the vintage path's GPT
  Image steps.
- Every view is **cut at the sheet's full pixels and delivered capped at 2048 px
  on the long side**, in one export. The model renders 1080p and declares no
  input pixel limit, so an uncapped 4K crop is size it never uses and a failure
  waiting to happen.
- Views cut and checked: every tag the cards name resolves to one single-view
  file (identity view always; wardrobe view; one per tagged panel), each probed against its box and looked
  at. `film.json` carries `grid`, `panels` with positions, and `views[]`; the
  save carries the view URLs in `referenceImages`.
- One state, one box, one file: every run that names a state passes the **same
  view URL**, and the URLs recorded are the ones `picsart_save_asset` handed
  back (it re-hosts; an export URL expires). An expiring warning in the save's
  message is said out loud, with the sheet's prompt and boxes kept so a view
  can be re-cut.
- No image label points into its picture — *panel 4*, *the rightmost panel* —
  in the references header or in any cut header. That is a dispatch error and the fix is a
  crop, never a rewording. (Position words about the frame being made — the
  location map, the blocking, the camera — are staging, and required.)
- Descriptors recorded verbatim; any amended line carries what it replaced and why.
- User-supplied assets: the original saved unchanged (probe matches),
  `source: "user"`, one save at lock time with no board (`portraitUrl` = the
  original, `turnaroundUrl` = the angle sheet when one exists); the sheet only
  when a card needs an angle the photo lacks, generated from the photo and
  approved like any sheet; a card that uses a panel needs that panel's **view**
  to exist. A composite the user supplied is saved byte-for-byte and cut into
  views from a copy — it never travels whole. An era-adapted portrait exists
  only when the user chose it — offered once when a vintage tone meets a photo
  of today, a recorded derived file, and IMAGE 1 then says so.

Mistakes: re-encoding, enhancing or cutting out a user's photo on the way in —
the original is what IMAGE 1 comes from and every changed copy is a recorded
derived file (a composite the user supplied is the one routine crop, taken from
a copy); passing a multi-panel sheet or composite to the video model with the
wanted panel named in words — cut it into views; a sheet with two people, a
face too small to read, or figures crossing the gutters — that sheet cannot be
cut; a portrait or sheet in another medium than the film (a drawing on a
live-action drama) — the style prefix did not open its prompt, and it is a
re-dispatch, never a tile; a character sheet on a scenic background
— it leaks into every scene; evaluative words in a descriptor ("stylish");
re-approving in words what was approved as a picture.

## Stage 5 · Library — `picsart-film-assets` (runs with Stage 4)

**Goal:** every locked sheet findable; every scene's tags covered before its run
dispatches.
**Output:** the registry (`film.json.assets[]`, written by `picsart_save_asset`)
and a silent scene×assets check.

Gate checklist (silent — no board, no walkthrough):
- `picsart_list_assets` `byStatus` shows every tag `locked`.
- Every scene a run spans has a `locked` row for every tag it names; a hole is a
  sheet nobody generated — generate it.
- Location column read in script order for state the story changed.

Mistakes: a sheet saved as a plain Drive upload — invisible to the registry;
declaring the gate from memory instead of from `byStatus`.

## Stage 6 · Generation — `picsart-film-scenes`

> **The unit of generation is the run, not the shot.** A film generated shot
> by shot and cut together loses to the same shots generated as one multi-shot take with the shot cards
> written in as its cut list — on identity, light, voice, and the cuts
> themselves. So as much of the film as fits the model's ceiling — scenes
> included; a short under 30s is one generation — is bought as one run in
> reference mode (every view and plate the run uses in `imageUrls`, numbered,
> each shot block naming its images, its lens and aperture, any non-auto
> palette, and user-changed light — never a sheet or restated setup value), the
> model makes the cuts, and the delivered take is split back into shot-shaped
> clips at the cuts it actually made. Shots are still authored one at a time and
> the user still works the short cards on the board; what is lost is per-shot
> *re-rolling*, not per-shot editing. There are no narrative exceptions to
> packing: payoff, climax, close-up, emotional change and scene boundary do not
> justify another run. The partition must use the fewest runs that fit; if two
> adjacent proposed runs fit together at the live ceiling including handles,
> merge them before dispatch. There are no per-shot repair exceptions: a fix
> routes on what was selected and what the note means: a note
> about how a marked stretch plays → the model's **edit** sibling on that clip;
> a note asking for something the clip has not shown yet → its **extend**
> sibling; only "regenerate / redo", or a note about the whole run, → a fresh
> roll. Regenerating a clip the user wanted kept is the failure this rule
> prevents. `picsart-film-scenes` step 5 has the derivation table.

> **One run before the rest.** With the shot list approved and the sheets
> locked, buy a single run — the riskiest, with a line in it and the most cuts — before
> dispatching the rest. It proves the video path, the model's identity hold
> across its own cuts, that it makes the cuts it was told to, and lip-sync, for
> the price of one generation instead of the film; its recipe is what the batch
> reuses. This is the handbook's own step between the animatic and the draft
> pass ("Generation tests: choose model/method per shot; save recipes"), and it
> is NOT the pre-lock test shot the traps forbid.

> **Every charged dispatch is quoted, then confirmed.** Before any
> charged video call — the pilot run, the batch, a re-roll, an edit, an extend —
> a `picsart_preflight` number goes to the user in one line and the call waits
> for their yes. One quote per dispatch, not per shot. The forecast, the shot
> list's approval and the sheets' lock are none of them that yes, and express
> pace does not skip it. Runs going out with no figure in front of the user is
> the failure this rule prevents.

> Additions from production practice: the stage opens with the film's **budget
> forecast** (runs × ~2 takes × run length × rate + buffer + foreseeable edit
> passes + QC frames — the per-shot keep rate does not transfer and the per-run
> rate is unmeasured, so the forecast says so).

> **Every scene gets its pictures before its run.** Follow `picsart-film-scenes`
> step 3: generate a 4K wide with the opening cast's identity and wardrobe
> references; check it; crop the opening scene picture from it; generate the
> room map from the wide only when needed. Quote the required generations
> together when their concrete payloads are known, and review each ready
> scene's wide, crop and map together. Original-size approved views travel as
> `START FRAME` and `SPACE`; thumbnails are for looking only. An approved
> run's exported frame may supply `FRAME REFERENCE for cut N`. A changed
> source invalidates only descendants whose visual content it changed.

> **The edge between two videos is the handbook's join.** The
> last shot of a video ends in the middle of a movement; the next video's first
> shot picks it up from a clearly different angle and size — a detail or an
> extreme close-up by preference; both videos carry the same pictures, so all
> of them dispatch together. The edge falls where the 30-second ceiling falls,
> never dragged to a scene change. No frame is copied between videos except in
> the case below.

> **A run at a place an earlier run changed waits for that run's frames.** The script says where the story changes a place; the
> runs after it there are dependent, quoted with the earlier run in one batch
> and approved once, and dispatch on their own when the frames are in hand —
> pulled without a stop: one frame per angle the dependent run will see, chosen
> on a contact sheet, exported at native size, replacing that place's pictures
> (never attached beside them), named in the `notes` line when the earlier
> run's scene opens in the scene editor. Every other run dispatches together (`picsart-film-scenes` step 6).

**Goal:** produce every run: final shotlist → the scenes' pictures (each ready scene reviewed) → run grouping → one prompt per run
→ drafts → iterations → the delivered take split at its cuts → selected takes.
The "shooting period", run as a seven-step conveyor per scene, in this order,
because each step is more expensive than the last.
**Output:** selects for all the block's shots + the full generation log.

Gate checklist:
- Every run's take accepted and split at its delivered cuts (`cutTimesActual`);
  every shotlist shot has status `final` and is in selects.
- Every scene's pictures approved on its review board and carried in its run's
  `imageUrls` with their roles; a dependent run's pictures of a changed place
  are frames from the run that changed it.
- Every charged dispatch went out on a preflight number the user saw and a yes
  that followed it, recorded in `film.json`'s `credits`.
- The prompt saved, one per video; the take's link and the verdict logged
  (the models used per stage feed `DISCLOSURE.md` at Stage 11).
- On a film of several runs, the run edges reviewed before the general edit
  (the automatic rough cut is off — `picsart-film-edit`).

Mistakes: a run dispatched with no credit figure in front of the user, or on the
forecast instead of a quote for that call; a descriptor pasted into the prompt —
the pictures carry identity and the prompt names them by number
(`../../picsart-film-scenes/references/prompt-blocks.md`); no
geography line — characters swap places between shots; a run without its
scene's pictures, or a run at a changed place carrying the clean pictures
beside the frames; a scene generated shot by
shot out of habit — the weaker path; a delivered run split at its planned cut
times instead of the ones the model made; accepted takes not isolated from raw
takes — the editor assembles from the unapproved pile.

## Stage 7 · Edit — `picsart-film-edit`

> Additions: AI motion cuts short (a shot inside a run is generated at its cut
> length, 3–8s authored; a solo take is generated 10–15s and cut to 3–8s;
> uneven cut lengths; cut on motion); dialogue and ambience on separate audio
> layers; join QC verified on real frames at video edges — the angle clearly
> changed, the movement carries, the level step is hidden by the bed — while
> the model's own cuts inside a run are checked once
> and expected to hold; verification bounded to two fix rounds, then deliver
> with one honest line.

> **There is no automatic rough cut.** A run arrives already cut by
> the model and its edges are joined by the angle change, so nothing is derived: the take is
> split at its delivered cuts and the scene editor opens on it as delivered —
> every shot a clip bounded by the model's cut, untrimmed. Trims are the user's,
> made in the editor (`trimSource: "user"`), and nothing automatic ever moves
> one.

**Goal:** assemble the film and reach the cut the user calls final.
**Output:** the final cut — the cut that no longer changes.

Editing runs **in parallel with generation** and orders what is missing ("need a
cutaway to the hands") — a reshoot costs minutes. Assembly → one review → the final cut.
Generations run draggy: cut more aggressively than feels necessary,
and plan to trim the first and last half-seconds of every clip.

Gate — one review: the assembled film is watched
once with the user in `picsart_scene_editor`; what they point at is fixed — a
glitch by the model's edit sibling, a bad join by a re-roll of the take that
missed its ending, a hole by a new shot — and the cut is final when they say
so. The locked picture is the scene document `picsart_scene_editor` returned
with that verdict, recorded in `film.json`; `picsart_media_export` renders it
for the masters. After that: no new generations except a fix the user asks for.

Mistakes: editing started only after all generation finished — months lost,
coverage holes found late.

## Stage 8 · Cleanup — part of Stage 7

Glitches — hands, teeth, a melted face, drifting objects — are fixed inside
Stage 7's one review, by the model's **edit sibling** on the clip (the defect
named to the second, the same references, nothing else — `picsart-film-scenes` step 5)
or by a re-roll when the edit will not take. No separate defect list, no
separate full-size pass.

## Stage 9 · Color — `picsart-film-finishing`

> Addition: the post order is upscale (a video upscaler from the live catalog —
> none named here, the tools change) → grain/texture → grade — the anti-AI-look recipe.

**Goal:** unify shots, then grade. Every generation arrives with its own baked-in
grade, so unification comes first; the creative tone was already set in the
location assets, so the grade refines, never invents.

Gate: neighbouring shots of a scene match; the grade applied per the bible;
upscaling (if any) done **before** the grade so the final pixels are what gets
graded.

## Stage 10 · Sound — `picsart-film-finishing`

> Additions: dialogue is the model's native in-shot delivery (`voicePolicy` is
> always `native`); the music bed is offered once, after the cut is picked,
> instrumental, ducked under speech. Stage 11 adds `DISCLOSURE.md` (AI models
> per stage, from the log) as a required archive deliverable.

**Goal:** the full soundtrack. Dialogue is **not re-recorded** — the voice is
cleaned from the generation (the model delivered lip-synced lines in-shot; between
clips its timbre and loudness drift, and that drift is what gets levelled).
Ambience is the glue of a scene: a continuous bed stitches shots that differ
slightly in picture into one space. Music from generation is unlicensed — flag it.

Gate: lines clean and even, actions sounded, ambiences continuous, rights
documented, loudness to the target platform's norm.

## Stage 11 · Master — `picsart-film-finishing`

**Goal:** deliverables, QC, archive.

Gate checklist:
- Frame-by-frame QC with fresh eyes: artifacts, joins (dropped/black frames,
  desync), digital errors (banding, over-compression), titles (spelling, rights,
  AI-use disclaimers where required).
- Masters exported per platform and verified by playback.
- Archive assembled and duplicated: all final prompts + generation log, asset
  library + registry, breakdown/shotlists/bible, edit records, all selects at max
  quality. The archive is the means of production — a sequel regenerates from it.
