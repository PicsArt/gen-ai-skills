---
name: make-cartoon
description: Make a short cartoon with a character the user picks or describes - a clip (one 9:16 video of 8 to 20 seconds, one or two characters in one place, who walk in, wave, reach, hold or carry a prop, with a narrator's voice-over or captions), or an episode (any number of shots, any length, any characters, in one or more places, 9:16 or 16:9, who talk, lip-synced, with the shots joined into one video). A character is picked from the ready-made cast or the user's saved library, or built from a part sheet into an editable cut-out rig and checked on a short test render, then saved for reuse. Use when the user wants a cartoon, an animated character or a mascot clip, a kids' story beat, a short scene with their character, or a cartoon with several scenes where the characters talk. Not for a character's sheet with no scene, nor for a live-action or generated-video drama, nor for motion on a design (animate-design).
metadata:
  uses: character-rigging, scene-building-basics, voice-over-generation, background-music, motion-review
  optional: voice-over-generation, background-music
  title: Make a cartoon
  short-description: Cast a character and make a short animated scene
  argument-hint: '[who is in it and what happens]'
  starter-prompt: Make me a short cartoon with a character.
argument-hint: '[who is in it and what happens]'
---

# Make a cartoon

When you read `picsart_scene_capabilities` or the recipe index (`picsart_scene_recipe` without `name`), pass `useCase: "make-cartoon"`: the answer leads with what this job reads and names the rest in one line.

Read picsart-video-rules first. Two modes, chosen in stage 1:
- **Clip**: one short cartoon, 9:16, 8 to 20 seconds, one or two characters, one place, with a narrator's
  voice-over or captions. The characters do not speak on screen.
- **Episode**: any number of shots, of any length, with any characters, in one or more places, 9:16 or 16:9 (one ratio for the whole episode), and the
  characters may speak.

Nothing here turns, hugs, claps or hands a prop to another character: reword such a beat or say
"not yet". A character can sit: `motionPreset:sit` seats a side-view character on a seat or bench (`seat` 0.5 to 1, how
far down it settles); only the side view is covered, so reword a sit in another view. A clip
with more than two characters, a second place or more than 20 seconds is an episode. A clip's limits are for planning it, and never cap an edit the user asks for: an edit that
lengthens the clip, such as slowing the ending, is done as asked. If it pushes the clip past 20 seconds, say so once and do it anyway.
Everything below is for both modes; **Episode** notes mark what only an episode adds.

Before acting on a stage, load the available skills in its row that apply to this job, also when the work resumes there.

character-rigging is read by section, not whole: `references/rig-build.md` for Cast, `rig-place.md` and `rig-controls.md` for Place and Prop, `rig-act.md` for Build the scene (its router table names them).

| Stage | Gate | Skills |
|---|---|---|
| 1. The plan | ASK | scene-building-basics |
| 2. Cast | ASK, SPEND, REVIEW | character-rigging |
| 3. Place | SPEND | scene-building-basics |
| 4. Prop | SPEND | character-rigging |
| 5. Build the scene (an episode: each shot) | SPEND | character-rigging, scene-building-basics, voice-over-generation, background-music |
| 5b. Join (episode only) | SPEND | character-rigging, scene-building-basics, background-music |
| 6. Review | REVIEW | motion-review |
| 7. Export | DELIVER | scene-building-basics |

## 1. The plan

Choose the mode: a clip, or an episode when the request has several places, more than 20 seconds, three
characters, or characters who talk. Turn the request into one short paragraph and ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) the user to approve or edit it in one turn: who (a clip: one
or two characters; an episode: as many as the story needs), where (a clip: one place), what happens in 3 to 5 beats, and the narration or caption lines. A beat is
one of: walk in or out, idle, wave, reach, pick up, hold or carry a prop, put it down, jump, jog.
Think and hand-over join the list when `picsart_scene_capabilities` shows them. Read the allowed actions
from `picsart_scene_capabilities`, not from memory: a beat it does not list is reworded or refused.

