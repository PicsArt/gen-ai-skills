# Reuse intent without copying root coordinates and timelines

The same intended relationship can apply to several parameter variants or nested instances. Keep ownership and shared-parameter construction first. Pass the request below with the scene to `picsart_scene_check_contracts`: it resolves the `template` against `targets`, `numbers` and optional `clock`, checks the result, and returns the `resolved` document beside the verdicts. Derive expected values from design, not from observations.

The template has `version:1,timeSpace:"local"` and the same assertion grammar as the checker.
Replace a whole target with `{"$target":"role"}` and a numeric schedule/assertion value with
`{"$number":"name"}`. All bindings must be supplied and used. There is no string interpolation,
expression execution, selector matching or automatic geometry conversion.

This complete resolver request declares a 200-root-pixel surface width during local [0,1),
placed at root 3 seconds and stretched to two root seconds:

```json
{
  "template": {
    "version": 1,
    "timeSpace": "local",
    "contracts": [
      {
        "id": "surface-width",
        "window": { "start": 0, "end": { "$number": "hold" } },
        "assert": {
          "kind": "motion_range",
          "target": { "$target": "surface" },
          "channel": "width",
          "min": { "$number": "width" },
          "max": { "$number": "width" }
        }
      }
    ]
  },
  "targets": { "surface": { "id": "instance__surface", "composition": "instance" } },
  "numbers": { "hold": 1, "width": 200 },
  "clock": { "offset": 3, "scale": 2 }
}
```

Bind actual target IDs and composition scopes from `picsart_scene_query_layout`; the names above are examples,
not selectors. Choose expected values independently from the design and intended host transform.
For example, a 400 px design surface under a uniform 0.5 host scale expects 200 root pixels. Do not
take the measured width as the expected width: that would encode a resizing bug as success.
For a tolerance, bind distinct lower/upper limits instead of expecting exact equality.

Keep the resolver request and the returned `resolved` record together so target, value and clock mappings are reproducible. Resolving a template is not evidence that a target exists or passes a check. Read pass, fail or inconclusive per contract against the actual assembled scene, and preserve unexecuted assertions as unchecked.

## Clock and geometry boundaries

- **root time = offset + scale × local time**; default clock is identity. Scale is positive.
  Window start/end, boundary time and handoff moments map as timestamps; step/delta scale as
  durations. Even the default 0.25-second step scales. Window end remains exclusive.
- A component starting at root 3 with normal speed uses `{offset:3,scale:1}`. A deliberate 2x
  timeline stretch uses scale 2, not playback speed 2. Use the actual supported host time mapping.
- One affine clock does not represent loops, reverse, nonlinear remapping, or arbitrary trimming.
  Split those cases into explicit root-time contracts; do not infer a clock from first/last bounds.
  A cross-component handoff with different clocks also needs explicit root-time moments.
- Assertion numbers stay in the checker's units: root pixels, degrees or opacity. Clock scaling
  does not scale geometry, tolerances or opacity. Bind expected root values for each assembled
  instance. For rotating/scaling geometry, honor each assertion's documented evidence limits.
- Bindings cannot add/remove contracts or members. When list counts or relationships change,
  regenerate the relevant assertions, keeping stable semantic IDs; there are still at most
  64 contracts and 1000 unique sample times. Unknown or unused inputs are errors, not ignored knobs.

## Read the coverage, not just pass

For each relationship, inventory the explicit target, assertion and requested samples. A uniquely resolved target is not proof of correctness. Inspect observed values against independent expectations; a presence check does not establish centering, padding or opacity. This surface supplies no contract-sidecar coverage report.

Review `observedUntargetedLayers` against your intended relationships, not as a mandate to check
every decoration. This list excludes internal layers and the duration-only probe; unseen content
and unsampled intervals remain unknown. Lists cap at 256 with explicit omission counts. Coverage
does not change the verdict or infer semantic quality. Preserve deliberate unchecked intervals.

For a new reusable check, run a valid parameter variant and a deliberately broken variant with
the SAME resolved expected intent (for example, move the child 8 local pixels without changing
the center constraint). Confirm the latter fails with useful evidence, then restore the scene.
Also test one delayed/nested placement. Geometry analysis does not replace painted-text alignment,
occlusion or continuous-motion inspection.
