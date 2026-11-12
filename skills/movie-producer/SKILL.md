---
name: movie-producer
description: Make a short narrative film from a story, with recurring characters, one look and approved cast/location references, then draft video and a reviewed cut. Storyboard or animatic only on explicit request. Use for short films, movies, multi-scene scripts, or continuing an existing film (shot list, shot changes or next step). Load first; it brings in the film skills for each stage. Not for a drama series or its episodes (make-short-drama), a single clip, or footage the user already has.
metadata:
  uses: film-story-writing, film-cast-design, film-shot-generation, film-cutting, film-finishing, footage-reframing, background-music, scene-building-basics, quality-review, realistic-color-grade, sd25-pe, sd2-pe, film-animatic, voice-over-generation
  optional: realistic-color-grade, film-animatic, voice-over-generation
  title: Produce a short film
  short-description: Make a short film from your story, scene by scene
  argument-hint: '[story idea or script]'
  starter-prompt: Make a short film from my story.
argument-hint: '[story idea or script]'
---

# Short film

When you read `picsart_scene_capabilities` or the recipe index (`picsart_scene_recipe` without `name`), pass `useCase: "movie-producer"`: the answer leads with what this job reads and names the rest in one line.

A film is not a long video. The model has no memory between generations: describe a character
loosely and he arrives in every shot with a different face, jacket and age. Everything here exists
to keep those people and places consistent. Lock the story, shot list, cast and location references,
then shoot draft video directly. The first moving draft the user reviews is the assembled cut.
Storyboard panels and an animatic are made only when the user explicitly requests them. They are
not part of the default flow, and are never offered as another decision before shooting.

Read picsart-video-rules first. One job: a story in, a short film out, with recurring people and places
and one look.

Before acting on a stage, load the skills in its row that apply to this job, also when the work resumes there.
`(preview-requested)` applies only to an explicit request for a storyboard or animatic;
`(animatic-requested)` only to an explicit animatic request. These skills and the preview REVIEW
are otherwise skipped; the location references are still prepared.

| Stage | Gate | Skills |
|---|---|---|
| 1. The idea | — | — |
| 2. The look | ASK | film-story-writing |
| 3. The story and the model | ASK | film-story-writing, film-shot-generation, sd2-pe, sd25-pe |
| 4. The shot list | ASK | film-story-writing, film-shot-generation |
| 5. Cast, places and props | SPEND, ASK, REVIEW (preview-requested) | film-cast-design, film-shot-generation, scene-building-basics, film-animatic (preview-requested), voice-over-generation (animatic-requested), quality-review (preview-requested) |
| 6. Shooting | SPEND, ASK | film-shot-generation |
| 7. The cut | SPEND, ASK, REVIEW | film-cutting, scene-building-basics, quality-review |
| 8. Finishing | SPEND, ASK, REVIEW | film-finishing, background-music, realistic-color-grade |
| 9. Deliver | ASK, DELIVER | film-finishing, footage-reframing |

Read these before you need them:

| File | Read it before you… |
|---|---|
| `references/stages.md` | say a stage is done, or open the next one |
| `references/board-replies.md` | act on a reply from any board |
| `references/project-record.md` | write or resume the project record |

## Before you start

**Route first.** The dividing line is recurring identity across scenes.

| The user brings | Route |
|---|---|
| One clip's worth of idea ("a boot stepping onto scree") | Not this use case. Say so, and offer one generation: `picsart_model_choose`, then SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says) and `picsart_generate` |
| Footage to cut together | Not this use case. Say it is not built yet here |
| A story: scenes, people who recur, dialogue | This use case, from stage 1 |
| A film already under way (a project record) | Resume: read the record, say where the film stands, continue at its stage |

**Pace: director by default**, as picsart-video-rules says. In express pace the user comes in only for the
boards, the three locks (the look, the story with its model, the assets), the cut's review, every charged call no stated spend limit covers and
anything beyond a quote.

## How you talk to the user

Talk and ask as picsart-video-rules says. Here that means:

