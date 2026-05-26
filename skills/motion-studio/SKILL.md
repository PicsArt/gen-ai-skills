---
name: motion-studio
description: End-to-end AI video production with Picsart gen-ai.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: creative
    tags: [picsart, video, motion-graphics, creative]
---

# Motion Studio

A complete pipeline for producing finished videos from a story idea:

**Reference image → AI-generated clips → animated composition → final MP4**

Combines AI generation via the Picsart gen-ai CLI or equivalent MCP tool calls with a programmatic scene compositor to assemble clips with animations, transitions, text overlays, lower-thirds, captions, intro/outro cards, and audio.

---

## When to Use

Trigger this skill when the user asks to:
- Create a video, reel, TikTok, Short, Story, or ad
- Turn an idea, script, or storyline into a finished video
- Animate a sequence of AI-generated clips
- Build an explainer, product demo, testimonial, or influencer video
- Mock up a pitch reel, creator launch video, or marketer campaign reel
- Assemble multiple clips with transitions, text, or music
- Produce videos with character consistency across scenes

**Do not use for:** static images only, audio-only edits, or pre-existing video edits that don't need AI generation.

## Prerequisites

Picsart `gen-ai` CLI installed and authenticated (`gen-ai login`).

## How to Run

_Use the agent's `terminal` tool to invoke `gen-ai` commands as described in the Procedure below._

## Quick Reference

| Need | Model | Notes |
|------|-------|-------|
| Best quality, i2v, 9:16, audio | `kling-v3` with `--speed pro` | Check `gen-ai models info kling-v3` for current parameters before spending. |
| Cheaper Kling draft | `kling-v3` with `--speed std` | Lower cost, lower fidelity. Use for prompt iteration and drafts. |
| Nature/abstract, fast | `seedance-1.5-pro` | T2V only. 4-12 credits. Durations: 4, 5, 8, 10, 12s |
| Talking-head with lip-sync | `kling-avatar` | Requires portrait + audio file. Best for spoken dialogue |
| Latest Kling t2v | `kling-v3` | Same family, no `--start-frame` when the brief does not require character consistency |

**Always estimate first:**
```bash
gen-ai pricing kling-v3 --duration 8 --resolution 1080p --audio

gen-ai generate -m kling-v3 \
  -p "<clip prompt>" \
  --start-frame "<project>/public/portrait/character.png" \
  --ar 9:16 \
  --duration 8 \
  --generate-audio \
  --speed pro \
  --download "<project>/public/clips" \
  --dry-run --no-input
```

## Procedure



## Pitfalls

_See Common Pitfalls below._

## Verification

Run `gen-ai whoami` to confirm authentication, then re-run the failed command with `--debug`.

## Persona entry points

This one skill intentionally covers the former agency, marketer, and prosumer Motion Studio bundles. The production pipeline is the same; only the brief emphasis changes:

| User asks for | Treat as | Default shape |
|---|---|---|
| Reels, TikToks, social ads, campaign stories | Marketer | Hook -> value -> CTA, platform-native 9:16, optional voiceover |
| Launch videos, creator shorts, product updates | Prosumer | Title card -> 3 scene beats -> CTA, lightweight polish |
| Pitch reels, client mockups, concept sizzles | Agency | Client-safe mockup labels, on-brand talent/reference, handoff-ready file names |

Do not branch to persona-specific duplicate skills; keep the workflow here and adapt the plan to the user's brief.

---

## Workflow (always follow this order)

```
1. INTERVIEW         → clarify story, format, character, length, platform
2. PLAN & ESTIMATE   → propose structure + credit cost, get approval
3. REFERENCE IMAGE   → generate 1 portrait for character consistency (if needed)
4. CLIPS             → generate N AI video clips (parallel where possible)
5. SCAFFOLD          → set up scene compositor project from template
6. COMPOSE           → write scene components with animations + overlays
7. RENDER            → output final MP4, verify duration + format
8. DELIVER           → open the file, summarize what was built
```

**Critical rules:**
- **NEVER generate clips without explicit user approval of the plan + cost.** Paid API calls require approval.
- **ALWAYS estimate before generating** — use `gen-ai pricing <model>` for credit ranges and `gen-ai generate --dry-run` / `gen-ai batch run --dry-run` to validate payloads. If an MCP pricing/estimate tool is available, the same rule applies there.
- **Character persistence requires image-to-video (i2v)** — generate one portrait first, then feed it to every Kling clip with `--start-frame` or the equivalent MCP `startFrame` parameter.
- **Match composition duration math exactly** to the sum of sequences minus transitions. Miscalculation causes last frame freeze or truncation.
- **Use `linearTiming` with explicit `durationInFrames`** for all transitions. Never mix `springTiming` with fixed-duration math.

