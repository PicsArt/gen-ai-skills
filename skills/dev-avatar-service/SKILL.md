---
name: dev-avatar-service
description: Deterministic default-avatar generator per user.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: dev
    tags: [picsart, dev, developer-tools, automation]
---

# Avatar service

A service endpoint that returns a branded avatar for any user: photoreal, illustrated, or pixel, deterministic from a seed (user ID / email hash / initials). Built around a fallback hierarchy — real photo → upload → AI from initials → static default — with caching by seed so you pay once per user.

## When to Use

- New user signup where you need an immediate profile image.
- Comment systems or forums that default to gravatars.
- Team pages, directories, leaderboards without uploaded photos.
- Placeholder avatars during onboarding before the user picks one.
- Branded alternative to Gravatar / UI Avatars / DiceBear.
- Mock data for staging/demo environments.

Not for: deepfaking real people from a single photo (wrong tool + wrong ethics), or stylizing an already-great uploaded photo — let users keep their own.

## Prerequisites

Before building, ask (one message, 5 questions):

1. **Seed source**: user ID, email hash, username, initials? Is it stable forever?
2. **Style**: photoreal portrait, illustrated (Pixar/Disney-ish), flat vector, pixel art, claymorphic, monogram?
3. **Brand palette**: accent color for backgrounds + monogram fallbacks.
4. **Storage + cache**: S3/CDN + DB column, Picsart Drive URL, or KV key? TTL?
5. **Fallback chain**: photo → AI avatar → initials-on-color → default SVG? Order matters.

Skip if the user hands over a detailed brief.

## How to Run

1. **Decide the fallback hierarchy first.** This is the whole service:
   ```
   1. user.photo_url          → return as-is
   2. cache.get(seed)         → return stored AI avatar URL
   3. gen-ai generate         → store URL + return
   4. initials on brand color → SVG fallback (no credits)
   5. static /default.png     → last resort
   ```

2. **Estimate + validate model.**
   ```bash
   gen-ai models info recraftv4
   gen-ai pricing recraftv4
   gen-ai generate -m recraftv4 -p "illustrated avatar, seed abc123" \
     --aspect-ratio 1:1 --dry-run --debug
   ```

3. **Deterministic seed → prompt.** Hash the seed into stable attribute picks. Never inject `Math.random()` or timestamps.
   ```bash
   SEED="u_482c91"
   # Pick palette + mood from the seed, not from RNG
   HUE=$(printf "%s" "$SEED" | shasum | cut -c1-2)   # 0-255 from hash
   gen-ai generate -m recraftv4 \
     -p "illustrated profile avatar, round frame, abstract humanoid silhouette, HSL hue ${HUE}, friendly neutral expression, flat vector, centered composition, studio background" \
     --aspect-ratio 1:1 \
     --negative-prompt "text, watermark, letters, realistic face, specific person" \
     --save-to-drive --drive-folder avatars \
     --json --no-input | jq -r '.url'
   ```

4. **Cache the URL** (not the binary) keyed on the seed. Any store: Redis, KV, Postgres column, S3 + stable filename.

5. **Initials fallback (zero credits).** When gen-ai is down, rate-limited, or over budget — return an SVG built from the user's initials on a hue derived from the same seed. Users never see a broken image.
   ```ts
   const initials = name.split(' ').map(p => p[0]).slice(0, 2).join('').toUpperCase();
   const hue = parseInt(sha1(seed).slice(0, 2), 16);
   const svg = `<svg viewBox="0 0 64 64"><rect width="64" height="64" fill="hsl(${hue} 70% 45%)"/><text x="32" y="40" text-anchor="middle" font-size="28" fill="#fff" font-family="system-ui">${initials}</text></svg>`;
   ```

6. **Wire the endpoint.** `/avatar/:seed` → check photo → check cache → gen-ai → initials. 302 to CDN URL on success; inline SVG on fallback.

7. **Pre-warm the cache in batch** for existing users so your prod rollout doesn't hammer gen-ai live:
   ```bash
   gen-ai batch run avatars-backfill.json -c 4 -o ./avatars-out
   ```

## Quick Reference

Backfill 500 existing users:

```json
{
  "defaults": {
    "model": "recraftv4",
    "aspectRatio": "1:1",
    "negativePrompt": "text, watermark, letters, realistic face, specific person"
  },
  "jobs": [
    { "id": "u_482c91", "prompt": "illustrated profile avatar, round frame, flat vector, hue 42, friendly neutral, studio background" },
    { "id": "u_91ac3b", "prompt": "illustrated profile avatar, round frame, flat vector, hue 128, calm expression, studio background" },
    { "id": "u_7de119", "prompt": "illustrated profile avatar, round frame, flat vector, hue 201, warm smile, studio background" }
  ]
}
```

