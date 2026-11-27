# Silhouette titles

A title poster cut from black on a red field: a big cream moon low on the horizon, a jagged black ridge and pines, a
lone figure with a staff and a dog walking in front of the moon, crows crossing and a chunky stencil word across the top.
Every shape is one flat black except the field, the moon, the word, a deep-red far ridge for depth and the falling ash. It
is a graphic title card and a quiet walking loop, not a paper-cut diorama (that is [cut-paper](cut-paper.md)), not a
lit night scene and not a shadow play (that is [shadow-puppet](shadow-puppet.md)).

## Palette and colour roles

| Role | Colour | Its one job |
|---|---|---|
| field | red `#d42a1c` | the whole ground, kept flat |
| halo | `#e2462f` | a solid ring round the moon, one step lighter than the field |
| moon | cream `#f4e4c1`, two craters `#e8d3a8` | the one light disc, a stage for the figure |
| far ridge | deep red `#8f1810` | the second tone: far hills and one far pine |
| silhouettes | black `#0b0707` | near ridge, pines, figure, dog, crows |
| word | cream `#f4e4c1` | the stencil title, the same cream as the moon |
| ash | cream at 85 % | slow falling specks |

Hero colour: the field red `#d42a1c`. The cream is used for the moon and the word only; black never carries a
highlight, an outline or a gradient.

## The medium

- **Black cut shapes.** Every figure is flat black polygons that read as one shape, with straight, slightly jagged edges: a coat with a
  zigzag hem, a hat with a brim, a mitten hand that wraps a staff. No curves on a silhouette, no inner lines.
- **The ridge and pines are random zigzags** built from a fixed seed (alternating peak and valley, 38 to 46 px apart),
  so the edge looks torn and stays the same on every export.
- **The moon is the stage.** The figure stands in front of it so the silhouette reads in the one place it has contrast
  with a light ground. The dog and the pines sit on the ridge, where black meets deep red.
- **The word is stencil letters:** each letter is a few rects and one slanted polygon, separated by a thin gap
  (about 6 to 18 px, a real cut in every letter: the H's crossbar and the N's diagonal float free) so the stencil bridges read as cut, not as a font.

## Rates

| Held rate | Root rate |
|---|---|
| none | everything: moon drift, pine sway, trot, crows, ash, the word's float |

## Boil

None: the edges are hard and the shapes do not wobble.

## Line width under a zoom

There are no strokes, only fills (the staff is a thin polygon), so a camera push keeps the same edges.

## Motion habits, and the transitions

- Every motion repeats a whole number of times in the 6 s loop: the moon and its halo drift about 10 px once, the pines
  lean under 1 degree once, the figure and the dog take two steps (legs swing 16 to 22 degrees twice, the body bobs 4 px
  twice), the crows flap four times while crossing the frame once at different heights, the ash falls one full height
  once and each letter floats about 7 px once with a small stagger.
- A figure walks in place against a still ridge; nothing travels across the frame except the crows and the ash.
- Nothing fades: the crows and ash wrap around the frame edge, shapes keep their opacity.
- Transitions: a black ridge rising to fill the frame, a moon wipe (the cream disc growing to cover the shot), a
  word cut away letter by letter.

## Type

One chunky word, four to five capital letters, as stencil shapes, never a font, in the cream of the moon, set across the
top third. Any small line is a short phrase in the same cream, plain and wide.

## Scene features used

Hints, not rules: the look needs flat fills only, so any way of drawing filled polygons works (check `picsart_scene_capabilities` for shapes and
expressions). The proof used shape layers with `fill` only and expression tracks over whole cycles of the loop; in a
shape layer an earlier item draws on top of a later one.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. The first and last frames match: nothing jumps at the loop point.
2. Every silhouette is the same black with straight jagged edges; no gradient, outline or highlight on black.
3. The figure stands against the moon, with a hat, a coat with a ragged hem, a staff held in a mitten hand and legs
   that step; the hand wraps the staff at 2x.
4. The word is cream stencil on the red, clear of the moon and the figure.
5. Only the field red, the deep red, black and cream appear, plus the halo tint and the crater tint on the moon.
6. The crows stay in the red sky and never cover the word.

QC: lean on the loop seam, the viewer's pass at normal speed, and a 2x look at the figure's hand and the stencil gaps.

## Build with the tools (a hint, optional)

Any construction that keeps the look is fine. The proof went back to front: field, halo, moon, far ridge, pines, near
ridge, figure, dog, crows, word, ash. The loop rule holds whatever the construction: write each periodic motion as a `math.sin`
of whole cycles of the loop length, and compare frame 0 with the last frame.

## Do / don't

- **Do** keep black flat and the edges straight and jagged; a ragged hem and a ridge say "cut".
- **Do** put the figure against the moon so the silhouette reads.
- **Do** keep the word the one cream thing besides the moon.
- **Don't** add a second light source, a gradient on a figure or an outline: that is not a silhouette title.
- **Don't** use a font for the word.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Rate split: everything runs at the root rate; nothing is held.
  - Nothing fades: crows and ash wrap the frame, shapes keep their opacity.
  - Height is shadow: none; black shapes are flat, depth comes from the deep red ridge behind.
  - Boil: none.

## Originality guard

Design your own figure, creature, word and wording. It must not copy a known poster, film title or game logo. A red
field, a cream moon, black jagged-cut figures and a chunky stencil word are the style.

## Proven on

A 6 s portrait loop (1080 by 1350, 24 fps): a four-letter stencil word, a
walking figure and a dog against a moon, a torn ridge with about seven black pines and one deep-red one, three crows and 22 specks of ash; exported
locally, not on the hosted renderer.

**Not proven:** the stage editor (not tried), a figure with a face or a second figure close to the first, a camera
push, a longer word, the three transitions (a rising ridge, a moon wipe, a word cut away letter by letter), a landscape frame, a daylight variant and a version where the figure leaves the frame.