---

## Step 1: Interview

Before proposing, ask (combine into 1 message):

1. **Story/topic**: what's the video about?
2. **Format & platform**: TikTok (9:16), YouTube (16:9), square (1:1)? What platform?
3. **Length**: target seconds? (hard max 30s for short-form, 60s for explainers)
4. **Character**: should the same character appear across scenes? Describe them.
5. **Voice**: AI-generated voiceover (via the video model) or silent with text captions?
6. **Tone**: cinematic, playful, professional, dramatic?

If the user provides a detailed brief, skip the interview and go straight to Step 2.

---

## Step 2: Plan & estimate

Present a **table of scenes** with per-clip durations, a **visual/copy breakdown**, a **credit cost table**, and the **total duration math**. Wait for explicit "go" before spending credits.

Example plan table:

| # | Scene (duration) | Visual | On-screen text | Character action |
|---|-------------------|--------|----------------|------------------|
| 1 | Hook (8s) | Neon studio | "One command." | Leans in, smiles |
| 2 | How (8s) | Desk | "Generate → Compose" | Gestures to timeline |
| 3 | Tips (8s) | Urban | "3 Best Practices" | Counts on fingers |

Cost table:

| Asset | Model | Credits |
|-------|-------|---------|
| 1× portrait | `gemini-3-pro-image` | ~5 |
| 3× i2v clips (8s, 9:16, audio) | `kling-v3` | ~60 |
| **Total** | | **~65** |

---

## Step 3: Reference image (for character persistence)

Skip this step if no character is required (abstract/nature/product videos).

**Best model for character fidelity:** `gemini-3-pro-image` (Nano Banana Pro). Alternatives: `flux-2-pro`, `imagen-4.0-ultra`.

**Portrait prompt template:**
```
Hyperrealistic [framing] portrait of a [age] [role/persona],
[physical features: skin, hair, eyes, distinctive details],
wearing [wardrobe],
[expression/pose],
shot on [lens], shallow depth of field,
[lighting setup],
[background],
photorealistic skin texture, editorial fashion photography,
[aspect ratio] composition, [crop].
```

Generate with the CLI:
```bash
gen-ai generate -m gemini-3-pro-image \
  -p "<portrait prompt>" \
  --ar 9:16 \
  --download "<project>/public/portrait" \
  --json --no-input
```

When using MCP, pass the same model, prompt, aspect ratio, and download directory to the generation tool. Save the returned image URL if the MCP response includes one; the CLI will upload local image inputs for the clip step when needed.

Before proceeding to clips, Read the downloaded image to verify it matches the brief. If off, regenerate with sharper prompt. Do not waste clip credits on a bad portrait.

---

## Step 4: Clip generation



### Clip prompt structure (for character-consistent i2v)

Reference the character, describe the action, describe the environment, specify the dialogue (if any), and describe the camera/lighting:

```
The same [character description] from the reference image [action/pose].
She/he [specific gestures and movement].
She/he says: "<exact dialogue>".
[Environment + lighting + camera style],
cinematic vertical/horizontal video, hyperrealistic.
```

### Generation call (parallel when independent)

Fire all clips in parallel where your shell or agent environment supports it — they're independent API calls:

```bash
gen-ai generate -m kling-v3 -p "<clip 1>" --start-frame "<portrait file>" --ar 9:16 --duration 8 --generate-audio --speed pro --download "<project>/public/clips" --no-input
gen-ai generate -m kling-v3 -p "<clip 2>" --start-frame "<portrait file>" --ar 9:16 --duration 8 --generate-audio --speed pro --download "<project>/public/clips" --no-input
gen-ai generate -m kling-v3 -p "<clip 3>" --start-frame "<portrait file>" --ar 9:16 --duration 8 --generate-audio --speed pro --download "<project>/public/clips" --no-input
```

When using MCP, call the equivalent generation tool with `model`, `prompt`, `startFrame`, `duration`, `aspectRatio`, `generateAudio`, `renderingSpeed`, and `download`.

