# Picsart Image API — MCP Tool Reference

Picsart's Programmable Image APIs cover background removal, enhancement/upscaling, effects, masks, content generation, basic editing, and classification. Base URL: `https://api.picsart.io/tools/1.0`. All tools below are already exposed via the `picsart` MCP server — the MCP tool name equals the operation's `operationId` verbatim (dashes preserved).

Every image input accepts either an uploaded file (`image`) **or** a URL (`image_url`) — supply exactly one. Most write tools also accept `format` (`JPG` default, `PNG`, `WEBP`). Auth is handled by the MCP server.

## Tool index

| MCP tool name | Purpose | Key inputs |
| --- | --- | --- |
| `image-remove-background` | Remove or replace background | `image`/`image_url`, `output_type`, `bg_*`, `shadow`, `stroke_*` |
| `image-upscale` | Standard 2x–8x upscale | `image`/`image_url`, `upscale_factor` |
| `image-ultra-upscale` | Heavy upscale w/ noise suppression (async) | `image`/`image_url`, `upscale_factor` (2–16), `image_type` |
| `image-ultra-upscale-getresult` | Poll Ultra Upscale async result | `transaction_id` |
| `image-ultra-enhance` | Generative enhance/denoise (2–16x) | `image`/`image_url`, `upscale_factor` |
| `image-face-enhance` | Restore faces and selfies | `image`/`image_url`, `format` |
| `image-list-effect-names` | List photo effect names | — |
| `image-apply-effect` | Apply one of 60+ photo effects | `image`/`image_url`, `effect_name`, `fade` |
| `image-create-effect-previews` | Thumbnail previews for up to 10 effects | `image`/`image_url`, `effect_names[]`, `preview_size` |
| `image-apply-laser-engraving-effect` | Laser engraving look | `image`/`image_url`, `engrave_color`, `background_color` |
| `image-list-ai-effect-names` | List AI effect names | — |
| `image-apply-ai-effect` | Apply one of 40+ generative AI effects | `image`/`image_url`, `effect_name` |
| `image-adjust` | Brightness/contrast/etc. adjustments | `image`/`image_url`, 11 adjustment ints |
| `image-selective-blur` | Blur a segment (e.g. face, background) | `image`/`image_url`, `segment`, `blur` |
| `image-transfer-color` | Transfer color palette from reference | `image`, `reference_image`/`reference_image_url` |
| `image-transfer-style` | Transfer artistic style from reference | `image`, `reference_image`/`reference_image_url`, `level` |
| `image-create-mask-previews` | Thumbnails for mask styles | `image`/`image_url`, `mask[]` |
| `image-apply-mask` | Apply decorative mask (lace, prism, etc.) | `image`/`image_url`, `mask`, `blend`, `opacity` |
| `image-generate-texture` | (deprecated) → use `image-generate-pattern` | same as pattern |
| `image-generate-pattern` | Tile image into background pattern | `image`/`image_url`, `pattern`, `width`, `height` |
| `image-vectorize-raster-to-svg` | Raster → SVG vectorizer | `image`/`image_url`, `downscale_to` |
| `image-design-import` | Import AI/SVG → Replay project (async) | `file`/`file_url` |
| `image-design-import-getresult` | Poll Design Import async result | `transaction_id` |
| `image-surfacemap` | Print sticker onto target via mask | `image`/`image_url`, `mask`/`mask_url`, `sticker`/`sticker_url` |
| `image-add-watermark` | Overlay watermark image | `image`/`image_url`, `watermark`/`watermark_url`, position params |
| `image-upload` | Upload image once, reuse `id` | `image`/`image_url` |
| `image-credits-balance` | Get remaining credits | — |
| `image-edit` | Resize/crop/flip/rotate/perspective | `image`/`image_url`, `mode`, `width`, `height`, `crop_*`, `rotate` |
| `image-smart-crop` | AI-based crop around a segment | `image`/`image_url`, `segment`, `ratio` |
| `image-blend` | Composite/overlay two images with blend mode | `image`/`image_url`, `overlay_image`/`overlay_image_url`, `blend_mode` |
| `image-zoom` | Zoom image 1–75x scale | `image`/`image_url`, `scale_factor`, `anchor_point` |
| `image-segmentation` | Multi-matting per class (hair, sky, etc.) | `image`/`image_url`, `segmentation_class` |
| `image-tagging` | Suggest hashtags from image | `image`/`image_url` |
| `image-describer` | Generate text caption from image | `image`/`image_url` |
| `image-cars-classifier` | Classify car shot angle/part | `image`/`image_url`, `model` |
| `image-extract-colors` | Up to 5 dominant colors | `image`/`image_url` |

