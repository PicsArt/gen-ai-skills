# Validation by motion pattern

## Contents

- Acceptance card and execution
- What the assertions actually establish
- Patterns: measurable outcome and visual gate
- UI beats
- Mechanics shared by these patterns
- Executable contract example: one intended resting edge

Use this alongside the selected construction, not after deciding the scene is finished. All tools
below accept scene; evaluate the document through the tools' default path.
This is independently authored scene guidance, not imported Hyperframes implementation.

## Acceptance card and execution

1. Declare intent, targets/scopes, root-clock events, independent expected values, units, tolerances and sampling before checking.
2. Validate with `picsart_scene_validate`, then resolve evaluated ids/scopes using `picsart_scene_query_layout`. Authored edit addresses are not evaluated query scopes. Include intended descendants, not only their owner.
3. Use supported `picsart_scene_lint_layout` relationships and explicit query comparisons for other measurable requirements. Run contract records with `picsart_scene_check_contracts` and frame-complete motion records with `picsart_scene_check_motion`. A successful call is not a semantic motion verdict.
4. Inspect full-resolution `picsart_scene_contact_sheet` with `resolution` set to the composition dimensions, images and continuous video, recording observations rather than only artifact URLs.
5. Report measured, visually inspected and unchecked evidence with revision, arguments, targets, times and tolerances. Repair the authoring and rerun affected windows; never relax limits or copy broken observations into expectations.

### Sampling notation used below

`A` = action start, `B` = landing/end of motion, `H` = end of intended hold, `E` = shared event,
`d = 1 / output fps`. All checks use **root seconds**. Map nested/local/layer-window events into
root time first. An expression's `time` is layer-local seconds, zero at its layer's start,
not root or composition time. In nested scenes, map through the reference's timeline before
subtracting the child's start. For example, with no trim/speed change, a reference starting at
root 1s and a child starting at local 0.5s give the child's expression `time = 0` at root 1.5s.

For each moving interval, sample a frame-spaced grid plus exact event times and known extrema.
At a seam inspect `E-d, E, E+d` within scene bounds. Refine around closest approaches, peaks,
and fast changes. Sampling is not continuous-time proof. Contract and lint windows exclude their
end: add a separate boundary/query for `B` or `H` when needed. At the scene's exclusive end,
inspect its final visible frame instead. Stay within 64 contracts / 1000 unique contract samples
per call (lint caps at 600 samples); split long scenes into named beats and summarize each.
Preview at most 8 `times` per `picsart_scene_contact_sheet` call; set `resolution` to the composition dimensions for small details.

## What the assertions actually establish

| Relationship assertion (`picsart_scene_check_contracts`) | Use and limit |
|---|---|
| `present` | Required on-canvas geometric presence; not visible paint, opacity, mask coverage, or readability. |
| `co_presence` | Members appear/disappear together, with at least one joint-present sample. Joint absence elsewhere is allowed. |
| `translation` | Fixed size/rotation and relative offsets against an anchor, learned at the initial joint sample. Both can drift wrongly together; not absolute stillness or a scale/rotation grouping test. |
| `contains` | Member geometry inside anchor with declared padding at joint-active samples. Add `present` where disappearance must fail. Not painted clipping. |
| `opacity_match` | Equal evaluated effective opacity, not an absolute opacity target or proof that a fade happened: two zeroes match. |
| `fixed_edge` | Edge stays at declared root-pixel `valuePx`. Four edges can constrain an unrotated rest box; one edge alone allows resizing. |
| `edge_attachment` | Member edge follows anchor edge with declared pixel gap; useful during resize. Does not automatically resize or reflow content. |
| `handoff` | Geometry matches between explicitly chosen outgoing/incoming moments. Not identity, velocity continuity, paint equivalence, or proof of no gap between those moments. |
| `motion_range` | A selected subject's evaluated scalar stays within declared inclusive `min`/`max`. Channels: root-pixel `centerX`, `centerY`, `width`, `height`; reported `rotationDeg`; `effectiveOpacity` in [0,1]. Available off-canvas boxes are allowed; box channels require unrotated, nondegenerate geometry. Missing evidence is inconclusive. Not authored scale, velocity, accumulated turns, or painted alpha. |

