# Picsart Video API — MCP Tool Reference

Programmable video and audio tools wrapping Picsart's Video API as MCP operations. Coverage: video enhancement (FPS upscale), background removal/replacement, color/audio adjustments, 40+ visual effects, edit/trim/crop/fit/concat, watermarking, metadata + thumbnail read/write, CTV ad encoding, audio extraction, multi-language transcription, file upload, and credit balance.

- **Base URL:** `https://video-api.picsart.io/v1`
- **Auth:** `apiKey` header (Picsart API key)
- **Async:** Almost every transformation returns `202 { transaction_id, status }`. Poll the matching `-getresult` tool until `status: success` to obtain the result URL. Synchronous tools: `video-metadata`, `video-get-thumbnail`, `video-upload`, `video-credits-balance`.

## Tool index

| MCP tool | Purpose | Key inputs | Sync/Async |
|---|---|---|---|
| `video-upscale-fps` | Upscale low-FPS video to 60FPS (generative) | `video_url` | async |
| `video-upscale-fps-getresult` | Fetch FPS upscale result | `transaction_id` | sync poll |
| `video-remove-background` | Remove or replace video background | `video_url`, `bg_color`/`bg_image_url` | async (use `video-getresult`) |
| `video-adjust` | Color/audio/speed adjustments (14 dials) | `video_url`, AdjustParameters, ExportParameters | async (`video-getresult`) |
| `video-apply-effect` | Apply one named visual effect | `video_url`, `effect_name`, ExportParameters | async (`video-getresult`) |
| `video-edit` | Combined edit: fit + crop + extended export (codec, quality, bitrate) | `video_url`, EditParameters, ExtendedExportParameters | async (`video-getresult`) |
| `video-trim` | Trim by start/end ms | `video_url`, `start`, `end`, ExportParameters | async (`video-getresult`) |
| `video-crop` | Pixel-coordinate crop | `video_url`, `width`/`height`/`start_x`/`start_y`, ExportParameters | async (`video-getresult`) |
| `video-concat` | Concatenate clips/images with transitions | `items[]`, optional `bg_audio_*`, ExportParameters | async (`video-getresult`) |
| `video-concat-highlights` | Concat trimmed segments of one video | `video_url`, `trim_segments[]`, ExportParameters | async (`video-getresult`) |
| `video-fit` | Resize/letterbox to ratio or w/h | `video_url`, FitParameters | async (`video-getresult`) |
| `video-metadata` | Read codec/resolution/duration/etc. | `video_url` | sync |
| `video-get-thumbnail` | Extract up to 4 frames as thumbnails | `video_url`, `source`, `timestamps[]` | sync |
| `video-set-thumbnail` | Set/replace embedded video thumbnail | `video_url`, `image`/`image_url` | async (`video-set-thumbnail-getresult`) |
| `video-set-thumbnail-getresult` | Fetch new-thumbnail result | `transaction_id` | sync poll |
| `video-encode-ctv` | Re-encode video to meet CTV ad requirements | `video_url` | async (`video-getresult`) |
| `video-adjust-audio` | Adjust audio volume / add audio track | `video_url`, `audio_url`, volumes | async (`video-getresult`) |
| `video-extract-audio` | Export audio track from video | `video_url`, audio `format` | async (`video-getaudioresult`) |
| `video-transcribe-audio` | Speech-to-text (60 languages) | `file_url`, `language`, `format`, `granularity` | async (`video-transcribe-audio-getresult`) |
| `video-transcribe-audio-getresult` | Fetch transcription result | `transaction_id` | sync poll |
| `video-add-watermark` | Overlay image watermark | `video_url`, `watermark`/`watermark_url`, placement | async (`video-getresult`) |
| `video-getresult` | Generic video-result poller | `transaction_id` | sync poll |
| `video-getaudioresult` | Audio-result poller | `transaction_id` | sync poll |
| `video-upload` | Upload binary file, get hosted URL | `file` (binary) | sync |
| `video-credits-balance` | Check remaining credits | — | sync |

---

## Video enhancement

### `video-upscale-fps`
`POST /upscale/fps` — Upscale low-FPS video to 60FPS high-quality video using generative AI.

**Inputs:**
- `video_url` (string, uri, required) — Source video URL.

**Output:** `202 { transaction_id, status }` — async.

**Async?** Poll with `video-upscale-fps-getresult` until `status: success`, then `data.url` is the upscaled video.

