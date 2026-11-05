---
name: scene-3d-authoring
description: Build a 3D scene (a composition whose space is 3d) — models, camera, lighting presets, floor, groups and parenting, model parameters, 3D motion presets (drop_in, fly_in_arc, snap_settle, bounce, idle_bob, wiggle, turntable; camera orbit, dolly, push_in, crane, whip_pan) — then render and measure it. Use when making a product or toy showcase, a build-up sequence of parts, an object that builds itself and then moves (drives, walks, unfolds), a turntable, a 3D title or any 3D document, or when 3D motion lands wrong, sinks into the floor or fails to evaluate. Not for a 2D cartoon character, face or mascot (shapes and the cartoon rig templates, in character-rigging), nor for flat layers in depth (photo cards that flip, a camera orbiting cards or panels) — that is a 2D scene with layer depth and the composition camera, in scene-animation-reference.
metadata:
  category: authoring
  version: '1.1'
  ported-from: 3d-authoring 1.1 at 55.91.0
user-invocable: false
---

# 3D scenes — models, light, motion, render

A 3D scene is a scene whose composition says `space: "3d"`: metres, y up, rotations in
degrees about x then y then z (intrinsic). Its layers are objects (a `model`, a `media` or 2D-scene card,
a `scene_ref` group, or a `light`), it is seen through one camera, and it plays as a rendered video:
`picsart_scene_contact_sheet` and `picsart_scene_export` render it, whether the 3D scene is the document
itself or one a 2D scene plays through a `scene_ref`. **Ask `picsart_scene_capabilities` for
`schema:Composition3D` and `schema:Layer3D` before writing a field** — a 3D object refuses 2D placement
fields (`anchor`, `effects`, `looks`, `transforms`) by name.

Flat layers in depth are not a 3D scene. Photo cards that flip in, panels that fan out, a camera
that orbits them: keep the 2D scene and give its layers `z`/`rotationX`/`rotationY` under the
composition camera (`picsart_scene_recipe scene-animation-reference`, "Depth and the camera"). The catalog
entries that work that way are tagged `2.5d` (`flip_in`, `flip`, `tilt_3d`, and the camera moves
`orbit`, `dolly`, `push_in`).

Every asset a 3D scene names — a model, a picture, a video — is a public https URL. Build the
document inline and change it with `picsart_scene_patch`.

## Start from a frame, a camera and a light

```json
{ "version": "1.0",
  "composition": { "space": "3d", "width": 1920, "height": 1080, "fps": 30, "duration": 8,
    "camera": { "eye": [0, 0.75, 1.7], "target": [0, 0.08, -0.1], "shutterAngle": 180 },
    "motionBlurSampleCount": 8 },
  "assets": { "brick": { "type": "model", "uri": "https://cdn.example.com/brick.glb" } },
  "layers": [ { "id": "b1", "content": { "kind": "model", "assetId": "brick",
      "materials": { "*": { "baseColor": "#e3000b", "roughness": 0.35, "clearcoat": 0.6 } } },
    "transform": { "position": [0, 0, 0], "scale": [10, 10, 10] } } ] }
```

- **Camera.** `eye` is where it stands, `target` what it looks at, both in metres; `lens.fov`
  is vertical degrees (default 35). Frame the subject by moving the eye, not by scaling the
  subject. `shutterAngle` 180 with 8 samples is film motion blur for the whole frame.
- **Light.** Set `composition.lighting` (`schema:Composition3D`): a `preset` — `studio`, `dark`,
  `sky` or `white_room` — then tune any one light over it (`key`, `fill`, `rim`, `ambient`: a key's
  `intensity`, `color`, `direction`, `shadow.softness`). `background`, `environment` and `ground`
  finish the look: a warm paper sweep with a soft-shadowed key is `studio`; a low orange key from the
  side with a dusk-gradient `background` reads as sunset; near-black with a bright cool `rim` is dramatic.

- **Post effects.** `composition.effects` is the 3D scene's post stack: `glow`,
  `ambient_occlusion`, `depth_of_field`, `color_grade`, `vignette`, `film_grain`,
  `channel_shift`. Their params, ranges and units are the `space: "3d"` entries of
  `picsart_scene_capabilities` `effects` — `sections: ["effect:ambient_occlusion"]` for one, or
  the whole `effects` section, keeping the entries whose `space` is `3d`. A glow spreads only emitted light: a lamp or an LED
  (`emissive` with an `emissiveStrength` above the `threshold`), never a lit surface.
- **Floor.** `ground` is the plane y = 0 and takes the key's shadows. An object stands on it
  when its lowest point is at y = 0 — see *Models* for where that is. Over a drawn floor the
  backdrop shows only where the floor does not: a camera looking down sees floor, not sky. To
  show a gradient or sky, lower the eye or raise the target until the horizon is in frame.
