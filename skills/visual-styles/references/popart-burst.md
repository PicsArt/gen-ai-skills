# Pop-art burst

A comic-printing look: a toaster pops two slices with a "DING!" burst, outlined in black on a yellow ground
of Ben-Day dots, with radiating action lines. Primary colours, thick ink and one loud sound word.

## Palette

Ground yellow `#ffd23f`, red `#e8332a`, blue `#2a6fdb`, ink `#111111`, cream `#fff6e0`, toast `#f0c27a` and
`#a8622a`. **The hero colour is the red `#e8332a`, reserved for the burst, the lever and the dots on the
ground** so the pop of the joke is red.

## The medium

- A yellow ground with a **Ben-Day dot field**: dots (12 px, 26 px apart) in red at about 90 % opacity, built as
  a row group (an ellipse plus a `repeater` of columns) inside a column group (a second `repeater` of rows,
  offset half a step per row so the dots stagger).
- Objects have **10 px ink outlines** and flat fills: a blue toaster body (rounded rectangle), dark slot caps,
  cream highlight strokes, two toast slices (a brown crust bar over a tan rounded block), a small red lever.
- **Action lines:** one thin triangle repeated 18 times by 20 degrees round a point (a `repeater` with
  `rotation`) in cream behind the toaster.
- The **burst** is a 14-point `star` item, red with a 10 px ink outline, and the sound word on top in a comic
  display face, yellow with a 10 px ink outline.
- Shading is the `halftone_dots` effect on the toaster (pointSize 20, contrast 80). There is no tone-driven dot
  screen on arbitrary art yet: a shaded object gets the effect, a flat object stays flat.

## Motion habits

- The gag is one beat: the lever drops, a pause, then **pop**: the toast shoots up (position keys with an
  overshoot easing), the toaster squashes (`[1.08, 0.9]` back to 1), the action lines flash on and the burst
  scales in from 0 with a strong overshoot.
- Hold the burst, rocking it a few degrees with the `wiggle` preset; step the action lines' rotation on twos by
  putting them in a nested `composition` with `fps` 15 (12 under a 24 fps root).
- Cued layers use `timeMode: "layer"`.

## Type

A comic display face, yellow on a heavy black outline, upper case, one word with an exclamation mark.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Every object has the same thick ink outline.
2. Only the three primaries, ink, cream and the toast browns.
3. The dots stagger and stay behind the objects.
4. One loud sound word inside a burst at the moment of the pop.
5. The pop has anticipation (the lever), the hit and a hold.

## Build with the tools

Build the dot field with nested repeaters (one repeater per group), the objects as shape layers with outlines,
the action lines as one repeater, and the burst as a `star` item. Put stepped parts in one nested composition.

## Do / don't

- **Do** let the burst overlap the toaster and the frame edge.
- **Don't** use gradients or soft shadows; don't use more than one burst.

## Originality guard

Invent your own joke and object. It must not copy a famous pop-art painting, a known comic's panel, or a named
artist's dots-and-speech-balloon composition. The Ben-Day dots, thick outlines and sound word are the style.

## Proven on

The ding-popart film (a toaster popping toast, a lever, radiating lines, a halftone-shaded body, a red DING!
burst).
