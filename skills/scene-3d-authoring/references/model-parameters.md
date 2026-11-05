# Model parameters, actions and faces

## Contents

- What a parameter binds
- Playing the model's clips
- Character control names
- A car without bones
- Faces and screens on a model

A model's parameters are declared inside its GLB. `picsart_scene_import_model` proposes them from
what the model has (bones, shape keys, materials, clips) and lists them in its report;
`picsart_scene_build_model` returns its models with theirs. A layer sets them through
`content.parameters` — a constant, keyframes or an expression.

## What a parameter binds

`bind` is one target or a list of them:

| `bind` | Drives |
|---|---|
| `node:<node>.position` / `.rotation` / `.scale` | the node's whole channel, from a `vec3` |
| `node:<node>.rotation.y` (any channel, `.x`/`.y`/`.z`) | one axis, from a `number` |
| `node:<node>.visible` | shown or hidden, from a `boolean` |
| `material:<material>.baseColor` / `.emissive` | a colour |
| `material:<material>.opacity` / `.roughness` / `.metalness` | a number |
| `morph:<node>/<target>` | a morph target's weight |
| `action:<action>.time` | an action's playhead, in seconds |
| `[]` | nothing: a knob other parameters read |

Names are the glTF node, material and clip names, dots allowed (`wheel.fl.rotation.x`). The
value replaces the node's own value for that channel or axis — in the node's local space, its
other axes keeping the model's pose; rotation is in degrees. A declaration with
`mode: "aggregate"` (node position, rotation, scale and morph binds only) adds the value over the
clips' pose instead: a position added, a rotation turned after the pose, a scale multiplied, a
morph weight added — so its `default: 0` holds nothing still. A number target may end in a
response `[in:out, …]` (two or more points, `in` increasing): the value is read through it,
linear between the points and held past the ends; `node:lid.rotation.x[0:0, 1:-110]` opens a
lid 110° as the knob goes 0 → 1. Without one the value is written as it is.

- **One target, one parameter.** Two parameters on one target, or one on a whole channel and
  another on one of its axes, are refused (`model_param_bind_shared_target`). Different axes of
  one node may each have one. They turn X, then Y, then Z in the node's frame, so a wheel that
  steers and rolls needs two nodes: a pivot that steers (`y`) holding the wheel that rolls (`x`).
- **A parameter may read another.** A `default` of `{ "expression": "return
  ctx.layer:getParameters():drive() * 360 / (2 * math.pi * 0.3)" }` follows the `drive`
  parameter; a declared `min`/`max` holds it. A layer that sets the parameter itself overrides it.

## Playing the model's clips

The document spelling is `content.animation: { action: "walk" }`; for a model, `action` names one of
the glTF file's animations. Only `action` is accepted as the entry's name field. 2D scenes use the
same entry for a placed scene's root `actions` (`picsart_scene_recipe scene-animation-reference`,
"Named actions on a placed scene"). A model with no stack stands still; a `scene_ref` with no stack
plays its own timeline. `animations` is a layer field; the action stack is `content.animation`.

- **Several actions at once.** `animation` is one entry or a list; each takes `weight` (a number or
  a track, default 1), a window (`start`, `duration`, `fade` seconds ramping the weight at each edge
  it gives), `mode` and a literal integer `tier >= 0` (default 0; a tier of the stack,
  not a keyframe track). Tiers evaluate ascending. Within one tier `replace` entries
  (the default) mix per channel at their weights: normalised above a sum of 1,
  the lower tiers' result filling the remainder below it (initially rest); an action takes no part in
  a channel it leaves alone, so a walk and a blink on other nodes each play in full. Idle → Walking →
  Running is three entries whose windows overlap by their `fade`.
  After each tier's replace pool, that tier's `aggregate` entries add their action's
  offsets from its frame at `trim.in` over that blend, in authored order, at their
  weight: a Wave (`loop: false`) over a Walking. An action-time parameter plays its action as a
  replace entry at weight 1 (two such actions on one channel each take half), or supplies the playhead
  of the entry naming it (that entry then takes no `speed`, `trim` or `loop`: `model_action_playhead_twice`).
  Two entries naming an action driven by a parameter are refused (`model_param_action_conflict`).
- **Layer aim over walk.** `[{"action":"walk"}, {"action":"aim","tier":1,"start":3.5,"fade":0.2},
  {"action":"shoot","tier":1,"mode":"aggregate","start":4,"duration":1.9}]`
  keeps legs walking while aim replaces its keyed arm channels and shoot adds over aim.
  Keep crossfade partners in the same tier: aim→wave in tier 1, walk→idle in tier 0.
  Different tiers introduce a rest dip `(1-m)*m` during a complementary crossfade.
  Put aggregates on the top tier they should follow; higher full replace masks lower
  aggregates on its keyed channels. Use the model's own actions; no derived arm/leg splits.

