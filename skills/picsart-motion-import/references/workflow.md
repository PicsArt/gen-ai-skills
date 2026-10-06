# Stage 1 — Import: the design in as layers

Motion design animates *elements*, so the import's whole job is to bring the design in as
**layers, not flat frames**. A frame delivered as one sealed PNG can only ever
cross-dissolve; a frame delivered as its layers — panels, headline, buttons, the image,
the list — is a thing whose elements can slide, scroll, type on, parallax and
smart-animate. **Everything downstream is gated on this**: if the layers are lost here,
no amount of tuning later can recover the ad; it stays a slideshow.

## Pull the layer tree, per frame

Figma is a source the user brings. **When the host has a Figma connector**, read structure before
pixels through it: walk each frame's node tree, then export each animatable node as its own asset.
**When it doesn't**, the user exports each frame as an image and uploads it
(`picsart_media_upload`); that is the flat-frame fallback below (*When layers cannot be had*),
announced as a slideshow. For every layer capture:

> **AUDIT EVERY NESTED LAYER — never compose from Figma's simplified, frame-level output.** The
> single biggest way items go missing from the ad: Figma's frame-level / summarized read (a shallow
> design-context read, or a metadata read that stops at the top level) **collapses nested children**
> — groups, component instances, auto-layout children, masked contents — into a summary. Take that at
> face value and **every nested element is silently dropped**, so the composed frame is missing pieces
> that were plainly in the design. **Recursively expand each frame's FULL tree** (read the frame node
> with its children expanded, or walk *all* descendants) and audit it
> **node by node** — do not trust a frame-level layer list to be complete. **Completeness check:** the
> layers you capture must match the count of leaf/animatable nodes in the *fully-expanded* tree, not
> the handful the frame-level view showed. If a group or instance shows as one node, open it — its
> children are the layers. (Downstream this is the Stage-2 "layer count ≈ node count" gate; catch it
> here, at the read, not after a frame composes short.)

- **id** and **name/role** (what it is — `chrome`, `headline`, `cta`, `image`, `list`, `fx`)
- **type** — `text`, `vector` (icon/logo/shape), or `raster` (photo/complex image); plus `group`
- **transform** — `x, y, w, h, rotation, opacity`, and **z-order** (front-to-back)
- **parent/group** — so a group can move as one
- **for a text layer, also the type properties** — the **string**, the **font** (matched to a
  `picsart_media_list_fonts` entry) + size,
  **horizontal alignment** (read Figma's `textAlignHorizontal` — `left`/`center`/`right`; *never*
  guess it from position or from "it's a big headline"), and the **box sizing/wrap**: a Figma
  **fixed-width** text box that runs past the frame **clips, it does not wrap** — record the box
  width and that it clips, or the renderer soft-wraps the line into two downstream.

### Export each layer *as what it is* — PNG is the fallback, not the default

The layer's **source type** decides the export format. Deciding this per layer is the job;
reaching for PNG on every element is the freelance-default that quietly wrecks quality —
**stop and ask "is this layer actually raster?" before you export a PNG.**

- **Text** → keep as **live text** (the string + its font), *never* an image. This is
  what makes type-on, per-line and per-character animation possible; baking text to PNG kills
  all of it and can't reflow.
- **Vector** — icons, logos, line art, flat shapes → keep **vector**: export **SVG**, or keep a
  flat `#rrggbb` fill as a fill (no asset at all). **Default: turn the SVG's paths into a live
  shape layer** with `picsart_media_import_svg_path` (one call per `<path>` `d`, carrying its
  fill/stroke/opacity). A live shape needs no hosting, is never CSP-blocked, and can recolor and
  draw on. Keep the SVG itself as an uploaded asset only when it holds what paths can't express
  (filters, masks, embedded images/text). Vector stays crisp when it scales/pops and is lighter to
  move. Rasterize to PNG **only** if the node genuinely can't be had as vector.
- **Raster / photographic** — the hero image, a photo, a gradient/blur that won't survive as
  vector → **PNG with transparency** so the layer floats over what's behind it.

If you're about to export a PNG of an icon, logo, or shape, that's the tell you *defaulted*
instead of decided — go back and take it as vector.

