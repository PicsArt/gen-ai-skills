---
name: marketer-ad-variant-factory
description: Fan out 50+ ad variants from one hero image.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: marketing
    tags: [picsart, marketing, campaigns, creative]
---

# Ad variant factory

Take one approved concept and explode it into 10-30 shippable ad variants for A/B testing on Meta, Google, TikTok, and Pinterest. Built for speed (parallel batch) and for direct upload to ad accounts (deterministic naming).

## When to Use

- User has a hero / concept and needs many variants across headline × visual × CTA × background for A/B tests.
- "Fan out 30 variants of this ad for Meta" / "generate a test matrix" / "multiply this creative".
- Prepping a new ad-set launch — needs 9:16, 1:1, 16:9 with 3-5 visual variants each.
- Do NOT use for a single hero (use `gen-ai generate`) or for cross-channel creative (use `marketer-campaign-kit`). This skill is for depth on one concept, not breadth across channels.

## Prerequisites

Ask up front if the brief doesn't cover it (combine into one message):

1. **Hero asset** — path or URL to the approved concept image.
2. **Axes to vary** — visual direction (1-5), background/scene (1-5), focal composition (close-up vs wide), optional: color treatment.
3. **Platforms / aspect ratios** — Meta needs 9:16 + 1:1, TikTok is 9:16, Display wants 16:9. Confirm which.
4. **Variant count** — how many total? 10-15 is typical for a first test, 30+ for broad exploration.
5. **Naming convention** — what does the ad platform require (e.g. `{campaign}_{axis}_{variant}_{size}.webp`)?
6. **Brand guardrails** — colors (hex), forbidden elements, existing brand.md?

If the user just says "a lot", default to 5 visuals × 3 ratios = 15 variants.

## How to Run

1. **Anchor on the hero.** The hero is the reference image — every variant should feel like a sibling, not a cousin. Upload to Drive first if it's local so downstream jobs can reference a URL.
2. **Define the variant matrix.** Keep axes explicit. 5 visual directions × 3 aspect ratios = 15 jobs. Don't mix 8 axes — the test becomes unreadable.
3. **Write the manifest.** One job per variant, unique `id` that maps to your ad-platform naming convention. The `image` field references the hero.
4. **Estimate + dry-run.**
   ```bash
   gen-ai batch run variants.json --dry-run
   ```
5. **Run at concurrency 6-8.** Image variants are fast and independent — push concurrency higher than the default 3. Watch for 429s; back off to 4 if you see them.
   ```bash
   gen-ai batch run variants.json -c 8 -o ./ad-variants
   ```
6. **Audit and resume.** Filter `results.json` for non-completed jobs, retry.
   ```bash
   gen-ai batch resume ./ad-variants
   ```
7. **Hand off.** Ads platform uploaders expect a flat folder with standard naming — `results.json` has every path + URL for direct CSV import to Meta Ads Manager / TikTok Ads / Google Ads.

## Quick Reference

Naming convention `{campaign}_{visual}_{composition}_{size}` keeps downstream uploads clean.

```json
{
  "defaults": {
    "model": "recraftv4",
    "negativePrompt": "low quality, watermark, busy background",
    "imageUrls": ["https://cdn-pipeline-output.picsart.com/.../hero.webp"]
  },
  "jobs": [
    { "id": "launch_bright_closeup_9x16", "prompt": "bright daylight variant, close-up focal, warm tones", "aspectRatio": "9:16" },
    { "id": "launch_bright_closeup_1x1",  "prompt": "bright daylight variant, close-up focal, warm tones", "aspectRatio": "1:1"  },
    { "id": "launch_bright_closeup_16x9", "prompt": "bright daylight variant, close-up focal, warm tones", "aspectRatio": "16:9" },
    { "id": "launch_studio_wide_9x16",    "prompt": "studio lighting, wide shot, neutral backdrop",        "aspectRatio": "9:16" },
    { "id": "launch_studio_wide_1x1",     "prompt": "studio lighting, wide shot, neutral backdrop",        "aspectRatio": "1:1"  },
    { "id": "launch_studio_wide_16x9",    "prompt": "studio lighting, wide shot, neutral backdrop",        "aspectRatio": "16:9" },
    { "id": "launch_urban_medium_9x16",   "prompt": "urban street setting, medium shot, cinematic",        "aspectRatio": "9:16" },
    { "id": "launch_urban_medium_1x1",    "prompt": "urban street setting, medium shot, cinematic",        "aspectRatio": "1:1"  },
    { "id": "launch_urban_medium_16x9",   "prompt": "urban street setting, medium shot, cinematic",        "aspectRatio": "16:9" }
  ]
}
```