**Tips:**
- Use only when source FPS is meaningfully below 60.
- This is a dedicated pipeline — must poll the `video-upscale-fps-getresult` endpoint, not the generic `video-getresult`.

### `video-upscale-fps-getresult`
`GET /upscale/fps/{transaction_id}` — Retrieve upscaled video for a given FPS-upscale transaction.

**Inputs:**
- `transaction_id` (string, path, required) — From `video-upscale-fps`.

**Output:** `200 { data: { id, url }, status: success }` when ready; `202 { status: processing|queued }` while still working.

---

## Remove Background

### `video-remove-background`
`POST /remove-background` — Remove the background or replace it with a color/image.

**Inputs:**
- `video_url` (string, uri, required) — Source video URL.
- `bg_color` (string, optional, default `#008800`) — Hex (`#82d5fa`, `#fff`, `#18d4ff87`, `#00000066`) or color name (e.g. `blue`). Use `transparent` or `#00000000` for full transparency (forces `.webm` export). Use either `bg_color` or `bg_image_url`.
- `bg_image_url` (string, uri, optional) — Background image URL. Use either `bg_color` or `bg_image_url`.

**Output:** `202 { transaction_id, status }`.

**Async?** Yes — poll via `video-getresult`.

**Tips:**
- For chroma-key/greenscreen workflows keep the default `#008800`.
- Transparent backgrounds force WEBM output; downstream tools may need to handle that.

---

## Effects

### `video-adjust`
`POST /adjust` — Apply up to 14 color/audio/motion adjustments in one pass.

**Inputs:**
- `video_url` (string, uri, required) — Source video URL.
- `audio_url` (string, optional) — Sound file URL to overlay.
- `audio_volume` (integer, 0–100, default 100) — Overlay audio volume.
- `video_volume` (integer, 0–100, default 100) — Source video volume.
- `brightness` (integer, -100 to 100, default 0)
- `contrast` (integer, -100 to 100, default 0)
- `clarity` (integer, -100 to 100, default 0)
- `saturation` (integer, -100 to 100, default 0)
- `hue` (integer, -100 to 100, default 0)
- `shadows` (integer, -100 to 100, default 0)
- `highlights` (integer, -100 to 100, default 0)
- `temperature` (integer, -100 to 100, default 0)
- `sharpen` (integer, 0–100, default 0)
- `noise` (integer, 0–100, default 0)
- `vignette` (integer, 0–100, default 0)
- `export` (object, optional) — ExportParameters: `format` (MOV/MP4/WEBM/GIF, default MP4), `frame_rate` (1–60, default 30), `bitrate` (1–10000 kb/s, auto if blank).

**Output:** `202 { transaction_id, status }`.

**Async?** Yes — `video-getresult`.

**Tips:**
- Values outside ranges silently fall back to default 0.
- No speed/reverse parameter is exposed in the schema despite the description mentioning it; use `video-edit` if you need codec/quality control.

### `video-apply-effect`
`POST /effects` — Apply one named visual effect.

**Inputs:**
- `video_url` (string, uri, required) — Source video URL.
- `effect_name` (string enum) — One of: `apr1`, `apr2`, `apr3`, `brnz1`, `brnz2`, `brnz3`, `brnz4`, `cyber1`, `cyber2`, `cyber3`, `icy1`, `icy2`, `icy3`, `icy4`, `mnch1`, `mnch2`, `mnch3`, `noise`, `ntrl1`, `ntrl2`, `ntrl3`, `pixelize`, `saturation`, `sft1`, `sft2`, `sft3`, `sft4`, `tl1`, `tl2`, `sharpen`, `vignette`, `Focal Zoom`, `Lens Blur`, `Motion Blur`, `Radial Blur`, `Smart Blur`, `Blur`, `Black And White`, `stenciler1`, `stenciler3`, `stenciler4`, `stenciler6`, `stenciler7`, `DTN1`, `DTN2`, `DTN3`, `DTN4`, `DTN5`.
- `export` (object, optional) — ExportParameters (see `video-adjust`).

**Output:** `202 { transaction_id, status }`.

**Async?** Yes — `video-getresult`.

**Tips:**
- Capitalised effects (`Focal Zoom`, `Lens Blur`, etc.) must be passed verbatim with spaces.
- Only one effect per call — chain calls or use `video-edit` to combine with crop/fit.

---

## Edit

### `video-edit`
`POST /edit` — Comprehensive editing in one operation: fit + crop combined with full ExtendedExportParameters (codec, audio codec, quality, bitrate, color space).

