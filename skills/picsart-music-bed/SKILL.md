---
name: picsart-music-bed
description: Generate and place a Picsart music bed. Use for instrumental background tracks, mood, pacing, and music under speech.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, audio, music]
---

# Music bed

Generate a background music track with a Picsart model and place it under the picture.

## When to Use

- Generate an instrumental background track with a set mood and pacing.
- Place new music under speech in a scene.
- Not for music that already exists; mix that instead.

## Prerequisites

- The `picsart` MCP server is connected.
- Read the [interface map](../picsart-workflows/references/interface-map.md).

## How to Run

Use [audio mix](../picsart-audio-mix/SKILL.md) when the music already exists.

## Quick Reference

- Tools: `picsart_model_catalog`, `picsart_model_params`, `picsart_media_analyze_audio`.

## Procedure

1. Set the track's role, duration, mood, energy, and main instruments. Identify speech windows and the intended ending.
2. Query `picsart_model_catalog` with `mode: "audio"` and `inputType: "music"` when no model is chosen.
3. Read `picsart_model_params`. Choose a supported duration. Enable the declared instrumental control when vocals would compete with speech. Do not assume that a prompt alone prevents vocals.
4. Describe the intended musical structure. Keep a clear opening, a useful middle section, and an ending suitable for the cut.
5. Preflight the full request. Stop before submission when unavailable pricing prevents compliance with a strict credit cap.
6. Generate the authorized take. Use explicit async behavior for connector jobs. Save its returned handle before another operation. Poll that job after a timeout.
7. Listen for unintended vocals, abrupt changes, and a suitable ending. Treat requested tempo and duration as targets until the output is checked.
8. Use `picsart_media_analyze_audio` only when measured beat or energy data helps placement. Check confidence and missing measurements.
9. Add the accepted track as a separate audio layer. Trim and fade it to the picture. Reduce its level under speech with supported volume animation.

## Pitfalls

- Do not promise a seamless loop or exact beat alignment without checking the result.

## Verification

- Report the accepted file and any timing limits.
