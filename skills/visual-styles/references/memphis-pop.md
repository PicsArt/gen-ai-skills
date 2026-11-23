# Memphis pop

A 1980s-flavoured promo of pastel slabs, squiggles, blobs, rings and terrazzo confetti, every shape outlined in
black and bouncing in with an overshoot, under big stacked words with a heavy outline.

## Palette

Cream `#fff6e9`, ink `#1b1b1b`, pink `#ff8fab`, lemon `#ffd166`, sky `#7bdff2`, mint `#b2f7ef`, lilac `#cdb4db`,
green `#06d6a0`. **The hero colour is the lemon `#ffd166`, reserved for one blob and the second word** so the
loudest word has a loud colour; the other pastels are the field.

## The medium

- Portrait 1080 by 1920 on cream. Shapes: a big sky-blue **slab** with an 8 px ink outline, a **dot grid** of
  36 ink dots, two **zig-zag squiggles** (a straight path with a `zigZag` item, smooth points, 14 px stroke), two
  **blobs** (a polygon with a `puckerBloat` item, 8 px outline), a green triangle and a thick ring (one wide
  coloured stroke under a thin ink one).
- **Terrazzo confetti:** about 70 tiny rounded rectangles in the pastels, scattered by a seeded random
  generator in a script, in one shape layer behind everything.
- Words are stacked: "SUMMER" in white, "POP-UP" in lemon, a date line smaller, all in a condensed heavy face
  with a 10 px ink outline set fill-over-stroke.

## Motion habits

- Every shape **pops in** with a scale from 0 and a strong overshoot (`[0.3, 1.6, 0.5, 1]`, 0.45 s), the
  starts 0.2 s apart; words pop the same way.
- Afterwards each shape keeps a different slow motion: the slab rocks a few degrees, a blob spins, a triangle
  sways. Use the `wiggle` preset at a low frequency on rotations (a different `seed` each), and keep any
  squiggle breathing to a short keyed loop.
- Nothing is still for longer than half a second.
- Cued layers use `timeMode: "layer"`.

## Type

A condensed heavy face, upper case, in white and lemon with a thick black outline; the date is white.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Every shape has the same ink outline except the confetti.
2. At least five different shape kinds on the page.
3. Words are the largest elements and overlap the shapes.
4. Everything pops in with overshoot, then keeps a small motion.
5. Colours are pastels; only ink and white are not.

## Build with the tools

Each shape is its own shape layer with a pop scale key. Add `zigZag` and `puckerBloat` items to the paths; apply
`wiggle` with `picsart_scene_apply_preset` to the shapes' rotation. Script the confetti coordinates.

## Do / don't

- **Do** crowd the page; Memphis is a pattern, not a layout.
- **Don't** use gradients, drop shadows or a realistic photograph; don't align shapes to a grid.

## Originality guard

Compose your own pattern and event. It must not copy a known Memphis-group furniture pattern, a named
designer's textile, or a brand's campaign. The pastel slabs, squiggles and outlined shapes are the style.

## Proven on

The summer-memphis film (a portrait promo with a slab, squiggles, blobs, a ring, terrazzo confetti and stacked
SUMMER / POP-UP / date words).