**Inputs:**
- `video_url` (string, uri, required) — Source video URL.
- `fit` (object, optional) — FitParameters: `ratio`, `width`, `height`, `bg_color`, `bg_blur`, `bg_image_url`, `bg_video_url` (see `video-fit`).
- `crop` (object, optional) — CropParameters: `width`, `height`, `start_x`, `start_y` (see `video-crop`).
- `export` (object, optional) — ExtendedExportParameters:
  - `format` (enum: MOV, MP4, WEBM, GIF, default MP4)
  - `max_size_mb` (integer, nullable) — soft target size cap
  - `quality` (enum: low, medium, high, default medium)
  - `codec` (enum: default, HEVC, h264, theora, vp8, vp9, gif, av1, cinepak, ffv1, MPEG4, vc2; default `default`)
  - `audio_codec` (enum: default, aac, ac3, opus, mp3, ogg_vorbis, ogg_speex, wav, flac, PCM; default `default`)
  - `frame_rate` (integer 1–60, default 30)
  - `bitrate` (integer 1–10000 kb/s)
  - `color_space` (enum: SRGB, DisplayP3; default SRGB)

**Output:** `202 { transaction_id, status }`.

**Async?** Yes — `video-getresult`.

**Tips:**
- Use `video-edit` when you need codec/quality/bitrate control or to combine fit+crop in one call. Use the dedicated `video-trim`/`video-crop`/`video-fit` for simpler single-purpose calls.
- `codec: default` and `audio_codec: default` preserve the source encoding.

### `video-trim`
`POST /trim` — Trim a video to a specific segment.

**Inputs:**
- `video_url` (string, uri, required) — Source video URL.
- `start` (integer, ms, required, default 0, min 0) — Trim begin time.
- `end` (integer, ms, required, default 1000, min 1000) — Trim end time, must be greater than `start`.
- `export` (object, optional) — ExportParameters.

**Output:** `202 { transaction_id, status }`.

**Async?** Yes — `video-getresult`.

**Tips:**
- Times are in milliseconds, not seconds.
- For multi-segment merge use `video-concat-highlights` instead.

### `video-crop`
`POST /crop` — Pixel-coordinate crop.

**Inputs:**
- `video_url` (string, uri, required) — Source video URL.
- `width` (integer, min 16) — Output width in px; if larger than source, blurry-mirror fills the extra. Default = source width.
- `height` (integer, min 16) — Output height in px; same blurry-mirror fill behaviour. Default = source height.
- `start_x` (integer, default 0, min 0) — Left-edge offset in px.
- `start_y` (integer, default 0, min 0) — Bottom-edge offset in px (measured from bottom).
- `export` (object, optional) — ExportParameters.

**Output:** `202 { transaction_id, status }`.

**Async?** Yes — `video-getresult`.

**Tips:**
- `start_y` is from the **bottom**, not the top.
- To enforce an aspect ratio with letterboxing instead of cutting pixels, use `video-fit`.

### `video-concat`
`POST /concat` — Concatenate multiple videos and/or images into one timeline with optional transitions and background audio (slideshows, intro/outro).

**Inputs:**
- `items` (array, 1–10, required) — Each item merges ConcatVideoParameters + ConcatImageParameters + Transition:
  - `video_url` (string, uri, nullable) — Use either `video_url` or `image_url` per item.
  - `volume` (integer, 0–100, default 100, nullable) — Per-clip video volume.
  - `image_url` (string, uri, nullable) — Image source for slideshow frame.
  - `scale` (enum: `fit`, `fill`, default `fit`, nullable) — Image scaling: `fit` fits longer side; `fill` fills shorter side.
  - `duration` (integer, ms, min 1, default 1000, nullable) — Image display duration. Image only.
  - `transition` (enum: `none`, `fade`, `zoom_in`, `zoom_out`, `spin`, `fly_in_from_left`, `fly_in_from_right`, `fly_in_from_top`, `fly_in_from_bottom`, `fly_out_to_left`, `fly_out_to_right`, `fly_out_to_bottom`, `fly_out_to_top`; default `none`) — Transition into this clip.
- `bg_audio_url` (string, uri, optional) — Background audio/sound URL.
- `bg_audio_repeat` (boolean, default true, nullable) — Loop background audio over total duration.
- `bg_audio_volume` (integer, 0–100, default 100, nullable) — Background audio volume.
- `export` (object, optional) — ExportParameters.

