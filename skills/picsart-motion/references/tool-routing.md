# Tool routing — which tool for which job

The rule under everything (see the `picsart-motion` skill): **ground your facts in tools, own your
judgment, author through tools** — get every *fact* (layers, coordinates, what changed between
frames, valid easings/presets) from the tool that owns it and never invent it; apply your
*judgment* (which motion, timing, focal element) on those facts, with the designer; and *author*
every edit through a tool, never hand-written. This is the lookup for *which* tool. When a
request maps to a tool here, call it; do not substitute a guess for a fact the tool would give you.

Tool names are `picsart_media_*` / `picsart_*`. **This whole pipeline is free — it uses no
paid tools.** Compose, query, validate, the panel, `contact_sheet` and `export` are all 0-credit
(export/contact_sheet may show a "writes a file / charged"-looking badge from their `readOnlyHint:
false` annotation — that is behavior, not price; credits are zero). The only tools that charge are
**generative** (`picsart_generate`, `change_bg`, `remove_bg`, `enhance`, `vectorize`,
`media_describe_video`), and this flow calls none of them — so never warn the designer about cost.

## The opening sequence — "add motion to this Figma design"

When the user gives a Figma link (or file) and asks for motion, this is the tool run — in
order, before any motion is authored. Do not skip ahead to animating; a scene that isn't
composed and verified first produces wrong motion on wrong geometry.

**For the full, reproducible end-to-end procedure — including the coordinate rules that make
positions correct (frame-relative → composition, `position` = layer *center*, exact coords never
eyeballed) — follow [`authoring-flow.md`](authoring-flow.md).** It is the golden path; the steps
below are its tool-by-tool summary.

**Phase 0 — orient (all free, one call each):**
1. `picsart_media_quickstart` — the server's on-ramp for this job (it surfaces the relevant
   recipe steps; prefer what it says over this list if they disagree).
2. `picsart_media_get_scene_schema` — the MP Scene shape you are about to author. **It is ~200KB in
   full — always narrow it:** pass `summary:true` (field names/types, ~8KB) or `name:"<Definition>"`
   for one definition. Never call it bare: the full document overflows context.
