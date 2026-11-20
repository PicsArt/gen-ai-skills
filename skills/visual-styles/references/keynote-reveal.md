# Keynote reveal

A dark product reveal: a title types out of black, a light sweep crosses the object, the object rises into
frame with a soft glow and a thin line of specs fades in underneath. Very little colour, very slow.

## Palette

Black `#050506`, near-black panel `#0e0e12`, text white `#f5f5f7`, grey `#8e8e93`. **The hero is the white shine**:
a soft white sweep and highlight on the object's edge; the reveal needs no hue.

## The medium

- A black field with a very faint radial lift behind the object (a gradient fill, white at 6 % alpha to 0).
- **The object** is a simple product shape (a rounded slab, a puck, a pair of earbuds) built from two or three
  dark-grey fills with a thin lighter rim line along its upper edge.
- **The shine:** a narrow diagonal band with a gradient fill, white at 0 to 35 % to 0 alpha, clipped to the
  object with `mask.clip`.
- **Specs:** a single line of small grey text with generous letter spacing.

## Motion habits

- **Slow ease:** every move uses a long ease-in-out (`[0.65, 0, 0.35, 1]`) of 1.2-1.8 s; nothing is quick.
- **Title:** reveal with `typewriter` or a word-by-word fade of 0.35 s each.
- **The rise:** the object moves up 40 px and scales from 0.94 to 1 as its opacity fades in; the glow behind it
  grows with it.
- **The sweep:** the shine band moves across once, over 1.6 s, after the object has settled.
- **Specs** fade in last, 0.4 s apart, and the title lifts 10 px to make room.
- Cued layers use `timeMode: "layer"`.

## Type

A light-weight, wide-tracked grotesque in white for the title; the same family in grey for specs. No bold.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. The background is black, not grey.
2. No colour other than white and greys.
3. Every move takes over a second.
4. The sweep is clipped to the object.
5. Text never sits on the object.

## Build with the tools

Build the object from two or three shapes; give the shine a gradient fill with alpha stops and clip it with
`mask.clip`; add a faint `glow` effect on the rim. Preview a frame at the shine's midpoint.

## Do / don't

- **Do** hold the final frame for a full second.
- **Don't** add lens flares, particles or a spinning object.

## Originality guard

Invent your own product shape, name and specs. It must not copy a real company's product, logo, typeface or
launch-event graphics. The black field, slow rise and white sweep are the style.

## Proven on

The dark-keynote-reveal film (a title typing out of black, an object rising with glow, a light sweep across it, a
line of specs).
