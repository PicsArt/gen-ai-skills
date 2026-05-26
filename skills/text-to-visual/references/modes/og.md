
# OG image service

A per-URL Open Graph image service: given a post title + category, emit a branded 1200×630 image URL for `<meta property="og:image">`. Same input → same image → cache-friendly. Deploys as a Vercel / Cloudflare / Next.js route handler.

## When to Use

- Blog or docs site needs OG/Twitter cards generated from post title + category.
- Marketing LPs where every slug gets its own social card.
- Changelog or release pages that auto-refresh OG on publish.
- PR preview deployments that need per-branch social cards.
- Replacing a hand-maintained `/og/*.png` folder with an endpoint.

Do not use for heavy layout-critical branding (type-accurate logos, small legal text) — use `satori`/`@vercel/og` for those. Use this skill for the visual/editorial layer.

## Prerequisites

Before scaffolding, ask (one message, 5 questions):

1. **Title + category source**: URL param, frontmatter, CMS field?
2. **Brand tokens**: primary color, accent, font family, logo URL — or a `brand.md` path.
3. **Platform**: Next.js App Router, Vercel Edge, Cloudflare Worker, Express, static CI job?
4. **Cache target**: CDN (Vercel KV / CF KV), S3 + CloudFront, or Picsart Drive URL directly?
5. **Fallback**: static default image path for when gen-ai fails or is rate-limited?

Skip if the user provides a full brief.

## How to Run

1. **Validate model + estimate cost once.**
   ```bash
   gen-ai models info ideogram-v3
   gen-ai pricing ideogram-v3
   gen-ai generate -m ideogram-v3 -p "test poster, headline: 'Hello World'" \
     --aspect-ratio 1200x630 --dry-run --debug
   ```

2. **Scaffold the endpoint.** Route handler takes `?title=...&category=...`, normalizes to a cache key (`sha1(title+category+version)`), checks KV, else calls gen-ai.

3. **Generate (deterministic cache key).** Prompt must be a pure function of inputs. No `Date.now()`, no random style words.
   ```bash
   TITLE="Shipping the CLI"
   CATEGORY="engineering"
   gen-ai generate -m ideogram-v3 \
     -p "editorial poster, headline reads: \"$TITLE\", subtitle: \"$CATEGORY\", dark #0D0A1F background, magenta #FF006E accent, high contrast, centered typography" \
     --aspect-ratio 1200x630 \
     --json --no-input | jq -r '.url'
   ```

4. **Cache the URL** (not the image) in KV under the hash. TTL 30 days. Edge then 302-redirects to the CDN URL.

5. **Wire CI regeneration.** On every merge that touches `content/**/*.md`, re-emit the cards for changed posts. Use `gen-ai batch resume <output-dir>` so unchanged posts skip.

6. **Set up CI auth for headless runs.**
   ```bash
   export PICSART_ACCESS_TOKEN="${{ secrets.PICSART_TOKEN }}"
   export PICSART_USER_ID="${{ secrets.PICSART_USER_ID }}"
   ```

## Quick Reference

For bulk regeneration at build time:

```json
{
  "defaults": {
    "model": "ideogram-v3",
    "aspectRatio": "1200x630"
  },
  "jobs": [
    { "id": "post-shipping-cli",     "prompt": "editorial poster, headline: \"Shipping the CLI\", subtitle: \"engineering\", dark #0D0A1F, magenta #FF006E accent" },
    { "id": "post-og-service",       "prompt": "editorial poster, headline: \"OG at the edge\", subtitle: \"infra\", dark #0D0A1F, cyan #00F0FF accent" },
    { "id": "post-launch-week-2026", "prompt": "editorial poster, headline: \"Launch Week 2026\", subtitle: \"product\", dark #0D0A1F, yellow #FFBE0B accent" }
  ]
}
```

Run with `gen-ai batch run og-manifest.json -c 4 -o ./public/og` — each post becomes `public/og/post-*.webp`.

## Quick Reference

| Sub-task | Model | Why |
|----------|-------|-----|
| Typography-driven OG (headline as the hero) | `ideogram-v3` | Best-in-class in-image text rendering |
| Abstract/editorial background, text added client-side | `flux-2-pro` | Rich textures, no text required |
| Fast/cheap drafts or preview-branch OGs | `gemini-3.1-flash-image` | Lowest credit cost |
| Product screenshot as OG (with treatment) | `flux-kontext-pro` + `-i screenshot.png` | Edit model, preserves UI |

Always confirm with `gen-ai models --mode image` — IDs shift.

## Procedure

- **Deterministic prompts.** Same title → byte-identical prompt → cacheable hash. Never inject timestamps.
- **Version the prompt template.** Bump a `V=3` constant in the hash when you restyle the card; old URLs keep working.
- **Truncate long titles** at ~70 chars with ellipsis before injecting into the prompt. Ideogram v3 handles ~8-12 words cleanly; beyond that, text breaks.
- **Escape quotes and newlines** in the title before interpolation — `jq -R`, `printf %q`, or a proper template lib.
- **Keep CI cheap.** Gate regeneration on the post's frontmatter hash changing. Don't regenerate every build.
- **Store Drive URLs, not blobs.** `--save-to-drive --drive-folder OG-Cards` gives a stable CDN URL you can redirect to.
- **Always ship a fallback.** If gen-ai returns 429 / 5xx, serve a static `/og/default.png`. Never block page render on gen-ai.
- **Measure once, cache forever.** Run `gen-ai pricing ideogram-v3` before the first batch; one post = ~2-4 credits.

## Pitfalls

| Pitfall | Fix |
|---------|-----|
| Cache never invalidates when you restyle the card | Version the prompt template constant (`V=3`); old hashes naturally age out of KV |
| Long titles render as `Lorem ipsum…` with unreadable fallback text | Truncate at 70 chars before the prompt; pick `ideogram-v3` for text fidelity |
| Different URL per regeneration breaks social re-crawls | Use `--save-to-drive` + a stable filename; redirect to that, not the raw generation URL |
| Quotes or emojis in titles blow up the shell command | Pass title via `--prompt-file` or JSON stdin, never raw interpolation |
| CI regenerates every build, burns credits | Hash post frontmatter; skip on unchanged hash via `gen-ai batch resume <output-dir>` |
| Rate-limit storms on launch-week traffic spikes | Pre-generate all cards at build time; serve from static/KV, never generate on request |

## Verification

Run `gen-ai whoami` to confirm authentication, then re-run the failed command with `--debug`.

## Cost & time

| Task | Credits | Time |
|------|---------|------|
| 1 OG card (Ideogram v3, 1200×630) | 2-4 | ~8-12s |
| 1 OG card (Flux 2 Pro, then SVG text overlay) | 4-6 | ~10-14s |
| 1 OG card (Gemini 3.1 Flash, draft) | 1-2 | ~4-6s |
| Batch of 50 posts at concurrency 4 | ~150 | ~3 min |
| Cloudflare KV read (cache hit) | 0 | ~5ms |

Expect ~95%+ cache hit rate in steady state.

## See also

- `gen-ai-use.md` — full CLI reference, flags, auth, troubleshooting
- `gen-ai-batch.md` — manifest shapes, CI/CD recipes, Cloudflare Worker example
- `gen-ai-workflows.md` — Workflow 4 (OG image service) end-to-end
- `dev-screenshot-beautifier` — if your OG is a treated product screenshot
