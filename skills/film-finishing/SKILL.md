---
name: film-finishing
description: Finish a film after picture lock - the takes finished to full quality, colour matched and graded from the scene tools' looks, the soundtrack (the takes' own voices, an ambience or music bed), QC, masters, the archive and any AI disclosure. Use when a film's cut is final and it needs finishing, delivery files or its archive.
user-invocable: false
---

# Film finishing

Picture lock is behind you: nothing here changes the cut. The order is fixed and worth saying to the
user:
**finish the draft takes → re-assemble → grade → export once → masters → archive.** Grading
a draft wastes the grade; exporting before the grade wastes an export.
For a cut of the user's own footage, the order is **assemble the locked cut at the finish size →
grade → export once → masters → archive.** Read `references/delivery.md` before QC, masters or the archive.

## Finishing the draft takes

Runs are shot as drafts (film-shot-generation), so the approved cut is finished before colour.
**The finish comes only after the user approves the draft cut, on its own quote and its own yes**:
the draft batch's quote showed it as an estimate, never as bought. Ask once: ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) whether the
drafts are good enough for where the film goes, with the finish of every approved take priced
beside them: finish them, or keep the drafts. **That one question is the finish's quote and its
yes**; keeping the drafts skips this section. Only a model shot at its finish settings (no draft
setting and no lower resolution) has nothing to finish.

The finish, per take, in this order of preference:

- **A draft that returned a `finalizeDraft` handle** (Seedance 2.5): send its arguments unchanged,
  with the draft's prompt. It renders the same take at the finish settings instead of a fresh
  roll, so the approved performance and trims hold. The handle lasts 7 days; an older draft takes
  the next route.
- **No handle:** an upscale where one fits, a separate model chosen from `picsart_model_catalog` at
  the time (none is named here); or the approved run **generated again at the finish settings with
  its saved final prompt, verbatim**: same blocks, same references, the model's final settings as
  `picsart_model_params` names them. Say it before it runs: this is a **fresh roll**, not an
  upscale. Small differences from the draft are expected. Where a re-roll breaks something the draft
  had (a face, a join), that is a repair on the final take (film-shot-generation), logged and fixed.

Every approved take is finished in one batch, on that one yes, and a repair made during the draft
review is finished with the rest. Upscale first, then texture, then grade: every correction
touches the highest-resolution pixels. Then re-assemble the locked cut at the finish size
(film-cutting), with the user's trims unchanged. A cut with a fresh roll in it is shown once more
before colour: its differences from the approved draft are the user's to see.

## Colour: match, then grade

Every generation carries its own baked-in grade.
The first job is **matching** neighbouring shots
of each scene, and only then the look. The film's tone already lives in its places' pictures, so
the grade refines it and never invents a new one.

- Read the real looks from `picsart_scene_capabilities` with `sections: ["looksCompact"]`
  (never a remembered look name, and never the full `looks` section, which can overflow), and
  return three or four that suit the film's colour.
- The user picks the look: apply each of them to one representative scene and show the versions
  in `picsart_scene_picker`, each card labelled in their terms ("warm dusk", "cool and muted"),
  never a `look:<id>`. Never choose for them or describe the looks in text; grade the film with
  the one they keep and say which (picsart-video-rules, "A choice made by eye").
- Apply with `picsart_scene_apply_preset`, one call per clip layer: it takes `scene` (the assembled
  scene), `layerId` (that clip's layer) and `preset` (`look:<id>`), and changes only that layer. Do the layers of
  one scene first, then the rest of the film. Setting a look is free.
- Check a chosen look on a few frames from two or three scenes with `picsart_scene_contact_sheet`
  before applying it to the film.
- A fine grain or texture pass at finishing is distinct from the grain the look put in the
  generation: this one unifies what the renders became.
- If the user has a colourist, export ungraded and hand off (`references/delivery.md`).

## Sound

What generation gave: lip-synced dialogue in the shot, in-frame action noise, some ambience. What
it cannot give: one voice timbre across takes, licensed music, a mix.

- **The takes keep their voices.** A line is never re-recorded here. Where a speaker's timbre drifts
  enough to distract, prefer a retake of the worse clip over pretending a mix exists.
- **Ambience is the glue.**
  Generated audio is per clip, so seams are audible:
  A continuous bed under
  each scene hides the level and tone steps. Match levels shot to shot.
- **A music bed is drafted and laid as the background-music skill says**: its brief takes the register
  from the film's look and the tempo from its cut, and it is laid under the takes' dialogue and the
  ambience, never in place of them.
- **Music the user brings** comes in with `picsart_drive_upload_ask` and is laid under the takes'
  dialogue and the ambience, never in place of them.
- A film going to festivals or dubbing needs a sound team: it gets the handoff package, never an
  imitation.

## Traps

- Grading the draft.
- Finishing before the user approved the draft cut, or on the draft batch's yes.
- Calling a re-generated take an upscale, or re-rolling a draft that has a `finalizeDraft` handle.
- Re-rolling the film at final resolution on the strength of the forecast: quote this batch, then
  wait.
- Another export per master nobody asked for. Free or not (picsart-video-rules says which tools are), each
  is a render and a file in the user's Drive.
- Music shipped without the background-music skill's licence caveat.
- Music the user brought, shipped without asking whether they hold its rights.
- Archiving the film without its
  prompts and
  asset rows: a film without its means of production
  cannot be revised or continued.
