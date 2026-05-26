---
name: prosumer-headshot-studio
description: Selfie to four polished headshots for any use.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: prosumer
    tags: [picsart, prosumer, creator, social]
---

# Headshot studio

Input: one casual phone selfie. Output: a set of professional-grade headshots at platform-correct ratios — LinkedIn polished, ID / passport, editorial / creator portrait, casual founder shot — with the same face across every variant. The bar is "plausibly a real photoshoot" not "obvious AI filter".

## When to Use

- Solo creator, founder, or job-seeker needs a LinkedIn / speaker bio / About page headshot and doesn't want a photographer
- User has one usable selfie (well-lit enough, face clearly visible) and wants 3-5 polished variants
- They say "headshot", "LinkedIn photo", "professional profile pic", "polish this selfie", "make this a pro photo", "editorial portrait"
- They need the same face across multiple styles (not just one image)

**Don't use for:** group photos, full-body fashion shoots (different model family), or character consistency across video clips (use `motion-studio` with a generated reference).

## Prerequisites

Ask before running (combine into one message):

1. **Source selfie** — path or URL. Must be frontal, eyes visible, decent lighting. If the source is blurry or dark, recommend re-shooting before generation.
2. **Styles wanted** — which variants? Default set is LinkedIn / editorial / casual / ID. Offer mix-and-match.
3. **Wardrobe direction** — should the model wear the same outfit as the source, a suggested one ("dark blazer", "neutral knit"), or let the model pick per style?
4. **Aesthetic lean** — warm / cool, editorial-magazine / corporate-safe / creative-tech?
5. **Background** — neutral studio, office, outdoor, plain color, blurred environment?
6. **Aspect ratios needed** — 1:1 for LinkedIn/ID, 4:5 for editorial, 9:16 for reels / stories?

## How to Run

```
1. INTERVIEW        → confirm source, styles, wardrobe, ratios
2. ENHANCE SOURCE   → upscale the selfie for better identity lock
3. GENERATE         → i2i per style, face reference locked
4. REVIEW           → verify face consistency; check hands, eyes, ears
5. REGENERATE       → one-at-a-time for misses
6. DELIVER          → per-platform folder with correct ratios
```

1. **Upscale the selfie first.** Gemini / Flux i2i models lock identity better from a sharp reference:
   ```bash
   gen-ai enhance -i selfie.jpg -m topaz-upscale-image --download ./headshots/src
   ```
   Alternatively use `picsart-enhance` for a lighter pass.

2. **Estimate the batch.**
   ```bash
   gen-ai batch run headshots.json --dry-run
   ```

3. **Generate per style with the enhanced selfie as reference.** Face identity locking is the whole game — always pass `-i`:
   ```bash
   gen-ai generate -m gemini-3-pro-image -i ./headshots/src/selfie-hd.png \
     -p "professional LinkedIn headshot of the same person, dark blazer over neutral knit, soft studio lighting, clean charcoal background, shallow depth of field, 50mm lens look, editorial corporate photography" \
     --ar 1:1 --download ./headshots/linkedin
   ```

4. **Review each output for identity drift.** Common failure modes:
   - Face looks subtly different (different nose, jawline, eye shape)
   - Skin oversmoothed into uncanny-valley territory
   - Hair changed color or style beyond the prompt
   - Eyes slightly misaligned

   If the face drifted, regenerate with a stronger prompt: "exact same face as the reference image, matching bone structure, skin tone, eye color, and hair exactly".

5. **Deliver in a platform-correct folder layout.**
   ```
   ./headshots/
     linkedin/  1:1, 1200×1200
     ig/        4:5, 1080×1350
     story/     9:16, 1080×1920
     id/        1:1, 600×600, neutral background
     editorial/ 4:5, wider crop
   ```

## Quick Reference

```json
{
  "defaults": {
    "model": "gemini-3-pro-image",
    "imageUrls": ["./headshots/src/selfie-hd.png"]
  },
  "jobs": [
    {
      "id": "linkedin",
      "prompt": "professional LinkedIn headshot of the same person, dark blazer over neutral top, soft studio lighting, clean charcoal background, shallow DoF, 50mm look, editorial corporate photography, exact same face as reference",
      "aspectRatio": "1:1"
    },
    {
      "id": "id",
      "prompt": "passport-style ID photo of the same person, neutral expression, plain white background, even front lighting, shoulders visible, no shadows, exact same face as reference",
      "aspectRatio": "1:1"
    },
    {
      "id": "editorial",
      "prompt": "editorial portrait of the same person, moody side light, textured dark background, film grain, 85mm lens, shallow DoF, magazine cover composition, exact same face as reference",
      "aspectRatio": "4:5"
    },
    {
      "id": "casual",
      "prompt": "casual founder portrait of the same person, natural window light, cafe background blurred, warm tones, slight smile, 35mm lens, documentary style, exact same face as reference",
      "aspectRatio": "4:5"
    }
  ]
}
```

