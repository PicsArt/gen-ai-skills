# Frame-complete motion validation

Use output-frame evidence when endpoints are insufficient: a card must keep moving right, a reveal must not reverse, a resize must stay within limits, or a spring must settle. `picsart_scene_check_motion` checks every root output-frame timestamp `n / fps` in `[start,end)`; pass the actual export FPS. Manual `picsart_scene_query_layout` observations establish only the sampled channels and times. Sub-frame oscillations, shutter samples and overall painted quality remain unchecked.

## A runnable request

Validate its `scene` with `picsart_scene_validate`, then pass the whole object to `picsart_scene_check_motion`. The linear example should move right at 40 pixels/second with zero acceleration. Choose tolerances independently and verify a deliberately broken variant fails the check. Do not copy extrema from a broken result into the limits.

```json
{
  "scene": {
    "version": "1.0",
    "composition": { "width": 400, "height": 200, "duration": 1, "fps": 20 },
    "layers": [{
      "id": "card",
      "content": { "kind": "color", "color": "#ffffff", "size": [20, 20] },
      "transform": { "position": [100, 100] },
      "animations": { "position": { "expression": "return Vec.v2(100 + time * 40, 100)" } }
    }]
  },
  "motion": {
    "version": 1, "timeSpace": "root", "fps": 20,
    "window": { "start": 0, "end": 0.3 },
    "checks": [
      { "id": "corridor", "target": { "id": "card", "composition": "main" }, "kind": "value_range", "channel": "centerX", "min": 99, "max": 112 },
      { "id": "rightward", "target": { "id": "card" }, "kind": "velocity_range", "channel": "centerX", "min": 39, "max": 41 },
      { "id": "smooth", "target": { "id": "card" }, "kind": "acceleration_range", "channel": "centerX", "min": -10, "max": 10 }
    ]
  }
}
```

A successful call is not a passing motion verdict; read `status`. The `motion` record is distinct from a relationship `contracts` record, which `picsart_scene_check_contracts` runs.

## Choose assertions from intent

| Intent | Checks |
|---|---|
| No reversal | Signed `velocity_range` on the intended axis: a rightward move has a near-zero lower bound, leftward a near-zero upper bound. This is not vector speed. |
| No overshoot / stay in corridor | `value_range` on center or size throughout the move. Add the other axis if needed. A speed limit alone cannot prove the correct destination. |
| No unexpected jump | Bound adjacent-frame velocity; also bound acceleration when changing speed itself must be smooth. Intentional cuts need separate windows. |
| Settled by a deadline | Tail window with both destination `value_range` and near-zero `velocity_range` on each relevant channel. Small acceleration alone accepts constant drift. |
| It must move (a walk, a wave) | `kind: "must_move"` with `channel`, `min` (least peak-to-peak travel, px or deg), `within` (seconds each window spans; at least a full stride, 1 s, for a foot, since a foot is planted half of every stride) and optionally `window` (the span the motion is expected in). The verdict names the failing run as one `not_moving` issue (first and last frame, `actual` = best travel in it): a freeze or a missing wave, with no extrema to read. No `max`. |
| A planted foot skating (a regression alarm, not a delivery gate: over `max` means look at it at 1x, since whether a few px shows depends on focus, how still the surroundings are and the shot size) | `kind: "foot_slip"` with `max` (the alarm level, 4 px) on a `{rig, parts: ["foot"]}` target; no `channel`, `min`, `within` or `window`; optional `floorTolerance` (px, default 3). It reads each foot layer's own point (the ik target), not its drawing, whose centre also moves as the foot rolls heel to toe, and counts a frame planted while the point is within `floorTolerance` of the lowest it gets in the window. Each stance (an unbroken run of planted frames) is reported in `stances` (`start`, `end`, `frames`, `slipPx`, the travel along x); `observedMax` is the worst, and any stance over `max` raises one `outside_range` issue. Give a window that holds whole stances, and a lift of at least 3 px or the whole step reads as one stance. |
| A character's parts | Target `{ "rig": "kid", "parts": ["foot", "hand"] }` instead of layer ids: each layer `kid__<name>` whose name is or ends in a part (`foot` reads `leftFoot` and `rightFoot`, not `leftFootArt`) is its own result. Works with every kind. |
| Resize / fade | Width/height or `effectiveOpacity` value and rate ranges. Opacity is evaluated layer opacity, not painted alpha. |
| Shared widget / phase attachment | Construct shared motion with parenting/composition ownership or a supported binding first. Check cross-layer relations with `picsart_scene_check_contracts`, supported layout lint or explicit query comparisons; scalar rates alone do not establish ownership handoffs. |

