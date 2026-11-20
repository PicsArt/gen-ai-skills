# Brick parts script

The Blender Python that builds one part of the [brick toy](brick-toy.md) style as one GLB. Copy the whole block
below, set its `PART` line, and pass it as `script` to `picsart_scene_build_model`; one call builds one part. On a
machine with Blender, run the same code there and export the scene as GLB.

- Sizes are 10 times real toy bricks, in metres: stud pitch 0.08, brick 0.096 (3 plates), plate 0.032, studs 0.048
  across and 0.017 tall with a rounded lip, every edge bevelled by 0.045 of a stud.
- Blender's -Y is the front (it exports as +z). Every part's origin is the centre of its base, except a `limb`,
  whose origin is its top, the joint it swings from.
- Every part has one material, `main` (the desk: `wood`); colour it per layer with `content.materials`.
- The model-building sandbox imports only `bpy`, `bmesh` and `math` and refuses file members such as
  `image.pack()`: keep any edit inside that.

| `PART` | Builds |
|---|---|
| `{"kind": "brick", "w": 2, "d": 4, "plates": 3, "studs": True}` | `w` studs across (x), `d` deep (z), `plates` high; `plates` 1 is a plate, `studs` False a tile |
| `{"kind": "round", "studs_across": 1, "plates": 3, "studs": True}` | a round brick, 1 or 2 studs across |
| `{"kind": "limb", "w": 1, "d": 1, "bricks": 3, "foot": True}` | a column of bricks hanging from its top, with a foot plate pointing forward |
| `{"kind": "desk", "width": 9, "depth": 6}` | a wooden desk top at y = 0, in metres |

```python
import math

import bmesh
import bpy

PART = {"kind": "brick", "w": 2, "d": 4, "plates": 3, "studs": True}

P, PH = 0.08, 0.032                  # stud pitch, plate height
SR, SH = 0.024, 0.017                # stud radius, stud height
BEV = 0.045 * P                      # edge bevel
GAP = 0.002                          # a part is this much smaller than its grid cell, so neighbours show a seam


def clear():
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)


def material(name):
    return bpy.data.materials.get(name) or bpy.data.materials.new(name)


def mesh_object(bm, m):
    me = bpy.data.meshes.new("part")
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new("part", me)
    bpy.context.collection.objects.link(o)
    me.materials.append(material(m))
    return o


def bevelled(o, width, segments=3):
    mod = o.modifiers.new("bevel", "BEVEL")
    mod.width, mod.segments, mod.limit_method = width, segments, "ANGLE"
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    bpy.ops.object.modifier_apply(modifier="bevel")
    o.select_set(False)
    return o


def box(sx, sy, sz, at, m="main"):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1)
    bmesh.ops.scale(bm, vec=(sx, sy, sz), verts=bm.verts)
    bmesh.ops.translate(bm, vec=(at[0], at[1], at[2] + sz / 2), verts=bm.verts)
    o = bevelled(mesh_object(bm, m), BEV)
    for p in o.data.polygons:
        p.use_smooth = False
    return o


def cylinder(r, h, at, m="main", segments=40, bevel=BEV):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=segments, radius1=r, radius2=r, depth=h)
    bmesh.ops.translate(bm, vec=(at[0], at[1], at[2] + h / 2), verts=bm.verts)
    o = bevelled(mesh_object(bm, m), bevel)
    for p in o.data.polygons:
        p.use_smooth = len(p.vertices) == 4      # smooth side, flat caps
    return o


def studs(w, d, z):
    # the small bevel on each stud's top edge is its lip
    return [cylinder(SR, SH, ((i - (w - 1) / 2) * P, (j - (d - 1) / 2) * P, z), segments=32, bevel=0.0022)
            for i in range(w) for j in range(d)]


def brick(w, d, plates, top=True, z0=0.0):
    h = plates * PH
    parts = [box(w * P - GAP, d * P - GAP, h, (0, 0, z0))]
    return parts + (studs(w, d, z0 + h) if top else [])


def round_brick(n, plates, top=True):
    h = plates * PH
    parts = [cylinder(n * P / 2 - GAP / 2, h, (0, 0, 0))]
    return parts + (studs(n, n, h) if top else [])


def limb(w, d, bricks, foot):
    parts = []
    for k in range(bricks):
        parts += brick(w, d, 3, False, -3 * PH * (k + 1))
    if foot:
        parts.append(box(w * P - GAP, (d + 1) * P - GAP, PH, (0, -P / 2, -3 * PH * bricks - PH)))
    return parts


def desk(width, depth):
    # wood grain in plain Python (the stage sandbox imports only bpy, bmesh and math)
    W, H = 1024, 512
    rnd = [0.37, 0.81, 0.13, 0.66, 0.29, 0.92]
    dark, light = (0.30, 0.16, 0.07), (0.62, 0.40, 0.22)
    px = [0.0] * (W * H * 4)
    for r in range(H):
        y = r / (H - 1)
        for c in range(W):
            x = c / (W - 1)
            warp = sum(math.sin(2 * math.pi * (f * y + rnd[i]) + 3 * x * rnd[i + 3]) / f
                       for i, f in enumerate((1, 2.3, 5.1)))
            rings = 0.5 + 0.5 * math.sin(2 * math.pi * (38 * y + 0.9 * warp + 0.15 * math.sin(9 * x)))
            fine = 0.25 * math.sin(2 * math.pi * 260 * y + 4 * warp) + 0.12
            t = min(1.0, max(0.0, 0.55 * rings + 0.3 * fine + 0.15))
            k = (r * W + c) * 4
            for ch in range(3):
                px[k + ch] = (dark[ch] + (light[ch] - dark[ch]) * t) ** 2.2
            px[k + 3] = 1.0
    img = bpy.data.images.new("wood", W, H)
    img.pixels.foreach_set(px)
    bpy.ops.mesh.primitive_plane_add(size=1)
    o = bpy.context.active_object
    o.scale = (width, depth, 1)
    o.location = (0, -depth / 6, 0)               # more desk behind the subject than in front of it
    bpy.ops.object.transform_apply(scale=True, location=True)
    m = material("wood")
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    tex = m.node_tree.nodes.new("ShaderNodeTexImage")
    tex.image = img
    m.node_tree.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.6
    o.data.materials.append(m)
    return [o]


def build(part):
    kind = part["kind"]
    if kind == "brick":
        return brick(part.get("w", 2), part.get("d", 4), part.get("plates", 3), part.get("studs", True))
    if kind == "round":
        return round_brick(part.get("studs_across", 1), part.get("plates", 3), part.get("studs", True))
    if kind == "limb":
        return limb(part.get("w", 1), part.get("d", 1), part.get("bricks", 3), part.get("foot", True))
    if kind == "desk":
        return desk(part.get("width", 9), part.get("depth", 6))
    raise ValueError(f"unknown part kind {kind!r}: brick, round, limb or desk")


clear()
objs = build(PART)
for o in bpy.context.collection.objects:
    o.select_set(o in objs)
bpy.context.view_layer.objects.active = objs[0]
if len(objs) > 1:
    bpy.ops.object.join()
bpy.context.view_layer.objects.active.name = PART["kind"]
```
