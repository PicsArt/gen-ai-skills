# Morphing a shape's outline

Part of [the character-rigging recipe](../SKILL.md); sections 1 to 11 of it, read on their own.

## Contents
- 1 Prepare the drawings; 2 Choose the technique; 3 Targets; 4 Timing; 5 Breakdowns; 6 Volume; 7 Faces; 8 Scene-to-scene morph transitions; 9 When not to morph; 10 Bending a picture and live pins; 11 Explicit skin weights

## 1. Prepare the drawings

- Draw A and B each as its own best outline, then match them — the three things a morph needs:
  the same vertex count, the same winding (the sign of the signed area, Σ (xᵢ·yᵢ₊₁ − xᵢ₊₁·yᵢ),
  agrees) and the same start vertex on the same feature of both drawings.
- A missing vertex is added, not faked with a handle: an eased segment needs equal counts
  (`shape_path_vertex_count_mismatch`), and a handle dragged to stand in for a corner bulges mid-morph.
- Corresponding vertices should sit on the same feature of both drawings (top-centre to top-centre,
  tip to tip). Every vertex travels a straight line to its twin; unrelated twins cross and the
  outline twists through itself.
- Give the outline enough vertices for its roundest pose, and no more: 8 round a blob or a mouth,
  evenly spread, a flat contact edge included. With fewer, each span carries a bigger bend and the
  squashed, stretched or opened poses go lumpy. A morph reads through clear silhouettes. A drawing with many sub-shapes, holes or an
  open↔closed change does not morph; it swaps (§2) or dissolves.
- Round stays round: every smooth vertex carries `inTangent`/`outTangent` in every pose, sized to
  that pose (`r · 4/3 · tan(π / 2N)` for N vertices on a circle of radius r, `0.552·r` at 4). A pose
  that opens, widens or grows lengthens its handles in proportion; handles kept from a smaller pose
  flatten the curve and leave corners. A vertex without handles is a deliberate corner.
- A morph changes the outline only: the drawing's `fill` and `stroke` (width, join, cap) stay as
  drawn. A colour change rides on the fill's own keyframes, not on the outline.

## 2. Choose the technique

| Need | Write |
|---|---|
| One drawing becomes another (A→B, A→B→C) | `vertices` keyframe track, one `easing` per segment |
| Independent changes that mix (open + smile + blink) | `morphs`: named targets, each with its own `weight` |
| One part on its own timing (tail tip lags, one mouth corner) | static `vertices` list, that vertex's `point`/handles keyframed |
| Replace drawings without blending (mouth charts, frame-by-frame) | `"easing": "step"` on the earlier keyframe; counts may differ |
| A catalog mouth or cartoon wipe, no outlines of your own | `picsart_scene_looks {"tags": ["cartoon"]}`: `mouth_shapes` takes `shape` as a name (the visemes `rest`/`aa`/`oh`) or a step track of names; `squash_wipe` uncovers its layer |
| Loop, breathe, wobble | `vertices.expression`: `return ctx:loopOut("cycle")` repeats the outline keyframes; or a target whose `weight.expression` cycles (`return picsart.oscillate(time, 0, 1, 1.2)`), or a `scale` expression |

A path has one driver: a `vertices` track or per-vertex tracks, never both (`shape_path_driven_twice`).
`morphs` add on top of either, so a wobbling base can still smile.

