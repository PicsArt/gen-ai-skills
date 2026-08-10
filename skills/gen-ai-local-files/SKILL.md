---
name: gen-ai-local-files
description: Turn a local file into a URL for Picsart MCP tools.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux]
allowed-tools: Read, Bash
metadata:
  hermes:
    category: creative
    tags: [picsart, cli, upload, local-files, mcp]
---

# Local Files → Hosted URL

Picsart's MCP tools take **URLs**, not local paths. This skill is the bridge: it turns a file the user named on their own machine into a hosted URL you can hand to any Picsart MCP tool. It is not a Drive browser and not a directory scanner — it moves exactly the file the user pointed at.

## When to Use

_See the description above._

Concretely, reach for this when **both** hold:

- The user named a specific local file (`~/photos/hero.jpg`, `./renders/clip.mp4`, a path they pasted).
- The Picsart tool you want to call next needs a URL (`image_url`, `video_url`, `startFrame`, `image`, …).

Do **not** use this skill to discover what files the user has — see Pitfalls. And skip it entirely before a `gen-ai` CLI generation: pass the local path to `-i` and the CLI uploads it for you (see Procedure, step 1).

## Prerequisites

- **A Picsart MCP server connected**, for the preferred small-file route — `picsart_drive` lives on the `picsart-gen-ai` server. Check what's connected before promising a next step.
- **For a large file, the `gen-ai` CLI.** Run `gen-ai whoami` (auth + install + Node 22+ check). If the command is not found: `curl -fsSL https://picsart.com/gen-ai-cli/install.sh | bash` (or `npm install -g @picsart/gen-ai`, needs Node 22+). If `gen-ai whoami` fails, tell the user to either run `gen-ai login` **themselves, interactively** — it's a browser OAuth flow, so you cannot drive it from a non-TTY shell — or export `PICSART_ACCESS_TOKEN` and `PICSART_USER_ID` for non-interactive use. Don't retry the upload until `gen-ai whoami` succeeds.

## How to Run

_Small files: call `picsart_drive` directly. Large files: use the agent's `terminal` tool for `gen-ai` commands. No script to run — this skill is a decision and one call._

## Quick Reference

| Situation | Action |
|---|---|
| Already an `https://` URL | Use it as-is |
| Next step is a `gen-ai` CLI generation | Pass the path to `-i` — the CLI uploads it for you |
| Small file (fits as a `data:` URI), MCP connected | `picsart_drive` action `upload`: `url: "data:..."`, `name`, `type` |
| Large file, shell available | `gen-ai upload-to-drive <path>` |

`picsart_drive upload` returns `result.url` — a CDN URL ready for `image_url` / `video_url` / etc.

`gen-ai upload-to-drive <path>` prints one JSON object on stdout and nothing else, so `| jq -r .drive_url` is safe:

```json
{ "status": "ok", "drive_url": "https://cdn…", "drive_uid": "…", "file_name": "hero.jpg.mp4", "elapsed_ms": 1234 }
```

`gen-ai upload <path>` also saves the file to Drive but prints no URL on any output stream — it's the wrong tool when the goal is a URL.

## Procedure

### 1. Confirm the file and pick the route

Take the path from the user's message. If they said "the screenshot I just took" or "my photos", **ask which file** and wait — do not `ls`, glob, or walk directories to find candidates.

- Already a public URL → skip to step 4.
- Feeding a `gen-ai` CLI generation next → pass the path to `-i`; this skill doesn't apply.
- Otherwise, pick by size: small enough to inline as a `data:` URI → step 2; larger → step 3.

### 2. Small file: `picsart_drive` (preferred — no shell needed)

Read the file, base64-encode it, and call `picsart_drive`:

```json
{ "action": "upload", "url": "data:image/jpeg;base64,...", "name": "hero.jpg", "type": "image" }
```

Set `type` (`image` / `video` / `audio`) from the real file, not a guess — it's what makes the Drive entry findable later. Read `result.url` from the response; that's the hosted URL.

### 3. Large file: `gen-ai upload-to-drive`

```bash
gen-ai whoami                                     # gate on auth first
gen-ai upload-to-drive /absolute/path/to/file.jpg
```

Pass the path the user gave, resolved to an absolute path. Parse `drive_url` from the single stdout object.

### 4. Hand the URL to the tool the user actually wanted

Read the connected tool list, find the tool that does what the user asked, and pass the URL in its URL-shaped parameter. Don't invent a tool name — if nothing connected matches the request, say so.

If the operation is asynchronous, poll its paired result tool before reporting success, and do it promptly: a CDN URL from `upload-to-drive` is `editing-temp` and a long stall between upload and submit can invalidate it.

## Pitfalls

- **Scanning for files the user didn't name.** The user's explicit path is the trust boundary — stay inside it.
- **`upload-to-drive` mistypes non-video files.** It hardcodes `resourceType: VIDEO` and appends `.mp4` to the display name regardless of the source file. Drive classifies the entry by name pattern before it even checks `resourceType`, so `gen-ai list --type image` will never surface it — not just cosmetic. The returned URL itself is still fine to use; only the Drive filing is wrong. `picsart_drive upload` with the correct `type` avoids this.
- **CDN MIME type is only correct for `.jpg/.jpeg/.png/.gif/.webp/.mp4/.webm/.mp3/.wav`.** Other extensions (`.heic`, `.svg`, `.bmp`, `.tiff`, `.avif`, …) upload as generic binary.
- **`--folder` on `upload-to-drive` is accepted but ignored** — the file always lands in the Drive root regardless of the flag.
- **Treating the CDN URL as durable.** Both routes hand back `editing-temp` storage — fine to feed straight into a tool call, not a permanent link to give the user.
- **If `gen-ai upload-to-drive` fails at the Drive-save step, you get no output** even though the file already reached the CDN — re-run rather than assuming nothing happened.
- **Driving `gen-ai login` yourself.** It's an interactive browser flow. Asking the user to run it is the procedure, not a fallback.
- **Guessing the MCP tool name.** Read what's connected — `picsart_*` (this server) and `genai-*`/`image-*`/`video-*` (the REST-API server) are different servers with different tool shapes.

## Verification

1. The route you used returned a non-empty URL (`result.url` from `picsart_drive`, or `drive_url` from `upload-to-drive`).
2. The URL resolves — the downstream MCP tool accepting it without a fetch error is sufficient proof; don't separately download it.
3. If durability was requested, don't point the user at an `upload-to-drive` link — use `picsart_drive`, or `gen-ai upload` (which files correctly but prints no URL), and confirm the file from Picsart Drive.

## Related

- [`gen-ai-use`](../gen-ai-use/SKILL.md) — the full CLI surface, including batch upload and Drive download ([references/DRIVE.md](../gen-ai-use/references/DRIVE.md)).
- [`picsart-api`](../picsart-api/SKILL.md) — the MCP tool catalog this skill feeds URLs into.