**Episode: the shot list.** Instead of the paragraph's beats, write one row per shot, approved in the
same ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says): place, who is in it, its beats, its lines (speaker and text), its size (wide, medium or close,
as Staging says) and the transition into it (a cut, or one `picsart_scene_capabilities` lists). Cast and places are fixed for
the whole episode; its length is the sum of the shots. A long film is built shot by shot, each shot reviewed before the next.

## 2. Cast

One character at a time. **Episode:** each character is cast once and reused in every shot, placed by its
`library:` uri as below and never inlined, so it is the same drawing in every shot. Look in the user's saved library first with `picsart_scene_library_list`
(`kind: "character"`; each row gives `parameterCount`, and `detail: "full"` with `name` returns that one
character's controls), and offer the ready-made cast from `picsart_scene_capabilities`. ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) which:
a saved or ready-made one,
a new one described in their words,
or one built from a part sheet they drew.

**Pick.** A saved character is a scene in the library, placed by reference so a second scene with the same
character is identical: `picsart_scene_apply_template` with `uri: "library:<libraryId>"` (no `mode`) returns a
`scene_ref` snippet, and `picsart_scene_patch` adds it as a layer: an `add` op with `kind: "layer"` and
`value` `{ id, start, duration, content: <the snippet> }`. Do not inline the character. A ready-made one
comes from `picsart_scene_templates` the same way, with the template's `uri`.
Actions are applied later, to the placed character, with `picsart_scene_apply_preset`.

**Describe.** Follow character-rigging's "From a picture" and its part-sheet prompt:
1. Quote ONE turnaround sheet with `picsart_preflight`, then SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says). Draw it with ONE
   `picsart_generate` call, `count: 1`, with the part-sheet prompt and the user's description, and the
   child's or user's reference image when they sent one. That sheet is the character: build it, save it,
   and reuse it in every scene. Never draw a second near-duplicate sheet of the same prompt to pick from.
   Offer a choice only when the user asks for one: each candidate then has its own prompt, differing in
   style or silhouette (one `picsart_generate` call per candidate), never `count: 2` on one prompt.
   A sheet takes four minutes or more, so say so in the same turn the receipt comes back: "Drawing the
   sheet, about four minutes; I'll check in." Then follow the receipt with `picsart_job_status`, the
   longest `waitSeconds`, and tell the user in a sentence each time something changes (done, a failure
   and what you do next). Never wait silently. A failed sheet is retried once.
2. ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) to approve the sheet, with `picsart_asset_approve`; a change is surgical, a new sheet is
   quoted on its own.
3. Build the rig with `picsart_scene_build_model`, `character: { svgUrl }` (and `view`), `svgUrl` being the
   chosen sheet's `url` from the generation result: the server fetches it, so never paste the SVG into the
   call. Run it with `check: true` first and read `pictureCheck`: a failed named check is a sheet problem,
   fixed by a surgical change to the sheet, never by building anyway.
4. Place the built scene in a 3-second test scene (rest, then walk) and render it with
   `picsart_scene_export`. REVIEW that render by eye: every part present and attached, the far hand
   there, feet on the floor. The user accepts it or retries once.
5. After two failed builds, stop. Tell the user, in a sentence, what failed and why, and offer the
   ready-made characters as their choice. Never fall back to one silently, and never build a third
   time.
6. Save every described character with `picsart_scene_library_save`: `kind: "character"`, the build's
   `scene`, the sheet in `referenceImages`, the description in `prompt`, a portrait in `previewUrl`.
   It is reused from the library, never generated again.

**Their own sheet.** The user sends one SVG drawn to character-rigging's part-sheet layout, received with
`picsart_drive_upload_ask`. Run `picsart_scene_build_model` with `character: {svg, check: true}` first and
read `pictureCheck`: a failed named check is fixed on the drawing by the user, never by building anyway.
Build the view with `character: {svg, view}`, place it in a 3-second test scene (rest, then walk),
render it with `picsart_scene_export` and REVIEW it by eye: every part present and attached, the far hand
there, feet on the floor. Save the accepted character with `picsart_scene_library_save`,
`kind: "character"`, so it is reused from the library.

## 3. Place

The background is one of:
- a generated background plate, in the cartoon's ratio, one image: quote it with `picsart_preflight`, then SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says),
  generate it with `picsart_generate` and declare it as an asset;
