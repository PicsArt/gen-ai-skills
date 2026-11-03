# Drag and synchronized controls

Use for an authored demonstration, not a live pointer-event system. These are independently
authored scene constructions informed by reusable motion concepts, not adopted HyperFrames
implementations. Choose event times and tolerances for the actual design.

## Carry, release, then leave

Declare approach, grab, carried travel, release, optional snap/settle and pointer departure as
separate phases. Name the pointer's **hotspot** and the payload's **grip point**; neither is
necessarily its bounding-box center. Keep the payload's backing, text and decoration as one
semantic unit. Prefer one persistent payload when its identity should survive the drop.

For a fixed-size, unrotated payload in root coordinates, let `g` be the grip offset from its
center, and `h(t)` the pointer hotspot. During the held phase require `center(t) = h(t) - g`.
For example, a grip 24px right and 10px above center means `g = [24,-10]`; a hotspot at
`[180,120]` requires center `[156,130]`. This is illustrative geometry, not a scene JSON fragment.
Use a known hotspot-centered wrapper or documented query transforms; do not guess matrix order.

Two editable constructions are possible:

- Bake matched position tracks from one path/progress schedule, with the grip offset applied.
  Match times, easing and path shape, not just endpoints. Split the tracks after release: the
  payload holds or follows its own snap track while the pointer departs.
- Use a shared transform owner for the carried phase, then keep that owner still and animate
  the pointer's own local departure. `parentId` is static transform ownership, not an animated
  attachment switch, shared opacity or inherited lifetime. A common moving owner across all
  phases can accidentally carry the dropped payload away again.

If scale/rotation changes during the hold, the grip offset changes in root space; transform the
local grip point and check it, or postpone that change until release. A fixed-offset translation
assertion is not a rotating-grip assertion. If a duplicate ghost is genuinely required, author its
lifetime and paint switch explicitly; inspect release for a blink or double object. Do not add a
ghost merely because another implementation used one.

**Validation:** run `picsart_scene_validate`; resolve painted targets with `picsart_scene_query_layout`.
During fixed-size/rotation carry, `translation` can check constant relative offset, but establish
the correct initial grip separately: the assertion learns its initial relationship. Check intended
absolute travel too; two stationary subjects can pass translation. At release and neighboring
frames, inspect alignment and paint. After release, constrain the payload's intended center/size/
rotation with `motion_range` and check that the pointer actually departs. Do not extend the carried
translation contract through the independent departure. Inspect both families, not only a rig.

## A control and its result share progress

Define one event interval and one normalized progress function `p(t)` (including easing). Map it
into each output's range: `x = x0 + (x1-x0)*p`, `width = w0 + (w1-w0)*p`, or another supported
channel. Matching duration without matching easing can agree at the ends and disagree throughout
the gesture. Shared progress is an authoring source of truth: bake ordinary keyframed tracks or use
supported expressions. Do not invent a reactive binding field or a new validator assertion.

Keep the control and result visible together when simultaneous comparison is the point. Preserve
label legibility; scaling a whole widget and resizing only its backing are different intentions.
Route adaptive content/reflow to `linked-element-motion`.

Map all event times into each layer's clock. Expression `time` starts at zero at that layer's
start; it is independent of keyframe `timeMode`. A delayed control and root-start target must not
blindly receive the same expression. Test delayed or nested instances at the same root times.

For discrete selections, define one table of root event times and intended control/target states,
then author both sides from it using supported tracks or explicit layer windows. Do not assume
text strings accept numeric animation tracks; retrieve the current text schema. If separate label
layers are used, inspect boundary frames for duplicate or missing labels. Text content needs
authored-state and rendered inspection; a box query does not verify a displayed number.

Validation: query interior moments as well as endpoints. For nonzero endpoint deltas, compare `(x-x0)/(x1-x0)` and `(width-w0)/(w1-w0)` against an independent intended progress schedule and tolerance. This requires explicit query comparisons; a zero-delta channel needs an absolute band. Equality in one unit cannot prove agreement between pixels and degrees. Check pre-event rest, extrema, release, hold and boundary neighbors. Absolute bands can run as `motion_range` contracts with `picsart_scene_check_contracts`.

## Acceptance and fault injection

Follow the frame-grid, event-boundary and evidence rules in `motion-pattern-library` →
`references/validation-by-pattern.md`. Contract windows are end-exclusive. Inspect decisive
rendered frames and continuous playback; report the latter unchecked if only stills were inspected.

Before accepting the check, deliberately give the carried payload a different easing, let it follow
the departing pointer, or offset the result's clock. The unchanged expectations should detect the
specific fault. Repair the authored scene, not its expected values. Record scene revision, tool
arguments, times, tolerance, actual results and visual observations; passing samples do not prove
continuous-time attachment or perceived causality.
