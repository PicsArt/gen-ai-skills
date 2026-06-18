# Picsart GenAI API — MCP Tool Reference

Generative AI tools exposed as MCP tools by the Picsart B2B MCP server. Each
operationId in the underlying OpenAPI spec maps verbatim to an MCP tool name
(dashes preserved). All tools call `https://genai-api.picsart.io/v1` and
authenticate with the `X-Picsart-API-Key` header (handled by the MCP server).

**Surface covered:**

- Text → Image (`genai-text2image`)
- Text → Sticker (`genai-text2sticker`, `genai-text2sticker-laser-engraving`)
- Logo generation (`genai-generate-logo`)
- Image editing with a prompt (`genai-image-edit`)
- Inpaint / Outpaint (`genai-image-inpainting`, `genai-image-outpainting`)
- Smart background replace (`genai-smart-background`)
- Object removal (`genai-remove-object`)
- Image expansion / bleed (`genai-expand-image`, `genai-generate-image-bleed`)
- Text → Video (`genai-text2video`)
- Image → Video (`genai-image2video`)
- Text → Speech (`genai-text2speech`)
- Text → Sound / Music (`genai-text2sound`)
- Text → Text chat completions (`genai-text2text-completions`)
- Credits balance (`genai-credits-balance`)

Most generation endpoints are **asynchronous**: the POST returns an
`inference_id`, and you must poll the matching `-getresult` tool until
`status == "success"`.

---

## Quick-pick decision table

| If the user wants to …                                       | Use this tool                       |
| ------------------------------------------------------------ | ----------------------------------- |
| Generate an image from a text prompt                         | `genai-text2image`                  |
| Edit an existing image with a text prompt                    | `genai-image-edit`                  |
| Fill a specific area of an image (inpaint)                   | `genai-image-inpainting`            |
| Extend an image beyond its bounds (outpaint)                 | `genai-image-outpainting`           |
| Resize/expand an image with new content on the sides         | `genai-expand-image`                |
| Add a small print-safe bleed margin around an image          | `genai-generate-image-bleed`        |
| Replace the background of an image with an AI scene          | `genai-smart-background`            |
| Remove an object from an image (with a mask)                 | `genai-remove-object`               |
| Generate a sticker from a prompt                             | `genai-text2sticker`                |
| Generate a laser-engraved style sticker                      | `genai-text2sticker-laser-engraving`|
| Generate a logo for a brand                                  | `genai-generate-logo`               |
| Generate a video from a text prompt                          | `genai-text2video`                  |
| Animate a still image into a video                           | `genai-image2video`                 |
| Speak text aloud (TTS)                                       | `genai-text2speech`                 |
| Generate music or sound effects from a prompt                | `genai-text2sound`                  |
| Get a chat/text completion from an LLM                       | `genai-text2text-completions`       |
| Check remaining Picsart credits                              | `genai-credits-balance`             |

---

## Tool index

| MCP tool                                | Purpose                              | Key inputs                                          | Sync/Async |
| --------------------------------------- | ------------------------------------ | --------------------------------------------------- | ---------- |
| `genai-text2text-completions`           | Chat / text completion               | `messages`, `model`, `max_tokens`, `temperature`    | Sync       |
| `genai-text2image`                      | Text → image                         | `prompt`, `width`, `height`, `count`, `model`       | Async      |
| `genai-text2image-getresult`            | Poll text2image                      | `inference_id`                                      | Sync poll  |
| `genai-text2sticker`                    | Text → sticker                       | `prompt`, `width`, `height`, `count`, `model`       | Async      |
| `genai-text2sticker-laser-engraving`    | Text → sticker w/ engraving effect   | `prompt`, `engrave_color`, `background_color`, `format` | Async  |
| `genai-text2sticker-getresult`          | Poll text2sticker                    | `inference_id`                                      | Sync poll  |
| `genai-generate-logo`                   | Brand logo generation                | `brand_name`, `business_description`, `color_tone`, `logo_description`, `reference_image[_url]`, `count`, `model` | Async |
| `genai-generate-logo-getresult`         | Poll logo generation                 | `inference_id`                                      | Sync poll  |
| `genai-image-edit`                      | Edit any image with a prompt         | `image[_url]`, `prompt`, `count`, `format`, `model`, watermark_* | Sync or Async |
| `genai-image-inpainting`                | Fill inside masked area              | `image[_url]`, `mask_image[_url]`, `prompt`, `count`, `format` | Sync or Async |
| `genai-image-outpainting`               | Paint outside masked area            | `image[_url]`, `mask_image[_url]`, `prompt`, `count`, `format` | Sync or Async |
| `genai-smart-background`                | AI-replace image background          | `image[_url]`, `prompt`, `count`, `format`          | Sync or Async |
| `genai-remove-object`                   | Mask-driven object removal           | `image[_url]`, `mask_image[_url]`, `format`         | Sync or Async |
| `genai-expand-image`                    | Generative resize / outpaint to size | `image[_url]`, `prompt`, `width`, `height`, `direction`, `count`, `format` | Sync or Async |
| `genai-generate-image-bleed`            | Print bleed margin                   | `image[_url]`, `bleed_size`, `format`, optional `prompt` | Sync       |
| `genai-image-inpainting-getresult`      | Poll inpaint/outpaint/expand/SmartBg | `inference_id`                                      | Sync poll  |
| `genai-text2video`                      | Text → video                         | `prompt`, `width`, `height`, `quality`, `audio`, `length`, `model` | Async |
| `genai-image2video`                     | Image → video                        | `image[_url]`, `prompt`, `quality`, `audio`, `length`, `model` | Async |
| `genai-text2video-getresult`            | Poll video generation                | `inference_id`                                      | Sync poll  |
| `genai-text2speech`                     | Text → speech audio                  | `text`, `language`, `model`, `voice`                | Async      |
| `genai-text2sound`                      | Text → music/sound effect            | `prompt`, `duration`, `loop`, `model`               | Async      |
| `genai-text2audio-getresult`            | Poll speech/sound generation         | `inference_id`                                      | Sync poll  |
| `genai-credits-balance`                 | Check credit balance                 | —                                                   | Sync       |

