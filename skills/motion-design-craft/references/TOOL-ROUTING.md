# Tool routing — which tool for which job

The rule under everything (see the `animate-design` skill): **ground your facts in tools, own your
judgment, author through tools** — get every *fact* (layers, coordinates, what changed between
frames, valid easings/presets) from the tool that owns it and never invent it; apply your
*judgment* (which motion, timing, focal element) on those facts, with the designer; and *author*
every edit through a tool, never hand-written. This is the lookup for *which* tool. When a
request maps to a tool here, call it; do not substitute a guess for a fact the tool would give you.

Tool names are the connector's `picsart_scene_*` (scene authoring), `picsart_media_*` (media
analysis) and `picsart_*`. These docs often use a short name (`validate_scene`, `patch_scene`) or
an older `mp_<x>` one. No prefix rule turns a short name into the tool's name, because several
tools changed their suffix in the 4.6.0 rename (`layout_lint` is now `picsart_scene_lint_layout`).
Look the short name up in this table. A short name that is not in the table is not a tool:
do not guess a name for it.

| Short name in these docs (also as `mp_<short>`) | Call this tool |
|---|---|
| `upload` | `picsart_drive_upload_ask` |
| `analyze_audio` | `picsart_media_analyze_audio` |
| `describe_video` | `picsart_media_describe_video` |
| `probe`, `probe_media` | `picsart_media_probe` |
| `reframe_video` | `picsart_media_reframe_video` |
| `screen_moments` | `picsart_media_screen_moments` |
| `screen_stages` | `picsart_media_screen_stages` |
| `transcribe` | `picsart_media_transcribe` |
| `video_stills` | `picsart_media_video_stills` |
| `apply_gradient` | `picsart_scene_apply_gradient` |
| `apply_preset` | `picsart_scene_apply_preset` |
| `apply_scene_template`, `apply_template` | `picsart_scene_apply_template` |
| `capabilities`, `get_capabilities` | `picsart_scene_capabilities` |
| `check_contracts` | `picsart_scene_check_contracts` |
| `check_motion` | `picsart_scene_check_motion` |
| `contact_sheet` | `picsart_scene_contact_sheet` |
| `diff_layouts` | `picsart_scene_diff_layouts` |
| `editor` | `picsart_scene_editor` |
| `expand_ref`, `expand_scene_ref` | `picsart_scene_expand_ref` |
| `export` | `picsart_scene_export` |
| `fonts`, `list_fonts` | `picsart_scene_fonts` |
| `import_figma_paint` | `picsart_scene_import_figma_paint` |
| `import_svg_path` | `picsart_scene_import_svg_path` |
| `inspect`, `inspect_scene` | `picsart_scene_inspect` |
| `layout_lint`, `lint_layout` | `picsart_scene_lint_layout` |
| `list_looks`, `looks` | `picsart_scene_looks` |
| `patch`, `patch_scene` | `picsart_scene_patch` |
| `query_layout` | `picsart_scene_query_layout` |
| `get_recipe`, `recipe` | `picsart_scene_recipe` |
| `resolve_looks` | `picsart_scene_resolve_looks` |
| `motion_setup`, `setup` | `picsart_scene_setup` |
| `list_scene_templates`, `templates` | `picsart_scene_templates` |
| `translate`, `translate_scene` | `picsart_scene_translate` |
| `validate`, `validate_scene` | `picsart_scene_validate` |

**This whole pipeline is free — it uses no
paid tools.** Compose, query, validate, the panel, `contact_sheet` and `export` are all 0-credit
(export/contact_sheet may show a "writes a file / charged"-looking badge from their `readOnlyHint:
false` annotation — that is behavior, not price; credits are zero). The only tools that charge are
**generative or analysis** tools (`picsart_generate`, the four `picsart_image_*` edits, and the paid
media analyses such as `picsart_media_describe_video`; each says so in its description), and this
flow calls none of them — so never warn the designer about cost.

## The opening sequence — "add motion to this Figma design"

When the user gives a Figma link (or file) and asks for motion, this is the tool run — in
order, before any motion is authored. Do not skip ahead to animating; a scene that isn't
composed and verified first produces wrong motion on wrong geometry.

**For the full, reproducible end-to-end procedure — including the coordinate rules that make
positions correct (frame-relative → composition, `position` = layer *center*, exact coords never
eyeballed) — follow [`AUTHORING-FLOW.md`](AUTHORING-FLOW.md).** It is the golden path; the steps
below are its tool-by-tool summary.

