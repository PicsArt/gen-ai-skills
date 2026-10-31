---
name: make-short-drama
description: Make a vertical drama series, pilot or episode with a recurring cast. Use for a short drama, microdrama, web series or its next episode. Not for a one-off film (movie-producer).
metadata:
  uses: drama-series-writing, film-story-writing, film-cast-design, film-shot-generation, film-cutting, film-finishing, retention-hooks, spoken-captions, background-music, scene-building-basics, quality-review, realistic-color-grade
  optional: realistic-color-grade
  title: Make a short drama
  short-description: Make a vertical drama series with a recurring cast
  argument-hint: '[series idea or the next episode]'
  starter-prompt: Make a short drama series from my idea.
argument-hint: '[series idea or the next episode]'
---

# Make a short drama

Read picsart-video-rules first. Keep one visual world, one series Library and one accepted story
ledger. Decide on text and stills before buying video. A generated episode is a candidate until
the user accepts it.

| Stage | Gate | Skills |
|---|---|---|
| 1. The brief | ASK | — |
| 2. The series bible | ASK | drama-series-writing |
| 3. The look | ASK | film-story-writing |
| 4. Cast, places and props | SPEND, ASK | film-cast-design |
| 5a. Episode outline, script and model | ASK | drama-series-writing, film-story-writing, retention-hooks, film-shot-generation |
| 5b. The shot list | ASK | film-story-writing, film-shot-generation |
| 5c. Scene pictures | SPEND, ASK | film-shot-generation, film-cast-design |
| 5d. Shooting | SPEND, REVIEW | film-shot-generation, scene-building-basics, quality-review |
| 5e. The cut | REVIEW | film-cutting, scene-building-basics, quality-review |
| 5f. Finishing | SPEND, ASK, REVIEW | film-finishing, spoken-captions, background-music, realistic-color-grade |
| 6. Verdict | REVIEW | quality-review |
| 7. Deliver and accept | ASK, DELIVER | film-finishing |

| File | Read it before you… |
|---|---|
| `references/series-record.md` | create, update or resume the series record |

## Route and resume

| Request | Route |
|---|---|
| One-off short film | movie-producer |
| One clip | Offer one generation via `picsart_model_choose`, then SPEND and `picsart_generate` |
| Series, pilot, sitcom or drama episode | This use case |
| Series record present | Read it, call `picsart_film_list_assets` with its `projectFolderUid`, say where the series stands, continue at the next episode |

An unfinished proposed episode resumes at its recorded stage before another is started. Restore
the accepted ledger and current asset versions first. Do not reset people to the original premise.
Take supplied state as fact; ask only for missing facts needed by the next step. A writing-only
request stops at the requested outline or script and needs no paid step or production board.
On every resume, before outlining the next episode, call `picsart_film_list_assets` with the
record's `projectFolderUid`. The Library is the authority on who is locked at which version; the
record's cast manifest is only its copy. Do this even for an outline-only request.

## Gates and interaction

Use ASK, SPEND, REVIEW and DELIVER as picsart-video-rules defines them. Director pace is the
default. Express pace still keeps boards, bible/look/asset locks, each charged call and any change
beyond a quote. Ask one decision at a time; keep the others in `openDecisions`.

The exit checklist at each stage is binding. Before calling a stage done, mark each item ✓ or ✗
with evidence: a returned status, a user's answer or a conscious override and reason. A ✗ keeps
the gate closed. Record overrides; never choose to spend against a closed gate yourself.
Run quality-review's challenger at the brief, bible, look, script, shot list, selected assets and
every quote before SPEND. A stop or rethink of the user's choice goes to the next ASK with the
cheaper alternative first. Craft choices remain yours; spending and quality/cost trades are theirs.

A board's opening result is not a decision. Wait for its feedback. Use these replies:

| Reply | Update |
|---|---|
| `film_setup_feedback` | Require `verdict: "locked"`; retain `selections` and `stylePrefix` verbatim |
| `model_choice_feedback` | Store `chosen.id` and `chosen.name`; a story comment needs a rewritten scene and fresh board |
| `shotlist_board_feedback` | Replace the approved scenes and runs, never merge; retain non-board fields by shot id |
| `asset_review_feedback` | Approved tiles go to view extraction and locked save; regenerate only `changes`; never use `discarded` |
| `render_monitor_feedback` | Match `done` and `failed` rows by `jobId`; use label only when absent; save finished results before review; `unchecked` rows follow SPEND rule 4 of the `picsart-video-rules` skill |
| Scene editor reply | `approved` or `needs_changes`; preserve `edited`, `documentUrl`, `comments` and `timelineComments`, including user trims |

## 1. The brief

