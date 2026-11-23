# Documentary collage

A history told on a cream desk: faded archival photographs taped down at a tilt, cut-out objects with a white sticker
edge, one red disc carrying a big year, a keyword on a red bar, a dashed route that connects two things and a rubber
stamp that lands last. A single idea to a frame, a slow push-in, film grain over all of it.

## Finish

The picture is built as one scene and the film finish goes over it (see Motion habits): grain, a little dust and a
vignette, no paper texture (the cream paper is already in the fills).

## Palette

Old cream paper `#ece2cc` to `#f3ead6`, charcoal ink `#2b2622`, archival photos in warm sepia. **The hero colour
is one red `#c23a2b`**, used for four things only: the disc, the keyword bar, the dashed route and the stamp. No
second accent.

## The medium

- **Archival print:** a sepia photograph with a cream border about 22 px wide, a soft drop shadow, a strip of tape
  across one corner and a tilt of 3 to 5 degrees.
- **Cut-out:** an object with its background removed, a white sticker edge about 12 px at 1× and a soft shadow.
- **A halftone dot patch** in one corner at 16 % ink, drawn as nested repeaters.
- **The disc:** a flat red circle behind the title; the hero is a year or a number in a heavy condensed face
  (Bebas Neue), charcoal on the red.
- **The keyword bar:** one word in cream on a red bar that wipes in from the left under the title.
- **The route:** a dashed red line with a round end that connects two things (from, to); its dashes keep
  marching after it has drawn on.
- **The stamp:** a double ring and one word in red, tilted, that lands from 1.6× to 1×.
- **Border, shadow and sticker edge are baked into the picture today.** A look would be cleaner, but a card
  look outlines the layer's box and a media layer's box is the composition size, so it cannot hug the print.
  Bake them into the PNG until a shape-following look exists.

## Motion habits

- **Pieces slide in from an edge** and settle with a small overshoot; each lands once and then holds.
- **The route draws on** (`trim` `end` 0 to 1), then its dashes march with a dash-offset track, which keeps a long
  hold alive without a second move.
- **A slow push-in** of about 4.5 % over the shot, the paper on a slower scale than the pieces for parallax.
- **The film finish:** `analog_film_finish` with grain 0.45, dust at most 0.15, vignette 0.45.
- **One thing drifts** besides the push-in: smoke, a cloud or water moving sideways, with the rest held still.
- **Pieces that appear and vanish** use opacity `step` keys at least `1/fps` apart (a 0.001 s gap lands on the same
  frame and blends every window); see the easing part of the `scene-animation-reference` skill.

## Type and captions

A heavy condensed face for the year and title (Bebas Neue), a plain sans for the keyword and stamp, one size per
role. When the film is narrated, set the words as heavy captions with a thick outline, two lines at most, broken where the sentence
naturally pauses, with one keyword in the red.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. A single idea in the frame; the red appears only on the disc, the bar, the route and the stamp.
2. The route connects two things, from and to.
3. Nothing is cut by the frame edge, and the number fits inside its disc.
4. Photos are sepia, tilted and taped; cut-outs have the sticker edge.
5. The grain and vignette are on and there is no dissolve inside a shot.
6. Test the frame: if it reads like a movie frame it is wrong; if it reads like a printed editorial page it is right.

## Build with the tools

Source pictures: an archival photograph generated as faded sepia with grain and scratches, a cut-out made with the
background-removal tool, the print border and shadow baked in. Build the pieces as layers with `position` keys
(slide, overshoot), the route as a `trim`med dashed path, the stamp as a ring and text group with a scale key, the
dot patch as repeaters. Place the scene once as an asset and put the film finish look on it. Validate, preview
the year beat, the route beat and the stamp beat, then check a contact sheet across the shot.

## Do / don't

- **Do** give each frame one idea and let the route join two things.
- **Do** keep the push-in slow; the stamp is the only hard hit.
- **Don't** add a second accent colour, a 3D orbit, shake, or a dissolve inside a shot.
- **Don't** set a number wider than its disc.

## Originality guard

Take the props, ornaments and stamp from the subject (a ship, a cable, a coast) and keep the grammar: border, shadow,
dots, tape and one accent. Invent your own events, objects and layouts; generate your own faded photographs. Do not reproduce a real archive's
photograph, a broadcaster's or studio's title card or lower third, or a named documentary's graphics. The cream
desk, tilted prints, red disc and stamp are generic conventions.

## Proven on

The cable film: a tilted sepia ship photograph, a red disc with "1858", the keyword "OCEAN" wiping onto a red bar,
a cut-out cable coil with a dashed route to an "ATLANTIC" stamp (6 s, 1280×720, checked frame by frame).
