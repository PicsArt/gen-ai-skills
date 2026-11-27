# Math explainer

A dark-board maths explainer: axes and a curve draw on, an equation transforms into the next line, a point
slides along the curve with its value updating, and the result lights up in yellow.

## Palette

Board `#0E0E10`, axis and text `#E8E8EA`, grid `#2A2A31`, curve blue `#58C4DD`, secondary teal `#83C167`, accent
red `#FC6255`. **The hero colour is the result yellow `#F7D96F`, reserved for the final answer and the highlight
on the term being explained.**

## The medium

- **Axes and grid:** a 2 px axis with small tick marks and a 1 px grid, both quiet against the board.
- **The curve:** an open path sampled from the function in a script, 5 px, blue, with round caps.
- **Equations:** text layers set in a serif face, one line per layer, aligned on the equals sign.
- **A moving point:** a small disc on the curve with a dashed projection line to the axis and a value label.
- **Braces and boxes:** thin strokes that group terms; the highlight is a yellow rounded rectangle at 18 % fill.

## Motion habits

- **Draw on:** the axes draw with `trim` over 0.8 s, then the curve over 1.4 s with an ease-in-out.
- **Transform the equation:** the old line is wiped out right to left by a mask and shifts up 20 px while the new line writes in below with a
  left-to-right mask wipe; matching terms keep their position so the eye follows them (cue one layer per term
  and move the shared ones rather than wiping them).
- **Slide the point:** position keys sampled from the curve in a script, at constant parameter speed; the label
  is one counting text layer (an expression on `text` that writes the curve's value with `mp.formatNumber`).
- **Result:** the answer pops with a small overshoot and the yellow box draws round it.
- Cued layers use `timeMode: "layer"`.

## Type

A serif face for equations and a clean grotesque for labels; one size for terms, a larger one for the result.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. The curve is the true function, sampled finely enough to look smooth.
2. Matching terms stay put between lines.
3. The moving point is always exactly on the curve.
4. Yellow is reserved for the result.
5. Equations align on the equals sign.

## Build with the tools

Sample the curve and the point positions in a script and write them as path points and position keys; build
equations as text layers and check their alignment with `picsart_scene_query_layout`. Verify the point against the curve at
three frames with `picsart_scene_contact_sheet`.

## Do / don't

- **Do** pause a beat before each new line so the previous one can be read.
- **Don't** copy a known explainer channel's character, intro animation or typeface pairing as a set.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Nothing fades: content arrives by draw-on (axes, curve, yellow box), by a left-to-right write-in, or by the result's pop; a new idea starts on a cleared board by a hard cut, no cross-dissolve between boards (ours).
  - True data: one table of samples of the function draws the curve and drives the point, its projection line and the value label; axis ticks and the curve share one scale; the function stays written in frame from first line to result; a curve drawn only as a sketch is labelled `sketch`.

## Originality guard

Choose your own function, wording and layout. It must not reproduce a named channel's scenes, its logo or its
signature transitions. The dark board, drawn axes and term-by-term transform are generic conventions.

## Proven on

The math explainer film (axes and a curve drawing on, an equation transforming term by term, a point sliding along
the curve with a value label, a yellow result).

**Not proven:** the wipe-out of an old equation line was shown on a plain board, not beside a plotted curve.