---

## Remove Background

### image-remove-background
`POST /removebg` — Remove or replace the background of an image with AI cutout. Supports custom backgrounds (image, URL, or solid color), borders, shadows, and resizing.

**Inputs:**
- `image` (file) **or** `image_url` (string) — source image (one required).
- `output_type` (enum, default `cutout`) — `mask` (alpha mask) or `cutout` (subject as sticker).
- `bg_image` / `bg_image_url` (file/string) — new background. Only used when `output_type=cutout`.
- `bg_color` (string) — hex (`#fff`, `#82d5fa`, 4/8-digit for alpha) or color name. Mutually exclusive with other `bg_*`.
- `bg_blur` (int 0–100, default 0).
- `bg_width`, `bg_height` (int, px) — defaults to original background dims.
- `scale` (enum, default `fit`) — `fit` or `fill`.
- `auto_center` (bool, default false) — center the cutout (skip if subject is partially cropped).
- `stroke_size` (int 0–100, default 0), `stroke_color` (string, default `FFFFFF`), `stroke_opacity` (int 0–100, default 100).
- `shadow` (enum, default `disabled`) — `disabled`, `custom`, `bottom-right`, `bottom`, `bottom-left`, `left`, `right`, `top-left`, `top`, `top-right`.
- `shadow_opacity` (int 0–100, default 20), `shadow_blur` (int 0–100, default 50).
- `shadow_offset_x`, `shadow_offset_y` (int -100..100) — required when `shadow=custom`.
- `model` (enum) — `urn:air:picsart:model:picsart:sod@10` (default) or `urn:air:picsart:model:picsart:sod@10.1`.
- `format` (enum, default `PNG`) — `JPG`, `PNG`, `WEBP`.

**Output:** JSON with `data.url` (and `data.id`) of the resulting image.

**Async?** No.

**Tips:**
- For just the alpha mask use `output_type=mask`.
- `bg_color` + transparent stroke + `shadow` = product-photo style cutout.
- PNG output preserves transparency; switch to JPG only if you set a `bg_*`.

---

## Photo enhancement

### image-upscale
`POST /upscale` — Standard upscaler that increases resolution using predictive + generative AI. Best on clean (low-noise) images.

**Inputs:**
- `image` / `image_url` (one required).
- `upscale_factor` (int, **required**, default 2) — one of `2`, `4`, `6`, `8`.
- `format` (enum, default `JPG`) — `JPG`, `PNG`, `WEBP`.

**Output:** JSON with `data.url`.

**Async?** No.

**Tips:**
- Prefer `image-ultra-upscale` for noisy or low-resolution images, especially with faces.
- Prefer `image-ultra-enhance` when you want sharper detail without smoothing.

### image-ultra-upscale
`POST /upscale/ultra` — Ultra upscale with noise suppression. Excels on small images, stickers, faces, and geometric/clear-edge content. Can be asynchronous for large factors.

**Inputs:**
- `image` / `image_url` (one required).
- `upscale_factor` (int, default 2) — any of `2..16`.
- `image_type` (enum, optional) — `product`, `portrait`, `nature`, `graphics`. Helps the service pick the best model.
- `format` (enum, default `JPG`) — `JPG`, `PNG`, `WEBP`.
- (`mode` and `product_type` are deprecated — use the HTTP `Prefer` header for sync/async if needed.)

