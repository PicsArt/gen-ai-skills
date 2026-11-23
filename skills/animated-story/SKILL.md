---
name: animated-story
description: 'Make an animated story you can edit afterwards: drawn or built 2D or 3D animation, with characters, objects or just shapes, played as a scene, not generated video. Use for a cartoon, a kids'' story, a mascot clip or any animated short in a drawn look. Not for live-action or generated-video films and dramas (movie-producer, make-short-drama, story). Covers a clip (one shot in one place, any length, any number of characters, 9:16 or 16:9, who walk in, wave, reach, hold or carry a prop, with a narrator''s voice-over or captions) or an episode (several shots or places, or characters who talk, lip-synced, with the shots joined into one video). A character is picked from the ready-made cast or the user''s saved library, or built from a part sheet into an editable cut-out rig and checked on a short test render, then saved for reuse. Not for a character''s sheet with no scene, nor for motion on a design (animate-design).'
metadata:
  uses: character-rigging, scene-building-basics, voice-over-generation, lip-sync-lines, visual-style, visual-styles, background-music, motion-review
  optional: visual-style, visual-styles, voice-over-generation, background-music
  title: Make a cartoon
  short-description: Cast a character and make a short animated scene
  argument-hint: '[who is in it and what happens]'
  starter-prompt: Make me an animated story with a character.
argument-hint: '[who is in it and what happens]'
---

# Make a cartoon

When you read `picsart_scene_capabilities` or the recipe index (`picsart_scene_recipe` without `name`), pass `useCase: "animated-story"`: the answer leads with what this job reads and names the rest in one line.
**Read the capabilities once, in slices.** Call `picsart_scene_capabilities` with `useCase: "animated-story"` and no `sections`
first: that returns the index, small, with each section's name and size. Then ask only for the sections the step needs
(`sections: ["motionPresetList"]` for presets, `["template:<uri>"]` for one template, `["look:<id>"]` for one look), once
each, and keep what they return in your notes instead of calling again. Never ask for the whole document or the whole scene
schema, never pipe a result through a shell filter to find a field, and read the schema of a layer or asset type once, when
the first layer of that type is built. A section that is large is read by its name, not around it.

Read picsart-video-rules first. The film's style is fixed first (stage 1), then the plan and one of two modes are chosen together (stage 1b):
- **Clip**: one shot in one place, of any length, with any number of characters, 9:16 or 16:9, with the words the style carries (a narrator's
  voice-over or captions by default). The characters do not speak on screen.
- **Episode**: any number of shots, of any length, with any characters, in one or more places, 9:16 or 16:9 (one ratio for the whole episode). It is several shots or places, or characters who talk in a style whose `words` has `lip-sync` (the default for an episode), and the
  characters may speak.

The mode follows the shape of the request, never its size: a length or a number of characters does not make a clip an episode. Words on cards or captions do not make one either: a style whose `words` puts them there (`captions`, `intertitles`, `sound-words`) is made without a lip-synced voice, and an episode in it carries those words.

Nothing here turns, hugs, claps or hands a prop to another character: reword such a beat or say
"not yet". A character can sit: `motionPreset:sit` seats a side-view character on a seat or bench (`seat` 0.5 to 1, how
far down it settles); only the side view is covered, so reword a sit in another view. A clip
with a second place or a second shot is an episode. Cutting front pieces out of a set picture (cartoon-film §3) is not done here: stage a character clear of what it would stand behind. A pose the skin cannot bend into (a seated skirt, a fist) is reworded on a part-sheet or ready-made rig. A clip has no length or cast limit, and an edit the user asks for is done as asked, such as slowing the ending.
Everything below is for both modes; **Episode** notes mark what only an episode adds.

Before acting on a stage, load the available skills in its row that apply to this job, also when the work resumes there.

character-rigging is read by section, not whole: `references/cartoon-film.md` for the plan and each stage it names below, `references/character-rules.md` for Cast and Review, `references/rig-build.md` for Cast, `rig-place.md` and `rig-controls.md` for Place and Prop, `rig-act.md` for Build the scene (its router table names them).

| Stage | Gate | Skills |
|---|---|---|
| 1. Style | ASK | scene-building-basics, visual-style, visual-styles |
| 1b. The plan | ASK | character-rigging, scene-building-basics |
| 2. Cast | ASK, SPEND, REVIEW | character-rigging |
| 3. Place | SPEND | character-rigging, scene-building-basics |
| 4. Prop | SPEND | character-rigging |
| 5. Build the scene (an episode: each shot) | SPEND | character-rigging, scene-building-basics, voice-over-generation, lip-sync-lines, background-music |
| 5b. Join (episode only) | SPEND | character-rigging, scene-building-basics, background-music |
| 6. Review | REVIEW | character-rigging, motion-review |
| 7. Export | DELIVER | scene-building-basics |

## 1. Style

