---
name: dev-app-assets
description: Generate icons, empty states, onboarding for apps.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: dev
    tags: [picsart, dev, developer-tools, automation]
---

# App assets

A one-shot pipeline that turns a single app idea into the full store-ready asset pack: app icon across every required size, splash screen, device-framed App Store / Play Store screenshots, and feature graphic. One visual language, one style reference, every platform.

## When to Use

- Launching an iOS / Android / cross-platform app and need the full asset set before submission.
- Rebranding an existing app: re-render all icons + store art in a new style.
- Indie / hackathon ships where you'd otherwise hand-crop 30 icon sizes.
- Watch + phone + tablet variants that must feel like one product.
- Regenerating localized App Store screenshots for new markets.

Not for: motion assets (use `motion-studio`), marketing LP heroes (`dev-screenshot-beautifier`), or final pixel-perfect logo work (hand off to a designer).

## Prerequisites

Ask before generating (one message, 6 questions):

1. **App name + one-line concept** (e.g. "Rally — a focus timer for ADHD brains").
2. **Style direction**: flat, gradient, claymorphic, glass, pixel? Any existing logo or style exemplar to reference?
3. **Brand tokens**: primary + accent colors (hex), typography, mood keywords.
4. **Platforms**: iOS, Android, watchOS, macOS, web PWA — which sizes do you need?
5. **Device frames for screenshots**: iPhone 16 Pro, Pixel 9, Apple Watch, iPad Pro? Portrait or landscape?
6. **Deliverable folder**: where should the pack land (e.g. `./app-assets/`)?

## How to Run

1. **Estimate + validate the master style.**
   ```bash
   gen-ai models info flux-2-pro
   gen-ai generate -m flux-2-pro -p "<style prompt>" --aspect-ratio 1:1 --dry-run --debug
   ```

2. **Generate the master icon (1024×1024, the source-of-truth).** This is what every downstream size gets derived from — make it right once.
   ```bash
   gen-ai generate -m flux-2-pro \
     -p "app icon, 'Rally' focus timer, minimalist gradient, magenta #FF006E to purple #8338EC, soft shadow, rounded-rect canvas, centered glyph, hyperreal studio render" \
     --aspect-ratio 1:1 \
     --download ./app-assets/icon-master \
     --save-to-drive --drive-folder "rally-app-assets"
   ```
   Review visually. Regenerate until approved — do NOT batch before the master is locked.

3. **Derive all icon sizes locally** (no gen-ai credits). Icons are deterministic resizes of the master.
   ```bash
   MASTER=./app-assets/icon-master/result.png
   # iOS sizes (App Store 1024, iPhone 60@2x/@3x, iPad, Settings, Spotlight, Notification)
   for size in 1024 180 120 167 152 76 87 80 58 40 120 87 58; do
     sips -z $size $size "$MASTER" --out "./app-assets/ios/icon-${size}.png"
   done
   # Android (mipmap-mdpi … xxxhdpi: 48, 72, 96, 144, 192, 512)
   for size in 48 72 96 144 192 512; do
     sips -z $size $size "$MASTER" --out "./app-assets/android/ic_launcher-${size}.png"
   done
   # watchOS (24, 27.5, 29, 40, 44, 50, 86, 98, 108)
   for size in 48 55 58 80 88 100 172 196 216; do
     sips -z $size $size "$MASTER" --out "./app-assets/watch/icon-${size}.png"
   done
   ```

4. **Generate the splash / launch screen** off the same master (keep visual DNA).
   ```bash
   gen-ai generate -m flux-kontext-pro \
     -i ./app-assets/icon-master/result.png \
     -p "splash screen, centered app icon on a vertical gradient, same magenta-to-purple palette, 9:19.5 mobile canvas, calm negative space" \
     --aspect-ratio 9:16 \
     --download ./app-assets/splash
   ```

5. **Batch the App Store screenshots** — one manifest per platform, framed separately.
   ```bash
   gen-ai batch run app-store-shots.json -c 4 -o ./app-assets/screenshots
   ```
   Then wrap with device frames using `dev-screenshot-beautifier` (see that skill) or a tool like `fastlane frameit`.

6. **Feature graphic (Play Store) + promo (App Store).**
   ```bash
   gen-ai generate -m flux-2-pro \
     -p "Play Store feature graphic, 'Rally' wordmark, 1024×500, same gradient, key benefit 'Focus in bursts'" \
     --aspect-ratio 1024x500 \
     --download ./app-assets/store
   ```

7. **Verify mask alignment.** iOS auto-masks to a rounded-rect; content must sit inside the safe zone or you'll get clipped corners. Preview at 60×60 — if the glyph bleeds, regenerate with `centered glyph, 15% padding all sides` in the prompt.

## Quick Reference

