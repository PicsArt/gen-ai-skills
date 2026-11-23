# Pictogram

An information graphic made of one repeated icon: rows of little people appear one by one, one row changes
colour, a headline number lands beside them and a bar chart grows from its axis. Quiet, flat and exact.

## Palette

Paper `#f4efe4`, navy ink `#22314f`, muted grey-blue `#9aa3b5`. **The hero colour is the orange `#e4572e`,
reserved for the one row (or bar) the story is about.**

## The medium

- **One icon, drawn once**: a person is an ellipse head and a rounded-rectangle body in one group with one
  fill. Rows are that group with a `repeater` (10 copies, 46 px apart) in a shape layer of its own, four rows
  92 px apart.
- Counts appear by **keying the repeater's `copies`** from 0 to 10 with a `step` easing, 0.05 s per icon, rows
  starting 0.35 s apart.
- The highlighted row's fill is keyed from ink to the accent; later, other rows' fill is keyed to the muted grey
  so the highlight reads.
- A **headline figure** ("1 in 4") in a very large bold grotesque, with a small caps caption under it; a title
  and a "data is illustrative" note at the top left.
- A **bar chart**: an axis as an open path (trimmed on), four rectangles in groups anchored on their base and
  scaled in y with an overshoot (`[0.3, 1.5, 0.5, 1]`), the last in the accent.

## Motion habits

- Icons arrive in counted steps, never fading: the row fills left to right like a tally.
- The colour change on the highlighted row happens after the row is full; the headline number slides up 30 px
  and fades in on the same beat.
- Bars grow 0.15 s apart, each 0.6 s long. Hold the final frame; the graphic needs a moment to be read.
- Cued layers use `timeMode: "layer"`.

## Type

A bold grotesque for title, number and caption; a regular weight for the footnote. Upper case for captions.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. One icon only, drawn once and repeated, never redrawn per row.
2. The accent marks one thing and the headline refers to it.
3. Counts are stepped, not faded or scaled.
4. The numbers on the chart agree with the icons shown.
5. A footnote says the data is illustrative when it is.

## Build with the tools

Draw the icon group, add a `repeater` after it (one repeater per group), and key `copies` with `step`
easing. Build bars as groups with `anchor` on the base. Check counts with `picsart_scene_contact_sheet` at the end of
each row.

## Do / don't

- **Do** keep icon spacing constant so a row reads as a measure.
- **Don't** use more than one icon style, add shadows, or animate the icons' size to make them appear.

## Originality guard

Draw your own icon and write your own figures. It must not reproduce a known statistics poster, a named
agency's icon set or an official chart's layout. The repeated icon, the counted reveal and the single accent are
the style.

## Proven on

The pictogram film (four rows of ten people counting in, one row turning orange, a headline number, a four-bar
chart).
