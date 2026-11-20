# Pop-up book

An open book on a table whose paper scenery folds up off the page one piece at a time, seen from one fixed
camera. Everything is a cut piece with a pale paper edge. The shot is a book from first frame to last:
the cover rim, the page's front edge or the gutter are in frame all the time and the open spread fills most of
the frame.

## Finish

A pale paper edge on every piece; anything that wobbles steps on twos (`fps` 12 under a 24 fps root) if the book should feel handmade; no film look.

## Palette

Table `#6b4a35`, cover `#8c3b2e`, page block `#e6dbc0`, page `#f3ead6` with a fold line `#c9b994`, paper edge
`#fffaf0`, sky `#9fd3e6`, hills `#7cb36b`, trees `#3f8f55`, house `#f2c48d` with a roof `#d0573f`, grass
`#5aa05a`. **The hero colour is the fox's orange `#e8833a`, reserved for the one animal** and used on no
scenery. A kite or pull-tab is the one other warm accent, `#f2c14e`.

## The medium

- The table, a cover rim, the page block and the page are flat planes: shape layers with `rotationX` 90, each
  3 px higher than the one under it (a `y` of 566, 563, 560, 557 in a 1280×720 frame), the page two panels
  split by a thin fold line with a faint darker strip either side of it so the spine reads. The cover 20 px
  proud of the page on every side and the block 8 px, so the paper has a thickness at the front edge.
- Each piece of scenery is a shape layer of flat fills with a **5 px paper-edge outline** (`#fffaf0`) and no
  other line. Its `anchor` is `[0, 0]` and its position sits on the page, so it hinges at its base. Give each
  piece its own depth with `z` (sky furthest, then hills, house, trees, back grass, the character, flowers,
  front grass nearest).
- A piece lies flat toward the viewer, on the page, and stands up by animating `rotationX` from -90 to 0 over
  0.7 s with a small overshoot (`[0.3, 1.45, 0.5, 1]`), so it springs past upright and settles. It is
  never gated with `opacity`: lying flat it is the printed picture on the page (see "The pieces are printed on
  the page before they fold up").
- A sky is a rounded arch with clouds in front of it; hills are a closed path with soft tangents; trees are
  three ellipses and a trunk; flowers sit in a row in front of a grass strip.

## The book stays a book

**A spread uses both pages.** The scenery runs across the gutter: every wide piece (sky, hills, grass strips)
is two halves, one per page, hinged on the same band and meeting at the gutter, and the single pieces (house,
trees, a tent) are spread over both pages. A page left blank is a defect.

The camera is the composition's and it orbits a pivot. Give it `rotationX` 20 (**the tilt is at most 32
degrees**: a steeper tilt leaves a wide empty band of table above the scenery and squashes everything that folds
up) and a `zoom` of about 1.06 in a 1280×720 frame (above that the cover's corners touch the frame's sides), so that the open spread with its standing pieces covers **at
least 80 % of the frame's width and 55 % of its height**. Lay the book at `y` about 400 (the page's plane) so it
sits in the middle of the frame, and paint the table as the composition's `background` instead of a plane.
Rules:

1. In every frame the page's front edge with the cover rim, or the gutter, is visible, and the left and right
   edges of the book are inside the frame.
2. **The camera is locked: one framing per spread.** Its only move is one smooth pull-back and push-in through
   a page turn: zoom held until 0.2 s before the leaf lifts, `ease_in_out` down to 0.56 of its value at upright
   (an upright leaf is as tall as the page is wide; its tip then stays in frame), `ease_in_out` back 0.5 s after
   the landing. No other keys, no size jumps. Check it: the corners of the book and of every standing card stay
   on the same pixel, second by second, outside the turn.
3. **A scene changes by a page turn or by the book closing, never by a dissolve inside the book.**

**Draw order.** Layers draw far to near by where each layer's plane meets the camera's centre ray, with no
depth buffer. The centre ray passes through the pivot, so **keep the pivot about 100 px above the page** (`y`
of the page minus 100): the ray then meets the page behind the sky band and every flat plane of the book draws
before every standing piece. A pivot on the page itself (or a table plane under the book) draws the page over
the hills and the sky. Keep the standing pieces within `z` -170 (sky) to 180 (front grass).

