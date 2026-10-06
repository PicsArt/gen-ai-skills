---
name: picsart-film-edit
description: "Edit the film from selected takes to the cut the user calls final. Covers assembly, join repair, reshoot orders, review and the user's final cut. Use for Stages 7-8 once scenes have selects, or to improve a join between existing clips. Routed from picsart-film. A one-off montage needs no pipeline."
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, film, edit]
---

# Film edit

Edit the film from selected takes to the cut the user calls final.

## When to Use

- Stages 7-8 of the film pipeline, once scenes have selects.
- To improve a join between existing clips.
- Not for a one-off montage; it needs no pipeline.

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
| Assembling a scene as one track, with per-seam transitions | [Assembly](references/assembly.md) |
| A join between two clips needs repair | [Join repair](references/join-repair.md) |

## Procedure

Previous stage: [picsart-film-scenes](../picsart-film-scenes/SKILL.md). Send reshoot orders back there as new shot cards.
Next stage: [picsart-film-finishing](../picsart-film-finishing/SKILL.md), after the user calls the cut final.

## Pitfalls

- Cut from selects only, never the raw generation pile.
- Diagnose a bad join before repairing it. A repair is not automatically a model call.
- State what changes, what stays, and the cost before any charged order.
- Open `picsart_scene_editor` once for the whole cut, not per clip.
- The fine cut and polish run in `picsart_scene_editor`. The document it returns with the user's verdict is the cut; `picsart_media_export` renders the file from it.
- Upload the rendered file to `picsart_drive`. Keep the edited scene document in the workspace project folder and record its path in `film.json`.

## Verification

- Approval is the user's actual decision: a submitted verdict, or an explicit text answer when the editor is unavailable.
- Opening or previewing the editor is never approval.
