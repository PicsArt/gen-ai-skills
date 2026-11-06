# Pixel art sampling and layer follow-through

For a pixel-art atlas, put `sampling: "nearest"` on its image asset (also supported on video and
video-with-matte assets), not on the media content. A matte video uses the same sampling for colour
and matte. Nearest has no mipmaps, so shrinking aliases; use linear for smooth minification.

## Layer follow-through

Let a hair tip linger as its support moves, with a live rotational constraint:

```json
{"type":"follow_through","property":"rotation","end":[0,90],
 "inertia":0,"hold":0.22,"frequency":1.59,"damping":0.49}
```

`end` is content px from this layer's pivot and is rotation-only; it replaces the
inferred lever. `hold` (0..1, default 0) is how much the far end keeps its world
position per tick as the support moves. Damping dissipates spring motion; hold
resists moving the far end. Inertia responds to support acceleration; hold responds
to support displacement. Inertia (0..1, default 0.6), hold, frequency (0.5..10 Hz),
and damping (0.1..2, a ratio) accept numbers or tracks. Tracks sample on 1/120-second
ticks from composition time zero, so backward seeks replay deterministically.
Gravity and wind remain literal `[x,y]` accelerations, not tracks.