**Phase 0 — orient (all free, one call each):**
1. `picsart_scene_recipe` — with no `name`, the index of recipes; the `quick-merge-and-export`
   recipe is the server's on-ramp for common jobs (prefer what a recipe says over this list if
   they disagree).
2. `picsart_scene_capabilities`, schema sections — the scene shape you are about to author.
   **It is ~200KB in full — always narrow it:** ask for `["schemaSummary"]` (field names/types,
   ~8KB) or `["schema:<Definition>"]` for one definition, never `["schema"]` whole. If a call
   ever overflows context, do **not** re-call it blind; lean on the catalog sections + these
   references for the shapes instead.
3. `picsart_scene_capabilities` — the real presets / easings / effects / limits. **It answers
   only to exact section names, and one wrong name fails the whole call.** Called with no arguments
   it returns just the index of section names; then pass `sections` from it. The ones this skill
   uses: `easing` (easing ids), `motionPresets`, `textAnimations`, `transitions`, `effects`, `mask`,
   `layerContentKinds`, `compositionCamera`, `expressionAnimation`, `limits`, and `looksCompact` to
   choose a look, then `look:<id>` for one look in full. **Never** a name made from a word
   (`easings`, `presets` are refused) and **never** `["all"]` — the whole document overflows
   context; ask for a large section (`effects`, `looks`, `supports`) in a call of its own. A refused
   call's error lists the valid names: take the name from there.
4. `picsart_scene_fonts` — the available fonts (needed for the compose font check). Its
   `query` also searches the live catalog (`live.fonts`), for a design font outside the bundled
   snapshot.

**Phase 1 — import (the FIGMA connector reads; Picsart tools lift):**
5. Figma `get_metadata` / `get_design_context` — the frames in **Figma's order** (never ask
   the user to confirm it) and each frame's **layer tree**.
6. Decide granularity: split to **what moves** (headline, button, hero = own layers).
7. **Tag matched elements** across frames (one `matchKey` per element that persists) — this
   is what enables smart-animate; skipping it forfeits the whole product.
8. `picsart_drive_upload_ask` — **only the RASTER/external-media assets** (photos, videos, textures,
   unavoidable raster) onto a real https URL (the renderer cannot fetch Figma exports or file://
   paths). **Text, shapes, cards, borders, circles, masks, and vectors/icons need NO asset — they
   are authored as native scene elements, never uploaded or rasterized.** "Upload every asset" is
   external media only, never every visual element.
   **First** create this design's own Drive folder — `picsart_drive_create_folder` with
   `path: "Motion Projects/<Figma design name>"` (idempotent) — and pass its `folderUid` on
   **every** upload for this project. One design = one folder; nothing lands loose in the root.
9. **Set the format on `picsart_scene_setup`.** Open the Motion Setup console once, prefilled:
   the frames in order, the ratio from their aspect (1080×1920 → 9:16) and the energy from the
   design in `suggested.selections`, never a total duration; its lock replies
   `motion_setup_feedback`. Without the console, infer the same, state it to the designer and let
   them adjust in plain conversation. Surface output scale as a plain ASK only
   when it's genuinely open. (See `design-layer-import` *Set the format*.)

**Phase 2 — create the scene (compose):**
10. Build each frame as a **composition of scene layers** — one scene layer per imported
    design layer, placed by its `transform` — via `picsart_scene_patch` (`add` ops,
    id-keyed layers + assets), or a compose recipe/template if the server offers one.
    **Never** bind frames to `mpscene://montage` (that flattens them → slideshow). A
    matched element is **one continuous layer** with per-frame transform states.
11. Font check against the `list_fonts` result — a missing font is **surfaced**, never
    silently swapped.
12. `picsart_scene_validate` — fix until clean.
13. Render-match: one `picsart_scene_contact_sheet` frame per composed frame vs the design
    — **a composed frame must render identical to the mockup** before motion starts.

Only after 13 passes does motion begin: pair 1→2, the edit
loop, pair by pair. (No Figma connector / flat images only → the flat-frame fallback in
`design-layer-import`: say it will be a slideshow, offer layered.)

The authoring methods that were once server-only recipes ship as skills of this plugin: read
`figma-storyboard-animation` (the canonical Figma→scene flow), `motion-intent`, `motion-pattern-library`,
`scene-animation-reference` and `custom-transitions` by name.

## Optional capabilities — check your tool list first

