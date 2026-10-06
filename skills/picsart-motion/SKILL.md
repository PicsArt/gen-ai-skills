---
name: picsart-motion
description: "Turn Figma layers or uploaded assets into a motion-designed ad or reel. Use to animate a design or assets, or to add motion to a Figma flow. Also use to make an ad or reel from images or screens. Not for stitching edited footage or text-to-video."
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, motion, figma]
---

# Motion

Turn Figma layers or uploaded assets into a motion-designed ad or reel through the motion pipeline.

## When to Use

- To animate a design or assets, add motion to a Figma flow, or make an ad or reel from images or screens.
- Not for stitching edited footage or text-to-video.

## Prerequisites

The `picsart` MCP server is connected.
Read [host conventions](../picsart-workflows/references/host-conventions.md) first, including its motion server section.
Read [the interface map](../picsart-workflows/references/interface-map.md) before tool calls and cost checks.
Read [media production](../picsart-workflows/references/media-production.md) for review evidence.

## How to Run

Read [the overview](references/overview.md) in full when this skill starts.
Read each file below in full before its step.

## Quick Reference

| When | Read |
| --- | --- |
| Stage 1 | [picsart-motion-import](../picsart-motion-import/SKILL.md) |
| Stage 2 | [stage](references/stage-2-compose.md), [assets](references/asset-composition.md), [fundamentals](references/compose-fundamentals.md), [Figma](references/authoring-flow.md) |
| Stage 3 | [picsart-motion-design](../picsart-motion-design/SKILL.md), [stage](references/stage-3-motion.md), [principles](references/motion-principles.md), [choreography](references/choreography.md), [elements](references/element-motion.md), [patterns](references/motion-patterns.md), [transitions](references/transitions.md) |
| Tool choice | [routing](references/tool-routing.md), [vocabulary](references/mp-scene-vocabulary.md) |
| Validation errors | [validation](references/scene-validation.md), [engine](references/engine-gotchas.md), [troubleshooting](references/motion-troubleshooting.md) |
| Editor feedback | [feedback](references/widget-feedback.md), [editor](references/mp-scene-editor-widget.md) |
| Uploaded assets or no brief | [working mode, propose](references/propose-mode.md) |
| Video generation | [generation](references/video-generation.md) |
| Before writing `motion.json`; costs | [state](references/state.md) |
| Studying motion | [studying](references/studying-motion.md) |

## Procedure

Run the stages in the Quick Reference order, starting at Stage 1.

## Pitfalls

- Keep layers editable. Flat frames are only the honest fallback.
- `picsart_media_import_figma_paint` takes CSS paint values. It does not fetch a Figma file.
- Read its `skipped` result before any fallback.
- A rendered screenshot does not establish hidden layer geometry. Rebuild each frame from its layer tree.
- Report each loss of editability when you flatten an element.
- Video generation is opt-in. Get an explicit yes on its shown cost.
- Export and save to Drive only on request.

## Verification

- Approval is the user's actual decision: a submitted verdict, or a text answer when the editor or payload is unavailable. Opening or previewing the editor is never approval.