**Output:** `202 { transaction_id, status }`.

**Async?** Yes — `video-getresult`.

**Tips:**
- Mix images and videos in one `items` array — image items need a `duration`.
- Max 10 items per call.

### `video-concat-highlights`
`POST /concat/highlights` — Build a highlights reel by trimming and concatenating multiple segments of one source video.

**Inputs:**
- `video_url` (string, uri, required) — Source video URL.
- `trim_segments` (array of 2–10 objects, required) — Each segment:
  - `start` (integer, ms, required, min 0, default 0)
  - `end` (integer, ms, required, min 1)
  - `transition` (enum from the Transition list above; default `none`)
- `export` (object, optional) — ExportParameters.

**Output:** `202 { transaction_id, status }`.

**Async?** Yes — `video-getresult`.

**Tips:**
- Minimum 2 segments; for a single cut use `video-trim`.
- All segments come from the same source `video_url`; for multi-source mash-ups use `video-concat`.

### `video-fit`
`POST /fit` — Fit a video into target dimensions or aspect ratio, padding with color/blur/image/video background.

**Inputs:**
- `video_url` (string, uri, required) — Source video URL.
- `ratio` (number float, 0.1–10.0, nullable) — width/height. Defaults to original ratio.
- `width` (integer, min 16, nullable) — Output width px. Larger than source = blurry-mirror fill.
- `height` (integer, min 16, nullable) — Output height px. Larger than source = blurry-mirror fill.
- `bg_color` (string, nullable) — Hex (3/4/6/8 digit) or color name. If set, other `bg_*` must be empty.
- `bg_blur` (integer, 0–100, default 0) — Background blur amount.
- `bg_image_url` (string, uri, optional) — Background image URL.
- `bg_video_url` (string, uri, optional) — Background video URL.

**Output:** `202 { transaction_id, status }`.

**Async?** Yes — `video-getresult`.

**Tips:**
- Use `video-fit` when cropping would lose content; the background fills the padding.
- Only one `bg_*` source at a time.
- No `export` block on `video-fit` — output keeps source defaults.

---

## Metadata

### `video-metadata`
`POST /metadata` — Analyse video and return metadata (codec, dimensions, bitrate, durations, audio info, thumbnail info).

**Inputs:**
- `video_url` (string, uri, required) — Source video URL.

**Output (sync `200`):** `{ status, data: { video_streams, audio_streams, bit_rate, size, duration, format_name, video_codec_name, video_width, video_height, video_duration, video_bit_rate, video_pix_fmt, video_fps, audio_codec_name, audio_sample_rate, audio_channels, audio_channel_layout, audio_duration, audio_bit_rate, thumbnail_codec_name, thumbnail_width, thumbnail_height, thumbnail_pix_fmt } }`.

**Async?** No — direct response.

**Tips:**
- Cheap pre-flight to validate input before paying credits on a transform.

### `video-get-thumbnail`
`POST /metadata/thumbnail/extract` — Extract up to 4 frames from the video as thumbnails.

**Inputs:**
- `video_url` (string, uri, required) — Source video URL.
- `source` (enum: `auto`, `container`, `timestamp`; default `auto`) — Where to take the thumbnail from. `container` reads the embedded thumbnail; `timestamp` extracts from `timestamps`; `auto` picks.
- `timestamps` (array of 1–4 strings, nullable) — Timestamps to extract frames at. Multiple formats supported (see Picsart timestamp docs).

**Output (sync `200`):** `{ status, data: [{ id, url }, ...] }` (0–4 items).

**Async?** No — direct response.

**Tips:**
- For embedded thumbnail only: `source: container`, omit `timestamps`.
- For arbitrary frames: `source: timestamp` plus 1–4 entries in `timestamps`.

### `video-set-thumbnail`
`POST /metadata/thumbnail` — Replace the embedded thumbnail of the video with a supplied image.

**Inputs:**
- `video_url` (string, uri, required) — Source video URL.
- `image` (binary, optional) — Source image file (mutually exclusive with `image_url`).
- `image_url` (string, uri, optional) — Source image URL (mutually exclusive with `image`).

**Output:** `202 { transaction_id, status }`.

**Async?** Yes — **must** poll via `video-set-thumbnail-getresult`, **not** `video-getresult`.

### `video-set-thumbnail-getresult`
`GET /metadata/thumbnail/{transaction_id}` — Retrieve the video with the updated thumbnail.