- a plain or gradient background from the capabilities;
- the user's own picture in the cartoon's ratio, received with `picsart_drive_upload_ask` and declared as an asset.

Set the floor line where the characters stand, and say where it is.

## 4. Prop

Only when a beat needs one, and one prop per character, one of:
- a small generated image: quote it, then SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says), generate it, remove its background with
  `picsart_image_remove_bg`, and check its alpha edges;
- a shape;
- the user's own picture with a transparent background (PNG or SVG), received with
  `picsart_drive_upload_ask`; check its alpha edges.

It is held by the hand socket, and by the mouth for the dog: read how from
character-rigging's held props. A prop that is not held by a socket is not a prop.

## 5. Build the scene

Catalogue presets only, through `picsart_scene_apply_preset` and `picsart_scene_patch`: the walk, wave,
reach, hold and carry, jump, jog, idle, with the camera fixed for each shot and one view per beat.
Place each character's scene with `fit: none` on the floor line. The narration is one of:
- a generated voice: write the narration lines, quote the voice with `picsart_preflight`, then SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says),
  and generate it as voice-over-generation says;
- the user's own recording, received with `picsart_drive_upload_ask` and transcribed with
  `picsart_media_transcribe` for its timing;
- the lines as captions, with no voice.

A child character's lines take a child's voice, cast as voice-over-generation says; say which voice was picked.
Start each line within 0.3 seconds of the beat it describes. Background music is optional:
when the user wants some, choose it as background-music says and duck it under the voice;
music the user sends, received with `picsart_drive_upload_ask`, goes on an audio layer under any voice.
Check the scene with `picsart_scene_validate` and the capabilities' own limits.

**Episode: shots.** Build each shot as its own scene, at its own length, staged as Staging says, with
`returnSceneUrl: true` so it has its own `sceneUrl`. Characters are placed by their `library:` uri, never inlined.

**Episode: dialogue.** Each character has one voice, and the user is told which voice each character got.
Cast each voice as voice-over-generation says, and generate each line in its speaker's voice.
Get each line's word timings with `picsart_media_transcribe`. Combine all of one character's lines in a shot into one transcript at their shot-relative times, then apply `picsart_scene_apply_preset` once with `preset: "lipSync:visemes"` on that
character's rig layer, for its own lines only (`speaker`), with the transcript and the rig's `visemes` in
`params`. Applying it again replaces the mouth tracks, so a second line applied alone would erase the first.
A rig without the viseme mouth set is named to the user ("X can't lip-sync"), and its lines become narration.

### Staging

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

**Episode:** review each shot first (below), then the root.

Render the busiest beat for 3 to 5 seconds first, then the whole clip, and look at every beat of it,
not one still. Review it as motion-review says. The checks that matter:
- no torn, floating or missing part in any frame, and the far hand never vanishes in a walk;
- planted feet do not slip, the walk starts and stops cleanly, and the character stays on the floor line;
- a wave keeps the hand beside or above the head, never over the face;
- a held prop stays at its socket in every frame, and is picked up and put down without a jump.

**Self-check before export.** Render a contact sheet with `picsart_scene_contact_sheet` at about 2 frames
a second and look at it. Fix each failure through its own path and render again, before any export:
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
- the voice-over starts on its beat: move the audio layer's `start`.

**Episode: continuity.** On the root, render one contact sheet with `picsart_scene_contact_sheet` across each shot
boundary and look: each character the same size and look on both sides of a cut, and screen direction kept
(who walked out right walks in from the left). A mouth that does not move on its line is a lip-sync that was
not applied: apply it again.

REVIEW the preview with the user. They tweak timing, positions and colours in `picsart_scene_tune`,
or ask in words.

## 7. Export

`picsart_scene_export`, 1080 by 1920 (16:9: 1920 by 1080) at 30 fps (an episode: the root scene). DELIVER the `downloadUrl`, naming each check that failed its bar before any praise, and for each character whether it was loaded from the library or newly drawn (DELIVER in picsart-video-rules). Offer to save the scene to
the library as kind `story` with `picsart_scene_library_save`, and do it only on a yes. Say where each
described
character is kept.
