# Cutting views

A video model takes **one image per view**. A sheet with the right panel named in words ("the
rightmost panel") comes back as a face blended from two panels, so a panel pointer is a dispatch
error. Cut the panel into its own file; if it cannot be cut yet, wait.

## Which views

| Asset | Views the cards can need |
|---|---|
| A person you generated | identity (the front face), wardrobe (the full body), profile (the side face) when a card shows it, one per state the cards name |
| A person the user photographed | identity is the photo itself (or its face cut from a copy when it is a composite); profile from the generated profile; wardrobe and states from the approved sheet |
| A prop | the object alone; the scale panel is for the review only |
| A place | the map and the wide, cut when its scene pictures are approved (film-shot-generation) |

Cut only what a card names. One state is one file from one box, passed byte-identical in every run
that names it.

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
  "composition": { "width": 600, "height": 640, "duration": 1, "fps": 30 },
  "layers": [{ "id": "panel",
    "content": { "kind": "media", "fit": "none", "bounds": [2400, 640],
      "asset": { "type": "image", "uri": "<the sheet>", "width": 2400, "height": 640 } },
    "transform": { "anchor": [1800, 0], "position": [0, 0], "scale": [1, 1] } }] }
```

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
  re-cut; never ship a strip.
- `k` above 1 satisfies the floor and sharpens nothing. Ship it so the run is not blocked, and say
  the sheet was too small.

## Check every cut

1. Probe it: its width and height equal the box times `k`, or the anchor or the scale was wrong.
2. Read the **smaller** of the two numbers against the floor. A tall, narrow view fails on its
   width.
3. Look at it: exactly one full view, nothing of the next panel, no
   gutter stripe.

A wrong cut is a re-cut with a corrected box, never a regenerated sheet. Record each view's box in
sheet pixels and its delivered size: when a face drifts, those two numbers are read first.

If a run's references later need a smaller copy of a view, that copy becomes the view: recorded,
and passed by every run after it. Two files behind one state make the model average them.
