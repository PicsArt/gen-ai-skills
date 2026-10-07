---
name: picsart-variable-data
description: Export personalized assets from structured rows and one scene template through the picsart MCP, patching the scene per row and exporting each. Use for name cards, localized banners, or per-store variants from a CSV or table. Not for open-ended creative variants (use picsart-scene-variants).
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, variable-data, template, batch]
---

# Variable Data

Turn rows of data and one template into one export per row.
Bind the template once, patch its fields per row, and export each patched scene.

## When to Use

- The user has rows (CSV, sheet, list) and a fixed layout to fill per row.
- Not for creative variations without data (use [scene variants](../picsart-scene-variants/SKILL.md) or [batch variants](../picsart-batch-variants/SKILL.md)).

## Prerequisites

- The `picsart` MCP server is connected. See the [interface map](../picsart-workflows/references/interface-map.md).
- Row images have public URLs. Read [remote resources](../picsart-workflows/references/remote-resources.md) before you select templates, fonts, or artwork.

## How to Run

1. Find a template with `picsart_media_list_scene_templates`, or use an approved scene.
2. Read its parameters with `picsart_media_describe_scene_template` (`uri`).
3. Bake an editable base scene with `picsart_media_apply_scene_template` (`uri`, `mode: "bootstrap"`, `parameters`).
4. Per row, apply `picsart_media_patch_scene` (`scene`, `ops`) with `set` ops on the variable layers.
5. Per row, render with `picsart_media_export` (`scene`, `mediaType`, `fileName`).

## Quick Reference

| Step | Tool | Key fields |
| --- | --- | --- |
| Discover | `picsart_media_list_scene_templates` | `id`, `uri`, `width`, `height` |
| Variables | `picsart_media_describe_scene_template` | `parameters` (type, required, default) |
| Base scene | `picsart_media_apply_scene_template` | `mode: "bootstrap"` |
| Row values | `picsart_media_patch_scene` | `{op:"set", layer:"<id>", path:"content/text", value:"..."}` |
| Text fit | `picsart_media_layout_lint` | overflow and clipping |
| Fonts | `picsart_media_list_fonts` | locale coverage |
| Output | `picsart_media_export` | `mediaType`: `png`, `jpeg`, `webp`, `mp4`, ... |

## Procedure

1. Record the accepted template URI or scene revision and every source URL.
2. Map each column to a declared parameter or a layer field. Reject columns with no target.
3. Give each row a stable, unique ID. Duplicate names must not collapse distinct rows.
4. Check required fields, missing values, image access, and locale fonts before any export.
5. Patch one row, lint it, and check a frame with `picsart_media_contact_sheet`.
6. After that row passes, patch and export the rest. Use `fileName` with the row ID.
7. Keep each export's job receipt. Poll `picsart_job_status` until it finishes.
8. Match every row to its output URL or a recorded failure. Retry only rows whose failure is established.
9. Save outputs with `picsart_drive` (`action: "upload"`, up to 10 `files` per call) when the user needs storage.

## Pitfalls

- **Coverage:** this route makes one patch and one export per row, so large batches take one call pair per row. Output formats are the ones `picsart_media_export` supports; there is no PDF output.
- Do not loop paid calls after a credit or storage error. Stop and report the remaining rows.
- Long localized text can overflow. Lint every row, not only the first.

## Verification

- Count outputs against rows. Every row ID has a URL or a failure reason.
- Inspect representative outputs for wrapping, artwork, and localization.
- Return the row-to-output manifest, failed rows, template revision, and receipts.
- An export receipt does not prove a stored file. Report a save only with a `driveUid` or Drive receipt.
