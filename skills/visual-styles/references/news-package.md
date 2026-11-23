# News package

A broadcast news package: a headline bar slides in, a lower third carries a name and role, a ticker runs along the
bottom, a location tag pops and a red "live" badge pulses. Navy and white with one red accent.

## Palette

Navy `#0b2447`, deep navy `#071a33`, white `#ffffff`, grey text `#c9d3e3`, ticker band `#f4f6fa` with navy text.
**The hero colour is the broadcast red `#d7262e`, reserved for the live badge and the headline's left tab.**

## The medium

- **Headline bar:** a navy rectangle with a red tab at its left end and a white headline in bold capitals.
- **Lower third:** two stacked bars, the name in white bold over a thinner role line in grey, with a thin white
  rule above.
- **Ticker:** a full-width pale band at the bottom with navy text scrolling left.
- **Location tag:** a small navy pill with a white pin dot.
- **Live badge:** a red rounded rectangle with "LIVE" and a white dot.
- Place everything inside the title-safe margin (about 5 % from each edge, more at the bottom for the phone UI).

## Motion habits

- **Slide and settle:** bars enter from the left over 0.45 s with an ease-out and a 12 px overshoot, text revealing
  0.1 s later with a mask wipe left to right.
- **Ticker:** a long text layer on a constant position track (about 140 px/s), looping with `ctx:loopOut("cycle")`.
  A ticker needs the text twice end to end so the loop shows no gap.
- **Live dot** pulses its opacity from 1 to 0.3 and back in 1.2 s, on a looping track.
- **Exit** by reversing the entrance, bars leaving in the order they came.
- Cued layers use `timeMode: "layer"`.

## Type

A bold condensed grotesque for headlines and names in capitals; a regular weight for roles and the ticker.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Every graphic sits inside the safe margin.
2. Red appears only on the live badge and the headline tab.
3. The ticker loop has no visible gap.
4. Text is readable against its bar at phone size.
5. Entrances and exits mirror each other.

## Build with the tools

Build the bars and text as layers; make the ticker text twice its visible length and loop its position; use a
mask or a clip rectangle for the text wipes. Check margins with `picsart_scene_query_layout`.

## Do / don't

- **Do** keep the headline to one line.
- **Don't** use a real network's logo, jingle graphics, name or colour pairing; don't stack more than three
  graphics at once.

## Originality guard

Invent your own station, names and headlines. It must not copy a real broadcaster's lower thirds, bug, ticker or
palette as a set. The bars, ticker and live badge are generic conventions.

## Proven on

The harbour-news-package film (a headline bar, a lower third, a scrolling ticker, a location tag and a pulsing
live badge).
