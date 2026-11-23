# Factory loop

A seamless looping production line: blank parts ride a conveyor, a press stamps each one, a scanner sweeps it
and the finished part leaves the frame. The loop closes exactly, so it plays forever.

## Palette

Floor `#2b2f36`, belt `#454b55` with lighter slats `#5a616d`, parts blank `#cfd8dc` and finished `#7fd1a3`,
machine body `#8a94a3`. **The hero colour is the press red `#e05a47`, reserved for the press and its warning
stripe**; the scanner beam is a thin mint `#9dffcf` line.

## The medium

- A belt as a long rounded rectangle with slats (a repeater is fine: one per group, set once) whose offset moves.
- Parts are small rounded squares riding on the belt.
- **The press** is a block on two guide posts above the belt; a stripe band marks its edge.
- **The scanner** is a gantry with a line that sweeps across the part.

## Motion habits

- **Everything runs on one period** (say 4 s) and every keyed value returns exactly to its start by the end, so the
  loop is seamless. Use `ctx:loopOut("cycle")` on repeating tracks and key whole frames.
- **Belt:** slat offset moves one slat-pitch per period at constant speed; parts ride at the same speed.
- **Press:** drops and rises on an ease-in with a hard stop (`[0.7, 0, 1, 0.6]`), squashing the part by 12 % for
  two frames at contact, then the part changes colour (a keyed fill step).
- **Scanner:** the line sweeps once per part with a smooth ease.
- **Stagger parts** a pitch apart so every period shows the same picture.
- Cued layers use `timeMode: "layer"`.

## Type

Usually none; a small mono counter-style label is possible, but counters are a known gap: key a few static
numbers or leave it out.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. The last frame matches the first exactly.
2. Belt and parts move at the same speed.
3. The press lands on a part, never between parts.
4. Red appears only on the press.
5. Parts change state exactly when processed.

## Build with the tools

Build the belt, parts, press and scanner as layers; set the loop period once in a script and derive every key
from it; render the first and last frames and compare them by eye on a contact sheet.

## Do / don't

- **Do** leave parts with the same spacing so the pitch is the same everywhere.
- **Don't** add a motion that has a different period from the rest; it breaks the loop.

## Originality guard

Draw your own machines. They must not copy a known factory sim game's machinery or a manufacturer's ad. The
looping belt, the press beat and the colour change are the style.

## Proven on

The assembly-line-loop film (a belt carrying parts through a press and a scanner on one period, looping
seamlessly).
