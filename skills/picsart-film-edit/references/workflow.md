# Edit — takes → one review → the final cut

The editor's material is **selects only** — never the raw generation pile. And AI
editing has one structural difference from set footage: a reshoot costs minutes,
so **the edit runs in parallel with generation and actively orders shots**: "need
a cutaway to the hands", "need a wider size between 12B and 12C". Route those
orders back to `picsart-film-scenes` as new shot cards after checking the existing
coverage. For a bad join, first read **Join repair** below: a repair is not
automatically a model call. A new connecting insert can preserve both accepted
clips; it does not require re-rolling their run. Say what will change, what stays
untouched and the cost before any charged order (`picsart-film-scenes` step 5).

## Join repair — diagnose the pair before choosing the operation

When the user wants two existing clips to connect better, read
[join-repair.md](join-repair.md). Inspect both sides with sound and
actual boundary frames, explain the observed failure, and recommend the smallest
repair that addresses it. Missing story information needs a motivated beat, not
a cosmetic transition. Keep the accepted cut unchanged while comparing candidates.

## A run arrives already cut

**The model made every internal cut**, and a video edge is joined by the
handbook's angle change (`../../picsart-film-scenes/references/seams.md`), so no
trim is derived before anyone watches — not from the line's word timings, not
from the beat clock, and no seam pass moves the points at a boundary. When a run
lands (`picsart-film-scenes` step 6), the take is split at its delivered cuts
(`cutTimesActual`, compositor bookkeeping), and the scene editor opens on the run
**as delivered** — every shot a clip with the model's cut as its bounds, no trims
applied, nothing shaved. The user trims where they want to, and only then does a
shot get a `trim`, always with `trimSource: "user"`.

Three consequences, said once:

- **No "I made a first rough cut" line, no alignment wait.** The editor opens the
  moment the split is written. There is no automatic window to explain or to
  reverse.
- **The run's end handles play until the user trims them.** With `handles` on,
  the run's two ends carry unscreened seconds by design; nothing trims them
  automatically, so they are visible in the editor and a drag away from gone.
  `picsart-film-scenes` keeps the per-film switch; this is the consequence to
  know when setting it.
- **`trimSource` has one value, `user`.**

**Transcription earns its keep — for "the line reads", not for trims.**
`picsart_media_transcribe` on the take is diffed against the scripted line to
catch lip-sync saying the wrong words and to verify the one-second silence tail.
It does not place an in-point.

**User trims stay reversible, and that is a constraint on how the editor is
opened.** Author each shot as a track clip on the run's url with
`content.trim` in run-file seconds bounded by the `cutTimesActual` either
side of it — never a trimmed export — and open the editor on that scene. The
editor trims windows over the source, so widening a trim back is one handle
drag: free, instant, no round trip. Export a
trimmed clip and show that instead, and the trimmed second stops existing. Past
a delivered cut is the next shot's picture, not trim room; past `genSec` there
is nothing, and that is a retake, not a trim.

Their edits come back as `scene_editor_feedback.document` — the scene as they
left it, each piece a clip with its `content.trim` over its source, in play
order — and land straight on each shot's `trim` with `trimSource: "user"`. A `user` trim is never touched by anything automatic; a
re-rolled run re-opens untrimmed, because its cuts are new.

## What generated footage cuts like

- **It runs draggy.** Entries into action are slow. Cut more aggressively than
  feels necessary.
- **Held AI motion reads uncanny.** Viewers notice something is synthetic when
  a generated shot is HELD: dramatic beats sustain 4–7s at most, action cuts
  live at 1–2s, and mathematically even cut lengths read as machine editing —
  vary them on the emotional beat. A solo take was generated long (10–15s) as
  coverage and **the cut uses 3–8 seconds of it**; a shot inside a run was
  generated at its `sec`, so the 3–8 seconds were authored and the cut uses
  roughly all of it. On a solo take, trim into it: the best in-point is rarely
  the first stable frame.
