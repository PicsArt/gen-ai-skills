# Watercolour anime

Anime characters and places painted in pale watercolour: transparent washes with soft wet edges, thin pencil-like
lines, paper showing through everything, and colour that fades to bare paper at the edges of the picture. It moves
slowly and holds long, and suits quiet slice-of-life stories. Every character and set is a generated picture, and
each character is cut into a puppet, because a wash, its pooled edge and the paper under it are things a shape
cannot draw. Who the characters are comes from the story; this page holds only how they are painted, cut and
moved. The sheets and the rig are the ones [picture cut-out](picture-cutout.md) uses.

## Contents

- [What it is not](#what-it-is-not)
- [Palette](#palette)
- [The medium](#the-medium)
- [Pictures: model and what stays the same](#pictures-model-and-what-stays-the-same)
- [Characters](#characters)
- [Views](#views)
- [Creatures and props](#creatures-and-props)
- [Sets](#sets)
- [One sheet of paper](#one-sheet-of-paper)
- [Cutting a soft edge](#cutting-a-soft-edge)
- [Motion habits](#motion-habits)
- [Drawn effects](#drawn-effects)
- [Camera](#camera)
- [Type](#type)
- [Sound](#sound)
- [Scene features used](#scene-features-used)
- [Frame checklist](#frame-checklist-on-top-of-framemd)
- [Build with the tools](#build-with-the-tools)
- [Do / don't](#do--dont)
- [Originality guard](#originality-guard)
- [Proven on](#proven-on)

## What it is not

- Not [pastel anime](pastel-anime.md): that one has clean tinted lines, soft cel shading, full evening sets and
  star magic. Here the line is a broken pencil line, the colour is a wash, the picture ends in bare paper, and
  nothing glows.
- Not [painted anime](painted-anime.md) or its watercolour look: those characters are built from SVG part sheets
  and walk through an opaque painted place. Here every character is cut from a painted picture.
- Not [cel anime](cel-anime.md): that is a sky scene built from shapes with one hard shade tone.
- Not a look of [picture cut-out](picture-cutout.md): its looks are cut along an edge each piece has (a dark
  line, a torn rim). A wash has no such edge, and the cut here is made for that.
- Not an Ink & Sketch style: [line-boil sketch](line-boil-sketch.md) is graphite line with no colour, and
  [woodblock print](woodblock-print.md) is flat printed colour with hard edges.
- Not a paper craft style: in [cut paper](cut-paper.md) paper is the pieces. Here paper is the ground the paint
  sits on.

## Palette

Pale and few. The colours are the pictures' own; name them in a prompt only to bring a later picture back in line
with the first.

| Role | Colour | Its one job |
|---|---|---|
| paper | `#fdfdfb` | the ground, the light in every wash and the edge of every picture; the pictures' own paper, never pure white |
| pencil | `#8a6f5c` | the line: a warm brown, thin, breaking in places; never black |
| sky wash | `#cfe3ea` | skies, water, far hills, cool clothes |
| leaf wash | `#cfe0bf` | grass, trees, banks |
| skin wash | `#f6dccb`, shade `#e9b9a6` | skin, with the cheek a touch pinker |
| earth wash | `#e2d2bd` | paths, wood, walls |
| blossom (hero) | `#f3c3cb` | **the one warm accent**: the petals or leaves that drift, and one small thing a character wears |

- A wash is never stronger than about half strength: the darkest thing in a picture is the pencil line and the
  hair.
- One accent per film. In autumn it is a leaf orange `#e9b48a`, and blossom is not used.
- Evening is the same picture under a warm grade, never a redrawn one.

## The medium

- **A wash, not a fill.** Colour is uneven inside a part, a little darker where the wash dried at its edge, and
  it stops short of the pencil line in places so the paper shows.
- **A pencil line, not an ink line.** Thin, warm brown, lighter and broken on the lit side. There is no black
  line and no cel shade tone.
- **The picture ends in paper.** A set is a vignette: its colour fades to bare paper before the frame's edge,
  with loose brush ends.
- **Paper is everywhere.** One sheet lies under the set, the characters and the effects alike
  ([One sheet of paper](#one-sheet-of-paper)).
- **No cast shadow.** A character stands on a pale wash mark painted in the scene, wider than the feet and soft.

## Pictures: model and what stays the same

Once a cartoon is in this style, every character, creature, prop and place in it comes from the prompts below,
reused as they are with only the `<slots>` changed. That keeps the look the same from the first picture to the
last.

- **Model:** Nano Banana 2 (`gemini-3.1-flash-image`) at 2K. 9:16 for a character, 1:1 for a creature or a
  prop, 16:9 for a set (9:16 for a vertical film, 21:9 for a slow pan). Quote each batch with `picsart_preflight`
  first.
- **Every new picture passes an earlier picture of the same cartoon as its style reference** (`imageUrls`): a
  later character passes the earlier bases, a creature, a prop or a set passes a character base, an edit passes
  the picture it changes. Only the first base has no reference.
- **Keep the same in every prompt:** the medium's words (transparent watercolour on white paper, pale washes with
  soft wet edges, pigment pooling at the edge of a wash, paper grain, thin soft brown pencil lines that break, no
  black line, no cel shading), soft even light, no shadow, and a plain white background. A shorter "watercolour
  style" comes back stronger in colour and with an ink line.
- **Name the anime face in words** (large glossy eyes, tiny nose, pointed hair locks, large head). Without
  them the watercolour words pull the face toward a picture-book child, not an anime one.
- **Write prompts in plain words:** colours by name ("pale blue", "warm brown"), never codes or numbers.

## Characters

The first character's base names the style in words. Draw it twice and keep the cleaner:

> Anime character painted by hand in transparent watercolour on white cold-pressed paper, <view and pose, from
> Views below>. <who they are: age, hair and where it ends, eyes, expression>, <outfit and its colours, in pale
> colours>. A clear Japanese anime face: large expressive eyes with big glossy irises and soft light highlights,
> long lashes, a tiny nose, a small mouth, a soft pointed chin. Hair in anime locks and pointed strands with side
> bangs. Anime proportions: a large head, a slim body, long legs. Pale washes
> with soft wet edges, pigment pooling a little darker at the edge of each wash, the paper grain showing through,
> thin soft brown pencil outlines that break in places, no black line, no cel shading. The washes stop a little
> short of the outline in places and the white paper shows. Pale gentle colours, the darkest thing is the hair.
> Soft even light. Full body, nothing in the hands, no shadows, plain pure white background, for 2D cut-out
> animation.

Every later character passes the earlier bases as `imageUrls` and changes only who it is:

> A different character from the same watercolour anime as the reference pictures, painted in exactly the same
> way: the same pale transparent washes with soft wet edges, the same paper grain, the same thin soft brown pencil
> line, the same anime face with large glossy eyes, the same proportions and the same pose. <who they are: age,
> hair and where it ends, eyes, expression>.
> <outfit and its colours, in pale colours>. No black line, no cel shading. Full body, nothing in the hands, no
> shadows, plain pure white background, for 2D cut-out animation.

- Hair shape and one pale signature colour tell the cast apart. Say where long hair ends ("ends above the
  shoulder and does not touch the arm"), so it does not cover a part that moves.
- Keep each outfit to two or three pale colours; one small thing a character wears may carry the accent.
- A cast that belongs together (a class, a family) can share one outfit design: add "the same outfit design in
  <colour>, same body proportions".

## Views

A character that talks to the viewer and walks is two models from two bases, used by shot. A quiet film often
needs only the side one.

| View | `<view and pose>` | Used for |
|---|---|---|
| Side | exact side view (profile), the whole body faces right, standing straight, legs straight, the near arm hanging straight down with the hand beside the thigh | walking, meeting someone, looking at the place |
| Front | standing straight facing the camera, both arms straight and held a little away from the sides, open hands, feet slightly apart | talking to the viewer, a wave |

The side base can also be an edit of the front one (pass the front base):

> Same character, same watercolour painting and outfit, full body, exact side view (profile). The whole body faces
> right: the face, the chest and the toes all point to the right side of the picture. Standing straight, the near
> arm hanging straight down with the hand beside the thigh. Everything else unchanged, the same paper.

The edits the cut needs pass the base and change one thing. Each ends with `Everything else unchanged, the same
paper.`:

| Piece | Edit |
|---|---|
| arm with its sleeve | `Same picture without the near arm, without the hand and without the sleeve: the <top or dress> is sleeveless with a small round armhole edge at the shoulder, and the side of the body and the clothes are painted complete where the arm and hand were, in the same watercolour washes and pencil line.` |
| blink | `Same picture with eyes closed.` |
| mouth | `Same picture with mouth open.` and `Same picture with mouth in a small o.` |
| hair | `Same picture without hair: the head is a complete smooth head painted in the same skin wash.` |
| front arms | `Same picture without arms, without hands and without sleeves: ...`, as the arm edit, for both sides |

Only the patch round the eyes or the mouth is taken from a face edit; the arm and the hair are the base minus the
edit ([Cutting a soft edge](#cutting-a-soft-edge)). The arm and blink edits came back right on the first try.

## Creatures and props

A small animal or creature is a base with a character's base as the style reference, then one edit per part that
moves:

> A character sheet picture for animation, painted in exactly the same watercolour way as the reference picture:
> pale transparent washes with soft wet edges, the paper grain showing, thin soft brown pencil lines that break,
> no black line, no cel shading. One small <creature: kind, body, ears or tail held clearly apart from the body,
> colours in pale washes> alone, side view facing right. The whole creature is in the picture with space around
> it. Soft even light, no ground, no shadows, no other characters, no text, plain pure white background.

- `Same picture without the tail: the body is painted complete where the tail was.` gives the body; the tail is
  the base minus it. Ears and wings come the same way. `Same picture with eyes closed.` gives the blink.
- A tail or an ear bends over a mesh that grows out of the body; it is not turned whole about its root.

A prop a character holds or a thing that stands in a set:

> One <prop: what it is, its shape, colours in pale washes>, painted in exactly the same watercolour way as the
> reference picture: pale transparent washes with soft wet edges, the paper grain showing, thin soft brown pencil
> lines. Side view, the whole object with space around it. Soft even light, no shadows, no hands, no text, plain
> pure white background.

Size it against the characters as the story says. A prop is cut with the same soft-edge cut as a character.

## Sets

One picture per place, with a character's base as the style and scale reference:

> A background painting for an animation, in exactly the same watercolour style as the reference picture: pale
> transparent washes with soft wet edges, the paper grain showing, thin soft brown pencil lines. <the place and
> the time of day>: a wide flat pale <path or floor> running straight across the lower third of the picture, seen
> from the side at eye level, <what stands behind it>, <the sky or the far wall>. The painting is a vignette: the
> colour fades out to bare white paper toward all four edges of the picture, with loose brush edges. The character
> in the reference shows the style and the scale only: do not draw them. Only the background: no people, no
> characters, no text.

- The floor is the palest wash in the set, so a character's soft edge sits on near-paper.
- A second place in the same cartoon passes the first set as well as the base, so the sky and the paper match.
- Evening or night is the same set under a warm or blue grade, never a new picture.
- Trees and grass sway over a mesh as [pastel anime's sets](pastel-anime.md#sets) do, at half the angle.

## One sheet of paper

Each generated picture has its own paper grain, and two grains side by side read as two sheets glued together.

1. Measure every picture's paper (the median of its border). With the prompts above the pictures came back within
   two levels of each other; shift any picture that is further off by the difference.
2. Build the whole shot (set, characters, effects) in one `scene` asset. Scale the set about 3% past the frame so
   its own paper fills the margins.
3. Put the paper on that asset's one `scene_ref`: `analog_film_finish` with `paper` about 0.35, `grain` about
   0.05, `dust` 0, `vignette` 0 and `tintAmount` 0. The fibre then lies inside every wash, every petal and the bare
   margins alike, and it holds still. At `paper` 0.5 the margins read as speckle.
4. The set prompt fades to paper by itself. Where a set does not, lay four soft paper-coloured bars over its edges
   inside the asset (a `rect` with `gaussian_blur` about 38 and `roughen_edges`), under the paper.

## Cutting a soft edge

The cut tool looks for a line that closes each piece. A wash has none: read as character-rigging's
`references/cut-any-edge.md` reads an edge, the rim is `change`, and the pencil line breaks. The pieces are cut
by hand as that page says, with these differences for the soft edge:

1. **Paper** is the median colour of the picture's border. A pixel's distance from paper is its largest channel
   difference.
2. **Figure:** every pixel further than about 10 from paper, closed, holes filled, the largest area.
3. **Core:** the figure shrunk by about 10 px is fully opaque, however pale its wash. A pale skin wash keyed by
   its distance from paper turns see-through and the set shows in the face.
4. **Edge band:** between the core and the figure grown by about 14 px, opacity rises with the distance from
   paper (from 4 to 28), and the paper is taken back out of the colour (`colour = (pixel - (1 - a) * paper) / a`).
   The piece then ends in its own wash fading out, with no white rim over a painted set.
5. **A piece in front** (the near arm) is the difference of the base and an edit without it, as in
   [pastel anime](pastel-anime.md#sheets-and-the-cut). Compare them blurred by about 3 px and keep a difference
   over about 22: an edit repaints the wash, and its grain differs everywhere.
6. **The difference misses what is the same colour.** A blue sleeve over a blue dress barely differs, and loose
   bits of the repainted dress do. So the arm is built in two parts: the sleeve is the convex hull of the bare
   armhole in the edit and the arm's upper part, and below the sleeve hem only the skin and the pencil line
   round it are kept (red over blue by more than 25, closed by about 14 px so the hand stays whole).
7. **A joint is an overlap, not a line.** The sleeve covers the armhole, so the arm turns about the armhole's
   middle with nothing showing behind it. Inside the body the arm's opacity is feathered about 3 px; along the
   figure's outside it takes the edge band's opacity. A hard cut through a wash shows as a line the painter
   never drew.
8. **A blink** is the closed-eye edit cropped round the difference, with about 30 px around it and a soft
   10 px feather, swapped in for about a sixth of a second.
9. **A filled hole** takes the wash round it plus its unevenness, never a flat colour.

Check every piece alone on a strong flat colour: a white rim or a see-through patch shows there and nowhere else.

## Motion habits

- **Slow, and long holds.** A move takes about twice as long as in another anime style, eases in and out, and is
  followed by a hold of a second or more in which only breathing, a blink and the air move.
- **Something always drifts:** petals or leaves across the frame, a branch, a hem, the ends of the hair. Hair and
  cloth follow a move late and settle slowly.
- **The wash edge boils lightly.** `roughen_edges` on each character piece (`border` about 5 and `scale` 30 at
  the piece's own size, `complexity` 2) with its `evolution` stepped six times a second moves the soft edge a
  pixel or two; the inside of the wash, the set and the paper hold still. Start the stepped value above 0
  (`return 100 + math.floor(time * 6) * 37`).
- **Breathing** is the whole character scaled about 0.6% taller from the feet over three seconds; an arm at
  rest swings about 2 degrees.
- Walks come from the rig's walk action at an unhurried pace, one pace per height. Nobody runs.
- One character talks at a time, mouths are small, and the listener only blinks.
- **Transitions:** a wash that spreads from one point until the frame is paper, then the next picture soaking in
  the same way; or a cut on a held frame. No wipe, no flash, no zoom cut.

## Drawn effects

The only shapes in the style. Each is one pale flat colour, blurred by a pixel or two, at about three quarters
opacity, inside the page asset so the paper lies over it:

- **Petals:** a pointed oval with rounded corners in the accent colour, 10 to 20 px long. Each falls on a slow
  S, turning half a turn in three seconds; five to ten in frame, never a shower. For a loop, lay them in a chain:
  every petal ends where the next one began and all look the same, so the loop has no jump.
- **Drifting leaves:** the same with a notched oval, for autumn.
- **Light spots:** paper-white discs (`#fffdf6`), 40 to 80 px, blurred by about 40% of their size, whose
  opacity breathes between a quarter and a half over three seconds: light through leaves. Over a pale sky
  they are almost unseen; put them over the tree and the bank.

## Camera

Held, or a pan so slow it is felt more than seen, or a slow push in on a face. The floor line stays level. The
camera never follows a petal.

## Type

A light rounded serif in the pencil brown at the foot of the frame, on bare paper, appearing as a wash soaks in.
A title is the same face, larger, with one petal beside it.

## Sound

A solo piano or a soft guitar with room to breathe, wind, birds, water, footsteps on gravel, a far train. Silence
is allowed.

## Scene features used

- `analog_film_finish` (`paper`, `grain`) on the page's `scene_ref`.
- `roughen_edges` with a stepped `evolution` (`return 100 + math.floor(time * 6) * 37`) for the wash-edge boil.
- `gaussian_blur` on the effect shapes and the edge bars.
- A `mesh` with a skin deformer for swaying trees and hair.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Paper shows inside the washes, at the picture's edges and under the effects, as one sheet.
2. No black line, no hard shade tone, no wash at full strength.
3. No white rim and no see-through patch on any piece; no straight seam across a wash at a joint.
4. The accent colour is only on the drifting petals or leaves and the one worn thing.
5. Every move is followed by a hold.

## Build with the tools

1. **Pictures:** quote every batch with `picsart_preflight`, then generate with `picsart_generate`:
   Nano Banana 2 (`gemini-3.1-flash-image`), 2K, 9:16 for a character, every later picture with the earlier
   bases as references.
2. **Characters:** cut by hand as [Cutting a soft edge](#cutting-a-soft-edge) says, each piece saved as a
   transparent picture; save each character with `picsart_asset_save`, every picture in `referenceImages`.
3. **Page:** set, characters and effects in one `scene` asset, the paper on its `scene_ref`.
4. **Check:**
   - Look at every piece alone on a strong flat colour, then at the widest pose of every joint, zoomed in.
   - Render two frames a second apart and compare: the paper must not move.
   - Make a `picsart_scene_contact_sheet` across the film.
5. **Render:** `picsart_scene_export` at full quality.

## Do / don't

- **Do** repeat the medium's sentence word for word in every prompt, and pass the earlier bases as references.
- **Do** put the paper on once, over the whole page.
- **Do** let a move end in a hold.
- **Don't** key a pale wash by its distance from paper: keep the core opaque.
- **Don't** cut a joint on a straight line through a wash.
- **Don't** put an effect shape outside the page asset: without the paper over it, it reads as vector.
- **Don't** add glow, sparkle, speed lines or a camera shake.

## Originality guard

Invent the cast and the places. They must not resemble the characters, the towns or the title lettering of a
known anime film or series, or a named illustrator's picture books. A quiet anime painted in watercolour is a
shared way of drawing; one studio's girl, house or hillside is not.

## Proven on

A 3 second 960x540 loop: one side-view character and one riverside set, four pictures in all (base, an edit
without the near arm, a closed-eye edit and the set), Nano Banana 2 at 2K. The character was cut
as above into a body, an arm with its sleeve and a blink patch. Seen alone on a dark colour, no piece had a white
rim or a see-through patch. She breathes, her arm swings, she blinks once, petals drift in two chains and the
paper lies over everything. The first base, asked without the anime face words, came back as a picture-book
child; with them (the base prompt above) it came back clearly anime, and the edits and the set came back right
on the first try. A front view, a walk and a talking mouth are not proven in this look.
