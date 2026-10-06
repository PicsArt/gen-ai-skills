---
name: picsart-sound-effects
description: Generate and place Picsart sound effects for visible actions, transitions, and scene atmosphere.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, audio, sound-effects]
---

# Sound effects

Generate sound effects with a Picsart model and place them on the timeline.

## When to Use

- Add sound for visible actions and transitions.
- Add background atmosphere to a scene.

## Prerequisites

- The `picsart` MCP server is connected.
- Read [the interface map](../picsart-workflows/references/interface-map.md) before tool use.

## How to Run

Use [audio mix](../picsart-audio-mix/SKILL.md) when suitable recordings already exist.

## Quick Reference

- Tools: `picsart_model_catalog`, `picsart_model_params`.
- Use supported trim and volume controls to fit the effect.

## Procedure

1. Identify the event that needs sound.
2. Record its position in the final cut.
3. Separate a short action sound from continuous background atmosphere.
4. Describe the source, distance, movement, and intended length.
5. Use `picsart_model_catalog` with audio mode and `inputType: "sfx"` when the model is unknown.
6. Read `picsart_model_params` for supported duration and prompt controls.
7. Preflight the complete request before generation.
8. If a hard credit cap applies and price is unknown, do not submit.
9. Generate the authorized take with an explicit async media request.
10. Save the job handle before waiting for its result.
11. Listen for unwanted speech, clipping, and a suitable beginning and ending.
12. Place the accepted sound as a separate audio layer.
13. Align the sound with the visible event.
14. Check the sound with dialogue and music.

## Pitfalls

- Keep the picture unchanged unless the request includes picture edits.
- Do not claim exact synchronization until you review the final cut.

## Verification

- Return the accepted sound and its timeline position.
