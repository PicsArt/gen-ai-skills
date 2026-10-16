---
name: film-finishing
description: Finish a film after picture lock - the final-resolution pass from the saved prompts, colour matched and graded from the scene tools' looks, the soundtrack (the takes' own voices, an ambience or music bed), QC, masters, the archive and the AI disclosure. Use when a film's cut is final and it needs finishing, delivery files or its archive.
user-invocable: false
---

# Film finishing

Picture lock is behind you: nothing here changes the cut. The order is fixed and worth saying to the
user: **final-resolution pass → re-assemble → grade → export once → masters → archive.** Grading
the draft wastes the grade; exporting before the grade wastes an export. Read
`references/delivery.md` before QC, masters or the archive.

## The final-resolution pass

The film was shot in drafts, as film-shots says, so its final quality comes from **re-generating every approved run
at the finish settings with its saved final prompt, verbatim**: same blocks, same references, the
model's final settings as `picsart_model_params` names them (a draft switch, a resolution). The
whole batch is one quote and the film's biggest single spend. Only a model with no draft setting
skips this pass: its takes are already final.

**The pass is offered, never assumed.** First ask the user whether the drafts are good enough for where the
film goes, with the pass priced beside them: keep the drafts, or run the pass. Keeping them skips
this section. A model whose draft returns a `finalizeDraft` handle (Seedance 2.5) renders the same
take at the finish settings instead of a fresh roll: send its arguments unchanged, with the
draft's prompt.

Say it before it runs: this is a **fresh roll**, not an upscale. Small differences from the draft
are expected. Where a re-roll breaks something the draft had (a face, a join), that is a repair on
the final take (film-shots), logged and fixed.

Upscaling is a separate model, chosen from `picsart_model_catalog` at the time; none is named here.
Upscale first, then texture, then grade: every correction touches the highest-resolution pixels.
Then re-assemble the locked cut at the finish size (film-edit), with its windows unchanged.

## Colour: match, then grade

Every generation carries its own baked-in grade, so the first job is **matching** neighbouring shots
of each scene, and only then the look. The film's tone already lives in its places' pictures, so
the grade refines it and never invents a new one.

- Read the real looks from `picsart_media_get_capabilities` with `sections: ["looksCompact"]`
  (never a remembered look name, and never the full `looks` section, which can overflow), and
  return three or four that suit the film's colour.
- Apply with `picsart_media_apply_look`, one call per clip layer: it takes `scene` (the assembled
  scene), `layerId` (that clip's layer) and `look`, and changes only that layer. Do the layers of
  one scene first, then the rest of the film. Setting a look is free.
- Check a chosen look on a few frames from two or three scenes with `picsart_media_contact_sheet`
  before applying it to the film.
- A fine grain or texture pass at finishing is distinct from the grain the look put in the
  generation: this one unifies what the renders became.
- If the user has a colourist, export ungraded and hand off (`references/delivery.md`).

## Sound

What generation gave: lip-synced dialogue in the shot, in-frame action noise, some ambience. What
it cannot give: one voice timbre across takes, licensed music, a mix.

- **The takes keep their voices.** A line is never re-recorded here. Where a speaker's timbre drifts
  enough to distract, prefer a retake of the worse clip over pretending a mix exists.
- **Ambience is the glue.** Generated audio is per clip, so seams are audible: a continuous bed under
  each scene hides the level and tone steps. Match levels shot to shot.
- **A music bed is drafted and laid as the music-bed skill says**: its brief takes the register
  from the film's look and the tempo from its cut, and it is laid under the takes' dialogue and the
  ambience, never in place of them.
- A film going to festivals or dubbing needs a sound team: it gets the handoff package, never an
  imitation.

## Traps

- Grading the draft.
- Calling the final pass an upscale.
- Re-rolling the film at final resolution on the strength of the forecast: quote this batch, then
  wait.
- Another export per master nobody asked for. Free or not (video-core says which tools are), each
  is a render and a file in the user's Drive.
- Music shipped without the music-bed skill's licence caveat.
- Archiving the film without its prompts and asset rows: a film without its means of production
  cannot be revised or continued.
