# Hand-drawn line boil

`line_boil` (`appliesTo: ["shape_path"]`, tags `cartoon`, `hand-drawn`) gives a shape's outlines the
look of a line redrawn for each drawing. Each point of each `path` sits up to `amplitude` px off its
drawn place, takes a new place `rate` times a second and holds still in between. Every path boils
its own way.

**When it fits.** A sketchy, hand-inked look: a cartoon character, an explainer's drawn arrows and
doodles, a title drawn as outlines. Not for a clean UI shape, a logo or a product mock, where the
lines must stay put. It changes the outline only; the layer does not move:
- `shake` moves the whole layer, so the drawing jumps as one piece.
- A `wiggle` on a layer or a group moves that part rigidly, so its outline keeps its shape.
- The boil moves each outline point, so the line itself redraws while the figure stays in place.
  Combine it with the others: a character can boil and wiggle at once.

```json
picsart_scene_apply_preset { "scene": "...", "layerId": "cat", "preset": "line_boil",
  "params": { "amplitude": 1.5, "rate": 12 } }
```

To boil one outline, give that `path` item (or the `group` holding several) a `name` in the layer's
`content.items` and pass it as `item`: `{"type": "path", "name": "tail", "closed": false, "vertices":
[...]}`, then

```json
picsart_scene_apply_preset { "scene": "...", "layerId": "cat", "preset": "line_boil", "item": "tail",
  "params": { "amplitude": 2, "rate": 8, "seed": 3 } }
```

`amplitude` 1 to 3 px reads as a pencil line, more as a nervous scribble. `rate` must divide the
output frame rate, or the holds alternate and the cadence stutters: 12 is on twos at 24 fps, 15 on
twos at 30 fps, 8 on threes at 24 fps, while 12 at 30 fps holds 3, 2, 3, 2 frames. `seed` picks
the places; a re-render gives the same boil.

**Pitfalls and refusals, the important one first.**
- **It boils `path` items only.** `rect`, `ellipse` and `polystar` items stay still and are named in
  the result's `notes`. A character built from them looks half pasted on: its eyes stay still while
  the lines around them boil. Redraw each as a path with `picsart_scene_import_svg_path`, which takes an SVG
  `d` (an ellipse is two arcs, `M cx-rx,cy A rx,ry 0 1,0 cx+rx,cy A rx,ry 0 1,0 cx-rx,cy Z`; a
  rect is `M x,y h w v h h -w Z`), then remove the parametric item. An `item` naming one of them is
  refused (`shape_item_not_a_path`).
- A path whose vertices move on their own tracks is refused (`shape_path_driven_twice`).
- A path whose outline is still an `$eval` reference is refused (`unresolved_param_ref`): resolve the scene first.
- A keyframed whole-outline `vertices` track keeps its keyframes and boils on top of them.
- It does not stack. Applying it again, or applying it over an outline that already has an
  expression (a `loopOut`), replaces that expression, and the result's `notes` say so.
- An `item` name that no item has, or that several items share, is refused (`unknown_shape_item`,
  `ambiguous_shape_item`); name the group they share instead. A layer with no paths is refused
  (`no_shape_path`).
- Inside a held composition ([Held drawings](../SKILL.md#held-drawings-animating-on-twos)) the hold
  applies too, so keep `rate` at or under the held rate.
