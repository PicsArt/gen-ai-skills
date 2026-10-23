```json
{
  "project": "ai-playground-ad", "stage": 3,
  "source": { "kind": "figma", "fileKey": "…", "frames": ["node:1:2", "node:1:8"] },
  "target": { "ratio": "9:16", "width": 1080, "height": 1920, "fps": 30 },
  "sceneRef": "scenes/<hash>.json",
  "frames": [
    { "id": "f1", "name": "model picker", "hold": 3.0,
      "layers": [
        { "id": "f1_tabs", "role": "chrome", "type": "group", "matchKey": "tabs",
          "transform": { "x": 80, "y": 120, "w": 920, "h": 96, "opacity": 1, "z": 10 },
          "asset": { "url": "https://…/tabs.png" },
          "motion": [ { "kind": "slide", "from": "top", "at": 0, "duration": 0.5, "easing": "ease_out" } ] },
        { "id": "f1_list", "role": "content", "type": "raster",
          "transform": { "x": 80, "y": 260, "w": 920, "h": 1300, "opacity": 1, "z": 5 },
          "asset": { "url": "https://…/model-list.png" },
          "motion": [ { "kind": "scroll", "axis": "y", "by": -600, "at": 0.6, "duration": 1.8, "easing": "ease_in_out" } ] },
        { "id": "f1_tap", "role": "fx", "type": "vector",
          "transform": { "x": 610, "y": 940, "w": 64, "h": 64, "opacity": 0, "z": 20 },
          "motion": [ { "kind": "tap_pulse", "at": 2.4, "duration": 0.4 } ] }
      ] }
  ],
  "matched": [ { "key": "tabs", "layers": { "f1": "f1_tabs", "f2": "f2_tabs" } } ],
  "seams": [ { "between": ["f1", "f2"], "kind": "smart-animate", "approved": false } ],
  "gates": { "1": "passed", "2": "passed", "3": null, "4": null, "5": null },
  "blocked_on": null
}
```

Why the shape: a **layer** carries its own `transform`, `asset`/`content`, and a `motion`
list; `matchKey` links a layer to its twin in the next frame so `matched[]` can drive a
smart-animate; a **seam** is a `smart-animate` (matched layers morph) rather than a flat
transition wherever elements are shared. `sceneRef` **moves** with every edit — store
the latest.

A layer's **`type`** records what it *is*, which is what `design-layer-import` decided the export
format from: **`text`** (live text — the string + font, animatable per-line/char), **`vector`**
(icon/logo/shape kept as SVG or a flat fill — stays crisp at any scale), **`raster`** (a photo
or complex image baked to PNG), or **`group`**. Don't record a vector or text layer as a raster
PNG — that's the defaulting mistake that softens the ad at every scale but the one it was baked
at (see `design-layer-import`).

**`motion[].kind` labels above are DESCRIPTIVE project state — NOT `apply_preset` ids.**
Each is *realized* through a real scene mechanism, and you must map it, not pass the label to the
engine: `slide` → `apply_preset("motionPreset:slide_in")`; `tap_pulse` → **`apply_preset("motionPreset:tap_pulse")`
— this IS a real preset** (verified on current builds; a one-shot dip to ~0.92 and back, `at` = when it
fires, `appliesTo` includes `shape`; older text here said it didn't exist — that's out of date);
`scroll` / `smart-animate` → `position`/`scale`/`opacity` **keyframes** via `patch_scene` (there is no
`scroll` preset). So the label→mechanism map is: some labels are presets (`slide`, `tap_pulse`), some
are keyframes (`scroll`, `smart-animate`) — **resolve every id from `get_capabilities`** rather than
assuming a label is or isn't a preset, and only if your build lacks `tap_pulse` compose it from
`scale_pop` + `opacity` keyframes. Hand-authoring a whole animation "from scratch" when a real preset
(`scale_pop`, `slide_in`, `fade_in`, `tap_pulse`…) fits is the anti-pattern (see *"reach for the
highest-level tool"*); keyframe only the part no preset covers.
