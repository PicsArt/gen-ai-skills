---
name: picsart-delivery-check
description: Check and export a finished Picsart scene. Use for final media delivery, render results, and confirmed file links.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, export, delivery]
---

# Delivery check

Check a finished Picsart scene against its brief, then export it and confirm the file links.

## When to Use

- Check and export a finished scene for final media delivery.
- Confirm render results and the file links the export returns.

## Prerequisites

- The `picsart` MCP server is connected.
- Read the [interface map](../picsart-workflows/references/interface-map.md).

## How to Run

Use the final accepted scene, including returned editor edits.

## Quick Reference

- Tools: `picsart_media_validate_scene`, `picsart_media_contact_sheet`, `picsart_media_export`, `picsart_media_translate_scene`.

## Procedure

1. Match the brief's dimensions, duration, frame rate, container, and caption requirements. Check the first and last frames, clip joins, text, and audio. Record limits that affect delivery.
2. Run `picsart_media_validate_scene` after direct changes. Fix errors by their paths and codes. Treat warnings according to their effect on the output. A current patch result with `valid: true` already provides validation.
3. Use `picsart_media_contact_sheet` to inspect specific scene times before export. Include a critical caption, a join, and the final visible state as needed. This call renders frames.
4. Use the editor for motion and audio review. A contact sheet cannot establish either.
5. For a requested file, use `picsart_media_export`. Set the supported `mediaType` and delivery options. Default output is MP4. For an editable project, use `picsart_media_translate_scene` after validation.
6. Follow an export receipt's stated status tool with the unchanged `job`. Report success only after the output result arrives. Check returned dimensions and duration when available. Allow frame rounding in duration checks.
7. Give `downloadUrls` to the user for saving. Use matching `urls` for further tool inputs. Confirm a Drive save only when a returned `driveUid` proves it.

## Pitfalls

- Do not retry only because some frames returned URLs without inline images.
- Schema and geometry checks cannot prove successful rendering.

## Verification

- Deliver the final links and a short check result.
- State any failed render, missing review, or unverified delivery requirement.
