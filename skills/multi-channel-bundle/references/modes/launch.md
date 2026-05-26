
# Launch kit

One-person launch day. The creator has a product idea, a deadline, and needs every asset a launch hits: landing-page hero, app-store screenshots, Twitter/LinkedIn announcement cards, Product Hunt gallery, and an email hero — all visually consistent.

## When to Use

- Solo founder or indie creator shipping a product this week
- Product Hunt launch, App Store submission, or newsletter send
- The user says "launch kit", "launch package", "announcement assets", or "Product Hunt assets"
- They already have a name + description but no visuals
- They want the whole bundle to look like one brand, not ten stock images glued together

**Don't use for:** single-image asks, ongoing content queues (use `prosumer-content-visual-pair`), or enterprise campaigns with brand.md governance (use `gen-ai-workflows` Workflow 5).

## Prerequisites

Before running any generation, ask (combine into one message):

1. **Product** — what is it, one sentence? (e.g. "AI meal-planner for busy parents")
2. **Audience + platform** — Product Hunt, App Store, Twitter, LinkedIn? This determines aspect ratios.
3. **Aesthetic / mood** — editorial, playful, techy, minimal, retro? One or two reference vibes.
4. **Brand palette** — any colors, fonts, or existing logo to match? If none, propose one.
5. **Deadline** — today, this week, no rush? Drives whether you draft-first or ship-final.
6. **Must-have assets** — hero yes, but also PH gallery, OG image, App Store screenshots, email hero?

Skip the interview if the user already pasted a brief with these five fields.

## How to Run

```
1. INTERVIEW        → lock product, audience, mood, palette
2. PLAN & ESTIMATE  → list every asset + spec, run `gen-ai pricing`
3. HERO             → one anchor image, user approves before fan-out
4. FAN OUT          → batch the rest using the hero as reference
5. REEL (optional)  → animate the hero into a 15s clip + soundtrack
6. DELIVER          → organized output folder + approved archive/upload
```

1. **Plan the bundle** — write out every asset with exact dimensions. Typical solo launch:

   | Asset | Ratio / size | Model |
   |---|---|---|
   | LP hero | 16:9 | flux-2-pro |
   | PH gallery tiles (×4) | 1:1 | recraftv4 (ref: hero) |
   | Twitter announcement | 1200×675 | recraftv4 |
   | LinkedIn card | 1200×627 | recraftv4 |
   | OG image | 1200×630 | imagen-4.0 or recraftv4 |
   | Email hero | 3:1 | recraftv4 (ref: hero) |
   | App store screenshots (optional) | 1242×2688 | flux-2-pro or gpt-image-1.5 |

2. **Estimate before spending.** Write the manifest, then dry-run:
   ```bash
   gen-ai batch run launch-kit.json --dry-run
   ```
   Sum the credits. If > $5, show the user and wait for "go".

3. **Generate the hero first, alone.** Everything else references it. Do not batch the hero with the rest.
   ```bash
   gen-ai generate -m flux-2-pro \
     -p "$PRODUCT — magazine editorial hero, $MOOD, brand palette $PALETTE" \
     --ar 16:9 --download ./launch-kit
   ```
   Open it with `--open`. If the user rejects, regenerate with a tighter prompt. Do not fan out until the hero is approved.

4. **Fan out with the hero as reference.** Pass `-i ./launch-kit/hero.webp` to keep every downstream asset visually in the same world:
   ```bash
   gen-ai batch run launch-kit.json -c 4 -o ./launch-kit
   ```

5. **Optional reel.** If the brief includes video:
   ```bash
   gen-ai generate -m kling-v3 -i ./launch-kit/hero.webp \
     -p "slow push-in on the product, soft rim light" \
     --duration 5 --ar 16:9 --download ./launch-kit
   gen-ai extend --video ./launch-kit/reel.mp4 --times 2 --ar 16:9   # ~21s
   ```
   Add soundtrack with a music model if the CLI account has audio access.

## Quick Reference

```json
{
  "defaults": {
    "model": "recraftv4",
    "imageUrls": ["./launch-kit/hero.webp"]
  },
  "jobs": [
    { "id": "ph-tile-1",   "prompt": "Product Hunt gallery tile 1 — feature callout",  "aspectRatio": "1:1" },
    { "id": "ph-tile-2",   "prompt": "Product Hunt gallery tile 2 — UI closeup",        "aspectRatio": "1:1" },
    { "id": "ph-tile-3",   "prompt": "Product Hunt gallery tile 3 — use-case scene",    "aspectRatio": "1:1" },
    { "id": "ph-tile-4",   "prompt": "Product Hunt gallery tile 4 — testimonial frame", "aspectRatio": "1:1" },
    { "id": "twitter",     "prompt": "Twitter announcement card, headline space",       "aspectRatio": "16:9" },
    { "id": "linkedin",    "prompt": "LinkedIn announcement card, professional tone",   "aspectRatio": "16:9" },
    { "id": "og",          "prompt": "OG share image with headline space",              "model": "imagen-4.0", "aspectRatio": "16:9" },
    { "id": "email-hero",  "prompt": "Email hero banner, wide format",                  "aspectRatio": "16:9" }
  ]
}
```

