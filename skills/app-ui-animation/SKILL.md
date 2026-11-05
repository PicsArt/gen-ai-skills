---
name: app-ui-animation
description: Build a phone or web UI in a scene with scrolling, carousels, button feedback, cursor paths and clicks, context menus, drag-and-drop, synchronized controls, bottom sheets and frosted-glass panels. Use when animating an app mockup, UI walkthrough, slider or onboarding flow, frosted glass or glassmorphism cards, or when a mock renders correctly but reads as a picture rather than an app somebody is using.
metadata:
  category: authoring
  version: '1.11'
  ported-from: ui-motion 1.11 at 55.75.0
user-invocable: false
---

# UI motion — making a mockup behave like a device

A UI mock that renders correctly and still reads as a screenshot is almost always missing
three things: the content does not carry momentum, nothing answers a touch, and panels
appear instead of arriving. Each has a home in the catalog. **Read this before authoring a
new preset for a UI beat — most UI beats are arrangements of what already exists.**

## Where a UI beat belongs

Before choosing a preset, settle the semantic units and who owns their motion with
linked-element-motion (fetch with `picsart_scene_recipe`, name `linked-element-motion`); it also
covers the ownership/binding/phase decision, growing panels and sibling reflow. Derive backing
dimensions and child placement from shared parameters so a size edit preserves the layout by
construction; grouping does not make a container automatically fit its animated children. Validate
those relationships throughout the event window.

| Home | When |
|---|---|
| **Motion preset** or **Look** | Choose between them with motion-pattern-library (fetch with `picsart_scene_recipe`, name `motion-pattern-library`). Only a look adds structure the layer does not have — a viewport, a mask, extra layers (`scroll`, `rounded_corners`) |
| **Scene template** | The motion depends on a layer's index or count (a list stagger, a grid) |
| **This recipe** | No new capability — a known-good arrangement of the above |

And before adding any of them: **prefer a param on an existing preset over a new preset.**
Paged scrolling is `snap` on `scroll`, not a `carousel` look. A catalog that grows one entry
per arrangement stops being scannable, and then finding costs more than building.

## Build the chrome from shapes

UI chrome is rectangles with rounded corners and text on top. Author it as `kind: "shape"` —
it is built in. Do **not** reach for an SVG data-URI; it
costs you a rasterised asset, a URI-encoding trap, and animatable geometry.

A button, as a scene asset so the whole thing can be referenced and pressed as one unit:

```json
{ "type": "scene", "scene": {
  "version": "1.0",
  "composition": { "width": { "$eval": "width" }, "height": { "$eval": "height" }, "duration": 6, "fps": 30, "background": "#00000000" },
  "parameters": {
    "width": { "type": "number", "default": 560, "min": 300, "max": 1000 },
    "height": { "type": "number", "default": 104, "min": 80, "max": 200 }
  },
  "layers": [
    { "id": "bg", "content": { "kind": "shape", "items": [
        { "type": "group", "contents": [
        { "type": "rect", "size": [{ "$eval": "width" }, { "$eval": "height" }], "position": [0, 0], "roundness": { "$eval": "height / 2" } },
          { "type": "fill", "color": "#111111ff" } ] } ] },
      "transform": { "position": [{ "$eval": "width / 2" }, { "$eval": "height / 2" }] } },
    { "id": "lb", "content": { "kind": "text", "text": "Continue",
        "font": { "family": "helvetica-bold", "size": 40 }, "color": "#ffffffff", "alignment": "center" },
      "transform": { "position": [{ "$eval": "width / 2" }, { "$eval": "height / 2" }] } } ] } }
```

Store this as a scene asset and place a `scene_ref` with `fit:"none"`, binding `width`/`height`
on that reference. Animate the reference once for shared motion and opacity. The formulas resolve
when the instance is assembled; after expanding/baking the reference, its geometry is concrete and
later parameter edits do not remain live. Re-resolve the source for a new size, or edit the expanded
geometry coherently. Shared centers prevent independent drift, not text overflow or optical imbalance.

`roundness` is ONE number for all four corners — a `rect` has no per-corner radius,
and neither does the `rounded_corners` look. Design around it rather than hunting for it.

Text is vertically centered on `transform.position.y`; it is not a baseline coordinate.
Use the intended control center, without adding a guessed font-size/baseline correction.
For a centered label, check both its fit and its center against the control's intended layout.
For icon-plus-label layouts, establish the intended content region or group center rather than
forcing every child to the button's horizontal center. An intentional optical offset should be
explicit and previewed with the actual font, not inferred from an already displaced label.
Read the UI alignment reference linked from linked-element-motion (fetch with `picsart_scene_recipe`, name `linked-element-motion`)
for executable checks before calling the control validated. Through MCP, fetch `picsart_scene_recipe` for
`linked-element-motion`, then its listed UI alignment reference. Cover alternate labels/states and
rerun after copy, font, size or nesting changes; shared motion does not prove initial alignment.

