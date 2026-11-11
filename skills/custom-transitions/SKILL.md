---
name: custom-transitions
description: How to write a new scene transition as an inline JSON definition — the slot contract, the token vocabulary a definition may read, the four mechanisms a transition can be built from, and the frictions that make a plausible-looking definition render wrong. Every rule here was rendered, and the numbers are what was drawn. Use when authoring or reviewing a transition definition, or when a transition renders at the wrong speed, cuts, or is refused by the validator.
metadata:
  category: authoring
  version: '1.0'
  ported-from: transition-authoring 1.0 at 55.75.0
user-invocable: false
---

# Writing a transition

A transition is DATA: a JSON definition, declared inline as a `type: "transition"`
asset. This is what the definition has to say, and what goes wrong.

**Check what already exists first.** `picsart_scene_capabilities({sections:
["transitions"]})` returns every built-in transition with its id, description
and parameters; if one of them does what you need, apply it by id and stop
here. Authoring is for the case where none of them does.

## Incoming continuity contract

This skill defines an already-decided seam; it does not decide what two beats should mean together.
Before writing a definition, require four inputs:

1. the semantic relationship — continuation, replacement, reveal, arrival, interruption, or reset;
2. the intended travel vector, or an explicit decision that this boundary resets it;
3. the visual carrier, when the viewer should be able to follow one;
4. the concrete reason no shipped catalog transition expresses that relationship.

If any of these is still undecided, return to
motion-scene-continuity (fetch with `picsart_scene_recipe`, name `motion-scene-continuity`). Do not invent a custom transition merely
because the adjacent scenes feel disconnected; the representation may instead be one persistent
layer, a hard cut, or an existing crossfade or directional transition.

## The shape of a definition

Two parts: `meta` identifies it, `scene` IS a scene — the same document model as
anywhere else, with two extra powers.

```json
{ "meta": { "id": "crossfade", "displayName": "Crossfade",
            "description": "Linear dissolve from source to destination: the two weights always sum to one, so the background never shows through an opaque pair." },
  "scene": {
    "version": "1.0",
    "composition": { "width": {"$eval":"width"}, "height": {"$eval":"height"},
                     "fps": 30, "duration": {"$eval":"duration"} },
    "layers": [
      { "id": "source", "start": 0, "duration": {"$eval":"duration"},
        "content": { "kind": "slot", "role": "source" },
        "animations": { "opacity": { "keyframes": [
          { "time": 0, "value": 1 }, { "time": {"$eval":"duration"}, "value": 0 } ] } } },
      { "id": "destination", "start": 0, "duration": {"$eval":"duration"}, "blendMode": "add",
        "content": { "kind": "slot", "role": "destination" },
        "animations": { "opacity": { "keyframes": [
          { "time": 0, "value": 0 }, { "time": {"$eval":"duration"}, "value": 1 } ] } } } ] } }
```

That is a complete, shipping transition. The destination ADDS onto the fading
source inside the firing's own canvas, so the weights are t and 1 − t and sum to
one. Two `normal` fades would each let the composition background through: at
the midpoint a red→red crossfade over green read G = 132, a 25% background
share.

The two extra powers:

**`content: { "kind": "slot", "role": "source" | "destination" }`** — a hole
filled at render time with the outgoing clip's last frame or incoming clip's first frame. A
definition never names a clip; it arranges two boundary-frame slots. Exactly one of each role. The
definition animates those supplied frames on its own clock; neighboring clip animation does not
continue live through the transition window. If the seam needs a genuinely live shared object,
keep that object alive outside this slot contract.

**Firing-supplied tokens.** `width`, `height` and `duration` are handed in by the
call site and are NOT declared in `parameters`. Read them as `{"$eval":"width"}`
or inside an expression as `{"$eval": "width / 2"}`.

## What a definition may read

