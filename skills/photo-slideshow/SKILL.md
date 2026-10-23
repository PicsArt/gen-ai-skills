---
name: photo-slideshow
description: Build a photo promo or slideshow in a scene — probe the photos, sequence them as a track of clips with transitions, fill off-aspect photos with a blurred copy, add an animated title that stays readable over any photo, choose a font, and verify with a sweep of full-resolution frames. Use when asked for a photo slideshow, photo montage, photo reel, promo video from photos, Reels/Shorts/TikTok from pictures, or a titled sequence of images.
metadata:
  category: authoring
  version: '1'
user-invocable: false
---

# Photo promo / slideshow

Assumes the font asset from picsart_scene_fonts (a `live.fonts` entry), and that picsart_scene_patch returns the patched scene you pass to the next tool.

The most common scene job: N photos, one after another, a transition at each seam, a title.
Every value below was validated and rendered at 1080x1920; the whole scene is in
[the worked example](references/worked-example.md).

Related recipes: `picsart_scene_recipe scene-video-edits` owns the track, transition-window and
`blur_fill` detail; `picsart_scene_recipe motion-intent` chooses durations and easing.

## 1. Probe the photos

Call `picsart_media_probe` on every photo URL before authoring. Declare its `width` and `height` on the
asset. Those numbers decide which fit each photo gets (section 3), and they let `blur_fill` skip
its fill on a photo whose aspect already matches the composition.

```json
"p2": { "type": "image", "uri": "https://…/507090463024201.jpg", "width": 2494, "height": 2560 }
```

Compare each photo's aspect (w/h) with the composition's (1080/1920 = 0.5625). `cover` crops
the difference away: 2296x4080 (0.563) loses nothing visible, and a 2:3 portrait such as
2308x3462 (0.667) loses 16% of its width. A square or landscape photo such as 2494x2560 (0.974)
would lose 42% of its width, so it gets a blurred fill instead.

## 2. A track of clips with transitions

One `track` layer holds the photos as clips, back to back. Each seam that should not be a hard
cut gets one `transitions[]` entry keyed by `between`, the index of the gap (0 = between clips 0
and 1):

```json
{ "id": "reel", "start": 0, "duration": 12, "content": { "kind": "track",
  "clips": [
    { "id": "c1", "duration": 3, "content": { "kind": "media", "assetId": "p1", "fit": "cover" } },
    { "id": "c2", "duration": 3, "content": { "kind": "media", "assetId": "p2" },
      "looks": [{ "look": "blur_fill", "params": { "blur": 8, "resFactor": 10, "dim": 0.25 } }] },
    { "id": "c3", "duration": 3, "content": { "kind": "media", "assetId": "p3", "fit": "cover" } },
    { "id": "c4", "duration": 3, "content": { "kind": "media", "assetId": "p4", "fit": "cover" } }
  ],
  "transitions": [
    { "between": 0, "id": "crossfade", "duration": 0.6 },
    { "between": 1, "id": "slide", "duration": 0.6, "params": { "direction": "left" } },
    { "between": 2, "id": "crossfade", "duration": 0.6 }
  ] } }
```

- **Timing.** The track's `duration` is the sum of its clip durations (4 x 3 = 12). A transition
  does not shorten the reel. Its window is centred on the seam, so a 0.6s crossfade at the 3.0s
  seam runs from 2.7 to 3.3.
- **Duration rule.** Each window takes half its duration out of each clip beside it. The halves a
  clip gives up to both of its seams must fit inside that clip, or validation refuses the scene
  with `transition_window_exceeds_clip`. With 3s photos and 0.6s transitions, an inner photo
  still has 2.4s on its own.
- **Choosing a transition.** Read `picsart_scene_capabilities({ sections: ["transitions"] })`. A
  closed-set param lists its allowed `enum` values, and the validator refuses anything else. Keep one
  calm transition, `crossfade`, as the default, and spend a directional one (`slide`) on the seam
  that should read as "next". The rendered example's `slide` `direction: "left"` visibly moves
  through its window.
- **All seams the same?** `mpscene://montage` (`picsart_scene_capabilities`, section `template:mpscene://montage`) binds a clip list
  plus one `transition` id and `transitionDuration` for every seam. Author the track by hand as
  above when seams differ or a transition takes params.

