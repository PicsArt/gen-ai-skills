---
name: enterprise-brand-governor
description: Gate every generation through a brand policy file.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: enterprise
    tags: [picsart, enterprise, governance, scale]
---

# Enterprise Brand Governor

Policy-as-code for AI-generated imagery. Every prompt is pre-validated against `brand.md`, every output is post-checked, violations escalate to a human approver, and every decision is logged. Built for regulated industries and any enterprise where an off-brand asset in production is a material risk.

---

## When to Use

- Multiple teams (marketing, product, sales, agency partners) generating on the same brand system
- Regulated industries (pharma, finance, alcohol, kids) where imagery has legal constraints
- Brand-safety SLA — zero tolerance for competitor logos, restricted props, or off-palette output reaching production
- Agency handoff — external vendor generating on your brand, you need a gate you control
- Pre-production review cycle needs automation; humans only review escalations

Do **not** use for: quick exploration / mood-board work (gating slows ideation), or accounts without a written brand system yet (build `brand.md` first).

---

## Prerequisites

Before rolling the governor across teams:

1. **Brand system location** — path / repo / URL for `brand.md`. Who owns it? What's the change-control process?
2. **Policy strictness** — reject (halt), flag (log + allow), or tier by asset destination (production = reject, internal = flag)?
3. **Approval chain** — who reviews flagged items? What's the SLA for escalation turnaround (1h, 24h, 3 business days)?
4. **Logging destination** — local `~/.gen-ai/audit/`, S3 bucket, or ship to SIEM (Splunk, Datadog)?
5. **Compliance constraints** — GDPR / HIPAA / COPPA / financial-services rules that must be encoded in `brand.md`?
6. **Rollback plan** — if the governor blocks a legitimate launch, who has override authority and how is that logged?

---

## How to Run

The governor runs at three checkpoints: prompt, generation, output.

1. **Author `brand.md`** — palette, typography, allowed/denied props, imagery style, voice, regulated-category rules. Versioned in git. Commit SHA is the policy ID.
2. **Pre-flight (prompt lint)** — `gen-ai validate` against the prompt before spending credits. Catches banned terms, disallowed concepts, missing required elements (e.g., disclaimer placement).
3. **Brand-context generation** — every `gen-ai generate` and `gen-ai batch run` prompt includes the relevant `brand.md` constraints. Review violations during QA.
4. **Post-flight (output check)** — for critical assets, a second-pass model (`gemini-3-pro-image` or vision check) verifies the output matches policy. Palette sampling, logo presence detection, prop allow-list.
5. **Escalation** — any `violation` status routes to the approver queue. Humans review, approve or reject, decision is logged against the audit ID.
6. **Audit export** — daily / weekly export of all decisions to the configured SIEM or compliance archive.

## Quick Reference

The governor adds policy metadata to every job record.

```json
{
  "defaults": {
    "model": "flux-2-pro"
  },
  "metadata": {
    "policy_id": "brand.md@sha:a4f1c9",
    "policy_version": "2.3.0",
    "policy_mode": "reject",
    "approver": "brand-governance@company.com",
    "escalation_channel": "#brand-review",
    "audit_id": "GOV-2026-04-CAMPAIGN-LAUNCH",
    "compliance_tags": ["GDPR", "US-FTC-native-ad"],
    "data_residency": "eu-west-1"
  },
  "jobs": [
    {
      "id": "launch-hero-001",
      "prompt": "Production launch hero. Editorial hero, team of four diverse professionals collaborating, modern office, natural light, brand palette. Apply brand.md constraints and require legal review before publishing."
    }
  ]
}
```

Record policy decisions in the downstream audit ledger: `approved`, `flagged`, or `rejected` with the reason.

---

## Quick Reference