## The pieces are printed on the page before they fold up

A piece never appears from nowhere. From the first frame every flat lies face-up on the page, drawn there as
the printed picture (the sky, hills, house, trees, grass), and it folds up on its hinge when its turn comes.

- **One band per piece, none overlapping.** Hinge each flat at the front edge of its band and let it lie behind
  the hinge: sky at the back, then hills, trees and house, then the three grass strips at the front. A piece lies
  only inside its band: measure its height, so a tree (about 100 px lying down) fits between its hinge and the
  band behind, and two trees do not touch. In page depth `z`: sky -120, hills -38, trees 72, house 104, grass 124,
  150 and 176 (front).
- **Lying flat and standing use the same layer.** World flat: `rotationX` 90 lying, 0 standing, hinge at the
  layer's `position`, `anchor` `[0, 0]`. Never gate it with `opacity` (a flat at opacity 0 is the "pieces appear
  from nowhere" defect).
- **Flat layers a hair apart, not coplanar.** Give each flat its own height, 0.5 px above the one before
  (`position` y minus 0.5 per piece). Layers at exactly the same height z-fight when they overlap while the page
  is seen at a slant, and a band that does not overlap still flickers at the edges.
- **Fold up on the `BACK` ease** (a gentle start, a small overshoot at the end:
  `cubic_bezier [0.35, 0, 0.4, 1.3]`). An ease that starts steeply (`[0.3, 1.45, 0.5, 1]`) throws a large
  flat about 20 degrees on its first frame, which reads as a pop.
- **Draw the flowers after the grass blades they sit in**, or the blades hide them while the strip lies flat.
- Check it with numbers: over the first 0.5 s (all flat) the change from frame to frame in each band is under
  1 grey level and has no spike, against 0.2 for the untouched page; and across each rise the frame change
  rises and falls smoothly, no single frame above twice its neighbours.

## A rigged character lives in the book

The character is a `scene_ref` of its rig (see `character-rigging`), made of
the same paper as the scenery:

- **It stands on the page between the flats**, on a depth plane of its own (`z` 10: behind the flowers and the
  front grass, in front of the back grass, trees and house). It never stands on the table or outside the open
  book: keep its `x` inside the page (about 140 to 1140 in the frame above) and its `z` low enough that it lies
  flat on the page, not past its front edge: it is about 270 px long lying down, so `z` 10 on a page that ends at 295.
- **It enters by folding up out of the page on its hinge**, exactly like a flat: anchor at its feet, `rotationX`
  -88 to 0 with the same overshoot, 0.7 s. Use -88, not -90: a rig whose tail follows through cannot evaluate
  a parent that is edge-on. It leaves the same way, folding down with `ease_in` over 0.5 s, and it is hidden
  while it lies flat (below). For a second spread the same rig is a second layer.
- **A pull-tab slot is the other way in**: a flat slit in the page with a tab that slides along it; the
  character stands on a piece that the tab moves.
- **Paper edge.** Two effects on the layer: `stroke` (`width` 5, `color` `#fffaf0`), which follows the
  character's outline, and `drop_shadow` (`offset` `[4, 6]`, `blur` 6, `color` `#00000066`) for the cut paper's
  thickness. A cast shadow on the page is a flat ellipse (a `rotationX` 90 shape at the character's `z`, 150 by
  40 px, `#2a1d12` at 38 % opacity) that follows the character's `x`; it is visible only while the character
  stands.
- **Scale it as the scenery**: about 170 px of the frame for a fox where the house is 215. Move it on the page
  by the distance its gait covers at that scale (a run authored at scale 0.8 for 560 px covers 294 px at 0.42);
  a gait played at another speed slides its feet.
- **An applied gesture or gait lives in the rig's parameters** (keys and an expression with its start time baked
  in), not only in `presetBindings`: to move a point to another moment, rewrite those parameters' times. A rig
  reused for a character that stands still settles out of the gait in its first seconds, so start that layer
  hidden 2 s early and fold it up once it stands.
