---
name: gen-ai-persona-creation
description: Create AI influencer or branded character personas.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: creative
    tags: [picsart, personas, character-design, creative]
---

# AI Influencer Persona

Turn one sentence into a head-to-toe 4-angle casting card in signature wardrobe, persona profile, platform-tuned captions, and (optional) a reel with ambient audio. Output: `./<persona-slug>/`.

## When to Use

_See the description above._

## Prerequisites

```bash
gen-ai whoami            # auth + gen-ai install + Node v22+ check
command -v curl          # ships with macOS / Linux / Git-Bash
```

If `gen-ai whoami` fails: `gen-ai login` or set `PICSART_ACCESS_TOKEN` + `PICSART_USER_ID`. No extra media tools needed.

## How to Run

_Use the agent's `terminal` tool to invoke `gen-ai` commands as described in the Procedure below._

## Quick Reference

_See the Procedure for canonical commands._

## Procedure

_See sections below for the detailed walkthrough._

## Pitfalls

_See Common Pitfalls below._

## Verification

Run `gen-ai whoami` to confirm authentication, then re-run the failed command with `--debug`.

## How the skill calls `gen-ai`

```bash
URL=$(gen-ai generate -m <model> -p "<prompt>" --json --no-input | grep -oE 'https?://[^"]+' | head -1)
curl -sSL -o ./<persona-slug>/<file>.<ext> "$URL"
```

`--download` doesn't work with `--json --no-input` — URL+curl is canonical.

**Bash footguns:** never add `2>&1` or stderr redirects between `--json --no-input` and the closing `)` — shell parse error before the command runs (verified). Keep the inner pipe strictly `--json --no-input | grep -oE 'https?://[^"]+' | head -1`. One generation per `URL=$(...)`.

## Style routing

| Style | Model | For | Cost |
|---|---|---|---|
| `realistic` (default) | `gemini-3.1-flash-image` | photoreal humans + photoreal common pets / anthropomorphic animals | ~3 cr |
| `stylized` | `grok-imagine` | anime, 3D-animated fruit/object/character, illustration | ~1 cr |

**Cross-provider fallback:** primary fails → retry with `flux-2-max` (~3 cr, supports `imageUrls`). Both fail → surface error.

### Style inference (read the brief)