```json
{ "type": "path", "closed": true,
  "vertices": { "keyframes": [
    { "time": 0.0, "easing": "step", "value": [
      {"point": [0, -80], "inTangent": [-44, 0], "outTangent": [44, 0]}, {"point": [80, 0], "inTangent": [0, -44], "outTangent": [0, 44]},
      {"point": [0, 80], "inTangent": [44, 0], "outTangent": [-44, 0]}, {"point": [-80, 0], "inTangent": [0, 44], "outTangent": [0, -44]}] },
    { "time": 0.4, "easing": "ease_in", "value": [
      {"point": [0, -80], "inTangent": [-44, 0], "outTangent": [44, 0]}, {"point": [80, 0], "inTangent": [0, -44], "outTangent": [0, 44]},
      {"point": [0, 80], "inTangent": [44, 0], "outTangent": [-44, 0]}, {"point": [-80, 0], "inTangent": [0, 44], "outTangent": [0, -44]}] },
    { "time": 0.7, "easing": "ease_out", "value": [
      {"point": [12, -96], "inTangent": [-46, 0], "outTangent": [46, 0]}, {"point": [96, 10], "inTangent": [0, -46], "outTangent": [0, 46]},
      {"point": [-8, 70], "inTangent": [46, 0], "outTangent": [-46, 0]}, {"point": [-70, -14], "inTangent": [0, 46], "outTangent": [0, -46]}] },
    { "time": 1.0, "easing": "ease_in_out", "value": [
      {"point": [0, -130], "inTangent": [-22, 0], "outTangent": [22, 0]}, {"point": [40, 0], "inTangent": [0, -72], "outTangent": [0, 72]},
      {"point": [0, 130], "inTangent": [22, 0], "outTangent": [-22, 0]}, {"point": [-40, 0], "inTangent": [0, 72], "outTangent": [0, -72]}] },
    { "time": 1.2, "value": [
      {"point": [0, -120], "inTangent": [-26, 0], "outTangent": [26, 0]}, {"point": [48, 0], "inTangent": [0, -66], "outTangent": [0, 66]},
      {"point": [0, 120], "inTangent": [26, 0], "outTangent": [-26, 0]}, {"point": [-48, 0], "inTangent": [0, 66], "outTangent": [0, -66]}] }
  ] } }
```
Hold (0–0.4, `step` on an identical outline) → breakdown at 0.7 that is not the midpoint → overshoot
past B at 1.0 → settle on B at 1.2. Each pose carries its own handles (`0.552 ×` its half-width or
half-height), so the circle stays round on its way to the tall ellipse.

A `puckerBloat` item puffs or pinches a whole outline (`amount` animatable): see [references/outline-mechanics.md](outline-mechanics.md) "Puff or pinch a whole outline".

## 3. Targets (blend-shape hygiene)

- One target, one change, small: `jawOpen` moves the jaw vertices only, `{}` for every other vertex.
  Targets that each touch everything fight when mixed.
- A target that moves a smooth vertex moves its handles too: offset `inTangent`/`outTangent` along
  with `point` so that in the target pose the handles still point along the outline (parallel to the
  line between the vertex's two neighbours) and stay in proportion to the new curve (an opening lip's
  handles lengthen as it drops). An offset with `point` alone keeps the base's handles: what grew goes
  flat, what turned kinks.
- A corner that opens gains handles in the target: a closed mouth meets at sharp corners, an open one
  is rounded there, so `aa`/`oh` give each mouth corner short handles along the lips. A corner stays
  sharp only where the open drawing is sharp too.
- Offsets are relative to the base outline, so the base may be redrawn; the vertex count may not —
  every target has one offset per vertex (`shape_path_morph_vertex_count_mismatch`).
- A combination that looks wrong (smile × jawOpen pinches the corners) gets a corrective target whose
  offsets are only the fix, weighted by the product of the two drivers. Drive the two from
  `animatable` parameters and read them in the corrective's `weight.expression`.
- An in-between (the half-open mouth is not half of the open mouth): author a second target for the
  mid pose and cross-fade — `mid` rises 0→1 while `full` stays 0, then `mid` falls 1→0 as `full`
  rises 0→1.
- Keep weights in 0..1 except for a deliberate overshoot or anticipation (§4); weights are not clamped.

