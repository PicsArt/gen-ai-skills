---
name: picsart-motion-design
description: "Stage 3 of the motion pipeline. Turn a composed, layered scene into a motion-designed ad. Choose motion per element by role and author matched-element smart-animate between frames. Review it pair by pair in the scene editor (picsart_scene_editor). Called by picsart-motion."
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, motion, animation]
---

# Motion design

Stage 3 of the motion pipeline: turn a composed, layered scene into a motion-designed ad.

## When to Use

- Stage 3 of the motion pipeline, called by picsart-motion, once the scene is composed and layered.

## Prerequisites

The `picsart` MCP server is connected.
Read [host conventions](../picsart-workflows/references/host-conventions.md) first. They apply to this skill and its references.
Read [the interface map](../picsart-workflows/references/interface-map.md) before tool calls and cost checks.

## How to Run

Read [the workflow](references/workflow.md) in full when this stage starts.
Read each file below in full before its step.

## Quick Reference

| When | Read |
| --- | --- |
| Map a change to motion, easing and duration | [motion principles](../picsart-motion/references/motion-principles.md) |
| Pace the seam between two frames | [transitions](../picsart-motion/references/transitions.md) |
| Read editor feedback | [scene editor](../picsart-motion/references/mp-scene-editor-widget.md) |

## Procedure

Called by [picsart-motion](../picsart-motion/SKILL.md).
When every pair is approved, return to Stage 4 in [picsart-motion](../picsart-motion/SKILL.md).

## Pitfalls

- Author one pair A→B at a time. Open the whole scene in `picsart_scene_editor` for each pair.
- Never self-approve by describing the motion.
- Animate only what changed. Leave unchanged layers still.
- Smart-animate matched elements. Do not cross-dissolve shared chrome.
- When feedback has `edited` true, use the returned `document`.
- Keep `picsart_media_export` for the final deliverable and the error fallback.

## Verification

- Approval is the user's actual decision. It is a submitted verdict, or an explicit text answer when the editor or its payload is unavailable. Opening or previewing the editor is never approval.
