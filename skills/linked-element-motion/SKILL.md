---
name: linked-element-motion
description: Keep related scene elements aligned and moving together, including container resizing, shared fades, content reveals and sibling reflow. Use when labels detach, companions fade separately, panels fail to grow, content overflows, or an outside object must join a template at a particular time and remain attached.
metadata:
  category: authoring
  version: '1.7'
  ported-from: layout-choreography 1.7 at 55.75.0
user-invocable: false
---

# Layout relationships through motion

Served checks: `picsart_scene_check_contracts` runs contract records and reusable templates, `picsart_scene_check_motion` runs frame-complete motion records, and `picsart_scene_inspect` pages large sources; the one remaining limit is that pixel records have no automated checker, so inspect full-resolution rendered frames for them.

Editable layers are not necessarily independent motion units. Before animating, state which things
belong together, which may change internally, and what must make room when new content appears.

## Construct the relationship before checking it

Choose the construction from how long the relationship must hold:

- **Always one motion unit:** put the plate, label and icon in one composition/scene reference;
  animate that owner once. Leave children in local coordinates. Use `parentId` for transform-only
  ownership when appropriate; it does not inherit opacity or lifetime. A shared fade belongs on
  the enclosing composition owner. Do not copy the same travel/press/exit tracks onto every child.
- **Always one layout rule:** declare shared width, height, padding and offsets, then derive the
  backing size and child placement from them. In a parameterized scene, use `$eval` expressions
  such as `height / 2` for the label center as well as the backing center. Resizing an instance
  then changes one binding instead of several unrelated coordinates. `$eval` resolves parameters;
  it is not a per-frame read of another layer's animated geometry.
- **A property follows another each frame:** use the supported Lua property-read API when the
  dependency is needed and a common owner is insufficient. Fetch `scene-animation-reference` for syntax,
  scope, coordinate and clock limits. Keep the dependency one-way; do not invent reactive fields
  or use another layer's local placement as if it were a root-space painted center.
- **Related only during a phase:** keep intentional independent motion, derive the attached phase
  from one path/progress source, and declare when it releases. Use time-windowed contracts for
  those phases and inspect the handoff. Static parenting is not an animated reparenting switch.

Contracts verify the construction; they do not create the relationship. For a simple rigid widget,
prefer one owner and a shared sizing formula over independent tracks plus many corrective checks.
Still verify initial layout, realistic parameter edits and the final painted result: parenting can
preserve an incorrect offset, and a shared formula can encode the wrong design.

## Assign motion and layout ownership

| Relationship | Authoring choice | Evidence |
|---|---|---|
| Panel + label + icon travel together | One inline composition or supported parent rig; common transform on the owner | Constant relative offsets during translation; inspect scale/rotation separately |
| Badge enters inside a moving card | Common card placement plus deliberate badge-local entrance | Card trajectory plus badge's local event window |
| Panel grows for another row | Animate panel geometry independently from text; move following rows/siblings explicitly | Fixed edge, attached gaps and padded containment throughout resize |
| Whole unit changes scale | Scale the semantic group intentionally | Text, stroke and corner appearance in rendered frames |
| Same object crosses a scene boundary | Keep the owner alive across the seam | Presence window and continuous video |
| Label on a plane in depth | Label is a child of the plane by `parentId`, no `z` of its own; titles over the scene are `cameraExempt: true` roots | `picsart_scene_lint_layout`: the label absent from `covered`, `order` on `depth`/`y` for the planes; rendered frame at the held camera: label on its plane, in front of it |

Record a component's common owner, members, entry/exit window and deliberate local exceptions
before animating. A local badge reveal can differ; a whole-card exit belongs to the owner. Derive
checks from this intent, not only from the final tracks: copied mistakes should not define success.

Grouping is a transform/ownership mechanism, **not an automatic content-sized layout solver**.
scene does not infer “this label belongs to that box” from spatial proximity. A validator accepting
independent layers does not mean they obey the designer's relationship. Do not invent a CSS auto-layout
field or duplicate identical keyframes on every child as the default substitute for a common owner.

