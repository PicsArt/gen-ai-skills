
# Ecommerce variant fan-out

One hero product photo → every color, material, or finish variant, rendered in matching lighting and composition. For Shopify / Amazon / marketplace feeds that demand a shot per variant without the cost of reshooting.

## When to Use

- New collection with 4-12 colorways per SKU and no budget for a per-color photoshoot
- Adding a late colorway to an already-shot range — need it to match the existing set exactly
- Material swaps: leather → vegan leather, matte → gloss, wood → metal
- Marketplace feed requires a PDP image per `option_value` (Shopify variant image URL)
- A/B testing colorway imagery without a physical sample

Not for: background/style changes (use `/ecommerce-catalog-styling`), lifestyle scenes (use `/ecommerce-lifestyle-compose`), seasonal props (use `/ecommerce-seasonal-refresh`).

## Prerequisites

1. **Hero photo** — which shot is the reference? Must be clean, high-res, with final lighting + final background. Every variant inherits from this.
2. **Variant list** — exact colors, materials, finishes. Use the same names you ship on the PDP (`Midnight Navy`, not "dark blue") so filenames match the feed.
3. **Product type** — apparel, hard-goods, furniture, cosmetics? Textiles tolerate more drift; hard-goods with logos need pixel accuracy.
4. **Texture preservation** — does the recolor need to keep fabric weave, leather grain, wood texture? Default yes, but sometimes a full material swap is the goal.
5. **Output aspect** — Shopify PDP (4:5), Amazon (1:1), paid social (1:1, 9:16)? Usually need at least two.
6. **Swatch consistency** — do the generated variants have to match a physical swatch / Pantone? If yes, plan a sample pass + human color-pick before batching.

## How to Run

1. **QA the hero.** Crop tight, high-res (≥ 2048px on long edge), neutral shadow, no color cast. A bad hero multiplies across every variant.
2. **Pilot one variant per material class.** If you have matte + gloss + textured colorways, run one of each first:
   ```bash
   gen-ai generate -m qwen-image-edit-plus -i hero.png \
     -p "same product, midnight navy, preserve fabric weave and shadow" \
     --ar 4:5 --download ./pilot
   ```
3. **Human review.** Color true to swatch? Shadow identical to hero? Texture preserved? If no, tune prompt (add Pantone, add "same lighting as reference") and re-pilot.
4. **Manifest the full set.** One job per variant, consistent prompt template:
   ```bash
   gen-ai batch run variants.json --dry-run
   ```
5. **Estimate gate, then batch.**
   ```bash
   gen-ai batch run variants.json --concurrency 6 -o ./variants
   jq '.jobs[] | {id, status, url, localPath, error}' ./variants/results.json > results.jsonl
   ```
6. **Swatch QA.** Lay all variants side-by-side in a grid. Any color that looks "off the ramp" from the others gets regenerated with a tighter prompt.
7. **Fan out aspects.** Re-run the manifest with `--ar 1:1` and `--ar 9:16` for marketplace / paid surfaces, reusing the same recolored outputs as input for reframes.
8. **Export feed-ready.** Name as `{SKU}_{variant}_{aspect}.webp`. Generate the Shopify variant CSV with these URLs.

## Quick Reference

```json
{
  "defaults": {
    "model": "qwen-image-edit-plus",
    "imageUrls": ["./hero/SKU-042_hero.png"],
    "aspectRatio": "4:5"
  },
  "jobs": [
    { "id": "SKU-042_black",       "prompt": "same product recolored in jet black #0A0A0A, preserve fabric weave, keep lighting and shadow identical to reference" },
    { "id": "SKU-042_navy",        "prompt": "same product recolored in midnight navy #1B2A44, preserve fabric weave, same lighting" },
    { "id": "SKU-042_olive",       "prompt": "same product recolored in olive green #556B2F, preserve fabric weave, same lighting" },
    { "id": "SKU-042_cream",       "prompt": "same product recolored in cream #F3E9D2, preserve fabric weave, same lighting" },
    { "id": "SKU-042_vegan_black", "prompt": "same product in vegan leather, jet black, subtle grain, same lighting as reference" }
  ]
}
```

