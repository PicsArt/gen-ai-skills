# Silhouette rhythm

Black shapes on a full-colour field that hard-cuts every bar, with motion built like a drum-machine pattern at
120 bpm: things hop on the beats a pattern marks.

## Finish

No texture; stepping, when wanted, is a nested composition at `fps` 12 under a 24 fps root (see Motion habits).

## Palette

Black `#111014` for every object. Four background colours, one per bar: `#ff5a36`, `#ffc531`, `#2ec4b6`,
`#8f5cff`. **The hero colour is white, reserved for the beat ring and the count marker** and nothing else.

## The medium

- Every object is a pure black shape with no inside detail; the pose carries it. Each character keeps one clear
  silhouette (a head shape, a tail, ears, a hat) so two never read alike.
- Birds on a wire: a head ellipse, a beak triangle, a body ellipse, a tail triangle and two leg strokes. A
  sagging wire is an open path between two poles with a vertical tangent pair; a fence is two rails and 21
  pickets; a cat is a head (two triangle ears and an ellipse), an ellipse body and a stroked tail (14 px).
- The place is the colour field and two or three silhouette props: a wire, a fence, a skyline, a hill. No
  gradients, no outlines. A count line (1 2 3 4) with one dot stepping across it shows the bar.

## The character

Drawn from the style's own shapes, not a generated sheet (the mechanism, saving and talking are in [shapes-character](shapes-character.md)); build once, save once to the library, place it by its `uri` in every shot.

- **Proportions:** about 6 heads tall, one black shape per part.
- **Shapes:** a solid black polygon each for head, body, arms and legs on a bold colour field; no line and no interior detail.
- **Face:** none: no face, no talking.
- **Controls:** drop `blink` and `mouth`; acting is the pose changing on the beat, so key the dials as steps.

## Motion habits

- **Plan the rhythm first**: give each object a pattern string over eight beats (for example `10001000`) and a
  script may turn it into numbers (key times), but the scene itself gets plain keys: a hop is an up-and-down pair
  on each marked beat, a short squash on landing, a lean of about 12 degrees. Six birds, six different patterns:
  the pattern is the choreography.
- **Hard cuts**: four full-frame rectangles, each keyed to opacity 1 for its own bar and 0 otherwise with `step`
  easing, never a fade.
- A beat ring: a white ring scaling up and fading once per beat. The cat's head dips on each beat; its tail
  flicks once a bar.
- Stepping, when wanted, is a nested composition at `fps` 15 (12 under a 24 fps root). Cued layers use `timeMode: "layer"`.

## Type

Only the count, in a condensed display face, about 48 px, in black.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. A subject with a clear silhouette and a pose that acts (head turn, hop, tail flick).
2. The colour field fills the frame; the bar's colour changes with a hard cut.
3. Three or more silhouettes moving on different patterns.
4. White appears on the beat marker only; everything else is black.
5. Every motion is on the same beat grid, so nothing drifts.

## Build with the tools

Write the rhythm table first, then draw. Key every hop from the table; a new object is a new pattern, nothing
else. Check on a contact sheet that the cut frames land on the bar.

## Do / don't

- **Do** keep the camera locked; rhythm is the camera.
- **Don't** add inside detail, gradients or a second silhouette colour.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Rate split: the bar-colour cuts, the beat ring and the count marker run at the root rate; hops may step on twos in a nested composition; a beat is a whole number of frames (12 at 24 fps at 120 bpm) and every key sits on a whole frame.
  - Stop time (optional): freeze on the last beat by ending the silhouettes' keys at that time in their nested composition while the beat ring and count marker keep theirs.

## Originality guard

Birds, a cat and a fence are generic. It must not resemble a known jazz or music-label poster, the silhouette
dancers of a film or title sequence, a recognisable mascot, game hero or logo shape and its pose, or a brand's
silhouette advertising. Invent the characters' silhouettes and the rhythm they play.

## Proven on

The wire-birds-and-cat scene (six birds on patterns, a cat, a fence, four colour bars).
