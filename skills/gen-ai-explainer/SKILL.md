---
name: gen-ai-explainer
description: Use when the user wants a short animated explainer video. Trigger phrases include "animated explainer", "make an explainer", "explainer video about X", "30-second video about Y", "90-second video explaining Z", "how X works as a video", "explain X in a short video".
---

# Animated Explainer Workflow (Light Producer)

You drive a 6-stage pipeline. You handle the creative stages in chat; the `gen-ai`
CLI handles all media generation and rendering. State lives in
`~/.gen-ai/projects/explainer/<slug>/` as JSON files.

## The 6 stages — FOUR are hard approval gates

Every creative stage is a hard stop. You do the work, present it, then **STOP**
and wait for the user. Do NOT chain stages without explicit user approval.

1. **research** — you, in chat. Read `references/research-director.md`. **STOP after presenting findings.**
2. **proposal** — you, in chat. Read `references/proposal-director.md`. **Pick a playbook with each concept.** **STOP until the user picks A / B / C.**
3. **script** — you, in chat. Read `references/script-director.md`. Read the chosen playbook's `audio.voice_style` and reflect it in `speaker_directions`. **STOP after showing the script.**
4. **scene_plan** — you, in chat. Read `references/scene-plan-director.md`. **Include the `playbook` field at the top of `scene-plan.json`.** **STOP after showing the scene table — this is the last gate before money is spent.**
5. **assets** — CLI (~1500-3000 credits, 5-25 min wall time). Read `references/asset-director.md`. Write `scene-plan.json` (with `playbook` field) and `script.json` into the project dir. Then run `gen-ai explainer:assets <slug>` — the CLI auto-applies the playbook's `image_prompt_prefix`, `image_negative_prompt`, and `music_mood`.
6. **render** — CLI (~1-3 min). Read `references/render-director.md`. Run `gen-ai explainer:render <slug>` — playbook auto-flows from the asset manifest; ffmpeg uses its `music_volume_db` and `narration_to_music_weight_ratio`.

After stage 6: draft title / description / chapters / hashtags in chat. Then run
`gen-ai upload-to-drive <slug>/explainer.mp4 --name "<title>"`. Share the URL.

## Rule Zero — Read the director skill before EVERY stage

Each of the 6 stages has a dedicated director skill at
`~/.claude/skills/gen-ai-explainer/references/<stage>-director.md`. You **MUST** read
the director skill BEFORE executing each stage. Not after. Not skimmed. Read.

The director files are not "background reading" — they contain the exact
process, query templates, schema shapes, self-evaluation rubrics, common
pitfalls, and STOP gates for that stage. Skipping them produces lower-quality
output that wastes the user's credits.

### Skill-loading protocol (apply at the START of every stage)

1. **Announce in chat**: *"Loading `references/<stage>-director.md`."* One line. So the
   user sees you're following the protocol.
2. **Read the file** with the Read tool. The full file.
3. **Follow its Process steps exactly.** Don't improvise — the directors
   were written precisely so you don't have to invent the workflow each time.
4. When the director's STOP gate fires, **STOP**. Don't pre-load the next director.

### Stage → director mapping (memorize this)

| Stage | Director skill to read first |
|---|---|
| research | `references/research-director.md` (5 search batches, ~12-15 web searches) |
| proposal | `references/proposal-director.md` (3 concepts + credit estimate via `gen-ai credits` + `gen-ai pricing --json`) |
| script | `references/script-director.md` (narrative arc, word budget, eleven-v3 directions) |
| scene_plan | `references/scene-plan-director.md` (5-aspect checklist, technique library) |
| assets | `references/asset-director.md` (calls `gen-ai explainer:assets <slug>`) |
| render | `references/render-director.md` (calls `gen-ai explainer:render <slug>`) |

### Do NOT (skill-loading violations)

- Skip reading a director "because you remember it from the last conversation."
- Read directors in batches "to save round-trips" — fresh context per stage.
- Improvise a stage from your general knowledge instead of following the
  director's specific process.
- Carry stale director content from a previous stage into the current one
  (e.g., applying scene-plan rules to the script stage).
- Silently drop director-mandated steps (web searches, self-evaluation,
  pronunciation guides) "to be faster."

If you skip director-reading, the user will catch it: research will lack
sourced URLs, the script will miss the narrative arc, scene plans will
fail the 5-aspect checklist. Sub-quality output betrays the protocol.

## Rule One — Approval gates are non-negotiable

The four creative stages (research / proposal / script / scene_plan) each
end with a **hard STOP**. After presenting your output:

- WAIT for the user to reply.
- If they say "continue" / "looks good" / "approve" / "go" — proceed to the next stage.
- If they say "edit X" / "rewrite Y" / "swap N" — revise, present again, STOP again.
- Iterate until they explicitly approve.

**Do NOT:**
- Auto-advance to the next stage without user reply.
- Pre-draft the next stage "to save time" while waiting.
- Assume approval from silence.
- Skip showing the artifact to the user.
- Collapse multiple stages into one message.

If you skip a gate, the user pays for visuals they didn't sign off on. The
whole point of this pipeline is human-in-the-loop creative control.

## Other rules

- The asset stage is expensive (~1500-3000 credits for 30-90s). Announce the
  credit estimate before running, and confirm one more time at the start of
  stage 5.
- If a CLI call fails, read the error JSON's `hint` field and decide whether
  to retry, re-plan, or surface to the user.
- Never override the default models unless the user asks. Defaults are:
  - image: `gemini-3.1-flash-image` (Nano Banana 2)
  - video: `seedance-2.0`
  - voice: `eleven-v3`
  - music: `minimax-music`

## Resume protocol

If the user references an existing project, run `ls ~/.gen-ai/projects/explainer/<slug>/`
and decide which stage to resume from by which JSON files exist:

| Files present | Resume from |
|---|---|
| only `manifest.json` | stage 3 (script) |
| `script.json` | stage 4 (scene_plan) |
| `scene-plan.json` | stage 5 (assets) |
| `asset-manifest.json` | stage 6 (render) |
| `render-report.json` | upload step |

See `references/pipeline.yaml` for the machine-readable manifest.