---

## Text2Text

### `genai-text2text-completions`

`POST /text2text/chat/completions`

OpenAI-style chat completion endpoint backed by a wide model selection
(OpenAI GPT-4/4.1/5 family, Anthropic Claude Sonnet, Google Gemini).

**Inputs:**

- `messages` (array, required) — Array of `{ role, content }` objects. `role`
  is one of `system`, `user`, `assistant`. The system message sets behavior;
  user messages are requests; assistant messages can seed prior context or
  desired-output examples.
- `max_tokens` (number, optional, default `512`) — Max tokens in response.
- `temperature` (number, optional, default `1`) — Sampling temperature.
- `model` (string, optional, nullable, default `urn:air:openai:model:openai:gpt-4o-mini@1`) — Pick a specific model. Available enums:
  - `urn:air:openai:model:openai:gpt-5@1`
  - `urn:air:openai:model:openai:gpt-5-search-api@1`
  - `urn:air:openai:model:openai:gpt-5.1@1`
  - `urn:air:openai:model:openai:gpt-5.1-chat@1`
  - `urn:air:openai:model:openai:gpt-5.2@1`
  - `urn:air:openai:model:openai:gpt-5-mini@1`
  - `urn:air:openai:model:openai:gpt-5-nano@1`
  - `urn:air:openai:model:openai:gpt-4o@1`
  - `urn:air:openai:model:openai:gpt-4o-mini@1`
  - `urn:air:openai:model:openai:gpt-4o-search-preview@1`
  - `urn:air:openai:model:openai:gpt-4-turbo@1`
  - `urn:air:openai:model:openai:gpt-4.1@1`
  - `urn:air:openai:model:openai:gpt-4.1-mini@1`
  - `urn:air:openai:model:openai:gpt-4.1-nano@1`
  - `urn:air:openai:model:openai:gpt-3.5-turbo@1`
  - `urn:air:anthropic:model:anthropic:claude-sonnet-4-5-latest@1`
  - `urn:air:anthropic:model:anthropic:claude-sonnet-4-6@1`
  - `urn:air:google:model:google:gemini-2.0-flash-001@1`
  - `urn:air:google:model:google:gemini-2.0-flash-lite@1`
  - `urn:air:google:model:google:gemini-2.5-pro@1`
  - `urn:air:google:model:google:gemini-2.5-flash@1`
  - `urn:air:google:model:google:gemini-3-pro-preview@1`

**Output:** Synchronous. Returns `{ status, data: <text string> }`.

**Async?** No — fully synchronous.

**Tips:**
- Use a `system` message to set persona/tone, then `user` for the actual ask.
- Pick a `*-search-*` model when the user needs fresh web-grounded answers.
- Lower `temperature` for deterministic outputs; raise for creative copy.

---

## Text2Image

### `genai-text2image`

`POST /text2image`

Generate one or more images from a text prompt. Output max 1024x1024.

**Inputs:**

- `prompt` (string, required) — Positive prompt describing the desired image.
- `negative_prompt` (string, optional, **deprecated**) — Things to avoid. Phrase
  positively (e.g. `distorted faces`, not `no distorted faces`).
- `width` (number, optional, default `1024`, min `64`, max `1024`) — Drives
  aspect ratio + resolution tier; provider snaps to closest supported size.
- `height` (number, optional, default `1024`, min `64`, max `1024`) — Same as
  above. Common supported ratios: `1:1`, `4:3`, `3:4`, `16:9`, `9:16`, `21:9`.
- `count` (number, optional, default `2`, min `1`, max `10`) — Number of images.
- `model` (string, optional, nullable, default `urn:air:sdxl:model:fluxai:flux_kontext_max@1`) — Available:
  - Flux: `urn:air:sdxl:model:fluxai:flux_kontext_max@1`, `urn:air:sdxl:model:fluxai:flux_kontext_pro@1`, `urn:air:fluxai:model:fluxai:flux-2-flex@1`, `urn:air:fluxai:model:fluxai:flux-2-pro@1`, `urn:air:fluxai:model:fluxai:flux-2-max@1`
  - Google Gemini image: `urn:air:google:model:google:gemini-2.5-flash-image@1`, `urn:air:google:model:google:gemini-3-pro-image-preview@1`, `urn:air:google:model:google:gemini-3.1-flash-image-preview@1`, `urn:air:google:model:google:gemini-3.1-pro-preview@1`
  - Hunyuan: `urn:air:hunyuan:model:hunyuan:hunyuan-image@3`
  - Ideogram: `urn:air:ideogram:model:ideogram:ideogram@1`, `…@2`, `…ideogram-turbo@1`, `…ideogram-turbo@2`, `…ideogram-2a@1`, `…ideogram-2a-turbo@1`, `…ideogram@3`
  - Google Imagen: `urn:air:google:model:google:imagen-4.0-generate-001@1`, `…imagen-4.0-ultra-generate-001@1`, `…imagen-4.0-fast-generate-001@1`
  - OpenAI: `urn:air:openai:model:openai:dall-e-3@1`, `urn:air:openai:model:openai:gpt-image-1@1`, `urn:air:openai:model:openai:gpt-image-1.5@1`
  - Qwen: `urn:air:qwen:model:qwen:qwen-image-2.5@1`
  - Reve: `urn:air:reve:model:reve:reve@1`
  - Runway: `urn:air:runway:model:runway:gen4-image-ref@1`
  - Seedream: `urn:air:seedream:model:seedream:seedream@4.0`, `…@4.5`, `…@5.0-lite`

