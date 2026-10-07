---
name: picsart-character-continuity
description: Keep a character's appearance consistent across Picsart images or scenes with reference images and a scene continuity record.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, character-continuity, reference-images, consistency]
---

# Character continuity

Hold one character's identity steady across images or scenes with references, an identity record, and a scene table.

## When to Use

- A character must look the same across several Picsart images or scenes.
- The user supplies character references, or accepted assets of the character already exist.

## Prerequisites

- The `picsart` MCP server is connected.
- Read [the interface map](../picsart-workflows/references/interface-map.md) before a tool call. Confirm that the selected model accepts the required references.

## How to Run

Use [asset reuse](../picsart-asset-reuse/SKILL.md) to find existing cast in the shared Drive Library.

## Quick Reference

- Continuity records: the identity record (step 2) and the scene table (step 3).

## Procedure

1. Inspect the user's character references. Resolve conflicting references before generation. Use existing accepted assets when available.
2. Write a short identity record. Include face shape, hair, body proportions, distinctive marks, and fixed clothing. Describe visible features. Do not claim that a reference image trains an identity model.
3. Make a scene table. Record the scene ID, character reference, clothing, carried objects, action, and story time. Mark intentional changes.
4. Separate identity from pose, expression, and setting. Reuse the identity description without new synonyms. Change only the scene details that the request requires.
5. Attach the relevant reference images through fields in the verified schema. Use clear reference roles. Do not assume that a seed guarantees identity.
6. Inspect each result beside the reference and adjacent scenes. Check facial features, hair, proportions, clothing, object placement, and movement direction. Treat an unintended change as a defect.
7. Repair only the affected scene within the user's generation limit. If the model cannot hold the required feature, state the limitation before further paid attempts.
8. Deliver the continuity table and accepted image references. For film assets, use the asset review and save contract in the interface map. Report an asset as locked only when the returned result confirms it.

## Pitfalls

- Steps 2 and 5 limit claims about identity training and seeds; step 7 limits paid repair attempts.

## Verification

- Step 6 sets the checks for each result; step 8 sets the delivery and lock report.
