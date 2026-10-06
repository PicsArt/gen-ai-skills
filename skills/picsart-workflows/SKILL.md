---
name: picsart-workflows
description: Route Picsart MCP media-production work to the right picsart-* skill and hold the shared references (interface map, Drive library, media production, remote resources, host conventions). Use when a Picsart image, video, audio, scene or delivery task needs a workflow choice, or when another picsart-* skill links a shared contract. Not for one-off terminal generation with the gen-ai CLI; use gen-ai-use.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, workflows, routing, media-production]
---

# Picsart Workflows

Select the Picsart skill for a media-production request. This skill also holds the references that the other `picsart-*` skills share.

## When to Use

- The user asks for Picsart media work and the matching skill is not yet clear.
- Another `picsart-*` skill links a shared reference in `references/`.
- Not for a single terminal generation with the gen-ai CLI; use [gen-ai-use](../gen-ai-use/SKILL.md).

## Prerequisites

- The `picsart` MCP server is connected (`https://api.picsart.com/gen-ai/mcp`, OAuth on first connect). See [interface map](references/interface-map.md).
- The host rules in [host conventions](references/host-conventions.md) apply to every Picsart skill.

## How to Run

1. Match the request to a row in Quick Reference.
2. Open that skill and follow its procedure.
3. If no row matches, use the [interface map](references/interface-map.md) to pick the tool group directly.

## Quick Reference

| Request | Skill |
| --- | --- |
| Local file to hosted URL | [Add media](../picsart-add-media/SKILL.md) |
| Terminal generation (CLI alternative) | [gen-ai CLI](../gen-ai-use/SKILL.md) |

Shared references:

| Reference | Use for |
| --- | --- |
| [interface-map.md](references/interface-map.md) | Server, tool groups, generation chain, credit rules |
| [drive-library.md](references/drive-library.md) | Shared Drive Library paths, selection, and limits |
| [media-production.md](references/media-production.md) | Scene revision, footage timing, design motion, film, verification |
| [remote-resources.md](references/remote-resources.md) | Resource identity, saves, publication, handoff |
| [host-conventions.md](references/host-conventions.md) | Tool discovery, board decisions, state files, motion server notes |

## Procedure

1. Reuse supplied and remote resources before generation. Check the [Drive Library](references/drive-library.md) first.
2. Carry resource versions, scene revisions, budgets, and job receipts between skills.
3. Confirm requested remote saves with the actual save receipt.
4. Return outputs and unfinished requirements.

## Pitfalls

- Do not retry a paid call after a credit or storage error, or after an ambiguous acceptance. Check job status first.
- Do not hard-code tool names. The host can prefix them; discover the live names and schemas.

## Verification

- The selected skill matches the request type.
- Every output, receipt, and unsaved item is reported to the user.
