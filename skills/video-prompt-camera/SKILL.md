---
name: video-prompt-camera
description: Refine camera framing, angle, movement and focus in an existing video prompt. Use for confusing camera directions, unwanted camera drift, or professional shot names.
license: MIT
metadata:
  version: "1.0.0"
---

# Video Prompt: Camera

## Scope and output

Use the supplied prompt and requested change. If no prompt is supplied, ask for it; do not invent a new brief. No generation tools, paid jobs or publication are needed.

Keep subject, action, identity, brand requirements, duration, aspect ratio, audio and references unchanged unless the request explicitly changes them. Replace conflicting in-scope wording rather than appending contradictions. If two explicit requirements conflict and the intended outcome is unclear, ask one focused question; otherwise make the smallest useful edit and label assumptions. Do not require a model choice for a model-neutral wording repair.

Return the revised full prompt in a copyable block (or only the replacement clause if requested), a short change note, assumptions only when needed, and one relevant output check. Do not claim the edit is tested or will cure a model defect. When a model is named, use its documented controls and limits; unknown capabilities remain unknown.

## Refinement decisions

Separate five decisions: framing, camera height and aim, physical path, focus, and support. Use a professional name followed by a visible instruction. Expand MCU (medium close-up), CU (close-up), ECU (extreme close-up), OTS (over the shoulder) and POV (point of view); framing boundaries vary by crew.

- Pan/tilt rotate from a fixed position; truck translates sideways; push in/dolly in and pull back/dolly out travel toward/away from the subject. Translation can reveal occluded surfaces and change parallax. Zoom changes focal length from a fixed viewpoint; it is not a push-in. Real lenses may breathe or change distortion.
- Boom up/down describes vertical travel; crane describes equipment. Pedestal up/down describes a vertical lift without necessarily changing aim. State both height and aim: a camera near the floor need not look up.
- A fixed Dutch angle is not a rolling camera. A rack focus changes the sharp plane between named targets; focus breathing may change framing. Do not promise a perfectly unchanged frame.
- Locked off means a stationary camera. Handheld, stabilized tracking, aerial and performer-mounted describe support or operation, not a complete path. Steadicam and Snorricam are equipment names, not generic synonyms for all stabilization or body mounting. FPV names a control/viewing method; specify banking or a level horizon explicitly.
- Arc and rise, push past and reveal, and other combinations are descriptive directions. Keep a feasible user-requested combination; do not invent an industry nickname or prohibit all combined moves.
- Tracking is broader than following behind. An insert is not every cutaway; a two-shot is not a three-shot. A dirty single includes another person at the edge, but is not always the same composition as OTS. A oner describes a continuous-take treatment; do not claim hidden joins are a true unbroken capture.
- Choose field of view, camera distance and focus target before arbitrary lens numbers. Viewpoint determines perspective; sensor/film format affects the field of view for a given focal length. A lens number in a generative prompt is a request, not calibrated optics.

Read [the 64-case terminology reference](references/camera-cases.md) only when selecting a name or resolving an alias. The examples are original directions, not universal crew commands.

## Example

Original: Camera pans closer to the cup.

Revision: Push in toward the cup, keeping it centered and the full rim visible.

This illustrates a scoped edit, not a tested model recipe. Keep any other clauses in the actual user's prompt.

## Review

Check the intended path, start/end framing, occlusions and focus. Preserve existing movement timing unless that is also in scope.

For evidence boundaries, see [sources](references/sources.md).