The assertion vocabulary records intent; run it with `picsart_scene_check_contracts` and read pass, fail or inconclusive per contract. Do not invent assertions or treat missing targets as evidence of a pass. Contract checks and explicit query comparisons do not inspect masks, blur or stroke paint, and painted motion in exported video is not tracked automatically; those require rendered evidence.

### Absolute motion checks without ad hoc calculations

The `motion_range` assertion describes a numeric acceptance band, scheduled by a `window` or `boundary`:
`assert: {kind:"motion_range",target:{id:"card"},channel:"width",min:99,max:101}`.
This example expects a designed 100px width within ±1px, not a scale value of 1. For settling,
start the window at the declared deadline and continue through the intended hold. For stillness,
constrain both centers, both dimensions, and rotation as required; one channel cannot certify a
whole pose. Use separate pre-event and post-event opacity ranges to detect a fade that never ran.
For a pulse/overshoot, constrain the allowed envelope through the action and the tighter rest range
through its tail; an envelope alone does not prove a peak occurred. Event-centered narrow ranges
can check planned peak/landing values. Choose sampling to include the actual extrema.

Read `motion.observedMin`, `motion.observedMax`, `motion.maxError`, `motion.unit` and the verdict.
Extrema are null when no value was measured. Failure evidence includes `actual`, `min`, `max`,
and `unit`; `maxErrorPx` is not the degrees/opacity score. Limits include their endpoints and have
no extra hidden tolerance: put the accepted band into min/max. A tiny numeric range may pass a
still-moving subject; range compliance does not establish zero velocity or mathematical rest.
Rotation is the query's reported angle, not unwrapped accumulated turns; use visual review at wraps.

## Patterns: measurable outcome and visual gate

For absolute center, size, rotation and opacity, declare independent expected bands at relevant events. For motion, compare every relevant output frame if claiming frame-complete evidence; value, signed velocity and acceleration use different units. Run those with `picsart_scene_check_motion` at the export FPS. Read `scene-animation-reference` and its frame-motion reference for thresholds and limits; record samples not examined as unchecked.

Apply these checks to the rows below where the query measures the intended quantity:

- Slides, cascades, scrolling and parallax: signed per-axis velocity limits catch wrong-direction
  travel; value bands constrain corridors and destinations. Each plane can have its own rate band.
- Pops, springs, presses and nudges: value bands constrain excursion; a separate tail window needs
  both rest-pose and near-zero velocity limits. Check intentionally still siblings separately.
- Ambient motion and arcs: value/rate/acceleration limits constrain the permitted envelope and
  abrupt changes, not exact path shape, period, damping or perceived quality.
- Fades and resizes: constrain opacity or size and their rates; retain relationship checks for
  companions, fixed edges, padding and attachments. Painted clipping/alpha remains a visual gate.
- Shared-element seams: include adjacent frame intervals across the seam on the same target;
  use handoff contracts for distinct outgoing/incoming targets. Rates do not establish identity.

Remaining relative-speed ratios, damping envelopes, exact trajectories and clearance comparisons
need explicit query comparisons against the acceptance card. Spin rates use shortest angular
steps; they cannot prove turn counts. No frame-complete pass proves sub-frame behavior, shutter
samples, or pixel quality. Keep the rendered checks in every applicable row.

