---
name: scene-animation-reference
description: How a scene expresses motion — preset catalogs, layer animations and transform stacks, easing and spatial tangents, Lua expressions, shared path phase, text on a curved or closed path, depth and the composition camera, motion blur, and transition firing. Use when motion needs authoring or validation, objects need editable path offsets, text must follow a baseline, a scene validates but renders wrong, or a preset is rejected for the content kind.
metadata:
  category: authoring
  version: '1.9'
user-invocable: false
---

# Saying motion in a scene

The decision — what a beat is for, how long, which register — is `picsart_scene_recipe motion-intent`.
This is the other half: how the format says it, and the places where the obvious spelling is the
wrong one. For the relationship across beats or the choice of seam mechanism, decide first with
`picsart_scene_recipe motion-scene-continuity`, then return here for syntax. For semantic grouping, container
growth and sibling reflow, first use `picsart_scene_recipe linked-element-motion`. A common placement owner
does not imply automatic layout. The constructions below need verification in the actual scene.

## Two catalogs, two ways in

They look alike and are applied differently. Getting this wrong is the commonest first failure.

| | Motion looks | Motion presets | Text animations |
|---|---|---|---|
| What | entrance/exit (`role: in`/`out`) `fade`, `slide`, `zoom`, `spin`, `wipe`, `blur`, `flip`; entrance `pop`, `flash`; loops `float`, `sway`, `shake`, `pulse`, `glow_pulse`, `blink`, `rotate`, `clockwork`, `ken_burns` | entrances `fade_in`, `slide_in`, `zoom_in`, `scale_pop`, `spring`, `rotate_in`, `blur_in`, `flip_in`, `reveal_in`; exits `fade_out`, `slide_out`, `zoom_out`, `rotate_out`, `blur_out`, `reveal_out`; emphasis `tap_pulse`, `glow_pulse`, `shake`; atmosphere `ken_burns`, `breathe`, `float`, `sway` | `typewriter`, `fade_in_chars`, `slide_up_lines`, `flicker_chars` (+ ambient ones, below) |
| Applied with | `picsart_scene_apply_preset` with `look:<id>` (iOS `applyLook`) and `params` (`role`, `length`, …); a window `start`/`duration` is set on the `looks[]` entry with `picsart_scene_patch` | `picsart_scene_apply_preset` with `motionPreset:<id>` (iOS `applyMotionPreset`) | name it in `content.animations[]`, or bake an entrance with `picsart_scene_apply_preset` and `textAnimation:<name>` |
| Lands in | the layer's `looks[]` | the layer's `animations` / `transforms[]` / `effects` | the text content's `content.animations[]` |
| Named in the document? | yes — `{ "look": "fade", "params": { "role": "in" } }`, so an editor shows and swaps it | no — the tool expands it into ordinary keyframes | yes — `{ "preset": "typewriter", "params": {} }` |

**A preset or a look.** A motion preset is a starting point: it writes ordinary keyframes (and
effects) that the agent or the editor user then owns and edits keyframe by keyframe. A look stays a
named entry an editor shows and swaps as a whole. Use a preset when the keyframes will be edited
afterwards; use a look when the motion should stay a named, swappable entry. A one-shot beat at a
chosen moment (`tap_pulse`, `spring`, `scale_pop`) is a preset.

A look applies to the kinds its `appliesTo` lists. Most motion looks take `color` and `shape` layers
too (`blur` and `flip` take `color` but not `shape`; `wipe`, `flash`, `blink`, `rotate` and
`clockwork` take neither). For a look that does not list the kind, wrap
the layer in a scene asset and apply the look to the `scene_ref`.

`content.animations[]` is a mixed source list: each row is either a named `{preset, params?}` reference
or a concrete per-glyph `{transform, selector}` entry. Resolution expands every named row before the
renderer sees it. Naming keeps the choice editable and can reach a `type: "text_animation"` definition
declared in the document's own assets; baking with the tool writes the concrete entries instead.

**Content-kind traps.** `ken_burns`, look or preset, takes `media` / `scene_ref` only, and a look
or preset on a kind outside its `appliesTo` is `preset_kind_mismatch`. A plain text layer may name either an entrance preset or an **ambient** one
(`drift`, `flicker`, `hop`, `shake`, `sway`, `throb`, `transform`, `wiggle`). Ambient motion uses
the layer's duration as its resolution window; its mode decides whether it is static, plays once,
loops, or ping-pongs. It selects every glyph. A caption can use the same ambient definition through
a decoration row's `place: "text"` field when it needs line/emphasis/highlight selectors instead.

