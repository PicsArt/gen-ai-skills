---
name: picsart-scene-design
description: Build Picsart title cards, overlays, and product cards with editable text, shapes, media, and motion.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, design, motion]
---

# Scene design

Build editable Picsart scenes from templates, text, shapes, media, and motion.

## When to Use

- Build title cards, overlays, or product cards.
- Keep text, shapes, media, and motion editable in the scene.

## Prerequisites

- The `picsart` MCP server is connected.
- Read the [interface map](../picsart-workflows/references/interface-map.md).

## How to Run

Set the output size, message, and visible hierarchy from the brief.

## Quick Reference

- Tools: `picsart_media_get_capabilities`, `picsart_media_list_scene_templates`, `picsart_media_apply_scene_template`, `picsart_media_list_fonts`, `picsart_media_patch_scene`, `picsart_media_query_layout`, `picsart_media_layout_lint`, `picsart_scene_editor`.

## Procedure

1. Read only the required sections of `picsart_media_get_capabilities`. Use `picsart_media_list_scene_templates` to find a suitable structure. Describe a chosen template before binding its parameters.
2. Use `picsart_media_apply_scene_template` with mode `bootstrap` for a complete editable scene. Use mode `inline` to add template layers to an existing scene. Keep stable layer IDs.
3. Use `picsart_media_list_fonts` before adding text. Use its font key or declare its font asset.
4. Fetch the required schema definitions. Add or change layers with `picsart_media_patch_scene`. Keep the returned document.
5. Read an effect or motion preset's parameters before using it. Use the matching apply tool.
6. Start an entrance text animation at the text layer's `start`. The apply tool adds no delay parameter. Keep motion within the message's reading window.
7. Validate direct edits. Use `picsart_media_query_layout` for geometry. Use `picsart_media_layout_lint` for suspected overlaps. Inspect its limits; a clean result does not prove visible output.
8. Expand scene references before opening `picsart_scene_editor`. Check the beginning, transitions, and final state. Use the user's returned document after edits.
   Inspect `stillReferenced` after expansion. Expand nested references again. Report unresolved remote references before editor review.

## Pitfalls

- Do not pass an unverified CSS font name.
- Do not reuse parameter names between effects.

## Verification

- Use [delivery check](../picsart-delivery-check/SKILL.md) for a final file.
- Report missing assets or unresolved layout checks.
