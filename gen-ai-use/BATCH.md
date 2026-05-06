# Batch Generation

Run many `gen-ai` generations from a single manifest file.

## Contents

- Batch workflow checklist
- Commands and key flags
- Manifest schema
- Output format (`results.json`)
- Parallel stress test (N variants of one model)
- Summarizing a run

## Batch workflow checklist

Copy this checklist and check off items as they complete:

```
Batch run progress:
- [ ] Write manifest.json ({ defaults?, jobs[] })
- [ ] Validate with `gen-ai batch run manifest.json --dry-run`
- [ ] Execute with `gen-ai batch run manifest.json -c <n> -o <dir>`
- [ ] Inspect <dir>/results.json for entries where status !== "completed"
- [ ] Retry failures with `gen-ai batch resume <dir>/results.json`
- [ ] Summarize durations / success rate (see "Summarizing a run" below)
```

## Commands

```bash
gen-ai batch run manifest.json                         # default concurrency = 3
gen-ai batch run manifest.json -c 20 -o ./out          # 20 parallel jobs, custom output dir
gen-ai batch run manifest.json --dry-run               # validate without executing
gen-ai batch resume ./out/results.json                 # retry only failed jobs
gen-ai batch status ./out/results.json                 # summary of a prior run
```

Key flags: `-c, --concurrency <n>` (default 3), `-o, --output <dir>` (default `./batch-output`), `--no-download` (skip file download), `--download-concurrency <n>` (default 3), `--dry-run`.

JSON is the safest manifest format. YAML is also accepted.

## Manifest schema

Top-level is `{ defaults?, jobs[] }`. Each job needs a unique `id`, a `model`, and a `prompt`. Any extra keys become per-job params and override `defaults`. Image-edit models accept `image: <local-path|url>`.

```json
{
  "defaults": { "aspect_ratio": "1:1" },
  "jobs": [
    { "id": "hero",   "model": "flux-2-pro",             "prompt": "sunset over mountains", "aspect_ratio": "16:9" },
    { "id": "cat",    "model": "gemini-3.1-flash-image", "prompt": "a cat in space" },
    { "id": "remix",  "model": "flux-kontext-pro",       "prompt": "make it watercolor",    "image": "./src.jpg" }
  ]
}
```

There is **no `count:` field** — to get N variants of the same prompt, emit N jobs with unique `id`s (see stress-test recipe below).

## Output

Per manifest: `<output>/<job-id>.<ext>` for each downloaded asset, plus `<output>/results.json` summarizing all jobs. Each job entry looks like:

```json
{ "id": "hero", "model": "flux-2-pro", "status": "completed",
  "url": "https://cdn-pipeline-output.picsart.com/...png",
  "durationMs": 22306, "localPath": "out/hero.png" }
```

`status` is `"completed"` on success (not `"success"`). Filter failures with `status !== "completed"`.

## Parallel stress test (N variants of one model)

Generate 20 varied prompts for the same model at full concurrency. Pattern used for `gemini-3.1-flash-image` (Nano Banana 2):

```bash
cat > /tmp/nb2.json <<'JSON'
{
  "defaults": { "aspect_ratio": "1:1" },
  "jobs": [
    { "id": "01-neon-city",     "model": "gemini-3.1-flash-image", "prompt": "neon cyberpunk street at night, rain reflections" },
    { "id": "02-koi-pond",      "model": "gemini-3.1-flash-image", "prompt": "overhead koi pond with lily pads" },
    { "id": "03-astronaut-cat", "model": "gemini-3.1-flash-image", "prompt": "astronaut cat floating in space, earth in visor" }
  ]
}
JSON
# Note: to run 20 jobs, repeat the same object shape for ids 04..20 with distinct prompts.
# JSON does not support comments, so do not paste a "/* ... */" placeholder into the manifest.

gen-ai batch run /tmp/nb2.json -c 20 -o ./batch-output/nb2-parallel
```

With `-c 20` all 20 jobs are submitted before the first finishes — check the per-job `ACCEPTED` timestamps in stdout to verify true parallelism. Backend may retry slow jobs internally (re-emits `ACCEPTED` at higher elapsed times); that's not a concurrency issue on the client.

For a ready-made runner in this repo, see `scripts/parallel-nb2-test.sh` (env vars: `COUNT`, `CONCURRENCY`, `MODEL`, `OUT_DIR`).

## Summarizing a run

```bash
node -e '
  const r = require("./batch-output/nb2-parallel/results.json");
  const jobs = r.jobs || [];
  const ok = jobs.filter(j => j.status === "completed");
  const durations = ok.map(j => j.durationMs).sort((a,b) => a-b);
  console.log(`${ok.length}/${jobs.length} ok`);
  console.log(`fastest ${(durations[0]/1000).toFixed(1)}s, slowest ${(durations.at(-1)/1000).toFixed(1)}s`);
'
```
