# One pen marker

Reasoning shown as a single marker pen working on blank sheets. The pen has one width and three inks, and each ink
says what kind of thing it draws; a sheet poses one question, and the next sheet is reached by moving the camera or
the paper, never by wiping. It is working-out on paper, not a doodle page (no filler scribbles) and not a board
that gets cleaned (nothing is rubbed out).

## Palette and colour roles

| Role | Colour | Its one job |
|---|---|---|
| ground | `#f7f5f0` | the matte sheet |
| line | `#171717` | black: the structure of the picture, outlines, labels, signs |
| field | `#2457d6` (blue) | the facts the question starts from: its numbers and counted things |
| accent | `#d62828` (red) | **one** reserved colour: what is being asked, then its answer; one red mark per sheet, laid down after everything else on it |

A sheet shows at most one red mark. Blue never answers and red never explains.

## The medium

- One stroke width (ours 22 px at 1080 wide, tune by render), round caps and joins, constant
  everywhere: no taper, no pressure.
- Every stroke layer is `multiply` at high opacity (0.92, ours) so crossings darken a little, as marker does.
- Each stroke is one path; a line with two visible sides is two paths, so each side can be drawn on separately.
- Writing is **glyph paths drawn on with `trim`**: set the text's outlines as paths with `picsart_scene_import_svg_path`
  from a handwriting face (a one-stroke face if there is one) and trim each from 0 to 1, in reading order. Text
  layers are for captions only.
- A sheet is mostly empty: one question, its facts in blue, a few black parts, one red mark.
- The sheet is flat: no paper texture, no shadow on the page; only a peeling sheet throws a narrow soft shadow.

## Rates

| Held rate | Root rate |
|---|---|
| the drawing's strokes (12 fps nested composition), so the boil steps | the sheet push, the peel, the camera zoom, captions and text |

## Boil

A stroke boils on twos only while it is being drawn (`line_boil`, `amplitude` 2, 12 a second, a fixed seed, one seed
per stroke layer, the time that feeds it capped at the moment the stroke finishes); once drawn it holds that shape, so
finished letters, digits and rings are still. The paper, captions and the camera stay still too.

## Line width under a zoom

Constant on screen: a push-through zoom keys one shared parameter that scales the zoom and divides the stroke width
by the same factor, so the marker never gets thinner or fatter in the move.

## Motion habits, and the transitions

- Strokes arrive by being drawn: `trim` from 0 to 1 at the speed a hand moves (0.25 to 0.6 s a stroke, ours); within
  a sheet the reading order of the black and blue marks leads, and the red mark comes last, followed by a hold of
  0.4 s. Everything is finished before the camera moves.
- Between sheets there are two moves. **Push through:** the camera zooms into one part of the sheet until that part
  fills the frame, and that part is the next sheet's first mark (a match cut). **Peel:** a `page_curl` lifts the
  finished sheet away to show the next, with a narrow soft shadow. A torn slip (a rect with `roughen_edges` at a
  constant `evolution`) can carry an aside onto the sheet.
- Never fade between sheets and never erase.

## Type

Captions are written by the same hand (glyph paths) or set in a rounded hand face in black at the sheet's edge, held
long enough to read; numbers that start the question are in blue.

## Scene features used

Constant-width `stroke` with round caps, `trim`, `multiply`, `line_boil`, nested `composition` at 12 fps,
`page_curl`, camera `zoom`, `roughen_edges`, `picsart_scene_import_svg_path`, `timeMode: "layer"`.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. One stroke width and three inks, no fourth colour.
2. Red appears once on a sheet and is its last mark.
3. Blue marks are the question's own facts and nothing else.
4. A stroke boils on twos only while it is drawn; finished marks, the paper and the captions are still.
5. Crossings darken; nothing is translucent otherwise.
6. The sheet is mostly white and the question reads at thumbnail size.

QC: lean on the viewer's pass at normal speed (the order of the strokes), the thumbnail read and the palette count.

## Build with the tools

Convert the lettering and any complex shape to paths with `picsart_scene_import_svg_path`; one shape layer per ink per sheet,
each with a `trim` item keyed from 0 to 1 and `multiply`; nest each sheet's strokes in a `composition` at 12 fps and
apply `line_boil` with `picsart_scene_apply_preset` to its stroke layers; the sheets themselves sit at the root rate for
the push and the peel. Check the push-through on a contact sheet at every frame of the move.

## Do / don't

- **Do** keep one question per sheet and make the red mark the answer.
- **Do** let the next sheet's first mark be the thing the zoom landed on.
- **Don't** add a second pen width, a shadow on the page, a fade or an eraser.
- **Template rules, this style's choices** (the rules every recipe holds):
  - Rate split: strokes step while drawn and then hold; the sheet, the camera and the captions run at the root rate.
  - Nothing fades: strokes are drawn on, sheets are pushed through or peeled, a torn slip slides in.
  - Height is shadow: only the peeling sheet and a slip carry a shadow, narrow and soft.

## Originality guard

Design your own question, sheets and wording. It must not copy a known explainer channel's sheets or a named
illustrator's lettering. The single pen, ink as meaning and the camera-led move between sheets are the style.

## Proven on

A 6 s portrait clip (1080 by 1350, 24 fps) of two sheets: "3 + 2 = ?" written by trimmed strokes (digits in blue, the
signs in black, the red question mark last, each drawn stroke boiling only while it is drawn and still once it is
finished), a push-through zoom that scales the whole sheet about the top bar of the equals sign with no sideways move,
so no other glyph crosses it, landing on sheet two, where that bar is the first mark and becomes the counting line;
the rings start drawing as soon as the push lands, so the ground is never blank, and a red 5 closes the sheet;
exported on the hosted renderer.

**Not proven:** lettering taken from a real handwriting face (the digits and the question mark in the proof are
hand-built strokes), the `page_curl` peel, the torn slip, a constant on-screen width beyond the proof's 0.6 s move,
black ink laid down before all the blue (the proof draws the plus in black first, then the blue digits), and what the
neighbouring glyphs do during the push (the whole blue 2 and the red question mark sweep across the frame for part of
the 0.6 s move, and a few edge fragments stay in view).
