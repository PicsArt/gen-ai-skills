---
name: picsart-library
description: Browse the shared Picsart Drive Library and resolve existing characters, props, locations, and cast for reuse across tools.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, drive-library, asset-discovery]
---

# Shared Library

Resolve characters, props, locations, and brands in the shared Drive Library into reference records.

## When to Use

- A task names a Library asset, folder ID, or category, or needs existing cast before new generation.
- Other tools need reference records with roles and plain URLs from the shared Library.

## Prerequisites

- The `picsart` MCP server is connected.
- Read [the library contract](../picsart-workflows/references/drive-library.md) for reference roles and interface limits.

## How to Run

Use this skill to find existing references before creating replacements.

## Quick Reference

### Paths

- Characters: `/Assets/Library/Characters`.
- Props: `/Assets/Library/Props`.
- Locations: `/Assets/Library/Locations`.
- Brands: `/Assets/Library/Brands`.

## Procedure

1. Identify the requested asset type, name, folder ID, or library mention.
2. Prefer a supplied folder ID when it resolves to the requested category.
3. Otherwise, use `picsart_drive` with `action: "list"` to descend through the canonical folders.
4. Follow pagination. Resolve duplicate names by folder ID and task context.
5. Read the selected folder's description, files, and reference metadata when available.
6. Keep its folder ID as the asset identity. Derive its type from the category parent.
7. Use role and primary tags when present. Use filename fallback only when those tags are absent.
8. For a default image, prefer a verified sheet, collage, primary view, then another suitable view.
9. Keep source-sheet and voice carriers separate from visual views.
10. Return a reference record for each selected asset.

### Attach selected references

Use [asset reuse](../picsart-asset-reuse/SKILL.md) to attach selected references or handle film registry assets.

## Pitfalls

- Start at Drive root. Do not add a `My files` path segment.
- Do not treat a failed read as an empty library.
- Do not create or move folders during discovery.
- A film project's Library and legacy Film Assets are separate stores.

## Verification

Include name, category, folder ID, description, selected roles, plain URLs, and metadata confidence.
If the response omits tags, report filename-based choices as provisional.
