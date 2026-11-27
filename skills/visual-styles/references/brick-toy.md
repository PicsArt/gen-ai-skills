# Brick stop-motion

Toy bricks on a real desk, filmed close like a macro photograph: glossy plastic with a clearcoat shine, studs on
every top face, bevelled edges, darkened seams, shallow focus. The figures move in held poses on twos while the
camera glides. Small, warm and handmade.

This is a 3D scene (`composition.space: "3d"`): read the 3D authoring recipe (`picsart_scene_recipe scene-3d-authoring`)
first; this page adds only what makes the look.

## Finish

Objects step on twos and the camera does not; shallow focus and a clearcoat shine (see Motion habits).

## Palette

Bricks in a few saturated plastic colours: yellow `#f2cd37`, blue `#0a5cc4`, grey `#a0a5a9`, dark grey `#4c4e4a`,
white `#f4f4f4`. Desk a mid-brown wood grain, backdrop a dark warm gradient `#2a211b` to `#5a4636`. **The hero
colour is red `#c91a09`, reserved for the part the story ends on** (a roof, a door, the last brick) and used nowhere
else. Every brick shares one plastic material and differs only in `baseColor`.

## The medium

- **Bricks are real geometry at 10 times real size.** Stud pitch 0.08 m, brick height 0.096 m, plate 0.032 m,
  studs 0.048 m across and 0.017 m tall with a rounded lip on their top edge, every edge bevelled by 0.045 of a
  stud. Why 10 times: the `ambient_occlusion` radius cannot go below 0.01 m, and at real size (8 mm pitch) that
  darkens whole faces instead of seams. At 10 times, 0.04 m reads as a seam. Size the camera, the motion and the
  depth of field to the same scale.
- **Each part is one GLB with its origin at the centre of its base** (a limb that swings has it at the joint), so
  `position` stacks it by whole brick heights and a squash flattens it onto what holds it.
- **Plastic** is one material on every part: `roughness` 0.28, `clearcoat` 0.8, `clearcoatRoughness` 0.08. The
  clearcoat gives the sharp second highlight that reads as moulded plastic rather than paint.
- **Seams** are `ambient_occlusion` (`intensity` 1.6, `radius` 0.04) over the bevels: the bevel catches a light
  line, the AO darkens the gap beside it.
- **Studio light**: the `studio` lighting preset with a warm key from above left (`direction` `[0.5, -1, -0.45]`,
  soft shadows), a cool fill and a warm rim. The softbox highlights come from the surroundings: a 2:1 equirect PNG
  of a dim room with two or three bright rectangles as `environment.assetId`. Without it the clearcoat reflects
  soft blur and the bricks look like resin.
- **Focus** is `depth_of_field` at one compromise distance (`fStop` 2.8, `focusDistance` between the camera's start
  and end distance to the subject). Its params are constants, so there is no rack focus: keep the push-in short
  enough that both ends stay acceptably sharp.
- **The desk** is a wooden top whose surface is y = 0: a plane with a wood-grain texture and a low clearcoat (0.08)
  so the key's reflection does not wash it out. The backdrop gradient sits behind it, out of focus.
- **Grade**: `color_grade` with `toneMapping` `agx`, a small `exposure` lift (0.25), `contrast` 0.12, and a
  `vignette`.

## The character

Drawn from the style's own shapes, not a generated sheet (the mechanism, saving and talking are in [shapes-character](shapes-character.md)); build once, save once to the library, place it by its `uri` in every shot.

- **Proportions:** 3 bricks tall in 3D: a head cylinder, a torso brick, two leg bricks.
- **Shapes:** the figure is a group of brick parts (see Parts below), each a `model` placed with `parentId` joints; the face is a printed decal.
- **Face:** a printed face decal; to talk, swap two decal layers by `opacity` steps on the `mouth` track.
- **Controls:** joints turn by rotation tracks, not parameters: key the leg and arm groups directly; not proven in this style.
- **No run, jog, point or pick_up:** those presets need a cut-out figure with an elbow and a knee, and a brick figure has neither (two leg bricks, no upper and lower piece). The SVG cut-out builder refuses it by name (`missing_part`, `missing_joint`); act with the rotation tracks above.

## Motion habits

