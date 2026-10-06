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
| Connect | [Connect](../picsart-connect/SKILL.md) |
| Generate | [Model choice](../picsart-model-choice/SKILL.md), [Generate](../picsart-generate/SKILL.md) |
| Browse resources | [Library](../picsart-library/SKILL.md) |
| Reuse references | [Asset reuse](../picsart-asset-reuse/SKILL.md) |
| Publish or save resources | [Resource library](../picsart-resource-library/SKILL.md) |
| Plan shots | [Storyboard](../picsart-storyboard/SKILL.md), [Continuity](../picsart-character-continuity/SKILL.md) |
| Social ad | [Social ad](../picsart-social-ad/SKILL.md) |
| Product images | [Product shoot](../picsart-product-shoot/SKILL.md) |
| Product mockup | [Mockup](../picsart-product-mockup/SKILL.md) |
| Image change | [Image edit](../picsart-image-edit/SKILL.md) |
| Exact image derivatives | [Finishing](../picsart-image-finishing/SKILL.md) |
| Merge or trim clips | [Video edit](../picsart-video-edit/SKILL.md) |
| Revise accepted scene | [Revision](../picsart-scene-revision/SKILL.md) |
| Repurpose footage | [Repurpose](../picsart-video-repurpose/SKILL.md) |
| Remove video background | [Cutout](../picsart-video-cutout/SKILL.md) |
| Graphics | [Scene design](../picsart-scene-design/SKILL.md) |
| Music-timed montage | [Beat edit](../picsart-beat-edit/SKILL.md) |
| Adapt master | [Scene variants](../picsart-scene-variants/SKILL.md) |
| Data-driven exports | [Variable data](../picsart-variable-data/SKILL.md) |
| Compare generated versions | [Batch variants](../picsart-batch-variants/SKILL.md) |
| Brand | [Brand kit](../picsart-brand-kit/SKILL.md) |
| Captions | [Captions](../picsart-captions/SKILL.md) |
| Narration | [Voiceover](../picsart-voiceover/SKILL.md) |
| Music or effects | [Music](../picsart-music-bed/SKILL.md), [Effects](../picsart-sound-effects/SKILL.md), [Mix](../picsart-audio-mix/SKILL.md) |
| Cover | [Thumbnail](../picsart-thumbnail/SKILL.md) |
| Explain | [Explainer](../picsart-explainer/SKILL.md) |
| Presenter | [Presenter](../picsart-presenter/SKILL.md) |
| Cartoon | [3D cartoon](../picsart-3d-cartoon/SKILL.md) |
| Interrupted job | [Recovery](../picsart-job-recovery/SKILL.md) |
| Editable handoff | [Portability](../picsart-scene-portability/SKILL.md) |
| CTV file | [CTV](../picsart-ctv-delivery/SKILL.md) |
| Final files | [Delivery](../picsart-delivery-check/SKILL.md) |
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