`applied` in the result names the preset once; `entryCount` says how many animator entries it
appended (a multi-decorator preset like `slide_up_lines` appends two).

### What `picsart_scene_apply_preset` writes

- **Camera presets** (`appliesTo: ["camera"]`, e.g. `motionPreset:push_in`, `dolly`, `orbit`) move the
  root composition's camera when `layerId` is omitted, or the camera of the `composition` or
  `scene_ref` layer it names.
- **Effects** can be confined to a detected region with `mask`: the effect's `supports.effects` row
  says whether it takes one, and the detectors are listed under `supports.maskProviders`.
- **Text animations** start at the text layer's local time 0: set the layer's `start` to reveal it
  later. An ambient text animation is not baked; it is attached by name in `content.animations[]`.
- **Looks** wrap the layer's content in an isolated nested composition, so the look treats the
  composited result as one image. By reference (the default) nothing is baked: preview, translate
  and query expand it when needed, and `picsart_scene_resolve_looks` bakes a self-contained scene.
  `mode: "expand"` bakes it now: `transform`, `animations`, `blendMode`, `mask` and `motionBlur`
  move onto the wrapper, the layer's own effects apply once before the look, and a track clip bakes
  its whole `looks[]` chain and keeps its slot. A layer with `adjustmentLayer: true` takes no look.

## Where a motion lives

Two places, and the choice is not stylistic.

**`animations`** — the layer's own Placement tracks (`position`, `scale`, `rotation`, `z`,
`rotationX`, `rotationY`, `opacity`, `anchor`). Pivots about the layer's own anchor. Always available.

**`transforms[]`** — an ordered stack of motion components applied *outside* Placement, each with its
own `id` and `animations` (`translation` / `scale` / `rotation` / `z` / `rotationX` / `rotationY` /
`anchor`), evaluated in array order:

```json
"transforms": [
  { "id": "entrance", "animations": { "translation": { "keyframes": [ ... ] } } },
  { "id": "breathe",  "animations": { "scale": { "expression": "return value * (1 + 0.02 * math.sin(2*math.pi*time/3))" } } }
]
```

The stack exists so **layout stays editable**: `transforms` carries motion (animations, presets) and
`transform` is the placement a user or host edits. They compose, so editing placement never rewrites
the motion, and the motion follows the edit. That is why a `motionPreset:` preset applied with `picsart_scene_apply_preset` routes geometry here. One
component per motion layer also keeps each independently re-timeable, instead of one `scale` track
carrying an entrance and a breathe that can no longer be told apart.

Positions follow After Effects: `transform.position` places the layer's `transform.anchor` in its
parent's space (the parent layer's own pixels with `parentId`, otherwise composition pixels from the
top-left). An omitted component `anchor` is that anchor **where it currently sits**, following a
`position` animation and parenting, so a component scale or rotation turns the layer in place even
while it moves:

```json
"transform": { "position": [300, 300] },
"animations": { "position": { "keyframes": [ {"time": 0, "value": [300, 300]}, {"time": 2, "value": [700, 300]} ] } },
"transforms": [
  { "id": "spin", "animations": { "rotation": { "keyframes": [ {"time": 0, "value": 0}, {"time": 2, "value": 360} ] } } }
]
```

Mental model: a component is a parent null (After Effects) or a wrapper element (CSS) sitting on the
layer's anchor. With no `anchor` it rotates and scales about the layer's anchor wherever the layer
currently is, and `translation` moves in parent pixels.

- **Turn about a fixed point** — give the component an `anchor`: a fixed point in the layer's
  parent space, not the layer's own pixels. It replaces the pivot and does not follow placement edits.
  `anchor: [0,0]` pivots on the parent's top-left.
- A component's `animations.anchor` is its pivot track, in the same parent space; a layer's own
  `animations.anchor` is layer-local, like `transform.anchor`.

## Easing

`linear`, `ease_in`, `ease_out`, `ease_in_out`, `step` — **plus** a parametric curve:

```json
"easing": { "kind": "cubic_bezier", "control": [0.175, 0.885, 0.32, 1.275] }
```

