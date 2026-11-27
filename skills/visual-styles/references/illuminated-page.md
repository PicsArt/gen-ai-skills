# Illuminated page

A page of a medieval book written live: aged vellum inside a gold double rule, a red blackletter heading with a small
gold diamond rule under it, a blue drop-cap panel with a gold capital, lines of dark blackletter ink that a quill uncovers
one after another, and green vines with red and blue berries that grow up both margins. It is warm, patient and
handmade, not a scanned book, not a fantasy map (that is [route-map](route-map.md)) and not a woodcut (that is
[woodblock-print](woodblock-print.md)).

## Palette and colour roles

| Role | Colour | Its one job |
|---|---|---|
| vellum | `#efe0b8`, darkened to `#a47c3a` at the top and bottom edges | the page, flat in the middle so text sits on it |
| ink | `#2b1d12` | every line of text |
| heading | red `#b3261e` | the one big word |
| drop cap panel | blue `#27407f` with gold `#c79a2e` rules and a gold letter | the one cool block |
| gold | `#c79a2e` | frame rules, the diamond rule, the capital |
| vine | stem `#3f6b3a`, leaves `#4f8a47` with a pale vein `#7fb06e` | the margins' growth |
| berries | red `#b3261e` and blue `#27407f` | small accents on the vine |
| quill | cream `#f4ecd8` with a dark outline `#3a2a1a` | the writing hand |

Hero colour: the heading red `#b3261e`. Gold and blue stay small: a frame, a capital, a few berries.

## The medium

- **The ground is flat vellum** with a multiply vignette drawn last, so the edges warm and darken while the text area stays
  one even colour (the covers that hide unwritten lines are the same flat vellum).
- **Type is blackletter**, never a plain sans: one blackletter face for the heading, the capital and the body lines.
- **Writing is a reveal:** each line is shown by a flat vellum cover that shrinks away to the right, edge first, with the
  quill's nib riding that edge. The quill is a feather with a curved brown shaft, a barbed cream vane shaded tan along the shaft, and a dark nib, laid along the line pointing up and right, so it covers only unwritten space.
- **Vines** are a wavy stem, leaves as paired ellipses with a pale vein, and berries sitting on the stem. Stems and leaves stay inside the gold rule.

## Rates

| Held rate | Root rate |
|---|---|
| none | everything: the pops, the reveal and the quill's small tremble |

## Boil

None: edges are clean; the quill's tremble is a small sine, not a boil.

## Line width under a zoom

The frame rules are 5 px and 2 px strokes, the vine stem is 7 px, the feather outline is 3 px and its shaft 5 px. A camera push keeps them as
thin lines.

## Motion habits, and the transitions

- **The heading arrives first:** it pops from the middle with a small overshoot, then the gold rule, then the drop cap and
  its letter.
- **The vines grow up the margins:** the stem grows from the bottom over about 2.3 s, and a leaf pair pops by scale with a
  back ease every 0.16 s as the stem reaches it; a berry follows every third pair.
- **The text is written** one line at a time, about 1.2 s a line, the quill's nib on the writing edge with a small
  tremble; between lines and at the end it rests at the end of the line just written.
- Transitions: the page turns (a slow slide with the vellum edge darkening), or the gold rule grows into the next frame.

## Type

A blackletter face (the proof used UnifrakturCook): about 150 px for the heading, 130 px for the capital and about 50 px for the
lines, left aligned, a short sentence per line. The drop cap hangs over the first two lines, which are set in from it, and
the whole text block sits between the margins: the vines never reach a letter.

## Scene features used

Hints, not rules: the look needs a blackletter font (check `picsart_scene_fonts`; the proof used the free UnifrakturCook) and a
way to uncover a line left to right (a mask, a text reveal or a cover all work). Everything else is shapes and text.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. The text area is one even vellum: no seam where a cover meets the page.
2. Every line of text is fully readable at the end and sits inside the gold frame.
3. The heading is the only large red; gold and blue stay small.
4. The quill's nib is on the writing edge of the line being written, and it never hides the line above.
5. The vines stay in the margins and never cover a letter.
6. The last frame has every line written and the quill at rest.

QC: lean on a contact sheet across the writing and the viewer's pass at normal speed for the pace.

## Build with the tools (a hint, optional)

Any construction that keeps the look is fine. If lines are uncovered with flat vellum covers, keep each cover the same
colour as the page and inside the margins so it never hides a vine.

## Do / don't

- **Do** write each line left to right, the way a hand does.
- **Do** keep gold and blue small and the red heading large.
- **Do** write your own short lines.
- **Don't** use a plain sans or a script for the lines.
- **Don't** put a texture or a photograph on the vellum; the covers must match it.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Rate split: everything runs at the root rate; nothing is held.
  - Nothing fades: elements pop by scale or are uncovered; nothing changes opacity.
  - Height is shadow: none; the page is flat, depth comes from the edge vignette only.
  - Boil: none.

## Originality guard

Design your own text, heading, capital and border. It must not copy a known manuscript page, its decoration or its
wording. Aged vellum, a gold double rule, a red blackletter heading, a blue drop cap and growing vines are the style.

## Proven on

An 11 s portrait clip (1080 by 1350, 24 fps): a heading, a drop cap, seven written
lines, two vines of fourteen leaf pairs and a quill; exported locally, not on the hosted renderer. The clip writes the page
and does not loop.

**Not proven:** the stage editor (not tried), the transitions (a page turn, the rule growing into the next frame), a page with a painted picture, a second page turning, a longer text than
seven lines, a landscape frame, a font other than UnifrakturCook and a seamless loop.
