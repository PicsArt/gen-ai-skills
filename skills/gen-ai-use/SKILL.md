---
name: gen-ai-use
description: Generate AI images, videos, audio via Picsart gen-ai CLI.
version: 1.3.0
author: Picsart
license: MIT
allowed-tools: Read, Bash, Grep, Glob
platforms: [macos, linux]
metadata:
  hermes:
    category: creative
    tags: [picsart, cli, image-generation, video-generation, audio-generation]
---

# gen-ai CLI — Usage Guide

The `gen-ai` CLI generates AI images, videos, and audio from the terminal via the Picsart API.

## When to Use

_See the description above._

## Prerequisites

Picsart `gen-ai` CLI installed and authenticated (`gen-ai login`).

## How to Run

_Use the agent's `terminal` tool to invoke `gen-ai` commands as described in the Procedure below._

## Quick Reference

- **Auth:** `login`, `logout`, `whoami`
- **Generation:** `generate`, `remove-bg`, `change-bg`, `enhance`, `vectorize`, `redo`, `extend`
- **Models / pricing:** `models`, `models info`, `models compare`, `pricing`, `credits`, `validate`
- **Batch:** `batch run`, `batch status`, `batch resume`
- **Drive:** `upload`, `download`, `list`
- **Config:** `config get | set | list | keys | unset`
- **History:** `history`, `history last`, `history files`, `history clear`
- **Utilities:** `completion`, `update`

Run `gen-ai <command> --help` for full flag details, or see [references/FLAGS.md](references/FLAGS.md).

## Procedure

_See sections below for the detailed walkthrough._

## Pitfalls

- **Stale model ID** — using a name from memory that's been renamed/removed → run `gen-ai models` first or `gen-ai validate -m <id>`.
- **Passing `--image` to a non-i2v video model** — it's silently ignored, not auto-mapped. Confirm with `gen-ai models info <id>`.
- **Forgetting `--no-input` in CI** — the CLI sits waiting for an interactive prompt and the job times out. Always pair `--script` (or `--no-input`) with non-TTY contexts.
- **Mixing `--multi` and `--batch`** — they're mutually exclusive `--input-dir` modes; pick one.

## Verification

Run `gen-ai whoami` to confirm authentication, then re-run the failed command with `--debug`.

## Where to look

- **Flags & full command list** → [references/FLAGS.md](references/FLAGS.md)
- **Batch generation** (manifests, concurrency, stress tests) → [references/BATCH.md](references/BATCH.md)
- **Picsart Drive** (upload, download, list) → [references/DRIVE.md](references/DRIVE.md)
- **Advanced** (validate, extend VEO, interactive mode, piping) → [references/ADVANCED.md](references/ADVANCED.md)
- **Troubleshooting** (dry-run, debug, common errors) → [references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)
- **Example workflows** (image → video, cross-model comparison) → [references/EXAMPLES.md](references/EXAMPLES.md)
- **Shell completions** (bash, zsh, fish) → [references/COMPLETIONS.md](references/COMPLETIONS.md)

## When NOT to use

- SDK-level integration questions → consult the `@picsart/ai-sdk` reference / `specs/` source
- Picsart web miniapp or mobile flows → unrelated
- New backend models that aren't in the catalog yet → backend MR first; CLI picks them up automatically once they ship in `@picsart/ai-sdk`

## Install & auth

```bash
# Signed binary (no Node required) — recommended
curl -fsSL https://picsart.com/gen-ai-cli/install.sh | bash

# Or via npm (requires Node 22+)
npm install -g @picsart/gen-ai

gen-ai login     # OAuth browser flow
gen-ai whoami    # verify
```

## Generate

```bash
# Interactive wizard
gen-ai generate

# Image, fully specified
gen-ai generate -m flux-2-pro -p "a sunset over mountains" -s

# Image-to-image
gen-ai generate -m gemini-3.1-flash-image -i ~/photo.jpg -p "make it watercolor"

# Text-to-video
gen-ai generate -m kling-v3-pro -p "a cat playing piano" --ar 16:9

# Image-to-video (--image is auto-mapped to startFrame for i2v models)
gen-ai generate -m veo-3.1 -i ~/photo.jpg -p "camera zooms in" -d 5
```

## Image operations

```bash
gen-ai remove-bg -i photo.jpg
gen-ai change-bg -i photo.jpg -p "tropical beach sunset"
gen-ai enhance   -i photo.jpg                       # upscale / enhance
gen-ai vectorize -i logo.png                        # raster → SVG
```

All operation commands accept the same output flags as `generate` (`--download`, `--save-to-drive`, `--drive-folder`, `--open`, `--clipboard`, `--json`, `--quiet`, etc.). See [references/FLAGS.md](references/FLAGS.md).

## Browse models, check pricing

Model IDs change as new versions ship — always check the live catalog:

```bash
gen-ai models                       # list (filter --mode, --provider)
gen-ai models info <id>             # capabilities, inputs, aspect ratios
gen-ai models compare <a> <b>       # side-by-side
gen-ai pricing <model-id>           # credit cost
gen-ai credits                      # remaining balance
```

## Important defaults

- **Drive auto-save** — results save to Picsart Drive in folder `gen-ai-cli` by default. Disable with `--no-save-to-drive`; use `--drive-folder NAME` for a custom folder.
- **startFrame mapping** — for i2v models (VEO, Kling i2v, Wan, Luma, Seedance, Runway), `-i / --image` is auto-mapped to `ctx.startFrame`.
- **Script mode** — `--script` = `--silent --quiet --json`, the right combo for piping or CI.
- **CI mode** — pass `--no-input` to fail fast instead of hanging on interactive prompts.

## When to reach for the reference files

- Many generations at once, or retry/resume → [references/BATCH.md](references/BATCH.md)
- Files in/out of Drive → [references/DRIVE.md](references/DRIVE.md)
- Validation, VEO extension, scripting → [references/ADVANCED.md](references/ADVANCED.md)
- A command is failing → [references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)
- Chaining (image → video) or comparing models → [references/EXAMPLES.md](references/EXAMPLES.md)
- Tab completion → [references/COMPLETIONS.md](references/COMPLETIONS.md)
- All flags / all commands → [references/FLAGS.md](references/FLAGS.md)
