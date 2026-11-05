---
name: character-rigging
description: Build and animate a 2D cartoon character in a scene — rig-humanoid and rig-face, their control names and ranges, walk_cycle, acting and drivers on a rig, two-bone IK, draw order, tapered ink lines, lip sync — and the craft of morphing a shape's outline — preparing two drawings so they morph without twisting, choosing between outline keyframes, morph targets, per-vertex tracks and outline expressions, blend-target hygiene, timing (anticipation, overshoot, holds), volume-keeping squash, face visemes and blinks, scene-to-scene morph transitions, bending a picture over an art mesh, and explicit skin weights. Use when a cartoon character, mascot or face walks, waves or talks; when a path's outline changes shape over time — one drawing becomes another; a jelly, blob or character squashes, stretches, bounces, wobbles or breathes; a cartoon face talks (lip sync, mouth shapes), smiles or blinks; a cut is hidden by a morph; or an image, text or composition has to bend.
metadata:
  category: authoring
  version: '1.6'
  ported-from: shape-morphing 1.6 at 55.91.0
user-invocable: false
---

# Cartoon characters and shape morphing

Field names are the `path` item's (`picsart_scene_capabilities` with `sections: ["schema:ShapeContent"]`); the outline mechanics are in
[references/outline-mechanics.md](references/outline-mechanics.md).

## Named motions on a rig

A rig document can declare root `actions`, named motions an instance plays: bone tracks go in
`actions.<name>.layers`, drawing and order selectors in `actions.<name>.parameters`. Keep the
skeleton and painted weights once, with static rest transforms; place the rig once and use the
`scene_ref`'s `content.animation` to blend one action into the next (walk→idle). Set
`content.blending: "pass_through"` so limbs can reach beyond the rig's frame without canvas padding:
under pass_through the frame sizes and places, it does not clip. A layer treatment that needs a
composited result (mask, effect, non-normal blend, opacity below 1, motion blur, mesh, stroke or shadow,
adjustment or look) isolates and clips it. Action bodies have time keys, no `$eval` or expressions;
layer expressions and constraints run after the mix. Step channels switch immediately. Delayed first
keys need the `beforeFirst: "rest"` action policy. `animations` is a layer field and the action stack is
`content.animation`; root `actions` are distinct from a track content's sequential `clips`. Catalog rig
presets stay parameter bindings, not actions. The schema is `picsart_scene_capabilities` with
`sections: ["schema:SceneAction"]`; the full crossfade example is in
`picsart_scene_recipe scene-animation-reference`.

## 0. Cartoon character rigs

A 2D cartoon character starts from a catalog rig when one fits, not from a 3D
model and not from hand-written joint Lua; one no rig fits is built by hand from bent limbs and `ik`
([references/character-motion.md](references/character-motion.md)), its ink lines
pointed at the ends with a stroke `taper` ("Ink lines" below).
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
([references/character-motion.md](references/character-motion.md)). The torso and neck are one outline
`skin`ned to the empty `spine` and `neck` bone layers, which `spineLean` and `headNod` turn inside
the `min`/`max` on their rotation tracks; the arms hang from `spine` and the head from `neck`.
The template poses the parts from its parameters, and each FK parameter's `min`/`max` is its joint's
limit. Animate only the parameters: key them in the layer's
`content.parameters` (`{"leftUpperArmRaise": {"keyframes": [...]}}`), or apply a rig preset.

**Standard control names**, shared with 3D characters: a face takes VRM expressions, a body `<vrmBone><Motion>`, hair, ears and tails `<part><Motion>` (`Sway` is a side-to-side pendulum). Any rig of the same type uses the same names
and ranges, so a preset or a keyed track moves every one of them.