| Motion/concept | Samples and numerical acceptance | Inspect rendered frames and playback |
|---|---|---|
| Fade entrance/exit | The `motion_range` assertion measures `effectiveOpacity` at pre-event, intermediate and final/hold phases, with distinct intended bands. Use `opacity_match` only for subjects intended to fade together. | Paint appears/disappears without unwanted motion; no child or shadow left behind. Bounds alone cannot establish a fade. |
| Slide entrance/exit | Query start, midpoint, landing and hold plus frame grid; compare direction, displacement and final box to intended layout. Test actual exit against edited layer end. | No unintended cut-off, drift, lingering contents, or unreadably short hold. |
| Zoom entrance/exit | Compare sizes and intended pivot location through `[A,B]`; use verbose transforms for a noncentral pivot. | Growth/shrinkage stays anchored; text and backing transform together. A box center may move legitimately around an off-center pivot. |
| Spin | Compare sampled rotation, size and pivot with intended turn and scale; sample more than endpoints (a full revolution can share endpoint pose). | Direction, turn count and perspective/readability; conservative boxes are not painted silhouettes. |
| Pop / single overshoot | Query peak candidates, neighboring frames, `B`, and `[B,H]`; compare maximum size/displacement, rest box and chosen settling tolerance. | Peak is appropriate to the leader, and landing does not look like a second accidental beat. Bézier control values are not measured overshoot. |
| Damped spring | Sample alternating extrema and tail through `H`; the `motion_range` assertion describes an allowed action envelope and tighter designed rest band after the settle deadline. Compare decreasing peak envelope explicitly. Use box ratios only with suitable fixed underlying geometry. | No visible tail chatter or cutoff. A passing tail range is not a spring/velocity assertion; finite samples do not prove mathematical rest. |
| Float / sway / shake / pulse | Sample several periods and extrema; compare amplitude, period, mean pose and any ramp-in/out against intent. Check support that should remain still separately. | Ambient motion stays subordinate and loops without a jump. Passing amplitude limits does not prove attention hierarchy. |
| Glow pulse | Query geometry to catch unintended movement; validate effect compatibility. Pose cannot measure brightness or glow extent. | Inspect low/high glow and repeated cycles, clipping and whether the glow overwhelms text. |
| Ken Burns | Compare visible image features/crops at start/mid/end; viewport bounds may intentionally stay constant. Rendered tracking is optional for visible pose. | Image coverage, focal subject and clipping stay correct throughout the pan/zoom. Fixed frame geometry is not proof of internal motion. |
| Curved path / arc | Query departure, bow/extrema, arrival and dense closest approach to obstacles. Compare intended travel and box clearance. Lint is supplementary: inspect all pair classifications, not only collision findings. | No painted collision or unreadable depth crossing. Lint can classify an overlap as transient/contained/allowed; no findings is not strict avoidance. No swept-path or continuous-clearance proof. |
| Layered entrance + ambient | Query entrance's landing and a full later ambient cycle; compare the intended final baseline and loop envelope. | Entrance resolves while ambient continues; transform order does not create unexpected orbit/drift. |
| Whole-beat register | Query each role's onset, landing, and hold; compare intended ordering and declared quiet intervals. | One leader at a time, enough reading time, support does not steal attention. No semantic hierarchy assertion exists. |
| Row stagger / cascade | Check every item's start/mid/landing, frame grid, and hold after the last landing. Compare declared onset offsets and final row/grid; query effective opacity too. | Correct reading order and sufficient last-item hold. Copied easing or correct timestamps alone do not establish rhythm. |
| Leader-only directional nudge | Sample anticipation/action extrema, return and hold; check leader event ranges and siblings' designed center/size/rotation bands with `motion_range`. Four `fixed_edge` checks per unrotated sibling remain an alternative for its box. | Only intended leader moves; no accidental group recoil. Never anchor sibling `translation` to the moving leader; sibling-to-sibling translation alone permits joint drift. |
| Persistent shared element | Check `present` through all required beats and both sides of seams; compare intended pose, size and opacity. Inspect authored identity/lifetime separately. | Same visual carrier persists without blink or duplicate; geometry presence cannot establish identity. See `picsart_scene_recipe motion-scene-continuity`. |
| Direction-matched seam | Sample both sides, midpoint and overlap window; compare incoming/outgoing displacement directions and declared handoff boxes when applicable. | No direction reversal, blank flash, unintentional double image, or velocity kick. Handoff geometry alone cannot certify smoothness. |
| Causal handoff | At approach, `E-d,E,E+d`, response peak/landing and hold, compare leader arrival and dependent onset to declared event order. Query rest state before `E` to detect premature response. | Action causes response at viewing speed; numerical simultaneity may still read ambiguously. No causality assertion exists. |
| Depth / parallax | Query each plane at start, quarters and end; compare displacement ratios, directions and any fixed y/size/rotation. Do not use rigid `translation` between intentionally different-speed planes. | Perceived depth, correct stacking, no exposed holes. Correct speed ratios alone do not prove depth. |
| Parent/group motion | Check whole visible family: `translation` for rigid translation only, `co_presence` for shared lifetime, `opacity_match` for intended shared fade. Query scale/rotation changes explicitly instead of forcing translation. | Background, contents, decoration and shadows remain one widget. `parentId` is transform parenting, not an opacity/lifetime guarantee; empty rig presence is not child paint. |
| Adaptive container / resize | Use `fixed_edge` for stationary edges, `edge_attachment` for following edges/gaps, `contains` plus required `present` for contents throughout resize and hold. | Text reflow, clipping and padding stay legible. Contracts detect broken relationships; they do not perform layout. See `picsart_scene_recipe linked-element-motion`. |
| Focus pull / blur | Validate compatible content/effect and window; inspect at `A`, quarters, `B` and hold. Layout bounds cannot quantify blur or sharpness. | Intended soft-to-sharp (or reverse) progression, no clipped halo, correct final focus. |
| Perspective flip | Query pose where meaningful; preview quarters, edge-on moment, landing and adjacent frames. | Correct pivot/axis, believable edge-on passage, orientation and backing; zero-width or conservative bounds cannot establish painted correctness. |
| Wipe / mask reveal | Validate mask/look window and role; render `A`, quarters, `B`, hold, and the final visible frame for an exit. | Edge travels in intended direction, fully reveals/conceals, retains corner clipping. Boxes do not measure mask progress or final coverage. |
| Drawn stroke | Validate trim/path structure; preview unrevealed start, partial progress, completion and hold with a crop. | Stroke begins at intended path end, grows continuously and finishes fully; layout boxes do not measure revealed length. |

