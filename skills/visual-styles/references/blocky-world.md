# Blocky world

A world built of 1 m cubes with coarse 8×8-texel faces, lit by one hard warm sun under a pastel sky. The camera
glides over stepped terrain; most of the time it holds. Crisp texels and clean blocks are the style.

This is a 3D scene (`composition.space: "3d"`): read the 3D authoring recipe (`picsart_scene_recipe scene-3d-authoring`)
first; this page adds only what makes the look.

**Characters:** two blocky figures, Tilo and Boro, walk through it on one shared `walk` action (see *Characters*).
Only that walk is proven; no other action exists yet.

## Palette

Named values; every block face is one of them with a few small texels in a second shade.

- **Turf top** `#639b76` with darker `#4a8260` and lighter `#78ad88` specks of 1 to 2 texels, never in rows. A sage
  green, warm, not lime.
- **Turf lip** `#3a634e`: the top row of a grass side, under one texel of turf `#639b76`; the rest of the side is soil.
- **Soil** `#c4764a` with darker `#a65e3a` and lighter `#d58d5f` specks. A terracotta, with no edge line on any face.
- **Stone** `#9d968a` with `#7f786d` and `#b1aa9c` patches: warm grey, a few flat patches, not salt and pepper.
- **Bark** `#d6b27a` with bands `#b08852` and ends with rings `#c49d64`: a pale log.
- **Leaves** `#587d33`, `#41602a`, `#6e9340` and olive `#7d8a3a` in clusters of 1 to 3 texels, with a pink pair of
  texels `#f0b4c4` on every leaf face (blossom).
- **Sky** gradient `#9ccbe6` at the top, `#e4e9e0` at 55 %, `#fbe0c4` at the horizon: pastel, warm at the bottom.

## The medium

- **One merged mesh.** Blocks are 1 m; only faces open to air are built; one 64×16 px atlas of 8×8-texel tiles.
- **Nearest filtering** (a `nearest` sampler in the glTF) so texels stay hard at every distance.
- **The world route.** Build the world with `picsart_scene_build_model` `script`, a list of calls, not Python (see
  `scene-3d-authoring`, `references/model-from-script.md`): a `cube` of size 1 per block (or a scaled one per run of
  blocks), a `duplicate` per repeat, one `material` per block type, a `join` per material. The script has no loops, so
  write the blocks out, leave out every block hidden inside the terrain, and use `ARRAY` (up to 50) for a straight
  run. A `textures` image covers a whole material and the script cannot unwrap a tile atlas onto the faces or set a
  texture's filtering, so the script builds flat-colour blocks (one material per named colour above); the specks and
  the blossom pair need a model that is already textured. The reply's `.glb` url expires: save the
  model with `picsart_scene_library_save` (`jobId`, `name`), which files the `.glb` in the user's Drive as it is. A shipped
  template on the public template host cannot take a `.glb`, so embed it as a single `.gltf`, upload that, and point the
  template's `model` asset at the public `.gltf` url (about a third bigger, plays the same).
- **Lighting**, `sky` preset, one hard sun: `key` `intensity` 2.6, `color` `#ffe8b0`, `direction`
  `[-0.45, -1, -0.55]`, `shadow.softness` 0.04; `ambient` `intensity` 0.55, `color` `#efe2c4`, `groundColor`
  `#d8c9a8`; `environment` `{"preset": "studio", "intensity": 0.3}`. Lower the ambient or the environment and the
  turf goes dark; raise them and the floor goes flat mint.

```json
{ "version": "1.0",
  "composition": { "space": "3d", "width": 1280, "height": 720, "fps": 24, "duration": 4,
    "background": { "colorStops": [{ "offset": 0, "color": "#9ccbe6" }, { "offset": 0.55, "color": "#e4e9e0" }, { "offset": 1, "color": "#fbe0c4" }] },
    "camera": { "lens": { "fov": 38 }, "eye": [-5.8, 1.7, 5.2], "target": [-4.1, 0.75, 0] },
    "lighting": { "preset": "sky",
      "key": { "intensity": 2.6, "color": "#ffe8b0", "direction": [-0.45, -1, -0.55], "shadow": { "softness": 0.04 } },
      "ambient": { "intensity": 0.55, "color": "#efe2c4", "groundColor": "#d8c9a8" } },
    "environment": { "preset": "studio", "intensity": 0.3 } },
  "assets": { "world": { "type": "model", "uri": "<the pcdn .gltf url>" } },
  "layers": [{ "id": "world", "content": { "kind": "model", "assetId": "world" } }] }
```

## Motion habits

- **The camera** slides along the world at a steady 1.25 m/s and pushes in with a smoothstep between 0.6 s and
  3.6 s of a 4 s move: the eye goes from `[-5.8, 1.7, 5.2]` to `[0.4, 1.5, 4.2]` while the target goes from
  `[-4.1, 0.75, 0]` to `[0.4, 1.0, 0]`; one key per frame. Long holds between moves.
