---
name: picsart-add-media
description: Bring the user's own clips, photos, or files into Picsart.
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
either. The fix is the `picsart` MCP server's **`picsart_media_upload`** tool: it opens a
drag-and-drop panel in the user's browser, the browser uploads the file directly to Picsart, and
the widget hands the resulting hosted URL back to you. No file bytes ever pass through a tool call.
Pass that URL to whichever Picsart tool comes next.

## When to Use

Fires on things like "I have 3 video clips", "here are my photos", "use my footage", "combine
these clips" — anything where the media is the user's own and you don't already have a link to
it.

Reach for this whenever the next step needs a URL (`image_url`, `video_url`, `startFrame`, …) and
the source is something on the user's own machine, a chat attachment you can't fetch, or anything
else not already a public `https://` link. Also use it after a Picsart tool refuses a local-path
argument with a `local_source_not_supported` error.

## Prerequisites

The `picsart` MCP server (`https://api.picsart.com/gen-ai/mcp`) connected in the current session, with `picsart_media_upload` in the tool list. The
server uses OAuth: on first connect, an OAuth-capable host asks the user to sign in to Picsart.

If the `picsart` server isn't connected, say so; don't guess a tool name.

## How to Run

_No script to run — this skill is one tool call plus a short wait for the user's next message._

## Quick Reference

`picsart_media_upload` arguments (all optional):

| Argument | What it does |
|---|---|
| _(none)_ | Opens the widget with no pre-filled context — a plain drag-and-drop |
| `purpose` | Label shown on the dropzone (e.g. `"the video you want to upscale"`) |
| `accept` | Restrict to `image`, `video`, or `audio` |
| `detected_files` | Filenames you can see in the conversation but can't reach yourself (e.g. a chat attachment) — rendered as a *hint* only |
| `known_urls` | URLs already produced earlier in the conversation, pre-selected so the user isn't asked to re-upload something already available |

The widget also has a "My Drive" tab (when the user's Picsart Drive is reachable) for picking
files already saved there, and after an upload it tries to save the file to their Drive
(best-effort, needs the connected account).

## Procedure

### 1. Call the upload tool

Call `picsart_media_upload` with whichever of `purpose`, `accept`, `detected_files`, `known_urls`
apply. Calling it with none just opens the widget. Opening it uploads nothing on its own.

```json
{ "purpose": "product photo", "accept": "image", "known_urls": ["https://cdn.picsart.io/…already-uploaded.jpg"] }
```

- `detected_files` is a **label hint only, never a filter** — it's model-supplied and can be
  wrong or hallucinated. The user can still drop any file they want; don't tell them a file is
  "not accepted" because it wasn't in your `detected_files` list.
- `known_urls` saves a re-upload: if a URL already exists from earlier in the conversation (a
  prior generation result, a prior upload), pass it here so it shows up pre-selected instead of
  the user finding the file again.

### 2. Tell the user what to do, then wait for their next message

The call only **opens** the widget and returns no URL itself. The widget reports the uploaded
URL(s) back into the conversation on the **user's next message** — not within the same turn. This
is a real two-turn handshake, not a delay you can poll through.

Say something like: "I've opened the upload panel — drop your file in and let me know once it's
there." Then stop and wait. Do **not** claim you can't see the file, or that the upload failed,
just because nothing arrived in the same turn you called the tool.

### 3. Hand the URL to the tool the user actually wanted

Once the URL comes back (on the user's next message), pass it **verbatim** into the URL-shaped
parameter of whatever Picsart tool the user's original request needs (`image_url`, `video_url`,
etc.).

## Pitfalls

- **Expecting the URL in the same turn.** It won't be there — see step 2. Prompt the user and
  wait for their next message instead of reporting failure early.
- **Treating `detected_files` as a filter.** It's a display hint for filenames you can see but
  can't fetch. Never reject or second-guess a file the user actually drops based on this list.
- **Re-asking for a file that's already uploaded.** Check the conversation for a URL you already
  have before opening the widget — pass it via `known_urls` instead of starting over.
- **Rewriting the returned URL.** Pass it exactly as returned; don't infer expiry or storage from
  its hostname or query string.

## Verification

- The tool call that opened the widget returned without error.
- A URL came back on a subsequent user message and looks like a real hosted link (not a local
  path).
- The downstream tool call accepting that URL didn't fail on the URL itself.

## Related

- [`gen-ai-use`](../gen-ai-use/SKILL.md) — the `gen-ai` CLI, which uploads local files itself
  rather than through this widget.
