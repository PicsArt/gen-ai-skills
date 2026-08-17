---
name: enterprise-pinned-registry
description: Pin exact model versions for reproducible output.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: enterprise
    tags: [picsart, enterprise, governance, scale]
---

# Enterprise Pinned Registry

A lockfile concept for AI generation. Model versions, prompts, brand tokens, and seeds are pinned to a manifest that regenerates the same campaign identically six months, a year, or three years later. Built for enterprises that need reproducibility for legal holds, brand-campaign continuity, regulatory defense, and year-over-year comparability.

---

## When to Use

- Multi-team deployment: 20+ designers / PMs / agencies generating on the same brand, need identical output across all of them
- Year-over-year campaign (annual report, quarterly earnings graphics) must match the prior year's look exactly
- Regulated industry where "reproducible" is a compliance requirement, not a preference
- Legal hold — a specific asset may need to be regenerated identically for litigation support
- Model-provider change management — new versions ship weekly; you want explicit, reviewed upgrades, not drift
- Audit trail: every shipped asset must trace back to a specific model version + prompt + brand token set

Do **not** use for: one-off exploration, draft/ideation phases, consumer projects.

---

## Prerequisites

Before authoring the registry:

1. **Scope** — which models, prompts, and brand tokens are in scope? Start narrow (heroes only) then expand.
2. **Bump cadence** — quarterly? On-demand only? Who approves a bump?
3. **Regression-test corpus** — what's the set of prompts that must be re-run before a bump is approved? (Typically 10–20 representative prompts.)
4. **Storage** — registry in the campaign repo, a dedicated `brand-registry` repo, or a central governance repo?
5. **Rollback plan** — if a bump produces unacceptable drift, how do we revert? (Git revert is usually enough if the registry is in git.)
6. **Audit retention** — how long must the registry + generated outputs be retained? 7 years for SOX-adjacent, 10 for pharma, indefinite for trademark defense.

---

## How to Run

Five steps. The registry is the contract; everything generates against it.

1. **Author `registry.json`** — model aliases, prompt templates, brand tokens, default params. Each alias pins to an explicit `model@version`.
2. **Fingerprint prompts** — every prompt template gets a SHA256 hash stored alongside it. If the prompt string changes, the fingerprint changes, and that's a versioned bump.
3. **Configure the CLI** — `gen-ai config set registry <path>` points every call on this machine at the registry. Teams commit the registry to git and sync via clone/pull.
4. **Generate against aliases** — designers use `flux` (alias), never `flux-2-pro@2.1.3` (raw). Alias resolution is the registry's job.
5. **Bump quarterly** — run the regression corpus against a candidate new version, diff the outputs, get approval, bump the registry, tag the release (`brand-registry-v2026.2`).

## Quick Reference

The registry itself is the manifest. Commit it. Tag it. Diff it on every bump.

```json
{
  "registry_version": "2026.2.0",
  "locked_at": "2026-04-01T00:00:00Z",
  "locked_by": "brand-governance@company.com",
  "previous_version": "2026.1.0",
  "regression_run_id": "REG-2026Q2-APPROVED",
  "models": {
    "flux":     { "id": "flux-2-pro@2.1.3",          "commercial_use": true,  "notes": "Hero, editorial" },
    "kontext":  { "id": "flux-kontext-pro@1.4.0",    "commercial_use": true,  "notes": "Product edit-mode" },
    "upscale":  { "id": "topaz-upscale-image@2.0.0", "commercial_use": true,  "notes": "Print prep" },
    "kling":    { "id": "kling-v3-pro@3.0.1",       "commercial_use": true,  "notes": "I2V broadcast" },
    "portrait": { "id": "gemini-3-pro-image@1.2.0",  "commercial_use": true,  "notes": "Portrait, verify license" }
  },
  "prompt_templates": {
    "hero_launch": {
      "text": "Editorial hero, {subject}, {environment}, brand palette, natural light",
      "fingerprint": "sha256:7b4f2a...c8e1"
    }
  },
  "brand_tokens": {
    "palette": { "primary": "#FF006E", "ink": "#0D0A1F", "accent": "#FFBE0B" },
    "aspect_ratios_allowed": ["16:9", "9:16", "1:1", "3:2"],
    "seed_default": 42
  },
  "audit_id": "REGISTRY-2026.2"
}
```

Every generated asset's `results.json` entry should carry `registry_version` so reproduction is one command away.

---

## Quick Reference

The registry pins them; it doesn't choose them. For picking, see the per-workflow skills. Typical enterprise registry contents:

| Alias | Pins to | Role |
|-------|---------|------|
| `flux` | `flux-2-pro@x.y` | Primary photoreal hero |
| `kontext` | `flux-kontext-pro@x.y` | Edit-mode, product-accuracy preserve |
| `portrait` | `gemini-3-pro-image@x.y` | Faces, commercial-safe (verify license) |
| `upscale` | `topaz-upscale-image@x.y` | Print / wire prep |
| `remove-bg` | `picsart-remove-bg@x.y` | Transparent PNG derivatives |
| `change-bg` | `picsart-change-bg@x.y` | Catalog background replace |
| `kling` | `kling-v3-pro@x.y` | Image-to-video for broadcast |

Confirm commercial-use + regional availability at bump time with `gen-ai models info <id>`. Provider terms change; pin is not a license.

---

## Procedure

- **Aliases everywhere, raw IDs nowhere.** Designers should never see `flux-2-pro@2.1.3` in a prompt — only `flux`.
- **The registry lives in git.** Commit, tag, diff, review, revert. Full audit trail for free.
- **Regression corpus before every bump.** 10–20 canonical prompts, run against old and new, visual diff approved by brand lead.
- **Pin seeds for reproducibility where the model supports it.** `--seed 42` reruns the same output deterministically.
- **Fingerprint prompt templates.** Any string change to a template is a versioned bump, not a silent edit.
- **Tag registry versions semver-like** (`2026.2.0` = year-quarter-patch). Patch for typo fixes; minor for new aliases; major for model swaps.
- **Deprecate, don't delete.** Removing an alias breaks historical reruns. Mark as deprecated, keep the pin, flag in CLI output.
- **Document the bump.** Every version bump ships with a changelog: which model, why, regression results, approver.
- **Re-run a prior campaign from its registry version** quarterly to verify reproducibility still works. If it breaks, the provider deprecated the version — plan migration.

---

## Pitfalls

- **Aliases + raw IDs mixed in manifests** — teams drift off the registry unintentionally. Lint for raw IDs in PRs.
- **No regression corpus** — bumps ship, drift is invisible until a comms leader notices a year later.
- **Provider deprecates a pinned version** — eventually happens. Run your registry's prior versions quarterly to catch this before a legal reroll is needed.
- **Prompt edits without fingerprint bump** — someone "fixes a typo" in a template, now the output differs. Fingerprint + bump.
- **Seed not pinned** — reproducibility is partial without it. Set a registry default seed.
- **Registry in a personal repo** — loses institutional access. Must live in a governance-owned repo.

---

## Verification

Run `gen-ai whoami` to confirm authentication, then re-run the failed command with `--debug`.

### Commands

```bash
# Point the CLI at the registry
gen-ai config set registry.path ./brand-registry/registry.json

# Pin a model alias
gen-ai config set registry.flux flux-2-pro@2.1.3
gen-ai config set registry.kontext flux-kontext-pro@1.4.0
gen-ai config set registry.kling kling-v3-pro@3.0.1
gen-ai config set registry.upscale topaz-upscale-image@2.0.0

# Verify a given alias resolves to the pinned version
gen-ai config get registry.flux
# → flux-2-pro@2.1.3

# Generate using the alias (reproducible)
gen-ai generate --model flux --prompt-file prompts/hero-launch.txt \
  --seed 42

# Batch resolves all aliases against the registry
gen-ai batch run campaign.json
```

Every manifest references aliases, never raw model IDs. The registry is the one place that maps alias → version.

---

## Cost & time

Registry operations are cheap. The value is in what they prevent.

| Activity | Cost | Time |
|----------|------|------|
| Author initial registry | 0 | 1 engineer-day |
| Quarterly regression corpus (20 prompts) | ~200 credits | ~1 h generation + ~2 h review |
| Version bump + tag | 0 | ~30 min |
| Reproduce a 1-year-old campaign | Same credits as original | Same wall time |
| Provider-deprecation migration | ~500 credits | 1–2 engineer-days |

Cost savings scale with team size: a 20-person design team bumping incidentally costs far more in drift than one quarterly reviewed bump.

---

## See also

- [enterprise-brand-governor](../enterprise-brand-governor/SKILL.md) — brand.md gating; pairs with the registry for full policy-as-code
- [product-photo-studio](../product-photo-studio/SKILL.md) — batch catalog runs (reshoot mode); use registry aliases
- [enterprise-press-batch](../enterprise-press-batch/SKILL.md) — embargo-aware pipeline, pin for year-over-year consistency
- [gen-ai-use](../gen-ai-use/SKILL.md) — CLI reference
