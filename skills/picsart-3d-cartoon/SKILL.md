---
name: picsart-3d-cartoon
description: Create expressive 3D cartoon characters, stylized portraits, and cinematic animated scenes with visual descriptions.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, 3d-cartoon, character-design, stylized-portrait]
---

# Expressive 3D cartoons

Turn a subject or supplied image into a 3D cartoon prompt and result built from visible design choices.

## When to Use

- The user wants a 3D cartoon character, a stylized portrait, or an animated cartoon scene.
- The style must come from described forms, materials, and light, not from named studios or artists.

## Prerequisites

- The `picsart` MCP server is connected.
- Read [the interface map](../picsart-workflows/references/interface-map.md) before generation.

## How to Run

Describe the visual result without studio, franchise, or artist names.

Use [asset reuse](../picsart-asset-reuse/SKILL.md) to find existing characters, props, and locations in the shared Library.

## Quick Reference

- Prompt choices: subject, action, emotion, setting, forms, proportions, surfaces, palette, light, and camera.

## Procedure

1. Record the subject, action, emotion, setting, and output format.
2. If an image is supplied, inspect it. Preserve age, facial features, skin tone, hair, and distinctive details.
   Otherwise, mark original design choices as proposed.
3. Define rounded forms, a readable silhouette, and expressive facial features.
4. Adjust head and eye proportions to suit the subject. Do not turn every adult into a child.
5. Use smooth shading and believable skin, fabric, fur, or painted surfaces.
6. Select a coherent color palette and a clear focal point.
7. Describe soft main light, reflected light, gentle shadows, and optional rim light.
8. Set camera distance and viewing angle. Use background depth to separate the subject from the setting.
9. Write the prompt from these choices. Describe visible details instead of named style references.
10. Reuse compatible accepted images. For required new output, use [generation](../picsart-generate/SKILL.md) within the authorized budget.
11. Inspect expression, silhouette, hands, materials, lighting, and reference fidelity.
12. Correct a specific defect while keeping the accepted design choices.

### Continue a sequence

For related scenes, use [character continuity](../picsart-character-continuity/SKILL.md).
Keep proportions, clothing, palette, and material descriptions consistent.
For animation, inspect an accepted still before dependent video generation.
Describe one main action and the intended expression change per shot.
Use [storyboard](../picsart-storyboard/SKILL.md) when the request has multiple shots.

## Pitfalls

- Step 4 limits proportion changes, and step 9 rules out named style references.

## Verification

Return the prompt, design choices, and available results.
Mark a prepared prompt as a plan when no image was generated.
