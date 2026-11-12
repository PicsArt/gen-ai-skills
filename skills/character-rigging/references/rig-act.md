# Acting a rig: IK, gestures, walk, actions, drivers, ink lines

Part of [the character-rigging recipe](../SKILL.md); one section of it, read on its own.

## Contents
- IK and gesture arms (raise × elbow, the wave rule)
- Motion presets: `walk_cycle`, `ground_scroll`, gestures, `acting`, actions, parameter drivers
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
  (swings or beats). They return every control to rest (`wave` keys the wave rule above; the others lift the arm inside the safe pair, raise 0.25 to 0.36 at an
  elbow of 0.45 to 0.55, so the hand stays off the face). `wave`: the hand swings from the
  wrist `count` times. `talk_beat`: the forearm beats with the speech, the hand follows. `point`: the arm's
  IK takes the wrist to `targetX`, `targetY` (rig px from where it rests, y down, default up and
  forward); the limb straightens toward a target out of reach, and the hand forms a point (`HandPoint`). `shrug`: both arms, the hands turned, the
  head tilts and the breath rises (no `side`, no `count`). Use cases: a greeting, a character talking with
  its hands, indicating an object, an "I don't know". Pitfalls: a gesture replaces a walk's bindings of the
  same arm (the result's notes say so), so apply it after the walk and give it a `start` inside the
  walk; `point` is IK, so a hand at a fixed target stays there while the body moves.
- `acting` (tag `rig-motion`): the character acts from commands. Key the text parameter `<layer id>Action` (the layer's id with any character that is not a letter or digit as `_`, e.g. `kidAction`) on
  the scene holding the rig layer (the preset declares it, default `idle`, when it has none) and the
  rig plays each key's motion from that key: `idle` (weight shifting leg to leg),
  `wave` (the near arm), `point` (the near arm, head and eyes at `pointX`/`pointY`, rig px),
  `talk` (head nods, brow lifts and hand gestures on beats; the mouth is the visemes', keyed apart),
  `walk` (`walk_cycle` from a half step on the key, closing the feet with a step when it stops, so no
  planted foot slides; `stepDuration`, `stride`, `lift`, `armSwing`, `bob`, `lean`, `travel` as
  `walk_cycle`'s). Its text parameter `<layer id>Action` selects a preset command; the `action` field in
  `content.animation` selects a named action from the rig document. Any other text plays `idle`.
  Each switch crossfades over `fade` (0.2 s), longer for a joint with further to go, what was playing carrying on under it, the forearm, hand and head
  trailing by 2 frames or more:
  `{"action": {"type": "text", "animatable": true, "default": {"keyframes": [{"time": 0, "value": "idle"},
  {"time": 2, "value": "wave"}, {"time": 4, "value": "walk"}, {"time": 7, "value": "point"}]}}}`.
  It drives every name its clips key and the walk's, so on one rig it takes the place of
  `walk_cycle`, never beside it; for life add `random_pulse` on `blink` and `cycle` on `breath`,
  which it leaves free. The clips key standard
  names only, so any rig with them acts. Each rig layer reads its own `<layer id>Action`, so two characters in one scene act apart from their own keys.
- Actions (tag `rig-motion`): `jog`, `jump`, `think` and `idle`, each `start`, on every humanoid rig (rig-humanoid,
  rig-humanoid-front, a cut-out of either view). `jog` loops in place: `stepDuration` (0.3 or less) per step, both feet
  off the ground for about 0.4 of it, `lift`, `bob`, `armSwing`, `elbow`, `lean`; `view` `side` (default) swings the feet
  fore and aft over `stride` / 4 (pair it with `ground_scroll`, `pace` `constant`, the same `stride`), `front` for
  rig-humanoid-front or a front cut-out lifts them on the spot. `jump` (`duration` 1.2, `height` up to 60, `tuck`,
  `crouch` 1, `view`): crouch of the hips' full 60 px with the arms back, spring, knees tucked at the top, land, take
  the landing and settle on the rest pose; the rise is the hips' own, so the figure stays in its frame. `think`
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
against them, and the planted foot does not slide. `lift` is the foot's clearance in rig px, not a 0..1 dial: a walk lifts about 24–40, a run up to about 100, and `lift: 1` barely steps. After setting the walk or jog numbers, check one loop with `picsart_scene_check_motion` `value_range` on `<side>FootArt` `centerY` for both feet (the amplitude, in the host's root pixels, is at least 0.8 × `lift` × the rig layer's scale: a rig placed at 0.25 moves a quarter as far), and look at the frames for clearance and for contact alternating. Show a walk, jog or run only in the three-quarter or side view, never the front view: the front view gets the rest or idle pose and face acting.

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