After download, either rename files to the template defaults (`01.mp4`, `02.mp4`, `03.mp4`) or update the `CLIPS` array in `Video.tsx` to your semantic filenames (`01-hook.mp4`, `02-how.mp4`, `03-tips.mp4`).

Verify without extra media tooling:
```bash
ls -lh <file>
```

Open/play the file in the OS viewer or browser and confirm it loads. Optional deep probe if ffprobe is already available:
```bash
ffprobe -v error -show_entries stream=width,height,codec_name,duration -of default=noprint_wrappers=1 <file>
```

---

## Step 5: Scaffold the compositor project

Pick any project directory — the skill has no hardcoded location. Examples: `~/videos/<project-name>/`, `./projects/<name>/`, or wherever your workspace lives. Substitute `<project>` throughout the rest of this guide.

**Standard structure:**
```
<project>/
├── package.json
├── tsconfig.json
├── remotion.config.ts
├── public/
│   ├── portrait/character.png
│   └── clips/*.mp4
├── src/
│   ├── index.ts        # entry point
│   ├── Root.tsx        # composition definition
│   └── Video.tsx       # main composition
└── out/<name>.mp4      # final render
```

**Get the templates.** This skill ships with ready-to-use template files in `assets/remotion-template/`. When the skill is installed (via `~/.claude/skills/motion-studio/`, `~/.codex/skills/motion-studio/`, or unzipped from `motion-studio.zip`), copy the templates into your project:

```bash
# Resolve the skill bundle location (adjust for your install path)
SKILL_DIR="$HOME/.claude/skills/motion-studio"   # or ~/.codex/skills/motion-studio, or wherever you unzipped the bundle
PROJECT_DIR="<project>"                          # your project root, e.g. ~/videos/bee-story

mkdir -p "$PROJECT_DIR/src" "$PROJECT_DIR/public/clips" "$PROJECT_DIR/public/portrait" "$PROJECT_DIR/out"
cp "$SKILL_DIR/assets/remotion-template/package.json"        "$PROJECT_DIR/"
cp "$SKILL_DIR/assets/remotion-template/tsconfig.json"       "$PROJECT_DIR/"
cp "$SKILL_DIR/assets/remotion-template/remotion.config.ts"  "$PROJECT_DIR/"
cp "$SKILL_DIR/assets/remotion-template/index.ts"            "$PROJECT_DIR/src/"
cp "$SKILL_DIR/assets/remotion-template/Root.tsx"            "$PROJECT_DIR/src/"
cp "$SKILL_DIR/assets/remotion-template/Video.tsx"           "$PROJECT_DIR/src/"
```

Then `cd "$PROJECT_DIR"` and run `npm install` once before rendering.

---

## Step 6: Compose scenes



### Duration math (CRITICAL)

N_TRANSITIONS depends on `AUDIO_MODE` (see Step 7). The template derives both `N_CLIPS` and `TOTAL_DURATION_FRAMES` from `CLIPS.length` — add or remove entries freely, the math adapts.

```
music / silent: TOTAL = INTRO + Σ CLIPS + OUTRO − (N_CLIPS + 1) × TRANSITION_FRAMES
dialogue:       TOTAL = INTRO + Σ CLIPS + OUTRO − 2 × TRANSITION_FRAMES
```

Verified examples (`INTRO = 45f`, `CLIP = 240f`, `OUTRO = 60f`, `TRANSITION = 15f`):

| Mode | N | Transitions | Formula | Total |
|------|---|-------------|---------|-------|
| silent / music | 3 | 4 | 45 + 720 + 60 − 60 | **765f = 25.5s** |
| silent / music | 2 | 3 | 45 + 480 + 60 − 45 | **540f = 18.0s** |
| dialogue | 3 | 2 | 45 + 720 + 60 − 30 | **795f = 26.5s** |
| dialogue | 2 | 2 | 45 + 480 + 60 − 30 | **555f = 18.5s** |
| dialogue | 1 | 2 | 45 + 240 + 60 − 30 | **315f = 10.5s** |

**Rules:**
- All transitions MUST use `linearTiming({ durationInFrames: N })`
- Do NOT use `springTiming` in transitions unless you compute its duration explicitly — spring durations depend on the spring config and will break the math
- Composition `durationInFrames` must equal the formula for the current mode exactly — the template's `TOTAL_DURATION_FRAMES` expression already does this, so don't override it with a hardcoded number

### Resolution by format