**Output:** Either `data.url` (sync) or `transaction_id` (async, 202).

**Async?** Yes (sometimes). If you receive a `transaction_id`, poll with `image-ultra-upscale-getresult`.

**Tips:**
- Provide `image_type` when you know it — gives noticeably better results.
- Very high factors (e.g. 8–16) on big inputs almost always run async.

### image-ultra-upscale-getresult
`GET /upscale/ultra/{transaction_id}` — Poll for the finished Ultra Upscale image.

**Inputs:**
- `transaction_id` (string, **required**, path) — id from the original POST response.

**Output:** Same as the original 200 (image `data.url`) or still 202 if processing.

**Async?** This *is* the polling endpoint.

**Tips:**
- Poll every few seconds; large factors can take 10–30s.

### image-ultra-enhance
`POST /upscale/enhance` — Generative upscaler optimized for high-frequency detail and de-noising. Output capped at 64Mpx. Pairs well with `image-face-enhance`.

**Inputs:**
- `image` / `image_url` (one required).
- `upscale_factor` (int, default 2) — any of `2..16`.
- `format` (enum, default `JPG`) — `JPG`, `PNG`, `WEBP`.

**Output:** JSON with `data.url`.

**Async?** No.

**Tips:**
- If you'll process the same image multiple times, first upload via `image-upload` and reuse the `id`.
- Use after `image-face-enhance` for the cleanest portrait pipeline.

### image-face-enhance
`POST /enhance/face` — Restores and sharpens faces in old/blurry photos, balancing realism with fidelity.

**Inputs:**
- `image` / `image_url` (one required).
- `format` (enum, default `JPG`) — `JPG`, `PNG`, `WEBP`.

**Output:** JSON with `data.url`.

**Async?** No.

**Tips:**
- Works on photos with detectable faces; non-portrait images are unchanged.
- Common pipeline: `image-face-enhance` → `image-ultra-enhance`.

---

## Effects

### image-list-effect-names
`GET /effects` — Returns the list of supported photo effect names (the values valid for `image-apply-effect`).

**Output:** JSON `data: [{ name: ... }]`.

**Async?** No.

### image-apply-effect
`POST /effects` — Apply one of ~70 photo effects.

**Inputs:**
- `image` / `image_url` (one required).
- `effect_name` (string, **required**) — one of: `1972`, `apr1`, `apr2`, `apr3`, `blur`, `gblur`, `lensblur`, `motionblur`, `smartblur`, `pixelize`, `brl1`, `brnz1`-`brnz4`, `cyber1`, `cyber2`, `dodger`, `fattal2`, `food1`, `food2`, `icy1`-`icy3`, `light1`-`light20`, `mnch1`-`mnch3`, `nature1`, `nature2`, `noise`, `ntrl1`, `ntrl2`, `popart`, `saturation`, `sft1`-`sft4`, `shadow1`, `shadow2`, `sketch1`-`sketch3`, `sketcher1`, `sketcher2`, `spc1`, `tl1`, `tl2`, `urban1`, `urban2`, `water1`, `water2`.
- `fade` (int 0–100, default 0) — 0 = full effect, 100 = disabled. Note `light*`, `shadow1`, `shadow2`, `lensblur`, `pixelize`, `saturation` do not support fade.
- `format` (enum, default `JPG`) — `JPG`, `PNG`, `WEBP`.

**Output:** JSON with `data.url`.

**Async?** No.

**Tips:**
- Call `image-list-effect-names` first if the user picks "any cool filter".
- Use `image-create-effect-previews` to A/B several effects on the same image.

### image-create-effect-previews
`POST /effects/previews` — Returns thumbnail previews for up to 10 effects applied to the same input image.

**Inputs:**
- `image` / `image_url` (one required).
- `effect_names` (array of strings, **required**, max 10) — same enum as `image-apply-effect`. Comma-separated string also accepted.
- `preview_size` (int 50–240, default 120) — preview width in px.
- `fade` (int 0–100, default 0).
- `format` (enum, default `JPG`) — `JPG`, `PNG`, `WEBP`.

