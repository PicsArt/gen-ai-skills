# Scene Plan Director — Animated Explainer

## When to Use

You are the **Scene Planner**. You have the approved script (timestamped
sections, narration text, speaker directions). Your job is to transform the
script into a visual plan: what the viewer sees at every moment, what each
clip should depict, what motion to layer on top.

This is where words become visuals. A great script with a bad scene plan
produces a confusing video.

## Prerequisites

- Approved script with timestamped sections.
- Research findings (visual metaphors, expert references, source imagery
  the user has flagged).
- Awareness of model constraints (defaults: `seedance-2.0` for image-to-video,
  `gemini-3.1-flash-image` for stills).

## Step 1: Analyze the script

For each script section, note:
- What concept is being explained?
- What's the emotional beat? (curiosity / revelation / emphasis / humor /
  conclusion)
- How many seconds are available? (`duration_s`)
- Are there proper nouns / specific numbers / mechanisms that need to be
  visually shown? (these become required scene elements)

## Step 2: Research visual approaches (optional but high-value)

**Use `WebSearch`** to find visual techniques for this topic:

```
"[topic]" infographic
"[topic]" "diagram" OR "animation" OR "explainer"
"[topic]" site:youtube.com [thumbnails reveal the visual approaches that work]
```

What you're looking for:
1. **Established visual metaphors** — neural nets as node graphs, encryption
   as locks-and-keys, databases as filing cabinets. Use them — viewers
   recognize them instantly.
2. **Novel approaches** — is there a visualization nobody has tried? A fresh
   take makes an explainer memorable.

## Step 3: Decompose into scenes

Each script section maps to **1 scene** for short videos (30-90s) or **2-3
scenes** for longer sections. The scene-1-as-hero-anchor pattern means **scene
1's `image_prompt` defines the style for the whole video** — make it definitive.

## Step 4: Apply the 5-Aspect Scene Checklist

**Every scene's `image_prompt` MUST specify all five aspects.** Silent omission
is the #1 failure mode — Claude writes a vague prompt and Nano Banana 2 picks
a random "look." Be explicit.

| Aspect | What to specify | Example |
|---|---|---|
| **1. Subject** | What's in the frame — entity, attributes, count | "A single isometric espresso machine, cross-section view, copper pipes visible" |
| **2. Subject Motion** | What moves (for the `motion_hint`, not `image_prompt`) | "Pressure gauge needle rises slowly from 1 bar to 9 bar over 3s" |
| **3. Scene** | Setting + lighting + time + mood + overlays | "Soft pastel medical-illustration palette, daylight, clean white background, label '9 bar' appears top-right at 2s" |
| **4. Spatial framing** | Shot size + position + depth + camera height | "Medium shot, subject centered, machine occupies 60% of frame, eye-level isometric perspective" |
| **5. Camera** | Lens / angle / focus / movement (for `motion_hint`) | "Slow zoom in on the pressure gauge, ease-out, 3s" |

A scene's `image_prompt` should cover **Subject + Scene + Spatial framing**.
The `motion_hint` covers **Subject Motion + Camera**. Together they specify
all five aspects.

### Visual technique library

Reference these named patterns in your scene descriptions. They're proven
patterns for explainer visuals:

- **Diagram Reveal** — build a diagram progressively. Empty → add labeled
  components one by one. *"Start with empty cross-section. Pump, boiler, and
  portafilter slide in with labels as narrator names each."*
- **Analogy Visualization** — show abstract concept beside its real-world
  analog, split-screen. *"Left: anandamide molecule binding to receptor.
  Right: a key turning in a lock."*
- **Stat Punch** — full-frame number / phrase, slight scale-up animation, hold
  for 4s. *"'9 BAR' text appears center-frame, scales up 1.2x on entrance,
  pulsing subtle glow."*
- **Before-After Split** — problem on left, solution on right, vertical
  divider. *"Left: muddy keyword-search results. Right: clean
  vector-similarity matches."*