**Settle output scale in the first five minutes, not the fiftieth.** Whether the ad ships at
one size or several (multiple ratios/resolutions, or any later up-scale) is what makes vector
the *normal* case, not an edge case — a PNG baked at one scale is soft or jagged at any other,
while vector is resolution-free. Decide this up front (see *Set the format* below); don't
discover the constraint at export time and re-import. And when you do capture
a vector layer, **declare it `type: "vector"`** — silently recording an SVG as `type: "image"`
is the same defaulting mistake wearing a different hat.

**Format doesn't excuse hosting:** a vector converted to a live shape needs no asset at all. But
whatever you keep as a file, the asset still has to be lifted onto a
**Picsart-hosted `https://` URL** (below). A `figma.com` SVG URL is CSP-blocked in the preview
exactly like any other figma.com asset — "keep it vector" does **not** mean "author the
figma.com link." Export vector → upload → author the returned Picsart URL.

### Granularity — split to what moves

Not every node, and not one blob. **A layer is anything that either moves independently or
persists across frames.** Group the rest.

- Split out: the headline, each CTA, the hero image, a scrollable list, a tap target,
  anything that will animate on its own.
- Keep grouped: static decoration, a card's fixed internals, backgrounds.
- Over-splitting (hundreds of nodes) is noise the designer must wrangle; under-splitting
  (the whole screen as one image) is the slideshow trap in disguise. When unsure, split
  by what the ad would animate.

### Import every element the design shows — visibility is the design's call, not yours

Import **every element the design renders**. A layer is dropped for exactly one reason: the
**design itself hides it** (Figma `visible:false` / a `hidden` node) — that is the designer's
signal, and even then a *prominent* hidden layer is worth a note, since it may be meant to appear
mid-animation. **Never drop a layer because *you* judged it "won't be seen":**

- **Partially on-frame** (clipped by the frame edge) is **on screen** — it shows in the very first
  hold, so omitting it is a visible hole against the design. A search pill or tag row cut by the
  frame edge is *clipped, not absent*, and dropping it leaves the composed frame missing content
  the mockup plainly shows.
- **Fully off-frame is not a licence to drop it either.** In motion a wide row or an off-edge
  element is usually there to **scroll or pan into view** — import it and let choreography decide,
  don't pre-empt the motion by deleting it (that is how a design's intended scroll becomes a
  static gap).

A judgment call to leave something out is **surfaced to the designer, never silent** — same rule
as a missing font. The Stage-2 compare against the design's frame image is what catches a dropped element, as a
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
collapses to a cut. (This is the import half of
[`motion-patterns.md`](../../picsart-motion/references/motion-patterns.md) *"Progressive text build."*)

The A→B **delta** itself (how far a matched layer moved, what actually changed) is not judged
by eye at motion time — it is **read with `picsart_media_diff_layouts`** (which resolves both
frames through `query_layout` and returns the classified delta; `query_layout`-on-both is the
fallback when the tool is unavailable). The `matchKey` you set here is exactly what that diff
takes as its `matchHints` to pair the layers up — a dropped key becomes a missed match there.
The full frame-diff procedure is in
[`../../picsart-motion/references/motion-principles.md`](../../picsart-motion/references/motion-principles.md) §1.

## Get every asset onto a real URL

A Figma export and a `file://` path are both **unfetchable by the renderer**. So each
layer asset that is not already a Picsart-hosted `https://` URL must be lifted onto one:
`picsart_media_upload` (the drag-and-drop panel, for a file the user has locally) or `picsart_drive`
`action: "upload"` (for media already at a URL), then **read back the resulting `https://` URL and
author *that*.** Text and fills carry no asset and need no lift.

**A scene asset's `uri` must be a Picsart-hosted `https://` URL (the ones Picsart tools return) —
never a base64 `data:` URI, and never a `figma.com`
URL.** The editor preview runs in a browser that blocks both — they get **blocked → blank** in
the editor preview, even though the scene *validates* and the
server-side `export`/`contact_sheet` render them fine. That server/browser split is the trap: a
`figma.com` URL or a `data:` URI is only ever an **intermediate** — hand it to `upload`/`drive` and
author the **Picsart-hosted URL it returns**. **`validate_scene` and a clean `contact_sheet` do NOT
prove it renders in the preview** (both are lenient server-side paths) — the only reliable proof is
the editor preview itself, so default to Picsart-hosted URLs and it's fine everywhere.

## When layers cannot be had — the honest fallback

