---
title: "Motion Studio — Example Projects"
type: skill
tags: [motion-studio, examples, video, reference]
date: 2026-04-22
---

# Motion Studio — Example Projects

Two reference projects illustrating the end-to-end workflow. Both live in `~/videos/`.

---

## Example 1: Nature story (landscape, no character)

**Use case:** ambient nature story, abstract visuals, no talking-head needed.

**Specs:**
- 1280 × 720 landscape (16:9)
- 17.0s total
- 3× AI clips (5s each) + intro + outro + 4 transitions
- No reference image (nature shots via text-to-video)

**Models used:**
- Clips: `seedance-1.5-pro` (t2v) — cheapest, fits nature aesthetic

**Credit cost:** 15 credits total (3 × 5)

**Structure:**
```
INTRO (2s) + CLIP_1 (5s) + CLIP_2 (5s) + CLIP_3 (5s) + OUTRO (2s) − 4 × 0.5s transitions = 17.0s
60f + 150f + 150f + 150f + 60f − 60f = 510f @ 30fps
```

**Clip prompts (t2v, 5s, 720p, 16:9):**

| # | Prompt |
|---|--------|
| 1 | Macro cinematic shot of a honeybee taking off from a bright yellow sunflower at golden hour, shallow depth of field, slow motion, petals gently swaying |
| 2 | A honeybee flying through a vibrant wildflower meadow, camera tracks alongside the bee, sun flares, dreamy bokeh |
| 3 | Ultra close-up macro shot of a honeybee landing on a bright pink flower, tiny golden pollen dust floating, ultra slow motion |

**Text overlays:**
- Intro: big title "A Bee's Day" with spring-in + tagline
- Per-scene: small uppercase label ("Act I") + big caption ("Takeoff.")
- Outro: emoji + "— fin —"

---

## Example 2: Influencer TikTok (vertical, character-consistent, with dialogue)

**Use case:** creator-style explainer with a recurring on-screen character speaking.

**Specs:**
- 1080 × 1920 vertical (9:16)
- 25.5s total
- 1× portrait + 3× AI clips (8s each) + intro + outro + 4 transitions
- Character consistency via i2v workflow

**Models used:**
- Portrait: `gemini-3-pro-image` (best for facial fidelity) — 4-5 credits
- Clips: `kling-v3` i2v with `generateAudio: true` and `renderingSpeed: "pro"` — about 20 credits each × 3 = 60

**Total cost:** ~64 credits

**Structure:**
```
INTRO (1.5s) + CLIP_1 (8s) + CLIP_2 (8s) + CLIP_3 (8s) + OUTRO (2s) − 4 × 0.5s transitions = 25.5s
45f + 240f + 240f + 240f + 60f − 60f = 765f @ 30fps
```

**Portrait prompt:**
```
Hyperrealistic studio portrait of a confident 27-year-old creative director,
warm brown skin, short undercut with pastel lavender highlights,
chunky black square-framed glasses, oversized gold hoop earrings,
oversized cream graphic tee under cropped black leather jacket,
slight smirk, bold expressive eyes,
shot on 85mm lens, shallow depth of field,
moody purple and teal rim lighting, dark background with subtle neon glow,
photorealistic skin texture, editorial fashion photography,
vertical 9:16 composition, head and upper chest in frame
```

**Clip prompt pattern (i2v, 8s, 9:16, with audio):**
```
The same confident woman from the reference image [action].
She [specific gesture], then [next gesture].
She says: "[exact dialogue]."
[Environment + lighting + camera],
cinematic vertical video, hyperrealistic, natural lip sync.
```

**Example clip prompt:**
```
The same confident woman from the reference image speaks directly to the camera
with warmth and energy. She tilts her head slightly, smiles, and gestures with
one hand near her face. She says: "Gen AI CLI plus Remotion equals one command
to cinema." Studio setting with purple and teal neon lighting, shallow depth of
field, natural lip movement, cinematic vertical video, hyperrealistic.
```

**Text overlays:**
- Intro: large stacked title on purple→pink gradient + yellow tagline
- Per-scene: colored pill chip at top ("HOOK" / "HOW IT WORKS" / "BEST PRACTICES") + bold caption at bottom + yellow sub-caption
- Outro: gradient-filled text headline with radial glow

**Audio mode:** clip audio (AI voiceover from Kling, no music bed needed).

---

## Key lessons from these examples

1. **Matching aspect ratios end-to-end.** Portrait 9:16 → Kling 9:16 → Composition 9:16. Any mismatch causes letterboxing or cropping.
2. **One portrait, many clips.** The same portrait file or CDN URL goes into every `--start-frame` / `startFrame` parameter. This is the character-persistence hack.
3. **Clip duration enums are fixed.** Seedance and Kling both offer only specific durations (e.g., 3, 5, 8, 10, 12s). Plan the composition math around what's actually available.
4. **`linearTiming` only.** Mixing `springTiming` breaks the duration math and leads to freeze frames at the end.
5. **AI voiceover vs. music.** Pick one. If clips have generated audio (Kling with `generateAudio: true`), don't add music — it'll clash with the voiceover.
6. **Fade UI before transitions.** The last 20 frames of each scene should fade overlays out, so the crossfade is clean.
7. **Open the file after rendering.** Instant visual confirmation is OS-aware: `open <path>` on macOS, `xdg-open <path>` on Linux, `Invoke-Item <path>` on Windows. Don't just check the size.