## UI beats

| Beat | Numerical acceptance and schedule | Visual gate |
|---|---|---|
| Scroll | Check fixed viewport and any query-visible inner content at each flick's start, travel, stop and hold. Compare intended travel and bounce bounds, with root-time mapping. If inner motion is not query-visible, render/track features; do not claim box proof. | Clipping, readable stops, no blank overscroll, and continuous nested animation. |
| Snapped carousel | As for scroll; compare each settled content offset to its intended page multiple and inspect each final page. | Correct page, no half-page stop or wrong-direction bounce. |
| Button press | Scope whole widget, not label. Query pre-event rest, compression minimum, rebound maximum, return and hold; compare declared rest size and scale envelope. Inspect children too. | One coherent press, intended pivot, no detached label. Historical sample widths are not a universal oracle. |
| Pointer → press → result | Check approach, `E-d,E,E+d`, feedback extrema, result landing/hold. Compare transformed pointer **hotspot**, not bounding-box center, to intended target (verbose query matrices if needed). Require button rest and hidden/offscreen result before event using appropriate geometry/opacity comparisons. | Pointer settles, feedback starts after arrival, result becomes leader. No hit-test/causality assertion; geometry presence cannot establish hidden paint. |
| Drag → release → departure | Establish hotspot/grip alignment and intended absolute travel; use `translation` only during fixed-size/rotation carry. Query interior travel, release neighbors and departure. After release, use designed payload pose bands with `motion_range` and separately require pointer displacement. | Off-center grip stays attached, then releases without a blink, duplicate or payload following the pointer away. For rotating/resizing grips compare transformed points, not constant box offsets. See `app-ui-animation` → `references/drag-and-sync.md`. |
| Control → synchronized result | Query pre-event, interior progress, landing and hold in root time, including a delayed instance. Explicitly compare each channel's normalized progress to the other and the designed schedule; use absolute bands for zero-delta channels. For discrete edits inspect both sides of each state boundary. | Both sides change together and land on the intended value; inspect readout text separately. Equal endpoints do not prove equal easing, box geometry does not verify text, and no generic progress-equality assertion exists. See the UI drag/sync reference. |
| Bottom sheet + dim | Query rise and landing; `fixed_edge` bottom at its designed position during final hold (canvas height for a flush sheet, beyond it for a backing extended to hide lower rounded corners), `contains` for contents and `present` only when intended on-canvas. Compare dim's effective opacity separately. | Dim covers underlying UI, rounded corners/occlusion correct, sheet stops as designed, no leaked content. Do not equate dim/backing opacity unless that is the actual intent. |

