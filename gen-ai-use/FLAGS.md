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

Use `gen-ai models info <id>` to confirm what a specific model supports.

| Pattern | Flag usage |
|---------|------------|
| Multi-image (models that accept multiple inputs) | `--image` repeated (up to 14) |
| Start frame (i2v / keyframe video models) | `--image` (auto-mapped to startFrame) |
| End frame (Luma) | Prompted interactively after start frame |
| Image + audio (avatar / lipsync models) | `--image` + `--audio` |
| Image + video (motion-control models) | `--image` + `--video` |

## Full command list

### Auth
```bash
gen-ai login          # OAuth browser login
gen-ai logout         # Clear stored credentials
gen-ai whoami         # Show current user
```

### Generation
```bash
gen-ai generate       # Generate image/video/audio (interactive or flags)
gen-ai remove-bg      # Remove background from an image
gen-ai change-bg      # Replace background using a prompt
gen-ai enhance        # Upscale or enhance an image
gen-ai vectorize      # Convert a raster image to SVG
gen-ai redo           # Re-run last generation (accepts generate flags as overrides)
gen-ai extend         # Extend a VEO video by +7s (chainable with --times)
```

### Models, pricing & credits
```bash
gen-ai models                    # List all models (filter with --mode, --provider)
gen-ai models info <id>          # Model capabilities, inputs, aspect ratios
gen-ai models compare <a> <b>    # Side-by-side comparison
gen-ai pricing <model-id>        # Credit cost for a model
gen-ai credits                   # Show current credit balance
gen-ai validate -m <id>          # Validate payload against model schema
```

### Batch
```bash
gen-ai batch run manifest.json   # Run batch jobs from manifest
gen-ai batch status <dir>        # Summary of a prior run
gen-ai batch resume <dir>        # Retry only failed jobs
```

### Drive
```bash
gen-ai upload <files>            # Upload to Picsart Drive
gen-ai download                  # Download from Picsart Drive
gen-ai list                      # List Drive files/folders
```

### Config
```bash
gen-ai config get <key>          # Get a setting
gen-ai config set <key> <value>  # Set a preference
gen-ai config list               # Show all settings
gen-ai config unset <key>        # Remove a preference
gen-ai config keys               # List valid config keys
```

Config persists to `~/.gen-ai/config.json`. Valid keys: `defaultModel`, `downloadDir`, `autoOpen`, `autoClipboard`, `autoBell`, `autoNotify`, `recentFilesCount`, `imagePreview`, `autoUpdate`.

### History
```bash
gen-ai history                   # Recent generations (default 20)
gen-ai history last              # Details of the last generation
gen-ai history files             # Recently used input files
gen-ai history clear             # Clear all history
```

### Utilities
```bash
gen-ai completion <shell>        # Shell completions (bash, zsh, fish)
gen-ai update                    # Self-update to latest version
```
