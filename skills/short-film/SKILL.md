---
name: short-film
description: Make a short narrative film from a story - several scenes, characters who look like themselves in every shot, one locked look - through a staged production the user approves step by step. Use when the user wants to make a short film, a movie, an episode or a multi-scene story ("make a short film about…", "I have a script", "a movie with two characters"). Not for a single clip from a description, and not for cutting footage the user already has.
metadata:
  uses: film-story, film-cast, film-shots, film-edit, film-finishing, music-bed, scene-compose, evaluate
---

# Short film

A film is not a long video. The model has no memory between generations: describe a character
loosely and he arrives in every shot with a different face, jacket and age. Everything here exists
to beat that one problem, consistency, and it runs on one economic law: **stills are cheap, video
is expensive.** Every decision that can be made on text or pictures is made there, before the
first video is bought.

Read video-core first. One job: a story in, a short film out, with recurring people and places
and one look.

| Stage | Gate | Skills |
|---|---|---|
| 1. The idea | — | — |
| 2. The look | ASK | film-story |
| 3. The story and the model | ASK | film-story, film-shots |
| 4. The shot list | ASK | film-story, film-shots |
| 5. Cast, places and props | SPEND, ASK | film-cast |
| 6. Scene pictures | SPEND, ASK | film-shots, film-cast |
| 7. Shooting | SPEND, REVIEW | film-shots, scene-compose, evaluate |
| 8. The cut | REVIEW | film-edit, scene-compose, evaluate |
| 9. Finishing | SPEND, ASK, REVIEW | film-finishing, music-bed |
| 10. Deliver | ASK, DELIVER | film-finishing |

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
| One clip's worth of idea ("a boot stepping onto scree") | Not this use case. Say so, and offer one generation: `picsart_model_choice`, then SPEND and `picsart_generate` |
| Footage to cut together | Not this use case. Say it is not built yet here |
| A story: scenes, people who recur, dialogue | This use case, from stage 1 |
| A film already under way (a project record) | Resume: read the record, say where the film stands, continue at its stage |

**Pace: director by default.** The user sees each stage's decision before the next one starts.
Say once, at the start, that they can ask for express pace: you make the routine craft calls and
bring them in only for the boards, the three locks (the look, the story with its model, the
assets), every charged call and anything beyond a quote. Pace changes how often you ask, never a
safeguard: every SPEND still gets its own quote and its own yes.

## How you talk to the user

- **Say only what they need to decide.** The pipeline is your bookkeeping. No accounting of what
  the last stage cost, no explaining how the machine works, no subtitles on a stage name, no
  standing offers ("drop in references any time"). Two sentences and one question is a good turn.
- **One decision per turn**, and one board per decision. Keep everything else in the record's
  `openDecisions` until it blocks.
- **One confirmation covers a set.** Things shown together get one "anything to change?", never
  one sign-off per item.
- **Free work never asks permission.** Opening a board, drafting descriptors, compiling a prompt,
  updating the record: do it. Questions are for taste and for money.
- **A board is the whole turn.** Open it, add at most one line, and end the turn. Never write the
  board's content out in chat beside it.
- **Read the reply before the sentence around it.** A board's decision arrives as the host notes
  say; what each one holds is in `references/board-replies.md`. Never ask the user to repeat, press
  again or paste a decision.
- **A request to see something is a request to open its surface**: the shot list on its board, an
  asset as its picture, a cut in REVIEW. Never print its data instead.
- **Material arriving is itself the request.** Pictures or takes that land are shown, checked and
  put up for the user's verdict in that turn, unasked. Say what you observed; never grant the
  approval yourself ("three of the four check out").
- **Where things stand.** At the start of a session, and when a stage changes, one line: "Stage 5
  of 10 · cast, places and props — locking Cal (2 of 5 done)". When asked, show the stage list with
  ✓ or ✗ per gate and which scenes have everything they need, as markdown tables read from the
  record, in plain words ("not ready yet", never "a hole").
- **Progress is never damage.** Mid-stage state is "not yet". Alarm words are for a real gate
  violation, such as a video about to be bought for a scene whose assets are not locked.

## The project record

The film's state is one record, and it outranks your memory of it. Where the host gives you
files, keep it as `film.json` in the working folder; otherwise keep it in the conversation and
give it to the user once, at the end of a working session, to paste back next time. Never print it
mid-flow. Update it whole at every milestone: a gate passed, an asset locked, a batch dispatched or
landed, a review round, picture lock, the export. Its shape is `references/project-record.md`.

