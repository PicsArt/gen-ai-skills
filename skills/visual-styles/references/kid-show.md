# Kid show

A cartoon made for young children: clean thin coloured lines, soft cel shading with one shadow tone, big
friendly eyes, round soft shapes and bright clear colours that stop short of neon. Nothing is sharp, dark or
scary; the acting is simple and the faces say everything. Every character and set is a generated picture, and
each character is cut into a puppet, so the cast keeps the shading and the eye shine a shape cannot draw. Who
the characters are comes from the story; this page holds only how they are drawn, cut and moved, and the
prompts that keep every picture of one cartoon in the same look. The sheets and the cutting are the ones
[pastel anime](pastel-anime.md) and [picture cut-out](picture-cutout.md) use.

## Contents

- [What it is not](#what-it-is-not)
- [Palette](#palette)
- [The medium](#the-medium)
- [Pictures](#pictures)
- [Characters](#characters)
- [Views](#views)
- [Part edits](#part-edits)
- [Creatures and props](#creatures-and-props)
- [Backgrounds](#backgrounds)
- [Motion habits](#motion-habits)
- [Camera](#camera)
- [Type](#type)
- [Sound](#sound)
- [Frame checklist](#frame-checklist-on-top-of-framemd)
- [Build with the tools](#build-with-the-tools)
- [Do / don't](#do--dont)
- [Originality guard](#originality-guard)
- [Proven on](#proven-on)

## What it is not

- Not [classic cartoon](classic-cartoon.md): that is thick dark ink outlines and flat fill, built from shapes.
  Here the line is thin and coloured, a darker shade of the fill it bounds, every fill carries one soft shadow
  tone, and the characters are pictures.
- Not [pastel anime](pastel-anime.md): that has anime faces (small nose, pointed chin, eyes with two highlights),
  a pastel palette and star and sparkle magic. Here faces are round cartoon faces (a button nose, a wide mouth
  that stretches with the feeling, eyes that are a large white with a big round pupil), the colours are clear
  and bright, and there is no magic: the acting carries the scene.
- Not [simple shapes](simple-shapes.md) or [flat explainer](flat-explainer.md): those draw people from primitives
  with no shading.

## Palette

Bright and clear, never neon, never pastel, never dark. The colours are the pictures' own: the prompts name them
in words, and a later picture takes them from the earlier ones it is given.

- **One clear main colour per character** on the top or the hair, a second on the trousers, shorts or skirt,
  white or a light neutral for the rest. Tomato red `#e9503f`, sky blue `#3d9be0`, grass green `#5cba4a`,
  sunflower yellow `#f7c23c` and violet `#8a63d2` sit well together.
- **Skin** from the story, shaded by one warmer, darker tone.
- **Sets:** a clean day sky `#8fd3f4`, white clouds, a mid green `#7cc96a`, warm walls `#f3e1c6`. Sets are a
  little softer than the cast, so the characters stand out.
- **The hero colour is a coral `#ff6f61`**, kept for the one thing the scene is about: a prop, a sign, a heart.

Night and interiors darken the whole picture with a grade, never by redrawing. A night stays friendly: a deep
blue, never black.

## The medium

- **Thin coloured lines.** Each outline is a darker shade of the colour it bounds (dark red round red, navy round
  blue, warm brown round skin), about 5 px wide on a 2K picture, even along its length. There is no black line.
- **Soft cel shading:** one shadow tone, a soft step darker, on the side away from the light: under the chin,
  under the hair, inside folds. No gradient, no rim light, no texture.
- **Faces:** big eyes with a large white and a round dark pupil, eyebrows that move, a round button nose, a wide
  mouth that changes shape with the feeling.
- **Round shapes:** a large head, soft rounded hands with four fingers, short rounded shoes. No sharp corner on a
  body, an outfit, a prop or a building.
- **Characters and sets are pictures.** The scene draws only a soft flat ellipse under each character's feet.
- **No cast shadow** in any picture.

## Pictures

The prompts below are the style. Once a cartoon picks it, every picture in that cartoon comes from them, so the
look holds from the first shot to the last.

- **Model:** Nano Banana 2 (`gemini-3.1-flash-image`), 2K. 9:16 for a character, a creature or a prop sheet;
  16:9 for a held background, 9:16 for a vertical film, 21:9 for a pan.
- **What stays the same** in every prompt: thin coloured outlines that are a darker shade of the colour they
  bound and never black, soft cel shading with one shadow tone, big friendly eyes with a round pupil, a round
  button nose, round soft shapes, bright clear colours, soft even light, no cast shadows.
- **Every new picture passes an earlier one of the same cartoon in `imageUrls`:** the first character's base for
  every later character, creature, prop and background; the picture being edited for every part edit. Only the
  very first base is made from words alone.
- Fill the `<slots>` from the story in plain words. A prompt never carries a hex code, a number or a name.

## Characters

**The first base** names the style in words. Draw it twice and keep the cleaner:

> Children's TV cartoon character for 2D cut-out animation, full body, <view and pose, from Views>. <who they
> are: a child, a grown-up or an animal person, age in words, hair, a friendly expression>. <outfit: each piece
> and its clear bright colour, simple shapes, no small print or logos>. Clean thin coloured outlines, each a
> darker shade of the colour it bounds, no black lines, soft cel shading with one shadow tone, big friendly eyes
> with a large white and a round dark pupil, a round button nose, round soft friendly shapes, four-fingered
> rounded hands, bright clear colours, soft even light, no shadows, nothing held in the hands, no text, plain
> pure white background.

**Every later character** passes the earlier bases in `imageUrls` and changes only who it is:

> A different character from the same cartoon as the reference picture, drawn in exactly the same style, same
> line weight, same shading, same head-to-body proportions and the same pose: <view and pose, from Views>.
> <who they are: hair, skin, a friendly expression>. <outfit and its colours>. <where long hair ends: "The hair
> ends above the shoulders and does not touch the arms.">. Soft even light, no shadows, nothing held in the
> hands, no text, plain pure white background.

- Silhouette and main colour tell the cast apart at a glance: vary height, head shape and hair, not only colour.
- Say where long hair ends, so it does not cover a part that moves.
- A scarf, a bag strap or a collar that would cover the sleeves is asked "small, not covering the sleeves".
- Grown-ups keep the same round style: "same style and line weight, a grown-up, taller, with a longer body and
  the same big round head shape".

## Views

A character that both talks to the viewer and walks is two models from two bases, used by shot. A character seen
one way only needs one.

| View | Pose words for the base | Used for |
|---|---|---|
| Front | `standing straight facing the camera, both arms straight and held clearly away from the sides, open hands, feet slightly apart` | talking to the viewer, a reaction, a jump, a wave |
| Side | `exact side view (profile), standing straight, legs straight, the near arm hanging straight down with the hand beside the thigh` | walking, meeting someone, talking to each other |

The side base is an edit of the front one, with the front base in `imageUrls`:

> Same character, same cartoon style and outfit, full body, exact side view (profile), standing straight, legs
> straight, the near arm hanging straight down with the hand beside the thigh. The whole body faces right: the
> face, the chest and the toes all point to the right side of the picture. Soft even light, no shadows, nothing
> held in the hands, no text, plain pure white background.

Without "the whole body faces right" the head can come back facing one way and the body the other.

## Part edits

Each edit passes the picture it changes in `imageUrls` and keeps everything else. The pose list, the sheets a
plot needs and the edits that fail are character-rigging's `references/picture-sheets.md`. The edge is a
coloured line, as in pastel anime, so the pieces are cut by hand as character-rigging's
`references/cut-any-edge.md` says, and a covered piece is the difference of two aligned pictures.

| Piece | Edit |
|---|---|
| arm with its sleeve (the base minus this) | `Same picture without the arm, without the hand and without the sleeve: the top is sleeveless with a small round armhole edge at the shoulder, and the side of the body and the clothes are drawn complete where the arm and hand were. Everything else unchanged.` |
| hair (the base minus this) | `Same picture without hair: a smooth round bald head in the same skin colour. Everything else unchanged.` |
| a tail of hair that sways (the base minus this) | `Same picture without the ponytail: the hair ends short at the back of the head. Everything else unchanged.` |
| legs under a skirt or a coat | `Same picture, with skin-coloured leggings instead of the skirt. Everything else unchanged.` |
| blink | `Same picture with eyes closed. Everything else unchanged.` |
| talk | `Same picture with mouth open, as if talking. Everything else unchanged.` and `Same picture with mouth in a small round o. Everything else unchanged.` |
| a laugh | `Same picture with mouth wide open, laughing, eyes happy. Everything else unchanged.` |
| surprise | `Same picture with a surprised face: eyebrows raised high, eyes wide open, mouth a small round open o. Everything else unchanged.` |
| worry | `Same picture with a worried face: eyebrows tilted up in the middle, mouth a small wavy line. Everything else unchanged.` |

- From a face edit only the head is taken; a whole head piece swaps over the base head for its span.
- The faces carry this style: plan three or four face edits per lead, not only a talk mouth.
- When one edit removes only the sleeve, chain a second edit on its result for the arm and the hand.
- A cuff and a shoe top are drawn lines to cut along; a knee and an elbow have no line, so those bend over a mesh.

## Creatures and props

A pet, a toy or a made-up creature is cut from a few pictures, its base with the first character's base in
`imageUrls`:

> A character sheet picture for animation, in exactly the same children's cartoon style, thin coloured lines and
> soft cel shading as the reference picture. One small friendly <animal or creature> alone on a plain pure white
> background: <body, colour, ears or tail held clearly apart from the body, big friendly eyes>. Three-quarter
> view, the face turned to the right. The whole creature is in the picture with space around it, no ground, no
> shadow, no other characters, no text.

- `Same picture without the tail: the back is drawn complete where the tail was.` gives the body; the tail is the
  base minus that picture. Ears and wings come the same way.
- `Same picture with eyes closed.` and `Same picture with its mouth open as if talking.` give the blink and the
  mouth.
- An ear, a tail or a wing grows out of the body: one mesh, its root pinned to the body.

A prop a character holds or uses is its own picture, with the first character's base in `imageUrls` for style
and scale:

> One <prop: what it is, its clear bright colour, simple round shape> for 2D cut-out animation, in exactly the
> same children's cartoon style, thin coloured lines and soft cel shading as the reference picture, at the size
> it would be beside the character in the reference. Alone on a plain pure white background, no hands, no
> shadow, no text.

## Backgrounds

One picture per place, with the first character's base in `imageUrls` for style and scale:

> A background painting for an animation, in exactly the same children's cartoon style, thin coloured lines and
> soft cel shading as the reference picture, slightly softer colours. <the place> in <the time of day>: a wide
> flat <path, floor or ground> running straight across the lower third of the picture, seen from the side at eye
> level, <what stands behind it, in simple round shapes>, <the sky or the far wall: a clean blue sky with two
> soft clouds, a warm sunset sky, a deep friendly blue night sky with a round moon>. Simple round shapes, little
> detail, nothing sharp or scary. No people, no characters, no animals, no text. Only the background. The
> character in the reference shows the style and the scale only: do not draw them.

- A background can come back inside a white border: crop to the painted area before placing it.
- Moving pieces of a set (clouds, a sun, leaves) are cut as [picture cut-out](picture-cutout.md#moving-the-set)
  says.

## Motion habits

- Smooth at the scene's rate; nothing steps on twos.
- Squash on landings, a small anticipation before a big move, a little overshoot on arrival, and holds of four to
  eight frames on a reaction so the face reads.
- Every character breathes and blinks; the head nods and tilts with every line.
- Faces swap on the beat of the line: a head piece changes on a frame, never cross-fades.
- Walks come from the rig's walk action with a little bounce. Two characters who meet stop a body width apart.
- One character talks at a time, and the others react to the speaker.
- Pace stays gentle: no fast cuts, no shake, no flash.

## Camera

Held for a talk, a gentle push in on a reaction, a slow pan along a wide set for a walk. The floor line stays
level.

## Type

A rounded bold sans in white with a thin outline in the speaker's main colour; a title in the hero coral with a
small pop-in. Words a young child can read: short and big.

## Sound

Light bouncy music with ukulele, glockenspiel, pizzicato and soft percussion, a soft cartoon accent (a boing, a
pop) on a big reaction, clear warm voices.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Every character has the same line weight, line colour rule and shadow tone.
2. No black line, no gradient and no cast shadow anywhere.
3. The hero coral is on the one thing the scene is about.
4. Every face reads its feeling at the frame size the film plays at.
5. Nothing sharp, dark or scary in the frame.
6. No gap, flap or sliver at a shoulder, elbow, hip or neck in the widest pose.
7. Every character stands on the floor line on its soles, with its shadow ellipse under it.

## Build with the tools

1. **Pictures:** fill the prompts above, quote every batch with `picsart_preflight`, then generate with
   `picsart_generate`, every later picture with the earlier ones in `imageUrls`.
2. **Characters:** cut by hand along the coloured line, each piece saved as a transparent picture; save each
   character with `picsart_asset_save`, every picture in `referenceImages`.
3. **Motion:** walks from the rig's walk action; face edits swap on the line's beats.
4. **Check:**
   - Look at every piece alone on a flat colour, then at the widest pose of every joint, zoomed in.
   - Run `picsart_scene_check_motion` on a walk.
   - Make a `picsart_scene_contact_sheet` across the film.
5. **Render:** `picsart_scene_export` at full quality.

## Do / don't

- **Do** reuse this page's prompts for every picture of the cartoon, filling only the slots.
- **Do** pass the earlier pictures in `imageUrls` for every new character, creature, prop and background.
- **Do** read each joint off the drawing it turns in.
- **Do** give every lead more faces than a talk mouth.
- **Don't** let a later picture drift to black lines, flat fill or pastel colours: regenerate it with the base in
  `imageUrls`.
- **Don't** tint the far arm or leg.
- **Don't** draw a prop or a character as a shape.

## Originality guard

Invent the cast and the world: names, faces, outfits, pets, homes. It must not resemble the characters,
families, animal heroes, vehicles, title cards or songs of a known children's show. A bright round cartoon with
coloured lines is a shared genre idea; a copy of one show's character design is not.

## Proven on

Two front puppets cut from five pictures (two bases, a blink and a surprised face from edits, one street
background), each a body and a head on a neck joint: one talks with nods and a lean, the other blinks, swaps to
a surprised face with an anticipation squash, a small hop and a landing squash, and settles back. The side view,
the arm cut and the walk are the [pastel anime](pastel-anime.md) route, proven there.
