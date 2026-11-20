# Painted anime looks

[Painted anime](painted-anime.md) draws its characters in the TV cel look by default. The looks below are
variants of that character, each a different fill for the description slot of the frozen part-sheet template
(`character-rigging`, the SVG part-sheet route). The template itself stays unchanged: only the description
changes, and the rig is built from the sheet as usual. The background is unchanged: an SVG band layout painted over
once ([painted anime](painted-anime.md)), never a text-to-image background.

**Use a look only when the user's words ask for it** ("chibi", "90s anime", "shoujo", "watercolour"…).
Otherwise keep the cel default. A look is not a picker choice: it gets a style row of its own only once it has a
matching place and a walk proof (a rigged character from its sheet walking through that place, judged at normal
size). Bold graphic is the first with a walk proof; its place does not match it yet.

## Routes

| Look | Route | Rigs on stage today |
|---|---|---|
| chibi, 90s retro, shoujo, glossy 2020s, bold graphic | SVG sheet as is | yes, with the joint seams below |
| watercolour | SVG sheet, then one paint-over of the whole sheet | no: waits for character `paintUrl` |

**SVG sheet as is.** Generate the sheet with the look's description, check it with `picsart_scene_build_model`
(`character: {svgUrl, check: true}`), and build the rig from it. Every proof sheet below passed the sheet checks
except where its flaws say otherwise.

