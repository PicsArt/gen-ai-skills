---
name: picsart-film-finishing
description: "Finish the film: colour unification and grade, the final-resolution pass, masters, and the project archive. Decide the soundtrack: keep generation audio, add a music bed, or hand off to a sound team. Use for Stages 9-11 of the film pipeline, after picture lock and cleanup. Routed from picsart-film."
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, film, finishing]
---

# Film finishing

Finish the film: grade, final-resolution pass, soundtrack decision, masters and archive.

## When to Use

- Stages 9-11 of the film pipeline, after picture lock and cleanup.
- Deciding the soundtrack: keep generation audio, add a music bed, or hand off to a sound team.

## Prerequisites

The `picsart` MCP server is connected.
Read [host conventions](../picsart-workflows/references/host-conventions.md) first. They apply to this skill and its references.
Read [the interface map](../picsart-workflows/references/interface-map.md) before tool calls and cost checks.

## How to Run

Read [the workflow](references/workflow.md) in full when this skill starts.
Read each file below in full before its step.

## Quick Reference

| When | Read |
| --- | --- |
| Stage 11 QC, masters, promo reframes and the archive | [Delivery](references/delivery.md) |

## Procedure

Previous stage: [picsart-film-edit](../picsart-film-edit/SKILL.md).
Picture lock is behind this stage. Nothing here changes the cut.

## Pitfalls

- Keep the fixed order: final-resolution re-roll, re-assemble, grade, export once, masters, archive.
- The final pass is a fresh roll, not an upscale. Quote it and wait for the user.
- Never grade the draft. Grade the final pixels.
- The generated voice is the performance. Never re-record generated dialogue.
- Archive the prompts, registry and log with the film. Write the disclosure pack from the generation log.

## Verification

- Confirm the deliverable list before each export.