**Inputs:**
- `transaction_id` (string, path, required) — From `video-set-thumbnail`.

**Output:** `200 { data: { id, url }, status: success }` when done; `202` while still processing.

---

## Ads

### `video-encode-ctv`
`POST /encode/ctv` — Re-encode video to meet CTV (Connected TV) ad format requirements.

**Inputs:**
- `video_url` (string, uri, required) — Source video URL.

**Output:** `202 { transaction_id, status }`.

**Async?** Yes — `video-getresult`.

**Tips:**
- See Picsart CTV format docs for the underlying constraints; this is a one-shot conformance encode.

---

## Audio

### `video-adjust-audio`
`POST /audio/adjust` — Adjust audio volume of source video and/or layer in a new audio track.

**Inputs:**
- `video_url` (string, uri, required) — Source video URL.
- `audio_url` (string, optional, nullable) — Audio track URL to overlay.
- `audio_volume` (integer, 0–100, default 100) — Overlay audio volume.
- `video_volume` (integer, 0–100, default 100) — Source video's own audio volume.
- `export` (object, optional) — ExportParameters.

**Output:** `202 { transaction_id, status }`.

**Async?** Yes — `video-getresult`.

**Tips:**
- Set `video_volume: 0` to fully mute the source while keeping the overlay.

### `video-extract-audio`
`POST /export/audio` — Extract the audio channel from a video as a standalone audio file.

**Inputs:**
- `video_url` (string, uri, required) — Source video URL.
- `format` (enum: `mp3`, `m4a`, `wav`, `flac`; default `mp3`) — Output audio format.

**Output:** `202 { transaction_id, status }`.

**Async?** Yes — poll via `video-getaudioresult` (not `video-getresult`).

---

## Transcriptions

### `video-transcribe-audio`
`POST /audio/transcribe` — Speech-to-text for audio or video files (≤25 MB).

**Inputs:**
- `file_url` (string, uri, required) — Source audio or video URL. Max 25 MB.
- `language` (enum, default `en`) — ISO 639-1 code. Supported: `af, ar, am, az, be, bs, bg, ca, zh, hr, cs, da, nl, en, et, fi, fr, gl, de, el, he, hi, hu, is, id, it, ja, kn, kk, ko, lv, lt, mk, ms, mr, mi, ne, no, fa, pl, pt, ro, ru, sr, sk, sl, es, sw, sv, tl, ta, th, tr, uk, ur, vi, cy`.
- `format` (enum: `TXT`, `SRT`, `VTT`, `SBV`; default `TXT`) — Transcription output format.
- `granularity` (enum: `1-word`, `2-words`, `sentence`; default `sentence`) — Subtitle granularity. Applies to SRT/VTT/SBV only.

**Output:** `202 { transaction_id, status }`.

**Async?** Yes — poll via `video-transcribe-audio-getresult`.

**Tips:**
- Supported MIME types: `audio/flac`, `audio/mpeg`, `audio/x-m4a`, `audio/ogg`, `audio/x-wav`, `video/mp4`, `video/mpeg`, `video/webm`.
- For plain text transcripts use `TXT`; for time-coded captions use `SRT`/`VTT`/`SBV` with appropriate `granularity`.

### `video-transcribe-audio-getresult`
`GET /audio/transcribe/{transaction_id}` — Retrieve the transcription result.

**Inputs:**
- `transaction_id` (string, path, required) — From `video-transcribe-audio`.

**Output:** `200 { data: { id, url }, status: success }` when done; `202` while processing. `url` points to the transcript file.

---

## Watermark

### `video-add-watermark`
`POST /watermark` — Overlay an image watermark on the video.

**Inputs:**
- `video_url` (string, uri, required) — Source video URL.
- `watermark` (binary, nullable) — Watermark image file (mutually exclusive with `watermark_url`).
- `watermark_url` (string, uri, nullable) — Watermark image URL (mutually exclusive with `watermark`).
- `anchor_point` (enum, default `center-middle`) — Placement: `left-top`, `left-middle`, `left-bottom`, `center-top`, `center-middle`, `center-bottom`, `right-top`, `right-middle`, `right-bottom`, `pattern`.
- `watermark_width` (integer, min 1, nullable) — Override width in px.
- `watermark_height` (integer, min 1, nullable) — Override height in px.
- `watermark_opacity` (integer, 0–100, default 50, nullable) — Opacity (0 transparent, 100 opaque). Schema description claims default 100 but the property default is 50.
- `watermark_angle` (integer, 0–360, nullable) — Rotation angle in degrees.
- `watermark_padding_x` (integer, min 0, default 0, nullable) — Horizontal padding from anchor.
- `watermark_padding_y` (integer, min 0, default 0, nullable) — Vertical padding from anchor.