- **The edges drift.** The first and last half-second of a *generation* are the
  least stable. Plan to trim both; that is what the shot's `trim` field is for.
  Inside a run the edges are the run's, not each shot's — the model's own cuts
  are clean and are not shaved.
- **Cut on motion, match motion.** Prefer cutting while something moves, and
  match motion direction across the seam — two static compositions butted
  together is the "AI slideshow"; a movement handed across the cut is cinema.
- **Every video edge is a suspect; an internal cut is the model's.** Shots
  inside a video were born in one generation — check its cuts once, on the real
  frames, and expect them to hold. A video edge was born in two and joined the
  handbook's way (`../../picsart-film-scenes/references/seams.md`), so the QC there asks
  three things: the angle and size clearly changed, the movement carries
  across, and the level step is hidden by the bed. Then the classical list —
  eye-lines match, the axis is not jumped, costume/props/hair continuous, tempo
  does not lurch. Run it once at assembly.

## The cut — assemble, then one review

1. **Assembly** — author one scene with one track layer. Its `clips` are
   the shots in playback order, each with an id, source reference and its
   approved `trim`. Preserve the model's delivered cuts and the user's edits.
   The procedure and per-seam transitions are in `assembly.md`.
2. **One review with the user.** The assembled film in `picsart_scene_editor`,
   watched once through. What they point at is fixed: a glitch — hands, teeth,
   a melted face — by the model's edit sibling on that clip; a bad join through
   **Join repair** above, not an automatic re-roll; a coverage hole by a new shot
   card back to `picsart-film-scenes` when the chosen repair needs new footage.
   Then the cut is final when they say so, recorded in `film.json`. This one
   review is the whole review: there is no separate rough cut, fine cut,
   written picture lock, defect list or full-size watch. After it: no picture changes except a fix the user asks for — colour and
   sound work on this cut, and a silent change strands them on a stale one.

## The fine cut and polish — in the scene editor

Everything above is you editing on the user's behalf, one round-trip per note.
That is right for structure — order, coverage, which take — and wrong for the last
half-second of a shot, which is faster to *feel* than to describe. So the fine
cut and the polish pass happen in `picsart_scene_editor`, by the user's own hand:
it plays the assembled scene document, lets them trim, split, delete, duplicate,
crop, adjust, change speed, effects, volume and size, and returns the edited
document with their verdict.

- **Pass the shots, not a rendered cut.** The scene you open it on is the
  assembled track, every shot a clip over its source in playback order. That
  keeps the shot boundaries visible, keeps every trim handle able to reach back
  into the source, and needs nothing rendered first.
- **Give every asset its probed `width`, `height` and `duration`, truthfully.**
  `picsart_media_probe_media` gives all three for free, and you already hold them
  from the assembly. An overstated `duration` promises footage that does not
  exist.
- **The editor judges AND cuts; export renders.** The editor hands back the
  edited scene document and renders nothing, which is what keeps the next round
  reviewable. When the user approves the cut, `picsart_media_export` renders the
  file from that returned document — never from your earlier assembly.
- **Keep both: the picture on Drive, the document in the project folder.**
  Upload the rendered mp4 to `picsart_drive`; it takes media only. Save the
  approved scene document in the workspace project folder's scenes folder and
  record its path in `film.json`. The document is the editable cut and the
  export is the picture; keep both, so a later session resumes inside the
  user's own edit rather than from a flattened file.
- Full feedback contract in `../../picsart-film/references/widget-feedback.md`
  (`scene_editor_feedback`).

Gate line for the final cut: **the locked cut is the document the user approved
in the scene editor** — not your assembly. Record its `stateHash`, the document's
project-folder path and the rendered file's Drive location in `film.json`, so finishing
grades the picture the user actually approved.

## Assembling a scene — mechanics

The scene tools do the work: probe → author → validate → review →
export, condensed in `assembly.md`, which is self-contained.

