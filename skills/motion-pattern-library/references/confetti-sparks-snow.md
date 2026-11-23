# Confetti, sparks and snow

Many small copies of one thing, thrown and falling, are one layer with `particles`, not hand-copied
layers. The layer's `content` is the particle; its `transform.position` places the emitter:

```json
{ "id": "confetti", "transform": { "position": [540, 1080] },
  "content": { "kind": "shape", "items": [{ "type": "rect", "size": [22, 12] }, { "type": "fill", "color": "#ff3b6b" }] },
  "particles": { "seed": 1, "emit": { "bursts": [{ "time": 0, "count": 120 }] },
    "life": [2, 3.2], "direction": -90, "spread": 40, "speed": [1100, 2300], "gravity": [0, 1500],
    "spin": [-450, 450], "opacityOverLife": [1, 0.3] } }
```

Fire and embers: `"colorOverLife": ["#fff2a0", "#ffb000", "#e03000"]` multiplies a white or grey sprite by the colour at
its age (opaque `#rrggbb` stops, blended in linear light); `"blend": "add"` sums the particles' light, so overlapping
flame brightens (the layer then draws with the `add` blend; a layer authoring another `blendMode` is refused). One
cloud has one blend: flame and smoke are two layers.

Every particle draws the layer's content, so several colours are several such layers, each with its
own colour and `seed`. Each burst releases `count` particles at its `time`; a stream is
`"emit": { "rate": 40 }`, which emits until the layer ends (or for its `"duration"`), and a negative
`start` has it already running at the layer's first frame. Snow streams from a wide
`"origin": { "shape": "line", "size": [1400, 1] }` on a layer placed above the frame, with
`"direction": 90`, a small `"spread": 30` and little `gravity`: a directed throw needs a small spread,
since the default 360 throws every way. Two layers with different particle sizes, speeds and
opacities read as depth. Change `seed` for another throw of the same effect; the same seed always
draws the same frames.

Smoke, steam and dust slow and wander instead of flying free: `"drag": 1.2` (per second) bleeds a throw's
speed until the particle drifts at `gravity / drag` (a small upward `gravity` is buoyancy), and
`"turbulence": { "amplitude": 30, "frequency": 0.6 }` wanders each particle up to 30 px about its path
(a smooth seeded wiggle that is zero at birth; `frequency` is Hz, at most 60; the position keys get denser as it rises). Together they turn a
burst of sparks into a puff: `"drag": 2.2` alone makes sparks that fly out and stop.
