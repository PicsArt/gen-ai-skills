
# Blog to visuals

Take a written article and generate the 5-10 visuals it needs to ship: hero, 3-5 inline illustrations, social share card, OG image, and optional pull-quote cards — all in one cohesive visual style pulled from the article itself.

## When to Use

- User has a blog draft (markdown / doc / URL) and wants article-ready visuals without stock-hunting.
- "Illustrate this post" / "render visuals for my article" / "need a hero + OG + 3 inline images".
- Publishing an evergreen post and wants distinctive visuals instead of generic stock.
- Refreshing an old post with new imagery.
- Do NOT use for multi-channel campaign kits (use `marketer-campaign-kit`) or for ad A/B variants (use `marketer-ad-variant-factory`).

## Prerequisites

Ask up front if the draft doesn't answer (combine into one message):

1. **Article source** — file path, URL, or paste? Confirm you can read the full text, not just the H1.
2. **Visual count** — default is hero + 3 inline + OG + social share card = 6 visuals. Confirm or trim.
3. **Style direction** — photoreal (journalistic), editorial illustration, flat vector, 3D render, moody/cinematic? If unsure, read the article's tone and propose.
4. **Brand colors / brand.md** — colors (hex) or a brand.md path for gating.
5. **Output destination** — local folder (default `./assets/blog-{slug}/`) and/or Picsart Drive.
6. **OG vs social share needs** — OG at 1200×630 for Twitter/LinkedIn link previews. Square 1:1 social card is separate.

## How to Run

1. **Read the full article.** Extract: H1 (title), section headings (likely inline moments), a 2-sentence summary (hero concept), 1-2 pullquote candidates (quote cards).
2. **Draft prompts from the article, not from thin air.** Each prompt should reference specific moments, objects, or concepts mentioned in the post — this is what makes the visuals feel like they belong.
3. **Pick one style spine.** All 6 visuals should share aesthetic (e.g. "editorial illustration, limited palette, dark background, magenta accent"). Put this in the manifest `defaults.negativePrompt` and repeat the style phrase in each prompt.
4. **Estimate first.**
   ```bash
   gen-ai batch run blog-visuals.json --dry-run
   ```
5. **Generate the hero alone, show the user, approve the style.** Hero becomes the style anchor — its URL goes into `image` for every inline/OG job.
   ```bash
   gen-ai generate -m flux-2-pro -p "$HERO_PROMPT" --aspect-ratio 16:9 \
     --download ./assets/blog-$SLUG
   ```
6. **Batch the rest.** Inline illustrations, OG, social card — all reference the hero.
   ```bash
   gen-ai batch run blog-visuals.json -c 4 -o ./assets/blog-$SLUG
   ```
7. **OG image check.** Render at 1200×630 exactly. Verify legibility at small sizes (preview will be 300px wide on Twitter mobile).
8. **Deliver.** Paste markdown image tags into the post at correct anchor points, share the approved asset folder, note credits spent.

## Quick Reference

```json
{
  "defaults": {
    "model": "recraftv4",
    "negativePrompt": "low quality, watermark, stock-photo feel, generic",
    "imageUrls": ["https://cdn-pipeline-output.picsart.com/.../hero.webp"]
  },
  "jobs": [
    { "id": "hero",        "model": "flux-2-pro", "prompt": "editorial hero — $ARTICLE_SUMMARY, cinematic lighting, dark palette, magenta accent", "aspectRatio": "16:9" },
    { "id": "inline-1",    "prompt": "concept illustration for section: $H2_1 — editorial, dark palette, magenta accent",   "aspectRatio": "1:1" },
    { "id": "inline-2",    "prompt": "concept illustration for section: $H2_2 — editorial, dark palette, magenta accent",   "aspectRatio": "1:1" },
    { "id": "inline-3",    "prompt": "concept illustration for section: $H2_3 — editorial, dark palette, magenta accent",   "aspectRatio": "1:1" },
    { "id": "og",          "model": "ideogram-v3", "prompt": "editorial poster, headline: \"$ARTICLE_TITLE\", dark palette, magenta accent", "aspectRatio": "1200x630" },
    { "id": "social-card", "prompt": "square share card — $ARTICLE_SUMMARY, editorial, dark palette, magenta accent",       "aspectRatio": "1:1" },
    { "id": "quote-1",     "model": "ideogram-v3", "prompt": "editorial quote card, large type: \"$PULLQUOTE\", dark background, magenta underline", "aspectRatio": "1:1" }
  ]
}
```

