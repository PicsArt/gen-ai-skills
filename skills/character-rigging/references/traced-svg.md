# A traced SVG as shapes

A vectorizer's SVG (30+ `<path>`, each with its own `fill`, a `translate(...)`, a viewBox such as
`0 0 1311 2048` for a 640×1000 picture) comes in whole with `picsart_scene_import_svg_path` and `svg` in place of `d`:

```json
{ "scene": "<handle>", "layerId": "art", "svg": "<svg viewBox=\"0 0 1311 2048\" width=\"640\" height=\"1000\" ...>…</svg>",
  "skipBackground": true }
```

- One `group` per path (its outlines plus its fill/stroke), later paths on top; `perPathLayers: true`
  gives each path its own shape layer above `layerId` (`art_1`, `art_2`, …) so a part can be parented
  or posed. Read `paths` and `colors` in the result and compare with the SVG's own count.
- The viewBox maps to `targetWidth`/`targetHeight` (default the SVG's own `width`/`height`) honouring
  `preserveAspectRatio`; transforms (also on parent `<g>`) are baked into the vertices, so the layer
  needs no transform. A layer with none gets `position [0,0]`, `anchor [0,0]` (the SVG's top-left);
  keep it that way or the picture shifts.
- Pitfalls: `skipBackground` drops only a FILLED path that covers the whole canvas; a rect, circle,
  `<use>`, gradient or pattern fill is not read and lands in `skipped`, so check `skipped` before
  trusting the count. Per-path `color`/`stroke` args are refused here: paint comes from the SVG.
  `opacity` on a path or `<g>` becomes the group's opacity.

