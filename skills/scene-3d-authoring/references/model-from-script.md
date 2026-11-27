# A detailed model from your own script

`picsart_scene_build_model` with `script` builds your model in an empty scene and returns it as
one GLB. The script is a short list of calls, one per line: you make shapes, move them, join
them and give them materials. It is not Python. A script that breaks a rule is refused before
anything is built, and you fix the line it names (see "When a script is refused").

The job runs async, so poll it with `picsart_job_status`. A build that outlasted the wait
answers its model when `picsart_scene_build_model` is called with only `jobId` (the receipt's
`job.id`).

The finished model's `report` gives its `vertices`, `triangles`, `meshes`, `materials` and `bytes`.
The build saves nothing: place its `url` as the `model` asset, and save the one you keep with
`picsart_scene_library_save` (`jobId` and a `name`).

## Contents

- The script form
- Limits
- The calls
- When a script is refused
- Plan the model as parts
- Edges, curves and cuts
- Materials that survive the export
- A worked example
- Check it before building on it

## The script form

- One statement per line, in one of three forms: `x = call(...)`, `call(...)` or
  `x.attr = literal`.
- Not allowed: imports, loops, `if`, functions, classes, arithmetic (`a + b`, `2 * x`),
  indexing, f-strings, comprehensions, method calls and `print`. Write each number out.
- Calls come from a fixed list (below). Each parameter has a type and a range.
- Arguments are keywords: `cube(size=1, location=(0, 0, 0.45))`. Positional ones also work, in the
  order the parameters are listed.
- A name (`x`) is lowercase letters, digits and `_`, starting with a letter, up to 40 characters.
- A value is a number, text, `True`, `False`, `None`, a list or tuple of values, or a name made
  earlier. A list of objects is all names or all values, never mixed.
- Lengths are metres, rotations are degrees. A color is `(r, g, b)` with each from 0 to 1, or
  `"#rrggbb"`.
- Text is at most 256 characters and cannot hold slashes, backslashes, colons, `..`, `__` or
  control characters. An object or material name is 1 to 63 characters.
- A line that starts with `#` is a comment.

## Limits

- At most 2000 statements.
- At most 2000 objects (copies and joins count).
- At most 1,000,000 faces in one object, and 2,000,000 in the whole script.
- Every number is at most 1,000,000 in absolute value, and each parameter has its own range.
  Location and size values stay within 1000.
- At most 20,000 items in one list, and lists nest 3 deep.
- Deleting an object does not give its faces back.

## The calls

Shapes (each returns an object, and takes `location`, `rotation`, `scale` and `name`):

- `cube(size)`, `plane(size)`, `circle(radius, vertices, fill)`
- `cylinder(radius, depth, vertices, cap_ends)`, `cone(radius1, radius2, depth, vertices, cap_ends)`
  (a cone with a second radius is a taper)
- `uv_sphere(radius, segments, ring_count)`, `ico_sphere(radius, subdivisions)`
- `torus(major_radius, minor_radius, major_segments, minor_segments)`
- `text(body, size, extrude)`: text as geometry, up to 200 characters
- `curve(points, bevel_depth, bevel_resolution, cyclic)`: a line through 2 to 2000 points, thickened by the bevel
- `mesh(vertices, faces)`: your own geometry from vertex positions and faces (each face 3 to 64 vertex indices)

Working with objects:

- `duplicate(obj, location, rotation, scale, name)`: a copy at an absolute transform
- `join(objects=[a, b, c])`: up to 64 objects into one new object
- `boolean(obj, cutter, operation, keep_cutter)`: `operation` is `"difference"` (the default),
  `"union"` or `"intersect"`; returns the result
- `apply_transform(obj, location, rotation, scale)`: absolute values
- `parent(child, parent)`, `delete(obj)`
- `modifier(obj, kind, ...)` and `apply_modifiers(obj)`
- `shade_smooth(obj, auto_angle)` and `shade_flat(obj)`

Materials:

- `material(name, base_color, roughness, metallic, emission_color, emission_strength, alpha, coat_weight, coat_roughness, texture, texture_scale)`
- `assign(obj, mat)`

Animation, if the model needs it: `fps(value)`, `frame_range(start, end)` and
`keyframe(obj, path, frame, value)`, where `path` is `"location"`, `"rotation"` or `"scale"`.

Setters, written `name.attr = value`:

- an object: `location`, `rotation`, `scale`, `dimensions`, `name`
- a material: `base_color`, `roughness`, `metallic`, `emission_color`, `emission_strength`,
  `alpha`, `coat_weight`, `coat_roughness`, `name`
- a modifier: the settings of its kind

Modifier kinds and their settings (`modifier(obj=x, kind="BEVEL", width=0.01)`):

| Kind | Settings |
|---|---|
| `BEVEL` | `width` 0.001 to 1, `segments` 1 to 8, `limit_method` (`"NONE"`, `"ANGLE"`, `"WEIGHT"`), `angle` 0 to 180 |
| `SUBSURF` | `levels` 0 to 2, `render_levels` 0 to 2 |
| `ARRAY` | `count` 1 to 50, `relative_offset` (3 numbers, -10 to 10) |
| `MIRROR` | `x`, `y`, `z` (True or False) |
| `SOLIDIFY` | `thickness` 0.001 to 1, `offset` -1 to 1 |
| `SMOOTH` | `factor` 0 to 2, `iterations` 1 to 30 |
| `DECIMATE` | `ratio` 0.01 to 1 |
| `SIMPLE_DEFORM` | `method` (`"TWIST"`, `"BEND"`, `"TAPER"`, `"STRETCH"`), `angle`, `factor`, `axis` |
| `WEIGHTED_NORMAL` | `keep_sharp` |