Use hex codes whenever possible — natural language colors drift more than named Pantones / hex.

## Quick Reference

| Sub-task | Model | Why |
|---|---|---|
| In-place recolor, preserve composition + shadow | `qwen-image-edit-plus` | Strongest at localized recolor without touching layout |
| Recolor + subtle relight | `flux-kontext-pro` | Better lighting realism, slight risk of composition drift |
| Material swap (leather → canvas) | `flux-kontext-pro` | Can re-render surface texture; `qwen-image-edit-plus` won't |
| Preserve logo/label exactly | `recraftv3-replace-bg` (reverse) + mask | Use for regulated products; lock the label region |
| Cheap draft to pick final palette | `gemini-3.1-flash-image` | Use first to validate color list before spending |

Confirm current capabilities with `gen-ai models info qwen-image-edit-plus` before batching.

## Procedure

- **Hex or Pantone in the prompt, always.** "Red" is not a color. `#B91C1C crimson red` is.
- **One reference hero for the whole set.** Never mix hero references — variants will look like they were shot on different days.
- **Preserve lighting explicitly.** The phrase "keep lighting and shadow identical to reference" meaningfully reduces drift on `qwen-image-edit-plus`.
- **Generate swatch strip first.** One 1:1 tile per color in a cheap model for approval. Then run flagship at PDP size.
- **Naming convention: `{SKU}_{variant}_{aspect}.webp`.** Matches Shopify `image_position` + `option_value`. Don't invent a new one.
- **Resolution ≥ 2048px.** PDP zoom and retina displays punish low-res recolors — artifacts show instantly.
- **Re-use outputs for aspect fan-out.** Don't recolor twice for 4:5 and 1:1 — recolor once at the tallest aspect, then reframe.
- **Gate with brand.md** so off-palette variants (not on the approved ramp) get rejected before spend.

## Pitfalls

- **Color drifts from the approved ramp.** Always hex-code. Compare strip-view side-by-side before sign-off. Reshoot the outlier.
- **Shadow direction flips on one variant.** Model occasionally re-lights. Add "same lighting and shadow as reference" and regenerate just that variant.
- **Texture lost on dark colors.** Fabric weave disappears to flat black. Add "preserve visible weave, subtle texture" to the prompt; or switch to `flux-kontext-pro`.
- **Logo color shifts with the body.** The model recolors everything including the logo. Mask the logo region or note "logo remains white" in the prompt.
- **Wrong marketplace aspect.** Amazon variant images must be 1:1; Shopify PDP is typically 4:5. Generate both.
- **Overwriting the hero.** Never write outputs over `hero.png` — that's your master for future variants, seasons, and re-shoots.

## Verification

Run `gen-ai whoami` to confirm authentication, then re-run the failed command with `--debug`.

## Cost & time

| Scale | Per variant (qwen-image-edit-plus) | Per variant (flux-kontext-pro) | Total time @ concurrency 6 |
|---|---|---|---|
| 4 colors × 1 SKU | ~8 credits | ~16 credits | 30-60s |
| 6 colors × 20 SKUs (120) | ~240 credits | ~480 credits | 15-20 min |
| 8 colors × 100 SKUs (800) | ~1600 credits | ~3200 credits | 1.5-2 hours |
| 12 colors × 500 SKUs (6000) | ~12k credits | ~24k credits | overnight |

Multiply by 2-3 for per-aspect fan-outs. Always `gen-ai pricing <model>` before committing.

## See also

- `/ecommerce-catalog-styling` — one treatment across the whole catalog
- `/ecommerce-lifestyle-compose` — place product in a scene
- `/ecommerce-seasonal-refresh` — seasonal overlays on variants
- `gen-ai-batch.md` — manifest + resume + concurrency tuning
- `gen-ai-workflows.md` — Workflow 10 (Ad-variant factory) for volume patterns
