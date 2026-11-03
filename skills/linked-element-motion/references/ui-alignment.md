# UI alignment: make the intended relationship executable

A contract is a separate JSON record of which relationship must hold, for which targets, during which root-time samples, and within what tolerance. It describes intent; it does not reposition layers or infer good design. Run the example below with `picsart_scene_check_contracts` and read pass, fail or inconclusive per contract.

First construct persistent relationships with a shared owner and parameter-derived local geometry
as described in the main recipe. The stationary fixture below deliberately isolates assertions;
it is not a recommendation to author reusable controls as independently positioned root layers.
For an editable button construction, fetch `app-ui-animation`. Use contracts as regression guards or
for phase-specific relationships, not to replace a common motion owner or shared sizing source.

## Choose the assertion that proves the claim

| Design claim | Check | What a pass does not prove |
|---|---|---|
| Label fits inside a button | `contains`, with intended padding | Centering, legibility or opacity |
| Label is centered on a stationary control | Separate `motion_range` bounds on `centerX` and/or `centerY` | Painted glyph balance or moving relative alignment |
| Label retains its correct placement during translation | Verify initial alignment, then `translation` relative to its owner | The initial offset was correct; scaling/rotation are not covered |
| Content keeps an explicit edge inset/gap | `edge_attachment` with design-derived signed gap | Alignment on the other axis |
| Label/background must exist and fade together | `present`/`co_presence`, plus `opacity_match` during the shared fade | Actual ink, clipping or occlusion |

scene text is vertically centered on its position, not anchored at a baseline. Do not add a
font-size fraction to compensate. Geometric centering and optical centering are different claims:
an intentional optical offset needs its own stated target and pixel review with the actual font.

## Runnable stationary-control example

Design: a 560×104 control with its label centered at root (280,52), a 1 px geometry tolerance,
and at least 8 px containment padding during the 0–2 second hold. These expected coordinates
come from the design, not from measuring the label's current placement.

Scene:

```json
{
  "version": "1.0",
  "composition": { "width": 560, "height": 104, "duration": 2, "fps": 30 },
  "layers": [
    {
      "id": "button",
      "transform": { "position": [0, 0] },
      "content": { "kind": "shape", "items": [
        { "type": "rect", "position": [280, 52], "size": [560, 104], "roundness": 52 },
        { "type": "fill", "color": "#152820ff" }
      ] }
    },
    {
      "id": "label",
      "transform": { "position": [280, 52] },
      "content": { "kind": "text", "text": "Continue", "font": { "family": "default", "size": 40 }, "color": "#ffffffff", "alignment": "center" }
    }
  ]
}
```

Sidecar:

```json
{
  "version": 1,
  "timeSpace": "root",
  "contracts": [
    { "id": "control-exists", "window": { "start": 0, "end": 2, "step": 0.25 }, "assert": { "kind": "present", "members": [{ "id": "button" }, { "id": "label" }] } },
    { "id": "label-fits", "window": { "start": 0, "end": 2, "step": 0.25 }, "assert": { "kind": "contains", "anchor": { "id": "button" }, "members": [{ "id": "label" }], "paddingPx": 8 } },
    { "id": "label-centered-x", "window": { "start": 0, "end": 2, "step": 0.25 }, "assert": { "kind": "motion_range", "target": { "id": "label" }, "channel": "centerX", "min": 279, "max": 281 } },
    { "id": "label-centered-y", "window": { "start": 0, "end": 2, "step": 0.25 }, "assert": { "kind": "motion_range", "target": { "id": "label" }, "channel": "centerY", "min": 51, "max": 53 } }
  ]
}
```

Validate the example with `picsart_scene_validate` and query its actual ids and geometry using `picsart_scene_query_layout`. Check supported centering/containment relationships with `picsart_scene_lint_layout`; explicitly compare any unsupported relation and retain the observations. Negative control: on a disposable copy, change label y from 52 to 64 while keeping the original expected center. Containment may still hold, but the intended centering comparison must fail. Restore y=52 and rerun; removing the label must not count as a pass. Inspect full-resolution `picsart_scene_contact_sheet` with `resolution` set to the composition dimensions, images separately for glyphs, contrast and clipping. The sidecar itself is not executed here.

## Adapt the check, not its verdict

- **Other sizes/fonts/copy:** derive centers from the intended control/content region, use actual
  text metrics for fit, and keep tolerances appropriate to the output scale. Test each repeated
  label and each distinct state; checking only the first/last containment cannot cover alignment.
- **Moving controls:** the numeric bounds above are absolute root coordinates, not relative centers.
  Verify correct initial centering, then use `translation` for an unscaled/unrotated rigid group.
  A constant wrong offset also passes `translation`. A fixed-size moving label can alternatively
  use an `edge_attachment` top inset **(control height − text height) / 2**, using measured text height and
  intended control height; rerun when those dimensions change.
- **Resizing/scaling controls:** a constant edge inset may no longer mean centered. Query both
  centers at matching root times and compare their difference to the intended offset/tolerance, or
  generate narrow per-sample `motion_range` contracts from the intended center trajectory. The tool
  has no general relative-center assertion; do not invent an `align` kind or learn expected values
  from the displaced label. Report a comparison not encoded in the sidecar separately. Rotation can
  make box checks inconclusive; retain that verdict and inspect pixels.
- **Nested/delayed instances:** rebind query-returned IDs/scopes and convert all windows and expected
  coordinates to root space. Local y=52 is not root y=52 after placement. Include settled states and
  event boundaries; a hold-only check says nothing about the entrance or transition.
- **Icon plus label:** center the intended content group/region; individual horizontal centers may
  deliberately differ. Verify vertical alignment separately. Keep intentional offsets explicit.

Deliver coverage by claim: what passed, failed, was inconclusive, and was not checked. A green
sidecar certifies only its sampled assertions, not overall visual quality.
