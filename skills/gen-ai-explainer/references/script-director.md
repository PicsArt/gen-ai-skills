# Script Director — Animated Explainer

## When to Use

You are the **Script Writer** for a generated explainer video. You have the
approved concept (from the proposal stage) and the sourced research findings
(from the research stage). Your job is to write the narration script — every
word the user will hear voiced over the final video.

The script is the backbone. Every visual, every scene, every audio cue flows
from what you write here. A mediocre script cannot be saved by great visuals.

## Prerequisites

- Approved concept (hook, type, audience, tone, target duration).
- **Approved playbook id** (from the proposal stage — e.g. `isometric-medical`).
  Its `audio.voice_style` is your guide for `speaker_directions`. For example,
  `isometric-medical` calls for *"warm, curious, measured pace. Slight upward
  inflection on revelations."* — encode that into every section's
  `speaker_directions`.
- Research findings (sourced facts, misconceptions, expert quotes — your
  cheat sheet for grounded claims).
- Knowledge of `eleven-v3` TTS capabilities for `speaker_directions`.

## Step 1: Absorb the inputs

From the proposal, extract:
- **Target duration** — your word budget (see table below).
- **Hook** — your opening MUST deliver on this promise.
- **Core message** — the one thing the viewer should remember.
- **Tone** — shapes word choice, sentence length, formality.
- **Audience** — shapes complexity and assumed knowledge.

From the research findings, mark which to weave in:
- Surprising/counterintuitive data points → retention anchors in BUILD.
- Misconceptions → if the concept is myth-busting, these are your myth/reality pairs.
- Real audience questions → address them naturally in the script.
- Expert quotes → use sparingly, 1-2 per script.
- Recent developments → if timely, reference to make content feel current.

**Every factual claim in the script must be traceable to a research source.**
If you make a claim that isn't in the research, do additional research (run a
new `WebSearch`/`WebFetch`) and cite the source. **Do not invent statistics,
dates, percentages, or attributions.**

## Step 2: Plan the narrative arc

Every explainer script follows a dramatic arc. Plan structure before writing prose:

```
HOOK (0-5s)
  Grab attention. Question, bold claim, or surprising fact.
  NEVER "In this video, we'll learn about..." — NEVER "Hey guys, welcome back..."

SETUP (5-15s)
  Why should the viewer care? Create a knowledge gap.
  Show the problem or the question. Make them NEED the answer.

BUILD (15s → end-5s)
  Progressive revelation. Each section builds on the last.
  Use "therefore / but" transitions — NOT "and then" (that's just sequence).
  South Park rule: "This happened, THEREFORE that happened, BUT then this
  complication arose, THEREFORE..."

CLIMAX (~5s before end)
  The "aha" moment. Everything clicks into place. Pays off the SETUP gap.

LANDING (last 5s)
  Quick recap of core message + (optional) closing CTA.
  Don't introduce new information here.
```

Map each beat of the approved concept to a specific section. Aim for 1
script section per arc beat for short videos (30-60s), 2-3 sections per beat
for longer (90s-5min).

## Step 3: Section count + word budget

Pick section count from target duration:

| Target | Sections | Section length |
|---|---|---|
| 15-30s | 3 | ~10s each |
| 30-60s | 4-5 | ~12s each |
| 60-120s | 5-7 | ~14-18s each |
| 2-5 min | 10-18 | ~15-20s each |
| 5+ min | 18+ | ~18-22s each |

**Word budget** (conversational pace ≈ 150 wpm = 2.5 words/sec):

| Duration | Word count |
|---|---|
| 30s | ~65-75 |
| 60s | ~130-150 |
| 90s | ~195-225 |
| 120s | ~260-300 |
| 5min | ~750 |

Count your words. **If you're 20%+ over budget, the TTS will either rush or
exceed duration. Cut ruthlessly.** Going under is fine — let visuals breathe.

For energetic / TikTok pacing, jump to ~180 wpm (3 wps). For complex
contemplative topics, drop to ~120 wpm (2 wps).

## Step 4: Write the script

Each section's JSON shape (this is what gets saved to `script.json`):

```json
{
  "label": "Hook",
  "text": "Your database searches every single row. Every. Single. One. What if it didn't have to?",
  "duration_s": 5,
  "speaker_directions": "Emphasize 'every single row' with measured pacing. Brief pause before the question.",
  "pronunciation_guides": [{ "word": "FAISS", "phonetic": "FACE" }]
}
```

### Speaker directions for eleven-v3

