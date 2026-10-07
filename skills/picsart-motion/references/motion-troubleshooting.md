# Motion troubleshooting — symptom → cause → fix

When the designer says a pair "feels off," this maps the symptom to a concrete fix. It plugs into
the edit loop: **locate** the layer via `picsart_media_query_layout` → **apply** the fix via
`picsart_media_patch_scene` (or the `apply_*` tools) → **show** the re-rendered result. Never
"fix" it by describing the change; author it and show it. Easing/preset values come from
`get_capabilities`.

## "Feels robotic"
- Linear easing on spatial movement → use ease-out (entrance) / ease-in-out (on-screen).
- Straight path → add a 10–20px arc at the midpoint.
- Uniform timing → stagger siblings 50–100ms.
- Everything synced → offset starts/stops 50–150ms.
- No secondary motion → add a shadow, icon reaction, or subtle ambient.

## "Too slow"
- Duration over the element's budget → check the duration ranges (`motion-principles.md` §3 / `motion-patterns.md`).
- ease-in-out where ease-out would do → ease-out feels faster.
- Too much anticipation → reduce to ~10% or remove.
- Stagger cascade too long → keep total <500ms.

## "Too fast / jarring"
- Below the minimum → modals 300ms+, page/screen transitions 400ms+.
- No easing → add ease-out at minimum.
- No resolution → add a 50–100ms settle at the end.
- Large move with no wind-up → add 100–200ms anticipation.

## "Feels cheap / flat"
- Only the primary moves → add a secondary (and ambient if it fits).
- Opacity-only → combine with position or scale.
- Same easing everywhere → vary primary vs secondary.
- No follow-through → child elements trail 50–150ms.
- No overshoot → add 3–10% (only in a playful/energetic register).

## "Too distracting"
- Too many things moving → the ⅓ rule (max ⅓ of elements active at once).
- Amplitude too large → reduce to the minimum that reads.
- Competing focal points → one focal element per beat; dim the rest.
- Ambient too prominent → keep it under ~20% of the primary motion's energy, and slower.
- No breathing room → 100–200ms pause between beats.

## "No personality / inconsistent"
- Default easing everywhere → apply the reel's personality register (`motion-principles.md` §6).
- Durations vary for the same element type → use the personality's duration range consistently.
- Entrance direction changes shot to shot → pick one origin and keep it.
- Mixed archetypes → commit to one for 90%+ of the reel.

## "Dropped frames / heavy"
- Animating width/height/margin → animate transform (position/scale) instead.
- Too many animated elements → keep under ~20 per frame.
- Heavy shadows/filters → simplify or pre-render.
- Everything firing at once → stagger to spread the load.

## "Content shows through a header / overlay" (occlusion)
A layer meant to *cover* moving content (sticky header, modal backdrop, overlay) but content is visible through it:
- **Covering layer is semi-transparent** (a gradient / low-opacity fill) → it overlaps but doesn't occlude → add an **opaque `color` backing** behind it (over the content, under the header text) so the content is fully hidden; keep the gradient only as a soft edge.
- **Wrong z-order** → the cover must be *above* the content it hides (later in `layers[]`).
- **Header band too short** → its opaque zone must span the full header height, not just behind the first line.
- **Verify at the *deepest* overlap** → check a `contact_sheet` frame when content is fully scrolled *under* the cover, not at the start — the leak only appears once content moves behind it.
- **Run `layout_lint` first — it catches most of this cheaply:** it flags overlapping boxes over time and is z-order aware, so it *will* surface a wrong-z-order cover or a box that shouldn't overlap. Its one blind spot is opacity: a *semi-transparent* leak reads as an intentional overlap and isn't flagged. So lint first, then verify occlusion on a rendered frame for the transparency case — the frame check is the follow-up, not the substitute.

