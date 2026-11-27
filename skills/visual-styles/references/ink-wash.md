# Ink wash

A landscape brushed in ink on warm paper: grey-to-black dry-brush mountains with ink dots along their ridges,
bands of mist between layers that grow paler with distance, a small red sun, a fisherman in a boat on water
marked by a few strokes, a pavilion on a cliff, a swallow and willow strands in soft green. A brush title sits
in the empty paper. Everything moves slowly.

## Contents

[Finish](#finish) · [Palette](#palette) · [The medium](#the-medium) · [Pictures](#pictures) ·
[The character](#the-character) · [Motion habits](#motion-habits) · [Type](#type) ·
[Frame checklist](#frame-checklist-on-top-of-framemd) · [Build with the tools](#build-with-the-tools) ·
[Do / don't](#do--dont) · [Originality guard](#originality-guard) · [Proven on](#proven-on)

## Finish

No finish: flat warm paper with no grain look, no film look and no stepped rate. The softness comes from the
mist, not from a filter.

## Palette

Paper `#efe8d8`; ink `#1c1a18`; hill washes from mid grey `#8c8983` to light grey `#d6d0c2`, fading into the
paper; mist a near-white `#fbf8f1`; willow green, soft and pale, only on the willow. **The hero colour is the red
sun (`#e2553f`)**, used on nothing else.

## The medium

- **The landscape is built from shapes, not generated.** Each hill, cliff and peak is one smooth closed path
  (points joined as a smooth curve) with a vertical `gradientFill`: grey at its top, paler toward its foot, and
  on the far hills and the main peak an `alphaStops` ramp that fades the foot into the paper.
- **One heavy ink edge per hill**: an open path along the side that faces the light, a `stroke` 6-8 px with a
  `taper` (thin where it starts, swelling, thin or cut off by the frame where it ends). The other side has no
  line. A few thin tapered vertical strokes in dark grey mark a cliff face.
- **The main peak** carries the texture: some forty short diagonal tapered strokes (2-4 px, dark grey, half to
  most opaque) running down its face parallel to its left slope, a heavy tapered stroke down its right ridge,
  and a row of small black ink dots of uneven size along the top of that ridge.
- **Water** is the empty paper, marked only by a few thin tapered horizontal strokes, stacked under the boat as
  its reflection and scattered low in the frame.
- **Small things are generated SVG**, imported as shape paths: the boat, the willow, the swallow, figures and
  props (see Pictures). Drop each SVG's first path (its paper) and its other paper-coloured paths, and import the
  paths last to first: an SVG paints its first path at the back, a shape layer draws its first item on top. A
  gradient fill in the SVG becomes one flat tone, the mean of its stops.
- **Mist** is long paper-white rounded bars, wider than the frame and 25-45 px tall, `opacity` 0.45 to 0.85,
  under a `gaussian_blur` about as large as the bar is tall; the main one lies across the foot of the peak. No
  line round them; a lined or short mist bar reads as a screen bar.
- **Depth is layers fading paler**: far humps, the sun, the peak, mist, the water and the boat, low mist, then the
  near hill, the willow and the cliff with its pavilion in front, each its own shape layer.
- **The pavilion** is a few tapered strokes: an upturned roof curve, a second roof line, two posts and a rail.
- **The sun** is a flat red disc cut by the top edge of the frame.

## Pictures

Model: **Recraft V4.1 Vector** (`recraftv4_1_vector`, 3 credits a picture), for the small things only; the
landscape is shapes. Ask for one element per picture on plain paper, so it imports as one piece. Every prompt
ends with "Plain warm cream paper background, nothing else". Fill the braces and keep the rest.

**Figures (4:3 or 3:4).** Figures are small in this style; they are props in the landscape.

> Ink wash painting of a small fisherman in a wide pointed straw hat sitting in a narrow wooden boat, holding a
> long thin bamboo rod whose fine line drops straight into the water, drawn in loose black ink brush strokes
> with a grey wash inside the boat, a few short horizontal ripple strokes under the boat. Plain warm cream paper
> background, nothing else.

> Ink wash painting of {a scholar in a long robe walking with a staff, a woodcutter carrying a bundle of
> sticks, a child leading an ox, an old woman under an umbrella}, seen from the side, drawn in a few loose black
> ink brush strokes with a pale grey wash on the clothes, no face details beyond a stroke or two. Plain warm cream
> paper background, nothing else.

**Props and buildings (3:4).**

> Ink wash painting of {an arched stone bridge, a thatched hut among rocks, a pine leaning over a rock, a
> bamboo stem with a few leaves, a blossoming plum branch with small pale pink flowers}, drawn in black ink brush
> strokes with grey washes. Plain warm cream paper background, nothing else.

**Plants and creatures.**

> Ink wash painting of a willow: a dark grey ink branch curving in from the top, many long thin strands hanging
> down, each strand a soft pale green wash with a darker green edge, loose and sparse. Plain warm cream paper
> background, nothing else.

> Ink wash painting of a single swallow gliding with wings spread wide and a long forked tail, drawn in a few
> quick black ink brush strokes. Plain warm cream paper background, nothing else.

> Ink wash painting of {a crane standing on one leg, two ducks on still water, a carp turning in water, a
> small flock of birds in a line}, drawn in a few quick black ink brush strokes with a grey wash. Plain warm cream
> paper background, nothing else.

**What stays the same across a film:** the model, the paper sentence, "black ink brush strokes with grey
washes", red only on the sun, green only on willow and leaves.

## The character

Figures are SVG pieces from the prompts above, built once, saved to the library and placed by `uri` in every
shot (the mechanism is in [shapes-character](shapes-character.md)). In a landscape they are small and do not act:
a figure bobs, glides or walks by moving the whole piece. A figure that has to act gets parts: one SVG per part
from the same prompt, naming the part alone ("only the head and hat", "only the arm holding the rod").

- **Proportions:** about 6 heads tall, mostly robe.
- **Shapes:** loose brush strokes and a grey wash, no outline closed all round.
- **Face:** at most a stroke for an eye; usually none.
- **Controls:** the whole piece moves; parts, when there are any, turn about their joints a few degrees.

## Motion habits

- **Slow, and back to where it started.** In a 3 s loop each move goes out and returns with an ease-in-out: the
  layers pan left and back, a few pixels for the far humps and up to twenty for the cliff (parallax), the mist bands drift
  sideways in opposite directions, the boat bobs two or three pixels and rocks about a degree twice a loop, the
  willow sways a degree or two about its branch.
- **The swallow crosses the sky right to left** over the whole loop, off frame at both ends, below the title,
  flapping four times a second (its `scale` y keyed between full and about half, `scale` x negative so it faces
  its way).
- The sun and the title never move.
- Longer shots: the same moves at the same speed, or a slow pan across the landscape; never a fast cut inside a shot.
- Cued layers use `timeMode: "layer"`.

## Type

A brush face in ink (`bitterbrush-regular`, declared as a font asset): a short title at the top left and one
short word (a month, a place in the story) at the top right. Type holds still; no write-on.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Warm paper, ink greys and black; red only on the sun; green only on the willow.
2. Hills are smooth washes with one heavy tapered ink edge; the main peak has dry streaks and ridge dots.
3. At least one soft, unlined mist band, and far layers paler than near ones.
4. A large part of the frame is empty paper, holding the title.
5. Every move is slow and returns to its start at the end of a loop.

## Build with the tools

Draw each hill as a shape layer: one closed path with a `gradientFill`, then its tapered ink `stroke`s (list
items front first). Generate the small things with `picsart_generate` and import each SVG path with
`picsart_scene_import_svg_path` (last path first, the paper dropped), anchored where they pivot (the willow at its
branch, the boat at its waterline). Add the mist as rounded rectangles with a `gaussian_blur` effect. Check two
frames half a loop apart with `picsart_scene_contact_sheet`.

## Do / don't

- **Do** leave paper empty; the space is part of the picture.
- **Don't** line the mist, add a second accent colour, outline a hill all round, generate the landscape as one
  busy picture, or put a picture in instead of paths.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Rate split: none; every layer runs at the root rate.
  - Boil: none; the brush strokes hold still.
  - Arrivals: pieces are in place from the first frame; between shots a slow fade through paper.
  - Finish: none (see Finish).

## Originality guard

Compose your own landscape: invented peaks, your own placement of sun, boat and cliff. Never copy a known
painting, or a named painter's scroll. The ink washes, the mist and the single red are
the style.

## Proven on

The river loop: a peak with dry streaks, a ridge of dots and a cropped red sun; far humps; drifting mist; a
fisherman bobbing on the water with his reflection; a near hill, a willow and a pavilion cliff in parallax; a
flapping swallow crossing the sky; a brush title and a month word. The boat, willow and swallow came from
the three prompts for them above.

**Not proven:** the bracketed variants and a figure built from parts.