- one board per decision; everything else waits in the record's `openDecisions`;
- what each board's reply holds is in `references/board-replies.md`;
- where things stand reads like "Stage 5 of 9 · cast, places and props — locking Cal (2 of 5
  done)", and the gate view shows which scenes have everything they need ("not ready yet", never
  "a hole");
- an alarm word is for a real gate violation, such as a video about to be bought for a scene
  whose assets are not locked.

## The project record

The film's state is one record, and it outranks your memory of it. Where the host gives you
files, keep it as `film.json` in the working folder; otherwise keep it in the conversation and
give it to the user once, at the end of a working session, to paste back next time. Never print it
mid-flow. Update it whole at every milestone: a gate passed, an asset locked, a batch dispatched or
landed, a review round, picture lock, the export. Its shape and the migration of older ten-stage records are in `references/project-record.md`.

Beside the facts it keeps the **brief**: the logline, the world in three sentences, the people as
people, and the standing decisions with their reasons ("hard cuts only: the film is about
abruptness"). On resume, read it before saying where things stand. With no record at hand, take
what the user says about the film as its state and carry on; ask for the record only when the step
needs a fact they have not given.

## Gates

**A gate is passed only when its checklist in `references/stages.md` is met**, or when the user
consciously overrides it; record the override and its reason. Before you say a stage is done or
name the next one, write its checklist with ✓ or ✗ per line and the evidence beside each ✓ (a
status a tool returned, a user's yes, a recorded override). A line with ✗ means the stage is not
done: say which line and what closes it.

**Choosing how to meet a rule is your craft call; choosing to spend or risk money against a closed
gate is never yours.** Which model shortlist, which order, whether a face needs one more view: yours,
recorded, never asked. Buying video for a scene whose assets are not locked, going beyond a quote,
trading quality for money: the user's.

**The challenger at each decision.** Before you go on from a decision, quality-review's challenger (the
`challenger` agent where the host has it) asks "why this?" of it: the idea (stage 1), the look and
the story (2, 3), the shot list (4), each sheet, plate, scene picture and location map picked and why (5), and
every quote before its SPEND (5, 6, 8, and a repair in 7 that needs a generation). Act on its
verdict as quality-review says. A `stop`, or a `rethink` of the user's own choice, goes to the user in the
next ASK, the cheaper alternative first, before anything is spent.

## 1. The idea

- **Read the user's brief first.** Every file in the material that is not media, read in full
  before the first question, as picsart-video-rules's The user's own brief says. A brief sets the message, the
  audience and the must-shows.

Ask for the idea only if the user has not given one. Once there is one, ask nothing more here:
runtime and frame are set on the look console, and the story proposes an ending the user can
change.

## 2. The look

**`picsart_film_setup` comes first, before a word of story is written**, one call per visual
world. Genre decides how the story is told, and every shot card sits under what this console
locks: the style line, the lens family the cards' focal lengths come from, and the colour scheme
each card's own palette has to fit.

- Pre-set it from the idea with `suggested`, one `suggested.why` line each, as film-story-writing says: the genre the
  events make, a tone when the story names a period, and the colour.
- **`film` (the title) is required.** `ratio` and `duration` go inside `suggested.selections`, under
  those field names, never as top-level arguments: the schema rejects anything it does not list.
- **Pass `ratio` whenever the user named a format at all** ("vertical", "TikTok", "square"). Pass
  the runtime they said as `duration`. Nothing infers a format; the console's default stands
  otherwise.
- The console is the ASK. On `film_setup_feedback` (`verdict: "locked"`), store `stylePrefix`
  verbatim and the `selections` as they came. That lock is the look's lock; there is no later one.
- If the genre changes at any point, film-story-writing rewrites the story first.

## 3. The story and the model

**The story.** film-story-writing writes it, for the locked genre, with its viewer track. State the identity budget
you inferred ("two faces and one garage") rather than asking for it. Show the track's after-watch questions under the
story, for correction: they are what the user and the cold watch are asked after each draft.

**The model, in the same turn.** The candidates are the current models, in this order:

| Model | Frame | Length per run | Reference images | Draft |
|---|---|---|---|---|
| `seedance-2.5` | 16:9, 9:16, 1:1, 4:3, 3:4, 21:9 | 4–30 s | 30 | `draft: true` |
| `kling-v4-omni` | 16:9, 9:16, 1:1, 21:9 | 3–30 s | 8 | none: `720p` |
| `wan-3.0-video` | 16:9, 9:16, 1:1, 4:3, 3:4 | 2–30 s | 10 | none: `480P` |
| `veo-3.1` | 16:9, 9:16 | 4, 6 or 8 s | 3 | none: `720p` |

Read each one's `picsart_model_params` before the board (film-shot-generation's model steps 2 and
3); the table is a guide, the params decide. Drop a candidate only when its params cannot hold the
film's frame or its runs (Veo 3.1 holds no 1:1 and no run over 8 s). Never offer an older model
(Seedance 2.0, its Fast and Mini, Kling V3, Hailuo, Wan 2.7) unless the user names it. The user's
balance and the cheapest-first rule set the draft resolution, never the model: they never put an
older model on the board or make one `recommended`.

