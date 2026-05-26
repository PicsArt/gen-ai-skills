---
name: enterprise-press-batch
description: Press photos into wire, web, print, social packs.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: enterprise
    tags: [picsart, enterprise, governance, scale]
---

# Enterprise Press Batch

Produce full press-release asset bundles — hero, executive headshots, product shots, event-ready horizontal and vertical crops — with embargo controls, wire-service naming conventions, EXIF rights metadata, and multi-resolution exports. Built for comms / PR teams shipping to Reuters, AP, Getty, and corporate newsrooms under embargo.

---

## When to Use

- Product launch, earnings announcement, exec change, crisis response — assets needed across wire + web + print + social in parallel
- Embargoed announcement requiring strict asset handling until lift
- Multi-publication distribution where each wire has different resolution + EXIF requirements
- Executive headshot refresh across a leadership team (consistent lighting, backgrounds, crops)
- Event kits: pre-event (concept), during-event (placeholder + real), post-event (recap)

Do **not** use for: social-only launches (use `gen-ai-workflows` launch-kit), single-asset news posts.

---

## Prerequisites

Before the batch runs:

1. **Release type + embargo** — announcement date/time, embargo lift, distribution list. Embargoed runs must write to a locked Drive folder.
2. **Asset scope** — which of: 1 hero, N exec headshots, M product shots, event horizontal, event vertical, social derivatives. Count per type.
3. **Distribution targets** — wire service specs (AP: 3000px long edge JPEG, Getty: TIFF, Reuters: sRGB embedded). Determines resolution + format per pack.
4. **Rights metadata** — credit line, copyright owner, usage rights, caption, contact. Written to EXIF/IPTC.
5. **Approval chain** — legal, comms lead, exec approval for headshots? Who signs off before embargo pack ships?
6. **Audit trail** — does the archive need the original brief + manifest + results for seven years (SOX-adjacent)?

---

## How to Run

Six steps. Embargo handling is non-negotiable.

1. **Scope the bundle** — write the deliverable matrix: asset × pack (wire / web / print / social) × resolution. Costs scale by cells, not by source images.
2. **Generate / ingest sources** — AI-generated heroes via `gen-ai generate`; real executive photography ingested via `gen-ai upload`. Enhance with `topaz-upscale-image` if source resolution is below print spec.
3. **Embargo lock** — create a restricted archive location. Everything until lift lands here. Never ship intermediate drafts.
4. **Batch exports** — one manifest per pack (wire / web / print / social), each with the correct resolution, format, and color profile. Watermark drafts; never watermark final approved wire assets.
5. **Stamp EXIF / IPTC** — rights, credit, caption, embargo notice injected on every file. Use `exiftool` as a post-batch step.
6. **Deliver** — at embargo lift, promote from the locked folder to the public press-kit URL. Archive the manifest + results.json + checksum manifest for the audit trail.

## Quick Reference

Each pack is its own manifest so wire / print / web / social can run in parallel with correct specs.

```json
{
  "defaults": {
    "model": "topaz-upscale-image"
  },
  "metadata": {
    "release": "2026-04-LAUNCH",
    "embargo_lift": "2026-04-22T13:00:00Z",
    "brand_system_version": "brand.md@sha:a4f1c9",
    "approver": "comms-lead@company.com",
    "audit_id": "PRESS-2026-04-LAUNCH",
    "distribution": ["AP", "Reuters", "Getty", "corporate-newsroom"],
    "rights": {
      "credit": "Company Inc.",
      "copyright": "(c) 2026 Company Inc.",
      "usage": "Editorial use in connection with 2026 launch coverage only."
    }
  },
  "jobs": [
    {
      "id": "hero-16x9-wire",
      "imageUrls": ["./sources/hero-master.png"],
      "prompt": "4x upscale, sharpen, retain color profile",
      "aspectRatio": "16:9"
    },
    {
      "id": "exec-ceo-headshot-3x4-wire",
      "imageUrls": ["./sources/ceo-raw.jpg"],
      "prompt": "Editorial portrait enhance, studio light preserved"
    }
  ]
}
```

Filename convention (wire-service friendly): `{release-id}_{asset-type}_{subject}_{aspect}_{resolution}.{ext}` → `2026-04-LAUNCH_hero_product_16x9_4k.jpg`. Survives rebranding; matches Reuters/Getty ingest patterns.

---

## Quick Reference

