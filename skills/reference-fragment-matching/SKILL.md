---
name: reference-fragment-matching
description: Rebuild a reference video as a scene one fragment at a time - split the reference into spans where one arrangement holds, take a census of each, measure every beat, build it, then check it against the reference on motion and on appearance until it matches - and join the fragments without tearing their seams. Use when a scene must reproduce a reference clip, or when one part of a recreation does not match its reference.
user-invocable: false
---

# Fragment matching

Two laws:

1. **Measure, don't guess.** Every invented motion or timing has been wrong on its first render.
   Numbers come from the reference's pixels, through the tools, never from imagination.
2. **One fragment at a time.** Split the timeline into fragments and match each one against the
   reference until it holds, then move on. Never tune the whole clip at once.

**What it can rebuild today: flat-background motion graphics** (app and product promos: cards,
bars, chips, chat, grids) **and illustrated templates** (photo or clip slots dressed with stickers,
doodles and cut-out shapes). Live action, kinetic typography, particles, 3D and character animation
are out of reach. Say so before building, rather than deliver a plausible-looking wrong recreation.

The tools here read only a hosted reference. Frames you grabbed yourself carry no reliable times, so
nothing is timed from them.

Read this before you need it:

| File | Read it before you… |
|---|---|
| `references/seams.md` | plan more than one fragment, or join fragments into one scene |

## The loop

1. **Split the reference.** `picsart_media_segment_shots` with the `source` and the window `t0`/`t1`
   returns fragments, each a `hold` (one arrangement holds still) or a `transition` (it changes),
   with a `suggestedStep`: how densely to look at it. Look at a still either side of every boundary
   with `picsart_media_video_stills`: merge a boundary where nothing visibly changes, split a slow
   change it missed. A transition is real content and needs the densest work, never a gap to skip.
   Name each fragment by what happens in it ("the hero card shrinks and docks onto the input bar",
   never "fragment 3"), and work them in timeline order.
2. **Take the census.** Stills of the fragment at its `suggestedStep`. List everything that is
   there, not only what moves: each element's box, its fill or accent colour, its text, its corner
   radius. Motion checks cannot see a missing icon, a wrong accent or absent text, and those are the
   differences people notice first. Per element, also record:
   - **how it changes**: a rigid move, video inside its box, a mask reveal, a fade or twinkle, a flap
     or bend, a small idle motion, or none;
   - **its first and last visible time**, read on stills either side, not guessed from the motion;
   - **what it is tied to**: the container it moves with, or the element that drives its reveal;
   - **the sound** it lands on, when one lands with it.
3. **Measure every beat** on its route (below) with the motion-tracking-from-video skill, and write the **measured beat table**
   before you build any motion: per beat, its start and end time, its start and end extent
   (position, scale, rotation), and the tracking result each number came from. A beat with no row is
   a beat you are about to guess. One agent measured a card's geometry on stills and invented its
   time: it built a 0.225 s, 15% shrink where the reference measures 1.40 s and 67%. The beat it
   tracked over time was the one it got right.
4. **Choose what carries each motion** before you write it. Elements that move because their
   container moves are one composition with the motion on it, never the same keyframes copied onto
   each member, which drift apart. A treatment that appears around an element in place is a look's
   fade, not a second layer. A reveal tied to a moving element takes its edge from that element's
   measured track, never from keyframes of its own.
5. **Build the fragment** as the scene-building-basics skill says, and check it as the quality-review skill says.
6. **Check it against the reference** (below). Fix, and check again, within the fix rounds
   picsart-video-rules allows. Then go on, and say what is still off.

### One route per kind of change

| How it changes | How to measure it |
|---|---|
| rigid move: slides, turns, grows | `picsart_media_track_motion`, each target set up as the `motion-tracking-from-video` skill says |
| video playing inside the box | the same, on the box: its row in the `motion-tracking-from-video` skill's "Choosing targets" table |
| the whole layout whips across | track one rigid element of it; everything else rides that motion |
| a reveal, a fade or twinkle, a flap or bend, a small idle loop, motion blur | as the motion-tracking-from-video skill says under "What the tracker cannot see" |

