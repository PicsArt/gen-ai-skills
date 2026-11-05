# Frosted glass

## The look

`frosted_glass` puts a frosted pane the size of a layer's box beneath that layer:

```json
{ "id": "card", "content": { "kind": "color", "color": "#ffffffff", "size": [600, 400] },
  "transform": { "position": [540, 700], "opacity": 0.35 },
  "looks": [ { "look": "frosted_glass", "params": { "blur": 40, "cornerRadius": 32 } } ] }
```

- **Box:** the pane is the layer's `bounds` (a colour's `size`). A `scene_ref` widget needs
  `bounds` equal to its own size, and its surface opacity below 1 (`surfaceOpacity`,
  `fillOpacity`, `bubbleOpacity` or `trackOpacity`, by widget) or the surface hides the pane.
- **Params:** `blur`, `tint` (opaque `#rrggbb`) at `tintOpacity`, a `rimWidth` px edge at
  `rimOpacity`, `cornerRadius`.
- **Motion:** the layer's own `position`, `scale`, `rotation` and `opacity` tracks move and
  fade the pane with it. `fade` and a `start`/`duration` window on the look entry scale the pane
  alone.
- **Rules:** it is the last of the layer's `looks` (`look_backdrop_not_last`) and takes no motion
  look beside it (`look_order_static_after_motion`): animate the layer itself instead. The layer carries
  no `mask` or non-normal `blendMode` (`look_backdrop_host_isolated`), no `anchor`
  (`look_backdrop_host_anchor`), no `opacity` expression
  (`look_backdrop_host_opacity_expression`) and no `min` / `max` on its `opacity` track
  (`look_backdrop_host_opacity_limit`).

## By hand

For a pane that is not a rounded rect, or one that does not follow a layer, write the two
layers yourself, the blur first and the tint above it:

1. **Blur** — `adjustmentLayer: true` with `gaussian_blur`. It blurs everything composited
   beneath it, clipped to its silhouette. Its fill only marks the region, so any opaque colour
   works.
2. **Tint** — an ordinary shape layer: a white fill at low `opacity` and a thin white stroke.

```json
{ "id": "glass", "content": { "kind": "composition", "blending": "pass_through", "layers": [
  { "id": "glass_blur", "adjustmentLayer": true, "transform": { "position": [960, 540] },
    "content": { "kind": "shape", "items": [ { "type": "group", "contents": [
      { "type": "rect", "position": [0, 0], "size": [1100, 600], "roundness": 60 },
      { "type": "fill", "color": "#ffffffff" } ] } ] },
    "effects": [ { "id": "gaussian_blur", "params": { "blur": 40 } } ] },
  { "id": "glass_tint", "transform": { "position": [960, 540] },
    "content": { "kind": "shape", "items": [ { "type": "group", "contents": [
      { "type": "rect", "position": [0, 0], "size": [1100, 600], "roundness": 60 },
      { "type": "fill", "color": "#ffffffff", "opacity": 0.18 },
      { "type": "stroke", "color": "#ffffffff", "width": 3, "opacity": 0.5 } ] } ] } } ] } }
```

Shape paint colours carry no alpha: `#ffffff2e` is refused. Write the colour opaque and set
the transparency with the paint's `opacity`. The pane's edges stay clean, with no dark rim,
because the blur samples pixels beyond the outline.

## Where it frosts

The blur grades the canvas it composites into, so the content to frost must be beneath it
on that canvas:

| Placement | Frosts |
|---|---|
| The two layers as siblings, after the content in the same `layers` list | yes |
| Wrapped in an unsized composition with `blending: "pass_through"`, after the content | yes |
| Wrapped in a composition with `blending: "isolated"` or no `blending` | nothing, only the tint draws |
| Wrapped in a sized composition (`composition: { width, height }`) | nothing |
| Inside a `scene_ref`, a scene asset or a `scene://ui-*` widget preset | nothing beyond the scene's own layers |

The validator warns `adjustment_layer_grades_nothing` at the blur layer when nothing is
beneath it, and names the cause.

## Animating it

- **Fade or reveal:** put the `opacity` keyframes on BOTH children, not on the wrapper. An
  opacity below 1 or an opacity animation on the wrapper makes it render isolated, and the
  blur disappears. A mask, looks, effects, a non-normal `blendMode` or `adjustmentLayer` on
  the wrapper do the same.
- **Move:** a `transform.position` on the unsized wrapper is an OFFSET from the frame centre.
  A wrapper at `[1160, 540]` in a 1920×1080 frame moves children authored at `x: 1360` to
  `x: 1560`.
- **A shadow under the pane:** a `drop_shadow` in the tint's `effects` keeps the pane frosted
  (it is on a child, not the wrapper). The shadow also shows through the translucent tint, so
  the pane reads darker than without it.

## Limits

- **Cost** grows with blur radius and blurred area. Measure actual playback before committing to a large pane.
- **Refraction** is not part of this construction: it produces frosting, not displacement.
- Validate and inspect the requested output; leave unsupported compositing behavior unverified.
