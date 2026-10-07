---
name: picsart-video-edit
description: Assemble or change an existing Picsart video scene. Use for trim, sequence, crop, speed, and transitions.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, video, editing]
---

# Video edit

Cut, order, and time video clips in an editable Picsart scene.

## When to Use

- Assemble clips into a new video scene or change an existing one.
- Trim, sequence, crop, change speed, and add transitions.

## Prerequisites

- The `picsart` MCP server is connected.
- Read the [interface map](../picsart-workflows/references/interface-map.md).

## How to Run

Use the Picsart app media tools for scene edits.

## Quick Reference

- Tools: `picsart_media_upload`, `picsart_media_probe_media`, `picsart_media_quickstart`, `picsart_media_apply_scene_template`, `picsart_media_patch_scene`, `picsart_scene_editor`.

## Procedure

1. Set the target size, frame rate, and duration from the brief. Keep the approved source order.
2. Use `picsart_media_upload` for local files. Wait for the upload response. Use `picsart_media_probe_media` when source dimensions or duration are unknown. Do not treat absent duration as zero.
3. For sequential clips, start with `picsart_media_quickstart` and recipe `concat_videos`. Build its montage with `picsart_media_apply_scene_template`, mode `bootstrap`. Use separate overlapping layers for picture-in-picture.
4. Edit with `picsart_media_patch_scene`. Address layers by ID. Use slash-separated paths. Keep the returned scene for the next edit.
5. Set explicit source trim bounds for speed changes. Adjust the layer duration to the intended playback length. Mute reversed video audio. Negative video speed does not reverse its sound.
   To preserve forward speech, add an audio layer from the same video source with positive speed and matching trim.
6. Check the crop on important subjects and text. Use `contain` to keep the full picture. Use `cover` only when the crop fits the brief.
7. Validate after direct edits. A patch result with `valid: true` already passes validation.
   Expand scene references before `picsart_scene_editor`. Inspect `stillReferenced` after each expansion.
   Expand nested references again. If remote references remain unresolved, report the editor limitation.
   Check seams and motion in the editor.

## Pitfalls

- Do not treat editor approval as a rendered file.

## Verification

- Use the editor's returned document after user edits.
- Use [delivery check](../picsart-delivery-check/SKILL.md) when the user requests an export.