| Sub-task | Model | Notes |
|----------|-------|-------|
| Hero concept (AI-generated) | `flux-2-pro` / `gemini-3-pro-image` | Commercial-safe, editorial fidelity |
| Exec headshot enhance (real photo) | `topaz-upscale-image` | Preserves identity; no hallucination |
| Background cleanup on real photo | `picsart-change-bg` | Studio backdrop substitution |
| Background removal for transparent pack | `picsart-remove-bg` | Social + overlay-ready PNG |
| Product shot from angle library | `flux-kontext-pro` | Edit-mode, product-accuracy preserve |
| Event B-roll from single still | `kling-v3-pro` (i2v) | For broadcast packs only |

**Never** use fully-generative models on named executives or real products without explicit legal sign-off. Use enhance/edit-only models. Confirm licensing per account with `gen-ai models info`.

---

## Procedure

- **Embargo-first workflow.** Locked Drive folder from minute one. No assets leave it until lift.
- **Never AI-generate a real executive's face.** Enhance / upscale real photography only. Legal + reputational risk otherwise.
- **Watermark drafts, never watermark approved finals.** Wires reject watermarked assets.
- **Wire-service naming convention** is the contract. `{release}_{type}_{subject}_{aspect}_{res}`. Do not deviate.
- **Stamp EXIF/IPTC before delivery.** Credit, copyright, caption, embargo notice. `exiftool` pass is non-negotiable.
- **Resolution matters.** Print = 300dpi, 4k long edge min. Web = 2400px long edge, sRGB. Social = per-platform. Export once per spec; don't downscale at publish time.
- **Checksum the delivery.** SHA256 manifest shipped alongside the pack so newsrooms can verify integrity.
- **Multi-resolution from a single master.** Render the hero at max quality once, derive downward. Never upscale a JPEG.
- **Brand-gate the AI-generated portions** with `brand.md` (see `enterprise-brand-governor`).

## Pitfalls

- **Embargo leak via public Drive folder** — assets land in the default `gen-ai-cli` folder, which may be broadly accessible. Always `--drive-folder` to a restricted path.
- **AI-generated executive faces** — never acceptable. Use real photography + enhance.
- **Watermark on approved wire asset** — auto-rejected by AP / Reuters ingest. Separate draft vs. final pipelines.
- **Missing EXIF rights** — Getty will reject; Reuters will strip your credit. Always stamp.
- **Wrong color profile** — print pack needs CMYK or at least embedded sRGB. Validate with `exiftool -ColorSpace`.
- **One manifest per pack, not per release** — trying to run all 44 deliverables in one batch mixes resolution specs and you get wrong sizes somewhere. Pack per manifest.

---

## Verification

Run `gen-ai whoami` to confirm authentication, then re-run the failed command with `--debug`.

### Commands

```bash
# Generate the hero
gen-ai generate --model flux-2-pro --prompt "$HERO_PROMPT" \
  --aspect-ratio 16:9 --resolution 4k \
  --save-to-drive --drive-folder "Press-2026-04-LAUNCH"

# Enhance exec headshots to print spec
gen-ai batch run exec-headshots.json \
  --concurrency 3 --output ./runs/press-2026-04-execs

# Export the multi-resolution packs
gen-ai batch run press-packs.json \
  --concurrency 5 --output ./runs/press-2026-04-packs

# Post-process: stamp rights metadata (exiftool)
exiftool -overwrite_original \
  -Credit="Company Inc." \
  -Copyright="(c) 2026 Company Inc. All rights reserved." \
  -Caption-Abstract="$CAPTION" \
  -By-line="Company Inc. Press Office" \
  ./runs/press-2026-04-packs/*.jpg
```

---

## Cost & time

Assumes one release: 1 hero + 4 exec headshots + 6 product shots × 4 packs each (wire / print / web / social).

| Component | Credits | Wall time |
|-----------|---------|-----------|
| 1 hero (flux-2-pro, 4k) | ~10 | ~2 min |
| 4 exec enhances (topaz, 4x) | ~40 | ~5 min |
| 6 product edits (flux-kontext-pro) | ~30 | ~8 min |
| Multi-res derivatives + EXIF + Drive | 0 | ~8 min |
| **Total per release** | **~80** | **~25 min** |

Crisis-response same-asset-set in <60 min is achievable with this pipeline; physical shoots cannot.

---

## See also

- [enterprise-brand-governor](../enterprise-brand-governor/SKILL.md) — brand.md gating for AI-generated portions
- [enterprise-pinned-registry](../enterprise-pinned-registry/SKILL.md) — lock models so pre-embargo renders match final
- [product-photo-studio](../product-photo-studio/SKILL.md) — adjacent batch pattern (reshoot mode)
- [multi-channel-bundle](../multi-channel-bundle/SKILL.md) — launch and campaign bundle patterns
- [gen-ai-use](../gen-ai-use/SKILL.md) — CLI reference
