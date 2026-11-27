# Pop-art burst

A comic-printing look: a toaster pops two slices with a "DING!" burst, outlined in black on a yellow ground
of Ben-Day dots, with radiating action lines. Primary colours, thick ink and one loud sound word.

## Palette

Ground yellow `#ffd23f`, red `#e8332a`, blue `#2a6fdb`, ink `#111111`, cream `#fff6e0`, toast `#f0c27a` and
`#a8622a`. **The hero colour is the red `#e8332a`, reserved for the burst, the lever and the dots on the
ground** so the pop of the joke is red.

## The medium

- **Plates, said honestly:** the yellow ground, the blue toaster and the red burst are flat colour plates (solid,
  no dots); the red Ben-Day dots are a separate screen that **overprints** the yellow ground with `multiply`
  (red over yellow prints a deeper red-orange) and is knocked out where an object sits; the ink key plate (the 10 px
  outlines and the type outline) is the only black.
- A yellow ground with a **Ben-Day dot field**: dots (12 px, 26 px apart) in red at full strength, `multiply` blend,
  built as a pair of row groups (an ellipse plus a `repeater` of columns; the second row offset half a step so the
  dots stagger) repeated by a row `repeater`. Halftone dots, not stipple.
- **Knockout halo:** a layer above the dots and below the objects holds the toaster and burst silhouettes in the ground
  yellow with a 12 px yellow stroke (ours), so the dots stop short of every object.
- **Registration:** the ink plate sits at a fixed small offset from the colour plates for the whole shot (ours (6, 4) px),
  and kicks about (14, 8) px further when the burst lands, settling back over 0.35 s (ours, tune by render). Never jittered per frame.
- Objects have **10 px ink outlines** and flat fills: a blue toaster body (rounded rectangle), dark slot caps,
  cream highlight strokes, two toast slices (a brown crust bar over a tan rounded block), a small red lever.
- **Action lines:** one thin triangle repeated 18 times by 20 degrees round a point (a `repeater` with
  `rotation`) in cream behind the toaster.
- The **burst** is a 14-point `star` item, red with a 10 px ink outline, and the sound word on top in a comic
  display face, yellow with a 10 px ink outline.
- Shading is the `halftone_dots` effect on the toaster (pointSize 20, contrast 80). The `screentone` effect is the
  tone-driven alternative: it reads each cell's luminance, sets the dot size, and has `angle`, `ink`, `paper` and
  `inkFollows`; on the object's own layer the dots travel with the object.

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

Build the dot field with nested repeaters (one repeater per group), the colour fills and the ink outlines as two
layers (so the ink can be offset), a halo layer between dots and objects, the action lines as one repeater, and the
burst as a `star` item. Put stepped parts in one nested composition.

## Do / don't

- **Do** let the burst overlap the toaster and the frame edge.
- **Do** keep the loud sound word ("DING!"): it is deliberate and part of this style's identity.
- **Don't** use gradients or soft shadows; don't use more than one burst.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - **Print family.** pop-art plates: ink is the only black; flat colour plates plus one red dot screen that overprints (`multiply`); the ink plate sits at a fixed small offset (ours (6, 4) px, tune by render), with a short decaying kick when the burst lands and no per-frame jitter; a knockout halo (ours 12 px of yellow stroke) keeps the dots off the toaster and the burst, and any caption sits on a cream strip.
  - **Line width.** no zoom, the 10 px outline is fixed.
  - **Finish.** the dot field is built inside the ground group so it stays on the page; no pan, so nothing slides across it; its pitch stays coarse enough for 1080p H.264.
  - **Height is shadow.** no blur; a lifted slice may carry a flat ink-coloured offset duplicate of its silhouette (ours 10 px, one light from the upper left), none once it rests.

## Originality guard

Invent your own joke and object. It must not copy a famous pop-art painting, a known comic's panel, or a named
artist's dots-and-speech-balloon composition. The Ben-Day dots, thick outlines and sound word are the style.

## Proven on

The ding-popart film (a toaster popping toast, a lever, radiating lines, a halftone-shaded body, a red DING!
burst). The overprinting dot screen, the halo and the ink registration with its kick were also rendered on a test frame (1080 by 1080).
