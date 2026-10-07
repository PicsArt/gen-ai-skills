---
name: picsart-product-mockup
description: Place supplied artwork onto a photographed product through picsart_generate with an image-edit model that takes the artwork and product photo as references. Use for visual product mockups. Not for print-accurate proofs or new product photography.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, mockup, product, image-edit]
---

# Product Mockup

Put supplied artwork on a product photo with a reference-image edit model.
The result is a visual mockup, not a geometric surface map.

## When to Use

- The user has artwork (logo, label, print) and a product photo and wants the artwork shown on the product.
- Not for new product scenes from text (use [product shoot](../picsart-product-shoot/SKILL.md)).
- Not for print proofs or exact physical placement.

## Prerequisites

- The `picsart` MCP server is connected. See the [interface map](../picsart-workflows/references/interface-map.md).
- The artwork and product photo have public URLs. Read [remote resources](../picsart-workflows/references/remote-resources.md) and use [asset reuse](../picsart-asset-reuse/SKILL.md) first.

## How to Run

1. Find a candidate model with `picsart_model_catalog` (`mode: "image"`, `acceptsImage: true`, `purpose: "edit"` or `"generate"`).
2. Read its inputs with `picsart_model_params`. Pick one that takes several `imageUrls`.
3. Validate and price the payload with `picsart_preflight`.
4. Run `picsart_generate` (`model`, `prompt`, `imageUrls`, `aspectRatio`, `count`).

## Quick Reference

| Input | Where it goes |
| --- | --- |
| Product photo | `imageUrls[0]`; prompt names it "IMAGE 1 - PRODUCT" |
| Artwork | `imageUrls[1]`; prompt names it "IMAGE 2 - ARTWORK" |
| Placement | Prompt: surface, position, size, and "keep artwork unchanged" |
| Candidates | `count` (one call; do not loop) |
| Clean artwork edges | `picsart_remove_bg` on the artwork first, if it has a background |
| Finishing | [image finishing](../picsart-image-finishing/SKILL.md) on the accepted mockup |

## Procedure

1. Reuse approved artwork and product photos. Record URLs, revisions, and dimensions.
2. Confirm that the user may use the supplied artwork for this task.
3. If the artwork has a background, cut it out with `picsart_remove_bg` (`image`, `outputFormat: "png"`).
4. Pick the model at runtime as in How to Run. Do not hardcode a model ID.
5. Write the prompt: which image is the product, which is the artwork, the target surface, placement, and what must not change.
6. Preflight, then generate once with `async: true`. Keep the job handle. Poll `picsart_job_status`.
7. Inspect edges, perspective, curves, texture, and placement. Compare logo shape and lettering against the original.
8. If finishing is needed, use [image finishing](../picsart-image-finishing/SKILL.md).

## Pitfalls

- **Coverage:** a generative edit redraws the artwork rather than warping its exact pixels onto the surface. Lettering, logo geometry, and colors can drift, and there is no mask input or warp guarantee.
- Do not retry a paid call after a credit error until the user says they are ready.
- Small text on artwork is the first thing to break. Ask for a larger artwork crop or flag the risk.
- Do not infer physical print accuracy from a visual mockup.

## Verification

- Compare each candidate against the original artwork at full size: shape, spelling, colors.
- Return the mockup URL, artwork and product references, the model ID used, and review results.
- Report distortions or unverified artwork fidelity explicitly.
- Report a Drive save only when the result carries a `drive` receipt.
