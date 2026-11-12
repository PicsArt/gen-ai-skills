---
name: motion-pattern-library
description: Worked scene motion patterns for entrances, exits, stagger, directional nudges, emphasis, ambient life, springs, arcs, layered beats, parenting, parallax, focus, wipes, drawn strokes, and cartoon fast motion (smears, multiples, speed lines). Use when the motion intent is known and you need supported scene properties and keyframe structures to adapt; values are starting points, not universal timing rules.
metadata:
  category: authoring
  version: '1.6'
  ported-from: motion-patterns 1.6 at 55.104.0
user-invocable: false
---

# Worked beats

Choose a construction for the intended beat, adapt it to the scene, then check the result.
The snippets are fragments, not complete scenes or ready-to-run MCP calls; `…` marks omitted input.
Times, distances and amplitudes are starting choices, not quality guarantees. Use `picsart_scene_validate`
for structure, `picsart_scene_query_layout` / `picsart_scene_lint_layout` for declared geometry, and `picsart_scene_contact_sheet` with explicit `times` and `resolution` equal to the composition dimensions
plus continuous playback to judge the motion. Fetch current preset/look parameters before applying one.

Before adapting **any pattern below**, read
[Validation by pattern](references/validation-by-pattern.md). Select its row, declare the intended
outcome and tolerance, and retain its measurement and visual checks in the beat's acceptance plan.
Fetch it through MCP with `picsart_scene_recipe` using `name: "motion-pattern-library"` and
`reference: "references/validation-by-pattern.md"`. A successful render or schema check alone is
not motion acceptance; report measured, visually inspected, and unchecked outcomes separately.

Decisions behind these — which beat, which register, how long — are
`picsart_scene_recipe motion-intent`. The fields themselves are
`picsart_scene_recipe scene-animation-reference`. For whole-sequence relationships, visual carriers, intentional
resets, and seam choice, start with `picsart_scene_recipe motion-scene-continuity`. This is the middle: shapes
that work.

## Entrance, and the exit that answers it

A useful pacing trial is an exit around 65–75% of its entrance. This is a motion heuristic, not an
scene rule. Pick the form by what happens next:
a **motion preset** when the keyframes will be edited afterwards (by the agent or in the editor), a
**look** when the motion should stay a named, swappable entry for the editor.

As a look, both halves are one look played at either end of the layer by `role`:

```json
{ "scene": …, "layerId": "card", "preset": "look:zoom", "params": { "role": "in",  "length": 0.5,  "scale": 0.9 } }
{ "scene": …, "layerId": "card", "preset": "look:zoom", "params": { "role": "out", "length": 0.35, "scale": 0.9 } }
```

Each call appends one `looks[]` entry, so the document keeps both by name and an editor can show and
swap them. `role: in` starts at the layer's start; `role: out` ends exactly at its end, however the
layer is later trimmed.

As motion presets, `picsart_scene_apply_preset` with `motionPreset:<id>` (iOS `applyMotionPreset`) expands each into ordinary
keyframes you then own:

```json
{ "scene": …, "layerId": "card", "preset": "motionPreset:zoom_in",  "params": { "duration": 0.5, "from": 0.9 } }
{ "scene": …, "layerId": "card", "preset": "motionPreset:zoom_out", "params": { "duration": 0.35, "to": 0.9 } }
```

Check start, midpoint and end bounds: the size should change around the intended pivot, with no
unintended center drift. Check the exit against the layer's actual end after trimming.

The motion looks at a glance, so a substitution is an informed one (`picsart_scene_capabilities`
`look:<id>` has every param):

| Look | What it does |
|---|---|
| `fade` (`in` / `out`) | opacity only; nothing moves |
| `slide` (`in` / `out`) | travels `distance` multiples of its own size along `direction`, `up` by default |
| `zoom` (`in` / `out`) | grows from, or shrinks to, `scale` of its own size |
| `spin` (`in` / `out`) | turns through `angle` while scaling from `scale`; `scale: 1` turns without scaling |
| `wipe` (`in` / `out`) | a hard edge uncovers or covers it along `direction` |
| `blur` (`in` / `out`) | focus pull: `gaussian_blur` from, or to, `amount` |
| `flip` (`in` / `out`) | turns edge-on through `angle` about `axis` (`y`, or `x`) in perspective |
| `pop` (`in`) | overshoots to `overshoot` and settles |
| `float`, `sway`, `shake`, `pulse` | loops for the layer's whole length |
| `glow_pulse` | a blurred copy screened over the layer swells and fades each `period` |
| `ken_burns` | zooms or pans the picture inside a fixed frame; `media` / `scene_ref` only |

