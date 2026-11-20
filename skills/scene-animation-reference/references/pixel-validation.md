# Rendered pixel assertions

Painted-pixel measurement of a render: ink presence, alignment, padding and region stability.


Use `picsart_scene_check_pixels` after schema validation and the geometry and motion checks (`picsart_scene_check_contracts`, `picsart_scene_check_motion`). It renders the scene and tests declared pixel intent. Build shared movement with one owner or supported bindings first; a pixel check does not replace ownership or looking at the frames.

The tool replies with a media job receipt by default: pass its `job` to the status tool named in `tools.jobStatus`, or call it with `async:false` to wait. Tool success means a report was produced, not that the assertions passed: read `status` and `coverage`. An unavailable renderer is not a pass.

## A runnable painted-bounds check

Validate `scene` first, then pass the whole object. The black marker is a stand-in for a label, not a typography test. It sits centered vertically. Move it down four pixels: the unchanged assertion must fail with a four-pixel offset. Repair the scene, never the tolerance.

```json
{
  "scene": {
    "version": "1.0",
    "composition": { "width": 80, "height": 40, "duration": 1, "fps": 10 },
    "layers": [
      { "id": "background", "content": { "kind": "color", "color": "#ffffff", "size": [80, 40] }, "transform": { "position": [40, 20] } },
      { "id": "marker", "content": { "kind": "color", "color": "#000000", "size": [40, 10] }, "transform": { "position": [40, 20] } }
    ]
  },
  "pixels": {
    "version": 1,
    "times": [0, 0.5],
    "checks": [{
      "id": "centered-marker", "kind": "ink_alignment", "region": [0, 0, 80, 40],
      "foreground": [0, 0, 0], "background": [255, 255, 255],
      "colorTolerance": 12, "minPixels": 10, "maxFillFraction": 0.5,
      "axis": "y", "offsetPx": 0, "tolerancePx": 1
    }]
  }
}
```

## Regions

A region is fixed root output pixels `[x,y,width,height]`, or follows a queried container: `{"target":{"id":"button","composition":"main"},"insetPx":2}`. Take the id and composition from `picsart_scene_query_layout`; never guess nested instance names. The inset shrinks all four edges. Missing, ambiguous or inactive targets, rotated or clipped anchors, collapsed regions and regions outside the frame are inconclusive; the tool never clips silently. Fractional edges round outward, so allow that in the tolerance.

For a moving widget, parent the label and its background to one composition and inspect that container's interior. Anchor the container, not the ink under test: following an already-wrong label and asking whether it centers on itself is circular.

## Choose the measured property

| Kind | Fields | Measurement |
|---|---|---|
| `ink_presence` | foreground, background, colorTolerance, minPixels, maxFillFraction | Enough isolated paint exists. It does not recognise words or objects. |
| `ink_alignment` | the ink fields, axis x/y, signed offsetPx, tolerancePx | Painted bounding-box center minus region center on one axis; not optical centering. |
| `ink_padding` | the ink fields, paddingPx | The smallest left/top/right/bottom painted margin reaches the declared padding. |
| `region_stability` | pixelTolerance, maxChangedFraction; at least two times | Every later sample against the FIRST sample, in local pixels, without resizing. Different crop sizes are inconclusive. |

Every check needs a unique `id` and a `region`. Pass each kind its own fields only. Colors are integer sRGB `[r,g,b]`. `colorTolerance` (0 to 64) is the largest per-channel residual from the foreground and background blend; a pixel is ink when its projected foreground share is at least 20%. That accepts antialiasing, not gradients, shadows or photos; more than 0.5% unexplained colors is inconclusive.

Missing ink fails. Excess fill, ink touching the region boundary and transparency inside the region are inconclusive; transparency elsewhere is irrelevant. Author an opaque matte rather than letting the checker invent one. Ink presence does not prove a given layer is visible, and clipping strictly inside a region can escape it.

## Evidence and limits

Status precedence is a measured fail, then inconclusive, then pass. At most 64 times and 16 checks, 16 megapixels per frame and 256 per call; split longer windows, never lower the FPS. All times must sit inside the scene duration. A sample-only pass proves nothing between samples. Colors differ with fonts, antialiasing and color conversion, so lock those and choose a documented allowance. This is a measurement under stated inputs, not a judgment of legibility or beauty: still look at the decisive frames and watch the final motion.
