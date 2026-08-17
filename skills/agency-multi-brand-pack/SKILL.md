---
name: agency-multi-brand-pack
description: Per-client asset templates scoped by workspace.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: agency
    tags: [picsart, agency, creative, client-work]
---

# Agency multi-brand pack

Run generations for N retainer clients in one coordinated pass — each client's output strictly namespaced, each job gated by that client's brand rules, every run audit-ready for legal and billing.

**N clients × M templates per client → one batch, zero cross-contamination.** For agencies running weekly/monthly creative cycles across a client portfolio.

## When to Use

- Weekly/monthly retainer refresh across multiple retainer clients
- Portfolio-wide seasonal re-skin (e.g. holiday refresh for all 8 retainer brands in one batch)
- Multi-client pitch week where each pitch needs its own branded mockup set
- Audit-ready production runs where finance/legal need a per-client spend breakdown
- Any agency workflow where "run the same pipeline for every client, with their rules" is the task

**Do not use for** single-client deep-production work — drop to `agency-pitch-mockups` or a client-specific workflow. Multi-brand is for portfolio parallelism.

## Prerequisites

Ask the user (one message):

1. **Client list** — slugs of clients in scope (e.g. `acme-fintech`, `zest-retail`, `nova-travel`). Each must have a locked `brand-system.json`.
2. **Template set per client** — same across all clients (hero + 3 social + OG) or does each client have a different deliverable?
3. **This week's theme / brief** — one brief that gets re-expressed per client (e.g. "Q2 product refresh") or fully independent briefs per client?
4. **Output destination** — Drive folder per client? Dropbox / S3? Internal repo path?
5. **Billing scope** — tag each job with `client:<slug>` so per-client spend can be pulled from `gen-ai history`
6. **Concurrency ceiling** — default 4, raise to 8 if clients all have premium rate limits

If any client in the list lacks `brand-system.json` or `brand.md`, stop and run `agency-brand-scoping` for that client first — do not batch-generate without locked brand files.

## How to Run

```
1. VERIFY BRANDS  → every client in scope has clients/<slug>/brand.md + brand-system.json
2. SCAFFOLD       → build per-client manifest fragments, merge into one master manifest
3. ESTIMATE       → gen-ai batch run <manifest.json> --dry-run + estimate; break into smaller batches if > $20
4. RUN            → `gen-ai batch run <manifest.json>` with client names in job IDs and a resume-ready output dir
5. VERIFY         → per-client output folders populated; cross-check any NULLs in results.json
6. AUDIT          → export per-client spend + asset list for billing
7. DELIVER        → folder per client, approved files uploaded or linked in the retainer channel
```

**Rules:**

- **One folder per client.** `out/<slug>/...` — never a shared output folder where filenames can collide.
- **One brand context per job, not per batch** — each job prompt should include the relevant client `brand.md` constraints. Batch-level generic prompts are the biggest source of cross-contamination.
- **Use stable job IDs.** Put client or campaign names in each `id` so downloaded files and `results.json` remain easy to group.
- **Resume with `gen-ai batch resume <output-dir>` by default.** `gen-ai batch resume <output-dir>` so mid-run failures don't cost the completed half.

## Quick Reference

```json
{
  "batch_kind": "multi-brand-pack",
  "week": "2026-04-22",
  "defaults": { "model": "recraftv4", "aspectRatio": "1:1" },
  "clients": [
    { "slug": "acme-fintech", "templates": ["hero", "social-1", "og"] },
    { "slug": "zest-retail",  "templates": ["hero", "social-1", "og"] }
  ]
}
```

A scaffolding script expands this into the flat `jobs[]` manifest the CLI expects. Keep the expanded manifest checked in under `out/retainer-<date>/manifest.json` for reproducibility.

## Quick Reference

| Sub-task | Model | Notes |
|---|---|---|
| Per-client hero (default) | `recraftv4` | Design-forward, respects brand palette |
| Per-client hero (photo-led brands) | `flux-2-pro` | Override at the job level for photo-heavy clients |
| Social tiles (1:1, 9:16) | `recraftv4` | Same brand rules, cheaper |
| OG / readable-headline slides | `ideogram-v3` | Only reliable text rendering |
| Background replacement on product shots | `recraftv3-replace-bg` | For ecomm retainers |
| Video cuts per brand | `kling-v3-standard` (draft) / `kling-v3-pro` (final) | Per-client concurrency 2 |

## Procedure

