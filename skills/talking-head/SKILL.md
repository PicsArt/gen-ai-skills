---
name: talking-head
description: Put a generated presenter on screen and keep them honest - lip-sync (the face on screen says the audio that plays), one take on the whole step narration, the head bubble and the head-and-screen split, the inputs for the avatar take (the voice is the voice-over skill's), and the presenter's portrait - how to write it and how to check it before a take. Use when a video needs an on-camera presenter made from a portrait photo and a voice.
user-invocable: false
---

# Talking head

A promo where the presenter disappears after the hook loses the human thread. Keep them present in
some of the steps — as the top band of a head-and-screen split, or as a round bubble over the panel.

| Read this | Before you |
|---|---|
| `references/portrait.md` | write the presenter's portrait, or start a take from a portrait |

## Lip-sync

**The face on screen must be saying the audio that is playing.** A talking head over a voice line
it did not speak is visibly out of sync and reads as fake. So:

- If the presenter appears during the steps, generate **one** `kling-avatar` take on the **whole
  step narration** (one voice line holding every step line, the same voice as the hook), and use
  that take for every on-screen step, trimmed to each step's sentence (the transcript's word times
  give the ranges; see the captions skill). The take's own audio is the step voice-over: **unmute
  the presenter layer and add no separate audio layer for that step**. Only one layer plays it at a
  time.
- If the budget covers only the hook take, the presenter does not appear in the steps. Never loop
  the hook take or freeze a frame as a stand-in.
- Price the longer take alongside the hook take. Whether the presenter appears in the steps is the
  user's choice, and the use case asks it.

## The voice and the take

- **Voice.** The voice lines are made as the voice-over skill says. When the presenter appears in
  the steps, the step lines are one line instead (above).
- **Presenter.** An on-camera line is a `kling-avatar` take through `picsart_generate`: one face
  portrait (`imageUrls`) plus that line's voice as the speech audio — the catalog names it
  `audioUrl`, singular and required, so take the exact names from
  `picsart_model_params({ model: "kling-avatar" })` rather than from memory. There is no duration
  parameter: the clip runs as long as its audio, so the line's length IS the clip's length. Quote
  each take with `picsart_preflight`. Before its voice line and portrait exist it may not price;
  then quote it as a paid call whose amount is not known in advance (video-core, SPEND), and never
  generate its inputs to get a number. Keep on-camera lines few: takes are slow and paid.
- **Portrait.** Every take inherits its portrait's flaws, so the portrait passes the check in
  `references/portrait.md` before any take is generated, whether it was generated or uploaded.

## Head bubble

**Head bubble.** The presenter clip, `fit: "contain"`, framed on the face with the layouts skill's
panel formula (scale up so the face fills the circle; `cover` would crop the face away when the
clip is landscape and the face is off its centre), masked with a `rect` whose `roundness` is half its size (a circle; ≈ 300–340 px at 1080
wide), with a 4–6 px rim shape behind it. Place it in a panel corner that the step's focus point
never visits, outside the platform's UI zones (the right-hand action rail and the bottom caption
area on TikTok and Reels) and clear of the caption band. If the focus moves into its corner, move
the bubble to the opposite corner at a cut, never during a zoom. Enter it with a 0.25 s fade and a
scale from 0.85 (the rim is a shape, so fade it with `opacity` keyframes; the fade presets do not
apply to a shape layer); it holds still while the recording zooms, so the eye has one fixed point.

**While masks fail, nest the bubble.** Render one frame of the masked bubble before relying on it,
as the layouts skill says of masks. If that frame fails and the same frame without the mask
renders, clip the bubble by nesting as the layouts skill clips a panel, with a `scene_ref` to a
nested scene the bubble's size, framed on the face. Don't wait for the error to name the mask: on
Dev on 2026-10-01 the masked bubble failed with a generic error about downloading asset URLs, and
the nested bubble rendered and exported. The nested bubble is square (layouts), so give its rim a
`roundness` no more than three times the rim's width, so the square's corners stay inside the rim.

## Head and screen

**Head and screen split.** The presenter band keeps the face in its upper half, eyes near a third of
the band's height; the panel below frames the result. It is the best handoff out of the hook: cut
from the full-frame hook to the split on the next line, and the presenter carries the viewer into
the product.

## Check

Verify every presenter layout with `picsart_media_contact_sheet` before review: the face fully
inside the bubble or band, not cut at the chin, and nothing covering the focus point at the reveal.

Look at every take before it goes into a scene, with frames from its first second, its middle and
its last second, and generate again on any of these:

- the mouth moves while the line is silent, or stays still while it speaks;
- a second mouth, or one that slides off the face;
- a blurred or smeared mouth, or teeth that melt into each other;
- a face that drifts from the portrait's, or eyes that never blink;
- a seam at the jaw or the neck;
- the last word clipped: the take ends before its voice line does.

A generated presenter is AI-made. Say so when you deliver, and tell the user to switch on the
platform's AI-content label when they post the video.