- **Objects step on twos, the camera does not.** Start every object expression with
  `local time = math.floor(time * 15 + 1e-6) / 15` (30 fps root): the pose holds for two frames, as a hand moved
  it. Keep the camera on smooth keyframes. That contrast is the style.
- **Except a root that travels while the camera follows it.** Keep that carrier's travelling position continuous, or
  step the camera on the same twos (*Hold the pose, not the travel* in the `scene-animation-reference` skill's held drawings). Held limb poses (swing, bob) are the
  style's habit, not proven for travelling figures yet: the blocky-world walk keys its poses on every frame.
- **Entrances** are the `drop_in` and `snap_settle` presets, with the twos line added at the top of each
  expression they write. A brick drops onto studs and squashes; the last brick snaps.
- **A figure walks in held poses**: legs swing about the hip, the body bobs a little each step, and it stops dead
  with no ease. Build it from parts parented to a carrier group (`parentId`) so one position expression moves the
  whole figure (that position continuous under a following camera, see above).
- **A carried brick rides the hands**: compute its position from the same arm angle the arms use, so it never
  floats. Set it down onto studs, then press and squash.
- **Order by support**: a brick arrives only once what holds it has landed; one brick per beat.
- **The camera** starts wide enough to see the walk, drifts with it, and ends on a short push-in to the result.

## Type

Usually none. A title is a 2D scene around the 3D one, a rounded bold sans set late and still.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Every top face has studs, every edge a bevel, every gap a dark seam.
2. The plastic has two highlights (the clearcoat and the base), with rectangular softbox shapes in them.
3. Objects hold for two frames; the camera moves every frame; a figure travelling under the following camera
   keeps a continuous root (track a point on it per frame: no direction flip on every frame).
4. Nothing floats: a carried brick touches the hands, a placed brick sits on studs.
5. The focus falls off front and back; the desk grain blurs into the distance.
6. Red appears only on the hero part.

## Build with the tools

Build the parts, the desk and the softbox environment (see *Parts* below), place them as `model` layers in a
`space: "3d"` composition, apply `drop_in` and `snap_settle` with `picsart_scene_apply_preset`, then add the twos line
to each expression it wrote. Validate, preview three or four moments (an entrance, a placement, the end), then
export. Review it on a contact sheet: floating bricks and arms through bricks show only in motion.

A minimal scene, a desk and two bricks, the second snapping on at 0.6 s:

```json
{
  "version": "1.0",
  "composition": {
    "space": "3d", "width": 1920, "height": 1080, "fps": 30, "duration": 2,
    "background": { "colorStops": [{ "offset": 0, "color": "#2a211b" }, { "offset": 1, "color": "#5a4636" }] },
    "camera": { "lens": { "fov": 30 }, "eye": [0.3, 0.45, 1.4], "target": [0, 0.1, 0] },
    "lighting": { "preset": "studio",
      "key": { "intensity": 2.6, "color": "#fff1df", "direction": [0.5, -1, -0.45], "shadow": { "softness": 0.35 } },
      "fill": { "intensity": 0.45, "color": "#dfe8ff" }, "rim": { "intensity": 1.4, "color": "#ffe2c0" },
      "ambient": { "intensity": 0.35 } },
    "environment": { "assetId": "softboxes", "intensity": 1.2 },
    "effects": [
      { "id": "ambient_occlusion", "params": { "intensity": 1.6, "radius": 0.04 } },
      { "id": "depth_of_field", "params": { "fStop": 2.8, "focusDistance": 1.45 } },
      { "id": "color_grade", "params": { "toneMapping": "agx", "exposure": 0.25, "contrast": 0.12 } },
      { "id": "vignette", "params": { "fade": 50, "size": 75 } }
    ]
  },
  "assets": {
    "desk": { "type": "model", "uri": "desk.glb" },
    "b2x4": { "type": "model", "uri": "brick_2x4.glb" },
    "softboxes": { "type": "image", "uri": "https://pcdn.picsart.com/templates-cdn/0c5d719f-8c62-4d62-a1ac-d0496601c56e.png" }
  },
  "layers": [
    { "id": "desk", "content": { "kind": "model", "assetId": "desk",
        "materials": { "*": { "roughness": 0.65, "clearcoat": 0.08 } } } },
    { "id": "base", "content": { "kind": "model", "assetId": "b2x4",
        "materials": { "*": { "baseColor": "#f2cd37", "roughness": 0.28, "clearcoat": 0.8, "clearcoatRoughness": 0.08 } } } },
    { "id": "top", "start": 0.6,
      "transform": { "position": [0, 0.096, 0] },
      "content": { "kind": "model", "assetId": "b2x4",
        "materials": { "*": { "baseColor": "#c91a09", "roughness": 0.28, "clearcoat": 0.8, "clearcoatRoughness": 0.08 } } },
      "animations": {
        "position": { "expression": "local time = math.floor(time * 15 + 1e-6) / 15\nlocal off = Vec.v3(0, 0.12, 0)\nif time < 0.3 then local u = math.max(time, 0) / 0.3 return value + off * (1 - u * u) end\nlocal s = time - 0.3\nif s >= 0.6 then return value end\nreturn value - off * (0.35 * math.exp(-10 * s) * math.sin(25 * s) * (1 - s / 0.6))" },
        "scale": { "expression": "local time = math.floor(time * 15 + 1e-6) / 15\nlocal s = time - 0.3\nif s < 0 or s >= 0.6 then return value end\nlocal k = 0.12 * math.exp(-10 * s) * math.cos(25 * s) * (1 - s / 0.6)\nreturn Vec.v3(value.x * (1 + k * 0.5), value.y * (1 - k), value.z * (1 + k * 0.5))" }
      } }
  ]
}
```

## Parts

Every part is built by a short script in [brick parts](brick-parts.md) (fetch it with the recipe tool:
`name: "visual-styles"`, `reference: "references/brick-parts.md"`). The script is a list of calls, not Python, so
each part has its own script with its sizes written out. Copy the one you need, change its numbers as that page
shows, and pass it as `script` to `picsart_scene_build_model`: one call builds one part in a few seconds, and its
reply's `url` is the GLB, a `model` asset's `uri`.

| Part | Builds |
|---|---|
| a brick | a 2×4 brick, 3 plates high (change the body size and the stud lines for another size; 1 plate is a plate) |
| a tile | a brick with no studs: the body alone |
| a round brick | a round brick, 1 or 2 studs across, for heads and arm segments |
| a limb | a leg of three 1×1 bricks hanging from its hip, with a foot plate |
| the desk | the wooden desk top, its surface at y = 0 (metres) |

- Build each distinct part once and reuse its URL on every layer that shows it; colour it per layer through
  `content.materials` (`"*"` or `main`), never by building a coloured copy.
- `w` runs along x and `d` along z: a brick that runs across the frame is `w` long, or a `d`-long one turned
  `rotation` `[0, 90, 0]`.
- The built URL is a temporary one: build the parts in the same session as the export.

The softbox surroundings are one fixed image, `https://pcdn.picsart.com/templates-cdn/0c5d719f-8c62-4d62-a1ac-d0496601c56e.png`
(a dim warm room with two rectangular softboxes and a strip light, 2048×1024 equirect). Declare it as an `image`
asset and name it in `environment.assetId`.

## Do / don't

- **Do** keep every part on the stud grid: positions in whole studs across, whole brick or plate heights up.
- **Do** keep the camera low and close, a little above the bricks, so the desk recedes into blur.
- **Don't** smooth the steps: no eased object keys, no motion blur on objects.
- **Don't** let a carried or placed part float or pass through another; check placements in motion, not on stills.
- **Don't** model at real size: the seams vanish (the AO radius floor).
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - A finish belongs to the page: the desk grain is a texture on the desk plane so it travels with the desk; a fixed `noise` (about 2, `seedMode` fixed; ours, tune by render, check it renders in the 3D effects chain) after the grade keeps the dark backdrop gradient from banding; a title stays a sharp 2D scene on top.

## Originality guard

Design your own figures and builds. A figure is made of plain bricks (1×1 columns for legs, a 2×2 torso, round
bricks for arms and head), never a toy-figure silhouette with clawed hands and a cylinder head on a neck, and
never a brand's logo on a stud or a named toy line's sets, characters or packaging. The method (moulded plastic,
studs, seams, macro focus, twos) is the style; the builds are new.

## Proven on

The brick-robot film: a brick robot walks a white brick to a small house as the house builds itself, sets it on
the roof ridge, steps back and cheers, while the camera pushes in (7 s, 1920×1080, reviewed on a contact sheet). The example above was rendered on the stage export
service from parts built with the brick parts scripts.
