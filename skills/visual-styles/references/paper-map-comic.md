# Paper map comic

A short story about who owns which land, told with scraps of card on a printed map laid out as comic panels. Each
change of ownership is a visible move of a scrap: it lands, covers or cuts. Countries are paper pieces, people are small
paper puppets, and the panels are sheets that slide across the page. It is a handmade tale, not a data map and not an
animated atlas.

## Palette and colour roles

| Role | Colour | Its one job |
|---|---|---|
| ground | `#f3ecd8` | the page and the gutter |
| field | `#8fb8c0` | the sea inside a panel |
| field | `#58838c` | flat shadows on the sea |
| line | `#2a1c14` | panel borders, cut marks, speech text |
| line | `#fff6e0` | the pale card edge on every paper piece and the speech bubble |
| field | `#d9a441`, `#c4573a`, `#6f9a6b` | each country's own paper (ochre, rust, sage in the proof) |
| field | `#d9795c` | a taken piece: its new owner's colour one step lighter |
| accent | `#7d2a18` | the stamp, and nothing else |

A taken territory shows the taker's colour one step lighter, never the colour of its own country.

## The medium

- Paper pieces are flat polygons in one colour with a pale 8 px edge, like card stock, and nothing is translucent.
- Height is shadow: a piece held in the air throws a flat offset shadow (70 px in the proof) and lands with a thin
  one (9 px); the offset shrinks with the fall and the piece is slightly larger while it is up.
- The page is a comic page: each panel is a bordered sheet (12 px ink border) with the gutter showing round it.
- Puppets are cut-paper figures (shapes with the pale edge), simple, with one face feature that moves.
- Speech: the bubble sits above the speaker and its tail ends at the mouth, drawn over the head so the tip reaches it.
- Numbers and names use the heavy condensed face; keep any date or count as plain figures.

## Rates

| Held rate | Root rate |
|---|---|
| puppets (12 fps nested composition), so their pops step | map pieces, the slap, the stamp, panel slides, bubbles and text |

## Boil

Puppets step on twos (the pop and the jaw both sit inside the 12 fps composition); paper pieces and panels do not boil. Edges are straight; a tear or rough edge, if used, holds a
constant evolution so it does not crawl.

## Line width under a zoom

Scales with the world: panel and card edges are drawn at full-frame size and no camera zoom is used between panels.

## Motion habits, and the transitions

- Countries arrive on a small overshoot (scale 0.85 to 1.05 to 1 in 0.45 s), staggered.
- A cut mark is drawn on (`trim`) before a piece lands on it; the piece flies in from outside the panel (0.5 s,
  ease in), landing as its shadow thins.
- The stamp slams (scale 1.6 to 1 over 0.25 s) and the page shakes for four frames (a few px).
- Between panels the page moves: the first sheet slides out as the next slides in on a back ease (0.6 s), so the
  camera is the page. No fades or wipes.
- A puppet pops with a spring on twos; a bubble pops with an overshoot after the puppet has arrived.

## Type

Heavy condensed: the caption box at 48 px, the stamp at 96 px, speech at 100 px, all in the ink tone.

## Scene features used

Nested `composition` layers as panels, closed paths with `fill` and `stroke`, `trim`, a 12 fps nested composition for
puppets, scale and position keys with back and ease curves, `timeMode: "layer"`.


## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Every piece has the pale edge and an opaque fill.
2. A taken piece is the taker's colour one step lighter.
3. Shadow offset follows height: large in the air, thin when down.
4. The bubble tail reaches the mouth.
5. The page moves between panels; nothing fades.

QC: lean on the viewer's pass at normal speed (does the slap read as a piece landing), the phone-size read of the speech and the colour roles.

## Build with the tools

Build each panel as its own nested composition and slide them as layers. Make each country, patch and puppet part a
closed path; copy a piece for its shadow and animate the copy's offset. Put the puppet in a 12 fps composition. Check
the slap and the panel slide frame by frame on a contact sheet.

## Do / don't

- **Do** let every change of ownership be a move of paper the viewer can follow with the eye.
- **Do** keep the number of pieces small enough that every one reads.
- **Don't** use a transparent overlay, a blur, a fade or a map projection effect.
- **Template rules, this style's choices** (the rules every recipe holds):
  - Rate split: puppets step, paper and panels run at the root rate.
  - Nothing fades: pieces fly in, panels slide, bubbles and stamps pop.
  - Height is shadow: a flat offset duplicate whose offset is the height.

## Originality guard

Invent your own countries, story and wording. It must not trace a real map or copy a known comic or history channel. The
ownership shown by moving card scraps, the lighter taker colour and the sliding page are the style.

## Proven on

A 5 s portrait clip (1080 by 1350, 24 fps) of two panels: three paper countries arrive, a cut mark is drawn, a lighter
patch of the neighbour's colour is slapped across the border with its shadow shrinking, a TAKEN stamp slams on the patch and the
page shakes; the page then slides to a second panel where a paper ruler pops on twos, its jaw cycling, and a bubble says its line with the
tail at its mouth; exported on the hosted renderer.

**Not proven:** a `page_curl` peel, a torn edge, a cut-and-slide of a piece along a dashed line, coast ripples, a
puppet cut from a drawing with IK limbs, and a soft shadow for a piece high in the air (the proof's shadows are flat).
