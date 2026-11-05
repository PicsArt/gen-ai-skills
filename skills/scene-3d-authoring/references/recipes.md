# 3D recipes

## A build sequence

Parts arriving one by one into a finished model, then a showcase turn.

1. **Model the result first.** Place every part at its final pose — the layer `transform` is
   the finished model. Validate; render a still at the end time. Nothing moves yet.
2. **Order by support.** A part arrives only once what holds it has landed, big before small;
   each one settles before the next touches it.
3. **Put the beat on a grid.** One part per beat (e.g. 0.27 s at 112 BPM, a beat per part,
   two per new section). Each part's `start` is its beat; nothing of it is on screen before then.
4. **Choose an entrance by role.** Bulky bricks `drop_in`; parts that come from the side
   `fly_in_arc` with `direction` toward their slot; small parts that must seat precisely
   `snap_settle` with `direction` down. Keep `duration` under two beats.
5. **Sub-assemblies are groups.** Build them on their own beats beside the model, then fly the
   group in (`fly_in_arc` on the group layer) as one beat of its own.
6. **Camera in shots.** `push_in` through the first section, `crane` up for the reveal, then
   one `orbit` of 60–90° (or a `whip_pan` out) last. Keyframed moves chain; plan them as one
   timeline and apply them in time order, the orbit or whip pan after them.
7. **Finish with a turn.** Put the finished model in a group and `turntable` the group, or
   `orbit` the camera a full turn — the turn reads the silhouette the build created.
8. **Accent the beat.** A model parameter (studs glow) keyed on each landing, and a squash
   (built into the entrances) sell the contact more than any extra motion.

Check before the final render: no part passes through another on its way in. Render a check view
of each entrance and test the moving part's box against the parts already placed.

## Builds itself, then comes alive

Any object that assembles and then moves on its own: a toy, a robot, a product that unfolds —
say a brick car that snaps together, switches its lamps on, drives off and parks for a hero shot.

1. **The build is staged assembly.** Few parts: one layer each, with the snap presets of *a build
   sequence* above. Many parts of one model: one `build` parameter, 0 the bare base and 1 the
   finished object, binding every part through its own window. Each part's
   `.scale.x/.y/.z[a:0, a+0.0001:1]` keeps it hidden until `a`, and its
   `.position.y[a:<rest + drop>, …, b:<rest>]` brings it down into its slot by `b`; a squash is a few
   more `.scale.y` points after `b`. A `visible` bind takes a boolean, so it cannot open a window —
   the scale does. The values replace the node's own, so every `out` is the part's absolute local
   coordinate. Key `build` 0 → 1 on the layer and the length of that key is the build's speed.
2. **The camera follows the build.** Write it from the object's parameters, not from clock times: an
   `eye` expression reading `ctx.composition:getLayer('car'):getParameters():build()` circles in as the
   build rises, so a template that changes the build's length keeps the shot.
3. **The hand-off is through model parameters.** Once built, the object's own knobs bring it to life:
   lamps on (a `materials` `emissive` track), a hop, the front wheels wiggling (`steer`). Then the
   motion that carries it reads the same knobs. The car keys `drive` (metres) and `steer`; its wheels
   roll from `drive` inside the model, and a carrier group rides the path a bicycle would, heading
   turning by `ds · tan(wheel angle) / wheelbase`, the wheel angle being what `steer` binds (`-30 · steer`°), so where it goes and how its wheels turn are one fact:

   ```lua
   local p = ctx.composition:getLayer('car'):getParameters()
   -- step from the drive's start to `time`: ds = p:drive(t1) - p:drive(t0), steer at the step's middle
   local dth = ds * math.tan(math.rad(-30 * p:steer(tm))) / 0.32
   x = x + ds * math.cos(th + dth / 2); z = z - ds * math.sin(th + dth / 2); th = th + dth
   ```

   The car layer's `parentId` is that carrier, so its own `animations` stay free for the chassis'
   `drop_in`.
4. **Text goes over it in 2D.** A title is a 2D scene playing the 3D one through a `scene_ref` whose
   `parameters` pass the caller's values on, with the text layer beside it.

## Lights pulsing on the beat behind a group

Two or three point lights just behind the singers, close to what stands behind them (a fence,
bunting), each flashing on the beat and stepping through a palette one colour per beat, out of phase
with each other. The pool lands behind the group and leaves the frame's edges alone, where a pulse on
`key` flashes the whole frame. At 120 BPM:

```json
{ "id": "glow_mid", "transform": { "position": [0, 1.6, -5.6] },
  "content": { "kind": "light", "type": "point", "range": 2.5,
    "intensity": { "expression": "return picsart.cycle(time, \"saw\", 30, 1, 0.5, 0)" },
    "color": { "expression": "local p = {Color.rgb(1,0.31,0.63), Color.rgb(0.25,0.78,1), Color.rgb(1,0.82,0.25), Color.rgb(0.62,0.42,1)}; return p[(math.floor(time/0.5+1e-6)+1)%4+1]" } } }
```

The saw flashes to 30 on each beat and falls to 1; `+1` is this light's phase in the palette (0, 1, 2
for three lights). For another tempo replace both `0.5`s with `60 / BPM`. `range` keeps each pool off
the edges; a light's `intensity` falls with the square of the distance, so one 0.7 m from the fence
needs some 30.

## The whole scene pulsing on the beat

`key`, `fill` and `rim` are directional: each lights the whole scene, so a pulse on one flashes
everything it faces. For a glow that pools behind a group, use point lights (above). A colour
expression returns `Color.rgb(r, g, b)` (0..1), never a hex string: `picsart_scene_validate` refuses a
literal one or a table of them, and a string the expression builds still fails the render. On a
0.5 s beat, measured, brightness follows the beat at r = 0.993:

```json
"key": { "intensity": { "expression": "return picsart.cycle(time, \"saw\", 3.0, 0.4, 0.5, 0)" },
         "color": { "expression": "local p = {Color.rgb(1,0.31,0.63), Color.rgb(0.25,0.78,1), Color.rgb(1,0.82,0.25), Color.rgb(0.49,0.88,0.42)}; return p[math.floor(time/0.5+1e-6)%4+1]" } }
```

The saw flashes to 3.0 on each beat and falls to 0.4; the colour steps through the palette, one per
beat. For another tempo replace both `0.5`s with `60 / BPM`.
