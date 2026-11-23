---
name: video-prompt-engineer
description: Write or improve AI video prompts, including focused repairs to camera, timing, lighting, film look, skin, performance, continuity and product detail. Use for a new video idea, an existing prompt, or a reported visual defect; return prompt text rather than generating video.
version: 1.1.0
author: Picsart
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: creative
    tags: [picsart, video, prompt-engineering, prompt-optimization, generation]
---

# Video Prompt Engineer

Turn a brief into observable shot instructions, or make a scoped improvement to an existing prompt. Output ready-to-use text. This skill does not authorize generation, spending, editing assets or publication. Clear wording helps express intent; it does not guarantee adherence or prove the cause of a model failure.

## When to use

Use for a new video idea, a prompt revision, a style-match request or a defect report. Support commercial work, photoreal scenes and animation. When the user asks to fix only the camera, preserve lighting, subject, brand, action and other settled choices.

## Inputs and scope

Read the brief, original prompt, supplied images, style/character references and any reported defect. Use project-local approved references first; do not assume an unseen file or image was inspected. A prompt can be improved without a generated clip, but then describe possible causes, not an observed diagnosis.

- **New brief:** settle the scene's subject, purpose, action, framing and ending. Ask only for unresolved choices that materially change the outcome; use labelled reasonable assumptions for minor gaps.
- **Existing prompt:** identify requested edit dimensions and frozen requirements before writing. Replace contradictory clauses within scope. Do not rewrite unrelated dimensions to demonstrate every technique.
- **Two conflicting explicit requirements:** ask a focused question if their priority is unclear. Offer labelled alternatives when helpful; do not quietly discard one.
- **Image-to-video:** preserve the approved starting image and focus on the requested changes, movement and ending. Do not introduce a new appearance by redescribing the image. If a requested camera move exposes unseen surfaces, flag the missing reference coverage.
- **Named model:** check current provider/endpoint documentation for controls, audio, references, duration, aspect ratio, negative fields and prompt limits. Record source/date for any capability claim outside the prompt. Unknown stays unknown. Do not invent endpoint syntax or a universal word limit.
- **Unknown model:** a model-neutral text revision is useful. Say it has not been adapted to a specific endpoint rather than blocking a simple edit on a model question.

## Route the refinement

The specialist skills below are optional entrypoints for narrowly scoped edits. Use only relevant ones when installed; do not chain all eight by default. An individually installed copy of this skill has equivalent core guidance in [craft refinements](references/craft-refinements.md), so sibling installation is not required.

| Request | Specialist | Decisions to inspect |
|---|---|---|
| Fix camera, framing, angle or focus | `video-prompt-camera` | Shot size, height versus aim, path versus rotation/zoom, focus targets, support |
| Make movement steady, ease or stop | `video-prompt-motion-timing` | Speed profile, phases, pauses, endpoint; camera versus subject time |
| Improve light or reflections | `video-prompt-lighting` | Motivated source, direction, softness, fill, intensity and material response |
| Film look, palette, grain or glow | `video-prompt-film-look` | Colour, contrast, roll-off, grain, bloom and halation; generation versus finishing |
| Waxy skin or facial detail | `video-prompt-skin-detail` | Approved identity, age, texture scale, light response and temporal stability |
| Robotic gaze, gait or contact | `video-prompt-performance` | Intention, gaze target, contact, weight transfer and settling |
| Shots do not cut together | `video-prompt-continuity` | Geography, eyelines, action phase, references and world-space sources |
| Premium/luxury product presentation | `video-prompt-product-detail` | Material, silhouette, finish, brand, wear, contact and truthful condition |

For a broad “improve this prompt” request, review every dimension for relevance, then apply only changes supported by the brief. A skin edit is irrelevant to a mechanical component; a fixed shot does not need easing. Describe feasible combined movements such as an arc and rise rather than banning all combinations or inventing slang.

## Write the shot

