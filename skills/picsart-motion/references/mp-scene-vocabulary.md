# mp-scene motion vocabulary — the real, authorable set

This is a **curated index** of the mp-scene motion vocabulary — a fast lookup that pairs each real
preset / look / transition with *when to use it*. The principles in
[`motion-principles.md`](motion-principles.md) tell you *what* to do and *how* to tune it; this
sheet maps that intent onto the format's real building blocks.

> **`picsart_media_get_capabilities` is the source of truth — this sheet is only a guide.**
> The catalogue **grows**: new presets / looks / transitions / motions get added over time. So:
> - **Call `get_capabilities` first and choose from *its* current list** — never assume this sheet
>   is complete or current.
> - If `get_capabilities` returns something **not listed here**, it is still valid — read its
>   description / `appliesTo` / params from `get_capabilities` and slot it by intent using the map
>   below. **Do not limit yourself to this sheet.**
> - If something **here** is missing from `get_capabilities`, it's gone — don't use it.
> - "Don't invent" means: never use a preset/easing absent from `get_capabilities` — *not* absent
>   from this sheet.
>
> Snapshot below: 19 motion presets, 17 transitions, 19 looks, 12 text
> animations, 5 named easings. Treat the counts as indicative, not a contract.

## Layer content kinds — the palette (`get_capabilities` `layerContentKinds` is source of truth)
A scene layer is one of these — reach for the kind the content *is*, never rasterize text/shapes/
vectors into `media`:

| Kind | Use |
|---|---|
| `media` | a photo or video |
| `text` | live text (animatable per char/word/line; font from `picsart_media_list_fonts`) |
| `shape` | vector geometry — gradient fills, strokes, and **animated draw-on strokes** (lines, checkmarks, arrows, progress bars). An SVG icon/logo becomes one via `picsart_media_import_svg_path` (its `d` → `path` items) |
| `color` | a solid / bounded fill (scrims, backings, plates) |
| `composition` / `scene_ref` | a nested scene — group several layers and move/scale/mask them as one |
| `track` | a sequence of clips with transitions between them (a montage/slideshow) |
| `captions` | timed caption text |
| `audio` | an audio track |
| `empty` | a null layer for **parenting** — the "world" rig that carries a pan (see `transitions.md`) |

