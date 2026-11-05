---
name: make-short-drama
description: Make a vertical drama series, pilot or episode with a recurring cast. Use for a short drama, a story reel, microdrama, web series or its next episode. Not for a one-off film (movie-producer).
metadata:
  uses: drama-series-writing, film-story-writing, film-cast-design, film-shot-generation, film-animatic, film-cutting, film-finishing, footage-reframing, retention-hooks, spoken-captions, background-music, scene-building-basics, quality-review, realistic-color-grade, voice-over-generation
  optional: realistic-color-grade, voice-over-generation
  title: Make a short drama
  short-description: Make a vertical drama series with a recurring cast
  argument-hint: '[series idea or the next episode]'
  starter-prompt: Make a short drama series from my idea.
argument-hint: '[series idea or the next episode]'
---

# Make a short drama

Read picsart-video-rules first. Keep one visual world, one series Library and one accepted story
ledger. Decide on text, stills and sound before buying video: the user watches each episode as a
voiced animatic, and says yes to it, before its first take is bought. A generated episode is a candidate until
the user accepts it.

Before acting on a stage, load the skills in its row that apply to this job, also when the work resumes there.

| Stage | Gate | Skills |
|---|---|---|
| 1. The brief | ASK | — |
| 2. The series bible | ASK | drama-series-writing |
| 3. The look | ASK | film-story-writing |
| 4. Cast, places and props | SPEND, ASK | film-cast-design |
| 5a. Episode outline, script and model | ASK | drama-series-writing, film-story-writing, retention-hooks, film-shot-generation |
| 5b. The shot list | ASK | film-story-writing, film-shot-generation |
| 5c. Storyboard and animatic | SPEND, ASK, REVIEW | film-animatic, film-shot-generation, film-cast-design, voice-over-generation, scene-building-basics, quality-review |
| 5d. Shooting | ASK, SPEND | voice-over-generation, film-shot-generation |
| 5e. The cut, once the last take lands | SPEND, REVIEW | film-cutting, scene-building-basics, quality-review |
| 5f. Finishing, once per series | ASK, SPEND | spoken-captions, background-music, realistic-color-grade |
| 6. Verdict | — | quality-review |
| 7. Deliver and accept | ASK, DELIVER | film-finishing, footage-reframing |

| File | Read it before you… |
|---|---|
| `references/series-record.md` | create, update or resume the series record |

## Route and resume

| Request | Route |
|---|---|
| One-off short film | movie-producer |
| One clip | Offer one generation via `picsart_model_choose`, then SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says) and `picsart_generate` |
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

Use ASK, SHOW, SPEND, REVIEW and DELIVER as picsart-video-rules defines them. Director pace is the
default. Express pace still keeps boards, bible/look/asset locks, each charged call and any change
beyond a quote. Ask one decision at a time; keep the others in `openDecisions`.
Where the host notes give a drama its own route, follow it: it replaces the stages it names,
and every other gate here holds.

The exit checklist at each stage is binding. Before calling a stage done, mark each item ✓ or ✗
with evidence: a returned status, a user's answer, an approval already in the series record, or a
conscious override and reason. A ✗ keeps
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

## Build in stages: slides, voice, video

When the user asks for one stage of an episode by name (`slides`, `voice` or `video`, as the
`story` command passes it), build only that stage and stop at its REVIEW. Each stage opens only once
the user approved the one before it. A stage asked for early says, in one line, which approval is
missing, and offers to show that stage again. Take as fact whatever the series record or the user
already gives as approved: the brief, the bible, the look (its `stylePrefix` and `selections`), the
cast, the script, the model, the shot list and the voices. Mark that stage's exit ✓ with "approved in
the record" and never open its board again; a stage asks, or opens its board, only for what is still
missing. A supplied cast or picture is not in the Library until it is saved: when the record has no
`drive`, create the project as stage 4 says, then save each approved person, place and prop with
`picsart_film_save_asset` (`status: "locked"`, `projectFolderUid`, `sheetVersion`; it is free), read
`locked` in each result and write it to the cast manifest, before 5c.

| Stage | What it builds | Paid |
|---|---|---|
| `slides` | stages 1 to 5c's panels, then the silent animatic: one panel per shot, held for its line's time, with its on-screen text, and no sound | the pictures |
| `voice` | 5c's sound: each line in the cast's locked voice, the beds and effects, as the film-animatic skill says, laid on the approved slides, the panels re-timed to the real lines | the voice lines and sound |
| `video` | stages 5d to 5f, each take with its line's approved voice as reference audio where the model takes it, cut to the approved timing | the takes |