```json
"parameters": { "smile": { "type": "number", "default": 0, "animatable": true },
                "jaw":   { "type": "number", "default": 0, "animatable": true } },
...
{ "type": "path", "closed": true, "vertices": [
    {"point": [-60, 0]},
    {"point": [-30, -8], "inTangent": [-19, 2], "outTangent": [9, -1]},
    {"point": [0, -9], "inTangent": [-11, 0], "outTangent": [11, 0]},
    {"point": [30, -8], "inTangent": [-9, -1], "outTangent": [19, 2]},
    {"point": [60, 0]},
    {"point": [30, 8], "inTangent": [19, -2], "outTangent": [-9, 1]},
    {"point": [0, 9], "inTangent": [11, 0], "outTangent": [-11, 0]},
    {"point": [-30, 8], "inTangent": [9, 1], "outTangent": [-19, -2]}],
  "morphs": {
    "happy": { "offsets": [
        {"point": [-2, -10]}, {"inTangent": [0, -2], "outTangent": [0, 1]}, {},
        {"inTangent": [0, 1], "outTangent": [0, -2]}, {"point": [2, -10]},
        {"inTangent": [-1, -4], "outTangent": [0, 2]}, {}, {"inTangent": [0, 2], "outTangent": [1, -4]}],
      "weight": { "expression": "return ctx.composition:getParameters():smile()" } },
    "aa": { "offsets": [
        {"point": [4, 16], "inTangent": [0, 12], "outTangent": [0, -12]},
        {"point": [2, -6], "inTangent": [1, 4], "outTangent": [-1, -2]},
        {"point": [0, -9], "inTangent": [1, 0], "outTangent": [-1, 0]},
        {"point": [-2, -6], "inTangent": [1, -2], "outTangent": [-1, 4]},
        {"point": [-4, 16], "inTangent": [0, -12], "outTangent": [0, 12]},
        {"point": [-2, 38], "inTangent": [-1, -4], "outTangent": [1, 2]},
        {"point": [0, 41], "inTangent": [-1, 0], "outTangent": [1, 0]},
        {"point": [2, 38], "inTangent": [-1, 2], "outTangent": [1, -4]}],
      "weight": { "expression": "return ctx.composition:getParameters():jaw()" } },
    "happyAa": { "offsets": [{"point": [2, 3]}, {}, {}, {}, {"point": [-2, 3]}, {}, {}, {}],
      "weight": { "expression": "local p = ctx.composition:getParameters() return p:smile() * p:jaw()" } } } }
```
Eight vertices clockwise from the left corner: corners 0 and 4, upper lip 1–3, lower lip 5–7. The
lips are smooth, each handle `4/3 · tan(Δθ/4)` of the arc it spans. `aa` opens to a round mouth
(a 56 × 34 half-axis ellipse): every lip vertex moves with its handles, and the corners gain handles
of 12 so the open mouth rounds off there. `happy` lifts the corners without handles, because a
smile's corners stay sharp, and re-aims the lip handles along the lifted line.
On the eye path, a blink is one target with a hold at closed:
```json
"morphs": { "blink": { "offsets": [{}, {"point": [0, 14]}, {}, {"point": [0, -14]}],
  "weight": { "keyframes": [{"time": 1.40, "value": 0, "easing": "ease_in"}, {"time": 1.48, "value": 1, "easing": "step"},
                            {"time": 1.54, "value": 1, "easing": "ease_out"}, {"time": 1.66, "value": 0}] } } }
```

## 4. Timing

- Anticipation: a small move the other way first — `weight` 0 → −0.15 → 1, or an outline keyframe
  a little "before A" ahead of the main segment. Short: a few frames.
- Overshoot and settle: `weight` 1.2 → 1, an outline keyframe past B followed by B, or a
  `cubic_bezier` easing whose `y` leaves 0..1 (`[0.175, 0.885, 0.32, 1.275]`); render to check the
  peak, the control number is not the overshoot.
- Slow in / slow out: `easing` on the starting keyframe of every segment, per target weight; a
  keyframe without `easing` is `linear` — right for a hold-to-swap, wrong for a pose change.
- Holds: repeat the value on the next keyframe, or `"easing": "step"`. Keys read when they rest.
- Follow-through: parts arrive at different times — a second target whose weight keyframes are
  delayed, or a per-vertex track lagging the body.
