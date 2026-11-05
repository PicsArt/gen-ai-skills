# Live pins: recipes and checks

## Contents

- Find the rest points
- Tail with root, middle and tip
- Flag or long tail wave
- Squash a sticker corner
- Bend, then place a free handle
- Refusals and preview
- Keep the head firm while the body bends
- Region fields and coverage checks

Use a `shape` content's `deformers` for a drawn outline. Use a layer's `mesh.deformers`
for a raster picture, live text or any other content without editable outline geometry.
An explicit mesh from `mesh:auto` (`picsart_scene_apply_preset`) follows a transparent image's silhouette; `grid`
covers a rectangular picture. The same `pins` entry works in both places, and a mesh's
UVs stay fixed while its vertices move. Do not bake a live pose into sampled `mesh.points`.

## Find the rest points

`rest` is a content-local coordinate on the part before this `pins` entry. Read a
`path` item's `vertices` in the scene document; `picsart_scene_capabilities` with `sections: ["schema:ShapeContent"]`
shows their format. For a `rect`, its `position` is the centre and half its `size` gives
the extents from that centre; an ellipse uses its radii. `picsart_scene_query_layout` reports the resolved
layer box, not the outline's vertex list. A `getShape():point(i)` expression can
read the current drawn path vertices when a control must follow another path.
Use `picsart_scene_validate` after choosing rest points, then render or query the
shape: a rest point off the painted part is refused there. Keep the first
pin on the fixed root (`target` equal to `rest`), then space moving pins along
the part, not across a gap or a different part.

## Tail with root, middle and tip

Three pins are a useful start for a short tail; use four for a longer one. The
root holds, the middle leads the bend, and the tip travels farther. This tail is
a 24×120 rounded shape centred at `[0, 60]`, so its centreline runs from
`[0, 0]` to `[0, 120]`. Put the entry in that shape's `content.deformers`:

```json
{
  "type": "pins",
  "pins": [
    { "id": "root", "rest": [0, 0], "target": [0, 0] },
    { "id": "middle", "rest": [0, 60], "target": { "keyframes": [
      { "time": 0, "value": [0, 60] },
      { "time": 0.5, "value": [14, 55] },
      { "time": 1, "value": [0, 60] }
    ] } },
    { "id": "tip", "rest": [0, 120], "target": { "keyframes": [
      { "time": 0, "value": [0, 120] },
      { "time": 0.5, "value": [38, 104] },
      { "time": 1, "value": [0, 120] }
    ] } }
  ]
}
```

A jointed arm or leg should use a `bend` with `min`/`max` and `ik`, as the
humanoid rig templates do. Pins have no joint angle limit or IK target.

## Flag or long tail wave

Use four or five pins spaced about one quarter of the length apart. Hold the
root at x=0; phase-delay each later target by roughly 0.1–0.2 s so a crest
travels toward the tip. For a 240 px flag, centreline positions are 0, 60,
120, 180 and 240. These are the five controls; later pins have larger travel:

```json
{
  "type": "pins",
  "pins": [
    { "id": "root", "rest": [0, 0], "target": [0, 0] },
    { "id": "wave1", "rest": [60, 0], "target": { "keyframes": [
      { "time": 0, "value": [60, 0] }, { "time": 0.25, "value": [60, -12] },
      { "time": 0.75, "value": [60, 12] }, { "time": 1.25, "value": [60, 0] }
    ] } },
    { "id": "wave2", "rest": [120, 0], "target": { "keyframes": [
      { "time": 0, "value": [120, 0] }, { "time": 0.4, "value": [120, -20] },
      { "time": 0.9, "value": [120, 20] }, { "time": 1.4, "value": [120, 0] }
    ] } },
    { "id": "wave3", "rest": [180, 0], "target": { "keyframes": [
      { "time": 0, "value": [180, 0] }, { "time": 0.55, "value": [180, -27] },
      { "time": 1.05, "value": [180, 27] }, { "time": 1.55, "value": [180, 0] }
    ] } },
    { "id": "tip", "rest": [240, 0], "target": { "keyframes": [
      { "time": 0, "value": [240, 0] }, { "time": 0.7, "value": [240, -34] },
      { "time": 1.2, "value": [240, 34] }, { "time": 1.7, "value": [240, 0] }
    ] } }
  ]
}
```

## Squash a sticker corner

Put a media layer over a `mesh:auto` result or `grid: [8, 8]`. Hold two
corners, push the other corners inward, and ramp `mix` in and out so the same
rest graph and targets stay authored. For a 240×160 sticker:

```json
{
  "mesh": { "grid": [8, 8], "deformers": [{
    "type": "pins",
    "pins": [
      { "id": "topLeft", "rest": [0, 0], "target": [0, 0] },
      { "id": "bottomLeft", "rest": [0, 160], "target": [0, 160] },
      { "id": "topRight", "rest": [240, 0], "target": [218, 12] },
      { "id": "bottomRight", "rest": [240, 160], "target": [218, 148] }
    ],
    "mix": { "keyframes": [
      { "time": 0, "value": 0 }, { "time": 0.2, "value": 1 },
      { "time": 0.5, "value": 1 }, { "time": 0.75, "value": 0 }
    ] }
  }] }
}
```

## Bend, then place a free handle

Order matters: a later entry acts on the geometry moved by earlier entries.
The pin's `rest` stays in the authored coordinates. Here a bend turns the
base of a tail, then a pin places its tip; the pin target is expressed in the
bent pose's coordinates:

```json
"deformers": [
  { "type": "bend", "from": [0, 0], "to": [0, 60], "angle": 25,
    "min": -35, "max": 35 },
  { "type": "pins", "pins": [
    { "id": "root", "rest": [0, 0], "target": [0, 0] },
    { "id": "tip", "rest": [0, 120], "target": [30, 105] }
  ] }
]
```

