# Acting a rig: IK, gestures, walk, actions, drivers, ink lines

Part of [the character-rigging recipe](../SKILL.md); one section of it, read on its own.

## Contents
- IK and gesture arms (raise × elbow, the wave rule)
- Motion presets: `walk_cycle`, `ground_scroll`, gestures, `acting`, actions, parameter drivers
- A seated pose on painted furniture
- Ink lines


**IK.** A limb on IK puts its wrist or ankle on the target and bends at the elbow or knee to reach it
(knees fold forward, elbows back); a target out of reach straightens the limb toward it. The swings
still pose the limb under a partial `mix`. The targets are in the rig's own space and stay where they
are while the body moves, so a foot that keeps its target is planted: lower
`hipsRaise` and the knees bend. To touch something, set `<side>HandIk` 1 and bind the absolute, composition-space `<side>HandTarget` parameter; its default follows `<side>HandX/Y` offsets from the resting wrist. The parameter drives the same-named target layer, whose final placement is the arm solve's goal, so an `attach` or `ik` constraint on that layer overrides the input through the same path. Those constraints stay inside the rig's composition; a parent binds inputs through the instance and reads its published sockets, without addressing internal layers.

**Gesture arms: raise × elbow.** Up to a 60° raise (`UpperArmRaise` ≤ 0.375), the natural
elbow bend folds the hand onto the face. Measured safe pair for a talking gesture, a point or a shrug:
`UpperArmRaise` 0.25–0.36 with `LowerArmSwing` 0.45–0.55. Unsafe, hand at the nose or mouth: raise 0.36
with elbow 0.85, raise 0.2 with elbow 0.7. Swing the hand with `HandSwing`, not by bending the elbow
further, and check a `picsart_scene_contact_sheet` for the hand against the head.

**The wave rule** (stated once; the presets, the actions and the robot all follow it). A wave keys one world pose: the arm out and up beside the head, the forearm up (an opening near 0.7). Where that pose runs through the arm's pole (pointing at the camera) on a 2D rig, the preset keys the in-plane dial instead, picking its row by the rig's `viewAngle`, with the forearm's sign following the view's + side: one preset, three rows, no new control. Front (0): `UpperArmOpen` 0.68–0.76 with `LowerArmSwing` −0.2 to −0.35. Three-quarter (45) and side (90): `UpperArmRaise` 0.5–0.6 with `LowerArmSwing` +0.25 to +0.35, the hand standing in front of the head, clear of the face. `HandSwing` swings on every row.

**Review every action before it is shown.** Each action keyed on a rig (a preset below, a gesture, a
pick-up, a sit, a head turn) gets the pose review of [cartoon-film.md](cartoon-film.md) §7: its start,
deepest pose, contact, prop swap and end on one `picsart_scene_contact_sheet`, then a zoomed crop of each
joint the action turns (waist, neck, shoulder, hip, elbow, knee) at its start, end and extremes: no gap,
crack or doubled art at a seam. A pose the rig cannot reach cleanly takes a smaller value (a shallower `crouch`, `bow` or
`height`) or another action, never a workaround.

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
  To walk to a mark, set `distance` (rig px) instead of `steps`: it takes the whole steps nearest at about
  `stride` and adjusts the stride so the walk stops on the mark.
  Before `start` the layer holds the walk's first pose, and with `from` `walking` that is mid-stride (one
  arm forward, one back). A character who stands, then walks, takes `from` `rest` with `steps` or
  `distance`.
  Pitfall: never settle the rig by hand after a `steps` walk (a key on the same parameters is a second
  writer, and pops at the stop); the arms take 0.15 s longer than the feet to come to rest. Use a fresh
  `walk_cycle` for the next walk, `start` after the action. `steps` with `travel` `forward` needs the same
  plain layer as the loop.
