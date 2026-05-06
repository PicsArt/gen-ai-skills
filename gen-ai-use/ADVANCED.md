# Advanced features

Commands and modes that go beyond a single `gen-ai generate` call.

## Contents

- Validate (schema + payload check)
- Extend (VEO video extension)
- Interactive mode
- Piping and scripting
- Global flags and auth injection

## Validate

Inspect the parameter schema for a model or check a payload before sending it. Useful for building manifests and debugging `"Invalid parameter"` errors.

```bash
gen-ai validate --model <id> --schema                    # Print parameter schema
echo '{"prompt":"test"}' | gen-ai validate --model <id>  # Validate via stdin
gen-ai validate --model <id> --file payload.json         # Validate from a file
```

For previewing a full request without sending it, use `gen-ai generate --dry-run --debug` — see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## Extend

Extend a VEO video by +7 seconds per iteration. Chainable.

```bash
gen-ai extend --video ./clip.mp4                    # +7s extension
gen-ai extend --video ./clip.mp4 --model <veo-id>   # Specific VEO model
gen-ai extend --video ./clip.mp4 --times 3          # Chain 3 extensions (+21s)
gen-ai extend --video ./clip.mp4 --download --open  # Download + open result
gen-ai extend --video ./clip.mp4 --json             # JSON output
```

| Flag | Default | Description |
|------|---------|-------------|
| `--video` | (required) | Video file or URL to extend |
| `--model, -m` | (latest VEO) | Must be a VEO model — use `gen-ai models --provider google` to list |
| `--times` | 1 | Number of +7s extensions to chain |

## Interactive mode

When running without `--silent` in a TTY, operation commands walk through a wizard:

1. **Model** → fuzzy-searchable model picker (filtered to models supporting the operation)
2. **Files** → source picker: drop/paste local path, Picsart Drive browse, or URL input
3. **Parameters** → step-by-step param wizard (aspect ratio, resolution, duration, etc.)
4. **Prompt** → rich text input with arrow-key cursor movement (for commands that need a prompt)
5. **Confirm** → summary card with options: Run, Edit parameters, Change files

Navigation: `Esc` = back one step, `Ctrl+C` = cancel. Any CLI flag provided pre-fills its step.

Each operation command (`generate`, `remove-bg`, `change-bg`, `enhance`, `vectorize`) uses this same wizard pattern but with operation-specific model filters and required inputs.

To skip all prompts and use model defaults, pass `--silent` (`-s`).

## Piping and scripting

The CLI is pipe-friendly. Stream separation: data → stdout, errors → stderr, spinners → stderr.

### Output control flags

| Flag | Effect |
|------|--------|
| `-s, --silent` | Skip interactive prompts, use model defaults |
| `-q, --quiet` | Suppress info/success/spinner output (errors still on stderr) |
| `--json` | Output result as JSON to stdout |
| `--script` | Shorthand for `--silent --quiet --json` — one flag for clean pipe output |

### TTY detection

When stdin is piped (not a TTY) and no `--prompt`/`--prompt-file` is given, the entire stdin is read as the prompt. In non-TTY mode, `--model` is required (there's no way to prompt for it).

### Example pipelines

```bash
# URL only
gen-ai generate -m <image-id> -p "sunset" --script | jq -r '.url'

# Generate and download in one pipeline
cat prompt.txt | gen-ai generate -m <image-id> --script | jq -r '.url' | xargs curl -o out.png

# Loop over prompts
while IFS= read -r p; do
  gen-ai generate -m <image-id> -p "$p" --script >> results.json
done < prompts.txt

# Filter models to video-only, extract IDs
gen-ai models --json | jq '.[] | select(.mode=="video") | .id'
```

## Authentication

The CLI uses OAuth2 browser login:

```bash
gen-ai login     # Opens browser for Picsart SSO
gen-ai whoami    # Check current auth status
gen-ai logout    # Clear stored credentials
```

Credentials are cached in `~/.gen-ai/credentials.json` (mode 0o600). Tokens auto-refresh when expired.

### CI / headless environments

For CI pipelines or environments without a browser, set these environment variables:

```bash
export PICSART_ACCESS_TOKEN="<your-access-token>"
export PICSART_USER_ID="<your-user-id>"
```

When both are set, the CLI skips the browser login entirely. If neither is set and stdin is not a TTY, the CLI exits with an auth error and instructions.

## Global flags

Apply to every command:

| Flag | Alias | Description |
|------|-------|-------------|
| `--json` | | Output as JSON |
| `--plain` | | Plain tabular output (no formatting) |
| `--quiet` | `-q` | Suppress non-essential output |
| `--no-color` | | Disable color output |
| `--no-input` | | Disable all interactive prompts |
| `--debug` | | Show debug output |
| `--help` | | Show help |
| `--version` | `-v` | Show version |