**Read the live editing recipe before changing the scene.** Use
`picsart_media_get_recipe({ name: "video-editing" })` and load its relevant
schema slices. Apply trims, crops, transitions, transforms and sound changes
according to that recipe, then validate and reopen `picsart_scene_editor`.

**Every edit is a `picsart_media_*` operation on the scene — never a
regeneration, and never a file the user is asked to handle.** Trim, split,
re-order, drop a stretch, a transition, a speed or motion change, a crop, a
sound edit: all of it exists as a compositor operation, all of it is
bookkeeping over the source clips, and none of it spends a credit. The
failure this rule exists to stop is spending video rates on something the
timeline already does — re-rendering a shot to make it shorter, or to start
later, or to lose its last second, when a trim does that for nothing. If an
edit seems to have no compositor operation, say so and ask; do not reach for
`picsart_generate`, and do not tell the user to export it and fix it
themselves.

The habits that matter here:

- Bootstrap, validate and **`picsart_media_export` are all free** — iterate
  order, trims and transitions without paying, and render when you need a real
  file rather than hoarding the call. What an export still costs is TIME (a real
  GPU render) and a new file in Drive, so it is worth doing on a settled cut
  rather than on every keystroke — but it is not a budget decision.
- Before any render, put the cut in **`picsart_scene_editor` — the scene
  editor**: the authored, validated track scene, every shot a clip in
  playback order, passed as `scene`. The editor plays it in the browser, so the
  user watches the real cut with nothing rendered. **The editing there is free
  and instant** — it moves windows over the source clips, so trimming a shot's
  edges, splitting it at the playhead and deleting it all happen live and cost
  nothing. Only two things come back: the edited scene, and comments. Never
  paste scene JSON at the user. The editor takes no per-shot prompt or cast, so
  keep each clip's shot, prompt and characters in `film.json` — that is what
  turns a comment into a retake.
- **One editor, and it always carries the whole cut.** The scene is
  every shot in playback order. Never an editor for a single clip, never one per
  piece of a cut the user just made, and never two open in one turn — one per
  piece shows the same picture back several times. Their own edit needs no
  second look to confirm it — record the cut, say in one line what changed, and open the editor
  again only for material they have not seen, with the full recut in it. If two
  are ever live at once anyway, queue them as `picsart-film-scenes` says: one editor's
  feedback is one item, and nothing advances until the queue is empty.
  **Focused join comparisons are the exception:** follow
  `join-repair.md` to review A → B against A → candidate → B without
  changing the accepted cut. An edited or extended clip is never a lone clip in
  the editor either: it goes into the cut, and the whole cut goes back up with
  one line naming the seconds that changed.
- Within a scene the default seam is a **hard cut** (`transition: ""`) — scenes
  are constructed from coverage, and continuity is the cut's job. Transitions
  belong *between* scenes if anywhere; `crossfade 0.5` is the defensible default,
  `assembly.md`'s transition table for anything else.
- Draft exports at draft canvas (854×480). The final-resolution export happens
  once, in `picsart-film-finishing`, after the final-res re-roll.
- Ordinary review rounds run in that same editor, on the NEW take. Focused join
  variants use `join-repair.md`; otherwise, if the user prefers the
  previous attempt they say so and you put its url back in the cut yourself —
  free. Keep every take's url in your own plan
  bookkeeping so you can.
- **Read its feedback as two different things.** `document` (when `edited` is
  true) is an EDIT THE USER ALREADY MADE — the editor performs trims, splits and
  deletions in place, so it is not a request and there is nothing to interpret.
  `comments` (pins, each with its `layerId` and `time`) and `timelineComments`
  (stretches, `start`/`end`) are the part that carries a requested change.
  Diagnose each note's meaning before choosing compositor work or generation; a
  note about a seam is not itself permission to regenerate. Combine compatible
  notes on a shot while preserving everything the user asked to keep.
