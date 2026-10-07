---
name: picsart-video-cutout
description: Remove or replace a footage background through the picsart MCP, using a scene segment mask for cutouts and a video-edit model for replacements, and verify the alpha or composite. Use for keying a person or object out of a clip. Not for still images (use picsart_remove_bg) or for new footage.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, video, background, matte]
---

# Video Cutout

Take the background out of a clip, or swap it for another one.
`picsart_remove_bg` takes an `image` only, so video uses the scene tools or a video-edit model.

## When to Use

- The user wants a person or object cut out of footage, with transparency or over a new background.
- Not for a single still (use `picsart_remove_bg` or [image edit](../picsart-image-edit/SKILL.md)).
- Not for restyling the whole clip (use [video edit](../picsart-video-edit/SKILL.md)).

## Prerequisites

- The `picsart` MCP server is connected. See the [interface map](../picsart-workflows/references/interface-map.md).
- The footage has a public URL. Read [remote resources](../picsart-workflows/references/remote-resources.md) before you select it.

## How to Run

Pick the route from the brief:

- **Cutout or composite over supplied media:** put the clip in a scene, add `remove_segment` with `picsart_media_apply_effect` and a `mask` (detector and segment from `supports.maskProviders`), add the new background as a lower layer, then `picsart_media_export`.
- **Replace with a described background:** pick a video-edit model with `picsart_model_catalog` (`mode: "video"`, `acceptsVideo: true`, `purpose: "edit"`), read `picsart_model_params`, then `picsart_generate` with `videoUrl` and a prompt that keeps the subject unchanged.

## Quick Reference

| Need | MCP route |
| --- | --- |
| Source facts | `picsart_media_probe_media` (`durationSeconds`, `width`, `height`, `fps`, `hasAudio`) |
| Segments available | `picsart_media_get_capabilities` sections `["maskProviders", "effects"]` |
| Cut the subject out | `picsart_media_apply_effect` `effect: "remove_segment"` + `mask` |
| Transparent file | `picsart_media_export` `mediaType: "webm"` or `"mov"`; alpha is not guaranteed |
| Prompted new background | `picsart_generate` with a video-edit model and `videoUrl` |
| Check frames | `picsart_media_contact_sheet` (`times` at motion peaks) |

## Procedure

1. Reuse supplied footage. Record its URL, duration, resolution, and audio.
2. Choose transparent cutout, composite over a supplied background, or prompted replacement.
3. Read the mask providers. Pick the segment that matches the subject (for example `person`, or invert `background`).
4. For a cutout, build the scene, apply `remove_segment`, and add any background layer below the clip.
5. For a prompted replacement, check the model's duration and resolution limits in `picsart_model_params`. Preflight, then generate once with `async: true` and poll `picsart_job_status`.
6. Inspect hair, edges, occlusions, shadows, and motion blur with `picsart_media_contact_sheet` before export.
7. Export. Keep the job receipt and poll `picsart_job_status` until it finishes.
8. Probe the file with `picsart_media_probe_media` and recheck frames with `picsart_media_contact_sheet`. When alpha matters, ask the user to confirm the file in their compositor.

## Pitfalls

- **Coverage:** there is no dedicated frame-by-frame matte, and a `webm` or `mov` export is not guaranteed to carry alpha. This route uses a best-effort segment mask: where it cannot be produced, `remove_segment` returns the input unchanged, with no error. A video-edit model redraws the frame, so subject pixels and duration can change. Neither route guarantees an alpha channel.
- Segments are fixed classes (person, car, dog, ...). An arbitrary product may have no matching segment.
- A `.webm` name does not prove transparency. Check the alpha.
- Video-edit models can cap source length and output resolution. Split or trim before you submit.

## Verification

- View the alpha over contrasting backgrounds, or the composite, at the first, middle, and last frames.
- Probe the output for duration, resolution, and `hasAudio` against the source.
- Return output URLs, the route and model used, receipts, and review limits.
- If alpha fails, report the limit before further processing.
