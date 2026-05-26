---
name: agency-client-handoff
description: Export a white-label client deliverable as a zip.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: agency
    tags: [picsart, agency, creative, client-work]
---

# Agency client handoff

Package a completed engagement for transfer to the client's in-house team, DAM, or next agency — with the asset set, prompt library, model pins, rights documentation, and everything else the receiving team needs to regenerate consistent work without you in the loop.

**Engagement done → reproducible handoff bundle.** Knowledge transfer over lock-in: the receiving team should be able to keep the brand on-model without calling the agency back.

## When to Use

- End of an engagement, client taking work in-house
- Transition to a new agency of record — outgoing handoff
- Completed pitch / campaign — asset package with provenance for the client's DAM
- Contract-mandated "source file" delivery with regeneration rights
- Year-end portfolio snapshot for a long-term retainer client

**Do not use for** work-in-progress reviews (use Drive links), approvals (use proof PDFs), or internal archival (use your agency's backup). Handoff is the formal, client-owned, reproducible bundle.

## Prerequisites

Ask the user (one message):

1. **Client slug + engagement scope** — which client, which project or retainer period is being handed off
2. **Receiving team** — in-house creative? Another agency? Which format and tools do they use (Figma, Adobe, CapCut, Notion)?
3. **Rights status** — are all inputs licensed? Any stock, fonts, or reference faces that need redacting or citing?
4. **Regeneration expectation** — does the client need to re-generate assets on their own, or is this a static archive?
5. **Confidentiality** — any internal prompts, competitor references, or tagged metadata that must be stripped before delivery?
6. **Delivery format** — zip + Drive link? Direct to client S3 / DAM? Physical drive?

If the client needs regeneration capability, they'll need the gen-ai CLI themselves — add an install guide to the bundle.

## How to Run

```
1. INVENTORY   → pull every asset + results.json from clients/<slug>/ across the engagement
2. FILTER      → exclude drafts, rejected variants, internal-only WIP
3. STRIP       → white-label: remove agency tags, internal prompt notes, competitor refs
4. PIN MODELS  → lock every prompt's model to an exact ID + version (not "latest")
5. DOCUMENT    → generate README, RIGHTS.md, CHANGELOG, prompt library
6. PACKAGE     → zip with consistent folder structure + naming
7. VERIFY      → extract and cold-test: can a fresh machine regenerate one asset?
8. DELIVER     → upload to client destination, share link, brief the receiving team
```

**Rules:**

- **Pin every model ID.** `recraftv4` → `recraftv4@2026-03-15` (or the exact ID returned by `gen-ai models info`). "Latest" will drift and break reproducibility.
- **Strip internal metadata.** Tags like `retainer-week-2026-04-22` or `pitch-concept-b` are internal — not for client eyes.
- **Include prompts, not just outputs.** A prompt library lets the client's in-house team iterate without re-inventing the system.
- **Never ship a handoff you haven't cold-tested.** Unzip, pick one prompt, regenerate — if the output drifts, something isn't pinned.

## Quick Reference

```json
{
  "handoff_kind": "client-final",
  "client_slug": "acme-fintech",
  "engagement": "2025-Q3 to 2026-Q2 retainer",
  "delivered_at": "2026-04-22",
  "brand_system": "docs/brand-system.json",
  "brand_rules": "docs/brand.md",
  "pinned_models": "docs/model-pins.json",
  "assets_count": 247,
  "prompts_count": 54,
  "rights_status": "all generated, no licensed stock",
  "regeneration_supported": true,
  "support_window_days": 30
}
```

Include this as `docs/handoff-manifest.json` — a single file that tells the receiving team what they got and what they can do with it.

## Quick Reference

Handoffs don't generate new assets — they package existing ones. But for reproducibility checks:

| Task | Model | Notes |
|---|---|---|
| Dry-run regeneration test (cheapest) | `gemini-3.1-flash-image` | Use to verify payload validity, not output quality |
| Full regeneration proof (one asset) | Same as original, pinned | Matches the original bundle; compare outputs visually |
| Re-export at higher resolution | `topaz-upscale-image` | If the client DAM wants 4K versions |

Never substitute a newer model for the pinned one during handoff — the whole point is that the client can reproduce the agency's output exactly.

## Procedure

- **Reproducibility is the deliverable.** If the client can't regenerate without you, the handoff failed — even if the asset folder is beautiful.
- **Strip, don't redact.** Remove internal tags entirely; the bundle should look native to the client.
- **Version the handoff** — `handoff-v1/`, `handoff-v2/`. Don't overwrite if an updated bundle is requested later.
- **Include a sunset date** for agency support — clarifies when the client self-serves or re-engages.
- **Pin exact model IDs** with `gen-ai models info <id> --json` — preserves capabilities at handoff time.
- **Test on a clean machine.** Your laptop has tokens, fonts, caches. The bundle has to work without those.
- **No lock-in flags.** Everything in the bundle runs on a stock `gen-ai` install.
- **Ship prompts, brand, and rationale.** Context beats artifacts for knowledge transfer.

## Pitfalls

- **Unpinned models** — client regenerates 6 months later, output drifts, blames the agency.
- **Internal metadata leakage** — competitor refs, pitch-concept tags, reviewer names surviving in prompt files.
- **Missing rights documentation** — client legal can't sign off on re-use, bundle is DOA.
- **Proprietary tools in the regen path** — strip to stock `gen-ai` CLI only.
- **No cold test** — bundle ships, step 1 of the README fails, urgent Slack follows.
- **One-and-done mentality** — promise 30 days of Q&A post-handoff, price it in.

## Verification

Run `gen-ai whoami` to confirm authentication, then re-run the failed command with `--debug`.

## Step 1: Inventory and filter

```bash
CLIENT="acme-fintech"
HANDOFF="handoff/$CLIENT-$(date +%Y-%m-%d)"
mkdir -p "$HANDOFF"/{assets,prompts,source,docs}

find "clients/$CLIENT" -name "results.json" -exec cp {} "$HANDOFF/source/" \;
cp -r "clients/$CLIENT/deliverables/"* "$HANDOFF/assets/"
node scripts/extract-prompts.js "$HANDOFF/source/" > "$HANDOFF/prompts/prompt-library.json"
```

## Step 2: Pin models, strip internal data

```bash
# Get pinned model IDs for every model the engagement used
for model in $(jq -r '.jobs[].model' "$HANDOFF/source/"*.json | sort -u); do
  gen-ai models info "$model" --json >> "$HANDOFF/docs/model-pins.json"
done

# Strip internal tags from the prompt library
jq 'del(.jobs[].tags[] | select(startswith("internal-") or startswith("retainer-")))' \
  "$HANDOFF/prompts/prompt-library.json" > "$HANDOFF/prompts/prompt-library.clean.json"
mv "$HANDOFF/prompts/prompt-library.clean.json" "$HANDOFF/prompts/prompt-library.json"
```

## Step 3: Documentation

Generate a `README.md` covering: folder walkthrough, regeneration steps (CLI install + one worked example), pinned model note, rights status, support contact + sunset date. Include `docs/brand-system.json`, `docs/brand.md`, `docs/model-pins.json`, `docs/RIGHTS.md`, `docs/CHANGELOG.md`.

Minimum regeneration steps to include in the README:

```
1. Install CLI: curl -fsSL https://picsart.com/gen-ai-cli/install.sh | bash
2. gen-ai login
3. Pick a prompt from prompts/prompt-library.json
4. gen-ai generate -m <pinned-model-id> -p "<prompt>"
```

## Step 4: Package + verify

```bash
cd handoff
zip -r "$CLIENT-handoff-$(date +%Y-%m-%d).zip" "$CLIENT-$(date +%Y-%m-%d)/" \
  -x "*.DS_Store" "*/.git/*"

# Cold test — extract to a clean dir, regenerate one asset
tmpdir=$(mktemp -d) && unzip -q "$CLIENT-handoff-$(date +%Y-%m-%d).zip" -d "$tmpdir"
cd "$tmpdir/$CLIENT-$(date +%Y-%m-%d)"
SAMPLE_PROMPT=$(jq -r '.jobs[0].prompt' prompts/prompt-library.json)
SAMPLE_MODEL=$(jq -r '.jobs[0].model' prompts/prompt-library.json)
gen-ai generate -m "$SAMPLE_MODEL" -p "$SAMPLE_PROMPT"  --dry-run --debug
# Dry-run validates = bundle is regeneration-ready.
```

## Cost & time

| Phase | Spend | Time |
|---|---|---|
| Inventory + filter + strip | $0 | 1-2 hrs |
| Documentation (README, RIGHTS, CHANGELOG) | $0 | 1-2 hrs |
| Cold-test regeneration (1-2 assets) | ~$0.50 | 15 min |
| **Total handoff** | **<$1** | **~4 hrs** |

The real cost is time, not credits. Budget a half-day per handoff; cutting corners creates support calls for months after.

## See also

- `workflows/agency-brand-scoping/` — `brand-system.json` + `brand.md` that ship in the handoff
- `workflows/agency-multi-brand-pack/` — source of per-client results.json archive
- `workflows/agency-pitch-mockups/` — pitch bundles that become part of the final handoff
- `gen-ai-use.md` — regeneration reference for the client
