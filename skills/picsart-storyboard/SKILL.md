---
name: picsart-storyboard
description: Plan Picsart image or video scenes as a storyboard with shot purpose, framing, timing, action, and reusable references.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, storyboard, planning]
---

# Storyboard

Plan image or video scenes shot by shot before any Picsart generation or composition.

## When to Use

- Plan image or video scenes as a storyboard before production.
- Set shot purpose, framing, timing, action, and reusable references.

## Prerequisites

- The `picsart` MCP server is connected.
- Read [the interface map](../picsart-workflows/references/interface-map.md) before generation or composition.

## How to Run

A storyboard request can end with a plan; it does not require paid renders.

## Quick Reference

- Use [asset reuse](../picsart-asset-reuse/SKILL.md) to bind existing characters, props, and locations to shots.

## Procedure

1. Extract the message, audience, duration, format, and required story events. Preserve the user's script and exact copy.
2. Divide the story into visible actions. Assign one main action to each shot. Add a shot only when it supplies needed information or coverage.
3. Create a shot table. Include shot ID, duration, framing, subject action, camera movement, dialogue or sound, and transition. Check the total duration.
4. Identify the character, location, and object references for each shot. Record continuity across connected shots. Keep screen direction and object position clear.
5. Write a frame description for each shot. Describe what the viewer can see.
6. Check that the sequence explains the story without relying on missing shots. Use a wider view when the viewer needs spatial context. Use a detail view when the action needs emphasis.
7. If the user requests images, generate the required frames through verified Picsart interfaces. Review them in sequence. Fix an unclear action or continuity defect before dependent video work.

## Pitfalls

- Avoid instructions that require an unsupported model parameter.

## Verification

- Deliver the shot table and available frames in story order.
- Mark planned, generated, and accepted items separately.
- Include unresolved references or timing conflicts.
