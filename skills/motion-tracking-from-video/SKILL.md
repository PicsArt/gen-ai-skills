---
name: motion-tracking-from-video
description: Measure what objects visibly do in a video - where each one moves, turns and grows, frame by frame - with picsart_media_track_motion, and turn the measurement into scene keyframes; then measure your own render the same way and compare the two with picsart_media_track_motion_diff. Covers choosing targets and estimators, tolerances, reading the result honestly, and placing tracked motion on a layer. Use when a scene must reproduce motion seen in a reference video, or when a render's motion must be checked against one.
user-invocable: false
---

# Motion extraction

`picsart_media_track_motion` recovers what objects **visibly do** in a flattened video: their
position, rotation and scale on every frame, fitted into scene keyframes. It does not recover the
keyframes someone authored. It produces new motion data that reproduces what is on screen.

Looking decides **what** to track. The tracker measures **where**, every frame, to a fraction of a
pixel. Never write a motion's numbers from a still or from memory: every timing and distance comes
from a tracking result.

## Cost and receipts

The tool replies with a job receipt by default: follow it as picsart-video-rules says, and start every
tracking job a step needs before you follow any. Whether it charges credits is in its description;
when it does, it is a SPEND, as picsart-video-rules says. `picsart_media_track_motion_diff` is the same.

## The method

1. **Look at the first frame of the window** with `picsart_media_video_stills`, and choose what to
   track. On a flat background, `{ "auto": true, "max": 9 }` finds the distinct objects at `t0` and
   tracks each, ranked by how much they move. Objects that overlap merge into one, so give those a
   box each instead.
2. **Track.** `picsart_media_track_motion` with the video's `source`, the window `t0`/`t1` in video
   seconds, and `targets`: each one `bbox` (`[x, y, w, h]` at `t0`, in video pixels), `points`, or
   `auto`. Set `tolerance` for the source (below).
3. **Read the result before you trust it.** Per target it returns `animations` (the fitted
   keyframes, or a Lua expression), `static` (the channels that did not move), `meta` with each
   channel's `maxError`, and `notes` on anything that weakened the track. `maxError` is the honest
   reconstruction error: a fit with a large one is an approximation, and you say so.
4. **Place it on a layer** (below), as keyframes with `timeMode: "layer"`.
5. **Check it.** Export your render of the same window, track it with the same targets, and compare
   the two with `picsart_media_track_motion_diff` (below).

## Tolerance, per channel and per unit

`tolerance` is position in **pixels**, `toleranceScale` a **ratio** (default 0.01) and
`toleranceRotation` **degrees** (default 0.5). Never reuse a pixel tolerance for scale: 1.5
"pixels" once declared a 57% shrink static.

| Source | `tolerance` |
|---|---|
| a compressed reference video | about 1.5 (it measures to about 0.5–2 px) |
| your own render | 0.5 or less |

Too tight on a compressed source and the keyframes chase codec noise.

## Choosing targets

- **Start where the object is solid.** During a fade-in its features are weak, the track dies on
  the first frame and freezes. Start `t0` once it is fully opaque.
- **A tight box inside the object's face.** A box over a tilted card in a stack catches its
  neighbours, and the fit mixes two motions.
- **Opaque objects only, for rotation and scale.** A half-transparent object blends with whatever
  moves behind it, and its measured pose drifts toward that. Ghosts, depth-faded cards and
  translucent chrome give approximate motion at best; say so.
- **Video playing inside the box**: the features follow the content, not the box. Set `"estimator":
  "segmentation"` on that target, which tracks the silhouette. Its centre leans toward bright
  content, so a still element of the same group, tracked instead, is more exact.
- **A rotating object takes a box, never points.** A point tracks translation only: a corner
  turning in place reads about 4 px wrong at 30°. A box in `similarity` mode compensates.
- **End the window before the object is covered.** When it slides behind something, its confidence
  falls and its pose freezes. Shorten `t1` and track again, rather than keep the frozen tail.
- **Coming in from off screen**: while the object is clipped by the frame edge, its centre and scale
  are biased. Start once it is fully on screen.
- **Clip the window, not the keyframes.** A fit over frozen samples emits false keyframes at the
  tail. Track again with an earlier `t1`; never prune the keyframes by hand.

| Content | `mode` | `estimator` |
|---|---|---|
| textured (a photo, a UI card with text) | `similarity` | `features` |
| flat or solid, or video inside the box | `similarity` | `segmentation` |
| stretched in perspective | `corners` | `features` |
| position alone matters | `center` | either |

## Reading the result

- **Position is the object's centre**, in the video's own pixels. Under a layer's default anchor
  (the centre of its box, for every content kind but text), that is the layer's
  `transform.position`. Text anchors at its origin: place it by its alignment instead.
- **Rotation and scale are relative to `t0`**: 0° and 1.0 there. The tracker cannot know an
  object's tilt at `t0` from one box: add the pose the layer starts at yourself.
- **Rotation is counter-clockwise positive; a scene's rotation is clockwise.** A turn the tracker
  reports as +12° is `-12` in the scene. Flip the sign of every rotation value you place.
- **Scale comes as `[s, s]`**, because a scene's scale is 2-D.
- **Keyframe times count from `t0`** unless the call set `normalizeTime: "absolute"`.
- **Easing is one of four presets** (`linear`, `ease_in`, `ease_out`, `ease_in_out`), chosen per
  segment as the closest fit. A motion with a sharp snap or a long settle reads close, not exact:
  its `maxError` says how close.
- **An orbit expression** instead of keyframes means the path fit a circle within tolerance. On a
  compressed reference real paths often are not pure circles, and the keyframes it falls back to
  are the honest answer, not a failure.
- **The tracker has no alpha.** It cannot tell a fade from a move. Judge a fade on stills either side
  of it, and never invent one to cover a jump in pose.

## Placing tracked motion on a layer

The result is in the reference's frame and time. A layer needs its own:

- **Time.** A keyframe's layer time is its tracked time, plus `t0` when times count from `t0`, plus
  the scene second where the reference's second 0 plays, minus the layer's `start`.
- **Pixels.** When the scene is not the reference's size, multiply each position by the scene's size
  over the reference's (the same factor on both axes) and add the offset of where the reference's
  frame sits in the scene.
- **Pose.** Rotation: the layer's starting rotation minus the tracked value. Scale: the layer's
  starting scale times the tracked value.
- **Easing**: keep each keyframe's easing where it is; it shapes the segment that starts at it.

An orbit expression is in the reference's pixels and time and cannot be moved by these rules: when
the scene differs from the reference in size, track that object again as keyframes, or place it at
the reference's size inside a composition sized like the reference.

## Checking a render against the reference

Export your render over the fragment, track it with the same targets and the same `mode`, and pass
both tracking results to `picsart_media_track_motion_diff` with the `target` and the `channel`.
It returns `maxDev`, `meanDev` and `worstT`, the time where the two differ most. A number replaces
"it looks about right": tune until `maxDev` clears the threshold the use case sets.

- **Like for like.** The same targets, the same window, the same tolerance on both sides. Your
  render tracked from its own second 0 against the reference from its second 4 is a 4 s offset, not
  a mismatch.
- **What the deviation says.** A constant offset is geometry: a position or a size. A deviation
  that grows and shrinks along a move is easing. One that peaks at a beat's start or end is timing.