| Source | Declared where | Read as |
|---|---|---|
| `width`, `height`, `duration` | nowhere — the firing supplies them | `{"$eval":"duration"}` |
| Your own knobs | `scene.parameters` | `{"$eval":"softness"}` |
| The selected variant's row | `scene.variants.table.<row>` | `{"$eval":"sweep"}` |

`{"$eval": "..."}` computes over all three. The grammar is small on purpose — it
admits **`min`, `max`, `abs`, `floor`, `ceil`, `round`, `sqrt`, `sin`, `cos`,
`atan2(y, x)`** (angles in radians) and nothing else. There is no `hypot` and no ternary; `and`/`or`/`not` exist for `$when` gates.
The frame diagonal is `sqrt(width * width + height * height)`, so a circle that
must cover the frame from its centre needs a diameter of exactly that.

Names that are refused rather than shadowed: the grammar's own
(`min max abs floor ceil round sqrt sin cos atan2 and or not true false`), the firing-supplied
three, and a variant row's own selector. The check covers EVERY row, not the
selected one — a clean row does not excuse a broken sibling.

## Variants

One definition, many looks. `by` names the selector param; each row's fields join
the scope for that firing.

```json
"parameters": { "variant": { "type": "text", "default": "circle",
                             "enum": ["circle", "star", "bar"] } },
"variants": { "by": "variant", "table": {
  "circle": { "isCircle": true, "isStar": false, "isBar": false },
  "star":   { "isCircle": false, "isStar": true,  "isBar": false } } }
```

Gate whole layers or shape items on a row field with `"$when": "isStar"`. A row
field beats a firing param of the same name.

## The four mechanisms, and what each costs

| Built from | Example | Needs an asset | Fits any `duration` |
|---|---|---|---|
| **Opacity** | `crossfade` | no | yes, by construction |
| **Transform** | `slide`, `diagonal_slide` | no | yes, by construction |
| **Effect** | `blur_dissolve` | no | yes, by construction |
| **Mask — shape layer** | `iris`, `shape_reveal` | **no** | **yes, by construction** |
| **Mask — video/lottie matte** | none shipped (`push`, `splatter` were) | yes, remote | **no — see below** |

The first four animate on the DEFINITION's own clock. Their keyframes are written
at `{"$eval":"duration"}`, so whatever window the author asks for is the window
they fill. Nothing else is needed.

**Prefer a shape mask over a video matte.** It needs no asset, no network,
no external renderer, and it cannot drift out of time with its window. **Never
ship a `.webm` matte:** iOS (AVFoundation) cannot decode WebM, so the incoming
clip just cut in there — which is why `push`, `bubble`, `cubes`, `free_fall`, `kaleida` and `splatter` were removed from the catalogue.
The matte notes below are kept for a matte in a format supported by the intended playback environment.

**Keep a definition cheap enough to play in real time on a phone.** A blur's cost
grows with its radius times the area it covers, and a firing pays it on every frame
of the window. `movement_camera` peaked at a full-frame whip blur, 260 px at 720p, which cost up to ~180 ms a frame at the cut and stalled playback, so it was removed
from the catalogue too. Blur a small layer, or keep the radius low.

`iris` does a circle, a six-point star and a widening bar from one definition:

```json
"mask": { "invert": false, "clip": {
  "id": "iris_mask",
  "transform": { "position": [{"$eval":"width / 2"}, {"$eval":"height / 2"}] },
  "content": { "kind": "shape", "items": [
    { "$when": "isCircle", "type": "ellipse",
      "size": [{"$eval":"width * 1.6"}, {"$eval":"width * 1.6"}], "position": [0,0] },
    { "$when": "isStar", "type": "polystar", "starType": "star", "points": 6,
      "position": [0,0], "outerRadius": {"$eval":"max(width, height) * 1.45"},
      "innerRadius": {"$eval":"max(width, height) * 0.80"} },
    { "type": "fill", "color": "#ffffffff" } ] },
  "animations": { "scale": { "keyframes": [
    { "time": 0, "value": [0.001, 0.001], "easing": "ease_in" },
    { "time": {"$eval":"duration"}, "value": [1, 1] } ] } } } }
```

