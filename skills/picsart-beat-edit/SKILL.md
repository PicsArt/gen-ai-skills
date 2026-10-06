---
name: picsart-beat-edit
description: Sequence existing photos or video to measured music beats in an editable Picsart timeline with verified audio synchronization.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, video, audio, music]
---

# Beat edit

Cut existing photos or video to measured music beats in an editable Picsart timeline.

## When to Use

- Sequence supplied photos or video clips to the beats of a soundtrack.
- Keep the result as an editable timeline with checked audio synchronization.

## Prerequisites

- The `picsart` MCP server is connected.
- Read [production state](../picsart-workflows/references/media-production.md) for timing maps, receipts, and verification limits.
- Read [remote resources](../picsart-workflows/references/remote-resources.md) before requesting new music or visuals.

## How to Run

Follow the Procedure below.

## Quick Reference

- Tools: `picsart_media_list_recipes`, `picsart_media_analyze_audio`.
- Recipes: `photo-promo` for photos, `video-editing` for video.

## Procedure

1. Establish the soundtrack, target duration, and required visual order.
2. Reuse supplied media and matching remote assets before generation.
3. Preserve source handles and the original scene version when available.
4. Discover native recipes with `picsart_media_list_recipes`.
5. Fetch `photo-promo` or `video-editing` according to the selected media.
6. Probe unknown source durations and dimensions.
7. Use `picsart_media_analyze_audio` with `beats` in `include` for measured beat timestamps.
8. Follow the returned receipt with its named status tool.
9. Inspect confidence, `notes`, and event limits before treating the grid as complete.
10. If events were subsampled, request sufficient coverage before assigning consecutive beat cuts.
11. If timing confidence is low, use deliberate manual pacing and disclose the uncertainty.
12. Map source beat times through soundtrack trims and timeline offsets.
13. Choose cut points that preserve the message and readable visual holds.
14. Account for transition overlap when calculating clip windows.
15. Arrange the soundtrack with [audio mix](../picsart-audio-mix/SKILL.md).
16. Listen across joins and inspect synchronization during playback.
17. Keep the returned scene after each change.
18. Validate direct scene edits.

## Pitfalls

- A tempo estimate alone does not establish the first beat's position.
- Do not claim complete synchronization from still previews.

## Verification

- Use [delivery check](../picsart-delivery-check/SKILL.md) for requested exports.
- Return the editable timeline, beat mapping, soundtrack settings, and completed review evidence.