## 3. Cover, or contain with a blurred fill

| Photo aspect vs composition | Clip content |
|---|---|
| Portrait, cover loses under about a fifth of the photo | `"fit": "cover"`. It fills the frame and crops the overflow. Add `align` (`"top"`, …) if the subject sits off-centre. |
| Clearly different (square, landscape) | No `fit`, plus `looks: [{ "look": "blur_fill", … }]`. The whole photo is contained, and a blurred, cover-fitted copy of it fills the margins. |

`blur_fill` with `blur: 8, resFactor: 10, dim: 0.25` renders the fill as an out-of-focus copy of
the photo under a light scrim that separates it from the contained photo. Fine detail softens,
but large shapes stay recognisable: the example's tree trunks still read in the margins. Raising
`blur` to its maximum of 32 halves the fill's edge detail, and the trunks still show. The fill is
a soft backdrop, not an abstract wash. Ranges and defaults are in the `looks`
capability section. A look on a clip is written on the clip itself, as above, and the clip keeps
its transitions.

## 4. The title and its timing

A text layer above the track. Keep the entrance editable as a preset reference in
`content.animations`, or bake it with `picsart_scene_apply_preset` (`textAnimation:<name>`). Both render identically.

```json
{ "id": "title", "start": 0.5, "duration": 2.1, "transform": { "position": [540, 1400] },
  "animations": { "opacity": { "keyframes": [ { "time": 2.3, "value": 1 }, { "time": 2.6, "value": 0 } ] } },
  "content": { "kind": "text", "text": "OUR WINTER",
    "font": { "family": "gilroy-bold", "size": 132 }, "color": "#ffffff", "alignment": "center",
    "animations": [ { "preset": "fade_in_chars", "params": { "duration": 0.8, "stagger": 0.4 } } ] },
  "effects": [ { "id": "drop_shadow", "params": { "offset": [0, 6], "blur": 24, "color": "#000000b3" } } ] }
```

- **An entrance starts at its layer's local time 0.** No text-animation preset takes a delay.
  To reveal later, move the layer: `start: 0.5` begins the reveal at 0.5s. Change `start` and
  `duration` together. Rendered: no ink at 0.5, partial at 0.9, the whole title by 1.3.
- **Layer keyframes are composition seconds.** A layer's own `animations` keyframes (the opacity
  exit `2.3 → 2.6`) are composition time by default, unlike the text preset's clock. The
  validator warns (`keyframe_time_outside_window`) when one falls outside the layer's window.
- **Gone before the first seam, by choice.** The example's title is an opening card over the
  first photo, so it leaves before anything moves under it. The layer ends at 0.5 + 2.1 = 2.6s,
  and the first seam's window opens at 2.7s (0.6s centred on 3.0). Rendered at 2.65: no title
  and no scrim. To keep a title up for the whole promo, give it and its scrim the reel's window
  instead. The scrim then has to hold over every photo, including the brightest (section 5).
- **Wrap at a column you declare.** `wrapWidth: 900` wraps a long title inside the 900px
  between 90px side gutters. Without `wrapWidth` a line wraps at the composition's full width,
  so it can run edge to edge. "OUR WINTER" at 132px `gilroy-bold` draws 776px of ink, one
  line inside 900px.

## 5. Readability over photos

White text over a photo is only as readable as the brightest photo it can sit on. Measured over
the brightest photo in the example (snow; background median luminance 0.59), with white
`gilroy-bold` 132px, against the median background pixel under the title (brighter patches
fare worse). The scrim and plate rows keep the shadow on:

| Treatment | Contrast vs background |
|---|---|
| none | 1.6 : 1 |
| `drop_shadow` `offset [0,6]`, `blur 24`, `#000000b3` | 2.0 : 1 |
| gradient scrim, alpha 0 → 0.6 at the text line → 0.6 at the bottom | 4.0 : 1 |
| backing plate: 860x190 `rect`, `roundness 28`, black `fill` `opacity 0.55` | 4.0 : 1 |

Rules that follow:

- **A shadow defines edges; it does not make text readable on a bright photo.** Keep the shadow
  for crispness, and put a scrim or a plate under any title that can land on a light photo. The
  large-text floor is 3:1, and both treatments clear it.
- **Scrim.** A full-width shape layer beneath the title, with exactly the title's window
  (`start` 0.5, `duration` 2.1) and its own opacity fades at both ends:

```json
{ "id": "scrim", "start": 0.5, "duration": 2.1, "transform": { "position": [540, 1420] },
  "animations": { "opacity": { "keyframes": [
    { "time": 0.5, "value": 0 }, { "time": 0.8, "value": 1 }, { "time": 2.3, "value": 1 }, { "time": 2.6, "value": 0 } ] } },
  "content": { "kind": "shape", "items": [
    { "type": "rect", "position": [0, 0], "size": [1080, 1000] },
    { "type": "gradientFill", "gradientType": "linear", "startPoint": [0, -500], "endPoint": [0, 500],
      "colorStops": [ { "offset": 0, "color": "#000000" }, { "offset": 1, "color": "#000000" } ],
      "alphaStops": [ { "offset": 0, "alpha": 0 }, { "offset": 0.5, "alpha": 0.6 }, { "offset": 1, "alpha": 0.6 } ] } ] } }
```

- **Placement.** A common convention for 9:16 social output is to keep text inside x 90–990 and
  y 250–1540. The example's title ink spans x 153–928 and y 1351–1447.

## 6. Fonts

`font.family` is a NAME. Search the catalog with `picsart_scene_fonts({ query: "gilroy" })` and put a
returned `key` in `font.family`. The example uses `gilroy-bold`, which that query returns and
which is also in the list `picsart_scene_fonts()` gives with no query. Pass `licenseType: "commercial"` to list only faces cleared
for commercial use; personal-licence faces are listed too otherwise.
The renderer has no system fonts, so a CSS name such as `Inter` is refused with
`unknown_font_family`, and the refusal lists the closest keys.

For a face the catalog lacks, the same `picsart_scene_fonts({ query })` call returns it in `live.fonts`. Each entry carries `asset`, a
ready-made font asset: add it to `assets` under an id, and name that id:

```json
"assets": { "display": { "type": "font", "name": "Casual Fonts", "uri": "https://cdn111.picsart.com/230454663055900.ttf" } },
… "font": { "family": "display", "size": 64 }
```

A bare `.ttf` URL in `font.family` also renders, but it loses the font's name.

## 7. Keep the context lean

Author the scene once. Then edit it with `picsart_scene_patch` ops anchored on ids
(`{ op: "set", layer: "title", path: "content/text", value: "…" }`) rather than re-sending the
document. A patch returns the patched scene as `scene`: pass it as the next tool's
`scene` (patch, validate, contact sheet, export). A successful patch has already been validated, so don't validate again until you
hand-edit.

## 8. Verify with one sweep

Ask for the decisive moments in as few calls as possible: `picsart_scene_contact_sheet` with `times: [t1, t2, …]` and `resolution` set to the scene's `composition.width` and `composition.height`. Without `resolution` the sheet returns downscaled thumbnails, which are not for judging position. The sheet image scales every frame to fit one picture; to judge full-resolution detail, open a frame's `url`.
The example has twelve moments, so it takes two calls, both with `resolution: { width: 1080, height: 1920 }`:

```
times: [0.5, 0.9, 1.3, 1.5, 2.65, 3.0]
times: [4.5, 6.0, 7.5, 9.0, 10.5, 11.967]
```

| Times | What they prove |
|---|---|
| 0.5, 0.9, 1.3 | The title's reveal: nothing, partial, whole |
| 1.5, 4.5, 7.5, 10.5 | Clip midpoints: the fit / `blur_fill` framing of each photo |
| 2.65 | Title and scrim are gone before the first seam's window (2.7) opens |
| 3.0, 6.0, 9.0 | Seam centres: each transition is mid-flight, not a hard cut |
| 11.967 | The last frame (`duration − 1/fps`): the reel ends on a photo, not on black |

A seam centre that shows only one photo is a hard cut. Before you re-author anything, check the
transition's `values`.
