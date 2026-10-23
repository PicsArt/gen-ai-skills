---
name: screen-recording-layouts
description: Lay a screen recording out in a 1080x1920 vertical frame or a 1920x1080 landscape one - the layout catalog (full frame, prompt over result, head and screen, screen with head bubble, results grid), recording panels, whether a moment's UI will read in its panel, and each destination's safe zone. Use when composing a vertical or a 16:9 video from screen footage, landscape, portrait or square.
user-invocable: false
---

# Layouts for a vertical frame

A desktop recording is landscape; the reel is 1080×1920. Do **not** cover-crop the whole screen and
zoom into it — at cover scale the UI is already enlarged, and any emphasis zoom on top reads as "too
much zoom". Instead, put the recording in a **panel** that frames the part of the screen that
matters (usually the content column), and use the rest of the frame for what the viewer needs to
read. A recording that is already portrait or square is laid out differently, as the last section
says.

| Read this | Before you |
|---|---|
| `references/landscape.md` | lay a recording out in a 16:9 frame, 1920×1080, rather than the vertical one |

Pick one layout per beat. Vary them — a promo that uses one layout for every step feels like a
slideshow; switching between two is enough.

| Layout | Use for | Frame (1080×1920) |
|---|---|---|
| **Full frame** | The hook; an outro on camera; every beat of a portrait recording | The presenter's clip, `fit: "cover"`; a portrait recording as the last section says |
| **Prompt over result** | A step that is a typed request and its answer (chat UIs, AI tools, search) | Captions at y ≈ 290, just below the band the platforms cover, a prompt bubble under them (≈ y 340–550), the recording panel below (1000×1280 at y 600–1880) |
| **Head and screen** | A step the presenter explains; the handoff out of the hook | The presenter band on top (1080×760, face in its upper half), the recording panel below (1000×1080), captions on the seam between them |
| **Screen with head bubble** | Steps where the screen needs the most room but the presenter stays present | The recording panel full height, a round presenter bubble in a corner (the ai-presenter skill) |
| **Results grid** | The end card: every result side by side | 2×2 cells (470×700, 24 px gaps), each a panel on its own result, then the call to action under the grid |

**Prompt over result is the typing beat.** Typing is the most engaging thing a chat-style recording
has, so re-type the user's prompt large instead of hoping the viewer reads the tiny input box: the
bubble is a `shape` layer (`rect` + `fill`, `roundness` ≈ 44, a fill one step lighter than the
background) faded in over 0.2 s with `opacity` keyframes (the fade presets do not apply to a shape
layer), and the prompt is a `text` layer on it whose `content.text` is a list
of lines (wrap at ≈ 30 characters for 42 px; there is no wrap box) and whose
`content.animations: [{ preset: "typewriter", params: { duration: 0.9 } }]` types it out. Start the
text 0.1 s after the bubble; in this beat the voice line starts with the text, not at
scene-building-basics's usual panel + 0.15 s. Other text entrances
(`slide_up_lines` for the end title, `fade_in_chars`) are in `picsart_scene_capabilities` →
`textAnimations`. `scripts/panels.py` builds the bubble layer, below.

**A panel is a masked media layer.** The recording is `fit: "contain"`, and the panel shape is a
mask on it: `mask: { layer: { id, transform: { position }, content: { kind: "shape", items: [ { type:
"rect", size: [w, h], roundness }, { type: "fill", color: "#ffffff" } ] } } }`. The mask's
`position` is in composition pixels and the rect is centered on it. **Every mask layer id must be
unique across the whole scene** (`s1_mask`, `grid_0_mask` …); reusing one is a
`mask_layer_id_conflict` error. A slightly larger rounded `shape` behind the panel, one step lighter
than the background, gives it a rim so it reads as a card.

