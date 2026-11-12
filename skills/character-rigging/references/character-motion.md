# Character motion: rigs, constraints, cycles and drivers

Part of the `character-rigging` skill. Read it before building a character by hand, posing limbs with `ik`, looping a cycle, or adding a parameter driver or follow-through.

## Contents

- Character motion: rigs, constraints, cycles
- Parameter drivers
- Secondary motion: a parameter that follows
- Held drawings: animating on twos

## Character motion: rigs, constraints, cycles

A character moves from few keys: limbs are drawn shapes bent at their joints, a limb's tip follows a
target layer, and one keyed cycle loops for the whole shot. This is the by-hand build, for a character
the catalog rig `rig-humanoid` does not fit; when it fits, pose the rig instead
([SKILL.md](../SKILL.md) §0).

**A limb is one drawn shape bent by a `bend`** (`deformers` on the shape content: `bend`, `push`,
`stretch`; see "Bending or denting an outline" in `references/outline-mechanics.md`). A joint dial is the bend's
`angle`: keyed, or keyed `by` a parameter. An ink-line limb is a stroke with a `taper`, thin at both
ends and full in the middle ([rig-act.md](rig-act.md), "Ink lines").

**A torso and neck are one drawing `skin`ned to bone layers** (`spine`, `neck`): the bones are
empty layers in the chain, keyed or driven by `spineLean` and `headNod`, the arms and head parented
to them; the drawing follows. A bone's `radius` reaches across what it carries (the spine's the whole
torso, the neck's only the neck), so a nod leaves the shoulders the arms hang from. A joint's limit
is its bone's `rotation` `min`/`max`. Keep skin to wide, gentle joints: a skinned hinge folds once
each limb's half-length is at most the limb's half-width × tan(angle / 2), so an elbow or knee stays a
`bend`.

**`ik` poses a limb from a target.** A layer's `constraints` list:

```json
"constraints": [{"type": "ik", "joint": "knee", "end": [0, 176], "pole": [1, 0], "soft": 0, "mix": 1,
                 "target": {"layer": "footF", "position": [0, -28]}}]
```

- `joint` — the `id` of the layer's `bend` that is the joint. The layer's rotation (the upper bone,
  about its pivot) and that bend's `angle` are solved so `end` lands on the target; out of reach the
  limb straightens toward it.
- `end` — the limb's tip at rest, content px.
- `pole` — the side the joint folds to (a knee's front), content px, `[x, y]`; never along the line
  from the joint's `from` to `end`. Default: the side a positive `angle` folds to. A mirrored rig
  mirrors the pose. It is a side of the limb as DRAWN AT REST and turns with the limb, never a
  screen direction: on a character facing +x with limbs drawn hanging down (`[0, 0]` to `[0, 176]`),
  a knee is `[1, 0]` (forward) and an elbow `[-1, 0]` (back). Raised forward-up to wave, that arm keeps
  `[-1, 0]` and its elbow points down, below the line from shoulder to hand; `[1, 0]` points it up.
- `target.layer` — a layer of the same composition; `target.position` — the point in that layer's
  own space (default its pivot).
- `mix` 0..1 (default 1), a number or a number track (keys, or keyed `by` a parameter), is the only
  on/off: it moves the rotation and joint angle that far from what they are before the entry to the
  solve. `soft` (px, ≥ 0, default 0) eases the limb straight short of full reach.
- Entries apply in list order over the layer's keyframes and its authored expression; at `mix` 1
  the solve owns the limb's rotation and joint angle.

Refusals: `ik_unknown_joint` (no bend with that id), `ik_pole_has_no_side`, `ik_unknown_target` (not
in this composition), `ik_target_cycle` (the target is the limb or one of its children),
`ik_mix_out_of_range`, `ik_soft_out_of_range`, `ik_reserved_field` (`upper`/`lower`),
`deformer_id_duplicate`, and `ik_unsupported` for: two joints on one layer, a look on the limb,
another deformer of the limb animating, depth (`z`, `rotationX`, `rotationY`) on the limb or on a
parent of it or of the target below the layer they share, roots that differ in `cameraExempt`, a
`pole` with depth.

**A joint limit is the bone's track `min`/`max`.** A layer's number track (`rotation`, `z`,
`rotationX`, `rotationY`, `opacity`, `volume`) takes `min` and/or `max` in its own units; every frame
its value is held inside them, whatever drives it: keys, `by`, an expression, a constraint. On
`rotation` the angle is first taken as the same turn in (-180, 180] (an expression giving 300 is -60),
and a child layer follows the held pose. A vector track refuses them
(`animation_limit_unsupported_property`), as does `min` above `max` (`animation_limit_inverted`).
A track may be only the limit: `"rotation": {"min": -150, "max": 0}` holds the static
`transform.rotation`, or the rotation an ik writes on its bone, without dummy keys.
With `transforms[]` moving the same channel the limit holds what the channel composes to, the layer's
value plus every component's, and takes the excess off the layer's own value; the components play as
authored. Everything outside the layer (children, another layer's `getPlacement()`, a constraint
targeting it, a query) reads the layer as drawn; its own expressions read its track held by its own
limit alone. The values add about one axis only, so a limit is refused (`animation_limit_axes_differ`)
when a turn about another axis lies between them: an element before the last one moving the channel
turns about another axis (a `z` only by a tilt), that last one turns inside the channel's axis (x, then
y, then z, outermost first), or the layer turns outside it.

