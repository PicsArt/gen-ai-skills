# Classic cartoon (the default)

The look a film gets when no style is named: thick dark outlines, flat saturated colour, rounded friendly
shapes and bouncy, readable motion. The library characters and places are drawn in it, so it needs no
restyling.

## Finish

A light grain and vignette on one `scene_ref` of the whole film (see "Build with the tools"); motion at the scene's own rate.

## Palette

Three to five colours per film, from the request or the brand: ink `#1f1b2e` (never pure black), a light
neutral `#fff6e5`, one main, one support. **The hero colour is a warm orange `#ff7a2f`, reserved for the
subject's clothing or skin accent** and never used on the world. Skin and fur are flat; one hard-edged shade
tone a step darker is allowed. A background is one calm field or a two-band sky and ground.

## The medium

- Every character and prop is a shape layer of flat fills with a `stroke` of 6-8 px in the ink colour,
  `lineCap: "round"`, `lineJoin: "round"`. Limbs and tails take a stroke `taper` so the line thins at the ends.
- Forms: big head, small body, round hands, simple feet. Eyes are a white ellipse, a dark pupil and one shine
  dot; the mouth is a curved stroke that opens into a filled shape to speak.
- A place is a ground band, a back wall or hill and two or three chunky props with one detail each. No
  texture, no gradients except a two-band sky.
- A library character is placed as a `scene_ref` layer sized by its `transform.scale`; its walk, wave and
  talk are its rig actions, never re-keyed by hand.

## Motion habits

- Squash and stretch on landings, anticipation before a big move, overshoot on arrival
  (`[0.3, 1.5, 0.5, 1]`), holds of four to eight frames on key poses.
- Smooth motion at the scene's own rate; the style does not step time. Life comes from idle `wiggle` on
  hair, tails and antennae (different `seed` per part) and `random_pulse` blinks.
- Cued layers (anything that starts after 0) use `timeMode: "layer"` so their keys count from their start.

## Type

One heavy rounded display face for titles, 60-110 px, ink on light or white on dark, with the same outline
weight as the drawings. Captions in a plain bold sans.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. The outline weight is the same on the character, the props and the title lettering.
2. The hero orange appears on the subject only.
3. The horizon and ground line sit in the same place across shots of one place.
4. At least three small background movers: a cloud, a bird, a swaying plant, a passer-by.

## Build with the tools

Place the library character, play its `content.animation` actions in order, put the place behind it as shape
layers or a `scene_ref` of a place scene. A finish look (light grain, vignette) goes on one `scene_ref` of the
whole film, never on a shape layer. Validate, preview, then `picsart_scene_contact_sheet` the clip.

## Do / don't

- **Do** keep shapes round and the colour few; let motion carry the personality.
- **Don't** paste this look onto another style's film, and don't add texture or glow.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Easing: arrivals use the small back-ease `[0.3, 1.5, 0.5, 1]`; a big move anticipates with a small pull-back, holds
    four to eight frames, then snaps; walk and rig loops and drawn lines are linear; a cloud or plant drift is an
    ease in and out.

## On a part sheet

When a character comes through the SVG part-sheet flow (the `character-rigging` skill), every arm and leg is two pieces, an upper and a lower, each its own group, overlapping at the elbow or knee. That is a rig requirement no style overrides: the builder refuses a sheet whose limb is one piece. Draw each limb as two pieces, upper and lower, with the same fill and a rounded joint end overlapping the other piece; leave out any line across the joint, because the builder skins the pair into one outline there.

## Originality guard

Invent the cast and the world. It must not resemble a known studio's mascot, princess, robot or talking
animal or their famous poses, a known series' house, street or title card, or the lead characters of a game or
streaming hit.

## Proven on

The library characters and places, and the cartoon film scenes built from them.
