
# Enterprise Catalog Reshoot

Re-render an entire product catalog (hundreds to thousands of SKUs) with a new season, brand treatment, or lifestyle concept — without booking a photo shoot. Built for ecommerce + retail teams who need consistent, auditable, brand-gated output at scale.


## When to Use

- Catalog has 500+ SKUs and a physical reshoot is not viable on cost or timeline
- Seasonal refresh: swap backgrounds / props / lighting across every product in one pass
- Brand migration: apply a new visual system across legacy product photography
- M&A: unify two catalogs under a single look
- Compliance: re-render with approved backgrounds only (no unlicensed props, no competitor branding)

Do **not** use for: a handful of hero images (use `gen-ai generate` directly), or catalogs where physical product accuracy cannot be validated post-gen (jewelry close-ups, color-critical textiles).


## Prerequisites

Before touching the CLI, confirm:

1. **Source catalog** — CSV or JSON? Columns `sku_id`, `source_image`, `title`, `category` at minimum. Where does it live (S3, local, Drive)?
2. **Brand system** — path to `brand.md` (palette, props allow/deny lists, lighting spec, aspect ratios). Which version/commit?
3. **Target scenes per SKU** — 1 variant? 4? (Kitchen, outdoor, studio, lifestyle.) Hard cap per SKU.
4. **Approval chain** — who signs off the treatment sample before the full batch runs? Who receives the audit log?
5. **SLA** — delivery date. Drives concurrency + whether we split across multiple runs.
6. **Data residency + audit** — must outputs stay in a specific Drive folder? Does legal need the full manifest + results.json archived?


## How to Run

Seven steps. Never skip the treatment sample or the estimate.

1. **Ingest catalog** — normalize to `catalog.json` with one entry per SKU: `{ id, input, prompt_vars }`. Keep `sku_id` as the primary key through the whole pipeline so filenames round-trip back to the PIM.
2. **Treatment sample (5–10 SKUs)** — run a small batch first, get written approval from brand + merchandising before scaling. No exceptions.
3. **Pin the model** — lock the exact model version in `defaults` so runs are reproducible six months from now (see `enterprise-pinned-registry`).
4. **Estimate** — `gen-ai batch run catalog.json --dry-run` then price it. Pause at the approved threshold ($20 / $100 / whatever the approver set).
5. **Execute** — run with brand context in prompts and a resume-ready output directory. Never run without `gen-ai batch resume <output-dir>`-friendly filenames.
6. **Validate** — diff output count vs. SKU count, check `results.json` for `status !== "completed"`, spot-check 5% for brand drift.
7. **Deliver + archive** — ship filenames back to the PIM keyed by `sku_id`, archive the manifest + results + audit log under the run ID. Never overwrite a prior run — increment.

## Quick Reference

Enterprise manifests must include metadata so legal / brand / IT can reconstruct any prior run.

```json
{
  "defaults": {
    "model": "flux-kontext-pro",
    "aspectRatio": "1:1"
  },
  "metadata": {
    "campaign": "spring-2026",
    "brand_system_version": "brand.md@sha:a4f1c9",
    "approver": "brand-lead@company.com",
    "approved_at": "2026-04-18T14:22:00Z",
    "audit_id": "CAT-RESHOOT-2026-04-SPRING",
    "data_residency": "eu-west-1"
  },
  "jobs": [
    {
      "id": "SKU-00123-kitchen",
      "prompt": "Same product, bright morning kitchen, marble counter, soft daylight, editorial catalog",
      "imageUrls": ["s3://catalog-raw/SKU-00123.jpg"]
    },
    {
      "id": "SKU-00123-outdoor",
      "prompt": "Same product, outdoor patio, golden hour, shallow depth of field",
      "imageUrls": ["s3://catalog-raw/SKU-00123.jpg"]
    }
  ]
}
```

Filename pattern: `{sku_id}-{scene}.{ext}` — survives PIM round-trips and rebrands.


## Quick Reference