CSS convention: `x` stays in [0,1], while `y` may extend beyond it. A control ordinate is not the
rendered overshoot percentage: the curve, endpoints and timing determine the actual peak. Query or
render the peak in the scene before deciding whether it suits the intended motion.

**A keyframe with no `easing` is `linear`.** Use it deliberately for constant-rate travel or progress;
use an eased curve when acceleration or settling serves the beat. Easing belongs on the segment's
starting keyframe; the terminal keyframe has no following segment to ease.

## Path, separately from timing

`inTangent` / `outTangent` on a `position` or `anchor` keyframe are `[x, y]` velocity handles
relative to that keyframe's value — AE motion-path handles. `easing` shapes the timing *along* the
path; the tangents shape the path itself. Omitted means a straight line, which is why every
unattended long move is one.

```json
"position": { "keyframes": [
  { "time": 0, "value": [200, 540], "easing": "ease_in_out", "outTangent": [120, -160] },
  { "time": 1.6, "value": [880, 540], "inTangent": [-120, -160] }
] }
```

A handle on any other property is dropped.

For **a path driven by a separate phase**, use tangent keyframes plus
`ctx:sampleBase(seconds)` on that same property. Read [Shared path phase](references/path-phase.md)
for a runnable scene, offset/clamp/wrap choices, clock and sampling limits, and executable checks.
This keeps position geometry editable without retiming the card's video. Ordinary timed movement
still needs only keyframes; this extra sampling is for independently controlled progress.

For **text on a curved or closed baseline**, use `content.textPath` rather than
one animated layer per letter. Read [Text on a path](references/text-on-path.md)
for geometry, animated offsets, combined character animators and validation. This is distinct from
moving an entire object along its position track.

## Expressions

For an object that turns along its path, keep one authoritative position track and bind
`animations.rotation.expression` to `positionDirection()`. Do not introduce an auto-orientation
flag or copy the path into a separate heading track. The artwork's forward-axis correction belongs
in `transform.rotation`; the expression adds it through `value`. This applies to arrows, vehicles
and other path followers, not only cursors. Ordinary value reads do not request motion samples;
direction/velocity work is on demand when the expression calls it.

