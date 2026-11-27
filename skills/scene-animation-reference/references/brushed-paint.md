# Brushed paint

A `fill`, a `stroke` and a text content take a `brush`: the paint is laid as bristle streaks instead of
flat colour. `tip` is `"bristle"` or `"chalk"`; `coverage` below 1 leaves dry-brush gaps that show what is
beneath (about 0.6); `streaks` (0..1, default 0.15) adds lighter and darker gouache streaks; a fill's and a
text's `size` (streak width, default 24, text a quarter of its font size) and `angle` (default -20) set the
hatch. A stroke's bristles follow the line at its width, so its brush has no `size` or `angle`, and it is
refused with `taper` or `wave`. Gradient paints and a text's `stroke` have none. A brushed text hatches each
glyph in its own space, so per-glyph animators carry the texture with the letter.

It is static paint, drawn again only when the content changes: a brushed fill the size of the frame costs a
few milliseconds per redraw, so brush a still or whole-layer-animated shape freely and keep per-frame
changes (an animated colour, outline or per-glyph animator) on small brushed areas.

A shape `fill`'s brush also takes the `"pastel"` tip and `flow`; a stroke and a text refuse both. `"pastel"`
keeps the fill solid and scatters oil-pastel marks over it, each about `size` long with its own place, tilt and
pressure, lighting or deepening the paint so it keeps its hue; `streaks` is their strength (0.5 to 0.75 reads
as pastel, `0` leaves flat paint). `coverage` below 1 lays the paint itself as grainy dabs with gaps between
them. `flow: "around"` runs the marks round the fill's centre, pastel's as short curved strokes, bristle and
chalk streaks on rings that follow the fill's box, so a round body (a head, a ball, a cheek) reads as painted
along its form; keep a large flat piece (a sky, a hill) `"straight"`, where one ring the size of the piece reads
as a vortex. One fill lays about 20,000 pastel marks at most: a finer `size` on a large fill is laid coarser.