Open `picsart_model_choose` under the story with the candidates that survive, in that order, the
first one `candidates[].recommended`, each `candidates[].bestFor` line written as this film's trade
("one continuous 30 s take, tops out at 720p").

- The pick is the story's yes unless the user sends a note with it. A note about what happens is
  answered as film-story-writing says, and the rewritten paragraph is shown again with the model board.
- On the pick, record the model, its take ceiling and its edit and extend siblings, as film-shot-generation
  finds them. One model for the whole film. A Seedance pick (`seedance-…`) also brings in the `sd25-pe`
  skill for Seedance 2.5 or `sd2-pe` for Seedance 2.0, as film-shot-generation's Seedance reference says.

## 4. The shot list

**`picsart_film_shotlist` once, with every scene in one call.** Load film-story-writing before you write
the cards: it turns the approved story into them, and its peak rule marks one card, the `Peak`
line's shot, with the moved face `unguarded` and what shows ("@teo relief, unguarded: the tears
come"), every other face held in; film-shot-generation packs them into runs against the model's ceiling, with one join
sentence on the shot that opens each run. Pass `film`, the model, and the setup's defaults, so the
user never picks from a vocabulary the film has not adopted.

**Use the model's capacity before opening the board.** Load film-shot-generation's Runs method
and its seams reference. Read the selected model's accepted durations and reference limits from
`picsart_model_params`, then pack the ordered shot cards into the fewest runs that fit, across
scene boundaries. Assign run ids only after packing: the board preserves those boundaries, so
one id per beat would lock in needless generations. Several cuts belong inside one generation;
a climax, a close-up, a new scene or "easier to generate" is no reason to split it.

Check each boundary: can the next shot fit in the preceding run within the model's duration and
reference limits? If yes, keep packing; if no, record the limiting constraint. Preserve shot order,
shot lengths and dialogue; do not stretch shots or add filler to reach the ceiling. The final
remainder can be short. A shorter run otherwise needs a specific model limit or the user's explicit
split. For example, six proposed runs of 7, 7, 4, 3, 6 and 3 seconds become one 30-second generation
when the selected model accepts 30 seconds and their combined references fit. The nine shot
cards and their internal cuts stay separate inside that generation.

Write the internal cut pairs and each necessary run edge using film-shot-generation's seams
reference: match action, eyelines and screen direction, keep geography, and carry frames only
for its named exceptions. Fewer generations must preserve this method, not replace the cuts
with one long shot or buy a bridge for every boundary.

- The board approves camera and seconds. It is not a place to rewrite the story: an edit that
  changes what happens is a story note, so rewrite the paragraph first, then open the board again.
- On `shotlist_board_feedback`, **replace** your list with it, runs included. Fields the board does
  not carry (references, prompt versions, trims) stay on the shot by id.
- A long scene held in one shot comes with film-shot-generation' coverage recommendation on its card. Keep
  the single shot only if the user chooses it on the board.
