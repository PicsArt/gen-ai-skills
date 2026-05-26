---
name: product-photo-studio
description: Transform product photos via Picsart gen-ai — six modes.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: creative
    tags: [picsart, product-photos, ecommerce, catalog, mockups, variants]
---

# Product Photo Studio

A single skill that covers every "transform a product photo with AI" workflow Picsart's `gen-ai` CLI supports. Use this whenever the user has product photography (single packshot, full catalog, or one artwork) and needs it re-rendered, re-staged, or fanned out into variants. Replaces six narrower skills with one entry point and six mode references.

**Input:** one or more product photos. **Output:** styled, composed, or fanned-out variants ready for PDPs, marketplaces, ads, mockup listings, or campaigns.

## When to Use

Pick the mode that matches the task. If the user's request maps to any of these, this skill is the right one:

| Mode | Trigger phrases | Reference |
|---|---|---|
| **bulk-restyle** | "catalog styling", "consistent background across SKUs", "PDP-ready staging at scale" | [`references/modes/bulk-restyle.md`](references/modes/bulk-restyle.md) |
| **compose** | "lifestyle compose", "product in context", "put this product in a scene" | [`references/modes/compose.md`](references/modes/compose.md) |
| **seasonal** | "seasonal refresh", "holiday catalog", "Christmas / summer / Black Friday catalog" | [`references/modes/seasonal.md`](references/modes/seasonal.md) |
| **variants** | "color variants", "material variants", "colorway fan-out", "size chart re-render" | [`references/modes/variants.md`](references/modes/variants.md) |
| **reshoot** | "batch reshoot", "regenerate catalog", "enterprise catalog re-render with brand rules" | [`references/modes/reshoot.md`](references/modes/reshoot.md) |
| **mockups** | "product mockup", "POD mockup", "Etsy / Shopify listing mockup", "in-hand render" | [`references/modes/mockups.md`](references/modes/mockups.md) |

If the user's task involves video, characters, or persona generation, this is the wrong skill — see `motion-studio`, `gen-ai-persona-creation`, `gen-ai-use`.

## Prerequisites

Picsart `gen-ai` CLI installed and authenticated:

```bash
# Install (signed binary, recommended)
curl -fsSL https://picsart.com/gen-ai-cli/install.sh | bash

# Authenticate
gen-ai login
gen-ai whoami    # verify
```

Per-mode prerequisites (image counts, brand files, manifests) are documented inside each mode reference. Always confirm pricing before a bulk run:

```bash
gen-ai pricing --model <model> --count <N>
```

## How to Run

1. Identify the mode from the user's request using the table in **When to Use**.
2. Load the corresponding mode reference: `Read` `references/modes/<mode>.md`.
3. Follow the procedure described there — interview, manifest, generate.
4. Return to this SKILL.md only when switching modes mid-task.

## Quick Reference

```bash
# Single image (compose / mockups)
gen-ai generate --model <model> --image input.jpg --prompt "<prompt>"

# Batch (bulk-restyle / seasonal / variants / reshoot)
gen-ai batch --manifest manifest.json

# Estimate cost before running
gen-ai pricing --model <model> --count <N>

# Browse available models
gen-ai models
```

Manifest patterns, model recommendations, and per-mode best practices live in the individual mode references.

## Procedure

Always follow the same outer loop regardless of mode:

1. **Interview** — confirm: which mode, how many inputs, target output format(s), brand constraints, deadline.
2. **Manifest** — assemble a JSON manifest (single-shot inline, or batch file). Each mode reference has a template.
3. **Estimate** — run `gen-ai pricing` before committing. Surface the total to the user.
4. **Generate** — invoke `gen-ai generate` or `gen-ai batch`. Stream progress.
5. **Verify** — open the output directory and confirm the expected files exist with the expected dimensions.
6. **Hand off** — drop into the configured Drive folder, marketplace feed, or deliverable zip.

## Pitfalls

Mode-specific pitfalls (e.g. "shadow direction drifts across variants", "seasonal overlays expire", "brand.md gate blocks SKU-XYZ") live inside each mode reference. Shared pitfalls:

- **Never skip the pricing estimate.** Bulk runs across thousands of SKUs can rack up real cost.
- **Always namespace outputs by client/run** — don't write into a global output dir, you'll lose track of which batch produced which assets.
- **Respect brand governance.** If the user has an `enterprise-brand-governor`-style brand.md in scope, the manifest must reference it.
- **Don't switch models mid-batch.** Pin the exact model version per run for consistency; see `enterprise-pinned-registry`.

## Verification

After any run:

```bash
# Confirm output count matches expected
ls -1 outputs/<run>/ | wc -l

# Spot-check one output's dimensions
gen-ai inspect outputs/<run>/<sample>.jpg
```

If anything looks off, re-run with `--debug` and consult the mode reference's "Common pitfalls" section.

## See also

- [`motion-studio`](../motion-studio/) — video pipeline (out of scope here)
- [`gen-ai-use`](../gen-ai-use/) — foundational gen-ai CLI reference
- [`enterprise-brand-governor`](../enterprise-brand-governor/) — policy gating
- [`enterprise-pinned-registry`](../enterprise-pinned-registry/) — version pinning