- Timing is the count of frames between poses; spacing near a pose is tight (ease), the middle is
  wide. A morph under ~0.2 s reads as a swap — then write the swap.

## 5. Breakdowns

The middle drawing is not the average of A and B. Favour one key, and add the extra movement the
straight path lacks (A → Z → B): a third outline keyframe, or a transient target that peaks mid-way
(`weight` 0 → 1 → 0 across the A→B segment) on top of the track. Vertices travel straight lines, so
an arc, a bulge or a lean exists only as a breakdown.

## 6. Volume

A squash keeps its area: lower by ×0.8, widen by ×1.25. For a target, the squash offsets lower
the top and push the sides out together, and stretch the horizontal handles of the top and bottom
by the same ×1.25 (shorten the vertical ones by ×0.8) so the widened body stays round; for a whole-layer squash, `scale` `[1.25, 0.8]` with the
`anchor` on the contact edge. Measure the ink area on `picsart_scene_contact_sheet` frames rather than trusting the numbers; the eye reads volume loss as deflation.

## 7. Faces

- Name mouth targets by the VRM presets: `aa`, `ih`, `ou`, `ee`, `oh`; eyes `blink`, `blinkLeft`,
  `blinkRight`; moods `happy`, `angry`, `sad`, `relaxed`, `surprised`. Consonants borrow the nearest
  vowel at a lower weight.
- Mood geometry owns the corners, brows and lids; `aa`, `ih`, `ou`, `ee`, `oh` own the aperture and speech shape, whatever the mood strength. `speech` 1 reserves the aperture through the whole dialogue, pauses and closures included (a surprised O closes on m, b, p only inside that window); `speech` 0 restores the mood's resting mouth. Pass `visemes: ["aa","ih","ou","ee","oh","speech"]` to `lipSync:visemes` and merge every returned track into the rig instance's parameters. A mood change eases 0.4 s from the evaluated current weights: key the current values, then the next recipe 0.4 s later with `ease_in_out` on the outgoing keys, and clear the outgoing mood weights; never reset to neutral at the change or step-select a mouth drawing to change a vector mood.
- Visemes cross-fade: at any moment the viseme weights sum to about 1, each segment eased, with a
  short hold on a stressed vowel.
