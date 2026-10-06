---
name: picsart-film-scenes
description: "Generate the film's shots in film pipeline Stage 6. Covers final scene shotlists, preset-driven shot design, scene pictures on one board, and one two-part prompt per run of shots. Also covers drafts, surgical iterations, splitting delivered runs, and take selection into selects. Use only after the scene asset sheets are approved. Routed from picsart-film."
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, film, scenes]
---

# Film scenes

Generate the film's shots in Stage 6, from final scene shotlists to selects.

## When to Use

- Stage 6 of the film pipeline: shotlists, shot design, scene pictures, runs, iterations and selects.
- Only after the scene asset sheets are approved.

## Prerequisites

The `picsart` MCP server is connected.
Read [host conventions](../picsart-workflows/references/host-conventions.md) first. They apply to this skill and its references.
Read [the interface map](../picsart-workflows/references/interface-map.md) before tool calls and cost checks.

## How to Run

Read [the overview](references/overview.md) in full when this skill starts.
Read each file below in full before its step.

## Quick Reference

| When | Read |
| --- | --- |
| Step 1, final scene shotlist | [shotlist](references/step-1-shotlist.md) |
| Step 2, shot design | [shot design](references/step-2-shot-design.md) |
| Step 3, scene pictures | [scene pictures](references/step-3-scene-pictures.md) |
| Steps 4–5, runs and iterations | [runs](references/step-4-5-runs.md) |
| Steps 6–7, selects and conveyor | [selects](references/step-6-7-selects.md) |
| Prompt assembly | [prompt blocks](references/prompt-blocks.md), [prompt verify](references/prompt-verify.md) |
| Camera, lighting, or acting presets | [camera](references/presets-camera.md), [lighting](references/presets-lighting.md), [acting](references/presets-acting.md) |
| Joins and seams | [seams](references/seams.md) |

## Procedure

Previous stage: [picsart-film-assets](../picsart-film-assets/SKILL.md). Next stage: [picsart-film-edit](../picsart-film-edit/SKILL.md). Routed from [picsart-film](../picsart-film/SKILL.md).

## Pitfalls

- Generate only after the scenes' asset sheets are approved. No run starts until every scene it spans is locked.
- Quote every charged video call with `picsart_preflight`. Dispatch only after the user's yes to that number.
- Never fill `startFrame`. Put every person's identity and wardrobe views in `imageUrls`.
- After a timeout, poll `picsart_job_status` first. Never resubmit.

## Verification

- Approval is the user's actual decision: a submitted verdict. It can also be an explicit text answer when the board or payload is unavailable. Opening or previewing a board is never approval.