- `ground_scroll` (tag `rig-motion`): the set's side of a walk across a scrolling background. Walk the rig
  `in_place`, put the scenery under one parent layer (an empty one is fine), and apply `ground_scroll` to
  that parent with the walk's own `start`, `stepDuration`, `stride`, `steps` and `from`, `direction`
  `right` for the rig as drawn (`left` for a mirrored one) and `walker` the walker's layer id: the ground's
  pace is read from that layer's drawn size (its scale times its fit; `stride` is in rig px), so it cannot be
  mistyped (the one walker in the composition is taken when `walker` is left out; `walkerScale` overrides). The parent moves against the travel on the same clock,
  so the planted foot stays still on the ground; pair it with the camera's `push_in` on a pivot at the
  walker. Pitfall: change a walk's numbers in both presets, or the feet slide.
- Gestures (tag `rig-motion`, `gesture`): `wave`, `talk_beat`, `point` and `shrug`, each `start`,
  `duration` (seconds from the arm leaving rest to its return), `amount` 0..1, and for `wave`, `talk_beat`
  and `point` a `side` (`right` the near arm, `left` the far one); `wave` and `talk_beat` also `count`
  (swings or beats). They return every control to rest (`wave` takes the wrist out beside the head by IK, as `hold_overhead` does; the others lift the arm inside the safe pair, raise 0.25 to 0.36 at an
  elbow of 0.45 to 0.55, so the hand stays off the face). `wave`: the hand swings from the
  wrist `count` times. `talk_beat`: the forearm beats with the speech, the hand follows. `point`: the arm's
  IK takes the wrist to `aimAt` (the id of a layer of the scene: the kite, a bird; the hand goes to where its anchor is on screen at every frame and follows it, however the rig is scaled or travelling) or to `targetX`, `targetY` (rig px from where it rests, y down, default up and
  forward; any target in frame, up to the top of the composition, is accepted, so the sky is a large negative `targetY` and
  the arm keeps its direction); the limb straightens toward a target out of reach, and the hand forms a point (`HandPoint`). A side or three-quarter
  cut-out rig aimed more than 15° above its shoulder and past the arm's reach rolls the shoulder forward and stretches the arm (up to 1.9×, full at 50°; the hand sweeps an arc about the shoulder and comes home over the last half of `duration`, so the stretched arm shortens gradually and never folds to a stub),
  so the hand lands clearly beyond the muzzle (the mitt does not touch the nose), and while the hand is a point (`HandPoint` from 0.5) the head draws over the arm, so a straight
  arm passes behind the face and only the hand shows past the muzzle; a reachable target keeps both bones whole. The stretch is part of the rig's expressions: rebuild a
  rig made before it from its part sheet to get it. On `point`, `amount`
  scales the reach (0.6 to 1.4 of the target, 1 at the default 0.5), the body's lean and an overshoot as the hand
  arrives together. Three levels for "show the viewer where to look": **subtle** `amount` 0.2, a short `duration`;
  **clear** `amount` 0.5 with a `headTurn` toward the target at the same `start` and a 0.6 s hold (`duration` about
  1.6 s); **big** `amount` 1 with an anticipation dip (`hipsRaise` −2 and `spineLean` −0.5 over the 0.25 s before `start`, back to 0 at `start`) and a `push_in`
  on the target. `shrug`: both arms, the hands turned, the
  head tilts and the breath rises (no `side`, no `count`). Use cases: a greeting, a character talking with
  its hands, indicating an object, an "I don't know". Pitfalls: a gesture replaces a walk's bindings of the
  same arm (the result's notes say so), so apply it after the walk and give it a `start` inside the
  walk; `point` is IK, so a hand at a fixed target stays there while the body moves.
- `acting` (tag `rig-motion`): the character acts from commands. Key the text parameter `<layer id>Action` (the layer's id with any character that is not a letter or digit as `_`, e.g. `kidAction`) on
  the scene holding the rig layer (the preset declares it, default `idle`, when it has none) and the
  rig plays each key's motion from that key: `idle` (weight shifting leg to leg),
  `wave` (the near arm), `point` (the near arm, head and eyes at `pointX`/`pointY`, rig px; a front arm opens at most 130° from hanging, so a target
  above that, however far or high, is pointed at along that limit, the arm lifted beside the head and brought back down outside it),
  `talk` (head nods, brow lifts and hand gestures on beats; the mouth is the visemes', keyed apart),
  `walk` (`walk_cycle` from a half step on the key, closing the feet with a step when it stops, so no
  planted foot slides; `stepDuration`, `stride`, `lift`, `armSwing`, `bob`, `lean`, `travel` as
  `walk_cycle`'s), `hold` (still, no weight shift), `lean` (forward from the hips), `nod`, `lookUp`,
  `sit` (the pelvis onto a seat `seatHeight` rig px above the floor line: 0 the floor, about 150 a stool; it stands up on any standing key), `seated` (the same seat held from its key with no sit-down: key `seated` first, at time 0, for a character already seated when the shot opens; to sit down mid-shot use `sit`: a `seated` after another action puts the feet and pelvis on the seat in one frame, and the validator warns) and `fall` (a pratfall that ends seated and dazed). All three work on every view of `rig-humanoid` and `rig-humanoid-front`; use `sit` for a calm seat or a stool and `fall` for a comic slip. The seat's height is also the number parameter `<layer id>SeatHeight` declared beside `<layer id>Action` (`kid` is `kidSeatHeight`; default `seatHeight`, `max` the legs' reach, 0.85 of the leg, rig px above the sole line): key it to change the seat; a height above the reach is refused. The hands stay in front of the body: key your own arms under a sit or a seated with `UpperArmSwing` >= 0 on the front rig. Its text parameter `<layer id>Action` selects a preset command; the `action` field in
  `content.animation` selects a named action from the rig document. Any other text plays `idle`.
  Each switch crossfades over `fade` (0.2 s), longer for a joint with further to go, what was playing carrying on under it, the forearm, hand and head
  trailing by 2 frames or more:
  `{"action": {"type": "text", "animatable": true, "default": {"keyframes": [{"time": 0, "value": "idle"},
  {"time": 2, "value": "wave"}, {"time": 4, "value": "walk"}, {"time": 7, "value": "point"}]}}}`.
  It drives every name its clips key and the walk's, so on one rig it takes the place of
  `walk_cycle`, never beside it; for life add `random_pulse` on `blink` and `cycle` on `breath`,
  which it leaves free. The clips key standard
  names only, so any rig with them acts. Each rig layer reads its own `<layer id>Action`, so two characters in one scene act apart from their own keys.
- Actions (tag `rig-motion`): `jog`, `run`, `jump`, `think` and `idle`, each `start`, on every humanoid rig (rig-humanoid,
  rig-humanoid-front, a cut-out of either view). `jog` (0.26 s a step) and `run` (0.2 s, a sprint 0.16) read as running, not as
  a fast walk: a flight every step (both feet off the ground for 55% / 65% of it), the heel kicked back and up (`kick`) with the knee
  driven through under the body, the hips lowest at the footfall and highest in the flight (`bob`), the arms pumped
  against the legs at the elbow's right angle (`elbow`, `armSwing`) and the torso leaning from the hips (`lean`, 1 is 20°).
  Take `run` for a chase and `jog` for an easy pace; do not turn a `walk_cycle` up for either. Keep the default `lift` (a long
  skirt rides with the raised knee, so a high lift needs no care); a low `lift` (20) keeps the lean and the arms but loses the
  kick, and reads as a brisk walk. Both carry the layer on, `travel` `forward` (the default): a `stride` a step at a constant speed from `start` (stopping after `steps` when it is set), as `walk_cycle` does, so one `run` crosses the ground without a position track; `travel` `in_place` runs on the spot, for `ground_scroll`. Keys you set by hand before `start`, or after the end of a `steps` run, stay. Mirror the layer to run left. A run fills its beat and covers ground: set `steps` to the beat's seconds divided by `stepDuration` so the legs do not stop early (a 12 s run at 0.27 s a step is 44 steps, not 10), and keep the scenery still, with the camera holding or panning with the runner, so the distance crossed reads against it; the distance is `steps` × `stride` × the layer's scale, so plan it to end with the character inside the frame, whole: start further left, run fewer steps, or let the camera follow the runner with the scenery in parallax, and check the last frame of the run. Both loop: `stepDuration` (0.3 or less) per step, `lift`, `kick`, `bob`, `armSwing`,
  `elbow`, `lean`; `view` `side` (default) swings the feet
  fore and aft over a third of `stride` (pair it with `ground_scroll`, `pace` `constant`, the same `stride`), `front` for
  rig-humanoid-front or a front cut-out lifts them on the spot. `jump` (`duration` 1.2, `height` 140 host px by default (a hop of 60 reads as a bounce), `tuck`,
  `crouch` 1, `view`): crouch of the hips' full 60 px with the arms back, spring, knees tucked at the top, land, take
  the landing and settle on the rest pose; the rise is the hips' own, so the figure stays in its frame. **To stand on a prop,
  name it: `onto: "<layer id>"`** puts both feet on the middle of that layer's top edge, read from the layout at the
  landing (any anchor, scale or drawing; a stool, a box, a table; the pair may sit in a pre-comp or group that is scaled, offset, turned, retimed or fitted into bounds: the landing is read through it), and `landX`/`landY` then move the landing from there. List the
  character after the prop in `layers` so he is drawn in front of it, and hop off with a second hop (`landY` the seat's height).
  Check that no foot floats with `picsart_scene_check_motion` `foot_support`. `think`
  (`duration` 3, `side`): the arm's IK reaches toward the rig's chin and holds through the middle 40%, the other arm
  hangs; it keys `<side>HandIk` and `<side>HandToChin` (0..1, default 0), which blends the `<side>HandTarget` layer toward
  an `attach` target on the head (the chin plus the rig's wrist-contact offset, carried through the head's placement and
  deformers), so contact geometry stays inside the rig. `idle` (`period` 3, `amount`): breath, head sway a quarter
  period behind it, a weight shift and one blink a period, looping seamlessly, the arms left at the sides.
  Each rig also declares `<side>AnchorShoulder` and `<side>AnchorEye` (vec2, absolute rig px): the shoulder a `point`
  aims from and the eye its head follows; a rig missing one is refused (`rig_parameters_missing`). Every humanoid rig
  declares read-only `viewAngle` (degrees from facing the camera: front 0, three-quarter 45, side 90), read into a
  preset's scope beside the anchors; a rig that declares none is not assumed to be a side view, and `point` is refused
  by the name. The anchors and the angle are the rig's own geometry: a `scene_ref` binding one is refused by name. An
  arm opened toward the lens has no direction on a side or three-quarter view, so its drawn length fades to nothing
  there and the forearm takes its direction from the arm's 3D pose; no joint jumps.
- Everything else is a parameter driver with `parameter` naming the rig's control — the "Parameter
  drivers" table in [references/character-motion.md](character-motion.md):
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
against them, and the planted foot does not slide. `lift` is the foot's clearance in rig px, not a 0..1 dial: a walk lifts about 24–40, a run up to about 100, and `lift: 1` barely steps. A run is not a quicker walk: a flight (both feet off the ground every step), a forward lean, a heel kicked back (`kick`) and arms pumped at a right angle make it read as one, so use the `run` or `jog` preset, not `walk_cycle` with a shorter `stepDuration`. After setting the walk or jog numbers, check one loop with `picsart_scene_check_motion` `value_range` on `<side>FootArt` `centerY` for both feet (the amplitude, in the host's root pixels, is at least 0.8 × `lift` × the rig layer's scale: a rig placed at 0.25 moves a quarter as far), and look at the frames for clearance and for contact alternating. Show a walk, jog or run only in the three-quarter or side view, never the front view: the front view gets the rest or idle pose and face acting.

## A seated pose on painted furniture

Place the rig with `on_floor`, passing the seat's pelvis x and feet row as `at` and the character's `size` (such as 0.6 for a child). `sit_on` keeps this size. For a character already seated at the first frame, apply `acting` with `travel: "in_place"`. Apply `sit_on` with the seat id in `seat` and omit `start`. It holds the `seated` pose. To show the sit-down, give `sit_on` a positive `start` on a seat with standing room.

For planted feet, use a side rig facing the way the seat faces. For this `on_floor` placement, pass the seat's `feet` point as `at` and the character's `size`. Apply `acting` with `travel: "in_place"` and `sitFeet: "planted"`. Then apply `sit_on`. The hips move back while the feet stay put. Key a standing action to rise again.

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