Some tools/recipes are **connector-dependent** (not on every deployment, and commonly **not mirrored
today**). Look for them in your tool list; if present, prefer them; if absent, treat it as normal and
use the fallback — never assume they exist.

| If it's in your tool list | Use it for | Fallback when absent |
|---|---|---|
| `picsart_scene_lint_layout` | **occlusion / overlap QA — run it on every scene when present** (a cheap automatic pass over the whole timeline): flags overlapping boxes over time, z-order aware | it's **opacity-blind**, so *in addition* verify occlusion on a `contact_sheet` frame at the deepest overlap to catch a semi-transparent leak — additive to the lint, not a replacement for it ([`MOTION-TROUBLESHOOTING.md`](MOTION-TROUBLESHOOTING.md)) |

## By job

| You need to… | Tool |
|---|---|
| Read the layers, geometry, stacking, active windows | `picsart_scene_query_layout` (at a `time`; `verbose:true` adds raw matrices and transform components). A layer's authored content — its items, paints, effects — is read from the scene document itself, by the id `query_layout` returns |
| Decide **what changed** between two frames / what should animate | `picsart_scene_diff_layouts` (frame A + frame B + the import `matchKey`s as `matchHints`) → returns each layer's class (moved/resized/restyled/content-changed/entered/exited/unchanged) with root-space deltas + a whole-pair `relationship`; animate only what changed. **Fallback:** `query_layout` on A **and** B and diff by hand. **Caveat:** the diff is opacity-blind (reads only `visible`) — check fades yourself. Procedure + change→motion mapping in [`MOTION-PRINCIPLES.md`](MOTION-PRINCIPLES.md) |
| Get a value the scene/layout tools don't carry — **exact text ink bounds** (`absoluteRenderBounds`), glyph / per-character positions, sub-string geometry | `use_figma` (**read-only** JS via the Figma Plugin API — read `node.absoluteRenderBounds`, character boxes). `get_metadata` / `query_layout` return only a text node's **layout box**, which is *not* the glyphs — positioning text by it lands it wrong (see [`AUTHORING-FLOW.md`](AUTHORING-FLOW.md) §2/§4) |
| Check for **unintended overlaps / occlusion** (a cover leaking, colliding layers) | `picsart_scene_lint_layout` — **run it whenever it's in your tool list** (cheap automatic pass, flags overlapping boxes over time, z-order aware). It's **opacity-blind**, so *also* verify occlusion on a `contact_sheet` frame at the deepest overlap to catch a semi-transparent leak — the frame check is additive, it does not replace the lint ([`MOTION-TROUBLESHOOTING.md`](MOTION-TROUBLESHOOTING.md)) |
| Know a source clip's duration / dimensions / fps | `picsart_media_probe` |
| Know the valid presets, easings, effects, looks, limits | `picsart_scene_capabilities` |
| Know the available fonts | `picsart_scene_fonts` (bundled snapshot, plus a live search of the catalog in `live.fonts` for a `query`). Author a text layer's font with the entry's **catalog key**, its resolved **file URL** (`.ttf`/`.otf`), or an `assets[]` `{type:"font"}` entry carrying that URL, never a bare family name (it fails `validate_scene`); keys and URLs both open in the scene editor, where a font URL must use HTTPS on `picsart.com` or a `*.picsart.com` host to load |
| Get the scene JSON schema | `picsart_scene_capabilities` with `schemaSummary` or `schema:<Definition>` |
| Apply / author a motion preset on a layer | `picsart_scene_apply_preset` with `motionPreset:<id>` |
| Animate text (type-on, word/char stagger…) | `picsart_scene_apply_preset` with `textAnimation:<name>` |
| Apply an effect / a look | `picsart_scene_apply_preset` with `effect:<id>` / `look:<id>` |
| **Reproduce a design's visual treatment** — rounded corners, drop shadow, glow, blurred fill, reflection, color grade, frame/badge — instead of baking it into a PNG or dropping it | **Resolve the exact id from `get_capabilities` first**, then `picsart_scene_apply_preset` with `look:<id>` (style bundles: `rounded_corners`, `blur_fill`, `clip_path`, `reflection`…) / `effect:<id>` (`drop_shadow`, `gaussian_blur`…). The catalogue is large — **19 looks + 137 effects — so *enumerate* it and match by name/description; don't assume the treatment isn't supported** (see [`SCENE-VOCABULARY.md`](SCENE-VOCABULARY.md)) |
| Author a **gradient** (fill, stroke, background, or overlay) | `picsart_scene_apply_gradient` on an **existing shape layer** that already has geometry (`rect`/`ellipse`/`path`/`polystar`). Colors in `stops` (`#rrggbb`), transparency in a separate `alphaStops` ramp; `linear` or `radial`; re-applying replaces the paint instead of stacking. Stops are static, but the endpoints can be animated afterward. Don't hand-write the `gradientFill` object. For patterns (gradient text, a wash over media, a sweep), see the `scene-gradients` recipe (`get_recipe`) |
| **Bring an SVG icon / logo / line art (uploaded, or a Figma vector's path data) in as a live shape** (animatable, recolorable, draw-on, no asset, no CSP) instead of an SVG asset. A Figma vector's CSS paint then goes on with `picsart_scene_import_figma_paint` (next row) | `picsart_scene_import_svg_path`: pass each `<path>`'s `d` onto a shape layer. Add `color` (+ `fillRule`, `fillOpacity`) and/or `stroke` + `width` (+ `strokeOpacity`) from that path's own attributes. Call it once per differently-painted path, into the **same** layer so a mark stays one unit. Coordinates come in as the SVG's user units: `viewBox`/`transform` are **not** applied, so scale and place the result with the layer's `transform`. For a **gradient** path, import it with no paint onto a dedicated shape layer, then call `picsart_scene_apply_gradient`. Keep the SVG as an uploaded asset only for content paths can't express (filters, masks, embedded images/text), and disclose that |
| **Bring a Figma shape over as a native shape layer** (see `design-layer-import`), or just an element's paint (its fill, box-shadow, or CSS gradient from `get_design_context`), instead of baking it into an SVG/PNG | **Create the shape layer first** — `picsart_scene_patch` adds it (`content.kind: "shape"`, a `rect`/`ellipse` item sized to the node, placement in its `transform`), or `picsart_scene_import_svg_path` appends a non-rectangular outline to it — **then paint it** with `picsart_scene_import_figma_paint` (`scene` + that `layerId`): `fill` → shape fill, outer `boxShadow` → `drop_shadow`, `gradient` → `gradientFill` (pass the element `size`; `gradientPaint: "stroke"` + `gradientStrokeWidth` for an outline). It paints an EXISTING layer only and never creates one; `fill`/`gradient` need a shape layer, `boxShadow` alone takes any visual layer. **Read `skipped`**: an **inset** shadow has no native primitive yet, so keep a bake for that one treatment and **tell the designer** |
| Instantiate a template (montage, title, slide…) | `picsart_scene_apply_template` (+ `list_scene_templates` with a category or tags filter and `detail:"full"` to compare descriptions / the `template:<uri>` capabilities section) |
| **Edit anything already in the scene** — timing, easing, params, position, colour, text, opacity, or a transition on a seam | `picsart_scene_patch` (id-anchored → a new `sceneRef`) |
| Validate a scene before rendering | `picsart_scene_validate` |
| Show / preview the motion | `picsart_scene_editor` — play the **whole scene built so far** (titled for the current pair) in the browser so the pair is seen in context (free; don't re-export just to see it); `picsart_scene_export` for a rendered video / the final deliverable |
| Preview as stills / a strip | `picsart_scene_contact_sheet` (a grid), `picsart_scene_export` (`mediaType: "png"` with `startTime`, one specific frame per call) |
| Show the finished motion as a video | `picsart_scene_export` — the WHOLE reel, not one pair |
| Bring in a user's file → an asset URL | `picsart_drive_upload_ask` |
| **Generate video footage (SPENDS CREDITS — gated)** | Flow, in order: `picsart_credits` (show balance first) → `picsart_model_catalog` (`concise: false`) then `picsart_model_choose` (designer picks the model) → `picsart_model_params` (schema) → **`picsart_preflight` (exact dry-run cost, free)** → **quote the cost + get explicit yes** → `picsart_generate` (`async` for video, pass project `folderUid`) → its own card follows the job (watch) → place the clip as a `media` layer. **No preflight cost shown + no explicit yes = no generate.** Full gate in the `animate-design` skill *Video generation*. |

## By user request — the common ones

**This is the plugin's core loop.** The designer points at a part and says a small edit —
*"speed this up", "drop the animation from that", "update the easing", "this button has an
extra outline"*. Every one is the same shape: **locate** the target (`picsart_scene_query_layout` for its
id and box, then that layer in the scene document for its content) → **edit** it (`picsart_scene_patch`, `set` or `remove`, id-anchored)
→ **validate** (runs inside `patch_scene`) → **show** (the panel or `export`). Never "fix" it
by describing the change or answering from your reading of the image — author it through the tool.

| The designer says… | Do this |
|---|---|
| "make this **faster**" | `query_layout` → `patch_scene` `set` → shorten the animation's **duration** on that layer |
| "**slower** / hold it longer" | `patch_scene` `set` → lengthen the duration or the frame's hold |
| "make it **ease-in-out** / snappier / smoother" | `get_capabilities` (`sections: ["easing"]`) for the easing id → `patch_scene` `set` **easing** |
| "**remove** the animation from this / make it static again" | `query_layout` → `patch_scene` **`remove`** the layer's animation (no `path` on the animation entity, or the `animations` field) |
| "this button has an **extra outline** / drop the stroke / border" | `query_layout` (the layer's id) → find its stroke item / outline effect in that layer of the scene document → `patch_scene` **`remove`** that stroke/effect item |
| "**delete / hide** this layer" | `patch_scene` **`remove`** the layer (or `set` its opacity to 0) |
| "**slide** it in from the right / scroll / pop / parallax it" | pick the preset via `get_capabilities` (`sections: ["motionPresets"]`) → `apply_preset` with `motionPreset:<id>` (or `patch_scene` to tune an existing one) |
| "type the headline **on** / stagger it in" | `apply_preset` with `textAnimation:<name>` |
| "change the **colour / text / opacity / position**" | `patch_scene` `set` (id-anchored, the authored property) |
| "use a **crossfade / slide / cut** at this seam" | `patch_scene` `set` → the seam's `transition` + `transitionDuration` |
| "what **fonts** can I use?" | `picsart_scene_fonts` (its `query` also live-searches the catalog) |
| "how **long** is this clip?" | `picsart_media_probe` |
| "**show me** the result / play it" | `picsart_scene_export` the WHOLE reel → play the video (or the editor on a pair) |
| "is this **valid** / will it render?" | `picsart_scene_validate` |
| "how should I animate this **page transition / button tap / list / modal**?" | the scenario recipe in [`MOTION-PATTERNS.md`](MOTION-PATTERNS.md); for sequencing several elements, [`CHOREOGRAPHY.md`](CHOREOGRAPHY.md) — then author via `apply_preset` / `patch_scene` (values from `get_capabilities`) |
| "this **feels robotic / too slow / cheap / distracting**" | look up the symptom in [`MOTION-TROUBLESHOOTING.md`](MOTION-TROUBLESHOOTING.md) → apply the concrete fix through the same locate→edit→show loop |

### Worked example — *"this scroll should be faster and ease-in-out"*

1. `picsart_scene_query_layout` — find the scroll layer and read its **current** timing/easing (don't assume which layer or what it is now).
2. `picsart_scene_capabilities` with `sections: ["easing", "limits"]` — the real `ease_in_out` id and the duration/speed bounds (so you write a legal value, not "ease in out").
3. `picsart_scene_patch` — on that animation: **shorter duration** (= faster) + **easing `ease_in_out`**. Mints a new `sceneRef`.
4. `picsart_scene_validate` — confirm it's valid.
5. **Show** the new scroll moving — view it in `picsart_scene_editor`, or `picsart_scene_export` it as a rendered video.

Not: *"it's ~1.2s, I'll make it 0.6s ease-in-out"* in prose and move on. That is the failure.

## Anti-patterns — fabricated facts & hand-built artifacts (the tells)

- Describing layers, coordinates, or fonts from **looking at the image** instead of `query_layout` — an invented fact. (Need exact text ink/glyph positions the layout box doesn't carry? That's not an eyeball case and not a reason to give up — read `absoluteRenderBounds` via `use_figma`, read-only.)
- Inferring **what changed between two frames** by eye instead of running `picsart_scene_diff_layouts` (or, as fallback, reading both frames' geometry from `query_layout`).
- **Hand-writing scene JSON** or typing in coordinates instead of `patch_scene` / the apply tools.
- **Naming an easing or preset from memory** instead of `get_capabilities`.
- Deciding the motion (your job) but then **describing it in prose** instead of authoring it through the tool and showing the render — stopping at a description is the failure, not the deciding.
- Proceeding as if you had real data when the tool was never called — or when it wasn't available: then **say so and stop**, don't self-substitute.
- **Asking permission before a free call** — "the render needs your go-ahead", "say go and I'll run it", or any type-a-keyword-to-continue prompt. Free previews and validations run unasked; the designer approves the *shown result*, not the tool call.
