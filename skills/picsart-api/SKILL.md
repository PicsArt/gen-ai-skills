---
name: picsart-api
description: Generate and edit media via Picsart MCP API tools.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: api
    tags: [picsart, mcp, image-api, video-api, genai-api, variable-data]
---

# Picsart API (MCP)

The `picsart` MCP server at `https://mcp.picsart.io/v1` exposes four Picsart REST APIs as MCP tools. Each tool name equals the OpenAPI `operationId` verbatim — dashes preserved (e.g. `genai-text2image`, `image-remove-background`, `video-trim`, `vd-export-replay`).

## When to Use

Use this skill whenever the user asks to:

- Generate net-new content from a prompt — image, video, sticker, logo, speech, sound, music, SFX, or text completion.
- Edit, enhance, resize, reformat, recolor, or transform an existing image or video.
- Remove backgrounds or objects; inpaint, outpaint, or extend canvas.
- Apply effects, masks, styles, adjustments, blur, color/style transfer.
- Extract, transcribe, or manipulate audio tracks in video.
- Upscale, FPS-upscale, super-resolve, or enhance faces.
- Watermark, crop, trim, concat, or fit media.
- Render bulk personalised creative assets via a Replay.

If the request touches any of the above, read the relevant doc in `references/` BEFORE calling any `picsart-*`, `image-*`, `video-*`, `genai-*`, or `vd-*` MCP tool.

## Prerequisites

The `picsart` MCP server must be connected and a Picsart API key available:

- **MCP server.** This repo ships the server config at the repo-root `.mcp.json`. Claude Code auto-loads it when the repo (or the installed skill) is in scope. For other hosts (Cursor, Codex) or a manual setup, register an HTTP MCP server named `picsart` pointing at `https://mcp.picsart.io/v1`:

  ```json
  {
    "mcpServers": {
      "picsart": {
        "type": "http",
        "url": "https://mcp.picsart.io/v1",
        "headers": {
          "X-Picsart-API-Key": "${PICSART_API_KEY}",
          "Accept": "application/json"
        }
      }
    }
  }
  ```

- **API key.** Export `PICSART_API_KEY` in the environment before starting the agent. Never hardcode it — the config interpolates `${PICSART_API_KEY}` at runtime.

## How to Run

1. Identify the user's intent and read only the matching `references/` doc (see Quick Reference). Do not read docs for surfaces the task won't touch.
2. Look up the exact tool name (= OpenAPI `operationId`) in that doc's tool index.
3. Call the tool verbatim via the `picsart` MCP server. For async tools, chain through the paired poller until the job is terminal (see Procedure).
4. Return the final result URL(s) to the user.

## Quick Reference

Four API surfaces, four reference docs in this skill's `references/` folder:

- **Image** ([`references/image-api.md`](references/image-api.md)) — background removal, upscale, effects, masks, adjust, watermark, crop, blend, segmentation, tagging, vectorize, design-import. Base: `https://api.picsart.io/tools/1.0`.
- **Video** ([`references/video-api.md`](references/video-api.md)) — edit, trim, crop, concat, fit, effects, FPS upscale, thumbnails, metadata, audio adjust / extract / transcribe, CTV encoding, watermark. Base: `https://video-api.picsart.io/v1`.
- **GenAI** ([`references/genai-api.md`](references/genai-api.md)) — text→image, text→sticker, logo gen, image edit / inpaint / outpaint, object removal, smart-background, expand / bleed, text→video, image→video, text→speech, text→sound, text→text completions. Base: `https://genai-api.picsart.io/v1`.
- **Variable Data** ([`references/variable-data-api.md`](references/variable-data-api.md)) — bulk personalised rendering from Picsart Replay templates. Base: `https://vd-api.picsart.io/v1`.

Load the doc(s) that match the user's intent:

| Task intent | Doc to read |
|---|---|
| Generate image from prompt, sticker, logo, text completion | `references/genai-api.md` |
| Generate video from text or from an image | `references/genai-api.md` |
| Generate speech or sound / SFX / music from text | `references/genai-api.md` |
| Edit an image with a prompt; inpaint, outpaint, remove-object, smart-background, expand, bleed | `references/genai-api.md` |
| Transform an existing image without a prompt — bg removal, upscale, effects, masks, adjust, watermark, crop, blend, vectorize | `references/image-api.md` |
| Describe, tag, segment, classify, or extract colors from an image | `references/image-api.md` |
| Edit / trim / crop / concat / fit a video; apply video effects; FPS upscale; thumbnails; watermark; CTV encode | `references/video-api.md` |
| Adjust / extract / transcribe audio of a video | `references/video-api.md` |
| Bulk personalised rendering from a Replay template | `references/variable-data-api.md` |

Known submit → poller pairs (read the per-API doc for the authoritative list):

- `genai-text2image` → `genai-text2image-getresult`
- `genai-text2sticker`, `genai-text2sticker-laser-engraving` → `genai-text2sticker-getresult`
- `genai-generate-logo` → `genai-generate-logo-getresult`
- `genai-image-edit`, `genai-image-inpainting`, `genai-image-outpainting`, `genai-remove-object`, `genai-smart-background`, `genai-expand-image`, `genai-generate-image-bleed` → `genai-image-inpainting-getresult`
- `genai-text2video`, `genai-image2video` → `genai-text2video-getresult`
- `genai-text2speech`, `genai-text2sound` → `genai-text2audio-getresult`
- `image-ultra-upscale` → `image-ultra-upscale-getresult`
- `image-design-import` → `image-design-import-getresult`
- `video-upscale-fps` → `video-upscale-fps-getresult`
- `video-transcribe-audio` → `video-transcribe-audio-getresult`
- `video-set-thumbnail` → `video-set-thumbnail-getresult`
- Other video operations that return a job id → `video-getresult` (or `video-getaudioresult` for audio outputs).
- `vd-export-replay` → `vd-export-replay-getresult`
- `vd-export-variable-data-content` → `vd-export-variable-data-content-getresult`

## Procedure

**Core principles**

1. **Tool name = operationId.** Look up the exact name in the doc's tool index, then call it verbatim via the MCP server. Dashes stay dashes.
2. **Async jobs must be polled.** Many tools return a job id and complete later. Never tell the user "done" on the submit call alone — always chain through the paired poller until the job's status is `FINISHED` / `succeeded`.
3. **Inputs: file OR url.** Most endpoints accept either an uploaded file or an `*_url` string (e.g. `image_url`, `video_url`). Prefer URLs when the asset is already hosted publicly — avoids upload overhead. **For a file on the user's own machine**, an MCP server cannot read it — you need a URL first. Open the upload widget (`picsart_upload_widget` or `mp_upload`, whichever connector is present) and wait for the URL it reports back. Full procedure, including the two-turn handshake, in [`picsart-add-media`](../picsart-add-media/SKILL.md).
4. **Credits before expensive calls.** Each API exposes a balance tool (`image-credits-balance`, `video-credits-balance`, `genai-credits-balance`, `vd-credits-balance`). For a first call in a session that may be heavy (video generation, bulk exports, long upscales), call the matching balance tool so the user isn't surprised by a 402.
5. **Enum values are exact.** Effect names, aspect ratios, styles, voices, and output formats are closed enums in the docs. Copy values verbatim — do not paraphrase. Invalid enums fail the call and waste a round trip.
6. **Prefer specialised tools over generic ones.** For a 4× or larger upscale use `image-ultra-upscale` over `image-upscale`; for face shots use `image-face-enhance`; for video cuts use `video-trim` over `video-edit`.

**Async polling pattern**

1. Call the submit tool, capture the returned id (field names vary: `id`, `inference_id`, `transaction_id`).
2. Call the paired poller with that id. If status is pending (`IN_PROGRESS`, `PENDING`, etc.), wait briefly and call again.
3. Stop when status is terminal (`FINISHED` / `succeeded` / `FAILED`). Surface the result URL(s) to the user, or the error on failure.