| Brief contains | Style → opening |
|---|---|
| Fruit/veggie/food + "character" / "anthropomorphic" / "brainrot" | stylized → fruit/object |
| Animal name + "pet" / "influencer" / "creator" / breed (NOT "real form" / "four-legged") | realistic → **anthropomorphic humanoid pet** (default for animal/pet briefs — fluffy biped in cute clothes, matches project's `pets` category vibe) |
| Animal name + explicit "real form" / "four-legged" / "on all fours" / "real cat / dog / animal" | realistic → real-form quadruped pet (opt-in) |
| "Anime", "manga", "magical girl", "kawaii", "shoujo", "shonen" | stylized → anime |
| "3D rendered", "stylized 3D", "claymation", "feature-film animation" | stylized → 3D character |
| "Illustrated", "painted", "watercolor", "comic book" | stylized → illustration |
| Human profession + demographic, no style cue | realistic → photoreal human |

Both anthropomorphic-humanoid and real-form-quadruped are supported, but **anthropomorphic is the default** for pet briefs — that matches the Picsart project's `pets` category which is fluffy biped influencers in cute clothes (tiny sweaters, mini hoodies, bow ties), with food-themed names (Biscuit, Mochi, Nugget, Bean, Waffles, Tofu, Pickle) and gen-z bios ("professional napper | treat negotiator | certified good boy/girl"). Real-form four-legged is the opt-in for creators who explicitly say so. Style conflict (e.g. "anime fitness coach") → prefer the **stylistic** cue.

**Most creators want stylized.** Don't blindly default to realistic.

**IP-safe wording (mandatory):** never name studios / franchises in prompts sent to the model — no "Pixar", "Disney", "Toy Story", "Studio Ghibli", "Marvel", etc. Recognize creator phrasing like "Pixar-style" as a 3D-animated *intent* (route to stylized 3D) but use generic descriptors in the actual prompt: "3D-animated", "feature-film animation aesthetic", "stylized 3D rendering", "anime cel-shaded illustration". Studio names trigger content policies + downstream IP risk.

## What creators express in their brief (natural language)

The agent extracts intent — no CLI flags to learn:

- **Reference image** (*"from /path/photo.png"*) → adds `-i` to casting-card call
- **Reel** (*"add a tiktok reel"*, *"with motion"*) → triggers Step 4 (~11 extra cr)
- **Platform** (*"for tiktok"*, *"instagram reel"*, *"linkedin"*) → drives reel AR + caption tuning
- **Style** (*"anime"*, *"3D"*, *"painted"*, *"photoreal"*) → routes realistic / stylized
- **Name** (*"named Nova"*) → sets persona name
- **Character type** (*"strawberry character"*, *"golden retriever pet"*, *"magical girl"*) → picks subject opening

## Quick start

Plain English. Examples:

- *"Create a persona for: fitness coach, gen-z, neon vibe"* (realistic human)
- *"Create a fluffy golden puppy pet influencer, sassy queen energy, mini hoodie"* (anthropomorphic pet — DEFAULT for pet briefs: fluffy biped in cute clothes)
- *"Create a calico kitten content creator, sleepy baby vibe, tiny knitted sweater"* (anthropomorphic pet)
- *"Create a real four-legged tortoiseshell cat in a sunlit Tokyo apartment"* (real-form pet — opt-in only with explicit "real form / four-legged" cue)
- *"Make me an anime magical-girl librarian"* (stylized)
- *"Create a strawberry character, brainrot 3D-animated vibe"* (stylized fruit)
- *"Create a persona based on /path/photo.png — indie folk musician"* (reference)
- *"Create a persona for: fitness coach — and add a tiktok reel"* (with reel)

Output: `casting.png`, `persona.md`, `_meta.json` (+ `reel-hero.png` + `reel.mp4` if reel requested).

Cost: **~3 cr** lean / **~14 cr** with reel.

## Pipeline



### Step 1 — Intent

Extract: persona seed | style | reference image | reel + platform requested | name | slug.

**Bias hard toward "infer and proceed."** Only ask if brief is truly thin (1–2 words). Invent missing details (gender, age, ethnicity, vibe), note in `persona.md`, let creator re-roll.

If you must ask, ask exactly **ONE direct question**. Never enumerate A/B/C/D menus. Never stack multiple questions.

GOOD response (only when brief too thin):

```
Give me a one-liner — vibe / type / niche.
Examples:
- anthropomorphic pet (default for pet briefs): "fluffy golden puppy influencer, sassy queen, mini hoodie" / "calico kitten creator, sleepy baby, tiny sweater"
- real-form pet (opt-in): "real four-legged tortie cat in a sunlit apartment"
- realistic human: "Berlin art curator, dark academia, mid-thirties"
- stylized: "anime magical-girl librarian" / "anthropomorphic strawberry, brainrot 3D"
Add-ons: "from /path/photo.png" / "add a tiktok reel" / "named Mochi"
```

BAD: A/B/C/D menus + multiple questions stacked. Don't.

### Step 2 — Identity → `persona.md`

Write: name | bio (2–3 sentences) | voice/tone | **frozen appearance block** (verbatim, reuse in every prompt). Block contains identity DNA only (face geometry, eye/hair/skin, body type, distinguishing marks, wardrobe aesthetic baseline) — NOT per-shot deltas (expression, pose, lighting, scene, specific outfits).

### Step 3 — Casting card

One call. 4 head-to-toe angles, plain seamless gray, signature wardrobe, neutral expression. 9:16 portrait with 2×2 grid inside (each panel ≈ 9:16 — fits full body).

```bash
URL=$(gen-ai generate -m <style-model> -p "<subject-opening> The image shows the same exact character from four camera angles in a 2x2 portrait grid (9:16 canvas). ALL FOUR PANELS share: identical plain seamless studio gray background — flat uniform fill, no gradient/texture/scene. Identical signature wardrobe — same complete outfit head to feet (or, for common pets, identical simple accessories like collar/bandana/sweater — never humanoid clothing). Identical neutral expression — relaxed mouth. Identical even soft frontal softbox key + subtle fill + soft ground shadow, no rim lights, no colored gels. Identical hair/fur. Same identity in every panel: <frozen appearance block>. Differs only in angle: TOP-LEFT front-facing full body eyes at camera; TOP-RIGHT 3/4 facing camera-right; BOTTOM-LEFT full left profile looking off-left; BOTTOM-RIGHT 3/4 from behind over-the-shoulder. Magazine fashion model sheet composition, thin clean grid lines. The four panels MUST look like consecutive shots from one session — same wardrobe, backdrop, lighting, character; only angle differs. Absolutely no text, no captions, no watermarks, no logos, no UI elements, no phone, no device, no screen, no social media overlays in any panel." --aspect-ratio 9:16 --json --no-input | grep -oE 'https?://[^"]+' | head -1)
curl -sSL -o ./<persona-slug>/casting.png "$URL"
```

`<style-model>` = `gemini-3.1-flash-image` (realistic) or `grok-imagine` (stylized). Apply fallback wrapper to `flux-2-max`.

**Reference image:** add `-i <reference-path>` to this same call. Identity via i2i, same prompt + cost.

#### Subject openings (replace `<subject-opening>` above)

- **Photoreal human** *(default)* — *"Professional fashion photograph head-to-toe casting card / model sheet, shot on 85mm lens, RAW photo, 8k UHD, crisp focus, photorealistic, natural skin texture with visible pores, no AI smoothing."*
- **Anthropomorphic humanoid pet** *(DEFAULT for pet/animal briefs — fluffy biped in cute clothes, project's `pets` category)* — *"An anthropomorphic [puppy / kitten / bunny / hamster / duckling / fox cub / baby panda / hedgehog / penguin / monkey] character standing upright on two legs like a human, full body visible head to toe, humanoid body proportions, expressive face, [coat detail — e.g. warm golden honey-colored fur / pure snow white fluffy fur / deep midnight black sleek fur / warm ginger orange fur / chocolate brown fur / shimmering silver grey fur / patchy calico orange-white-black fur / soft cream colored fur], adorable, looking directly at camera, professional fashion photograph, shot on 85mm lens, shallow depth of field, cinematic studio lighting with soft key light, photorealistic, RAW photo, 8k ultra high definition, crisp focus."* Wardrobe options the agent can pick from when composing the casting card outfit: tiny knitted sweater | mini oversized hoodie | dapper bow tie + collar | flower crown of daisies and roses | tiny stylish sunglasses | flowing superhero cape | stylish bandana around neck | au naturel (no clothing, just fluffy fur). Vibe options for expression / pose: Sassy Queen (hand on hip, serving looks, unbothered) | Silly King (goofy, tongue out, awkward funny pose) | Sleepy Baby (drowsy half-asleep, leaning) | Zoomies Mode (excited, arms up, chaotic joy) | Distinguished (regal, arms crossed, noble) | Mischief Maker (sneaky, hands behind back, guilty-not-sorry). Suggested name (food-themed, project's pool): Biscuit, Mochi, Nugget, Bean, Waffles, Tofu, Dumpling, Peanut, Pickle, Noodle, Churro, Pretzel, Taco, Maple, Truffle, Sesame, Crouton, Muffin, Cupcake, Boba. Suggested bio style (gen-z internet humor, pipe-separated): "professional napper | treat negotiator | certified good boy/girl" / "fluffy & unbothered | snack motivated | full-time cuddle bug" / "chaos gremlin | zoomies champion | will boop for treats".
- **Real-form quadruped pet** *(opt-in only — creator explicitly said "real form / four-legged / real cat / on all fours")* — *"Professional pet portrait photograph head-to-toe model sheet of a [breed] [animal] in their natural anatomical form (four-legged / quadruped, NOT humanoid), full body nose-to-tail visible, shot on 85mm with shallow depth of field, RAW, 8k UHD, photorealistic natural fur with visible individual hairs, no AI smoothing. Pet may wear simple accessories (collar, bandana, harness) but never humanoid clothing — the character is the animal in real anatomical form."*
- **3D-animated anthropomorphic fruit / object** — *"High quality 3D-animated head-to-toe character sheet of an anthropomorphic [fruit/object] character, feature-film animation aesthetic, [fruit/object] serves as the head on a full human-proportioned athletic body, [skin/surface] texture extending naturally to arms and hands, ultra-high resolution, brainrot character-drama vibe, dramatic cinematic studio lighting with soft fill + subtle ground shadow."*
- **Anime / manga** — *"High quality anime / manga style head-to-toe character sheet, cel-shaded illustration, clean line art, vibrant saturated colors, soft anime lighting, expressive eyes, [shoujo/shonen/kawaii] aesthetic, magazine character reference sheet composition."*
- **Stylized 3D-animated human / fantasy** — *"High quality stylized 3D-animated head-to-toe character sheet, feature-film animation aesthetic, soft global illumination, slightly exaggerated proportions, expressive features, character-animation art direction."*
- **Painted / illustrated** — *"Hand-painted editorial illustration head-to-toe character sheet, [watercolor/gouache/digital painting] aesthetic, painterly brushwork, layered soft light, magazine illustration composition."*

**Casting-card rules — non-negotiable:** identical bg / wardrobe-or-accessories / lighting / expression / hair-fur across all 4 panels — only angle differs | bg flat plain gray | full body (head-to-toe humans/bipeds INCLUDING anthropomorphic humanoid pets, nose-to-tail quadrupeds for real-form pet opt-in) | wardrobe stays same in all panels (same outfit for humans + anthropomorphic pets — yes, anthropomorphic pets wear humanoid clothing like tiny sweaters/mini hoodies/bow ties; only real-form quadruped pets are limited to simple accessories like collar/bandana/harness) | expression and pose match the chosen vibe (Sassy Queen / Silly King / etc. for anthropomorphic pets) — neutral default for humans, eyes at camera (or off per profile/back).

### Step 4 — Reel (only if requested)

Two sub-calls. Seedance treats `imageUrls` as **first frame** (verified) — passing the casting-card grid would open the reel on it. So: generate single-frame reel-hero first, then animate.

#### Pick the concept first

Don't auto-default to "slow contemplative push-in" — most creator content rewards confident energy.

Concepts: **Hook reveal** | **Power pose** | **Attitude flick** (look-away → snap-back smirk) | **Walk-by** | **Outfit reveal** | **Vibe drop** (lighting shift mid-clip) | **Establish-and-hold** | **Calm narrative beat** (only for genuinely-calm-niche personas).

**Hook rule:** first second must arrest attention. **Platform sensitivity:** TikTok / IG Reel / Shorts → punchy; LinkedIn / YouTube → professional / calm; fruit / 3D / anime → lean stylized + confident (calm beats fall flat for them).

**Camera move (pick ONE):** slow push-in | slow pull-out | partial orbit | slow track left/right | static | tilt up | whip-in.

**Action (pick ONE):** punchy default — confident camera-direct stare with attitude shift | power-pose hold | hair flip | smile breaking through | walking confidently toward camera | outfit-reveal turn | hand gesture | rhythmic vibe | look over shoulder | lighting drop. Quieter (calm-niche only) — looking up from book + soft smile | slow head tilt | hair lift in light wind | eyes opening | lip part.

**Environment / lighting:** atmospheric specifics > generic. Replace "in a cafe" with "neon-pink Tokyo coffee shop interior, signage reflections" (punchy) OR "rain-streaked window with candlelight, steam from teacup" (calm). Match energy to concept.

#### Sub-step 4-i: Reel hero (gemini i2i, target AR, single full-body frame)

```bash
URL=$(gen-ai generate -m gemini-3.1-flash-image -i ./<persona-slug>/casting.png -p "<subject-opening from Step 3> Single full-body photograph of the same character from the casting-card reference, head-to-toe in frame. <frozen appearance block>. Wearing the same signature wardrobe shown in casting card. <opening pose / framing for chosen concept>. <atmospheric environment + lighting>. Composition: full body head to toe, framed for video animation in <platform-AR>. Real photograph quality (or stylized rendering per opening). No text, no captions, no watermarks, no logos, no UI, no phone, no device, no screen, no social media overlays." --aspect-ratio <platform-AR> --json --no-input | grep -oE 'https?://[^"]+' | head -1)
curl -sSL -o ./<persona-slug>/reel-hero.png "$URL"
```

Cost: ~3 cr. Apply fallback to `flux-2-max`.

**Reel-hero ≠ final action pose.** Gemini tends to preserve the casting card's neutral stance even when prompted for power-pose / mid-action (verified). That's fine — the action lands in the Seedance prompt at 4-ii. Don't re-roll the hero just because the pose looks calmer than expected.

#### Sub-step 4-ii: Animation (Seedance i2v, audio enabled)

Platform → AR + duration:

| Platform | AR | Duration |
|---|---|---|
| tiktok / instagram-reel / instagram-story / youtube-shorts | 9:16 | 8s |
| instagram-feed | 1:1 (Seedance has no 4:5; closest universal) | 6s |
| youtube / linkedin / x / twitter | 16:9 | 8–10s |

```bash
URL=$(gen-ai generate -m seedance-2.0 -i ./<persona-slug>/reel-hero.png -p "<subject-opening>. <frozen appearance block>. Wearing same signature wardrobe. <single action from vocabulary matching the concept — strong language here, this is where action actually lands>. <same atmospheric environment + lighting as hero>. <single camera move from vocabulary>. Audio: <ambient soundscape matching scene — environmental sounds, mood-appropriate underscore; no spoken dialogue, no voiceover, no music vocals>. Single continuous moment, no scene changes, no multiple sequential actions, no fast or chaotic movement. No text, no captions, no watermarks, no logos, no UI, no phone, no device, no screen, no social media overlays." --aspect-ratio <platform-AR> --duration <platform-duration> --generate-audio --json --no-input | grep -oE 'https?://[^"]+' | head -1)
curl -sSL -o ./<persona-slug>/reel.mp4 "$URL"
```

Cost: 1 cr/sec × duration. **Total reel: ~8–13 cr.**

Seedance prompt order (verified KLING_RULES): Subject → Action → Environment → Camera → Lighting → Audio. One continuous camera move, one primary action — never chain.

**Models we DON'T use for reel:** any `startFrame`-only i2v (`seedance-i2v`, `hailuo-2.3-fast`, `runway-gen3a-turbo`, `wan-2.7-i2v`, `luma-flash2-i2v`, `pika-frames`) drifts across the clip; `runway-gen4-ref` returns a still PNG (verified, not a video); `kling-3.0-pro` / `veo-3.1` / `veo-3.1-fast` are `startFrame`-only — multi-image char-ref modes (Kling element / Veo Ingredients) aren't surfaced in the CLI today (roadmap).

**Honest constraint:** Seedance's `imageUrls` behaves as first frame, not pure char-ref. Single-frame hero + i2v = clean character image opens the reel and animates from there.

### Step 5 — Captions, deliver

Append captions to `persona.md` — 3 by default, in persona's voice. Hashtag block ALWAYS leads with `#picsart #picsartcreator`, then platform-specific niche tags.

| Platform | Length | Niche tags after Picsart pair |
|---|---|---|
| tiktok / youtube-shorts | 80–150 chars, single hook | 4–6 trending |
| instagram (reel/story/feed) | 150–300 chars, hook + story | 6–10 |
| youtube standard | 300–500 chars, keyword-dense | 3–5 keyword |
| linkedin | 500–1000 chars, professional | 3–5 industry |
| x / twitter | ≤280 chars total (incl tags) | 1–2 |
| (no platform) | ~150 chars, balanced | 4–6 generic |

Print final summary: `✓ Persona "Lena" delivered. Local: ./lena/. Spent: ~3 credits. Files: casting.png, persona.md (+ _meta.json)`. Add `reel-hero.png` + `reel.mp4` to file list if reel was generated.

## Cost transparency

Show plan before spending — pull live rates with `gen-ai pricing <model>`, never hardcode. After each step: `✓ <step> (<credits>)`.

```
Plan:
  Casting card (gemini-3.1-flash-image, 1 image)         ~3 cr
[ Reel hero (gemini-3.1-flash-image, 1 image)            ~3 cr ]   reel only
[ Reel animation (seedance-2.0, 8s @ 9:16)               ~8 cr ]
  ────────────────────────────────────────────────────────
  Estimated total                                       ~3 or ~14 cr
Continue? [Y/n]
```

## Output

```
./<persona-slug>/
├── persona.md       # name, bio, voice, frozen appearance block, captions
├── casting.png      # head-to-toe 4-angle casting card
├── reel-hero.png    # only if reel requested
├── reel.mp4         # only if reel requested (includes ambient audio)
└── _meta.json       # step parameters
```

## Re-rolls

Natural language. Agent reads `_meta.json` and reruns the right step:

- *"Regenerate Lena with darker hair"* (~3 cr)
- *"Redo the reel with a slow camera push instead of static"* (~8 cr)

Confirm spend before re-running.

## Limitations (today)

- Local-only output (Drive integration tracked v1.1 once new CLI Drive API ships)
- One persona per run (multi-persona via `gen-ai generate -m kling-multi-image-v2-1 -i nova/casting.png -i lena/casting.png -p "<scene>"` or future Scene Composer skill)
- No premium photoreal tier (`gemini-3-pro-image` deferred)
- No premium motion-control reel (Kling Motion Control V3 + creator motion-ref deferred)
- No voice / talking-head reel (Picsart-Eleven gender unreliable). Reel ships with Seedance ambient audio — environmental + atmospheric underscore, no synthesized speech
- No bespoke music (Seedance underscore via `--generate-audio`; dedicated music pass deferred)
- No Kling-element / Veo-Ingredients char-ref video (not surfaced in CLI)
- No built-in scene variations (casting card is the character; downstream tools handle scenes)