**Output:** JSON `data: [{ url, effect_name, id }]`.

**Async?** No.

**Tips:**
- Cheaper way to let users compare options before committing to one.

### image-apply-laser-engraving-effect
`POST /effects/laserengraving` — Apply a laser-engraving look to stickers/logos.

**Inputs:**
- `image` / `image_url` (one required).
- `engrave_color` (string, default `black`) — hex or color name; 4/8-digit hex supported for alpha.
- `background_color` (string, default `white`) — same color rules.
- `format` (enum, default `JPG`) — `JPG`, `PNG`, `WEBP`, `SVG`.

**Output:** JSON with `data.url`.

**Async?** No.

**Tips:**
- Choose `format=SVG` if you need a vector result for laser hardware.

### image-list-ai-effect-names
`GET /effects/ai` — Returns the list of supported AI effect names.

**Output:** JSON `data: [{ name: ... }]`.

**Async?** No.

### image-apply-ai-effect
`POST /effects/ai` — Apply one of 40+ generative AI effects.

**Inputs:**
- `image` / `image_url` (one required).
- `effect_name` (string, **required**) — one of: `winterblues`, `wispy`, `geode`, `744`, `sketchy`, `dystopia`, `libtest2`, `pastel`, `moonlight`, `rainbow`, `money`, `popsketch`, `hintofyellow`, `badlands`, `letitsnow`, `flora`, `staygold`, `holidayparty`, `galaxy`, `crushedmarble`, `pow`, `shades_of_gray`, `haze`, `shamrock`, `815`, `flare`, `prettyinpink`, `rosegold`, `wonderland`, `whiteice`, `nightcore`, `pleinair34_120`, `soul`, `rosequartz`, `animation`, `feast`, `undead`, `highlight`, `neopop`, `midnight`, `colorbright`, `cartoon1`, `cartoon2`.
- `format` (enum, default `JPG`) — `JPG`, `PNG`, `WEBP`.

**Output:** JSON with `data.url`.

**Async?** No.

**Tips:**
- AI effects re-render the image (slower, more credits). Prefer `image-apply-effect` for cheap traditional filters.

### image-adjust
`POST /adjust` — Apply 11 adjustments to an image (no AI). Suitable for any photo type.

**Inputs:**
- `image` / `image_url` (one required).
- `brightness`, `contrast`, `clarity`, `saturation`, `hue`, `shadows`, `highlights`, `temperature` (int -100..100, default 0).
- `sharpen`, `noise`, `vignette` (int 0..100, default 0).
- `format` (enum, default `JPG`) — `JPG`, `PNG`, `WEBP`.

**Output:** JSON with `data.url`.

**Async?** No.

**Tips:**
- Combine multiple sliders in one call — they are applied together.

### image-selective-blur
`POST /selective-blur` — Use AI to blur only a named segment (e.g. faces, license plates).

**Inputs:**
- `image` / `image_url` (one required).
- `segment` (string 1–90 chars, **required**) — e.g. `foreground`, `background`, `faces`, `car plates`. Keep short.
- `blur` (int 1–100, default 50).
- `format` (enum, default `JPG`) — `JPG`, `PNG`, `WEBP`.

**Output:** JSON with `data.url`.

**Async?** No.

**Tips:**
- Use short, concrete segment names. Long prompts hurt accuracy.

### image-transfer-color
`POST /color-transfer` — Transfer color palette/style from a reference image to the input.

**Inputs:**
- `image` / `image_url` — target image (one required).
- `reference_image` / `reference_image_url` — reference image (one required).
- `format` (enum, default `JPG`) — `JPG`, `PNG`, `WEBP`.

**Output:** JSON with `data.url`.

**Async?** No.

**Tips:**
- Preserves structure of the target; only colors are restyled. Use `image-transfer-style` for full stylistic transfer.

### image-transfer-style
`POST /styletransfer` — Painterly style transfer from reference to content image.