Beside the facts it keeps the **brief**: the logline, the world in three sentences, the people as
people, and the standing decisions with their reasons ("hard cuts only: the film is about
abruptness"). On resume, read it before saying where things stand.

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

## 1. The idea

Ask for the idea only if the user has not given one. Once there is one, ask nothing more here:
runtime and frame are set on the look console, and the story proposes an ending the user can
change.

## 2. The look

**`picsart_film_setup` comes first, before a word of story is written**, one call per visual
world. Genre decides how the story is told, and every shot card sits under what this console
locks: the style line, the lens family the cards' focal lengths come from, and the colour scheme
each card's own palette has to fit.

- Pre-set it from the idea with `suggested`, one `why` line each, as film-story says: the genre the
  events make, a tone when the story names a period, and the colour.
- **`film` (the title) is required.** `ratio` and `duration` go inside `suggested.selections`, under
  those field names, never as top-level arguments: the schema rejects anything it does not list.
- **Pass `ratio` whenever the user named a format at all** ("vertical", "TikTok", "square"). Pass
  the runtime they said as `duration`. Nothing infers a format; the console's default stands
  otherwise.
- The console is the ASK. On `film_setup_feedback` (`verdict: "locked"`), store `stylePrefix`
  verbatim and the `selections` as they came. That lock is the look's lock; there is no later one.
- If the genre changes at any point, film-story rewrites the story first.

## 3. The story and the model

**The story.** film-story writes it, for the locked genre. State the identity budget you inferred ("two
faces and one garage") rather than asking for it.

**The model, in the same turn.** film-shots narrows the video models to the few that can shoot
this film. Then open `picsart_model_choice` under the story: 2–4 candidates, exactly one
`recommended`, each `bestFor` line written as this film's trade ("one continuous 30 s take, tops
out at 720p").

- The pick is the story's yes unless the user sends a note with it. A note about what happens is
  answered as film-story says, and the rewritten paragraph is shown again with the model board.
- On the pick, record the model, its take ceiling and its edit and extend siblings, as film-shots
  finds them. One model for the whole film.

## 4. The shot list

**`picsart_shotlist_board` once, with every scene in one call.** film-story turns the approved
story into cards; film-shots packs them into runs against the model's ceiling, with one join
sentence on the shot that opens each run. Pass `film`, the model, and the setup's defaults, so the
user never picks from a vocabulary the film has not adopted.

- The board approves camera and seconds. It is not a place to rewrite the story: an edit that
  changes what happens is a story note, so rewrite the paragraph first, then open the board again.
- On `shotlist_board_feedback`, **replace** your list with it, runs included. Fields the board does
  not carry (references, prompt versions, trims) stay on the shot by id.
- A long scene held in one shot comes with film-shots' coverage recommendation on its card. Keep
  the single shot only if the user chooses it on the board.
- A card that film-shots flags for a kinetic move on a big face, set on the board or changed
  later, gets one short ASK before the run is compiled: the move as the user set it, or one of
  film-shots' safer versions. The camera stays the user's.
- After a long stretch on one video, offer once to reopen the board to recap what comes next.
  Honour a no without asking again.

## 5. Cast, places and props

**The project folder first**, before anything is generated. `picsart_drive` with
`action: "create_folder"`, `path: "Picsart Films/<film-slug>"` and
`children: ["Library", "Assets", "Shots", "Exports"]`. Keep every uid it returns in the record.
Say it once, plainly: "Created Picsart Films/the-garage in your Picsart Drive, with Library,
Assets, Shots and Exports inside. Everything this film makes is filed there." Never say it again,
and never list the whole Drive: no `list` without a `folderUid`. Pass the right `folderUid` on
every `picsart_generate` and `picsart_job_status` call of the film, and the project folder as
`projectFolderUid` on every asset call. Never call a filed file permanent.

Then film-cast's conveyor, in one pass:

1. Draft every descriptor as film-cast says. No separate approval round.
2. Compile each picture with `picsart_film_compile_asset_prompt` and check it with
   `picsart_prompt_verify`, then **one SPEND for the whole batch**: every sheet and plate on one
   quote.
3. Dispatch on the yes as one batch (video-core, SPEND), with `folderUid` set to Assets, and
   follow the jobs on `picsart_render_monitor` as video-core says.
4. Look at each picture (video-core, Asset URLs) before anything uses it, then put them all on
   `picsart_asset_review` in one call, with the one thing to judge them by as the board's `judge`, and one line per tile as its `why`.
5. Act on the reply as `references/board-replies.md` says. Each approved asset is cut into views and
   locked with `picsart_save_asset`, as film-cast says. A change is regenerated under its own SPEND and put on a fresh board with `version` and
   `previousUrl`. A discarded tile is never used.

A person the user photographed is saved as it came and is not put up for approval: it is theirs.
film-cast flags what it cannot settle on its own, about a photo the user brought or about the
film's era. Raise each flag once, as one short ASK with the options film-cast names. Anything
generated is its own SPEND.

## 6. Scene pictures

Every scene gets its pictures before its first run: the wide, the scene picture cut from it, and a
room map where the scene cuts between walls, as film-shots says. **One SPEND for every scene's
pictures**, one batched call, one monitor, one `picsart_asset_review` for all of them. The scene picture is the
opening frame of the scene's first run; the wide and the map are its place.

**The cast on stills:** film-cast's test of the locked cast is **one SPEND for the batch**, before
the first run. A person who fails it goes back through stage 5's conveyor alone: the tightened
descriptor, a new sheet under its own SPEND, and a fresh board.

**The gate into shooting:** film-cast's gate into a run holds for every run, every scene it spans
has approved pictures, and the cast passed its stills. A missing one is a stop.

## 7. Shooting

Before any run is quoted, a shot that film-shots flags for a palette arguing with the film's
scheme gets one short ASK with its options.

1. **The forecast, once, before the first video:** runs × two takes × each run's seconds at the
   model's rate from `picsart_preflight`, plus a margin for repairs. It is an estimate, not a quote.
2. **One run first.** If the whole film is one run, that is the film. Otherwise the riskiest run:
   the one with dialogue and the most cuts. SPEND on its own quote, saying a re-roll costs again.
   What it teaches goes into the recipe before the rest are bought.
3. **Then the rest, as a conveyor**: independent runs dispatched together, each run compiled, verified and
   sent as film-shots says, one call per run. One quote for the batch, one yes, one monitor.
4. **Every take that lands opens REVIEW in that turn, unasked.** film-shots splits it at the cuts
   it actually made. Build the whole film so far with film-edit's assembly, every accepted take
   plus the new one in story order, check it with evaluate, and open it in
   `picsart_scene_editor`. Never a review of the new take alone: what fails is the join.
5. **Notes route by meaning**, as film-shots says: an edit, an extend or a re-roll. A note it
   flags as ambiguous gets one short ASK between its two routes. **Each is its own SPEND.** A yes
   to the run is not a yes to its repair.
6. Dialogue is judged in REVIEW, by ear. Say that the words were not checked against the script
   by a tool.

A scene block is done when every run in it is accepted and split at its real cuts, every shot is
final, and every prompt, quote and take is in the record.

## 8. The cut

film-edit assembles the selects into one scene, hard cuts within a scene, every shot its own clip
over its run file. Check it with evaluate, then REVIEW the whole cut. Apply what the user points
at and open it again, until they call it final. A note on a seam is not a licence to buy footage:
film-edit's join repair diagnoses first, and a repair that needs a generation is its own SPEND. So
is a bridge between two runs, reviewed as film-edit's join repair says. After the user calls the cut
final, change no picture unless they ask.

## 9. Finishing

In this order, as film-finishing says: the final-resolution pass, then colour, then sound.

1. **The final-resolution pass**, as film-finishing describes it, on its own quote and its own
   yes.
2. **Colour:** ASK with three or four looks that suit the film, from the look list in
   `picsart_media_get_capabilities` (`sections: ["looksCompact"]`). Applying one is free.
3. **Music:** offer it once, only after the cut is final, and never bare: ASK with the brief
   drafted as the music-bed skill says, and three exits: generate it, change the brief, or skip. A
   changed brief is redrafted and asked again; a skip is settled for the session. A yes is a SPEND,
   as video-core says. Lay the bed as film-finishing says, then REVIEW the film with it, on how it
   sits under the dialogue. A note on its level moves it as the music-bed skill says; a different
   track goes back through the music-bed skill's brief, with a new SPEND. A film going to festivals
   or dubbing gets film-finishing's sound-team handoff offered once.

## 10. Deliver

DELIVER the final cut once, as video-core says. Any further master from film-finishing's delivery
list is confirmed with one ASK before the first is exported.
Then film-finishing's archive and disclosure: give the user the disclosure text (every model used,
per stage) and record it, and say generated music's licence is theirs to check before a festival or
a commercial use.

## When something fails

- **Out of credits: zero retries.** Say which step is paused and what it needs against the balance
  `picsart_credits` reads. Keep the record and every job handle. Continue only when the user says
  their credits are there; never poll the balance.
- **A dropped call is not a failed generation**: follow its job as film-shots says.
- **A board that errors on a value** gets the value fixed and the board sent again. A board the
  host cannot draw gets the host notes' fallback, and the gate still holds.
- **Anything else a stage cannot run without** gets one identical retry, then one plain line: what
  you tried, what blocked it, what you need. Never reword and refire.
- **An outage is status, not a decision.** Keep going on everything free, keep the blocked item in
  `openDecisions`, and try again next turn. Never offer a choice the rules already answer, such as
  giving up a lead's consistency to dodge a temporary outage.