## Refusals and preview

- `deformer_pins_empty`: add at least one pin.
- `deformer_pin_id_invalid` / `deformer_pin_id_duplicate`: give every pin a
  non-empty, unique `id` within its entry.
- `deformer_pin_rest_invalid` / `deformer_pin_rest_duplicate`: use finite
  content-local points that fit float32, and do not reuse a rest point.
- `deformer_pin_displacement_out_of_float_range`: reduce the target movement.
- `deformer_pin_rotation_undefined`: the targets collapse a local part so its
  orientation cannot be determined. Keep the controls separated through the
  motion, or use `skin`/`bend` to specify the intended articulation.
- A rest point outside the filled or stroked part cannot attach;
  move it onto that part. A rest point equal to its target still anchors it.
- On a layer hosting a look, expression-driven pin targets have unbounded
  reach (`look_mesh_deformer_unbounded`). Key the targets, or put the meshed
  layer in a composition and host the look on the composition layer.

Call `picsart_scene_validate` on the final scene, `picsart_scene_query_layout` at the rest
time and the largest bend, and `picsart_scene_contact_sheet` at the rest time, the
crest, the opposite crest and the layer end. Inspect the actual pixels for
pin accuracy, fill/stroke contact and independent parts. `picsart_scene_query_layout`
gives layer bounds; it does not replace a rendered check.

Also preview the motion between the two crests, especially where controls pass
through the center. The same time must give the same pose when playing forward,
backward or seeking directly. A firm head should move continuously through that
crossing; checking only the extreme poses will miss a snap between them.

## Keep the head firm while the body bends

Use one continuous head–neck–body outline, or one connected art mesh carrying the
whole drawing and its face. Separate painted islands stay separate; a stiffness
region does not join a detached head to the body. Facial marks belong to that
same mesh.

Start with three pins: a held body root, a moving neck, and a moving head tip.
Here the head is 130×120 px, centered at `[65, 60]`; the neck narrows to 30 px and
reaches `[65, 140]`, and the body ends at `[65, 330]`. Put this entry in the
continuous shape's `content.deformers` or the art mesh's `mesh.deformers`:

```json
{
  "type": "pins",
  "pins": [
    { "id": "root", "rest": [65, 330], "target": [65, 330] },
    { "id": "neck", "rest": [65, 140], "target": { "keyframes": [
      { "time": 0, "value": [65, 140] },
      { "time": 2, "value": [105, 155] },
      { "time": 4, "value": [65, 140] }
    ] } },
    { "id": "tip", "rest": [65, 0], "target": { "keyframes": [
      { "time": 0, "value": [65, 0] },
      { "time": 2, "value": [155, 30] },
      { "time": 4, "value": [65, 0] }
    ] } }
  ],
  "stiffnessRegions": [
    { "id": "head", "center": [65, 60], "radius": 70,
      "stiffness": 1, "falloff": 0 }
  ]
}
```

Choose the radius from the head's size: 70 px covers this head's widest 65 px
half-width and its rounded corners, reaches only to y=130, and leaves the lower
neck and the whole body free to bend. Start at `stiffness: 1` and `falloff: 0`
for a firm plateau across the head. Tune the region's coverage before reducing
stiffness. For a softer transition, try `falloff: 0.2`; its outer 20% fades,
while its inner 80% stays at full authored stiffness. Enlarge or reposition the
region if that fade reaches details that should remain firm, keeping it clear
of the body. `falloff` accepts 0..1, defaults to 1 (a fade across the entire
radius), and 0 keeps full influence through the radius's edge.

At the largest pose, compare head width, height, eye spacing and the mouth with
the rest frame; the firm panel should resist their distortion while the body
bends. All three pin positions must still match between panels. A firm head can
translate and turn: stiffness resists local stretch and does not anchor it or
guarantee perfect rigidity. To keep the head at a specific position, add a fixed
pin (`target` equals `rest`) there. Add more position pins when you need more
placement controls; use `skin` for bone-driven articulation and `bend` for a
joint. Conflicting position targets can still distort a stiff region.

## Region fields and coverage checks

Every region has a unique nonempty `id`, a finite float-range `center`, a positive
float-representable `radius`, `stiffness` in `[0, 1]`, and optional `falloff` in
`[0, 1]`. Fields are static; template parameters may bind constants. Do not put
keyframes, parameter tracks or time-dependent expressions on region fields. Animate
the pin targets and `mix` instead. A preceding deformer carries the center;
the radius remains the authored content-pixel radius. Overlapping regions use
the strongest influence rather than adding their strengths.

A positive-stiffness region must reach at least one existing edge midpoint with
positive influence after pin placement refines the rest graph. Otherwise graph
construction reports `deformer_pin_stiffness_region_empty`, even at rest or with
`mix: 0`. Enlarge or move the region onto the intended detail, or increase mesh
resolution when a small detail falls between edges. With a fading rim, merely
touching an edge midpoint at the radius does not give it positive influence;
`falloff: 0` includes that rim. The region creates no new edges and never joins
separate islands. `stiffness: 0` deliberately disables a region and bypasses the
empty-coverage check; omitting regions or using an empty list also keeps normal
behavior.

Run `picsart_scene_validate`, then query and render the scene so the geometry-dependent
coverage check runs. Inspect rest, both bend directions and the return pose;
layer bounds alone do not verify a firm face. Shape and art-mesh
deformers share the stiffness behavior; look/sprite source sizing accounts for
the same region falloff. Changing rest geometry or an unbounded target still
needs an explicit source region where required.
