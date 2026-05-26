# Render Director — Animated Explainer

You make the CLI compose the final mp4 from the asset manifest.

## Run

```bash
gen-ai explainer:render <slug>
```

The CLI reads the active playbook from `asset-manifest.playbook` and applies
its `audio.music_volume_db` and `audio.narration_to_music_weight_ratio` to
the ffmpeg mix — no manual audio tuning needed. The CLI announces the playbook
in stderr (`◇ playbook: …`); relay it to the user as confirmation.

Default visuals: 1920x1080, 30fps, h264. Only pass flags if the user asked for
something custom:
- `--width <px>` / `--height <px>`
- `--fps <n>`

Wall time: ~1-3 min depending on duration.

## Parse the result

```json
{ "status": "ok", "output_path": "...", "duration_s": N,
  "resolution": "1920x1080", "fps": 30, "codec": "h264", "elapsed_ms": ... }
```

## Hand off

Now draft the metadata (title / description / chapters / hashtags) in chat,
then run:

```bash
gen-ai upload-to-drive <slug>/explainer.mp4 --name "<the title>"
```

Share the returned `drive_url` with the user.
