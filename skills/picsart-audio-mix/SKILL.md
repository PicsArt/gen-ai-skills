---
name: picsart-audio-mix
description: Arrange and balance existing voice, music, and sound in a Picsart scene. Use for levels, trims, fades, and timing.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, audio, mixing]
---

# Audio mix

Balance voice, music, and effect layers that already exist in a Picsart scene.

## When to Use

- Set levels, trims, fades, and timing for existing voice, music, or sound in a scene.
- Not for new music or effects; generate them first, then mix them here.

## Prerequisites

- The `picsart` MCP server is connected.
- Read the [interface map](../picsart-workflows/references/interface-map.md).

## How to Run

Use existing authorized audio sources.

## Quick Reference

- Tools: `picsart_media_patch_scene`, `picsart_media_analyze_audio`.

## Procedure

1. Identify each sound's role: voice, music, or effect. Keep speech clear at important story points.
2. Read the `audioAuthoring` capability section. Fetch the audio and animation schema definitions before authoring fields.
3. Add each separate sound as a layer with `content.kind: "audio"`. Set its source, `start`, `duration`, and trim. Do not use `scene.audio` or insert audio into a visual track's clips.
4. Use `content.volume` from 0 to 100. Use `content.muted` to silence a source. Control a video's embedded sound on its media layer.
5. Use `animations.volume` for fades or planned music dips under speech. Set `timeMode` explicitly when keyframes need layer-local time. Use `picsart_media_patch_scene` with layer IDs. Keep its returned scene.
6. Use `picsart_media_analyze_audio` only when beat timing or energy measurements help the edit. Follow its job receipt. Treat low confidence and absent measurements as uncertainty.
7. Listen across joins and overlaps. Check for duplicate source audio, abrupt cuts, masked speech, and sound beyond the picture's end. Validate direct scene edits.

## Pitfalls

- Do not claim automatic ducking, noise removal, stem separation, or loudness normalization. These operations are not established by the verified media interface.
- Do not equate a volume percentage with LUFS or peak level.

## Verification

- Use [delivery check](../picsart-delivery-check/SKILL.md) for an export.
- Report any required audio measurement that remains unavailable.
