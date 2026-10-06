---
name: picsart-explainer
description: Create a Picsart explainer from supplied material with clear narration, supporting visuals, and verified final delivery.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, explainer, narration, video]
---

# Explainer

Turn supplied material into a sourced explainer with narration, matching visuals, and a checked final file.

## When to Use

- The user supplies material and wants an explainer with clear narration and supporting visuals.
- The final file needs factual sources and a delivery check.
- For a short animated explainer from a topic with the gen-ai CLI, use [gen-ai-explainer](../gen-ai-explainer/SKILL.md).

## Prerequisites

- The `picsart` MCP server is connected.
- Read [the interface map](../picsart-workflows/references/interface-map.md) before tool use.

## How to Run

Define what the audience must understand after viewing.
Read the supplied material before writing narration.
Verify changeable or uncertain facts with primary sources.
Keep source links for factual claims.
Preserve the user's personal details without adding events.

## Quick Reference

- Linked skills: storyboard for sections, generation for new narration or footage, scene design for visuals, audio mix for narration, captions, and delivery check.

## Procedure

### Write the explanation

Write a concise explanation in the requested language.
Introduce required terms before using them.
Give each section one teaching purpose.
Use a demonstration, comparison, or diagram when it explains the point clearly.
Keep the visual evidence consistent with the spoken claim.

### Plan the sections

Plan the sections with [storyboard](../picsart-storyboard/SKILL.md).
Set duration from the explanation and requested total length.
Reuse supplied narration when suitable.
For generated narration or footage, follow [generation](../picsart-generate/SKILL.md) and its schema checks.

### Compose and mix

Compose the visuals with [scene design](../picsart-scene-design/SKILL.md).
Arrange narration with [audio mix](../picsart-audio-mix/SKILL.md).
Keep spoken words clear at transitions.
When captions are required, apply [captions](../picsart-captions/SKILL.md) to the final audio timing.

## Pitfalls

- Do not assume fixed clip lengths or a specific narrator model.

## Verification

Review the sequence for factual accuracy, reading time, and gaps in the explanation.
Inspect the narration and visuals together.
Use [delivery check](../picsart-delivery-check/SKILL.md) for the requested final file.
Deliver the file and factual sources.
State any incomplete section or unverified claim.
