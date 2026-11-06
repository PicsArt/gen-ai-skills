# Secondary motion on layers and bone chains

Choose parameter-mode `follow_through` for rig-control-driven sway, layer-mode
`follow_through` for world-motion physics on bone layers, and `walk_cycle`'s `followLag`
for baked walk lag. A layer constraint works identically on empty bones, shapes and art meshes.
A layer with no `parentId` follows its composition's host world transform; at the scene
root that transform is identity. It can also swing under gravity or wind.
The authored `rotation` is the rest pose; physics adds its swing to that rotation. Set a
tail's resting direction on the bone, then let the spring supply the lag. An animated
rotation remains the authored pose at that time, with the swing added on top.

The spring vocabulary and ranges are shared across both hosts; each host keeps its own defaults:

| Parameter | Range / default | Meaning |
|---|---|---|
| `frequency` | 0.5..10 Hz / parameter 1.8, layer 1.59 | Natural frequency, ω = 2πf |
| `damping` | 0.1..2 / parameter 0.3, layer 0.49 | Damping ratio; below 1 rings, 1 is critically damped |
| `property` | rotation (default), position, scale | Layer channel to simulate |
| `inertia` | 0..1 / 0.6 | Layer response to parent world acceleration |
| `hold` | 0..1 / 0 | Layer constraint: fraction of support displacement retained each tick |
| `end` | finite nonzero [x,y] / inferred lever | Rotation-only layer constraint: content-pixel vector from this layer's pivot to its far end |
| `gravity`, `wind` | literal [x,y], each -100000..100000 / [0,0] | Layer world acceleration in px/s²; +y down; affects position and angular pendulums; no tracks |
| `follow` | parameter/weight list / required for parameter host | Rig controls that drive parameter sway |
| `amount` | -10..10 / 1 | Parameter swing multiplier |
| `segments` | integer ≥1 / 1 | Number of generated parameter followers |

Rotation bounds belong on the driven animation track's `min`/`max`, using the existing bounded
path. Vector position and scale tracks currently remain unbounded;
there is no separate spring `limit`, `mass`, or `strength` control. Forces are accelerations.

On a layer's `follow_through` constraint, `inertia`, `hold`, `frequency` and `damping`
accept numbers or tracks. They evaluate on fixed 1/120-second ticks from composition
time zero, so backward seeks replay deterministically. `end` replaces the inferred
rotation lever; position and scale constraints refuse it. Author `hold`, `end` or live
control tracks directly on the constraint; the preset's parameter inputs are separate.
See the **Layer follow-through** example in `character-rigging` for a hair tip held back by support motion.

Inertia responds to support **acceleration**, hold retains part of its **displacement**,
and damping dissipates the spring's velocity. Hold is not another damping control:
use it to keep the far end from immediately travelling with its support. For position
and scale it retains the corresponding channel's support displacement.

For hair and ponytail layer chains, start with **inertia 0.7 and damping 0.5**, then tune
from root to tip. These are authoring recommendations, not host defaults: omitting frequency
and damping still uses 1.59 Hz / 0.49 on layers and 1.8 Hz / 0.3 on parameters. Use the
following starting points; the damping range is for deliberate tuning after the first render:

| Part | Frequency starting range | Damping start / tuning range | Inertia start |
|---|---|---|---|
| Tail | 1.2–2 Hz | 0.65 / 0.4–0.65 | 0.35 |
| Hair / ponytail | 1.5–2.5 Hz | 0.5 / 0.4–0.65 | 0.7 |
| Cape | 0.8–1.5 Hz | 0.65 / 0.4–0.65 | 0.35 |

Lower damping keeps more ringing; no damping value below 1 promises exactly one overshoot.
In the measured five-link chain, damping 0.4 rang twice after the support stopped:
about −3.0° then +1.4°. Check the whole chain after a stop, not just the root link.
In the measured two-link walking ponytail at inertia 0.7 / damping 0.5, the first link
peaked at 3–4° after +3 frames, the second at 13–15° after +4–5 frames, and the chain
settled in about 9 frames. These observations describe that rig and motion, not guaranteed
amplitudes or timing for every chain.