## "A layer is blank in the preview — but the scene validates (and export looks fine)"
The asset is blocked in the **browser preview**, even though `validate_scene` passes and server-side
`contact_sheet`/`export` render it (**validates ≠ works; server ≠ browser preview**):
- **A `figma.com` asset** → the asset `uri` is a `figma.com` URL, which the browser preview blocks. For an icon/logo, the better fix is to **drop the asset**: convert its paths into a live shape with `picsart_media_import_svg_path` (no URL, so nothing to block). Otherwise **lift it to a Picsart-hosted URL** (`picsart_drive` `action: "upload"` with the URL) and author the URL it returns.
- **A `blob:` asset** → the asset `uri` is a `blob:` object URL (a transient browser handle, never a valid scene asset). **Upload the underlying file** (`picsart_media_upload`) and author the Picsart-hosted URL it returns.
- **base64 `data:` URI** → same story: blocked/unsupported in the preview (esp. SVG). Use a Picsart-hosted URL, not `data:`.
- **`file://` or an expired short-lived link** → lift to a durable Picsart-hosted URL.
- **Font by a bare CSS family name** → text renders empty; author a font from `picsart_media_list_fonts` (see `stage-2-compose.md`).
- **Fix ONLY the affected asset — never flatten to dodge CSP.** Re-host that one image (or convert an unsupported vector to a raster *for that element alone*); do **not** rasterize the card, component, or screen it lives in. Flattening to make the CSP error disappear destroys the layering — it's a wrong ad, not a fix. And never rasterize a shape or live text for CSP: those are authored, not uploaded.
- **Don't trust `contact_sheet`/`export` here** — they're server-side and won't reproduce the browser CSP block. Verify in the editor preview, or just use Picsart-hosted URLs everywhere so it works in both.

## "Engine failed to boot: content kind X has no component"
The scene uses a layer `content.kind` the **browser player has no component for** (`composition`
is the usual case), while the server render path considers it valid — so `validate_scene` passes and
server-side `contact_sheet`/`export` render it (**validation ≠ boot**, the same class of gap as
fonts-by-name). It is a **render-path gap**: the server renders the kind, the browser player doesn't.
- **Do now:** the export/still fallback is correct — show the exported result and keep working.
- **Author around it:** for editor-bound scenes prefer a kind the browser surface renders
  (`media`, `text`, `color`, `empty`, `shape`, `scene_ref`) — a nested `composition` usually
  restructures into an `empty` rig with parented children (same visual, and the rig still scales its
  children together for a zoom). This is the reliable path.

## "The rebuilt frame matches the design but nothing animates per-element / it's basically an image"
The frame was **rasterized** — composed from one whole-frame screenshot (or a few big group slabs)
instead of per-node layers. A slab can only fade/scale as a whole, so no element moves independently:
that's a slideshow, not motion design.
- **Cause:** took an image export of the frame/group as the layer — usually because the per-node tree
  wasn't fetched (or was skipped when metadata "looked empty"), so the screenshot was the easy path.
- **Fix:** throw the slab out. Fetch **this frame's full layer tree** (you only hold one or two
  frames — you can afford all of it) and rebuild: **each design node = its own scene layer**, authored
  as its native kind (text→`text`, rects/cards/borders/circles→`shape`, icons/logos→vector, only true
  photos/video→raster). **Definition of done:** the scene's layer count ≈ the design frame's node
  count. One media layer covering the frame = failed, redo. (Hard gate: `stage-2-compose.md` Stage 2.)
- **Never rasterize to fix CSP** — re-host the one affected asset, don't flatten (see above).

## "It looked right in the stills but wrong when it played" (stills ≠ editor)
The still renderer (`contact_sheet`/`export` with `mediaType:"png"`) and the browser editor **do not draw
some things the same way**, so a move that looks correct frame-by-frame can be wrong in motion:
- **The editor is the ONLY proof of MOTION.** Stills are fine for the Stage-2 *position* render-match
  (a frozen layout vs the Figma frame), but **motion correctness — overlap during an animation,
  timing, z-order while things move — is judged in `picsart_scene_editor`, never from stills.**
  Approve a pair on the played editor, not a contact sheet.
- **Known divergence:** a **photo scaling in from its left edge** (edge-anchored scale)
  can look correct in stills but **overlap a sibling line** in the editor. If a move reads clean in
  stills, don't trust it — watch it play in the editor. (For the connector/line case, the fix is to **fade the arriving
  photo in rather than scale it**, and put the connector *below* the photo — [`transitions.md`](transitions.md)
  §"Recipe — the connected-canvas rig".)
- Also render-path-only, already covered above: **CSP-blocked assets** and **`composition`/`track`
  content kinds** render server-side (stills/export) but blank or fail to boot in the editor — same
  lesson, the editor is authoritative for what the designer will actually see.

## Quick diagnostic (run before approving a pair)
No linear on spatial motion · duration matches the element type · a primary + at least a secondary
where it helps · consistent personality · directional easing correct · no move >⅓ screen without an
intermediate keyframe · ≤⅓ of elements active at once · follow-through present · every motion has a
purpose · still holds up on the 100th viewing.
