---
name: picsart-add-media
description: Bring the user's own clips, photos or audio into Picsart as hosted URLs, through the gen-ai MCP's upload widget or, where a shell can read the file, a direct upload. Use when a Picsart tool needs a URL and the media is on the user's machine or in a chat attachment.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, upload, local-files, widget]
---

# Add Media (Upload Widget)

Picsart's MCP tools take **URLs**, not local paths, and most agent hosts (browser-based chats,
Claude Code without shell access, ChatGPT web) can't read a file straight off the user's disk
either. The fix is a browser-based **upload widget**: an MCP tool opens a drag-and-drop panel in
the user's browser, the browser uploads the file directly to Picsart's CDN, and the widget hands
the resulting URL back to you. No file bytes ever pass through a tool call.

## When to Use

Fires on things like "I have 3 video clips", "here are my photos", "use my footage", "combine
these clips" — anything where the media is the user's own and you don't already have a link to
it.

Reach for this whenever the next step needs a URL (`image_url`, `video_url`, `startFrame`, …) and
the source is something on the user's own machine, a chat attachment you can't fetch, or anything
else not already a public `https://` link.

## Prerequisites

The Picsart gen-ai MCP server (`picsart-gen-ai`, declared in this repo's `.mcp.json`) in the
current tool list. It offers two routes:

- **`picsart_media_upload`** — opens the upload widget. Works on every host, including ones with
  no shell. The widget also has a "My Drive" tab when the user's Picsart Drive is reachable, and
  tries to save each upload to their Drive.
- **`picsart_upload_local_files`** — for a host that can run shell commands and can read the file
  on disk. It returns one upload command per file; run it, and the printed JSON holds the hosted
  URL at `response.url`. No widget and no wait for the user. The hosted copy is temporary.

If the server is not connected, say so; don't guess a tool name.

## How to Run

_No script to run — this skill is one tool call plus a short wait for the user's next message._

## Quick Reference

| Argument | What it does |
|---|---|
| _(none)_ | Opens the widget with no pre-filled context — a plain drag-and-drop |
| `purpose` | Label shown on the dropzone (e.g. `"product photo"`) |
| `accept` | Restrict to `image`, `video`, or `audio` |
| `detected_files` | Filenames you can see in the conversation but can't reach yourself (e.g. a chat attachment) — rendered as a *hint* only |
| `known_urls` | URLs already produced earlier in the conversation, seeded as pickable chips so the user isn't asked to re-upload something already available |

## Procedure

If you have a shell and the file is on disk, use `picsart_upload_local_files` instead: pass each
file's `name` and `bytes`, run the command it returns with the file's path, and go straight to
step 3 with the URL it prints. Otherwise:

### 1. Call the upload tool

Call `picsart_media_upload` with whichever of `purpose`,
`accept`, `detected_files`, `known_urls` apply. All arguments are optional — calling with none
just opens the widget.

```json
{ "purpose": "product photo", "accept": "image", "known_urls": ["https://cdn.picsart.io/…already-uploaded.jpg"] }
```

- `detected_files` is a **label hint only, never a filter** — it's model-supplied and can be
  wrong or hallucinated. The user can still drop any file they want; don't tell them a file is
  "not accepted" because it wasn't in your `detected_files` list.
- `known_urls` saves a re-upload: if a URL already exists from earlier in the conversation (a
  prior generation result, a prior upload), pass it here so it shows up as a chip the user can
  pick instead of finding the file again.

### 2. Tell the user what to do, then wait for their next message

The widget reports the uploaded URL(s) back to you via a mechanism most agent hosts only deliver
on the **user's next message** — not instantly within the same turn. This is a real two-turn
handshake, not a delay you can poll through.

Say something like: "I've opened the upload panel — drop your file in and let me know once it's
there." Then stop and wait. Do **not** claim you can't see the file, or that the upload failed,
just because nothing arrived in the same turn you called the tool.

### 3. Hand the URL to the tool the user actually wanted

Once the URL comes back (on the user's next message), pass it into the URL-shaped parameter of
whatever tool the user's original request needs (`image_url`, `video_url`, etc.).

## Pitfalls

- **Expecting the URL in the same turn.** It won't be there — see step 2. Prompt the user and
  wait for their next message instead of reporting failure early.
- **Treating `detected_files` as a filter.** It's a display hint for filenames you can see but
  can't fetch. Never reject or second-guess a file the user actually drops based on this list.
- **Re-asking for a file that's already uploaded.** Check the conversation for a URL you already
  have before opening the widget — pass it via `known_urls` instead of starting over.
- **Guessing the tool name.** The upload tools are `picsart_media_upload` and
  `picsart_upload_local_files`, both on `picsart-gen-ai`. Read what the tool list actually shows.

## Verification

- The tool call that opened the widget returned without error.
- A URL came back on a subsequent user message and looks like a real hosted link (not a local
  path).
- The downstream tool call accepting that URL didn't fail on the URL itself.

## Related

- The `video-prompt-engineer` skill writes the prompt for a video generated from the URLs this
  skill returns.