9 variants from 3 visual × 3 ratios. Scale to 15 or 30 by adding visual rows. Remember: no `count` field — emit one job per variant.

## Quick Reference

| Sub-task | Model | Why |
|----------|-------|-----|
| Brand-consistent variants from a hero (default) | `recraftv4` | Strongest at keeping design language consistent across many renders |
| Photoreal product / lifestyle variants | `flux-2-pro` | Best photoreal adherence, great for Meta/TikTok product ads |
| Variants with readable headline text baked in | `ideogram-v3` | Only model that reliably renders legible copy — use when you can't overlay |
| Face/character continuity across variants | `gemini-3-pro-image` | Nano Banana Pro locks subject identity best |
| Background swaps on a fixed subject | `gen-ai change-bg` (subcommand) | Keeps the subject pixel-identical, only swaps the scene |
| Ultra-cheap exploration before the flagship run | `gemini-3.1-flash-image` | ~5x cheaper, fast — use to pick winning prompts, then regenerate with flux/recraft |

Confirm IDs with `gen-ai models --mode image`.

## Procedure

- **Explicit variant axes.** Decide 3-4 axes up front (visual, composition, color, setting). Scattershot prompts make A/B results unreadable.
- **Hero as reference image on every job.** Use the `image` field in `defaults` — every variant inherits the brand look.
- **Deterministic naming = direct ad-platform import.** `{campaign}_{visual}_{composition}_{size}` parses cleanly in Meta/TikTok/Google ads CSV templates.
- **Draft cheap, upgrade winners.** Run 30 variants through `gemini-3.1-flash-image` for ~$1. Pick top 8. Regenerate those 8 through `flux-2-pro` or `recraftv4` for the final upload.
- **Text-safe zones per platform.** Meta Stories reserve 250px top + 310px bottom. TikTok reserves ~300px at bottom for UI. Prompt focal into the center 60% of the canvas.
- **Concurrency 6-8 for image variants.** Images are fast — higher concurrency finishes a 30-variant run in under 2 minutes. Drop to 4 if you see 429s.
- **Never overwrite silently.** Unique `id` per variant means unique output filename — resume is safe and collision-free.
- **Never claim results in the prompt.** "Viral ad, 10M views" doesn't improve output; describe framing, subject, lighting, mood.

## Pitfalls

- **Too many axes → unreadable A/B.** Vary 3-4 at most. If you change visual + composition + color + setting + headline in one variant, you can't isolate the winner.
- **Missing the hero reference.** Without `image` in defaults, each variant drifts visually — the bundle doesn't feel like one campaign.
- **Wrong aspect ratio for the platform.** TikTok is 9:16 full-bleed, Meta Reels is 9:16, Meta feed is 1:1 or 4:5 (not 1.91:1 anymore), Google Display is 300×250 / 728×90 / 160×600 — check the ad set requirements before fanning out.
- **Text in the image without localization plan.** Baked-in copy blocks localization — keep ad copy in the ads-manager overlay unless it's a one-market run.
- **Running 100 variants in one go with no draft phase.** 100 full-price flagship renders = wasted credits. Draft → pick → upgrade.
- **Overwriting results on re-runs.** Keep output dirs per run (`./variants-$(date +%F-%H%M)`) so resume + audit work cleanly.

## Verification

Run `gen-ai whoami` to confirm authentication, then re-run the failed command with `--debug`.

## Cost & time

| Variant count | Model | Credits each | Total | Wall time @ concurrency 8 |
|--------------|-------|--------------|-------|---------------------------|
| 9 variants | `recraftv4` | ~2 | ~18 | ~45s |
| 15 variants | `recraftv4` | ~2 | ~30 | ~90s |
| 30 variants (exploration) | `gemini-3.1-flash-image` | ~0.5 | ~15 | ~2 min |
| 30 variants (flagship) | `flux-2-pro` | ~2 | ~60 | ~3 min |
| 30 drafts + 8 upgraded | mixed | | ~30 | ~4 min total |

Always confirm with `gen-ai batch run variants.json --dry-run` and pause if the estimate exceeds the user's cap.

## See also

- `gen-ai-use/SKILL.md` — full CLI reference (flags, model catalog, auth)
- `gen-ai-batch/SKILL.md` — manifest shape, concurrency tuning, resume
- `gen-ai-workflows/SKILL.md` — general multi-step patterns
- `workflows/marketer-campaign-kit/SKILL.md` — chain before this to establish the hero + brand look
- `workflows/marketer-localize-campaign/SKILL.md` — chain after this to fan winning variants across markets