Read every supplied non-media brief in full before asking. Extract the premise, audience and fixed
facts. Ask what is missing: format (serial, pilot, standalone, finale or sitcom), episode count,
episode length, language, whether it has a successor, and template or Freeform. Never assume an
episode count. Suggest the nearest named template without replacing a supplied story. Template
counts and lengths are suggestions to confirm. Trending needs host web search; say when absent.

**Exit:** format, count, length, language, successor status and template/Freeform are answered;
fixed facts are recorded. Do not spend while these decisions are missing.

## 2. The series bible

Use drama-series-writing for Story DNA, relationships, knowledge tiers, reveal bank, sets and the
season arc. ASK on the proposed bible. Scope a long commission as drama-series-writing's season arc says. Test another
pairing and action before extrapolating the pilot to the season.

**Exit:** the user locked the bible and arc, with successor flags, planned ending rotation and
terminal closure. Story DNA here is a concept plan; write scene scripts after the look locks.

## 3. The look

Open `picsart_film_setup` once for the series, before the shot list. Use the series title as
`film`. Set `suggested.selections.ratio` to `vert` (9:16) unless the user named another frame;
put episode seconds in `suggested.selections.duration`, not season seconds. Supply the suggestion
reasons as film-story-writing says. Store the lock's `stylePrefix` and `selections` verbatim,
including scheme and hue for subsequent compilation. Reopen with `current` only for an explicit
look revision; later episodes inherit the lock. Record varying episode runtimes separately.

**Exit:** actual setup feedback locks the look and frame; the episode runtime is recorded.

## 4. Cast, places and props for the whole series

Create one series project with `picsart_drive_create_folder`,
`path: "Picsart Films/<series-slug>"`, `children: ["Library", "Assets", "Shots", "Exports"]`.
Record all returned uids and say once where files go. Scope any listing to its folder. Pass the
proper `folderUid` on every generation and job-status call, and `projectFolderUid` on asset calls.
Save finished pictures and takes before showing them. A filed file is not promised permanent.

Use film-cast-design to design and lock the WHOLE series inventory once: people, sets and props.
Quote its compiled and verified reference batch under one SPEND, then review the landed pictures
on `picsart_film_review_assets` (at most 12 tiles per board). On approval, cut views and save with
`picsart_film_save_asset`, `status: "locked"`, `projectFolderUid` and `sheetVersion`. This files the
asset in the project's Library. Read `locked` in the result; `saved` alone does not establish a lock.
A changed tile gets its own SPEND and a fresh board with `assets[].version` and `assets[].previousUrl`. Approved
tiles never reappear on a board. A supplied person's photo is theirs, not a redesign invitation.
Raise film-cast-design's photo or era flags in one short ASK with its named options.

Later episodes call `picsart_film_list_assets` with `projectFolderUid` and reuse locked rows.
Never re-design a locked person or reopen their review merely because an episode changed.
A requested changed look is a new `sheetVersion`, saved and locked, with superseded versions and
affected episodes recorded. Preserve voice notes verbatim. Check dependencies by identity,
wardrobe, geometry and light; a version bump alone does not force regeneration.

**Exit:** the whole planned inventory is locked, every needed tag has a usable view and version,
and the manifest, folder uids and voice notes are in the record. Unforeseen new assets later go
through this gate alone; an existing lock survives.

## 5. Produce one episode

### 5a. Outline, script and model

Use drama-series-writing against the committed ledger, with its episode beats and serialization
checks, the finale's closure included. Use retention-hooks for
the opening and film-story-writing for scene writing and dialogue. Keep its story and scene
form; put the serialization delta beside it. A story note returns a rewritten paragraph.

Use film-shot-generation to shortlist models. Open `picsart_model_choose` under the script:
3 candidates (2 is fine), exactly one recommended, with the trade for this episode. The pick
accepts the script unless accompanied by a story note; rewrite and show again in that case.
Keep one video model across the series unless a deliberate change is approved. Record ceiling,
edit/extend siblings and the image model. Subsequent episodes inherit that choice.

**Exit:** script accepted, proposed delta checked, model and limits known. Nothing is canon yet.

### 5b. Shot list

Use film-story-writing for cards and film-shot-generation for runs. Open `picsart_film_shotlist`
once with every scene of this episode, the model and setup defaults. The board approves camera
and seconds; story changes return to the paragraph first. Replace its list and runs from feedback;
keep references, prompt versions and trims by id. Rebuild joins on newly grouped runs and split
any run over the ceiling. Keep a long single shot only if the user chooses it over recommended
coverage. A kinetic move on a large face gets one short ASK with film-shot-generation's safer
options before compilation. After a long stretch, offer once to reopen the board; honor a no.

