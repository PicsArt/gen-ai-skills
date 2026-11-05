# Explicit skin weights

Use explicit weights when importing a character mesh, painting which bones move a sleeve,
or making a vector limb follow the same influences as image art. Put `weights` on the
`skin` entry in `content.deformers` for a shape, or `mesh.deformers` for an art mesh.
Without `weights`, skin keeps its automatic radius falloff.

## Place the bones and drawing in the same rest pose

`bones[].layer` names a bone layer in the same composition. Bone positions are ordinary
layer positions: `transform.position` is in the parent's coordinates, or composition
coordinates for a root. The bone starts at its `transform.anchor`; an optional `end` is
in that bone layer's own coordinates. These are not positions to copy directly from a
shape vertex unless the bone and drawing already share an origin and scale.

The binding converts each bone's static `transform` and `transforms[]` through its parent
chain into the skinned drawing's content coordinates. Shape points use the authored
shape origin; mesh points use the content origin described in [art-mesh.md](art-mesh.md).
Align the bone pivots with the joint locations in that rest pose, then animate the bones
away from it. For example, a shape at [200,60] with anchor [0,0] and an elbow at drawing
point [0,120] needs its elbow pivot at composition [200,180]. The example below gets this
by parenting the forearm at [0,120] to an upper arm at [200,60].

## Give every point its share of the bones

Each `weights` row belongs to one authored mesh vertex, or one shape outline point.
Shape numbering is exactly the numbering used by `target.point`: paths in item order,
depth-first inside groups, with reversed paths flipped. There is only one numbering.
Each row lists `{ "layer": "bone-layer-id", "weight": 0.5 }` entries naming this skin's
bones. Weights are finite, nonnegative, with a positive total; each row is normalized.
Five or more influences are supported. Unknown or duplicate bones, empty rows, zero totals
and the wrong row count are errors. `radius` and `falloff` are refused with explicit
weights; `end` is optional.

An importer may add a literal `bindOffset: [x,y]` to an influence (default [0,0]): a
rest-space bind displacement from the drawn point in the vertex's own units (mesh.points
units or shape control-vertex units). Never author it by hand; Live2D does not use it. The
normalized weighted mean of every row must be zero within 0.001 units or `skin_offset_mean`
refuses it: rescale the row's offsets or drop them. No tracks or `$eval` are supported.
Handles follow the blended linear transform only; `mix` scales the displacement with the
rest of the skin.

**Spread the blend across the joint.** A single cross-section of 50/50 weights at a bend
of angle θ narrows to cos(θ/2) of its rest width under the two bones' blended rotations.
At 90°, the measured 60 px limb narrowed to about 42 px and folded on the inner side,
leaving a roughly 20 px notch. Blend over about one limb width with at least three
cross-sections of graded weights. Extra weight entries cannot add missing vertices.
This softens the transition; it does not make linear skinning preserve volume.

This shape is 60 px wide. Its elbow is at y=120, with a 60 px blend band from y=90 to 150
and three mixed cross-sections at y=105, 120 and 135. Points go down the right edge and
back up the left, so the weight rows follow the perimeter, one row per point in order:

```json
{ "version": "1.0", "composition": { "width": 480, "height": 360, "fps": 30, "duration": 2 },
  "layers": [
    { "id": "upperArm", "content": { "kind": "empty" },
      "transform": { "position": [200, 60], "anchor": [0, 0] } },
    { "id": "forearm", "parentId": "upperArm", "content": { "kind": "empty" },
      "transform": { "position": [0, 120], "anchor": [0, 0], "rotation": 0 },
      "animations": { "rotation": { "keyframes": [
        { "time": 0, "value": 0, "easing": "ease_in_out" }, { "time": 1, "value": 90 }, { "time": 2, "value": 90 } ] } } },
    { "id": "arm", "transform": { "position": [200, 60], "anchor": [0, 0] },
      "content": { "kind": "shape",
        "items": [
          { "type": "path", "closed": true, "vertices": [
            { "point": [30, 0] }, { "point": [30, 90] }, { "point": [30, 105] }, { "point": [30, 120] },
            { "point": [30, 135] }, { "point": [30, 150] }, { "point": [30, 240] },
            { "point": [-30, 240] }, { "point": [-30, 150] }, { "point": [-30, 135] }, { "point": [-30, 120] },
            { "point": [-30, 105] }, { "point": [-30, 90] }, { "point": [-30, 0] } ] },
          { "type": "fill", "color": "#40d8b0" } ],
        "deformers": [{ "type": "skin",
          "bones": [{ "layer": "upperArm" }, { "layer": "forearm" }],
          "weights": [
            [{ "layer": "upperArm", "weight": 1 }],
            [{ "layer": "upperArm", "weight": 1 }],
            [{ "layer": "upperArm", "weight": 0.75 }, { "layer": "forearm", "weight": 0.25 }],
            [{ "layer": "upperArm", "weight": 0.5 }, { "layer": "forearm", "weight": 0.5 }],
            [{ "layer": "upperArm", "weight": 0.25 }, { "layer": "forearm", "weight": 0.75 }],
            [{ "layer": "forearm", "weight": 1 }],
            [{ "layer": "forearm", "weight": 1 }],
            [{ "layer": "forearm", "weight": 1 }],
            [{ "layer": "forearm", "weight": 1 }],
            [{ "layer": "upperArm", "weight": 0.25 }, { "layer": "forearm", "weight": 0.75 }],
            [{ "layer": "upperArm", "weight": 0.5 }, { "layer": "forearm", "weight": 0.5 }],
            [{ "layer": "upperArm", "weight": 0.75 }, { "layer": "forearm", "weight": 0.25 }],
            [{ "layer": "upperArm", "weight": 1 }],
            [{ "layer": "upperArm", "weight": 1 }] ] }] } } ] }
```

For a mesh, use the same graded shares, ordered to match `mesh.vertices` instead of the
shape perimeter, and connect neighboring cross-sections with triangles. Check it with
`picsart_scene_validate`, then render the bend with `picsart_scene_contact_sheet` at the
intermediate poses as well as the final angle.

## Controls, cost and limits

- Weights range from 0 upward; only their normalized ratio matters. `mix` is 0..1
  (default 1), blending the posed drawing with its rest pose. Intermediate `mix` can
  also shrink a rotated limb. Handles follow their vertex's blend, so curves move too.
- Import weights from another rig tool, paint them per vertex, or start from a
  radius/falloff seed and edit it. Persist that seed as explicit rows and omit
  radius/falloff from the bones. Cost grows with vertex count × influences per row;
  omit zero influences and bones that do not affect the point.
- Supported shape items are paths, nested groups, fills/strokes and gradient paints.
  Keep every pose's point count fixed. Whole-outline `vertices` keys, per-point tracks
  and morph offsets keep the same row identities. Parametric generators and shape
  modifiers that change topology are refused.
- Explicit shape skin must be its only deformer. Explicit mesh skin runs after
  `points`/`morphs` and earlier ordinary deformers, must be last, and cannot share a
  list with pins. Shape curves are deformed at their control points before flattening;
  an earlier nonlinear deformer needs bindings on the extra curve samples to keep its
  result.
- Indexed outline point/tangent queries and attachments follow the posed controls.
  Use `target.point` for attachments. Arbitrary-position attach/aim targets, an IK end,
  and look reach on explicit skin are refused in validation and resolution because they
  do not identify a weight row. Bounds and hit queries use the posed geometry.