## Mechanics shared by these patterns

For pointer-hotspot checks, do not guess a verbose matrix's storage/multiplication convention.
Use a documented convention, or author a wrapper whose known center is the hotspot and query
that point; otherwise inspect the hotspot in rendered pixels and label the numerical check unchecked.

| Mechanism | How to check |
|---|---|
| Placement, anchor, ordered transforms | Query baseline and transformed states with `verbose:true`; compare intended pivot and boxes in root coordinates. Inspect rendered family. A correct local keyframe is not evidence of correct combined transforms. |
| Easing | Query interior fractions and extrema, not only endpoints; compare displacement against intended progress. Watch acceleration/landing. There is no semantic easing-quality assertion. |
| Expressions and local clocks | Query the same root time repeatedly for deterministic expectations, plus mapped start, extrema and hold; test a delayed/nested instance. Expression `time` starts at zero at the layer's start; map that clock to root-time checks, separately from keyframe `timeMode`. Validate expression acceptance and inspect rendered output. |
| Text animation/selectors | Validate preset parameters; preview first/last glyph, intermediate reveal, final text and hold. Whole-text bounds cannot establish glyph order, per-glyph timing, visibility or readability. |
| Motion blur | Validate settings; inspect fast travel and rest with full-quality crops. Geometry and pose tracking do not measure shutter smear quality; check clipping, ghosting and sharp rest. |
| Transition definitions | Validate structure; query explicit geometric relationships where applicable, then inspect window quarters and both sides of seam in sequence. Paint coverage, masks and velocity continuity need their own observations, not merely valid `between`/duration. |

## Executable contract example: one intended resting edge

This sidecar expresses one intended edge: a uniquely scoped `panel` top at 40 root pixels during `[0,2.1)`. Run it with `picsart_scene_check_contracts` (or as a fixed-edge relationship in `picsart_scene_lint_layout`) and read its verdict, but one edge does not establish a stationary panel or visual quality:

```json
{
  "version": 1,
  "timeSpace": "root",
  "contracts": [{
    "id": "panel-top",
    "window": { "start": 0, "end": 2.1, "step": 0.25 },
    "assert": {
      "kind": "fixed_edge",
      "members": [{ "id": "panel" }],
      "edge": "top",
      "valuePx": 40,
      "tolerancePx": 1
    }
  }]
}
```

Rebind scopes, independent values and schedules before reuse. Coarse sampling can suit a constant edge but miss a fast nudge. Pair opposing edges on both axes for an unrotated rest box and require presence where absence must fail. Read `linked-element-motion` for construction and evidence limits; unsupported or unexecuted sidecar checks remain unchecked.