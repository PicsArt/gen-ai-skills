# Text on a path

## Contents

- Authoring
- Combine path travel and character animation
- Validation loop

Use `content.textPath` when letters must sit on a curved baseline or circulate
around a closed outline. Keep the text editable; do not create one layer and
keyframe track per letter. For a whole object following a trajectory, keep the
existing position track and optional direction expression instead. This feature
does not morph shape geometry or introduce a new position-stream type.

## Authoring

This is a complete text layer for a scene at least 4 seconds long:

```json
{
  "id": "curved-title",
  "transform": {"position": [100, 300]},
  "content": {
    "kind": "text",
    "text": "FOLLOW THE CURVE",
    "font": {"size": 32},
    "color": "#ffffffff",
    "textPath": {
      "path": {
        "closed": false,
        "vertices": [
          {"point": [0, 0], "outTangent": [160, -160]},
          {"point": [600, 0], "inTangent": [-160, -160]}
        ]
      },
      "offset": {"keyframes": [{"t": 0, "v": 0}, {"t": 4, "v": 200}]},
      "normalOffset": -8,
      "alignment": "start",
      "orient": true
    }
  }
}
```

- The path uses content-local pixels relative to `transform.position`, not
  root coordinates. Parent transforms still apply once to the whole layer.
- Handles are **offsets relative to their vertex**, like shape paths.
- `offset` is distance along the path in pixels, not a normalized Bézier `t`.
  A linear offset advances at approximately constant arc-length speed.
- `offset` and `normalOffset` accept a number or the text rail's
  `{keyframes: [{t, v, easing?}], expression?}`. Times are layer-local seconds,
  including on delayed/nested instances. An expression-only value starts at 0;
  `return value + 20 * math.sin(time)` composes with the interpolated value.
- `normalOffset` shifts along the normal vector (negative tangent y, tangent x); positive shifts down on
  a left-to-right horizontal path in screen coordinates.
- Path `alignment` puts the start, center or end of the text's advance at the
  offset. Do not also author ordinary `content.alignment`, `wrapWidth` or
  `lineHeight`. Use one authored line and separate layers for multiple baselines.
- `orient: false` leaves glyphs upright while their centers follow the curve.
  It does not disable path positioning.
- Open paths hide a glyph when its advance midpoint is outside the path.
  Closed paths wrap distances, including negative offsets. Text longer than a
  closed path can overlap itself; the path is not an automatic typesetter.
- Existing glyph animators compose in the glyph's path-local frame. Geometry
  queries measure the baseline layout, not the painted result of those animators.

Keep authoring and validation in scene. Inspect real fonts and
target-platform renders for complex scripts and ligatures; a path does not
improve the underlying text shaping. Underlines and strikethrough are not
supported by this path layout.

## Combine path travel and character animation

Add this `animations` array to the text content in the complete layer above.
The named entrance reveals the letters; the concrete animator lifts a travelling
selection off the curved baseline without splitting the text into layers:

```json
"animations": [
  {"preset": "typewriter", "params": {"duration": 1.2}},
  {
    "transform": {"kind": "offset", "x": 0, "y": -26},
    "selector": {
      "basedOn": "character", "start": 0, "end": 0.28,
      "offset": [{"t": 1.3, "v": -0.28}, {"t": 3.3, "v": 1}],
      "shape": "round"
    }
  }
]
```

These three offsets have different meanings: `textPath.offset` moves the text
along the baseline in pixels; the selector's `offset` moves its normalized
character window; the glyph transform's `x`/`y` displaces selected letters in
the tangent/normal frame. A glyph's local `x` displacement is not a new
arc-length sample on the curve. To add a coordinated rotation or color wave,
append concrete `rotation` or `color` entries with the same selector. Keep one
authoritative selector definition when generating those entries.

Compare against the same scene with `content.animations` removed. That isolates
the character animation from baseline travel. Inspect selected and unselected
letters, not just the text layer's box. Opacity, scale, rotation and color can
compose with the path; this is not a guarantee that every preset or arbitrary
combination remains readable.

## Validation loop

1. Validate geometry and tracks with `picsart_scene_validate`; it cannot judge readability.
2. Query start, middle, end, reversals and seams with `picsart_scene_query_layout`, including delayed/nested instances and reverse query order. Random-access queries do not prove stateful playback.
3. Use supported `picsart_scene_lint_layout` relationships for bounds and containment. A layer AABB cannot certify glyph spacing, tangent alignment or self-overlap.
4. Compare actual output-frame geometry when motion matters. Use `picsart_scene_check_motion` for frame-complete geometry; pixel checks are not automated, and a stationary bounding box does not prove glyph motion.
5. Inspect full-resolution `picsart_scene_contact_sheet` with `resolution` set to the composition dimensions, images and continuous video for glyph orientation, spacing, clipping and closed seams.
6. Where a player is available, compare an early frame with a backward seek to that same time in the same loaded player, preserving font and viewport. Separate fresh renders or cached images do not prove state restoration. If only stills are available, leave stateful seeking unverified.

Save the scene and its contract document with the exact sample times and
validation report. If drawing a baseline guide, allow only that guide/text
overlap intentionally; do not suppress arbitrary pairs. Passing one fixture
does not guarantee arbitrary typography or edited copies.