3. `picsart_media_get_capabilities` — the real presets / easings / effects / limits (also large —
   pass `sections`, never the whole thing; see the tool's own note).
4. `picsart_media_list_fonts` — the available fonts (needed for the compose font check): the
   built-in catalog plus, on page 1, a live search (`live.fonts`) for a face the catalog lacks.

**Phase 1 — import (the host's Figma connector reads, when the host has one; Picsart tools lift):**
5. Through the host's Figma connector — the frames in **Figma's order** (never ask
   the user to confirm it) and each frame's **layer tree**. **No Figma connector:** the user
   exports each frame as an image and uploads it (`picsart_media_upload`) — the flat-frame
   fallback in `picsart-motion-import` (say it will be a slideshow, offer layered).
6. Decide granularity: split to **what moves** (headline, button, hero = own layers).
7. **Tag matched elements** across frames (one `matchKey` per element that persists) — this
   is what enables smart-animate; skipping it forfeits the whole product.
8. **Only the RASTER/external-media assets** (photos, videos, textures, unavoidable raster) go onto
   a Picsart-hosted https URL (the renderer cannot fetch Figma exports or file:// paths): a file
   the user has locally comes in through `picsart_media_upload` (the upload widget); media already
   at a URL is saved with `picsart_drive` `action: "upload"`. **Text, shapes, cards, borders,
   circles, masks, and vectors/icons need NO asset — they are authored as native scene elements,
   never uploaded or rasterized.** "Upload every asset" is external media only, never every
   visual element.
   **First** create this design's own Drive folder — `picsart_drive` `action: "create_folder"` with
   `path: "Motion Projects/<Figma design name>"` (idempotent) — and pass its uid as `folderUid` on
   every `picsart_drive` upload for this project (batch a set in one call with `files`). One
   design = one folder; nothing lands loose in the root.
9. **Decide the format directly (no setup widget).** Infer ratio/resolution from the frames'
   aspect (1080×1920 → 9:16), fps 30, and energy from the design; state them to the designer and
   let them adjust in plain conversation. Surface output scale as a question in the host question interface only
   when it's genuinely open. (See `picsart-motion-import` *Set the format*.)

**Phase 2 — create the scene (compose):**
10. Build each frame as a **composition of scene layers** — one scene layer per imported
    design layer, placed by its `transform` — via `picsart_media_patch_scene` (`add` ops,
    id-keyed layers + assets), following the `figma-storyboard-to-scene` recipe.
    **Never** bind frames to `mpscene://montage` (that flattens them → slideshow). A
    matched element is **one continuous layer** with per-frame transform states.
11. Font check against the `list_fonts` result — a missing font is **surfaced**, never
    silently swapped.
12. `picsart_media_validate_scene` — fix until clean.
13. Render-match: one `picsart_media_contact_sheet` frame per composed frame vs the design
    — **a composed frame must render identical to the mockup** before motion starts.

Only after 13 passes does motion begin: pair 1→2, the edit
loop, pair by pair. (No Figma connector on the host / flat images only → the flat-frame fallback in
`picsart-motion-import`: the user exports the frames as images and uploads them; say it will be a
slideshow, offer layered.)

## Recipes and lint — with their fallbacks

Prefer these when they cover the job; when one doesn't (a named recipe isn't in the catalogue), use
the fallback.

| Tool | Use it for | Fallback |
|---|---|---|
| `picsart_media_get_recipe` / `picsart_media_list_recipes` | the **official authoring recipes** — **`figma-storyboard-to-scene`** (canonical Figma→scene flow), `motion-intent` / `motion-patterns` / `motion-mechanics`, `transition-authoring` | this skill's references (`authoring-flow`, `motion-principles`, `motion-patterns`, `transitions`, `mp-scene-vocabulary`) + `picsart_media_quickstart` |
| `picsart_media_layout_lint` | **occlusion / overlap QA — run it on every scene** (a cheap automatic pass over the whole timeline): flags overlapping boxes over time, z-order aware | it's **opacity-blind**, so *in addition* verify occlusion on a `contact_sheet` frame at the deepest overlap to catch a semi-transparent leak — additive to the lint, not a replacement for it ([`motion-troubleshooting.md`](motion-troubleshooting.md)) |

## By job

| You need to… | Tool |
|---|---|
| Read the layers, geometry, stacking, active windows, authored content | `picsart_media_query_layout` (geometry at a `time`); the authored values are in the scene document itself |
| Decide **what changed** between two frames / what should animate | `picsart_media_diff_layouts` (frame A + frame B + the import `matchKey`s as `matchHints`) → returns each layer's class (moved/resized/restyled/content-changed/entered/exited/unchanged) with root-space deltas + a whole-pair `relationship`; animate only what changed. **Fallback:** `query_layout` on A **and** B and diff by hand. **Caveat:** the diff is opacity-blind (reads only `visible`) — check fades yourself. Procedure + change→motion mapping in [`motion-principles.md`](motion-principles.md) |
| Get a value the scene/layout tools don't carry — **exact text ink bounds** (`absoluteRenderBounds`), glyph / per-character positions, sub-string geometry | When the host's Figma connector can run a **read-only** Plugin API read, read `node.absoluteRenderBounds` / character boxes there. **Otherwise** measure the ink: render the composed frame with `picsart_media_contact_sheet` (`times`) and compare against the user's exported frame image via `picsart_view_image`, nudging until the glyphs sit where the design has them. A Figma metadata read and `query_layout` return only a text node's **layout box**, which is *not* the glyphs — positioning text by it lands it wrong (see [`authoring-flow.md`](authoring-flow.md) §2/§4) |
| Check for **unintended overlaps / occlusion** (a cover leaking, colliding layers) | `picsart_media_layout_lint` — **run it on every scene** (cheap automatic pass, flags overlapping boxes over time, z-order aware). It's **opacity-blind**, so *also* verify occlusion on a `contact_sheet` frame at the deepest overlap to catch a semi-transparent leak — the frame check is additive, it does not replace the lint ([`motion-troubleshooting.md`](motion-troubleshooting.md)) |
| Know a source clip's duration / dimensions / fps | `picsart_media_probe_media` |
| **Match the real motion of a reference clip** (copy an actual move instead of guessing keyframes) | `picsart_media_probe_media` (duration / fps) → place the clip as a `media` layer and pull `picsart_media_contact_sheet` stills at fixed times; read the move's path, timing and easing off those frames with the designer. Author it with `patch_scene`, then contact-sheet your scene at the same times and compare frame by frame. `picsart_media_describe_video` adds a prose read of the clip but **spends credits**, so run it only on the designer's explicit yes |
| Know the valid presets, easings, effects, looks, limits | `picsart_media_get_capabilities` |
| Know the available fonts | `picsart_media_list_fonts` — the built-in catalog plus a live search (`live.fonts`) for a face not in it. Author a text layer's font from that result: a catalog entry's `key`, or a live entry's ready-made `asset` added to `assets[]` with its id in `font.family` — **never a bare CSS family name** ("Inter", "Arial" render empty text) |
| Get the scene JSON schema | `picsart_media_get_scene_schema` |
| Apply / author a motion preset on a layer | `picsart_media_apply_motion_preset` |
| Animate text (type-on, word/char stagger…) | `picsart_media_apply_text_animation` |
| Apply an effect / a look | `picsart_media_apply_effect` / `picsart_media_apply_look` |
| **Reproduce a design's visual treatment** — rounded corners, drop shadow, glow, blurred fill, reflection, color grade, frame/badge — instead of baking it into a PNG or dropping it | **Resolve the exact id from `get_capabilities` first**, then `picsart_media_apply_look` (style bundles: `rounded_corners`, `blur_fill`, `clip_path`, `reflection`…) / `picsart_media_apply_effect` (`drop_shadow`, `gaussian_blur`…). The catalogue is large — **19 looks + 137 effects — so *enumerate* it and match by name/description; don't assume the treatment isn't supported** (see [`mp-scene-vocabulary.md`](mp-scene-vocabulary.md)) |
| Author a **gradient** (fill, stroke, background, or overlay) | `picsart_media_apply_gradient` on an **existing shape layer** that already has geometry (`rect`/`ellipse`/`path`/`polystar`). Colors in `stops` (`#rrggbb`), transparency in a separate `alphaStops` ramp; `linear` or `radial`; re-applying replaces the paint instead of stacking. Stops are static, but the endpoints can be animated afterward. Don't hand-write the `gradientFill` object. For patterns (gradient text, a wash over media, a sweep), see the `gradient-authoring` recipe (`get_recipe`) |
| **Bring a vector icon / logo / line art in as a live shape** (animatable, recolorable, draw-on, no asset, no CSP) instead of an SVG asset | `picsart_media_import_svg_path`: pass each `<path>`'s `d` onto a shape layer. Add `color` (+ `fillRule`, `fillOpacity`) and/or `stroke` + `width` (+ `strokeOpacity`) from that path's own attributes. Call it once per differently-painted path, into the **same** layer so a mark stays one unit. Coordinates come in as the SVG's user units: `viewBox`/`transform` are **not** applied, so scale and place the result with the layer's `transform`. For a **gradient** path, import it with no paint onto a dedicated shape layer, then call `picsart_media_apply_gradient`. Keep the SVG as an uploaded asset only for content paths can't express (filters, masks, embedded images/text), and disclose that |
| **Bring a Figma element's paint over as native items** (its fill, box-shadow, or CSS gradient, as the host's Figma connector reports it) instead of baking it into an SVG/PNG | `picsart_media_import_figma_paint`: `fill` → shape fill, outer `boxShadow` → `drop_shadow`, `gradient` → `gradientFill` (pass the element `size`). `fill`/`gradient` need a shape layer. **Read `skipped`**: an **inset** shadow has no native primitive yet, so keep a bake for that one treatment and **tell the designer** |
| Instantiate a template (montage, title, slide…) | `picsart_media_apply_scene_template` (+ `list_scene_templates` / `describe_scene_template`) |
| **Edit anything already in the scene** — timing, easing, params, position, colour, text, opacity, or a transition on a seam | `picsart_media_patch_scene` (id-anchored → a new `sceneRef`) |
| Validate a scene before rendering | `picsart_media_validate_scene` |
| Show / preview the motion | `picsart_scene_editor` — play the **whole scene built so far** (titled for the current pair) in the browser so the pair is seen in context (free; don't re-export just to see it); `picsart_media_export` for a rendered video / the final deliverable |
| Preview as stills / a strip | `picsart_media_contact_sheet` (a grid), `picsart_media_export` (`mediaType:"png"` + `startTime`) |
| Show the finished motion as a video | `picsart_media_export` — the WHOLE reel, not one pair |
| Bring in a user's file → an asset URL | `picsart_media_upload` (opens the upload widget; the URL arrives on the user's next message) |
| **Generate video footage (SPENDS CREDITS — gated)** | Flow, in order: `picsart_credits` (show balance first) → `picsart_model_catalog` then `picsart_model_choice` (designer picks the model) → `picsart_model_params` (schema) → **`picsart_preflight` (exact dry-run cost, free)** → **quote the cost + get explicit yes** → `picsart_generate` (`async` for video, pass project `folderUid`) → `picsart_render_monitor` (watch) → place the clip as a `media` layer. **No preflight cost shown + no explicit yes = no generate.** Full gate in the `picsart-motion` skill *Video generation*. |

## By user request — the common ones

**This is the skill's core loop.** The designer points at a part and says a small edit —
*"speed this up", "drop the animation from that", "update the easing", "this button has an
extra outline"*. Every one is the same shape: **locate** the target (`picsart_media_query_layout`)
→ **edit** it (`picsart_media_patch_scene`, `set` or `remove`, id-anchored)
→ **validate** (runs inside `patch_scene`) → **show** (the panel or `export`). Never "fix" it
by describing the change or answering from your reading of the image — author it through the tool.

| The designer says… | Do this |
|---|---|
| "make this **faster**" | `query_layout` → `patch_scene` `set` → shorten the animation's **duration** on that layer |
| "**slower** / hold it longer" | `patch_scene` `set` → lengthen the duration or the frame's hold |
| "make it **ease-in-out** / snappier / smoother" | `get_capabilities` for the easing id → `patch_scene` `set` **easing** |
| "**remove** the animation from this / make it static again" | `query_layout` → `patch_scene` **`remove`** the layer's animation (no `path` on the animation entity, or the `animations` field) |
| "this button has an **extra outline** / drop the stroke / border" | `query_layout` (find the layer, then its stroke / outline effect in the scene document) → `patch_scene` **`remove`** that stroke/effect item |
| "**delete / hide** this layer" | `patch_scene` **`remove`** the layer (or `set` its opacity to 0) |
| "**slide** it in from the right / scroll / pop / parallax it" | pick the preset via `get_capabilities` → `apply_motion_preset` (or `patch_scene` to tune an existing one) |
| "type the headline **on** / stagger it in" | `apply_text_animation` |
| "change the **colour / text / opacity / position**" | `patch_scene` `set` (id-anchored, the authored property) |
| "use a **crossfade / slide / cut** at this seam" | `patch_scene` `set` → the seam's `transition` + `transitionDuration` |
| "what **fonts** can I use?" | `picsart_media_list_fonts` (`query` / `family` to narrow; page 1 also live-searches) |
| "how **long** is this clip?" | `picsart_media_probe_media` |
| "**show me** the result / play it" | `picsart_media_export` the WHOLE reel → play the video (or the editor on a pair) |
| "is this **valid** / will it render?" | `picsart_media_validate_scene` |
| "how should I animate this **page transition / button tap / list / modal**?" | the scenario recipe in [`motion-patterns.md`](motion-patterns.md); for sequencing several elements, [`choreography.md`](choreography.md) — then author via `apply_motion_preset` / `patch_scene` (values from `get_capabilities`) |
| "this **feels robotic / too slow / cheap / distracting**" | look up the symptom in [`motion-troubleshooting.md`](motion-troubleshooting.md) → apply the concrete fix through the same locate→edit→show loop |

### Worked example — *"this scroll should be faster and ease-in-out"*

1. `picsart_media_query_layout` — find the scroll layer and read its **current** timing/easing (don't assume which layer or what it is now).
2. `picsart_media_get_capabilities` — the real `ease_in_out` id and the duration/speed bounds (so you write a legal value, not "ease in out").
3. `picsart_media_patch_scene` — on that animation: **shorter duration** (= faster) + **easing `ease_in_out`**. Mints a new `sceneRef`.
4. `picsart_media_validate_scene` — confirm it's valid.
5. **Show** the new scroll moving — view it in `picsart_scene_editor`, or `picsart_media_export` it as a rendered video.

Not: *"it's ~1.2s, I'll make it 0.6s ease-in-out"* in prose and move on. That is the failure.

## Anti-patterns — fabricated facts & hand-built artifacts (the tells)

- Describing layers, coordinates, or fonts from **looking at the image** instead of `query_layout` — an invented fact. (Need exact text ink/glyph positions the layout box doesn't carry? That's not an eyeball case and not a reason to give up — read `absoluteRenderBounds` through the host's Figma connector when it offers a read-only Plugin API read, otherwise measure the glyphs on a `picsart_media_contact_sheet` frame against the exported design via `picsart_view_image`.)
- Inferring **what changed between two frames** by eye instead of running `picsart_media_diff_layouts` (or, as fallback, reading both frames' geometry from `query_layout`).
- **Hand-writing scene JSON** or typing in coordinates instead of `patch_scene` / the apply tools.
- **Naming an easing or preset from memory** instead of `get_capabilities`.
- Deciding the motion (your job) but then **describing it in prose** instead of authoring it through the tool and showing the render — stopping at a description is the failure, not the deciding.
- Proceeding as if you had real data when the tool was never called — or when it wasn't available: then **say so and stop**, don't self-substitute.
- **Asking permission before a free call** — "the render needs your go-ahead", "say go and I'll run it", or any type-a-keyword-to-continue prompt. Free previews and validations run unasked; the designer approves the *shown result*, not the tool call.