App Store screenshots (6.9" iPhone, 1290×2796, 5 screens):

```json
{
  "defaults": {
    "model": "flux-kontext-pro",
    "aspectRatio": "1290x2796",
    "imageUrls": ["./app-assets/icon-master/result.png"]
  },
  "jobs": [
    { "id": "screen-1-hero",      "prompt": "iPhone app UI mockup, 'Rally' focus timer home screen, large timer dial, magenta-to-purple gradient, tagline 'Focus in bursts' above the fold" },
    { "id": "screen-2-session",   "prompt": "iPhone app UI mockup, active focus session, glowing timer ring at 00:14:23, calm dark background" },
    { "id": "screen-3-stats",     "prompt": "iPhone app UI mockup, weekly focus stats bar chart, magenta bars, caption 'You focused 12h this week'" },
    { "id": "screen-4-streak",    "prompt": "iPhone app UI mockup, 14-day streak celebration, confetti, flame icon, headline 'Day 14 unlocked'" },
    { "id": "screen-5-settings",  "prompt": "iPhone app UI mockup, settings screen, clean list rows, same palette, tagline 'Built for ADHD brains'" }
  ]
}
```

## Quick Reference

| Sub-task | Model | Why |
|----------|-------|-----|
| Master app icon (hero render) | `flux-2-pro` | Best photoreal gradients, clean glyphs |
| Icon style variations from master | `flux-kontext-pro` + `-i master.png` | Preserves identity, varies background/treatment |
| Vector-style / flat icons | `recraftv4` | Clean shapes, flat color, tight edges |
| App Store screenshot mockups with readable UI text | `ideogram-v3` | Renders in-image copy cleanly |
| Splash / onboarding illustration with app icon reference | `flux-kontext-pro` + `-i` | Keeps visual DNA across the set |
| Cheap drafts while style-hunting | `gemini-3.1-flash-image` | Lowest credits |

Confirm IDs with `gen-ai models --mode image`.

## Procedure

- **Lock the master before batching.** One great 1024 is worth 30 mediocre variants. Never run the icon-size loop until the master is approved.
- **Resize locally, don't regenerate.** `sips` / `ImageMagick` / `sharp` for all sizes below the master. AI-regenerating each size produces drift.
- **Reference the master for every downstream asset.** `-i icon-master.png` into splash, screenshots, feature graphic. Shared visual DNA.
- **Respect iOS mask.** iOS auto-clips to a superellipse at the OS level; keep the glyph within 80% of the canvas, centered. Test at 60×60 before committing.
- **Android adaptive icons** need separate foreground + background layers (108×108 with 72×72 safe zone). Generate foreground transparent, background as a solid/gradient tile.
- **Save everything to Drive.** `--drive-folder "<app>-assets"` — so a designer can review in one place without cloning your repo.
- **Version the style prompt.** Store the exact prompt in `app-assets/STYLE.md`. Future "just one more screenshot" requests stay consistent.
- **Don't re-render on every CI run.** Assets are release artifacts — commit them, or generate once and upload to your asset pipeline.

## Pitfalls

| Pitfall | Fix |
|---------|-----|
| Icon clipped at corners after iOS mask | Re-prompt with `centered glyph, 15% safe-zone padding`, regenerate master |
| Android adaptive icon background bleeds through | Generate foreground with transparent bg (`transparent background, isolated glyph`); layer manually |
| Screenshots look inconsistent across 5 shots | Always reference the master icon with `-i` on every screenshot job |
| Store screenshot copy is gibberish | Switch the screenshot model to `ideogram-v3` — it renders text |
| Watch icon glyph unreadable at 48px | Increase stroke weight + contrast in the master; re-derive |
| Drift between iOS and Android variants | Use one master image, resize locally — do not regenerate per platform |
| Style prompts forgotten 3 months later for "one more screen" | Commit `STYLE.md` with the exact prompt + palette |

## Verification

Run `gen-ai whoami` to confirm authentication, then re-run the failed command with `--debug`.

## Cost & time

| Task | Credits | Time |
|------|---------|------|
| 1 master icon (Flux 2 Pro, 1024) | 3-5 | ~15-25s |
| Local resize to ~25 icon sizes | 0 | ~5s total |
| 1 splash screen (Flux Kontext Pro, 9:16) | 3-5 | ~15-25s |
| 5× App Store screenshots (Ideogram v3) | 10-20 | ~60-90s batched c=4 |
| 1 feature graphic (Flux 2 Pro, 1024×500) | 3-5 | ~15-25s |
| **Full app pack (iOS + Android + watchOS + store)** | **~35-50** | **~5-8 min** |

## See also

- `gen-ai-use.md` — CLI reference, flags, auth
- `gen-ai-batch.md` — manifest shapes, batch resume, concurrency tuning
- `gen-ai-workflows.md` — Workflow 5 (launch kit) for motion/reel companion assets
- `dev-screenshot-beautifier` — device-frame the App Store screenshots
- `dev-og-image-service` — social cards for the marketing site
