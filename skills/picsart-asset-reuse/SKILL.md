---
name: picsart-asset-reuse
description: Reuse characters, props, locations, and cast from the shared Picsart Drive Library or an existing film.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, asset-reuse, drive-library, film-assets]
---

# Asset reuse

Find and attach existing references before a Picsart workflow creates new ones.

## When to Use

- A task needs characters, props, locations, or cast that may already exist in the shared Drive Library.
- A film needs its own registered references, or a new film reference needs review and a lock.

## Prerequisites

- The `picsart` MCP server is connected.
- Read [the interface map](../picsart-workflows/references/interface-map.md) for film registry and upload calls.

## How to Run

Use [Library](../picsart-library/SKILL.md) to find shared references and select their roles.

## Quick Reference

### Reference selection

- For a default image, prefer a verified sheet, collage, primary view, then another suitable view.
- Keep source sheets and voice carriers separate from visual views.
- If semantic metadata is missing, report filename selection as provisional.

## Procedure

1. Start with assets already supplied for this task.
2. Search the shared Library for characters, props, and locations before new generation.
3. Keep the selected reference records and their metadata confidence.
4. For a film's references, use `picsart_list_assets` with `projectFolderUid` and `scope: "library"` separately.
5. Read available descriptions and reference roles. Confirm that the asset fits the requested use.
6. Record the source asset folder ID, category, plain URLs, and selected roles.
7. Keep the original asset when the task requires a revised version.
8. Attach the plain URL through a supported model or scene field.

### Lock a new film reference

For a new film reference, open `picsart_asset_review` when user acceptance is needed.
Wait for the actual verdict.
Use `picsart_save_asset` with the approved sheet, descriptor, and `status: "locked"`.

## Pitfalls

- Do not create folders during discovery or move the source asset between tools.
- Do not use download URLs or filesystem paths as MCP generation inputs.
- Film registry saves and generation saves do not automatically publish into the shared Library.
- Do not infer a film lock from membership in the shared Library.

## Verification

- Report a lock only when the returned `locked` value confirms it.
- Return the selected assets and any unresolved reference requirements.
