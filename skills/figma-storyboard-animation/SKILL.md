---
name: figma-storyboard-animation
description: Turn a Figma storyboard of static frames into an animated scene — read the frame tree, recover the motion the designer already encoded, then build scene by scene, agreeing each transition before moving on; or build a single frame as a still scene. Use when converting a Figma design or storyboard into video/animation, when a designer hands over frames to "make move", or when the user mentions Figma frames, storyboard, motion design from design, design-to-animation, animating scene to scene, or turning a mockup into a scene. A Figma design made into a finished video starts in animate-design.
metadata:
  version: '1.3'
  ported-from: figma-storyboard-to-scene 1.3 at 55.75.0
user-invocable: false
---

# Figma storyboard → scene motion design

A storyboard is a series of static 1920×1080 frames. Your job is to produce one scene whose
timeline moves between them. Most of the motion is **already in the design** — recover it rather
than invent it.

> **Can't run code?** Everywhere this recipe says "author a generator script", build the scene
> through `picsart_scene_patch` instead and pin the same invariants with
> `picsart_scene_query_layout` after each change (see Commands below). The method is identical — only the
> execution surface differs.

## The flow

1. **Read the tree once** — if the user has shared the storyboard through their Figma connector,
   read the page's frame tree once: it returns every frame, layer, name and box. Everything below is derived from it. Do not walk the board frame by frame to explore.
2. **Plan the beats** — write the beat table down before authoring (below).
3. **Extract each element as its own layer** from the design the user shared: construct editable
   shape geometry from its source measurements and use `picsart_scene_import_figma_paint` for CSS
   fill, shadow or gradient paint on an existing layer. Keep text live. Automatic shape-node
   conversion is not exposed here. Use an image only for an unsupported treatment or a genuinely
   unlayered source; see [extraction](references/figma-extraction.md).
4. **Build the scene from the geometry, and pin every rule.** Where you can run code, author a
   generator script (not hand-written JSON) so each rule becomes an `assert`; where you can't,
   build it through `picsart_scene_patch` and pin the same invariants with
   `picsart_scene_query_layout`. Geometry comes from the metadata, never from eyeballing.
5. **Verify numerically**, then export.

Steps 3–5 run **once per scene**, in order — that loop is the method.

## One static frame

When the ask is a single frame (a still, a store image, a card), there is no storyboard. Skip the
beats and build that frame as a still scene:

1. **Read the selected frame through the user's shared Figma connector.** Its size is `composition.width` and `height`, its fill is
   `composition.background`, and a short `duration` (`1`) is enough.
