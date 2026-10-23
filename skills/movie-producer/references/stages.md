# Stages: goals, gate checklists, common mistakes

Print a stage's checklist, ✓ or ✗ per line with the evidence beside each ✓, before you say the
stage is done. A ✗ line is what you say next: which line, and what closes it.

## Contents

1. The idea
2. The look
3. The story and the model
4. The shot list
5. Cast, places and props
6. Scene pictures
7. Shooting
8. The cut
9. Finishing
10. Deliver

## 1. The idea

**Goal:** an idea to build on.

- [ ] The user gave an idea, in their words, recorded in the brief.

## 2. The look

**Goal:** the film's look, locked before a word of story.

- [ ] `picsart_film_setup` opened, pre-set from the idea, with `ratio` in `suggested.selections`
  when the user named a format.
- [ ] `film_setup_feedback` arrived with `verdict: "locked"`.
- [ ] `stylePrefix` stored verbatim, and the `selections` as they came.

Common mistakes: writing the story first and keeping it under the wrong genre; typing a style line
by hand; asking the runtime, frame or ending as a round of questions before the console.

## 3. The story and the model

**Goal:** a story the user has read and said yes to, and the one video model for the film.

- [ ] Ten lines, then every scene as what the viewer sees and hears, in the viewer's words.
- [ ] The thing the story is about is seen in the first scene; no camera or film words.
- [ ] Nothing contradicts what the user's brief fixed.
- [ ] The user said yes to this text (a pick on the model board with no note counts).
- [ ] `model_choice_feedback` arrived; the model, its take ceiling and its edit and extend siblings
      are recorded.

Common mistakes: approving a story the user has not read; picking the model silently. How a story
note is answered, and the writing traps, are film-story-writing's.

## 4. The shot list

**Goal:** every scene as shots, with camera and seconds, grouped into runs.

- [ ] Every shot has a card: action and line copied from the story, the tags of everyone and
      everything in frame, what each face feels, seconds, and camera.
- [ ] Every shot's seconds keep film-shot-generation' duration rule.
- [ ] Every shot has its run; the shot opening each run carries the join sentence.
- [ ] Every person, place and prop has a tag, including the lasting changes the story makes (a
      wrecked room, a torn coat).
- [ ] `shotlist_board_feedback` arrived with `verdict: "approved"`, and the stored list was replaced
      with it.

Common mistakes: opening the board before the look is locked; one board per scene; a
ceiling-length action with no coverage because the model allows it; a story change made on the
board and never shown as text.

## 5. Cast, places and props

**Goal:** every person and prop approved as a picture and locked; every place described.

- [ ] The project folder exists and its uids are in the record.
- [ ] Every generated picture was compiled, verified, quoted and bought on a yes.
- [ ] Every picture was looked at before it went on a board.
- [ ] Every generated person and prop is approved on `picsart_film_review_assets` (a photographed person
      is not put up for approval), and its `picsart_film_save_asset` result reads `locked: true`.
- [ ] Every card's tag resolves to a single-view file (identity, wardrobe, each state, each prop),
      cut and checked.
- [ ] A photo the user brought is saved as it came, matched on probe, and never put up for approval.
- [ ] Every speaking character has a saved voice line.

Common mistakes: putting a picture on a board before looking at it; the rest are film-cast-design's
Traps.

## 6. Scene pictures

**Goal:** every scene's place, pictured and approved, before its first run.

- [ ] Every scene has an approved wide and a scene picture cut from it, and a room map where the
      scene cuts between walls.
- [ ] Each scene picture shows the opening shot's cast only, as designed.
- [ ] Every picture was quoted and bought on a yes, looked at, and approved on one board.
- [ ] Every tag of every scene in a run has a locked row, read back from `picsart_film_list_assets`.
- [ ] The locked cast passed film-cast-design's stills, quoted and bought on a yes of their own.

Common mistakes: reading coverage from memory; a scene picture that stages the dramatic centre
instead of the opening; clean pictures of a place a later run has already wrecked.

## 7. Shooting

**Goal:** every run accepted, split at its real cuts, every shot final.

- [ ] A forecast was given once, before the first video, and called an estimate.
- [ ] The first run went alone, and its recipe is recorded.
- [ ] Every charged dispatch was compiled, verified on its literal arguments, quoted, and bought on
      a yes, and its job handle is in the record.
- [ ] Every take that landed was split at the cuts it actually made and reviewed inside the whole
      film.
- [ ] Every shot is `final`, with one prompt version per run and the take's verdict logged.

Common mistakes: dispatching on the forecast; sending the first run with others. The shooting
traps are film-shot-generation'.

## 8. The cut

**Goal:** the cut the user calls final.

- [ ] The selects are assembled in story order, one clip per shot, windows over the run files.
- [ ] quality-review passed, or its weak points were said.
- [ ] The user reviewed the whole cut and called it final.
- [ ] Every trim the user made is recorded as theirs.

Common mistakes: waiting until every run is shot to start cutting, and finding the holes late;
buying footage for a seam before the pair was diagnosed; a separate review per clip.

## 9. Finishing

**Goal:** the final pixels, one look across the film, the sound decided.

- [ ] The final-resolution pass was quoted as its own SPEND, called a fresh roll, and re-assembled
      at the finish settings.
- [ ] Neighbouring shots match within each scene; the chosen look is applied.
- [ ] Music was offered once, after the cut was final, and the answer recorded; a bed was
      reviewed under the dialogue before it stayed.

Common mistakes: offering music before the cut is final. The grading traps are
film-finishing's, and the music traps background-music's.

## 10. Deliver

**Goal:** the film in the user's hands, and everything needed to make it again.

- [ ] QC notes closed: artifacts, joins, black or dropped frames, sound level steps.
- [ ] The final cut exported once; saved to Drive only if the result carried a `driveUid`.
- [ ] Any further master was confirmed with one ASK before the first was exported.
- [ ] The disclosure text given to the user and recorded: every model used, per stage.
- [ ] The record holds the final prompts, the asset rows, the shot list, the cut and every take.