- A card that film-shot-generation flags for a kinetic move on a big face, set on the board or changed
  later, gets one short ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) before the run is compiled: the move as the user set it, or one of
  film-shot-generation' safer versions. The camera stays the user's.
- After a long stretch on one video, offer once to reopen the board to recap what comes next.
  Honour a no without asking again.

## 5. Cast, places and props

**The project folder first**, before anything is generated. `picsart_drive_create_folder` with
`path: "Picsart Plugin/<film-slug>"` and
`children: ["Library", "Assets", "Shots", "Exports"]`. Keep every uid it returns in the record.
Say it once, plainly: "Created Picsart Plugin/the-garage in your Picsart Drive, with Library,
Assets, Shots and Exports inside. Everything this film makes is filed there." Never say it again,
and never list the whole Drive: no `list` without a `folderUid`. Pass the right `folderUid` on
every `picsart_generate` and `picsart_job_status` call of the film, and the project folder as
`projectFolderUid` on every asset call. A finished job is filed only when you save it, as
picsart-video-rules's SPEND rule 4 says: save every finished picture and take into its folder before you
show it. Never call a filed file permanent.

Then film-cast-design's conveyor, in one pass:

1. Draft every descriptor as film-cast-design says, then offer the cast board once
   (film-cast-design, *The starting point*). It is the one stop here and costs nothing; a reply that
   ignores it keeps the story's descriptors. There is no other approval round.
2. Compile each picture with `picsart_film_compile_prompt` (a reference `kind`) and read its
   `check`, then **one SPEND for the whole batch**: every sheet and plate on one
   quote.
3. Dispatch on the yes as one batch (picsart-video-rules, SPEND), with `folderUid` set to Assets, and
   let the batch's card follow the jobs as picsart-video-rules says.
4. Look at each picture (picsart-video-rules, Asset URLs) before anything uses it, then put them all on
   `picsart_asset_approve` in one call (at most 12 tiles; more go on a second board), with the one thing to judge them by as the board's `judge`, and one line per tile as its `assets[].why`.
5. Act on the reply as `references/board-replies.md` says. Each approved asset is cut into views and
   locked with `picsart_asset_save`, as film-cast-design says. Before regenerating a rejected
   picture, save that version as `rejected` and record it as below. The replacement is regenerated
   under its own SPEND and shown alone on a fresh board, with `assets[].version`; omit `assets[].previousUrl` when the previous picture
   was rejected. A discarded tile is recorded as rejected and never used.

A person the user photographed is saved as it came and is not put up for approval: it is theirs.
film-cast-design flags what it cannot settle on its own, about a photo the user brought or about the
film's era. Raise each flag once, as one short ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) with the options film-cast-design names. Anything
generated is its own SPEND.

### A rejected cast picture

Treat "Change one", "not her", "profile is not ok", "it's not her", or any no to a cast picture
as a rejection. If several pictures were shown and the target is unclear, ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) which one
without showing them again; do not regenerate until it is identified.

Before regenerating, call `picsart_asset_save` for the rejected version with `status: "rejected"`,
its original `tag`, `sheetVersion`, `portraitUrl`, `projectFolderUid` and saved asset metadata.
Pass the saved `identityReferences` too. Every new save supplies the user's original photo URLs
there, or `identityReferences: []` when all views are generated. Do not infer provenance from a
view's position; preserve unknown provenance on older records.
Record its tag, version, file uid, URL and all extracted view/panel URLs in the project's
`rejectedAssets[]`, and mark that version's asset row `rejected`. Confirm the save succeeded before
a replacement is generated; on failure keep the local rejected entry and retry the save, never reuse it.
A replacement gets a new version and stays in review until the user approves it.

Never show a rejected picture again, including in a comparison, `previousUrl`, an old plan card or
an asset recap. Never pass any part of it as a reference: no full-body front, profile, crop, view
or panel. Rejecting one view rejects the whole sheet unless the user explicitly said otherwise;
record any such exception and keep only the explicitly permitted view separate from the rejected sheet.
Check `rejectedAssets[]` before every display, reference selection, plan and resumed film turn.
Remove rejected references from pending opening frames and shot plans before continuing.

