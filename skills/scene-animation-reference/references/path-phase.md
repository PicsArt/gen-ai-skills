# An editable path driven by shared phase

Use this when geometry should remain editable tangent keyframes but progress must
come from a separate phase control: circulating cards, offset followers, scrubbed
paths or a shared nonlinear pace. Ordinary timed movement needs only keyframes.
This is position sampling, not shape morphing or a text baseline.

`ctx:sampleBase(seconds)` samples the **current property's pre-Lua stream**:
constant/keyframes plus ordered composition stages, preserving easing, spatial
tangents and colour blend space. It never reruns that expression or mutates
`time`, `value`, other properties or media playback. It is not another layer's
arbitrary time-sampled final value, final-property history, or a normalized-distance getter.

Use `timeMode:"layer"` for an explicit domain. Sampling accepts layer-local
seconds after keyframe clock conversion; composition-time keys are shifted by
the layer start first. Negative and beyond-last times hold endpoints. Only finite
numbers in [-1000000,1000000] are accepted; strings, nil, not-a-number values and infinity fail
the frame. scene time rounds to 1/120 second. A path authored over 0..100 seconds
gives finer **phase** steps than one over 0..1; the animation still plays for the
layer's real duration. This does not provide arbitrary sub-frame precision.

## One editable phase, curved geometry

This complete scene uses a hidden rotation channel as a scalar phase carrier;
its numeric value is deliberately 0..1, not an angle used for drawing. Replace
its track to change pace. Keep phase and follower starts aligned in one authored
composition: sibling value reads use the caller's local clock. For delayed use,
move the containing scene reference, not the individual driver or follower.

```json
{
  "version":"1.0",
  "composition":{"width":800,"height":600,"duration":6,"fps":30},
  "layers":[
    {"id":"background","transform":{"position":[400,300]},"content":{"kind":"color","color":"#ffffff","size":[800,600]}},
    {"id":"phase","transform":{"opacity":0},"content":{"kind":"color","color":"#00000000","size":[1,1]},"animations":{"rotation":{"keyframes":[{"time":0,"value":0,"easing":"ease_in_out"},{"time":4,"value":1}]}}},
    {"id":"card","timeMode":"layer","content":{"kind":"color","color":"#ee6644","size":[40,20]},"animations":{"position":{"keyframes":[{"time":0,"value":[200,300],"outTangent":[0,-200],"easing":"linear"},{"time":100,"value":[600,300],"inTangent":[0,-200]}],"expression":"local q = ctx.composition:getLayer('phase'):getPlacement():rotation()\nreturn ctx:sampleBase(math.max(0, math.min(1, q)) * 100)"}}}
  ]
}
```

The symmetric cubic's midpoint is independently [400,150]. The phase is .5 at
two seconds, regardless of the long geometry-key domain. For multiple cards,
sample the sum of phase and the card's slot offset on each one's keyframed path; expose the shared key
list as a template parameter rather than authoring different geometry by hand.
Choose offsets from count, e.g. `index/count`, not a fixed twelve-card assumption.
Replace color content with media using a suitable sized wrapper; do not animate
source time, trim or speed to control spatial phase.

- **Open, one-shot path:** clamp phase to [0,1], as above.
- **Closed loop:** wrap the sum of phase and the card's slot offset modulo 1 only when endpoints join.
- **Open conveyor:** wrapping jumps from end to start; fade the owner around both
  ends using the same phase. Check that the jump happens while hidden. Do not
  suppress every motion finding just because one wrap is intentional.
- **Heading:** bind rotation to `positionDirection()` when it should follow actual
  travel. Reversal changes heading; zero motion has no inferred travel direction.
- **Arc speed:** spatial interpolation follows arc length within each
  segment. Equal time per segment is not equal speed across unequal-length
  segments; allocate key times proportional to measured lengths when needed.
  Keep geometry keys linear if the separate phase should own all pacing.

## Validate intent, not merely syntax

Strictly validate the scene with `picsart_scene_validate`, then query 0, 2, 4 and 5
seconds with `picsart_scene_query_layout`. Expect centers [200,300], [400,150], [600,300],
[600,300]. Discover new IDs/root times after nesting or detaching.

The following contract records expected midpoint geometry. Run it against the scene above with `picsart_scene_check_contracts` and read each contract's pass, fail or inconclusive verdict:

```json
{"version":1,"timeSpace":"root","contracts":[{"id":"midpoint-x","window":{"start":2,"end":2.001,"step":0.01},"assert":{"kind":"motion_range","target":{"id":"card"},"channel":"centerX","min":399.9,"max":400.1}},{"id":"midpoint-y","window":{"start":2,"end":2.001,"step":0.01},"assert":{"kind":"motion_range","target":{"id":"card"},"channel":"centerY","min":149.9,"max":150.1}}]}
```

The following motion record requires rightward travel on every output frame around the midpoint. Pass it as `motion` to `picsart_scene_check_motion` and read its status, without claiming arbitrary-time proof:

```json
{"version":1,"timeSpace":"root","fps":30,"window":{"start":1.5,"end":2.5},"checks":[{"id":"rightward","kind":"velocity_range","target":{"id":"card"},"channel":"centerX","min":1,"max":1000}]}
```

The following illustrative pixel record describes expected orange paint at the midpoint. Pixel records have no automated checker; inspect a full-resolution rendered frame, report the visual observation, and keep numerical pixel thresholds unverified:

```json
{"version":1,"times":[2],"checks":[{"id":"midpoint-ink","kind":"ink_presence","region":[370,120,60,60],"foreground":[238,102,68],"background":[255,255,255],"colorTolerance":16,"minPixels":700,"maxFillFraction":0.7}]}
```

All three should pass. Freeze the phase at zero: midpoint geometry and rightward
motion must fail unchanged. Restore phase and remove both tangents: the Y
contract and ink check must fail. Repair and rerun the original checks, not wider
bounds. These acceptance cases concern this fixture, not arbitrary caller edits.

Also hold phase at .5 while advancing playback: path placement must stay fixed
and other animation/media must continue. Change phase at one fixed timestamp:
placement must change. Repeat with changed handles, offsets/counts, a delayed and
retimed reference, and nonmonotonic seeks. Run `picsart_scene_lint_layout`, inspect rendered
extrema/wraps and watch playback. Choose new intent bounds after intentional
geometry edits; a motion-range check alone does not establish path membership,
phase attachment or acceptable pixels throughout the video.