Read the current `composition`, `parentId` and transform schema before building a rig. Child coordinates
must be authored in the chosen owner's space; use a query to confirm the first child before copying
the pattern. Use stable ids and query-returned composition scopes for repeated instances.
For a sized inline composition, its width/height define its own raster, not necessarily its drawn
size in the host. Use explicit bounds or `fit: "none"` when it should draw at its own size; otherwise
default fitting can enlarge the whole card. Validate and query this before adding motion.

For a join between an outside object and a template, query the assembled host at the intended
root-time event before writing the approach. The existing destination can be measured before the
source exists. Use root geometry to derive the missing object's placement in its own parent space,
then re-query both; one snapshot does not create persistent following. Fetch `scene-template-remix`
and its **content replacement and template handoffs** reference for content replacement, clock/space conversion,
post-arrival ownership and same-time versus cross-time checks.

## Plan resize and reveal as one event

1. Name the event and its time: “the details row appears and the panel makes room.” Record old and new
   content extents, padding, minimum readable area, and which edge stays fixed.
2. Choose behavior: reserve space from the start, resize before/during reveal, or deliberately clip/scroll.
   These are different designs. Never make accidental clipping masquerade as a reveal.
3. Measure final text using the actual font and wrap width; use `picsart_scene_query_layout`, not character count.
   Calculate required container extent from visible child bounds + padding in a consistent space.
4. Author a shared progress/timing schedule for background size, sibling reflow and reveal. With a fixed
   top edge, a height increase of Δh needs a center shift of Δh/2. With centered growth, no shift is needed.
   Animate the supported shape geometry or the background's own scale/position, not the text-bearing
   group, unless scaling the text is intended. Background scaling can distort corners/strokes—inspect it.
5. Reveal only when there is room at **every relevant intermediate time**. Matching end states is not
   enough: different easing curves can make content overtake the growing panel. Keep readable holds.
6. Recompute after text, font, padding, duration or component-size edits. Do not promise automatic reflow
   from one hard-coded demonstration.

## Declare what the tooling should check

### Translate design intent into assertions

For each intended relationship, record **targets, expected relation, phase/root times, tolerance,
assertion and uncovered visual evidence**. Choose these from the design before using the measured
result as evidence. An unasserted relationship remains unchecked even when every existing contract
passes. A centered label needs alignment checks as well as containment; constant relative motion
can preserve an initially wrong offset.

For buttons, chips, labels and icons, read [UI alignment contracts](references/ui-alignment.md).
Through MCP, fetch `picsart_scene_recipe` with `name:"linked-element-motion"` and
`reference:"references/ui-alignment.md"`. It contains a runnable example and a deliberately
misaligned negative control, plus guidance for moving, resized and nested controls. Use one
representative negative control when introducing a new relationship check; do not change the
expected values to make the broken variant pass.

### Relationships that change over time

Hierarchy expresses ownership; a contract expresses intent during a chosen interval. A badge can
stay in one card, travel freely, then belong visually to another card without dynamic reparenting.
Write the intended phases and exceptions before keyframes. Map those semantic roles to actual query
ids/scopes after assembly. Do not derive the expected result from the tracks being tested.

For repeatable validation, keep a separate JSON sidecar as a record of independent design intent, not an extra scene field. The following record for `source`, `destination` and `badge` runs with `picsart_scene_check_contracts`; read pass, fail or inconclusive per contract and report any unexecuted assertions as unchecked.

```json
{
  "version": 1,
  "timeSpace": "root",
  "contracts": [
    {
      "id": "before-transfer",
      "description": "Badge stays in source until departure; 2–3s is independent travel.",
      "window": { "start": 0, "end": 2, "step": 0.1 },
      "assert": { "kind": "contains", "anchor": { "id": "source" }, "members": [{ "id": "badge" }], "paddingPx": 12 }
    },
    {
      "id": "after-transfer",
      "window": { "start": 3, "end": 5, "step": 0.1 },
      "assert": { "kind": "contains", "anchor": { "id": "destination" }, "members": [{ "id": "badge" }], "paddingPx": 12 }
    },
    {
      "id": "arrival-carrier",
      "boundary": { "at": 3, "delta": 0.03333333333333333 },
      "assert": { "kind": "present", "members": [{ "id": "badge" }] }
    }
  ]
}
```

