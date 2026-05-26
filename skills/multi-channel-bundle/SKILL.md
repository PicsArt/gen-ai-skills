---
name: multi-channel-bundle
description: Ship a coordinated multi-format asset bundle for any push.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: marketing
    tags: [picsart, campaigns, launches, social, multi-format]
---

# Multi-Channel Bundle

Produce a coordinated set of assets — hero, social variants, OG image, reel, optionally audio — for a single push: a marketing campaign or a product launch. Replaces two near-identical skills (campaign-kit, launch-kit) with one entry point and two mode references that differ only in scale, naming, and channel mix.

**Input:** the brief (campaign or launch). **Output:** a folder per channel with on-brand, on-format assets ready to ship.

## When to Use

| Mode | Trigger phrases | Reference |
|---|---|---|
| **campaign** | "campaign kit", "multi-channel campaign assets", "LinkedIn + IG + email + LP + ads in one go" | [`references/modes/campaign.md`](references/modes/campaign.md) |
| **launch** | "launch kit", "product launch assets", "launch day social + reel + soundtrack" | [`references/modes/launch.md`](references/modes/launch.md) |

If the user wants pitch-deck slides for an agency client, that's `agency-pitch-mockups`. If they want N ad variants from one hero (no other channels), that's `marketer-ad-variant-factory`.

## Prerequisites

Picsart `gen-ai` CLI installed and authenticated:

```bash
curl -fsSL https://picsart.com/gen-ai-cli/install.sh | bash
gen-ai login
gen-ai whoami
```

Per-mode setup (channel matrix, copy alignment, motion source, audio licensing) lives inside each mode reference.

## How to Run

1. Identify the mode from the user's request using the table above.
2. Load the corresponding mode reference: `Read` `references/modes/<mode>.md`.
3. Follow the per-mode procedure — confirm channels, build the manifest, batch-generate.
4. Return here only when switching modes.

## Quick Reference

```bash
# Bundle generation is always a batch run
gen-ai batch --manifest manifest.json --output bundle/

# Estimate before committing
gen-ai pricing --manifest manifest.json
```

Manifest templates per mode live in the mode references.

## Procedure

Shared outer loop:

1. **Scope** — confirm: which channels, hero asset, copy lock state, motion (reel) required yes/no, audio required yes/no, deadline.
2. **Manifest** — assemble a JSON manifest covering every required channel and format.
3. **Estimate** — `gen-ai pricing --manifest manifest.json`. Surface the total.
4. **Generate** — `gen-ai batch`. Stream progress.
5. **Compose** — if a reel is in scope, hand the clips to `motion-studio` for assembly.
6. **Package** — drop into `bundle/<run>/<channel>/`. Optionally zip via `agency-client-handoff`.

## Pitfalls

- **Aspect ratios drift.** Bake all required ratios (1:1, 4:5, 9:16, 16:9, 1200×630) into the manifest up front; don't fix per-channel afterward.
- **Copy lock matters.** If copy isn't locked, treat the run as a draft; mark outputs in filenames (`<channel>-DRAFT-...`).
- **Audio licensing.** Launch reels with soundtracks need licensed tracks; document the source in the manifest.
- Mode-specific pitfalls live in the mode references.

## Verification

```bash
# Confirm one folder per channel exists with expected file counts
find bundle/<run> -type d -maxdepth 1
ls -1 bundle/<run>/<channel>/ | wc -l
```

## See also

- [`agency-pitch-mockups`](../agency-pitch-mockups/) — pitch-deck slide variant (different output type)
- [`marketer-ad-variant-factory`](../marketer-ad-variant-factory/) — ad-only fan-out
- [`motion-studio`](../motion-studio/) — reel assembly
- [`product-photo-studio`](../product-photo-studio/) — product-photo transforms feeding into a bundle
