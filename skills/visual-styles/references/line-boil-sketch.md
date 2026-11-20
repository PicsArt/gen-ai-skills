# Line-boil sketch

Pencil outlines on cream paper that never quite sit still: each line is drawn on, then wobbles from frame to
frame as if redrawn by hand every time. A kettle, its steam and a scribbled note.

## Finish

`line_boil` on every stroke, the stroke layers nested at `fps` 12 under a 24 fps root (see Motion habits).

## Palette

Paper `#f6f0e2`, graphite `#2b2b2b`, steam `#7a7a7a`. **No hue is reserved: the film is graphite on paper.** If
a colour is added, use one pencil accent (for example a red `#d4553a`) on one object only.

## The medium

- **Everything is a line.** No fills: objects are open paths stroked 3-4 px in graphite (lighter 2 px for hatch),
  round caps, on one paper-coloured layer.
- Build an object from several strokes drawn separately and overlapping a little at the joins: a kettle is a
  body (smoothed with tangents), a lid, a knob (a circle), a spout and a handle. Leave small gaps and overshoots;
  a hand does not close its shapes exactly.
- Shading is **hatching**: five or six short parallel strokes at 2 px.
- Steam is three thin curls in grey, each an S-shaped open path.
- Lettering is a loose hand face at 90 px in graphite, no outline.

## Motion habits

- **Draw each stroke on** with a keyed `trim` end (0 to 1), about 0.4-0.5 s a stroke and each starting a little
  before the last one ends, in the order a person would draw: table, body, lid, knob, spout, handle, hatch.
- **Boil** is the `line_boil` preset on every stroke layer and on the text (`rate` 10 to 15 per second,
  `amplitude` 2-3). Put all the stroke layers in a nested `composition` with `fps` 10 or 15 (8 or 12 under a 24 fps root) and apply the preset
  to the layer ids inside it, so the wobble steps instead of sliding.
- **Steam** rises and fades in a loop: position keys rising about 60 px over 1.8 s with a staggered start per
  curl, opacity keys fading in and out; the loop is built from repeated keys, not a time floor.
- The note fades in after the last stroke.
- Cued layers use `timeMode: "layer"`.

## Type

One short hand-lettered line in a loose marker or hand face, graphite, the same boil as the lines.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Lines only; no fills except the paper.
2. The boil is on every line and is stepped (10-15 changes a second).
3. Strokes are drawn on in a natural order with small overlaps.
4. A rising element (steam) keeps the held frame alive.
5. The wobble is small enough to read the shape from across a room.

## Build with the tools

Make each stroke its own shape layer with a `trim` and a stroke. Nest them in one `composition` layer with `fps`
10 or 15, then apply `line_boil` with `picsart_scene_apply_preset` to the nested ids (never to the composition
layer). Where a stroke needs more life, add a `wiggle` at a small amount.

## Do / don't

- **Do** keep the amplitude below the line weight times about 0.8, so the boil moves the line without breaking
  its shape.
- **Don't** put the boil on the paper, or tie the boil to a time-floor expression; don't use more than one
  accent colour.

## Originality guard

Draw your own subject. It must not copy a known studio's boiling-line short, a named illustrator's sketchbook
subject, or a recognisable character. The graphite line, the draw-on and the stepped boil are the style.

## Proven on

The kettle film (a table, a kettle, steam curls and a note, all boiling at 10 fps, drawn on stroke by stroke).
