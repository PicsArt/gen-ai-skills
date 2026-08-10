---
name: gen-ai-local-files
description: Turn a local file into a URL for Picsart MCP tools.
version: 1.2.0
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

- **A Picsart MCP server connected**, for the small-file route — `picsart_drive` lives on the `picsart-gen-ai` server. Check what's connected before promising a next step.
- **For a large file, the `gen-ai` CLI, authenticated.** Run `gen-ai whoami` (auth + install + Node 22+ check) before uploading. If `gen-ai` is not found: `curl -fsSL https://picsart.com/gen-ai-cli/install.sh | bash` (or `npm install -g @picsart/gen-ai`, needs Node 22+). If `gen-ai whoami` fails, tell the user to either run `gen-ai login` **themselves, interactively** — it's a browser OAuth flow, so you cannot drive it from a non-TTY shell — or export `PICSART_ACCESS_TOKEN` and `PICSART_USER_ID` for non-interactive use. Don't retry the upload until `gen-ai whoami` succeeds.

## How to Run

_Small files: call `picsart_drive` directly. Large files: use the agent's `terminal` tool to run `gen-ai upload`. No script to run — this skill is a decision and one call._

## Quick Reference

| Situation | Action |
|---|---|
| Already an `https://` URL | Use it as-is |
| Next step is a `gen-ai` CLI generation | Pass the path to `-i` — the CLI uploads it for you |
| Small file (fits as a `data:` URI — roughly a couple MB raw), MCP connected | `picsart_drive` action `upload`: `url: "data:..."`, `name`, `type` |
| Large file, shell available | `gen-ai upload <path> --json` |

`picsart_drive upload` returns `result.url` — a CDN URL ready for `image_url` / `video_url` / etc. It needs no local CLI at all.

`gen-ai upload --json` prints `{ok, files:[{path,url,driveUid,error}]}` straight to stdout (progress goes to stderr). Full field semantics — matching your file by `path`, what `null` means where, safe `jq` usage — are in [`gen-ai-use`'s Drive reference](../gen-ai-use/references/DRIVE.md); don't re-derive them here, that's the canonical copy.

## Procedure

### 1. Confirm the file and pick the route

Take the path from the user's message. If they said "the screenshot I just took" or "my photos", **ask which file** and wait — do not `ls`, glob, or walk directories to find candidates.

- Already a public URL → skip to step 4.
- Feeding a `gen-ai` CLI generation next → pass the path to `-i`; this skill doesn't apply.
- Otherwise, pick by size: small enough to inline as a `data:` URI (a couple MB raw — base64 inflates it ~1.37× inside the tool-call payload, so budget accordingly) → step 2; larger → step 3. The CLI's own hard ceiling is 500 MB regardless of route; above that the file needs to be shrunk or transcoded first.

### 2. Small file: `picsart_drive` (no shell needed)

Read the file, base64-encode it, and call `picsart_drive`:

```json
{ "action": "upload", "url": "data:image/jpeg;base64,...", "name": "hero.jpg", "type": "image" }
```

To produce the base64 payload from a shell, `base64 < file | tr -d '\n'` works identically on
macOS and Linux — the `-w0` / `-w 0` line-wrap flags don't (only one of the two platforms'
`base64` accepts them, and a wrapped value breaks a `data:` URI).

Set `type` (`image` / `video` / `audio`) from the real file, not a guess — it's what makes the Drive entry findable later. Read `result.url` from the response; that's the hosted URL.

This route creates a real Drive entry (the tool groups `upload` with other persistent
Drive-management actions like `move`/`delete`/`update`), so treat it as durable — though
that's about the Drive record, not a guarantee on how long `result.url` itself stays live. If
the user needs the link itself to persist, confirm via a Drive listing rather than assuming.

### 3. Large file: `gen-ai upload`

```bash
gen-ai whoami                                      # gate on auth
gen-ai upload /absolute/path/to/file.jpg --json
```

Capture the output before parsing it — don't pipe straight into `jq`, which would report its
own exit code instead of `gen-ai`'s and silently print `null` on a lookup miss. Then find your
file's entry by its `path` field: `files` also lists any skipped inputs first and expands a
folder argument into one entry per file, so don't index by position, even for a single-file
call. `url` is set the moment that file's own upload succeeds and survives a later Drive-save
failure — check `url` for "do I have a link," not `error` or `ok`. Full contract in
[`gen-ai-use`'s Drive reference](../gen-ai-use/references/DRIVE.md).

If the file is a video and you specifically need the older single-object `upload-to-drive`
pipeline shape (e.g. to match an existing script), its caveats are in the same reference —
but `upload --json` above is the general-purpose route and doesn't mistype non-video files.

### 4. Hand the URL to the tool the user actually wanted

Read the connected tool list, find the tool that does what the user asked, and pass the URL in its URL-shaped parameter. Don't invent a tool name — if nothing connected matches the request, say so.

If the operation is asynchronous, poll its paired result tool before reporting success, and do it promptly: a CDN URL from `gen-ai upload`/`upload-to-drive` is `editing-temp` and a long stall between upload and submit can invalidate it.

## Pitfalls

- **Scanning for files the user didn't name.** The user's explicit path is the trust boundary — stay inside it.
- **`upload-to-drive` mistypes non-video files.** It hardcodes `resourceType: VIDEO` and appends `.mp4` to the display name regardless of the source file. Drive classifies the entry by name pattern before it even checks `resourceType`, so `gen-ai list --type image` will never surface it — not just cosmetic. The returned URL itself is still fine to use; only the Drive filing is wrong.
- **`--folder` on `upload-to-drive` is accepted but ignored** — the file always lands in the CLI's fixed "Gen AI" folder, never the one you asked for.
- **CDN MIME type is only correct for a fixed extension list**: `.jpg .jpeg .png .gif .webp .heic .avif .mp4 .webm .mov .mp3 .wav .m4a`. Everything else — including `.heif` (`.heic`'s sibling), `.svg`, `.bmp`, `.tiff` — uploads as generic binary.
- **Treating every route's link as equally durable.** `gen-ai upload`/`upload-to-drive` CDN URLs are explicitly `editing-temp` — not durable. `picsart_drive upload` creates a genuine Drive entry, so that's a different, more durable case; see step 2's note on it.
- **If `gen-ai upload-to-drive` fails at the Drive-save step, you get no output** even though the file already reached the CDN — re-run rather than assuming nothing happened. (`gen-ai upload --json` doesn't have this failure mode — a Drive-save failure there still returns `url` with `driveUid: null`.)
- **Driving `gen-ai login` yourself.** It's an interactive browser flow. Asking the user to run it is the procedure, not a fallback.
- **Guessing the MCP tool name.** Read what's connected — `picsart_*` (this server) and `genai-*`/`image-*`/`video-*` (the REST-API server) are different servers with different tool shapes.

## Verification

1. The route you used returned a non-empty URL (`result.url` from `picsart_drive`, `url` from `gen-ai upload --json` matched by `path` — not by array index — or `drive_url` from `upload-to-drive`).
2. The URL resolves — the downstream MCP tool accepting it without a fetch error is sufficient proof; don't separately download it.
3. If durability was requested, don't point the user at an `editing-temp` link — use `picsart_drive`, or confirm the file from Picsart Drive via `gen-ai list`.

## Related

- [`gen-ai-use`](../gen-ai-use/SKILL.md) — the full CLI surface, including batch upload and Drive download ([references/DRIVE.md](../gen-ai-use/references/DRIVE.md)).
- [`picsart-api`](../picsart-api/SKILL.md) — the MCP tool catalog this skill feeds URLs into.