2. **One layer per child, in paint order** (the tree's first child at the bottom). A layer's
   `position` is its box CENTRE in the frame, `[x + width/2, y + height/2]`: a layer turns and
   scales about its centre. Cross-check one nested child against the frame: some groups store
   children relative to the group ([references/figma-extraction.md](references/figma-extraction.md)).
3. **Each child in the medium that keeps it editable**: author shape geometry, then apply its CSS paint through `picsart_scene_import_figma_paint`,
   text as live text, and each IMAGE fill as a media layer on its original
   bitmap — never the node `export`, which flattens transparency onto the frame's background —
   by its `scaleMode` (`FILL`→`cover`,
   `FIT`→`contain`, `CROP`→`cover` + `crop`, `TILE`→not expressible; the table and the crop maths are
   in [references/figma-extraction.md](references/figma-extraction.md), "Image fills"). Upload each
   image first; a Figma asset URL expires.
4. **A local group that clips or fades as one is usually an inline `composition` layer.** Use a
   scene reference when it is intentionally a reusable, separately owned component.
5. **Verify with numbers, then one full picture.** `picsart_scene_query_layout` at `0`: every `box` within a
   pixel of its Figma box. A top-level image without `crop` carries `drawn`: its box and
   `sourceCrop` as the design shows them. An image inside a group reads `clippedBox`, the part its
   group leaves showing.
   Then one `picsart_scene_contact_sheet` with explicit `times` and `resolution` equal to the composition dimensions: a thumbnail drops 2 px lines and small text.

## Layers, not screens

The scene is a composite of **movable layers**, never a montage of flat screens. A design comes in
as layers; keep them separable so each can move on its own — that is the whole reason for building a
scene rather than cross-fading screenshots.

- **Reconstruct, don't rasterise.** Build editable `shape` geometry from the user-shared design.
  Apply CSS paint to that existing layer with `picsart_scene_import_figma_paint`. Complete Figma
  design-node import is not supported here. Keep corners, paths and placement editable and text live.
  Flattening these into a PNG or SVG prevents independent animation of their parts.
- **When you take assets from a design shared through the user's Figma connector, never take a
  parent frame in place of its children.** The children are what move.
- **Flattening to an image is the fallback only** — for a genuinely un-layered source (a rasterised
  asset, no layer access). When you fall back, say so plainly.
- The "export a node for faithful appearance" habit in
  [references/figma-extraction.md](references/figma-extraction.md) is about fidelity of *one* element
  you have already chosen to bring in whole. Do not generalise it into "raster everything".

## Build scene by scene, in order

This matters more than any individual rule below. Do not author the whole timeline and then present
it. Do not prototype a striking mid-story beat first either: motion designed in the middle has
nothing to be joined to, so it gets thrown away.

Start at the first frame and walk forward. Per scene:

1. **Split by semantic motion units, not just editable layers.** A control, its label and its icon
   normally share one placement owner. Add child-local motion only for a deliberate state change.
   Stillness is useful hierarchy and reading time, not a defect. For grouping, panel growth and
   reflow use linked-element-motion (fetch with `picsart_scene_recipe`, name `linked-element-motion`).
2. **Author its motion by adding to what is already built** — appending to the generator where you
   can run code, patching the same scene where you can't. Never start over: every earlier beat's
   constants and checks stay, so a new beat cannot silently break a settled one.
3. **Render that beat and show it as video** over its own window. Motion cannot be reviewed in a
   still or a contact sheet.
4. **Take direction and re-render.** Expect several passes on one beat. Direction arrives as
   qualities, not numbers — "snappier", "decouple the tiles", "that element makes noise, drop it" —
   and each maps to timing, staggering or element inventory, not to a new design.
5. **Then design the join into the next scene as its own explicit step.** A scene is not done when
   it looks right; it is done when its exit and the next scene's entrance are agreed. The join is
   the part the storyboard does *not* contain, so it is where direction is most specific ("zoom out,
   then the next scene arrives *from the camera*, not zoomed in") and where guessing wastes most.

When autonomous iteration is authorized, use these as internal verification gates and show meaningful
milestones rather than requesting approval for every beat. For large timelines, use
large-scene-assembly (fetch with `picsart_scene_recipe`, name `large-scene-assembly`) to keep components independently editable.

Only then move on. Keep the beat table updated as you go — it is the record of what was agreed, and
the timeline is long before the build is finished.

## Read the storyboard

- **Canvas x-order is temporal order.** Frames are laid left to right; sort by `x`, not by name.
- **Frame names lie; the order doesn't.** Duplicate names are common (a designer duplicates a
  frame and forgets to renumber). Count frames against numbers before concluding one is missing.
- **Duplicate-named frames are usually A→B poses of one beat.** Diff their layer sets: same
  children, different transforms means the designer encoded the motion as a delta. That motion is
  **measurable**, not a design decision you have to make.
- When the design comes through the user's Figma connector, capture frames one at a time: a whole
  board captured at once is far wider than it is tall and shrinks to a sliver.

What is genuinely yours to design: dwell, easing, and the joins between unpaired frames.

For each unpaired join, use motion-scene-continuity (fetch with `picsart_scene_recipe`, name `motion-scene-continuity`) to name the
semantic relationship and choose persistent layer, catalog transition, hard cut, crossfade, or
custom transition before writing mechanics. This storyboard workflow still owns recovery of motion
implied by paired design frames; continuity owns only the relationship and representation at their
boundaries.

## Solve transforms, don't choose them

A uniform scale `s` about an unknown pivot `C` maps `p → C + s(p − C)`. So **one corresponding
coordinate pair pins the pivot**:

```
C = (p2 − s·p1) / (1 − s)
```

Take `s` from any element's size ratio between the two frames, solve `C`, then **check it against
a second, independent element**. Agreement to a fraction of a pixel means you have the designer's
actual transform; disagreement means the element moved on its own and needs its own treatment.

Write the beat table down — measured deltas, the solved pivot, the time allocation.
Nine beats of choreography with numbers will not survive scrollback, and you will want to diff it
against renders.

## Motion rules

Full detail and worked numbers: [references/motion-rules.md](references/motion-rules.md). The
rules that decide whether a beat reads correctly:

- **Rigid vs independent.** Stagger position/scale only for genuinely *independent* objects (grid
  tiles, stickers). A card, a lockup, or any object with parts must share **one** geometry clock,
  or its parts drift out of register mid-flight. Put the stagger on the fade instead.
- **A fade must be co-terminous with its motion** to read as one gesture. If the fade finishes
  before the move does, the eye sees two events. Match the easing curves too.
- **On a flat frame render, a zoom-in is safe; a translate is not.** Scaling up never exposes an
  edge; translating exposes the image's own trailing edge.
- **Size entry travel** so the leading part starts just off-canvas — travel `≥ canvas − leftmost_x`.
  Too little and it begins on screen; far too much is dead time.
- **Exits accelerate** (`ease_in`). Give two objects different spans for differential acceleration.
- **Selection chrome is exclusive** — never two marquees at once, and it must not outlive its beat.
  If element steps overlap their spans, an element loses its selection mid-manipulation.

## Rendering facts that change the authoring

- **Opacity composites in linear light.** It does not scale the encoded sRGB value. To hit a
  measured brightness, convert through gamma: `opacity = linear(target) / linear(source)`.
- **Opacity is only a *darkness* control over a black background.** Over a light backdrop it
  makes a dark subject *lighter* as the backdrop bleeds through. A real dim there needs a dark
  scrim on top, not opacity on the subject.
- **`anchor` gives a non-centre pivot** (layer-local pixels from the layer's top-left). Use it for
  corner-pivot scaling — e.g. scaling about a selection box's top-left so it reads as dragging the
  bottom-right handle. Do not fake pivots with position keyframes.
- **Per-character text animation is built in.** A text layer's `content.animations[]` is an After Effects
  animator + range selector: `basedOn: "character"`, plus `randomizeOrder`/`randomizeSeed` for
  flicker. Stack entries on different seeds so they don't beat in lockstep. The active span is
  `[start + offset, end + offset]`: a narrow window parks its far edge at the text's end at
  `offset: 1 − end`, or clears every glyph at `offset: 1 − start` (`1 − w` / `1` only when `start`
  is 0 — don't use them otherwise). A FULL window (`start:0,end:1`) with a ramp shape is instead
  one ramp exactly as wide as the text: sweep `offset` `-1 → 1` and each glyph eases over half the
  sweep, staggered by position rather than switching all at once — see
  `textAnimationAuthoring.rawSelector` in `picsart_scene_capabilities` for the worked numbers.
- **Inline SVG must be url-encoded with `#` percent-encoded.** A raw `#` starts a URI fragment and
  truncates the SVG at its first hex colour.
- **Measure easing, don't trust preset names.** Sample the value at 25%/75% of a keyframe window
  and confirm the curve is what you intended.

## Verify numerically

Eyeballing a downscaled contact sheet will produce false alarms — it reliably reports position
errors that measurement disproves. Compare frames at full resolution, or measure.

- `picsart_scene_validate` checks structure only. It passes on a scene whose layers render nothing.
- `picsart_scene_query_layout` resolves boxes without rendering — use it to confirm geometry against the
  Figma numbers before spending a render. It is geometry-only: a resolved box says nothing about
  whether the content decodes.
- To find gaps where nothing is on canvas, look at the suspect times with `picsart_scene_contact_sheet` with `times: [t1, t2, …]` and `resolution` set to the scene's `composition.width` and `composition.height`.
  A frame holding only a small logo can look empty at a glance — check it before calling it a gap.
- Where you can run code, put the invariants in the **generator** as asserts (solved pivots agreeing, travel long enough,
  one selection at a time, bounds sane). They catch regressions that a still frame hides.

## Commands

Where you can run code, maintain the same generator and self-checks. Otherwise use bounded `picsart_scene_patch` edits. Validate with `picsart_scene_validate`, query event geometry with `picsart_scene_query_layout`, and inspect full-resolution stills using `picsart_scene_contact_sheet` with `times: [t1, t2]` (at most 8 times per call) and `resolution` set to the scene's `composition.width` and `composition.height`. Inspect continuous exported video for motion claims.

Without the generator you lose its `assert`s, so pin each invariant explicitly with `picsart_scene_query_layout`
after every `picsart_scene_patch` — solved pivots agreeing, entry travel long enough, one selection at a
time, bounds sane.

Each `picsart_scene_patch` returns the patched scene as `scene`: pass that as `scene` to the next
patch, query, contact sheet or translate.
