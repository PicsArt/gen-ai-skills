---
name: picsart-scene-revision
description: Revise selected parts of an existing Picsart scene while preserving its accepted footage, timing, and source version.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, editing, revision]
---

# Scene revision

Change selected parts of an existing Picsart scene and leave the accepted parts as they are.

## When to Use

- Revise selected layers, assets, or timing in an existing scene.
- Keep the accepted footage, timing, and source version intact.

## Prerequisites

- The `picsart` MCP server is connected.
- Read [production state](../picsart-workflows/references/media-production.md) for snapshots, receipts, and review limits.
- Read [remote resources](../picsart-workflows/references/remote-resources.md) before replacing assets.

## How to Run

Follow the Procedure below.

## Quick Reference

- Tools: `picsart_media_list_recipes`, `picsart_media_get_recipe`, `picsart_media_patch_scene`, `picsart_scene_editor`.

## Procedure

1. Obtain the latest scene document and requested changes.
2. Preserve its source version and an unchanged snapshot.
3. Search supplied assets, the remote Library, and relevant catalogs before generating replacement material.
4. Discover applicable native recipes with `picsart_media_list_recipes`.
5. Fetch the selected recipe with `picsart_media_get_recipe` when its authoring detail is needed.
6. Map each requested change to stable layer or asset IDs.
7. Read the exposed schema before changing unfamiliar fields.
8. Apply atomic changes with `picsart_media_patch_scene` and slash-separated paths.
9. Keep the returned scene for the next change.
10. Compare the revision against the snapshot for unintended changes.
11. If a patch reports `valid: true`, do not repeat structural validation.
12. Validate direct edits and repair reported errors.
13. Review changed intervals and their joins with surrounding material.
14. Expand references before opening `picsart_scene_editor`.
15. Use the editor's returned document after user changes.

## Pitfalls

- If only a rendered file exists, explain that its hidden layers cannot be recovered exactly.
- Use supported footage edits or obtain the editable source.
- Keep exact text and logos as editable layers when available.

## Verification

- Use [delivery check](../picsart-delivery-check/SKILL.md) for requested exports.
- Return the new revision, change list, source version, and completed review evidence.
