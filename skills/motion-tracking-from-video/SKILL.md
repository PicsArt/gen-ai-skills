---
name: motion-tracking-from-video
description: Measure what objects visibly do in a video - where each one moves, turns and grows, frame by frame - with picsart_media_track_motion, work out each move's easing (curve, overshoot, bounce) and turn it into scene keyframes; then measure your render the same way and compare them with picsart_media_track_motion_diff. Covers targets, estimators, tolerances, reading results, and placing tracked motion on a layer. Use when a scene must reproduce a reference video's motion, or a render's motion must be checked against one.
metadata:
  ported-from: motion-extraction unversioned at 55.75.0
user-invocable: false
---

# Motion extraction

`picsart_media_track_motion` recovers what objects **visibly do** in a flattened video: their
position, rotation and scale on every frame, fitted into scene keyframes. It does not recover the
keyframes someone authored. It produces new motion data that reproduces what is on screen.

Looking decides **what** to track. The tracker measures **where**, every frame, to a fraction of a
pixel. Never write a motion's numbers from a still or from memory: every timing and distance comes
from a tracking result. The end points are not enough: a move is matched when it **feels** the
same, so its easing (how it speeds up, slows down, overshoots and settles) is measured too, and
built from the numbers.

## Cost and receipts

Measure every required window with `picsart_media_track_motion` and
`picsart_media_track_motion_diff`, applying picsart-video-rules's SPEND rule to their billing
contracts. Each replies with a job receipt by default: follow it as picsart-video-rules says. Targets that share a tracking window go in one call, as many as
its `targets` schema allows: one `t0`/`t1` holds for every target, and each must be fully visible at
`t0`. A target that enters later, or is covered before `t1`, gets a call with its own window.

## The method

1. **Look at the first frame of the window** with `picsart_media_video_stills`, and choose what to
   track. On a flat background, `{ "auto": true, "max": 9 }` finds the distinct objects at `t0` and
   tracks each, ranked by how much they move. Objects that overlap merge into one, so give those a
   box each instead.
2. **Track.** `picsart_media_track_motion` with the video's `source`, the window `t0`/`t1` in video
   seconds, and `targets`: each one `bbox` (`[x, y, w, h]` at `t0`, in video pixels), `points`, or
   `auto`. Set `tolerance` for the source (below). For a card, photo or title, a `bbox` in
   `"mode": "similarity"` (position, scale and rotation); `"corners"` when it skews or tilts in 3D.
   Leave `fps` out, so it samples at the video's own rate, and run the window over the whole move:
   from the frame before it starts to the frame after it settles, so the easing and the settle are
   in the samples.
3. **Read the result before you trust it.** Per target it returns `animations` (the fitted
   keyframes with their easing, or an expression), `static` (the channels that did not move), `meta` with each
   channel's `maxError`, and `notes` on anything that weakened the track. `maxError` is the honest
   reconstruction error: a fit with a large one is an approximation, and you say so.
4. **Work out the easing** of each move from the dense samples (below).
5. **Place it on a layer** (below), as keyframes with `timeMode: "layer"`.
6. **Check it.** Export your render of the same window, track it with the same targets, and compare
   the two with `picsart_media_track_motion_diff` and their speed profiles (below).

## What the tracker cannot see

It measures where texture goes, frame to frame. Some changes have no texture to follow:

| Change | What to do instead |
|---|---|
| a reveal: a wipe, a mask growing | cropped stills of the box, one per frame of the reveal, for its edge; track whatever drives the reveal |
| a fade or a twinkle | stills either side and through it; the tracker has no alpha (below) |
| non-rigid motion: a flap, a bend, a wobble | track the centre only, and build the shape change as a loop |
| a small idle loop: bobbing, swaying, breathing | track over several cycles, at least one and a half: a sway in rotation comes back as a `sine` expression; build any other loop from the cycles you measured |
| motion blur on a fast move | track it again with `"estimator": "segmentation"`, whose centre stays on the smear, and read it with `fit_motion.py --min-confidence 0.2`; check the smeared positions against cropped stills, one a frame. Each move says how many of its samples were smeared (`blurred`) |

## Illustrated templates

Stickers, doodles and cut-out shapes over a photo or a flat background:

- **A sticker with a white border tracks best with `"estimator": "segmentation"`**: the border is a
  clean silhouette, where its flat fill gives features little to hold.

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
- **Coming in from off screen**: while the object is clipped by the frame edge, a box around it is
  biased. Start at its first visible frame with a box on the textured part already in view (a
  photo's face, not its edge), with `"estimator": "features"`, so the fit follows the content, not
  the clipped outline. `fit_motion.py` then marks the move `startsBeforeWindow`: build the entrance
  from off screen so it crosses the edge at the measured speed.
- **Clip the window, not the keyframes.** A fit over frozen samples emits false keyframes at the
  tail. Track again with an earlier `t1`; never prune the keyframes by hand.
- **A track that is covered, then reacquired.** After the confidence collapses, the later samples can
  be a valid track of the object that replaced it (a card becoming a chip). Check them against a
  still before discarding them.
- **One object, two stretches that need different estimators** (a video inside a card, then siblings
  touching it): track each stretch on its own, with one overlapping frame. The two estimators'
  reference points differ by about 2 px: measure that offset on the overlap frame and subtract it
  when you join them, and multiply the second stretch's scale by the overlap frame's scale.

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
- **Easing is a preset or a fitted curve**, chosen per segment. The closest of the four presets
  (`linear`, `ease_in`, `ease_out`, `ease_in_out`) comes first. When none of them fits within
  `tolerance`, the segment moves and it has enough samples, it gets a fitted curve instead:
  `{"kind": "cubic_bezier", "control": [x1, y1, x2, y2]}`, the scene's own parametric easing, with
  a y outside 0–1 for an overshoot. Copy either form into the keyframe as it came. A short segment
  keeps its closest preset, so a sharp snap or a long settle there reads close, not exact: its
  `maxError` says how close; track it denser to give it a curve.
- **An expression** instead of keyframes means the channel fit one within tolerance: `orbit` (the
  path is a circle) or `sine` (a rotation that sways back and forth, `meta`'s `kind` says which). On
  a compressed reference real paths often are not pure circles, and the keyframes it falls back to
  are the honest answer, not a failure.
- **The tracker has no alpha.** It cannot tell a fade from a move. Judge a fade on stills either side
  of it, and never invent one to cover a jump in pose.

## The feel of each move: easing

The fitted `animations` give each segment's easing, and the report at `resultUrl` holds every
sample (`t`, `x`, `y`, `rotation`, `scale`, `confidence`). Save that report (as a file, where you
run commands) and read each move's timing curve from it:

```
python3 scripts/fit_motion.py moves track.json [--target card1] [--into sheet.json]
```

Per move, on each channel that moves, it gives:
- the target, the channel, `from` and `to`;
- `delay` (from the window's start) and `at` (source seconds), then `duration`, up to the frame it
  settles, and `hold`, how long it rests after;
- `curve`: `linear`, `ease_in`, `ease_out`, `ease_in_out`, or `spring` when it overshoots and
  swings back, named from where its peak speed comes (`peakAt`, 0 to 1) and how far above the mean
  speed it is;
- `cubicBezier`, the curve fitted to the samples (a y outside 0–1 is an overshoot), and `preset`
  when one of the scene's four presets fits about as well;
- `overshoot`, how far past the rest it goes as a share of the travel, `swings`, how many times it
  crosses its rest before it settles, and for a spring its stiffness and damping (mass 1);
- `peakSpeed` and `meanSpeed`, and `staggerAfter`: how long after the previous target's move it
  starts;
- `keyframes` the scene can take as they are: one curve, or for a spring each swing as its own
  segment, since one cubic-bezier holds only one overshoot.

A move out and back, or one that bounces back and forth, comes back as one move per leg; a spring's swings about its rest, each smaller than the last, stay one move however lightly damped. Where it rests is measured from the frames that hold still after it; only when the track ends while it still moves is the rest worked out from its swings. A rotation that crosses ±180° is read as the short turn it is. A slow move
is kept: its start is the last frame within the tolerance of the rest before it. `--into` replaces
every target and channel it measured, so a channel measured still again loses its old move. Track each window of one object under its own target id (`card1_in`, `card1_out`): moves of the
same id and channel from another report are replaced.

Use the tracker's own fitted keyframes and easings where the scene takes them (a preset or a
`cubic_bezier`); take `fit_motion.py`'s keyframes only where it does not, such as a spring with
more than one swing. Either way, the numbers that describe the move come from `fit_motion.py`.
A move it marks `startsBeforeWindow`, or not `settled`, was tracked over too short a window:
widen it and track again.

**Record each move** where the use case keeps the spec: target, channel, from → to, duration,
delay, curve, overshoot, and the tracking result it came from. Never words alone ("slides in").

**Known limits of splitting moves.** Samples alone cannot tell these apart; `fit_motion.py`
reads them as below, and its tests pin it. Look at the stills when one matters.
- A trip whose swings shrink like a spring's, with the track ending before it holds still
  (0→100→30→80, still moving at the end), reads as one spring. Keep a still second after the
  motion in the tracked window, and the measured rest splits it.
- One turn back by less than the travel, then still (0→100→60), reads as one move with an
  overshoot (67 % here), as an ease with a big overshoot would. A turn back past that (0→100→40)
  is two moves.
- A spring that freezes mid-swing and holds there rests where it froze: it may come back as more
  than one move, and the last one ends where it froze.
- A window that opens on the frame the spring is released, with the track ending after two
  turns (still moving), cannot show the spring started from rest: it reads as up to three
  ease moves. Start the window a few still frames before the release, or track it until it
  settles, and it is one spring.

## Creating similar motion

- **Build each move from its numbers**: its from and to, its duration, its curve (the preset, the
  fitted `cubic_bezier`, or the spring's keyframes) and its overshoot.
- **Keep the order and the stagger.** The moves start in the reference's order, each `staggerAfter`
  the one before it, scaled to the scene's time like every keyframe.
- **Match a text animation by its mechanism**, not only its timing: a wipe, letters one by one, a
  line rising, or a mask reveal that follows a moving object (a sticker that wipes the title in as
  it passes). Read the mechanism from cropped stills of the reveal, one per frame, and track the
  object that leads it; then build the same mechanism, with the measured timing.

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

An expression is in the reference's time, and an orbit also in its pixels, so these rules cannot
move it: when the scene differs from the reference in size or timing, track that object again as
keyframes, or place it at the reference's size and time inside a composition sized like the
reference.

## Checking a render against the reference

Export your render over the fragment and track it with **the same box** as the reference: the same
part of the object, the same size against it, at the same moment of the move, with the same `mode`
and `estimator`. The tracker reports the centre of the box you drew, so another box is another
point, and a card tracked by its face against one tracked by its corner reads 150 px apart while
both move alike.

Then measure the deviation with the starting offset removed:

```
python3 scripts/fit_motion.py diff ref-track.json our-track.json --offset <ref second 0 minus ours>
```

Both tracks are read at every sample time of either, over the time both cover. For each channel that changes on either side from the first shared sample (a slow pan too), it gives:
- `startOffset` and `placement`: where ours sits at the first shared sample against the reference;
- `maxDev`: the raw deviation;
- `moveDev`: the deviation once the starting offset is removed, which is the move itself.

The move passes on `moveDev`, within the threshold the use case sets. The placement is the layout:
report it, and fix it when the layout should match. `picsart_media_track_motion_diff` gives the raw
`maxDev`, `meanDev` and `worstT` for the same pair. A number replaces "it looks about right".

**Then check the feel.** A linear move can pass the position check against one that eases. Compare
the two speed profiles:

```
python3 scripts/fit_motion.py compare ref-track.json our-track.json --offset <ref second 0 minus ours>
```

Per move it checks the start, the duration, where the peak speed comes (not when both moves are
linear: a linear move has no peak) and how big it is, the overshoot, the swings and the curve's
name, and says which differ. `speed` writes each target's
speed over time as CSV, to show the two side by side. Fix the measured differences and check
again while each correction makes progress. If the evidence or a tool limit prevents a match,
report the remaining difference with its numbers and cause. ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) whether to accept that
approximation or change the approach; never label it a pass.

- **Like for like.** The same targets, the same boxes, the same window, the same tolerance and the
  same `--min-confidence` on both sides. Your
  render tracked from its own second 0 against the reference from its second 4 is a 4 s offset, not
  a mismatch.
- **What the deviation says.** A constant offset is geometry: a position or a size. A deviation
  that grows and shrinks along a move is easing. One that peaks at a beat's start or end is timing.

## Measuring for a seam

When a seam decision depends on a reference's velocity, path or overlap, the measurement feeds
`motion-scene-continuity` (fetch with `picsart_scene_recipe`). Tracking answers what moved, where
and when; continuity judges what that movement communicates and whether the scene should preserve,
replace, interrupt or reset it. A close numeric fit does not by itself prove a readable handoff.
