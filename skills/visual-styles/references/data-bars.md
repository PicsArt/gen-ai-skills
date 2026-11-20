# Infographic bars

A clean data chart that builds itself: axis and gridlines draw, bars grow from the baseline in turn, values
appear on their tips, one bar is picked out in colour and the rest drop to grey.

## Palette

Paper `#fbfbfa`, ink `#1f2328`, grid `#e3e6ea`, bars `#c3c9d1`. **The hero colour is the red `#e8505b`, reserved
for the one bar the story is about**; a single deeper grey `#8b94a1` marks the average line.

## The medium

- Horizontal gridlines every 25 % of the axis, 1.5 px; a 3 px baseline.
- **Bars** are rounded rectangles with a 6 px radius on the free end only, equal widths, equal gaps.
- **Value labels** sit on each tip in a tabular figure face; **category labels** sit under or beside each bar.
- A **title** and one-line subtitle at the top-left, a source line at the bottom-right.

## Motion habits

- **Grow from the baseline:** each bar's length keys from 0 to its value over 0.7 s with an ease-out
  (`[0.2, 0.7, 0.2, 1]`), 0.12 s apart; anchor at the baseline so the base never moves.
- **Numbers follow:** each label fades in and rises 8 px as its bar finishes. A counter that ticks up is a gap
  today, so key the label's final value only.
- **Pick the story:** after all bars land, the others fade to a lighter grey and the story bar turns red with a
  small scale pulse (`[0.4, 1.12, 0.5, 1]`).
- **Average line** draws with `trim` last.
- Cued layers use `timeMode: "layer"`.

## Type

One grotesque family: bold title, regular labels, tabular figures for values.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Bars start at zero and are scaled to the true values.
2. One bar is red; the rest are grey.
3. Values are legible and not clipped.
4. A title says what the chart shows and a source line says where it is from.
5. Gridlines stay quiet: lighter than the lightest bar.

## Build with the tools

Compute bar lengths from the data in a script and write them as keys; labels as text layers placed from the same
numbers. Check the final frame with `picsart_scene_query_layout` for overlaps.

## Do / don't

- **Do** sort bars by value unless the categories have a natural order.
- **Don't** use 3D bars, gradients, or truncated axes.

## Originality guard

Use your own data and wording. It must not copy a named publication's chart house style, its fonts and
colours together, or a real report's figure. The one red story bar on a grey field is the style.

## Proven on

The orders-dataviz film (axis and grid drawing, bars growing in turn, values on tips, one bar picked out in red,
an average line).