`fade` on a motion look blends its motion toward the layer's rest: `fade: 0.5` slides half the
distance, `fade: 0` leaves the layer where it stands, and a keyframed fade ramps the motion in.

A look plays over its whole layer unless the entry names a window — `start` (on the layer's clock)
and `duration`: `{ "look": "shake", "start": 1.2, "duration": 0.4 }` shakes for 0.4s and rests
around it. An entrance inside a window starts at the window's start and holds its start before it;
an exit ends at the window's end and holds there after it.

Preset behaviour at a glance (`picsart_scene_capabilities` with `sections: ["motionPresets"]` lists preset parameters):

| Preset | Construction to inspect |
|---|---|
| `fade_in` / `fade_out` | opacity only; nothing moves |
| `slide_in` | directional arrival; inspect the selected direction and travel |
| `slide_out` | directional departure; inspect the final visible frame |
| `zoom_in` | scales from `from` toward rest |
| `zoom_out` | scales from rest toward `to` |
| `scale_pop` | inspect the peak and settling; do not assume an entrance from small to large |
| `glow_pulse` | continuous pulse, does not resolve |
| `ken_burns` | `media` / `scene_ref` only |

A one-shot beat at a chosen moment — `spring`, `tap_pulse`, `scale_pop` — is a preset only: looks
hold entrances, exits and loops.

## A settle with overshoot

One segment, no third keyframe — the curve carries it:

```json
"scale": { "keyframes": [
  { "time": 0.0, "value": [0.8, 0.8],
    "easing": { "kind": "cubic_bezier", "control": [0.175, 0.885, 0.32, 1.275] } },
  { "time": 0.45, "value": [1.0, 1.0] }
] }
```

The `y2` control ordinate influences overshoot but is not the rendered overshoot percentage.
Sample the track through its peak and landing; judge the peak against this element's size and role.

## A real spring

When one overshoot is not enough — a damped oscillation as a single expression:

```json
"scale": { "expression": "return value * (1 + 0.35 * math.exp(-6*time) * math.cos(18*time))" }
```

The exponential damps the amplitude; the cosine controls oscillation frequency. Check extrema and
the settled tail, not only endpoints. Confirm the expression's clock when the layer starts late.

A part that lags ANOTHER part's motion (hair behind a turning head) is not this: apply the
`follow_through` preset to a parameter (`picsart_scene_recipe scene-animation-reference`, "Secondary motion and characters").

## Ambient life

Background motion that keeps looping while the beat lasts:

```json
"scale": { "expression": "return value * (1 + 0.02 * math.sin(2*math.pi*time/4))" }
```

The `0.02` coefficient varies the base scale by ±2%. Keeping ambient amplitude below the leader is a motion
heuristic; leaving the background still is also valid.
The literal `4` is a four-second period: changing the beat's duration does not retime it. Change the
period explicitly if the intended number of cycles must stay fixed, then recheck the loop and ending.

For text, inspect the available ambient text-animation presets; caption decorations and ordinary
text layers have different authoring entry points (`scene-animation-reference`).

## Confetti, sparks and snow

Many small copies of one thing, thrown and falling, are one layer with `particles`, not hand-copied
layers. The layer's `content` is the particle; its `transform.position` places the emitter:

```json
{ "id": "confetti", "transform": { "position": [540, 1080] },
  "content": { "kind": "shape", "items": [{ "type": "rect", "size": [22, 12] }, { "type": "fill", "color": "#ff3b6b" }] },
  "particles": { "seed": 1, "emit": { "bursts": [{ "time": 0, "count": 120 }] },
    "life": [2, 3.2], "direction": -90, "spread": 40, "speed": [1100, 2300], "gravity": [0, 1500],
    "spin": [-450, 450], "opacityOverLife": [1, 0.3] } }
```

Every particle draws the layer's content, so several colours are several such layers, each with its
own colour and `seed`. Each burst releases `count` particles at its `time`; a stream is
`"emit": { "rate": 40 }`, which emits until the layer ends (or for its `"duration"`), and a negative
`start` has it already running at the layer's first frame. Snow streams from a wide
`"origin": { "shape": "line", "size": [1400, 1] }` on a layer placed above the frame, with
`"direction": 90`, a small `"spread": 30` and little `gravity`: a directed throw needs a small spread,
since the default 360 throws every way. Two layers with different particle sizes, speeds and
opacities read as depth. Change `seed` for another throw of the same effect; the same seed always
draws the same frames.

## An arc instead of a straight line

Tangents bow the path; easing still shapes the timing along it:

```json
"position": { "keyframes": [
  { "time": 0, "value": [200, 540], "easing": "ease_in_out", "outTangent": [120, -160] },
  { "time": 1.6, "value": [880, 540], "inTangent": [-120, -160] }
] }
```

Inspect the swept path for collisions and unintended depth crossings. The handles bow this path;
without them the same two keyframes describe a straight line.

## Two motion layers on one element

Primary and ambient as separate components, so each stays re-timeable:

```json
"transforms": [
  { "id": "entrance", "animations": { "translation": { "keyframes": [
      { "time": 0, "value": [0, 200], "easing": "ease_out" }, { "time": 0.6, "value": [0, 0] } ] } } },
  { "id": "breathe", "animations": { "scale": {
      "expression": "return value * (1 + 0.12 * math.sin(2*math.pi*time/1.5))" } } }
]
```

Check that the entrance lands at its intended time while the ambient track continues independently.
The 12% amplitude here demonstrates separation, not a recommendation for subtle background motion.

## A whole beat in one register

Brief: *"clean, professional quarterly review card"*. Try a restrained timing palette, then judge it
against reading time and the actual layout. Four roles, each entering when its context justifies it:

| Layer | Starts | Motion |
|---|---|---|
| background | 0 | 2% breathe expression — least motion in the frame |
| card | 0.2 | `position` 600 → 520 with a co-terminous opacity fade, 0.5s `ease_out` |
| headline | 0.8 | `slide_up_lines` 0.5s — a build, after its context |
| CTA | 2.0 | scale 0.9 → 1.0; inspect any easing overshoot instead of deriving it from a control ordinate |

Preview the entrance order and readable holds. If the background competes with the headline or the
CTA arrives before its context is understood, reduce competing motion or retime the beat.

## Staggering a row

Per-item delay inside a `$each` body, using the loop index:

```json
{ "$each": "tiles", "as": "tile", "body": {
    "id": "tile",
    "animations": { "opacity": { "keyframes": [
      { "time": { "$eval": "tile.@index * 0.08" }, "value": 0 },
      { "time": { "$eval": "tile.@index * 0.08 + 0.2" }, "value": 1 } ] } } } }
```

A compact stagger is a starting trial; adjust the spread to the reading order. Resolve the
template first (`picsart_scene_apply_template` with `mode='bootstrap'`) — the tools refuse a stray
`$each` by name.

## A cascading spatial entrance

**Intent.** Reveal a reading order without turning every item into a separate hero. The first item
leads; later siblings repeat the same relationship with a compact delay.

**scene translation.** Give each sibling the same position-plus-opacity arrival, offsetting its
keyframe times. The opacity and position tracks below end together, so each sibling reads as one
arrival. These are fragments for three ordinary layers, not a named preset:

```json
{ "id": "item-a", "animations": {
  "position": { "keyframes": [
    { "time": 0.00, "value": [540, 680], "easing": "ease_out" },
    { "time": 0.50, "value": [540, 600] } ] },
  "opacity": { "keyframes": [
    { "time": 0.00, "value": 0, "easing": "ease_out" },
    { "time": 0.50, "value": 1 } ] } } }
{ "id": "item-b", "animations": {
  "position": { "keyframes": [
    { "time": 0.08, "value": [540, 880], "easing": "ease_out" },
    { "time": 0.58, "value": [540, 800] } ] },
  "opacity": { "keyframes": [
    { "time": 0.08, "value": 0, "easing": "ease_out" },
    { "time": 0.58, "value": 1 } ] } } }
{ "id": "item-c", "animations": {
  "position": { "keyframes": [
    { "time": 0.16, "value": [540, 1080], "easing": "ease_out" },
    { "time": 0.66, "value": [540, 1000] } ] },
  "opacity": { "keyframes": [
    { "time": 0.16, "value": 0, "easing": "ease_out" },
    { "time": 0.66, "value": 1 } ] } } }
```

**Heuristic, not contract.** `0.08s`, `0.5s`, and `80px` are trial values. Compress the spread for a
dense row, lengthen it when order needs to be read, and change travel with the layout. scene only
requires valid ascending times and supported values; it does not define an ideal cascade.

**Avoid when.** Use a single group motion when the items form one inseparable object, or when the
last sibling would arrive too late for the available reading time. Do not add overshoot to every
item merely because they are staggered.

**Check.** Validate the assembled scene, query each landing, and preview the entire cascade to check
reading order and the time left for the last item.

## A three-phase directional nudge

**Intent.** Emphasize a direction after the cascade reaches rest. Nudge the semantic leader only;
subordinates stay still so the second beat does not restart the entire row.

**scene translation.** Keep the entrance and the nudge as separate motion responsibilities.
Use an outer empty control for the leader's entrance, an inner empty control for the nudge, and
parent the painted leader to the inner control. The inner positions are offsets in the outer empty's
local space. Keep the leader's opacity track on the painted item as in the cascade example above;
only its spatial motion moves to the two controls:

```json
{ "id": "leader-entrance-rig",
  "content": { "kind": "empty" },
  "transform": { "position": [540, 600] },
  "animations": { "position": { "keyframes": [
    { "time": 0.00, "value": [540, 680], "easing": "ease_out" },
    { "time": 0.50, "value": [540, 600] }
  ] } } },
{ "id": "leader-nudge-rig", "parentId": "leader-entrance-rig",
  "content": { "kind": "empty" },
  "transform": { "position": [0, 0] },
  "animations": { "position": { "keyframes": [
    { "time": 0.80, "value": [0, 0], "easing": "ease_in_out" },
    { "time": 0.86, "value": [-12, 0], "easing": "ease_out" },
    { "time": 1.02, "value": [30, 0], "easing": "ease_in_out" },
    { "time": 1.22, "value": [0, 0] }
  ] } } },
{ "id": "item-a", "parentId": "leader-nudge-rig",
  "transform": { "position": [0, 0] },
  "content": { "kind": "color", "color": "#61d5ffff", "size": [720, 120] },
  "animations": { "opacity": { "keyframes": [
    { "time": 0.00, "value": 0, "easing": "ease_out" },
    { "time": 0.50, "value": 1 }
  ] } } }
```

The small local move left is anticipation, the move through zero to the right is the directional
action, and the final keyframe resolves at `[0, 0]`. The entrance rig lands before the nudge rig
starts. One motion responsibility per track also keeps the entrance and nudge independently
retimeable. A single long spatial track is also valid; choose controls when separate editing helps.

**Heuristic, not contract.** The `12px` anticipation, `30px` action, and phase durations are trials.
Scale them to the element and viewing size. A nudge can omit anticipation when speed or restraint
matters more than character.

**Avoid when.** Do not nudge a decorative element that does not own the direction, repeat the gesture
until it becomes jitter, or copy it to every sibling. Skip the nudge entirely if the cascade already
spent the beat's attention budget.

**Check.** Query the leader and siblings before, during and after the nudge: only the leader should
deviate from its settled position. Inspect playback to decide whether anticipation reads or flickers.

## A persistent shared element

**Intent.** Let the eye follow one object into a new arrangement when its identity matters.

**scene translation.** Keep one layer id and one layer window alive across both states; animate
its placement delta while subordinate layers leave or arrive around it:

```json
{ "id": "shared-card", "start": 0, "duration": 4,
  "animations": {
    "position": { "keyframes": [
      { "time": 1.7, "value": [540,720], "easing": "ease_in_out" },
      { "time": 2.3, "value": [320,520] } ] },
    "scale": { "keyframes": [
      { "time": 1.7, "value": [1,1], "easing": "ease_in_out" },
      { "time": 2.3, "value": [0.74,0.74] } ] } } }
```

**Heuristic, not contract.** Match the path and pace to the surrounding layout; scene requires
valid tracks, not a particular duration or scale delta. **Avoid when.** Use two layers when the
objects are not semantically identical or cannot share one lifetime. **Check.** Declare the carrier
with `present` across the seam, then inspect playback: geometric presence alone cannot prove that
the viewer recognizes the same object.

## A direction-matched seam

**Intent.** Continue an already-established whole-frame direction across a clip boundary.

**scene translation.** Use a catalog transition on the track gap; omit the entry for a deliberate
hard reset:

```json
"content": { "kind": "track", "clips": [
  { "duration": 2, "content": { "kind": "color", "color": "#1b2d45ff" } },
  { "duration": 2, "content": { "kind": "color", "color": "#34234dff" } }
], "transitions": [
  { "between": 0, "id": "slide", "duration": 0.6,
    "params": { "direction": "left" } }
] }
```

**Heuristic, not contract.** Match direction only when continuation is the message; a cut,
crossfade, or reversal may better express punctuation, ambiguity, or interruption. **Avoid when.** Do
not spend a transition to disguise an unresolved semantic relationship. **Check.** Preview both
sides of the actual seam and its midpoint; compare a simple cut when the intended relationship is a reset.

## A causal handoff

**Intent.** Make an action visibly cause a response and reveal instead of reading as three unrelated
animations.

**scene translation.** Give the action landing, response onset, and reveal onset one event time;
their later settling times may differ:

```json
{ "id": "action", "animations": { "position": { "keyframes": [
  { "time": 1.35, "value": [230,1350], "easing": "ease_in_out" },
  { "time": 2.2,  "value": [760,1220] } ] } } },
{ "id": "response", "animations": { "opacity": { "keyframes": [
  { "time": 2.2, "value": 0, "easing": "ease_out" },
  { "time": 2.35, "value": 0.85 }, { "time": 2.6, "value": 0 } ] } } },
{ "id": "reveal", "animations": { "position": { "keyframes": [
  { "time": 2.2, "value": [540,1660], "easing": "ease_out" },
  { "time": 2.7, "value": [540,1540] } ] } } }
```

**Heuristic, not contract.** Share the onset unless latency is an intentional story or interface
state; amplitude and settling remain project trials. **Avoid when.** Do not synchronize unrelated
events merely because they are nearby in time. **Check.** Query immediately before and after the
event, then watch whether action, response and reveal read as one causal sequence.

## Depth from one camera

Parallax and an exploded stack, built from one camera move rather than per-layer offsets, are in
[references/depth-from-one-camera.md](references/depth-from-one-camera.md). Read it before giving layers
different depths.

## Moving a group without grouping it

`parentId` names a SIBLING whose transform this layer rides — animate the parent, the children come
along, and each keeps its own timing, opacity and easing:

```json
{ "id": "card",  "content": { "kind": "color", "color": "#3355ff", "size": [200, 140] },
  "transform": { "position": [200, 420] },
  "animations": { "position": { "keyframes": [
      { "time": 0, "value": [200, 420], "easing": "ease_out" }, { "time": 2, "value": [600, 420] } ] } } },
{ "id": "badge", "parentId": "card", "transform": { "position": [140, 70] },
  "content": { "kind": "color", "color": "#ffcc00", "size": [40, 40] } }
```

**The child's position is in the parent's local pixel space, not the composition's.**
With the default centered anchor, a `[200, 140]` parent pivots at `[100, 70]`, so a child at `[140, 70]` sits 40px right
of it — and a child at `[500, 400]` is 400px right and 330px down, which is almost never what the
number looked like. Author the child near the parent's box centre and read the offset from there.
If the parent's anchor changes, recompute that offset and query the result.

Only the transform travels — Placement and its `transforms[]` stack, in that order. A child of a
transparent parent does not inherit that opacity through `parentId`. For a group
fade or a group mask, nest the layers in an inline composition instead —
`{ "kind": "composition", "layers": [...] }` — and put the fade or `mask` on that layer. It is part
of this scene and shares its assets. A `scene_ref` is a separate document, for a body you reuse.
Build a card this way as one group: its backing, image, label and icon in one composition,
keyframed once, so its parts cannot drift apart.

**A control layer is the driver you did not have to elect.** `{ "kind": "empty" }` draws nothing and
exists to be parented to — After Effects' Null Object:

```json
{ "id": "rig", "content": { "kind": "empty" }, "transform": { "position": [200, 150] },
  "animations": { "rotation": { "keyframes": [
      { "time": 0, "value": 0, "easing": "ease_in_out" }, { "time": 2, "value": 90 } ] } } },
{ "id": "a", "parentId": "rig", "transform": { "position": [120, 0] },   "content": … },
{ "id": "b", "parentId": "rig", "transform": { "position": [0, 120] },   "content": … }
```

An empty occupies no area, so it is a POINT — which changes the rule above in the way you want:
its children's positions are measured from the empty ITSELF (a child at `[0, 0]` sits on it), and
turning or scaling it swings them around it. It carries no `effects`, `looks`, `mask` or
`blendMode` — there are no pixels for those, so authoring one is an error rather than a no-op.

Query the parent and child at rest and during travel; use `translation` only while their sizes and
rotations remain fixed. A cycle, self-reference or unknown parent id is invalid.

## A focus pull, and a card that turns

Blur and flip are effects rather than transforms, so they compose with motion instead of competing
with it. The preset/look choices, checks, stacking behavior, and wipe
construction live in [references/focus-flip-and-wipe.md](references/focus-flip-and-wipe.md).

## A wipe

Nothing about a transform can hide half a layer, so a wipe is a mask. Prefer a wipe look when it
must stack with other masks; a layer has only one direct `mask` field. See the linked reference above
for role slots, directions, reveal presets, checks, and look ordering constraints.

## Drawing a line on

A stroke that appears to be *drawn* — a line, an underline, a checkmark, an arrow, a progress bar — is
one mechanism: a `shape` whose `trim` item is animated. `trim.end` 0 → 1 reveals the stroked path
progressively. Order the items `[path, trim, stroke]` — the trim modifies the geometry before it, the
stroke paints the trimmed result:

```json
{ "kind": "shape", "items": [
  { "type": "path", "closed": false, "vertices": [ { "point": [-400, 0] }, { "point": [400, 0] } ] },
  { "type": "trim", "start": 0, "end": { "keyframes": [
      { "time": 0, "value": 0, "easing": "ease_in_out" }, { "time": 1.2, "value": 1 } ] } },
  { "type": "stroke", "color": "#5b6cff", "width": 18 } ] }
```

This path authors an 800px line with a 1.2s reveal. The four
"variants" are the SAME trim track — only the path geometry and stroke change: a 3-point `V` polyline
is a checkmark, an arrow-shaped path an arrow, and a fat round-capped stroke over a dim full-length
twin is a progress bar (the twin is a second layer with no trim — the track, drawn first so the bright
fill lands on top). `ease_in_out` reads hand-drawn; `linear` reads mechanical, right for a progress
bar. This lives at the shape-`items` level, which layer presets don't reach, so it is a pattern rather
than a preset. Preview the start, partial stroke and completion; verify the intended path direction.

An ink line that writes on — a signature, a doodle, a character's outline — is the same trim track with a
tapered stroke (`character-rigging`, `references/rig-act.md` "Ink lines"). The taper is laid along the drawn part, so the moving
end keeps its point as it writes on.

## Cartoon fast motion: smears, multiples and speed lines

A dash, a fast wave or a zip exit reads as a cartoon when its fast frames are drawn differently. The
`smear`, `multiple` and `speed_lines` motion presets read the layer's real motion and draw only above a
speed threshold, along the motion. Which layer each goes on, frame counts, the exit zip and how they
combine with motion blur are in [references/cartoon-fast-motion.md](references/cartoon-fast-motion.md).