**Inputs:**
- `image` / `image_url` — content image (one required).
- `reference_image` / `reference_image_url` — style reference (one required).
- `level` (enum, default `l1`) — `l1`, `l2`, `l3`, `l4`, `l5`. Higher = more of the reference style.
- `format` (enum, default `JPG`) — `JPG`, `PNG`, `WEBP`.

**Output:** JSON with `data.url`.

**Async?** No.

**Tips:**
- Start at `l2`/`l3` for natural blends; `l5` produces dramatic restylings.

### image-create-mask-previews
`POST /masks/previews` — Return thumbnails for up to 10 decorative mask styles applied to the input.

**Inputs:**
- `image` / `image_url` (one required).
- `mask` (array of strings, **required**, min 1) — any of: `lace1`, `lace2`, `lace3`, `lace4`, `shdw2`, `shdw17`, `rpl3`, `rpl5`, `prsm3`, `prsm9`, `prsm10`.
- `blend` (enum, default `screen`) — `normal`, `screen`, `overlay`, `multiply`, `darken`, `lighten`, `add`.
- `opacity` (int 0–100, default 100).
- `hue` (int -180..180, default 0).
- `mask_flip` (enum) — `left`, `right`, `mirror horizontal`, `mirror vertical`, `turnaround`.
- `preview_size` (int, default 120, max 240) — width/height in px.
- `format` (enum, default `PNG`) — `JPG`, `PNG`, `WEBP`.

**Output:** JSON `data: [{ url, mask_name, id }]`.

**Async?** No.

### image-apply-mask
`POST /masks` — Apply one decorative mask to an image.

**Inputs:**
- `image` / `image_url` (one required).
- `mask` (enum, **required**) — `lace1`, `lace2`, `lace3`, `lace4`, `shdw2`, `shdw17`, `rpl3`, `rpl5`, `prsm3`, `prsm9`, `prsm10`.
- `blend` (enum, default `screen`) — same set as previews.
- `opacity` (int 0–100, default 100).
- `hue` (int -180..180, default 0).
- `mask_flip` (enum) — same as previews.
- `format` (enum, default `PNG`) — `JPG`, `PNG`, `WEBP`.

**Output:** JSON with `data.url`.

**Async?** No.

**Tips:**
- Workflow: call `image-create-mask-previews` to pick a mask, then `image-apply-mask` for the final render.

---

## Content Generation

### image-generate-texture *(deprecated)*
`POST /background/texture` — Deprecated alias of `image-generate-pattern`. Same inputs/outputs. Migrate to `image-generate-pattern`.

### image-generate-pattern
`POST /background/pattern` — Generate a tiled background pattern from a source image (e.g. a logo or shape).

**Inputs:**
- `image` / `image_url` (one required) — base unit to tile.
- `width` (int, default 1024, max 8000), `height` (int, default 1024, max 8000).
- `offset_x`, `offset_y` (int, default 0) — pattern offset from center.
- `pattern` (enum, default `hex`) — `hex`, `mirror`, `diamond`, `hex2`, `tile`.
- `rotate` (int -180..180, default 0).
- `scale` (float 0.5..10, default 1.0).
- `format` (enum, default `JPG`) — `JPG`, `PNG`, `WEBP`.

**Output:** JSON with `data.url`.

**Async?** No.

**Tips:**
- Use small source stickers/icons (with transparency) for best tiling.

---

## Conversion

### image-vectorize-raster-to-svg
`POST /vectorizer` — Convert a raster PNG/JPG into an SVG vector image. Output can be scaled without quality loss.

**Inputs:**
- `image` / `image_url` (one required).
- `downscale_to` (int, default 2048) — downscale long side until below this. Use `-1` to disable (then input must be <4000px on each side).

**Output:** JSON with `data.url` to an SVG.

**Async?** No.

**Tips:**
- Best for logos, icons, simple illustrations; photo-realistic input will produce gigantic SVGs.

### image-design-import
`POST /design2replay` — Convert design files (AI, SVG) into Picsart's Replay project format used by the Photo and Video Editor SDK. **Async only.**