**SVG sheet plus paint-over.** An SVG sheet cannot carry a painted medium: asked for watercolour, it gives clean
vector shapes with soft gradients, with no wet edges, pooling or paper. Use the SVG sheet for structure only.
1. Drop the joint and socket marker groups and rasterize the sheet.
2. Repaint it with an image model that takes a reference image. The prompt has this shape: "Repaint IMAGE 1 as a
   real hand-painted [medium] illustration. Keep IMAGE 1's layout exactly: the same character in the same three
   poses, every part at exactly the same position, size and outline; do not move, add or remove anything and do
   not change any silhouette edge. Paint inside each shape only: [the medium's marks]. A limb is painted as one
   continuous wash from shoulder to hand and from hip to ankle. Plain paper background."
3. The painting registers to the SVG parts within a few px; each SVG part, grown by about 3 px, is that part's
   mask on the painting.

Rigging the painted sheet waits for the queued `paintUrl` input on `picsart_scene_build_model` `character`, which
keeps the SVG's parts and joints and fills each part from the painting. `picsart_scene_cut_parts` does not do it today: it
cuts the parts by `labels.masks`, but it refuses masks together with `sheets`, and its `rig` needs `sheets`.

## What waits for the builder

- **Joint seams.** On most sheets the lower part's rounded end, outlined and painted over the upper part, shows
  at rest as a disc or seam at the knee and elbow. It is visible at normal size on watercolour, retro, shoujo,
  glossy and graphic. A prompt sentence does not fix it (the template notes why); the queued builder fix draws
  each limb as one outline across the knee and elbow. Until it lands, a costume piece over the joint hides the
  seam: the graphic sheet's knee pads cover its knees completely.
- **Painted looks.** Watercolour rigs only once character `paintUrl` lands.

## The looks

Fill `{subject}` (who it is) and `{outfit}`, keep the rest word for word, and append the template. Each
description ends where the template's "in a single SVG" begins.

### Chibi

> {subject} drawn in cute anime chibi style: about 2.5 heads tall, head as large as the whole body below it, short
> stubby arms and legs, small round hands, small rounded feet; huge round anime eyes filling the middle of the face
> (each eye a tall oval, a bright iris lighter at the bottom, one big and one small white highlight dot), no nose
> line, small round cheeks; hair as one round mass of 5 soft spiky tufts and one strand curling up from the crown;
> thick even dark-navy outlines (never pure black); {outfit}; cel shading: every part has flat bright base colour
> plus ONE hard-edged darker shadow shape of the same hue on the side away from a light at the upper left, and the
> hair has one pale highlight band

- **Reads by:** the 2.5-head proportion, eyes filling the face, no nose, thick soft-navy line.
- **Proof sheet:** `anime-sheet-chibi.png` (with its prompt), kept locally in the style catalogue renders.
- **Flaws:** in the side view the far arm came out a third thinner than the near arm (the far-arm check fails).

### 90s retro

> {subject} drawn in 1990s cel-animation anime style: about 7.5 heads tall, long legs, broad square shoulders,
> angular jaw with a sharp pointed chin; narrow sharp anime eyes (each eye an angular almond shape under a heavy
> straight dark upper line, one small sharp white highlight), a nose drawn as a sharp angled line with a small
> shadow wedge, thin straight eyebrows; tousled hair falling over the forehead in 6 long sharp angular locks, one
> lock crossing between the eyes; bold dark outlines of even medium weight in a deep brown-violet; {outfit}; retro
> cel shading: every part has a slightly desaturated base colour plus ONE large hard-edged shadow shape tinted
> toward violet (no gradient, no soft edge) on the side away from a light at the upper left, the hair has two
> sharp narrow white-blue highlight streaks, the whole palette muted and dusty like an old film cel

- **Reads by:** the long angular face and jaw, a violet tint in every shadow, the dusty palette, and the sharp
  streak highlights.
- **Proof sheet:** `anime-sheet-retro90s.png`.
- **Flaws:**
  - The neck is a wide flat block.
  - The far arm is too thin in the three-quarter view (the check fails).
  - Hard seams cross the trousers at the knees and thighs in all three views.

### Shoujo

> {subject} drawn in shoujo anime style: about 7 heads tall, long slender legs and arms, small delicate hands; very
> large sparkling eyes (each eye a tall rounded shape under a thick dark upper lash line with three small lash
> flicks at the outer corner, the iris darker in its top half and lighter and pinker in its lower half, one large
> white highlight, two small white sparkle dots and a tiny white star), a tiny nose as one short line, soft small
> pointed chin, faint pink blush lines under the eyes; very long wavy hair: side-swept bangs of 5 soft pointed
> locks and two long side locks over the shoulders, the rest falling behind the back to the waist in soft waves
> (that back hair is hairBack); thin rosy-brown outlines (never black) of even weight; {outfit}; soft cel shading:
> every part has a pastel base colour plus ONE hard-edged darker shadow shape of a cool pink-violet tint on the side
> away from a light at the upper left, and the hair has one pale shining highlight band

- **Reads by:** the sparkle eyes (lash flicks, star, two-tone iris), waist-long hair, the pastel palette and the
  rosy line.
- **Proof sheet:** `anime-sheet-shoujo.png`.
- **Flaws:**
  - Knee discs show in all three views, and the sleeves have a seam at the elbows.
  - Naming the skirt as its own group in `{outfit}` ("a pleated knee-length skirt, its own skirt group") built
    correctly.

### Glossy 2020s

> {subject} drawn in glossy modern 2020s TV-anime style: about 7 heads tall, long slim legs, narrow shoulders;
> large glossy anime eyes (each eye a tall rounded shape under a thin dark lash line that thickens at the outer
> corner, the iris a vertical gradient from deep at the top to bright at the bottom, a darker pupil, one large soft
> white highlight, one small white dot and a thin bright crescent reflection in the lower iris), a tiny nose as one
> short line, small pointed chin, a soft pink blush gradient on each cheek; hair drawn as one mass with fine strand
> lines, side-swept bangs of 6 thin pointed locks; very thin even outlines in a dark cool grey-violet (never black),
> slightly lighter than the shadows; {outfit}; modern anime shading: every part has a clean flat base colour, ONE
> hard-edged darker shadow shape of a cool blue-violet tint on the side away from a key light at the upper left,
> and ONE thin bright rim-light strip of pale warm peach along the edge of the shadow side (the back light), the
> hair has one glossy highlight band, the palette clean and bright with cool shadows

- **Reads by:**
  - Gradient irises with layered highlights.
  - A cool shadow plus a thin warm rim light on every part. The rim light is drawn on the parts, so it turns with
    the limbs.
  - A blush gradient.
- **Glow:** the bloom and glow of modern anime is not in the sheet. Add it over the finished frame with the
  [finishing pass](painted-anime.md#finishing-pass).
- **Proof sheet:** `anime-sheet-glossy.png`.
- **Flaws:** knee discs, puffy sleeve bulges at the elbows, and a slightly open mouth instead of the neutral one.
- **Keep socks short in `{outfit}`:** a sock that crosses the knee splits there.

### Bold graphic

> {subject} drawn in bold graphic action-anime style: about 7 heads tall, long legs, broad angular shoulders, a sharp
> angular jaw; sharp angular anime eyes (each eye a wide almond under a thick dark upper line, a bright iris with a
> hard darker top half, one sharp white highlight), a nose drawn as one angular wedge, thick angled eyebrows; spiky
> hair as one bold mass of 8 big sharp triangular spikes sweeping back; bold thick outlines of even heavy weight in
> near-black deep navy; {outfit}; graphic shading: every part has a saturated flat base colour plus ONE big
> hard-edged angular shadow shape (straight-edged polygons, never curves) in a much darker tone of the same hue on
> the side away from a light at the upper left, and the hair has two sharp angular white highlight shards; a
> high-contrast palette of only four colours, like a poster

- **Reads by:** a four-colour poster palette, polygon shadows, the heavy line, and big spiky hair.
- **Proof sheet:** `anime-sheet-graphic.png`.
- **Flaws:** discs at the elbows. Knee pads in `{outfit}` hide the knee seam completely.
- **Walk proof:** walked through the painted shopping street, feet planted, passing behind a bike and a lamp
  post. The flat poster look clashes with the painted street: it needs a matching graphic place before it gets
  its own row.

### Watercolour (paint-over route)

The SVG sheet uses a soft storybook description:

> {subject} drawn in a soft hand-painted storybook-anime style: about 6 heads tall, gentle rounded proportions;
> large gentle anime eyes (each eye a rounded shape under a soft thin dark-brown upper line, an iris with a lighter
> lower half, one soft white highlight), small nose as one tiny curve, rosy cheek blush ovals; hair drawn as one
> soft mass with rounded locks at the ends; very thin warm sepia outlines (never black) that thin out at the ends;
> {outfit}; soft shading: every part has a muted pastel base colour that fades by a soft linear gradient to a
> slightly deeper tone of the same hue on the side away from a light at the upper left, the whole palette muted and
> warm like a sunlit summer picture book

The paint-over prompt names the medium's marks: "transparent watercolour washes with wet-in-wet blooms, pigment
pooling into darker hard edges where a wash dried, soft colour bleeding between neighbouring tones of the same
part, the white paper grain showing through the light areas, fine broken sepia pencil-and-ink outlines".

- **Reads by:** the washes, blooms, pooled edges and paper grain, all from the paint-over. The SVG sheet alone
  reads as clean vector.
- **Proof sheets:** `anime-sheet-watercolour.png` (the SVG sheet), `anime-sheet-watercolour-hipfix.png` (with the
  hip fix below) and `anime-sheet-watercolour-painted.png` (the paint-over).
- **Flaws and fixes:**
  - On the SVG sheet, skin showed between the shirt and the shorts. Giving the torso's base shape the shorts'
    colour fixed it.
  - The SVG sheet also had knee discs, which the paint-over removed.
  - The painting opened the mouth slightly.
  - Not rigged: waits for character `paintUrl`.

## Originality guard

Invent every character: no hair, uniform, palette or silhouette that points to a known series or studio. A
look is a set of drawing choices; it never copies a particular character's design.
