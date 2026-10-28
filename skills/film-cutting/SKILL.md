---
name: film-cutting
description: Cut a film's accepted takes into one scene - how generated footage cuts, every shot a window over its run's file, the montage bootstrap with hard cuts, separate dialogue and ambience, cleanup of named glitches, and diagnosing a bad join before choosing the smallest repair. Use when a film's takes are assembled into a cut, a cut is changed, or a join between two shots is repaired.
user-invocable: false
---

# Film edit

The cut is built from the selects, never from the raw pile, and it stays editable: shots, not a
flattened strip. Read `references/join-repair.md` before you change a join between two shots.

## What generated footage cuts like

- **It runs draggy.** Entries into action are slow; cut harder than feels necessary.
- **Held generated motion reads uncanny.** Dramatic beats hold four to seven seconds at most; action
  cuts live at one to two. Vary lengths on the emotional beat, never evenly.
- **The first and last half-second of a generation are the least stable.** A solo take is trimmed
  at both ends; inside a run, the edges are the run's cuts, kept unless the user moves them.
- **Cut on motion and match it.** Static frames butted together read as a slideshow.
- **Check every run edge**: a changed angle and size, a carried movement, a sound step hidden by the
  bed, then eyelines, action axis, costume, props, hair, light and tempo.
- Weigh continuity in this order: emotion, story, rhythm, eye trace, then screen direction and
  literal space. Never sacrifice a beat to save a prop match.

## Windows

A run's shots are **windows over the run's own file**, in its source seconds, bounded by the cuts
the take actually made. One run URL appears in many clips, each with its own window. Never replace
a window with a trimmed export: that welds the handles shut.

**Only the user moves a window.** Nothing automatic sets trims from word timings, a beat clock or
planned durations. A trim the user makes is recorded on the shot as theirs and never recomputed. A
re-rolled run opens untrimmed, because its cuts are new. The run's end handles stay visible until
the user trims them; past a cut is the next shot's picture, and past the run's end there is nothing.

## Assembly

Build the cut with `picsart_scene_apply_template`: `uri: "scene://montage"`,
`mode: "bootstrap"`, and `parameters`:

- `clips`: one per shot, in playback order. Each is a full clip: `duration` (the window's length)
  and `content: { kind: "media", assetId: "<the run's url>", assetType: "video", trim: { in, out },
  fit: "cover" }`. Without `assetType: "video"` the file is read as a still and the trim is ignored.
  This URL-in-`assetId` form is the template's input, not a scene document's;
- `transition: ""`, for hard cuts. The template's default is a crossfade;
- `width` and `height`: the film's frame.

Probe every distinct file with `picsart_media_probe` for its real size and duration first.
Then change the scene with `picsart_scene_patch`, as scene-building-basics says. Never set the
composition's duration: it comes from the track. The result is reviewed as the scene object.

**Sound.** Dialogue and ambience or music on **separate audio layers**, so a J or L cut is possible
and a bed can carry across picture cuts. A bed does not repair a changed or invented line.

**Seams.** Within a scene, a hard cut. Between scenes, a hard cut or a short crossfade; another
transition only when the film's grammar calls for it, never to hide a discontinuity, and chosen as
scene-building-basics says. A crossfade on a run edge is a last
resort: it eats half its length from each side, so move both trims in by that much.

**Text in the world** (a sign, a screen, a door number) is a text layer in the scene, never asked of
the model.

## The review

The whole cut is reviewed once through; never one review per clip.

- The user's own edits are taken as picsart-video-rules says for an editor reply of `needs_changes`.
- Each comment is located on its clip and its source seconds, diagnosed, and applied; compatible
  notes are combined, and what the user asked to keep is kept.
- A note on a seam is a join to diagnose (`references/join-repair.md`), never a licence to generate.
- Once the user calls the cut final, no picture changes unless they ask.

## Cleanup

A named glitch (hands, teeth, a melted face, a drifting object, boiling texture, pseudo-text) is
repaired on its clip with the edit model, naming the defect and its time and keeping the run's
references. Put the fix back in the cut and review the **whole affected stretch**: a fix can break
the light or the continuity. If two edits do not fix it, the run may need a re-roll. When a shot
cannot be made clean, the honest fallbacks are a cut around it (a cutaway, a tighter trim) or the
user's acceptance of the flaw, in words.

## Traps

- Regenerating to shorten a clip, move its start or fix a cut point: move the window.
- Exporting to answer "what if", which picsart-video-rules's Preview and export does not allow: change the
  scene and review it.
- A cut built from raw takes instead of selects.
- A flattened strip that cannot be recut.
- Deleting or overwriting an old take: every version stays, and the record keeps it.
