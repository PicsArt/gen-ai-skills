# A still painted background that lives

- **Tree crowns, grass, water painted into the picture:** `picsart_scene_apply_preset` with `preset` `mesh:auto`
  and `motion` (`{ "kind": "sway" }` or `"water"`, a `region` `[x, y, width, height]` in content px) writes the
  background's own `mesh` with morphs on expressions. The motion loops for as long as the layer lasts. Keep a
  `water` region on the water: a bank inside it bends too.
- **A drifting cloud:** a cloud on its own transparent layer, keyed slowly across with linear
  easing (a few px a second; it should not be noticed moving). A cloud painted into the background
  cannot leave its place: cut it out to its own picture and paint the sky behind it first
  (`scene-gradients`).
- **Birds:** a shape layer, one group a bird. Each bird is an open three-point path with a round
  stroke, and its wing tips beat on a morph weighted by an expression. The group's `position` is
  keyed across the sky, linear. Shape px count from the layer's position, the frame's centre by
  default: this bird crosses a 960 px wide frame in 12 s, just above the middle.

```json
{ "type": "group", "position": { "keyframes": [
    { "time": 0, "value": [-500, -20], "easing": "linear" }, { "time": 12, "value": [500, -40] } ] },
  "contents": [
    { "type": "path", "closed": false,
      "vertices": [
        { "point": [-9, -1], "outTangent": [4, -3] },
        { "point": [0, 2], "inTangent": [-3, -3], "outTangent": [3, -3] },
        { "point": [9, -1], "inTangent": [-4, -3] } ],
      "morphs": { "flap": {
        "offsets": [ { "point": [0, 5] }, { "point": [0, -1] }, { "point": [0, 5] } ],
        "weight": { "expression": "return math.sin(time * 12.6)" } } } },
    { "type": "stroke", "color": "#2b2b2b", "width": 1.3, "lineCap": "round", "lineJoin": "round" } ] }
```

Give each bird its own speed, height and wingbeat phase (`+ 1.7` inside the `sin`), about two
beats a second; a wingspan near 2% of the frame's width reads as far away.