- `slides`: build the animatic as the film-animatic skill says, without its sound, and watch it
  cold. Then REVIEW it, titled "<Episode> - slides", opened cold. The on-screen text follows the house style the user gave (font, plate,
  safe area); without one, as the spoken-captions skill says. 5c's SPEND bought the pictures it
  quoted. A line with no picture yet, or a picture made again, is new: SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says) on the extras as one
  batch before you make them, never under 5c's yes. The animatic is a timing draft, so its stills
  hold on purpose: never add a move to a still only to pass a motion check. Check its joins,
  overlays, text and screens; the motion checks (a held still, an idle hold, a zoom over a still)
  run on the cut, in 5e.
- `voice`: SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says) on the episode's lines as one batch, then REVIEW the voiced animatic. A line's
  real length moves its still, never the words.
- `video`: forecast and buy as 5d says. The voiced animatic is the cut's timing reference in 5e.

Record the stage and each approval in the series record, so a later request resumes at the next
stage. Without a named stage, the episode runs straight through as below.

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
season arc. ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) on the proposed bible. Scope a long commission as drama-series-writing's season arc says. Test another
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
Raise film-cast-design's photo or era flags in one short ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) with its named options.

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
the opening and film-story-writing for scene writing and dialogue, and for the episode's viewer
track. Keep its story and scene form; put the serialization delta beside it, and the track's
after-watch questions under it, for correction. A story note returns a rewritten paragraph.

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
coverage. A kinetic move on a large face gets one short ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) with film-shot-generation's safer
options before compilation. After a long stretch, offer once to reopen the board; honor a no.

**Exit:** approved cards, valid runs, joins and asset tags all match the accepted script.

### 5c. Storyboard and animatic

The episode is drafted on stills and sound, and the user watches it before any take is bought. Load
film-animatic before you say what this stage needs or ask anything in it.

Use film-shot-generation for the wide, the scene picture and a room map where needed, and
film-animatic for one panel per shot, checked against its scene picture. A real app's screen is a
scene layer built from the user's own screenshots or recording, never generated. SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says) on the
episode's scene pictures and panels as one batch, then ASK through asset review. Batch generation
follows picsart-video-rules; review boards hold at most 12 tiles. Reuse suitable locked plates
rather than recreating sets. Check the cast's faces on these pictures as film-cast-design says;
there is no separate still test. Only a change the user asks for returns an asset through stage 4,
under its own SPEND, with a new version and fresh review.

Then the sound, as film-animatic says: every line in the cast's locked voice, a bed per scene and
the cards' effects, on one SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says), each line's real length probed. Build, validate and
cut-check the animatic, watch it cold (quality-review's cold watch, quoted first with its own
SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says) unless every call is quoted at 0 credits),
then REVIEW it with its sound, opened cold. Notes route as film-animatic says, a story
note back to 5a's script, a shot note to that panel or line alone, each change under its own SPEND;
loop until the user says yes. A user who wants to shoot without the animatic may, as a recorded
override; never skip it yourself.

**Exit:** every scene a run spans has approved pictures, every shot an approved panel, every needed
asset is locked, and the user approved the voiced animatic (or the override is recorded). Missing
evidence stops shooting.

### 5d. Shooting

Use film-shot-generation. **Which shots go to video is the user's:** ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) once, every shot
recommended unless the animatic showed a held panel works; a shot kept as a panel stays in the cut
as approved, and only the picked shots are quoted, each opening on its approved panel. Raise its
palette conflict flag through one ASK before quoting.
**Shoot every run as a draft,** as film-shot-generation says: the model's draft setting (Seedance
2.5's `draft`) or its lowest resolution, so the user sees the episode quickly and cheaply; the
finish comes after the cut is approved (5f). Forecast once: runs × two takes × seconds at the draft
rate from `picsart_preflight`, plus a repairs margin, with the finish beside it; the forecast is an
estimate, not a quote. Every independent run goes in one batch, on one quote and one SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says), the
finish shown on that quote as an estimate and not bought with it; never a test run before the
others unless the user asks for one (film-shot-generation, Traps). Say
a re-roll costs again. Before the quote, check every picture a run passes against the model's
input limits, its sides and its ratio, as film-cast-design's views say, and fix any outside them
for free; the user never approves a batch the model will refuse. Before the paid batch, declare
decisive evidence as quality-review's readiness verdict says. Compile, verify, generate and
monitor as the skill says. Every edit, extend or re-roll has
its own SPEND and is shot as a draft like the takes; a yes to the original run never buys a repair. Ask once about an ambiguous note.

**No partial episode.** While the episode's takes are still running, **never assemble, cut, open
or show the episode so far**: a landed take waits for the others. As each take lands, find
its actual cuts and judge it as film-shot-generation's takes reference says ("Judge it before the
user does"). That is your technical check, not acceptance: every landed take stays a candidate
until the user approves the cut (5e). So a run that film-shot-generation makes wait for an earlier
take waits here for that take to land and pass your check. There is no question between the
takes and the cut.