| Format | Resolution | Aspect |
|--------|-----------|--------|
| TikTok / Reels / Shorts | 1080 × 1920 | 9:16 |
| YouTube | 1920 × 1080 | 16:9 |
| Instagram square | 1080 × 1080 | 1:1 |
| Twitter | 1280 × 720 | 16:9 |

Always @ 30fps unless user requests otherwise.

### Scene component pattern

Each scene has three layers stacked:

```
┌─────────────────────────────────┐
│ LAYER 3: Animated text overlays  │  ← chips, captions, lower-thirds
│ LAYER 2: Legibility gradient     │  ← dark gradient under text
│ LAYER 1: Background video/image  │  ← AI clip with optional Ken Burns
└─────────────────────────────────┘
```

Text animations: spring-based pop-in (frames 6-30), hold, fade out before transition (last 20 frames).

### Animation primitives (the motion engine)

Frame-driven animation with these core functions:

| Function | Use case |
|----------|----------|
| `interpolate(frame, [inputRange], [outputRange], options)` | Linear value mapping |
| `spring({ frame, fps, config })` | Physics-based animation |
| `interpolateColors(frame, [inputRange], [colors])` | Color transitions |

Extrapolation: always set `extrapolateLeft: "clamp", extrapolateRight: "clamp"` on fades to prevent overshoot.

Spring presets:
```typescript
const SPRING = {
  snappy: { damping: 200, stiffness: 400, mass: 0.5 },  // UI
  smooth: { damping: 30, stiffness: 120, mass: 1 },     // transitions
  bouncy: { damping: 12, stiffness: 200, mass: 0.8 },   // emphasis
  wobbly: { damping: 8, stiffness: 180, mass: 0.6 },    // playful
};
```

### Transitions

Use `TransitionSeries` to chain sequences with crossfades:

```tsx
<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={INTRO_FRAMES}>
    <IntroCard />
  </TransitionSeries.Sequence>

  <TransitionSeries.Transition
    presentation={fade()}
    timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
  />

  <TransitionSeries.Sequence durationInFrames={CLIP_FRAMES}>
    <Scene clipFile="clips/01.mp4" />
  </TransitionSeries.Sequence>
  {/* ...more transitions + sequences */}
</TransitionSeries>
```

Available transition presentations: `fade`, `slide({ direction })`, `wipe()`, `flip()`, `zoom()`.

### Text overlays

**Chip (pill label) — top of screen:**
```tsx
<div style={{
  position: "absolute", top: 80, left: "50%",
  transform: `translateX(-50%) translateY(${chipY}px)`,
  padding: "16px 40px", background: brandColor,
  color: "#fff", fontSize: 38, fontWeight: 900,
  letterSpacing: 4, borderRadius: 999,
  boxShadow: "0 10px 40px rgba(0,0,0,0.4)",
}}>
  {chipLabel}
</div>
```

**Caption — bottom, large:**
```tsx
<div style={{
  position: "absolute", bottom: 140, left: 50, right: 50,
  fontSize: 72, fontWeight: 900, color: "#fff",
  textShadow: "0 4px 24px rgba(0,0,0,0.6)",
  opacity: captionOpacity,
  transform: `translateY(${captionY}px)`,
}}>
  {caption}
</div>
```

**Always add a dark gradient below text** for legibility:
```tsx
<AbsoluteFill style={{
  background: "linear-gradient(to top, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0) 45%)",
}}/>
```

### Ken Burns (subtle motion for still-feeling clips)

```tsx
const zoom = interpolate(frame, [0, CLIP_FRAMES], [1.0, 1.08]);
<AbsoluteFill style={{ transform: `scale(${zoom})` }}>
  <OffthreadVideo src={staticFile(clipFile)} ... />
</AbsoluteFill>
```

### Video component — always use `OffthreadVideo`

For better performance on large files and for clips with audio:
```tsx
<OffthreadVideo src={staticFile("clips/01.mp4")} endAt={CLIP_FRAMES} muted={false} />
```

Set `muted` based on whether the AI clip has useful audio. For silent clips with added background music, set `muted`.

---

## Step 7: Audio

**CRITICAL — crossfade transitions do NOT crossfade audio.** During a `TransitionSeries` + `fade()` overlap, both adjacent sequences render simultaneously, including their audio tracks. Visual crossfade: smooth. Audio: BOTH play at once. If both clips contain dialogue, the outgoing voiceover talks over the incoming one for the duration of the overlap.

