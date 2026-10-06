# Scene assembly — the cut as one track, condensed

The assembly procedure with the film-specific defaults. Self-contained — a
one-off cut of the user's own footage is this same sequence without the
pipeline around it.

## Tool names

Every compositor tool on this server is prefixed `picsart_media_`.

## Procedure per scene

1. **Real URLs only.** Takes come from selects as `https://` URLs already. A user
   file goes through `picsart_drive` (`action: "upload"`, from a `data:` URI) first.
2. **Probe every take** — `picsart_media_probe_media` per URL for exact `width`,
   `height`, `duration`. The assets carry them; guessing produces a
   scene that validates and renders wrong. Skip only if a prior result already
   gave exact numbers.
3. **Author the cut** — one scene, one layer, whose content is a **track**
   holding the shots as `clips` in playback order. Pass it directly — as
   `picsart_media_validate_scene`'s `scene`, as `picsart_scene_editor`'s `scene` — and read the
   exact field set from `picsart_media_get_scene_schema`:

```json
{
  "version": "1.0",
  "composition": { "width": 854, "height": 480, "fps": 30, "background": "#000000" },
  "assets": {
    "sc01_12A": { "type": "video", "uri": "https://…/sc01_12A.mp4",
                  "width": 854, "height": 480, "duration": 8.0 }
  },
  "layers": [
    { "id": "cut", "start": 0, "content": { "kind": "track", "clips": [
      { "id": "sc01_12A", "duration": 7.2, "content": { "kind": "media", "assetId": "sc01_12A",
          "trim": { "in": 0.4, "out": 7.6 }, "fit": "cover", "align": "center" } }
    ] } }
  ]
}
```

   Rules: never set composition duration (it derives from the track);
   an asset's `type: "video"` or the take is treated as a still; every clip
   carries an `id` (the shot's name), the handle a camera move on that one shot
   targets; a clip's `duration` is its window, `trim` is `{ in, out }` on the source; the same
   take twice with different `trim` windows is how a cutaway returns; hard
   ceiling 1920×1920. Transitions are **per seam**, on the track's
   `transitions: [{ between, id, duration }]`, where `between` is the index of
   the clip the seam follows.
4. **Validate** — `picsart_media_validate_scene`. Free; catches schema errors
   that otherwise fail after minutes of rendering.
5. **Review** — `picsart_scene_editor` (the scene editor) on the validated
   scene, passed as `scene` — the parsed document from step 3, with **all** the
   shots in playback order. One editor, never one per clip and never one per
   piece of a cut the user made in it. It plays in the browser and renders
   nothing. When the reply says `edited: true`, its `document` is the scene
   from here on — the user's trims, splits and deletions already applied; apply
   any comment-driven change to it (`picsart_media_patch_scene`, free),
   validate, and reopen if there is something new to watch.

6. **Export** — `picsart_media_export`, `mediaType: "mp4"`. **No credits**,
   but a real GPU render: a failed or abandoned one still costs
   the wait and leaves nothing. Never retry speculatively; never present a
   successful render as an error.

Free, instant look-check before rendering real frames: `picsart_media_query_layout`
(where layers land at time t).
`picsart_media_contact_sheet` renders real frames — **No credits**, costs render
time: target the suspect joins, not all of them.

## Film defaults

- **Within a scene: hard cut** — no `transitions` entry for that seam.
  Continuity is the cut's job; crossfading coverage smears what Stage 6 paid for.
- **Between scenes**: hard cut or `crossfade` 0.3–0.6s. Anything decorative must
  be motivated by the film's grammar, not novelty.
- Draft canvas 854×480 to match 480p drafts; the final canvas (≤1920×1920) exists
  only in `picsart-film-finishing`.
- **The window is the model's cut until the user moves it** (nothing derives a
  window — below). A run generated with handles is longer than its shots on
  purpose: `genSec` (what was ordered) minus the sum of `sec` (what the film
  runs) is material at the run's two ends for the user to trim in the scene
  editor, and it plays until they do. **Do not derive the handle as 2s.** Snapping
  to the model's duration ladder gives more than that most of the time and less
  at the ceiling; the numbers on the run are the truth.

### Where the trim window comes from

**No window is derived.** A run is
split at its delivered cuts, and each shot's window is the model's cut —
`in`/`out` are the `cutTimesActual` either side of it — until the user moves it
in the scene editor. Record `trimSource: "user"` beside a window the user set;
nothing else is written, and nothing automatic ever moves a window.

The one thing that bites silently: **a run-edge crossfade of 0.3–0.6s
consumes 0.15–0.3s from each side**, so if one is used (last resort — see
`../../picsart-film-scenes/references/seams.md`) both points move inward by half the window or
the transition eats designed action. A seam with no `transitions` entry pays
nothing, which is why the default is a hard cut and a window, if ever, is spent
only at a run edge.

## Virtual camera moves — animating the layer's window

A move over an existing clip is the layer's own transform, animated. Two ways,
both free to stage:

