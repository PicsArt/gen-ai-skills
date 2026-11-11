---
name: make-cartoon
description: Make a short cartoon clip with a character the user picks or describes - one 9:16 video of 8 to 20 seconds with one or two characters in one place, who walk in, wave, reach, hold or carry a prop, and a narrator's voice-over or captions. A character is picked from the ready-made cast or the user's saved library, or built from a part sheet into an editable cut-out rig and checked on a short test render, then saved for reuse. Use when the user wants a cartoon, an animated character or a mascot clip, a kids' story beat, or a short scene with their character. Not for a character's sheet with no scene, nor for a drama with several scenes, nor for motion on a design (animate-design).
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

Read picsart-video-rules first. One job: one short cartoon clip, 9:16, 8 to 20 seconds, one or two
characters, one place, with a narrator's voice-over or captions. The characters do not speak on screen, and
nothing here turns, sits, hugs, claps or hands a prop to another character: reword such a beat or say
"not yet". More than two characters, a second place, more than 20 seconds or another ratio is a
different job: say so before starting. These limits are for planning a new cartoon. They never cap an edit the user asks for: an edit that
lengthens the clip, such as slowing the ending, is done as asked. If it pushes the clip past 20 seconds, say so once and do it anyway.

Before acting on a stage, load the available skills in its row that apply to this job, also when the work resumes there.

| Stage | Gate | Skills |
|---|---|---|
| 1. The plan | ASK | scene-building-basics |
| 2. Cast | ASK, SPEND, REVIEW | character-rigging |
| 3. Place | SPEND | scene-building-basics |
| 4. Prop | SPEND | character-rigging |
| 5. Build the scene | SPEND | character-rigging, scene-building-basics, voice-over-generation, background-music |
| 6. Review | REVIEW | motion-review |
| 7. Export | DELIVER | scene-building-basics |

## 1. The plan

Turn the request into one short paragraph and ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) the user to approve or edit it in one turn: who (one
or two characters), where (one place), what happens in 3 to 5 beats, and the narration or caption lines. A beat is
one of: walk in or out, idle, wave, reach, pick up, hold or carry a prop, put it down, jump, jog.
Think and hand-over join the list when `picsart_scene_capabilities` shows them. Read the allowed actions
from `picsart_scene_capabilities`, not from memory: a beat it does not list is reworded or refused.

## 2. Cast

One character at a time. Look in the user's saved library first with `picsart_scene_library_list`
(`kind: "character"`), and offer the ready-made cast from `picsart_scene_capabilities`. ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) which:
a saved or ready-made one,
a new one described in their words,
or one built from a part sheet they drew.

**Pick.** A saved character is a scene in the library: place it with `picsart_scene_apply_template`,
`uri: "library:<libraryId>"`, so a second scene with the same character is identical. A ready-made one
is placed with `picsart_scene_apply_template` too, with the template's `uri` from `picsart_scene_templates`.
Actions are applied later, to the placed character, with `picsart_scene_apply_preset`.

**Describe.** Follow character-rigging's "From a picture" and its part-sheet prompt:
1. Quote two turnaround sheets with `picsart_preflight`, then SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says). Draw both with ONE
   `picsart_generate` call, `count: 2`, with the part-sheet prompt and the user's description, and the
   child's or user's reference image when they sent one. The call honours `count` for sheets: the two jobs
   come back in `jobs`.
   A sheet takes four minutes or more, so say so in the same turn the receipt comes back: "Drawing two
   sheets, about four minutes; I'll check in." Then follow the receipts with `picsart_job_status`, the
   longest `waitSeconds`, and tell the user in a sentence each time something changes (one sheet done, both
   done, a failure and what you do next). Never wait silently. A failed sheet is retried once.
2. ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) which sheet, with `picsart_film_review_assets`; a change is surgical, a new sheet is
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
- a generated background plate, 9:16, one image: quote it with `picsart_preflight`, then SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says),
  generate it with `picsart_generate` and declare it as an asset;
- a plain or gradient background from the capabilities;
- the user's own 9:16 picture, received with `picsart_drive_upload_ask` and declared as an asset.

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

Start each line within 0.3 seconds of the beat it describes. Background music is optional:
when the user wants some, choose it as background-music says and duck it under the voice;
music the user sends, received with `picsart_drive_upload_ask`, goes on an audio layer under any voice.
Check the scene with `picsart_scene_validate` and the capabilities' own limits.

## 6. Review

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
- the ending hold is 1 s or less (`picsart_scene_check_motion` shows when the last part stops): shorten the
  composition and layer `duration`;
- the voice-over starts on its beat: move the audio layer's `start`.

REVIEW the preview with the user. They tweak timing, positions and colours in `picsart_scene_tune`,
or ask in words.

## 7. Export

`picsart_scene_export`, 1080 by 1920 at 30 fps. DELIVER the `downloadUrl`, naming each check that failed its bar before any praise, and for each character whether it was loaded from the library or newly drawn (DELIVER in picsart-video-rules). Offer to save the scene to
the library as kind `story` with `picsart_scene_library_save`, and do it only on a yes. Say where each
described
character is kept.