## Quick Reference

| Sub-task | Model | Why |
|---|---|---|
| Primary — identity-locked headshots | `gemini-3-pro-image` (Nano Banana Pro) | Best face fidelity across restyles, strong prompt adherence |
| Alternative — creative restyles | `flux-kontext-pro` | Strong i2i edit, faster iteration, slightly less identity-strict |
| Source enhancement / upscale | `topaz-upscale-image` | Sharpest 2-4× upscale before i2i |
| Softer enhancement (fewer artifacts) | `picsart-enhance` | Gentle sharpen + color; safer for already-good selfies |
| Final-pass upscale for print / 4K web | `topaz-upscale-image` | Crisps up the output to retina / print quality |
| Background swap only (keep face 100%) | `picsart-change-bg` | When the face is perfect but the background is wrong |
| Background removal (for transparent PNG) | `picsart-remove-bg` | Clean cutout for site / avatar use |

**Avoid `flux-2-pro` here** — it's t2i-dominant and will drift the face more than Gemini or Kontext.

## Procedure

- **Source quality is everything.** A blurry, backlit, or heavily-filtered selfie produces drifted faces. Spend 30 seconds asking the user to re-shoot in daylight before burning credits.
- **Always upscale the source first.** Sharper reference = tighter identity lock downstream.
- **Use the phrase "the same person" or "exact same face as reference"** in every prompt. Models respond to explicit identity cues.
- **Generate 1-2 variants per style first**, verify identity, then scale up. Don't batch 12 before checking the first one.
- **Keep wardrobe + lighting changes explicit per style** — don't leave them ambiguous. "Dark blazer, neutral knit" beats "business clothes".
- **Check eyes, ears, and hairline** — these are where AI headshot drift hides. Ears especially: asymmetric, missing, or fused ears are a giveaway.
- **Avoid extreme angles or expressions in the prompt** — profile shots, wide laughs, tilted-head glamour poses all break identity. Frontal, neutral-to-slight-smile is the safe zone.
- **Upscale finals to 2048+** for LinkedIn / About-page use. The source was phone quality; the output should not ship at that resolution.

## Pitfalls

- **Face drifts subtly across variants** — source too low-res, prompt didn't say "same person", or model wasn't an identity-locking i2i. Fix: upscale source, use Gemini 3 Pro, explicit identity phrasing.
- **Uncanny plastic skin** — over-processed look. Add "natural skin texture, subtle pores, no beauty retouching" to the prompt.
- **Asymmetric or fused ears** — regenerate; don't try to patch in post. Gemini 3 handles this better than older models.
- **Wrong aspect ratio for LinkedIn** — LinkedIn profile is effectively circular cropped from 1:1. Plan compositions with centered face + breathing room on all sides.
- **Batch-generating before verifying one** — if style 1 drifted, styles 2-4 will too. Always verify the first output before fanning out.
- **Forgetting to upscale the final** — shipping a 1024×1024 headshot to LinkedIn looks soft on retina screens. Always final-upscale.

## Verification

Run `gen-ai whoami` to confirm authentication, then re-run the failed command with `--debug`.

## Cost & time

| Asset | Model | Credits | Time |
|---|---|---|---|
| Source upscale (topaz) | `topaz-upscale-image` | ~2 | ~15s |
| 1× headshot (Gemini 3 Pro, i2i) | `gemini-3-pro-image` | ~3 | ~25s |
| 1× headshot (Flux Kontext, i2i) | `flux-kontext-pro` | ~4 | ~30s |
| Final upscale per image | `topaz-upscale-image` | ~2 | ~15s |
| **Typical 4-style set (Gemini)** | — | **~16** | **~2 min** |
| **Typical 4-style set + final upscales** | — | **~24** | **~3 min** |

## See also

- [gen-ai-use](../gen-ai-use/SKILL.md) — CLI command reference, flags, model IDs, batch manifest schema
- [multi-channel-bundle](../multi-channel-bundle/SKILL.md) — when the headshot is part of a broader founder launch
- [text-to-visual](../text-to-visual/SKILL.md) — for the ongoing creator-content queue