Keep polling quiet — a single "still rendering…" update is enough; do not narrate each poll.

**Common workflows** (each step is one MCP tool call; consult the per-API doc for exact parameter names)

- **Generate image from prompt** — `genai-text2image` → `genai-text2image-getresult` → return image URL.
- **Generate short video from prompt** — `genai-text2video` → `genai-text2video-getresult` → return mp4 URL.
- **Animate an existing image** — `genai-image2video` → `genai-text2video-getresult` → return mp4 URL.
- **Text-to-speech (voice-over)** — `genai-text2speech` → `genai-text2audio-getresult` → return audio URL.
- **Text-to-sound / SFX / music** — `genai-text2sound` → `genai-text2audio-getresult` → return audio URL.
- **Remove background from a photo** — `image-remove-background` (sync) → return result URL.
- **Upscale an image** — small factor or quick job → `image-upscale` (sync); 4× / 8× or heavy → `image-ultra-upscale` → `image-ultra-upscale-getresult`.
- **Edit photo with a natural-language instruction** — `genai-image-edit` → `genai-image-inpainting-getresult` → return image URL.
- **Fill in a region of a photo** — `genai-image-inpainting` → `genai-image-inpainting-getresult`.
- **Extend a photo beyond its edges** — `genai-image-outpainting` or `genai-expand-image` → `genai-image-inpainting-getresult`.
- **Remove an object from a photo** — `genai-remove-object` → `genai-image-inpainting-getresult`.
- **Transcribe a video's audio** — `video-transcribe-audio` → `video-transcribe-audio-getresult` → return transcript.
- **Trim / crop / concat a video** — `video-trim` / `video-crop` / `video-concat` → poll with `video-getresult` if it returns a job id.
- **Bulk personalised renders from a Replay** — `vd-export-replay` → `vd-export-replay-getresult`. For variable-data-driven batches: `vd-describe-variable-data-content` → `vd-export-variable-data-content` → `vd-export-variable-data-content-getresult`.

## Pitfalls

- **Don't declare success on a submit-only response.** Async jobs return a job id; wait for the paired poller to report a terminal status before telling the user the task is done.
- **Disambiguate similar intents:**
  - "Enhance this photo" with no prompt → **Image API** (`image-upscale`, `image-ultra-enhance`, `image-face-enhance`).
  - "Edit this photo to …" with a natural-language instruction → **GenAI** (`genai-image-edit`).
  - "Remove background" from a still → **Image API** (`image-remove-background`); from a video → **Video API** (`video-remove-background`).
  - "Extend / widen / fill beyond edges" → **GenAI** (`genai-image-outpainting`, `genai-expand-image`, `genai-generate-image-bleed`).
- **Enum drift fails calls.** Paraphrasing an effect name, style, voice, or aspect ratio wastes a round trip — copy enum values verbatim from the docs.
- **Watch limits and content policy.** Respect the [Picsart Developer Guidelines](https://picsart.io/terms) — no disallowed content. Image upload size / format limits: see `references/image-api.md`. Video duration, resolution, and codec limits: see `references/video-api.md`. GenAI prompt-length caps, seed / count limits, and safety filters: see `references/genai-api.md`. Variable Data batch size and Replay compatibility notes: see `references/variable-data-api.md`.

## Verification

- Return the final result URL(s) in the response.
- For async jobs, wait for completion before declaring success. A submit-only response is not a finished task.
- Preserve URLs exactly as returned — they're signed / time-bound.
- If the user hasn't specified an output format, use the endpoint default (noted in each doc).

## References

Official portal: https://docs.picsart.io/

Spec sources used to produce the docs in this skill:

- https://apidocs.picsart.io/picsart-image-tools-api.yaml
- https://apidocs.picsart.io/picsart-video-tools-api.yaml
- https://apidocs.picsart.io/picsart-genai-tools-api.yaml
- https://apidocs.picsart.io/picsart-variable-data-tools-api.yaml