```json
"animations": {"rotation": {"by": "leftLowerArmSwing", "min": -150, "max": 0,
  "keyframes": [{"at": 0, "value": 0, "easing": "linear"}, {"at": 1, "value": -150}]}}
```

**A hand-built arm as one shape.** The catalog rigs already build each limb as one outline bent at its joint. For an arm built by hand
outside them: one outline shape, one `skin` with a bone per segment.

- Leave the upper bone's `end` unset, so it ends at the forearm's pivot; an offset `end` tears the outline. The last bone writes its
  `end`. Give every bone a positive `radius`, about the limb's width (`skin_bone_radius_out_of_range` otherwise).
- Fold creases are interior lines inside the same shape, each a `morph` target keyed by the elbow dial, for example
  `"weight": { "expression": "return picsart.ease(ctx.composition:getParameters():elbow(), 0.3, 1, 0, 1)" }`.
  A crease grows by its offsets, not by `opacity`.
- The hand is its own rigid layer, listed before the sleeve layer so the cuff covers the wrist (layers: later on top; shape `items`:
  first on top; see [cut-out-puppet.md](cut-out-puppet.md) "Draw order" for where a depth-ordering `z` goes).
- Optional: a round outer heel is a `heel` morph target on the outer corner; a painted fold is two sleeve drawings (hanging, folded)
  aligned vertex to vertex and applied as a `fold` morph target. Both are author-named targets, not format features.

**The walk: animate foot TARGETS, not angles.** Proven natively: a whole looping walk shot in 67
timed keys, feet slipping ≤ 0.81 px.

- Each leg's ik target is a small target layer keyed through ONE stride (contact, plant, passing,
  next contact) and looped with `ctx:loopOut`: `"offset"` when the character travels (each stride
  lands one stride further on), `"cycle"` in place.
- The shoe is a CHILD of its target (`parentId`), so it stays planted while the leg reaches for it.
- The body travels by two keys one stride apart, looped `"offset"`; the hip bob is a few keys per
  half stride, looped `"cycle"`.
- The far leg is the same stride started half a cycle in, so it loops from frame 0: the keys after
  mid-cycle move back half a cycle, the ones before it forward half a cycle (`offset`: their values
  one stride further on). Delaying its keys instead holds it on its first key, which breaks an
  in-place loop.
