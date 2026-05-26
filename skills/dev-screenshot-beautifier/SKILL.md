---
name: dev-screenshot-beautifier
description: Polish raw screenshots into LP-ready heroes.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: dev
    tags: [picsart, dev, developer-tools, automation]
---

# Screenshot beautifier

A polish pipeline that takes a raw UI screenshot (localhost capture, production screen grab, mobile viewport) and turns it into a blog-ready, changelog-ready, doc-ready hero: device-framed, drop-shadowed, on a gradient backdrop, dark-mode matched.

## When to Use

- Release notes / changelog entries that need a hero image per ship.
- Blog posts and docs that reference a product screen.
- PR descriptions where a raw screenshot looks amateurish.
- Twitter/LinkedIn launch posts where the screenshot is the creative.
- Dark-mode and light-mode site variants that each need their own polished hero.
- PM/eng team members who don't have a designer on call.

Not for: generating UI that doesn't exist (use Figma or a mockup tool), or replacing real content with fake text (prefer annotation/blurring).

## Prerequisites

Before processing, ask (one message, 5 questions):

1. **Raw screenshot path** — PNG preferred over JPEG for clean edges.
2. **Device frame**: browser chrome (Chrome/Safari/Arc), iPhone bezel, Android, MacBook, iPad, or none (just soft shadow)?
3. **Background vibe**: soft studio gradient, brand palette, dark rim-lit surface, glassmorphic, matte neutral?
4. **Output target + aspect**: blog hero (16:9), Twitter card (1200×675), LinkedIn (1200×627), mobile story (9:16), doc inline (3:2)?
5. **Dark mode variant needed?** If yes, generate a paired dark version.

Skip if the user hands over a detailed brief.

## How to Run

1. **Estimate the background swap cost.**
   ```bash
   gen-ai models info recraftv3-replace-bg
   gen-ai pricing recraftv3-replace-bg
   ```

2. **Option A — Background swap only** (UI stays pixel-exact, just drop on a new surface). Use this when the screenshot itself is final.
   ```bash
   gen-ai change-bg \
     -i ./raw.png \
     -p "soft studio gradient, magenta #FF006E to deep purple #0D0A1F, subtle rim light from top-left, very slight film grain" \
     --download ./out
   ```

3. **Option B — Full edit** (add device frame + shadow + reflection in one pass). Use when you want the model to re-composite.
   ```bash
   gen-ai generate -m flux-kontext-pro \
     -i ./raw.png \
     -p "product screenshot of the provided UI, placed inside a MacBook Pro 14 bezel, floating slightly tilted at 4° right, soft drop shadow below, glassy reflection underneath, matte charcoal background, centered composition, 16:9" \
     --aspect-ratio 16:9 \
     --download ./out
   ```

4. **Option C — Background only, composite locally** (maximum UI fidelity, optional). Use only when local compositing tools are available; otherwise use Option A or B. Generate a backdrop, then overlay the raw PNG with `sharp`, browser canvas/CSS, or ffmpeg if already installed.
   ```bash
   gen-ai generate -m flux-2-pro \
     -p "abstract studio backdrop, soft magenta-to-purple gradient, subtle light orb top-left, empty center composition, 1920×1080" \
     --aspect-ratio 16:9 \
     --download ./out/bg
   # Then locally: sharp, browser canvas/CSS, or optional ffmpeg composite with device frame + shadow
   ```

5. **Dark-mode paired variant.**
   ```bash
   gen-ai generate -m flux-kontext-pro \
     -i ./out/result.png \
     -p "same composition, re-lit for dark mode: deep #0D0A1F background, teal #00F0FF accent rim light, subtle glow behind the device, keep UI content identical" \
     --aspect-ratio 16:9 \
     --download ./out/dark
   ```

6. **Verify.** Open side by side with the raw. UI text must still be readable. No melted edges on the bezel. No duplicated chrome.

## Quick Reference

Batch-beautify all screenshots for a release:

```json
{
  "defaults": {
    "model": "flux-kontext-pro",
    "aspectRatio": "16:9"
  },
  "jobs": [
    { "id": "hero-dashboard",       "imageUrls": ["./raw/dashboard.png"],  "prompt": "MacBook Pro 14 bezel, soft drop shadow, magenta-to-purple studio gradient, slight 3° tilt right" },
    { "id": "hero-dashboard-dark",  "imageUrls": ["./raw/dashboard.png"],  "prompt": "MacBook Pro 14 bezel, deep #0D0A1F backdrop, teal rim light, subtle glow, identical UI content" },
    { "id": "hero-mobile-timer",    "imageUrls": ["./raw/timer.png"],      "prompt": "iPhone 16 Pro bezel, portrait, floating with soft shadow, gradient backdrop", "aspectRatio": "9:16" },
    { "id": "hero-settings",        "imageUrls": ["./raw/settings.png"],   "prompt": "Browser chrome (Arc-style), soft studio gradient, subtle reflection under window" }
  ]
}
```

