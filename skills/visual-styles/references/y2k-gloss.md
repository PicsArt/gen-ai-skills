# Y2K gloss

A turn-of-the-millennium web poster: a violet-to-pink sky, a word in fat gel letters that look wet and lit from above, a
chrome ring tilted round them, soap bubbles rising, a pink jelly icon bobbing and four-point sparkles that twinkle.
Low behind it sits a dusk: a cut orange sun and a perspective grid. It shares a violet-to-pink sky, a bar-cut sun and a grid floor with [synthwave](synthwave.md); what separates it is
the gel type, the ring, the bubbles and the jelly icon, and a sky that is not dark. It is glossy, bright and a little silly, not a night
drive, not a flat poster and not a photograph of glass.

## Palette and colour roles

| Role | Colour | Its one job |
|---|---|---|
| sky | violet `#5a3fe0` at the top, `#9a84ff`, `#ffc2e6` at the horizon | the deeper ground the aqua gel stands out from |
| gel letters | rim `#0f8fd0`, body `#37c9f5`, inner light `#8fe6ff`, glint `#ffffff`, drop `#0a2a6b` at 35 % | the one wet-looking object, built in five passes |
| chrome ring | white, `#8aa0b8`, `#f2f8ff`, `#5b6f88`, white | a metal ring with a hard dark band, behind the word |
| bubbles | white, fill 16 %, rim 75 %, glint 85 % | clear rings, the lightest thing after the glints |
| sun | `#ffe14d` to `#ff7a3d`, cut by bars in the horizon tint `#f6bce8` | a half disc sitting on the horizon, below the word |
| floor | `#c39bff` to `#4a2fb0`, grid `#ff9fe0` at 70 % | a violet plane that rolls toward the viewer |
| jelly | `#ff4fb0`, gloss `#ffffff` at 35 %, base shadow `#b0207f` | the one saturated pink, a squashy icon |
| clouds, sparkles | `#ffffff` | solid clouds that drift, sparkles that twinkle |

Hero colour: gel aqua `#37c9f5`. The jelly's pink is the second voice and the only saturated pink; the horizon and the
grid are soft pink tints, and the sun is orange and yellow, not pink.

## The medium

- **Gel is five strokes on one outline.** From the back: a dark drop (offset 16 px down, width 104, opacity 35 %), the
  deep rim (width 100), the body (80), an inner light (52, nudged 4 px left and 8 px up) and a thin white glint (14,
  nudged 10 px left and 20 px up). The offsets are what makes it read as lit from above. Letters are open round-capped
  paths and an ellipse for the "o".
- **Bubbles** are a faint fill, a thin bright rim and a white crescent near the upper left. No outlines darker than white.
- **The ring** is a `gradientStroke` along its long axis with a hard dark band, tilted a few degrees.
- **The sun** is a half disc on the horizon (330 px across, a vertical `gradientFill`, the floor hides its lower half),
  set below the word so nothing covers it. Its cuts are bars filled with the horizon tint, so the sky seems to show
  through; the cuts thicken as they sink toward the horizon.
- **The floor** is a vertical `gradientFill` slab; the grid's verticals are fixed paths from a point just under the
  horizon to the bottom edge, its horizontals are groups that move down and speed up (`y = horizon + k * u * u`).
- **The jelly** is a rounded square with a pale half-height gloss, a small bright highlight and a thin base shadow.

## Rates

| Held rate | Root rate |
|---|---|
| none | everything: the letters' bob, ring rock, bubbles, sparkles, jelly, clouds and floor |

## Boil

None: edges are clean and the gloss comes from the passes, not from noise.

## Line width under a zoom

The camera does not move. The gel passes are wide strokes, so they scale with the letter if a camera push is ever added.

## Motion habits, and the transitions

- Every motion repeats a whole number of times in the 6 s loop: the letters bob once with staggered phases (a wave runs
  W, O, W), the ring rocks about 3 degrees either side of its tilt once, the jelly bobs once and squashes twice, the
  sparkles pulse in scale twice with a different phase each and turn about 12 degrees once, the clouds cross once, the grid advances twice,
  each bubble rises once, the sun swells 2 % once and its five cut bars sink and thicken twice, a new one born thin at the top as one leaves at the horizon.
- Squash keeps volume: the jelly's x scale goes up as its y scale goes down by the same 5 %.
- Nothing fades: bubbles keep their size and opacity and rise in and out of the frame, sparkles pulse by scale, and the
  gloss never animates its opacity.
- Transitions: a slow slide of the word out with a bubble burst, a gel wipe, a page of bubbles rising over the cut. No
  glitch, no scanlines (that is [vhs-tape](vhs-tape.md)).

## Type

The word is the logo of the poster: three to five lowercase or capital letters drawn as gel paths, never a font. Any
small line under it is a rounded sans in white on the floor, one short phrase.

## Scene features used

How the proof was built, optional: shape layers with groups, open and closed paths, ellipses, rounded rects and `polystar` (four points); `fill`,
`stroke`, `gradientFill` and a `gradientStroke`; group `position`, `rotation` and `scale` driven by expression tracks
(`math.sin` over whole cycles of the loop). In a shape layer an earlier item draws on top of a later one, so author each
layer from front to back.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. The first and last frames match: nothing jumps at the loop point.
2. The gel reads wet: a dark rim, an aqua body, a lighter inside and a white glint, all offset up and left.
3. Saturated pink appears only on the jelly; the sky and grid carry soft pink tints, the sun is orange, and the letters have none.
4. The chrome ring sits behind the word and does not cover a letter.
5. The sun sits below the word, clear of the ring, and its bars keep drifting.
6. Bubbles never cover the glints of the word.
7. The jelly is clear of the word and the ring.

QC: lean on the loop seam, the viewer's pass at normal speed, and the gel against the sun on a contact sheet.

## Build with the tools (how the proof was built, optional)

The proof built each layer from back to front: sky, clouds, sun, sun cuts, floor, grid verticals, grid horizontals, bubbles, ring,
word, sparkles, jelly. Every layer got the same centred transform so shape points were written in composition pixels (any construction that keeps the look is fine).
The loop rule holds whatever the construction: write each periodic motion as a `math.sin` of whole cycles of the loop
length, and compare frame 0 with the last frame.

## Do / don't

- **Do** keep the offsets of the gel passes consistent: one light, from the upper left.
- **Do** keep every motion periodic so the loop has no seam.
- **Do** keep the sky deeper than the gel: aqua on violet, so the letters stand out; the dusk is only at the horizon.
- **Don't** add scanlines, noise or a dark night sky: that is synthwave or vhs.
- **Don't** put a second saturated colour beside the jelly's pink.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Rate split: everything runs at the root rate; nothing is held.
  - Nothing fades: bubbles rise in and out of the frame, sparkles pulse by scale, the gloss is drawn.
  - Height is shadow: the jelly has a thin base shadow; no other piece casts one.
  - Boil: none.

## Originality guard

Design your own word, ring, icon and wording. It must not copy a known logo, a published poster or an operating-system
skin. Fat gel letters, a chrome ring, bubbles, a jelly icon, a violet sky and an orange cut sun are the style.

## Proven on

A 6 s portrait loop (1080 by 1350, 24 fps) of about a dozen shape layers (more is fine): a gel "wow" over a chrome ring and a cut orange sun, a violet
grid floor rolling toward the viewer, drifting clouds, about eleven rising bubbles, about eight sparkles and a bobbing jelly icon;
exported locally, not on the hosted renderer.

**Not proven:** the stage editor (not tried), a title of more than three letters, a photograph inside the gel, a camera
push, a second word, a longer loop than six seconds and a nighttime variant.
