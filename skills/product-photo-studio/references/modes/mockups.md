
# Product mockups

Render a product (physical or digital) into lifestyle scenes: phone in hand on a cafe table, laptop open on a desk, packaging on a shelf, wearable on a model, canvas print on a wall. Photoreal fidelity is the bar — these mockups are going on store pages, pitch decks, and Instagram feeds where obvious AI artifacts kill conversion.

## When to Use

- Etsy / Shopify / POD seller needs store-listing mockups from one artwork file
- Indie maker wants lifestyle scenes for a product that ships next week
- SaaS founder needs "app in hand" or "laptop on desk" mockups for the landing page
- Consumer brand renders packaging in context (shelf, counter, unboxing) without a photoshoot
- The user says "product mockup", "lifestyle shot", "in-context render", "packaging mockup", "mockup on a model"

**Don't use for:** fully synthetic products without reference art (use `gen-ai generate` direct), or catalog-scale batches over 50 SKUs (use `gen-ai-workflows` Workflow 3).

## Prerequisites

Before generating, ask:

1. **Artwork / product asset** — path or URL? Is it a flat artwork (print, tee graphic), a product photo (mug, bottle), or a UI screenshot (app screen)?
2. **Surfaces / contexts** — which mockups? (e.g. "tee, mug, poster, tote" or "phone in hand, laptop on desk, packaging on shelf")
3. **Scene mood** — minimal studio, warm home, urban cafe, outdoor lifestyle, editorial luxury?
4. **Model / human presence** — should a person be in frame? If yes, any demographic direction?
5. **Brand constraints** — colors that must appear or be avoided, a specific aesthetic reference?
6. **Deliverable ratio** — Shopify product tile (4:5 or 1:1), IG feed (1:1), IG story (9:16), landing-page hero (16:9)?

If the user pasted a brief with the product + surfaces, skip to workflow.

## How to Run

```
1. INTERVIEW        → product type, surfaces, scene, ratio
2. PLAN & ESTIMATE  → one row per surface, estimate credits
3. GENERATE         → batch, with artwork passed as -i reference
4. REVIEW           → open each, check brand placement + realism
5. REGENERATE       → only the ones that missed
6. DELIVER          → organized folder, Drive-synced
```

1. **Identify what stays locked.** If the user has a flat artwork (tee graphic, sticker, poster), the design must survive across surfaces — use `gemini-3-pro-image` or `flux-kontext-pro` which preserve identity. If the product is 3D (mug, bottle, packaging), a lifestyle prompt with `flux-2-pro` usually wins.

2. **Write one job per surface.** Do not try to render "tee + mug + poster in one scene" — you'll get a muddy composite. One image per mockup, always.

3. **Estimate before spending.**
   ```bash
   gen-ai batch run mockups.json --dry-run
   ```

4. **Generate with artwork as reference.** For flat-artwork-on-product:
   ```bash
   gen-ai generate -m gemini-3-pro-image -i ./art.png \
     -p "the same artwork printed on a white cotton t-shirt, worn by a model, studio lighting, neutral background" \
     --ar 1:1 --download ./mockups
   ```

   For in-context lifestyle (3D product):
   ```bash
   gen-ai generate -m flux-2-pro \
     -p "matte charcoal ceramic espresso cup on a linen tablecloth, morning light, shallow DoF, minimal scandi home" \
     --ar 4:5 --download ./mockups
   ```

5. **Review every output.** Check: does the artwork/product look believable on the surface? Are the shadows right? Is the brand readable? Regenerate misses individually with `gen-ai redo`.

## Quick Reference

Physical merch fan-out (POD):
```json
{
  "defaults": {
    "model": "gemini-3-pro-image",
    "imageUrls": ["./art.png"],
    "aspectRatio": "1:1"
  },
  "jobs": [
    { "id": "tee",     "prompt": "the same artwork printed on a white cotton tee worn by a model, studio white background" },
    { "id": "mug",     "prompt": "the same artwork on an 11oz white ceramic mug on a wood desk, soft window light" },
    { "id": "poster",  "prompt": "the same artwork as a framed poster on a neutral gallery wall, natural light" },
    { "id": "tote",    "prompt": "the same artwork on a natural canvas tote bag held by a model, urban street" },
    { "id": "hoodie",  "prompt": "the same artwork on a heather grey hoodie worn by a model, outdoor park" },
    { "id": "sticker", "prompt": "the same artwork as a die-cut sticker on a laptop lid, cafe ambient" }
  ]
}
```