- **Recording the cut is bookkeeping, not a render.** Read `document`'s clips
  in playback order — the clips of the montage's `track` layer, or top-level
  media layers in a scene built by hand — each over its source (`assetId` into `assets[]`, or
  an inline `asset`) with `content.trim` in that file's seconds — and write each
  window to its shot's `trim` with `trimSource: "user"`; a split is two clips on
  one source, a deleted shot is a clip that is gone. Record `stateHash` beside
  the cut, and carry `document` forward as the film's scene. Validate it
  (`picsart_media_validate_scene`) before anything else is built on it.
- **The old takes never move.** Nothing already in `Shots/` is moved,
  overwritten or deleted — same rule as `Assets/`, and it is what lets the user
  come back and edit again from the original material. A render of the cut
  (`picsart_media_export`, when a file is wanted) goes in a new subfolder under
  `Shots/` (`picsart_drive action=create_folder`, `folderUid` =
  `film.json.drive.shotsUid`).
- **The next round reopens on `document`, not on a render** — and only when
  there IS a next round: new material, or a note that needs watching. The
  user's own cut is not a reason to reopen (above). Apply your changes to
  `document` (`picsart_media_patch_scene`, or a re-bootstrap from the recorded
  windows when a take was swapped), validate, and open the editor on the result.
  Its clips still reach into the whole source, so every handle can reach back
  into the material this round trimmed off. Reopening on rendered clips would
  weld each trim shut, and a shot cut a second too short could never be opened
  back up — which is precisely what the trim handles exist to allow.
- **Its direction speaks the shotlist board's language.** A camera move or a
  colour named in a comment is that board's own preset name, so
  `Slow push-in` in a note means exactly what that name meant when the shot was
  planned — any of the 50 in [presets-camera.md](../../picsart-film-scenes/references/presets-camera.md). It all arrives as the user's
  words in a comment's `instruction` or a stretch's `text` — fold it into the
  shot's prompt rather than parsing it. **Folding
  rewrites prose, so re-read the speaking characters' voice lines off their
  assets and keep them verbatim** (`../../picsart-film-scenes/references/prompt-blocks.md`)
  — a reworded voice line returns a different voice, and the same applies to a
  new shot card ordered from here.
- **Text that belongs to the world goes on as a layer here, never into a
  prompt.** A headline on a screen, a number on a phone, a name on
  a door, a sign in the street: the model glitches typographic text, so the shot
  is generated without it and the words are composited over the clip, sized and
  placed to sit in the frame as though they were always there. This is the same
  rule `picsart-film-finishing` applies to the film's own titles, applied to text
  inside the picture. The picture prompts ban invented
  lettering for the same reason
  (`../../picsart-film-scenes/references/step-3-scene-pictures.md`).
- **Keep dialogue and ambience/music on separate audio layers** in the scene
  graph — that separation is what makes J/L cuts possible (sound leading or
  trailing the picture across a seam) and lets the ambience bed carry across
  cuts, the edit-side counterpart of the prompt's audio-tail rule.
- **Speech-cut review on assembled dialogue scenes**: `picsart_media_transcribe`
  the assembled cut and read the reconstructed script AS PROSE — seams must read
  fluently, no dangling connective or orphan pronoun across a join, no clipped
  word at a scene edge. If it doesn't hold together as a paragraph it will not
  hold as a scene.
