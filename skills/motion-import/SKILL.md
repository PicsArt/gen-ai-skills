---
name: motion-import
description: Bring a design or static assets into a scene as LAYERS, not flat frames, whenever they are going to move — Figma frames for an ad or reel, or a Figma design, logo, UI screen or screenshot that animates inside a tutorial, promo or explainer. Pulls each Figma frame's layer tree (elements + transforms), captures each layer in its NATIVE format (live text, vector, or raster — PNG is a fallback, not the default), tags elements that recur across frames as matched, gets every asset onto a fetchable Picsart-hosted URL, and sets the video format (including output scale/sizes up front). Falls back to flat-frame ingest only when layers cannot be had. Stage 1 of the `motion` skill's pipeline, and used before the motion-design skill by any flow that animates a design.
metadata:
  owner: motion-designer
user-invocable: false
---

# Stage 1 — Import: the design in as layers

Motion design animates *elements*, so the import's whole job is to bring the design in as
**layers, not flat frames**. A frame delivered as one sealed PNG can only ever
cross-dissolve; a frame delivered as its layers — panels, headline, buttons, the image,
the list — is a thing whose elements can slide, scroll, type on, parallax and
smart-animate. **Everything downstream is gated on this**: if the layers are lost here,
no amount of tuning later can recover the ad; it stays a slideshow.

## Pull the layer tree, per frame

**With the Figma connector present**, read structure before pixels: `get_metadata` /
`get_design_context` to walk each frame's node tree, then export each animatable node as
its own asset. For every layer capture:

> **AUDIT EVERY NESTED LAYER — never compose from Figma's simplified, frame-level output.** The
> single biggest way items go missing from the ad: Figma's frame-level / summarized read (a shallow
> `get_design_context`, or a `get_metadata` that stops at the top level) **collapses nested children**
> — groups, component instances, auto-layout children, masked contents — into a summary. Take that at
> face value and **every nested element is silently dropped**, so the composed frame is missing pieces
> that were plainly in the design. **Recursively expand each frame's FULL tree** (`get_metadata` on the
> frame node with its children expanded, or `use_figma` to walk *all* descendants) and audit it
> **node by node** — do not trust a frame-level layer list to be complete. **Completeness check:** the
> layers you capture must match the count of leaf/animatable nodes in the *fully-expanded* tree, not
> the handful the frame-level view showed. If a group or instance shows as one node, open it — its
> children are the layers. (Downstream this is the Stage-2 "layer count ≈ node count" gate; catch it
> here, at the read, not after a frame composes short.)


- **id** and **name/role** (what it is — `chrome`, `headline`, `cta`, `image`, `list`, `fx`)
- **type** — `text`, `vector` (icon/logo/shape), or `raster` (photo/complex image); plus `group`
- **transform** — `x, y, w, h, rotation, opacity`, and **z-order** (front-to-back)
- **parent/group** — so a group can move as one: record the group (card, control, grid cell) each
  layer belongs to, and which member is its backing. Compose turns it into one group that carries
  the motion (motion-design skill, `references/AUTHORING-FLOW.md` §6); without it the members are
  keyframed one by one and drift apart
- **for an image fill, its `scaleMode`** (`FILL` / `FIT` / `CROP` / `TILE`), and for `CROP` its
  `imageTransform` — they decide the layer's `fit` and `crop`; a raw image placed without them is
  stretched to the box
- **for a text layer, also the type properties** — the **string**, resolved **font URL** + size,
  **horizontal alignment** (read Figma's `textAlignHorizontal` — `left`/`center`/`right`; *never*
  guess it from position or from "it's a big headline"), and the **box sizing/wrap**: a Figma
  **fixed-width** text box that runs past the frame **clips, it does not wrap** — record the box
  width and that it clips, or the renderer soft-wraps the line into two downstream.

### Export each layer *as what it is* — PNG is the fallback, not the default

The layer's **source type** decides the export format. Deciding this per layer is the job;
reaching for PNG on every element is the freelance-default that quietly wrecks quality —
**stop and ask "is this layer actually raster?" before you export a PNG.**