**The one-call way — the `ken_burns` motion preset** via
`picsart_media_apply_motion_preset`, with the clip's `id` as `layerId`. Parameters, as the
capability doc declares them:

| Param | Range | Meaning |
|---|---|---|
| `zoom` | 1–2 (use ≤ 1.2) | final scale zooming in; initial scale zooming out |
| `direction` | `in` `out` `n` `s` `e` `w` `ne` `nw` `se` `sw` | `in`/`out` are pure zoom; the compass values add a pan |
| `pan` | 0–500 **composition pixels** | pan distance; ignored for `in`/`out` |

So a slow push-in is `{ zoom: 1.15, direction: 'in' }`; a drift is
`{ zoom: 1.12, direction: 'w', pan: 120 }`.

**The precise way — keyframes** via `picsart_media_patch_scene`, setting the
clip's `animations` (the clip found by its `id`). It is an object keyed by property, each holding
`keyframes: [{ time, value, easing? }]`:

- `scale` — a per-axis `[sx, sy]`, identity `[1, 1]`. A push-in is
  `[{ time: 0, value: [1, 1], easing: 'linear' }, { time: <end>, value: [1.15, 1.15] }]`.
- `position` — **absolute composition pixels** `[x, y]`, for pans and tilts.
- `anchor` — layer-local pixels from the layer's top-left; this is what sets the
  **zoom centre**, so a push-in onto a face anchors on that face.
- easing sits on the keyframe that starts a segment, so the last one carries
  none: `linear` (one steady speed), `ease_in`, `ease_out`,
  `ease_in_out`, `step` (a hard jump — a punch-in is two scale keyframes ~0.1s
  apart, which reads as a cut).

Ken Burns on an animatic still is the same thing on an image layer.

Keep `scale` ≤ ~1.2 — past that the resolution loss shows. The overscan IS the
travel budget: nothing exists outside the source frame, so an offset can never
exceed half the scale-up, or the pan reveals emptiness. Check the framing with
`picsart_media_validate_scene` and `picsart_media_query_layout` (both free), or
one contact-sheet frame at the move's midpoint (**no credits**, costs render time). Staging is free; the
move renders inside the scene's existing export.

**Nothing previews a staged move before it renders.** Staging a move here is
legitimate edit craft — a push on a held insert, a drift across a still — but it
is unsighted, so check it with `picsart_media_query_layout` (free) before
committing to it. A camera-change note is answered with a retake, not a crop.

## Transition quick table

| Want | Use | Window |
|---|---|---|
| invisible | `crossfade` | 0.3–0.6s |
| soft, dreamy | `blur_dissolve` | 0.5–0.8s |
| directional energy | `slide` / `push` | 0.3–0.6s |
| impact | `zoom_through` | 0.3–0.5s |
| camera-whip energy | `movement_camera` (set `flashIntensity: 1`) | 0.6–1.0s |
| hard cut | `""` | — |

`shape_reveal` mattes are 3-second animations — the window must be ~3s or the
effect reads broken. `movement_camera` starts and ends at rest, so it splices
anywhere.

## Join QC checklist (run at every seam)

**First: did the join do what it was written to do?** At a video edge the
outgoing shot ends mid-movement and the incoming shot picks it up from a
clearly different angle (`../../picsart-film-scenes/references/seams.md`); a join where
neither side is moving, or both sides are the same framing, failed at
generation, not at assembly, and no trim repairs it.

Then the continuity list: eye-lines match · action axis kept (or crossed via a
cutaway) · costume/props/hair continuous · light and palette do not jump ·
movement tempo does not lurch · adjacent shots of one subject are not the same
size.

A failing join is fixed by re-order, a cutaway, a trim — or a reshoot order back
to `picsart-film-scenes` when the coverage simply does not exist.

**Weight them, do not just tick them.** The received order of importance
(Murch's, and it is the one professional editors work to) is emotion first, then
story, then rhythm, then where the viewer's eye lands, then screen direction —
and **literal three-dimensional continuity last.** Every item on the list above
sits in that bottom band. So a seam that jumps a prop but lands the beat is a
better cut than a spatially perfect one that kills the moment, and when the two
conflict the beat wins. This matters here more than on set, because our
continuity errors are the ones we cannot fix — knowing they are also the
cheapest to forgive is what stops a film being re-shot over a coffee cup.

**The join is authored upstream.** The mid-movement ending and the new angle
are written into the two shot blocks either side of the edge
(`../../picsart-film-scenes/references/seams.md`, *The video edge*), so a join judged
here was designed before it was generated; a join that fails it is a re-roll of
the take that missed its ending — not a trim.

**How to actually SEE a join** (the checklist is uncheckable from memory):
`picsart_media_contact_sheet` the outgoing clip's last frame and the incoming
clip's first frame (two frames per join — no credits but costs render time, so
spot-check the suspect joins, not all of them), then view both as inline
images and verdict the checklist against real pixels. Fold
these QC frames into the film's time budget. Two fix rounds maximum, then
ship with one honest line (see the skill's bounded-verification rule).
