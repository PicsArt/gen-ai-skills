---
name: video-prompt-continuity
description: Refine eyelines, screen direction and matching across existing video prompts. Use for dialogue coverage, inconsistent subjects or shots that do not cut together.
license: MIT
metadata:
  version: "1.0.0"
---

# Video Prompt: Continuity

## Scope and output

Use the supplied prompt and requested change. If no prompt is supplied, ask for it; do not invent a new brief. No generation tools, paid jobs or publication are needed.

Keep subject, action, identity, brand requirements, duration, aspect ratio, audio and references unchanged unless the request explicitly changes them. Replace conflicting in-scope wording rather than appending contradictions. If two explicit requirements conflict and the intended outcome is unclear, ask one focused question; otherwise make the smallest useful edit and label assumptions. Do not require a model choice for a model-neutral wording repair.

Return the revised full prompt in a copyable block (or only the replacement clause if requested), a short change note, assumptions only when needed, and one relevant output check. Do not claim the edit is tested or will cure a model defect. When a model is named, use its documented controls and limits; unknown capabilities remain unknown.

## Refinement decisions

Map people, props and light sources in world space first, using an existing master/shared view or a simple seating plan. Track speaker/listener, gaze target, screen position, body orientation, prop state and action phase for each shot.

Keep camera positions on the intended side of the action axis for conventional coverage. Deliberate axis crossings can work when geography is re-established; do not forbid them universally. A listener looks toward the other person, not automatically past the lens in every kind of film. Direct-address presenters may look into the lens.

Use OTS (over the shoulder), clean single, dirty single, two-shot, master, insert and reaction for their actual functions. A dirty single has some of another person in frame; OTS specifies shoulder-based framing. An insert isolates scene detail; a reaction is not necessarily an insert. A continuous-looking oner may contain joins.

Carry approved identity, wardrobe, product geometry and material references into each independent generation. Shared wording helps consistency but cannot guarantee it. Preserve the world-space key source across reverse angles, not an invariant camera-left label. Match focus, exposure, palette, action phase and background geography at the cut.

For one multi-shot prompt, state shared context once; for independent calls, include the needed context in every prompt. Keep dialogue/audio continuity as a separate edit decision. Do not claim repeatedly generating the same music description yields one continuous score.

## Example

Original: A sits left, B right. Cut to B looking right toward A.

Revision: A sits screen-left and B screen-right in the shared view. In B’s closer coverage from the same side of the action axis, B looks screen-left toward A. Preserve the established seats, props and window position.

This illustrates a scoped edit, not a tested model recipe. Keep any other clauses in the actual user's prompt.

## Review

Compare shots side by side and at the intended cut; verify references, eyelines, action phase and world-space light rather than matching isolated adjectives.

For evidence boundaries, see [sources](references/sources.md).