**Exit:** approved cards, valid runs, joins and asset tags all match the accepted script.

### 5c. Scene pictures

Use film-shot-generation for wide, scene picture and room map where needed. SPEND on the episode's
picture batch, then ASK through asset review. Batch generation follows picsart-video-rules;
review boards hold at most 12 tiles. Reuse suitable locked plates rather than recreating sets.
Run film-cast-design's still test under its own batch SPEND before the first video. A failure
returns only the affected asset through stage 4, with a new version and fresh review.

**Exit:** every scene a run spans has approved pictures, every needed asset is locked and the cast
passed its stills. Missing evidence stops shooting.

### 5d. Shooting

Use film-shot-generation. Raise its palette conflict flag through one ASK before quoting.
Forecast once: runs × two takes × seconds at the draft rate from `picsart_preflight`, repairs
margin, and the final-resolution pass beside it. The forecast is an estimate, not a quote.
SPEND first on one risky run with dialogue and cuts; say a re-roll costs again. Shoot as drafts.
Use its result to improve the recipe before buying the remaining independent runs as a batch.
Before the first paid run, declare decisive evidence as quality-review's readiness verdict says.
Compile, verify, generate and monitor as the skill says. Every edit, extend or re-roll has its
own SPEND; a yes to the original run never buys a repair. Ask once about an ambiguous note.

Every landed take opens REVIEW that turn. Split it at actual cuts, assemble every accepted take
plus the new one in story order with film-cutting, check with quality-review and open the whole
episode so far in `picsart_scene_editor`. A new take alone cannot prove a join. Judge dialogue by
ear and say when no tool checked its words against the script.

**Exit:** each run accepted and split, shots final, prompts, quotes, handles and actual cuts saved.

### 5e. The cut

Use film-cutting and scene-building-basics to assemble selects. REVIEW the whole episode with
quality-review until the user calls the cut final. Diagnose seam notes before buying footage;
a bridge or other generated repair needs its own SPEND and review. Preserve user trims and
splits. After picture lock, change picture only when asked.

**Exit:** final cut approved, join checks recorded, user edits preserved.

### 5f. Finishing

Use film-finishing in order: final-resolution pass, colour, sound. Ask whether drafts are good
enough to keep before quoting the pass on its own SPEND. ASK with three or four looks from
`picsart_scene_capabilities`, `sections: ["looksCompact"]`; applying a look is free. Offer
realistic-color-grade when available and useful for glossy footage.

Offer music once after picture lock. ASK with the background-music brief and generate/change/skip
exits. A yes is a SPEND. Use the series theme; a new track needs a new brief and SPEND. REVIEW
how it sits under dialogue. Offer film-finishing's sound-team handoff once where relevant.
Use spoken-captions for the locked language and caption style. Verify caption timing, line splits,
script shaping and face clearance on the pilot before repeating it. Review the finished episode.

**Exit:** finishing choices settled, captions and sound checked, master available and evidence saved.

## 6. Verdict

Apply quality-review's readiness verdict to existing evidence, with the series checks beside the media
checks: continuity from the accepted ledger, cast versions, knowledge transfer, thread accounting,
ending rotation and terminal closure where applicable. Never describe an unaccepted candidate as
an accepted episode. Use one headline: Needs revision, Not yet
verified, or Reviewed candidate. A playable export or a successful job is not proof of readiness.
User acceptance is separate. Keep every required check after a repair and inspect affected scope.

**Exit:** one supported verdict, material issues or unknowns and the next action are recorded.
An unresolved candidate may be shown as such, never described as a finished accepted episode.

## 7. Deliver and accept

DELIVER the actual HTTPS master once with its verdict, as picsart-video-rules says. Confirm any
additional master with one ASK before its first export. Use film-finishing for archive and model
disclosure; record the disclosure and the music licence check the user owns.

Only when the user accepts this episode version, commit its proposed story delta to the series
record, mark it accepted and advance the next episode. Preserve rejected proposals separately.
Review approval of a take or cut is not episode acceptance. Persist production milestones as they
happen without committing their story deltas. Say where the series stands at session end.

**Exit:** delivery URL and disclosure saved; acceptance, or the still-proposed status, is explicit.

## Recovery

Out of credits: zero retries. Read `picsart_credits`, say the paused step, keep jobs and record,
and wait for the user's notice that credits are there. Never poll the balance. A dropped call is
followed by its job handle through film-shot-generation, never submitted twice. Fix an invalid
board value and resend; an unavailable board uses the host fallback with the gate intact.
Other blocking calls get one identical retry, then record what failed and what is needed. An
outage is status: continue free work and keep the blocked item for the next turn. Never replace
a locked person's consistency to work around an outage.