Read Cursor-led action (fetch with `picsart_scene_recipe`, name `app-ui-animation`) and its direction reference
before authoring the binding. Through MCP, fetch `picsart_scene_recipe` with `name: "app-ui-animation"`,
then its listed **Cursor actions and menus** reference. It contains the executable expression, coordinate
and clock limits, hold/zero-direction behavior and validation. Check heading against independent
travel samples, including a changed path and a delayed instance; a valid expression and correct
positions alone do not prove correct orientation. Use an explicit heading track only when the
art direction deliberately differs from travel (banking, gaze, a stationary expression's held pose).

A track can carry a Lua `expression` instead of, or on top of, keyframes. It must `return`, sees
`value` (the keyframed base) and `time` in **layer-local seconds**, zero at that layer's start,
and returns `Vec.v2(x, y)` for vec2 properties. Moving the layer's start moves the expression's
onset too; do not subtract that start again. For a nested scene, map root time into the containing
composition first, including reference trim/speed, then subtract the child's start. Keyframe
`timeMode` does not turn an expression's clock into root time. Check delayed/nested instances with
`picsart_scene_query_layout` at their mapped start and later moments.

### Bind a supported property instead of copying its track

Prefer a common composition owner for a rigid widget. For a genuine one-way dependency between
separate layers, Lua can read a sibling's evaluated Placement, for example on the follower's
position track:

```json
{ "expression": "return ctx.composition:getLayer('driver'):getPlacement():position() + Vec.v2(0, 24)" }
```

This reads an authored sibling id in the same composition; it is not a flattened query id. The
result is Placement in that layer's parent space, not its root-space painted center or the result
of every `transforms[]` entry. Use this offset formula only with compatible parent spaces, anchors
and intended Placement motion. For shared transform-stack motion, use an owner instead. Self-reads
of the property being defined and cyclic dependencies are refused. Consult the current expression
schema for available getters; there is no arbitrary live shape-size or text-metrics getter.
Unlike `$eval`, this is a per-frame dependency. Validate and query the actual delayed/nested instance;
local `time` formulas on separately started layers need clock mapping even when their text matches.

Two compact time-expression uses:

**Ambient motion that continues looping** for the beat's duration:

```
"scale": { "expression": "return value * (1 + 0.15 * math.sin(2*math.pi*time/2))" }
```

The coefficient varies the base scale by ±15%. Its literal two-second period does not change when
the beat duration changes; adjust it explicitly to preserve a chosen cycle count. Inspect the
resulting bounds, final phase and reading comfort.

**A real spring** — a damped oscillation, which one `cubic_bezier` cannot express:

```
"scale": { "expression": "return value * (1 + 0.35 * math.exp(-6*time) * math.cos(18*time))" }
```

The expression alternates around the base value with diminishing amplitude. Raise the
`exp` coefficient to settle sooner, the `cos` coefficient for more bounces.

### The `picsart.*` stdlib — the recurring shapes, already written

These are built in. Reach for them before
hand-rolling the trigonometry. Call them directly as `picsart.<name>(...)`; an alias such as `local p = picsart` is not supported.

```
"opacity":  { "expression": "return picsart.oscillate(time, 0.3, 1, 0.7)" }
"position": { "expression": "return picsart.jitter(value, time, 16, 11, 0.3)" }
"rotation": { "expression": "return picsart.wiggle(value, time, 2, 4)" }
"scale":    { "expression": "return Vec.v2(picsart.oscillate(time, 1, 1.05, 2), picsart.oscillate(time, 1, 1.05, 2))" }
```

- `picsart.oscillate(time, low, high, halfPeriod)` — smooth low↔high, starting at `low`, one half cycle
  every `halfPeriod` seconds. A vec2 property takes one call per component inside `Vec.v2`.
- `picsart.jitter(value, time, ampX, ampY, step)` — deterministic shimmer around the layer's own base
  `value`, resampled every `step` seconds. Not random: same inputs, same frame.
- `picsart.wiggle(value, time, freq, amp)` — AE's `wiggle`, fractal noise at `freq` wiggles/sec.

**In a DEFINITION** (a look, a transition, a decoration) `{param}` splices the definition's own
scope into the expression text, so the shape stays parametric:

```
"opacity": { "expression": "return picsart.oscillate(time, {glow} * 0.3, {glow}, 0.18 / {speed})" }
```

`{name}` there is a raw TEXT splice, not a typed lookup — it drops the param's number into the Lua
source, so surrounding arithmetic is Lua's. (Everywhere OUTSIDE an `expression`, `{name}` is the
typed scope lookup instead.) `picsart_scene_capabilities` lists the full stdlib.

## Depth and the camera

Every composition is seen through one perspective camera, `composition.camera`. Omitted, it is the
default: pivot at the composition centre, `distance` `width * 50 / 36` (a 50 mm lens), no orbit. On
the `z = 0` plane that draws exactly the flat composition, so depth costs nothing until a layer asks.

| Field | Meaning |
|---|---|
| layer `transform.z` | depth in composition px, **positive toward the viewer** |
| layer `transform.rotationX` / `rotationY` | tilt in degrees, the `perspective_3d` effect's signs: +X tips the top edge away, +Y turns the right edge away; `rotation` stays the clockwise roll |
| `camera.position` | the pivot the eye looks at; zoom, roll and orbit turn about it |
| `camera.zoom` | image scale about the pivot — perspective unchanged |
| `camera.distance` | eye-to-pivot px, > 0; the `z = 0` plane keeps its size at any distance, so animating it is a **dolly zoom** (nearer layers grow, farther ones shrink) — a push-in is `zoom` |
| `camera.rotationX` / `rotationY` | orbit of the eye: the view is the inverse of a layer rotation of the same values (eye right = world turned left) — +X raises the eye, +Y moves it right |

The layer matrix is `T(x, y, z) · Rx · Ry · Rz · S · T(-anchor)` (intrinsic XYZ, as `perspective_3d`); `anchor`, `scale` and `position`
stay `[x, y]`. All six layer/camera depth fields animate like any track; a layer's `animations.z`,
`rotationX` and `rotationY` are replace-only, and motion components carry them too, so a preset can
flip a card in depth.

Layers in one run of camera-participating, non-adjustment layers draw **far to near**, re-sorted
every frame; equal depth keeps document order. `cameraExempt: true` on a root keeps its subtree flat
and in place (a HUD). A mask follows its host's plane and carries no depth of its own. A nested
composition, `scene_ref` or track has its own camera and is drawn as ONE flat card at its layer's
`z` and tilt — put layers that must interleave in depth in the same composition. A look (such as
`rounded_corners`) keeps its layer's depth, tilt and draw order.