- Arms swing on their elbow bends keyed `by` a parameter, or follow through on a parameter with
  `follow_through` ([Secondary motion](#secondary-motion-a-parameter-that-follows)).
- Hold on twos: put the character in a nested `composition` layer whose composition has `fps: 12`
  ([Held drawings](#held-drawings-animating-on-twos)).
- Retime it with that layer's content `speed`, not by re-keying: `1.3` is 30% faster, and an inner
  cycle of c seconds repeats every c / 1.3 host seconds. The composition plays `duration × speed`
  inner seconds, then holds its last frame, so give it a `composition` block (`width`, `height` and a
  `duration` of at least the host window × speed). Measured on an ik walk at 1.3: frame-identical to
  the walk at 1.3× time, and frozen from 4 / 1.3 s on without the longer `duration`.

```json
{"id": "walker", "content": {"kind": "composition", "speed": 1.3,
  "composition": {"width": 1080, "height": 1080, "duration": 5.2},
  "layers": ["... the character's layers, keyed at their own pace ..."]}}
```

One leg, its target and shoe: the `layers` of the character composition.

```json
{"layers": [
{"id": "hips", "content": {"kind": "empty"}, "transform": {"position": [100, 1430]},
 "animations": {"position": {"keyframes": [{"time": 0, "value": [100, 1430], "easing": "linear"},
                                           {"time": 1.333333, "value": [339.2, 1430]}],
                             "expression": "return ctx:loopOut('offset')"}}},
{"id": "torso", "parentId": "hips", "content": {"kind": "empty"}, "transform": {"position": [0, -192]},
 "animations": {"position": {"keyframes": [{"time": 0, "value": [0, -186], "easing": "ease_in_out"},
                                           {"time": 0.333333, "value": [0, -198], "easing": "ease_in_out"},
                                           {"time": 0.666667, "value": [0, -186]}],
                             "expression": "return ctx:loopOut('cycle')"}}},
{"id": "legF", "parentId": "torso", "transform": {"position": [0, 0]},
 "content": {"kind": "shape",
   "items": [{"type": "path", "closed": false, "vertices": [{"point": [0, 0]}, {"point": [0, 88]}, {"point": [0, 176]}]},
             {"type": "stroke", "color": "#2B2B2B", "width": 34}],
   "deformers": [{"id": "knee", "type": "bend", "from": [0, 68], "to": [0, 108], "angle": 0}]},
 "constraints": [{"type": "ik", "joint": "knee", "end": [0, 176], "pole": [1, 0],
                  "target": {"layer": "footF", "position": [0, -28]}}]},
{"id": "footF", "content": {"kind": "empty"}, "transform": {"position": [166, 1393]},
 "animations": {"position": {"keyframes": [
   {"time": 0, "value": [166, 1393], "easing": "ease_out"},
   {"time": 0.166667, "value": [172, 1430], "easing": "linear"},
   {"time": 0.666667, "value": [172, 1430], "easing": "ease_out"},
   {"time": 1.083333, "value": [290, 1375], "inTangent": [-30, 7], "outTangent": [30, -7], "easing": "ease_out"},
   {"time": 1.333333, "value": [405.2, 1393]}],
   "expression": "return ctx:loopOut('offset')"}}},
{"id": "shoeF", "parentId": "footF", "transform": {"position": [0, 0]},
 "content": {"kind": "shape", "items": [{"type": "rect", "size": [90, 30]}, {"type": "fill", "color": "#C0392B"}]}}
]}
```

The target's stride (405.2 − 166) equals the body's (339.2 − 100), so a planted foot never slides. The
foot stays within the leg's reach of the hip all cycle, swing included: it lands 42 px ahead of the
hip and lifts 48 px behind it, at most about 171 px from the hip on a 176 px leg. Lift it while the hip
is still near; a target out of reach straightens the leg short of it and leaves the shoe detached.

**A wave** is a parameter: the arm's ik target reads it, and hair or an antenna follows it
(`follow_through` follows parameters, never a layer's motion):

```json
picsart_scene_apply_preset { "scene": ..., "preset": "motionPreset:cycle", "parameter": "wave", "params": { "waveform": "sine", "period": 0.6 } }
{"id": "handTarget", "content": {"kind": "empty"}, "transform": {"position": [625, 270]}, "animations": {"position": {"expression": "local w = ctx.composition:getParameters():wave() return value + Vec.v2(70 * w, 12 * math.sin(math.pi * w))"}}}
picsart_scene_apply_preset { "scene": ..., "preset": "motionPreset:follow_through", "parameter": "hairSwing", "params": { "follow": [{"parameter": "wave", "weight": 1}] } }
```

The hair's rotation then reads `hairSwing()` ([Secondary motion](#secondary-motion-a-parameter-that-follows)).

**A jump**: anticipation squash on the body with the `squash` motion preset (`beats`, `pivot` at the
feet), then the hips and the foot targets keyed along arcs (`inTangent`/`outTangent`).

## Parameter drivers

Four presets write a number parameter's `default`, applied the same way (`"parameter": "<name>"`);
the layers read the parameter, so one value drives every part that shares it.

On a cartoon rig (a `scene_ref` layer drawing `scene://rig-humanoid` or `rig-face`), pass the rig
layer as `layerId` and its control as `parameter` (`random_pulse` on `blink`, `cycle` on `breath`):
the track is bound on that layer, so each instance moves on its own. The rigs and `walk_cycle` are in
[SKILL.md](../SKILL.md) §0.

| Preset | The value | Typical uses |
|---|---|---|
| `follow_through` | the swing of a damped spring trailing other parameters | hair, ears, tails, antennae, a dangling sign |
| `random_pulse` | brief eased events at seeded random intervals (`minInterval`, `intervalSpread`, `attack`/`hold`/`release`, `burstChance`) | blinks (`eyeOpen` from 1 to 0), lamp flicker, twinkling stars, glitch hits |
| `random_hold` | a seeded random value held, then a quick eased jump (`transition`) to the next, `minInterval` + `intervalSpread` apart; one `seed` shares the jump times, `channel` picks the value stream, `half` keeps its `positive` or `negative` side, `centerBias` gathers values mid-range | eyes looking around (`lookLeft`/`lookRight`/`lookUp`/`lookDown`), random pose or colour picks, a jittering needle |
| `cycle` | a repeating `sine`/`triangle`/`saw`/`square` wave every `period` seconds | breathing (`breath`, sine ~3.5 s), bobbing, a pulsing glow, UI pulses, beacons |

Drive eyelids or the eyes' y-scale from `eyeOpen`; drive chest or shoulder scale and a small head
bob from `breath`. A different `seed` per character keeps two characters from blinking together.

Eyes that look around: give each eye a `composition` layer holding its white and its pupil. Mask the
pupil with a clip that repeats the white's own `transform` and shape: a clip keeps its own transform,
so inside the eye it lands exactly on the white and the pupil never leaves it. A clip on the eye layer
itself does not sit on the white, and the eye draws nothing. The gaze is four one-sided 0..1 parameters,
the standard expression names `lookLeft`, `lookRight`, `lookUp`, `lookDown`. The pupil's position reads
them, `value + Vec.v2((p:lookRight() - p:lookLeft()) * r, (p:lookDown() - p:lookUp()) * r)` with
`p = ctx.composition:getParameters()` and `r` the room the white leaves. Apply `random_hold` to all four
with one `seed` and `centerBias` about 0.5: `lookRight` channel 0 `half: "positive"`, `lookLeft`
channel 0 `half: "negative"`, `lookUp` channel 1 `positive`, `lookDown` channel 1 `negative`. The eye
never looks left and right at once, and both axes jump at the same moments, as a glance does.

## Secondary motion: a parameter that follows

Hair, ears, a tail or an antenna that lag a turning head, swing past it and settle are one number
parameter following others through a damped spring. Apply `follow_through` to the PARAMETER, never
write the spring yourself:

```json
picsart_scene_apply_preset { "scene": ..., "preset": "motionPreset:follow_through", "parameter": "hairSwing",
  "params": { "follow": [{"parameter": "headTurn", "weight": 1}], "frequency": 1.8, "damping": 0.25 } }
```

It writes `hairSwing`'s `default` as one `picsart.follow(...)` call (declaring it `animatable`, keeping its
`min`/`max`; an output not declared yet is declared for you, so declare nothing in advance), on the
document's own parameters, or with `layerId` on the scene a `scene_ref` layer draws. Its value is the
SWING, in the drivers' units: 0 while they hold still, against their move while it trails (a turn
toward +1 swings it negative), past 0 on the overshoot. Scale it as the driver is scaled: a head
rotated `headTurn() * 20` degrees carries a hair shape, parented to it, rotated
`ctx.composition:getParameters():hairSwing() * 20`; a morph weight reads it directly.

- **The driver** is the motion the part reacts to: the head's turn, not the hair's rest pose. Make
  it a number parameter and drive the head from it too, so the two never disagree.
- **Weights** mix several drivers (`headTurn` 1, `spineLean` 0.5); the swing follows their weighted
  sum. `amount` scales the swing (negative flips it).
- **`frequency` and `damping`** set the feel: heavy hair ~1–1.5 Hz, ears and antennae 2–4 Hz;
  `damping` 0.2 rings, 0.4 overshoots once, 1 settles without overshoot.
- **`segments`** (any count, 1 or more) writes one value per piece: `hairSwing`, then `hairSwing2`,
  `hairSwing3` and so on, each piece's swing relative to the piece before it, so a chain of parented shapes reads one value per joint and ripples tip-last.
- Editing the driver's keyframes updates the swing everywhere; re-apply only to change the feel.
- **No motion read across a hold.** A `step`-keyed driver jumps, and `<name>Velocity()` /
  `<name>Direction()` (of the driver, or of the swing that follows it) fail at a jump. The preset
  reads values only; keep your own expressions on such parameters to values too.

A parameter that follows itself around a loop (`a` follows `b`, `b` follows `a`) is refused as
`parameter_read_loop`.

**Time since a key.** `ctx.composition:getParameters():<name>Since([t])` is the seconds from the
parameter's last key at or before `t` to `t`, on its instance's clock: every key restarts it, a key
repeating the value before it too, and before the first key -- or with none, as for a constant or an
expression alone -- it counts from the instance start. It
reads any type, so a text action parameter (`kidAction`) whose keys are commands (`idle`, `wave`, `wave`) clocks
each one: a clip plays its own local time as `p:kidActionSince()`, and the clip leaving in a
crossfade reads the action before the last key as `p:kidAction(time - p:kidActionSince() - 1/120)`
(`p = ctx.composition:getParameters()`). A parameter that is not `animatable` never carries keys, so
`<name>Since` on it is refused as `parameter_since_not_animatable`. On a cartoon rig the `acting`
preset is built this way: key the layer's `<layer id>Action` and the rig plays the clips
([SKILL.md](../SKILL.md) §0).

**A binding reads its host.** An expression bound at a `scene_ref` (`content.parameters.<name>`) is
written on that layer, so it runs in the host's scope and on the host layer's clock, its keys and
its `by` too: `ctx.composition:getParameters()` there is the HOST's parameters (suffixes too), never
the template's, and `value` is the template's default under it. A binding without an expression
stays on the template's clock and parameters. To drive a template's `x` from the
host's `hostX`, bind `{"x": {"expression": "return ctx.composition:getParameters():hostX()"}}` with
`hostX` declared on the host; a name the host does not declare is `parameter_read_unknown`.

## Held drawings: animating on twos

A nested composition (an inline `composition` or a `scene_ref` body) whose `composition.fps` is
LOWER than its host's rate draws on its own frame grid: every host frame shows the start of the
nested frame it falls in. `"fps": 12` inside a 24 fps scene is animation on twos, the stepped look of
hand-drawn animation, without duplicating a keyframe. The hold covers the whole composition:
keyframes, expressions (their `time` is the held one, so a wobble boils on twos), media, Lottie and
nested playback, which of its layers are live and reads between its own layers. A held frame keeps
the motion blur of its own instant. An effect's rolling seed follows the host clock (the grain is the
film, not the drawing), and sound is not held: audio inside plays on the host clock.

```json
{"id": "character", "content": {"kind": "composition",
  "composition": {"width": 1080, "height": 1080, "fps": 12},
  "layers": [{"id": "ball", "content": {"kind": "shape", "items": ["..."]},
    "animations": {"position": {"keyframes": [{"time": 0, "value": [100, 500]}, {"time": 1, "value": [900, 500]}]}}}]}}
```

An equal or higher rate, or none, holds nothing. A rate that does not divide the host's holds
unevenly (24 in 30 is a pulldown), so pick a divisor of the output rate. Put whatever must stay
smooth, such as a camera move, outside the held composition. Measure the result per frame: the ink
centroid moves only on the nested frames.