- A character that is not standing is hidden, never left lying flat on the page. A flat plane meets the camera's centre ray far
  behind the standing pieces, so a character lying flat sorts under the grass strips: keep it at `opacity` 0
  until 0.22 s into its fold-up, and fade it out from 0.32 to 0.40 s into an `ease_in` fold-down: earlier it
  still stands and vanishes in a pop, and later it has sorted under the scenery.

```json
{
  "id": "fox", "start": 3.25, "timeMode": "layer", "duration": 4.375,
  "transform": {"position": [420, 548], "anchor": [646, 1035], "scale": [0.42, 0.42], "z": 10},
  "content": {"kind": "scene_ref", "assetId": "rig", "fit": "none", "blending": "pass_through"},
  "animations": {
    "rotationX": {"keyframes": [
      {"time": 0, "value": -88},
      {"time": 0.3, "value": -88, "easing": {"kind": "cubic_bezier", "control": [0.35, 0, 0.4, 1.3]}},
      {"time": 1.0, "value": 0},
      {"time": 3.9, "value": 0, "easing": "ease_in"},
      {"time": 4.3, "value": -88}]},
    "position": {"keyframes": [
      {"time": 1.5, "value": [420, 548], "easing": "linear"},
      {"time": 3.5, "value": [714, 548]}]}},
  "effects": [
    {"id": "stroke", "params": {"width": 5, "color": "#fffaf0"}},
    {"id": "drop_shadow", "params": {"offset": [4, 6], "blur": 6, "color": "#00000066"}}]
}
```

## Wind

**A card is glued at its fold: once it stands it holds still.** No `rotation` on a flat, and clouds printed on
the sky card do not drift. Wind moves only the light things, big enough to read at 1x:

- **A gust is an amplitude that rises and falls**: `gust = 0.35 + 0.65 * (0.5 + 0.5 * sin(t * 1.57 + ph))`, a
  4 s period, `ph` per item so they do not breathe in unison. Multiply it by a gate that is 0 until the piece
  has stood 0.75 s and back to 0 before it folds down, so nothing moves while it lies flat.
- **Grass is a strip of blades, each a group** with its own `anchor` and `position` at its base, 14 to 36 px
  tall, and a `rotation` of 11 to 14 degrees at 4.5 to 5.5 rad/s times the gust, its phase `time * w - i * 0.35`
  stepping along the strip so a gust travels across it. Put a solid base band (8 px, the blade colour) under
  the blades, so an edge-on strip is a solid line and never a dashed one.
- **Leaf tips flutter**: a tree carries two or three small leaf ellipses (a pine one tip triangle) as groups
  anchored at their base, rotating 14 to 16 degrees times the gust. The crown itself stays glued.
- **A kite flies on a string from the character's hand** (Moves, below); its tail and its swing are the wind.

Check it: over a steady span the bounding box of every card's colour is identical second by second, while
the frame change over a grass strip is clearly above a still page's.

```json
{
  "id": "treeR",
  "transform": {"position": [930, 540], "anchor": [0, 0], "z": -50},
  "content": {"kind": "shape", "items": [
    {"type": "group", "contents": [
      {"type": "ellipse", "position": [0, -150], "size": [130, 150]},
      {"type": "fill", "color": "#3f8f55"}, {"type": "stroke", "color": "#fffaf0", "width": 5}]}]},
  "animations": {
    "rotationX": {"keyframes": [{"time": 0, "value": -90}, {"time": 1.3, "value": -90, "easing": {"kind": "cubic_bezier", "control": [0.35, 0, 0.4, 1.3]}}, {"time": 2.0, "value": 0}]}}
}
```

## Moves

A book that only opens is a thin shot. Beats are carried by what the paper does:

- **Page turns between beats: the right page turns over the gutter and lands on the left.** The spread being
  left is printed on the right page and on the left page; the next spread is printed on the page under the
  leaf and on the leaf's back, which becomes the new left page.
  1. The leaf is one page-coloured panel the size of the page, `rotationX` 90 (lying face-up), `anchor`
     `[0, 0]` at the gutter, its rectangle centred at local `x` 255 so it covers the right page, a few px above
     the page. Its `rotationY` goes 0 to -180 over 1.5 s with `ease_in_out` and it lands face-down on the left
     page.
  2. **The back of the page** is a child of the leaf turned `rotationY` 180 and 0.6 px behind it, drawn
     mirrored (centred at local `x` -255): page colour, a spine shadow along the gutter side and faint rules.
     After the landing it is the left page.
  3. Every flat and the character on the right page is a child of the leaf (`parentId`) at the same local `x`
     and `y` as on the page. Parented, a flat lies at `rotationX` 0 and stands at -90; each folds down (0.45 s,
     `ease_in`) in step with the lifting page, front pieces first (0.05 s apart), and is hidden at upright,
     where its face turns away. The left page's flats fold down at the same moments, so the landing leaf lies
     on flat paper.
  4. The next spread's right-page flats lie printed under the leaf from the first frame. Its left-page flats
     are **children of the back of the page** (`parentId` the verso), printed on it from the first frame, so
     the turning leaf carries the new left page's art the whole way over: no blank back, no fade-in. The
     verso's rotations cancel at landing but its origin sits at the gutter (and the leaf's lying-flat turn
     remains), and a child's `position` is parent-local: author each at its world spread position minus the
     gutter's (`x` minus the gutter `x`, `y` minus the gutter `y`), lying at `rotationX` 0 as in step 3, not at
     its world `x`. All of them fold up after the leaf has landed.
  5. Shift the pivot's `x` 20 px right of the gutter while the leaf leans right and 20 px left once it leans
     left, crossing at upright (the leaf is then edge-on), so the centre ray never runs along the leaf's plane.
  6. **The next spread is a different place**: another setting with its own hue family (a day meadow with a
     house, then a mountain lake at dusk with pines and a tent), not the same shapes recoloured.
  Check every frame of the turn: no spike, no jump between neighbouring frames, the leaf in the frame, no piece
  overlapping another while lying flat.
- **A kite on a string from the hand.** The kite is a shape layer on the character's own plane (same
  `position`, a `z` 2 behind, the same fold-up keys and opacity gate), so string and hand fold up together. In
  it, one group anchored at the hand holds a 2.5 px string from the hand to the kite's bridle, high in the sky
  inside the page, and the kite (a two-tone diamond with a bow tail that flutters). The group swings a few
  degrees about the hand in the gusts. When the character flips to face the kite, the group's `position`
  steps to the mirrored hand on the same frame. The character then points at it.
- **A character leaves before the turn and enters after the spread has stood.** It folds down on its hinge
  (`ease_in`, 0.5 s) before the first flat folds, and folds up again once the sky flat of the next spread is
  up: never stands in front of flats that are folded down or not yet up.
- Count one move per two seconds at least: a fold-up, a run, a turn, a slide, a gust.

```json
{
  "id": "leaf",
  "transform": {"position": [640, 390], "rotationX": 90, "anchor": [0, 0], "z": 0},
  "content": {"kind": "shape", "items": [
    {"type": "group", "contents": [
      {"type": "rect", "position": [255, 0], "size": [500, 590], "roundness": 6},
      {"type": "fill", "color": "#f3ead6"}, {"type": "stroke", "color": "#c9b994", "width": 2}]}]},
  "animations": {
    "rotationY": {"keyframes": [{"time": 0, "value": 0}, {"time": 8.3, "value": 0, "easing": "ease_in_out"}, {"time": 9.8, "value": -180}]}}
}
```

## Motion habits

- **Rise back to front, folding down in the same order.** The furthest piece (sky) rises first, then hills,
  trees and house, the grass last, the starts 0.3 s apart and the gap growing a little toward the reader, each
  with the overshoot ease; the pieces fold down back to front too, 0.05 s apart.