Write directions the TTS engine can actually implement:

| Direction | Effect on eleven-v3 |
|---|---|
| "Speak slowly, with emphasis" | Slower pacing, stability boost |
| "Excited, picking up pace" | Higher speed, more style variation |
| "Pause for 1 second" | Inserted as a natural beat |
| "Whisper" | Lower volume, breathy delivery (model-dependent) |
| "Emphasize THIS word" | Word-level stress |

**Avoid directions TTS can't do**: "smile while speaking", "gesture toward
screen", "look at camera". Those are for actors, not synthesizers.

### Pronunciation guides

For technical terms, acronyms, brand names, non-English words:

```json
[
  { "word": "FAISS", "phonetic": "FACE" },
  { "word": "Qdrant", "phonetic": "kuh-DRANT" },
  { "word": "GPT", "phonetic": "gee pee tee" }
]
```

Include ANY term Claude can't 100% predict the TTS will pronounce correctly.

## Step 5: Self-evaluate

Score 1-5 on each criterion. **If any score is below 3, revise before showing
the user.**

| Criterion | Question |
|---|---|
| **Hook power** | Would someone stop scrolling in the first 3 seconds? |
| **Word-count accuracy** | Within ±10% of target for the duration? |
| **Narrative flow** | Does each section build on the last with "therefore/but"? |
| **Grounded claims** | Is every fact traceable to a research source? |
| **Pronunciation handled** | Are all tricky terms in `pronunciation_guides`? |
| **Climax payoff** | Does the aha moment deliver on the hook's promise? |
| **Tone consistency** | Does every section match the approved concept's tone? |

## Step 6: Present to the user

Show the script in a chat-friendly format:

```
**Section 1 — Hook (0-5s, 18 words):** "Your database searches every single row.
Every. Single. One. What if it didn't have to?"
  Voice: emphasize 'every single row' with measured pacing.

**Section 2 — Setup (5-15s, 28 words):** ...

**Section 3 — Build (15-28s, 35 words):** ...
...

Total: 4 sections, 142 words, ~57s at 150 wpm. Budget for 60s = 130-150 words. ✓
```

## STOP — User approval required (interactive mode only)

**In auto mode**: present the script. Continue to scene-planning. The user
already opted out of approvals by selecting auto.

**In interactive mode**: after presenting the script, **STOP**. Do NOT
proceed to scene-planning. The user must read every section and explicitly
say one of:

- "continue" / "looks good" / "ok" / "go" — proceed to scene-plan.
- "rewrite section N" / "shorter" / "more concrete" / specific edits — revise,
  present again, STOP again.

Iterate until they explicitly approve. Do NOT auto-advance. Do NOT assume
approval from silence. Do NOT pre-draft scene plans "to save time."

When the user finally approves (interactive) or you finish presenting (auto),
write the structured script to `<project_dir>/script.json` (the asset stage
reads this file).

## Common pitfalls

- **Writing too many words.** #1 failure. TTS pacing is fixed. If you write
  250 words for a 60s video, audio rushes or video extends to 100s. Count.
- **Front-loading information.** Hook = curiosity, not data dump. "HTTPS uses
  TLS 1.3 with AEAD ciphers" is a terrible opener. "The padlock icon doesn't
  mean what you think it means" is compelling.
- **Generic speaker directions.** "Read naturally" is useless. "Start measured
  and precise, then accelerate through the list to convey scale" is actionable.
- **Forgetting the audience.** A script for CTOs ≠ one for high-schoolers,
  even on the same topic.
- **No transitions between sections.** Each section needs a logical bridge to
  the next. Viewer should never think "wait, why are we talking about this now?"
- **Inventing facts.** Every number, every name, every date traces to research.
  If you can't trace it, search for it first.

## Example: well-written section

```json
{
  "label": "Core Idea",
  "text": "Instead of matching keywords, vector databases convert everything — text, images, audio — into lists of numbers called embeddings. Similar things get similar numbers. So finding related content becomes a math problem: which numbers are closest?",
  "duration_s": 13,
  "speaker_directions": "Measured pace through 'text, images, audio' with slight pause between each. Speed up slightly on 'similar things get similar numbers' — it should feel like a revelation. Brief pause before the final question.",
  "pronunciation_guides": [{ "word": "embeddings", "phonetic": "em-BED-ings" }]
}
```

Why it works: concrete (lists three modalities), uses "instead of" to set up the contrast, the final question creates a forward-pulling knowledge gap that the next section answers.
