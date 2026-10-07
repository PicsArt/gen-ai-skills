---
name: picsart-ctv-delivery
description: Render an approved ad for a named CTV destination through picsart_media_export with the closest delivery settings, then check the file against the destination spec. Use before handing an ad to a streaming or CTV platform. Not for editing the ad itself.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, ctv, video, delivery]
---

# CTV Delivery

Render the approved ad at the destination's size, frame rate, and container.
Then measure the file against the destination spec and report every gap.

## When to Use

- The user has an approved ad and a named CTV or streaming destination.
- Not for creative edits (use [scene revision](../picsart-scene-revision/SKILL.md)).
- For the measurement step on its own, use [delivery check](../picsart-delivery-check/SKILL.md).

## Prerequisites

- The `picsart` MCP server is connected. See the [interface map](../picsart-workflows/references/interface-map.md).
- The approved master or its scene is available. Read [remote resources](../picsart-workflows/references/remote-resources.md).
- The destination's current delivery spec is in hand.

## How to Run

1. Probe the master with `picsart_media_probe_media`.
2. Wrap it in a scene sized to the destination (or reuse the approved scene).
3. Render with `picsart_media_export` (`mediaType`, `fps`, `resolution`, `duration`, `fileName`).
4. Check the file with [delivery check](../picsart-delivery-check/SKILL.md).

## Quick Reference

| Spec item | Export control |
| --- | --- |
| Container | `mediaType`: `mp4` or `mov` |
| Frame size | Composition `width`/`height`; `resolution` only downscales |
| Frame rate | `fps` |
| Duration | `duration` from `startTime` |
| Codec, bitrate, GOP, color, audio rate | Not exposed; measure and report |
| Loudness | Not exposed; measure and report |

## Procedure

1. Name the destination and get its current spec.
2. Reuse the approved master. Record its URL, revision, and probe result.
3. Map each spec item to an export control. List items that no control sets.
4. Set the composition to the spec frame size. Use `content.fit: "contain"` to keep safe areas.
5. Validate the scene and check the first and last frames with `picsart_media_contact_sheet`.
6. Export once. Keep the job receipt and poll `picsart_job_status` until it finishes.
7. Probe the output: codec, container, size, `fps`, duration, and audio.
8. Loudness is not measurable with the served tools. When the spec sets it, mark it unverified.
9. Compare every measured value with the spec. Record each failed or unverified item.

## Pitfalls

- **Coverage:** `picsart_media_export` sets container, size, frame rate, and duration only. Codec profile, bitrate, GOP, color range, audio sample rate, and loudness are not configurable, so spec conformance is not guaranteed.
- Conversion success does not prove destination acceptance.
- Do not upscale a master silently to meet a frame size. Report it.

## Verification

- Return the file URL, spec reference, master revision, receipts, and a pass/fail/unverified row per spec item.
- Delivery to the destination is the user's step: hand over the file URL and the per-item spec report.
