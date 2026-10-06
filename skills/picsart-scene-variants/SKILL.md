---
name: picsart-scene-variants
description: Adapt an accepted Picsart scene to new ratios, copy, languages, products, or brand treatments while reusing unchanged material.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, variants, localization]
---

# Scene variants

Make variants of an accepted Picsart scene and reuse the material that does not change.

## When to Use

- Adapt an accepted scene to new ratios, copy, languages, products, or brand treatments.
- Not for structured data rows or Replay variables; use variable data for those.

## Prerequisites

- The `picsart` MCP server is connected.
- Read [production state](../picsart-workflows/references/media-production.md) for master versions and output manifests.
- Read [remote resources](../picsart-workflows/references/remote-resources.md) before replacing assets or styles.

## How to Run

Follow the Procedure below.

## Quick Reference

- Tools: `picsart_media_list_recipes`, `picsart_media_get_recipe`.
- For structured rows and Replay variables, use [variable data](../picsart-variable-data/SKILL.md).

## Procedure

1. Obtain the accepted master scene and its source version.
2. Define each variant's ratio, copy, locale, product, and delivery target.
3. Preserve the master snapshot.
4. Search supplied assets and remote resources before generation.
5. Reuse unchanged media and approved brand assets.
6. Discover applicable native recipes with `picsart_media_list_recipes` when authoring detail is needed.
7. Fetch the chosen recipe with `picsart_media_get_recipe`.
8. Create a separate scene revision for each variant.
9. Keep stable IDs for corresponding layers across variants.
10. Bind exact supplied copy and product assets.
11. If translation is required, distinguish draft translation from supplied approved copy.
12. Recompute layout and crops for the target ratio.
13. Resolve fonts that support the target script.
14. Check wrapping, reading time, safe margins, product identity, and subject visibility.
15. Inspect motion and audio when changed timing affects them.
16. Keep every returned scene after patches or editor changes.
17. Validate direct edits and inspect rendered previews.

## Pitfalls

- Do not stretch a final render when the new ratio requires layout changes.

## Verification

- Use [delivery check](../picsart-delivery-check/SKILL.md) for requested exports.
- Return each editable variant with its master version, changes, review status, and output receipt.
