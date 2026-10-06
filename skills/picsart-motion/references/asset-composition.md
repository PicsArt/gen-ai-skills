# Asset composition — build a scene from uploaded assets (the non-Figma compose step)

This is Stage 2 for the **asset route**: the user uploaded photos / logos / screenshots / clips and
you've agreed a concept + layout (grid, stack, collage, montage, single focus). Now turn that into a
valid MP Scene. Unlike the Figma path there is **no layer tree and no coordinates handed to you** —
you place every asset deliberately, so the composition is yours to author from the concept.

**Obey [`compose-fundamentals.md`](compose-fundamentals.md) throughout** — hosting/CSP, one Drive
folder, live text + fonts, placement, treatment-from-the-catalogue, highest-level-tool-first, and the
eye. The **tools are the same as the Figma path** — only the *ingest* differs (here: `upload` +
`probe_media`, not the Figma connector). This file adds only the asset-specific ingest and layout.

## 1. Get the assets in, and MEASURED
- **Upload → Picsart URL.** `picsart_media_upload` every file; author the returned Picsart-hosted
  URL (the ones Picsart tools return), **never** a `blob:`/`data:`/local path (CSP-blocked in preview). One Drive folder per project
  — the shared hosting/Drive rule, [`compose-fundamentals.md`](compose-fundamentals.md) §2–4.
- **An uploaded SVG logo/icon → a live shape, not a `media` layer.** Read its `<path>` `d`s and
  convert them with `picsart_media_import_svg_path` onto one shape layer (see
  [`tool-routing.md`](tool-routing.md)), so it can recolor, draw on and scale cleanly. A PNG/JPG
  logo stays a `media` asset; don't trace a raster.
- **Probe before placing.** `picsart_media_probe_media` each asset for real **dims / aspect / fps /
  duration**. You cannot size a photo into a cell or fit a clip without its true dimensions — never
  guess them from the thumbnail.
- **View each asset** (`picsart_view_image`, up to 6 per call) to know *what* it is and which way is up — see `scene-validation.md`
  (the eye works at the input end too).

## 2. Pick the composition approach — template first
- **Scene template** — `picsart_media_apply_scene_template` (montage / collage / title families;
  browse with `list_scene_templates` / `describe_scene_template`). This is the fastest path to a grid,
  collage, or montage layout — it lands a valid, arranged scene you then drop assets into.
- **Recipe** — `photo-promo` is the canonical "photos → a composed reel with transitions, blurred
  fill, and a readable title"; `ui-motion` for screenshots. Fetch it (`get_recipe`) before hand-building.
- **Hand-place with `patch_scene`** only when no template/recipe fits the chosen layout — one `media`
  layer per asset, positioned by its `transform` (see §3). Constructing a whole scene op-by-op is the
  last resort, not the default.

## 3. Layout patterns — how to place assets
Every asset is a `media` layer (`bounds` = its placed box, `fit` per below), z-order = paint order.

- **Grid** — N assets in rows×cols. Compute cell size from the canvas minus gutters:
  `cellW = (W − (cols+1)·gutter) / cols` (same for height); each asset's `position` = its cell centre;
  `fit:"cover"` to fill the cell (crops overflow — **check the crop with the eye**) or `fit:"contain"`
  + a blurred fill behind (§4) to avoid gaps.
- **Stack** — assets overlapping, each offset + a small rotation, z-order = stacking order; the top of
  the stack is the focal one. A "fan" is a stack with increasing rotation.
- **Collage** — varied sizes and positions, larger for the hero; mind overlaps (they're intentional
  here, but verify nothing important is covered).
- **Montage / sequence** — one asset full-frame at a time, as a **track of clips** with transitions
  between (this is the *only* one-asset-per-screen layout — `photo-promo` builds exactly this).
- **Single focus** — one hero asset placed large/centred, the rest supporting (small, edged, or absent).

## 4. Size to the canvas — assets rarely match the target ratio
- **`fit:"cover"`** fills the box and **crops** the overflow — the usual choice for a full-bleed photo,
  but the crop can cut off a head/product, so **verify on a rendered still**.
- **`fit:"contain"`** shows the whole asset and leaves a gap — **never leave black bars**: fill the gap
  with a **blurred, scaled copy of the same asset** behind it (the `photo-promo` / `blur_fill` trick),
  or a solid/gradient backing that matches the concept.
- Default `position` is the box centre; a portrait photo in a landscape canvas is `cover`-cropped or
  `contain` + blurred fill, never squished (never `fit:"fill"` on a photo — it distorts).

## 5. Text over assets — readable
Titles/captions are **live text, font from `picsart_media_list_fonts`** (the shared rule —
[`compose-fundamentals.md`](compose-fundamentals.md) §5). The asset-specific part: keep it
**readable over a busy photo** — a scrim/gradient backing or a drop shadow (`get_capabilities`), never
raw text on a full-bleed image.

## 6. Validate — schema, then the eye
`picsart_media_validate_scene` first (schema), then the **eye check** (`scene-validation.md`): render a
`contact_sheet` still and look — is any asset **blank** (upload/CSP failed), **cropped** badly by its
fit, **off-frame**, is the **grid aligned** (even gutters, no drift), does anything **overlap/leak**
that shouldn't. There is no design to diff against here — the ground truth is the **agreed concept**;
confirm the composition matches it before adding motion, then hand off to Stage 3 (working mode: part
by part, or the whole motion at once).

## Mistakes
- Authoring a `blob:`/`data:`/`figma.com` asset URL — CSP-blocked → blank in preview; upload first.
- Guessing an asset's dimensions instead of `probe_media` — cells and fits land wrong.
- `fit:"fill"` on a photo (distorts) or leaving **black bars** on `contain` (use a blurred fill).
- Hand-placing a grid op-by-op when a **scene template** would land it in one call.
- One-asset-per-screen by reflex — that's only the *montage* layout; grid/stack/collage put several
  assets on screen together (see the Stage-0 triage note).
- Skipping the eye-check and shipping a scene that validates but has a cropped hero or a blank tile.
