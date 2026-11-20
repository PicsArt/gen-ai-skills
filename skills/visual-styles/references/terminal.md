# Terminal

A command-line session on a dark window: a prompt, a command that types out, lines of output that print in
bursts, a progress bar that fills and a final line that lands. Monospace everywhere.

## Palette

Window `#0d1117`, title bar `#161b22`, text `#c9d1d9`, dim `#6e7681`, success `#3fb950`, link blue `#58a6ff`.
**The hero colour is the orange `#ffa657`, reserved for the prompt and the command being typed.**

## The medium

- A rounded window with a title bar (three small circles, a short title) and a text area with generous padding.
- **Lines** of mono text at a fixed line height; the prompt `$` in orange, commands in orange, output in the
  main grey, success in green.
- **A caret:** a solid block at the end of the current line, blinking at 1 Hz.
- **A progress bar:** a bracketed bar of block characters or, better, a shape rectangle filling inside a thin frame.

## Motion habits

- **Type the command** with the text animation `typewriter` at a human pace (about 14 characters a second); the
  caret is a gap today (it does not follow the text), so show a blinking block at the end of the final string and
  hide it while the text types.
- **Print the output** in bursts: each line appears whole on a hold (no fade), three to five lines in the same
  frame, then a pause.
- **Progress** fills with a stepped key (jumping 10 % at a time) rather than a smooth ease.
- **Scroll:** when lines pass the bottom, all lines move up one line height on a quick ease (0.12 s).
- Cued layers use `timeMode: "layer"`.

## Type

Cutive Mono is the only mono face available; it lacks some glyphs (a play arrow, a coffee cup) and drops them
silently, so use plain characters (`>`, `*`, `#`) for decoration.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Every line sits on the line grid.
2. The caret is at the end of the last typed character.
3. Orange appears only on the prompt and command.
4. Output appears in bursts, not character by character.
5. No glyph is missing from the font.

## Build with the tools

One text layer per line with `start` times from the script; the caret as a small shape on a blinking opacity
track; the bar as shapes. Verify glyphs by rendering a frame and looking for blanks.

## Do / don't

- **Do** keep commands short and plausible.
- **Don't** copy a real tool's banner, ASCII logo or version string.

## Originality guard

Invent your own commands and output. It must not reproduce a real tool's branding, a distribution's logo art or a
specific shell theme. The dark window, mono text and typed command are generic conventions.

## Proven on

The terminal-coffee film (a prompt and a typed command, bursts of output, a filling progress bar and a final
success line).
