# Cursor paths, feedback and menus

## Contents

- Curved position tracks: complete editable scene
- Hotspot and direction
- Feedback and ownership
- Validation

Discover with category `ui_widget`, tag `cursor`, reference policy `reusable`.
Describe the selected template before applying.

| Intent | Use |
|---|---|
| Pointer appearance | `scene://ui-cursor`: arrow, hand, circle, size, fill, outline, shadow |
| Straight or curved travel | Owning-layer position keyframes with spatial tangents |
| Press response | Existing `tap_pulse` on the control owner, including its label and plate |
| Feedback at the click location | Separate expanding/fading ring with a layer-local clock |
| Open, select and confirm a menu | `scene://cursor-context-menu`: coordinated composition |

Do not add templates merely to rename position keyframes or wrap one preset. Add meaningful
structure or behavior. These are animated compositions, not event handlers. The menu independently
adapts an upstream idea; it imports neither implementation nor assets and performs no file operation.

## Curved position tracks: complete editable scene

```json
{
  "version": "1.0",
  "composition": { "width": 600, "height": 400, "duration": 2, "fps": 30 },
  "layers": [{
    "id": "cursor",
    "content": {
      "kind": "scene_ref", "sceneRef": "scene://ui-cursor", "fit": "none",
      "parameters": { "style": "hand", "size": 40, "duration": 2 }
    },
    "animations": { "position": { "keyframes": [
      { "time": 0, "value": [100, 100], "outTangent": [0, 150] },
      { "time": 1, "value": [400, 100], "inTangent": [0, 150] },
      { "time": 2, "value": [400, 100] }
    ] } }
  }]
}
```

Midpoint: [250,212.5], not [250,100]. Tangents are relative handles; easing controls progress.
Repeated positions create holds; do not carry nonzero handles into a hold segment.
An `animatable: true` `vec2` parameter accepts the same dynamic track, forwarded to
`animations.position` via `{$eval: "position"}`. No waypoint language is needed.
For delayed layers, use `timeMode: "layer"` for local keyframes; checks use root time.
Expressions already use layer-local `time`.

## Hotspot and direction

The cursor's intrinsic canvas is `4 * size` square. With `fit: "none"` and the default centered anchor,
position names the hotspot: arrow tip, hand fingertip or circle center. Explicit anchors are pixels,
not normalized coordinates. Query
`cursor__hotspot`, not glyph bounds. This invisible marker is geometry, not pixel evidence.

Position tracks do **not** automatically turn a cursor. Bind `animations.rotation.expression`
to its evaluated position direction; keep the artwork's forward-axis offset in `transform.rotation`.
For a right-pointing glyph the offset is zero:

```lua
local d = ctx.layer:getPlacement():positionDirection()
if d.x == 0 and d.y == 0 then return value end
return math.deg(math.atan(d.y, d.x)) + value
```

This is the preferred auto-orientation authoring pattern for any path-following object, not a
cursor-specific feature. Keep the expression when replacing the position track; do not regenerate
independent rotation keys or add a convenience flag with a second set of semantics. Use a separate
heading track only for intentional art direction that differs from travel. There is no
auto-orientation flag. Mutable scalar/vector properties expose `propertyVelocity()` in units/second;
vector properties also expose `propertyDirection()` as a unit vector. For example,
`positionVelocity()` can drive a speed readout. Ordinary value reads do not take extra motion samples.

Motion queries use local coordinates and numerical samples on the 120 Hz evaluation time grid, not
exact analytic tangents. Keyframed holds preserve the incoming heading, or the first outgoing
heading before travel, independently of seek order. A static path has zero direction. An expression
that is stationary at the sampled time also returns zero: there is no search through its history.
Thus the snippet falls back to the authored offset for a stationary expression; use explicit heading
intent if that expression must retain a previous turn. Hold jumps are not motion. Same-composition
layer references account for start offsets; cross-composition motion queries are refused.
If an expression reads another animated property and a motion sample crosses that property's
authored hold jump, the query fails naming the dependency. Keep motion-query windows away from
intentional cuts or author explicit heading for that cut; do not interpret a jump as travel.
Parent movement is not included. Avoid self/circular dependencies and sharp expression jumps;
rapid motion can alias at the sampling grid. This does not smooth a reversal or unwrap a heading
for subsequent interpolation. Check direction against independently sampled travel, not only position.

## Feedback and ownership

A click ring stays at the clicked location; do not parent it to a departing cursor.
Derive its time/location from the arrival event and retain its full feedback tail in the host.
Apply the `tap_pulse` look for a press response without a new template.

Menu plate, selection and rows share one entrance/exit owner. Count drives height; stage grows for
tall menus, target clamps, menu flips above if needed. It does not follow arbitrary moving targets.
Supply a nonempty string list and integer `selectedIndex` in [0,items.length). Parameter metadata
does not enforce this list-relative rule: validate in the caller and require selected row/result
presence after resolution. Copy is not automatically fitted.

Phases: click at `openAt`; reveal at `openAt+0.1`; travel after `openDuration`; arrival after
`travelDuration`; click after `selectHold`; close after 0.1s and `closeDuration`; then `tailHold`.
Recalculate checks after changing timing, count or placement.

## Validation

1. Strictly validate structure and tracks with `picsart_scene_validate`.
2. Query actual ids/root times, including `pointer__hotspot`, `menu__row_N__label` and `target__result_N` in the assembled host.
3. Compare independently intended arrival, hold, opacity, containment, exit and presence relationships using supported `picsart_scene_lint_layout` checks and explicit queries. The same relationships can run as a contract record with `picsart_scene_check_contracts`.
4. For heading, compare `rotationDeg` against independently computed travel direction, including delayed instances and holds. Position-only evidence cannot establish heading; use `picsart_scene_check_motion` on `rotationDeg` for frame-complete evidence.
5. Scan event windows with `picsart_scene_lint_layout`, allowing only named intentional overlaps.
6. Inspect full-resolution stills and continuous approach/turn/click/menu/exit video. Pixel stability is not asserted automatically; geometry cannot establish clipping, legibility or paint quality.

Adapt windows, IDs, bounds and regions to the actual request. Negative controls must fail:
displaced arrival, hold drift, wrong rotation, early reveal, overflowing text or missing selection.
Report analysis, pixel checks and visual inspection separately.
