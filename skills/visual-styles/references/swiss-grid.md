# Swiss grid

A typographic poster on a visible grid: hairlines draw themselves, one red circle jumps from cell to cell, a
black bar turns upright, and a huge headline slides up under a hard edge. Everything lands on a grid line.

## Palette

Ink `#141414`, paper `#f2efe8`. **The hero colour is the red `#e63322`, reserved for the circle and the small
index number** and used nowhere else. Grid hairlines are ink at about 18 % opacity.

## The medium

- A grid of five columns and three rows (lines 240 px and 180 px apart) drawn as 1.5 px ink hairlines, each a
  two-point path with a keyed `trim`.
- One **red circle** (diameter about 400), one **black bar** (a long thin rectangle, 760 by 36), and type. Three
  elements and a grid; nothing else.
- Type is a bold grotesque, flush left, set very large for the headline (about 230 px) and small for labels
  (22-30 px): a two-line sub-head, an index number and a caption naming the grid.
- The headline sits under a **hard mask edge**: a `mask.clip` with a colour rectangle so it is cut off where it
  slides in from below.

## Motion habits

- **Snap, never drift.** Every move uses a snap easing (`[0.7, 0, 0.15, 1]`): the circle jumps cell to cell with
  a hold of about a second between jumps, the bar wipes in from off-frame, turns 90 degrees about its centre and
  returns, and the headline rises 170 px in 0.7 s.
- The circle pops in with a small overshoot (`[0.3, 1.6, 0.5, 1]`) and shrinks to a dot at the end.
- Grid lines draw on first, staggered by 0.1 s, then the elements; labels fade in with a 30 px slide.
- Cued layers use `timeMode: "layer"`.

## Type

One bold grotesque (Helvetica-like), flush left, upper case; sizes jump by a factor of five or more, never
three nearby sizes.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Every element's edge or centre sits on a grid line when it rests.
2. Exactly one colour besides ink and paper, used on the circle and one number.
3. All moves are snaps; nothing eases softly.
4. The headline is larger than every other element and cut by a hard edge.
5. At least a third of the frame is empty paper.

## Build with the tools

Build the grid as eight two-point shape layers with `trim` keys, the circle and the bar as shape layers with
position, scale and rotation keys, and the text as text layers. Use `picsart_scene_query_layout` at rest times to confirm
edges land on the grid.

## Do / don't

- **Do** let the one circle cross the whole grid; its path is the motion.
- **Don't** add shadows, gradients, rounded corners on the bar or a second hue.

## Originality guard

Compose your own poster and wording. It must not copy a known Swiss poster, a named designer's layout or
a museum's identity. The visible grid, the snap, the single red and the huge flush-left headline are the style.

## Proven on

The swiss-form film (a five-by-three grid drawing on, a red circle jumping cells, a bar turning upright, a
FORM headline).
