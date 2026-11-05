# Settle and wiggle

Secondary motion on top of a part's keys: on a layer, or with `item` on one named group of a 2D
`shape` layer. Which of `follow_through`, `settle`, `wiggle`, `sway` and `shake` to use is the
table in [secondary-motion.md](secondary-motion.md).

A drawn character's tail, antennae and whiskers are such groups; a character built as separate
layers takes the preset on the part's layer instead.

`settle` carries the part on past where its keyed motion stops and damps it back: a cat runs in and
stops, and its tail, keyed to swing up as it runs, keeps going and settles over the next beats.

```json
picsart_scene_apply_preset { "scene": ..., "layerId": "cat", "item": "tail", "preset": "motionPreset:settle", "params": { "frequency": 3, "decay": 4, "amplitude": 0.08 } }
```

It follows the keys of what it is applied to: the layer's own `position` and `rotation`, or the
group's own time keys. It does nothing until that motion stops, so a constant, a loop that never
stops, or a part moved only by its parent gives nothing; key the part's own move. `amplitude` is
seconds of the move's top speed (0.05 after 800 px/s swings up to about 40 px), and the swing is
over 6 / `decay` s after the stop. Starting sets:

| Feel | `frequency` | `decay` | `amplitude` |
|---|---|---|---|
| gentle, a soft ear | 2 | 5 | 0.05 |
| bouncy, a cartoon tail or antenna | 3 | 3 | 0.1 |
| stiff, a short spring or a sign | 6 | 12 | 0.02 |

**Cost.** Each frame reads the motion back over 6 / `decay` s, and during the swing it reads the whole
move into the stop for its top speed. Measured natively, per settled part and frame: about 1 ms on a
group and 2 ms on a layer after a move of a second or two, but 4 ms (group) / 11 ms (layer) after a
10 s move and 10 / 22 ms after 30 s or more. After a long move, settle only a few parts at once.

`wiggle` wobbles the part around its keyed pose (`frequency` Hz, `angle` in degrees, `amount` in px,
`seed`), within `angle` and `amount`. Give each neighbouring part its own seed, so a set of whiskers
never moves as one:

```json
picsart_scene_apply_preset { "scene": ..., "layerId": "cat", "item": "whiskerL", "preset": "motionPreset:wiggle", "params": { "angle": 3, "frequency": 3, "seed": 1 } }
picsart_scene_apply_preset { "scene": ..., "layerId": "cat", "item": "whiskerR", "preset": "motionPreset:wiggle", "params": { "angle": 3, "frequency": 3, "seed": 2 } }
```

Starting values: whiskers 2–4°, antennae 6–10°, a tail 8–15°, at 1–2 Hz (whiskers up to 4 Hz).

**Both on one part.** A group's track carries one expression, so a second preset on the same group
replaces the first (the apply notes say so). For a tail that settles and wiggles, put `settle` on the
group and `wiggle` on a group inside it (`tail` around `tailTip`). On a layer, apply `settle` first
and `wiggle` after it: the wiggle stacks as its own component; the other way round is refused.

**Refusals.**
- `keyed_motion_unreadable`: `settle` on a group keyed `by` a parameter, or on a layer another
  transform component moves (another preset, or your own animated `transforms[]` entry).
- `unknown_shape_item` / `ambiguous_shape_item`: `item` names no item (the message lists the named
  items), or several share the name (it lists where each one is, such as `items/0/contents/1`). `shape_item_not_a_group`: the item is not a group; name the group
  around it.
- `preset_kind_mismatch`: `item` on a layer that is not a `shape` layer, or on a 3D, camera or
  parameter preset.
- `preset_not_for_group`: a preset that writes keys, effects, looks or a layer constraint
  (`follow_through`), which a group cannot carry.

iOS authoring applies a preset to a whole layer only.