**Output:** `202` returns `{ status, inference_id }`. Poll via
`genai-text2image-getresult`.

**Async?** Yes → `genai-text2image-getresult`.

**Tips:**
- Frontload subject + style + lighting + composition cues (e.g. "studio
  lighting, cinematic, shallow depth of field").
- Don't use `negative_prompt` (deprecated). Express avoidance positively
  inside the main prompt instead.
- Ideogram models excel at in-image text and typography; Imagen/Flux for
  photoreal; Seedream for stylized.

### `genai-text2image-getresult`

`GET /text2image/inferences/{inference_id}`

Fetch generated images for a prior `genai-text2image` submission.

**Inputs:**

- `inference_id` (string, path, required) — Returned by `genai-text2image`.

**Output:** `200` returns `{ status: "success", data: [{ id, url, status }] }`.
`202` means still processing.

**Async?** This is the poll endpoint.

**Tips:**
- Poll roughly every 2–3 seconds until `status == "success"`.
- Final image URLs are the values you return to the user.

---

### `genai-text2sticker`

`POST /text2sticker`

Sticker generation from a prompt. Output max 1024x1024.

**Inputs:**

- `prompt` (string, required) — Sticker description.
- `negative_prompt` (string, optional, **deprecated**).
- `width` (number, optional, default `1024`, min `64`, max `1024`).
- `height` (number, optional, default `1024`, min `64`, max `1024`).
- `count` (number, optional, default `2`, min `1`, max `10`).
- `model` (string, optional, nullable, default `urn:air:sdxl:model:fluxai:flux_kontext_max@1`) — same enum list as `genai-text2image`.

**Output:** `202` → `{ status, inference_id }`.

**Async?** Yes → `genai-text2sticker-getresult`.

**Tips:**
- Add explicit sticker cues to the prompt: "die-cut sticker, white border,
  vivid flat colors, vector style".
- Prefer Ideogram or Flux models for clean sticker outlines and crisp text.

### `genai-text2sticker-laser-engraving`

`POST /text2sticker/laserengraving`

Sticker variant that produces a laser-engraving look (monochrome on
background, optional SVG output for cutting/engraving workflows).

**Inputs:**

- `prompt` (string, required).
- `negative_prompt` (string, optional, **deprecated**).
- `width`, `height`, `count` — same as `genai-text2sticker`.
- `engrave_color` (string, optional, default `black`) — Hex code (`#82d5fa`,
  `#fff`, 4/8-digit hex for alpha like `#18d4ff87`) or color name.
- `background_color` (string, optional, default `white`) — Same color format.
- `format` (string, optional, default `JPG`) — One of `JPG`, `PNG`, `WEBP`, `SVG`.
- `model` (string, optional, nullable, default `urn:air:sdxl:model:fluxai:flux_kontext_max@1`) — Allowed: `urn:air:sdxl:model:fluxai:flux_kontext_max@1`, `urn:air:sdxl:model:fluxai:flux_kontext_pro@1`.

**Output:** `202` → `{ status, inference_id }`.

**Async?** Yes → `genai-text2sticker-getresult`.

**Tips:**
- Pick `format: SVG` when the user needs vector output for a laser cutter.
- Keep contrast high between `engrave_color` and `background_color`.

### `genai-text2sticker-getresult`

`GET /text2sticker/inferences/{inference_id}`

Poll result for both standard and laser-engraving sticker submissions.

**Inputs:**

- `inference_id` (string, path, required).

**Output:** `200` → `{ status, data: [{ id, url, status }] }`; `202` while processing.

---

### `genai-generate-logo`

`POST /logo`

Logo generation conditioned on brand info and (optionally) a reference image.

**Inputs:**

- `brand_name` (string, required) — Brand or company name.
- `business_description` (string, required) — What the business does.
- `color_tone` (string, optional, default `Auto`) — One of `Auto`, `Gray`,
  `Blue`, `Pink`, `Orange`, `Brown`, `Yellow`, `Green`, `Purple`, `Red`.
- `logo_description` (string, optional) — Free-form description of desired
  shapes, motifs, mood.
- `reference_image` (binary, optional) — Inline reference logo file.
- `reference_image_url` (string URI, optional, max 2083 chars) — URL to a
  reference logo. **Only one reference parameter may be set at a time.**
- `reference_image_id` (string, optional, **deprecated**) — Previously uploaded image ID.
- `count` (number, optional, default `2`, min `1`, max `10`) — Number of logos.
- `model` (string, optional, nullable, default `urn:air:ideogram:model:ideogram:ideogram@2`) — Same broad enum as `genai-text2image`.

**Output:** `202` → `{ status, inference_id }`.

**Async?** Yes → `genai-generate-logo-getresult`.

**Tips:**
- Ideogram models (the default) are strongest for legible logo text.
- Pass either `reference_image` *or* `reference_image_url`, never both.
- Use `logo_description` to constrain style (e.g. "minimal flat geometric
  monogram, no gradients").

### `genai-generate-logo-getresult`

`GET /logo/inferences/{inference_id}`

Poll the logo generation result.

**Inputs:**

- `inference_id` (string, path, required).

**Output:** `200` → `{ status, data: [{ id, url, status }] }`; `202` while processing.

---

## Image2Image / Inpainting

All endpoints in this group accept `multipart/form-data`. Each accepts the
image either as a file (`image`) or a URL (`image_url`). The deprecated
`image_id` is also accepted. **Exactly one image-source parameter must be
set per call.**

### `genai-image-edit`

`POST /painting/edit`

Edit an existing image guided by a prompt — apply transformations, style
changes, content swaps, etc.

**Inputs:**

- `image` (binary, optional) — Source image file.
- `image_url` (string URI, optional, max 2083 chars).
- `image_id` (string, optional, **deprecated**).
- `prompt` (string, required) — Description of the desired edit.
- `count` (integer, optional, default `2`, min `1`, max `10`).
- `format` (string, optional, default `JPG`) — One of `JPG`, `PNG`, `WEBP`.
- `mode` (string, optional, **deprecated**, default `sync`) — `sync` or
  `async`. Prefer the standard HTTP `Prefer` header (RFC 7240) instead.
- Watermark params (all optional):
  - `watermark_enabled` (boolean, default `false`, nullable) — Add AI-generated marker.
  - `watermark_url` (string URI, nullable) — Custom watermark image.
  - `watermark_anchor_point` (string, default `left-bottom`) — One of
    `left-top`, `left-middle`, `left-bottom`, `center-top`, `center-middle`,
    `center-bottom`, `right-top`, `right-middle`, `right-bottom`, `pattern`.
  - `watermark_width` (integer, min `1`, nullable).
  - `watermark_height` (integer, min `1`, nullable).
  - `watermark_opacity` (integer, default `50`, min `0`, max `100`, nullable).
  - `watermark_angle` (integer, min `0`, max `360`, nullable). Default `45` for `pattern`, else `0`.
  - `watermark_padding_x` (integer, min `0`, default `0`, nullable).
  - `watermark_padding_y` (integer, min `0`, default `0`, nullable).
- `model` (string, optional, nullable, default `urn:air:sdxl:model:fluxai:flux_kontext_max-image-to-image@1`):
  - Flux: `urn:air:sdxl:model:fluxai:flux_kontext_max-image-to-image@1`, `urn:air:sdxl:model:fluxai:flux_kontext_pro-image-to-image@1`, `urn:air:fluxai:model:fluxai:flux-2-flex-image-to-image@1`, `urn:air:fluxai:model:fluxai:flux-2-pro-image-to-image@1`, `urn:air:fluxai:model:fluxai:flux-2-max-image-to-image@1`
  - Seedream: `urn:air:seedream:model:seedream:seedream-4.0-image-to-image@1`, `…4.5-image-to-image@1`, `…5.0-lite-image-to-image@1`
  - Google: `urn:air:google:model:google:gemini-2.5-flash-image-image-to-image@1`, `…gemini-3-pro-image-preview-image-to-image@1`, `…gemini-3.1-flash-image-preview-image-to-image@1`, `…gemini-3.1-pro-preview-image-to-image@1`
  - OpenAI: `urn:air:openai:model:openai:gpt-image-1-image-to-image@1`
  - Reve: `urn:air:reve:model:reve:reve-edit-image-to-image@1`
  - Runway: `urn:air:runway:model:runway:gen4-image-ref-image-to-image@1`
  - Qwen: `urn:air:qwen:model:qwen:qwen-image-image-to-image@1`, `urn:air:qwen:model:qwen:qwen-image-edit-plus-image-to-image@1`
  - xAI: `urn:air:xai:model:xai:grok-imagine-image-edit-image-to-image@1`

**Output:** May complete synchronously (`200`, `{ status, data: [{ id, url }] }`) or asynchronously (`202`, `{ status, inference_id }`).

**Async?** Sometimes. When `202`, poll `genai-image-inpainting-getresult`.

**Tips:**
- Use `genai-image-edit` for free-form transformations ("turn this car red",
  "make it night-time"). Use `genai-image-inpainting` instead when the user
  wants the change confined to a specific area.
- Enable `watermark_enabled` when the user/policy requires labeling
  AI-generated outputs.

### `genai-image-inpainting`

`POST /painting/inpaint`

Inpaint the inside of a masked region of an image — or, with a single RGBA,
fill the inner transparent area. Both image and mask use the same multipart
inputs.

**Inputs:**

- `image` / `image_url` / `image_id` — Source image (one of, RGBA).
- `mask_image` (binary, optional) — Mask file matching the image size.
- `mask_image_url` (string URI, optional, max 2083 chars).
- `mask_image_id` (string, optional, **deprecated**).
- `prompt` (string, required) — What to paint inside the masked region.
- `negative_prompt` (string, optional, **deprecated**).
- `count` (integer, optional, default `2`, min `1`, max `10`).
- `format` (string, optional, default `JPG`) — `JPG`, `PNG`, or `WEBP`.
- `mode` (string, optional, **deprecated**, default `sync`) — `sync` or `async`.

**Output:** `200` (sync) `{ status, data: [{ id, url }] }`, or `202` (async) `{ status, inference_id }`.

**Async?** Sometimes. When `202`, poll `genai-image-inpainting-getresult`.

**Tips:**
- Use Single Image Mode (no `mask_image`) when the source already has a
  transparent area you want filled.
- Match mask dimensions exactly to the source image; white = paint, black = keep.
- Prefer `genai-remove-object` when the goal is purely to erase, not replace.

### `genai-image-outpainting`

`POST /painting/outpaint`

Reverse of inpainting: paint *outside* a masked region (i.e. extend beyond
or replace background while preserving subject).

**Inputs:** Identical to `genai-image-inpainting`:

- `image` / `image_url` / `image_id` (one of).
- `mask_image` / `mask_image_url` / `mask_image_id` (one of, optional).
- `prompt` (string, required).
- `negative_prompt` (deprecated).
- `count` (integer, default `2`, min `1`, max `10`).
- `format` (`JPG` | `PNG` | `WEBP`, default `JPG`).
- `mode` (deprecated).

**Output:** `200` (sync) or `202` (async) → poll `genai-image-inpainting-getresult`.

**Async?** Sometimes. When `202`, poll `genai-image-inpainting-getresult`.

**Tips:**
- For "extend canvas to wider aspect" use `genai-expand-image` instead — it
  has explicit width/height/direction inputs and handles the math for you.
- For "replace everything except subject", consider `genai-smart-background`.

### `genai-smart-background`

`POST /painting/replace-background`

AI-generated background replacement driven by a description (no need to
supply a background image, unlike the classic `removebg` flow).

**Inputs:**

- `image` / `image_url` / `image_id` — Source image with subject.
- `prompt` (string, required) — Description of the new background scene.
- `negative_prompt` (string, optional, **deprecated**).
- `count` (integer, default `2`, min `1`, max `10`).
- `format` (`JPG` | `PNG` | `WEBP`, default `JPG`).
- `mode` (deprecated).

**Output:** `200` (sync) or `202` (async) → poll `genai-image-inpainting-getresult`.

**Async?** Sometimes. When `202`, poll `genai-image-inpainting-getresult`.

**Tips:**
- Be specific in the prompt about scene, lighting, time of day; the model
  will try to match lighting on the subject.
- For a fixed reference background (literal image substitution) the user
  should use the classic Image API `removebg` `bg_image` flow instead.

### `genai-remove-object`

`POST /painting/remove-object`

Remove an object cleanly given a mask. Uses a model tuned for clean
removals (better than inpainting with an empty prompt for this case).

**Inputs:**

- `image` / `image_url` / `image_id`.
- `mask_image` / `mask_image_url` / `mask_image_id` (masked area = what to remove).
- `format` (`JPG` | `PNG` | `WEBP`, default `JPG`).
- `mode` (deprecated, default `sync`) — `sync`, `async`, or `auto`.

**Output:** `200` (sync) `{ data: { id, url }, status }`, or `202` (async) `{ status, inference_id }`.

**Async?** Sometimes. When `202`, poll `genai-image-inpainting-getresult`.

**Tips:**
- No `prompt` parameter — this endpoint is purely removal-driven.
- For "remove and replace with something specific", use
  `genai-image-inpainting` with a prompt instead.

### `genai-expand-image`

`POST /painting/expand`

Generative resize: enlarge an image to a target width/height, optionally
biasing where new pixels are added.

**Inputs:**

- `image` / `image_url` / `image_id`.
- `prompt` (string, required) — Hint for what the new edges should depict.
- `negative_prompt` (string, optional, **deprecated**).
- `width` (integer, optional, default `1024`, max `8000`) — Must exceed source width.
- `height` (integer, optional, default `1024`, max `8000`) — Must exceed source height.
- `direction` (string, optional, default `center`) — One of:
  - `center` — expand in all directions, source stays centered.
  - `top-left` — source ends up bottom-right corner.
  - `top-right` — source ends up bottom-left corner.
  - `bottom-left` — source ends up top-right corner.
  - `bottom-right` — source ends up top-left corner.
- `count` (integer, optional, default `2`, min `1`, max `2`).
- `format` (`JPG` | `PNG` | `WEBP`, default `JPG`).
- `mode` (deprecated, default `sync`) — `sync`, `async`, `auto`.

**Output:** `200` (sync) or `202` (async) → poll `genai-image-inpainting-getresult`.

**Async?** Sometimes. When `202`, poll `genai-image-inpainting-getresult`.

**Tips:**
- Target dimensions must be larger than the source — this is an enlarge
  operation, not a crop.
- The prompt should describe what should appear in the newly generated
  area, e.g. "ocean horizon and clear blue sky".

### `genai-generate-image-bleed`

`POST /painting/bleed`

Add a print-safe bleed margin around an image (continuation of the existing
edges, sized in pixels). Designed for print production.

**Inputs:**

- `image` / `image_url` / `image_id`.
- `prompt` (string, optional) — Usually leave empty; default bleed prompt is
  pre-tuned. Only set if you're confident.
- `negative_prompt` (string, optional, **deprecated**).
- `bleed_size` (integer, required, default `5`, min `1`, max `75`) — Bleed in
  pixels. For 300 DPI 0.125-inch bleed, compute `300 * 0.125 = ~38`.
- `format` (`JPG` | `PNG` | `WEBP`, default `JPG`).

**Output:** `200` (sync) `{ data: { id, url }, status }`. No `202` path.

**Async?** No — synchronous only.

**Tips:**
- This is for print bleed, not for creatively extending an image — for
  artistic expansion use `genai-expand-image`.
- Compute `bleed_size` from DPI × inches; the default `5` is rarely correct.

### `genai-image-inpainting-getresult`

`GET /painting/{inference_id}`

Single poll endpoint for all asynchronous painting endpoints: inpaint,
outpaint, smart background, expand, edit, remove-object.

**Inputs:**

- `inference_id` (string, path, required).

**Output:** `200` → `{ status, data: [{ id, url }] }`; `202` while processing.

---

## Text2Video & Image2Video

Video generation always returns asynchronously. Only one video per request
(no `count`). Output resolution/quality/length is best-effort: the provider
snaps to the closest supported value for the chosen model.

### `genai-text2video`

`POST /text2video`

Generate a single video from a text prompt.

**Inputs:**

- `prompt` (string, required) — Scene/action description.
- `width` (number, optional, default `1024`, min `64`, max `1024`) — Drives
  aspect ratio; provider snaps to closest. Common: `1:1`, `4:3`, `3:4`,
  `16:9`, `9:16`, `21:9`.
- `height` (number, optional, default `1024`, min `64`, max `1024`).
- `quality` (string, optional, default `480p`) — One of `480p`, `720p`, `1080p`.
- `audio` (boolean, optional, default `false`) — Request audio in the video.
  Some models (e.g. Grok Imagine Video / OVI) **always** emit audio regardless
  of this flag.
- `length` (number, optional, default `3`, min `1`, max `20`) — Seconds; snapped to nearest supported by the model.
- `model` (string, optional, nullable, default `urn:air:wan:model:wan:wan-2.7-text-to-video@1`):
  - Seedance: `urn:air:seedance:model:seedance:seedance-1.0-pro-text-to-video@1`, `…-1.0-pro-fast-text-to-video@1`, `…-1.5-pro-text-to-video@1`
  - Pika: `urn:air:pika:model:pika:pika-text-to-video-v2.2@1`
  - Kling: `…kling-v2-master-text-to-video@1`, `…v2-1-master-…`, `…v2-5-turbo-…`, `…v2-6-…`, `…v3-…`
  - Runway: `urn:air:runway:model:runway:gen4.5-text-to-video@1`
  - MiniMax Hailuo: `urn:air:minimax:model:minimax:hailuo-02-pro-text-to-video@1`
  - LTXV: `urn:air:ltxv:model:ltxv:ltxv-2-text-to-video@1`, `…ltxv-2-text-to-video-fast@1`
  - OVI: `urn:air:ovi:model:ovi:ovi-text-to-video@1`
  - xAI Grok: `urn:air:xai:model:xai:grok-imagine-video-text-to-video@1`
  - Google Veo: `…veo-2.0-text-to-video@1`, `…veo-2.0-exp-…`, `…veo-3.1-…`, `…veo-3.1-fast-…`, `…veo-3.1-preview-…`, `…veo-3.1-fast-preview-…`
  - Wan: `urn:air:wan:model:wan:wan-2.7-text-to-video@1`

**Output:** `202` → `{ status, inference_id }`.

**Async?** Yes → `genai-text2video-getresult`.

**Tips:**
- Treat `quality`, `length`, and aspect-ratio as best-effort hints; run a
  test render before committing to a specific model.
- For motion-heavy prompts, Kling / Seedance generally produce more dynamic
  results; Veo is strongest for cinematic-looking outputs.
- Don't bother flipping `audio: false` if you're using Grok Imagine / OVI;
  they always produce audio.

### `genai-image2video`

`POST /image2video`

Animate a still image into a video, optionally conditioned by a prompt.
Multipart upload (image file or URL).

**Inputs:**

- `image` / `image_url` / `image_id` — Source frame (one of).
- `prompt` (string, required) — Description of motion / action.
- `width`, `height`, `quality`, `audio`, `length` — same as `genai-text2video`.
- `model` (string, optional, nullable, default `urn:air:wan:model:wan:wan-2.7-image-to-video@1`):
  - Seedance: `…seedance-1.0-pro-image-to-video@1`, `…1.0-pro-fast-…`, `…1.5-pro-…`
  - Kling: `…kling-v2-master-image-to-video@1`, `…v2-1-master-…`, `…v2-1-image-to-video@1`, `…v2-5-turbo-…`, `…v2-6-…`, `…v3-…`
  - Runway: `urn:air:runway:model:runway:gen4.5-image-to-video@1`
  - Luma: `…ray-1-6-image-to-video@1`, `…ray-2-…`, `…ray-flash-2-…`, `…photon-1-…`, `…photon-flash-1-…`
  - Google Veo: `…veo-2.0-image-to-video@1`, `…veo-2.0-exp-…`, `…veo-3.1-…`, `…veo-3.1-fast-…`, `…veo-3.1-preview-…`, `…veo-3.1-fast-preview-…`
  - Wan: `…wan-2.5-image-to-video@1`, `…wan-2.6-…`, `…wan-2.7-…`
  - MiniMax Hailuo: `…hailuo-02-pro-image-to-video@1`
  - OVI: `urn:air:ovi:model:ovi:ovi-image-to-video@1`
  - xAI Grok: `…grok-imagine-video-image-to-video@1`

**Output:** `202` → `{ status, inference_id }`.

**Async?** Yes → `genai-text2video-getresult` (shared poll endpoint).

**Tips:**
- Phrase the prompt around motion ("camera slowly pans right", "subject
  smiles and looks at camera"); the still image already supplies the look.
- Luma `photon` / `ray-flash` variants are faster; pick the non-flash
  variants for higher fidelity.

### `genai-text2video-getresult`

`GET /video/{inference_id}`

Poll endpoint for both `genai-text2video` and `genai-image2video`.

**Inputs:**

- `inference_id` (string, path, required).

**Output:** `200` → `{ status, data: { id, url } }` (one video object);
`202` while processing.

**Tips:**
- Video jobs typically take longer than image jobs; poll every 5–10 seconds.

---

## Text2Audio

### `genai-text2speech`

`POST /text2speech`

Generate spoken audio from text (TTS).

**Inputs:**

- `text` (string, required, not nullable) — Up to **5000 characters**.
- `language` (string, optional, default `en`) — One of `en`, `fr`.
- `model` (string, optional, nullable, default `urn:air:openai:model:openai:tts-1@1`):
  - `urn:air:openai:model:openai:tts-1@1`
  - `urn:air:elevenlabs:model:elevenlabs:eleven-v3@1`
  - `urn:air:async:model:async:async-flash-v1.0@1`
- `voice` (string, optional, nullable) — Voice name. **Available voices vary
  by provider and change over time** — see each provider's docs. Defaults
  when omitted:
  - OpenAI → `alloy`
  - ElevenLabs → `Rachel`
  - Async → `nyomi`

**Output:** `202` → `{ status, inference_id }`.

**Async?** Yes → `genai-text2audio-getresult`.

**Tips:**
- Pre-clean text: collapse multiple spaces, expand abbreviations the user
  cares about (e.g. "Dr." → "Doctor") for predictable pronunciation.
- For long content, split into chunks under 5000 chars and call multiple times.
- Provider-specific voices: pass them through verbatim; the API does not
  validate the voice list.

### `genai-text2sound`

`POST /text2sound`

Generate music or sound effects from a text prompt.

**Inputs:**

- `prompt` (string, required, not nullable) — Description of the sound or
  music (e.g. "lo-fi hip hop with vinyl crackle", "thunderclap with rain").
- `duration` (number, optional, nullable, min `0.5`, max `22`) — Length in
  seconds. Vendor limits: ElevenLabs 0.5–22; Kling 3–10. Auto if omitted.
- `loop` (boolean, optional, default `false`) — Produce loopable audio.
  **ElevenLabs only** — silently ignored by other models.
- `model` (string, optional, nullable, default `urn:air:elevenlabs:model:elevenlabs:elevenlabs-sound-effects-v2@1`):
  - `urn:air:elevenlabs:model:elevenlabs:elevenlabs-sound-effects-v2@1`
  - `urn:air:kling:model:kling:kling-text-to-audio@1`

**Output:** `202` → `{ status, inference_id }`.

**Async?** Yes → `genai-text2audio-getresult`.

**Tips:**
- ElevenLabs leans toward sound effects / foley; Kling is broader (music
  + ambient).
- Only use `loop: true` if you actually need a seamless loop *and* you're
  on the ElevenLabs model.

### `genai-text2audio-getresult`

`GET /audio/{inference_id}`

Poll endpoint for both `genai-text2speech` and `genai-text2sound`.

**Inputs:**

- `inference_id` (string, path, required).

**Output:** `200` → `{ status, data: { id, url } }`; `202` while processing.
The `url` points to the generated audio file.

---

## Utilities

### `genai-credits-balance`

`GET /balance`

Return the remaining Picsart credits for the API key in use.

**Inputs:** None.

**Output:** Synchronous `{ credits: <integer> }`.

**Async?** No.

**Tips:**
- Useful as a preflight check before kicking off an expensive video job.

---

## Async workflow

Most generation operations are asynchronous. The POST returns
`{ status: "processing" | "accepted" | …, inference_id: "<uuid>" }` (HTTP
`202`). Callers MUST then poll the matching `-getresult` tool until
`status == "success"` (HTTP `200` with `data` populated).

Submit → poll pairs:

| Submit tool                              | Poll tool                            |
| ---------------------------------------- | ------------------------------------ |
| `genai-text2image`                       | `genai-text2image-getresult`         |
| `genai-text2sticker`                     | `genai-text2sticker-getresult`       |
| `genai-text2sticker-laser-engraving`     | `genai-text2sticker-getresult`       |
| `genai-generate-logo`                    | `genai-generate-logo-getresult`      |
| `genai-image-edit` *(if 202)*            | `genai-image-inpainting-getresult`   |
| `genai-image-inpainting` *(if 202)*      | `genai-image-inpainting-getresult`   |
| `genai-image-outpainting` *(if 202)*     | `genai-image-inpainting-getresult`   |
| `genai-smart-background` *(if 202)*      | `genai-image-inpainting-getresult`   |
| `genai-remove-object` *(if 202)*         | `genai-image-inpainting-getresult`   |
| `genai-expand-image` *(if 202)*          | `genai-image-inpainting-getresult`   |
| `genai-text2video`                       | `genai-text2video-getresult`         |
| `genai-image2video`                      | `genai-text2video-getresult`         |
| `genai-text2speech`                      | `genai-text2audio-getresult`         |
| `genai-text2sound`                       | `genai-text2audio-getresult`         |

**Polling guidance:**

- Images / stickers / logos / paintings: poll every **2–3 seconds**.
- Videos: poll every **5–10 seconds**; full jobs can take 30s–several minutes.
- Audio: poll every **2–5 seconds**.
- Stop polling on first `status == "success"` (or `status == "error"`).
- Surface the returned `url` (or `data[].url`) to the user as the final
  artifact. The MCP server does not download the file for you.

**Sync/Async behavior of painting endpoints:**
`genai-image-edit`, `genai-image-inpainting`, `genai-image-outpainting`,
`genai-smart-background`, `genai-remove-object`, and `genai-expand-image`
all return `200` (with results) **or** `202` (with `inference_id`)
depending on processing time. Always branch on the response shape: if you
get an `inference_id` instead of a `data` array/object, poll
`genai-image-inpainting-getresult`.

The legacy `mode` parameter (`sync`/`async`) is **deprecated**. To force a
mode, use the standard HTTP `Prefer` header (RFC 7240). The MCP server
forwards request headers, so a caller can pass `Prefer: respond-async` or
`Prefer: wait=NN` to influence behavior.

---

## Speech and sound — explicit guide

The two audio generation tools share a single poll endpoint
(`genai-text2audio-getresult`) but have distinct purposes.

### Generating speech (`genai-text2speech`)

1. Call `genai-text2speech` with:
   - `text` — what to say (up to 5000 characters).
   - `language` — `en` (default) or `fr`.
   - Optionally `model` — one of:
     - `urn:air:openai:model:openai:tts-1@1` (default)
     - `urn:air:elevenlabs:model:elevenlabs:eleven-v3@1`
     - `urn:air:async:model:async:async-flash-v1.0@1`
   - Optionally `voice` — pass the provider-specific voice name. The voice
     list is **not** in the OpenAPI spec because it changes over time; refer
     to OpenAI / ElevenLabs / Async docs for current options. Defaults are
     `alloy` (OpenAI), `Rachel` (ElevenLabs), `nyomi` (Async).
2. Read `inference_id` from the response.
3. Poll `genai-text2audio-getresult` with that `inference_id` every 2–5
   seconds until `status == "success"`.
4. The `data.url` returned by the poll is the audio file URL. Output format
   is not user-selectable; the file format is whatever the underlying
   provider returns (typically MP3/M4A from OpenAI/ElevenLabs).

### Generating music / sound effects (`genai-text2sound`)

1. Call `genai-text2sound` with:
   - `prompt` — describe the desired sound (e.g. "soft rainfall on a tin
     roof", "epic orchestral cinematic build with timpani").
   - Optionally `duration` — seconds, between 0.5 and 22. Honor vendor
     ranges: ElevenLabs 0.5–22, Kling 3–10. If you omit it, the model
     auto-picks.
   - Optionally `loop` — `true` for seamless looping. **Only ElevenLabs
     supports this**; ignored on Kling.
   - Optionally `model`:
     - `urn:air:elevenlabs:model:elevenlabs:elevenlabs-sound-effects-v2@1` (default; best for SFX)
     - `urn:air:kling:model:kling:kling-text-to-audio@1` (better for music/ambient)
2. Read `inference_id`.
3. Poll `genai-text2audio-getresult` until success.
4. Use `data.url` from the poll response. Output is an audio file URL.

### Common pitfalls

- Don't confuse the tools: `genai-text2speech` is for spoken words;
  `genai-text2sound` is for non-speech audio and music.
- A user request like "narrate this in a deep voice" → `genai-text2speech`
  with an appropriate `voice`. A request like "background music for a
  trailer" → `genai-text2sound` with a music-capable model.
- The MCP server does not transcode audio. Give the user the URL as-is, or
  if they need a specific format, do that conversion client-side.

---

## Cross-cutting notes

- **Authentication:** all endpoints require `X-Picsart-API-Key` (handled
  by the MCP server, not a tool input).
- **Image sources:** for every multipart endpoint, the source image and
  mask each accept either a file (`image` / `mask_image`) or URL
  (`image_url` / `mask_image_url`). Set exactly one of each. The `_id`
  variants are deprecated.
- **Deprecated parameters:** `negative_prompt`, `mode`, `*_id`,
  `reference_image_id`. Avoid these in new calls.
- **Watermarking** is only available on `genai-image-edit`. Other paint
  endpoints do not accept watermark parameters; for cross-tool watermarking
  use the Picsart Image API `image-add-watermark` tool.
- **Counts:** image tools accept `count` 1–10 (except `genai-expand-image`
  which caps at 2). Video and audio tools return a single asset per call.
- **Aspect-ratio matching:** the API snaps `width`/`height` to the closest
  ratio the chosen model supports. Verify the output before assuming an
  exact size; do test renders before committing to a workflow.