- **Virtual camera moves — the free camera adjustment.** The compositor can
  animate the clip layer's own window: either the **`ken_burns` motion preset**
  (`zoom` ≤ 1.2, `direction` `in`/`out`/a compass point, `pan` in composition
  pixels) via `picsart_media_apply_motion_preset`, or **`animations` keyframes**
  on `scale` / `position` / `anchor` via `picsart_media_patch_scene` — `anchor`
  is the zoom centre. A push-in is scale rising, a drift is position gliding, a
  punch-in is two scale keyframes ~0.1s apart. Exact shapes in
  `assembly.md`. No new pixels —
  staging and validating are free, and the cost rides inside the export the
  film already buys. Use it when a good take has a dead camera, to recentre a
  drifted composition, or to Ken-Burns the animatic stills. **Honest
  limits**: 2D only (no parallax, no orbit — it reads as zoom, not dolly);
  keep zoom ≤ ~15–20% or the resolution loss shows (the finishing upscale
  masks some of it); nothing exists beyond the source frame, so a pull-out
  only works on takes generated wide (see `picsart-film-scenes`' generate-wide
  note). Wrong move or wrong energy is a camera-change retake in
  `picsart-film-scenes`, not a crop. The desperate last resort — a video-edit model
  re-rendering the clip with a different camera — is charged and risks the
  identity; name it as such if ever offered.
- **Verification is bounded: two fix rounds, then deliver.** For focused join
  experiments, use `join-repair.md`'s stopping rule instead; a rejected
  candidate never becomes the cut merely because two rounds elapsed. One round = look
  once (a scene review or a contact-sheet spot-check, not both), fix EVERY
  failing join in ONE rebuild. After the second round, export what you have
  and say in one line what is still weak — a flawed delivered cut beats a
  perfect undelivered one, and ending a session with no film is the worst
  outcome. This bounds the VERIFICATION loop only — a shot's 10–15 generation
  iterations in `picsart-film-scenes` are a different budget and keep their own rule.

## Cleanup — inside the one review

What generation spoiled — extra fingers and teeth, drifting objects, boiling
textures, edge jitter, random pseudo-text — is fixed when the user points at
it in the review. The repair path is the **edit sibling** (`picsart-film-scenes` step
5): the clip, the defect named to the second ("shot 3, 14–16s: five fingers
on the left hand"), the same numbered references — nothing else. Swap the fix
into the cut and watch the whole stretch in `picsart_scene_editor`, not only
the defect — an edit can fix the hand and lose the light. A defect the edit
sibling will not take in two tries is a re-roll of the run. If the model will
not give the shot back clean in 2–3 tries, the honest fallbacks are a recut
around it (a cutaway or a tighter trim — free) or accepting it, said out loud.
Frame-by-frame retouch is a real path only outside this surface.

Gate out: the user has called the cut final · shot order and trims saved to
`docs/` · everything durable on Drive. Route to `picsart-film-finishing`.

## Costs

| Free | Charged |
|---|---|
| bootstrap, re-bootstrap, `picsart_media_validate_scene`, `picsart_media_query_layout`, `picsart_media_probe_media`, `picsart_media_apply_scene_template`, **`picsart_media_export`**, `picsart_scene_editor` (the scene editor — playing the cut, and trimming, splitting, deleting and commenting on a shot are all free, happen in the browser and render nothing), all planning | every cleanup regeneration (`picsart_generate`) |

The one charged thing here is a cleanup regeneration, and it routes through
`picsart-film-scenes` step 5 — so it carries that skill's rule: preflight, the number to
the user, then the yes. A fix nobody priced is still a purchase.

Export is a real GPU render, so it costs time and makes a file — spend it on a
settled cut, not on every keystroke. It does not cost credits.

## Traps

- Editing only after all generation ends. The parallel edit is where coverage
  holes are found while they are still cheap.
- Cutting from the raw pile because selects lag. Fix the selects.
- Re-exporting to answer "what if". Export costs no credits, but every render
  takes real time and leaves another file in the user's Drive — re-bootstrap and
  the scene editor answer the question sooner and leave nothing behind.
- Opening the scene editor per clip, or once per piece after the user cuts in
  it. The editor is the whole cut, once — anything else is the same picture
  shown back several times, and only the first send gets answered.
- Locking or exporting your assembly after the user edited in the scene editor.
  The document they returned is the cut; grading the wrong one strands finishing
  on a stale picture.
- Picture changes after lock without telling finishing.
- Grading before cleanup — the colorist grades shots that are about to be
  replaced.