**Output:** `202 { transaction_id, status }`.

**Async?** Yes — `video-getresult`.

**Tips:**
- `anchor_point: pattern` tiles the watermark across the frame.

---

## Utilities (polling, upload, balance)

### `video-getresult`
`GET /video/{transaction_id}` — Generic result poller for video editing transactions: effects, adjust, trim, crop, resize, fit, concat, highlights, watermark, remove-background, encode-ctv, video-edit, adjust-audio.

**Inputs:**
- `transaction_id` (string, path, required).

**Output:** `200 { data: { id, url }, status: success }` when ready; `202 { status: processing|queued }` otherwise.

### `video-getaudioresult`
`GET /audio/{transaction_id}` — Result poller for audio output transactions (`video-extract-audio`).

**Inputs:**
- `transaction_id` (string, path, required).

**Output:** Same shape as `video-getresult` — `url` points to the audio file.

### `video-upload`
`POST /upload` — Upload a local resource (video, audio, or image) and receive a hosted URL usable as input to other tools.

**Inputs:**
- `file` (binary, required) — Source file (multipart/form-data).

**Output (sync `200`):** `{ status, data: { id, url } }`.

**Async?** No — direct response.

**Tips:**
- Use this when the caller has a local file but the API only accepts URLs.

### `video-credits-balance`
`GET /balance` — Check remaining credits on the account.

**Inputs:** none.

**Output (sync `200`):** `{ credits: integer }`.

**Async?** No — direct response.

---

## Async workflow

Most video/audio transforms are asynchronous. The pattern is:

1. Call the submit tool (e.g. `video-trim`). Response: `202 { transaction_id, status: "processing" | "queued" }`.
2. Poll the matching getresult tool with that `transaction_id`.
3. While still working you receive `202 { status: "processing" | "queued" }`.
4. When done you receive `200 { data: { id, url }, status: "success" }`. The `url` is the result asset.
5. On failure, `status: "error"` is returned.

**Submit -> getresult routing:**

| Submit tool | Getresult tool |
|---|---|
| `video-upscale-fps` | `video-upscale-fps-getresult` |
| `video-set-thumbnail` | `video-set-thumbnail-getresult` |
| `video-transcribe-audio` | `video-transcribe-audio-getresult` |
| `video-extract-audio` | `video-getaudioresult` |
| `video-remove-background` | `video-getresult` |
| `video-adjust` | `video-getresult` |
| `video-apply-effect` | `video-getresult` |
| `video-edit` | `video-getresult` |
| `video-trim` | `video-getresult` |
| `video-crop` | `video-getresult` |
| `video-concat` | `video-getresult` |
| `video-concat-highlights` | `video-getresult` |
| `video-fit` | `video-getresult` |
| `video-encode-ctv` | `video-getresult` |
| `video-adjust-audio` | `video-getresult` |
| `video-add-watermark` | `video-getresult` |

Synchronous tools (no polling): `video-metadata`, `video-get-thumbnail`, `video-upload`, `video-credits-balance`.

---

## Audio vs video tools

**Affects audio tracks (no visual change to the video frames):**
- `video-adjust-audio` — change volumes, swap/add audio track.
- `video-extract-audio` — pull audio out into mp3/m4a/wav/flac.
- `video-transcribe-audio` — speech to text (TXT/SRT/VTT/SBV).

**Affects visual frames only:**
- `video-upscale-fps` — frame interpolation.
- `video-apply-effect`, `video-remove-background`, `video-fit`, `video-crop`, `video-trim`, `video-concat`, `video-concat-highlights`, `video-edit`, `video-encode-ctv`, `video-add-watermark`, `video-set-thumbnail`.

**Affects both (touches audio and video):**
- `video-adjust` — exposes `audio_url`, `audio_volume`, `video_volume` alongside the color/sharpen/noise dials.
- `video-concat` — clips carry their own `volume`, and `bg_audio_*` adds a soundtrack.
- `video-edit` (via ExtendedExportParameters `audio_codec`) — re-encodes both streams.
- `video-trim` — trims both audio and video in sync.

**Metadata-only:**
- `video-metadata`, `video-get-thumbnail` — read-only; no transformation.
