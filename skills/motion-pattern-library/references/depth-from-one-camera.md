# Depth from one camera

Depth is planes at different `z` under ONE camera move: nearer planes travel and grow more, farther
ones less, and the difference is the effect. Place each plane with `transform.z` (positive toward the
viewer) and move the camera once — no per-layer keyframes:

```json
"composition": { "width": 1080, "height": 1920, "duration": 4, "camera": {
  "position": { "keyframes": [
    { "time": 0, "value": [540, 960], "easing": "ease_in_out" }, { "time": 4, "value": [640, 960] } ] },
  "distance": { "keyframes": [
    { "time": 0, "value": 2400, "easing": "ease_in_out" }, { "time": 4, "value": 1500 } ] } } },
"layers": [
  { "id": "background", "content": { "kind": "media", "assetId": "sky", "fit": "cover", "bounds": [1600, 2840] },
    "transform": { "z": -600 } },
  { "id": "card", "content": { "kind": "media", "assetId": "portrait", "fit": "cover", "bounds": [720, 960] },
    "transform": { "position": [540, 960] } }
]
```

Shrinking `distance` dollies in while the `z = 0` plane holds: the card keeps its size and the
background behind it shrinks away (a dolly zoom; from 2400 to 1500 its scale falls from 0.8 to about
0.71). The pivot drift slides the two against each other — a plane at `z = 0` does not move with the
pivot alone, an off-plane one does. `camera.zoom` would instead scale every plane alike
(no parallax). A farther plane renders smaller, so oversize it (`bounds` above) to keep the frame
covered; how much depends on its `z`, the `distance` and the drift — render the extremes to check.
An orbit (`camera.rotationY`) turns the whole stack in perspective; planes re-sort far-to-near as
they turn.

**Avoid when.** Planes that must interleave in depth have to be layers of the same composition: a
nested composition is one flat card at its own `z`; a look keeps its layer's depth. `motionBlur` is
refused in a composition drawn in depth. **Check.** `picsart_scene_query_layout` at the first, middle and last frames reports each
plane's projected `quad`, `center` and eye `depth`: read the differential travel off the centres,
then render the extremes to confirm the frame stays covered.

### Exploded stack

Flat planes (screens, cards, layers of a product) fan out in depth and the camera tips to show them
as a stack, then folds back. Give each plane its own `z` (e.g. `-480, -160, 160, 480` on a
1080 × 1920 frame) and animate `camera.rotationX` from `0` to a held orbit and back:

```json
"camera": { "distance": 2400, "rotationX": { "keyframes": [
  { "time": 0, "value": 0, "easing": "ease_in_out" }, { "time": 1.4, "value": -40 },
  { "time": 5, "value": -40, "easing": "ease_in_out" }, { "time": 6.2, "value": 0 } ] } }
```

`rotationX < 0` lifts the front plane highest (the classic exploded diagram); `> 0` drops it lowest.
Opaque full-frame planes read as separate only with a large orbit (about ±35° or more) and a long
`distance` (about 2.2 × the frame width or more): at ±20° and `distance` 2600 the stack reads as one
card. A label belongs to its plane by `parentId` with no `z` of its own; titles over the stack are
`cameraExempt: true` roots. **Check.** `picsart_scene_lint_layout` with `t0`/`t1` on the held orbit (a stack
that starts or ends flat hides every plane but the front one there, and `covered` reports it), two `order`
relationships, members listed front plane first: `axis: "depth"` (front to back) and `axis: "y"`
(front plane highest; it fails when the orbit's sign drops the front plane lowest). Read `covered`:
a label listed there with bucket `findings` is hidden by a plane drawn after it. Then render the
held orbit: every plane's edge is visible and each label sits on its own plane.

```json
"relationships": [
  { "kind": "order", "axis": "depth", "members": [{ "id": "front" }, { "id": "mid" }, { "id": "back" }] },
  { "kind": "order", "axis": "y", "members": [{ "id": "front" }, { "id": "mid" }, { "id": "back" }] }
]
```