- **Text** → keep as **live text** (the string + resolved font URL), *never* an image. This is
  what makes type-on, per-line and per-character animation possible; baking text to PNG kills
  all of it and can't reflow.
- **Vector** — icons, logos, line art, panels, pills, flat shapes → a **shape layer**, no asset
  at all, built in two steps. **First create the layer**: `picsart_media_patch_scene` adds a
  layer whose `content.kind` is `"shape"`, with a `rect` (or `ellipse`) item sized to the node's
  box and the node's placement in the layer's `transform`; for a non-rectangular vector (an icon,
  a logo, a boolean), add the shape layer and append its outline with
  `picsart_media_import_svg_path` (the node's path data as `d`). **Then paint it**:
  `picsart_media_import_figma_paint` takes the `scene` and that layer's `layerId`, plus the
  node's CSS from `get_design_context` — `fill`, `boxShadow`, `gradient` (with the element
  `size`), and `gradientPaint: "stroke"` (+ `gradientStrokeWidth`) for a gradient outline. A
  solid stroke is not a paint it takes: it comes in with a path outline (`import_svg_path`'s
  `stroke` + `width`), or, on a `rect`/`ellipse` layer, as a stroke item added with
  `picsart_media_patch_scene`.
  A shape layer stays crisp at any scale and keeps every motion a shape has — radius and size
  tweens, recolour, draw-on — where an SVG image only moves as a whole. Whatever the paint tool
  lists in `skipped` (an inset shadow) is the one part to bring in another way; rasterize
  **only** a node that is not a shape.
- **Raster / photographic** — the hero image, a photo, a gradient/blur that won't survive as
  vector → **PNG with transparency** so the layer floats over what's behind it. Take the image
  fill's original bitmap from `download_assets` → `rawImages` (the largest), **never the node
  `export` or `get_screenshot`**: both draw the node over its frame's background colour, so a
  cutout photo on a dark frame comes back on an opaque black box. The raw bitmap is framed as
  uploaded, not as the layer shows it: place it by the fill's `scaleMode` (`FILL` → `fit:
  "cover"`, `FIT` → `"contain"`, `CROP` → `"cover"` plus `crop = [tx·W, ty·H, a·W, d·H]` from its `imageTransform`
  `[[a, 0, tx], [0, d, ty]]` on a W×H bitmap).

If you're about to export a PNG of an icon, logo, or shape, that's the tell you *defaulted*
instead of decided — go back and take it as vector.

**Settle output scale in the first five minutes, not the fiftieth.** Whether the ad ships at
one size or several (multiple ratios/resolutions, or any later up-scale) is what makes vector
the *normal* case, not an edge case — a PNG baked at one scale is soft or jagged at any other,
while vector is resolution-free. Decide this up front (see *Set the format* below); don't
discover the constraint at export time and re-import. And when you do capture
a vector layer, **declare it `type: "vector"`** — silently recording a shape as `type: "image"`
is the same defaulting mistake wearing a different hat.

**Format doesn't excuse hosting:** a shape layer carries no asset, but every raster you export
still has to be lifted onto a **Picsart-hosted `https://` URL** (below). A `figma.com` URL is
CSP-blocked in the preview — export → upload → author the returned Picsart URL.

### Granularity — split to what moves

Not every node, and not one blob. **A layer is anything that either moves independently or
persists across frames.** Group the rest.

- Split out: the headline, each CTA, the hero image, a scrollable list, a tap target,
  anything that will animate on its own.
- Keep grouped: static decoration, a card's fixed internals, backgrounds.
- Over-splitting (hundreds of nodes) is noise the designer must wrangle; under-splitting
  (the whole screen as one image) is the slideshow trap in disguise. When unsure, split
  by what the reference ad would animate.

### Import every element the design shows — visibility is the design's call, not yours

Import **every element the design renders**. A layer is dropped for exactly one reason: the
**design itself hides it** (Figma `visible:false` / a `hidden` node) — that is the designer's
signal, and even then a *prominent* hidden layer is worth a note, since it may be meant to appear
mid-animation. **Never drop a layer because *you* judged it "won't be seen":**

