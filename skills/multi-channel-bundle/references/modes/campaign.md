
# Campaign kit

One brief in, full platform-native bundle out: LinkedIn card, IG feed + story, email hero, LP hero, and 3 ad variants per size. All from a single manifest, brand-consistent across formats.

## When to Use

- User has a written brief (launch, seasonal, product announcement) and needs shippable creative for 4+ channels at once.
- "Generate the full campaign kit" / "need all the sizes" / "launch assets across LinkedIn, IG, email, LP, ads".
- User is about to hand off to paid, email, and organic — wants ONE visual system across all surfaces.
- Do NOT use this for a single hero (use `gen-ai generate` directly) or for 50+ A/B variants of one creative (use `marketer-ad-variant-factory`).

## Prerequisites

Ask up front if the brief doesn't cover it (combine into one message, 4-6 questions):

1. **What's the campaign** — product, offer, or announcement in one sentence?
2. **Which channels?** Default bundle is LinkedIn + IG feed + IG story + email hero + LP hero + 3 ad variants per size. Confirm or trim.
3. **Brand direction** — colors (hex), mood (photoreal / editorial / illustrative), any existing brand.md path?
4. **Hero subject** — one image-worthy concept that anchors the kit (product shot, scene, abstract treatment).
5. **Deadline / budget cap** — hard ceiling on credits? Any date anchoring copy?
6. **Save destination** — local folder and/or Picsart Drive folder name.

If brief answers these already, skip to the manifest.

## How to Run

1. **Build the manifest.** Scaffold `campaign.json` with one job per asset. Use `defaults` for shared settings (model, negativePrompt, brand reference imageUrls). Each job gets a unique `id` so the file lands at `out/<id>.webp`.
2. **Estimate before spending.** Always run dry-run + estimate first:
   ```bash
   gen-ai batch run campaign.json --dry-run
   gen-ai pricing flux-2-pro    # per-call cost sanity check
   ```
3. **Generate the hero first.** Produce the anchor hero alone, show the user, get approval. The hero becomes the reference image (`imageUrls`) for every other asset to preserve brand look.
   ```bash
   gen-ai generate -m flux-2-pro -p "$HERO_PROMPT" --ar 16:9 \
     --download ./out --save-to-drive --drive-folder "$CAMPAIGN-$(date +%F)"
   ```
4. **Run the bundle in parallel.** Point remaining jobs at the approved hero URL as an `imageUrls` reference. Concurrency 4 is the sweet spot for image batches.
   ```bash
   gen-ai batch run campaign.json -c 4 -o ./out
   ```
5. **Review results.json.** Filter for `status !== "completed"`, retry failures with `gen-ai batch resume ./out`.
6. **Deliver.** Rename to channel conventions (`linkedin.webp`, `ig-feed.webp`, `ig-story.webp`, `email-hero.webp`, `lp-hero.webp`, `ad-9x16-a.webp`, etc.), share the output folder or approved Drive upload, note the total credit spend.

## Quick Reference

```json
{
  "defaults": {
    "model": "flux-2-pro",
    "negativePrompt": "low quality, watermark, stock-photo feel, cluttered",
    "imageUrls": ["https://cdn-pipeline-output.picsart.com/.../hero.webp"]
  },
  "jobs": [
    { "id": "linkedin",      "prompt": "$BRIEF — LinkedIn post card, clean focal, 1200x627",       "aspectRatio": "1200x627" },
    { "id": "ig-feed",       "prompt": "$BRIEF — Instagram feed, centered subject, safe margins",  "aspectRatio": "1:1" },
    { "id": "ig-story",      "prompt": "$BRIEF — Instagram story, subject top-third, text-safe bottom", "aspectRatio": "9:16" },
    { "id": "email-hero",    "prompt": "$BRIEF — email header, wide cinematic",                    "aspectRatio": "3:1" },
    { "id": "lp-hero",       "prompt": "$BRIEF — landing page hero, dramatic, brand-forward",      "aspectRatio": "16:9" },
    { "id": "ad-9x16-a",     "prompt": "$BRIEF — vertical ad variant A, high contrast",            "aspectRatio": "9:16" },
    { "id": "ad-9x16-b",     "prompt": "$BRIEF — vertical ad variant B, close-up focal",           "aspectRatio": "9:16" },
    { "id": "ad-1x1-a",      "prompt": "$BRIEF — square ad variant A",                             "aspectRatio": "1:1" },
    { "id": "ad-1x1-b",      "prompt": "$BRIEF — square ad variant B, different angle",            "aspectRatio": "1:1" },
    { "id": "ad-16x9-a",     "prompt": "$BRIEF — landscape ad variant A",                          "aspectRatio": "16:9" },
    { "id": "ad-16x9-b",     "prompt": "$BRIEF — landscape ad variant B",                          "aspectRatio": "16:9" }
  ]
}
```

