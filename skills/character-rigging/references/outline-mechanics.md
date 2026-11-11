# A shape's outline: how the format says it

Part of the `character-rigging` skill: the field-level mechanics behind its morphing craft. Read it before writing a `path`'s `vertices` track, `morphs`, per-vertex tracks or an outline expression.

## Contents

- A shape's outline
- Puff or pinch a whole outline: `puckerBloat`

## A shape's outline

Within a shape's `items`, and a group's `contents`, the first item paints on top, as After Effects
stacks layers: list a face's mouth and eyes before the head they sit on.

A `path` item's `vertices` can be a track of whole outlines, one easing per segment:

```json
"vertices": { "keyframes": [
  { "time": 0, "value": [ {"point": [0, -100]}, {"point": [100, 0]}, {"point": [0, 100]}, {"point": [-100, 0]} ], "easing": "ease_in_out" },
  { "time": 1, "value": [ {"point": [0, -160]}, {"point": [60, 0]}, {"point": [0, 160]}, {"point": [-60, 0]} ] }
] }
```

- **Morph.** Vertex *i* moves to vertex *i*, so both keyframes of an eased segment need the same
  vertex count (`shape_path_vertex_count_mismatch`). Start every keyframe at the same vertex and
  wind it the same direction, or a closed outline twists through itself mid-morph.
- **Outlines drawn separately.** Draw each shape on its own, key them in order as the path's `vertices`
  track, then call `picsart_scene_apply_preset` with `preset` `outline:match` on the layer. It adds vertices without changing any of the shapes, matches the winding and
  picks corresponding start vertices. It refuses a path that already has `morphs`, whose offsets
  follow the old vertices: match first, then add morphs. Match static outlines only, then animate.
- **Swap.** `"easing": "step"` on the earlier keyframe holds its outline until the next keyframe,
  so differently drawn outlines with different vertex counts can replace each other (mouth shapes,
  frame-by-frame drawings).
- **Round outlines.** A circle of radius `r` drawn with `N` evenly spaced vertices needs handles
  tangent to the circle, each `r · 4/3 · tan(π / 2N)` long: `0.552·r` for 4 vertices, `0.211·r`
  for 10. Longer handles bulge between vertices and shorter ones read as facets.