## The three beats

### Scrolling content

Apply the `scroll` look to the layer holding the screen — a tall image, or a `scene_ref` to a
composition of rows. The look makes the layer's own box the viewport and moves the content
under it; travel is the content's overflow, computed for you.

```json
"looks": [ { "look": "scroll",
  "params": { "flicks": 2, "period": 1.1, "hold": 0.35, "decel": 0.45, "bounce": 40, "start": 0.3 } } ]
```

`decel` is the momentum time constant: `0.5` is UIScrollView's normal deceleration rate,
`0.1` its fast rate, `~0.25` approximates Android's spline fling. `hold` is the pause between
flicks — without it the content is still creeping when the next flick fires and the cadence
reads as a loop rather than a hand. `bounce` is the rubber band in px; set it to `0` for the
Android feel, which has no rubber band.

For a **carousel**, add `snap` — the page length in px. Each flick then advances exactly one
page, which is what a paged scroller does, and `flicks` counts pages. The rubber band is
suppressed automatically when the pages stop short of the travel.

A nested composition keeps running its own animations while it scrolls, so a live screen
inside a scrolling viewport works.

### Press feedback

Apply the `tap_pulse` motion preset to the button layer (the `scene_ref`, so the whole widget
presses rather than just its label).

```
picsart_scene_apply_preset { "scene": <scene>, "layerId": "cta", "preset": "motionPreset:tap_pulse", "params": { "at": 1.6 } }
```

`at` is seconds **into the layer's own window**, not into the composition — a tap lands
mid-shot, so the preset does not assume the layer's first frame. Historical observations on a 560px
button (not a portable benchmark: fixture/version/command were not retained beside this table):

| t | width | scale |
|---|---|---|
| 1.60 | 560 | 1.000 |
| 1.64 | 534 | 0.954 |
| 1.72 | 566 | 1.011 |
| 1.76 | 582 | 1.039 |
| 1.84 | 560 | 1.000 |

Down to `1 - amount` in the first 28% of `duration`, up through rest to a `1 + settle`
overshoot, then back. `settle: 0` snaps back flat — a mechanical switch rather than a finger.
The pop is a factor on the layer's own scale about its centre; move `transform.anchor` to
press from somewhere else.

### Cursor-led action

For reusable cursor styling, curved paths, direction and click feedback, or a variable-row context menu, read
[Cursor actions and menus](references/cursor-actions.md). Through MCP, fetch `picsart_scene_recipe`
with `name: "app-ui-animation"` and `reference: "references/cursor-actions.md"`.
It separates appearance from choreography, defines the hotspot and click-tail clocks, and routes
arrival, pause, menu ownership, copy-fit and rendered checks. Do not rebuild a cursor per style.
For direction-following, prefer the position-direction expression in that reference, not an
auto-orientation flag or independently duplicated rotation keyframes. One edited path should
remain the source of both travel and heading; keep the glyph's forward-axis offset in its transform.

For a card transfer with source-list reflow, use [Drag, drop and list reflow](references/cursor-drag-drop.md).
It keeps the cursor attached by expression during carry and maps each phase to validation tools.

When a walkthrough must show *why* the UI changed, author one causal chain around a shared event
time: **pointer arrives → control answers → result begins**. A visible pointer is an ordinary shape
layer; scene does not require or provide a special cursor primitive. Keep the pointer above the
UI in layer order, move it to the action target, and hold it there long enough for the press and
result to read.

Use the event time as a coordination point:

- end the pointer's travel at the event;
- begin the target's scale or color feedback at the event;
- begin a restrained press ring at the event when the click would otherwise be ambiguous;
- begin the result at the event, or shortly afterwards when intentional system latency is part of
  the story.

The exact travel time, pulse size, and latency are project trials, not scene rules. In the tested
portrait construction, a pointer arrived at `1.0s`, the target compressed and a ring expanded at
`1.0s`, and the result entered from `1.0–1.5s`. Those values prove one viable arrangement only.

Protect the attention order. Before the event, the pointer should be the moving leader. At the
event, feedback belongs close to the target. After the event, settle the pointer and let the result
become the leader. Avoid a looping cursor, a pulse that starts before arrival, or a result that is
already moving while the pointer is still travelling; each weakens causality.

