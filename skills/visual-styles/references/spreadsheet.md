# Spreadsheet

A spreadsheet explainer: a grid of cells fills with values, a cell is selected, a formula types into the bar, a
range highlights, and a total appears. Light grid, green accent.

## Palette

White `#ffffff`, grid `#d9dde1`, header band `#f1f3f4`, ink `#1f2328`, selection fill `#e6f4ea`. **The hero colour
is the green `#1a7f37`, reserved for the selection frame, the formula-bar caret and the result cell.**

## The medium

- A grid of 1 px lines: column letters across the top, row numbers down the left, in the header band.
- **Cells** hold values in a mono or tabular face, numbers right-aligned, text left-aligned.
- **The selection** is a 3 px green frame with a small square handle at the bottom-right corner.
- **The formula bar** is a strip above the grid with an "fx" label and the formula text.
- **A range highlight** is a translucent green fill over a block of cells.

## Motion habits

- **Fill the grid:** values appear row by row with a short fade, 0.05 s apart.
- **Move the selection:** the frame jumps cell to cell on whole-frame keys (no tween), as a keyboard would.
- **Type the formula:** text in the bar reveals character by character using the text animation `typewriter`;
  a caret that follows the text is a gap today, so use a blinking block at the end of the final string and
  hide it when typing ends.
- **Highlight the range** with a fill whose rectangle grows over 0.4 s, then the result cell fills and the total
  pops with a small overshoot.
- Cued layers use `timeMode: "layer"`.

## Type

Cutive Mono or a clean grotesque for the grid; the single mono font is the only one available for code-like
text, so keep formulas short and avoid glyphs it lacks.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Cells line up to the grid at every frame.
2. Numbers are right-aligned in their column.
3. The selection always sits on a whole cell.
4. The formula in the bar matches the cells highlighted.
5. Green appears only on the selection, caret and result.

## Build with the tools

Lay out cells from one cell width and height in a script, with one text layer per value; build the selection and
highlight as shape layers with keyed rectangles. Check alignment with `picsart_scene_query_layout`.

## Do / don't

- **Do** make the total equal the sum of the highlighted cells.
- **Don't** animate the grid lines or add a real application's chrome or logo.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Line width: no zoom, width fixed (1 px grid, 3 px selection frame).
  - True data: every cell value and the total come from one data array in the script, the total is a counter text
    (a text track expression with `mp.formatNumber`) over the highlighted range, a small "sample data" tag stays in
    frame, and the unit is stated once in a header; check cell positions and the total with `picsart_scene_query_layout`.

## Originality guard

Draw your own simple sheet and data. It must not copy a real spreadsheet application's toolbar, icons, logo or
colour scheme. The grid, selection frame and formula bar are generic conventions.

## Proven on

The spreadsheet-explainer film (a grid filling with values, a selected cell, a formula typing into the bar, a
highlighted range and a total).
