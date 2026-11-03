# Open-path carousel: editable curve, independent media

Use `scene://open-path-media-carousel` for photos, videos or compositions traveling
along an open curve. It is an independent scene adaptation, not imported HTML or
an exact visual copy. Describe it before binding. `cards` accepts any count of
`{content,width,height}` records; zero draws the background, one still travels.
For video content specify `assetType:"video"` and enough source duration. The box
controls fitting; inspect cropping. Audio and clip-level transforms are not forwarded.

Two inputs deliberately separate geometry from timing:

- `pathKeys` contains position keyframes from 0 to 100 seconds, at least two, with
  spatial `inTangent`/`outTangent` offsets. A phase of 0.5 samples at 50. The curve
  need not finish within the visible scene duration. Segment time allocation controls
  pace: equal times on unequal segments do not make globally equal-speed travel.
  Its declared `keyframes` list constraint rejects malformed samples, wrong domain
  endpoints, and times that coincide at 120 Hz evaluation precision before accepting
  a binding. This is checked even with zero cards. It does not certify the visual curve.
- `phase` is an animation map: its `rotation` track carries **turns**, not degrees.
  Use it to hold, reverse, ease or loop. One authoring input is instantiated in each
  scoped card; it does not retime the card's video or nested content. Do not independently
  start the internal phase and card layers: delay or retime their containing reference.

`initialPhase` and `spacing` place the slots. `edgeFade` fades near both ends; the
exact wrapped phase is transparent. A wrapped position jumps from end to start:
that jump is intentional only while paint is hidden. Check opacity at the seam,
and motion within each continuous travel interval, not a global no-jump claim.
At high speed a narrow fade may pass between output frames; inspect whole playback.

`globalScale`, `scaleDepth`, `scaleMin` and `depthAngleDeg` control 2D depth scale,
not depth sorting. `depthAngleDeg` and `rotationFollow` accept numbers or dynamic
tracks. Heading follows actual velocity, not always the curve's forward tangent:
it flips on reverse travel and returns to the base angle when stationary. Numerical
direction estimates and base sampling use the 120 Hz time grid; extremely slow
movement can quantize to a hold. Use upright cards when stable heading is required
through holds. Later list cards paint on top, unlike the source's first-on-top order.

Entry opacity and scale live on the painted surface, separately from endpoint
opacity on the moving card. Entry starts at `index/count*entryStagger-entryLead` and
lasts `entryDuration`, including any elapsed pre-roll. Long entries may be cut by
the scene duration. Preserve component ownership when editing; don't duplicate
surface placement to make it follow the card.

## Executable controlled check

Apply this request with `picsart_scene_apply_template`; retain the returned scene.
The symmetrical curve has its midpoint at (400,150), independent of the template's
implementation. These checks concern this specific instance, not all parameters.

```json
{"uri":"scene://open-path-media-carousel","mode":"bootstrap","parameters":{"width":800,"height":600,"duration":6,"cards":[{"width":100,"height":60,"content":{"kind":"color","color":"#ee6644ff"}}],"pathKeys":[{"time":0,"value":[200,300],"outTangent":[0,-200],"easing":"linear"},{"time":100,"value":[600,300],"inTangent":[0,-200]}],"phase":{"rotation":{"keyframes":[{"time":0,"value":0,"easing":"linear"},{"time":4,"value":1}],"expression":"return ctx:loopOut('offset')"}},"globalScale":1,"scaleDepth":0,"edgeFade":0.1}}
```

Run strict `picsart_scene_validate`, then `picsart_scene_query_layout` at 0, 1, 2, 3.8, 4 and 4.2.
Structural validation alone does not evaluate every expression: query custom paths
before rendering. Invalid path bindings are refused by `picsart_scene_apply_template`,
not deferred to evaluation. For the example, `unit_0__card` owns
path placement and endpoint opacity; `unit_0__card__surface_0` owns entry paint.
Query actual IDs after nesting, inline insertion or detaching; preserve composition
scopes that expression lookups depend on.

The following contract specifies midpoint position and a transparent seam. Run it with `picsart_scene_check_contracts`, and also check effective opacity near the initial entry. Geometric visibility alone does not prove painted visibility:

```json
{"version":1,"timeSpace":"root","contracts":[{"id":"arch-midpoint","window":{"start":2,"end":2.001,"step":0.01},"assert":{"kind":"motion_range","target":{"id":"unit_0__card"},"channel":"centerY","min":149.9,"max":150.1}},{"id":"hidden-wrap","window":{"start":4,"end":4.001,"step":0.01},"assert":{"kind":"motion_range","target":{"id":"unit_0__card"},"channel":"effectiveOpacity","min":0,"max":0.001}}]}
```

The following motion record requires rightward travel only within a continuous interval, excluding its invisible reset. Run it with `picsart_scene_check_motion`; it establishes only the frames in its window:

```json
{"version":1,"timeSpace":"root","fps":30,"window":{"start":1,"end":1.5},"checks":[{"id":"moves-right","kind":"velocity_range","target":{"id":"unit_0__card"},"channel":"centerX","min":100,"max":150}]}
```

The following illustrative pixel record specifies red paint at the midpoint with background margins. Pixel records have no automated checker; inspect a full-resolution frame and leave the numerical pixel assertion unchecked. This does not establish aesthetic quality:

```json
{"version":1,"times":[2],"checks":[{"id":"midpoint-red","kind":"ink_presence","region":[340,110,120,80],"foreground":[238,102,68],"background":[237,237,239],"colorTolerance":16,"minPixels":5800,"maxFillFraction":0.7}]}
```

Negative controls: remove both spatial tangents (midpoint must fail), replace phase
with `return -time/4` (rightward motion must fail), or change red to the background
color (pixel presence must fail). Restore the original and rerun **unchanged** checks.
Never widen tolerances to make a wrong curve pass.

After changing cards, curves, phase or hosts, rebase targets, expected bounds, root
times and pixel regions. Run `picsart_scene_lint_layout` over entry, extrema and seams; off-canvas
travel and designed overlap need explicit interpretation. Render seam-adjacent frames
and inspect video for abrupt headings or flashes. To check independent media time,
hold phase and compare the same visible video card at two times: its box must remain
fixed while footage advances. A moving box is not evidence of advancing video.
Report sampled geometry, pixel checks and continuous playback review separately.