Channels: `centerX`, `centerY`, `width`, `height` in root pixels, `rotationDeg` in degrees,
`effectiveOpacity` in [0,1]. `depth` is the eye distance a perspective camera draws the target at, in px
(larger is farther); a target drawn through a perspective camera measures its projected centre
and envelope. Limits are inclusive. Velocity is `(next-current)*fps`, acceleration
is the second difference times `fps²`, centered on the middle frame. Units become px/s, deg/s,
opacity/s or the corresponding per-second-squared unit. These are finite differences, not
instantaneous derivatives. Value checks need one frame, velocity two, acceleration three.

Rate checks use only consecutive frames inside the window, and a window that overruns the
scene is inconclusive, never clipped to pass.

Query geometry is rounded. Use a reasoned measurement allowance, especially at high FPS where
rounding is amplified by FPS or FPS²; do not demand exact zero derivatives from fractional-pixel
motion. Width/height require unrotated, nondegenerate geometry. Centers remain measurable under
rotation. Angular rates use shortest turns across the ±180° wrap; an exact half-turn is
inconclusive. More than 180°/frame or extra revolutions can alias; do not use this to count spins.

## Scope and act on evidence

- Discover evaluated `id` and `composition` using `picsart_scene_query_layout`; repeated nested instances
  need their actual query scope. Authoring IDs and nested local clocks are not root query IDs/times.
- A call supports 1–64 uniquely named checks and 1–1000 frames. Too much work is rejected,
  never silently downsampled. Split long windows with **one overlapping frame for velocity,
  two for acceleration** so intervals across the split remain checked. No cross-call intervals
  are inferred. Include transition/settling seams deliberately; the end timestamp is excluded.
- Read every check's status, extrema, units, measured value/interval counts and `issues`.
  Issues identify frames, times, input values and derived rates. At most 16 issues are retained
  per check, with `omittedIssues`. Repair the scene or a mistaken scope; rerun the same intent.
- Missing/ambiguous targets, unavailable geometry, insufficient frames and windows beyond the
  scene are **inconclusive**, never a clean pass. Missing frames are not bridged into long intervals.
  Measured failures take priority over unknown evidence, so a failing report can also have gaps.
- `coverage.frameGridComplete` means all requested timestamps were queried within the scene,
  not that every channel was measurable. `betweenFramesProven` is always false. Scene/motion
  hashes fingerprint input JSON, not remote asset bytes. Remote scene references are resolved
  once per call; use immutable assets/handles for reproducible runs.

`picsart_scene_lint_layout` pairs root layers (a rig is one layer; `parts: true` adds its limbs). On this server no layer is drawn alone, so overlaps are judged by bounds: a pair whose bounds overlap over drawings that never touch is still reported as a collision, and `edgeCut` stays empty. Read such a finding against a contact sheet before acting on it, and look there for a tail or limb the frame cuts.

Keep `picsart_scene_validate` for structure and `picsart_scene_lint_layout` or `picsart_scene_check_contracts` for sampled relationships. Explicitly compare remaining design requirements with `picsart_scene_query_layout` and record unexecuted checks as unchecked. Render full-resolution frames and watch playback for typography, clipping, occlusion, masks, effects, blur and perceived timing; numerical success is not a pixel-quality guarantee.