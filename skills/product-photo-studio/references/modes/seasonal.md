
# Ecommerce seasonal refresh

Re-dress an entire catalog for a seasonal push (Christmas, Valentine's, Black Friday, summer, back-to-school) without reshooting. Seasonal props, lighting, and palette are added as i2i overlays on the existing catalog — quick turnaround, brand-safe, with expiry dates baked into the file names.

## When to Use

- Seasonal landing-page drop in 1-2 weeks, no time for a shoot
- Always-on catalog needs a timed "skin" for campaign period only
- Marketplace (Amazon, Shopify, Instagram Shop) seasonal storefronts
- PDP hero swap tied to a campaign start/end date
- Paid-social creative refresh for a new season, same SKUs

Not for: net-new styling across the whole year (use `/ecommerce-catalog-styling`), variant colors (use `/ecommerce-variant-fan-out`), or full lifestyle scenes (use `/ecommerce-lifestyle-compose`). Those are the base — seasonal layers on top.

## Prerequisites

1. **Season / campaign** — Christmas 2026, Valentine's, summer, back-to-school, Black Friday? Drives props + palette + duration.
2. **Campaign start + end dates** — bake into filenames (`{SKU}_xmas26_20261201-20261231.webp`) so the team can hard-expire assets at end-of-campaign.
3. **Source catalog** — are we layering on packshots, styled catalog outputs, or lifestyle scenes? Each has different prompt patterns.
4. **SKU scope** — whole catalog, hero SKUs only, or a curated seasonal capsule? Don't seasonal-dress SKUs that won't be promoted.
5. **Brand-safe palette + props** — brand.md with approved seasonal cues. Christmas reds should be your brand red, not stock Coca-Cola red.
6. **Surfaces** — PDP hero, paid social, email header, LP hero? Each needs a different crop + aspect.

## How to Run

1. **Pull the base set.** Copy the latest styled catalog outputs into a working folder. Don't re-style raw packshots as part of the seasonal pass — two transforms compound drift.
2. **Lock seasonal brief.** One-line prompt suffix that captures the season:
   - Xmas: `+ warm festive props (pine sprig, red velvet ribbon), warm tungsten light, subtle snow glow`
   - Valentine's: `+ soft rose petals scattered, warm rosy light, hints of blush pink`
   - Summer: `+ sunlit linen backdrop, soft palm shadow, warm golden hour`
   - Back-to-school: `+ desk accessories (notebook corner, pencil), cool daylight, crisp shadow`
3. **Pilot 5 SKUs.** Cover a mix of categories to check prop scale and palette coherence:
   ```bash
   gen-ai generate -m qwen-image-edit-plus -i ./base/SKU-042_4x5.webp \
     -p "same product, same composition, same lighting — add warm festive props (pine sprig, red velvet ribbon), warm tungsten light, subtle snow glow" \
     --ar 4:5 --download ./pilot
   ```
4. **Human review.** Prop scale sane? Product untouched? Palette on-brand? If a category (e.g. tech) reads wrong with pine sprigs, drop it from the manifest — not every SKU needs every season.
5. **Manifest.** One job per SKU with campaign-tagged filenames:
   ```bash
   gen-ai batch run holiday.json --dry-run
   ```
6. **Batch.**
   ```bash
   gen-ai batch run holiday.json --concurrency 5 -o ./xmas26
   jq '.jobs[] | {id, status, url, localPath, error}' ./xmas26/results.json > results.jsonl
   ```
7. **Sample QA.** 5-10% spot check for prop drift, palette bleeds, product occlusion.
8. **Hand off with expiry metadata.** Export `results.jsonl` with campaign dates so the PDP team can auto-expire assets at campaign end.

## Quick Reference

```json
{
  "defaults": {
    "model": "qwen-image-edit-plus",
    "aspectRatio": "4:5",
    "prompt": "same product, same composition, same lighting — add warm festive props (pine sprig, red velvet ribbon), warm tungsten light, subtle snow glow"
  },
  "jobs": [
    { "id": "SKU-042_xmas26", "imageUrls": ["./base/SKU-042_4x5.webp"] },
    { "id": "SKU-101_xmas26", "imageUrls": ["./base/SKU-101_4x5.webp"] },
    { "id": "SKU-203_xmas26", "imageUrls": ["./base/SKU-203_4x5.webp"],
      "prompt": "same product, same composition, same lighting — add a single pine sprig only (no ribbon, no snow — this is a tech SKU)" }
  ]
}
```

Per-category prompt overrides prevent "pine sprig on a keyboard" failures.

## Quick Reference

| Sub-task | Model | Why |
|---|---|---|
| Add seasonal props + relight, preserve product | `qwen-image-edit-plus` | Best at additive edits that leave the base product untouched |
| Stronger seasonal atmosphere / relight | `flux-kontext-pro` | Better at mood/lighting shifts (snow glow, golden hour) |
| Full reshoot-style seasonal scene | `runway-gen4-ref` | When seasonal = new lifestyle scene, not just overlay props |
| Cheap palette/prop sanity check | `gemini-3.1-flash-image` with `-i` | Validate the seasonal brief on 3 SKUs before spending |
| Post-pass upscale for PDP zoom | `topaz-upscale-image` | Retina/zoom PDPs on seasonal heroes |

Confirm model capabilities with `gen-ai models info qwen-image-edit-plus` before batching.

## Procedure

- **Seasonal is additive, not destructive.** Prompt always includes "same product, same composition, same lighting" before the seasonal cues. The model should add, not replace.
- **Brand-safe palette, always.** Generic Christmas red reads as Coca-Cola red. Pin the exact brand hex in the prompt.
- **Bake expiry into filenames.** `{SKU}_{campaign}_{start}-{end}_{aspect}.webp`. Makes end-of-campaign takedown automatic.
- **Batch by category, not all-at-once.** Tech SKUs, fashion SKUs, and kitchen SKUs need different seasonal prop weight. Run 3 manifests, not one.
- **Turnaround target: ≤ 48h.** Seasonal is time-boxed. Pick a simple brief, don't over-iterate.
- **Keep base catalog clean.** Seasonal outputs go to a `./xmas26/` folder, never overwrite `./base/`. Next season starts from the same clean base.
- **Tag aggressively.** `campaign:xmas26`, `expires:2026-12-31` — lets the team query and expire without guessing which assets were seasonal.
- **Include brand.md constraints in prompts.** Seasonal creativity goes off-brand fast; manual QA catches it.

## Pitfalls

- **Props overwhelm the product.** Ribbon bigger than the mug. Fix: prompt "subtle, understated props — do not obscure the product".
- **Palette drift.** Brand red becomes stock Christmas red. Fix: pin brand hex in prompt, gate with brand.md.
- **Seasonal cues on wrong categories.** Pine sprigs on a keyboard. Fix: per-category prompt overrides, or exclude those SKUs from the manifest.
- **Overwriting base catalog.** Never write to `./base/`. Always `./xmas26/`, `./valentines26/`, etc.
- **No expiry metadata.** Seasonal assets stay up in May. Fix: campaign dates in filename + tag + an auto-takedown job on campaign end-date.
- **Too many iterations.** Seasonal is time-boxed. Ship 85%-right in 48h, not 99%-right in 2 weeks. The campaign is over before perfect ships.

## Verification

Run `gen-ai whoami` to confirm authentication, then re-run the failed command with `--debug`.

## Cost & time

| Scale | Per SKU (qwen-image-edit-plus) | Per SKU (flux-kontext-pro) | Total time @ concurrency 5 |
|---|---|---|---|
| 20 hero SKUs | ~40 credits | ~80 credits | 5 min |
| 100 SKUs | ~200 credits | ~400 credits | 15-20 min |
| 500 SKUs | ~1000 credits | ~2000 credits | 1-1.5 hours |
| 2000 SKUs | ~4000 credits | ~8000 credits | 4-6 hours |

Multiply by 2-3 for multi-surface (PDP 4:5 + social 1:1 + paid 9:16). Seasonal heroes usually ship only 1-2 aspects because the campaign is short. `gen-ai pricing <model>` first; pause at $20.

## See also

- `/ecommerce-catalog-styling` — the base layer seasonal overlays on top of
- `/ecommerce-lifestyle-compose` — full seasonal scene (not overlay)
- `/ecommerce-variant-fan-out` — combine seasonal with color variant drops
- `gen-ai-batch.md` — manifest + concurrency + resume
- `gen-ai-workflows.md` — Workflow 8 (Seasonal refresh) for the full end-to-end pattern