- **Partially on-frame** (clipped by the frame edge) is **on screen** — it shows in the very first
  hold, so omitting it is a visible hole against the design. This is the frame-6 tell: the search
  pill and the tag row are *clipped, not absent*, and dropping them leaves the composed frame
  missing content the mockup plainly shows.
- **Fully off-frame is not a licence to drop it either.** In motion a wide row or an off-edge
  element is usually there to **scroll or pan into view** — import it and let choreography decide,
  don't pre-empt the motion by deleting it (that is how a design's intended scroll becomes a
  static gap).

A judgment call to leave something out is **surfaced to the designer, never silent** — same rule
as a missing font. The Stage-2 `get_screenshot` compare is what catches a dropped element, as a
hole where the design has content.

## Tag matched elements across frames

The thing that makes an interface *move* between screens instead of dissolving is a
**matched element** — a layer present in consecutive frames that should animate from its
state in A to its state in B. So as you import, give any recurring layer a stable
**`matchKey`** (the same key on the header in every frame it appears in). Match by
name/role first, geometry second. `motion.json.matched[]` is built from these keys, and
Stage 2 keeps each matched element as **one continuous layer**, not a fresh copy per
frame. Miss this and the compose step can only cross-dissolve — the biggest "slideshow"
tell there is.

**A recurring element keeps its `matchKey` even when it is transformed or its content changed** —
a title that moves and shrinks, a headline whose wording grows (`AI` → `AI Effects`), a button that
recolours. Match by **semantic role** ("the title", "the CTA"), *never* by exact string or position:
`AI` and `AI Effects` are the same title. The fact that the same element is **present in both frames
but different** is the *strongest* match signal there is — it means the element should **animate from
A to B**, and it is precisely the case where matching must not fail. A same-role text or object that
is merely repositioned/resized/reworded must **never** be tagged as one element leaving and a
different one arriving; that misread is what makes it disappear-and-reappear (or get papered over
with a transition) downstream instead of moving.

**Matching is at the layer level — so an assembling sentence needs the layers split to match.**
The rule "a header in frames 1–4 is one layer with four transform states" is right for chrome, but
it breaks for text that *grows*: frames whose text reads `AI` → `AI Effects` → `AI Effects made
easy.` are usually **one whole-string text node each**, i.e. three differently-named layers — so
nothing marks `AI` as persisting; the thing that actually persists is a **substring**. Capture it
that way: split the shared words into their **own layer** carried by one `matchKey` across the
frames, and each added clause into its own layer that `enter`s. A single whole-string node per
frame gives the diff three different strings and no persisting layer, and the assembling effect
collapses to a cut. (This is the import half of `MOTION-PATTERNS.md` *"Progressive text build."*)

The A→B **delta** itself (how far a matched layer moved, what actually changed) is not judged
by eye at motion time — it is **read with `picsart_media_diff_layouts`** (which resolves both
frames through `query_layout` and returns the classified delta; `query_layout`-on-both is the
fallback when the tool is unavailable). The `matchKey` you set here is exactly what that diff
takes as its `matchHints` to pair the layers up — a dropped key becomes a missed match there.
The full frame-diff procedure is in
`references/MOTION-PRINCIPLES.md` in the motion-design skill §1.

## Get every asset onto a real URL

A Figma export and a `file://` path are both **unfetchable by the renderer**. So each
layer asset that is not already an `https://` URL must be lifted onto one: `picsart_media_upload`
(the drag-and-drop panel) or `picsart_drive`, then **read back the resulting `https://` URL and
author *that*.** Text and fills carry no asset and need no lift.

**A scene asset's `uri` must be a Picsart-hosted `https://` URL (`pastatic`/`gcdn`, from
`picsart_media_upload` / `picsart_drive`) — never a base64 `data:` URI, and never a `figma.com`
URL.** The interactive **preview engine runs in a browser with a Content-Security-Policy** whose
`connect-src` allowlist excludes both — they get **blocked → blank** in the editor preview
(`csp: blocked connect-src … figma.com/….svg`), even though the scene *validates* and the
server-side `export`/`contact_sheet` render them fine. That server/browser split is the trap: a
`figma.com` URL or a `data:` URI is only ever an **intermediate** — hand it to `upload`/`drive` and
author the **Picsart-hosted URL it returns**. **`validate_scene` and a clean `contact_sheet` do NOT
prove it renders in the preview** (both are lenient server-side paths) — the only reliable proof is
the editor preview itself, so default to Picsart-hosted URLs and it's fine everywhere.