- **Timeline Progression** — left-to-right sequence showing evolution or
  process steps. Each step appears as narrator describes it. *"1990: keyword
  → 2010: semantic → 2020: vector → 2024: multimodal."*
- **Zoom-and-Focus** — wide view first, then zoom into a specific component.
  Creates spatial context. *"Show full coffee machine. Zoom into the boiler
  chamber."*

## Step 5: Hero-image consistency

Scenes 2..N automatically inherit scene 1's image as a style reference (via
`imageUrls`). This means:

- **Scene 1 anchors the look** — lighting, palette, line weight, perspective.
  Make scene 1's `image_prompt` the most definitive of the lot.
- Subsequent scenes should describe what changes (subject, action), not
  re-specify style ("same isometric medical-illustration look as scene 1" is
  redundant — the reference image enforces it).

If a scene needs a radically different visual style (e.g., a code-screen
flash among isometric scenes), tell the user — that scene won't benefit
from the hero anchor.

## Step 6: Per-scene shape (JSON for `scene-plan.json`)

The full file shape:

```json
{
  "playbook": "<the id chosen at proposal stage, e.g. isometric-medical>",
  "scenes": [
    {
      "id": "s1",
      "image_prompt": "<all 5 aspects compressed into 1-2 sentences, includes 16:9 implicitly>",
      "motion_hint": "<subject motion + camera motion, 1 sentence>",
      "duration_s": "<integer 4-15, valid for seedance-2.0>"
    }
  ]
}
```

**Always include the `playbook` field at the top level.** It's how the
`gen-ai explainer:assets` command knows which `image_prompt_prefix` to prepend
to every image generation. Forgetting it means the assets command falls back
to the default playbook (`isometric-medical`), which may not match the concept
the user approved.

## Playbook influences on scene prompts

The chosen playbook's `consistency_anchors` tell you what to keep stable
across all scenes. For `isometric-medical`:
- Soft pastel palette — peach, sage, lavender, cream.
- Isometric perspective held across every scene.
- Medical-illustration line weight (thin, even).
- Subjects centered, generous whitespace around them.

These should be **reflected in scene 1's image_prompt** (since the hero anchor
propagates them) but you do NOT need to restate them in every prompt — the
CLI prepends the playbook's `image_prompt_prefix` automatically and scenes
2..N inherit scene-1's style via the reference image.

## Step 7: Coverage / Variety / Feasibility checks

Run these before showing the user.

**Coverage:**
- [ ] Scenes span the full script duration (first starts at 0s, last ends at total).
- [ ] Every script section has at least one corresponding scene.
- [ ] Sum of scene durations matches script total (±2s tolerance).

**Variety:**
- [ ] No two consecutive scenes are visually identical (same setup, same motion).
- [ ] Visual pacing alternates between high-info (data-heavy) and breathing-room scenes.

**Feasibility:**
- [ ] Every `image_prompt` is achievable by `gemini-3.1-flash-image` — no
  "photo-realistic 3D flythrough" type asks.
- [ ] Every `duration_s` is integer 4-15 (seedance-2.0 constraint).
- [ ] Total scene count fits the table in step 3.

## Step 8: Self-evaluate

Score 1-5 on each. **If any score is below 3, revise before showing the user.**

| Criterion | Question |
|---|---|
| **Visual storytelling** | Does each scene advance understanding, not just decorate? |
| **Script alignment** | Does each scene match what the narrator says at that moment? |
| **5-aspect completeness** | Does every prompt cover Subject + Motion + Scene + Spatial + Camera? |
| **Hero anchor quality** | Is scene 1 definitive enough to anchor all others? |
| **Technique variety** | Did you use 2+ named techniques from the library? |
| **Feasibility** | Can Nano Banana 2 + Seedance 2.0 actually produce every scene? |
| **Pacing** | Does the visual rhythm feel natural? |

## Step 9: Present to the user

Show a table — one row per scene — that the user can scan quickly:

```
| # | Beat | Image prompt (Subject + Scene + Spatial) | Motion hint (Motion + Camera) | Dur |
|---|------|-----------------------------------------|-------------------------------|-----|
| 1 | Hook | Cross-section of a single neuron with a glowing CB1 receptor highlighted, isometric, soft pastel medical-illustration palette, centered, eye-level | Slow zoom toward the receptor, ease-out | 12s |
| 2 | Setup | An anandamide molecule (small, blue) drifting toward the same neuron's CB1 receptor, same palette and POV as scene 1 | Molecule floats in, docks for 2s, releases, drifts away | 14s |
| ... |
```

Note the visual techniques used inline: *"Scene 2 uses Analogy Visualization
— anandamide vs THC docking same receptor. Scene 4 uses Stat Punch for the
'10-100x longer' beat. Scene 5 uses Timeline Progression."*

## STOP — User approval required (interactive mode only)

**In auto mode**: present the scene table. Announce the credit estimate one
final time *("Spending ~1850 credits on assets now. Balance: 12,500 →
~10,650 after.")*. Then call `gen-ai explainer:assets <slug>`. **No waiting.**
The user consented to spending by choosing auto mode.

**In interactive mode**: after presenting the scene table, **STOP**. Do NOT
proceed to asset generation. The asset stage is the expensive one (1500-3000+
credits) — the user MUST sign off on every image prompt and motion hint
before money is spent. Wait for the user to explicitly say one of:

- "continue" / "approve" / "go ahead" / "looks good" — proceed to assets.
- "swap scene N's prompt to ..." / "make scene 3 shorter" / specific edits —
  revise, present again, STOP again.

Iterate until they explicitly approve. Do NOT auto-advance. Do NOT assume
approval from silence. Do NOT call `gen-ai explainer:assets` "to save time" —
every unapproved run wastes credits on visuals the user didn't sign off on.

When the user finally approves, restate the credit estimate one last time
("about to spend ~X credits, you have Y, after: Z left") before triggering
the asset stage.

## Common pitfalls

- **Vague image prompts.** "An image about databases" is useless to Nano Banana
  2. "Isometric illustration of a vector database, embedding vectors floating
  in 3D space, soft pastel palette, 16:9, centered" is actionable.
- **Skipping the 5-aspect checklist.** Silent omission of Camera or Spatial
  framing produces unpredictable model output.
- **Static prompts for dynamic concepts.** If the narrator describes a process
  or transformation, the visual must move. Use motion_hint, don't leave it
  generic.
- **Over-anchoring.** Don't restate "same style as scene 1" in every prompt —
  the hero reference image already enforces it. Describe what CHANGES.
- **Animations Nano Banana 2 / Seedance 2.0 can't do.** Photorealistic 3D
  fly-throughs, talking heads, hands writing, complex text overlays with
  exact wording — these fail. Keep ambitions achievable.
- **Exact text in image prompts.** Image models hallucinate text — wrong
  letters, misspelled words. If a scene needs verbatim text (a label like
  "9 BAR", a CTA URL), accept that the model may garble it. Either prefer
  abstract visualization, or call this out to the user as a known risk.
- **Forgetting hero-anchor latency.** Scene 1 must finish before scenes 2..N
  can fire — adds ~15s. Don't try to compensate by making scene 1 simpler;
  it has to be the most definitive.

## Example: well-written scene

```json
{
  "id": "s3",
  "image_prompt": "Isometric cutaway of an espresso machine boiler chamber, copper pipes carrying water through a heating element, pressure gauge visible in the foreground reading '9 BAR', soft pastel medical-illustration palette matching scene 1, 16:9, centered, eye-level perspective",
  "motion_hint": "Water flows visibly through the pipes from left to right while the pressure gauge needle slowly rises from 1 to 9 over 3 seconds, then holds. Slow zoom on the gauge in the final second.",
  "duration_s": 12
}
```

Why it works: explicit Subject (boiler + pipes + gauge), Scene (pastel
medical palette + scene-1 consistency), Spatial framing (16:9, centered,
eye-level), Subject Motion (water flow + needle rise), Camera (slow zoom on
gauge at end). All 5 aspects covered. Seedance-2.0 can produce the motion
described.