Verify at four moments: during approach, at arrival, immediately after the event, and after the
result settles. Use layout queries to confirm the pointer reaches the target, then preview or export
the continuous interval because correct timestamps do not prove readable causality. If the result
continues into another scene or track seam, route the relationship and representation choice through
`motion-scene-continuity`; this skill owns the device-like beat inside a scene.

### Dragging and synchronized controls

For **grab → carry → release → pointer departure**, or a slider/readout driving another element,
read [Drag and synchronized controls](references/drag-and-sync.md) before building the beat.
Through MCP, fetch `picsart_scene_recipe` with `name: "app-ui-animation"` and
`reference: "references/drag-and-sync.md"`. It covers phase-bounded attachment, off-center grip,
shared progress, delayed clocks and negative-control checks. A click's shared event time alone does
not keep two moving subjects synchronized throughout a gesture.

### Loading into readable content

Use `scene://skeleton-reveal` for a variable-row loading card; use an ordinary opacity track
when no placeholder structure or coordinated handoff is needed. Read
[Loading reveal](references/loading-reveal.md) for customization, phase clocks and executable
validation intent. Through MCP, fetch `picsart_scene_recipe` with `name: "app-ui-animation"` and
`reference: "references/loading-reveal.md"`. Shared layout prevents row drift, but does not
prove text fits or that loading and reading phases are visibly distinct.

### Frosted glass

A frosted pane (glassmorphism) behind a card is one line: `looks: [{ look: "frosted_glass" }]`
on the card. The pane is the card's box, and moves, scales and fades with it; give a
`scene_ref` widget `bounds` and a surface opacity below 1 so the frost shows through it. For a
pane that is not a rounded rect, write the two layers yourself: an `adjustmentLayer` shape
carrying `gaussian_blur`, and a translucent tint above it. They frost only content beneath them
on the same canvas, so they live as siblings or in an unsized `blending: "pass_through"`
composition, never inside a `scene_ref` widget. Read
[Frosted glass](references/frosted-glass.md) for the JSON, where it frosts nothing, and how
to animate it; through MCP, `picsart_scene_recipe` with `name: "app-ui-animation"` and
`reference: "references/frosted-glass.md"`.

### A bottom sheet

Four parts, none of which is a preset of its own:

1. A **dim** — a `color` layer over the screen (`#000000a0`) with the `fade` look,
   `role: "in"`, `length` the rise.
2. The **sheet** — a `scene_ref` to a composition of the sheet's own content, positioned so
   its bottom edge is flush with the frame bottom.
3. The **rise** — the `slide` look with `role: "in"`, `direction: "up"` and `distance: 1`
   (one sheet height: `distance` is in multiples of the layer's own size).
4. **`rounded_corners`** on the sheet. This rounds all four corners; placing its bottom exactly
   at the frame bottom does not hide the lower corner arcs. If only the top corners should show,
   extend the backing below the frame far enough to hide its lower arcs and inspect the crop.
   Update the expected bottom-edge contract to that extended backing's intended position.

A look cannot supply the dim. A look's fragment is isolated to its own subject, so it can
paint over the layer it is applied to but never over what sits below it — which is why a
sheet is an arrangement and not a look.

## Validate each UI beat

Fetch `picsart_scene_recipe motion-pattern-library` and its **Validation by pattern** reference.
Its **UI beats** rows specify scroll/carousel,
press, pointer, drag, synchronized controls, and sheet checks. Name the event and intended result before authoring, convert all
checks to root time, and test the whole widget owner plus its contents. A moving label inside a
stationary backing is not a successful button press. A stationary viewport box does not prove its
content scrolled. Layout contracts cannot prove dimming, clipping, or readable causality: inspect
those pixels and continuous playback, and report them separately from contract verdicts.

## Frictions

- **A layer with `start` and no `duration` gets the composition's FULL length, not the
  remainder.** `start: 1` in a 4s composition gives the layer `duration: 4` — a window that
  runs to 5s, of which the last second is outside the composition and never plays. The layer
  is live at 3.5s where a `duration: 2` twin has already ended, so a beat you meant to close
  before the end does not. The presets themselves are fine: `slide_in`, `fade_in` and
  `tap_pulse` bake identical keyframe times with and without a declared `duration`. Declare
  `duration` alongside `start`.
- **Order the preset applies after the scene is final.** A motion preset bakes keyframes at
  apply time, so editing a layer's `start`/`duration` afterwards leaves stale times behind.
  Re-apply. A look reads the layer's window at render time and needs no re-apply.
- **A `tap_pulse` on a text layer scales the label only.** Wrap the widget in a scene asset
  and pulse the `scene_ref` if you want the whole control to answer.