Per-job `model` overrides `defaults.model`. Use `ideogram-v3` for anything with on-image headline text.

## Quick Reference

| Sub-task | Model | Why |
|----------|-------|-----|
| Hero (photoreal editorial) | `flux-2-pro` | Best photoreal, strong prompt adherence for wide cinematic shots |
| Hero (illustrative / design-forward) | `recraftv4` | Clean editorial illustration, design-magazine aesthetic |
| Inline illustrations (design style) | `recraftv4` | Stays consistent across 3-5 inline images, good at abstract concepts |
| OG image with readable title | `ideogram-v3` | Only image model that reliably renders legible headline copy |
| Pull-quote cards | `ideogram-v3` | Same reason — needs crisp on-image text |
| Ultra-cheap draft to pick a style | `gemini-3.1-flash-image` | Cheap + fast, use to lock the look before flagship run |
| Photoreal portraits in-article | `gemini-3-pro-image` (Nano Banana Pro) | Best for a consistent person/subject across 2+ images |

Confirm with `gen-ai models --mode image`.

## Procedure

- **Read the full article, not just the title.** Prompts pulled from H2s, examples, and the conclusion land more relevantly than title-only prompts.
- **One style spine across all 6 visuals.** Put the style phrase ("editorial illustration, dark palette, magenta accent") in every prompt — not just `defaults` — repetition tightens consistency.
- **Hero first, then reference-chain.** Approve the hero look, then pass its URL as `image` to inline/OG/social jobs.
- **OG image rule: title must be legible at 300px wide.** Big bold type (50-80pt equivalent), strong contrast, no small text. Use `ideogram-v3` because it's the only model that reliably renders readable copy on the canvas.
- **Inline illustrations are 1:1, not 16:9.** Readers are on mobile — tall narrow images waste scroll space. Square or 4:3 reads better in-article.
- **Match the tone, not the topic.** An article about productivity doesn't need a clock illustration — abstract mood visuals age better than literal ones.
- **Name files semantically.** `hero.webp`, `inline-1-why-it-matters.webp`, `og.webp` — not `batch-output-001.webp`. Your future self maintaining the post will thank you.
- **Save a quote-card spare.** If the post gets picked up by social, a pre-rendered pull-quote card cuts 10 min off the amplification work.

## Pitfalls

- **OG text unreadable.** Using `flux-2-pro` or `recraftv4` for the OG means illegible squiggles where the headline should be. Use `ideogram-v3` for OG + quote cards.
- **Hero rendered in 1:1 instead of 16:9.** The blog's hero slot is almost always wide — check the CMS template before rendering.
- **OG at 1200×1200 or 1920×1080.** LinkedIn + Twitter cache at 1200×630. Mismatched sizes get cropped badly.
- **Inline images too literal.** Don't render a stock clock for "time management" — abstract, moody, relevant-feeling wins.
- **6 prompts, 6 styles.** If every visual has a different aesthetic, the post feels assembled from stock. Lock one style phrase and repeat it.
- **Skipping the hero approval step.** Running all 6 in one batch produces 6 disconnected looks — approve the hero first, reference-chain the rest.
- **Forgetting alt text.** Generated images still need descriptive `alt` for accessibility and SEO — write them as you drop each image into the post.

## Verification

Run `gen-ai whoami` to confirm authentication, then re-run the failed command with `--debug`.

## Cost & time

Rough estimate for the standard 6-visual blog kit:

| Asset | Count | Model | Credits each | Subtotal | Time |
|-------|-------|-------|--------------|----------|------|
| Hero | 1 | `flux-2-pro` | ~2 | 2 | ~25s |
| Inline illustrations | 3 | `recraftv4` | ~2 | 6 | ~60s parallel |
| OG image | 1 | `ideogram-v3` | ~3 | 3 | ~25s |
| Social square | 1 | `recraftv4` | ~2 | 2 | ~25s |
| **Total** | **6** | | | **~13 credits** | **~2 min** |

Add pull-quote cards at ~3 credits each. Budget goes up fast if you run hero at `gemini-3-pro-image` (~5) — reserve that for when subject identity must persist.

## See also

- `gen-ai-use/SKILL.md` — full CLI reference (flags, model catalog, auth)
- `gen-ai-workflows/SKILL.md` — general multi-step pipelines
- `gen-ai-batch/SKILL.md` — manifest shape, concurrency, resume
- `workflows/marketer-campaign-kit/SKILL.md` — use if the blog launch also needs LinkedIn + email + LP assets
- `workflows/marketer-localize-campaign/SKILL.md` — use to adapt the post's visuals per market
