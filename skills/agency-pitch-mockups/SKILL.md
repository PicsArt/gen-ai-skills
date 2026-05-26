---
name: agency-pitch-mockups
description: Client-branded pitch mockups: hero, tiles, slides.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: agency
    tags: [picsart, agency, creative, client-work]
---

# Agency pitch mockups

Rapid visuals for a new-business pitch deck: campaign hero, product tiles, key-visual explorations, quote slides — all client-branded, all clearly-labeled-as-mockup, all iterable in under an hour before the pitch.

**Brief + locked direction → full pitch-deck asset set.** Speed first (pitch windows are brutal), reusability second (if you win, these become production inputs), clarity third (nobody should confuse a mockup for shipped work).

## When to Use

- Net-new business pitch, 48-hour turnaround
- Mid-pitch concept swap — client leaned toward direction 3, need assets tonight
- Multiple concepts per pitch (A/B/C) — each needs its own hero + 3 tiles
- Internal review deck for a signed client's next campaign
- Pre-approval creative exploration before any photo/video production spend

**Do not use for** finished deliverables — pitch mockups are intentionally aspirational and mockup-flagged. For final assets after win, use `agency-multi-brand-pack` or project-specific production workflows.

## Prerequisites

Ask the user (one message):

1. **Client slug + brand file** — path to `clients/<slug>/brand.md` (output of `agency-brand-scoping`). If missing, run brand-scoping first.
2. **Pitch concept(s)** — one tagline or idea per concept (e.g. "Banking that waits for you")
3. **Deliverable breakdown** — how many heroes, tiles, quote slides per concept? Default: 1 hero + 3 tiles + 2 quote slides
4. **Pitch date** — drives whether we run cheap drafts or go straight to finals
5. **Confidentiality** — NDA status; affects Drive folder + any watermark choice
6. **Mockup labeling** — visible "MOCKUP" watermark, subtle footer, or none? (default: subtle footer for external pitches)

If the user hasn't locked a direction yet, stop and route them to `agency-brand-scoping` first. Don't pitch on guesses.

## How to Run

```
1. LOAD BRAND    → read clients/<slug>/brand.md + brand-system.json
2. PLAN          → table of every asset with prompt + aspect + model
3. ESTIMATE      → gen-ai pricing on the full manifest (target < $5)
4. DRAFT PASS    → run at draft quality (gemini-3.1-flash-image / recraftv4) for fast iteration
5. CLIENT REVIEW → internal pitch-team review on the draft set
6. FINALIZE      → upgrade approved concepts to flagship models
7. WATERMARK     → add subtle "MOCKUP" footer where required
8. DELIVER       → organized folder + approved upload/link + deck-ready filenames
```

**Rules:**

- **Always draft-then-upgrade.** 80% of pitch iterations die in internal review — don't pay flagship prices twice.
- **Every prompt cites the brand file.** ` on every generate / batch.
- **Pitch mockups should be obviously mockups** unless the client expects production-level polish. Padded aspect ratios, generic text ("HEADLINE HERE"), or visible mockup tags reduce the "why isn't this the final?" conversation.
- **Never use real competitor brand marks, real logos you don't have rights to, or recognizable faces.** Stock-lookalike issues kill pitch trust.

## Quick Reference

```json
{
  "client_slug": "acme-fintech",
  "concept": "waits-for-you",
  "phase": "draft",
  "brand_system": "clients/acme-fintech/brand-system.json",
  "defaults": {
    "model": "recraftv4"
  },
  "variants": {
    "asset": ["hero", "tile-01", "tile-02", "tile-03", "quote-01", "quote-02"]
  },
  "mockup_footer": "MOCKUP — For internal review only"
}
```

## Quick Reference

| Sub-task | Draft | Final | Notes |
|---|---|---|---|
| Hero / key visual | `recraftv4` | `flux-2-pro` | Flux lifts it to photoreal polish when a concept sticks |
| Product / audience tiles | `recraftv4` | `recraftv4_pro` if available, else hold at `recraftv4` | Usually fine at draft quality |
| Quote slides (readable headlines) | `ideogram-v3` | `ideogram-v3` | Only model that renders type reliably |
| Animated key visual for video pitch | `kling-v3-standard` | `kling-v3-pro` | See `motion-studio` skill for assembly |
| Throwaway concept tests (10+ options) | `gemini-3.1-flash-image` / `gemini-3.1-flash-image` | n/a | ~1 credit each |

## Procedure

- **Draft at 1/5 the cost of finals.** Approve concepts on cheap drafts, upgrade 2-3 winners only.
- **One concept per folder.** `pitches/concept-a/`, `pitches/concept-b/` — never mix.
- **Watermark external pitches.** Subtle `MOCKUP` footer on every image; use a deck/editor overlay, ImageMagick, or ffmpeg if available.
- **Reuse hero as tile input.** `gen-ai generate -m recraftv4 -i pitch/hero.webp --prompt "square crop variant"` keeps concept coherent.
- **Never show the client 6 options with 3 winners.** Curate to 2-3 strong concepts max before the pitch.
- **Keep filenames deck-ready.** `hero.webp`, `tile-01.webp` — not `gen_01H2XYZ.webp`.
- **Lock the prompt file per concept.** `pitches/<concept>/prompts.json` — when you win, production starts here.

## Pitfalls

- **Over-polished mockups** that the client expects you to deliver for pitch prices — add mockup footer + use draft models
- **Skipping ` — palette drift mid-manifest, deck looks incoherent
- **Cross-client prompt contamination** — don't copy prompts from another client's repo without stripping brand specifics
- **Using real faces / real brand marks** — rights issues; use descriptors ("a founder in their 30s") and generic marks
- **Missing rights documentation** — if the pitch wins, you'll need to reproduce these with clean provenance; save `results.json` per run
- **No `gen-ai pricing` before a 50-variant concept explosion** — pitch budgets don't absorb $40 surprises