**Drive full (`failure_space_limit_reached`) is status, not a retry.** Every file in the batch fails
the same way, so stop at the first one — don't send the rest or the next batch. Tell the designer
their Drive is full and how many assets still need a home, then:

- **Shrink the upload first.** Shapes, text and flat fills need no asset; only true rasters do.
  A batch full of icons and panels is the vector rule above being skipped.
- **Offer cleanup, never do it blind.** `picsart_drive` `list` (`flat: true`) shows what is there;
  move only the files the designer names to trash (`delete` without `permanent` — recoverable),
  after their explicit yes.
- **Never route around it** with a `blob:`, `data:` or `figma.com` URL: that is the blank preview
  (`csp: blocked img-src … blob:`), just later.

## When layers cannot be had — the honest fallback

Two cases force flat-frame ingest, and both are a **degrade, announced**:

- **No Figma connector.** Suggest it once, and offer the fallback in the same turn —
  never block, never re-ask, and you cannot connect it for them:
  > Connecting the Figma connector (Settings → Connectors → Figma) lets me pull your
  > design's layers, which is what makes real motion design possible. Without it I can
  > only animate whole flat frames — a slideshow. Share the Figma file, or paste flat
  > frame images to do the simpler version.
- **Figma export quota'd out.** Figma export is metered **per Figma seat** and can quota
  out mid-batch — that is **status, not an error**: continue on the upload path for the
  remaining assets, and if only flats are reachable, say the result will be a slideshow
  and offer to resume layered when the seat's quota returns.

A flat frame is imported as a single `image` layer filling the composition — the montage
fallback in the `motion` skill. Say plainly what is lost: *"without the layers this is a
slideshow, not motion design."*

## Order — take Figma's, never ask for it

The running order is **Figma's own** — the frame/artboard sequence in the file (or, for
pasted images, the order they were given in). **Take it as authoritative, record it, and
move on — do not ask the designer to confirm it.** A question the source already answers is
noise — the house rule: *"don't turn something the pipeline
already knows into a user choice."*

Reordering is **optional and designer-initiated**: it happens on the storyboard board
(shown for a glance and a drag, never a mandatory confirm) or when the designer explicitly
says "swap 2 and 3." Absent that, Figma order stands, silently. Never open an
ASK to confirm the running order.

## Set the format — the Motion Setup console

Open **`picsart_motion_setup` once, at the start**, prefilled so it opens on the design rather
than a blank form (it is free and read-only):

- **`frames`** — the design frames in running order (Figma's own, above), each with its `id`, a
  **Picsart-hosted** `url` (a `figma.com` export is saved with `picsart_drive`,
  `action: "upload"`, first) and its `w`/`h`.
- **`suggested.selections`** — always the **ratio** from the frames' own aspect (1080×1920 →
  9:16) and the **energy** read from the design (see below), as one of the console's own values:
  `calm`, `standard` or `energetic` (any other value is dropped); fps 30 unless the design says
  otherwise. **Never prefill a total duration** — it derives from the motion.
- **`current`** — only when reopening a setup the designer already locked.

Opening it is the whole turn; wait for the lock. Its reply, `motion_setup_feedback`, is read as
the motion-design skill's `references/WIDGET-FEEDBACK.md` says: store `selections` as the target
and the hold/seam defaults, and quote `summary` verbatim.

**When `picsart_motion_setup` is not in your list or errors**, decide the format yourself from
the material — **infer it, state it, and proceed**:

- **ratio / resolution** — from the frames' own aspect (1080×1920 → 9:16 at 1080×1920). Take what
  the design already is.
- **fps** — 30 by default.
- **energy** — read from the design (see below); pick the register the ad calls for.

Either way:

- **output scale/sizes** — the console does not carry it, so default to a single size, but
  **surface the question when it's genuinely open**: will this ship at one size or several (multiple ratios/resolutions, or a later up-scale)?
  The answer decides raster-vs-vector for every layer above, and "multiple sizes" makes vector the
  norm — cheap to settle now, expensive to discover at export. When it isn't obvious, a plain
  an ASK is the right surface; otherwise state the single-size default and move on.

Without the console, state the chosen ratio/fps/energy to the designer in one line and let them
adjust in plain conversation ("make it square", "60fps", "more energetic") — a normal message.

**`energy` is a productive↔expressive dial**, not just "fast vs slow": *productive* =
subtle, efficient motion for routine beats; *expressive* = vibrant, highly-visible motion for
significant moments (an opening, a primary CTA, a hero reveal). It scales the motion's duration
and easing register downstream — see
`references/MOTION-PRINCIPLES.md` in the motion-design skill §6.

Two things are never asked: **order** (taken from Figma silently, above) and **total duration**
(derived from the motion by default; a soft target is the designer's own pick on the console, and
a designer who wants it tighter says "punchier").

## Output → `motion.json`

Write frames-of-layers and the target (schema in the `motion` skill). Each frame carries
a `layers[]` with `id`, `role`, `type`, `transform`, `asset`/`content`, and `matchKey`
where it recurs; `matched[]` is assembled from the keys.

## Gate to pass Stage 1

Print it with ✓/✗ before compose:

- Every frame imported as **layers** (or consciously flagged flat-fallback with the
  reason recorded).
- Every animatable layer has an **asset at a real `https://` URL** (or live text/fill)
  **and a transform** with z-order.
- **Every element the design shows is imported** — nothing dropped on a self-made "won't be
  visible" call; a partially-clipped or off-frame layer is still imported. Only designer-hidden
  layers (`visible:false`) are omitted, and a prominent one is noted.
- **Matched elements tagged** with `matchKey` across the frames they appear in.
- **Groups recorded** — every card/control/cell member names its group, so it moves as one.
- Each layer captured **in its native format** — text is live text, icons/logos/shapes are
  `type: "vector"` (a shape layer), only genuinely raster content is PNG. No vector or text baked to
  PNG by default.
- **Order** recorded, **target format** set, and **output scale/sizes** settled.

A frame that came in flat while its layers were available is a **gate failure, not a
shortcut** — the whole pipeline's value is here.

## Mistakes

- Exporting flat frames when the Figma layers were right there — the slideshow trap at
  its source.
- **Silently dropping a design element because you judged it "won't be visible."** A
  partially-clipped element is *on screen now*; a fully off-frame one usually *scrolls in*. Only a
  designer-hidden layer is a legitimate skip — and even that is surfaced if prominent, never a
  silent judgment call.
- Losing transforms/z-order, so composed layers stack or land wrong.
- Not tagging matched elements, forcing cross-dissolves later.
- Over- or under-splitting: hundreds of nodes to wrangle, or one blob that cannot move.
- **Flattening a vector or text layer to PNG by default** — text should stay live, icons/logos/
  shapes stay vector; PNG is only for genuinely raster content. Reaching for PNG per element is
  the freelance-default that softens the ad at any other scale.
- **Taking a raster from the node `export`** — it flattens transparency onto the frame's
  background, so a cutout lands on a black box. Use the fill's `rawImages` bitmap.
- **Declaring a shape layer `type: "image"`** — recording vector as raster is the same default
  wearing a different hat; it loses the resolution-free path.
- **Dropping a text layer's alignment or box behaviour** — capturing only `x/y/w/h` and then
  guessing `center`, or losing the fixed-width-clip box so the line soft-wraps to two downstream.
  Read `textAlignHorizontal` and the box sizing from Figma; don't infer them from position.
- **Not settling output scale up front** — discovering "it ships at three sizes" after baking
  single-scale PNGs means a re-import; ask it on the setup panel in the first five minutes.
- Binding a Figma link or local path directly — unfetchable; lift to a Picsart-hosted URL first
  (a `figma.com` SVG is CSP-blocked in preview just like any figma.com asset).
- Nagging about the Figma connector after the designer already chose the flat path.
