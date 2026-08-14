---
name: agency-brand-scoping
description: Five brand direction variations for pitch discovery.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: agency
    tags: [picsart, agency, creative, client-work]
---

# Agency brand scoping

A fast discovery pass for a new client: gather brand signals (site, deck, competitors, audience, tone), lock them into a reusable `brand-system.json` file, and produce 5 on-direction visual explorations to validate with the client before any production spend.

**URL / deck in → brand-system.json + 5 direction variations out.** One hour, under $1 in generation cost, reusable across the rest of the engagement.

## When to Use

- Responding to an RFP and need 5 distinct visual directions for the first review
- Net-new client pitch — you've read the brief, now you need on-brand sketches
- Kickoff phase of a signed engagement, before production generations start
- Scoping a rebrand: grab the existing brand, propose 5 evolution paths
- Any moment where "what does this brand look like in AI generation" is the open question

**Do not use for** finished campaign assets — this is discovery only. Lock the system here, then run `agency-pitch-mockups` or `agency-multi-brand-pack` for deliverables.

## Prerequisites

Ask the user (batch in one message):

1. **Client name + slug** — used for folder + manifest tags (e.g. `acme-fintech`)
2. **Brand references** — URL, existing deck, Figma file, or "no brand yet, we're defining it"
3. **Competitors / comparable brands** — 2-3 names; informs what NOT to look like
4. **Audience + tone** — who buys, what feeling ("premium + restrained" vs "bold + irreverent")
5. **Deliverable type the scope is for** — pitch deck, campaign, launch film, product shoot (informs aspect ratios)
6. **Confidentiality** — is this NDA? If yes, never name the client in public Drive folders or prompts

If the user gives a URL or deck, read/fetch it first and extract palette, typography impression, imagery style, and tone words. Propose the `brand-system.json` back for confirmation before generating.

## How to Run

```
1. INGEST     → read URL / deck / Figma, extract signals
2. DRAFT      → propose brand-system.json (palette, type-feel, imagery, tone, do-nots)
3. CONFIRM    → user locks the system; save to clients/<slug>/brand-system.json
4. ESTIMATE   → gen-ai pricing on the 5-direction batch (< $1 target)
5. GENERATE   → 5 directions, each with a single-word descriptor tag
6. REVIEW     → contact-sheet the 5 outputs, get client pick
7. LOCK       → winning direction becomes clients/<slug>/brand.md for all future work
```

**Rules:**

- **Never skip step 2.** Without `brand-system.json`, every future generation for this client re-litigates brand from scratch.
- **Always estimate before generating.** 5 variants at `recraftv4` ≈ 10 credits, but confirm in-session.
- **Keep pitch outputs watermark-free only if the client has signed.** For cold pitches, add `"obvious mockup"` language in prompt.
- **Never mix clients in a single Drive folder or manifest.** Namespace everything under `clients/<slug>/`.

## Quick Reference

```json
{
  "client_slug": "acme-fintech",
  "brand_system": "clients/acme-fintech/brand-system.json",
  "defaults": { "model": "recraftv4", "aspectRatio": "16:9" },
  "variants": {
    "direction": ["editorial", "bold", "minimal", "playful", "cinematic"]
  },
  "jobs": [
    { "id": "{direction}", "prompt": "<client descriptor> — {direction} direction" }
  ]
}
```

Lock the winning direction back into `clients/<slug>/brand.md` — a 10-line markdown file Claude + downstream batches can include in prompts.

## Quick Reference

| Sub-task | Model | Why |
|---|---|---|
| Direction exploration (default) | `recraftv4` | Design-forward, honors palette + type feel, cheap |
| Photo-led brands (fashion, hospitality) | `flux-2-pro` | Photoreal, better lighting, for brands that live in photography |
| Typography-centric directions (editorial posters, quote slides) | `ideogram-v3` | Only model that renders readable headlines reliably |
| Quick cheap drafts when testing 10+ directions | `gemini-3.1-flash-image` or `gemini-3.1-flash-image` | ~1 credit each; use for throwaway iteration |

Check live IDs with `gen-ai models --mode image` before committing — names shift.

## Procedure

- **Always scope brand before generating production work.** One hour of scoping saves a week of misaligned deliverables.
- **Descriptor-per-direction beats vague prompts.** "Editorial" + specific cues > "something clean and modern".
- **Never leak other clients' assets into a new client's prompt.** No `-i` from a different client folder, ever.
- **Save `brand-system.json` to the repo, not Drive.** It's versioned alongside code and MRs.
- **Propose 5, not 10.** Client decision fatigue is real; 5 distinct directions forces a real pick.
- **For NDA clients, don't name them in prompts.** Use a generic descriptor ("a premium fintech for seed-stage founders") — prompts are logged.
- **Build a reusable prompt library per client** at `clients/<slug>/prompts/` — hero, tile, social, OG templates that all reference the locked direction.

