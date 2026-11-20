# Paper fold

A square invitation that unfolds: four flaps hinged on the edges of a centre card swing open in turn under a
perspective camera, each revealing a printed motif, before the words type on. Cream paper on deep purple.

## Palette

Paper `#f6efe4` with a pale edge `#d8ccb8`, ground `#3b2f5c`, motifs `#e8a33d` (amber), `#c75b7a` (rose) and
`#4f8f8a` (teal), shadow `#1a1430`. **The hero colour is the amber `#e8a33d`, reserved for the star on the centre
card and one motif stripe set.**

## The medium

- A **centre card** (200 px square, cream, a 2 px pale edge) with a small five-point star in amber, over a soft
  `drop_shadow` (offset 10, blur 16).
- **Four flaps**, each a cream square of the same size stacked over the card, each with its own printed motif
  on the inside face: a rose chevron, a teal ring, four amber bars, a rose star. Each flap carries a
  `drop_shadow` (offset 8, blur 12).
- Each flap is **anchored on its hinge edge** (the anchor sits at the middle of the edge it turns about) and
  placed so that edge is on the card's edge.
- The composition has a **camera** (`distance` about 1400) so the turn has perspective.
- **Type:** two short lines ("YOU'RE INVITED") on the centre card in a condensed face, and a line along the
  foot in a bold grotesque in cream; both type on with a short typewriter or fade-in-characters animation.
- A layer shows only its front face: it has no back side today. A flap turned past 90 degrees would show its
  front mirrored, so the motif is hidden until the turn passes the edge-on moment (below).

## Motion habits

- **Open one flap at a time**, 0.9 s each with an ease in and out, starts 0.8-0.9 s apart: `rotationX` from
  -179 to 0 for the top, +179 to 0 for the bottom, `rotationY` from +179 to 0 for the left and -179 to 0 for
  the right. The flaps start folded (flipped over) on top of the card.
- **Motif swap at the edge-on moment:** the motif group's opacity steps from 0 to 1 with a `step` easing at 0.45 s
  into the turn, when the flap is edge-on and invisible.
- Stack order is the opposite of opening order: the first flap to open is on top.
- Cued layers use `timeMode: "layer"`.

## Type

A condensed display face for the card's lines, a bold grotesque for the foot line, in cream or ink.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Each flap hinges on a real edge of the card.
2. Camera perspective is on and the same for all flaps.
3. The motif appears only after the flap passes edge-on.
4. Shadows are present on card and flaps and consistent in direction.
5. The flaps open in order, one at a time.

## Build with the tools

Set `composition.camera.distance`, build each flap as a shape layer with the anchor on the hinge edge and
`rotationX` or `rotationY` keys, and key the motif group's opacity with `step`. Give each flap its own depth only
if two share a plane; see the coplanar line in the pop-up recipe.

## Do / don't

- **Do** put the first-opening flap on top of the stack.
- **Don't** leave a motif visible through a flap that is flipped over; don't use a different shadow per flap.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Finish: if a paper tooth is added it is one fixed, low `noise` inside each flap's group, so it turns with the
    flap; the typed lines stay sharp and there is no film damage.
  - Height is shadow: one light from the top left; while a flap swings, its shadow offset and blur key up toward the
    edge-on moment (about 1.6 times the resting values, ours, tune by render) and settle back; every flap uses the
    same keys.

## Originality guard

Choose your own motifs and event. It must not copy a real stationery brand's invitation, a famous paper-craft
book's fold, or a named designer's patterns. The hinged flaps, the perspective turn and the printed insides are
the style.

## Proven on

The paper-fold-invite film (a square card with four flaps opening in turn under a camera, motifs revealed edge-on,
typed lines).
