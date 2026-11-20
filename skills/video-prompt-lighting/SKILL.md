---
name: video-prompt-lighting
description: Refine lighting direction, softness and shadow detail in an existing video prompt. Use for flat lighting, unclear sources, inconsistent shadows or product reflections.
license: MIT
metadata:
  version: "1.0.0"
---

# Video Prompt: Lighting

## Scope and output

Use the supplied prompt and requested change. If no prompt is supplied, ask for it; do not invent a new brief. No generation tools, paid jobs or publication are needed.

Keep subject, action, identity, brand requirements, duration, aspect ratio, audio and references unchanged unless the request explicitly changes them. Replace conflicting in-scope wording rather than appending contradictions. If two explicit requirements conflict and the intended outcome is unclear, ask one focused question; otherwise make the smallest useful edit and label assumptions. Do not require a model choice for a model-neutral wording repair.

Return the revised full prompt in a copyable block (or only the replacement clause if requested), a short change note, assumptions only when needed, and one relevant output check. Do not claim the edit is tested or will cure a model defect. When a model is named, use its documented controls and limits; unknown capabilities remain unknown.

## Refinement decisions

Separate direction, quality, intensity, fill and colour. Identify a motivated key relative to the subject/camera: front, side, back, top or another specified position. Then describe a crisp or gradual shadow edge. Apparent source size at the subject affects softness; soft does not mean dim or low contrast.

Specify shadow-side readability separately with fill or negative fill where useful. A backlight can separate an edge while leaving the front dark; add readable front detail only when the brief needs it. Keep rims local to source-facing edges, not a glow around every object.

Describe what the light reveals: face shape, cloth weave, glaze, machining or glass contours. Soft light must not erase skin or material texture. On reflective objects, source shape and surroundings matter; keep highlights attached to geometry as the object turns.

For a single view, camera-left/right is useful. Across reverse angles, preserve the source in world space (for example, the window beside the door); its screen-side description can change with the camera. Do not force camera-left in every reverse shot and accidentally move the window. Treat setup names as optional shorthand, not universal mood guarantees. Do not invent key-to-fill ratios or lamp settings.

## Example

Original: A ceramicist turns a cup under cinematic lighting.

Revision: A ceramicist turns a cup beside a broad window on camera-left. Soft side light produces a gradual cheek shadow and a broad reflection on the glaze; gentle room bounce leaves the far eye readable.

This illustrates a scoped edit, not a tested model recipe. Keep any other clauses in the actual user's prompt.

## Review

Check cast-shadow direction, shadow edges, face readability, source position and reflections throughout the action.

For evidence boundaries, see [sources](references/sources.md).