**Build the pieces with `scripts/panels.py`.** From this skill's folder, run
`python3 scripts/panels.py <file>` on `{ items: [...] }`, one item per piece: a panel's `mask`, its
`rim`, the prompt `bubble`, or a masked panel to `nest` (below). It prints one result per item, in
order; its docstring lists each item's fields.

**Masks did not render on Dev on 2026-09-30.** Every layer with a `mask`, in exports and contact
sheets alike, failed with `the authored mask carries no clip, so there is no mask layer to
reference`, including a panel that had rendered the day before, unchanged. Unmasked layers
rendered. So did panels clipped by nesting: the panel becomes a `scene_ref` to a nested scene the
size of the panel, placed where the panel is, with the recording inside it framed the same way. A
nested scene clips at its own edge, so its corners are square. The scene editor cannot open a
`scene_ref`, and expanding one that is placed or scaled changes what it draws, so a nested panel
is for rendering, not for REVIEW. It is also softer: on Dev on 2026-09-30, a full-size export of a
nested panel was soft where the same framing on a plain layer was sharp. Before relying on masks,
render one frame with a mask in it. `scripts/panels.py` turns a masked panel into its nested scene,
rebasing track anchors with clip positions and leaving `fit: "none"` clips without bounds.

**Framing a panel on a focus point.** With `fit: "contain"` and no `bounds`, a source is first
scaled by `CONTAIN = min(frameW / srcW, frameH / srcH)`. To show the source at a total scale `S`
(source px → frame px) with source point `F` landing on frame point `C`, set the layer's
`scale = S / CONTAIN` and `position = C − S · (F − srcCenter)`. Pick the rest `S` so the content
column fills the panel width. Not `cover`: it crops the source to its box before `scale` and
`position` apply, so a focus off the source's centre drags the crop edge into the panel as an empty
band (a Blender recording framed left of its centre, 2026-09-30); full-frame clips and backdrops
stay `cover`, where that crop is wanted.

**Run `scripts/framing.py` for the transform; never work it out.** From this skill's folder, run
`python3 scripts/framing.py <file>` with the source's size, the panel, `S` and `F`. Without `S` it
uses the smallest scale that covers the panel, and without `F` the source's centre. The formula
above says what it does, for a host that cannot run it.

**Keep text off bright content.** A white caption over a white result disappears. Captions and
prompts live in the dark bands of the layout, never over the panel; on a portrait source that fills
the frame, over its quiet area on a bubble or a scrim.

## Will it read