Any other kind is refused. Every modifier left on an object is applied by the export.

## When a script is refused

A script that breaks a rule comes back refused, with three things: the **line number**, the
**rule** it broke and a **hint** on what to write instead. Nothing is built and nothing is charged
for it. Fix that line and call again. Fix one line at a time: the next refusal names the next
line. Typical causes are a loop, arithmetic, a function that is not in the list above, a number
outside its range, or a count over a limit.

## Plan the model as parts

1. **Measure first.** Pick real proportions in metres before writing the script (a chair: seat
   0.45 m high, 0.45 m square). Place every part from those numbers, never by eye.
2. **Axes.** Blender is +Z up; the export turns it to the scene's +Y up. Put the model's
   front along +X and its base at Z = 0 so it stands on the floor.
3. **One object per material and part.** Seat, legs, backrest: each its own object with one
   material, named with `name=`. That name is what `content.materials` overrides later.
4. **Build big to small.** Main volumes first, then the parts that make it read as the real
   thing, then the fine detail the light catches (bevels, bolts, rails, trim).
5. **Repeat by writing it out.** There are no loops. Make one part, then `duplicate` it at each
   position, one line each. For an evenly spaced row, use an `ARRAY` modifier (up to 50 copies).
   Join the copies into one object when you are done, so the scene stays light.

## Edges, curves and cuts

- **Bevel** catches the light on edges: a `BEVEL` modifier with a width of 0.005 to 0.015 m, 2 to 3
  segments and `limit_method="ANGLE"`. Without it, edges look like CG.
- **Subdivision** (level 1 or 2) on organic or cast shapes.
- **Round parts** (legs, domes, handles) come from `cylinder`, `cone`, `uv_sphere`, `torus`, or a
  `curve` with a `bevel_depth`. Use `mesh` for a shape none of them make.
- **Booleans** cut windows, holes and recesses. `boolean` returns the cut object, and the cutter
  is removed unless you pass `keep_cutter=True`:

  ```
  body = cube(size=1, location=(0, 0, 0.5), scale=(1.0, 0.6, 0.5), name="body")
  hole = cylinder(radius=0.1, depth=1, location=(0, 0, 0.5), rotation=(90, 0, 0))
  body = boolean(obj=body, cutter=hole)
  ```

  The object being cut must be closed and must not overlap itself. Cut before adding a bevel
  to the same object.

## Materials that survive the export

The GLB carries a Principled BSDF's **base color, metallic, roughness, emission** and image
textures. Get variation from geometry or from separate materials.

A real image (a photo, a decal, a label, a generated texture) goes in as `textures`: names to public
https PNG, JPEG or WebP URLs, such as Drive or generation results:
`"textures": {"concrete": "https://…/concrete.jpg"}`. A material uses one by its name with
`material(texture="concrete", texture_scale=2)`; the GLB embeds it. A name is 1 to 64 of
`a-z`, `0-9`, `_` and `-`.

| Look | Base color | Metallic | Roughness |
|---|---|---|---|
| Gloss paint (livery green) | 0.012, 0.09, 0.035 | 0 | 0.28 |
| Gloss black | 0.012, 0.012, 0.014 | 0 | 0.32 |
| Brass | 0.80, 0.56, 0.20 | 1 | 0.22 |
| Bright steel | 0.62, 0.63, 0.65 | 1 | 0.28 |
| Cast iron | 0.10, 0.10, 0.11 | 0.8 | 0.55 |
| Glass | 0.25, 0.32, 0.35 | 0 | 0.05 |

A lamp lens or screen gets an `emission_color` and an `emission_strength`. Contrast between
materials (gloss paint, bright metal, dull iron) is what makes the model read as real under the
scene's light.

## A worked example

A chair: four legs, a seat and a backrest, joined into one object with one material.

```
seat = cube(size=1, location=(0, 0, 0.45), scale=(0.45, 0.45, 0.04), name="seat")
leg1 = cylinder(radius=0.025, depth=0.43, vertices=16, location=(0.19, 0.19, 0.215))
leg2 = duplicate(obj=leg1, location=(0.19, -0.19, 0.215))
leg3 = duplicate(obj=leg1, location=(-0.19, 0.19, 0.215))
leg4 = duplicate(obj=leg1, location=(-0.19, -0.19, 0.215))
back = cube(size=1, location=(-0.2, 0, 0.75), scale=(0.04, 0.45, 0.45), name="back")
chair = join(objects=[seat, leg1, leg2, leg3, leg4, back])
modifier(obj=chair, kind="BEVEL", width=0.008, segments=2, limit_method="ANGLE")
oak = material(name="oak", base_color=(0.45, 0.28, 0.14), roughness=0.6)
assign(obj=chair, mat=oak)
chair.name = "chair"
```

## Check it before building on it

Look at it with `picsart_scene_preview_model` from at least two sides (for example yaw 40 and
yaw -140), then in a lit scene. Look for:

- **Floating or misplaced parts**: steps, bolts or rails with nothing holding them.
- **Pieces pushed through each other**: a roof below the walls, a part inside another.
- **Mirrored detail on the wrong side**.
- **Missing faces or open ends**, and a cutter still visible.

Fix the line in the script and build again.