No plan is written or approved before the film's look is fixed, from whatever the user starts with, as
picsart-video-rules' "A choice made by eye" says:
- **A style named in the request** (by its label or id, or a look the index names) is taken as asked, with no picker.
- **The story is known** (told first, or named together with a style request): read the style index with
  `picsart_scene_recipe` `name: "visual-styles"` (`references/style-index.md`) and open `picsart_scene_picker` with the rows
  whose `use` is `film` (never a `graphic` row) and `selection: "one"`, one tile each with its label, notes and video `previewUrl`, and a `category`: the chip the index's "Category chips each use case shows" NAMES for the row in the animated-story column, else `Other styles` (every card gets one). Mark 4 to 6 cards `recommended`, the best fits for the story (a style the request names goes first, 4 to 6 in all). Order the cards by that table's chip order, `Other styles` cards last (the board orders its chips by first appearance); within a chip, in order of
  how well each fits the story's mood, audience and setting, judged from the row's label and notes. The best match is the
  first tile and the default when the user skips. Story fit decides the order only: every `film` row is offered and nothing
  is left out, however unlikely a style looks for the story (a shadow puppet or manga panels for a bright toddler story
  go last, not away), because a user cannot choose a style they were never shown. The classic cartoon always stays. ASK (with `picsart_ask`, found as picsart-video-rules says, for any closed choice, a multi-select included, so the options are buttons the user taps, the recommended one first; then your host's own question tool, such as AskUserQuestion; only where all fail, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) the
  user to pick ONE. (visual-style holds the styles of videos built on recordings; a cartoon's style is chosen here.)
- **A style asked for first, with no story yet:** the same one-pick picker with every `film` row, the classic cartoon first and the
  default when the user skips. Once the story is told the style stays as picked.

Read the chosen row, which is already in hand, for `words`, `rows`, `cast` and `score`; an empty cell, or an index that has not got
these columns yet, takes the defaults: `words` voice-over or captions for a clip and `lip-sync` for an episode, `rows` shots,
`cast` rig, `score` last. A default never overrides the chosen style's own recipe
(`references/<id>.md`): where it says how its words are carried (cards, captions, no voice), that its characters are drawn
as shapes, or that its music is planned first, the recipe is followed, so a silent style gets no voice or lip-sync. They decide the rest of the flow: `words` how the plan's words reach the viewer (a comma-separated set
of `voice-over`, `lip-sync`, `captions` (which covers speech balloons), `intertitles`, `sound-words`; `none` means no words), `rows` what a row of the plan
is (`shots`, `panels` or `drawing`), `cast` whether stage 2 builds a rig (`rig`), the characters are drawn as shapes
(`shapes`, no rig build; `lip-sync` needs `rig`) or every character is cut from pictures (`pictures`), and `score` whether the music (score) is planned before the shots (`first`)
or laid after the picture (`last`).

**The style's finish is part of the style, built in from the first render, never an add-on.** The chosen recipe names it
(its film-finish look such as `analog_film_finish` grain, the stepped frame rate, the title card and the iris). Apply every
one while the film is built, so the first preview already looks like the style's tile; never offer it later as an
optional extra or wait for the user to ask. A finish the recipe names and the tools cannot apply is reported in the delivery.

**Every scene animation shown to the user opens in `picsart_scene_editor`** (picsart-video-rules, "Every scene animation is reviewed in the editor"): a character test render, each revision and the film's rounds, not only stage 6. A preview video or contact sheet does not
replace it. After the pins are fixed, reopen the editor on the new version and say which pins you addressed.

**An episode is reviewed by round, on the whole film: one card on the joiner per round, never one per shot.** Round 1 is not an editor card: before any spend, show the episode as a plain-text table, one row per shot with its name, its length (its words ÷ 2.3 + 0.4 s) and its lines, and ask OK or what to edit, in plain text, never `picsart_scene_editor`; round 2 has every shot built, silent, with the captions timed; round 3 is the same film with the voice. The user pins or comments anywhere; map each pin's time to the shot that holds it and fix those shots. After each card ask with the question tool and two buttons, **OK** and **I pinned changes**, never end the turn silent. A single shot over about 15 s that is the riskiest may get its own early card.

Follow the chosen style's own recipe (`references/<id>.md`) and `film-flow.md` for the rest: the plain-text shot table
first, every landing re-saves the joiner and posts the fresh link, and the final export refuses while a name card
remains (a name card is only a placeholder for a shot not built yet, never opened for review). Record the style in the film plan and never ask for it again, also when the work resumes.

## 1b. The plan

Choose the mode: a clip is one shot in one place; an episode is several shots or places, or characters who talk with a lip-synced voice. Turn the request into one short paragraph and ASK (with `picsart_ask`, found as picsart-video-rules says, for any closed choice, a multi-select included, so the options are buttons the user taps, the recommended one first; then your host's own question tool, such as AskUserQuestion; only where all fail, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) the user to approve or edit it in one turn, with the style and how its words are carried (from `words`) shown beside it: who (any number of characters), where (a clip: one place), what happens, as a guide in 3 to 5 beats and never a limit, the words the style's `words` carries (narration lines, captions, intertitles or sound words, and no voice line where `words` has none), the palette (the style's own, or the brand's colours keeping the style's one hero colour), the length, and the facts the film must state. In the same ASK (with `picsart_ask`, found as picsart-video-rules says, for any closed choice, a multi-select included, so the options are buttons the user taps, the recommended one first; then your host's own question tool, such as AskUserQuestion; only where all fail, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says), in plain text, suggest the sound with a yes or no for each, never as a separate question: a narrator or character voices, only where the style's `words` carries a voice (`voice-over` or `lip-sync`; a style with none offers no voice), and a music bed under the cut. Each says what it costs, the user is free to say no to either, and no audio is made or paid for without that yes and the credit quote. A beat is
one of: walk in or out, idle, wave, reach, pick up, hold or carry a prop, put it down, jump, jog.
Think and hand-over join the list when `picsart_scene_capabilities` shows them. Read the allowed actions
from `picsart_scene_capabilities`, not from memory: a beat it does not list is reworded or refused.

**Plan before building** (character-rigging `references/cartoon-film.md` §1): every story question that changes a
drawing (who waves to whom, which way they walk) is settled in the same turn.
The plan also names every picture and voice line it needs with its credit cost. Build a face, a pose or a small prop in
the scene first; a generation is proposed only after that attempt visibly fails.

**Episode: the shot list.** Instead of the paragraph's beats, write one row per shot, approved in the
same ASK (with `picsart_ask`, found as picsart-video-rules says, for any closed choice, a multi-select included, so the options are buttons the user taps, the recommended one first; then your host's own question tool, such as AskUserQuestion; only where all fail, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says): place, who is in it, its beats, its lines (speaker and text), its size (wide, medium or close,
as Staging says) and the transition into it (a cut, or one `picsart_scene_capabilities` lists). Cast and places are fixed for
the whole episode; its length is the sum of the shots. One world holds for every shot (cartoon-film §2): the same light,
grade and fades, each character's height from one reference figure, and each voice's first-line settings. A long film is built shot by shot and reviewed by round (stage 1). Where the style's `rows` is `panels` or `drawing`, a row is that unit and not a shot.

## 2. Cast

**Every character is saved once and placed by reference.** Whatever its cast kind, a character is built or drawn once,
saved with `picsart_scene_library_save` (`kind: "character"`, tagged `style:<style id>`), and then placed in every shot by
its `library:` uri (Pick, below), never inlined, so it is the same drawing in every shot. The save steps in the rig paths
below are that rule for a rig; a drawn character follows it too.

A style whose `cast` is `shapes` builds no rig: its characters are drawn as that style's recipe says, and this stage places and checks them, never rigging them. A style whose `cast` is `pictures` casts every character **From one picture** (below): the pose list per beat comes first, then each base picture, its sheets and plot poses as character-rigging's `references/picture-sheets.md` lays out; it never offers a part sheet or the ready-made cast. Only a `rig` cast is built, as below.

**A shapes character.** Before drawing it, fetch the recipe's character section: `picsart_scene_recipe` with
`name: "visual-styles"` and the style's reference (`references/<id>.md`), and read its proportions, shape vocabulary,
face and controls. Draw the character to them, save it as above, and before any shot build a look review: open it in
`picsart_scene_editor` posed as the recipe shows, as the rig path's test render is, and ASK (with `picsart_ask`, found as picsart-video-rules says, for any closed choice, a multi-select included, so the options are buttons the user taps, the recommended one first; then your host's own question tool, such as AskUserQuestion; only where all fail, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) the user to approve
the look or say what to change. No shot is built before they approve it.

**Only when the plan has a character** (a story of scenery or objects has no cast step, board or lookup). One character at a time. **Episode:** each character is cast once and reused in every shot, placed by its
`library:` uri as below and never inlined, so it is the same drawing in every shot. The pick is the cast board, `picsart_asset_choose_characters`: one card per character, never one per view, and never
`picsart_scene_picker`. The board lists the user's saved characters itself, as the first cards of every character's Ready-made tab, each with its
picture and its style tag, a scene-library rig and a saved portrait alike, so look nothing up first: a lookup draws nothing
(picsart-video-rules, "A lookup draws nothing"), and `picsart_scene_library_list` opens the Drive browser, so it is
called only when the user asks to browse. **If the board shows no saved character, never say "pick from your characters"**: the ready-made
cast and the new-character options are what it offers, as for a new user. With saved ones on it, those stay offered too.
The answer's `choice: "saved"` names the card: with a `libraryId` it is ready to use (`library:<libraryId>`); with only an `assetId`
(a portrait or turnaround, no rig) it has no `library:` id, so it is "make a cartoon of your saved character": the build step below
runs with that picture as the reference, then the in-action review, then a save to the scene library, and never straight to Pick.
**A saved character carries the style it was drawn in, as the tag `style:<style id>`** (the id of the chosen style's row in
the style index), which the board shows on the card. Never pick a character for the user, and never leave a saved one out. If the user takes a
character from another style or of unknown style, say once that it will not match the film's style and offer to draw it
again in this style; then do what they choose. The board asks which:
a saved or ready-made one,
a new one described in their words,
or one built from a part sheet they drew.
Or one cut from a single finished picture of the character, or a Spine rig they bring.

A character built here must pass character-rigging's `references/character-rules.md`: plan its poses and its cover map
(§4 and §5) before its sheet is drawn, so every covered part is drawn whole on the sheet.

**Pick.** A saved character is a scene in the library, placed by reference so a second scene with the same
character is identical: `picsart_scene_apply_template` with `uri: "library:<libraryId>"` (no `mode`) returns a
`scene_ref` snippet, and `picsart_scene_patch` adds it as a layer: an `add` op with `kind: "layer"` and
`value` `{ id, start, duration, content: <the snippet> }`. The reply may also carry a `transform` (`scale: [-1, 1]` for a character stored facing the other way): put it on that outer layer, or the character faces the wrong way and shots staged face to face break. Do not inline the character. A ready-made one
comes from `picsart_scene_templates` the same way, with the template's `uri`.
Actions are applied later, to the placed character, with `picsart_scene_apply_preset`.

**Describe.** Follow character-rigging's "From a picture" and its part-sheet prompt:
1. Quote ONE turnaround sheet with `picsart_preflight`, then SPEND (quote it in one line, then get the yes with `picsart_ask`, found as picsart-video-rules says, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", else your host's own question tool, such as AskUserQuestion; never as a typed question unless both fail; only then those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says). Draw it with ONE
   `picsart_generate` call, `count: 1`, with the part-sheet prompt and the user's description, and the
   child's or user's reference image when they sent one. That sheet is the character: build it, save it,
   and reuse it in every scene. Never draw a second near-duplicate sheet of the same prompt to pick from.
   Offer a choice only when the user asks for one: each candidate then has its own prompt, differing in
   style or silhouette (one `picsart_generate` call per candidate), never `count: 2` on one prompt.
   A sheet takes four minutes or more, so say so in the same turn the receipt comes back: "Drawing the
   sheet, about four minutes; I'll check in." Then follow the receipt with `picsart_job_status`, the
   longest `waitSeconds`, and tell the user in a sentence each time something changes (done, a failure
   and what you do next). Never wait silently. A failed sheet is retried once.
2. Build the rig at once, with no approval of the sheet: the sheet was paid for in step 1, and the user judges the character in the in-action review (step 3), never the flat sheet. Use `picsart_scene_build_model`, `character: { svgUrl }` (and `view`), `svgUrl` being the
   chosen sheet's `url` from the generation result: Picsart fetches it, so never paste the SVG into the
   call. Run it with `check: true` first and read `pictureCheck`: a failed named check is a sheet problem,
   fixed by a surgical change to the sheet, never by building anyway. `pictureCheck` is an internal gate and is not shown to the user.
3. Build the other two views of the same sheet too (`picsart_scene_build_model` with `view` `"front"`,
   `"threeQuarter"` and `"side"`, one call each) and open the one in-action review below (front, side, three-quarter): one editor opening, no separate
   picture step or sheet approval before it. That review is where the user approves the character or asks for changes. A change goes back as a surgical edit to the sheet, then a rebuild; a new sheet is quoted on its own. The user accepts it or retries once.
4. After two failed builds, stop. Tell the user, in a sentence, what failed and why, and offer the
   ready-made characters as their choice. Never fall back to one silently, and never build a third
   time.
5. Save every described character with `picsart_scene_library_save`: `kind: "character"`, the build's
   `sceneUrl`, the sheet in `referenceImages`, the description in `prompt`, a portrait in `previewUrl`. Add the tag `style:<id>` to `tags` (`<id>` the chosen style's id from the style index), so the library records the style it was drawn in.
   It is reused from the library, never generated again.

**From one picture.** Follow character-rigging's `references/cut-from-one-picture.md`, and read its "The first call" before the first `picsart_scene_cut_parts` call (a set piece cut from the set picture too):
1. The picture is the user's own, received with `picsart_drive_upload_ask` (`accept: 'image'`), or one drawn to that
   reference's Input spec in the film's chosen style (its recipe says how its characters look): quote it with
   `picsart_preflight`, then SPEND (quote it in one line, then get the yes with `picsart_ask`, found as picsart-video-rules says, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", else your host's own question tool, such as AskUserQuestion; never as a typed question unless both fail; only then those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says), and draw it with `picsart_generate`. The user's own picture is cut as it came.
   The cut parts are pictures, so the character's look comes from the picture: the style's treatments of a whole
   layer (stepping on twos, a shadow, a look) apply to it, and the ones that redraw a path (an outline stroke,
   `line_boil`, a line drawn on) do not.
   The cut tool cuts along a continuous dark outline, or a light rim with `labels.regions.edge: "light"`. In a
   style whose `cast` is `pictures`, a picture with any other edge is cut by hand (character-rigging's
   `references/cut-any-edge.md`); in any other style, say it cannot be cut and offer the other cast options.
2. Call `picsart_scene_cut_parts` with `seedMap: "base"` first and read the seeds off its numbered picture,
   then cut. Cut a side or three-quarter view: a front view's sleeves and elbows do not hold yet, so a
   front-facing character is cast from a part sheet or a ready-made one. A side-view character that walks is
   cut from aligned sheets with `rig: "humanoid-side"`; a pose the skin cannot bend into (a seated skirt, a
   fist) is drawn and passed in `poses`. Fix a named refusal by the input it names. A cut from the picture
   alone must give `check` 0 and 0. A cut from sheets differs from the picture wherever a sheet redraws a
   part, so look at `check.overlay` instead: the marked pixels must lie only on parts a sheet redrew.
3. Look at the reference's Gate poses on one `picsart_scene_contact_sheet`, then place the `sceneUrl` in the
   review scene and run the in-action review below on the view that was cut (one view, labelled): every part present and
   attached, no hole at a joint, feet on the floor. The user accepts it or
   retries once; after two failed cuts, stop and say what failed, as for a sheet.
4. Save the accepted character with `picsart_scene_library_save`: `kind: "character"`, `scene` its
   `sceneUrl`, the picture in `referenceImages`. Add the tag `style:<id>` to `tags` (`<id>` the chosen style's id from the style index), so the library records the style it was drawn in. It is reused from the library, never cut again.

**The in-action review.** Once the rig is built, the user reviews the character in action in ONE `picsart_scene_editor` opening, never
in a still picture first and then an actions test. The scene holds the views the build has, front, three-quarter and side, one after
another or side by side, whichever reads at 1x on a phone; each view is labelled with its name (a text layer: "Front",
"Three-quarter", "Side") and plays the same short action set, a walk, a wave and a talk beat
(`picsart_scene_apply_preset`: `motionPreset:walk_cycle`, then the `wave` and `talk_beat` gestures). The front view has no walk:
it plays idle, the wave and the talk beat, and the answer says so in one line; never fake a front walk, a mirrored front or a squashed
one, and say which view is missing when one is. The review is for comments only: ask for no editing, effects or dragging, open it with
`comments: "all"` and tell the user in one line that this view is for comments and edits made in it are not used. Apply the comments
as changes to the sheet or the build, and save only after the user accepts.

**A dog or cat.** Build it with `picsart_scene_build_model` `character: {animal: {species: "cat"}}` (`dog` or `cat`; the shape dials and `look` are optional):
a four-legged rig, side view only, actions `idle` and `walk`, no sheet and no spend. It covers only a dog and a cat. Any other four-legged animal (a horse, a fox, a cow) goes the custom part-sheet path: a side-view SVG sheet of named parts built with `character.family: "quadruped"`, as character-rigging's rig-build reference lays out; a biped sheet comes out upright. There is no quadruped template.

**A Spine rig.** The user brings the export of a rig made in Spine: the skeleton `.json` (a binary `.skel` is refused: ask for the JSON export), its `.atlas` and the PNG pages, or one `.zip` of them. Receive the files with `picsart_drive_upload_ask` (one `.zip` is simplest), then call `picsart_scene_import_spine` with `archiveUrl`, or with `skeletonUrl`, `atlasUrl` and `pages` (each page file name as the atlas lists it, to its URL). It spends nothing and returns `sceneUrl` (the editable rig, its animations as actions), `playbackUrl` (the rig playing its default action) and a `report`. Tell the user in plain words which animations the report left out and what it approximated. Open `playbackUrl` in `picsart_scene_editor` and REVIEW it by eye: every part present, attached and in the right front-to-back order, then play the animation they named. A refusal names the thing to fix (an unsupported attachment or constraint, a page that does not match its atlas): pass it on and ask for a fixed export, never retry unchanged. A Spine rig plays its own animations, not the standard walk and gestures: animate it with the action names the import lists. Save the accepted rig with `picsart_scene_library_save` (`kind: "character"`, tag `style:<id>`) so it is placed by its `library:` uri; if the save refuses a rig with no shape layer or standard control, place it by its `sceneUrl`.

**Their own sheet.** The user sends one SVG drawn to character-rigging's part-sheet layout, received with
`picsart_drive_upload_ask` (`accept: 'image'`). Run `picsart_scene_build_model` with `character: {svg, check: true}` first and
read `pictureCheck`: a failed named check is fixed on the drawing by the user, never by building anyway.
Build the view with `character: {svg, view}` (each view the sheet draws), then run the in-action review below: every part present and attached, the far hand
there, feet on the floor. Save the accepted character with `picsart_scene_library_save`,
`kind: "character"`, so it is reused from the library. Add the tag `style:<id>` to `tags` (`<id>` the chosen style's id from the style index), so the library records the style it was drawn in.

## 3. Place

The background follows the chosen style's recipe. For any anime style that is the SVG band layout (a 2D place, below) and then one paint-over that keeps it, as painted-anime.md lays out, never a free text-to-image plate. Otherwise it is one of:
- a generated background plate, for a style whose recipe does not say otherwise, in the cartoon's ratio, one image: quote it with `picsart_preflight`, then SPEND (quote it in one line, then get the yes with `picsart_ask`, found as picsart-video-rules says, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", else your host's own question tool, such as AskUserQuestion; never as a typed question unless both fail; only then those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says),
  generate it with `picsart_generate` and declare it as an asset;
- a plain or gradient background from the capabilities;
- the user's own picture in the cartoon's ratio, received with `picsart_drive_upload_ask` (`accept: 'image'`) and declared as an asset;
- a 2D place drawn as one SVG of depth bands, built with `picsart_scene_build_place`, saved with `picsart_scene_library_save`, and started from for each shot.

A set is one picture, never generated in layers (cartoon-film §3). Set the floor line where the characters stand, and say where it is.

## 4. Prop

Only when a beat needs one, and one prop per character, one of:
- a small generated image: quote it, then SPEND (quote it in one line, then get the yes with `picsart_ask`, found as picsart-video-rules says, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", else your host's own question tool, such as AskUserQuestion; never as a typed question unless both fail; only then those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says), generate it, remove its background with
  `picsart_image_remove_bg`, and check its alpha edges;
- a shape;
- the user's own picture with a transparent background (PNG or SVG), received with
  `picsart_drive_upload_ask` (`accept: 'image'`); check its alpha edges.

Check its size against the characters before placing it (cartoon-film §3). It is held by the hand socket, by the mouth for the dog,
or worn on the head (`heldBy: "head"`) by a character built from a part sheet: read how from character-rigging's held props. A prop that is not held by a socket is not a prop.

## 5. Build the scene

Presets first, through `picsart_scene_apply_preset` and `picsart_scene_patch`: the walk, wave,
reach, hold and carry, jump, jog, idle, with the camera fixed for each shot and one view per beat. What no preset gives follows **Motion, in this order**.
Place each character's scene with `fit: none` on the floor line.
A prop that falls, is dropped, lands or plops uses `picsart_scene_apply_preset` `toss`. A held prop takes `holder` and `holderSocket`; a whole character takes `bounces: 0` and `footY`, the px from its position down to its feet. Never stack `squash` on a layer `toss` drives. The narration is one of (only the words the style's `words` names are made: with no `voice-over` or `lip-sync` in it, no voice is generated or spent):
- a generated voice: write the narration lines now, but make the voice only after the user accepts the first render
  (**Order**, below): then quote it with `picsart_preflight`, SPEND (quote it in one line, then get the yes with `picsart_ask`, found as picsart-video-rules says, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", else your host's own question tool, such as AskUserQuestion; never as a typed question unless both fail; only then those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says), and generate it as voice-over-generation says;
- the user's own recording, received with `picsart_drive_upload_ask` (`accept: 'audio'`) and transcribed with
  `picsart_media_transcribe` for its timing (pass `text` when you have the script);
- the lines as captions, with no voice.

A child character's lines take a child's voice, cast as voice-over-generation says; say which voice was picked.
**Order: the picture first, the voice after.** Time the shots silent, from estimated line lengths: each line takes its
words ÷ 2.3 + 0.4 s. Show the lines in the plain-text shot table, and as captions in the first render, so the user judges the motion and the words together.
Generate the voice and apply the lip-sync only after the user accepts that first render. When the real line lengths
arrive, the slot grows to fit and you say so; a line is never cut to fit the slot. A recorded voice the user already
sent is real from the start: use its lengths at once.

**Voice fit.** Once the lines exist (generated, recorded or captions with a spoken pace), probe each line's real
duration with `picsart_media_probe` (a line carried only as a caption has no audio: time it by its caption display duration, the longer of its on-screen time and a reading pace of about 3 words a second) and set the clip's length from them: first line at 0.3 s, each next line after
the previous one's end plus a pause of 0.3 to 0.6 s, the ending hold 1 s or less. When the lines total less than the
length the user approved, say so and either shorten the clip to the voice or add beats (and more words, only with the
user's yes) so that actions and lines spread over the whole length. Never leave more than 1 s of silence with nothing
happening at the end, and never cut a line off. Start each line within 0.3 seconds of the beat it describes. A style whose `score` is `first` plans its beat table before any shot, and the rest lay sound after the picture is locked. Background music is optional:
when the user wants some, choose it as background-music says and duck it under the voice;
music the user sends, received with `picsart_drive_upload_ask` (`accept: 'audio'`), goes on an audio layer under any voice.
**Rig abilities, one call each** (`picsart_scene_apply_preset`, `layerId` the rig layer):
- A jump moves the layer in stage px: `{"preset":"jump","layerId":"kid","params":{"start":1,"height":40,"landX":200,"landY":-60}}` (`landY` -60 onto a 60 px stool,
  +60 off it); the result's `phases` (`takeoff`, `top`, `landing`) are the seconds to key sounds to.
- A walk's `distance` and `stride` are rig px, not stage px: the layer moves `distance` x its scale x its fit, so pass S / (scale x fit) for S stage px.
  `{"preset":"walk_cycle","layerId":"kid","params":{"distance":960,"from":"rest","start":1}}`. Before `start` the layer holds the
  walk's first pose; the default `from` `walking` is mid-stride, so a character who stands, then walks, takes `from` `rest`.
- A held prop sits under the whole near arm and under the head, so a jar hugged at the chest is behind the arm: `{"heldBy":"right","rightHandToHeld":1}` in the rig layer's `content.parameters`.
- The near arm draws in front of the head where it would meet it; a full overhead raise lifts the shoulder and stretches the arm so the paw clears the head:
  key `rightUpperArmRaise` 0 to 1. Nothing else to author.
- `picsart_scene_lint_layout` reads the result: `armUnderHead` (a near arm overlapping its head while painted below it), `armThroughHead` (a paw inside the head;
  `clearsAt` is the dial to stay under), `mouthCovered` (a mouth under its own arm, hand or prop). Fix the finding, never the lint.

Give every layer that starts after 0 `timeMode: "layer"`, so its keys count from its own start (cartoon-film §5).
Check the scene with `picsart_scene_validate` and the capabilities' own limits.

**Episode: shots.** Build each shot as its own scene, at its own length, staged as Staging says, with
`returnSceneUrl: true` so it has its own `sceneUrl`: one document per scene, joined only at the end (cartoon-film §6). Characters are placed by their `library:` uri, never inlined.

**Episode: dialogue.** Each character has one voice, and the user is told which voice each character got.
Once the user accepts the first render (Order above), cast each voice as voice-over-generation says, and generate each line in its speaker's voice.
Lip-sync each speaker's lines as lip-sync-lines says, after the voice exists. Each line's audio layer starts at its cue and lasts its own probed length (from the voice result or `picsart_media_probe`), never the film's length, so `picsart_scene_validate` shows no `media_window_exceeds_source`.

### Motion, in this order

Take a motion at the first step that gives it:
1. **A preset, by intent.** `picsart_scene_capabilities` with `sections: ["motionPresetList"]` lists every preset with its category, tags and parameter names (add `tag:<name>` to narrow it); the table below is the slapstick starting point.
2. **A live `expression`** on the property, for anything that repeats, decays, orbits or follows another layer: `"animations": {"rotation": {"expression": "return 12*math.exp(-6*time)*math.cos(18*time)"}}`. A vec2 property (position, scale) returns `Vec.v2(x, y)`, never `{x, y}`.
3. **A few eased keys through `picsart_scene_patch` `animate`**, for a one-off pose or path: `{"op":"animate","layer":"lid","property":"rotation","keys":[[0,0],[0.5,-25,"ease_out"],[0.9,0]]}`; an easing shapes the move from its key to the next, so the last key takes none.
4. **Never keys sampled from a formula.** Evenly spaced keys on one track are a formula: a sine typed as eleven keys is an `expression`, a bounce typed as thirty is a preset or an `expression`. A helper in your own script that turns a formula into keys is the same thing; a script may compute places, preset parameters and expression text, and nothing else.

The same keys twice are `copyAnimation`; the same layer several times (three stars, five jars) is `$each`, one definition over a list (`{ "$each": "stars", "as": "s", "body": { ... "$eval": "s.@index * 0.3" ... } }`) in a template resolved with `picsart_scene_apply_template` `mode: "bootstrap"`; the tools refuse a stray `$each` by name.

| The motion wanted | Use |
|---|---|
| a wobble that dies, an overshoot after a hit | `motionPreset:settle`; `motionPreset:spring` for an entrance that overshoots and bounces |
| a rattle, a shiver | `motionPreset:shake` |
| breath, a float, a sway | `motionPreset:breathe`, `float`, `sway`; `cycle` on a rig control |
| a blink, a twitch at random moments | `motionPreset:random_pulse` (it drives a parameter) |
| a landing, a squash on impact | `motionPreset:squash` |
| tail, ears, hair, a limb trailing the body | `motionPreset:follow_through` (a parameter or a layer) or `wiggle` |
| a prop that falls, is dropped, lands or plops; a thrown prop | `motionPreset:toss` (it squashes on contact itself) |
| circling stars, birds, a halo | `motionPreset:orbit_around`, once per star with its `index` |

**Land on a socket, not on arithmetic.** A prop that lands on, sits on or is held by a character targets one of its sockets (`{"layer": "kid", "socket": "head"}`; character-rigging's sockets and held props). `picsart_scene_query_layout` boxes check the result; they are never the target.

**A prop is drawn once, as SVG.** Import the whole drawing with `picsart_scene_import_svg_path` (`svg`, the markup), save the scene with `picsart_scene_library_save` (`kind: "template"`), and place it by reference like a character. Never type a prop as shape items.

**Check a value before it is written.** A point on a rotated or parented layer (a lid on a tilted rack), a wobble, positions on an orbit, rig px against stage px, the times to key a sound: `picsart_scene_evaluate_expressions` gives what the expression returns at the times you list, without writing the scene (the recipe on computing values; find it in the `picsart_scene_recipe` index). Then write the same text as the live `expression`, never baked keys, and verify with `picsart_scene_query_layout` at the same times.

### Beats: motion and order

- **Every beat moves.** In every beat the character visibly moves (an action or an idle with life in it), and the camera
  or the background moves too where the beat calls for it. Nothing on screen holds still for longer than about 1.5 s
  unless the plan says that beat is a hold; the opening and the ending are beats too, so the first and the last seconds
  move like the rest. The wait before the voice-over's first line counts: a stretch where the character, the camera and
  the background all hold still is a still stretch even when it is only the lead-in, so give that wait an idle or a
  camera drift from t=0, never a held frame.
- **Story order.** A prop starts where the story puts it (a kite that is picked up lies on the ground until the hand
  takes it), and nothing the story introduces later (a kite in the air, its string, a second character) is visible
  before its beat: it enters on its beat, with `start` at that time, never at 0 and hidden by opacity.
- **A run across a place moves the place.** A walk, jog or run across a place moves the background in depth: at least
  three layers (far, middle, near) moving at different speeds, the near one fastest. A background that stays put under a
  moving character reads as a walk in place.

A fade of a prop or any layer is keyed in `animations.opacity`, never `transform.opacity` (one constant value):
`"animations": {"opacity": {"keyframes": [{"time": 4, "value": 1}, {"time": 4.5, "value": 0}]}}`; the same fade is the
`animate` pair `{"op":"animate","layer":"stick","property":"opacity","keys":[[4,1],[4.5,0]]}`. To add one key to a
track that exists, add to the `keyframes` array (`"path":"animations/opacity/keyframes"`), never to `…/keyframes/0`.

Check it with `picsart_scene_check_motion` per beat, as the self-check before export says, before the editor review.
A foot's travel over a window is one `value_range` check on the rig's `foot` parts, with the `window` it reads, for
example `{"version":1,"timeSpace":"root","fps":10,"window":{"start":0,"end":6},"checks":[{"id":"feet","target":{"rig":"fox","parts":["foot"]},"kind":"value_range","channel":"centerY","min":-400,"max":400}]}`;
for a foot or hand that must keep moving use `kind: "must_move"` with `min`, `within` and its own `window`.

### Staging

Staging follows character-rigging `references/cartoon-film.md` §4 for the beats allowed here: two figures that touch
stand on one floor line, an empty parent is never faded (fade its leaves), and a moved point changes only that point.

Before building, list one shot per beat, each with its size:
- **wide**: the establishing shot, the opening beat only;
- **medium**: the characters are at least 35% of the frame height, for action and dialogue;
- **close**: head and shoulders, the face at least 15% of the frame width, for the emotional beat.

A story has at least 3 shots, and its emotional beat is a close. Change the framing with the camera: the `push_in`
preset (`zoom` is the scale it ends at) for a move in, or a cut, the camera keys on the same frame, for a new shot. A move
eases and never snaps in the middle of a beat.

Two characters who talk or react to each other face each other, both in the three-quarter view, never both side-on.
Nothing important is cut by the frame edge: never a face; feet leave the frame only in a close. A prop that changes state
(a tower that falls, a cup that fills) crossfades over at least 6 frames; it never swaps in one.

## 5b. Join (episode only)

Join the shots as character-rigging's "Films are scenes of scenes" says: no joiner tool. Build a root scene with
one `scene` asset per shot (`uri` the shot's `sceneUrl`) and a `track` of clips in shot-list order, each clip's
duration its shot's. Put the shot list's transitions on the clips. Captions, if any, go over the root, and
background music goes on the root under every voice.

A caption never sits on a character or a prop. Before placing one, read the figures' extent in that shot (a rig's
`anchor.bounds` from `picsart_scene_build_model`, or `picsart_scene_query_layout` with `ids` naming the rig layer and
the prop), then put the caption in the band they leave free: `verticalAlign: "top"` when they stand low in the
frame, the bottom when they stand high, with a `margin` that clears the tallest figure at the caption's time. A shot
that fills both bands gets its caption at the side the figures leave, or only while they hold still. Look at a
contact sheet at each caption's time and move any caption that covers a face, a hand or a prop.
Choose and duck it as background-music says.
Validate the root with `picsart_scene_validate`.

## 6. Review

**Episode:** check each shot yourself first (below), then the root; the user's reviews are the rounds of stage 1.

Render the busiest beat for 3 to 5 seconds first, then the whole clip, and look at every beat of it,
not one still. Review it as motion-review says, with the review loop of cartoon-film §7 (stills at the extreme moments
on one contact sheet, sent to the user) and, for a character built here, character-rules' Check. The checks that matter:
- no torn, floating or missing part in any frame, and the far hand never vanishes in a walk;
- planted feet do not slip, the walk starts and stops cleanly, and the character stays on the floor line;
- a wave keeps the hand beside or above the head, never over the face;
- a held prop stays at its socket in every frame, and is picked up and put down without a jump.

**Self-check before export (required; export does not start without it).** The check is run by tools over the
whole window, from 0 to the composition `duration`, never over one beat and never from memory. Do these in order, and name the
results in your reply to the user before any export call: (1) `picsart_scene_contact_sheet` at about 2 frames a
second over the whole clip, looked at and sent to the user; (2) `picsart_scene_check_motion` at 10 fps over the whole
window (one call up to 100 s; a longer clip in consecutive bounded windows, each under the tool's 1000-frame limit, that together cover 0 to `duration`) on each character's foot and hand part layers and on the layer of any held prop, and `picsart_scene_lint_layout` at a frame in each beat;
(3) every point, reach and hand-over: `picsart_scene_query_layout` at the beat's time and compare the hand with its target
(a point that misses its target by more than a hand's width is a failure); (4) the voice-fit check below; (5) the beat check of Beats: motion and order, one `picsart_scene_check_motion` per beat on the character, on the background layers and on any prop, and the first appearance of each layer against its beat. A clip that was not
watched end to end by this check is not exported, and you never tell the user you have not watched it: run the check
first. Fix each failure through its own path and render again, before any export:
- no stretch longer than 1 s where the characters, their hands and their feet all hold still (`observedMin` and
  `observedMax` flat over that stretch in `picsart_scene_check_motion`), except the ending hold: add a beat or an idle,
  or shorten the clip (Voice fit);
- a prop's string, tail or strap never crosses a character's face or head unless the story says so (sheet): move the
  prop's socket or hold it in the other hand;
- legs cycle while a character moves, and nothing freezes for over 1 s except the end hold: also run
  `picsart_scene_check_motion` at 10 fps on a foot's and a hand's part layer (`<id>__leftFootArt`,
  `<id>__rightHandArt`, ids from `picsart_scene_query_layout`) and read `observedMin`/`observedMax`: a foot that
  never moves up and down, or a hand flat for seconds, lost its preset bindings, so reapply `acting` (or
  `walk_cycle`) and merge new keys into `content.parameters`, never replace it;
- a held prop sits in the palm and is layered right (no tool checks this; look at the sheet): hold it in the near
  hand, `heldBy` the near side (`right` on a rig as drawn);
- no torn or missing part, and nothing cut by the frame edge (sheet; `picsart_scene_lint_layout` only lists a
  layer mostly off canvas): move the layer's `transform.position`;
- characters and props do not overlap each other (sheet; `picsart_scene_lint_layout` compares whole frames and
  flags a pair that does not touch): move the layer's `transform.position`;
- whatever stands nearer paints in front: for each beat where layers overlap, write a contract asserting
  `{"kind": "order", "axis": "paint", "follows": "bottom", "members": [...]}`, run `picsart_scene_check_contracts`
  and read `groundPaintOrder` in `picsart_scene_lint_layout`; on a failure, move the nearer layer after the other
  in `layers`;
- the ending hold is 1 s or less (`picsart_scene_check_motion` shows when the last part stops): shorten the
  composition and layer `duration`;
- the voice-over starts on its beat: move the audio layer's `start`;
- voice fit: the scheduled end of the last line (its start, which already counts the lead and every gap, plus its probed duration) is within 1 s of the composition's end minus the ending hold: shorten or fill as Voice fit says.

**Episode: continuity.** On the root, render one contact sheet with `picsart_scene_contact_sheet` across each shot
boundary and look: each character the same size and look on both sides of a cut, and screen direction kept
(who walked out right walks in from the left). A mouth that does not move on its line: lip-sync-lines.

REVIEW the preview with the user: open the scene in `picsart_scene_editor` (picsart-video-rules, REVIEW) and end
the turn. The contact sheets above are your check and are not the review. They tweak timing, positions and
colours there or in `picsart_scene_tune`, or ask in words. Nothing is exported until they approve the scene
you opened, unless they said in words to skip the review.

## 7. Export

Only after the editor review in stage 6 is approved (or skipped at the user's word; where the host cannot draw the editor, its fallback review on a draft preview export stands in): the final `picsart_scene_export`, 1080 by 1920 (16:9: 1920 by 1080) at 30 fps (an episode: the root scene). DELIVER the `downloadUrl`, naming each check that failed its bar and each shortfall you saw in the frames (a point that stops short of its target, a finish not applied) before any praise, and never saying the brief was met when you saw it was not, and for each character whether it was loaded from the library or newly drawn (DELIVER in picsart-video-rules), naming any character whose style is not the film's (or is unknown) as a style mismatch. Offer to save the scene to
the library as kind `story` with `picsart_scene_library_save`, and do it only on a yes. Say where each
described
character is kept.
