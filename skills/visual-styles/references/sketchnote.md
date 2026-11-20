# Sketchnote

A hand-lettered page: a seed grows into a seedling, an arrow carries the eye to a heading, doodled boxes and
underlines draw on, and a yellow highlighter sweeps the key word.

## Palette

Paper `#fffdf6`, ink `#2a2a2a`, leaf green `#6bbf59`, soil `#8a6a4a`. **The hero colour is the highlighter yellow
`#ffe45c`, reserved for the sweep behind the key word**, drawn at about 80 % opacity under the text.

## The medium

- **Wobbly line art:** every stroke is a slightly irregular path (a few points jittered by a seeded script), 4-5 px,
  round caps, ink colour; shapes close with a small overshoot instead of a clean join.
- **Doodles:** a seed, two leaves, a sun, a box, an arrow with a curved shaft, an underline, a spiral.
- **Lettering:** a handwriting face for headings and notes, not a typewriter face.
- **Highlighter:** a wide rounded rectangle with a slightly tilted edge, placed behind the word.

## Motion habits

- **Draw each doodle** with `trim` end 0 to 1 over 0.5-0.9 s, one after another, an ease-in-out on each.
- **Grow the seedling** with `scale` keys from the seed (anchor at the soil) and leaves unfolding with a small
  overshoot.
- **Line boil** (a gentle redraw wobble) is the `line_boil` preset on the drawn layers inside a nested composition
  at 6 fps, so the page never goes dead still. Keep it small.
- **Highlight sweep:** the highlighter's width keys from 0 to its width over 0.5 s, left to right.
- Cued layers use `timeMode: "layer"`.

## Type

A handwriting face for everything; a heavier weight for headings.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Every stroke looks hand-made, not ruled.
2. The highlighter sits behind the word and does not hide it.
3. Doodles draw in reading order.
4. Boil is small enough not to blur the text.
5. Yellow appears only on the highlighter.

## Build with the tools

Jitter path points in a script with a fixed seed; put the drawn layers in a nested composition at fps 6 and apply
the `line_boil` preset; give text layers a plain fade or `typewriter`.

## Do / don't

- **Do** leave generous margins and uneven spacing.
- **Don't** use perfect circles or straight rules, or a pen-brush texture that shifts every frame.

## Originality guard

Draw your own doodles and write your own notes. They must not copy a known sketchnote artist's icons, a book's
figures or a famous whiteboard channel's style sheet. The wobbly line, doodled arrows and yellow highlight are
the style.

## Proven on

The sketchnote-seed film (a seed growing into a seedling, an arrow, a boxed heading, underlines drawing on,
a yellow highlighter sweep).