Each contract has a stable id, one assertion and an explicit root-time schedule. Window ends are exclusive; boundary observations include before, exactly at, and after the event. A cross-time handoff compares separately chosen moments; see `motion-scene-continuity` for the intended geometry and limits. Retiming requires rebasing all relevant windows. For reusable expected values and affine clock mapping, read [reusable contracts](references/reusable-contracts.md). `picsart_scene_check_contracts` runs these documents directly, or resolves a reusable `template` with `targets`, `numbers` and optional `clock` and returns the `resolved` document beside the verdicts. Query comparisons outside its vocabulary explicitly without presenting them as checker verdicts.

Use `present` if a member must exist, not only `contains`: containment can legitimately skip a member
outside its lifetime. `co_presence` checks intended joint geometric lifetime, not visual opacity.
`translation` requires fixed sizes/rotations; `contains` can check explicitly resizing unrotated boxes.
During a free-travel phase, omitting containment is deliberate **unchecked coverage**, not proof the
path is safe. Add a presence contract if disappearance must be caught during that travel.

Read each named verdict, requested `sampleTimes`, `issues` and failure `evidence` (expected assertion
plus observed member/anchor geometry). The top-level `sampleTimes` lists actually queried times.
Outside-scene requested samples produce `inconclusive`, not a clipped pass; a measured violation
still produces `fail`. `maxErrorPx:0` does not mean a presence assertion passed. Missing/ambiguous
geometry is not evidence of correctness. Hashes identify supplied JSON, not remote media contents.

Read `coverage` as a scope inventory. Its target `checks` say which assertion kinds/channels were
requested; `resolvedSamples` only means a unique target was found, not that it passed all geometry
or motion checks. `observedUntargetedLayers` names returned non-internal layers never explicitly
targeted, including children whose owner alone was checked. Review these against the intended
relationships; decorative layers need not all acquire contracts. Missing/ambiguous/unavailable
counts, omission counts and unchecked intervals belong in the handoff. There is no whole-scene
coverage percentage, and no proof between sampled times.

Keep all intended relationships in the handoff, split by meaningful beats. A successful tool call is not proof that its checks passed: read each available result and distinguish pass, fail and inconclusive evidence. Do not invent a contract report; report the verdicts `picsart_scene_check_contracts` returned.

### Reading a `picsart_scene_query_layout` report

One moment, one report. What its fields do and do not say:

- **Opacity.** `opacity` is the layer's evaluated opacity; `effectiveOpacity` multiplies it
  through enclosing compositions, not transform-only `parentId` links. Neither is painted alpha.
  An absent value means the build could not evaluate it, not that the layer is opaque.
- **Ids.** Every id is a `picsart_scene_patch` layer address, except layers inside a referenced
  scene (edit them through `scope`) and `internal: true` implementation layers. Named track and
  mask clips keep their own id; other nested children are `host__child`.
- **Activity.** An inactive layer has `active: false` and no box, but held content can keep its
  geometry while inactive. Audio `volume` is in percent.
- **Bounds** are conservative layer geometry, not painted pixels: transparent shape branches
  still count. Degenerate boxes come with a note.
- **Perspective.** A layer drawn through its composition's perspective camera reports `quad`
  (its four projected corners, top-left first in its own corner order), `box`/`aabb` as their
  envelope, the projected center and `depth`, and no `rotationDeg`; `onCanvas` reads the envelope.
  A layer reaching the camera's eye has no geometry and is noted. A composition in depth paints
  far to near, so `zIndex` follows depth there.
- The query may fetch referenced scenes, fonts and caption transcripts through guarded
  public-URL reads; it saves no report file. It certifies no effects, assets or codecs: look at
  rendered frames before export.

### One-off checks and collision scanning

After `picsart_scene_validate`, get actual ids/scopes with `picsart_scene_query_layout`. Then call `picsart_scene_lint_layout`
with the scene, a narrow `t0`/`t1` window, a useful `step`, and explicit relationships, for example:

```json
{
  "t0": 0.8,
  "t1": 1.8,
  "step": 0.03333333333333333,
  "relationships": [
    { "kind": "present", "members": [{ "id": "card" }] },
    { "kind": "co_presence", "anchor": { "id": "card" }, "members": [{ "id": "label" }] },
    { "kind": "translation", "anchor": { "id": "card" }, "members": [{ "id": "label" }], "tolerancePx": 1 },
    { "kind": "contains", "anchor": { "id": "panel-bg" }, "members": [{ "id": "new-row" }], "paddingPx": 16 }
  ]
}
```

These are alternatives for appropriate targets/windows, not a requirement that a growing panel also
passes the translation check. `translation` only measures constant relative center offsets with
unchanged sizes/rotations; resizing or rotating rigs are **inconclusive**, not broken by definition.
`contains` uses unclipped unrotated boxes so a clip cannot hide overflow. `present` requires geometric
presence at each sample; `co_presence` compares member/anchor geometric presence, catching different
lifetimes or departures. Use the latter only in a window where simultaneous presence is intended;
exclude deliberate local entrances. At least one jointly present sample is required per member.
Neither check measures opacity: a fully faded layer may still have geometry and `visible:true`.
For a shared fade, put opacity on the common composition owner and inspect child-local exceptions.
Transform-only `parentId` links do not propagate opacity. Add `composition` for ambiguous ids.
Missing geometry is inconclusive; a never-measured member cannot pass.

### Matching fades, separately from presence

When companions should have the **same evaluated layer opacity** during a shared event, add this
assertion to a named contract's window (or to a one-off lint call):

```json
{ "kind": "opacity_match", "anchor": { "id": "card__background" }, "members": [{ "id": "card__label" }], "toleranceOpacity": 0.01 }
```

It compares `effectiveOpacity`: evaluated layer opacity multiplied through enclosing compositions,
not transform-only parents. Query reports also expose local `opacity`, so a mismatch can be traced
to an owner or a child-local fade. Use equal-opacity companions; a deliberately translucent label
or independent reveal should not be constrained to match its opaque background. Scope the check to
the shared event rather than suppressing an intentional earlier difference with a large tolerance.

Read `maxErrorOpacity` and timestamped evidence, not `maxErrorPx`. Tolerance is an absolute opacity
difference (default 0.01), not pixels or a timing tolerance. Missing evaluated opacity—older query
builds or an unavailable layer state—makes the check inconclusive, never implicitly opaque or zero.
Two zeros match: this check alone does not require visible content or prove a desired fade happened.
Pair it with the declared geometric lifetime checks and inspect the fade window in a preview.
Masks, source alpha, effects, occlusion and missing decoded media can still change painted visibility.

### Fixed edges and attached content during resize

Containment alone can pass while a panel's fixed edge drifts or an internal gap grows incorrectly.
Do not use `translation` on a growing panel: it requires unchanged sizes. Instead declare expected
edges/gaps from the design, not from the first measured frame. This complete sidecar assumes a
panel whose top must stay at root y=40 and a footer whose top follows 12 px below its bottom:

```json
{
  "version": 1,
  "timeSpace": "root",
  "contracts": [
    {
      "id": "panel-fixed-top",
      "window": { "start": 0, "end": 2.1, "step": 0.1 },
      "assert": { "kind": "fixed_edge", "members": [{ "id": "panel" }], "edge": "top", "valuePx": 40, "tolerancePx": 1 }
    },
    {
      "id": "footer-follows-growth",
      "window": { "start": 0, "end": 2.1, "step": 0.1 },
      "assert": { "kind": "edge_attachment", "anchor": { "id": "panel" }, "members": [{ "id": "footer" }], "edge": "top", "anchorEdge": "bottom", "gapPx": 12, "tolerancePx": 1 }
    }
  ]
}
```

Both assertions also work in `picsart_scene_lint_layout.relationships`. Edges are `left`, `right`, `top`,
`bottom` of **unclipped, unrotated root-space boxes**, not a local parent frame. Attachment edges
must share an axis. Its signed gap is **member edge minus anchor edge**: a row bottom 20 px above
the panel bottom uses `edge:"bottom", anchorEdge:"bottom", gapPx:-20`. An inset header top 20 px
below the panel top uses both `top` edges and `gapPx:20`. `fixed_edge.valuePx` is an explicit root
coordinate, including negative values; neither check learns a passing baseline from the scene.

