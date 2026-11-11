# Stages: goals, gate checklists, common mistakes

Print a stage's checklist, ✓ or ✗ per line with the evidence beside each ✓, before you say the
stage is done. A ✗ line is what you say next: which line, and what closes it.

## Contents

1. The idea
2. The look
3. The story and the model
4. The shot list
5. Cast, places and props
6. Shooting
7. The cut
8. Finishing
9. Deliver

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
- [ ] Current model durations and reference limits were read; the ordered shots are packed into
      the fewest runs that fit, across scenes, before assigning run ids. Each boundary records why
      the next shot cannot fit, or the user's explicit split; a final remainder may be short.
- [ ] Every shot has its run; the shot opening each run carries the join sentence.
- [ ] Internal cuts and necessary run edges follow film-shot-generation's seams method.
- [ ] Every person, place and prop has a tag, including the lasting changes the story makes (a
      wrecked room, a torn coat).
- [ ] `shotlist_board_feedback` arrived with `verdict: "approved"`, and the stored list was replaced
      with it.

Common mistakes: opening the board before the look is locked; one board per scene; a
ceiling-length action with no coverage because the model allows it; a story change made on the
board and never shown as text.

## 5. Cast, places and props

**Goal:** every person and prop approved as a picture and locked; every place has approved location references.

- [ ] The project folder exists and its uids are in the record.
- [ ] Every generated picture was compiled, verified, quoted and bought on a yes.
- [ ] Every picture was looked at before it went on a board.
- [ ] Every generated person and prop is approved on `picsart_asset_approve` (a photographed person
      is not put up for approval), and its `picsart_asset_save` result reads `locked: true`.
- [ ] Every card's tag resolves to a single-view file (identity, wardrobe, each state, each prop),
      cut and checked.
- [ ] A photo the user brought is saved as it came, matched on probe, and never put up for approval.
- [ ] Every speaking character has a saved voice line.
- [ ] Every scene has an approved wide and opening scene picture, with the opening cast only.
- [ ] A room map exists where the scene cuts between walls; it is reused per place and time of day.
      A single outdoor background uses its wide as its geography.
- [ ] Location URLs and the geography line are recorded in `scenes[].pictures` and `scenes[].geography`.
- [ ] Every tag in a run has a locked row read back from `picsart_asset_list`.
- [ ] Scene pictures were checked for the cast's faces, positions and room geometry; no separate
      still test was bought. Per-shot panels exist only for an explicit preview request.

Common mistakes: putting a picture on a board before looking at it; the rest are film-cast-design's
Traps.

## 6. Shooting

**Goal:** every take landed as a draft and checked by you; none accepted yet.

- [ ] The approved shot list and any existing user exclusions determine the video runs.
- [ ] Capacity was rechecked before quoting: generation count and each run's seconds against the
      selected model's ceiling are shown; no mergeable short runs remain. A changed approved
      grouping is shown in the existing approval/quote step, with prompts and quote refreshed.
- [ ] Existing job handles and footage are preserved; repacking never resubmits paid work.
- [ ] Stage 5's cast and location-reference checks passed. Only an explicit `requestedPreview`
      needs its own review completed; no preview is required in the default flow.
- [ ] A forecast was given once, before the first video, at the draft rate with the finish beside
      it, and called an estimate.
- [ ] Every independent run went out in one batch as a draft (the model's draft setting or lowest
      resolution): no test run first, and the finish was not bought with it.
- [ ] Every charged dispatch was compiled, verified on its literal arguments, quoted, and bought on
      a yes, and its job handle is in the record.
- [ ] Every take that landed had the cuts it actually made checked; the film so far was never
      assembled or shown while takes ran.
- [ ] Every run has one prompt version and your check's notes logged.

Common mistakes: dispatching on the forecast; a test run first; the first batch at the finish
settings; a review per take. The shooting
traps are film-shot-generation'.

## 7. The cut

**Goal:** the cut the user calls final.

- [ ] The cut was assembled once, when the last take landed: every candidate in story order, one clip per generation, exactly as generated: no
      automatic split, trim, transition, padding or freeze frame.
- [ ] quality-review passed, or its weak points were said.
- [ ] The user reviewed the whole cut and called it final; that accepted every take in it, and
      every shot is `final`.
- [ ] Every trim the user made is recorded as theirs.

Common mistakes: cutting or showing the film before the last take lands;
buying footage for a seam before the pair was diagnosed; a separate review per clip.

## 8. Finishing

**Goal:** the final pixels, one look across the film, the sound decided.

- [ ] The approved draft cut was finished as its own SPEND after the approval: from each draft's
      `finalizeDraft` handle where it had one, otherwise an upscale or a fresh roll called so; then
      re-assembled at the finish size with the user's trims.
- [ ] Neighbouring shots match within each scene; the chosen look is applied.
- [ ] Music was offered once, after the cut was final, and the answer recorded; a bed was
      reviewed under the dialogue before it stayed.

Common mistakes: offering music before the cut is final. The grading traps are
film-finishing's, and the music traps background-music's.

## 9. Deliver

**Goal:** the film in the user's hands, and everything needed to make it again.

- [ ] QC notes closed: artifacts, joins, black or dropped frames, sound level steps.
- [ ] The final cut exported once; saved to Drive only if the result carried a `driveUid`.
- [ ] Any further master was confirmed with one ASK before the first was exported.
- [ ] The disclosure text given to the user and recorded: every model used, per stage.
- [ ] The record holds the final prompts, the asset rows, the shot list, the cut and every take.
