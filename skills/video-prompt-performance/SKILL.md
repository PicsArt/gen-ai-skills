---
name: video-prompt-performance
description: Refine gaze, gesture, weight and object contact in an existing video prompt. Use for robotic acting, sliding feet, floaty motion or unclear physical actions.
license: MIT
metadata:
  version: "1.0.0"
---

# Video Prompt: Performance

## Scope and output

Use the supplied prompt and requested change. If no prompt is supplied, ask for it; do not invent a new brief. No generation tools, paid jobs or publication are needed.

Keep subject, action, identity, brand requirements, duration, aspect ratio, audio and references unchanged unless the request explicitly changes them. Replace conflicting in-scope wording rather than appending contradictions. If two explicit requirements conflict and the intended outcome is unclear, ask one focused question; otherwise make the smallest useful edit and label assumptions. Do not require a model choice for a model-neutral wording repair.

Return the revised full prompt in a copyable block (or only the replacement clause if requested), a short change note, assumptions only when needed, and one relevant output check. Do not claim the edit is tested or will cure a model defect. When a model is named, use its documented controls and limits; unknown capabilities remain unknown.

## Refinement decisions

Keep the intended action and emotion. Give gaze a target and a reason: notice an object, then react; direct lens contact remains valid for a presenter. Avoid stacking conflicting emotions or mandatory blinking/twitching into every shot.

For movement, describe approach, contact, weight transfer, release and settling only where visible. A supporting foot stays planted during weight transfer; hands maintain plausible grips; clothing responds and settles. Contact shadows alone do not prove weight. Keep geometry and product mechanisms stable.

Match action complexity to available duration and references. Simplify a difficult action as an explicitly labelled alternative rather than silently removing the requested demonstration. Preserve hands/feet in frame when the brief needs to verify them; cropping away defects is not a successful demonstration.

Separate camera movement from performer movement. A deliberate still pose is valid. For dialogue, preserve exact words and distinguish native speech/lip-sync from a separate voiceover workflow; prompt repair alone does not produce audio. Model failure, reference ambiguity and insufficient coverage remain possible even with a clear prompt.

## Example

Original: The maker walks up to the bench naturally.

Revision: The maker approaches the bench, plants the supporting foot, transfers weight and settles beside it. Clothing settles after the stop; feet remain visible against the floor.

This illustrates a scoped edit, not a tested model recipe. Keep any other clauses in the actual user's prompt.

## Review

Watch gaze targets, planted contacts, hand grips, proportions and the end state through the whole action.

For evidence boundaries, see [sources](references/sources.md).