| Rig | Parameter | Range | Meaning |
|---|---|---|---|
| both | `blink`, `blinkLeft`, `blinkRight`, `aa`, `happy` | 0..1 | eyes shut, one eye shut (the left eye is on + x), mouth open, smile |
| both | `headTurn`, `headNod`, `headTilt` | −1..1 | turn toward the viewer's right (0 face on, ±1 a three-quarter view; on the humanoid + toward +x the way its body faces), chin down, roll clockwise |
| both | `lookUp`, `lookDown`, `lookLeft`, `lookRight` | 0..1 | irises' direction; `lookLeft` is + x on screen (on the humanoid an eye turned away travels less across) |
| both | `ih`, `ou`, `ee`, `oh` | 0..1 | the other visemes |
| humanoid | `browInnerUp`, `browOuterUpLeft`, `browOuterUpRight`, `eyeWideLeft`, `eyeWideRight` | 0..1 | both brows' inner ends up; one brow's outer end up; one eye opened wide (a blink still shuts it) |
| face | `sad`, `angry`, `surprised`, `relaxed` | 0..1 | moods (mouth, eyes, brows) |
| humanoid | `spineLean`, `hipsRaise`, `hipsTilt` | −1..1 | torso lean ±20° (+ forward); hips ±60 px (+ up); pelvis roll ±10° (+ clockwise, the + x hip drops), the legs following on their IK and the shoulders tilting against it |
| humanoid | `breath` | 0..1 | breath: the chest swells, shoulders and head rise |
| humanoid | `<side>UpperArmSwing` / `UpperArmRaise` / `LowerArmSwing` / `HandSwing` | −1..1 / 0..1 / 0..1 / −1..1 | arm ±80° (+ forward); raised forward and up 0..160° (0 hangs, 0.5 forward, 1 overhead); elbow 0..150°; wrist ±40° |
| humanoid | `<side>UpperLegSwing` / `LowerLegSwing` / `FootSwing` | −1..1 / 0..1 / −1..1 | leg ±70°; knee 0..140° (elbow and knee limits are their bends' `min`/`max`, binding IK too); toe up ±35° |
| humanoid | `<side>HandSpread`, `<side>HandPoint`, `<side>HandFist` | 0..1 | hand poses on a palm, four fingers and a thumb, the relaxed open hand at 0: fingers fanned (the waving hand), the index pointing, a fist; the three share the hand (scaled to 1 above a sum of 1, the relaxed hand filling the rest), so a crossfade is two keyed weights |
| humanoid | `<side>HandIk`, `<side>FootIk` | 0..1 | the limb's `ik` `mix`: from the swings to the target (feet default 1, hands 0) |
| humanoid | `<side>HandX/Y`, `<side>FootX/Y` | −400..400 | the target layer, rig px from the resting wrist or ankle |
| humanoid | `hairSway`, `hairRaise`, `earSway` | −1..1 | follow-through, morphs inside the head: hair and quiff swing (+ toward + x), hair raise (+ up), ear rim swing (+ toward + x); key them a few frames behind the head |
| humanoid | `headSize` | 0.8..1.25 (1) | head size: the whole head (features, hair, ears) scales about the neck, the body does not; the planted feet and every limb are untouched |
| humanoid | `hairStyle`, `faceShape` | whole numbers 0..2 | which drawing shows: hair 0 the cap with a fringe, 1 cropped, 2 a tall quiff with long sideburns; skull 0 round, 1 long (chin 14 px lower), 2 short (chin 14 px higher). Drawings swap with `step` keys, they do not blend; the other head controls (`hairSway`, `hairRaise`, `headTurn`) move every style |

`<side>` is `left` (the far side, behind the body) or `right` (the near side).

**IK.** A limb on IK puts its wrist or ankle on the target and bends at the elbow or knee to reach it
(knees fold forward, elbows back); a target out of reach straightens the limb toward it. The swings
still pose the limb under a partial `mix`. The targets are in the rig's own space and stay where they
are while the body moves, so a foot that keeps its target is planted: lower
`hipsRaise` and the knees bend. To touch something, set `<side>HandIk` 1 and key `<side>HandX/Y`.

**Gesture arms: raise × elbow.** Up to a 60° raise (`UpperArmRaise` ≤ 0.375), the natural
elbow bend folds the hand onto the face. Measured safe pair for a wave or a talking gesture:
`UpperArmRaise` 0.25–0.36 with `LowerArmSwing` 0.45–0.55. Unsafe, hand at the nose or mouth: raise 0.36
with elbow 0.85, raise 0.2 with elbow 0.7. Swing the hand with `HandSwing`, not by bending the elbow
further, and check a `picsart_scene_contact_sheet` for the hand against the head.

**Draw order.** The far arm and leg draw behind the torso and the near ones in front, by document
order; an arm hangs outside its thigh, so the far arm draws behind the far leg and the near arm in
front of the near leg. An `ik` chain authors no depth, so the order holds in every pose: a raised far
arm stays behind the head (wave with the near arm, or the far arm forward beside the face), and a far
hand swung forward past the far thigh stays behind it. The near hand shows its back, the far hand its
palm; both thumbs sit on the forward edge. A turned face's far ear goes behind the head, driven by
`headTurn`: don't key `z` yourself.

**Motion.** Everything goes on the rig's `scene_ref` layer with `picsart_scene_apply_preset`
(`preset` `motionPreset:<id>`, `layerId` the rig layer), and writes bindings in its `content.parameters`:

- `walk_cycle` (tag `rig-motion`): one stride of keys (two steps of `stepDuration`) from `start`,
  looped with `ctx:loopOut`; keys the foot targets (`<side>FootX/Y`, `FootIk` 1) and `FootSwing`,
  `hipsRaise`, `spineLean`, `headNod` and the arms' swings, forearms and hands lagging, and moves the
  layer (`travel` `forward`, or `in_place`). Each step the body eases one stride forward while the
  planted foot's target eases the same stride back, so the foot stays put. A rig missing one of those
  names is refused, naming it.
  **A walk that stops** (a walk-in, a stop, an action, a walk on): `steps` `N` walks `N` whole steps and
  stops with every walking parameter on its rest value, instead of looping. `from` `rest` opens with a
  half-step out of the rest pose and ends with the half-step back, so the layer carries `N` × `stride`
  (the half-steps count as one of the `N`); `from` `walking` (the default) starts on the first walking pose
  and adds the closing half-step. Both feet are planted whenever neither is lifted, in the half-steps too.
  Pitfall: never settle the rig by hand after a `steps` walk (a key on the same parameters is a second
  writer, and pops at the stop); the arms take 0.15 s longer than the feet to come to rest. Use a fresh
  `walk_cycle` for the next walk, `start` after the action. `steps` with `travel` `forward` needs the same
  plain layer as the loop.
- `ground_scroll` (tag `rig-motion`): the set's side of a walk across a scrolling background. Walk the rig
  `in_place`, put the scenery under one parent layer (an empty one is fine), and apply `ground_scroll` to
  that parent with the walk's own `start`, `stepDuration`, `stride`, `steps` and `from`, `direction`
  `right` for the rig as drawn (`left` for a mirrored one) and `walkerScale` the walker layer's drawn size
  (its scale times its fit; `stride` is in rig px). The parent moves against the travel on the same clock,
  so the planted foot stays still on the ground; pair it with the camera's `push_in` on a pivot at the
  walker. Pitfall: change a walk's numbers in both presets, or the feet slide.
- Gestures (tag `rig-motion`, `gesture`): `wave`, `talk_beat`, `point` and `shrug`, each `start`,
  `duration` (seconds from the arm leaving rest to its return), `amount` 0..1, and for `wave`, `talk_beat`
  and `point` a `side` (`right` the near arm, `left` the far one); `wave` and `talk_beat` also `count`
  (swings or beats). They lift the arm inside the safe pair (raise 0.25 to 0.36 at an elbow of 0.45 to
  0.55, so the hand stays off the face) and return every control to rest. `wave`: the hand swings from the
  wrist `count` times. `talk_beat`: the forearm beats with the speech, the hand follows. `point`: the arm's
  IK takes the wrist to `targetX`, `targetY` (rig px from where it rests, y down, default up and
  forward); the limb straightens toward a target out of reach, and the hand forms a point (`HandPoint`). `shrug`: both arms, the hands turned, the
  head tilts and the breath rises (no `side`, no `count`). Use cases: a greeting, a character talking with
  its hands, indicating an object, an "I don't know". Pitfalls: a gesture replaces a walk's bindings of the
  same arm (the result's notes say so), so apply it after the walk and give it a `start` inside the
  walk; `point` is IK, so a hand at a fixed target stays there while the body moves.
- `acting` (tag `rig-motion`): the character acts from commands. Key the text parameter `action` on
  the scene holding the rig layer (the preset declares it, default `idle`, when it has none) and the
  rig plays each key's motion from that key: `idle` (weight shifting leg to leg),
  `wave` (the near arm), `point` (the near arm, head and eyes at `pointX`/`pointY`, rig px),
  `talk` (head nods, brow lifts and hand gestures on beats; the mouth is the visemes', keyed apart),
  `walk` (`walk_cycle` from a half step on the key, closing the feet with a step when it stops, so no
  planted foot slides; `stepDuration`, `stride`, `lift`, `armSwing`, `bob`, `lean`, `travel` as
  `walk_cycle`'s). Its text parameter `action` selects a preset command; the `action` field in
  `content.animation` selects a named action from the rig document. Any other text plays `idle`.
  Each switch crossfades over `fade` (0.2 s), longer for a joint with further to go, what was playing carrying on under it, the forearm, hand and head
  trailing by 2 frames or more:
  `{"action": {"type": "text", "animatable": true, "default": {"keyframes": [{"time": 0, "value": "idle"},
  {"time": 2, "value": "wave"}, {"time": 4, "value": "walk"}, {"time": 7, "value": "point"}]}}}`.
  It drives every name its clips key and the walk's, so on one rig it takes the place of
  `walk_cycle`, never beside it; for life add `random_pulse` on `blink` and `cycle` on `breath`,
  which it leaves free. The clips key standard
  names only, so any rig with them acts. One `action` serves every rig in its scene: give each character its own scene to act
  apart.
- Everything else is a parameter driver with `parameter` naming the rig's control — the "Parameter
  drivers" table in [references/character-motion.md](references/character-motion.md):
  `random_pulse` on `blink`, `cycle` on `breath` (sine, ~3.5 s, `to` ≈ 0.6), `random_hold` on the
  `look*` gaze. A different `seed` per character keeps two from blinking together. Parameter-mode
  `follow_through` on catalog-rig controls needs an owned scene body: a binding reads its host's
  parameters, not the rig's. Omit `parameter` to apply world-motion layer physics to a rig layer.

They combine on names they do not share: `walk_cycle` or `acting` with the blink and breath
drivers. A walk's travel follows the layer's size
when it is applied: set the layer's scale first. Travel needs a plain layer (no look, effect,
parent, transform track or component ahead, speed 1, untrimmed); anything else takes `in_place`. One
preset drives a name on a rig: a preset writing a name another preset already drives there is
refused as `rig_parameter_driven`, naming both; re-applying the same preset, or writing over a name
you keyed by hand, replaces that binding and says so in `notes`.

Verify a walk on a contact sheet (`picsart_scene_contact_sheet`): the legs alternate, the arms swing
against them, and the planted foot does not slide.

**Ink lines.** A hand-drawn line thins at its ends and swells in the middle: a stroke with a `taper`.

```json
{"type": "stroke", "color": "#1a1a1a", "width": 7, "lineCap": "round",
 "taper": {"startLength": 0.5, "endLength": 0.5}}
```

`startLength`/`endLength` are shares of each contour's length (`lengthUnits: "pixels"` for px), and
the line narrows to `startWidth`/`endWidth` (shares of `width`, default 0, a point) over them;
`startEase`/`endEase` (0..1) bow the ramp so the width recovers sooner. The lengths are measured on
the outline as drawn, after a `bend` or a `trim`, so a bent limb keeps its thin ends and a draw-on
keeps its point on the moving end. `wave` swells and narrows the width along the line.

**A 2D head turn.** `headTurn` (0 face on, ±1 a three-quarter view, + toward + x) and `headTilt`
are the one turn and tilt dials of both rigs: key them, never the features. rig-face turns its
features on their layers' transforms (`nose`, `leftEye`/`rightEye`, the brows, `mouth`, the ears),
so a drawing put in a feature layer turns the same way. A face built by hand turns the same way:

- **Depths.** Each feature turns round the head's vertical axis at its own depth `r`, starting at
  angle `φ = asin(x / r)` for its face-on `x`: `x = r · sin(φ + a)`, `a` the turn's angle (rig-face:
  40° at ±1). The nose stands proudest (rig-face 250 px on a 500 px head), then the mouth (210),
  then the eyes and brows (190); the outline moves least, by its morph. A nod moves each feature
  round the head's centre too, and a feature nodded low turns at the narrower jaw: scale `r` by the
  head's width at its new height.
- **Eyes.** The far eye is the one on the side the face turns toward: it narrows (scale x
  `cos(φ + a) / cos φ`, held at 0.55 or more), moves less and ends near the silhouette. The near
  eye keeps its width or grows a little (up to 1.08) and moves more. Both pupils lead the turn
  (rig-face: 16 px at ±1). Brows narrow with their eyes.
- **Outline.** Give the head outline a `turnRight` and a `turnLeft` morph target (the mirror),
  weighted by `max(0, ±sin a) / sin a_max`. Move the points mostly along x: the cheek and brow ridge
  push out on the face side, the jaw and chin come round more than the crown, the back flattens.
  Keep the handles, and lengthen them only where the outline flattens, so it stays round. Hair
  morphs with it, its fringe wrapping round with the face. Check every outline at a sweep of turns
  for a self-crossing: a fringe end that slides past the tip it hangs from loops there.
- **Ears.** Hang each ear on the outline's side at its height and slide it round with that side,
  not on the turning sphere: an ear placed past the 90° silhouette swings against the turn while
  the outline moves with it, and comes away from the head. The near ear widens and comes over the
  side toward the cheek, the far one narrows and tucks behind the outline; both move the way the
  face turns and touch the outline at every turn. Each ear's `z` follows the turn's sign: the near
  ear 1, over the head, the far one −1, behind it. Stand both ears just clear of the outline face on,
  so the swap at 0 changes nothing drawn.
- **Timing.** Lead with the eyes: the pupils (`look*`) a few frames before the head. Then key the
  turn past where it settles and back: to 0.95 and settle at 0.85 over about 0.2 s. Keys outside the
  dial's `min`/`max` warn, so the overshoot stays inside ±1. Hair and ears trail by a couple of
  frames (`hairSway`, `earSway` on the humanoid).
- **Profile.** Beyond about 0.8 a three-quarter drawing stops reading; swap to a profile drawing
  with `step` keys `by` the dial: its `opacity` `{"by": "headTurn", "keyframes": [{"at": 0.8, "value": 0,
  "easing": "step"}, {"at": 0.81, "value": 1}]}`, and the front features' `opacity` the reverse. A full
  turnaround needs a drawing per angle.
- **Several characters from one rig.** Set `headSize`, `hairStyle` and `faceShape` per instance (the `scene_ref` `parameters`): a child is `headSize` 1.15 with a short `faceShape`; a grown-up a long one at 0.9. They are fixed per character: do not key them across a shot (a keyed `hairStyle` pops). A different build (taller, broader) is a second rig, not a dial. Pitfall: `headSize` above about 1.2 with hairStyle 2 lifts the quiff 80 px higher, so leave headroom in the frame.
- **Verify** with a rendered sweep −1 → 0 → 1: every feature stays inside the silhouette, nothing
  jumps between frames, the features' x offsets keep the depth order, and at |turn| 1 the eye on the
  turn side is the narrower one and both pupils are offset toward the turn.

## 1. Prepare the drawings

- Draw A and B each as its own best outline, then match them — the three things a morph needs:
  the same vertex count, the same winding (the sign of the signed area, Σ (xᵢ·yᵢ₊₁ − xᵢ₊₁·yᵢ),
  agrees) and the same start vertex on the same feature of both drawings.
- A missing vertex is added, not faked with a handle: an eased segment needs equal counts
  (`shape_path_vertex_count_mismatch`), and a handle dragged to stand in for a corner bulges mid-morph.
- Corresponding vertices should sit on the same feature of both drawings (top-centre to top-centre,
  tip to tip). Every vertex travels a straight line to its twin; unrelated twins cross and the
  outline twists through itself.
- Give the outline enough vertices for its roundest pose, and no more: 8 round a blob or a mouth,
  evenly spread, a flat contact edge included. With fewer, each span carries a bigger bend and the
  squashed, stretched or opened poses go lumpy. A morph reads through clear silhouettes. A drawing with many sub-shapes, holes or an
  open↔closed change does not morph; it swaps (§2) or dissolves.
- Round stays round: every smooth vertex carries `inTangent`/`outTangent` in every pose, sized to
  that pose (`r · 4/3 · tan(π / 2N)` for N vertices on a circle of radius r, `0.552·r` at 4). A pose
  that opens, widens or grows lengthens its handles in proportion; handles kept from a smaller pose
  flatten the curve and leave corners. A vertex without handles is a deliberate corner.
- A morph changes the outline only: the drawing's `fill` and `stroke` (width, join, cap) stay as
  drawn. A colour change rides on the fill's own keyframes, not on the outline.

## 2. Choose the technique

| Need | Write |
|---|---|
| One drawing becomes another (A→B, A→B→C) | `vertices` keyframe track, one `easing` per segment |
| Independent changes that mix (open + smile + blink) | `morphs`: named targets, each with its own `weight` |
| One part on its own timing (tail tip lags, one mouth corner) | static `vertices` list, that vertex's `point`/handles keyframed |
| Replace drawings without blending (mouth charts, frame-by-frame) | `"easing": "step"` on the earlier keyframe; counts may differ |
| A catalog mouth or cartoon wipe, no outlines of your own | `picsart_scene_looks {"tags": ["cartoon"]}`: `mouth_shapes` takes `shape` as a name (the visemes `rest`/`aa`/`oh`) or a step track of names; `squash_wipe` uncovers its layer |
| Loop, breathe, wobble | `vertices.expression`: `return ctx:loopOut("cycle")` repeats the outline keyframes; or a target whose `weight.expression` cycles (`return picsart.oscillate(time, 0, 1, 1.2)`), or a `scale` expression |

A path has one driver: a `vertices` track or per-vertex tracks, never both (`shape_path_driven_twice`).
`morphs` add on top of either, so a wobbling base can still smile.

```json
{ "type": "path", "closed": true,
  "vertices": { "keyframes": [
    { "time": 0.0, "easing": "step", "value": [
      {"point": [0, -80], "inTangent": [-44, 0], "outTangent": [44, 0]}, {"point": [80, 0], "inTangent": [0, -44], "outTangent": [0, 44]},
      {"point": [0, 80], "inTangent": [44, 0], "outTangent": [-44, 0]}, {"point": [-80, 0], "inTangent": [0, 44], "outTangent": [0, -44]}] },
    { "time": 0.4, "easing": "ease_in", "value": [
      {"point": [0, -80], "inTangent": [-44, 0], "outTangent": [44, 0]}, {"point": [80, 0], "inTangent": [0, -44], "outTangent": [0, 44]},
      {"point": [0, 80], "inTangent": [44, 0], "outTangent": [-44, 0]}, {"point": [-80, 0], "inTangent": [0, 44], "outTangent": [0, -44]}] },
    { "time": 0.7, "easing": "ease_out", "value": [
      {"point": [12, -96], "inTangent": [-46, 0], "outTangent": [46, 0]}, {"point": [96, 10], "inTangent": [0, -46], "outTangent": [0, 46]},
      {"point": [-8, 70], "inTangent": [46, 0], "outTangent": [-46, 0]}, {"point": [-70, -14], "inTangent": [0, 46], "outTangent": [0, -46]}] },
    { "time": 1.0, "easing": "ease_in_out", "value": [
      {"point": [0, -130], "inTangent": [-22, 0], "outTangent": [22, 0]}, {"point": [40, 0], "inTangent": [0, -72], "outTangent": [0, 72]},
      {"point": [0, 130], "inTangent": [22, 0], "outTangent": [-22, 0]}, {"point": [-40, 0], "inTangent": [0, 72], "outTangent": [0, -72]}] },
    { "time": 1.2, "value": [
      {"point": [0, -120], "inTangent": [-26, 0], "outTangent": [26, 0]}, {"point": [48, 0], "inTangent": [0, -66], "outTangent": [0, 66]},
      {"point": [0, 120], "inTangent": [26, 0], "outTangent": [-26, 0]}, {"point": [-48, 0], "inTangent": [0, 66], "outTangent": [0, -66]}] }
  ] } }
```
Hold (0–0.4, `step` on an identical outline) → breakdown at 0.7 that is not the midpoint → overshoot
past B at 1.0 → settle on B at 1.2. Each pose carries its own handles (`0.552 ×` its half-width or
half-height), so the circle stays round on its way to the tall ellipse.

### Puff or pinch a whole outline: `puckerBloat`

`{ "type": "puckerBloat", "amount": 40 }` reshapes every geometry item above it in its group (nested
groups included) around each contour's centre, the average of its vertices. A positive `amount`
bloats: each vertex moves `amount` percent of the way to the centre while its handles push out, so the
edges bow outward. A negative `amount` puckers: the vertices move out and the handles move in, into
spikes. `amount` is animatable, so one item takes a star to a flower and back:

```json
{ "kind": "shape", "items": [
  { "type": "polystar", "starType": "star", "points": 6, "outerRadius": 120, "innerRadius": 60 },
  { "type": "puckerBloat", "amount": { "keyframes": [
    { "time": 0, "value": 0 }, { "time": 2, "value": 60 }, { "time": 4, "value": -40 } ] } },
  { "type": "fill", "color": "#F2A33A" } ] }
```

A rounded badge whose sides puff out: bloat a SHARP `rect`, then round it with `offsetPaths`. Bloat on
a `rect` with `roundness` pinches each rounded corner into ears, and `roundCorners` after the bloat does
not smooth them. `offsetPaths` grows the outline by `amount` with round corners, so draw the rect
`2 × amount` smaller than the badge:

```json
{ "kind": "shape", "items": [
  { "type": "rect", "size": [232, 92] },
  { "type": "puckerBloat", "amount": 14 },
  { "type": "offsetPaths", "amount": 24 },
  { "type": "fill", "color": "#3A7BF2" } ] }
```

## 3. Targets (blend-shape hygiene)

- One target, one change, small: `jawOpen` moves the jaw vertices only, `{}` for every other vertex.
  Targets that each touch everything fight when mixed.
- A target that moves a smooth vertex moves its handles too: offset `inTangent`/`outTangent` along
  with `point` so that in the target pose the handles still point along the outline (parallel to the
  line between the vertex's two neighbours) and stay in proportion to the new curve (an opening lip's
  handles lengthen as it drops). An offset with `point` alone keeps the base's handles: what grew goes
  flat, what turned kinks.
- A corner that opens gains handles in the target: a closed mouth meets at sharp corners, an open one
  is rounded there, so `aa`/`oh` give each mouth corner short handles along the lips. A corner stays
  sharp only where the open drawing is sharp too.
- Offsets are relative to the base outline, so the base may be redrawn; the vertex count may not —
  every target has one offset per vertex (`shape_path_morph_vertex_count_mismatch`).
- A combination that looks wrong (smile × jawOpen pinches the corners) gets a corrective target whose
  offsets are only the fix, weighted by the product of the two drivers. Drive the two from
  `animatable` parameters and read them in the corrective's `weight.expression`.
- An in-between (the half-open mouth is not half of the open mouth): author a second target for the
  mid pose and cross-fade — `mid` rises 0→1 while `full` stays 0, then `mid` falls 1→0 as `full`
  rises 0→1.
- Keep weights in 0..1 except for a deliberate overshoot or anticipation (§4); weights are not clamped.

```json
"parameters": { "smile": { "type": "number", "default": 0, "animatable": true },
                "jaw":   { "type": "number", "default": 0, "animatable": true } },
...
{ "type": "path", "closed": true, "vertices": [
    {"point": [-60, 0]},
    {"point": [-30, -8], "inTangent": [-19, 2], "outTangent": [9, -1]},
    {"point": [0, -9], "inTangent": [-11, 0], "outTangent": [11, 0]},
    {"point": [30, -8], "inTangent": [-9, -1], "outTangent": [19, 2]},
    {"point": [60, 0]},
    {"point": [30, 8], "inTangent": [19, -2], "outTangent": [-9, 1]},
    {"point": [0, 9], "inTangent": [11, 0], "outTangent": [-11, 0]},
    {"point": [-30, 8], "inTangent": [9, 1], "outTangent": [-19, -2]}],
  "morphs": {
    "happy": { "offsets": [
        {"point": [-2, -10]}, {"inTangent": [0, -2], "outTangent": [0, 1]}, {},
        {"inTangent": [0, 1], "outTangent": [0, -2]}, {"point": [2, -10]},
        {"inTangent": [-1, -4], "outTangent": [0, 2]}, {}, {"inTangent": [0, 2], "outTangent": [1, -4]}],
      "weight": { "expression": "return ctx.composition:getParameters():smile()" } },
    "aa": { "offsets": [
        {"point": [4, 16], "inTangent": [0, 12], "outTangent": [0, -12]},
        {"point": [2, -6], "inTangent": [1, 4], "outTangent": [-1, -2]},
        {"point": [0, -9], "inTangent": [1, 0], "outTangent": [-1, 0]},
        {"point": [-2, -6], "inTangent": [1, -2], "outTangent": [-1, 4]},
        {"point": [-4, 16], "inTangent": [0, -12], "outTangent": [0, 12]},
        {"point": [-2, 38], "inTangent": [-1, -4], "outTangent": [1, 2]},
        {"point": [0, 41], "inTangent": [-1, 0], "outTangent": [1, 0]},
        {"point": [2, 38], "inTangent": [-1, 2], "outTangent": [1, -4]}],
      "weight": { "expression": "return ctx.composition:getParameters():jaw()" } },
    "happyAa": { "offsets": [{"point": [2, 3]}, {}, {}, {}, {"point": [-2, 3]}, {}, {}, {}],
      "weight": { "expression": "local p = ctx.composition:getParameters() return p:smile() * p:jaw()" } } } }
```
Eight vertices clockwise from the left corner: corners 0 and 4, upper lip 1–3, lower lip 5–7. The
lips are smooth, each handle `4/3 · tan(Δθ/4)` of the arc it spans. `aa` opens to a round mouth
(a 56 × 34 half-axis ellipse): every lip vertex moves with its handles, and the corners gain handles
of 12 so the open mouth rounds off there. `happy` lifts the corners without handles, because a
smile's corners stay sharp, and re-aims the lip handles along the lifted line.
On the eye path, a blink is one target with a hold at closed:
```json
"morphs": { "blink": { "offsets": [{}, {"point": [0, 14]}, {}, {"point": [0, -14]}],
  "weight": { "keyframes": [{"time": 1.40, "value": 0, "easing": "ease_in"}, {"time": 1.48, "value": 1, "easing": "step"},
                            {"time": 1.54, "value": 1, "easing": "ease_out"}, {"time": 1.66, "value": 0}] } } }
```

## 4. Timing

- Anticipation: a small move the other way first — `weight` 0 → −0.15 → 1, or an outline keyframe
  a little "before A" ahead of the main segment. Short: a few frames.
- Overshoot and settle: `weight` 1.2 → 1, an outline keyframe past B followed by B, or a
  `cubic_bezier` easing whose `y` leaves 0..1 (`[0.175, 0.885, 0.32, 1.275]`); render to check the
  peak, the control number is not the overshoot.
- Slow in / slow out: `easing` on the starting keyframe of every segment, per target weight; a
  keyframe without `easing` is `linear` — right for a hold-to-swap, wrong for a pose change.
- Holds: repeat the value on the next keyframe, or `"easing": "step"`. Keys read when they rest.
- Follow-through: parts arrive at different times — a second target whose weight keyframes are
  delayed, or a per-vertex track lagging the body.
- Timing is the count of frames between poses; spacing near a pose is tight (ease), the middle is
  wide. A morph under ~0.2 s reads as a swap — then write the swap.

## 5. Breakdowns

The middle drawing is not the average of A and B. Favour one key, and add the extra movement the
straight path lacks (A → Z → B): a third outline keyframe, or a transient target that peaks mid-way
(`weight` 0 → 1 → 0 across the A→B segment) on top of the track. Vertices travel straight lines, so
an arc, a bulge or a lean exists only as a breakdown.

## 6. Volume

A squash keeps its area: lower by ×0.8, widen by ×1.25. For a target, the squash offsets lower
the top and push the sides out together, and stretch the horizontal handles of the top and bottom
by the same ×1.25 (shorten the vertical ones by ×0.8) so the widened body stays round; for a whole-layer squash, `scale` `[1.25, 0.8]` with the
`anchor` on the contact edge. Measure the ink area on `picsart_scene_contact_sheet` frames rather than trusting the numbers; the eye reads volume loss as deflation.

## 7. Faces

- Name mouth targets by the VRM presets: `aa`, `ih`, `ou`, `ee`, `oh`; eyes `blink`, `blinkLeft`,
  `blinkRight`; moods `happy`, `angry`, `sad`, `relaxed`, `surprised`. Consonants borrow the nearest
  vowel at a lower weight.
- Visemes cross-fade: at any moment the viseme weights sum to about 1, each segment eased, with a
  short hold on a stressed vowel.
- Lip sync from word timings: `picsart_scene_apply_preset` with `preset` `lipSync:visemes`, `layerId` the
  rig layer and in `params` the transcript (a `captions` `transcript`, as transcription returns it) and
  the face's `visemes`; it merges one track per control into the rig layer's `content.parameters`. It opens a syllable per vowel group, leads the sound by 50 ms,
  dips rather than shuts inside fast words, and closes on rests and on every m, b and p (60 ms shut up
  to the release; `closures` lists them). `speaker` picks one singer's segments, `gain` scales the
  opening, and `start`/`end` cut and rebase the tracks for a layer that plays only part of the song.
- Replacement drawings: pass `mouthShapes` mapping each drawing's name to its number on a `mouth`
  dial (`{"rest": 0, "aa": 1, "oh": 2}`) and a `mouth` track of `step` keys, one drawing per frame,
  joins the others. A viseme without a drawing takes its nearest one.
- "Make this character say the line" is `lipSync:visemes` on the rig. "Make this photo talk" is not: that
  is a pixel video from the Picsart lip-sync models (`kling-avatar`, `heygen-talking-photo`,
  `minimax-h3-max-lip-sync`, `bytedance-omnihuman-v1.5`), not editable animation.
- A blink is in fast (~0.08 s), held closed (~0.06 s), out slower (~0.12 s), and keeps the face's
  other targets running.
- Talking while smiling = `happy` steady + visemes cycling + a corrective per viseme that dents or
  pinches under the smile (`happyAa`, `happyOh`). Shape each viseme on the mouth as it is seen, the
  held mood applied, then render every viseme at full weight with the mood on: a dent, a flat lip
  or a pinched corner there is a missing corrective. The mouth and eyes sit before the head in
  `items` so they paint on top.
- Draw the mouth with a darker `stroke` over its `fill`, `"lineJoin": "round"`: the lip line reads at every
  opening, and the round join softens the corners. The stroke follows the morphed outline.
- End a grin in the silence: when a smile control opens the mouth (rig-humanoid's `happy` does past
  about 0.6), ease it after the last word over ~0.12 s to where it rests closed. Check that every silent frame reads closed.
- Keep a head turn moderate: talking to camera reads at about half the turn's range, and the full turn
  only where the body itself is turned that far. An ear slides round the head with the turn and never
  fades; hair trails the head by a couple of frames.
- A wave lifts the hand up and forward at shoulder height, clear of the face outline: a forearm bent
  across the cheek reads as a reach. Measure the clearance from geometry on every frame of the gesture.

## 8. Scene-to-scene morph transitions

- Three ways: direct (A's outline becomes B's, every frame honest); fast swap (the outline swaps
  under `motionBlur: true` and a large move or spin, the eye fills in); hybrid (the key object
  morphs directly, the rest leaves under a `mask` or slides out, new details enter last).
- Pick 1–3 key pairs that share two of colour, shape, volume. Morph those first; if they do not
  read, nothing else will.
- Order: key pairs → the largest, least-detailed objects → small details last; the morphing layer
  spans the cut (its `start`/`duration` cover both scenes), it belongs to neither scene.
- Every moving element shares one direction and speed across the cut; colour changes ride on the
  fill's keyframes timed with the outline's.
- Verify with `picsart_scene_contact_sheet` stills at the cut ±2 frames and `picsart_media_track_motion` on the key pair.

## 9. When not to morph

- No two of colour/shape/volume in common → cut, dissolve or a catalog transition.
- Raster media and text are not outlines; a `media` or `text` layer does not morph — bend it over an
  art mesh (§10), or mask, scale or transition it.
- Topology changes (open↔closed, a hole appears, a shape splits) → `step` swap or a dissolve.
- Under ~0.2 s, or more than a few dozen vertices → a swap reads the same and is cheaper to author.

## 10. Bending a picture and live pins

A layer's `mesh` draws a `media`, `text`, composition or `scene_ref` picture over triangles so it
bends: a `grid`, explicit `vertices` + `triangles`, or a mesh that follows a cut-out's transparency
from `picsart_scene_apply_preset` with `preset` `mesh:auto`; then `deformers` (`bend`, `push`, `stretch`, `warp`, `skin`, `pins`)
move its points over time, each fading in and out on its `mix`. `pins` give free handles to a flag,
tail, ear or sticker corner, with `stiffnessRegions` to keep a head firm on a bending body. Read
[references/art-mesh.md](references/art-mesh.md) before writing a mesh, and
[references/live-pins.md](references/live-pins.md) before writing pins.

## 11. Explicit skin weights

When a limb, sleeve or imported mesh should follow painted bone influences instead of the automatic
radius falloff, give the `skin` deformer `weights`, one row per mesh vertex or outline point. Read
[references/skin-weights.md](references/skin-weights.md) before writing them: the rest-pose
alignment, the row numbering, the blend band a bend needs, and the limits.

## Not expressible (format findings, not rules)

- Weight-indexed in-betweens: no target "at weight 0.5"; the mid pose is a second target cross-faded
  by hand (§3).
- Curved vertex trajectories: a vertex keyframe takes no spatial tangents (`inTangent`/`outTangent`
  are honoured on `position`/`anchor` only), so an arc needs a breakdown keyframe.
- A target's `weight.expression` reading another target's weight directly: unverified; the
  corrective pattern goes through parameters.
- No priority/override between procedural targets (VRM `overrideMouth`/`overrideBlink` block/blend):
  conflicts are authored by hand.
- `closed` is static and the hole count fixed: topology never morphs.
- No automatic volume preservation under a squash target.
