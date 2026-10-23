# Figma design → layered motion — the exact flow

The reproducible golden path from a static Figma design to a rendered, correctly-positioned
layered motion video. Follow it **in order**. It is the flow that produces correct results; most
"wrong position / looks off" outcomes come from skipping a step (usually §3 or §4) and **eyeballing**
instead of reading exact values.

> **Scope: this is the FIGMA path.** When the material is the user's **own uploaded assets** (photos,
> logos, screenshots, clips — arranged as a grid/stack/collage/montage), the compose step is
> [`ASSET-COMPOSITION.md`](./ASSET-COMPOSITION.md) instead — there is no Figma layer tree to read.
> The **hosting/CSP (§5), font, and coordinate rules here still apply** wherever an uploaded asset is
> placed; that file cross-references them rather than repeating them. Everything after compose (motion,
> validation, preview) is shared by both paths.

> **Iron rule for this flow:** every coordinate, size, and asset is **read from a tool**, never
> guessed from a screenshot. If you cannot obtain an exact value, **stop and say so** — a guessed
> position is a wrong ad (see [`TOOL-ROUTING.md`](./TOOL-ROUTING.md)).
>
> **And never downgrade the motion to dodge a value you couldn't get.** If you can't position a
> matched element exactly, do **not** quietly swap its smart-animate for a crossfade/fade and
> mention it in passing — that hides the failure behind weaker motion. Surface it and stop, exactly
> as you would a missing font: *"I can't get the exact glyph position for X, here's why"* — never a
> lesser motion presented as the plan. A fallback fade you reached for because positioning felt
> unobtainable is almost always a **tooling gap to close** (§2/§4, `use_figma`), not a design choice.

> **Read the `figma-storyboard-animation` skill first.** It is the canonical, fuller version of this
> exact flow (plus `motion-intent` / `motion-pattern-library` / `custom-transitions` for craft). This file
> is the short path, and it carries the coordinate rules (§4) either way.

## 0 · Orient (once)
`picsart_scene_capabilities` schema sections (the shapes you author against — **narrow it**:
`["schemaSummary"]` or `["schema:<Definition>"]`; the full `schema` is ~200KB+ and overflows context,
so if a call ever does, lean on the catalog sections + references, don't re-call it blind) · `picsart_scene_fonts` (fonts, if any text is live — with
its `query` live-searching a font not in the bundled snapshot) · `picsart_scene_capabilities` (real easings/presets/limits; pass
`sections` by their exact names, e.g. `["easing", "motionPresets", "limits"]` — the list is in
`TOOL-ROUTING.md`; never `["all"]`).