- **Seamless sweep.** A lit floor never matches an unlit backdrop: the lights shade it, so its
  horizon shows. `ground.shadowOnly: true` over a `background` draws the backdrop itself as the
  floor, with only the shadows on it (`studio` does this), and no horizon at any camera height.
- **Matte.** `ground.shadowOnly: true` with no `background` renders a matte that carries the
  shadows onto whatever 2D scene plays it.
- **Casts nothing.** A sky dome or a far backdrop model takes `content.castShadow: false`: it neither shuts
  the key out nor widens the shadow's fit, which follows the casters only, so shadows stay sharp.

## Models

A model is a GLB `model` asset at a public https URL. Asset keys are identifiers: `p3004`, never `3004`.

- **Origin at the base.** The origin is what `position` places, what a turn pivots on and
  what a squash flattens toward. With the origin at the centre of the base the object stands on
  the floor at `[x, 0, z]` and squashes onto it. A model whose origin is elsewhere is lifted by its
  height (the import report gives its bounds), or fixed in the file it came from.
- **Bring a model in.** `picsart_scene_import_model` takes a GLB, a glTF (buffers and images
  embedded as data: URIs) or a binary FBX from a public https URL, Draco or meshopt compressed
  included, and returns one uncompressed GLB plus a report of its nodes, bones, morph targets,
  materials and clips, with the model parameters it proposes. Reference the `url` it returns (the
  Drive copy when `driveUid` comes back; an `expiring` one must be re-imported before a scene
  depends on it). `expose` picks the parameter kinds (`bones`, `morphs`, `materials`, `clips`);
  a bone a clip already turns is proposed only when `bones` is named, so a walk clip still walks.
  Look at it with `picsart_scene_preview_model` (a still or a turntable) before building on it.
- **A ready-made model.** `picsart_scene_build_model` builds one GLB: `character` (a rigged toy
  bear with `blink`, `aa`, `happy` and body controls such as `headNod`, `leftUpperArmRaise`) or
  `set` (a meadow of props: path, hills, trees, flowers, blocks, mushrooms, castle, clouds, fence,
  bunting, balloons, sky; the same arguments build the same model). `sky` is an unlit dome: give that
  layer `castShadow: false`. Build the far set (sky, hills, clouds) and the near one (trees, fence,
  flowers) as two models.
- **Materials.** `content.materials` overrides by material name, `"*"` for all of them.
- **Model parameters.** A knob the model declares (a colour that makes the studs glow, a bone,
  a shape key) is set per layer through `content.parameters` — a constant or a track, so it can flash
  on a beat. What a parameter binds, aggregate mode, response curves, several actions mixed in tiers,
  lip sync, the standard character control names and a car without bones:
  [references/model-parameters.md](references/model-parameters.md).
- **A face or screen on a model** is a material texture slot, not a card:
  [references/model-parameters.md](references/model-parameters.md), "Faces and screens on a model".

## Groups and parenting

- **Group** — several objects that move as one: a `scene_ref` layer whose scene is a 3D
  scene with only `space` (and `duration`) in its composition. The group's `transform` and
  `animations` place the whole; its objects keep their own motion inside, on the group's clock.
  A sub-assembly built beside the main model, then flown in, is a group.
- **`parentId`** — one object rides a sibling's placement (position, rotation, scale) at
  every instant, keyframes and expressions included; opacity and time stay its own. Use it for
  a part that must stay attached to something that moves.
- **A carrier** — motion with nothing drawn, for several objects to ride: a group whose scene
  has no layers, holding the motion, and the objects parented to it. An object's own
  `animations` then stay free for its entrance or its loop.

  ```json
  "assets": { "rig": { "type": "scene", "scene": { "composition": { "space": "3d" }, "layers": [] } } },
  "layers": [
    { "id": "rig", "content": { "kind": "scene_ref", "assetId": "rig" },
      "animations": { "position": { "keyframes": [{ "time": 0, "value": [-1, 0, 0] }, { "time": 2, "value": [1, 0, 0] }] } } },
    { "id": "car", "parentId": "rig", "content": { "kind": "model", "assetId": "car" } }
  ]
  ```

## Lights

- **A light layer** — `content: { kind: "light", type: "point" | "spot", intensity, color }`: a light that
  stands in the scene, placed by the layer's `transform` and `animations` and parented by `parentId`. The rig's
  `key`, `fill` and `rim` are directional and light everything; a light layer lights what is near it. `scale`
  and `opacity` on it are refused (`light_layer_field`); dim it with `intensity`.
- **Units.** At 1 m a surface facing it is as bright as under a key of the same `intensity`; it falls off as
  `1 / d^decay` (`decay` 2 by default), and `range` (metres) fades it to nothing there.
