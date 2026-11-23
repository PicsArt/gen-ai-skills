# Weather cards

A forecast as a row of rounded cards: each card holds a day, an animated weather symbol and a temperature. Cards
rise in turn, the sun spins its rays, the cloud drifts, rain falls, and the current day's card lifts out.

## Palette

Backdrop sky gradient `#6fb6ff` to `#bfe3ff`, card `#ffffff` at 90 %, ink `#1f3a5f`, cloud `#e8eef6` with shade
`#c8d4e3`, rain `#4a90e2`. **The hero colour is the sun yellow `#ffd34d`**, reserved for the sun and the
temperature of the current day.

## The medium

- **Cards:** rounded rectangles (36 px radius) with a soft drop shadow; one symbol, one temperature and one day
  label per card.
- **Symbols are flat shapes:** a sun is a disc with ten rays (a star shape with long points), a cloud is three
  overlapping circles and a base, rain is short slanted strokes, snow is dots.
- **Temperature:** a large number with a small degree mark; values are set text, not counters.

## Motion habits

- **Cards rise** from 40 px below with an ease-out and fade, 0.14 s apart, left to right.
- **Sun:** the rays rotate slowly on a looping track (`ctx:loopOut("cycle")`); the disc breathes by 3 %.
- **Cloud:** drifts side to side by 14 px on a looping track with an ease-in-out.
- **Rain:** strokes fall along their slant and loop, offsets staggered; clip them to the card with `mask.clip`.
- **Current day:** its card lifts 16 px and scales to 1.06 with a slightly stronger shadow; the others dim to 70 %.
- Cued layers use `timeMode: "layer"`.

## Type

A rounded grotesque; large numerals for temperatures and a small-caps day label.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Every card has the same size and spacing.
2. Symbols stay inside their cards.
3. Yellow appears on the sun and the current temperature only.
4. Loops close exactly.
5. The current day is clear at a glance.

## Build with the tools

Build one card as a group and repeat it by script; clip falling rain with `mask.clip`; loop ambient motion with
`ctx:loopOut("cycle")`. Check the card row with `picsart_scene_query_layout`.

## Do / don't

- **Do** use one symbol style across all cards.
- **Don't** use a real weather app's icon set, layout or colour scheme.

## Originality guard

Draw your own symbols and write your own forecast. It must not copy a real weather app's icons, cards or
branding. The row of rounded cards with flat symbols is a generic convention.

## Proven on

The weather-cards film (cards rising in turn, a spinning sun, a drifting cloud, falling rain, a lifted current
day).
