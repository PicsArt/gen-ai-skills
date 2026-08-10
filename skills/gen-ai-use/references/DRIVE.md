# Picsart Drive (upload, download, list)

The `gen-ai` CLI can read from and write to Picsart Drive. Drive commands browse the real Drive root — all folders visible (AI Playground, Image Flow, AI Video Generator, and any other root folders the account has).

## Contents

- Upload
- Upload a single file and get its URL (`upload-to-drive`)
- Download
- List (folders and files as JSON)
- Common flags reference

## Upload

Upload a single file or a folder of media to Drive.

```bash
gen-ai upload photo.jpg                                  # Single file
gen-ai upload photo.jpg --folder "Campaign Assets"       # To a specific folder
gen-ai upload ./renders/                                 # All media in a dir
gen-ai upload ./renders/ -r --type image                 # Recursive, images only
gen-ai upload ./renders/ --dry-run                       # Preview, don't upload
gen-ai upload *.jpg --max-files 100                      # Override 200-file limit
gen-ai upload photo.jpg --json                           # Machine-readable result, with a URL
```

| Flag | Default | Description |
|------|---------|-------------|
| `--folder, -f` | Gen AI | Drive folder (interactive mode shows all root folders) |
| `--type, -t` | all | Filter: image, video, audio |
| `--recursive, -r` | false | Recurse into subdirectories |
| `--dry-run` | false | List files without uploading |
| `--max-files` | 200 | Safety limit on number of files |
| `--concurrency, -c` | 3 | Parallel uploads |

### Getting a URL back (`--json`)

`--json` puts a machine-readable payload on **stdout**; progress goes to stderr, so stdout
is safe to parse directly. Capture it to a variable before piping to `jq` — piping the raw
command straight into `jq` reports `jq`'s exit code instead of `gen-ai`'s, and a lookup
miss silently prints the string `null` instead of failing loudly:

```bash
OUT=$(gen-ai upload photo.jpg --json) || { echo "upload failed"; exit 1; }
echo "$OUT" | jq -r '.files[] | select(.path == "/abs/path/photo.jpg") | .url'
```

```json
{
  "ok": true,
  "files": [
    { "path": "/abs/path/photo.jpg", "url": "https://cdn.../photo.jpg", "driveUid": "abc123", "error": null }
  ]
}
```

- `files` has one entry per file actually attempted **plus** one per input that was skipped
  (bad path, wrong extension, empty folder) — skipped entries are listed first, and a folder
  argument expands into one entry per file it contained. Match your file by its `path` field;
  never assume position, even for a single-file call.
- `url` is set the moment that file's own upload succeeds, and it stays set even if the later
  Drive save for that file fails — check `url` for "do I have a link to use," not `error` or `ok`.
- `driveUid` is the durable Drive copy's id; `null` if that save failed or Drive was unavailable.
- `error` is `null` only if that file's entire pipeline (upload *and* Drive save) succeeded.
- `ok` is `true` only if every file's entire pipeline succeeded; the process exit code reflects
  the same thing.

Turning a user's local file into a URL for an MCP tool (rather than the CLI's own use) is its
own procedure — see [`gen-ai-local-files`](../../gen-ai-local-files/SKILL.md).

## Upload a single file and get its URL (`upload-to-drive`)

A separate, narrower command from `upload`: one file, one named Drive entry, always JSON on stdout.
Built for pipeline hand-offs (e.g. publishing a rendered video), not bulk transfer.

```bash
gen-ai upload-to-drive ./explainer.mp4 --name "How DNS Works"
```

| Flag | Default | Description |
|------|---------|-------------|
| `--name` | filename | Drive display name |
| `--folder` | *(accepted, ignored — always saves to the CLI's "Gen AI" folder)* | Drive folder name |

Output — the only thing this command writes to stdout:

```json
{ "status": "ok", "drive_url": "https://cdn…", "drive_uid": "…", "file_name": "How DNS Works.mp4", "elapsed_ms": 1234 }
```

Caveats:

- **Video-shaped**, and unaffected by `upload`'s URL support above. It hardcodes
  `resourceType: VIDEO` and appends `.mp4` to the display name regardless of the source file.
  Drive classifies the entry as video by name pattern before it even checks `resourceType`, so it
  won't show up under `gen-ai list --type image`. The `drive_url` itself is still fine to hand to
  a tool — only the Drive filing is mistyped. For a correctly-typed Drive copy of a non-video
  file, use `gen-ai upload` instead.
- `--folder` is accepted but ignored — the file always lands in the CLI's fixed "Gen AI" folder,
  never the one you asked for.
- `drive_url` is the same temporary `editing-temp` CDN URL every upload path returns — not
  durable; point the user at the Drive entry (or `gen-ai list`) for anything they need to keep.
- If the Drive-save step itself fails, this command throws before writing anything to stdout —
  unlike `upload --json`, where a Drive-save failure still returns `url` with `driveUid: null`.
  Re-run rather than assuming nothing happened; the file did reach the CDN.

## Download

Pull files out of Drive to the local filesystem.

```bash
gen-ai download                                          # Interactive folder/file picker
gen-ai download --folder "Campaign Assets" --all         # All from a folder
gen-ai download --folder "AI Playground" --type video    # Filter by media type
gen-ai download --all -o ./local-assets/                 # Custom output dir
gen-ai download --list --type video                      # List as JSON, no download
gen-ai download --list --folder "Image Flow"             # List files in any root folder
```

| Flag | Default | Description |
|------|---------|-------------|
| `--folder, -f` | — | Root-level Drive folder name |
| `--all, -a` | false | Download all (vs. interactive pick) |
| `--list, -l` | false | List files as JSON (no download) |
| `--output, -o` | ./downloads | Local destination directory |
| `--type, -t` | all | Filter: image, video, audio |
| `--max-files` | 30 | Safety limit on downloads |
| `--concurrency, -c` | 3 | Parallel downloads |

## List

Enumerate folders and files with metadata. Designed for piping into `jq` and shell scripts.

```bash
gen-ai list --folders                         # All root-level Drive folders
gen-ai list                                   # All AI Playground files with metadata
gen-ai list --folder "AI Playground"          # Files in a specific folder
gen-ai list --folder "Image Flow"             # Any root folder works
gen-ai list --type video                      # Filter by media type
gen-ai list --type video | jq '.[].model'     # Pipe to jq
gen-ai list --folders | jq '.[].name'         # Just folder names
```

| Flag | Description |
|------|-------------|
| `--folders` | List top-level Drive folders (uid + name) |
| `--folder, -f` | List files in a specific root folder |
| `--type, -t` | Filter: image, video, audio |

## Generation → Drive in one step

`gen-ai generate` can push the result straight to Drive without a separate upload:

```bash
gen-ai generate --model <id> --prompt "..." --save-to-drive
gen-ai generate --model <id> --prompt "..." --drive-folder "My Project"   # implies --save-to-drive
```