Lifestyle product scenes (SaaS / hardware):
```json
{
  "defaults": { "model": "flux-2-pro", "aspectRatio": "16:9" },
  "jobs": [
    { "id": "phone-in-hand", "prompt": "modern app UI on an iPhone 15 Pro held in one hand, cafe background, shallow DoF", "imageUrls": ["./screen.png"] },
    { "id": "laptop-desk",   "prompt": "same app on a MacBook Pro at a minimal wooden desk, morning light, plant in frame" },
    { "id": "billboard",     "prompt": "same product packaging on an urban billboard at dusk, cinematic wide shot" }
  ]
}
```

## Quick Reference

| Sub-task | Model | Why |
|---|---|---|
| Flat artwork on merch (identity-critical) | `gemini-3-pro-image` (Nano Banana Pro) | Best at preserving the exact artwork across surfaces |
| Flat artwork on merch (alternative) | `flux-kontext-pro` | Strong i2i edit, good for placement prompts |
| 3D product in lifestyle scene | `flux-2-pro` | Highest photoreal fidelity for free composition |
| Packaging / shelf / retail | `seedream-4.5` | Strong at product-in-environment realism |
| UI screenshot in device frame | `gpt-image-1.5` | Handles screens + devices without warping the UI |
| Model-worn apparel | `gemini-3-pro-image` | Best skin / fabric interaction from a flat reference |
| Large-scale batch (20+ SKUs, same treatment) | `recraftv4` + `recraftv3-replace-bg` | Cheaper, fast, acceptable for grid views |
| Upscale final before listing | `topaz-upscale-image` | Sharpens to print / 4K web |

## Procedure

- **One surface per job.** Never prompt "tee AND mug AND poster" in one call.
- **Use the phrase "the same [artwork / logo / design]"** when passing `-i` — models respond to explicit identity-lock language.
- **Describe the scene, not the photo.** "Morning light through a linen curtain, shallow DoF, film-grain texture" beats "a nice picture of a mug".
- **Pick one scene mood and stick with it** across the set — mixing "cozy home" and "urban night" in the same store listing looks chaotic.
- **Match the aspect ratio to the destination**: Shopify tile 4:5, Etsy hero 16:9, IG carousel 1:1, Amazon A+ 970×600 custom. Don't crop afterward.
- **Check hands, text, and edges.** These are the three places photoreal models still fail. Regenerate if hands are fused or brand text is garbled.
- **Upscale before listing.** A 1024×1024 mockup looks mushy on a 2× retina product page. Run `gen-ai enhance` or `topaz-upscale-image` on approved finals.
- **Don't skip the `-i` reference** on merch mockups — Gemini will invent a different design otherwise.

## Pitfalls

- **Artwork drifts across surfaces** — missing `-i` on the i2i call, or using a t2i model (flux-2-pro) when you needed Gemini/Kontext.
- **Fused or six-fingered hands on model-worn merch** — regenerate; Gemini 3 handles hands better than older models.
- **Brand text turned to gibberish** — don't ask the model to render small logo text. Leave text area clean, overlay in post.
- **Over-styled "AI-looking" scenes** — bokeh overload, plastic skin, magazine-cover HDR. Prompt "natural light, documentary style, film grain" to dial it back.
- **Wrong aspect ratio** — shipping 1:1 to a platform that expects 4:5. Verify target spec before batching.
- **Mixing identity models mid-batch** — if 3 are Gemini and 3 are flux-2-pro, the set looks split. Pick one primary model per set.

## Verification

Run `gen-ai whoami` to confirm authentication, then re-run the failed command with `--debug`.

## Cost & time

| Asset | Model | Credits | Time |
|---|---|---|---|
| 1× flat artwork on merch | `gemini-3-pro-image` | ~3 | ~20s |
| 1× lifestyle product scene | `flux-2-pro` | ~8 | ~45s |
| 1× packaging in context | `seedream-4.5` | ~5 | ~30s |
| 1× UI on device | `gpt-image-1.5` | ~4 | ~30s |
| Upscale to 4K | `topaz-upscale-image` | ~2 | ~15s |
| **Typical 6-surface POD set** | mixed | **~20** | **~3 min** |
| **Typical 6-scene lifestyle set** | flux-2-pro | **~50** | **~5 min** |

## See also

- [gen-ai-use.md](../../gen-ai-use/SKILL.md) — CLI command reference, flags, model IDs
- [gen-ai-workflows.md](../../gen-ai-workflows/SKILL.md) — Workflow 3 (catalog reshoot) for 50+ SKU batches
- [gen-ai-batch.md](../../gen-ai-batch/SKILL.md) — manifest schema, concurrency, `gen-ai batch resume <output-dir>`
- [install-gen-ai-cli-and-mcp.md](../../install-gen-ai-cli-and-mcp/SKILL.md) — set up the CLI + MCP server
- `prosumer-launch-kit` — if the mockups are feeding a broader launch
- `prosumer-content-visual-pair` — for single mockup-per-post content queues
