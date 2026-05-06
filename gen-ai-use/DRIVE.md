# Picsart Drive (upload, download, list)

The `gen-ai` CLI can read from and write to Picsart Drive. Drive commands browse the real Drive root — all folders visible (AI Playground, Image Flow, AI Video Generator, and any other root folders the account has).

## Contents

- Upload
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
```

| Flag | Default | Description |
|------|---------|-------------|
| `--folder, -f` | AI Playground | Drive folder (interactive mode shows all root folders) |
| `--type, -t` | all | Filter: image, video, audio |
| `--recursive, -r` | false | Recurse into subdirectories |
| `--dry-run` | false | List files without uploading |
| `--max-files` | 200 | Safety limit on number of files |
| `--concurrency, -c` | 3 | Parallel uploads |

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
