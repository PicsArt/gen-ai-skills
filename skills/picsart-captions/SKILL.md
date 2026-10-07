---
name: picsart-captions
description: Add or correct timed captions in a Picsart scene. Use for speech transcripts, speaker labels, and caption styles.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, captions, transcription]
---

# Captions

Add timed, reviewed captions to a Picsart scene from a transcript or the final audio.

## When to Use

- Add new captions or correct existing ones in a scene.
- Work with speech transcripts, speaker labels, and caption styles.

## Prerequisites

- The `picsart` MCP server is connected.
- Read the [interface map](../picsart-workflows/references/interface-map.md).

## How to Run

Follow the Procedure below.

## Quick Reference

- Tools: `picsart_media_transcribe`, `picsart_media_get_scene_schema`, `picsart_media_patch_scene`, `picsart_media_list_fonts`.
- Schema definitions: `MpCaptionsContent`, `MpCaptionStyle`.

## Procedure

1. Use the approved transcript when its timing matches the final cut. Otherwise use `picsart_media_transcribe` on the final audio or video URL. Request `srt` in `include` only when a separate SRT is needed.
2. Follow a returned job receipt with its stated status tool. Keep the `job` object unchanged. Read `notes` for missing word alignment or limited output. Never invent word times.
3. Check spelling, names, numbers, and speaker changes against the recording. Transcription detects speech. Add meaningful sound labels only from verified audio or user evidence.
4. Fetch the `MpCaptionsContent` and `MpCaptionStyle` definitions with `picsart_media_get_scene_schema`. Put the transcript in a `captions` layer's `content.transcript`. Use `picsart_media_patch_scene` to create or change the layer.
5. Use `picsart_media_list_fonts` for a valid font key or asset. Check line breaks and contrast. Keep captions clear of faces and required screen text.
6. Use word highlighting only where word timings exist. Read the `captions` capability section before adding decorations. Keep text readable throughout each segment.
7. Validate the scene. Check caption starts, ends, and dense passages in the editor. Review the complete caption sequence with the audio.

## Pitfalls

- Export burned captions only when requested.

## Verification

- Keep a separate transcript or SRT when the delivery brief requires it.
- Report any unreviewed speech or missing timings.
