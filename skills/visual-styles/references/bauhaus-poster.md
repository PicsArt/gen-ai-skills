# Bauhaus poster

A portrait poster of primary shapes and black bars that slide into a tight composition, a semicircle that
rotates over, and a heavy grotesque set at angles of the page. Geometric, flat and slightly severe.

## Palette

Cream `#efe8da`, red `#d63a2f`, yellow `#f2c230`, blue `#1f4fa0`, black `#151515`. **The hero colour is the red,
reserved for the square and one small dot**; yellow, blue and black are the supporting palette and each has one
large shape.

## The medium

- Portrait 1080 by 1350 on a cream page. Only flat fills: no outline, no gradient, no shadow.
- The shapes are the full set of primitives: a large yellow **circle**, a red **square**, a blue **semicircle**
  (a closed path of two bezier quarter arcs), a black **triangle**, two black **bars** (one wide, one tall) and
  a small red **dot**.
- Shapes overlap at their edges, not their centres, and are weighted toward one diagonal; the empty corner
  gives the type its room.
- Type is a heavy grotesque in black and blue at three sizes (a year at 90 px, a word at 110 px, a word at
  150 px), set horizontally and offset to the grid the shapes make.

## Motion habits

- **Slide in from off the page** on a firm ease (`[0.7, 0, 0.2, 1]`), 0.8 s each, starting 0.3 s apart in the
  order circle, square, semicircle, bars, triangle, dot.
- The semicircle then **rotates 180 degrees** in about 0.8 s with an ease in, flipping to its other face.
- Words slide up 40 px and snap on (a hard opacity step), staggered by 0.3 s.
- At the end rotate every shape a quarter turn together about the page centre by keying the same rotation
  on a parent layer, so the poster re-composes as one.
- Cued layers use `timeMode: "layer"`.

## Type

A heavy grotesque, black or blue, no outline, upper case, tracked tight; no more than three words and a year.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Only primaries, black and cream; red appears twice at most.
2. Every shape is a primitive: circle, square, half circle, triangle, bar.
3. The composition is weighted to one diagonal with a clear empty corner.
4. Type sits on the grid the shapes imply.
5. The final quarter turn moves everything as one group.

## Build with the tools

Each shape is its own shape layer with a position key from off-page to rest; make the semicircle from two
bezier quarter arcs. Parent every shape to an empty layer with a `transform` and key that layer's rotation for
the final turn.

## Do / don't

- **Do** overlap at edges so shapes read as stacked paper.
- **Don't** add pastel tints, soft shadows or a photograph; don't use a second weight of type.

## Originality guard

Compose your own poster, wording and date. It must not copy a known Bauhaus exhibition or school poster, a
named master's composition, or a school's logo. The primitives, the primaries and the quarter-turn are the style.

## Proven on

The bauhaus-form film (a portrait poster: circle, square, rotating semicircle, bars, triangle and dot sliding
in, then the whole quarter turn).