**Inputs:**
- `file` (file) **or** `file_url` (string) — source `.ai` or `.svg` (one required).

**Output:** 202 response with a `transaction_id`.

**Async?** Yes. Poll with `image-design-import-getresult`.

**Tips:**
- Use to make existing designs reusable inside the Picsart editor stack.

### image-design-import-getresult
`GET /design2replay/{transaction_id}` — Poll for Design Import status/result.

**Inputs:**
- `transaction_id` (string, **required**, path) — id from the original POST.

**Output:** 200 with result data when ready, 202 if still processing.

---

## Surfacemap

### image-surfacemap
`POST /surfacemap` — "Print" a sticker onto a target image guided by a mask. Maps the sticker pixels along the texture/curves of the target for a live-print preview.

**Inputs:**
- `image` / `image_url` — target (one required).
- `mask` / `mask_url` — mask defining the print area (one required).
- `sticker` / `sticker_url` — sticker/artwork to print (one required).
- `format` (enum, default `JPG`) — `JPG`, `PNG`, `WEBP`.

**Output:** JSON with `data.url`.

**Async?** No.

**Tips:**
- Mask is binary white-on-black indicating where the sticker should be placed.
- Pre-cut the sticker (e.g. with `image-remove-background`) for clean composites.

---

## Watermark

### image-add-watermark
`POST /watermark` — Overlay a watermark image on top of the input.

**Inputs:**
- `image` / `image_url` — base image (one required).
- `watermark` / `watermark_url` — watermark image (one required).
- `anchor_point` (enum, default `center-middle`) — `left-top`, `left-middle`, `left-bottom`, `center-top`, `center-middle`, `center-bottom`, `right-top`, `right-middle`, `right-bottom`, `pattern` (tiled).
- `watermark_width`, `watermark_height` (int, ≥1) — explicit size; optional.
- `watermark_opacity` (int 0–100, default 50).
- `watermark_angle` (int 0–360).
- `watermark_padding_x`, `watermark_padding_y` (int ≥0, default 0).
- `format` (enum, default `JPG`) — `JPG`, `PNG`, `WEBP`. (From `ExportParameters`.)

**Output:** JSON with `data.url`.

**Async?** No.

**Tips:**
- `anchor_point=pattern` tiles the watermark across the whole image.
- Use a transparent PNG as the watermark for best results.

---

## Utilities

### image-upload
`POST /upload` — Upload an image once and receive a reusable id. Use when you plan to run multiple transformations on the same image.

**Inputs:**
- `image` (file) **or** `image_url` (string) — one required. Supported formats: JPG, PNG, WEBP, TIFF, BMP, MPO, MJPEG, HEIC/HEIF.

**Output:** JSON with `data.id` and `data.url`.

**Async?** No.

**Tips:**
- For a single transformation, skip upload and call the target tool directly with `image`/`image_url`.
- `data.url` returned here can be passed as `image_url` to subsequent tools.

### image-credits-balance
`GET /balance` — Return the remaining credit balance.

**Output:** JSON `{ credits: <int> }`. The response header `X-Picsart-Credit-Available` is also populated on every API call.

**Async?** No.

---

## Editing

### image-edit
`POST /edit` — Basic non-AI editing: resize, crop, flip, rotate, perspective.

**Inputs:**
- `image` / `image_url` (one required).
- `mode` (enum) — `resize` (proportional fit to width/height) or `crop` (center-crop to width/height). Omit to apply rotate/flip/perspective without changing canvas size.
- `size` (int) — shortcut that sets both width and height.
- `width`, `height` (int) — output dims. If larger than input, original is kept.
- `crop_x`, `crop_y` (int) — anchor point of crop (center of crop area); origin is top-left.
- `crop_anchor` (enum, default `center`) — `center`, `top-left`, `top-right`, `bottom-left`, `bottom-right`. Alternative to `crop_x`/`crop_y`.
- `flip` (enum) — `horizontal`, `vertical`.
- `rotate` (float -180..180, default 0).
- `perspective_horizontal`, `perspective_vertical` (int -45..45, default 0).
- `quality` (int 10–100, default 90) — JPG/WEBP quality.
- `format` (enum, default `JPG`) — `JPG`, `PNG`, `WEBP`.