Camera moves ship as motion presets: `orbit`, `dolly` and `push_in`, each `appliesTo: ["camera"]`.
`picsart_scene_apply_preset` with `motionPreset:<id>` and no `layerId` keys them onto the root composition's camera as editable
tracks; their parameters are listed under `supports.motionPresets` in `picsart_scene_capabilities`.

Depth is verified by measurement. `picsart_scene_query_layout` reports each projected layer's `quad`, `depth`
(eye distance, larger is farther) and `zIndex` (this frame's paint order). In `picsart_scene_lint_layout`, a
relationship `{ "kind": "order", "axis": "depth", "members": [...] }` (members front to back) checks the
stack over a window, and `covered` names each layer left under half visible by the layers drawn after it.
An overlap between two planes stays a collision finding, annotated `depthStacked` (`near`, `far`): judge
whether the stack is intended, with `covered` as the check for text it hides.

Three laws for a scene in depth:

1. **A label rides its plane.** Make it a child of the plane (`parentId`) with no `z` of its own: it
   takes the plane's depth and tilt and draws in front of it. A label given its own `z` floats free
   of the plane and sorts on its own.
2. **Titles and HUD stay flat.** Make them `cameraExempt: true` roots.
3. **Read the orbit's sign, don't guess it.** `camera.rotationX > 0` raises the eye, so nearer planes
   project LOWER on screen; the classic exploded diagram, front plane highest, is `rotationX < 0`
   (measured: a four-plane stack at `distance` 2400 under ±42°). Render one frame at the held orbit
   before building on it.

## Motion blur

`"motionBlur": true` on the layer smears it along its own motion, keyframed or expression-driven.
It is what makes a fast move read as speed rather than a teleport. `composition.motionBlurSampleCount`
sets the shutter samples per frame (clamped 1..64); omit it for the default (16). It is refused in a
composition whose camera orbits or whose layers author depth (`motion_blur_3d_unsupported`).

## Transitions

A `transitions[]` entry needs `between` — which seam of the track it sits in — as well as `id` and
`duration`. Omitting it fails `transition_between_out_of_range`, which names the legal range.

Every shipped transition fills the `duration` it is given: its keyframes are written against the
window, so a longer window is a slower move — `card_flip` goes edge-on exactly at the seam, as
authored. None plays a video or lottie matte (those families were removed: their `.webm` mattes do
not decode on iOS).

## Validate the mechanism and its result

For reversals, jumps, overshoot, acceleration peaks or settling, inspect the actual output-frame times. Read [Frame-complete motion validation](references/frame-motion-validation.md) for independent thresholds and coverage limits. Run `picsart_scene_check_motion` with an explicit root-time window and the actual export FPS; explicit queries cover only the times actually requested. Do not claim frame-complete evidence unless every relevant frame and channel was compared. Construct rigid relationships with a shared owner or supported binding first; numerical checks do not replace ownership or visual inspection.

Read `picsart_scene_recipe motion-pattern-library` and fetch its **Validation by pattern** reference
before accepting a motion. Use its **mechanics**
rows for pivots/transform order, easing, local clocks, expressions, text selectors, and motion blur;
use its pattern rows for the intended beat. `picsart_scene_validate` accepts structure, not choreography.
Query evaluated geometry at the decisive events and extrema; run supported relationship contracts;
inspect rendered frames and playback for paint-only effects and perceived timing. Never substitute
authored keyframe values or a successful export for evidence that the evaluated result is correct.

## When it renders wrong

| Symptom | Look at |
|---|---|
| `preset_kind_mismatch` | a look or preset on a content kind outside its `appliesTo` (`ken_burns` on a non-media layer) |
| `unknown_text_animation_preset` | the name is absent from both the document and shipped text-animation catalogs |
| `invalid_text_animation_params` | a named text animation has a missing, unknown, or out-of-range parameter |
| the layer slides while it scales | a component `anchor` explicitly set to `[0,0]` |
| a transition fires but feels wrong | a mask-driven one whose `duration` is not its `sweep` |
| motion reads mechanical | `easing` omitted somewhere — that is `linear` |
| a layer moved in `z` does not reorder against a sibling | the sibling sits in another composition (a nested card), or a `cameraExempt`/adjustment layer splits the run |
