# Assembly manual

A flat-pack instruction sheet: a stool (a seat, three legs and four screws) assembled, pulled apart along its
axis, and tagged with numbered callouts and a quantity badge. Black line art on white with one orange accent.

## Palette

White `#ffffff`, ink `#202020`. **The hero colour is the orange `#f28c28`, reserved for screws, guide lines and
the numbered badges** so the parts the reader must handle are the only colour.

## The medium

- **Line art with white fills:** parts are drawn with 3 px ink outlines and a white fill so they hide what
  is behind them. The seat is a top ellipse, a short side band and a bottom ellipse; a leg is a tapered
  four-point path.
- **Screws** are a short vertical stroke with a small orange head.
- **Guides:** thin dashed orange lines (length 8, gap 7) between where parts will meet, shown only while the
  parts are apart.
- **Callouts:** a 1.5 px leader line from a part to a numbered disc (orange, 44 px) with a white numeral, and a
  "x4" quantity beside screws; a "step 2 / 5" label at a corner.

## Motion habits

- **Explode along one axis:** every part has position keys: rest, hold, move apart over 1.2 s with the
  ease-in-out easing (`[0.65, 0, 0.35, 1]`), hold, then return. Move parts by multiples of one step (the seat
  furthest up, legs down, screws between).
- **Callouts arrive after the explosion:** each leader line draws with `trim` over 0.4 s, then its disc pops with
  an overshoot (`[0.3, 1.5, 0.5, 1]`), 0.4 s apart; the quantity badge fades in last.
- Guides fade in as parts leave and out before they return.
- Cued layers use `timeMode: "layer"`.

## Type

A condensed display face in capitals for the step label and numerals; a plain grotesque for part names.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Parts move along one axis only.
2. Orange appears only on screws, guides and callout discs.
3. Every callout number matches a part.
4. Fills hide what is behind them.
5. The assembled and exploded states both read clearly.

## Build with the tools

Build each part as a shape layer with the position keys above; build leaders with `trim` and discs as scaled
shapes. Use `picsart_scene_contact_sheet` to check the assembled, exploded and callout states.

## Do / don't

- **Do** draw back parts first so fills hide lines correctly.
- **Don't** shade or add perspective to the parts; don't move parts diagonally.

## Originality guard

Design your own furniture and number your own steps. It must not copy a known flat-pack brand's manual
drawings, its pictogram person or its part names. The line art, single orange and numbered callouts are the
style.

## Proven on

The stool-manual film (a stool's seat, three legs and four screws assembled, exploded along an axis, with
numbered callouts and a quantity badge).
