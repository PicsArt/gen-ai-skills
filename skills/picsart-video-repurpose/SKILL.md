---
name: picsart-video-repurpose
description: Turn existing long or wide footage into short Picsart edits with meaningful segments, subject framing, and synchronized captions.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, video, reframe]
---

# Video repurpose

Cut existing long or wide footage into short Picsart edits that keep the subject in frame.

## When to Use

- Turn long or wide footage into short edits for other ratios.
- Keep meaningful segments, subject framing, and synchronized captions.

## Prerequisites

- The `picsart` MCP server is connected.
- Read [production state](../picsart-workflows/references/media-production.md) for timing maps and receipts.
- Read [remote resources](../picsart-workflows/references/remote-resources.md) before seeking new material.

## How to Run

Follow the Procedure below.

## Quick Reference

- Tools: `picsart_media_list_recipes`, `picsart_media_get_recipe`, `picsart_media_probe_media`, `picsart_media_describe_video`, `picsart_media_reframe_video`.
- Use [captions](../picsart-captions/SKILL.md) for caption authoring and review.

## Procedure

1. Establish the audience, target ratios, duration, and essential message.
2. Reuse supplied footage and matching remote assets before generation.
3. Preserve source handles and the original scene version when available.
4. Discover native recipes with `picsart_media_list_recipes`.
5. Fetch the applicable editing recipe with `picsart_media_get_recipe`.
6. Probe unknown source metadata with `picsart_media_probe_media`.
7. Use transcription for speech and `picsart_media_describe_video` for visual context when needed.
8. Follow each analysis receipt with its named status tool.
9. Choose coherent source windows that retain necessary context.
10. Record each source in/out, timeline start, and speed.
11. Assemble windows with [video edit](../picsart-video-edit/SKILL.md).
12. Use `picsart_media_reframe_video` for subject tracking when the target crop needs it.
13. Check its returned asset, trim, timing, and crop against the source mapping.
14. Validate the reframed scene before delivery.
15. Map caption timestamps through every trim, reorder, and speed change.
16. Review subject visibility, speech continuity, caption timing, and segment joins during playback.

## Pitfalls

- Reframe moves existing pixels; it cannot restore content beyond the source frame.
- If word timings are absent, do not invent them.

## Verification

- Use [delivery check](../picsart-delivery-check/SKILL.md) for requested exports.
- Return editable cuts, source mappings, and a manifest for each output.