**Exit:** every take landed, its actual cuts found and checked by you; what the check observed,
prompts, quotes, handles and actual cuts saved. No take is accepted yet.

### 5e. The cut, once the last take lands

When the last take of the episode lands, use film-cutting and scene-building-basics to assemble
the episode once: every candidate take (5d) in story order with hard cuts, as film-cutting says,
each one clip exactly as generated (never split at its internal cuts, never trimmed), dialogue
on its own layer, the series' look and captions (5f) and, when chosen, its music. Add nothing
else the user did not ask for: no transitions, padding, freeze frames, stills played as video,
titles or template looks. A panel the user kept in 5d is
theirs, not a still played as video.
Check it with quality-review, its cold watch included (quoted first with its own SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says) unless
every call is quoted at 0 credits; on a no, the review line says "no cold watch yet"), and run the
verdict (6), then REVIEW the whole episode, opened cold: this is the episode's one review. Once the
user has answered, say what your check observed in each take. At episode 1 the review
also offers music once (5f). Judge dialogue by ear and say when no tool checked its words against
the script.

Change requests come in this review. A note on the cut ("tighten the opening") is applied and the
cut REVIEWed again. A take to redo ("redo the hallway take") is a repair with its own SPEND; when
it lands, the episode is re-cut once and REVIEWed again. Diagnose seam notes before buying
footage; a bridge or other generated repair needs its own SPEND. Preserve user trims and splits.
After the cut is approved, change picture only when asked.

The user's approval of the cut is the acceptance of every take in it: record each as
film-shot-generation's takes reference says under "Accept". Never record a take as accepted
before that approval.

**Exit:** the cut approved and its takes accepted, join checks recorded, user edits preserved.

### 5f. Finishing, once per series

The series' look (stage 3) and captions are set once and carried into every cut without asking
again: spoken-captions in the locked language and caption style, with caption timing, line
splits, script shaping and face clearance verified on episode 1. Ask for the caption style only
if episode 1 is the first time it comes up. Applying a look is free; offer realistic-color-grade
only when the user asks for a grade.

Music is offered once per series, in episode 1's review (5e). A yes drafts the
brief with background-music and is a SPEND; the series theme then goes under every later episode
without asking. A no holds for the series unless the user brings music up.

**The finish, once the episode's cut is approved:** finish its draft takes as film-finishing says,
from each draft's `finalizeDraft` handle where it has one, otherwise an upscale or the approved run
generated again at the finish settings. It is its own SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says), never bought with the drafts:
film-finishing's one question for the episode, finish the approved takes or keep the drafts.
Re-assemble the approved cut at the finish size with the user's trims, before the verdict (6).

**Exit:** look, captions and the music choice recorded for the series; the episode's finish
quoted, and bought or declined.

## 6. Verdict

Run quality-review's readiness verdict yourself on each cut before its review, with the series
checks beside the media checks: continuity from the accepted ledger, cast versions, knowledge
transfer, thread accounting, ending rotation and terminal closure where applicable. Say it in one
line with the cut; it is never a step for the user. Fix what it finds that needs no spend before
the review. Never describe an unaccepted candidate as an accepted episode.

**Exit:** one supported verdict recorded with the cut.

## 7. Deliver and accept

The user's approval of the cut accepts the episode. Only when the user accepts this episode
version: DELIVER the actual HTTPS master once with its verdict, as picsart-video-rules says,
commit its proposed story delta to the series record, mark it accepted and advance the next
episode. Then offer once to post it. Use film-finishing for archive and model disclosure; record
the disclosure and the music licence check the user owns. Confirm any additional master with one
ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) before its first export; one in another shape is reframed as the footage-reframing skill says.

Preserve rejected proposals separately. Persist production milestones as they happen without
committing their story deltas. Say where the series stands at session end.

**Exit:** delivery URL and disclosure saved; acceptance, or the still-proposed status, is explicit.

## Recovery

Out of credits: zero retries. Read `picsart_credits`, say the paused step, keep jobs and record,
and wait for the user's notice that credits are there. Never poll the balance. A dropped call is
followed by its job handle through film-shot-generation, never submitted twice. Fix an invalid
board value and resend; an unavailable board uses the host fallback with the gate intact.
A run the model refuses, or that fails, is said at once in plain words, with whether it was
charged and the fix; never wait for the user to ask. Other blocking calls get one identical retry,
then record what failed and what is needed. An
outage is status: continue free work and keep the blocked item for the next turn. Never replace
a locked person's consistency to work around an outage.