For reviewable campaign kits, emit N jobs with unique `id`s for N variants. The `imageUrls` reference in `defaults` is what holds the kit visually together.

## Quick Reference

| Asset | Model | Why |
|-------|-------|-----|
| Photoreal hero, product, lifestyle | `flux-2-pro` | Best photoreal image model, strong prompt adherence, 16:9 works well |
| Editorial / design-forward / illustrative | `recraftv4` | Clean design aesthetic, strong typography-friendly backgrounds |
| Text-in-image (headline rendered in asset) | `ideogram-v3` | Only model that reliably renders legible copy on the canvas |
| Heavy brand identity / character consistency | `gemini-3-pro-image` (Nano Banana Pro) | Best subject consistency across variations |
| Quick drafts to sanity-check composition | `gemini-3.1-flash-image` | Cheap + fast for iteration before flagship render |

Run `gen-ai models --mode image` to confirm IDs — model names ship frequently.

## Procedure

- **Platform-native aspect ratios, always.** LinkedIn post card is 1200×627 (not 16:9), IG story needs 9:16 with subject in top two-thirds so bio + sticker zones don't crop the focal.
- **One hero, then reference-chain.** Generate and approve the hero, then pass its CDN URL as `image` to every downstream job — brand look locks in without re-prompting from zero.
- **Text-safe zones:** IG story has 250px top + 310px bottom reserved for UI. Email hero needs 80px lateral safe area for mobile rendering. Never place the focal where it'll crop.
- **Negative prompts are cheap insurance.** `"low quality, watermark, stock-photo feel, extra limbs"` in `defaults` prevents a lot of regens.
- **Keep a stable output folder from day one.** `-o ./out` gives the team one place to review files and keeps `results.json` aligned with the downloaded assets.
- **Use `results.json` as the deliverable ledger.** Every URL, local path, status, model, and duration is there — paste it into the handoff doc and estimate spend from `gen-ai pricing`.
- **Regenerate 1 asset, not the bundle.** If LinkedIn comes out weak, re-run just that job with a tweaked prompt — don't re-batch the whole kit.

## Pitfalls

- **Using 16:9 for LinkedIn post card.** It's 1200×627 — pass `--aspect-ratio 1200x627` explicitly.
- **Focal centered for IG story.** UI chrome crops it. Prompt for "subject in upper third".
- **Skipping the hero-first step.** Running all 11 in one shot gives 11 different brand looks. Approve hero, then chain.
- **Ignoring Picsart Drive folder naming.** Generic folders ("assets", "test") pile up — use `$CAMPAIGN-$(date +%F)` so the team can find it later.
- **Over-claiming in the prompt.** "Award-winning, viral, 10 million views" doesn't help — describe what's in the frame.
- **Generating ad copy in-image when you need localization.** Headline text baked into the image means you re-generate per locale. Keep ad copy in overlay unless you're already using `marketer-localize-campaign`.

## Verification

Run `gen-ai whoami` to confirm authentication, then re-run the failed command with `--debug`.

## Cost & time

Rough estimate for the standard 11-asset kit (flux-2-pro mostly):

| Asset type | Count | Credits each | Subtotal | Wall time |
|------------|-------|--------------|----------|-----------|
| Hero (flux-2-pro) | 1 | ~2 | 2 | ~25s |
| Platform heroes (LinkedIn/IG/email/LP) | 4 | ~2 | 8 | ~30s parallel |
| Ad variants (3 sizes × 2) | 6 | ~2 | 12 | ~45s parallel |
| **Total** | **11** | | **~22 credits** | **~2 min** |

Switch to `recraftv4` for illustrative kits (similar credits) or `ideogram-v3` if any asset needs on-image text (slightly higher). Always confirm with `gen-ai batch run campaign.json --dry-run` before spending.

## See also

- `gen-ai-use/SKILL.md` — full CLI reference (all flags, model catalog, auth)
- `gen-ai-workflows/SKILL.md` — general multi-step pipeline patterns
- `gen-ai-batch/SKILL.md` — manifest shape, concurrency tuning, error handling
- `workflows/marketer-ad-variant-factory/SKILL.md` — chain after this for heavy A/B testing
- `workflows/marketer-localize-campaign/SKILL.md` — chain after this to adapt the kit across markets