- **One brand file per client, no shared "agency-style" rules.** Each client pays for their own brand rigor.
- **Namespace every output by slug** — `out/<slug>/`, `drive:retainer-<date>/<slug>/`, `results.json` job IDs. Redundant is good.
- **Script the manifest.** For > 3 clients, a Node/Python scaffold that iterates `clients[]` × `templates[]` beats copy-paste errors.
- **Estimate before every run.** Multi-brand batches cross the $20 threshold easily — pause and confirm.
- **Persist `results.json` to the repo.** Audit trail for legal, billing input, and reproducibility.
- **Keep a per-client prompt library** at `clients/<slug>/prompts/` — manifest references these, edits propagate.
- **review brand-sensitive output.** `` — better a missing asset than a mis-branded one.
- **Weekly cadence deserves a cron** + Slack webhook on completion; see `gen-ai-batch.md` §CI recipes.

## Pitfalls

- **Brand cross-contamination** — missing `rules` on a single job, entire batch suspect. Fix: per-job `rules`, not batch-level.
- **Filename collisions** without slug prefixes — client B's `hero.webp` overwrites client A's.
- **Running without `gen-ai batch resume <output-dir>`** on a 100-job batch — one provider hiccup costs the whole run.
- **Shared Drive folder** — client A sees client B's folder, NDA breach.
- **Tagless jobs** — can't produce per-client billing; finance asks, you can't answer.
- **Flagship models applied everywhere** — $40 weekly batch instead of $15. Draft-then-upgrade selectively.

## Verification

Run `gen-ai whoami` to confirm authentication, then re-run the failed command with `--debug`.

## Step 1: Verify brands + build manifest

```bash
CLIENTS=("acme-fintech" "zest-retail" "nova-travel")
WEEK=$(date +%Y-%m-%d)

# Sanity check: every client has a brand file
for c in "${CLIENTS[@]}"; do
  test -f "clients/$c/brand.md" || { echo "Missing brand.md for $c"; exit 1; }
done
```

## Step 2: Per-client manifest fragments, merged

```bash
cat > /tmp/multi-brand-$WEEK.json <<'EOF'
{
  "defaults": { "model": "recraftv4", "aspectRatio": "1:1" },
  "jobs": [
    { "id": "acme-fintech/hero",    "prompt": "acme-fintech Q2 hero — editorial, restrained", "aspectRatio": "16:9" },
    { "id": "acme-fintech/og",      "prompt": "acme-fintech OG — headline: Q2 launch", "aspectRatio": "1200x630", "model": "ideogram-v3" },
    { "id": "zest-retail/hero",     "prompt": "zest-retail Q2 hero — playful, bold color", "aspectRatio": "16:9" },
    { "id": "nova-travel/hero",     "prompt": "nova-travel Q2 hero — cinematic wide", "aspectRatio": "16:9", "model": "flux-2-pro" }
  ]
}
EOF

gen-ai batch run /tmp/multi-brand-$WEEK.json --dry-run
gen-ai batch run /tmp/multi-brand-$WEEK.json -c 4 -o "out/retainer-$WEEK"
```

The `/` in each job `id` creates the per-client subfolder automatically — outputs land at `out/retainer-<date>/<client-slug>/<asset>.webp` plus `results.json`.

## Step 3: Per-client audit + delivery

```bash
# Per-client completion breakdown from results.json
node -e '
  const r = require("./out/retainer-2026-04-22/results.json");
  const by = {};
  for (const j of r.jobs) {
    const c = j.id.split("/")[0];
    by[c] ||= { completed: 0, failed: 0 };
    by[c][j.status] = (by[c][j.status] || 0) + 1;
  }
  console.table(by);
'
```

Create an archive sub-folder `retainer-$WEEK/<client-slug>/` per client, drop a summary with asset list + estimated spend from `gen-ai pricing`. Share only the per-client folder link — never the master folder.

## Cost & time

| Phase | Typical spend | Typical time |
|---|---|---|
| Scoping (per new client, one-time) | ~$1 | 30 min |
| Production (weekly retainer, 8 clients × 4 assets) | $15-30 | 20-40 min batch + review |
| Flagship-model upgrade pass (2-3 hero upgrades) | $5-10 | 10-15 min |

Per-client weekly spend should be trackable from `results.json` — if it isn't, the tagging is broken.

## See also

- `workflows/agency-brand-scoping/` — required prerequisite per client
- `workflows/agency-pitch-mockups/` — per-client pitch variant
- `workflows/agency-client-handoff/` — package retainer history at engagement end
- `gen-ai-batch.md` — concurrency, `gen-ai batch resume <output-dir>`, audit recipes
