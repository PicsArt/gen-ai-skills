
# Ecommerce catalog styling

Apply a single, consistent styling treatment (background, lighting, surface, mood) across an entire product catalog — without reshooting, and without the product drifting SKU-to-SKU.

## When to Use

- New collection drop: 50-2000 flat packshots need PDP-ready staging before launch
- Seasonal / brand refresh: existing catalog looks dated, needs a single new treatment
- Marketplace sync: Amazon / Shopify / Instagram Shop each need an on-brand variant
- Pre-launch PDP tune-up: a subset of hero SKUs need premium lifestyle backgrounds
- Migrating from a legacy studio to a new brand visual system

Not for: adding color/material variants (use `/ecommerce-variant-fan-out`), full lifestyle scenes with props (use `/ecommerce-lifestyle-compose`), or seasonal overlays (use `/ecommerce-seasonal-refresh`).

## Prerequisites

Ask before spending credits:

1. **Feed source** — Shopify CSV, Salesforce export, custom JSON, or a folder of PNGs? Need a SKU → filename map.
2. **SKU count + deadline** — 50 or 5000? Today or next sprint? Drives concurrency + estimate gates.
3. **Target surfaces** — own PDP (4:5), Amazon main (1:1, pure white tolerance), Instagram Shop (1:1), paid social (9:16, 16:9)? Each has different crop rules.
4. **Style brief** — one-line treatment: "airy studio, warm natural light, linen backdrop" or "dark moody, low-key, polished concrete". Lock this before batching.
5. **Brand constraints** — brand.md in the repo? Banned elements (competitor cues, lifestyle humans, specific colors)? Required palette?
6. **Product accuracy bar** — pixel-accurate (regulated, e.g. cosmetics label) or "close enough" (apparel, homewares)? Drives model choice.

If the user hands over a detailed brief plus feed, skip to Workflow step 2.

## How to Run

1. **Prep the feed.** Normalize to a simple CSV or JSON keyed by SKU with a local image path and any per-SKU metadata (title, category). Drop rows with missing files.
2. **Pick 5 pilot SKUs across categories.** Run them single-call to lock the prompt:
   ```bash
   gen-ai generate -m recraftv3-replace-bg -i pilots/SKU-001.png \
     -p "airy studio, warm natural light, linen backdrop, soft shadow" \
     --ar 4:5 --download ./pilot-out
   ```
3. **Review pilots + tune prompt.** If a category drifts (e.g. metallic products go flat), note it — you may need a per-category prompt.
4. **Generate the manifest.** One job per SKU, inherit the locked prompt from `defaults`:
   ```bash
   gen-ai batch run catalog.json --dry-run
   ```
5. **Estimate gate.** Under $5 just run. $5–$20 show the number. Over $20 break into category batches and confirm.
6. **Batch with safety flags.**
   ```bash
   gen-ai batch run catalog.json --concurrency 6 -o ./styled
   jq '.jobs[] | {id, status, url, localPath, error}' ./styled/results.json > results.jsonl
   ```
7. **QA sample.** Pull 20 random outputs. Check background consistency, shadow angle, product accuracy. Reject + regenerate the whole batch if drift > 10%.
8. **Crop for surfaces.** Use the same source to emit 1:1 Amazon / 4:5 PDP / 9:16 social variants (see Best practices for batching per-aspect).

## Quick Reference

```json
{
  "defaults": {
    "model": "recraftv3-replace-bg",
    "aspectRatio": "4:5",
    "prompt": "airy studio, warm natural light, linen backdrop, soft directional shadow, product centered"
  },
  "jobs": [
    { "id": "SKU-001", "imageUrls": ["./raw/SKU-001.png"] },
    { "id": "SKU-002", "imageUrls": ["./raw/SKU-002.png"] },
    { "id": "SKU-003", "imageUrls": ["./raw/SKU-003.png"],
      "prompt": "airy studio, cool daylight, marble surface, crisp shadow" }
  ]
}
```

Per-SKU `prompt` overrides `defaults.prompt` — use sparingly for categories that need a different surface.