For a person made from the user's own photos, keep those original photos in `identityReferences[]`
and use them as the identity reference for every replacement. Rejecting a generated sheet never
rejects the user's original photos; do not substitute a rejected generated face for them.

### Location references before shooting

Keep the location map. Follow film-shot-generation's scene-pictures reference: a wide for every
scene, its opening scene picture cut from that wide, and a room map where the scene cuts between
walls. Reuse one map per place and time of day; a single outdoor background uses its wide as its
geography. Record the URLs in `scenes[].pictures` and the geography line in `scenes[].geography`.

Compile and verify the required pictures, quote them together with SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says), then generate the
independent pictures in a batch. Check each before its board review, including the cast's faces,
opening positions and room geometry. Use `picsart_asset_approve` for the location references
and apply `references/board-replies.md`. Reuse approved pictures already in the record. A real app's
screen is built as a scene layer from the user's screenshots or recording, never generated.

**No still test.** The scene pictures are where the cast is checked, as film-cast-design says.
A cast or prop correction goes through that asset's conveyor only, under its own SPEND.

**The gate into shooting:** the story and shot list approved, every scene in a run has approved
location references, and film-cast-design's gate into a run holds for all its tags, read back from
`picsart_asset_list`. The opening scene picture starts the scene's first run; later runs use
film-shot-generation's continuity references. No storyboard panels, voiced slideshow or animatic
approval is required in the default flow.

### Only when the user requests a storyboard or animatic

Record the explicit request in `requestedPreview` (`kind: "storyboard"` or `"animatic"`,
`status: "requested"`) and load film-animatic for that work. A request for a **storyboard** uses
its panel method only: quote and make the requested panels, check them, and review them on
`picsart_asset_approve`. It does not buy voices, music or a timed animatic. A request for an
**animatic** uses its timed-preview method and voice-over-generation for its sound; quote the
needed pictures and sound with SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says), then validate, check and REVIEW the preview as that
skill says. Reuse the approved cast and location references in either case.

The request chooses the work, not permission for an unquoted spend. Apply SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says) to every new
charged operation. On approval, set `requestedPreview.status: "approved"` and continue to
shooting; no second shot-selection question is added. Storyboards and animatics are never
required, recommended as another gate, or created on a resume without that explicit request.

## 6. Shooting

Shoot the approved shot list directly, respecting any explicit exclusions the user already made.
Do not ask them to choose the shots again. Use the approved scene-opening images and continuity
references as film-shot-generation says; never require one generated panel per shot.

**Recheck capacity before the forecast or quote**, including on resume. Reconcile the approved
shot cards, current model limits and planned runs; show the generation count and each run's
seconds against the ceiling. A batch with six items is still six generations. Do not quote
mergeable short runs. If correcting them changes approved run boundaries, show that correction
in the existing approval/quote step; keep the user's explicit splits, shot choices and seconds.
Recompile the corrected runs and their joins, and replace the old quote. Never repack a submitted
or completed job into another paid generation; keep its handle and existing footage.

Before any run is quoted, a shot that film-shot-generation flags for a palette arguing with the film's
scheme gets one short ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) with its options.

1. **The forecast, once, before the first video:** runs × each run's seconds at the model's draft
   rate from `picsart_preflight`, plus a margin for repairs, and the finish beside it. It is an
   estimate, not a quote.
2. **Shoot every run as a draft, in one batch**, as film-shot-generation says: the model's draft
   setting or its lowest resolution, and no test run first. Every independent run is compiled,
   verified and sent together, one call per run: one quote for the batch with the finish priced
   beside it as an estimate, one yes, one monitor. The yes buys the drafts only. A run that waits for an earlier take (its frames
   are the references) is its own SPEND once that take lands and passes your check.
3. **No film so far.** While takes run, never assemble, cut, open or show the film so far: a landed
   take waits for the others. As each take lands, find its actual cuts and judge it as
   film-shot-generation's takes reference says. That is your technical check, not acceptance:
   every take stays a candidate until the user approves the cut (7). No question between the
   takes and the cut.