Measured on a 640×480 frame, `iris`/`circle` at `duration` 0.4, 1.0 and 2.0 gave
the SAME progression every time — 0% / ~5% / 66% / 100% across the window. Circle,
star and bar read 1.1 / 26.9 / 97.0, 1.8 / 45.5 / 100, 1.0 / 26.5 / 100 at
t = 2.7 / 3.0 / 3.3 through a 1s window.

`shape_reveal` is the larger worked example: twenty-one choreographies, with the
geometry written as fractions of `width`/`height` so a circle stays a circle at
every aspect. Its five `wipe_*` rows are the exception: an edge at any `angle`
is drawn in units of the frame diagonal inside a group that rotates by `angle`
and scales by `diagonal / 100`, so it covers every aspect at every angle. Those
rows also supply `lineShape` and `panelShape` for the `accent` layers (a divider
stroke drawn over the blur band, a colour panel under the destination); every
other row supplies them empty, because a body may only read a row key every row
carries. Each variant's row declares its shape tree ONCE, and three layers
draw it with `"items": {"$eval": "shape"}` (the sharp mask, the blur band, and
the band's lagged cut). The lagged copy is that same tree on a later clock:
`"start": {"$eval": "0.22 * duration"}, "timeMode": "layer"`. A later `start`
alone does NOT delay it, because keyframe times are composition seconds by
default. The lagged copy then moved in lockstep and the blur band disappeared.
One more friction it measured:

- **Land the motion before the window ends.** A track keyed to end exactly at
  `duration` on an ease-out is still short of its end pose on the last frame at
  short windows (0.4s). Its blurred band then cleared in one frame. Keying both
  copies to land by `0.9 * duration` left the last frames clean at 0.4s, 1s and 2s,
  and at 24 fps.

**Repeat a mask piece with `$each` over a number.** In a definition, `$each`
may name a whole number N (a parameter or a row field) and makes N copies whose
item is the copy's index. `tile_mosaic` nests `{"$each": "rows", "as": "r"}`
and `{"$each": "columns", "as": "c"}` inside the mask's shape `items`, one
group per tile, each with its own `opacity` keyframes timed from `r` and `c`.
The variant picks the order through numeric row weights (`byRow`,
`byDiagonal`, `byRandom`): a row field is filled at the definition's top scope,
so it cannot read `r` or `c` itself. A fraction or a negative count is refused with `invalid_each`.

The shape vocabulary is `ellipse`, `rect`, `polystar`, `path`, `fill`, `stroke`,
`gradientFill`, `gradientStroke`, `group`, `trim`, `repeater`, `roundCorners`,
`offsetPaths`, `zigZag`, `merge`.

## Frictions

**A shape item discriminates on `type`, not `kind`.** Content is `kind`, shape
items are `type` — they mirror Lottie's own item vocabulary. Getting it wrong fails
with `missing_field` on the item's `type`, listing every tag it could have been. Their
names are also camelCase (`gradientFill`, `roundCorners`, `zigZag`) while the
rest of the format is snake_case.

**The window is CENTRED on the cut and eats `duration/2` out of EACH neighbouring
clip.** A 7.25s transition needs 3.625s of both. Too long for the clips and the
validator refuses the whole document with `transition_window_exceeds_clip`. Size a
transition against the shortest clip it sits between, not against the composition.

**A time-based matte does not fit the window by itself.** A `.webm` or a lottie
plays at 1× from its own zero. Too long a window and the wipe finishes early and
then the matte runs out before the window ends. Too short and it is a hard cut: `splatter`/`blood_drop_1` in a 1.0s
window reached 9.8% and then gained 90 points in a single frame. The fix, which
every matte family carries, is
to map the window onto the matte's own travel time. `lead` is a second row field:
the last source second at which the matte still equals its first frame, so the
window does not spend its opening standing still (`cubes`/`style10` holds for
1.08s of a 1.63s matte, and without `lead` moved only in the last third):

```json
"trim":  { "in": { "$eval": "lead" }, "out": { "$eval": "sweep" } },
"speed": { "$eval": "(sweep - lead) / duration" }
```

`sweep` is a variant-row field holding the matte's active source extent in source
seconds — measure it as the first frame where no more than ~1.16% of the
matte's pixels remain above 0.5 alpha, the rule every shipped matte row
follows. **`speed` is refused
without an explicit `trim`**: time remapping needs a known source extent, and the
renderer cannot probe for one. A matte definition with no `sweep` is refused the same way.

**A matte whose edge travels the full frame in one direction (push) must `fill`;
a shaped matte keeps `cover`; verify at 9:16 as well as 16:9.** `cover` crops a
16:9 matte to its middle 32% on a portrait frame, so `push`'s left/right edge
crossed the visible strip in one matte frame and rendered as a hard cut; `fill`
maps the whole travel onto any frame. A shaped matte (a splatter, a bubble)
would distort under `fill`.

A shaped matte that keeps `cover` pays for it in time instead. A portrait frame
crops the 16:9 matte to its centre, which clears first, so a single `sweep`
finished `splatter`/`blood_splatter_1` at 45% of a 9:16 window and held. Cover-fit
rows therefore carry `sweep_tall` (9:16) and `sweep_square` (1:1) next to
`sweep` (16:9), and the trim end interpolates between them on the frame's aspect:

```json
"out": { "$eval": "sweep_tall + (sweep_square - sweep_tall) * min(1, max(0, (width / height - 0.5625) * 16 / 7)) + (sweep - sweep_square) * min(1, max(0, (width / height - 1) * 9 / 7))" }
```

`speed` is that same expression, minus `lead`, over `duration`. Measure each
value with the same residue rule as `sweep`: the first frame where no more than
the row's 16:9 residue remains, rendering the matte under its own `cover` fit on
a 9:16 frame for `sweep_tall` and on a 1:1 frame for `sweep_square`.

**A splatter matte leaves an edge residue on 16:9.** Stopping at the ~1.16%
threshold leaves ~1–1.6% of the outgoing clip at the frame edges, which drops
out on the window's last frame. That is accepted: holding the matte until it is
fully clear would spend most of the window on an almost-empty tail, and `cover`
crops the residue away on 9:16.

**A mask is an owned clip.** `mask.clip` spans the host layer's window, and its
keyframes count from the host's start. It carries its own `transform`,
`transforms[]` and `animations`, so an animated shape mask animates. A mask that
starts later than its host (a lag matte) puts a `composition` in the clip's
content, with the delayed layer inside it — see `shape_reveal`'s lag mask.

**The non-active part of a clip is its first or last frame.** A transition shows
the outgoing clip's last frame and the incoming clip's first, not live playback
of both. Design the beat around that.

## Verifying one

The definition is data, so the only question worth asking is what the renderer
drew. Validate it with `picsart_scene_validate`, then render full-resolution stills at the
sample times below in ONE call per `duration`:
`picsart_scene_contact_sheet` with `times: [t1, t2, …]` and `resolution` set to the scene's `composition.width` and `composition.height`. Without `resolution` the sheet returns downscaled thumbnails, which are not for judging position. The sheet image scales every frame to fit one picture; to judge full-resolution detail, open a frame's `url`.

Sample ACROSS the window, not at its midpoint: the failures above all look fine
at 50%. For a window `[c - d/2, c + d/2]` take at least `0.0, 0.25, 0.5, 0.75,
1.0` of it, and measure coverage rather than eyeballing — the incoming clip's
share of the frame, frame by frame, is what tells you whether it swept or cut.

If the definition claims duration independence, render the SAME definition at two materially
different `duration` values. If it claims aspect independence, render at 16:9 and 9:16. A
transition tested at one duration or one frame shape may still be useful, but scope the claim to
that tested case. A matte authored for one frame shape is fit onto every other, and a crop can hide
the travel that makes it a transition.
