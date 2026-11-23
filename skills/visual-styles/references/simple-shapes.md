# Simple shapes

The look of our shape-built cartoon rig (`rig-humanoid` and `rig-humanoid-front`), carried into the whole film:
figures and places built from plain primitives (circles, ovals, rounded rectangles, triangles) under one thin,
even slate outline, flat colour and no shading. Unlike [the classic cartoon](classic-cartoon.md), it has no
thick near-black ink, no tapered limbs and no drawn, hand-shaped forms: every part is a primitive, and the
line never changes width.

## Finish

No finish: smooth motion at the scene's own rate, no texture, no film look.

## Palette

Read it from the rig. The outline is slate `#2b2b3a` (the rig's `lineColor`) at the rig's 6 px times the
scale the characters are placed at (4.5 px at 0.75), on the figures and on every prop. Fills are flat,
mid-saturated hues from the same family as the rig's clothes (shirt `#ff7a45`, shorts `#3b5bdb`, sweater
`#7048e8`, skirt `#e64980`, dress `#12b886`, skin `#f6c9a0`): sky `#a5d8ff`, hedge `#40c057`, lawn `#8ce99a`,
trees `#51cf66`, `#37b24d` and `#69db7c`, trunks `#a9714b`, bench `#ffa94d`, path `#ffd8a8`, sun `#ffe066`,
clouds white. **The hero colour is red `#fa5252`, kept for the one object the story turns on** (a ball, a
balloon, a kite). Never reuse a character's clothing colour behind that character.

## The medium

- **Primitives only.** A tree is a circle, an oval or a triangle on a rounded-rect post; a hedge, a bench, a
  house or a sign is rounded rectangles; a cloud is two pills; the sun is a disc. Use `ellipse`, `rect`
  with `roundness` and three-point paths, never a hand-drawn curve.
- **One line, everywhere.** Every shape gets the slate outline at the one width, `lineJoin` round, no taper.
  Overlapping primitives that make one mass (a cloud) put their fills above their outlines, with the outline
  at twice the width, so only the outer edge shows.
- **No shading, no texture, no gradient.** One flat fill per shape; depth comes from overlap and from the
  far shapes sitting higher on the frame.
- Few, big pieces: a sky, a band of hedge or hills, a ground, two or three props. A primitive's detail is a
  second primitive (a window in a house, a ball's highlight bar), never a stroke drawn inside it.

## Characters

No generated sheet: the figure is the shape-built catalog rig, so it never has more detail than primitives (the mechanism for a figure of your own is [shapes-character](shapes-character.md)). Proportions about 7 heads tall with a round head; a face of dots, brows and a mouth the rig's own dials move. Use `rig-humanoid` (three-quarter, for walking across) and `rig-humanoid-front` (front, for facing the
camera), placed as `scene_ref` layers with `fit: none` and the same scale for both, anchored at the sole
(about rig y 1000) on the floor line. Vary a cast with the rig's own dials, not new drawings: `outfit` (front
rig), `hairStyle`, `faceShape`, `headSize` and the colour parameters (`skinColor`, `hairColor`,
`shirtColor`, `pantsColor`, `dressColor`). A girl is the soft face and a hairstyle together (`faceStyle` 1,
`lashes` 1, `blush` 1, a lip colour in `mouthColor`, `hairStyle` 3, 4 or 5, `faceShape` 2, `headSize` 0.8; the
ponytail's bow takes `ribbonColor`, kept off the hero red). Scale a hero to at least 40% of the frame height (0.75 puts the
figure at about 55% of 1080).

They act: a walk in (`walk_cycle` with `steps` and `from` `rest`), a wave, a point at the hero object, and a
reaction for each beat. Their faces are small, so act a reaction with the body too, big enough to read at 1x:
a **startle** is both hands snapped up to the chest (`UpperArmSwing` 0.5, `LowerArmSwing` 0.65,
`UpperArmRaise` 0.2), the head pulled back (`headNod` negative), eyes wide, brows up and the mouth open, held
about half a second, then settled; a **hop** is a crouch (`hipsRaise` about −1.1) 0.12 s before, a flight of
about a tenth of the body's height with both feet tucked (`FootY`), and a squash on landing (a scale of 1.07
wide by 0.9 tall about the feet). On the front rig an arm goes up beside the head with
`<side>UpperArmOpen` (1 is overhead), not `UpperArmRaise`, which folds the hand over the face; a forearm up
beside the head is `<side>LowerArmSwing` negative. Add `random_pulse` on `blink` (a seed per character) and
`breath`.

## Motion habits

- **Ambient life in every frame**: clouds drift a few pixels a second and the sun breathes 3%.
- **The props move like shapes**: the hero object enters on a simple path (a ball bounces in, eased, its
  bounces shrinking, turning as it rolls); nothing in the set wobbles or stretches.
- **The hero object stops on open ground**, in front of the set pieces and clear of every character's feet.
- Smooth motion at the scene's own rate; hold each reaction about a second before the next beat. Keep a
  character's `random_pulse` blink off the beat that is acted.

## Type

Captions only when the plan has words: a rounded geometric sans in the slate colour, on one line at the foot
of the frame.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Every shape on screen, figures and props, has the slate outline at the one width; nothing is unoutlined.
2. Every prop is built from primitives; no hand-drawn curves.
3. One flat fill per shape: no shade, no gradient, no texture.
4. The hero red is only on the story object.
5. Each hero is at least 40% of the frame height, every beat has someone acting, and no hand covers a face.

## Build with the tools

Draw the set as shape layers (sky, a back band with the trees, the ground, the props) from `ellipse`, `rect`
and three-point paths, and the hero object as its own layer. Place the two rigs from their templates
(`picsart_scene_apply_template`, or inline when the presets need to read the rig) and drive them with
`picsart_scene_apply_preset` (walk, gestures, blink) and keyed controls. Check a contact sheet across the whole
clip for the feet on the floor and the hands off the faces.

## Do / don't

- **Do** take the outline width and colour from the rig at its placed scale.
- **Don't** add a thick ink line, a taper, a shade shape or a hand-drawn curve: that is the classic cartoon.

## On a part sheet

When a character comes through the SVG part-sheet flow (the `character-rigging` skill), every arm and leg is two pieces, an upper and a lower, each its own group, overlapping at the elbow or knee. That is a rig requirement no style overrides: the builder refuses a sheet whose limb is one piece. Draw each limb as two primitives, upper and lower, of the same width, overlapping at the joint; the one even slate line runs round the pair, so the joint shows no seam.

## Originality guard

The figures are our own rig; build your own places. Never imitate a known show's or app's flat-shape
characters, sets or palette; primitives under one even line are the style.

## Proven on

The red ball (10 s, 16:9): a boy walks into a park, a girl waves, a red ball bounces in between them, both
startle (hands to the chest, head back), he points at it, and both smile and hop off a crouch with a squash,
under drifting clouds.