## Character control names

Standard control names are a convention, not validation: a face takes VRM expressions (`happy`,
`sad`, `blink`, `lookLeft`, the visemes `aa` `ih` `ou` `ee` `oh` for lip sync), with ARKit blendshapes
(`jawOpen`, `mouthSmileLeft`, …) optional for detail; a single-axis body control is
`<vrmBone><Motion>` with Raise, Swing, Nod, Turn, Tilt or Lean (`leftUpperArmRaise`, `headTurn`,
`hipsTurn`). Any name is legal; standard presets target these. The `picsart_scene_build_model`
bear declares `blink`, `aa`, `happy` and its body controls this way.

**Lip sync.** `picsart_scene_apply_preset` with `preset: "lipSync:visemes"` turns word timings (a
captions `transcript` in `params`) into one track per viseme control the model declares and merges
them into the layer's `content.parameters`. The lips shut on every m, b and p, so a model's `aa`..`oh`
all at 0 must read as closed lips. Parameter tracks are layer-local: a character played as several
layers (one per clip) gets one call per layer, with that layer's span as `start`/`end`, so the mouth
carries across the cuts. A model with no mouth shape keys cannot lip-sync; a face texture slot (below)
can. The 2D cartoon rigs (`scene://rig-humanoid`, `scene://rig-face`) use the same names.

## A car without bones

Each front wheel sits inside a pivot node (`pivot_fl` holding `wheel_fl`, the pivot at the wheel's
centre), the rear wheels on their own. The declarations such a model carries:

```json
{
  "steer": { "type": "number", "default": 0, "min": -1, "max": 1, "animatable": true,
             "description": "Front wheels turn: -1 full left, 1 full right (the car facing +z).",
             "bind": ["node:pivot_fl.rotation.y[-1:30, 1:-30]", "node:pivot_fr.rotation.y[-1:30, 1:-30]"] },
  "drive": { "type": "number", "default": 0, "animatable": true,
             "description": "Distance driven, in metres.", "bind": [] },
  "roll":  { "type": "number", "animatable": true,
             "description": "Wheel turn in degrees; follows drive (wheel radius 0.3 m).",
             "default": { "expression": "return ctx.layer:getParameters():drive() * 360 / (2 * math.pi * 0.3)" },
             "bind": ["node:wheel_fl.rotation.x", "node:wheel_fr.rotation.x", "node:wheel_rl.rotation.x", "node:wheel_rr.rotation.x"] }
}
```

The layer moves the car with its `transform` and keys the same distance on `drive`, and the
wheels roll with it: `"parameters": { "drive": { "keyframes": [{ "time": 0, "value": 0 },
{ "time": 3, "value": 4 }] }, "steer": { "keyframes": [{ "time": 1, "value": 0 }, { "time": 2,
"value": 0.6 }] } }`.

## Faces and screens on a model

A material's `baseColorTexture` or `emissiveTexture` shows the same picture a card does: a media
`{ kind: "media", assetId, trim?, speed?, loop? }` (image, video, `video_with_matte`) or a 2D
`scene_ref` with `parameters`, on the MODEL layer's clock. `width` and `lit` are a card's; a slot
refuses them (`material_texture_card_field`).

- The picture draws OVER the material by its alpha: a transparent part shows what the material drew
  underneath, an opaque video replaces it. Lights hit the result; `opacity` multiplies after.
- It rides the mesh's UVs, so it follows the skin and its morphs. `emissiveTexture` draws over the emission
  the same way, × `emissiveStrength` (a screen, a glow); an unlit material refuses it.
- A model with no face UVs: `picsart_scene_import_model` with `face: { node: "<the mesh node, e.g.
  Mage_Head>", cone?: 85, material?: "face" }` splits the triangles facing the front (+z, within
  `cone` degrees at bind pose) into their own primitive on material `face`, UVs a front projection
  (u left to right, v top to bottom). It keeps the skin, morphs and what the island drew. The
  report's `face.aspect` is the island's width / height: size the face scene's composition to it.

```json
"materials": { "face": { "baseColorTexture": { "kind": "scene_ref", "assetId": "faceArt",
  "parameters": { "aa": { "keyframes": [ ... ] },
    "blink": { "expression": "return picsart.randomPulse(time, 0, 1, 2, 5, 0.06, 0.04, 0.08, 0.2, 7)" } } } } }
```

Lip-sync tracks and drivers go in the slot's bindings,
`content.materials.face.baseColorTexture.parameters.<name>`: a viseme track as keyframes, a driver as
the `picsart.randomPulse` / `picsart.randomHold` / `picsart.cycle` expression its preset would write. The
parameter-driver presets write a `scene_ref` layer's bindings and refuse a model layer. A `scene_ref` slot or card plays a
declared 2D scene asset; to play `scene://rig-face`, that scene holds one `scene_ref` layer to it
and passes its parameters on.