Output lands at `./avatars-out/<user-id>.webp` — upload to your CDN under the same key. `results.json` becomes the seed → URL lookup table.

## Quick Reference

| Sub-task | Model | Why |
|----------|-------|-----|
| Illustrated / vector / flat avatars | `recraftv4` | Clean, consistent, cheap — ideal default |
| Photoreal portrait (synthetic, generic person) | `flux-2-pro` | Best faces; use with generic descriptors only |
| Pixel-art avatars | `recraftv4` with pixel-style prompt | Lowest credits, stylistic control |
| Stylize an uploaded real photo (opt-in) | `flux-kontext-pro` + `-i photo.jpg` | Edit model preserves identity |
| Cheap draft / style exploration | `gemini-3.1-flash-image` | Lowest per-call cost |
| Identity-locked variants across sizes | `ideogram-character` + `-i master.png` | Same face across multiple avatars |

Verify live IDs with `gen-ai models --mode image`.

## Procedure

- **Determinism = cacheability.** Derive every variable attribute (hue, pose, expression) from a hash of the seed. Same seed → same prompt → same image → one credit forever.
- **Version the prompt template.** Bump `V=2` in the cache key when you restyle; old avatars age out, new ones regenerate on demand.
- **Fallback is not optional.** Initials-on-hue SVG must always work. Never let the UI render a broken avatar because gen-ai 429'd.
- **Negative prompt matters.** Always exclude `text, watermark, letters, realistic face of specific person` — avatars must not resemble real celebrities or render accidental copy.
- **Don't generate on every page load.** Generate once per seed, cache forever (or until template version bump). A viral signup spike must not trigger a gen-ai spike.
- **Use Drive for storage.** `--save-to-drive --drive-folder avatars` gives a stable CDN URL with no extra infra.
- **Pre-warm before launch.** Batch-generate for existing users; don't migrate live traffic onto a cold cache.
- **Respect user uploads.** If the user has uploaded a real photo, return that — never override. AI avatars are for *missing* photos only.
- **Rate-limit at the edge.** Cap gen-ai calls per IP per hour. A bot probing `/avatar/:random` can burn your credit budget in minutes.

## Pitfalls

| Pitfall | Fix |
|---------|-----|
| Regenerated avatar looks different on every refresh | Non-deterministic prompt — hash the seed, derive attributes, no RNG/timestamps |
| Cache never invalidates after restyle | Version the prompt template (`V=3` in the cache key) |
| AI renders real-looking faces resembling celebrities | Add `negativePrompt: "realistic face of specific person, celebrity, known individual"` |
| Text or watermarks appear in the avatar | Add `negativePrompt: "text, watermark, letters, logos"` |
| Bot traffic burns credit budget | Rate-limit per IP; allow only authed users to hit the generator; fallback to initials for anons |
| Gen-ai 429s cause broken avatar UI | SVG initials fallback must be the last step in the chain |
| Batch backfill half-fails | `gen-ai batch resume <out>` retries only failures |
| Different avatar style across the app | Commit the prompt template; never let callers pass raw prompts |

## Verification

Run `gen-ai whoami` to confirm authentication, then re-run the failed command with `--debug`.

## Cost & time

| Task | Credits | Time |
|------|---------|------|
| 1 avatar (Recraft V4, illustrated) | 1-2 | ~4-8s |
| 1 avatar (Flux 2 Pro, photoreal) | 3-5 | ~10-15s |
| 1 avatar (Gemini 3.1 Flash, draft) | 1 | ~3-5s |
| Initials SVG fallback | 0 | <1ms |
| Cache read (KV/Redis hit) | 0 | ~2-5ms |
| Batch of 500 at concurrency 4 | ~750-1000 | ~15-20 min |

In steady state, expect >99% cache hit rate — near-zero ongoing cost.

## See also

- `gen-ai-use.md` — CLI reference, auth, scripting with `--json --no-input` / `jq`
- `gen-ai-batch.md` — manifest shapes, batch resume, rate-limit strategy, Cloudflare Worker pattern
- `gen-ai-workflows.md` — Workflow 6 (headshot studio) for stylizing uploaded photos
- `dev-og-image-service` — same caching + determinism patterns for OG cards
