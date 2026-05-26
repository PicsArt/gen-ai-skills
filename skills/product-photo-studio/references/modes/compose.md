
# Ecommerce lifestyle compose

Take a plain packshot and place the product into a believable lifestyle scene (kitchen counter, desk, gym floor, outdoor table) with realistic shadows, scale, and context — without reshooting on location.

## When to Use

- PDP needs 2-4 lifestyle shots per SKU, in addition to the clean packshot
- Paid social / display ads: product needs to be "in situ" to drive CTR
- Content refresh: existing packshots feel sterile against competitor lifestyle PDPs
- Amazon A+ content / brand-store tiles that demand contextual imagery
- Small product (accessories, cosmetics) where in-hand or on-surface shots convert better than isolated shots

Not for: background swaps without props (use `/ecommerce-catalog-styling`), color variants (use `/ecommerce-variant-fan-out`), or seasonal treatments (use `/ecommerce-seasonal-refresh`).

## Prerequisites

1. **Product reference** — clean, high-res packshot (transparent or pure-white BG, ≥ 2048px). Shadows help but aren't required.
2. **Scene list** — how many scenes per SKU, and which ones? Be concrete: "marble kitchen counter, morning light" — not "nice kitchen". 2-4 scenes is the sweet spot for PDP.
3. **Scale + placement** — is the product on a surface, in a hand, on a wall, on the floor? Misread scale is the #1 rejection reason.
4. **Human presence** — pure product-in-scene, a hand, a full person? Hands are safer than faces (fewer uncanny issues) and convert well.
5. **Target resolution** — PDP zoom needs ≥ 2048px on the long edge. Amazon A+ needs 1200px. Social needs 1080px. Always render at the highest required and downscale.
6. **Brand guardrails** — banned scenes (e.g. competitor cafes, specific locations), required palette, permitted lifestyles (family, urban, outdoor).

## How to Run

1. **Lock 1 pilot scene on 1 SKU.** Iterate on prompt until scale, shadow, and product fidelity are all right.
   ```bash
   gen-ai generate -m runway-gen4-ref -i ./hero/SKU-042.png \
     -p "on a white marble kitchen counter, morning light from the left, soft cast shadow, blurred background of a bright airy kitchen" \
     --ar 4:5 --download ./pilot
   ```
2. **Human review.** Is the product the same product? Scale correct (e.g. mug height matches a real mug)? Shadow matches scene light direction? If no, refine and re-pilot.
3. **Template the scenes.** Write 3-4 reusable scene prompts:
   - `kitchen-marble`: "on a white marble kitchen counter, morning light from the left, soft cast shadow, blurred bright kitchen in background"
   - `desk-wood`: "on a warm walnut desk, afternoon daylight, notebook and pen softly out of focus, cast shadow to the right"
   - `outdoor-cafe`: "on a small bistro table outdoors, dappled tree light, soft bokeh background of a cafe terrace"
4. **Expand to manifest** — scene × SKU grid:
   ```bash
   gen-ai batch run lifestyle.json --dry-run
   ```
5. **Estimate + batch.**
   ```bash
   gen-ai batch run lifestyle.json --concurrency 4 -o ./lifestyle
   jq '.jobs[] | {id, status, url, localPath, error}' ./lifestyle/results.json > results.jsonl
   ```
6. **Sample QA aggressively.** Pull 10% of outputs. Reject any with wrong scale, product drift, extra fingers, warped geometry. Regenerate only the rejects with `gen-ai batch resume <output-dir>`.
7. **Upscale if needed for PDP zoom.**
   ```bash
   gen-ai enhance -i ./lifestyle/SKU-042_kitchen.webp -m topaz-upscale-image -s
   ```
8. **Name for PDP slots.** `SKU-042_kitchen_4x5.webp`, `SKU-042_desk_4x5.webp` — map to PDP `image_position` 2, 3, 4.

## Quick Reference

```json
{
  "defaults": {
    "model": "runway-gen4-ref",
    "aspectRatio": "4:5"
  },
  "jobs": [
    { "id": "SKU-042_kitchen", "imageUrls": ["./hero/SKU-042.png"],
      "prompt": "on a white marble kitchen counter, morning light from the left, soft cast shadow, blurred bright airy kitchen" },
    { "id": "SKU-042_desk",    "imageUrls": ["./hero/SKU-042.png"],
      "prompt": "on a warm walnut desk, afternoon daylight, notebook and pen softly out of focus, cast shadow to the right" },
    { "id": "SKU-042_cafe",    "imageUrls": ["./hero/SKU-042.png"],
      "prompt": "on a small bistro table outdoors, dappled tree light, blurred cafe terrace background, gentle cast shadow" }
  ]
}
```

