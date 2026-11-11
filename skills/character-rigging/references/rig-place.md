# Placing a rig and its sockets, draw order and head turn

Part of [the character-rigging recipe](../SKILL.md); one section of it, read on its own.

A 2D cartoon character starts from a catalog rig when one fits, or from `picsart_scene_build_model` with
`character: {svg, duration: 4}` for named SVG parts ([rig-build.md](rig-build.md)); without `svg` that tool builds a 3D
model. Not from hand-written joint Lua: one no rig fits is built by hand from bent limbs and `ik`
([references/character-motion.md](character-motion.md), which also builds an arm as one shape), its ink lines
pointed at the ends with a stroke `taper` ("Ink lines" in [rig-act.md](rig-act.md)).
`picsart_scene_templates` with `tags: ["cartoon", "rig"]` lists them:

| Template | What it is |
|---|---|
| `scene://rig-humanoid` | A whole body, three-quarter view facing right, 600×1000, transparent |
| `scene://rig-face` | A face from the front, 800×800, transparent |

Place one as a `scene_ref` layer (`picsart_scene_apply_template`, reference mode); size it with the layer's
`transform.scale` or `bounds`, and mirror it (`scale` x negative) to face left. Every part is a shape
layer pivoting on its joint. Each arm and leg is one outline bent at the elbow or knee (a `bend` with
an `id`), posed by an `ik` constraint that reaches for a target layer (`leftFootTarget`,
`rightHandTarget`, ...); the hand or foot is `attach`ed to the limb's end
([references/character-motion.md](character-motion.md)). The torso and neck are one outline
`skin`ned to the empty `spine` and `neck` bone layers, which `spineLean` and `headNod` turn inside
the `min`/`max` on their rotation tracks; the arms hang from `spine` and the head from `neck`.
The template poses the parts from its parameters, and each FK parameter's `min`/`max` is its joint's
limit. Animate only the parameters: key them in the layer's
`content.parameters` (`{"leftUpperArmRaise": {"keyframes": [...]}}`), or apply a rig preset.

**Sockets, reach and held props.** A placed character publishes sockets (`head`, `chin`, `chest`, hands, grips, feet, `seat`, `mouth`, `held`; a dog or cat `mouth`, paws, `body`, `tail`): a parent targets `{"layer", "socket"}` and Lua reads `getSocket`. A `reach` constraint on the instance layer puts a socket on a stage point (`{"type": "reach", "socket": "rightHand", "target": {"layer": "ball"}, "mix": 1}` lands a hand on a ball; `"seat"` on a bench seats the character). A humanoid rig or a dog or cat holds a prop itself through `held` and `heldBy` (`right`, `left`, `chest`, `mouth`, `none`; an animal only `mouth` or `none`), two hands by `<side>HandToHeld`. Tables, the `via` dial, carriers and worked cases: [references/sockets-and-props.md](sockets-and-props.md).

**Read the bone map.** `picsart_scene_inspect` with `mode: "rig"`; pass an embedded rig asset key as `scope` and optionally `layer` for a subtree. Read entries in order, indenting by `level`: hips first, parents before children. The map derives bones from skins and constraints, so an unreferenced joint mark is absent; `parentId` is parenting, not art ownership. A standard name is that bone (`leftUpperArm` names the left upper arm). Keep imports' source names; any non-standard layer, including an imported bone or a plain parent frame, reads `helper` (IK targets read `target`); a helper is an ordinary layer, not a separate skeleton declaration. Placements resolve `$eval` at scoped parameter defaults, without use-site bindings: read them as authored rest, not a posed measurement. Drivers are lexical reads; Lua, time tracks, poses and automatic weights are not evaluated. Use `picsart_scene_query_layout` for evaluated geometry.

**Draw order.** The far arm and leg draw behind the torso and the near ones in front, by document
order; an arm hangs outside its thigh, so the far arm draws behind the far leg and the near arm in
front of the near leg. An `ik` chain authors no depth (a `z` within ±1, static or a keyed `by` track with no expression, only orders the drawing and is allowed on a chain bone), so the order holds in every pose of a flat scene: a raised far
arm stays behind the head (wave with the near arm, or the far arm forward beside the face), and a far
hand swung forward past the far thigh stays behind it. The near hand shows its back, the far hand its
palm; both thumbs sit on the forward edge. A turned face's far ear goes behind the head, driven by
`headTurn`: don't key `z` yourself. The order holds only while the whole composition is flat: put one layer in depth (a `z` beyond ±1, an expression `z`, `rotationX`/`rotationY`) or orbit the camera and every `z` of the scene, the rig's too, is depth (an `ik`, `skin`, `follow_through` or preset travel on a chain is then refused, and the validator warns `z_order_mixed_with_depth`).

**A 2D head turn.** `headTurn` (0 face on, ±1 a three-quarter view, + toward + x) and `headTilt` are the one turn and tilt dials of both rigs: key them, never the features. A face built by hand turns the same way (feature depths, eyes, outline morphs, ears, timing, profile swap, verify sweep): read [references/head-turn.md](head-turn.md). Set `headSize`, `hairStyle` and `faceShape` per instance, never keyed across a shot (a keyed `hairStyle` pops); a different build is a second rig. `headSize` above about 1.2 with hairStyle 2 lifts the quiff 80 px higher, so leave headroom.
