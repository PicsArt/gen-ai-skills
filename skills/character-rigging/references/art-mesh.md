# Bending a picture: the art mesh and live pins

Part of the `character-rigging` skill. Read it when a `media`, `text` or composition layer has to bend, or a flag, tail, ear or sticker corner needs free handles.

## Contents

- The art mesh (vertices and triangles, grid, mesh from transparency, deformers, points and morphs, warp, mix, draw order, looks)
- Live position pins on shapes and art meshes

## The art mesh

A layer's `mesh` draws its content over triangles, so a picture with no outline — `media`, `text`, a
`shape`'s rendered ink, a `composition` with its own `composition` size, a `scene_ref` — bends.

- **`vertices` + `triangles`.** Each vertex has a `point`, where it draws, and an optional `uv`, the
  spot of the content it shows; both are content-local px, and `uv` defaults to `point`.
  For an image, [0,0] is the image's top-left. For a shape layer, [0,0] is the shape's
  authored drawing origin, the same coordinate system as its paths after any shape-group
  transforms. It is not the rendered bounding box's top-left or the layer's anchor. For
  example, a path spanning x=-30..30 keeps those x values in mesh `point` and `uv`; do not
  shift them to 0..60. The layer transform places this whole drawing afterward. A triangle is `[a, b, c]`, three different vertex indices with area at rest.
  Triangles draw in list order: a later one covers an earlier one where they overlap.
- **`grid: [cols, rows]`.** A regular grid, two triangles a cell, over the bounds the content draws.
  At rest it draws exactly the plain layer.
- **Mesh from transparency → `picsart_scene_apply_preset` with `preset` `mesh:auto`.** On a cut-out image
  layer it writes `vertices` + `triangles` that follow the visible outline, holes kept, into its `mesh`
  (`params`: `spacing`, `margin`); then move outline points to bend.

The picture bends where a vertex's `point` differs from its `uv`. A `uv` outside the content shows
nothing there, so a triangle can crop as well as bend.

```json
{ "id": "sticker", "content": { "kind": "media", "assetId": "cat" },
  "mesh": {
    "vertices": [
      { "point": [0, 0] }, { "point": [400, 0] }, { "point": [400, 300] }, { "point": [0, 300] },
      { "point": [200, 120], "uv": [200, 150] }
    ],
    "triangles": [[0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4]]
  } }
```
The centre of a 400×300 image draws 30 px higher than it sits, and the edges stay put: a bulge.

- The rest `vertices`, `uv`s and `triangles` are fixed data. To bend over
  time, give the mesh `deformers`: the same `bend` / `push` / `stretch` list a `shape` content
  carries, with the same animatable fields, acting on the mesh's points in content px (a grid's
  once laid) while every `uv` stays put. Triangles stay straight between points, so give a bending
  part a fine grid (`grid: [4, 16]` for a tail). A tail painted along +y from its root at the top:
  ```json
  "mesh": { "grid": [4, 16], "deformers": [
    { "type": "bend", "from": [60, 20], "to": [60, 300], "falloff": 1,
      "angle": { "expression": "return 25 * math.sin(time * 4)" } } ] }
  ```
- **Moving the points themselves → `points` / `morphs`** (explicit `vertices` only, not a
  `grid`): the path's `vertices` and `morphs` spellings, one `{ point }` per mesh vertex in order,
  no handles, `uv`s kept. A head turn keys whole point lists `by` a `turn` dial; a smile is a morph
  target whose `weight` an expression or a dial drives:
  ```json
  "mesh": { "vertices": [...], "triangles": [...],
    "points": { "by": "turn", "keyframes": [
      { "at": -1, "value": [/* the points turned left */] }, { "at": 0, "value": [/* rest */] },
      { "at": 1, "value": [/* turned right */] } ] },
    "morphs": { "smile": { "offsets": [{}, {}, { "point": [0, -10] }, { "point": [0, -10] }], "weight": 0.5 } } }
  ```
  `points` first, then `morphs`, then `deformers` on the result.
- **Time-keyed per-vertex deformation uses the same path spelling.** Keep the rest mesh fixed and
  key a vertex's `point` inside `mesh.points`. This is an absolute content-local position; use
  `morphs.<name>.offsets` with a keyed `weight` for additive deform offsets, exactly as on a path.
  UVs and triangle indices stay fixed. Every key keeps the same number and order of points.
  ```json
  "points": [{"point":[0,0]},
    {"point":{"keyframes":[{"time":0,"value":[200,0]}, {"time":1,"value":[240,-40]}]}},
    {"point":[200,200]}, {"point":[0,200]}],
  "morphs":{"tip":{"offsets":[{},{},{"point":[20,-30]},{}],
    "weight":{"keyframes":[{"time":0,"value":0},{"time":1,"value":1}]}}}
  ```
  Coordinates and offsets are finite px; morph weights are ordinary numbers (0..1 for a rest-to-target
  blend, extrapolation allowed). A mesh has no Bezier handles. For a vector outline, use the same
  point tracks in the path's `vertices` and the same `morphs`. Playback and seeking evaluate these
  tracks directly; they do not accumulate frame to frame.