The inertial spring responds to **acceleration**: starts, stops, reversals and walking bob
excite it. Steady travel at constant speed does not sustain a trailing pose; after the
transient, the spring returns toward its rest pose. Use `wind` to represent drag when a
constant-speed character needs hair held behind it. `wind` is an authored acceleration,
not an automatic speed-dependent drag model.

### Worked five-segment hair chain

Move the support sideways; changes in the support's travel
speed excite the hanging chain. Start each link with inertia 0.7, frequency
1.59 Hz and damping 0.5, then tune from root to tip. The studied reference target is
2–5 frames of extra lag per link and amplitude ×1.1–1.4; those are tuning observations,
not automatic multipliers. Spine's default physics corresponds approximately to
frequency 1.59 Hz and damping 0.49.

Each link is a child of the one above it (the first of the moving support), with its pivot at its
top edge, a bounded rotation track and its own constraint. The first of five links:

```json
{ "id": "hair1", "parentId": "head",
  "transform": { "position": [20, 40], "anchor": [15, 0] },
  "animations": { "rotation": { "keyframes": [{ "time": 0, "value": 0 }], "min": -40, "max": 40 } },
  "content": { "kind": "shape", "items": [
    { "type": "path", "closed": true, "vertices": [
      { "point": [0, 0] }, { "point": [30, 0] }, { "point": [27, 48] }, { "point": [3, 48] } ] },
    { "type": "fill", "color": "#40d8b0" } ] },
  "constraints": [{ "type": "follow_through", "property": "rotation",
    "inertia": 0.7, "frequency": 1.59, "damping": 0.5 }] }
```

`hair2` to `hair5` repeat it with `parentId` the link above and `position` `[15, 48]`; `head` keys a
sideways `position` move (700 → 810 → 620 → 700 px over 1.2 s, then a hold).

Or apply the preset to an existing segment with `picsart_scene_apply_preset`:

```json
{"preset":"motionPreset:follow_through","layerId":"hair1",
 "params":{"property":"rotation","inertia":0.7,"frequency":1.59,"damping":0.5}}
```

Rotation reacts to support linear and angular acceleration; the pendulum's hanging axis is local +y.
Position simulates offsets in world pixels and maps them back into parent space; scale
responds to parent world-axis scale. These controls are not an exact Spine/Live2D import.

**Nested rigs and clocks:** world motion includes the composition host, its parents and every
outer host. Two placements of the same rig have independent simulations. Physics uses
elapsed presentation time from the instance's first active frame: a host starting at 2s
shows its zero-displacement opening pose at 2s. Each tick samples outer hosts at absolute
presentation time, then maps forward through their source clocks to sample authored poses.
A moving host still excites a rig whose source time is frozen or looping. A nested composition
that declares a lower frame rate holds its solved pose with each drawing; a 12-fps rig in a
24-fps scene shows the same local pose on both host frames. Camera motion does not move the
physical support. Keep this planar rig and its hosts in the world x/y plane.

Explicit-time placement reads use composition seconds. At speed 2, `position(1)` samples
the pose at presentation time 0.5s after the host starts. Reverse playback maps in the reverse
direction. Loops and ping-pong select the valid occurrence nearest the current presentation
time, with the earlier occurrence winning ties; they never select a loop before the instance
starts. A frozen source has no unique inverse and samples its current presentation occurrence.
Lower-frame-rate sampled reads select the held drawing's entry pose too.

**Seeking and cost:** a chain is a replay from the instance's first active frame with zero
displacement and velocity, in fixed 1/120 s ticks, so output fps and earlier seeks never change the
answer. Forward playback advances only new ticks; a backward seek replays from the start, so random
backward seeks cost more than sequential playback. A placement expression that reads an ancestor
keeps that ancestor's simulation separate and can cost more than a chain of keyed poses. Hold the opening pose for a gravity pre-roll.

**Pitfalls:** the complete ancestor chain must stay planar and parent scale must be nonzero
throughout the replay, including the instance's first active frame. A scale-in from zero is unsupported even when
sampling a later frame; use opacity to reveal a rig while preserving its transform space.
Transform stacks are supported. Use one writer per (layer, channel): rotation physics plus
position attach is legal, two position writers are not. Put looks on an outer wrapper.
`property`, `inertia`, `hold`, `end`, `gravity`, and `wind` are layer-only; `follow`, `amount`, and
`segments` are parameter-only. `frequency` and `damping` mean the same thing in both.
