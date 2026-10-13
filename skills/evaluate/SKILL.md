---
name: evaluate
description: Check a scene before the user sees it - validate it, lint its layout for overlaps, measure where layers sit, look at contact-sheet frames at the moments that matter and across the whole timeline, then fix and check again. Use after building or changing a scene, before REVIEW or an export.
user-invocable: false
---

# Evaluate

1. **Validate.** A successful `picsart_media_patch_scene` has already validated its result, so call
   `picsart_media_validate_scene` only after changes made any other way. Zero errors; fix the
   warnings too.
2. **Lint the layout.** `picsart_media_layout_lint` over the timeline; on a long scene, narrow
   `t0`/`t1` to the part in question. Each of its `findings` is a sustained overlap between layers
   that should not touch. For a pair placed together on purpose, pass `allow: ["idA:idB"]`. A clean
   lint is not proof: on the `jet` engine it never measures text, and on `v3` a text box is the
   font's line box, so it can flag empty space. If the tool is not in your list, or fails because
   the query build is unavailable, skip to the frames.
3. **Measure.** For a flagged pair, or a use-case question about where something sits (inside a
   panel, inside a mask), `picsart_media_query_layout` at that moment gives each layer's box. It
   reads layer geometry, not painted pixels, and has no box for text on `jet`.
4. `picsart_media_contact_sheet` at each moment the use case names. Look at every frame and answer
   the use case's questions about it.
5. `picsart_media_contact_sheet` once across the whole timeline — order, seams, nothing blank.
   Then, for every cut, its `times` at the cut and one frame either side (`cut − 1/fps`, `cut`,
   `cut + 1/fps`): a one-frame black gap falls between evenly spaced samples.
6. Fix the layers and check again. Building is free.

**When a frame or an export fails to render.** The scene validated, so the fault is in a feature
the renderer refuses, and the error names it rarely. Find it before changing anything:

1. Copy the error text exactly.
2. Cut a copy of the scene down to the one layer at the failing time, and sample that. Then take
   away one feature at a time (its mask, its effects, its animation) until it renders. Each sample is
   one frame.
3. Keep the scene as it is. Tell the user which feature fails, with the error and the smallest
   scene that shows it, and offer a way round it that keeps the look where one exists (for a mask,
   the layouts skill's nested panel). Never reshape the
   whole scene to guess past it.

Frames show framing, not motion: the user judges timing and easing in REVIEW.

How many rounds you get, and what to do when they run out, is in video-core (Evaluation). Never
export to "show" a draft that the user can review live; video-core (Preview and export) says when
to export.