## Checking against the reference

Export your render of the fragment's window and compare it with the reference over the same
window. Each check answers one question, and none of them alone says the fragment matches:

| Question | Tool | It returns |
|---|---|---|
| Does each element move like the reference's? | the motion-tracking-from-video skill: `picsart_media_track_motion` on both, then `picsart_media_track_motion_diff` | `maxDev`, `meanDev`, `worstT` per element and channel |
| Does the whole frame move the same way: fade or move, direction, order, which area moves when? | `picsart_media_flow_diff` with `a` the reference, `b` your render, `t0`/`t1`, and `fps: "auto"` | a `score` to rank versions, clustered findings to act on |
| Is everything there, in the right colour, size and place? | `picsart_media_inventory_diff` with `a`, `b` and `times`: 3–5 per fragment | missing and extra elements, colour, size, position, text, corner radius |
| Does each element appear and leave the same way? | `picsart_media_video_stills` cropped to the element, the reference's and yours side by side, across its first and last visible times | how a reveal, a fade or an exit plays, which the other checks cannot see |

- **Check every fragment as you build it**, not the clip at the end: a
  fragment that is wrong is cheaper to fix before the next one is built on it.

- **Look at the fragment's density, not a flat rate.** On one clip a hold asked for a still every
  0.42 s and the transition right after it for one every 0.045 s. A flat 8 per second oversamples
  the first 3.4 times and undersamples the second 2.8 times, and the transition is where
  recreations differ. `fps: "auto"` on `picsart_media_flow_diff` scores each fragment at its own
  density.
- **Every inventory run reports one `plate` finding per side, scored 0.** It is the census saying
  which background it measured and what it left out, not a defect: read it, never chase it.
- **Numbers first, pictures second.** A still reads to within dozens of pixels; a tracking result,
  a layout query or a diff is exact. Spend stills on choosing targets, on what a number cannot say,
  and on the final look.
- **A mismatch is usually** a beat measured too sparsely (track it again, denser), the wrong
  carrier (a fade covering a jump in pose that should be one continuous move), or something the
  scene format cannot do. Say the last plainly; never bury a workaround in the scene.

## Rules that bite

- **Never use the reference's own pixels as content.** A crop of the reference's photo in a content
  slot, or a whole frame, makes the appearance check score near perfect while proving nothing: the
  check compares your render with that same reference. Fill content slots with the user's own
  assets, or plain stand-ins, and expect colour findings on their content. A recreation is a document
  that could be re-rendered with other photos. When an element is a masked view of a larger picture,
  build the picture and the mask. Decorations are the one exception: they may be cut from a template
  the user owns (below). Leave those out of the appearance score, since matching them proves nothing.
- **Cutting a decoration out of the reference.** A still one is a cropped still: `picsart_media_video_stills`
  at one time with `crop` set to its box, saved with `picsart_drive_upload` before it goes into a
  scene, since a still sheet is not kept. A still has no transparency, so over anything but a flat
  background it takes its background box with it, unless it goes through `picsart_image_remove_bg`,
  which charges. A moving one is the hosted reference on a media layer, cropped and masked to its box,
  and only over a flat background the recreation keeps: a mask cannot separate it from what is behind
  it, so over a content slot it would carry a moving patch of the original photo across the user's.
  There, redraw it as shape layers, or generate it.
- **A layer's box is two fields.** `transform.position` is a point in composition pixels, top-left
  origin, and the layer's `anchor` lands on it. The anchor is the box's centre for every content
  kind except text, so measure each reference element to its **centre**, not its corner. Its size is
  `content.bounds` (`[w, h]`) on media and nested scenes, and `content.size` on a colour. Media
  without `bounds` fills the whole frame.
- **Text never reflows.** A scene has no wrap and no maximum width, so a long line runs straight out
  of the box around it. Break lines yourself with `\n`.
- **A frame at exactly the scene's duration renders black.** Take stills strictly inside it.
- **The same media URL may fill two boxes as it is.** Never make it unique per use.
- **Keep what you measured**: the fragment plan, the beat tables, the tracking results and the
  checks, so the user can see what you saw.
