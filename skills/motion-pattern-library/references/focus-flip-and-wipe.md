# Focus, flip, and wipe details

## Focus pull and card flip

A focus pull is an effect and a flip is a turn in depth (`rotationY` under the composition camera), so
both compose with motion instead of competing:

```json
{ "scene": …, "layerId": "hero", "preset": "motionPreset:blur_in",  "params": { "duration": 0.6, "amount": 28 } }
{ "scene": …, "layerId": "hero", "preset": "motionPreset:blur_out", "params": { "duration": 0.4, "amount": 20 } }
{ "scene": …, "layerId": "card", "preset": "motionPreset:flip_in",  "params": { "duration": 0.55, "from": -90 } }
```

Preview the soft edge, midpoint and sharp landing for a focus pull; inspect the edge-on pose and
face-on landing for a flip. Layout bounds alone do not measure blur or the painted edge.

`blur_in` + `blur_out` on one layer combine into a single curve, exactly as `fade_in` + `fade_out` do
on opacity—they share the `gaussian_blur` radius, and two same-id effects with animated params is a
document the validator refuses. Re-applying one preset replaces its own curve, so tuning params is a
re-apply rather than a stack. Keep `amount` at or below 32: above that the validator warns, because
large radii can be clamped and are expensive to render.

The same beats as named looks, for an editor to show and swap:

```json
{ "scene": …, "layerId": "hero", "preset": "look:blur", "params": { "length": 0.6, "amount": 28 } }
{ "scene": …, "layerId": "hero", "preset": "look:blur", "params": { "role": "out", "length": 0.4, "amount": 20 } }
{ "scene": …, "layerId": "card", "preset": "look:flip", "params": { "length": 0.55, "angle": 90 } }
```

An entrance and an exit are two looks in two role slots, each wrapping the layer in its own
`gaussian_blur`, so they never contend for one radius. `amount` tops out at 32. `flip` turns about
`axis: "y"` by default; `"x"` tips it toward the viewer. A flip turns the layer itself in depth, so
an orbit, dolly or push-in moves it with the rest of the scene and a child (`parentId`) turns with it.

A fade can quietly introduce content; a focus pull or flip can draw more attention. Choose according
to the beat's hierarchy, and inspect whether supporting motion competes with the leader.

## Wipe

Nothing about a transform can hide half a layer, so a wipe is a mask, and a mask that has to stack
with others lives in a look rather than in the layer's single `mask` field:

```json
{ "scene": …, "layerId": "hero", "preset": "look:wipe", "params": { "role": "in",  "length": 0.6 } }
{ "scene": …, "layerId": "hero", "preset": "look:wipe", "params": { "role": "out", "length": 0.4, "direction": "up" } }
```

`direction` is `right` (the default left-to-right), `left`, `up`, or `down`—the way the edge travels,
the same vocabulary `slide` uses—or a diagonal (`up_left`, `up_right`, `down_left`, `down_right`),
which moves a corner. `role: in` starts at the layer's own start; `role: out` lands on its end, so
the exit resolves exactly as the layer does. A layer holds one look per role: a second `in` is
refused (`look_role_duplicate`); to swap it, edit that `looks[]` entry with `picsart_scene_patch`.

The `reveal_in` / `reveal_out` presets write the same kind of wipe as a `reveal` look entry with
explicit travel, for when the edge itself will be tuned:

```json
{ "scene": …, "layerId": "hero", "preset": "motionPreset:reveal_in",  "params": { "duration": 0.6 } }
{ "scene": …, "layerId": "hero", "preset": "motionPreset:reveal_out", "params": { "duration": 0.4, "direction": "up" } }
```

Check the reveal edge at the start, intermediate times and end. For a layer that starts later in the
scene, check its local-time mapping rather than assuming the wipe begins at scene time zero.

The `reveal` look takes `fromX`/`fromY`/`toX`/`toY` in multiples of the subject's own size, so
`[-1, 0] -> [0, 0]` is the entrance, `[0, 0] -> [1, 0]` the exit, `[0, -1] -> [0, 0]` a downward
one; `sweep` is the travel time—`duration` is a name the look host already supplies, and the
validator refuses it as a param. A reveal preset applied twice appends a second entry instead of
retuning the first; to retune, remove the earlier entry.

**Looks stack; a `mask` does not.** Each look wraps the previous one in its own layer and puts its
mask there, so two mask-emitting looks are nested wrappers rather than a collision on one field:

```json
"looks": [ { "look": "rounded_corners", "params": { "cornerRadius": 60 } },
           { "look": "wipe",            "params": { "length": 1.0 } } ]
```

Verify that the wipe moves while the corners stay cut. The style goes first: a `static` look after a
motion look styles the motion's padded raster rather than the layer, so the validator refuses that
order (`look_order_static_after_motion`) and a `look:` preset applied with `picsart_scene_apply_preset` inserts a static look before the first
motion look. Any look that pads its subject counts there. Writing `mask` on the layer directly is
unsafe: a layer has exactly one, so the second write replaces the first.