- **Broad bends → `warp`** (mesh only): a lattice over the content's bounds, one offset per
  lattice corner, row by row (corner `(col, row)` at index `row * (cols + 1) + col`); every point
  moves by the blend of its cell's corners. A body slim: a
  `[2, 1]` lattice whose side corners pull toward the middle, keyed `by` a `slim` dial:
  ```json
  "mesh": { "grid": [8, 12], "deformers": [
    { "type": "warp", "grid": [2, 1], "offsets": { "by": "slim", "keyframes": [
      { "at": 0, "value": [{}, {}, {}, {}, {}, {}] },
      { "at": 1, "value": [{ "point": [12, 0] }, {}, { "point": [-12, 0] },
                           { "point": [12, 0] }, {}, { "point": [-12, 0] }] } ] } } ] }
  ```
  The lattice spans the whole picture, background included: what surrounds the body bends with it.
  Use `bend` for a joint, `skin` for a body driven by bone layers, `push` for a local dent, `pins` for
  free handles such as a flag tip or ear, and `warp` for a broad reshape; a finer `grid` on the
  mesh keeps the reshape smooth. What the lattice covers moves, the rest stays. By default it covers the content's bounds and the mesh's own points, so every vertex moves; a fixed `region: [x, y, w, h]` restricts or widens it.
- **A deformer for a moment → its `mix`.** Any entry, on a shape's `deformers` or a mesh's (a `skin` included),
  takes `mix`, 0..1, default 1: 0 at rest, 1 in full, typed as a constraint's `mix` (static, keyframes, an
  expression or keys `by` a dial). A gust that bends a tree for two seconds, with no keyframes on the bend:
  ```json
  { "type": "bend", "from": [0, 120], "to": [0, 220], "angle": 25,
    "mix": { "keyframes": [{ "time": 1, "value": 0 }, { "time": 1.4, "value": 1 }, { "time": 2.6, "value": 1 }, { "time": 3, "value": 0 }] } }
  ```
  The `mix` scales whatever drives the entry; a limited bend's `min`/`max` bound the angle first. A `skin`'s
  `mix` takes that share of each bone's turn and stretch, with each bone's pivot riding its parent's share, so a
  half-mixed limb bends half as far at every joint and stays joined. An `ik` limb's
  entries take none, the joint included: the ik's own `mix` fades it.
- Order: the content and its `contentEffects` bend together; the layer's `mask` clips the bent
  picture and its `effects` (a drop shadow included) draw on it. A mask clip can carry a mesh too.
- A layer hosting a `looks` entry keeps the whole bent picture: the look's source grows to where the
  points can reach. An offset driven by an expression (a point, a morph weight, a warp or push
  offset, a stretch factor) has no such bound and is refused (`look_mesh_deformer_unbounded`): key
  it, or put the meshed layer in a composition and apply the look to that composition's layer.
  An expression reading the layer through `ctx` (`ctx.layer`, `ctx:getLayer`) is refused too
  (`look_host_expression_context`): the look draws the mesh on a copy at identity. A parameter read
  (`ctx.composition:getParameters()`) answers the same there.
- Check a bend on `picsart_scene_contact_sheet` frames at rest and at each extreme.

## Live position pins on shapes and art meshes

Use `pins` for free handles on a flag, tail, ear, hair lock or sticker corner. A pin whose `rest`
equals `target` is a hold, so put one at the fixed root. Use `bend` for a limb's joint and its
`min`/`max` or an `ik` solve: pins have neither an angle limit nor an IK joint. Use `skin` when a
body follows bone layers. The humanoid rig templates therefore use `bend`/`ik` on arms and legs
and `skin` on the torso; pin accessories and soft parts that need freely placed handles.
For a firm head on a bending body, use `stiffnessRegions` to resist local stretch, a fixed pin to
hold a position, more pins to place more controls, and `skin`/`bend` for bone or joint articulation.

Put one `pins` entry in a drawn shape's `content.deformers` or a layer's `mesh.deformers`; raster
`media` and `text` need the mesh path. `rest` is in content-local px and `target` can be keyed or
expressed. Shape fill and stroke share the solve; separate painted parts remain separate. Mesh
UVs remain fixed. A later deformer acts on the geometry posed by earlier entries. Read
`references/live-pins.md` for worked recipes including a firm head on a bending body, rest-point placement, diagnostic
codes, look-host limits and the exact validation, query and preview tools.