## Quick Reference

| Sub-task | Model | Why |
|---|---|---|
| Replace BG, preserve product pixel-accurate | `recraftv3-replace-bg` | Best product fidelity — label text, logos, fine detail survive |
| Photoreal studio edit with lighting control | `flux-kontext-pro` | Stronger lighting/shadow realism than replace-bg; slight product drift risk |
| Hero-grade photoreal refresh | `flux-2-pro` with `-i` | Top photoreal quality; use for a small hero subset, not the tail |
| Stylized / editorial treatment | `seedream` | For art-directed or illustrated catalogs |
| Quick draft pass before flagship | `gemini-3.1-flash-image` | Cheap; use to lock prompt before spending on flagship |

Run `gen-ai models info <id>` to confirm current aspect-ratio support and pricing before committing to a batch.

## Procedure

- **Preserve the product via i2i, never t2i.** Always pass `-i <product>.png`. Text-to-image will hallucinate the SKU.
- **Lock the prompt on 5 pilots before batching.** Cheaper to re-prompt once than to re-batch 2000 SKUs.
- **Batch by category for style consistency.** Mugs, glassware, and textiles each need slightly different shadow/surface logic.
- **SKU → filename convention.** `SKU-001_4x5.webp`, `SKU-001_1x1.webp`, `SKU-001_9x16.webp`. Never overwrite source files.
- **Keep the source untouched.** Write to `./styled/`, not over `./raw/`. `gen-ai batch resume <output-dir>` needs deterministic out-paths.
- **One aspect per pass.** Don't ask one call for 3 aspects — run 3 batches sharing the same prompt with `--ar 4:5`, `--ar 1:1`, `--ar 9:16`.
- **Gate with `brand.md`** on every job so banned props/colors are caught before spend.
- **Sample-QA 5%** before delivering. A drifted shadow direction across 1000 SKUs is a PDP-wide disaster.

## Pitfalls

- **Background color drift SKU-to-SKU.** Lock the exact color in the prompt (`#F5F1EA linen`), don't rely on "warm". Re-run drifters with the same seed if the model supports it.
- **Shadow direction flips between SKUs.** Add "soft directional shadow from upper-left" to the prompt. Reject any output where shadow disagrees with the batch.
- **Label/logo hallucination.** Happens on `flux-kontext-pro` with small typography. Drop to `recraftv3-replace-bg` for regulated products (cosmetics, food, meds).
- **Wrong aspect for marketplace.** Amazon main image must be 1:1 with pure white. Don't ship a 4:5 with a linen backdrop to Amazon main — it'll be rejected.
- **Overwriting source files.** Always write to a new folder. Source PNGs are the single source of truth for future re-styles.
- **Skipping the 5-SKU pilot.** A 2000-SKU batch with a wrong prompt burns a day of lead time and ~$40.

## Verification

Run `gen-ai whoami` to confirm authentication, then re-run the failed command with `--debug`.

## Cost & time

| Scale | Per-SKU (replace-bg) | Per-SKU (flux-kontext-pro) | Rough total time @ concurrency 6 |
|---|---|---|---|
| 10 SKUs | ~2 credits | ~4 credits | 1–2 min |
| 100 SKUs | ~200 credits | ~400 credits | 10–15 min |
| 1000 SKUs | ~2000 credits | ~4000 credits | 2–3 hours |
| 5000 SKUs | ~10k credits | ~20k credits | 10–12 hours (overnight) |

For 3 surface aspects (4:5, 1:1, 9:16), triple the estimate. Always `gen-ai batch run <manifest.json> --dry-run` first — pause at $20.

## See also

- `/ecommerce-variant-fan-out` — color/material variants per SKU
- `/ecommerce-lifestyle-compose` — product in a full lifestyle scene
- `/ecommerce-seasonal-refresh` — seasonal overlay on an existing catalog
- `gen-ai-batch.md` — manifest schema, concurrency, resume semantics
- `gen-ai-workflows.md` — catalog reshoot (Workflow 3) and multi-step chains