## 1 · Frame list & running order
`get_metadata` on the **page/canvas** node → the top-level frames. **Running order = left→right by
`x`.** Record `id` + order. (If the page dump is large, that's fine — you only need the frame list here.)
- **If the page holds SEVERAL distinct sequences/storyboards, don't assume which one to animate.**
  A page routinely carries multiple reels side by side. **List the sequences you found and ask the
  designer which to animate first** before composing anything — group the frames into their sequences
  (by spacing/section/naming) and confirm the pick. Silently animating the first cluster is a common
  wrong turn.

## 2 · Per-frame layer tree — get EXACT coordinates
Call `get_metadata` **per frame node** (not the whole page — smaller output you can actually read).
For every animatable node capture: `id`, name/role, **`x`, `y`, `w`, `h`**, and z-order.
- **GO DEEP ENOUGH — expand every nested layer; never work from Figma's simplified, frame-level
  output.** A shallow/frame-level read collapses nested children (groups, component instances,
  auto-layout children, masked contents) into a summary; take it at face value and those elements are
  **silently dropped** and the frame composes short. Recursively expand the frame's **full** tree
  (children expanded, or `use_figma` to walk all descendants) and audit it node by node — if a group/
  instance shows as one node, open it. Your captured count must match the *fully-expanded* leaf/node
  count, not the top-level handful. (Read gate in `design-layer-import`; output gate = Stage 2's "layer count
  ≈ node count".)
- **If the output is too large to read in full, extract the exact values** (e.g. filter to the
  node ids you need). Do **not** work from a truncated view or the screenshot — positions must be exact.
- **If the metadata shows no text but the reference visibly has text, STOP and verify the node/frame
  — do not author from the screenshots.** `get_metadata` can land on the wrong node (a rectangle, a
  collapsed instance) or not expand the frame's nested tree, so it returns no text for a frame that
  clearly contains it. Re-inspect: `get_metadata` on the correct **frame** node, `use_figma` to walk
  the full nested tree. Reconstructing from the visible exported assets and omitting the text is the
  failure this prevents — missing text in the read means *read again*, never *guess*.
- **Text nodes: the `x/y/w/h` box is the text *frame*, not the glyphs.** A text node's `get_metadata`
  box is its layout container, routinely much larger than the visible ink and centred differently —
  e.g. a node box `714×400` centred at `(540,960)` whose actual ink is `334×280` centred at
  `(531.6,968)`. Position a text layer by the box and it lands wrong, silently. Read the **ink
  bounds** (`absoluteRenderBounds`) via `use_figma` (read-only — see [`TOOL-ROUTING.md`](./TOOL-ROUTING.md))
  and carry *those* into §4, not the node box.

## 3 · Diff each adjacent pair (A→B) — and detect multi-frame runs that are ONE motion
Match nodes across the pair by **name + hierarchy** (never id — ids differ across frames). Classify
each: `unchanged` / `moved` / `resized` / `entered` (B only) / `exited` (A only) / `content-changed`.
Compute Δ = B − A. **Animate only what changed; leave `unchanged` still.** (Full method: `MOTION-PRINCIPLES.md` §1.)

- **First scan the whole sequence for runs that are one continuous motion, not a chain of cuts.**
  From the diff facts (not by eye), test each stretch: **B = A translated** on one axis, same content
  → a **scroll**; **B = A scaled/cropped** → a **zoom/pan**; **B = A + emphasis** → highlight-in-place.
  When frame k, k+1, k+2… fit one of these, they are **keyframes of a single beat over one unit of
  content** — group the run and animate it as one continuous move (one scroll gesture, don't stop on
  each waypoint), then resume pairing after it. **How many frames belong to the run, and whether it's
  truly one motion vs. separate screens, is a per-case judgment** — decide from the tool-read deltas,
  confirm on the played result. Authoring detail: [`TRANSITIONS.md`](./TRANSITIONS.md).

- **Text that grows across frames is one assembling sentence, not a swap — and both the name+hierarchy
  rule and `diff_layouts` will mislabel it.** When A's text is a **prefix/superset** of B's (`AI` →
  `AI Effects` → `AI Effects made easy.`), the nodes have *different names/strings*, so name-match
  says "no match" and `diff_layouts` (which pairs on same text/content) reports `exited`+`entered` —
  i.e. "cut." **Override that:** the shared words **persist** (matched → they re-position/reflow A→B),
  and only the **new** words are `entered`. This only works if the persisting substring is its **own
  layer** — split it at import (see `design-layer-import`); recipe in [`MOTION-PATTERNS.md`](./MOTION-PATTERNS.md)
  *"Progressive text build."*

## 4 · Coordinates → composition — the two rules that make positions correct
These are the steps a cold chat usually gets wrong:
1. **Child coords are FRAME-RELATIVE.** A node's `x,y` is relative to its containing frame, not the
   canvas. Map the frame to the composition (e.g. a 1080×1920 frame → a 1080×1920 comp); the
   node's frame-relative `x,y` are its composition coords.
2. **`transform.position` is where the layer's CENTER lands — not its top-left.** So for a node at
   frame `(x,y)` size `(w,h)`: **`position = [x + w/2, y + h/2]`**, and set the media layer's
   **`bounds = [w, h]`**. Setting `position = [x,y]` offsets every layer by half its size — the
   classic "positions are not correct."
3. **For text, feed rule 2 the ink bounds, not the node box.** The `(x,y,w,h)` you plug in for a
   text layer must be its **`absoluteRenderBounds`** (the glyphs, from §2 via `use_figma`), not its
   layout box — otherwise the centre you compute is the frame's centre, not the text's, and the type
   sits off by the box's slack. This is the one case where the §2 values need the ink read first.

## 5 · Decide each layer's KIND first — then get the raster assets onto a **CSP-allowed (Picsart-hosted)** URL

> The hosting/CSP, upload-hygiene, and font rules in this section are the shared
> [`COMPOSE-FUNDAMENTALS.md`](./COMPOSE-FUNDAMENTALS.md) (stated here in Figma terms); §5 adds the
> **Figma-specific** parts — per-node kind triage and the `get_screenshot` bake gotcha.

**The scene is LAYERED, and layered means LIVE — this is mandatory, not stylistic.** Before any
screenshot, decide what each design node becomes; **rasterizing is the last resort**, never the default:

- **Text → a live `text` layer, always.** Never a PNG of text: baked text can't type-on, stagger,
  re-flow, or smart-animate as an assembling sentence; it blurs under any camera zoom; and it makes
  the copy uneditable. Font by resolved `.ttf`/`.otf` URL (§6).
- **Every Figma shape → a shape layer** — rectangles, pills, cards, dividers, icons, logos,
  booleans: create the shape layer with `picsart_scene_patch` (a non-rectangular outline
  appended with `picsart_scene_import_svg_path`), then paint it by `layerId` with
  `picsart_scene_import_figma_paint` (design-layer-import skill) — never a screenshot of a rectangle or
  an SVG image. A flat backdrop is a
  `color` layer. **A gradient is NEVER a raster
  asset** — a fade/scrim/overlay is a shape layer with `gradientFill`, authored with
  `picsart_scene_apply_gradient` (don't hand-write it). The resulting item (render-verified) looks like:
  ```json
  { "type": "gradientFill", "gradientType": "linear",
    "startPoint": [0, -233.5], "endPoint": [0, 233.5],
    "colorStops": [ { "offset": 0, "color": "#000000" }, { "offset": 1, "color": "#000000" } ],
    "alphaStops": [ { "offset": 0, "alpha": 0 }, { "offset": 1, "alpha": 1 } ] }
  ```
  under a `rect` item sized to the region. Gotchas the validator enforces: stops use **`offset`**
  (not `position`); a shape paint's color is **RGB-only** — its transparency goes in the item's own
  `opacity` (0..1), never an `#rrggbbaa` alpha byte (silently dropped).
- **Only true imagery becomes a raster asset**: photos, illustrations, complex mockups, or an effect
  the engine genuinely can't reproduce (e.g. Figma background-blur sampling what's behind the node).
  When you do bake such an effect in, **tell the designer** — it's a disclosed compromise, never a
  silent choice.
- **Bake at the LEAF level.** One asset per element that moves (or could move) independently. Never
  screenshot a group/frame that contains text or independently-animating children as one image — a
  flattened group can only fade/scale as a single slab, which is precisely the "slideshow, not ad"
  failure. Rasterizing the whole frame is the same failure at maximum size.
- **…but don't split FINER than the design's own units.** Granularity follows the layers the design
  authored — do **not** sub-divide a single vector/instance into invented sub-parts to animate them
  separately. A **brand mark / logo / app icon stays one unit** even when its parts look separable
  (splitting it reads as disassembling the logo). Sub-dividing is legitimate only when the parts are
  distinct content, the concept calls for it, and it's not the identity mark — otherwise keep it
  whole and *offer* the build. Full test in the `motion-design-craft` skill, *How finely to split*.

Only for the layers that survive that triage as rasters:
`get_screenshot(nodeId, contentsOnly:true)` per animating node gives an isolated asset — but the
`figma.com` URL it returns **is not safe to author directly.** Two render paths differ:

> **`get_screenshot` BAKES the node's own stroke and corner radius into the PNG.** There is no
> read-only way to export just an image *fill* without the node's border and rounded corners — seen
> live, a photo's **pink outline got baked into the asset**. So don't treat the screenshot as a clean
> fill. Two fixes: **(a)** strip the stroke/corner-radius in Figma before exporting the fill (if you
> can edit the file), or **(b)** export as-is *knowing* it's baked, or better, re-create the corners
> and border as **scene treatment** on a clean fill — `apply_preset("look:rounded_corners")` / a shape
> `stroke` (from `get_capabilities`), so the outline stays live and editable. If you can only get the
> baked version, **disclose it** to the designer (same rule as any baked-in effect), never ship the
> stray outline silently.

- **`export` / `contact_sheet`** (server-side) *can* fetch `figma.com` and `data:` — so they render
  and mislead you into thinking the asset is fine.
- **The interactive PREVIEW engine** runs in a browser with a **Content-Security-Policy**; its
  allowlist **excludes `figma.com`, `data:`, and `blob:`**, so the asset is **blocked → blank** in
  the editor preview (`csp: blocked connect-src … figma.com/….png`, `csp: blocked img-src … blob:`).

So: **lift every RASTER asset to a Picsart-hosted URL** via `picsart_drive_upload_ask` / `picsart_drive_upload`
(returns a `pastatic`/`gcdn` URL the preview CSP allows) and author **that** — **never a
`figma.com` URL, a `data:` URI, or a `blob:` URL.** (A `blob:` is a transient browser object URL —
it's never a valid scene asset; upload the file and use its Picsart URL.) One asset per moving
layer; a **matched** layer reuses **one** asset across the pair. Grab at ~1–2× the node's on-screen
size for crispness.

> **"Upload every asset" = external media ONLY, never every visual element.** Upload/Drive is for
> photos, videos, textures, and unavoidable raster. **Native scene shapes, vectors, and live text
> stay authored — never converted to raster merely for upload or CSP compatibility.** And **fix a
> CSP/blob failure by changing only the affected asset's URL/format — never by flattening** a card,
> component, or screen to make the error disappear. (Both are the exact mistakes that rebuild a frame
> from screenshots and make it diverge from the design.)
- **One Figma design = one Drive folder; every related asset goes there, never loose.** Before the
  first upload, `picsart_drive_create_folder` with `path: "Motion Projects/<Figma design name>"`
  (take the name from the Figma file, e.g. "Spring Sale reel"; idempotent — existing segments
  are reused). Remember the returned `folderUid` in `motion.json` and pass it on **every** `upload`
  batch (`files[]`, up to 10 per call) for this project — layer assets, re-grabs, and any artifact
  the designer asks to save. Assets dumped at the Drive root (or scattered "wherever") pollute the
  designer's Drive and are untraceable to the design they belong to.
- **A clean `contact_sheet` is NOT proof it renders in the preview** (server-side ≠ browser CSP).
  Verify in the editor preview, or just always use Picsart-hosted URLs so it's fine everywhere.

## 6 · Author the scene
One `media` layer per asset, positioned by §4 (`bounds` = node size, `fit:"contain"`):
- Keyframes on **`scale` / `opacity` / `position`**; easings **only** `ease_out` / `ease_in` /
  `ease_in_out` / `linear` (or a custom `cubic_bezier`). Overshoot = extra keyframes or `scale_pop`
  — there is **no** `back`/`bounce` easing.
- **Fonts by catalog key, resolved `.ttf`/`.otf` file URL, or an `assets[]` `{type:"font"}` entry
  carrying that URL**, never a family name. Keys and URLs both open in the scene editor; a font URL
  must use HTTPS on `picsart.com` or a `*.picsart.com` host to load there (see the animate-design skill's Stage 2 reference).
- **Occlusion:** any layer that must *cover* moving content (a sticky header over a scroll, an
  overlay) needs an **opaque `color` backing** above the content and under the header, so content
  scrolls *under* it — a semi-transparent gradient alone **leaks** (content shows through). Then
  **run `layout_lint` first when it's available** — it's a cheap automatic pass that flags box
  overlaps and wrong z-order across the whole timeline, so catch what you can there before rendering.
  Then **verify at the deepest scroll** with a `contact_sheet` frame, not just the start (the lint is
  opacity-blind, so this frame check is what catches a semi-transparent leak — additive to the lint).
- **A Figma group that moves as one is ONE group, never N copies of the same keyframes.** A card
  (backing + image + label + icon) keyframed member by member drifts apart the moment one member's
  times or values differ. Group it and keyframe **only the group**:
  - **An inline `composition` layer** (`{ "kind": "composition", "layers": [...] }`) — the default.
    It is **part of this scene** (same asset table, same bindings), unlike a `scene` asset, which is
    a separate document that inherits nothing and is for reuse, not grouping. **Omit its
    `composition` size block** so it is collapsed: no canvas and no crop, the members keep their
    positions, yet a fade, mask or blend on the group applies to it **as one** (no double-dark
    overlap where members cross mid-fade). Add the size block only when you want a canvas — it
    crops to that size. Its members' times are local to the group layer's `start`
    (`ENGINE-GOTCHAS.md`).
  - **`parentId`** = the card's backing (or an `empty`) — when the members must stay separate
    top-level layers (interleaved in `layers[]` with other content). It carries the **transform
    only**: opacity, masks, blend and time stay per layer.
- **Cuts abut on a frame boundary.** Every `start` and every end (`start + duration`) is a multiple
  of `1/fps`, and the next group's `start` is **the same number** as the previous group's end — not
  "a few hundredths later". At 30 fps, an end at `12.50` and a next start at `12.53` leave the frame
  at `12.500` with neither group on screen: a black flash. Keep one full-length opaque background
  layer at the bottom (the design's backdrop colour), so a gap you missed shows the backdrop, not
  black — and check each cut on the frames either side of it (§7).
- **A raw image fill is fitted by its Figma `scaleMode`, never by `fit:"stretch"`.** A node export
  already has the box's aspect (so `contain` is exact); a *raw* image fill does not. `FILL` →
  `fit:"cover"`, `FIT` → `fit:"contain"`, `CROP` → `fit:"cover"` + `crop`: read the paint's
  `imageTransform` `[[a, 0, tx], [0, d, ty]]` and, for an image of W×H px,
  `crop = [tx·W, ty·H, a·W, d·H]` (the asset declares its `width`/`height`). `TILE` has no scene
  equivalent — say so. Before authoring a grid, compare each asset's aspect
  (`picsart_media_probe`) with its cell: a mismatch under `stretch` is exactly a stretched cell.
- **Static treatment matches the mockup — from the catalogue, not faked.** Rounded corners, a
  gradient fill/overlay, a drop shadow, a blurred backing, a reflection: resolve each from
  `get_capabilities` (looks and effects via `apply_preset`, as `look:<id>` and `effect:<id>`) — a Figma node's own
  fill/shadow/gradient via `import_figma_paint`, any other gradient via `apply_gradient` — and apply it. **Enumerate the
  catalogue** (19 looks + 137 effects) rather than assuming the treatment isn't available; never bake
  it into the asset PNG or silently drop it. A missing treatment is a mockup mismatch at §7
  (`SCENE-VOCABULARY.md`).
- Reach for a real **motion preset** / the comp **`camera`** / text-animations before hand-keyframing
  what already exists (`SCENE-VOCABULARY.md`).

## 7 · Validate → preview → export
`validate_scene` (fix every `severity:error`) → `contact_sheet` at the key beats (**confirm
positions and motion on real frames before rendering**) → `contact_sheet` `times` at every cut:
`cut − 1/fps`, `cut`, `cut + 1/fps` (a one-frame gap falls between sparse samples) →
`picsart_scene_export` mp4 (free).
Author **one pair at a time** — **propose the motion, show it, take change requests, advance on approval** (don't ask up front; lead with a proposal).

---

## Why results differ across environments
Correct positions depend on **§2 (exact coords)** and **§4 (frame-relative + center)**. A surface
without a way to slice a large `get_metadata` dump (e.g. no shell) tends to eyeball the screenshot →
wrong positions. Mitigation baked into this flow: **pull metadata per-frame (§2), not the whole
page**, so the output stays small enough to read directly. The durable fix is to move §2–§4 into a
tool that returns ready-to-use composition geometry — until then, this flow is the manual golden path.