## Verification

Run `gen-ai whoami` to confirm authentication, then re-run the failed command with `--debug`.

## Step 1: Plan the asset set

Present a table before spending:

| # | Asset | Concept | Model (draft → final) | Aspect | Notes |
|---|---|---|---|---|---|
| 1 | Hero | "Banking that waits" | `recraftv4` → `flux-2-pro` | 16:9 | Full-bleed, tagline overlay |
| 2 | Tile A | Product focus | `recraftv4` | 1:1 | Clean product shot |
| 3 | Tile B | Audience focus | `recraftv4` | 1:1 | Founder at desk, moody |
| 4 | Tile C | Benefit focus | `recraftv4` | 1:1 | Abstract benefit icon |
| 5 | Quote slide 1 | Customer voice | `ideogram-v3` | 16:9 | Readable headline type |
| 6 | Quote slide 2 | Founder voice | `ideogram-v3` | 16:9 | Readable headline type |

Estimate the manifest. If under $5, proceed. If over, cut the draft resolution or concept count.

## Step 2: Draft manifest + run

```bash
CLIENT="acme-fintech"
CONCEPT="waits-for-you"
OUT="clients/$CLIENT/pitches/$CONCEPT/drafts"
mkdir -p "$OUT"

cat > /tmp/pitch-$CLIENT-$CONCEPT.json <<EOF
{
  "defaults": {
    "model": "recraftv4"
  },
  "jobs": [
    { "id": "hero",       "prompt": "$CLIENT hero, concept: banking that waits for you — editorial, cinematic, headline overlay area left-third", "aspectRatio": "16:9" },
    { "id": "tile-01",    "prompt": "$CLIENT product tile — clean product render, brand palette",           "aspectRatio": "1:1" },
    { "id": "tile-02",    "prompt": "$CLIENT audience tile — founder at desk, moody lighting, documentary", "aspectRatio": "1:1" },
    { "id": "tile-03",    "prompt": "$CLIENT benefit tile — abstract waiting metaphor, minimal composition", "aspectRatio": "1:1" },
    { "id": "quote-01",   "prompt": "quote slide, large editorial headline 'Finally a bank that moves like I do.', brand palette, minimal background", "aspectRatio": "16:9", "model": "ideogram-v3" },
    { "id": "quote-02",   "prompt": "quote slide, large editorial headline 'Built for founders who don't wait.', brand palette, minimal background",   "aspectRatio": "16:9", "model": "ideogram-v3" }
  ]
}
EOF

gen-ai batch run /tmp/pitch-$CLIENT-$CONCEPT.json -c 4 -o "$OUT"
```

Review internally. For approved concepts, re-run the subset with `model: flux-2-pro` and output to `pitches/$CONCEPT/finals/`.

## Cost & time

| Phase | Spend | Time |
|---|---|---|
| Draft pass (6 assets, `recraftv4`) | ~$1-2 | 10-15 min |
| Final upgrade (2-3 winners to `flux-2-pro`) | ~$2-4 | 15-20 min |
| **Total pitch kit** | **~$5** | **~45 min end-to-end** |

Compare to production-phase cost after win: single campaign set with final photography-grade generations runs $20-100+.

## See also

- `workflows/agency-brand-scoping/` — lock direction + brand.md before pitching
- `workflows/agency-multi-brand-pack/` — retainer production across clients
- `workflows/agency-client-handoff/` — package final deliverables post-win
- `motion-studio` — if the pitch needs a sizzle reel
- `gen-ai-workflows.md` §9 (Pitch mockups) — source recipe
- `gen-ai-batch.md` — manifest + concurrency tuning
