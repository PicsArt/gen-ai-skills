# Riso overprint

A two-ink risograph poster: a fluorescent pink and a mid blue print over cream as halftone dot screens, the
plates overprint into a darker third colour, and every plate sits a hair off from where it should be, at a fixed
offset that kicks once on a beat.

## Palette

Paper `#f4efe4`, fluorescent pink `#ff4f8b`, blue `#2f5bd3`. **The hero colour is the pink, reserved for the
bird and the headline**; the blue carries the sun, sea bands and the small line. Where they cross, the multiplied
violet is a third colour you did not draw.

## The medium

- Portrait 1080 by 1350 on a cream paper layer, with exactly **two inks**. Each ink is one plate layer set to the
  `multiply` blend; overprint is the default and nothing is knocked out (the overlap is the point).
- **Blue plate:** a large sun disc and five horizontal bands for sea. **Pink plate:** an offset disc that
  overlaps the sun, a bird made from one closed eight-point path, the headline and the footer. (The footer
  uses the blue ink; it overprints nothing.)
- **Halftone, not stipple:** each plate's shapes are drawn in greys (a gradient on the sun and the disc, a flat
  mid grey on the bands, bird and type) and the plate layer carries `screentone` (`cell` dot, `size` 12, `angle` 75 for
  blue and 15 for pink, `ink` the plate colour, `paper` the sheet colour so the holes show the page). The two screens
  at different angles make the rosette where plates cross. Size 12 holds at 1080 by 1350 and under H.264 (ours, tune by render).
  A speckle made with `gaussian_blur` and `alpha_dissolve` is a different texture (stipple) and is not used here.
- Shapes are large and simple; the headline is a very big condensed face set at the top.

## Motion habits

- **Registration:** the pink plate sits at a fixed offset from the blue one for the whole shot (ours (7, -5) px). It
  moves only as an event: on a beat it kicks about (16, 10) px further and settles back over 0.4 s (ours, tune by render). Never a
  per-frame wiggle: the plate's position holds still between events. Put the plates in a nested `composition` with `fps` 12 so
  the kick steps.
- The sea bands drift sideways by a third of their pitch each step (position keys, looped), the bird hops a
  little up and sideways on each step; the sun and disc stay still.
- Nothing eases softly; a print has stepped, tiny motion only.
- Cued layers use `timeMode: "layer"`.

## Type

A very large condensed face for the headline, pink; a medium-weight condensed footer, blue. Upper case, set on
the page edges.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Two inks only; every shape is multiplied.
2. The overlap of pink and blue prints visibly darker, a third colour you did not draw.
3. Every plate is a dot screen, each at its own angle (15 and 75).
4. Registration is a fixed offset, kicked only on an event, never jittered.
5. The headline is the largest element and sits near an edge.

## Build with the tools

Build one layer per plate with the `multiply` blend and `screentone`; nest them with `fps` 12 over a paper
layer inside it, and key the pink plates' `position` (a constant offset and one decaying kick). Check the overlap
with `picsart_scene_contact_sheet`.

## Do / don't

- **Do** overlap the big shapes so the third colour shows.
- **Do** set small type (under about 40 px) solid in one plate colour, never screened, so it stays legible; halftone is for shapes and large lettering.
- **Don't** add a third ink, a drop shadow or a blur; a gradient is only the grey tone fed to the screen, never a visible fill.
- **Template rules, this style's choices** (the rules every recipe holds):
  - Rate split: the plates, the sea bands and the bird step together in the one nested composition (10 or 15 fps); there is no camera, and a roller sweep or any wipe runs at the root rate.
  - Nothing fades: a print arrives by being printed, one roller sweep (a `mask` edge crossing the poster once, about 0.5 s, ours, tune by render) or a hard cut on the beat; the only transitions are that sweep and the hard cut.
  - Print family: every plate is `multiply` over the paper, as above; knockout only where the design says so, and here it says nowhere (the overlap is the point); the texture is a halftone screen per plate (dots, not stipple); registration fixed per shot with one decaying kick.
  - Finish: the dot screen lives on each plate layer, so it travels with the plate and holds steady; nothing else is laid over the page and there is no film finish.

## Originality guard

Design your own poster, subject and wording. It must not copy a known risograph studio's artwork, a festival's
poster or a named illustrator's bird or sun. The two inks, the overprint and the fixed, evented misregistration are
the style.

## Proven on

The tide-club-riso film (a portrait pink-and-blue poster: sun and wave bands, an offset disc, a hopping bird, a
headline and a footer). The halftone plates and the fixed registration with its kick were also rendered on a 3 s test poster (1080 by 1350).