## Easings (the ONLY named ones)
`linear` · `ease_in` · `ease_out` · `ease_in_out` · `step` — plus a custom **`cubic_bezier`**
(control points `[x1,y1,x2,y2]`). That's it. **There is no `back`, `bounce`, `elastic`, `expo`,
or `sine` easing.** Get overshoot from a preset (`scale_pop`, `spring`), and get a specific curve
(e.g. Material's Standard `(0.4,0,0.2,1)`) by authoring a **custom `cubic_bezier`**, not by name.
Per-keyframe `easing` applies to the segment *leaving* that keyframe.

## Motion presets — 19 (via `apply_motion_preset`)
Each declares `appliesTo` (text / media / color / scene_ref); the tool rejects a mismatch.

| Intent | Preset(s) |
|---|---|
| Enter | `slide_in`, `fade_in`, `blur_in`, `reveal_in`, `flip_in`, `zoom_in`, `scale_pop` |
| Exit | `slide_out`, `fade_out`, `blur_out`, `reveal_out`, `zoom_out` |
| Emphasis / pop | `scale_pop` (single overshoot — cheaper), `spring` (multi-overshoot) |
| Camera (one layer) | `ken_burns` (zoom+pan on media), `zoom_in`/`zoom_out` |
| Camera (whole frame) | `composition.camera` `{ position: pivot, zoom, rotation }` — one transform over *every* layer (`pos → pivot + zoom·(pos − pivot)`); per-layer opt-out via `cameraExempt: true`. Use for a viewport **zoom** of the whole scene — see [`motion-principles.md`](motion-principles.md) §1.4. **Caveat: a pan-only camera (position change, `zoom` unchanged) is a NO-OP in the scene player** — for a pure pan, parent layers to an `empty` "world" layer and animate *its* position instead ([`engine-gotchas.md`](engine-gotchas.md), [`transitions.md`](transitions.md) §"Recipe — the connected-canvas rig"). |
| Ambient / continuous | `float`, `breathe`, `sway`, `glow_pulse` |
| Attention / error | `shake` |

- **`spring`** is a *damped cosine* (params `intensity` 0–1, `settle` 0.5–20, `bounces` 1–40) — **not** a physics solver.
- **`scale_pop`** = one overshoot; prefer it over `spring` when you just want a pop.

## Text animations — 12 (via `apply_text_animation`)
Entrance (play once, per character/word/line): `typewriter`, `fade_in_chars`, `slide_up_lines`,
`flicker_chars`, `drift`, `flicker`, `shake`, `sway`, `throb`, `transform`, `wiggle`.
Ambient (caption decoration only): `hop`. Selectors support `basedOn` character/word/line, start/end
windows, `randomizeOrder`.

## Transitions — 17 (seam `transition` + `transitionDuration`)
`crossfade`, `blur_dissolve`, `slide`, `push`, `zoom_through`, `page_curl`, `card_flip`, `iris`,
`shape_reveal`, `diagonal_slide`, `bubble`, `cubes`, `free_fall`, `kaleida`, `manga_page`,
`splatter`, `movement_camera`. (Remember: for shared-layer pairs, prefer **matched smart-animate**
over any of these — see [`transitions.md`](transitions.md).)

## Looks — 19 (via `apply_look`) + effects — 137 (via `apply_effect`)
Looks (style/treatment bundles): `shimmer`, `light_leak`, `duotone`, `photo_frame`, `social_frame`,
`social_post`, `tilt_3d`, `tilt_reflection`, `reflection`, `reveal`, `vintage_bw`, `rounded_corners`,
`blur_fill`, `clip_path`, `chat_bubble`, `chat_input`, `play_badge`, `selection_chrome`, `vcr`.
Effects (137): color grades / LUTs / blur / stylize / retouch — e.g. `drop_shadow`, `gaussian_blur`,
`film_grain`, `glitch`, `golden_hour`, `neon_cyberpunk`… Resolve the full list from `get_capabilities`.

**Reproduce the design's static treatment from this catalogue — don't fake it or bake it into a PNG.**
A mockup's rounded image corners, drop shadow, blurred backdrop, reflection or colour grade is almost
always a **look or effect that already exists here** — match it by *enumerating* `get_capabilities`
(19 looks + 137 effects), not by assuming it's unsupported and flattening it into the asset. Common
intent → catalogue entry:

| Design shows… | Author it as |
|---|---|
| rounded image/card corners | `rounded_corners` (look) |
| soft/blurred fill behind a subject | `blur_fill` (look) |
| masked to a shape | `clip_path` (look) |
| drop shadow / elevation | `drop_shadow` (effect) |
| glow / neon edge | a glow effect — resolve the id from `get_capabilities` |
| colour grade / filmic tone | the matching colour-grade effect (`golden_hour`, LUTs…) |

**Gradients are the one common treatment *not* in the looks/effects list.** They have their own
tool: **`picsart_media_apply_gradient`** paints a `gradientFill`/`gradientStroke` onto an existing
shape layer (with `rect`/`ellipse`/`path`/`polystar` geometry) and encodes the stops, `alphaStops`,
endpoints and type correctly. For a Figma element, **`picsart_media_import_figma_paint`** converts
its CSS `linear-/radial-gradient(...)` directly (along with its fill and outer box-shadow). The
`gradient-authoring` recipe (`get_recipe`) covers the patterns. Never hand-invent a gradient object.

**Gradient-filled *text* (Figma's `bg-clip-text`) is not a text `color` and not a look.** A live
text layer's `color` is **solid-only** (schema: string/param, `additionalProperties: false`), and
**no look applies a gradient to text** — so a headline whose Figma fill is a gradient (e.g.
`#fbeac9 → #acb8fd`) renders flat if you just pick a mid-tone color. That is a *fill mismatch*, not
a positioning bug — **catch it in the Stage-2 compare against the design's frame image** (a solid where the
design ramps is easy to miss otherwise).

Reproduce it with a **mask** (`get_capabilities` `mask` → `track-mask`, `maskContentKinds` includes
`text`): the visible layer is a full-box **`gradientFill` shape**; the text goes in that layer's
**`mask.layer`** as an alpha matte (it's the stencil — its own `color` is irrelevant). Host and mask
each keep their own `transform`; glyph AA survives the clip, so the ramp shows only through the
letterforms, and it reflows when the string/font changes.

```jsonc
{ "id": "el_headline", "transform": { "position": [Cx, Cy] },
  "content": { "kind": "shape", "items": [
    { "type": "rect", "size": [boxW, boxH] },
    { "type": "gradientFill", "gradientType": "linear",
      "startPoint": [-boxW/2, 0], "endPoint": [boxW/2, 0],   // left→right ramp
      "colorStops": [ {"offset":0,"color":"#fbeac9"}, {"offset":1,"color":"#acb8fd"} ] } ] },
  "mask": { "layer": { "id": "el_headline_mask", "transform": { "position": [Cx, Cy] },
    "content": { "kind": "text", "text": ["Explore Presets"], "alignment": "left",
                 "color": "#FFFFFF", "font": { "family": "<font key or asset id>", "size": 130 } } } }
```

`colorStops` are **`#rrggbb` — no alpha** (a fade is a separate `alphaStops` ramp or the layer
`opacity`); stops are **static**, only the endpoints animate. The **`gradient-authoring`** recipe
(fetch it with `picsart_media_get_recipe`) has the fully worked gradient-text pattern. Baking the headline to a gradient SVG is the fallback **only** when the layer
needs no live-text animation.

## Animatable properties (keyframes via `patch_scene`)
`position` (vec2), `scale` (vec2), `rotation` (deg), `opacity` (0–1); `anchor` (static, not
animatable); `volume` (audio). Keyframes carry `time`, `value`, optional per-keyframe `easing`.
**`position` and `scale` also carry `inTangent`/`outTangent`** → real **arc / spatial-bezier paths**.
All animatable props also accept **Lua expressions** (`{ expression: "…" }`).

## How the principles map to this set
| Principle / need | Author it as |
|---|---|
| entrance (ease-out) | `slide_in` / `fade_in` / `reveal_in` / `blur_in`, or position+opacity keyframes with `ease_out` |
| exit (ease-in) | `slide_out` / `fade_out` / `reveal_out`, or keyframes with `ease_in` |
| matched smart-animate (A→B) | `position`/`scale`/`opacity` keyframes via `patch_scene`, `ease_in_out` |
| overshoot / bounce | `scale_pop` (once) or `spring` (multi) — **not** a "back" easing |
| a specific curve (Material Standard, etc.) | custom `cubic_bezier` control points |
| type-on / kinetic text | `typewriter`, `fade_in_chars`, `slide_up_lines` |
| camera push-in | `ken_burns` or `zoom_in` |
| ambient life | `float` / `breathe` / `sway` / `glow_pulse` (keep under the primary motion) |
| arc path | `position` `inTangent`/`outTangent` |
| stagger / follow-through | **author-managed** — offset each layer's keyframe start times; no primitive |
| parallax depth | **author-managed** — separate layers, smaller position delta on deeper ones; no primitive |
| squash & stretch | **author-managed** — independent `scale` x vs y keyframes; no primitive |

## Not in the format (don't reach for these)
Back/bounce/elastic/expo/sine **easings**; a spring-**physics** solver; parallax, stagger,
squash-stretch **primitives**. Each is either author-managed (keyframes/expressions) or approximated
by a preset above.

---

*Vocabulary sourced from the mp-scene capability catalogue (easings, motion/text-animation/transition/look
presets, effects, animatable properties) and the mp-scene model. `get_capabilities` is authoritative at
runtime.*

*This sheet is a snapshot. Because you always choose from `get_capabilities`, a stale sheet degrades
to a slightly-incomplete guide, never a wrong instruction.*
