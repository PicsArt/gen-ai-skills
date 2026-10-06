---
name: picsart-film-assets
description: "Produce and lock film assets. Make one T-cut sheet per generated character, the portrait, profile and sheet route for a supplied photograph, and prop plates. Review each asset as it arrives, then cut approved sheets into single-view references. Use for Stages 4-5 after the shot list, before picsart-film-scenes. Preserve user photographs and approve each asset before use."
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, film, assets]
---

# Film assets

Produce, review and lock the film's character sheets, photo routes and prop plates.

## When to Use

- Stages 4-5 of the film pipeline, after the shot list and before picsart-film-scenes.
- Any film asset that must be approved before use, including a supplied photograph.

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
| Before preparing image prompts or scheduling asset work | [Asset efficiency](references/asset-efficiency.md) |
| Sheets, descriptors, the asset record, user photographs, cutting views | [Asset sheets](references/asset-sheets.md) |
| Opening `picsart_asset_review` or reading its feedback | [Asset review board](references/asset-review-widget.md) |

## Procedure

Compile each sheet or plate with `picsart_film_compile_asset_prompt`, generate it with `picsart_generate`, review it on `picsart_asset_review`, and lock it with `picsart_save_asset`.

Previous stage: [picsart-film-development](../picsart-film-development/SKILL.md).
Next stage: [picsart-film-scenes](../picsart-film-scenes/SKILL.md), once every scene a run spans is covered.

## Pitfalls

- A user's photograph is the asset. Save it byte-for-byte and never re-encode, enhance or restyle it.
- Never generate a lookalike from a descriptor when the user gave the real face.
- Approve each asset before it is locked or used. Nothing is decided by silence.
- Never pass a multi-panel sheet to the video model. Cut it into single views.
- Register assets only with `picsart_save_asset`. Read the library instead of remembering it.

## Verification

- Approval is the user's actual decision: a submitted verdict, or an explicit text answer when the board is unavailable.
- Opening or previewing a board is never approval.