Before a moment of the recording is put in a panel, measure whether its UI will read there. **Run
`scripts/readability.py`; never judge it from the full-size still.** From this skill's folder, run
`python3 scripts/readability.py <file>` on `{ source, canvas, panel?, moments }`: per moment, the
`box` the viewer must read (source px), `textPx` (the height of the smallest line they must read,
in source px, measured on a still cropped to the box), `words` (the words of UI in the box) and
`luma` (the box's mean luma, from its event). `canvas` is the style's canvas colour; `panel`
defaults to the prompt-over-result panel.

It fits each box as large as the panel allows and prints, per moment, `textPx` in frame px,
`fill`, `lumaJump`, `reads` and `findings`, then `failing` and `recommend` (`recreate` or `keep`):

| Finding | Means | Threshold |
|---|---|---|
| `text_small` (fails) | the text is too small on a phone, even at the best fit | under 24 frame px |
| `dense` (fails) | more UI words than a viewer reads while the video moves | over 12 words |
| `shape` (warns) | the box is a strip in its panel; the rest is other UI or empty | under 50% of the panel |
| `luma_jump` (warns) | the UI is far brighter or darker than the canvas: the cut jumps out of the style | over 140 of 255 |

A moment that fails is not fixed by zooming harder (the screen-recording-zoom skill): frame a smaller box,
cut it, or redraw it with the screen-ui-redesign skill.

## Safe zones

Every app draws over the video: a caption and buttons at the bottom, a rail of buttons on the right,
a header at the top. Words under them are lost. Each destination has its own zone, as fractions of
the frame:

| Destination | Profile | Keep words out of |
|---|---|---|
| Instagram Reels | `reels` | the top 13%, the bottom 25%, 6% at the sides, and the rail on the right |
| Reels ads | `reels-ads` | the top 14% and the bottom 35%, and the rail |
| TikTok | `tiktok` | the top 10%, the bottom 22%, and the rail |
| YouTube Shorts | `shorts` | the top 10%, the bottom 20%, and the rail |
| A 16:9 video | `landscape` | 5% on every side, the title-safe area |
| Anywhere else | `ebu` | 5% on every side |

**Several places: the strictest holds**, side by side. **Run `scripts/safe_zone.py` to check a
scene; never judge it by eye.** From this skill's folder, run `python3 scripts/safe_zone.py <file>`
on `{ scene, destination }`, with `destination` one profile or a list of them. It prints
`{ ok, findings }`: each text layer that crosses a margin (`outside_safe_zone`) or sits under the
rail (`under_rail`), with how far, and a `fix` that says which way to move it. It estimates a text
box from its words, applies camera depth and each parent's default anchor, and checks geometric
keys before subsampling the remaining grid. Nested canvases clip both estimates and moving
measurements; text masks in `mask.clip` use their owner's playback clock and inherit only the
host's depth, with the enclosing camera on its own clock. Legacy `mask.layer` is also read,
with `clip` taking precedence. When a finding is close,
measure the layer with `picsart_scene_query_layout` and pass its box in `measured`, by layer id.
A visible layer it cannot place (a captions layer, or words moved by an expression or an unknown
clock) is listed in `unmeasured` and `ok` stays false:
measure it on a frame with `picsart_scene_query_layout` and pass its box in `measured`.

## Covering private data

A private box (an email, a key, a customer's name) is covered by an opaque card that moves with
the recording, through every push and pan. **Run `scripts/cover.py` for the card; never place it
by hand.** From this skill's folder, run `python3 scripts/cover.py <file>` with the recording
layer exactly as it is in the scene, the source's size, the `box` in source px, the style's
`surface` as `color`, and `from` and `to`, the scene seconds the box is on screen. It prints one
`shape` layer: add it right after the recording layer, in the same scene (inside the nested scene
for a nested panel, with that scene's size as `frame`). Its keyframes copy the recording's, so it
stays on the box exactly, and it takes a copy of the panel's mask. Cutting the moment, or framing
the box out of the panel, hides it too, and needs no card.

## A portrait or square recording

Read the shape from the source's width and height. A portrait source (a phone capture, or a video
already edited to 9:16) has the reel's shape, so it needs no panel card on a backdrop:

- **It fills the frame.** Keep it `fit: "contain"` and frame it with the formula above, as a panel
  the size of the frame: rest `S = max(1080 / srcW, 1920 / srcH)`, so it covers the frame edge to
  edge. A taller phone capture loses a strip at the top and the bottom (the status bar, the home
  bar); frame on the content so the strip lost is the empty one.
- **The push still applies**, as the screen-recording-zoom skill says, on the full-frame layer, with the
  focus clamped so the frame never shows past the source's edge.
- **Text goes over the source's own quiet area**: a band where nothing changes while the text is
  on screen (an app's empty header, the space under a short list), where no event's box reaches
  in that stretch, as the screen-recording-analysis skill reads them. Put it on the prompt bubble or a dark
  scrim, never straight on the picture. If the source has no quiet band while the text shows, put
  the text at the top on the bubble, and keep the push away from it.

A **square** source fills the frame's width, not its height: one panel the frame's width less the
margins (1000×1000), below the text band (the prompt bubble keeps its place at y ≈ 340–550), with
the band under it for the call to action. It needs no backdrop either: the bands above and below
are the layout's own. A results grid of portrait or square results keeps the grid's cells, each
framed on its result.
