---
name: picsart-scene-portability
description: Package an editable Picsart scene for handoff or archival, retaining dependencies and translating to supported Replay or Jet projects.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, handoff, export]
---

# Scene portability

Package an editable Picsart scene with its dependencies and translate it for another editor or archive.

## When to Use

- Hand off or archive an editable scene with its dependencies.
- Translate a scene to a supported Replay or Jet project.

## Prerequisites

- The `picsart` MCP server is connected.
- Read [media production](../picsart-workflows/references/media-production.md) for scene persistence, translation, and renderer checks.
- Read [remote resources](../picsart-workflows/references/remote-resources.md) when dependency URLs need durable storage.

## How to Run

Follow the Procedure below.

## Quick Reference

- Tools: `picsart_media_resolve_looks`, `picsart_media_expand_scene_ref`, `picsart_media_translate_scene`.

## Procedure

1. Identify the receiving editor, rendering engine, and required level of editability.
2. Snapshot the accepted scene and record its revision and capability build.
3. Inventory source media, fonts, templates, looks, external references, and destination access requirements.
4. Resolve by-reference looks through `picsart_media_resolve_looks` when removing look-catalog dependencies.
5. Expand resolvable scene references through `picsart_media_expand_scene_ref` when editable layers are required.
6. Inspect remaining references after each expansion; nested references can require further calls.
7. Retain unresolved remote or track references explicitly in the dependency inventory.
8. Validate the resulting scene before translation.
9. Translate through `picsart_media_translate_scene` with the supported engine: `v3` for Replay or `jet`.
10. Save the complete returned project without truncating its JSON.
11. Check destination loading, sampled frames, playback, and audio when the receiving environment is available.
12. Deliver the source revision, project, dependencies, validation results, and remaining compatibility limitations.

## Pitfalls

- Scene-reference expansion does not fetch remote HTTP references or detach track-clip references.
- Resolved looks remove preset dependencies; they do not embed remote media or fonts.
- Translation returns a project, rather than a final media export or confirmed cloud save.
- Keep the accepted source separate from the handoff copy.

## Verification

- When destination checks are unavailable, report compatibility as unverified.
