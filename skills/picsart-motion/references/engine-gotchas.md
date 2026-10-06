# Engine gotchas (MP Scene) — silent, visible bugs

Read before composing the first frame and again when a render "looks slightly wrong" with no
validation error.

## Opacity & colour
- **Figma layer opacity → scene opacity is sRGB→linear:** `lin = ((a + 0.055) / 1.055) ** 2.4`.
  Figma 20% → **0.0331**, 15% → 0.0196. Authoring Figma's raw value renders dimmed items far
  too bright. Confirm against the side-by-side render-match — the compare catches it either way.
- **Opacity on a composition hosting masked children is not honoured** — put the opacity on the
  leaf layers instead.
- **Shape paint colours carry no alpha** (`#rrggbb` only); transparency goes in the paint item's
  own `opacity` (an `#rrggbbaa` alpha byte is dropped).

## Timing
- **Children of a nested composition run on the parent's LOCAL clock** (t = 0 at the parent's
  `start`). Subtract the parent's start from global times. Shape-item keyframes (e.g. `trim.end`)
  are local too.
- Top-level layers' own keyframes use composition (global) time.
- Give leaving compositions a `duration` so they stop rendering after their exit.

## Transform channels
- **One track per channel per layer.** Two scale animations (a pop-in plus a tap, or two
  presets touching scale) must be merged into one keyframe list — or one of them moved to another
  channel (make the entrance a fade/slide instead).
- In a `transforms` stack, put `translation` **after** `scale`.
- Collapsed compositions: set `anchor` and `position` explicitly (both = the pivot) **before**
  animating scale — this is what makes "zoom toward the T-shirt tile" land on the T-shirt tile.
- **To pivot a SHAPE, set the shape GROUP-ITEM's `anchor` — NOT the layer's `transform.anchor`.** A
  layer-level `transform.anchor` on a shape is **rejected** (a shape has no resolution box to
  normalize the anchor against). The **supported, animatable** pivot is
  **`MpShapeGroupItem.anchor`** ("Pivot for rotation/scale, content-local px, default `[0,0]`") —
  wrap the geometry in a group and set that group's `anchor` (+ `position`).
- **`text` also rejects a layer `transform.anchor`** — the validator flags it
  (`text_anchor_unsupported`); text renders centre-anchored around its `position`. Only
  `media`/`color`/comps honour an arbitrary layer-level anchor (`authoring-flow.md`'s anchor guidance
  isn't universal — shape and text are the exceptions).
- Avoid scale exactly 0 — start pops at ≥ 0.3 with opacity 0.

## Camera & presets (resolve from `get_capabilities` — `appliesTo` matters)
- **A pan-only `composition.camera` is a NO-OP in the scene player** — a `position` change with `zoom`
  unchanged moves nothing. Camera **zoom** works; a pure **pan** does not. For a pan (e.g. a viewport
  travelling a drawing line), use the **empty-"world"-layer rig**: parent everything to one `empty`
  layer and animate *its* `position` so the world slides under a fixed viewport (recipe:
  [`transitions.md`](transitions.md) §"Recipe — the connected-canvas rig").
- **`fade_in` does NOT apply to `shape` layers** (its `appliesTo` is `text`/`media`/`color`/`scene_ref`
  in `get_capabilities`) — applying it to a shape does nothing. **Fade a shape with `opacity` keyframes**
  instead; `glow_pulse` and `tap_pulse` *do* list `shape`. Check any preset's `appliesTo` before
  authoring — the set differs per preset.
- **A trim-path draws from the path's FIRST vertex.** If a stroke draws backwards, the vertex order is
  reversed — fix the path's point order, don't flip the trim direction blind.

## Geometry from Figma
- Figma rotation is CCW-positive; scene rotation is CW-positive → **negate**.
- **Figma blur radius → engine blur ≈ 0.4×** (a Figma layer/gaussian blur of **60** ≈ an engine
  blur of **24**). Scale by ~0.4 as a starting point, then confirm on the
  side-by-side render-match (same as the opacity conversion — don't author Figma's raw value).
- Left-aligned text: x = box left edge; y = line-box centre.
- Stroke align INSIDE in Figma: inset the stroke rect by width/2 (and the radius by width/2).
- `gradientTransform [[0,1,0],[-1,0,1]]` = vertical gradient, stop 0 at top.
- Shape items paint with **index 0 on top**: for a stroke over a fill, list the stroke group first.
- Modifiers go after the path and before the paint: `[rect, trim, stroke]`.

## The smart-animate zoom, exactly (frame B = frame A transformed)
From ONE matched element: `s = wB/wA`, `tx = xB − s·xA`, `ty = yB − s·yA`, fixed point
`F = (tx/(1−s), ty/(1−s))`. Set the parent comp's `anchor = position = F`, animate scale
`1 → s` (~0.75 s, house curve). **Check two more matched elements land within ~1 px** — if they
do, B *is* A zoomed and the pair is one continuous camera move, never a cut. Rasters get upscaled
by `s` — export them at ≥ s× resolution when B is a big zoom.

## One house curve
All large moves (zoom, push, draw-on) share **one** easing — `cubic_bezier(0.65, 0, 0.2, 1)` —
so the film feels like one system. Small entrances use `ease_out`; presets keep their own easings.

## Scene editing
- Structural `remove` acts on top-level layers; for nested ones use
  `{op:"remove", layer:<parent>, path:"content/layers/<index>"}`.
- Mask layers are addressed through their owner: `layer: <owner_id>, path: "mask/layer/..."`.
- Validate/render with a trimmed scene (only the layers alive in the window) to keep payloads small.
- **Payload grows with the reel** — the whole scene document gets heavy as frames accumulate, and
  every edit re-sends it. Keep the working scene trimmed (only the layers alive in the window you
  are checking) so each call stays small.

## Invented layers — don't (by default)
Express motion by transforming and fading **layers that exist in Figma**. No invented cursors,
ripples, glows, shade overlays or helper shapes — designers notice immediately and it breaks trust
in the file. A *press* is the **`tap_pulse` preset** — `apply_motion_preset("tap_pulse")`, a
real preset (a one-shot dip to ~0.92 and back, with an
`at` param for *when* it fires mid-shot), `appliesTo` **includes `shape`** — applied to **every piece
of the pressed element** (content, mask, outline — same anchor), not a dot drawn on top. Add a
visible tap-dot/cursor only when the designer asks for one or the design language already contains it.
**(Still resolve it from `get_capabilities`, and only if it isn't listed there fall back to
`scale_pop` + `opacity` keyframes.)**