4. Dialogue is judged in the cut's REVIEW, by ear. Say that the words were not checked against the
   script by a tool.

Shooting is done when every take has landed and passed your check, with its actual cuts, prompt,
quote and handle in the record. No take is accepted yet.

## 7. The cut

When the last take lands, film-cutting assembles the film once: every candidate take in story order
with hard cuts, every generation one clip exactly as generated: no split at a run's internal cuts,
no trims, no transitions, padding or freeze frames. The user's own trims and splits are kept and
never recomputed. Check it with quality-review, its cold watch included (quoted first with its own SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says) unless
every call is quoted at 0 credits; on a no, the review line says "no cold watch yet"), then REVIEW the whole cut, unasked and opened cold: this is the film's review. Once the user has
answered, say what your check observed in each take. **The user's approval of the cut
accepts every take in it**, and its shots become `final`.

**Notes route by meaning**, as film-shot-generation says: an edit, an extend or a re-roll. A note it
flags as ambiguous gets one short ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) between its two routes. **Each is its own SPEND**, shot as a draft
like the takes: a yes to a run is not a yes to its repair. A note on a seam is not a licence to buy footage: film-cutting's
join repair diagnoses first. A bridge between two runs is its own SPEND too, reviewed as
film-cutting's join repair says. Apply what the user points at, re-cut once and open it again, until
they call it final. After that, change no picture unless they ask.

## 8. Finishing

In this order, as film-finishing says: the finish of the draft takes, then colour, then sound.

1. **Finish the approved cut**, as film-finishing says: from each draft's `finalizeDraft` handle
   where it has one, otherwise an upscale or the approved run generated again at the finish
   settings. It is its own SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says), after the cut is approved, asked as film-finishing's one
   question: finish the approved takes, or keep the drafts. Then the cut is re-assembled at the
   finish size with the user's trims.
2. **Colour:** ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) with three or four looks that suit the film, from the look list in
   `picsart_scene_capabilities` (`sections: ["looksCompact"]`). Applying one is free.
   When the takes look glossy or plastic, as generated footage often does, one option is the
   realism grade, applied as the realistic-color-grade skill says.
3. **Music:** offer it once, only after the cut is final, and never bare: ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) with the brief
   drafted as the background-music skill says, and three exits: generate it, change the brief, or skip. A
   changed brief is redrafted and asked again; a skip is settled for the session. A yes is a SPEND,
   as picsart-video-rules says. Lay the bed as film-finishing says, then REVIEW the film with it, on how it
   sits under the dialogue. A note on its level moves it as the background-music skill says; a different
   track goes back through the background-music skill's brief, with a new SPEND. A film going to festivals
   or dubbing gets film-finishing's sound-team handoff offered once.

## 9. Deliver

DELIVER the final cut once, as picsart-video-rules says. Any further master from film-finishing's delivery
list is confirmed with one ASK before the first is exported. A master in another shape is reframed as the
footage-reframing skill says.
Then film-finishing's archive and disclosure: give the user the disclosure text (every model used,
per stage) and record it, and say generated music's licence is theirs to check before a festival or
a commercial use.

## When something fails

- **Out of credits: zero retries.** Say which step is paused and what it needs against the balance
  `picsart_credits` reads. Keep the record and every job handle. Continue only when the user says
  their credits are there; never poll the balance.
- **A dropped call is not a failed generation**: follow its job as film-shot-generation says.
- **A board that errors on a value** gets the value fixed and the board sent again. A board the
  host cannot draw gets the host notes' fallback, and the gate still holds.
- **Anything else a stage cannot run without** gets one identical retry, then one plain line: what
  you tried, what blocked it, what you need. Never reword and refire.
- **An outage is status, not a decision.** Keep going on everything free, keep the blocked item in
  `openDecisions`, and try again next turn. Never offer a choice the rules already answer, such as
  giving up a lead's consistency to dodge a temporary outage.