## Quick Reference

| Sub-task | Model | Why |
|---|---|---|
| LP / anchor hero (photoreal) | `flux-2-pro` | Best photoreal fidelity, sharp text-adjacent composition |
| LP hero (illustrated / editorial) | `recraftv4` | Strong editorial look, brand-controllable |
| Social tiles, OG, email | `recraftv4` | Fast, cheap, consistent with a reference image |
| OG with readable headline | `imagen-4.0` or `ideogram-v3` | Cleanest in-image typography |
| App Store screenshots | `gpt-image-1.5` or `flux-2-pro` | Good at UI mockups + device frames |
| Reel / motion hero | `kling-v3` (i2v from hero) | 5-15s high-quality animation |
| Soundtrack | `minimax-music-v2` | Clip-synced AI score |

## Procedure

- **Generate the hero alone, first.** It sets the palette, composition language, and texture for everything else. Skipping this step produces a scattered-looking kit.
- **Always pass `-i hero.webp` to the fan-out.** That single flag is the difference between "one brand" and "ten stock images".
- **Dry-run the full manifest before the first real batch.** `gen-ai batch run ... --dry-run` catches typos and bad paths without spending credits.
- **Keep prompts short and specific about the container, not the content** — "LinkedIn announcement card, professional tone" beats a 40-word paragraph. The hero image is already carrying the visual language.
- **Save to Drive with a dated folder** (`launch-$(date +%F)`) so future tweaks have provenance.
- **Ship in a named project folder** on the user's machine (`./launch-kit/`) plus Drive. Don't dump into `~/Downloads`.
- **If the user hates one asset, regenerate only that one** — `gen-ai redo -p "<tweaked prompt>"` keeps everything else intact.
- **Cap the kit at ~10 assets for the first pass.** More = slower feedback loop = worse end result.

## Pitfalls

- **Fanning out before approving the hero** — every asset inherits the hero's aesthetic. A bad hero = 10 bad assets.
- **Forgetting the reference image on fan-out** — without `-i hero.webp`, Recraft will drift into its default style and the kit looks stitched together.
- **Over-prompting inside the fan-out** — the hero already defines palette and mood. Repeating all of that in every sub-prompt fights the model.
- **Mismatched aspect ratios across the kit** — if PH expects 3:2 gallery and you ship 1:1, you're cropping on launch day. Verify specs before batching.
- **Trying to render in-image headline text in every asset** — only `imagen-4.0` / `ideogram-v3` do this well. Put text via overlay (Figma, Canva) on the others.
- **Skipping the archive step** — when the user comes back for v2 next week, the originals are gone. Preserve the approved `./launch-kit` folder.

## Verification

Run `gen-ai whoami` to confirm authentication, then re-run the failed command with `--debug`.

## Cost & time

| Asset | Credits | Time |
|---|---|---|
| 1× hero (flux-2-pro, 16:9) | ~8 | ~45s |
| 4× PH tiles (recraftv4, 1:1, i2i) | ~8 | ~60s total |
| 4× social cards (recraftv4, i2i) | ~8 | ~60s total |
| 1× OG (imagen-4.0) | ~3 | ~30s |
| 1× reel (kling-v3, 5s) | ~15 | ~150s |
| 1× soundtrack (minimax-music, 15s) | ~3 | ~30s |
| **Typical 10-asset kit (no video)** | **~30** | **~5 min** |
| **Typical 10-asset kit + reel + music** | **~50** | **~10 min** |

## See also

- [gen-ai-use.md](../../gen-ai-use/SKILL.md) — CLI command reference, flags, model IDs
- [gen-ai-workflows.md](../../gen-ai-workflows/SKILL.md) — Workflow 5 (Launch kit) in the broader catalog
- [gen-ai-batch.md](../../gen-ai-batch/SKILL.md) — manifest schema, concurrency, cost control
- [install-gen-ai-cli-and-mcp.md](../../install-gen-ai-cli-and-mcp/SKILL.md) — set up the CLI + MCP server
- `prosumer-product-mockups` — if the launch needs physical/lifestyle product renders
- `prosumer-content-visual-pair` — for the ongoing content queue after launch day
