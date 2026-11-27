# Brick parts script

The scripts that build one part of the [brick toy](brick-toy.md) style as one GLB. Copy the script of the part you
need, change its numbers as shown, and pass it as `script` to `picsart_scene_build_model`; one call builds one part.
The script is a list of calls, one per line, not Python: there are no loops, no arithmetic and no variables for
sizes, so every number is written out. The calls and limits are in `scene-3d-authoring`
(`references/model-from-script.md`).

- Sizes are 10 times real toy bricks, in metres: stud pitch 0.08, brick 0.096 (3 plates), plate 0.032, studs 0.048
  across and 0.017 tall, every edge bevelled by 0.0036 (0.045 of a stud) with 3 segments.
- A part is 0.002 smaller than its grid cell on each side (a 1 stud brick is 0.078, not 0.08), so neighbours show a
  seam.
- Blender's -Y is the front (it exports as +z). A part sits on the scene origin with its base at z = 0, except a
  `limb`, which hangs from it: its top, the joint it swings from, is at z = 0.
- Every part has one material, `main` (the desk: `wood`); colour it per layer with `content.materials`. The colour
  in the script is only a placeholder.

| Part | Script |
|---|---|
| A brick: `w` studs across (x), `d` deep (y), 3 plates high | [A brick](#a-brick) |
| A plate (1 plate high) or a tile (no studs) | [A tile or plate](#a-tile-or-plate) |
| A round brick, 1 or 2 studs across | [A round brick](#a-round-brick) |
| A column of bricks hanging from its top, with a foot plate pointing forward | [A limb](#a-limb) |
| A wooden desk top at y = 0 | [The desk](#the-desk) |

## Changing the numbers

Work the numbers out by hand before you write them (the script cannot compute):

- **Body size:** `w` times 0.08 minus 0.002 across (x), `d` times 0.08 minus 0.002 deep (y), and the height is the
  number of plates times 0.032. The body's `location` is (0, 0, half the height), because a cube is centred.
- **Stud positions:** studs sit at multiples of 0.08 from the centre, so a row of `n` studs is at
  (i - (n - 1) / 2) times 0.08 for i from 0 to n - 1: a row of 2 is at -0.04 and 0.04, a row of 3 at -0.08, 0 and
  0.08, a row of 4 at -0.12, -0.04, 0.04 and 0.12. Their z is the body's height plus 0.0085.
- **One stud per line:** make the first stud, then `duplicate` it at each other position. A long row can be one stud
  with an `ARRAY` modifier (`count`, and a `relative_offset` of about 1.667 along the row's axis, since the offset is
  in stud widths); check the pitch in a preview, then `duplicate` the row for the next row.
- **Joining:** `join` takes up to 64 objects, so a brick with more than 63 studs joins its studs in two steps.

## A brick

A 2x4 brick, 3 plates high. For another size, change the body's `scale` and `location`, and add or remove stud
lines and their `join` entries as shown above. For a plate, use a body height of 0.032 (location z 0.016, stud z
0.0405).

```
# A 2x4 brick, 3 plates high, with its 8 studs.
body = cube(size=1, location=(0, 0, 0.048), scale=(0.158, 0.318, 0.096), name="body")
modifier(obj=body, kind="BEVEL", width=0.0036, segments=3, limit_method="ANGLE")
apply_modifiers(obj=body)
shade_flat(obj=body)
stud1 = cylinder(radius=0.024, depth=0.017, vertices=32, location=(-0.04, -0.12, 0.1045), name="stud")
modifier(obj=stud1, kind="BEVEL", width=0.0022, segments=1, limit_method="ANGLE")
apply_modifiers(obj=stud1)
shade_smooth(obj=stud1, auto_angle=30)
stud2 = duplicate(obj=stud1, location=(-0.04, -0.04, 0.1045))
stud3 = duplicate(obj=stud1, location=(-0.04, 0.04, 0.1045))
stud4 = duplicate(obj=stud1, location=(-0.04, 0.12, 0.1045))
stud5 = duplicate(obj=stud1, location=(0.04, -0.12, 0.1045))
stud6 = duplicate(obj=stud1, location=(0.04, -0.04, 0.1045))
stud7 = duplicate(obj=stud1, location=(0.04, 0.04, 0.1045))
stud8 = duplicate(obj=stud1, location=(0.04, 0.12, 0.1045))
part = join(objects=[body, stud1, stud2, stud3, stud4, stud5, stud6, stud7, stud8])
main = material(name="main", base_color="#c8c8c8", roughness=0.3)
assign(obj=part, mat=main)
part.name = "brick"
```

## A tile or plate

A tile has no studs: the body alone, with no `join`. This one is a 1x2 plate, 1 plate high.

```
# A 1x2 plate (1 plate high) with no studs, the shape of a tile.
body = cube(size=1, location=(0, 0, 0.016), scale=(0.078, 0.158, 0.032), name="body")
modifier(obj=body, kind="BEVEL", width=0.0036, segments=3, limit_method="ANGLE")
apply_modifiers(obj=body)
shade_flat(obj=body)
main = material(name="main", base_color="#c8c8c8", roughness=0.3)
assign(obj=body, mat=main)
body.name = "brick"
```

## A round brick

The body is a cylinder of radius `n` times 0.04 minus 0.001. With 1 stud across it has one stud in the middle:

```
# A round brick, 1 stud across, 3 plates high, with one stud.
body = cylinder(radius=0.039, depth=0.096, vertices=40, location=(0, 0, 0.048), name="body")
modifier(obj=body, kind="BEVEL", width=0.0036, segments=3, limit_method="ANGLE")
apply_modifiers(obj=body)
shade_smooth(obj=body, auto_angle=30)
stud = cylinder(radius=0.024, depth=0.017, vertices=32, location=(0, 0, 0.1045), name="stud")
modifier(obj=stud, kind="BEVEL", width=0.0022, segments=1, limit_method="ANGLE")
apply_modifiers(obj=stud)
shade_smooth(obj=stud, auto_angle=30)
part = join(objects=[body, stud])
main = material(name="main", base_color="#c8c8c8", roughness=0.3)
assign(obj=part, mat=main)
part.name = "round"
```

With 2 studs across it has four studs:

```
# A round brick, 2 studs across, 3 plates high, with four studs.
body = cylinder(radius=0.079, depth=0.096, vertices=48, location=(0, 0, 0.048), name="body")
modifier(obj=body, kind="BEVEL", width=0.0036, segments=3, limit_method="ANGLE")
apply_modifiers(obj=body)
shade_smooth(obj=body, auto_angle=30)
stud1 = cylinder(radius=0.024, depth=0.017, vertices=32, location=(-0.04, -0.04, 0.1045), name="stud")
modifier(obj=stud1, kind="BEVEL", width=0.0022, segments=1, limit_method="ANGLE")
apply_modifiers(obj=stud1)
shade_smooth(obj=stud1, auto_angle=30)
stud2 = duplicate(obj=stud1, location=(-0.04, 0.04, 0.1045))
stud3 = duplicate(obj=stud1, location=(0.04, -0.04, 0.1045))
stud4 = duplicate(obj=stud1, location=(0.04, 0.04, 0.1045))
part = join(objects=[body, stud1, stud2, stud3, stud4])
main = material(name="main", base_color="#c8c8c8", roughness=0.3)
assign(obj=part, mat=main)
part.name = "round"
```

## A limb

A column of 1x1 bricks hanging from the origin, with a foot plate one stud longer than the column is wide, pointing
forward (-y). Each brick is 0.096 lower than the last: add a `duplicate` line for each extra brick, lower the foot
by the same step, and add the new names to the `join`. For a wider column, widen the bricks and the foot as shown
above.

```
# A limb: three 1x1 bricks hanging from the origin (the joint), and a foot plate pointing forward.
top = cube(size=1, location=(0, 0, -0.048), scale=(0.078, 0.078, 0.096), name="brick")
mid = duplicate(obj=top, location=(0, 0, -0.144))
low = duplicate(obj=top, location=(0, 0, -0.24))
foot = cube(size=1, location=(0, -0.04, -0.304), scale=(0.078, 0.158, 0.032), name="foot")
part = join(objects=[top, mid, low, foot])
modifier(obj=part, kind="BEVEL", width=0.0036, segments=3, limit_method="ANGLE")
apply_modifiers(obj=part)
shade_flat(obj=part)
main = material(name="main", base_color="#c8c8c8", roughness=0.3)
assign(obj=part, mat=main)
part.name = "limb"
```

## The desk

A flat top, 9 m wide and 6 m deep, with more desk behind the subject than in front of it (its centre sits at
y = -1, a sixth of the depth). Change the plane's `scale` for another size and `location` y to a sixth of the new
depth.

```
# A wooden desk top, 9 m wide and 6 m deep, its surface at y = 0 and more of it behind the subject.
top = plane(size=1, location=(0, -1, 0), scale=(9, 6, 1), name="desk")
wood = material(name="wood", base_color=(0.45, 0.27, 0.13), roughness=0.6)
assign(obj=top, mat=wood)
top.name = "desk"
```

The script draws no wood grain. To get a grain, pass a wood image as an input texture and give the material
`texture="wood_grain"` (the name of that input) with a `texture_scale`; without one the desk is a plain wood brown.
