# Cutting views

A video model takes **one image per view**. A sheet with the right panel named in words ("the
rightmost panel") comes back as a face blended from two panels, so a panel pointer is a dispatch
error. Cut the panel into its own file; if it cannot be cut yet, wait.

## Contents

- Which views
- Where each view sits (the strip, and an older T-cut sheet)
- Before the first cut
- The cut (the ratio, and padding a view)
- Check every cut

## Which views

| Asset | Views the cards can need |
|---|---|
| A person you generated | identity (the close-up), wardrobe (the full-body front), profile (the full-body side) when a card shows it, back (the full-body back) when a card shoots from behind, one per state the cards name |
| A person the user photographed | identity is the photo itself (or its face cut from a copy when it is a composite); profile from the generated profile; wardrobe, back and states from the approved sheet |
| A prop | the object alone; the scale panel is for the review only |
| A place | the map and the wide, cut when its scene pictures are approved (film-shot-generation) |

Cut only what a card names. One state is one file from one box, passed byte-identical in every run
that names it.

## Where each view sits

A sheet is the strip: four views in one 16:9 row on one flat grey ground, separated by empty
margins, never by lines. Left to right:

| Position | Shows | View |
|---|---|---|
| 1 | full body, front | wardrobe |
| 2 | full body, side, facing right | profile |
| 3 | full body, from behind | back |
| 4 | a large head-and-shoulders close-up, front | identity |

The three full-body views share the left 55% of the frame, and the close-up the right 40%. The
identity view is always the close-up, never the front full-body view: only the close-up holds a
face at a size a run can keep. Save the views as `referenceImages` in the order identity, wardrobe,
profile, back, leaving out any the cards do not need. On every new save, pass
`identityReferences` with the user's original photo URLs, or `[]` if every view was generated.
The first `referenceImages` entry alone does not establish its origin. Keep the saved provenance
when updating or rejecting that version; do not label a generated close-up as an original photo.

**An older sheet is the T-cut** (front face top left, side face bottom left, the full body as a tall
panel on the right, and a fourth tall back panel beside it when it has one). Its saved views stay as
they are, and a re-cut of it reads those boxes: identity is the front face, wardrobe the full body,
profile the side face. Only a new sheet is a strip.

## Before the first cut

1. Cut only after approval, from the approved full-resolution sheet.
2. `picsart_media_probe` the sheet: its real width and height. Never assume the model obeyed
   the grid it was asked for.
3. Look at it (picsart-video-rules, Asset URLs; a smaller export first when it is too large to open) and
   read each box `[x, y, w, h]` from the pixels, inset enough to leave out gutters and neighbours.
4. Do the arithmetic before exporting. The identity view needs about 1024 px on its short side to
   hold a face; a panel under that means the sheet was too small or the grid too dense. Say so and
   fix the sheet before the next character, rather than shipping a soft face.

## The cut

A cut is a one-layer scene whose **composition is the delivered size**, exported once with
`picsart_scene_export`. The sheet sits at native pixels, anchored so the box's top-left corner lands
at the origin, and scaled by one factor `k`:

```json
{ "version": "1.0",
  "composition": { "width": 1024, "height": 1200, "duration": 1, "fps": 30 },
  "layers": [{ "id": "panel",
    "content": { "kind": "media", "fit": "none", "bounds": [2560, 1440],
      "asset": { "type": "image", "uri": "<the sheet>", "width": 2560, "height": 1440 } },
    "transform": { "anchor": [1536, 120], "position": [0, 0], "scale": [1, 1] } }] }
```

That is the identity view of a 2560 × 1440 strip: the box `[1536, 120, 1024, 1200]`, the close-up
from the 60% mark to the right edge, at `k` 1.

- `bounds` and the asset's `width`/`height` are the sheet's probed size. **`content.bounds` is
  mandatory**: validation passes without it and the export then fails.
- `anchor` is the box's `[x, y]` in the sheet's own pixels, and does not change with `k`.
- `k` caps the long side and lifts the short side off the floor:
  `k = max(min(1, cap / max(w, h)), floor / min(w, h))`, then `scale: [k, k]` and the composition
  `[round(w × k), round(h × k)]`. The cap is the long side of the film's video model at its highest
  `supportedResolutions` entry in `picsart_model_catalog`: a reference sharper than the model
  renders buys nothing. It never exceeds the largest side `picsart_preflight` accepts for a
  reference image (6000 px on the long side), and the floor is a margin above the smallest (300 px
  on BOTH sides, so a narrow panel is refused for its width just as a thumbnail is for its
  height). `picsart_preflight` enforces both and names the fix in `errors`; trust its verdict
  over these numbers if they ever disagree.
- `mediaType: "jpeg"` at a quality of at least 85, `startTime: 0`, and a `fileName` such as
  `view_cal_identity_v1`. **Never pass `resolution`**: the size lives in the scene, so the crop
  and the resize are one export.
- **When the two clamps fight, the box is wrong.** A panel so narrow that the floor pushes its long
  side past the cap is a row of panels, a colour bar or a gutter caught in the box. Re-read and
  re-cut; never ship two views in one file.
- `k` above 1 satisfies the floor and sharpens nothing. Ship it so the run is not blocked, and say
  the sheet was too small.
- **The ratio, too.** A video model refuses a picture outside its input ratio before it makes
  anything: width over height from 0.4 to 2.5 on Seedance and MiniMax H3, unless the model's own
  limits say otherwise. `picsart_preflight` measures the sides, not the ratio, and
  `picsart_model_params` does not list it, so check it here, when the view is cut, never after a
  run is refused. A full-body view is tall by design: on the strip each one is about 15% of a 16:9
  frame's width, about 0.27 before the inset, so the cut lands under 0.4. **A full-body view under 0.45 is
  padded when it is cut**, to 0.45 as below, so the wardrobe view any run passes is already inside
  the range with a margin. Pad a view
  outside it in a **second export whose only media is the cut view file** (`w` × `h`, probed),
  never the sheet: a wider frame over the sheet shows the next panels, not a margin. One layer,
  `fit: "none"`, `bounds` and the asset's size `[w, h]`, `anchor: [0, 0]`, `scale: [1, 1]`, and
  `composition.background` the sheet's own backdrop colour (`"#e9e6e1"`, read from the pixels
  beside the panel):
  - **Too tall** (a full-body view under 0.45, any other under 0.4): width `ceil(0.45 × h)`,
    height `h`, `position` `[(width − w) / 2, 0]`.
  - **Too wide** (over 2.5): width `w`, height `ceil(w / 2.5)`, `position` `[0, (height − h) / 2]`.

  The padded file becomes the view. The margin is plain; the person is never stretched, cropped
  or redrawn.

## Check every cut

1. Probe it: its width and height equal the box times `k`, or the anchor or the scale was wrong.
2. Read the **smaller** of the two numbers against the floor. A tall, narrow view fails on its
   width.
3. Divide width by height: from 0.4 to 2.5, and a full-body view at least 0.45, or pad it as
   "The ratio, too" says.
4. Look at it: exactly one full view, nothing of the next panel, no
   gutter stripe.

A wrong cut is a re-cut with a corrected box, never a regenerated sheet. Record each view's box in
sheet pixels and its delivered size: when a face drifts, those two numbers are read first.

If a run's references later need a smaller copy of a view, that copy becomes the view: recorded,
and passed by every run after it. Two files behind one state make the model average them.
