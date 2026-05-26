# gen-ai — flags & commands reference

Run `gen-ai <command> --help` for the authoritative, version-current help. This file is a quick-scan companion.

## Generate flags

| Flag | Alias | Description |
|------|-------|-------------|
| `--model` | `-m` | Model ID, name, or workflow |
| `--prompt` | `-p` | Generation prompt |
| `--prompt-file` | | Read prompt from file (multi-line) |
| `--image` | `-i` | Input image path or URL (repeatable) |
| `--video` | | Input video path or URL |
| `--audio` | | Input audio path or URL |
| `--duration` | `-d` | Video duration in seconds |
| `--aspect-ratio` | `--ar` | Aspect ratio (e.g. 16:9) |
| `--resolution` | `-r` | Resolution (e.g. 1080p) |
| `--count` | `-n` | Number of outputs |
| `--quality` | | Quality setting |
| `--style` | | Style preset |
| `--negative-prompt` | | Negative prompt |
| `--cfg-scale` | | CFG scale (guidance strength) |
| `--image-weight` | | Image weight (influence of input image) |
| `--generate-audio` / `--no-generate-audio` | | Enable/disable audio for video models |
| `--enhance-prompt` | | Enable prompt enhancement |
| `--seed <N>` | | Reproducible output (broadly supported across image models) |
| `--dry-run` | | Validate payload without executing |
| `--silent` | `-s` | Skip interactive prompts, use model defaults |
| `--script` | | Shorthand for `--silent --quiet --json` |
| `--download <dir>` | | Download to directory (default: `./output`) |
| `--no-download` | | Don't download result |
| `--save-to-drive` / `--no-save-to-drive` | | Save to Picsart Drive (on by default) |
| `--drive-folder <name>` | | Drive subfolder (default: `gen-ai-cli`) |
| `--open` / `--no-open` | | Open result in default app |
| `--clipboard` | | Copy result URL to clipboard |
| `--bell` | | Play terminal bell on completion |
| `--notify` | | Send desktop notification on completion |

Model-specific flags (e.g. `--voice`, `--language`, `--rendering-speed`, `--video-id`, `--remove-bg-noise`, `--source-image-id`, `--similarity`) are not listed here — run `gen-ai models info <id>` to see what a given model accepts.

## Directory input flags (generate)

| Flag | Description |
|------|-------------|
| `--input-dir <dir>` | Use all files in directory as input |
| `--multi` | Multi-image mode (all files to one generation, max 14) |
| `--batch` | Batch mode (one generation per file) |
| `--type` | Filter input files: image, video, audio |
| `--max-files <n>` | Max input files (default: 30) |
| `--concurrency <n>` | Parallel batch jobs (default: 3) |

## Base flags (all commands)

| Flag | Alias | Description |
|------|-------|-------------|
| `--json` | | Output as JSON |
| `--plain` | | Plain tabular output (no formatting) |
| `--quiet` | `-q` | Suppress non-essential output |
| `--no-color` | | Disable color output |
| `--no-input` | | Disable all interactive prompts |
| `--debug` | | Show debug output |

## Special input patterns

Use `gen-ai models:info <id>` (or `models info <id>`) to confirm what a specific model supports.

| Pattern | Flag usage |
|---------|------------|
| Multi-image (models that accept multiple inputs) | `--image` repeated (descriptor `array.max`) |
| Start frame (i2v / keyframe video models) | `-i` (auto-routes to `startFrame` when that's the model's only image input), or `--start-frame` explicitly |
| End frame | `--end-frame` |
| Image + audio (talking-photo / avatar / lipsync) | `-i` + `--audio` |
| Image + video (motion-control models like `kling-motion-control-v3`) | `-i` + `--video` |
| Reference video (Seedance extend) | `--reference-video <mp4>` (repeats up to descriptor max) |
| Multi-shot prompts (Kling V3) | `--multi-shot --shot-type customize` + repeated `--multi-prompt-prompt` / `--multi-prompt-duration` |

The old `--ref-image` / `--ref-video` / `--ref-audio` short flags were dropped when the SDK consolidated those descriptors into `imageUrls` / `videoUrls` / `audioUrls`. Pass references via `-i`, `--video-urls`, `--audio-urls`.

## Full command list

### Auth
```bash
gen-ai login          # OAuth browser login
gen-ai logout         # Clear stored credentials
gen-ai whoami         # Show current user
```

### Operations — CREATE
```bash
gen-ai generate          # Universal — any model
gen-ai image             # Text → image
gen-ai video             # Text → video
gen-ai image-to-video    # Animate a still
gen-ai music             # Text → music
gen-ai sfx               # Text → sound effect
gen-ai text-to-speech    # Synthesize spoken audio
gen-ai audio-from-text   # Generic text → audio
gen-ai talking-photo     # Photo + voice → lip-synced video
gen-ai character         # Consistent-character images
gen-ai multi-image       # Combine multiple inputs into one output
```

### Operations — EDIT
```bash
gen-ai remove-bg         # Strip background
gen-ai change-bg         # Prompt-replace background
gen-ai enhance           # Restore at same resolution
gen-ai upscale           # Increase resolution
gen-ai edit-image        # NL image editing
gen-ai voice-clone       # Convert speech to another voice (audio → audio)
gen-ai video-edit        # v2v transform / extend (Seedance / Wan / LTX / Sora)
gen-ai video-audio       # Generate an audio track for a video
gen-ai extend            # VEO-only +7s chain (use video-edit for other vendors)
```

### Operations — UTILITY
```bash
gen-ai vectorize         # Raster → SVG
```

### Meta
```bash
gen-ai redo              # Re-run last generation (accepts generate flags as overrides)
```

### Models, pricing & credits
```bash
gen-ai models                       # List all models (filter --mode, --provider, --input-type, --params)
gen-ai models:info <id>             # (or `models info <id>`) — capabilities, inputs, defaults
gen-ai models:compare <a> <b>       # Side-by-side comparison
gen-ai pricing <model-id>           # Credit cost for a model
gen-ai credits                      # Show current credit balance
gen-ai validate -m <id>             # Validate payload against model schema
```

### Batch
```bash
gen-ai batch:run manifest.json      # Run batch jobs from manifest
gen-ai batch:status <dir>           # Summary of a prior run
gen-ai batch:resume <dir>           # Retry only failed jobs
```

### Drive
```bash
gen-ai upload <files>            # Upload to Picsart Drive
gen-ai download                  # Download from Picsart Drive
gen-ai list                      # List Drive files/folders
```

### Config
```bash
gen-ai config:get <key>          # Get a setting
gen-ai config:set <key> <value>  # Set a preference
gen-ai config:list               # Show all settings
gen-ai config:unset <key>        # Remove a preference
gen-ai config:keys               # List valid config keys
```

Config persists to `~/.gen-ai/config.json`. Valid keys: `defaultModel`, `downloadDir`, `autoOpen`, `autoClipboard`, `autoBell`, `autoNotify`, `recentFilesCount`, `imagePreview`, `autoUpdate`.

### History
```bash
gen-ai history                   # Recent generations (default 20)
gen-ai history:last              # Details of the last generation
gen-ai history:files             # Recently used input files
gen-ai history:clear             # Clear all history
```

### Utilities
```bash
gen-ai completion <shell>        # Shell completions (bash, zsh, fish)
gen-ai update                    # Self-update to latest version
```
