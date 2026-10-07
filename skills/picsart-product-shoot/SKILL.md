---
name: picsart-product-shoot
description: Create Picsart product images for catalogs, campaign assets, and product scenes. Preserve supplied product details across the requested images.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, product-photography, catalog, campaign]
---

# Product shoot

Plan and produce a set of product views that keep the supplied product exactly as it is.

## When to Use

- The user needs product images for a catalog, campaign assets, or product scenes.
- The supplied product's shape, color, material, and label must stay the same across every image.
- For CLI product-photo transforms with the gen-ai CLI, use [product-photo-studio](../product-photo-studio/SKILL.md).

## Prerequisites

- The `picsart` MCP server is connected.
- Read [the interface map](../picsart-workflows/references/interface-map.md) before a tool call. Use its schema and cost checks.

## How to Run

Use [asset reuse](../picsart-asset-reuse/SKILL.md) for existing product props, cast, and locations in the shared Library.

## Quick Reference

- View purposes (step 3): show the whole product, a detail, or its use.

## Procedure

1. Extract the product, output size, placement, and image count from the request. Ask only for missing facts that affect the result.
2. Inspect the supplied product image. Record its shape, color, material, label, and visible parts. Treat these facts as fixed unless the user requests a change.
3. Plan the required views. Give each view a purpose: show the whole product, show a detail, or show its use. Keep the same product description across views.
4. Define the background, light direction, shadow, camera angle, and empty space for each view. Keep light and color consistent for a catalog set.
5. Select an interface that supports the required reference image. Use an image edit when the product must remain intact. Do not assume that text generation will reproduce a supplied label.
6. Submit within the user's requested count and cost limit. Inspect each returned image before another batch.
7. Compare the result with the reference. Check product geometry, text, material, shadow, crop, and unwanted parts. Repair the specific defect. Do not replace a correct image to fix another image.
8. Deliver the images with their view names. State any visible mismatch that remains. Keep exact brand text or logos as supplied assets when a separate composition is required.

## Pitfalls

- Step 5 limits label reproduction by text generation; step 7 keeps correct images while you repair another.

## Verification

- Step 7 sets the comparison checks; step 8 sets the delivery report.
