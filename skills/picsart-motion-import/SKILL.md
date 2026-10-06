---
name: picsart-motion-import
description: "Stage 1 of the motion pipeline. Bring a Figma design in as layers, not flat frames. Capture each layer in its native format and tag matched elements. Host every asset on a Picsart URL, and set the format and output sizes. Fall back to flat frames only when layers cannot be had. Called by picsart-motion; not a standalone entry point."
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, motion, figma, import]
---

# Motion import

Stage 1 of the motion pipeline: bring a Figma design in as editable layers.

## When to Use

- Stage 1 of the motion pipeline, called by picsart-motion.
- Not a standalone entry point.

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
| Split text that builds across frames | [motion patterns](../picsart-motion/references/motion-patterns.md) |
| Set match keys for the frame diff | [motion principles](../picsart-motion/references/motion-principles.md) |
| Before writing `motion.json` | [state](../picsart-motion/references/state.md) |

## Procedure

Run the steps in [the workflow](references/workflow.md) in order.
Called by [picsart-motion](../picsart-motion/SKILL.md).

## Pitfalls

- Import layers, not flat frames. A flat frame while its layers exist fails the gate.
- Keep text as live text and vectors as vectors. Use PNG only for raster content.
- Import every element the design shows. Omit only designer-hidden layers.
- Tag matched elements with a `matchKey` across frames.
- Lift every asset to a Picsart-hosted `https://` URL before you bind it.
- Announce a flat fallback, and say plainly what is lost.

## Verification

Print the Stage 1 gate with ✓/✗. Then continue with Stage 2 in [picsart-motion](../picsart-motion/SKILL.md).