Two cases force flat-frame ingest, and both are a **degrade, announced**:

- **No Figma connector on the host.** Suggest it once, and offer the fallback in the same turn —
  never block, never re-ask, and you cannot connect it for them:
  > Connecting Figma in your app's connector settings lets me pull your design's layers,
  > which is what makes real motion design possible. Without it I can only animate whole
  > flat frames — a slideshow. Connect it and share the Figma file, or export your frames
  > from Figma as images and upload them to do the simpler version.

  For the flat path, open `picsart_media_upload` (`accept: "image"`) so the user can drop the
  exported frames; their URLs arrive on the next message.
- **Figma export quota'd out.** Figma export is metered **per Figma seat** and can quota
  out mid-batch — that is **status, not an error**: continue on the upload path for the
  remaining assets, and if only flats are reachable, say the result will be a slideshow
  and offer to resume layered when the seat's quota returns.

A flat frame is imported as a single `image` layer filling the composition — the montage
fallback in the `picsart-motion` skill. Say plainly what is lost: *"without the layers this is a
slideshow, not motion design."*

## Order — take Figma's, never ask for it

The running order is **Figma's own** — the frame/artboard sequence in the file (or, for
pasted images, the order they were given in). **Take it as authoritative, record it, and
move on — do not ask the designer to confirm it.** A question the source already answers is
noise — the house rule: *"don't turn something the pipeline
already knows into a user choice."*

Reordering is **optional and designer-initiated**: it happens in chat, when the designer
explicitly says "swap 2 and 3" (a markdown table of the frames in order can be shown for a
glance, never as a mandatory confirm). Absent that, Figma order stands, silently. Never open
the host question interface to confirm the running order.

## Set the format — inferred directly (no setup widget)

Decide the video-wide format yourself from the material — **infer it, state it, and proceed**;
this workflow does not use the `picsart_motion_setup` console. Choose:

- **ratio / resolution** — from the frames' own aspect (1080×1920 → 9:16 at 1080×1920). Take what
  the design already is.
- **fps** — 30 by default.
- **energy** — read from the design (see below); pick the register the ad calls for.
- **output scale/sizes** — default to a single size, but **surface the question when it's genuinely
  open**: will this ship at one size or several (multiple ratios/resolutions, or a later up-scale)?
  The answer decides raster-vs-vector for every layer above, and "multiple sizes" makes vector the
  norm — cheap to settle now, expensive to discover at export. When it isn't obvious, a plain
  the host question interface is the right surface; otherwise state the single-size default and move on.

State the chosen ratio/fps/energy to the designer in one line and let them adjust in plain
conversation ("make it square", "60fps", "more energetic") — a normal message, not a widget.

**`energy` is a productive↔expressive dial**, not just "fast vs slow": *productive* =
subtle, efficient motion for routine beats; *expressive* = vibrant, highly-visible motion for
significant moments (an opening, a primary CTA, a hero reveal). It scales the motion's duration
and easing register downstream — see
[`../../picsart-motion/references/motion-principles.md`](../../picsart-motion/references/motion-principles.md) §6.

Two things are never asked: **order** (taken from Figma silently, above) and **total duration**
(derived from the motion, never a target; a designer who wants it tighter says "punchier").

## Output → `motion.json`

Write frames-of-layers and the target (schema in the `picsart-motion` skill). Each frame carries
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
- Each layer captured **in its native format** — text is live text, icons/logos/shapes are
  `type: "vector"` (SVG/fill), only genuinely raster content is PNG. No vector or text baked to
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
- **Declaring an SVG layer `type: "image"`** — recording vector as raster is the same default
  wearing a different hat; it loses the resolution-free path.
- **Dropping a text layer's alignment or box behaviour** — capturing only `x/y/w/h` and then
  guessing `center`, or losing the fixed-width-clip box so the line soft-wraps to two downstream.
  Read `textAlignHorizontal` and the box sizing from Figma; don't infer them from position.
- **Not settling output scale up front** — discovering "it ships at three sizes" after baking
  single-scale PNGs means a re-import; settle it when you set the format, in the first five minutes.
- Binding a Figma link or local path directly — unfetchable; lift to a Picsart-hosted URL first
  (a `figma.com` SVG is CSP-blocked in preview just like any figma.com asset).
- Nagging about the Figma connector after the designer already chose the flat path.