- **Loop or wobble.** The track takes an `expression` too. `value` is the keyframed outline: an
  array whose entries are `{point, inTangent, outTangent}` tables of `Vec.v2`, with
  `value.closed` read-only. `"return ctx:loopOut(\"cycle\")"` repeats the keyframes (modes in
  the `scene-animation-reference` skill's `picsart.*` stdlib); a wobble moves the points and returns `value`:
  `for i, v in ipairs(value) do v.point = v.point + Vec.v2(0, 6 * math.sin(time * 4 + i)) end return value`.
  The returned outline has the vertex count of one of the track's keyframes; a count no keyframe
  has fails the frame naming `vertices`. A `loopOut` over `step` keyframes loops swapped drawings
  (mouths, blinks) of different vertex counts; in `cycle` the last keyframe only ends the cycle, so
  end the track with a repeat of the first drawing.

**Per-vertex tracks.** When parts of an outline move on their own timing (a tail tip lagging the
base, one corner of a mouth), keep `vertices` a static list and animate a vertex's `point`,
`inTangent` or `outTangent` like any vec2 field, each with its own keyframes, easing and
expression:

```json
"vertices": [
  {"point": [0, 0]},
  {"point": {"keyframes": [{"time": 0, "value": [100, 0], "easing": "ease_in_out"}, {"time": 1, "value": [140, -30]}]}},
  {"point": [0, 60]}
]
```

A vertex field has no default, so an expression that reads `value` needs a keyframe to read;
an expression-only field fails `invalid_shape_expression_needs_base_value`. A tip on its own
rhythm:

```json
{"point": {"keyframes": [{"time": 0, "value": [130, -300]}],
           "expression": "return value + Vec.v2(90 * math.sin(2 * math.pi * time / 3.2), 0)"}}
```

A path has one driver: a whole-outline `vertices` track or per-vertex tracks, never both
(`shape_path_driven_twice`).

**Morph targets.** For shapes that blend independently (a mouth that opens and smiles, a blink),
give the path named `morphs` instead of authoring every combination as an outline keyframe. Each
target has one offset per outline vertex, moving its `point`, `inTangent` and `outTangent` by fixed
`[x, y]` amounts (`{}` leaves a vertex alone, so a target can round a lip by moving only its handles),
and a `weight`, an ordinary animatable number that defaults to 0 and is not clamped. Each frame adds
weight × offsets on top of whatever drives `vertices`, after the track's own expression
(`shape_path_morph_vertex_count_mismatch` when the counts differ). To drive a weight from a scene
parameter, declare the parameter `animatable` and read it in the weight's expression:

```json
"parameters": { "smile": { "type": "number", "default": { "keyframes": [{"time": 0, "value": 0}, {"time": 3, "value": 1}] }, "animatable": true } },
...
"morphs": { "smile": { "offsets": [{"point": [0, -8]}, {}, {"point": [0, -8]}],
                       "weight": { "expression": "return ctx.composition:getParameters():smile()" } } }
```

A character's controls take the standard control names
(`happy`, `aa`, `leftUpperArmRaise`, …). A 2D cartoon character starts from a catalog rig
(`rig-humanoid`, `rig-face`) when one fits, which already drives its parts from those names
([SKILL.md](../SKILL.md) §0), and is built by hand
(`references/character-motion.md`) when none does.

For the craft of a
morph — matching two drawings, targets and correctives, anticipation, overshoot, holds, breakdowns,
squash volume, visemes and blinks, scene-to-scene morphs — read this skill's [SKILL.md](../SKILL.md).

**In a look.** A look carries whole-outline keyframes through a `path` parameter, always
`animatable`, bound whole at a path item's `vertices`; the application passes its own outlines
(mouth shapes, a squash-and-stretch wipe) as `params`:

```json
"parameters": {"mouth": {"type": "path", "animatable": true, "description": "Mouth outlines.",
  "default": {"keyframes": [
    {"time": 0, "value": [{"point": [0, 0]}, {"point": [40, 0]}, {"point": [20, 4]}], "easing": "ease_in_out"},
    {"time": 0.5, "value": [{"point": [0, 0]}, {"point": [40, 0]}, {"point": [20, 24]}]}]}}},
"emit": {"duration": 1, "timeFit": "stretch", "layers": [{"id": "mouth", "content": {"kind": "shape", "items": [
  {"type": "path", "closed": true, "vertices": {"$eval": "mouth"}},
  {"type": "fill", "color": "#ffffff"}]}}]}
```

Its keyframe times fit the look's clock like any other track, and an expression bound with them
(`ctx:loopOut`, a wobble) is re-clocked with them. The outline laws hold where the param is
declared and where it is bound: a vertex count that changes across an eased segment
(`shape_path_vertex_count_mismatch`), a track inside a keyframe's vertex (`shape_path_driven_twice`)
and an expression with no keyframes are refused. A formula over the param, a path param at a vec2
field and a vec2 param at `vertices` are refused by the look's destination check, and so is a
`"loop"` time fit.

A path param may declare named `outlines`; a value then names one in place of an outline, and a
step track of names swaps them on time: `"shape": {"keyframes": [{"time": 0, "value": "oh", "easing":
"step"}, {"time": 1, "value": "aa"}]}` (`parameter_binding_not_in_enum` for a name it does not
hold). The catalog's `mouth_shapes` (the visemes rest / aa / oh) works this way, and `squash_wipe` carries its
wipe outline the same way; find both with `picsart_scene_looks {"tags": ["cartoon"]}`. A scene template
binds a path param the same way, at a path's `vertices` on a top-level layer keying in composition
seconds; anywhere else it is `param_site_type_mismatch`.

**Bending or denting an outline (`deformers`).** A `shape` content's `deformers` list moves the whole outline
its items draw (paths, rects, ellipses, polystars, inside groups too, after every modifier) in the
content's coordinates, before the layer's `transform`, each entry on the previous one's result; the
fill and stroke are drawn on the moved outline, so a stroke keeps its width, and a stroke's `taper`
is laid along the moved outline, so it stays at the limb's ends. A `bend` turns one
continuous drawing across a joint (a rubber-hose arm, a torso lean, a tail) along an arc, so the
limb keeps its width; a morph or an outline track moves vertices on chords and thins it.

```json
"content": { "kind": "shape", "items": [ ... ],
  "deformers": [
    { "type": "bend", "from": [0, 0], "to": [0, 40],
      "angle": { "by": "shoulder", "keyframes": [{"at": 0, "value": 0, "easing": "linear"}, {"at": 1, "value": 70}] } },
    { "type": "bend", "from": [0, 130], "to": [0, 170], "falloff": 1,
      "angle": { "by": "elbow", "keyframes": [{"at": 0, "value": 0, "easing": "linear"}, {"at": 1, "value": -100}] } }
  ] }
```

- `from` -> `to` is the joint band. Points at or before `from` (along that axis) stay; points past
  `to` turn rigidly by `angle` (degrees, clockwise); the band bends into an arc between. `angle` is
  any animatable number: static, keyframes, an expression or keyed `by` a dial.
- `falloff` 0..1: 0 (default) an even arc; 1 eases the turn in and out, tightest mid-band.
- `min`/`max` (degrees, optional) limit the turn: every frame the angle is held inside them, whatever drives it, an `ik` solve included.
- Write every joint where it sits at rest: a later bend's `from`/`to` are carried by the earlier
  ones, so a shoulder then an elbow bend the forearm on the turned arm.
- A band shorter than angle (radians) × half-width folds its inner side.
- An elbow bulge or crease is a path `morph` drawn at rest: morphs apply before the deformers, so the
  bend carries it.
- A `push` dents (or bulges) the outline around one point, as where a ball meets a floor:
  `{ "type": "push", "center": [0, -40], "radius": 120, "offset": { "keyframes": [{"time": 0.5, "value": [0, 0]}, {"time": 0.6, "value": [0, 35]}, {"time": 1.1, "value": [0, 0]}] } }`.
  The point at `center` moves by `offset`, easing to nothing at `radius`; points at or past `radius`
  stay. `center` and `offset` animate like `angle`. Keep |`offset`| under about 0.65 × `radius`, or
  the dent folds. A push before a bend turns with the limb; after it, its `center` rides the limb and
  it presses in a fixed direction.
- A `stretch` shortens (or lengthens) one section along its length and keeps its width, as a limb
  tilting toward the camera does on screen: `{ "type": "stretch", "from": [0, 0], "to": [0, 100], "factor": 0.6 }`.
  Points at or before `from` stay; a point `y` into the section lands `factor × y` in; everything
  past `to` moves with the section's end. `factor` animates like `angle`; 1 is rest, 0 closes the
  section up, below 0 it lands mirrored before `from`. `[stretch thigh, bend knee, stretch shin]`:
  the knee rides the shortened thigh and the shin shortens along its bent direction. An entry may
  carry an `id`, unique in its list.
- A `skin` makes the outline follow bone layers, so an arm drawn as one shape bends at the elbow
  with its width kept: `{ "type": "skin", "bones": [{ "layer": "upperArm", "radius": 70 },
  { "layer": "lowerArm", "end": [0, 150], "radius": 70 }] }`. A bone runs from its layer's pivot to
  `end` (the bone layer's px; default the next bone's pivot, so the last bone writes it); `radius`, about
  the limb's width, is how far from its segment it holds. The rest pose is the bone layers' static transforms: key or
  constrain the bones, not the drawing. Limit a joint on its bone layer: `"rotation": {"min": -150, "max": 0}` in
  its `animations`, with keys or without (a still bone). Put it last in the list. A clip `mesh`'s `deformers` take
  the same entry, so a meshed picture of a limb bends as a drawn one does.
- Put a hand, a hat or a prop on the bent, pushed, stretched or skinned drawing with an `attach` layer constraint:
  `{ "type": "attach", "target": { "layer": "arm", "position": [0, 160] }, "rotate": true }` lands the
  layer's anchor on the arm's point drawn at `[0, 160]`, carried through the arm's deformers, and
  `rotate` turns it with the drawing there; no `parentId` needed. `{ "layer": "arm", "point": 7 }`
  names an outline vertex instead (from 1, as drawn after keyframes, keyed poses, morphs and
  deformers), for an outline whose vertices move by morphs or keys. `aim` turns a layer's `axis`
  toward such a point (eyes on a ball).

**Poses keyed to a dial (`by`).** A track with `"by": "<number parameter>"` places its keys `at`
values of that parameter of the composition it is authored in (`at` in place of `time`): the track shows the pose
keyed at wherever the dial stands, eased between keys by their `easing`, the end key held past the
range. Draw each pose once and turn the dial; no per-part math. `by` works on `vertices`, a vertex
field, a morph `weight`, `position`, `scale`, `opacity`, a colour and effect params. It is refused on
the tracks keyed by time only: `crop`, a text rail's `{t, v}` stops, a 3D channel, and the opacity and
sizing effects of a look's host. The keys stand at strictly increasing `at` values, with |value| up to
500000 (`keyframe_at_out_of_range`) and a resolution of about 1e-6 (`keyframe_at_not_increasing`; a jump is `step`).

```json
"parameters": { "headTurn": { "type": "number", "min": -1, "max": 1, "animatable": true,
                              "default": { "keyframes": [{"time": 0, "value": -1, "easing": "ease_in_out"}, {"time": 4, "value": 1}] } } },
...
"vertices": { "by": "headTurn", "keyframes": [
  { "at": -1, "value": [ ...far-left eye... ] }, { "at": -0.667, "value": [ ... ] }, ...,
  { "at": 1, "value": [ ...far-right eye... ] } ] }
```

- **Mouth chart.** `step` keys at 0, 1, 2, 3 on a `mouth` dial swap drawn mouths of any vertex count;
  the dial's own `step` keyframes are the lip-sync; `lipSync:visemes` (`picsart_scene_apply_preset`) with `mouthShapes` mapping each
  drawing's name to its dial number writes them from a transcript.
- **Head turn.** A turn needs a pose every 15°: a ±45° turn is 7 poses. Three poses (left, front,
  right) leave features up to 11 px off a 190 px head mid-blend; 7 poses bring them under 1.4 px.
  On the turn side the far eye moves toward the edge and narrows.
- **Morph weight.** `"weight": {"by": "smile", "keyframes": [{"at": 0, "value": 0}, {"at": 1, "value": 1}]}`
  reads the dial without an expression, and the keys can shape it (an overshoot, a dead zone).
- **Two dials on one value** (turn and tilt), by how they combine:
  - *They add up* (turn slides a feature sideways, tilt slides it up): one track per dial, stacked as
    two `transforms[]` entries, or a morph target per dial. Poses: one row per dial.
  - *They mostly add up, with a fix where both are high* (a turned-and-tilted nose that also tucks): the
    per-dial tracks, plus a corrective morph whose `weight` expression is the product:
    `"return ctx.composition:getParameters():turn() * ctx.composition:getParameters():tilt()"`.
  - *Every combination is its own drawing* (an eye that reshapes differently up-left than up-right):
    one track keyed by both, `"by": ["turn", "tilt"]`. Each key stands `at` one value per dial, and
    the keys fill the grid: a key at every combination of the positions on each axis, no corner
    missing (`keyframe_grid_incomplete` names it), none twice. Between keys the value blends
    bilinearly. `easing` is one for both axes, or one per parameter by name (`{"turn": "linear",
    "tilt": "step"}`, a parameter left out is `linear`), and every key at one position on an axis eases
    alike along it (`keyframe_grid_easing_mismatch`). A list eases the value's components here as on
    any track: whole along both axes, or under one name (`{"turn": ["ease_out", "linear"], "tilt":
    "ease_in"}`). No grid parameter is named `kind`. Such
    a track is never `aggregate` and takes no motion-path handles (`animation_grid_unsupported`).
    Poses: rows × columns, so reach for it only when the corners really differ.

  ```json
  "vertices": { "by": ["turn", "tilt"], "keyframes": [
    { "at": [-1, -1], "value": [ ...left, up... ] },    { "at": [-1, 1], "value": [ ...left, down... ] },
    { "at": [ 1, -1], "value": [ ...right, up... ] },   { "at": [ 1, 1], "value": [ ...right, down... ] } ] }
  ```

  An `expression` on a `by` track sees the keyed pose as `value`; `by` with no keyframes is
  refused (`animation_clock_needs_keyframes`), a key with `time` on a `by` track or `at` on any
  other is `keyframe_axis_mismatch`, and keys outside a parameter's `min`/`max` warn
  (`keyframe_outside_parameter_range`), each axis judged as its own parameter.

## Puff or pinch a whole outline: `puckerBloat`

`{ "type": "puckerBloat", "amount": 40 }` reshapes every geometry item above it in its group (nested
groups included) around each contour's centre, the average of its vertices. A positive `amount`
bloats: each vertex moves `amount` percent of the way to the centre while its handles push out, so the
edges bow outward. A negative `amount` puckers: the vertices move out and the handles move in, into
spikes. `amount` is animatable, so one item takes a star to a flower and back:

```json
{ "kind": "shape", "items": [
  { "type": "polystar", "starType": "star", "points": 6, "outerRadius": 120, "innerRadius": 60 },
  { "type": "puckerBloat", "amount": { "keyframes": [
    { "time": 0, "value": 0 }, { "time": 2, "value": 60 }, { "time": 4, "value": -40 } ] } },
  { "type": "fill", "color": "#F2A33A" } ] }
```

A rounded badge whose sides puff out: bloat a SHARP `rect`, then round it with `offsetPaths`. Bloat on
a `rect` with `roundness` pinches each rounded corner into ears, and `roundCorners` after the bloat does
not smooth them. `offsetPaths` grows the outline by `amount` with round corners, so draw the rect
`2 × amount` smaller than the badge:

```json
{ "kind": "shape", "items": [
  { "type": "rect", "size": [232, 92] },
  { "type": "puckerBloat", "amount": 14 },
  { "type": "offsetPaths", "amount": 24 },
  { "type": "fill", "color": "#3A7BF2" } ] }
```