- **A spot** shines along the layer's −z: `rotation: [-90, 0, 0]` shines straight down. `angle` is degrees from
  its axis to the cone's edge (default 30), `penumbra` 0..1 softens the edge.
- **Shadows.** `shadow: { softness }` makes it cast them (a point light every way; a spot's `angle` at most 85);
  omitted, it casts none. Each one renders a shadow map (six for a point light) every frame: give it to the
  lights that need one.
- **Its tracks** are on the layer's clock. A colour expression returns `Color.rgb(r, g, b)` (0..1), never a hex
  string. Lights pulsing on a beat: [references/recipes.md](references/recipes.md).

## Cards

A card is a flat picture `width` metres wide (default 1), its height from the picture's aspect,
facing +z; `lit: false` shows it at its own colours.

- **Media card** — `content.kind: "media"` with an `image`, `svg`, `video` or `video_with_matte`
  asset. A video plays on the layer's clock: at layer time t it shows `trim.in + t × speed`,
  holding its last frame past `trim.out` unless `loop`. A `video_with_matte` is cut out by its
  matte. A card plays no sound: put the audio in the 2D scene around the 3D one.
- **Scene card** — a `scene_ref` whose scene is 2D (`assetId`, or an inline `asset`): the scene
  drawn flat, its composition `width`/`height` its aspect. `parameters` are its bindings, keyed
  on the card layer's clock: a sign's text, a screen's colour, a track a 2D template animates.
  A card's body is written out: to play a template, the body declares the parameters it takes
  and passes them to one `scene_ref` layer pointing at the template. `width` and `lit` belong to
  a scene card only; a group refuses them.
- A card is a flat plane: use it for screens, signs, posters and other 2D in 3D. It does not
  follow a bone; a picture painted on a model's surface is a material slot.

```json
{ "id": "sign", "transform": { "position": [0, 1.6, -2] },
  "content": { "kind": "scene_ref", "width": 1.2, "lit": true,
    "asset": { "type": "scene", "scene": { "composition": { "width": 600, "height": 200, "duration": 4 },
      "parameters": { "label": { "type": "text", "default": "OPEN" } },
      "layers": [{ "id": "t", "content": { "kind": "text", "text": { "$eval": "label" } } }] } },
    "parameters": { "label": "PLAY TIME" } } }
```

## Motion presets

`picsart_scene_apply_preset` with `preset: "motionPreset:<id>"` puts a preset on a 3D object
(`layerId`) or on the camera (no `layerId`). Defaults are tuned; pass only what you change. `orbit`,
`dolly` and `push_in` also name a 2D composition-camera preset; on a 3D scene the 3D one below
applies. Every `motionPresets` entry of `picsart_scene_capabilities` says its `space`; keep the
entries whose `space` is `3d`.

| Object preset | What it does | Params (default) |
|---|---|---|
| `drop_in` | Falls from above, lands, squashes | `duration` 0.5, `height` 0.6, `squash` 0.12 |
| `fly_in_arc` | Flies in on a rising arc, spinning, slows into place | `duration` 0.8, `distance` 0.8, `direction` right, `arc` 0.4, `spin` 1 |
| `snap_settle` | Drawn in, overshoots, swings back, squashes on contact | `duration` 0.3, `distance` 0.15, `direction` down, `intensity` 0.3, `settle` 10, `bounces` 25, `squash` 0.1 |
| `bounce` | Hops and lands, squashing, every period | `height` 0.15, `period` 0.6, `squash` 0.1 |
| `idle_bob` | Slow rise, fall and tilt that never resolves | `period` 3, `distance` 0.03, `angle` 2 |
| `wiggle` | Smooth never-repeating drift and turn | `frequency` 1.5, `amount` 0.02, `angle` 3, `seed` 0 |
| `turntable` | Turns about the world vertical, keeping its tilt | `period` 8, `direction` counterclockwise |

| Camera preset | What it does | Params (default) |
|---|---|---|
| `orbit` | Circles the point it looks at | `start` 0, `duration` 6, `angle` 360, `easing` ease_in_out |
| `dolly` | Travels along the view, target with it | `start` 0, `duration` 2, `distance` 1 |
| `push_in` | Closes in on the target, which stays | `start` 0, `duration` 3, `amount` 0.3 |
| `crane` | Rises, still looking at the target | `start` 0, `duration` 2.5, `height` 1 |
| `whip_pan` | Swings the view fast, standing still | `start` 0, `duration` 0.3, `angle` 70, `direction` left |

How they combine:

- **An object's motion is relative to where it rests.** Entrances end exactly at the object's
  `transform`, loops start from it. Move the object afterwards and its motion moves with it.
  Time is the object's own: an entrance starts at the object's `start`.
- **One channel carries one expression.** Two presets that both drive an object's position
  (say `drop_in`, then `idle_bob`) — the second replaces the first, and the result says so in
  `notes`. To follow an entrance with a loop, give the loop its own object: a group or a
  `parentId` parent holding the loop, the object holding the entrance.
- **Camera moves chain.** Each move starts where the camera is at its `start`; keyframed moves
  (`dolly`, `push_in`, `crane`) append, so `dolly` 0–2 then `crane` 2–4 runs as one path. A move
  starting inside existing camera keyframes is refused; start it at or after the last one.
  `orbit` and `whip_pan` ride whatever path is there and hold their end angle — so apply them
  **last**: a keyframed move after one cannot tell where the camera is, and is refused. They
  turn about the point the camera looks at (orbit) or stands at (whip pan) as it is at their
  `start`, so that point must have stopped moving by then. Each reads the channel the other
  turns, so a camera takes one of them: orbit through a shot, or whip pan out of one.

Worked sequences — a build of parts on a beat grid, an object that builds itself and then drives
off, the whole scene pulsing on the beat — are in [references/recipes.md](references/recipes.md).

## Render and verify

- **Validate.** `picsart_scene_validate`; a 3D document always carries a warning that a translated
  target cannot draw it — that warning is expected, nothing else is. Validation does not read a model
  at a URL: a `materials` override or `action` the model lacks shows up only when it renders, so take
  the names from the `picsart_scene_import_model` report.
- **Render.** `picsart_scene_contact_sheet` with `times` draws the moments you name into one sheet;
  `picsart_scene_export` renders the video, or one frame with `mediaType: "png"` and `startTime`. Both
  take the 3D document as it is, or a 2D scene that plays it, and draw the same frame at the same
  time. `parameters` set the scene's declared parameters on both. Look at **one** contact sheet
  through several `times`, not one render per still.

  ```jsonc
  // a bare 3D scene at fps 15 declaring `tilt`; times are multiples of 1/15 (the render's frame grid):
  picsart_scene_contact_sheet { "scene": <scene>, "parameters": { "tilt": 30 }, "times": [0.4, 1.2, 1.8] }
  ```

- **Text goes over it in 2D.** A 3D object is a model, a card or a group — no text drawn in 3D. A
  title is a 2D scene playing the 3D one through a `scene_ref` whose `parameters` pass the caller's
  values on, with the text layer beside it; render and export that 2D scene as it is.
- **Measure, don't eyeball.** Render a check view: a side or top `camera`, no `shutterAngle`, a
  small `width`/`height`, and a contact sheet with `times` around the motion — exact frames to
  look at. `picsart_media_track_motion` on the exported video (`targets: [{ bbox }]` on the moving
  part) returns the part's position every frame — of the final composite, so a 2D layer drawn over
  the part, or a background of the part's colour, moves the box too: track a check view with a plain
  contrasting `background` on the 3D document and nothing over it. Check that an entrance lands
  exactly on its `transform`, that nothing sinks below y = 0, that a moving part's box never crosses
  one already placed, and that the camera path is continuous across shot seams.
- **Pitfalls.**
  - A `parameters` name the scene does not declare is refused, naming the tool and the names it
    does declare: read them from the scene's `parameters` block, not from memory.
  - The render is a video at the scene's `fps`: a time between two of its frames draws one of them.
    Ask for times on the grid (`n / fps`) when comparing moments, or two "different" times can show
    the same frame.

## Gotchas

- **A one-number `scale` is one number to an expression.** `transform.scale: 10` makes a
  hand-written expression's `value.y` fail; write `[10, 10, 10]`. Presets convert it for you.
- **An expression returns `Vec.v3(x, y, z)`, never a Lua table** — `{1, 2, 3}` fails to
  evaluate. Read components as `value.x` or `value[1]`; `value * 2` and `value + Vec.v3(…)` work.
- **Another layer's depth is `getPlacement():z()`**, beside `position()` and its heading `rotationY()`.
- **The camera's `eye` and `target` have no resting value**, so an expression on one needs
  keyframes to start from; `orbit` and `whip_pan` write that keyframe for you.
- **Rotation keyframes interpolate the numbers.** `[0, 0, 0]` to `[0, 360, 0]` is a full turn;
  `[0, 350, 0]` to `[0, 10, 0]` turns 340° back. A turn about the world vertical on a tilted
  object is `turntable`, not a y keyframe.
- **Final values exactly.** A landing pose written with rounded numbers lands a hair off its
  neighbours; write the same numbers as the resting `transform`.
- **Something sinks into the floor.** Its origin is not at its base — lift it by its height.
- **A squash lifts the object off the floor.** Same cause: a squash flattens toward the origin.
- **The backdrop never shows.** The camera is looking down at a drawn floor; bring the horizon
  into frame, or make the ground `shadowOnly`.