- Lip sync from word timings: `picsart_scene_apply_preset` with `preset` `lipSync:visemes`, `layerId` the
  rig layer and in `params` the transcript (a `captions` `transcript`, as transcription returns it) and
  the face's `visemes`; it merges one track per control into the rig layer's `content.parameters`. It opens a syllable per vowel group, leads the sound by 50 ms,
  dips rather than shuts inside fast words, and closes on rests and on every m, b and p (60 ms shut up
  to the release; `closures` lists them). `params`: `transcript` the word timings in the voice's own
  seconds; `visemes` the face's mouth controls; `start` the scene second at which the transcript's 0
  plays (the voice layer's `start`, less its `trim.in`; default 0), so a word at 2.45 s in the
  transcript keys at `start` + 2.45 s on the scene clock; `audio` the id of the scene's audio layer carrying the
  voice: it sets `start` (do not pass both), and the voice's pauses are measured so the mouth closes in them;
  `silences` spans in transcript seconds that replace that measurement; `analysisJob` the job id a refusal names
  when that measurement is still running, passed verbatim to read it instead of starting another; `end` the scene second where keying stops;
  `speaker` picks one singer's segments, `gain` scales the opening.
- Replacement drawings: pass `mouthShapes` mapping each drawing's name to its number on a `mouth`
  dial (`{"rest": 0, "aa": 1, "oh": 2}`) and a `mouth` track of `step` keys, one drawing per frame,
  joins the others. A viseme without a drawing takes its nearest one.
- "Make this character say the line" is `lipSync:visemes` on the rig. "Make this photo talk" is not: that
  is a pixel video from the Picsart lip-sync models (`kling-avatar`, `heygen-talking-photo`,
  `minimax-h3-max-lip-sync`, `bytedance-omnihuman-v1.5`), not editable animation.
- Use `lipSync:visemes` on the rig to make the character say the line.
- A blink is in fast (~0.08 s), held closed (~0.06 s), out slower (~0.12 s), and keeps the face's
  other targets running.
- Talking while smiling = `happy` steady + visemes cycling + a corrective per viseme that dents or
  pinches under the smile (`happyAa`, `happyOh`). Shape each viseme on the mouth as it is seen, the
  held mood applied, then render every viseme at full weight with the mood on: a dent, a flat lip
  or a pinched corner there is a missing corrective. The mouth and eyes sit before the head in
  `items` so they paint on top.
- Draw the mouth with a darker `stroke` over its `fill`, `"lineJoin": "round"`: the lip line reads at every
  opening, and the round join softens the corners. The stroke follows the morphed outline.
- End a grin in the silence: when a smile control opens the mouth (rig-humanoid's `happy` does past
  about 0.6), ease it after the last word over ~0.12 s to where it rests closed. Check that every silent frame reads closed.
- Keep a head turn moderate: talking to camera reads at about half the turn's range, and the full turn
  only where the body itself is turned that far. An ear slides round the head with the turn and never
  fades; hair trails the head by a couple of frames.
- A wave lifts the hand up and forward at shoulder height, clear of the face outline: a forearm bent
  across the cheek reads as a reach. Measure the clearance from geometry on every frame of the gesture.

## 8. Scene-to-scene morph transitions

- Three ways: direct (A's outline becomes B's, every frame honest); fast swap (the outline swaps
  under `motionBlur: true` and a large move or spin, the eye fills in); hybrid (the key object
  morphs directly, the rest leaves under a `mask` or slides out, new details enter last).
- Pick 1–3 key pairs that share two of colour, shape, volume. Morph those first; if they do not
  read, nothing else will.
- Order: key pairs → the largest, least-detailed objects → small details last; the morphing layer
  spans the cut (its `start`/`duration` cover both scenes), it belongs to neither scene.
- Every moving element shares one direction and speed across the cut; colour changes ride on the
  fill's keyframes timed with the outline's.
- Verify with `picsart_scene_contact_sheet` stills at the cut ±2 frames and `picsart_media_track_motion` on the key pair.

## 9. When not to morph

- No two of colour/shape/volume in common → cut, dissolve or a catalog transition.
- Raster media and text are not outlines; a `media` or `text` layer does not morph — bend it over an
  art mesh (§10), or mask, scale or transition it.
- Topology changes (open↔closed, a hole appears, a shape splits) → `step` swap or a dissolve.
- Under ~0.2 s, or more than a few dozen vertices → a swap reads the same and is cheaper to author.

## 10. Bending a picture and live pins

A layer's `mesh` draws a `media`, `text`, composition or `scene_ref` picture over triangles so it
bends: a `grid`, explicit `vertices` + `triangles`, or a mesh that follows a cut-out's transparency
from `picsart_scene_apply_preset` with `preset` `mesh:auto`; then `deformers` (`bend`, `push`, `stretch`, `warp`, `skin`, `pins`)
move its points over time, each fading in and out on its `mix`. `pins` give free handles to a flag,
tail, ear or sticker corner, with `stiffnessRegions` to keep a head firm on a bending body. Read
[references/art-mesh.md](art-mesh.md) before writing a mesh, and
[references/live-pins.md](live-pins.md) before writing pins. See also [traced SVG](traced-svg.md) and [follow-through, pixel art](layer-follow-through.md).

## 11. Explicit skin weights

When a limb, sleeve or imported mesh should follow painted bone influences instead of the automatic
radius falloff, give the `skin` deformer `weights`, one row per mesh vertex or outline point. Read
[references/skin-weights.md](skin-weights.md) before writing them: the rest-pose
alignment, the row numbering, the blend band a bend needs, and the limits.
