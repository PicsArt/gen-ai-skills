# Tone-on-tone flat

One warm salmon world drawn with no outlines: skin, floor, furniture shadows and the car are all shades of the
background, so edges come only from steps between fills. Two cool notes (a sky blue and a near-black ink) carry
the people and the furniture. Big disc heads sit on small bodies with thin noodle limbs, and the faces act with
the eyes alone. Scenes change by a camera slide.

## Finish

No film or paper look and no stepped rate: motion is smooth tweens on ones. A scene change is a camera slide (see
Motion habits). A frame is finished when no edge in it is drawn with a line.

## Palette

Measure the reference's frames first (the `reference-fragment-matching` skill, "Measure the
reference before drawing anything"); the numbers below came from sampling and hold for an invented cast too.

- World: background `#ff8c8e`; skin `#fca7a8`; darker skin `#ee797b` and `#d9666b`; floor line `#f27b7e`;
  plant and car `#f26467` and `#fd6767`; shadow `#e57172`.
- Cool notes: sky blue `#8dd3fd` with `#a6dcfc` and `#6db7e6`, a pale belly `#d3ecfb`, near-black ink `#241112`.
- White is for the whites of eyes, picture frames and a pot; grey `#9a9293` for thin furniture legs.

Preview frames are tagged Display P3 and some encoders ignore the tag, so check an encoded clip's background against
`#ff8c8e` before you call the colour right.

## The medium

- **No outlines, no gradients, no shading.** A shape is one flat fill; a shadow is a flatter, darker salmon shape.
- Furniture is black slabs on thin grey legs; a car is a long flat slab with a raked tail and black wheels in a
  pale ring. Props never carry a line.
- Everything is on ones with eased tweens; do not step it.

## The character

Drawn from the style's own shapes, not a generated sheet (the mechanism, saving and talking are in
[shapes-character](shapes-character.md)); build once, save once to the library, place it by its `uri` in every shot.
Two are saved, a person and a bear, each a 900x1000 scene (hip at x 450, soles at y 1000) so a raised arm stays
inside the asset.

- **Proportions:** a disc head about a third of the height on a small rounded-box body: very big head, small body.
- **Limbs:** thin noodle limbs, each made of two pieces of the same width and the same colour with round ends
  (upper and lower, a forearm that ends in the limb's own round hand), so the joint shows no seam. The limbs
  are rooted inside the body's silhouette in the body's own tone, so no end cap shows at the shoulder or hip and
  no line crosses a join; at rest each arm angles a little outward so it reads against the body.
- **Face:** two almond or disc eyes, a pupil that slides, a lid patch, a heavy lid line, small brows. The eye rules
  are in outline-free-faces (the `character-rigging` skill, `references/outline-free-faces.md`): the pupil is a chord slice
  of the eye so it never leaves it, the lid patch slides fully out of the way when open, and the brows and lid line
  sit above the patch. Brows are short and darker than the skin, inner ends raised for worry.
- **Dials:** `spineLean`, `headTurn`, `blink` (lid patch down), `lookX` (pupil slide), `browWorry`,
  `{left,right}UpperArmRaise`, `{left,right}LowerArmSwing`, `stride`.
- **Acting:** small. One look, one blink, a brow lift, a lean, one arm. Faces are small, so let the body lean and
  the eyes move; hold a look for a second before the next.

## Motion habits

- **Camera slide for a scene change.** Put each scene in a composition layer and slide the old one out while the
  next slides in (about a second, eased). A composition content layer with no `composition` field shares the parent
  space but its origin is its centre, so key its position from the canvas centre
  (the `scene-animation-reference` skill, "Held drawings").
- One action per beat; the eyes lead and the body follows a beat later.
- Time numbers go into generated expressions in parentheses (the `scene-animation-reference` skill,
  "Expressions").

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. No outline anywhere; every edge is a fill step.
2. Only two cool notes (blue, ink) against the salmon; white only in eyes, frames and the pot.
3. Brows and lid lines are visible at rest and never under a lid patch.
4. The hand is the limb's own round end; no seam or blob at an elbow or knee.
5. A pupil never leaves its eye in any look.

## Build with the tools

Each scene is a back-to-front stack: background, floor line, furniture, props, then the characters as `scene_ref`s
of the saved assets (`fit` `none`, `anchor` `[450, 1000]`, soles on the floor line) keyed by their dials. Validate,
then look at a frame at every beat, and open the preview in the scene editor.

## Do / don't

- **Do** keep every shape a flat fill and let the tone steps do the drawing.
- **Don't** add an outline, a gradient or a drop shadow, a third cool colour, or long black angry brows.

## Originality guard

Invent the people, the animals, the rooms and the words. Never imitate a known film, its maker or its characters,
and never name one in a prompt. The one warm world, the no-outline fills, the big-headed noodle cast and the
camera slide are the style.

## Proven on

A room with a person and a bear and a scene beside a car with the same two (look, blink, brow lift, lean, a
waving arm, a shrug), each 16:9 and 6 s and previewed locally; and, in the earlier reference-matched proof, a
room-to-car camera slide.
**Not proven, so not in this recipe:** car squash and lean while it drives, smeared wheels, close-ups, walk
cycles, sitting.
