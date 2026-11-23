---
name: video-prompt-motion-timing
description: Refine speed, easing, holds and motion blur in an existing video prompt. Use when a move needs steady speed, acceleration, deceleration or a clear ending.
license: MIT
metadata:
  version: "1.0.0"
---

# Video Prompt: Motion Timing

## Scope and output

Use the supplied prompt and requested change. If no prompt is supplied, ask for it; do not invent a new brief. No generation tools, paid jobs or publication are needed.

Keep subject, action, identity, brand requirements, duration, aspect ratio, audio and references unchanged unless the request explicitly changes them. Replace conflicting in-scope wording rather than appending contradictions. If two explicit requirements conflict and the intended outcome is unclear, ask one focused question; otherwise make the smallest useful edit and label assumptions. Do not require a model choice for a model-neutral wording repair.

Return the revised full prompt in a copyable block (or only the replacement clause if requested), a short change note, assumptions only when needed, and one relevant output check. Do not claim the edit is tested or will cure a model defect. When a model is named, use its documented controls and limits; unknown capabilities remain unknown.

## Refinement decisions

Keep the chosen route and subject action. Specify timing separately for camera, subject, focus change and edit; they are different clocks.

| Profile | Visible instruction |
|---|---|
| Constant speed | Move at an even rate through the stated travel interval. |
| Accelerate | Start slowly and build speed toward the named endpoint. |
| Decelerate | Begin at the selected pace and progressively slow to a stop. |
| Ease in and out | Build speed gently, maintain the middle pace, then ease to rest. |
| Pause and resume | Arrive at the named view, hold, then resume the route. |

Smooth means stable or continuous; it does not necessarily mean slow or constant-speed. Constant speed through the entire clip conflicts with a gradual stop unless separate intervals are named. Constant speed around a curve is not a fixed velocity vector: use speed or angular rate rather than promising fixed velocity on an arc.

If an actual duration is known, make phases fit that duration; otherwise use start/middle/end and identify timing as an assumption. Do not invent a supported duration or frame rate. Use supported generation settings for export duration/rate. A prompt mentioning a shutter angle does not configure capture physics.

Slow camera travel, slowed subject playback, long exposure blur and fast-forward are different. Describe the moving part, blur direction and desired readability. Keep still areas stable; do not use smear to conceal morphing. A speed-versus-time sketch has time horizontally and speed/rate vertically: a plateau is constant, a rising line acceleration, a falling line deceleration, and zero a hold. It is a conceptual plan, not measured model output.

## Example

Original: Slow smooth push-in at constant speed, then gradually stop.

Revision: Push in at an even slow pace through the middle of the shot, then decelerate gently and hold the final composition.

This illustrates a scoped edit, not a tested model recipe. Keep any other clauses in the actual user's prompt.

## Review

Check the whole move at playback speed, then inspect the transitions and final hold. No promise of exact physical timing without tool controls.

For evidence boundaries, see [sources](references/sources.md).
