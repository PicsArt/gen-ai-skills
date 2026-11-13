# A detailed model from your own Blender script

`picsart_scene_build_model` with `script` runs your Blender Python in an empty scene and returns
what it built as one GLB. There is no cap on triangles, vertices or script length: build the
model as detailed as the shot needs. A model that holds up close is usually a few hundred
thousand to a million triangles. The build has the real limits of its machine: about 600 s, your
script running on one core, 12 GB of memory and 4 GB of disk. A 450k-triangle locomotive with
modifiers took about 150 s; a rocket whose script ran hand-rolled bmesh loops over a large mesh took
over 800 s and failed. Let modifiers and `bmesh.ops` do the heavy work, keep segment counts to what
the shot shows, and try a cut-down version first when a build is large. The job runs async, so
poll it with `picsart_job_status`. Its progress
reads 5 while your script runs, 45 while the model exports and 85 once it is exported.

A long script need not pass through your context. With a shell, write it to a `.py` file and upload
it with `picsart_upload_local_files` (`type: "script"`), then pass the URL it prints as `scriptUrl` instead of
`script`; after an edit, upload the file again. A script already at a public https URL goes
straight into `scriptUrl`; the server fetches it.

The finished model's `report` gives its `vertices`, `triangles`, `meshes`, `materials` and `bytes`,
and its `log` holds the end of the build's output, where your script's `print` lines land.
The build saves nothing: place its `url` as the `model` asset, and save the one you keep with
`picsart_scene_library_save` (`jobId` and a `name`). A build that outlasted the wait answers its model
when `picsart_scene_build_model` is called with only `jobId` (the receipt's `job.id`).

## What the script may use

- `bpy`, `bmesh`, `math`, `mathutils` and `random` only. No rendering, importing, exporting or
  file operations: the server exports, without your lights or cameras (the scene brings them).
- Modifiers (bevel, subdivision, array, mirror, solidify, boolean, ...), `bmesh` operators,
  materials and UVs. Every modifier left on an object is applied by the export.
- Not available: `eval`, `exec`, `type`, `globals` and similar builtins. Seed `random` so the same
  script builds the same model.

## Plan the model as parts

1. **Measure first.** Pick real proportions in metres before writing code (a standard-gauge
   locomotive: wheels 1.5 m across, boiler about 1.2 m, cab roof about 3 m above the rail).
   Write them as named constants, and place every part from them, never by eye.
2. **Axes.** Blender is +Z up; the export turns it to the scene's +Y up. Put the model's
   front along +X and its base at Z = 0 so it stands on the floor.
3. **One object per material and part.** Boiler, bands, rivets, wheels, rods: each its own
   object with one material. Its name is what `content.materials` overrides later.
4. **Build big to small.** Main volumes (body, boiler, cab), then the parts that make it read
   as the real thing (wheels with spokes, rods, domes, chimney), then the fine detail the light
   catches (rivets, bands, handrails, pipes, steps, lamp irons). The fine detail is what turns a
   toy into a model.

## Build with bmesh, not bpy.ops in loops

`bpy.ops` calls are slow and depend on context; a loop of thousands of them can exhaust the
time budget. Build each part in a `bmesh` and write it to one mesh:

```python
import bpy, bmesh, math
from mathutils import Matrix, Vector

def make(name, bm, mat, smooth_deg=35):
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    mesh.materials.append(mat)
    mesh.shade_smooth()
    mesh.set_sharp_from_angle(angle=math.radians(smooth_deg))  # smooth curves, crisp edges
    return obj

bm = bmesh.new()
for i in range(60):  # a ring of rivets: 60 spheres, one object
    a = 2 * math.pi * i / 60
    bmesh.ops.create_uvsphere(bm, u_segments=12, v_segments=8, radius=0.008,
                              matrix=Matrix.Translation((0.5, 0.6 * math.cos(a), 1.85 + 0.6 * math.sin(a))))
make("boiler_rivets", bm, green)
```

- Primitives take a `matrix` (translation @ rotation @ scale): `create_cube`, `create_cone`
  (cylinders and tapers), `create_uvsphere`, `create_icosphere`.
- **Turned parts** (domes, chimneys, wheels' tyres and flanges, buffers, lamps) are a profile
  revolved with `bmesh.ops.spin`: write the (radius, height) outline and spin it 360 degrees with
  `use_merge=True`. This is the fastest way to a part that looks machined.
- When several pieces go into one bmesh, **transform only the vertices you just made**
  (`before = set(bm.verts)` ... `new = [v for v in bm.verts if v not in before]`). Transforming
  `bm.verts` moves every earlier piece again and scatters the model.
- Repeated detail (rivets, spokes, bolts, coal lumps) goes into one object in a loop. Thousands
  of separate objects make a heavy scene.

## Edges, curves and cuts

- **Bevel** catches the light on edges: `obj.modifiers.new("bevel", "BEVEL")` with a width of
  5 to 15 mm, 2 to 3 segments and `limit_method = "ANGLE"`. Without it, edges look like CG.
- **Subdivision** (level 1 or 2) on organic or cast shapes (domes, chimney caps, handles).
- **Booleans** cut windows, holes and recesses. Apply the boolean in the script and delete the
  cutter, or the cutter is exported as a solid:

  ```python
  cut = cab.modifiers.new("windows", "BOOLEAN")
  cut.object, cut.operation, cut.use_self = cutters, "DIFFERENCE", True
  bpy.context.view_layer.objects.active = cab
  bpy.ops.object.modifier_apply(modifier="windows")
  bpy.data.objects.remove(cutters)
  ```

  The object being cut must be closed and must not overlap itself (shells that meet should meet,
  not intersect). Apply the boolean before adding a bevel to the same object.

## Materials that survive the export

The GLB carries a Principled BSDF's **Base Color, Metallic, Roughness, Emission** and image
textures. Procedural texture nodes (noise, musgrave) do not export: get variation from geometry,
from separate materials, or from an image built with `bpy.data.images.new` and its pixels.

| Look | Base color (linear) | Metallic | Roughness |
|---|---|---|---|
| Gloss paint (livery green) | 0.012, 0.09, 0.035 | 0 | 0.28 |
| Gloss black | 0.012, 0.012, 0.014 | 0 | 0.32 |
| Brass | 0.80, 0.56, 0.20 | 1 | 0.22 |
| Bright steel | 0.62, 0.63, 0.65 | 1 | 0.28 |
| Cast iron | 0.10, 0.10, 0.11 | 0.8 | 0.55 |
| Glass | 0.25, 0.32, 0.35 | 0 | 0.05 |

A lamp lens or screen gets an emission colour and strength. Contrast between materials (gloss
paint, bright metal, dull iron) is what makes the model read as real under the scene's light.

## Check it before building on it

Look at it with `picsart_scene_preview_model` from at least two sides (for example yaw 40 and
yaw -140), then in a lit scene. Look for:

- **Floating or misplaced parts**: steps, rivets or rods with nothing holding them.
- **Pieces pushed through each other**: a roof below the walls, a part inside another.
- **Mirrored detail on the wrong side**: a wheel flange faces the track centre on both sides.
- **Missing faces or open ends**, and a cutter still visible.

Fix in the script and build again. A refusal or the script's own error comes back with its line.
