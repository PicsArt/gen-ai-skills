# Comic panels

A western comic page in motion: panels pop onto a night-blue page one after another, each with its own colour
and dot tone, a short story is told across them, and the last panel lands a big sound word.

## Palette

Ink `#151515`, white `#ffffff`. Panel grounds: sky `#9fd3e6`, yellow `#f5d24a`, pink `#f2a0b8`, each with a dot
tone one step darker (`#2f6f9b`, `#d1462f`, `#7a2a5a`). **The hero colour is the burst yellow `#ffe23a`,
reserved for the sound word's star in the last panel.**

## The medium

- Each **panel** is a shape layer: an 8 px ink frame, its drawing inside, a **dot tone** over the ground (dots
  7 px on a 14 px pitch, about 55 % opacity, built as a row group with a `repeater` inside a column group with
  another), and a flat colour fill beneath. The panel's layer has a `mask.clip` of its own rectangle so nothing
  spills.
- Characters are flat shapes with 6 px outlines: a hatted animal in a coat (head, nose, hat, coat), a small
  second animal, a magnifier (a thick ring and a handle), a plate. Original animals only.
- **Speech:** a white balloon with a 5 px outline and a tail, or a caption box; lines are upper case in a
  condensed face with a typewriter text animation.
- A **sound word** ("GOTCHA!") inside a 14-point star burst in the last panel, with a few ink speed lines.

## Motion habits

- **Panels pop** one at a time: scale from 0.6 up to 1.06 and settle at 1 over 0.4 s while the opacity steps
  in, the starts about 2 s apart so each panel is read before the next.
- Inside a panel, things move simply: the animal walks in on an ease-out, a magnifier sweeps across, a crumb
  trail sits still. Keep one idea per panel.
- The burst lands with a scale overshoot, then jitters on twos: put it in a nested `composition` with `fps` 15 (12 under a 24 fps root)
  and apply the `wiggle` preset at a small amount.
- Cued layers use `timeMode: "layer"`.

## Type

A condensed comic face, upper case, ink on white; the sound word is large and has a heavy outline.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Every panel has the same frame weight and its own dot tone.
2. The story reads left to right, top to bottom, in order of appearance.
3. Text is short and inside balloons or caption boxes.
4. One panel is wider than the rest and carries the payoff.
5. The only yellow burst is in the final panel.

## Build with the tools

Make a panel layer per panel with the clip, key its pop, then add its contents as separate layers starting at
its start. Build the dot tone with nested repeaters. Use `picsart_scene_contact_sheet` to confirm the reading order.

## Do / don't

- **Do** leave gutters of the page colour between panels.
- **Don't** use gradients, shadows or panel borders of different weights; don't put the payoff in the first panel.

## Originality guard

Invent your own animals, plot and sound word. They must not resemble a known comic's cast, a famous
panel's composition, or a publisher's logo or lettering. The dotted panels, thick ink and lettered balloons are
the style.

## Proven on

The comic-mole-dossier film (three panels in turn: a hatted animal at night, a magnifier on crumbs, a small
culprit and a GOTCHA burst).
