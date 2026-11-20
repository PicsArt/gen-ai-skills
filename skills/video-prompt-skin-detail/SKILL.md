---
name: video-prompt-skin-detail
description: Refine skin texture and light response in an existing video prompt. Use for waxy, plastic or over-smoothed faces while preserving the approved person.
license: MIT
metadata:
  version: "1.0.0"
---

# Video Prompt: Skin Detail

## Scope and output

Use the supplied prompt and requested change. If no prompt is supplied, ask for it; do not invent a new brief. No generation tools, paid jobs or publication are needed.

Keep subject, action, identity, brand requirements, duration, aspect ratio, audio and references unchanged unless the request explicitly changes them. Replace conflicting in-scope wording rather than appending contradictions. If two explicit requirements conflict and the intended outcome is unclear, ask one focused question; otherwise make the smallest useful edit and label assumptions. Do not require a model choice for a model-neutral wording repair.

Return the revised full prompt in a copyable block (or only the replacement clause if requested), a short change note, assumptions only when needed, and one relevant output check. Do not claim the edit is tested or will cure a model defect. When a model is named, use its documented controls and limits; unknown capabilities remain unknown.

## Refinement decisions

Preserve identity, age, skin tone, makeup and distinctive marks from the brief/reference. Add only plausible visible detail at the shot scale. Do not manufacture wrinkles, freckles or pores as a universal realism recipe, and do not change demographic features to improve realism.

Distinguish surface texture, local colour variation and light response. Request subtle pores where visible, restrained specular highlights and natural transitions through shadow. Skin is not uniformly rough plastic; excessive sharpness or pore contrast can look etched. Soft illumination is not skin blur.

A reference frame may already settle the face and light. For image-to-video, concentrate on preserving those features through the requested motion rather than rewriting the appearance. Do not promise that terms such as subsurface scattering configure a physical renderer.

Review temporal attachment: marks should move with the face, not swim across it; cheeks, eyelids, teeth and ears should preserve form through a turn. Photoreal appearance is not evidence that footage records a real event. These are creative hypotheses to test, not proven cures for model defects.

## Example

Original: The approved woman turns toward the window, with perfect smooth skin.

Revision: The approved woman turns toward the window, retaining her age, skin tone and distinctive marks, with subtle visible skin texture and restrained highlights that follow the turn.

This illustrates a scoped edit, not a tested model recipe. Keep any other clauses in the actual user's prompt.

## Review

Compare identity before/during/after movement. Check texture at final crop size, not only an enlarged still.

For evidence boundaries, see [sources](references/sources.md).