1. Establish the intended visible result and preserve approved reference constraints.
2. Choose a framing and camera instruction if needed. Pair shorthand with meaning: “medium close-up (MCU), roughly chest-up”; “truck right, moving sideways past the foreground pillar.” Professional terminology varies by crew, and lens numbers are not calibrated generative controls.
3. Separate camera travel, performer action, focus and edit timing. Name start/end views, the relevant speed profile and any hold. Constant travel through the whole clip cannot also gradually stop within it; define separate phases.
4. Describe lighting direction and shadow quality independently. Then specify shadow detail, palette and finishing only as relevant. Preserve texture and product truth rather than using glow or grain to conceal defects.
5. Give human action a target and physical sequence when needed. Preserve identity and avoid adding age, skin marks or expressions merely as realism decoration.
6. For connected shots, keep a geography/reference plan. Preserve the light source in world space across reverse angles, even if its camera-left/right description changes.
7. Keep supported generation settings separate from visual prose. A written frame rate, shutter angle, duration or hex colour does not prove the output implements it exactly. Retain the user's intended specification and identify any unsupported part.
8. Remove redundant adjectives and contradictory directions. Use relevant model-supported constraints rather than a mandatory generic negative list. Preserve requested text/logos and approved details; if accuracy is essential, identify the asset/compositing work separately.

Read supporting guidance only as needed:

- [Camera](references/camera.md), [motion and pacing](references/motion-and-pacing.md), [lighting and colour](references/light-and-colour.md).
- [Live-action planning](references/cinematography.md), [commerce](references/commerce.md), [animation](references/animation.md), [style and medium](references/style-and-medium.md).
- [Structure](references/structure.md), [timing and format](references/timing-and-format.md), [audio](references/audio.md), [constraints](references/exclusions.md).
- [Research scope and sources](references/craft-sources.md) for the recent findings. Physical principles and creator advice do not establish model success rates.

## Explainers and production roles

For explainer scripts or coverage plans, use [explainer structure and production handoffs](references/explainer-and-production.md). Give each beat a teaching purpose and each shot a reason to exist. Separate the script/shot plan, per-shot generation inputs, output review and editing handoff. Do not treat a planning tool as the renderer or editor without verified support. A camera-only repair does not authorize a new sequence.

## Multi-shot and audio handling

For one multi-shot prompt, put shared context once above the shot blocks. For separately generated shots, include the necessary shared context in every call and use approved reference inputs where supported. Identical wording can reduce ambiguity; it cannot guarantee matching faces, materials, light or music.

Preserve the chosen audio plan. Native dialogue requires documented model support; otherwise give a separate voiceover/lip-sync or edit plan outside the video prompt. Do not replace exact narration with generated on-screen text. A continuous score across separate shots is normally a shared post track, not an assumption that repeated music descriptions produce matching audio. A silent shot may be intentional.

## Deliver

1. Revised or new prompt in a copyable block; return only a replacement clause if that is what the user requested.
2. Brief change notes for a revision, naming the decisions changed.
3. Assumptions, missing reference coverage or unsupported controls only where relevant.
4. One focused output check or comparison to try next. Do not render it automatically.

Keep source citations, setup advice and finishing instructions outside the generation prompt unless they describe requested visible behavior. Do not attach a lecture to a small edit.

## Verification

- Requested edit scope is respected; frozen subject, product, identity, action, audio, brand and format choices survive.
- Camera terms describe compatible behavior; size, angle, path, focus and support are not conflated.
- Timing phases fit a known duration or remain clearly relative; smoothness, speed and blur are separate.
- Source direction, softness, fill and grade agree with the intended view and references.
- Skin/performance instructions preserve the person; product detail does not invent a new condition or capability.
- Independent shots carry required context and geography. Review the intended cut, not only isolated stills.
- Prompt length is checked against a verified endpoint limit if known. Do not claim a universal truncation threshold.
- Negative fields are used only where supported; no duplicated or contradictory exclusions.
- Untested examples are labelled as proposals. Defects may persist because of model limitations, references, settings or stochastic variation.

When reviewing output, watch the whole take at delivery speed, inspect difficult motion, compare start/end identity and light, and change one relevant variable per comparison where practical. A plausible prompt is not evidence that a generated clip passed review.
