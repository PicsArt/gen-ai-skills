# Asset Director — Animated Explainer

You make the CLI generate all media in parallel. This is the expensive stage.

## Pre-flight

1. Project dir: ensure `gen-ai explainer:new <slug>` ran and `<slug>` exists under
   `~/.gen-ai/projects/explainer/`.
2. Write `scene-plan.json` (including the `playbook` field at the top!) and
   `script.json` into the project dir using the shapes from
   `scene-plan-director.md` and `script-director.md`.
3. Re-state the credit estimate ("about to spend ~X credits") and the active
   playbook ("using `isometric-medical` for the medical-illustration look").
4. **Interactive mode**: wait for explicit "go" from the user. **Auto mode**:
   skip the wait — announce and immediately fire.

## Run

```bash
gen-ai explainer:assets <slug>
```

The CLI announces the active playbook in stderr (`◇ playbook: Isometric
Medical (isometric-medical)`) — relay that line to the user as confirmation
the right playbook is being applied. The CLI then auto-prepends the
playbook's `image_prompt_prefix` to every image generation, passes
`image_negative_prompt` as `negative_prompt`, and uses `music_mood` as the
music model's prompt.

Optional overrides (only if the user asked):
- `--playbook <id>` (override the scene-plan.json field if the user said "swap to noir-tech")
- `--image-model <id>` (default `gemini-3.1-flash-image`)
- `--video-model <id>` (default `seedance-2.0`)
- `--voice <id>` (default `eleven-v3`)
- `--music-model <id>` (default `minimax-music`)
- `--no-hero-anchor` (only if the user wants no style anchor)

Wall time: ~30 sec/scene + 60 sec overhead. A 5-min video may take 20-30 min.
Tell the user before running.

## Parse the result

The CLI prints a single JSON object on stdout:

```json
{ "status": "ok", "scene_count": N, "total_credits": X,
  "credits_by_stage": {...}, "asset_manifest": "/.../asset-manifest.json", ... }
```

If `"status": "error"`, read `"hint"` and decide:
- Transient network failure → re-run the same command.
- Rate limit / credits exhausted → tell the user, stop.
- Schema error in scene-plan.json → re-write the file, re-run.

## Hand off

Once `asset-manifest.json` exists in the project dir, move to the render stage.
