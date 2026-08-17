---
name: marketer-localize-campaign
description: Localize a campaign across N markets.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: marketing
    tags: [picsart, marketing, campaigns, creative]
---

# Localize campaign

Take one finished campaign and adapt it to N markets — translated copy, culturally appropriate visuals, right-to-left handling for AR/HE, and text-expansion-safe layouts. Built for consistency (same campaign identity per market) and speed (one batch per locale).

## When to Use

- User has a shipped campaign in one market and needs to launch across 3+ additional locales.
- "Localize across DE, FR, JP, BR, ES" / "translate + adapt creatives per market" / "RTL version for AR".
- Master campaign has on-image text, people, or cultural motifs that need swapping per locale.
- Do NOT use for pure text translation (use an LLM directly) or for a fresh campaign (use `marketer-campaign-kit` first, then this skill).

## Prerequisites

Ask up front if the brief doesn't cover it (combine into one message):

1. **Master campaign assets** — paths/URLs to the approved creative. What's already finalized (hero, ad variants, email, LP)?
2. **Target locales** — language + region (e.g. `de-DE`, `fr-FR`, `ja-JP`, `ar-SA`, `pt-BR`). Region matters for cultural appropriateness.
3. **Translated copy** — is it done? If yes, paste it. If no, note which copywriter/vendor owns it (don't auto-translate ad copy — compliance risk).
4. **Cultural swaps needed** — people (face/ethnicity), settings (interior style, streetscape), props (food, gestures)? If the hero has a specific person, does that persist or get replaced per locale?
5. **RTL locales in scope** — Arabic, Hebrew, Farsi? Layout needs to mirror, text extends right-to-left.
6. **Deliverable naming** — ad-platform uploaders expect `{campaign}_{locale}_{size}.webp`.

Never auto-translate ad copy without a reviewer — legal/compliance owns sign-off.

## How to Run

1. **Inventory the master assets.** List every creative that needs localizing (hero, 6 ad variants, email, LP hero = 9 per locale × 5 locales = 45 assets).
2. **Collect translated copy per locale BEFORE generating.** Don't batch-run with English placeholders — you'll re-render everything.
3. **Choose adaptation strategy per asset:**
   - **Text-only change** (headline on a clean bg): use `ideogram-v3` with the translated copy and same visual.
   - **In-place motif swap** (person, setting): use an edit model (`qwen-image-edit-plus`, `flux-kontext-pro`) with the original image + a locale-specific prompt.
   - **Full regeneration** (complex cultural swap): generate fresh from the original prompt + locale guidance, referencing the original as `image` for composition.
4. **Write per-locale manifests.** One manifest per locale keeps naming clean and lets you parallelize across locales without collision.
5. **Estimate per locale.**
   ```bash
   gen-ai batch run localize-de.json --dry-run
   ```
6. **Run locales in sequence, not in parallel.** Review one locale's output end-to-end before kicking off the next — catching a cultural mismatch in DE means fixing the prompt before JP, FR, and BR inherit it.
   ```bash
   gen-ai batch run localize-de.json -c 4 -o ./out/de-DE
   ```
7. **Review with a native speaker per locale.** Every locale. No exceptions. Especially for JP (text rendering), AR (RTL + text), and any market with a dedicated country manager.
8. **Package and hand off.** Folder per locale, filename includes locale code, `results.json` archived for audit.

## Quick Reference

One manifest per locale keeps things tidy. `{locale}` and `{name}` placeholders support cross-locale reuse.

```json
{
  "defaults": {
    "model": "qwen-image-edit-plus",
    "imageUrls": ["https://cdn-pipeline-output.picsart.com/.../master-hero.webp"],
    "negativePrompt": "low quality, watermark, culturally inappropriate"
  },
  "jobs": [
    { "id": "hero_de-DE",        "prompt": "adapt hero for German market — preserve composition, swap setting to central-European urban, replace overlay text with: \"Jetzt entdecken\"",                     "aspectRatio": "16:9" },
    { "id": "ad_9x16_de-DE",     "prompt": "adapt ad for German market — keep product/subject, swap scene to Berlin street, overlay headline: \"Jetzt entdecken — 20% Rabatt\"",                          "aspectRatio": "9:16" },
    { "id": "ad_1x1_de-DE",      "prompt": "adapt ad for German market — clean background, German headline: \"Jetzt entdecken\", CTA: \"Mehr erfahren\"",                                                  "aspectRatio": "1:1"  },
    { "id": "email_de-DE",       "prompt": "email header for German launch — German copy on-canvas: \"Jetzt entdecken\"",                                                                                   "aspectRatio": "3:1"  },
    { "id": "lp_hero_de-DE",     "prompt": "LP hero for German market — same product, German subtitle: \"Entdecken Sie die neue Kollektion\"",                                                              "aspectRatio": "16:9" }
  ]
}
```

For RTL locales (AR, HE), mirror layouts explicitly in the prompt: "right-to-left layout, headline reads from right, mirror the hero composition".

For voiceover localization (video campaigns), pair with `gen-ai generate -m eleven-multilingual-v2` per locale — keep `voice` ID consistent across locales for brand continuity.

## Quick Reference

| Sub-task | Model | Why |
|----------|-------|-----|
| In-place text swap on clean bg | `ideogram-v3` | Only model that reliably renders legible text in multiple scripts (Latin, Cyrillic, JP, AR) |
| Motif / setting swap, preserve subject | `qwen-image-edit-plus` | Strong at in-place edits — keeps composition, swaps scene |
| Instructed edits with reference | `flux-kontext-pro` | Precise edit-to-prompt adherence, good when you need surgical changes |
| Full regeneration with cultural guidance | `flux-2-pro` | Best photoreal; reference the original as `image` to keep composition |
| Face/person swap with identity consistency | `gemini-3-pro-image` (Nano Banana Pro) | Best at persisting or deliberately swapping a subject across renders |
| Multilingual voiceover | `eleven-multilingual-v2` | Consistent voice across locales — set `voice` ID in `defaults` |
| Background replacement only | `gen-ai change-bg` (subcommand) | Pixel-identical subject, locale-appropriate scene |

Confirm IDs with `gen-ai models`.

## Procedure

- **Text expansion is real.** German runs 30% longer than English, French 20% longer, JP/ZH 30% shorter but character-dense. Leave 25-30% breathing room in text-safe zones before rendering.
- **Never auto-translate ad copy.** Compliance owns sign-off. Collect human-reviewed translations, then render.
- **RTL locales mirror the layout.** AR/HE need hero composition flipped and headline-reads-right. State it explicitly in the prompt.
- **Culturally appropriate faces/settings.** A Berlin scene feels wrong in Tokyo. If the master has a person, decide early: persist (identity consistency via Nano Banana Pro) or swap per market.
- **`ideogram-v3` is the only reliable option for on-image text in non-Latin scripts.** Other models render JP/AR/KR as gibberish. Use it for any text-bearing asset.
- **One locale at a time, reviewed end-to-end.** Parallelizing 5 locales hides prompt bugs until you've spent 5x the credits.
- **Native-speaker review is non-negotiable.** LLMs miss cultural nuance. Every locale gets eyes on from someone in-market before shipping.
- **Filename locale codes enable direct ad-platform upload.** `launch_de-DE_9x16.webp` parses cleanly in Meta / Google / TikTok CSV importers.
- **Keep voice ID consistent across multilingual VO.** Same voice across markets = brand continuity. Set `voice` in `defaults`, not per-job.

## Pitfalls

- **Text overflowing the safe zone in DE / RU / FI.** Copy expansion wasn't accounted for in the master layout — leave 25-30% margin before localizing.
- **JP / AR / KR text renders as gibberish.** Wrong model. Use `ideogram-v3` for any non-Latin on-image text, not flux/recraft.
- **RTL layout not mirrored.** Arabic users get a headline that reads wrong direction + hero composition that feels wrong. Explicit mirror instruction fixes it.
- **Culturally tone-deaf imagery.** A Christmas-themed visual in a Muslim-majority market, a left-hand gesture in SEA — run cultural review per market.
- **Translating in the prompt with the LLM.** Ad copy goes through compliance; don't have the model "translate this headline to German" mid-prompt. Use human-reviewed translations.
- **Parallelizing all 5 locales upfront.** One prompt bug becomes 5 locales of wasted credits. Sequence them; review DE, then kick off FR.
- **Inconsistent voice across locales in VO.** Different `voice` IDs per locale breaks brand continuity — set one voice ID across all TTS jobs.
- **Skipping native-speaker review.** "The model did fine on German last time" is how you ship a mistranslation.

## Verification

Run `gen-ai whoami` to confirm authentication, then re-run the failed command with `--debug`.

## Cost & time

Rough estimate to localize a 9-asset campaign across 5 locales (45 total renders):

| Asset type | Count per locale | Model | Credits each | Per locale | 5 locales |
|------------|-------|-------|--------------|------------|-----------|
| Hero + ad + email + LP (motif swap) | 5 | `qwen-image-edit-plus` | ~2 | 10 | 50 |
| Text-bearing assets (headlines, CTAs) | 4 | `ideogram-v3` | ~3 | 12 | 60 |
| **Image subtotal** | **9** | | | **~22** | **~110 credits** |
| Voiceover (if video campaign) | 1 per locale | `eleven-multilingual-v2` | ~1-3 | ~2 | ~10 |
| **Grand total** | | | | | **~120 credits** |
| **Wall time** (sequential per locale, concurrency 4 within) | | | | ~3 min | ~15 min |

Full regeneration via `flux-2-pro` roughly doubles the image credits. Estimate explicitly with `gen-ai batch run localize-{locale}.json --dry-run` before spending.

## See also

- `gen-ai-use/SKILL.md` — full CLI reference (flags, model catalog, auth, TTS models)
- `gen-ai-workflows/SKILL.md` — general multi-step patterns
- `gen-ai-batch/SKILL.md` — manifest shape, placeholders, concurrency
- `workflows/marketer-campaign-kit/SKILL.md` — run before this to produce the master campaign
- `workflows/marketer-ad-variant-factory/SKILL.md` — run winners through localization after A/B tests pick them
