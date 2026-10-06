---
name: picsart-voiceover
description: Create a Picsart voiceover from an approved script. Use for narration, spoken copy, voice selection, and speech timing.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, audio, voiceover]
---

# Voiceover

Generate spoken audio from an approved script with a Picsart text-to-speech model.

## When to Use

- Create narration or spoken copy from an approved script.
- Choose a voice and fit the speech to a time window.

## Prerequisites

- The `picsart` MCP server is connected.
- Read the [interface map](../picsart-workflows/references/interface-map.md).

## How to Run

Keep the spoken script separate from delivery notes.

## Quick Reference

- Tools: `picsart_model_catalog`, `picsart_model_params`, `picsart_preflight`.

## Procedure

1. Set the language, speaker, intended tone, and time window. Keep approved names, numbers, and claims exact.
2. Keep the user's model choice when suitable. Otherwise query `picsart_model_catalog` with `mode: "audio"` and `inputType: "tts"`.
3. Read `picsart_model_params` for the selected model. Select an available voice ID. Check script limits and supported delivery controls. Do not invent an accent or speed field.
4. Put the spoken text in `prompt`. Add supported voice parameters through the interface's declared fields.
5. Use `picsart_preflight` with the full candidate parameters. Correct errors. Stop before submission when an unknown price prevents compliance with a strict credit cap.
6. Generate only the authorized take. Use `async: true` for a recoverable connector request. Preserve its job handle. Poll the existing job after a timeout.
7. Listen for pronunciation, omissions, unwanted tags, and clipped words. Measure the returned duration. Do not promise that word count guarantees an exact speech length.
8. Place the accepted recording with [audio mix](../picsart-audio-mix/SKILL.md). Create [captions](../picsart-captions/SKILL.md) from the accepted audio when needed.

## Pitfalls

- Use voice references only when requested and supported. Reference conditioning does not prove model training.
- Keep later corrections within the authorized take budget.

## Verification

- Report the accepted take only after the step 7 listening and duration checks pass.
