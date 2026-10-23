# Compose fundamentals — shared by both compose paths

Whatever the source — a **Figma design** ([`AUTHORING-FLOW.md`](./AUTHORING-FLOW.md)) or the user's
**uploaded assets** ([`ASSET-COMPOSITION.md`](./ASSET-COMPOSITION.md)) — once you are placing layers
into a scene, these rules hold. Each path adds only its **source-specific ingest** on top of this
common base; everything below is identical for both.

## 1. Reach for the highest-level tool first
You are an orchestrator; the Picsart media server is the engine. Before hand-building anything op-by-op,
check for a **scene template** (`apply_scene_template`), a **motion preset** / **text animation**, or a
**recipe** (`get_recipe`: its index with no name, `quick-merge-and-export` among them) that already does it. `patch_scene` is for
*edits*, not for constructing whole scenes by hand when a template fits.

## 2. Every asset → a Picsart-hosted URL (the CSP trap)
A scene asset's `uri` must be a Picsart-hosted `https://` URL (`pastatic`/`gcdn`, from
`picsart_drive_upload_ask` / `picsart_drive_upload`) — **never** a `figma.com` URL, a `data:` URI, or a `blob:`
object URL. The trap: server-side `export`/`contact_sheet` **can** fetch those, so they render and
mislead you — but the **browser preview's Content-Security-Policy blocks them → blank**. So a clean
`contact_sheet` is **not** proof it loads in the editor. Upload → author the returned Picsart URL.

## 3. Upload = EXTERNAL MEDIA ONLY
Upload/Drive is for **photos, video, textures, unavoidable raster** — real imagery. **Native scene
shapes, vectors, and live text stay authored elements** and are **never** rasterized merely for upload
or to dodge CSP. Fix a CSP/blob failure by changing only the offending asset's URL/format, never by
flattening a card/component/screen. (Rasterizing what should stay live is the slideshow trap at its source.)

## 4. One Drive folder per project
Before the first upload, `picsart_drive_create_folder` with `path: "Motion Projects/<project name>"`
(idempotent), remember the returned `folderUid`, and pass it on **every** upload for this project.
Nothing lands loose in the Drive root.

## 5. Text is live; fonts are a resolved URL
Every title/caption/label is a **live `text` layer** — never a baked PNG of text (kills type-on,
stagger, reflow; blurs under zoom). The font is a **catalog key**, the entry's resolved **`.ttf`/`.otf` file URL** from
`picsart_scene_fonts` (its `query` also live-searches the catalog), or an `assets[]` `{type:"font"}` entry
carrying that URL, **never** a family name ("Inter"). Keys and URLs both open in the scene editor;
a font URL must use HTTPS on `picsart.com` or a `*.picsart.com` host to load there. A missing font is
**surfaced to the user, never silently swapped**.

## 6. Placement basics
A layer is positioned by its `transform`; **`position` is the layer CENTER**, not a corner. Size media
with `bounds` + `fit` (`contain`/`cover`); **never `fit:"stretch"` on a photo** (it distorts), and **never
leave black bars** on `contain` — fill the gap with a blurred, scaled copy of the same asset (the
`blur_fill` / `photo-slideshow` trick) or a backing that matches the concept.

## 7. Match the design's real treatment — from the catalogue, not baked
Rounded corners, a drop shadow, a blurred backing, a gradient, a reflection: resolve each from
`get_capabilities` (looks and effects via `apply_preset`, as `look:<id>` and `effect:<id>`; a gradient via `apply_gradient`;
a Figma node's fill/shadow/gradient via `import_figma_paint`) and apply it. **Enumerate the catalogue** (looks +
effects) rather than assuming a treatment isn't supported and baking it into a PNG or dropping it.

## 8. Prove it with the eye, not just the schema
`validate_scene` proves the JSON is legal; it does **not** prove the pixels are right. A composed
result is proven by rendering a still and **looking at it** (blank/failed asset, cropped, off-frame,
clipped text, overlap, wrong colour) before you show the user — the full ladder is in
[`SCENE-VALIDATION.md`](./SCENE-VALIDATION.md).

---

**On top of this base:** `AUTHORING-FLOW.md` adds the **Figma** ingest — reading the layer tree, exact
coordinates (§3/§4), per-node kind triage, and the `get_screenshot` bake gotcha. `ASSET-COMPOSITION.md`
adds the **upload** ingest — `probe_media`, the layout patterns (grid/stack/collage/montage), and
fit-to-canvas. After compose, motion (Stage 3) and validation are shared again.