**Output:** JSON with `data.url`.

**Async?** No.

**Tips:**
- For content-aware cropping use `image-smart-crop` instead.

### image-smart-crop
`POST /smart-crop` — AI-guided crop around a chosen segment (foreground, product, etc.).

**Inputs:**
- `image` / `image_url` (one required).
- `segment` (string 1–90 chars, **required**) — e.g. `foreground`, `hat`, `boots`. Keep short and concrete.
- `ratio` (enum) — `1:1`, `4:3`, `3:2`, `16:9`, `21:9`, `4:5`, `9:16`, `2:3`, `5:4`.
- `width`, `height` (int ≥0) — output dims; if both given, must match `ratio`.
- `margin` (int 0–100, default 0) — pixel margin around segment, applied before ratio.
- `format` (enum, default `JPG`) — `JPG`, `PNG`, `WEBP`.

**Output:** JSON with `data.url`.

**Async?** No.

**Tips:**
- Provide `ratio` for social/marketplace presets; the service back-fills the other dimension.

### image-blend
`POST /blend` — Composite a base image with an overlay using a photographic blend mode. Great for watermarks, textures, multi-image layouts.

**Inputs:**
- `image` / `image_url` — base (one required).
- `overlay_image` / `overlay_image_url` — overlay (one required).
- `opacity` (int 0–100, default 100).
- `blend_mode` (enum, default `normal`) — `normal`, `darken`, `multiply`, `lighten`, `screen`, `color_dodge`, `overlay`, `soft_light`, `hard_light`, `hue`, `saturation`, `color`, `luminosity`.
- `format` (enum, default `JPG`) — `JPG`, `PNG`, `WEBP`.

**Output:** JSON with `data.url`.

**Async?** No.

**Tips:**
- For positioning/rotation of the overlay, use `image-add-watermark` instead.

### image-zoom
`POST /zoom` — Zoom into an image with scale factors of 1–75 (50 = 2x, 75 = 1.5x).

**Inputs:**
- `image` / `image_url` (one required).
- `scale_factor` (int 1–75, **required**, default 2).
- `anchor_point` (enum, default `center-middle`) — `left-top`, `left-middle`, `left-bottom`, `center-top`, `center-middle`, `center-bottom`, `right-top`, `right-middle`, `right-bottom`, `ai` (AI picks focal point).
- `format` (enum, default `JPG`) — `JPG`, `PNG`, `WEBP`.

**Output:** JSON with `data.url`.

**Async?** No.

**Tips:**
- `anchor_point=ai` is slower but auto-targets the salient subject.

---

## Classification

### image-segmentation
`POST /multi-matting` — Multi-matting segmentation that isolates a specific class.

**Inputs:**
- `image` / `image_url` (one required).
- `segmentation_class` (enum, **required**) — `hair`, `skin`, `lips`, `teeth`, `eyes`, `clothes`, `glasses`, `background`, `foreground`, `sky`.

**Output:** JSON with `data.url` (the matted/segmented image).

**Async?** No.

**Tips:**
- For a generic foreground cutout, `image-remove-background` with `output_type=mask` is often easier.

### image-tagging
`POST /tags` — Generate hashtags relevant to the image content.

**Inputs:**
- `image` / `image_url` (one required).

**Output:** JSON `data: { ... tags ... }`.

**Async?** No.

### image-describer
`POST /describe` — Generate a detailed natural-language description (image-to-text).

**Inputs:**
- `image` / `image_url` (one required).

**Output:** JSON `data.description` (string).

**Async?** No.

**Tips:**
- Good upstream of `image-apply-ai-effect` or any prompt-driven GenAI flow.