Run with `gen-ai batch run screenshots.json -c 3 -o ./out/beautified`.

## Quick Reference

| Sub-task | Model | Why |
|----------|-------|-----|
| Background swap only, preserve UI pixel-exact | `picsart-change-bg` | Cleanest edge extraction on UI shapes |
| Background removal (transparent PNG out) | `picsart-remove-bg` | Fast, reliable, preserves anti-aliasing |
| Device frame + shadow + reflection (full recomposite) | `flux-kontext-pro` | Best edit model, follows `-i` reference |
| Standalone backdrop for local compositing | `flux-2-pro` | Richest textures + lighting |
| Quick draft while choosing direction | `gemini-3.1-flash-image` | Lowest credits |
| Upscale final export to print | `topaz-upscale-image` | 2-4× with UI-safe edges |

Verify with `gen-ai models --mode image`.

## Procedure

- **Always input PNG, not JPEG.** JPEG compression artifacts compound when the model recomposites.
- **Preserve the UI, don't let the model redraw it.** If text gets rewritten, you chose the wrong approach — switch from Option B (full edit) to Option C (local composite).
- **Lock palette per project.** Save `brand.md` with hex values; pass ` so backdrops don't drift between posts.
- **Device frames should match reality.** Use the actual device the user was on. Shipping an Android screenshot inside an iPhone bezel is a credibility tell.
- **One tilt, not five.** 3-5° of rotation reads premium; 15°+ reads stock-photo.
- **Dark variant off the light variant, not off raw.** Pass the already-beautified output as `-i` — shadows, tilt, and bezel stay identical, only lighting changes.
- **Don't use `--save-to-drive` for sensitive screenshots** (pre-launch UI, customer data). Keep local or use `--no-save-to-drive`.
- **Blur before beautifying** anything with real user data. The model will happily preserve a leaked email — do the blur pass first.

## Pitfalls

| Pitfall | Fix |
|---------|-----|
| UI text is rewritten / garbled after edit | Use Option A (bg swap) or Option C (local composite) — not Option B |
| Device bezel looks melted at corners | Drop Flux Kontext Pro; use remove-bg + local PNG composite with a real bezel asset |
| Perspective is wrong (tilted + fish-eye) | Prompt explicitly "flat, frontal, no perspective distortion" — or composite locally |
| Dark variant shifts UI colors | Pass the light variant as `-i`, prompt "keep UI content identical, re-light background only" |
| Screenshot contains leaked customer data | Blur/redact in the raw PNG BEFORE running gen-ai |
| Anti-aliasing fringe after bg removal | Use `picsart-remove-bg` with PNG input; avoid JPEG sources |
| Gradient backdrop clashes with UI accent color | Pull the UI's accent into the prompt palette; match rather than contrast |

## Verification

Run `gen-ai whoami` to confirm authentication, then re-run the failed command with `--debug`.

## Cost & time

| Task | Credits | Time |
|------|---------|------|
| Background swap (picsart-change-bg) | 1-2 | ~4-8s |
| Background removal (picsart-remove-bg) | 1 | ~3-5s |
| Full edit with device frame (flux-kontext-pro) | 3-6 | ~10-18s |
| Standalone backdrop (flux-2-pro) | 3-5 | ~10-15s |
| Paired dark-mode variant | +3-6 | +10-18s |
| Upscale to 4K (topaz-upscale-image) | 2-4 | ~15-30s |
| **Typical blog hero (light + dark, framed)** | **~10-15** | **~30-45s** |

## See also

- `gen-ai-use.md` — full CLI reference, remove-bg, change-bg, enhance flags
- `gen-ai-batch.md` — batching multiple screenshots, `gen-ai batch resume <output-dir>` for partial runs
- `gen-ai-workflows.md` — Workflow 1 (blog-to-visuals) for the full post asset set
- `dev-og-image-service` — turn the beautified hero into a per-URL OG card
- `dev-app-assets` — App Store screenshot framing at scale
