---
name: picsart-film
description: "Make a narrative AI film with recurring characters through the 11-stage Picsart pipeline. Use for a film, short film, movie, episode, multi-scene story, or script. Not for one clip from a description or stitching existing footage."
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, film, pipeline]
---

# Film

Route a narrative AI film through the 11-stage Picsart pipeline, one stage skill at a time.

## When to Use

- A film, short film, movie, episode, multi-scene story, or script with recurring characters.
- Not for one clip from a description or stitching existing footage.

## Prerequisites

The `picsart` MCP server is connected.
Read [host conventions](../picsart-workflows/references/host-conventions.md) first. They apply to this skill and its references.
Read [the interface map](../picsart-workflows/references/interface-map.md) before tool calls and cost checks.
Read [media production](../picsart-workflows/references/media-production.md) for production receipts.

## How to Run

Read [the overview](references/overview.md) in full when this skill starts.
Read each file below in full before its step.

## Quick Reference

| When | Read |
| --- | --- |
| Stage 1 | [development](../picsart-film-development/SKILL.md) |
| Stages 4–5 | [assets](../picsart-film-assets/SKILL.md) |
| Stage 6 | [scenes](../picsart-film-scenes/SKILL.md) |
| Stages 7–8 | [edit](../picsart-film-edit/SKILL.md) |
| Stages 9–11 | [finishing](../picsart-film-finishing/SKILL.md) |
| Planning or advancing a stage | [stages](references/stages.md) |
| Stage cards, gates, mistakes | [pipeline](references/pipeline.md) |
| Creating or resuming the project | [workspace](references/workspace.md) |
| Any tool or endpoint error | [outages](references/outages.md) |
| Before choosing or changing a model | [model policy](references/model-policy.md) |
| Film setup presets | [looks](references/presets-looks.md) |
| Shared review-board feedback | [review feedback](references/review-feedback.md) |
| Film-board feedback | [widget feedback](references/widget-feedback.md) |

## Procedure

Run the stages in the Quick Reference order, from Stage 1 to Stages 9–11.

## Pitfalls

- Generate nothing for a scene until its assets are locked.
- Verify literal generation arguments with `picsart_prompt_verify` before dispatch.
- Generate with `async: true` and persist every original job handle immediately.
- After a dropped call, check `picsart_job_status`. Never resubmit.
- Reuse Library characters, props, and locations with [asset reuse](../picsart-asset-reuse/SKILL.md).

## Verification

- Approval is the user's actual decision: a submitted verdict. It can be an explicit text answer when the board or payload is unavailable. Opening or previewing a board is never approval.

Finish requested exports with [delivery checks](../picsart-delivery-check/SKILL.md).