- **Turning around is a horizontal flip, never a rotation that shows the card edge-on.** A paper character that
  changes direction flips its `scale` x from -s to s with a `step` key, on the spot, then walks the other way.
  Never key it through 0: a rig with follow-through (a tail) cannot evaluate a zero-scale parent. A `rotationY` turn shows the flat card edge-on as a sliver.
- **One hue family per spread, and the page turn is the colour change.** Spread 1 a day meadow in greens and
  blues, spread 2 a dusk lake (peach, violet, teal), and so on, each with the same 2 or 3 accent colours repeated across spreads (the
  fox's orange, the kite's gold, one flower pink), so the book reads as one object.
- **Sound for the paper** (an audio note for the edit that lays the film): a page swish on the turn, a short
  snap as each flat reaches upright, a soft slide on a pull-tab, tiny taps for a paper character's steps. No
  music bed over the snaps.
- **A desk object may play a part** (a lamp as the sun, a pencil as a bridge): a real thing on the table beside
  the book, lit by its own warm gradient, never inside the book's pages. Optional; one at most.
- **Pull-tab or slide instead of a long fold-up** where a fold would squash a character: the character rides a
  piece that the tab slides along the slot, and the fold-up stays under 0.7 s.
- The bird, kite or any prop on a wire comes in with an opacity key after its spread stands.
- Anything that wobbles on the page is the `wiggle` preset at a small `amount`, on twos in a nested
  composition with `fps` 15 (12 under a 24 fps root) if the book should feel handmade.
- Cued layers use `timeMode: "layer"`.

## Type

Usually none; a title is hand-lettered on a paper tag in a rounded serif, standing in the same fold-up way.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. The camera holds one framing per spread (one smooth pull-back and push-in for a turn), and the page's front
   edge or the gutter is in frame in every frame. Cards stand still; only grass, leaf tips, a kite and fur move.
2. Every piece has the paper edge and its own depth; the character has `stroke` and `drop_shadow` and a
   shadow on the page, and stands between flats inside the open book.
3. The fox (or the hero) is the only orange.
4. At least four pieces fold up in order, and at least two of: a page turn, a gust through the grass, a kite
   on a string from the character's hand.
5. Flat pieces are each a few pixels apart on the page (below) and lie printed on it from the first frame, never gated with `opacity`.

## Build with the tools

Build every piece as its own shape layer with its start time on the layer, key `rotationX` with the overshoot
easing, and set the camera under `composition.camera`. **Layers lying exactly in one plane can swap draw order
from frame to frame under a moving camera**, so give each folded piece its own page position, 3 px apart in y,
until the plane-order fix is on your build; the lift is invisible once the pieces stand. Check the book with
`picsart_scene_contact_sheet` at the first frame, at the start of the page turn and at the last frame: the front edge and
the gutter must show in all three.

## Do / don't

- **Do** put the table under the page so the page has an edge, and the cover and page block under that.
- **Don't** put two pieces at the same `z` and the same page position; don't animate a piece's scale to make
  it appear (it must fold, not grow); don't zoom past 0.88 to "get closer".
- **Don't** place the character on the table, in front of the book or at a `z` where it overlaps the front grass
  strip's base; it belongs to the page.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Finish: the paper edge is the finish, no film look and no grain layer; the table, planes and strips are world geometry, so they travel with the camera, and the grass blades stay coarse (14 to 36 px) so they do not shimmer.
  - Height is shadow: a scenery card lying flat has only its paper edge; the character's flat page shadow grows with its fold-up (scale and opacity keyed to the `rotationX` keys, ours, tune by render), and its `drop_shadow` offset points the same way, one light for the whole book.

## Originality guard

Invent the pages and the creatures. They must not resemble a known pop-up book's spreads, a famous storybook
scene or its characters. The fold-up, the paper edge and the glued cards are the style.

## Proven on

The pop-up film (open book, seven pieces folding up, a camera sway, a paper bird) and a fox in a windy meadow
(two spreads, a page turn whose back carries the next spread, a fox folding up out of the page and walking
between the flats, then turning to point at a kite it flies on a string).
