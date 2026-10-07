---
name: picsart-social-ad
description: Produce Picsart social ad creative with a clear opening, product evidence, and call to action. Create comparable variants without launching campaigns.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, social-ad, ad-creative, variants]
---

# Social ad

Build social ad creative and comparable variants, and stop before any campaign launch.

## When to Use

- The user wants social ad creative with a clear opening, product evidence, and a call to action.
- The user wants comparable variants, but not campaign launch or spend.
- To fan out many ad variants from one hero image with the gen-ai CLI, use [marketer-ad-variant-factory](../marketer-ad-variant-factory/SKILL.md).

## Prerequisites

- The `picsart` MCP server is connected.
- Read [the interface map](../picsart-workflows/references/interface-map.md) before a tool call. Treat campaign publishing as a separate action.

## How to Run

Follow the Procedure below.

## Quick Reference

- Creative structure (step 2): one message, a clear opening, product evidence, and the requested call to action.

## Procedure

1. Extract the audience, product, offer, placement, format, and requested variants. Use supplied claims and exact prices. Ask for missing facts that change the message.
2. Define one message for each creative. Write an opening that makes its subject clear. Show the product or result that supports the message. End with the requested call to action.
3. For video, create a timed shot list. For a static image, define the reading order and space for copy. Keep the product visible.
4. Verify current placement dimensions and interface safe areas from the platform's primary guidance. Keep important copy and product details outside overlays.
5. Create variants that change one stated creative choice at a time. Hold the offer, product, and output format constant when the user wants a comparison.
6. Use [asset reuse](../picsart-asset-reuse/SKILL.md) for existing products, cast, locations, and brands. Generate only missing material. Keep exact logos and text as composition elements.
7. Inspect the opening, product fidelity, text legibility, crop, sound, and final action. Check that every claim matches the supplied facts.
8. Deliver labeled variants and describe the changed choice. Record any remaining defect. Do not call a variant a winner without relevant measured results. Keep campaign activation and spend outside this workflow unless separately authorized.

## Pitfalls

- Step 5 holds the comparison variables constant; step 8 keeps winner claims, activation, and spend out of scope.

## Verification

- Step 7 sets the checks before delivery; step 8 sets the variant labels and defect record.