For N SKUs × M scenes, generate programmatically — don't hand-write 400 items.

## Quick Reference

| Sub-task | Model | Why |
|---|---|---|
| Composite product into scene, preserve reference | `runway-gen4-ref` | Best at reference-preserving composites with believable cast shadows |
| Higher photoreal / editorial quality | `flux-2-pro` with `-i` | Top photoreal; slight product drift risk — pilot first |
| Scene edits on existing lifestyle shot | `flux-kontext-pro` | For tweaking an already-composited scene (change prop, change light) |
| In-hand / held product | `runway-gen4-ref` | Handles skin + product contact better than most |
| Cheap draft pass before flagship | `gemini-3.1-flash-image` with `-i` | Use to validate scene brief before spending |
| Post-pass upscale for PDP zoom | `topaz-upscale-image` | 4× for retina/zoom PDPs |

Confirm model capabilities with `gen-ai models info runway-gen4-ref` before batching.

## Procedure

- **Preserve the product via i2i.** Never t2i — the model will invent a similar-but-not-the-same product.
- **Scene prompts should name: surface, light direction, props, depth/bokeh, shadow direction.** Vague prompts produce generic scenes that don't convert.
- **Scale anchor objects in the scene.** "Notebook and pen", "coffee cup", "phone" — gives the model a size reference so your product isn't rendered wrong.
- **Shadow is the tell.** If the scene light is from the left, the shadow must cast right. Mismatched shadow = instant rejection.
- **Keep the hero angle consistent across scenes.** If the product is 3/4 in the packshot, all lifestyle scenes should show the same 3/4. Don't mix angles across PDP slots.
- **Generate at the highest required resolution.** Downscaling is free. Upscaling loses detail.
- **Sample-QA 10%.** Lifestyle shots have more failure modes than styled packshots (scale, shadow, uncanny hands) — budget QA time.
- **Reuse scene prompts as a library.** Kitchen, desk, gym, outdoor-table, bedroom, shelf — 6-8 templates cover most catalogs.
- **Gate with brand.md.** Banned lifestyles, required palette, excluded competitor cues all belong in rules.

## Pitfalls

- **Wrong scale.** Mug rendered as small as a shot glass. Fix: add scale-anchor props and explicit size cues in the prompt ("standard 12oz mug").
- **Product drift.** Logo or shape morphs slightly. Fix: drop to `runway-gen4-ref` (best fidelity); for regulated products, consider masking the label region.
- **Shadow direction wrong.** Scene has morning light left-to-right, but shadow goes right-to-left. Regenerate with explicit shadow-direction prompt.
- **Uncanny hands.** Skip hands entirely if the model keeps producing six fingers — go surface-only scenes.
- **Too-low resolution for PDP zoom.** Render large or upscale with `topaz-upscale-image`. Never ship sub-1200px lifestyle to a PDP.
- **Scene stock-photo fatigue.** Every shot looks like Pinterest. Mix in a desaturated / underexposed / grainier scene or two to look human-shot.

## Verification

Run `gen-ai whoami` to confirm authentication, then re-run the failed command with `--debug`.

## Cost & time

| Scale | Per shot (runway-gen4-ref) | Per shot (flux-2-pro) | Total time @ concurrency 4 |
|---|---|---|---|
| 1 SKU × 3 scenes | ~9 credits | ~15 credits | 1-2 min |
| 20 SKUs × 3 scenes (60) | ~180 credits | ~300 credits | 15-20 min |
| 100 SKUs × 4 scenes (400) | ~1200 credits | ~2000 credits | 1.5-2 hours |
| 500 SKUs × 4 scenes (2000) | ~6k credits | ~10k credits | overnight |

Add `topaz-upscale-image` at ~1-2 credits per output if PDP zoom is needed. Always `gen-ai pricing <model>` first.

## See also

- `/ecommerce-catalog-styling` — consistent background without props
- `/ecommerce-variant-fan-out` — color variants on each lifestyle scene
- `/ecommerce-seasonal-refresh` — swap props for seasonal campaigns
- `gen-ai-batch.md` — manifest schema and resume/retry flags
- `gen-ai-workflows.md` — Workflow 3 (Catalog reshoot) for scale patterns