- **Travel is continuous, never on twos.** A held drawing belongs to a pose, never to the root position of something
  that travels under a moving camera (*Hold the pose, not the travel* in the `scene-animation-reference` skill's held drawings). The walk below keys its poses on every
  frame.
- **Terrain steps**: hills are whole-block steps, never slopes. Trees are a log of 3 or 4 blocks with a cube canopy.

## Characters

Both are built of 1/16 m voxels, face +z with feet on y = 0, and their palette is one 32×1 px strip texture
(named colours, nearest sampling), so every face is a flat swatch.

- **Tilo**, 24 voxels (1.5 m) tall: a rounded-block head wider than tall, about a third of the height, hair
  `#4a3326`; plum hoodie `#7a3b6e`, ochre trousers `#d2a23c`, brown boots `#6b4326`, cream mitts of 2×2 voxels.
- **Boro**, 20 voxels (1.25 m): stout, a sea-green cap `#3f8f7a`, a slate-blue smock `#7d94a8` with gold buttons
  `#e6c660`, grey trousers and boots, a beard stub; legs of 4 voxels, so his walk reads mostly in the arms and the
  smock.
- **The model** is one `.gltf` per character with six part meshes (`head`, `torso`, `armL`, `armR`, `legL`, `legR`),
  each at the character origin, built from cubes by a script of calls. Each part has a boolean
  parameter `showHead` … `showLegR` bound to `node:<part>.visible`. Tilo
  `https://pcdn.picsart.com/templates-cdn/88274af8-466b-48aa-a50e-db582c2e4b76.gltf`, Boro
  `https://pcdn.picsart.com/templates-cdn/09ca1851-ed1e-4e74-811e-b79691f4066f.gltf`.
- **One layer per part, carriers as pivots.** A layer's transform has no anchor, so each character is a 3D scene
  asset: a `body` carrier (an empty `scene_ref` to a layer-less 3D scene), four pivot carriers (`armPivL`, `armPivR`,
  `legPivL`, `legPivR`) parented to `body` and set at the joints, and one `model` layer per part, parented to its
  pivot at minus the joint and showing only its own part (`showX` true, the rest false). Joints in voxels, left is
  +x: Tilo arms ±5 at 16, legs ±2.5 at 9; Boro arms ±7.5 at 10, legs ±3 at 4. A model layer's expressions read
  only its own parameters, which is why the parts are layers and the carriers read the scene's controls.
- **Controls** on each character scene, read in layer expressions as `ctx.composition:getParameters():name()`:
  `armSwing`, `legSwing` (degrees), `liftL`, `liftR` (foot lift, metres), `hipHeight` (metres; the proportions:
  Tilo 0.5625, Boro 0.25) and `pace` (travel multiplier; Tilo 1, Boro 2.25). A positive rotation about x swings a
  limb back for a character facing +z, so a left pivot takes the control negated.
- **One shared `walk` action** (1 s, two steps): `legSwing` 20° × a triangle wave, `armSwing` the opposite at 26°,
  `liftL`/`liftR` 0.04 m on the forward swing, keyed on every frame (24 keys). The `body` carrier's position
  expression: `Vec.v3(0, hipHeight * (cos(rad(legSwing)) - 1), 1.63 * hipHeight * pace * time)`, the hip drop and
  continuous travel. Both play it from the placed `scene_ref` with `content.animation`:
  `{"action": "walk", "speed": 1}` for Tilo, `{"action": "walk", "speed": 2}` for Boro (short legs take a faster
  cadence at the same ground speed). No per-character keyframes.
- **The shot**, 5 s at 1280×720, 24 fps: heading 90° (both walk toward +x), Tilo 1 m ahead of the pair's midpoint and
  Boro 1 m behind it, lane `z` 0.9 (1.9 m clear of the props); the camera rides ahead of and beside the pair so both
  faces show three-quarter: `eye` = midpoint + `[4.0, 1.8, 4.7]` easing to `[3.7, 1.7, 4.4]`, `target` midpoint
  `[x, 0.62, 0.9]`, `fov` 38, one key per frame, the midpoint moving at Tilo's ground speed (about 0.92 m/s).
  Placed behind the walkers the camera sees their backs; straight beside them, one in front of the other.

## Type

Usually none; a title is a 2D scene around the 3D one, heavy and square-set.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Texels are crisp at the nearest and the far block: no smoothing, no mip blur.
2. No pale hairlines across the floor at block boundaries, and no pale edge line on the soil (it reads as brick).
3. The stone block has no brown patch.
4. Shadows are hard and fall one way; the sun is warm, the turf stays sage.
5. Every leaf face shows its blossom pair; leaf clusters stay 1 to 3 texels.
6. Nothing in the frame is a character, a logo, a font or a texture from an existing game.
7. No jitter on root travel: track a point on a walker per frame. Root travel held on twos under a smooth camera
   gave a 5.7 px acceleration rms and a direction flip on every frame; continuous travel gave 1.1 px and 28 %.
8. Both faces show; both walkers are whole in the frame with ground under their feet; limbs grow out of the torso
   with no gap at the shoulder or hip; the feet land on the turf.

## Do / don't

- **Do** keep blocks on a 1 m grid and the texel size one size in the whole frame.
- **Do** keep the camera slow; the style is calm.
- **Don't** use a texture, character, logo, font or sound from any existing game, or draw a block that is a copy of one.
- **Don't** add a pale or lit edge on a block face; if an edge shows, make it a darker shade.
- **Don't** promise an action other than the `walk`: no run, wave or reach exists for these figures yet.

## Prompts that name another game

A prompt that names another block game or its look maps to this style. The output carries no brand words, no
characters and no textures from that game: its name stays out of every label, caption and file name.

## Known, small

Thin pale hairlines on the floor at block boundaries and a brown patch on the stone block are known defects; they
go in the next world rebuild.

## Proven on

A 4 s camera move over a 22 × 14 block world with three trees, a stone block and a hill, 1280×720 at 24 fps on
the stage export service, reviewed on a contact sheet. The world model is small, built with one
hosted model-build call.

Tilo and Boro walking side by side, a 5 s shot at 24 fps on the stage export service, reviewed on a
contact sheet: shoulders and hips attached, feet on the turf, faces visible. The character models were written
and exported with Blender locally and uploaded as `.gltf`; the hosted model build was not run for them. Known,
small: a 1 to 2 px speck at Tilo's hip seam in a few frames; Boro's stride is short because his legs are.
