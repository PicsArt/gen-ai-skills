# Pastel anime

A bright, pastel anime look: characters drawn with thin tinted lines and soft cel shading, acting on painted
evening sets, with star and sparkle effects for the magic. Every character and set is a generated picture, and
each character is cut into a puppet, so the cast keeps the shading, the eye shine and the hair gradients a shape
cannot draw. Who the characters are comes from the story; this page holds only how they are drawn, cut and
moved. The pictures, the sheets and the cutting are the ones [picture cut-out](picture-cutout.md) uses.

## Contents

- [What it is not](#what-it-is-not)
- [Palette](#palette)
- [The medium](#the-medium)
- [Characters](#characters)
- [Views](#views)
- [Sheets and the cut](#sheets-and-the-cut)
- [Creatures](#creatures)
- [Sets](#sets)
- [Motion habits](#motion-habits)
- [Magic effects](#magic-effects)
- [Camera](#camera)
- [Type](#type)
- [Sound](#sound)
- [Frame checklist](#frame-checklist-on-top-of-framemd)
- [Build with the tools](#build-with-the-tools)
- [Do / don't](#do--dont)
- [Originality guard](#originality-guard)
- [Proven on](#proven-on)

## What it is not

- Not [cel anime](cel-anime.md): that is a sky scene built from shapes with one hard shade tone.
- Not [painted anime](painted-anime.md): its characters are built from SVG part sheets and walk through a
  painted place. Here every character is cut from pictures.
- Not a look of [picture cut-out](picture-cutout.md): that style is a storybook stage in profile. This one is an
  anime drawing with a front and a side model of a character and magic effects.

## Palette

Pastel, bright and clean. The colours are the pictures' own; name them in a prompt only to bring a later picture
back in line with the first.

- **One signature colour per character**, on the hair and the outfit's accents, with white or cream for the
  rest of the outfit. Pick the colours from the story and keep them a soft pastel: a blossom pink `#e8bcd0`,
  a calm blue `#7685a9` and a warm yellow `#f8dfb6` with an amber shade `#cda46f` sit well together.
- **A white creature** is cream `#fef8ed` with a warm shade `#fcf2ea`, never pure white.
- **Evening set:** a pink sky `#fcd0cb` and `#dba4b5` turning violet `#998ebb` and `#7b7fbd`, blossom `#f1bfb5`,
  path and trunks `#8a6866`.
- **The hero colour is star gold `#fff6b8`**, kept for the magic: a falling star, a sparkle, a flash. It is on
  no outfit and no set.

Night and interiors darken the whole picture with a grade, never by redrawing.

## The medium

- **Thin tinted lines.** Each outline is a darker shade of the colour it bounds (rose round pink, navy round
  blue, brown round skin and yellow), about 6 px wide on a 2K picture. There is no black line.
- **Soft cel shading:** one soft shade tone under hair, folds and frills, a gradient in long hair, big eyes with
  two highlights.
- **Characters, creatures and sets are pictures.** Shapes draw only the magic ([Magic effects](#magic-effects)).
- **No cast shadow** in any picture. A character stands on a soft flat ellipse drawn in the scene.

## Characters

The first character's base names the style in words. Draw it twice and keep the cleaner:

> Anime character for 2D cut-out animation, full body, <view and pose, below>. <who they are: age, hair, eyes,
> expression>, <outfit and its colours>. Clean cel shading, thin clean outlines, soft even light, no shadows,
> nothing held in the hands, plain pure white background.

Every later character passes the earlier bases as references and changes only who it is:

> A different character from the same anime as the reference pictures, drawn in exactly the same style, same
> line weight, same shading and the same pose. <who they are in a few words>: <hair, eyes, expression>.
> <outfit and its colours>. Soft even light, no shadows, no text, plain pure white background.

- Hair shape and signature colour tell the cast apart at a glance.
- A group that belongs together (a team, a class, a family) can share one outfit design in different colours:
  add "the same outfit design but in <colour>" and "same body proportions".
- Say where long hair ends ("ends above the shoulder and does not touch the arm or sleeve"), so it does not
  cover a part that moves.
- A bow, a scarf or a collar that covers the sleeves is asked "small, on the chest, not covering the sleeves".

## Views

A character that both talks to the viewer and walks is two models from two bases, used by shot. A character seen
one way only needs one.

| View | Base pose | Used for |
|---|---|---|
| Front | standing straight facing the camera, both arms straight and held clearly away from the sides, open hands, feet slightly apart | talking to the viewer, a line-up, a jump, a wave |
| Side | exact side view (profile), standing straight, the near arm hanging straight down | walking, meeting someone, talking to each other |

The side base is an edit of the front one: `Same character, same anime style and outfit, full body, exact side
view (profile). The whole body faces right: the face, the chest and the toes all point to the right side of the
picture. <what is on the chest> is at the right, <what is on the back> is at the left. ...`
Without those words the head can come back facing one way and the body the other.

## Sheets and the cut

The pose list, the sheets a plot needs and the edits that fail are character-rigging's
`references/picture-sheets.md`. This style's edge is a line of another colour, so the cut tool returns one area:
the pieces are cut by hand as character-rigging's `references/cut-any-edge.md` says, and a covered piece is the
difference of two aligned pictures.

| Piece | Comes from |
|---|---|
| arm with its sleeve | the base minus `Same picture without the arm, without the hand and without the sleeve: the top is sleeveless with a small round armhole edge at the shoulder, and the side of the body and the clothes are drawn complete where the arm and hand were.` |
| hair | the base minus `Same picture without hair.` A long tail that sways is its own piece: `Same picture without the long ponytail: the hair ends short at the back of the head, and the back is drawn complete where the ponytail was.` |
| legs under a skirt or a coat | `Same picture, with skin-coloured leggings instead of the skirt.` |
| blink and mouths | `Same picture with eyes closed.`, `Same picture with mouth open.`, `Same picture with mouth in a small o.`: only the patch round the eyes or the mouth is taken |
| a wave in profile | `Same picture, the far arm is raised and waves to someone in front, open hand up in front of the face, the near arm stays down, everything else unchanged.` |

- When one edit removes only the sleeve, chain a second edit on its result for the arm and the hand.
- The drawn wave shows the elbow in front of the body, so its elbow joint is read off that drawing, not guessed
  inside the body (character-rigging's `references/cut-any-edge.md` has the joint and alignment checks).
- A boot top, a glove cuff and a sleeve band are drawn lines to cut along; a knee and an elbow have no line, so
  those bend over a mesh.

## Creatures

A small animal or made-up creature is cut from a few pictures: its base with a character's base as the style
reference, then one edit per part that moves.

> A character sheet picture for animation, in exactly the same anime style, clean thin lines and soft cel
> colouring as the reference picture. One small cute creature alone on a plain pure white background: <body,
> ears or tail held clearly apart from the body, eyes, cheeks, markings>. Three-quarter view, the face turned to
> the right. The whole creature is in the picture with space around it, no ground, no shadow, no other
> characters, no text.

- `... but without the two long ears: the head is a complete smooth round head.` gives the body; the ears are the
  base minus that picture. A tail or a wing comes the same way.
- `... with both eyes closed in a happy smile` and `... with its small mouth open as if talking` give the blink
  and the mouth.
- **An ear, a tail or a wing grows out of the body.** It is one mesh: its root follows the body and the rest
  follows its own joint, blended along its length. A part turned whole about its root lifts off the body and
  shows the background.
- A round creature without drawn legs floats a little above the ground, squashes on landing and hops; it does
  not walk.
- Size it against the characters as the story says, and keep a small one beside or behind a character, not in
  front of it.

## Sets

One picture per place, with a character's base as the style and scale reference:

> A background painting for an animation, in exactly the same anime style, clean thin lines and soft cel
> colouring as the reference picture. <the place and the time of day>: a wide flat path or floor running
> straight across the lower third of the picture, seen from the side at eye level, <what stands behind it>,
> <the sky or the far wall>. No people, no characters, no animals, no text. Only the background.

16:9 for a held shot, 9:16 for a vertical film, 21:9 for a pan. Moving pieces of a set (clouds, a sun, grass) are
cut as [picture cut-out](picture-cutout.md#moving-the-set) says. Trees sway without cutting: the whole picture is
one mesh, each tree's crown follows a joint at its trunk foot by how much leaf or blossom colour a point has and
how high above the foot it is, and each tree turns about half a degree every 2.6 s. Posts, benches and buildings
stay still.

## Motion habits

- Smooth at the scene's rate; nothing steps on twos.
- Every character breathes and blinks. Long hair, a ponytail and loose ribbons follow a move a beat late and
  settle.
- Walks come from the rig's walk action at one pace per height. Two characters who meet stop a body width apart.
- A wave moves the forearm from the elbow; the upper arm holds.
- One character talks at a time, and the others look at the speaker.
- A jump crouches first, and skirts and hair rise late and fall late.

## Magic effects

The only shapes in the style, all in star gold and white:

- **A falling star:** a five-point star with a tapering trail, crossing the sky on a slight curve in under a
  second, then a white flash of two or three frames and a ring that widens and fades where it lands.
- **Sparkles:** four-point stars that scale up, turn a little and fade, a few at a time.
- **A shine:** rays behind the subject that scale out from nothing. Draw them opaque and let their size carry the
  shine; a pale yellow fill at low opacity over a white body reads as grey.

## Camera

Held for a meeting or a talk, a slow pan along a wide set for a walk, a slow push in on the magic. The floor line
stays level.

## Type

A rounded bold sans in white with a thin outline in the speaker's signature colour, at the foot of the frame;
a title in star gold with a few sparkles.

## Sound

Bright pop with bells and a soft synth, a chime on every sparkle, a rising shimmer under a falling star, light
steps.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Every character has the same line weight and shading.
2. No gap, flap or sliver at a shoulder, elbow, hip, ear or tail root in the widest pose.
3. Star gold is only on the magic.
4. Every character stands on the floor line on its soles, with its shadow ellipse under it.
5. No black line and no cast shadow anywhere.

## Build with the tools

1. **Pictures:** quote every batch with `picsart_preflight`, then generate with `picsart_generate`:
   Nano Banana 2 (`gemini-3.1-flash-image`), 2K, 9:16 for a character, every later picture with the earlier
   bases as references.
2. **Characters:** cut by hand along the tinted line, each piece saved as a transparent picture; save each
   character with `picsart_asset_save`, every picture in `referenceImages`.
3. **Motion:** walks from the rig's walk action; a drawn pose swaps in mid-move.
4. **Check:**
   - Look at every piece alone on a flat colour, then at the widest pose of every joint, zoomed in.
   - Run `picsart_scene_check_motion` on a walk.
   - Make a `picsart_scene_contact_sheet` across the film.
5. **Render:** `picsart_scene_export` at full quality.

## Do / don't

- **Do** pass the earlier bases as references for every new character, creature and set.
- **Do** read each joint off the drawing it turns in.
- **Do** pin the root of anything that grows out of a body: an ear, a tail, a lock of hair.
- **Don't** replace a drawn arm with a plain tube to close a gap: move the joint to where the drawing bends.
- **Don't** tint the far arm or leg.
- **Don't** draw a prop or a character as a shape: shapes are for the magic only.

## Originality guard

Invent the cast: names, hair, outfits, creatures and their marks. It must not resemble the characters, outfits,
mascots, wands, brooches or transformation poses of a known anime series, or a named series' title lettering.
A pastel anime drawing with sparkle magic is a shared genre idea; a copy of one series' costume or hairstyle is
not.

## Proven on

Three characters, each as a front and a side model with idle, blink, talk, wave, walk and jump, and a small
creature with ear flap, blink, talk, hop, land and shine. Two short scenes on an evening park set with swaying
trees: two characters walk in, meet, wave and talk, then a star falls and lands between them.
