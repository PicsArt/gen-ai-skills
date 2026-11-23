# Riso overprint

A two-ink risograph poster: a fluorescent pink and a mid blue print over cream, the layers overlap into
violet, edges are soft and speckled, and every plate is a hair off from where it should be, stepping eight
times a second.

## Palette

Paper `#f4efe4`, fluorescent pink `#ff4f8b`, blue `#2f5bd3`. **The hero colour is the pink, reserved for the
bird and the headline**; the blue carries the sun, sea bands and the small line. Where they cross, the multiplied
violet is a third colour you did not draw.

## The medium

- Portrait 1080 by 1350 on a cream paper layer, with exactly **two inks**. Each ink's shapes are filled in its
  colour and set to the `multiply` blend.
- **Blue plate:** a large sun disc and five horizontal bands for sea. **Pink plate:** an offset disc that
  overlaps the sun, a bird made from one closed eight-point path, the headline and the footer. (The footer
  uses the blue ink; it overprints nothing.)
- **Grain:** on each plate a `gaussian_blur` of about 6 followed by `alpha_dissolve` (size 2, density 0.9, fixed
  seed, a different seed per plate) gives the soft speckled edge of a stencil (ink grain, not brushwork: keep the dissolve, a `brush` would draw paint streaks).
- Shapes are large and simple; the headline is a very big condensed face set at the top.

## Motion habits

- **Registration shift:** the `wiggle` preset on each plate's position (about 2 px, `frequency` 8, a different
  `seed` each). Put the plates in a nested `composition` with `fps` 8 or 12 so the shift steps.
- The sea bands drift sideways by a third of their pitch each step (position keys, looped), the bird hops a
  little up and sideways on each step; the sun and disc stay still.
- Nothing eases softly; a print has stepped, tiny motion only.
- Cued layers use `timeMode: "layer"`.

## Type

A very large condensed face for the headline, pink; a medium-weight condensed footer, blue. Upper case, set on
the page edges.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Two inks only; every shape is multiplied.
2. The overlap of pink and blue produces a visible violet.
3. Every plate's edge is speckled by the same grain method.
4. Registration moves in small steps, never a smooth drift.
5. The headline is the largest element and sits near an edge.

## Build with the tools

Build one shape layer per plate item with the `multiply` blend and the two grain effects; nest them with
`fps` 10, and apply `wiggle` to the plate layers inside it with `picsart_scene_apply_preset`. Check the overlap
colour with `picsart_scene_contact_sheet`.

## Do / don't

- **Do** overlap the big shapes so the third colour shows.
- **Don't** add a third ink, a gradient or a drop shadow; don't blur more than the grain recipe.

## Originality guard

Design your own poster, subject and wording. It must not copy a known risograph studio's artwork, a festival's
poster or a named illustrator's bird or sun. The two inks, the overprint and the stepped misregistration are
the style.

## Proven on

The tide-club-riso film (a portrait pink-and-blue poster: sun and wave bands, an offset disc, a hopping bird, a
headline and a footer, registration stepping at 8 fps).