| Sub-task | Model | Notes |
|----------|-------|-------|
| Prompt compliance check | `gpt-image-1.5` / text reasoner | Cheap pre-flight before image spend |
| Primary generation (brand-safe) | `flux-2-pro` | Strong prompt adherence, commercial-safe |
| Primary generation (product accuracy) | `flux-kontext-pro` | Edit-mode when subject must be preserved |
| Post-generation vision audit | `gemini-3-pro-image` | Strong scene understanding for policy checks |
| Upscale approved outputs only | `topaz-upscale-image` | Never upscale before approval — wastes credits |

Confirm commercial-use status per provider with `gen-ai models info <id>`. Pharma and financial services should maintain a short allow-list of pre-cleared models.

---

## Procedure

- **Treat `brand.md` as code.** Versioned, reviewed, signed. The file's commit SHA is the policy ID in every audit record.
- **Always pin the model version.** Policy interpretation changes when models change. Pair with `enterprise-pinned-registry`.
- **Pre-flight before spend.** `gen-ai validate` catches 80% of violations for $0.
- **Human-in-the-loop on rejects.** A reject is a business decision, not a tool decision. Route to the approver.
- **Default to reject, not flag.** Flag mode is for drafts only; production must reject.
- **Log everything.** Every prompt, every decision, every override. No silent approvals.
- **Rotate the audit log.** Daily JSONL, shipped off the dev machine. Local logs disappear; SIEM doesn't.
- **Test the governor with adversarial prompts.** Red-team your own policy quarterly — does it actually catch competitor logos, prohibited claims?
- **Document the override path.** There will be legitimate exceptions. Make the override visible, logged, and time-boxed.

---

## Pitfalls

- **`brand.md` too vague** — "use the brand palette" is not enforceable. Hex codes, prop allow-lists, explicit denies.
- **No override path** — legitimate exceptions get bypassed outside the system, breaking the audit. Build the override in.
- **Logs only local** — dev machines die. Ship to SIEM or a durable archive from day one.
- **Flag-mode in production** — "we'll review later" never happens. Default reject.
- **Unaudited model swaps** — someone swaps `flux-2-pro` for a new model mid-campaign and policy interpretation changes. Pin.
- **Missing post-check on hero assets** — prompt passed, output didn't. For production heroes, always run the vision audit.

---

## Verification

Run `gen-ai whoami` to confirm authentication, then re-run the failed command with `--debug`.

### Commands

```bash
# Pre-flight validate a prompt before spending credits
gen-ai validate --model flux-2-pro --file prompt.json

# Gated single generation
gen-ai generate --model flux-2-pro --prompt "$PROMPT" \
  --save-to-drive --drive-folder "Gated-Output"

# Gated batch with retry on transient failures only (not violations)
gen-ai batch run campaign.json \
  --concurrency 4 --output ./runs/campaign-2026-04

# Flag mode — for internal / draft contexts
gen-ai batch run drafts.json \
  --output ./runs/drafts-2026-04
```

---

## Cost & time

Governance overhead is tiny relative to generation. Pre-flight + post-check adds ~10–15% to credit cost on critical assets, ~0% on non-critical.

| Scenario | Governance overhead |
|----------|--------------------|
| Single gated generate | +0 credits (policy passed in-call) |
| Single gen + vision audit | +1–2 credits |
| Batch of 100, pre-flight only | +~5 credits (text reasoner) |
| Batch of 1,000, full pipeline | +~50 credits + 1 approver hour |
| Quarterly red-team audit | ~1 engineer-day + ~200 credits |

Violations rejected = credits saved. A single blocked off-brand production asset typically saves multiples of the governor's overhead.

---

## See also

- [enterprise-pinned-registry](../enterprise-pinned-registry/SKILL.md) — pin model versions so policy interpretation stays stable
- [product-photo-studio](../product-photo-studio/SKILL.md) — brand-gated catalog pipeline (reshoot mode)
- [enterprise-press-batch](../enterprise-press-batch/SKILL.md) — brand-gated PR pipeline with embargo handling
- [gen-ai-use](../gen-ai-use/SKILL.md) — CLI reference
