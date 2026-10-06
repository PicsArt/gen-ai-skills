---
name: picsart-image-edit
description: Edit a supplied image with Picsart background removal, background replacement, enhancement, or a verified image edit model. Preserve parts outside the requested change.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, image-edit, background-removal, enhancement]
---

# Image edit

Apply the smallest Picsart edit that meets the request and keep everything else intact.

## When to Use

- The user supplies an image and wants its background removed or replaced, its detail enhanced, or another visual change.
- Parts outside the requested change must stay as they are.

## Prerequisites

- The `picsart` MCP server is connected.
- Read [the interface map](../picsart-workflows/references/interface-map.md) before a tool call. Use only the input fields supported by the selected interface.

## How to Run

Follow the Procedure below.

## Quick Reference

- Operation choice (step 2): background removal, background replacement, enhancement, or a compatible edit model.

## Procedure

1. Inspect the source image. Keep its original file or URL available. Record the requested change and the parts that must remain intact.
2. Choose the smallest operation that meets the request. Use background removal for a transparent subject. Use background replacement for a new setting. Use enhancement for resolution or detail. Use a compatible edit model for other visual changes.
3. Check the source dimensions and input requirements. Use the supported upload route for a local file. Do not send a local path into a URL field.
4. Describe the changed area precisely. Specify the required relation to the retained subject, including light, perspective, and shadow. Use a mask only when the verified interface accepts it.
5. Submit within the user's scope and cost limit. Retain a job handle when returned.
   After a timeout, check the original job when possible. Do not resubmit because the result is absent.
6. Compare the result with the original. Check retained details, edges, transparency, color, geometry, text, and reflections. Inspect the intended output size.
7. Repair a specific defect with the original or last accepted source. Avoid repeated edits to a degraded result. Stop when the request is met or the authorized limit is reached.
8. Deliver the edited image and state the applied change. Mention any unintended change that remains visible.

## Pitfalls

- Steps 3 and 5 hold the input and resubmission limits; step 7 stops at the authorized limit.

## Verification

- Step 6 sets the comparison checks; step 8 sets the delivery report.