| Sub-task | Model | Notes |
|----------|-------|-------|
| Background replace, product unchanged | `picsart-change-bg` | Cheapest; preserves SKU fidelity. Commercial-use approved. |
| Edit-mode (add props, change lighting, keep SKU) | `flux-kontext-pro` | Best product-accuracy preserve. Commercial-safe. |
| Full-scene regenerate with reference | `flux-2-pro` | i2i with `--image-weight` high. Commercial-safe. |
| Hero / flagship SKUs, photoreal | `gemini-3-pro-image` | Highest fidelity. Verify license terms per account. |
| Upscale final deliverable | `topaz-upscale-image` | Print-resolution pass before handoff. |

Always confirm current commercial-use status with `gen-ai models info <id>` — provider terms change.


## Procedure

- **Pin model versions.** Aliases drift. Lock to `model@x.y` in `defaults` and commit the manifest.
- **Treatment sample is non-negotiable.** Five SKUs approved in writing before the 5000-SKU run.
- **Never overwrite.** Output dir carries the run ID (`./runs/2026-04-spring-full`). Reruns increment.
- **Filename = `sku_id`.** The single most important contract with the PIM / DAM. Do not rename after generation.
- **Brand context on every job.** Include the relevant `brand.md` constraints in default or generated prompts. One place to update.
- **`gen-ai batch resume <output-dir>` by default** on any batch >50 items. Network blips are free to recover from.
- **Archive the manifest.** Commit or store the exact `catalog.json` that produced this run. Legal will ask.
- **Spot-check 5%.** Human-in-the-loop review before marking the run "delivered".
- **Lock the concurrency.** Ten is safe for most tiers; higher risks 429s on long runs. Don't chase speed.


## Pitfalls

- **Model drift mid-run** — using an unpinned alias; a new version ships between batch A and batch B and the look shifts. Always pin.
- **Filename collisions** — rerunning without a new output dir overwrites the prior run. Increment.
- **SKU misidentification** — prompt drops the product, model hallucinates a new one. Use edit-mode, not full regenerate, for product-critical catalogs.
- **Brand-color drift** — palette shifts subtly across thousands of calls. Gate with `brand.md` and spot-check the palette.
- **Unapproved props in regulated categories** — alcohol, tobacco, healthcare, children's goods have category-specific prop/claim rules. Encode in `brand.md`.
- **Missing alt text** — catalog outputs need accessibility metadata. Generate alt text alongside the image in the same batch if your DAM requires it.


## Verification

Run `gen-ai whoami` to confirm authentication, then re-run the failed command with `--debug`.

### Commands

```bash
# Step 2 — treatment sample
gen-ai batch run catalog.sample.json --concurrency 3 \
  --output ./runs/2026-04-spring-sample

# Step 4 — estimate the full run
gen-ai batch run catalog.json --dry-run

# Step 5 — full run
gen-ai batch run catalog.json \
  --concurrency 10 \
  --output ./runs/2026-04-spring-full
```

For product-accurate edits where the SKU must remain recognizable, use `flux-kontext-pro` (edit-mode) or an image-to-image model with `--image`. For background replacement only, `picsart-change-bg` is cheaper and faster.


## Cost & time

Assumes `flux-kontext-pro` at typical pricing, 1:1, 1 variant per SKU. Verify live numbers with `gen-ai pricing <model>`.

| Scale | Credits (est.) | Wall time @ concurrency 10 |
|-------|----------------|----------------------------|
| 10 SKUs (sample) | ~40 | ~3 min |
| 100 SKUs | ~400 | ~25 min |
| 1,000 SKUs | ~4,000 | ~3.5 h |
| 5,000 SKUs | ~20,000 | ~18 h (split across runs) |
| 10,000 SKUs × 4 scenes | ~160,000 | Multi-day, split and pipeline |

Background-replace models (`picsart-change-bg`) run roughly 3–5× cheaper per call.


## See also

- [enterprise-pinned-registry](../enterprise-pinned-registry/SKILL.md) — lock model versions for reproducibility
- [enterprise-brand-governor](../enterprise-brand-governor/SKILL.md) — brand.md policy enforcement
- [gen-ai-workflows](../../gen-ai-workflows/SKILL.md) — general multi-step patterns
- [gen-ai-batch](../../gen-ai-batch/SKILL.md) — manifest schemas and concurrency tuning
- [gen-ai-use](../../gen-ai-use/SKILL.md) — CLI reference
