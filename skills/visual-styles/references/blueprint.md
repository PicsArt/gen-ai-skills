# Blueprint

A technical drawing on blueprint paper: a faint grid, dashed construction lines, a desk lamp drawn on in white
line work, dimension callouts and a title block, and finally the lamp's arm swings on its joint.

## Palette

Paper `#1d4f91`, line `#e8f1ff`, grid white at about 12 % opacity. **The hero is the pale line colour
`#e8f1ff`**; there is one drawing colour and it carries everything (outlines, dimensions, text).

## The medium

- A **grid**: vertical and horizontal hairlines every 40 px, 1 px, white at 12 % opacity.
- **Construction lines**: dashed lines (length 14, gap 10), 2 px, line colour at 50 % opacity, drawn first through
  the object's axes and joints.
- **The object** is outline only: 4 px strokes with no fill. Draw each part as its own layer (a base, a lower
  arm with a joint circle, an upper arm and head as a group anchored at the joint) so the part can move later.
- **Dimensions**: a line between two points with a short diagonal tick at each end (2 px), and a number and unit
  in capitals beside it. A title block at a corner says what it is and a revision.
- A **frame**: a 3 px rectangle just inside the edge.

## Motion habits

- **Draw in drafting order:** construction lines (0.2-1.2 s), then each part's outline with `trim` end 0 to 1
  (about 0.7 s each, overlapping), then dimensions (line then text), then the title.
- **Show it works:** after drawing, the upper arm swings about its joint: rotation keys of about -18, +6, 0
  degrees over 2 s with the ease-in-out easing; the group is anchored at the joint.
- Keep construction dashes static; a marching dash is possible but busy.
- Cued layers use `timeMode: "layer"`.

## Type

A condensed display face in capitals, the line colour, for dimensions and the title block; no mixed case.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. One drawing colour plus the grid; no fills.
2. Construction lines come before outlines.
3. Every dimension has two ticks and a unit.
4. Moving parts are separate layers anchored at their joints.
5. A title block names the part and a revision.

## Build with the tools

Build each part as a shape layer with `trim` and 4 px stroke; anchor the swinging group at the joint; build
dimensions from a short helper in a script. Check angles with `picsart_scene_query_layout`.

## Do / don't

- **Do** draw hidden joints (circles) as full circles.
- **Don't** shade parts, add colour, or use a perspective view; keep to an orthographic view.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Line width: no zoom, width fixed (4 px outlines, 2 px construction lines and ticks, 1 px grid).
  - Nothing fades: everything is drawn or written; construction lines, outlines and dimension lines by `trim`, dimension numbers and the title block by `typewriter`; the grid and frame are the paper and are there from the first frame; the only transition is a hard cut.

## Originality guard

Draw your own object. It must not reproduce a real manufacturer's drawing, a famous patent figure, or a known
lamp's silhouette. The blueprint colours, construction lines, dimensions and drafted draw-on are the style.

## Proven on

The desk-lamp-blueprint film (a gridded blueprint with construction lines, a lamp drawn on, two dimensions,
a title block and a swinging arm).