For clips with embedded AI dialogue (`kling-v3` with `generateAudio: true`, or any voiceover-bearing clip): **never use `TransitionSeries` + fade between dialogue-bearing clips.** Use `Series` (hard cuts) instead. Intro and outro can still fade since they're silent — the conflict only exists between two audio-bearing sections.

### The three audio modes

Pick one per project. The template dispatches composition structure based on the `AUDIO_MODE` constant in `Video.tsx`.

**Mode `dialogue`** — clips have embedded AI voiceover (typical for influencer/talking-head content)
- Composition uses `Series` between dialogue clips (hard cuts, no audio overlap). Intro↔first-clip and last-clip↔outro fade — safe because intro/outro are silent.
- Clips render unmuted (`muted={false}`).
- Do NOT add music or external audio — it clashes with the dialogue.
- Only 2 transitions in the duration math (intro + outro), not `N_CLIPS + 1`.

**Mode `music`** — clips are muted, one music bed plays over the whole composition
- Composition uses `TransitionSeries` with fades between every section (smooth visual crossfades are fine because there's only one audio source).
- All clips render muted (`muted={true}`).
- Add `<Audio src={staticFile("audio/music.mp3")} volume={0.35} />` at the top of the composition, outside any Sequence.
- Standard `N_SECTIONS − 1` transitions in the duration math.

**Mode `silent`** — no audio anywhere
- Composition uses `TransitionSeries` with fades.
- All clips muted. No `<Audio>` element.
- Standard `N_SECTIONS − 1` transitions.

### Duration math by mode

```
dialogue:   TOTAL = INTRO + Σ CLIPS + OUTRO − 2 × TRANSITION_FRAMES
music:      TOTAL = INTRO + Σ CLIPS + OUTRO − (N_CLIPS + 1) × TRANSITION_FRAMES
silent:     TOTAL = INTRO + Σ CLIPS + OUTRO − (N_CLIPS + 1) × TRANSITION_FRAMES
```

Example for 3 × 8s clips + 1.5s intro + 2s outro, 0.5s transitions:
- `dialogue` (2 fades): 45 + 720 + 60 − 30 = **795f = 26.5s**
- `music` / `silent` (4 fades): 45 + 720 + 60 − 60 = **765f = 25.5s**

### Implementation note

The `Video.tsx` template already implements both composition structures and picks one via `AUDIO_MODE`. If you're tempted to hand-edit a dialogue composition to use `TransitionSeries` + fade between clips for "smoother transitions," DON'T — you'll ship overlapping voiceovers. The only correct advanced path: (1) mute the clip's audio, (2) extract the dialogue into a separate `<Audio>` element with `startFrom`/`endAt` so adjacent dialogue tracks don't overlap in time, (3) then fade the visuals with TransitionSeries. Default to `Series` hard cuts unless the user explicitly asks for this.

---

## Step 8: Render

```bash
cd <project>
npm install --no-audit --no-fund  # first time only
mkdir -p out
npx remotion render src/index.ts <CompositionId> out/<name>.mp4 --codec h264 --concurrency 4
```

Verify output without extra media tooling:
```bash
ls -lh out/<name>.mp4
```

Open/play the render in the OS viewer or browser and confirm it loads. Optional deep probe if ffprobe is already available:
```bash
ffprobe -v error -show_entries format=duration,size:stream=width,height,codec_name -of default=noprint_wrappers=1 out/<name>.mp4
```

Check:
- Duration matches the composition math within 0.1s
- Resolution matches the target format
- Audio stream is present (or absent) as intended

Open for preview (OS-aware):
- macOS: `open out/<name>.mp4`
- Linux: `xdg-open out/<name>.mp4`
- Windows (PowerShell): `Invoke-Item out/<name>.mp4`

Or just drag the file into any video player.

---

### Planning

- **Never exceed the user's duration cap.** If they say 30s, target 25-28s to leave room for safety.
- **Odd number of scenes (3 or 5) reads as a story.** Even (2, 4) feels listicle-y.
- **Each scene needs a clear "beat"** — hook, reveal, payoff, etc.

### Cost control

- Always run `gen-ai pricing` and a dry run before generating. Show the user the estimate or pricing range.
- If the user says "cheaper", use `kling-v3 --speed std`, `kling-v2-6`, or Seedance (for nature/abstract).
- Generate ONE portrait first, verify visually, then batch clips — never regenerate 3 bad clips.

### Character consistency

- The portrait must be **hyperrealistic and studio-lit** to survive i2v animation. Cartoonish or heavily-stylized portraits degrade across clips.
- Reuse the exact same portrait file or CDN URL as the `--start-frame` / `startFrame` input for every clip.
- In the clip prompt, explicitly reference "the same [character] from the reference image" — this improves fidelity.
- Keep the character in frame similarly across clips (e.g., all medium shots) — wild framing changes break consistency more than outfit changes.

### Format choices

- **9:16 vertical** — TikTok, Reels, Shorts. Default for social/influencer content.
- **16:9 horizontal** — YouTube, explainers, product demos.
- **1:1 square** — feeds, ads.
- Match the portrait aspect to the clip aspect to the composition aspect. Don't mix.

### Transitions

- 0.5s (15 frames @ 30fps) is the sweet spot for crossfades. Longer feels sluggish.
- Use `fade()` as the default. `slide` or `zoom` for emphasis, never more than once per video.
- **Never use `springTiming` in transitions unless you calculate its duration explicitly.**

### Text overlays

- **Chips appear at frame ~6-36** (spring-in with overshoot), hold, **fade out at frame CLIP_FRAMES-20** (before transition).
- Caption font sizes: chip 38px, caption 72px, sub-caption 36px. Scale proportionally for 16:9 (~1.2×).
- Always pair text with a **dark gradient** for legibility against video backgrounds.
- Use brand colors consistently. Picsart palette: `#FF006E` (pink), `#8338EC` (purple), `#FFBE0B` (yellow), `#0D0A1F` (ink).

### Common pitfalls to avoid

| Pitfall | Fix |
|---------|-----|
| Composition duration doesn't match sequence math | Use `linearTiming` with explicit `durationInFrames`. Recompute formula. |
| Character drifts across clips | Use i2v with portrait, reference it in prompt, keep framing consistent |
| Audio clashes | Pick ONE audio source — either AI-generated clip audio OR music bed, not both |
| Low-res video | Kling default is 1080p, but match composition resolution (1080×1920 or 1920×1080) |
| Text unreadable over busy clip | Add dark gradient layer + text shadow |
| Flicker at clip boundaries | Fade UI elements out in the last 20 frames before a transition |
| Render takes forever | `--concurrency 4` minimum, use `<OffthreadVideo>`, avoid heavy CSS shadows |

---

## Cost & time reference

| Task | Credits | Time |
|------|---------|------|
| 1 portrait (Nano Banana Pro, 9:16) | 2-5 | ~30s |
| 1 clip (`kling-v3`, `--speed pro`, 8s, 9:16) | ~20 | ~170s |
| 1 clip (`kling-v3`, `--speed std`, 8s, 9:16) | ~8 | ~120s |
| 1 clip (Seedance 1.5 Pro t2v, 5s) | ~5 | ~75s |
| `npm install` (first time) | 0 | ~15s |
| Render (25s vertical, 30fps, h264) | 0 | ~90s |

**Typical full TikTok (1 portrait + 3× 8s clips + render): ~65 credits, ~10 min total.**

---

## Templates

This skill ships with starter templates in `assets/remotion-template/`:
- `package.json` — dependencies for the scene compositor
- `tsconfig.json` — TypeScript config
- `remotion.config.ts` — render config
- `index.ts`, `Root.tsx`, `Video.tsx` — reference composition with intro, 3 scenes, outro, transitions, chip labels, captions, and brand styling

Copy these to the project folder and fill in the clip paths + copy.

---

## Examples

See `references/example-projects.md` for reference projects:
- **Landscape nature story** (17s, 3 clips, no character, ambient style)
- **Vertical influencer** (25.5s, 3 clips, character-consistent, with AI voiceover)

---

## Deliverables checklist

Before telling the user "done":
- [ ] Final MP4 at `<project>/out/<name>.mp4`
- [ ] Duration within 0.2s of the computed math
- [ ] Resolution matches target format
- [ ] Audio mode matches intent (clip audio OR music OR silent)
- [ ] File opened for immediate visual preview (macOS `open`, Linux `xdg-open`, Windows `Invoke-Item`, or drag into any player)
- [ ] Summary of what's in it (scene table, credits spent, file size)
- [ ] Offer obvious tweak options (different copy, different music, different scene count)