### image-cars-classifier
`POST /cars/classify` — Classify a car image into views/parts. Returns one of `front`, `rear`, `left-side`, `right-side`, `34-front-right`, `34-front-left`, `34-rear-right`, `34-rear-left`, `top`, `interior`, `engine`, `detail`. May also return `vin` and `odo` strings when detectable.

**Inputs:**
- `image` / `image_url` (one required).
- `model` (enum, default `urn:air:openai:model:openai:gpt-5.1-chat@1`) — many OpenAI / Anthropic / Google URNs supported (e.g. `urn:air:openai:model:openai:gpt-5@1`, `urn:air:anthropic:model:anthropic:claude-sonnet-4-5-latest@1`, `urn:air:google:model:google:gemini-2.5-pro@1`).

**Output:** JSON `data: { class, vin, odo }`.

**Async?** No.

**Tips:**
- Input must actually be a car image; non-car inputs produce nonsense rather than an error.

### image-extract-colors
`POST /extract-colors` — Return up to 5 prominent colors (dominant foreground + background tones).

**Inputs:**
- `image` / `image_url` (one required).

**Output:** JSON `data: [<color>, ...]` (up to 5 unique color strings).

**Async?** No.

---

## Common patterns

**Background removal vs smart background**
- `image-remove-background` is the workhorse — supports cutout, mask, custom backgrounds, shadows, strokes, color fills.
- For a custom solid-color studio look, set `output_type=cutout` + `bg_color` + `shadow`.
- If you only want a binary alpha matte for compositing, use `output_type=mask` (or `image-segmentation` with `segmentation_class=foreground`).

**Upscaling / enhancement**
- `image-upscale` — fast standard 2–8x for clean photos.
- `image-ultra-upscale` — 2–16x with noise suppression; best for small/noisy/face images; can be async (poll with `image-ultra-upscale-getresult`).
- `image-ultra-enhance` — 2–16x with generative high-frequency detail; great for de-noising.
- `image-face-enhance` — restoration specialized for faces; runs well *before* `image-ultra-enhance`.
- Pipeline for old portrait: `image-face-enhance` → `image-ultra-enhance`.

**Effects vs AI effects**
- `image-apply-effect` (`/effects`) — cheap, traditional filters (blur, light, sketches, color presets). Discover names via `image-list-effect-names`.
- `image-apply-ai-effect` (`/effects/ai`) — generative restylings (cartoon, animation, painterly). Discover names via `image-list-ai-effect-names`.
- Use `image-create-effect-previews` to A/B test multiple traditional effects in one call.

**Masks workflow**
1. `image-create-mask-previews` with several mask names to choose a look.
2. `image-apply-mask` with the chosen mask, blend mode, opacity, optional flip/hue.

**Reusing the same source image**
- Upload once with `image-upload`, take `data.url`, then pass it as `image_url` to every downstream tool. Avoids re-uploading large files for each operation.

**Async polling pattern**
- Tools ending in `-getresult` (`image-ultra-upscale-getresult`, `image-design-import-getresult`) are pollers. Use the `transaction_id` from the 202 response of the corresponding POST.

**Crop and resize**
- `image-edit` — exact, parameter-driven resize/crop/flip/rotate/perspective.
- `image-smart-crop` — AI-driven crop around a named segment with optional aspect ratio.
- `image-zoom` — scale-factor based zoom with optional AI-picked focal point.

**Color and style**
- `image-adjust` — slider-style corrections without AI.
- `image-transfer-color` — paint your image with another image's palette.
- `image-transfer-style` — paint your image in another image's full artistic style (`level` controls strength).
- `image-extract-colors` — read dominant colors out of an image (great for design tokens).

**Compositing**
- `image-blend` — two-image blend with photographic blend modes.
- `image-add-watermark` — overlay with anchor/angle/opacity/padding controls (and `anchor_point=pattern` to tile).
- `image-surfacemap` — print a sticker through a mask onto a textured target (e.g. mockups).

**Understanding an image**
- `image-describer` (text caption), `image-tagging` (hashtags), `image-extract-colors` (palette), `image-segmentation` (class masks), `image-cars-classifier` (vehicle views).