Sizes may change. Each sampled member (and attachment anchor) must have measured on-canvas geometry;
known absence fails, while missing/ambiguous/unmeasured/rotated geometry is inconclusive. A held
frame with `active:false` can still have usable geometry. Any measured violation keeps the verdict
`fail` even when another observation is unavailable. Scope checks to the phase where the relationship
is intended; a later independent departure needs a separate window, not a relaxed tolerance.

Read timestamped `issues`/`evidence` and `measurement:{actualPx,expectedPx}` for a mismatch. For fixed
edges these are root coordinates; for attachments they are signed gaps. `maxErrorPx` is their absolute
difference and `tolerancePx` defaults to 1. Matching endpoints can hide intermediate easing errors:
sample through the growth/reveal, not only before and after it.

A vertical attachment says nothing about horizontal alignment, containment or paint. Add the other
axis or padded `contains` assertion when intended. These checks validate authored reflow; they do
not compute layout, scale text, or prove a reveal is readable. Still inspect intermediate frames.

Sampling includes `t0` and excludes `t1` (and the composition end); to inspect a seam,
place it on the sample grid and extend `t1` beyond it. Query the exact seam separately if needed.

Read `relationships` independently of collision `findings`. `allow` only acknowledges deliberate
overlap; it does not waive a relationship. A violation reports the input index, worst measured time,
pixel error and bounded issues. Missing measurements report `inconclusive`. Lint never fixes the scene.

### Reading the overlap report

Overlap candidates are visible on-canvas layers with geometry (held frames too) in the same
composition scope; nested wrappers use their painted child bounds. Each overlapping pair is
classified:

| Class | When | Where it lands |
|---|---|---|
| backdrop | the lower layer covers 85%+ of the canvas | `intentional` |
| containment | 90%+ coverage for 80% of the shared time | `intentional` |
| transient | overlapping for under 0.4 s | `info` |
| collision | sustained overlap at or above `iou` (default 0.05) | `findings` |
| graze | sustained overlap below `iou` | `info` |

- **Layers in depth** overlap on their projected quads, in each sample's paint order. A collision
  between two planes of a perspective camera stays a finding, annotated `depthStacked {near, far}`:
  judge it yourself, with `covered` as the hidden-text check.
- **`covered`** lists layers left under half visible at some sample by layers drawn after them, in
  any composition, that the document states opaque (alpha and `effectiveOpacity` 0.98+): a color, a
  JPEG or MP4 picture, a filled rectangle. A text layer under half visible for 0.4 s or more is a
  finding; anything else is info. A cover the document does not state opaque is noted unmeasured.
- **`allow`** moves the named pairs to `allowed`, keeping their class, and clears a covered layer
  whose every cover is allowed. An entry that never overlaps is reported as stale.
- **`mostlyOffCanvas`** lists root layers whose best visible share stayed below half.
- Text boxes are metric envelopes, not glyph bounds.
- Findings never fail the call. Bad options, a bad window and query errors do.

Sampling is bounded to 600 samples per call: a window that needs more, at the default 0.25 s step
or an explicit one, is refused with the smallest step that fits. It can miss a brief violation. Use windows around event/seam
times and frame-spaced samples; include before, during and settled states. Then inspect
`picsart_scene_contact_sheet` with explicit `times` and `resolution` equal to the composition dimensions and continuous scene video. Geometry alone cannot judge smoothness, painted
occlusion, typography or whether the story is understandable.

For timing syntax use scene-animation-reference (fetch with `picsart_scene_recipe`, name `scene-animation-reference`); for interactive causality
use app-ui-animation (fetch with `picsart_scene_recipe`, name `app-ui-animation`); for big compositions use
large-scene-assembly (fetch with `picsart_scene_recipe`, name `large-scene-assembly`).

**Research note:** independently authored for scene from the observed authoring failure modes and
general motion/layout principles. This is not an imported Hyperframes implementation.