## Pitfalls

- **Generating before locking `brand-system.json`** → 5 gorgeous directions that don't fit the brand
- **Brand cross-contamination** — reusing a prior client's `brand.md` "because it looked nice" — your competitive moat is per-client rigor, don't blow it
- **Descriptor overlap** — "bold" and "cinematic" blur if prompts aren't distinct enough; each direction needs a clearly different visual hypothesis
- **Over-polished scoping** — if the scoping output looks like a finished ad, the client will ask "why not use this?" and you've skipped production
- **Missing competitor check** — landing on a direction that looks identical to the client's biggest rival
- **Public Drive folder for an NDA client** — always use `--drive-folder "internal-$CLIENT"` or a private workspace

## Verification

Run `gen-ai whoami` to confirm authentication, then re-run the failed command with `--debug`.

## Step 1: Ingest + propose brand-system.json

Pull signals from whatever the client gave you. If it's a URL, fetch it. If it's a deck, read it. Summarize into:

```json
{
  "client_slug": "acme-fintech",
  "brand": {
    "palette": { "primary": "#0B1F3A", "accent": "#00D4A3", "neutral": "#F5F3EE" },
    "typography_feel": "geometric sans, tight tracking, editorial weights",
    "imagery_direction": "abstract finance, muted photography, no stock clichés",
    "tone_words": ["trustworthy", "calm", "precise"],
    "do_not": ["cartoon illustration", "neon gradients", "tech-bro stock photos"]
  },
  "competitors": ["wise.com", "mercury.com"],
  "audience": "seed-stage founders, CFO buyers",
  "confidentiality": "NDA"
}
```

Save to `clients/<slug>/brand-system.json`. This file is the single source of truth referenced by every downstream skill.

## Step 2: Generate 5 directions

Each direction gets a single-word descriptor. Standard starter set: **editorial, bold, minimal, playful, cinematic**. Swap any that clashes with the brand's tone words (e.g. drop "playful" for a private bank).

```bash
CLIENT="acme-fintech"
OUT="clients/$CLIENT/scoping"
mkdir -p "$OUT"

# Check per-call pricing first, then multiply by 5 directions.
gen-ai pricing recraftv4

# Run as 5 discrete jobs so each can get its own direction prompt
cat > /tmp/$CLIENT-scoping.json <<EOF
{
  "defaults": { "model": "recraftv4" },
  "jobs": [
    { "id": "01-editorial", "prompt": "$CLIENT hero — editorial magazine feel, restrained palette, generous whitespace, confident typography", "aspectRatio": "16:9" },
    { "id": "02-bold",      "prompt": "$CLIENT hero — bold graphic, high contrast, oversized type, flat color blocking", "aspectRatio": "16:9" },
    { "id": "03-minimal",   "prompt": "$CLIENT hero — minimal composition, single focal element, muted neutrals, precise negative space", "aspectRatio": "16:9" },
    { "id": "04-playful",   "prompt": "$CLIENT hero — playful abstract shapes, warm palette, hand-drawn accent, approachable energy", "aspectRatio": "16:9" },
    { "id": "05-cinematic", "prompt": "$CLIENT hero — cinematic photography, shallow depth of field, moody lighting, filmic grain", "aspectRatio": "16:9" }
  ]
}
EOF

gen-ai batch run /tmp/$CLIENT-scoping.json -c 5 -o "$OUT"
```

Results land at `clients/<slug>/scoping/0X-<direction>.webp` + `results.json`. Present the 5 side-by-side to the client.

## Cost & time

| Phase | Typical spend | Typical time |
|---|---|---|
| Scoping (this skill, 5 directions, `recraftv4`) | ~$0.50–$1 | 15-30 min incl. review |
| Production (after direction lock) | $5–$50 per asset set | Per deliverable |

Keep scoping under $1. If a client won't approve a direction after 5, the brief is broken — don't burn credits, push back on the brief.

## See also

- `workflows/agency-pitch-mockups/` — once direction is locked, produce pitch assets
- `workflows/agency-multi-brand-pack/` — run scoping-plus-production across many retainer clients
- `workflows/agency-client-handoff/` — package final work at engagement end
- `gen-ai-workflows.md` — general multi-step patterns
- `gen-ai-batch.md` — manifest shapes and concurrency tuning
