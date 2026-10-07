---
name: picsart-image-finishing
description: Produce exact image crops, output sizes, rotations, flips, formats, and quality settings through the picsart MCP scene and export tools, with upscale through picsart_enhance. Use for finishing an accepted image into delivery derivatives. Not for generative edits or new imagery.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, image, crop, resize, export]
---

# Image Finishing

Make delivery derivatives from an accepted image: crop, size, rotate, flip, format, and quality.
Build each derivative as a one-layer scene and render it with `picsart_media_export`.

## When to Use

- The user needs exact pixel sizes, crops, rotations, flips, or a format change of an accepted image.
- The user needs a set of derivatives (for example, social sizes) from one master.
- Not for content changes (use [image edit](../picsart-image-edit/SKILL.md)) or new images (use [generate](../picsart-generate/SKILL.md)).
- Not for layered layouts with text and logos (use [scene design](../picsart-scene-design/SKILL.md)).

## Prerequisites

- The `picsart` MCP server is connected. See the [interface map](../picsart-workflows/references/interface-map.md).
- The source image has a public URL. Read [remote resources](../picsart-workflows/references/remote-resources.md) before you select it.

## How to Run

1. Probe the source with `picsart_media_probe_media` (`url`) for `width`, `height`, and `orientation`.
2. Get a starting scene from `picsart_media_quickstart`, or bootstrap `mpscene://crop` with `picsart_media_apply_scene_template` (`mode: "bootstrap"`).
3. Set the composition size and the layer `content.fit`, `content.align`, and `transform` with `picsart_media_patch_scene`.
4. Render with `picsart_media_export` (`mediaType`, `jpegQuality`, `startTime`, `fileName`).

## Quick Reference

| Need | MCP route |
| --- | --- |
| Exact output size | Composition `width`/`height` equal to the target |
| Crop to fill | Layer `content.fit: "cover"` + `content.align` |
| Letterbox / pad | `content.fit: "contain"` over a `color` background layer |
| Crop window by center and zoom | `mpscene://crop` (`moves`, `sourceWidth`, `sourceHeight`) |
| Rotate / flip | Layer `transform` (rotation, signed scale); check `picsart_media_get_scene_schema` |
| Perspective tilt (approximate) | `picsart_media_apply_effect` `perspective_3d` (`rotation_x`, `rotation_y`, `distance`) |
| Format | `picsart_media_export` `mediaType`: `png`, `jpeg`, `webp`, `heif` |
| JPEG quality | `jpegQuality` 1-100 |
| Upscale | `picsart_enhance` (`image`, `scaleFactor`) before the scene step |

## Procedure

1. Reuse the accepted source. Record its URL, revision, pixel size, and orientation.
2. List each derivative: size, crop or pad, format, and quality.
3. Choose fit, crop, or pad from the brief before you change aspect ratio.
4. Keep the subject, logo, and exact text inside the crop. Use `content.align` or crop `moves` to place the window.
5. If the target is larger than the source, upscale first with `picsart_enhance`. Use its result URL as the layer source.
6. Patch the scene per derivative. Run `picsart_media_validate_scene` if a patch returns `valid: false`.
7. Check one frame with `picsart_media_contact_sheet` (`times: [0]`).
8. Export with `async: false` for a single still. Otherwise keep the job receipt and poll `picsart_job_status`.
9. Confirm the Drive save from `driveUid`, or save with `picsart_drive` (`action: "upload"`).

## Pitfalls

- **Coverage:** there is no exact pixel crop rectangle or four-corner perspective transform. This route crops by fit/align or a center-and-zoom window, and `perspective_3d` is a 3D tilt, not a four-corner perspective correction. Check edge pixels on tight crops.
- `picsart_media_export` `resolution` is a server-side downscale. Set the composition size to the target instead.
- Export renders the scene, so output pixels can differ slightly from the source. Do not promise a lossless crop.
- `picsart_enhance` is an AI upscale. It can change fine detail and text. Compare against the source.

## Verification

- Probe each output with `picsart_media_probe_media`. Check `width`, `height`, `contentType`, and transparency where needed.
- Compare the visible crop, artwork, and text against the source.
- Return a source-to-derivative manifest: output URLs, settings, and review results.
- An output URL alone does not prove a stored asset. Report a save only when `driveUid` or a Drive receipt is returned.
