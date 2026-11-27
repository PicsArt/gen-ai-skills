# Chibi anime

A small, round, comic anime look: characters two to three heads tall with a huge head, big eyes and stubby
limbs, drawn with one bold rounded line, acting on a flat colour card. They squash, stretch, pop in and hold,
and their feelings are drawn beside them as marks: a sweat drop, a sparkle, an anger mark. It suits comedy,
reactions and short gags. Every character is a generated picture cut into a puppet with very few joints; the
card and the marks are shapes. Who the characters are comes from the story; this page holds only how they are
drawn, cut and moved.

## Contents

- [What it is not](#what-it-is-not)
- [Proportions](#proportions)
- [Palette](#palette)
- [The medium](#the-medium)
- [Pictures](#pictures)
- [Characters](#characters)
- [Views](#views)
- [Part edits](#part-edits)
- [Faces](#faces)
- [Creatures and props](#creatures-and-props)
- [Backgrounds](#backgrounds)
- [The cut and the joints](#the-cut-and-the-joints)
- [The card](#the-card)
- [Motion habits](#motion-habits)
- [Reaction marks](#reaction-marks)
- [Camera](#camera)
- [Type](#type)
- [Sound](#sound)
- [Frame checklist](#frame-checklist-on-top-of-framemd)
- [Build with the tools](#build-with-the-tools)
- [Do / don't](#do--dont)
- [Originality guard](#originality-guard)
- [Proven on](#proven-on)

## What it is not

- Not [cel anime](cel-anime.md) or [painted anime](painted-anime.md): those are full-height figures in a place
  with light and weather. Here most shots stand on a colour card, and a place is flat and simple.
- Not a small version of a full-height anime cast: the proportions, the line, the joints and the timing are all
  different (the table below), so a full-height character is redrawn as a chibi, never scaled down.
- Not [picture cut-out](picture-cutout.md): that is a storybook stage in profile with walking puppets. A chibi
  faces the viewer, hops and reacts.

| | Full-height anime cut from pictures | Chibi anime |
|---|---|---|
| Height | six to seven heads | two to three heads |
| Line | thin, tinted by the colour it bounds | bold, one dark colour, even width, round corners |
| Shading | soft tone, hair gradients | flat colour, at most one small shade tone |
| Joints | shoulders, elbows, hips, knees, hair, skirt | body, head, two arms |
| Pictures per character | six or seven | one, plus one per face |
| Walk | a walk cycle | a hop-along |
| Timing | smooth, eased, late follow-through | snaps and holds, squash and stretch |
| Feeling | acted with the body | swapped on the face and drawn as a mark |
| Set | a painted place | a flat colour card, or a flat simple place |

## Proportions

- **Two to three heads tall**, 2.5 by default. The head is as wide as the whole body with its arms, or wider.
- **Eyes** sit below the middle of the head and each is about a quarter of the head's width. A tiny mouth, no
  nose, a blush oval on each cheek.
- **Arms and legs are stubs** with no elbow and no knee: an arm is about as long as the head is wide divided by
  three, with a mitten hand. Feet are small ovals.
- **Hair is one big simple shape** with a few large locks; no thin strands.
- A prop is drawn chibi too: short, fat and rounded, about the size of the head or smaller.

## Palette

Bright candy colours on a pale card.

- **Line:** one dark warm brown `#4a2f2a` for every character and prop. No black, no tinted line.
- **Skin** a warm cream `#ffe6d1`, **blush** `#ffb3b8`.
- **One main colour per character** for the hair and one for the outfit, both clear and light: mint `#a8e6cf`,
  coral `#ff8a7a`, butter `#ffe08a`, sky `#9fd3ff`, lilac `#c9b6f2`. White or cream fills the rest.
- **Calm cards:** mint `#c9f2e3`, peach `#ffe0cc`, lilac `#e4d8fa`. The pattern on a card is a lighter tint of
  the card's own colour, drawn opaque (`#eafbf4` on mint); white at low opacity renders grey.
- **Mood cards:** a shock card is deep indigo `#3b3470` with lines in `#655e9c`, a joy card warm butter `#ffe394`
  with shapes in `#fff6d6`, an anger card warm red `#ff7a66`.
- **The hero colour is mark red `#ff4d5a`**, kept for the anger mark, a heart and one word of a title. It is on
  no outfit and no calm card.
- The other marks have fixed colours: sweat drop `#8fd0ff` with a white highlight, sparkle `#ffd84a`, shock
  wedges white, a gloom cloud `#4a2f2a`.

## The medium

- **A bold rounded line** of even width, about 14 px on a 2K picture, closed round every form.
- **Flat colour.** One small shade tone under the hair and the chin at most; no gradients, no texture.
- **Characters and props are pictures.** The card, the marks, the shadow and the type are shapes.
- **No cast shadow** in a picture. A character stands on a flat ellipse drawn in the scene, which shrinks when
  the character leaves the ground.

## Pictures

Every character, creature, prop and place in a chibi cartoon is a generated picture, made with these prompts and
only their `<slots>` changed. Once the first character exists, **every new picture passes an earlier picture of
the same cartoon as its style reference** (`imageUrls`), so the line, the colour and the proportions stay the
same from the first picture to the last.

- **Model:** Nano Banana 2 (`gemini-3.1-flash-image`), 2K. Its edits keep the pose and the size, so a face or a
  part edit lines up with its base without moving it.
- **Shape:** 9:16 for a character, creature or prop; 16:9 for a place (9:16 in a vertical film, 21:9 for a pan).
- **Keep the same in every prompt:** the words for the line ("bold rounded dark-brown outlines of even
  thickness"), the colour ("flat colours with one soft shade tone"), the light ("soft even light") and the
  proportions ("about two and a half heads tall"). Change only the slots.
- **No numbers and no colour codes in a prompt:** name colours in words ("mint green", "coral").
- An edit takes the base as its only `imageUrls` entry and starts with "Same picture"; a new character, creature,
  prop or place takes one or two earlier bases.

## Characters

The first character's base names the whole style in words:

> Chibi anime character for 2D cut-out animation, full body, about two and a half heads tall: a very large round
> head, a tiny body, short stubby arms and legs with no drawn elbows or knees, small mitten hands. <view and
> pose>. <who they are: age, hair, eyes, expression>, <outfit and its colours>. Bold rounded dark-brown outlines
> of even thickness, flat colours with one soft shade tone, soft even light, very big round eyes with two
> highlights, small blush ovals on the cheeks, no nose. Full body, nothing held in the hands, no shadows, no
> text, plain pure white background.

Every later character passes one or two earlier bases as references and changes only who it is:

> A different character from the same chibi anime as the reference pictures, drawn in exactly the same style:
> same proportions, same bold rounded dark-brown line, same flat colours and the same pose. <who they are: age,
> hair, eyes, expression>. <outfit and its colours>. For 2D cut-out animation. Full body, nothing held in the
> hands, no shadows, no text, plain pure white background.

- `<who they are>` names the hair shape and colour first: hair shape and the two main colours tell the cast apart
  at a glance. Say the hair "ends above the shoulders and does not touch the arms", so it does not cover an arm.
- `<outfit and its colours>` is one simple garment and shoes in one or two light colours, for example "a simple
  cream hoodie dress with coral accents, coral shoes".
- A chibi of an existing character passes that character's picture as the reference and says "the same character
  redrawn as a chibi: same hair shape and colour, same outfit colours, everything else simpler".
- The base that built the proof had the slots "Standing straight facing the camera, both short arms held clearly
  away from the sides, feet slightly apart", "A cheerful girl with a short mint-green bob that ends above the
  shoulders, a tiny closed smile" and the outfit above. It and both face edits lined up at the first try.

## Views

| View | `<view and pose>` slot | Used for |
|---|---|---|
| Front | `Standing straight facing the camera, both short arms held clearly away from the sides, feet slightly apart` | talking to the viewer, a reaction, a hop |
| Three-quarter | made as an edit of the front base, below | two characters facing each other (mirror one) |

> Same character, same chibi style, same outfit and the same size, full body, turned three-quarters to the right:
> the face, the chest and the shoe toes all point to the right side of the picture, both short arms held clearly
> away from the body. No shadows, plain pure white background.

A chibi is seen front or three-quarter; it does not walk in profile, it hops.

## Part edits

The head, the body and the arms are cut from the base itself, so a chibi needs few part edits:

| Piece | Edit of the base |
|---|---|
| a bouncing lock, ponytail, ear or tail | `Same picture without the <lock or ponytail>: the hair ends short there and the head is drawn complete where it was. Everything else unchanged.` The piece is the base minus this picture. |
| a body hidden under long hair | `Same picture with the hair short above the shoulders: the shoulders and the top of the outfit are drawn complete. Everything else unchanged.` |
| a held prop | `Same picture, holding <prop> in both hands in front of the body. Everything else unchanged.` Swapped in as a drawn pose. |

## Faces

A feeling is a face swap, not acting. Each face is one edit of the base; only the patches round the eyes and the
mouth are taken, so one edit can give an eye patch and a mouth patch at once.

| Face | Edit | Gives |
|---|---|---|
| happy | `Same picture with both eyes closed in happy upward arcs and the mouth wide open in a big laugh. Everything else unchanged.` | the blink and joy eyes, the talking and laughing mouth |
| shock | `Same picture with a shocked face: the eyes are plain white circles with a tiny dot pupil, and the mouth is a small wavy line. Everything else unchanged.` | dot eyes, the wavy mouth |
| cross | `Same picture with an angry pouting face: eyebrows pulled down, eyes half shut, cheeks puffed. Everything else unchanged.` | cross eyes, the pout |

Order only the faces the plot uses. A blink is the happy eyes held for two or three frames; talk is the laughing
mouth swapped on and off. The words "Everything else unchanged" keep the edit aligned with the base.

## Creatures and props

One prompt each, with a character base as the style and scale reference:

> A <creature or prop> for 2D cut-out animation, in exactly the same chibi anime style as the reference picture:
> short, round and simple, bold rounded dark-brown outlines of even thickness, flat colours with one soft shade
> tone, soft even light. <its shape, colours and face if it has one>, <ears, tail or wings held clearly apart from
> the body>. About the size of the character's head. Alone, whole, no shadows, no text, plain pure white
> background.

- A prop that will be cut cleanly can come transparent instead: GPT Image Flare with a transparent background, the
  same prompt and the same reference.
- A creature's blink and mouth are face edits as in [Faces](#faces).

## Backgrounds

Most shots stand on a colour card ([The card](#the-card)). When the story needs a place, it is one picture with a
character base as the style and scale reference:

> A background for a chibi anime cartoon, in exactly the same style as the reference picture: bold rounded
> dark-brown outlines of even thickness, flat colours with one soft shade tone, soft even light, simple rounded
> shapes and few details. <the place>, at <the time of day>: a wide flat floor running straight across the lower
> third of the picture, seen from the front at eye level, <what stands behind it, drawn small and chibi>, <the
> sky or the far wall>. Plenty of empty floor in the middle. No people, no characters, no animals, no text.

- 16:9 for a held shot, 9:16 for a vertical film, 21:9 for a pan.
- Keep the place pale and quiet so the characters and the marks stay the strongest colour.

## The cut and the joints

A chibi has four joints. That is the whole rig.

| Piece | Cut | Joint |
|---|---|---|
| head with its hair | along the head's own outline, the chin line included | the chin: tilts up to 10 degrees and scales for a squash |
| body with both legs | everything below the chin line; the legs never bend | the feet on the ground: squash, stretch, lean |
| each arm | stays part of the body picture, bent over a mesh | the shoulder: swings up to about 35 degrees, no elbow |
| eyes and mouth | patches from the face edits, on the head | swapped, never faded |

- The bold line is a line of one colour, so the pieces are cut by hand along it as character-rigging's
  `references/cut-any-edge.md` says.
- The head hides the top of the body. Fill the body a few pixels up under the chin with its own colour so a
  tilt shows no gap.
- An arm is too short to hinge. It bends over a mesh from the shoulder, its root following the body. Weight only
  what lies past the shoulder sideways, blended over the first half of the arm, and the whole hand fully: a hem
  or a hand that is half on the arm tears. Past about 35 degrees the drawn sleeve smears; for a bigger move order
  a drawn pose.
- A long lock, a tail, ears or a ribbon that should bounce is its own mesh with its root pinned to the piece it
  grows from.

## The card

Most shots draw no place. The set is a flat colour card with one quiet pattern in a lighter tint, filling the frame:

- **Calm:** dots on a slanted grid, drifting slowly along the slant.
- **Shock or speed:** straight lines running to the subject from the frame's edge, on the mood colour.
- **Joy:** small four-point sparkles and dots, scaling in and out of step.
- **Gloom:** the card darkens from the top with a grade and a few vertical lines hang over the head.

The card changes with the feeling as a cut: the colour and pattern swap on the same frame as the face. A place,
when the story needs one, is one or two chibi props on the card (a desk, a door) or a flat chibi
[background](#backgrounds), never a painted one.

## Motion habits

- **Pose to pose.** A move takes 3 to 6 frames and then holds; nothing drifts between poses. Easing is a sharp
  ease-out with an overshoot, not an ease-in-out.
- **Squash and stretch on everything.** A landing squashes to about 80% height and 115% width for two frames,
  stretches past rest and settles; the head squashes a frame after the body.
- **Pop-in.** A character, a prop or a mark enters by scaling from nothing to 115% in 3 or 4 frames and settling
  to 100%. It leaves by shrinking, or the shot cuts.
- **Idle is a bounce**, not a breath: the body dips and rises about 2% twice a second, the head a frame late.
- **A hop-along instead of a walk:** small hops across the card, squashing on each landing, the arms flapping
  up on the way up. The legs never step.
- **Faces swap on a hold's first frame**, with a small squash of the head on the same frame.
- **A shake** for anger or cold: 2 or 3 px side to side every frame while the pose holds.
- A blink every two or three seconds, two frames long.

## Reaction marks

Shapes with the same bold brown line as the characters, placed beside the head and never over the face. Each
pops in, holds while the feeling holds and pops out.

- **Sweat drop:** a teardrop in sweat blue with a white highlight, by the temple; it pops in and slides down a
  little, slowly.
- **Sparkle:** a four-point star in sparkle yellow, two or three of them of different sizes, turning a little
  and scaling in and out of step.
- **Anger mark:** four short curved strokes round a small empty cross, in mark red, on the upper side of the
  head; it pulses in size.
- **Shock:** three short white wedges fanning away from each upper side of the head, popped in on the shock
  card's first frame and gone half a second later.
- **Heart, question mark, music note, gloom cloud** follow the same rules: one flat colour, the brown line,
  pop in, hold, pop out.

At most two kinds of mark at once.

## Camera

Held and flat on the character. A reaction is a cut to a closer shot or a snap zoom of 3 or 4 frames, never a
slow move. The frame can shake two frames on an impact.

## Type

A rounded heavy sans in white with the brown outline; a shouted word is bigger, tilted and pops in like a mark.
One word of a title can take mark red.

## Sound

Light, bouncy music with a toy or ukulele feel. Every pop-in has a pop, every landing a soft boing or tap, a
sweat drop a slide whistle, a sparkle a chime, a shock a sting. Voices are short.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Every character is two to three heads tall with the same bold line.
2. No gap under the chin or at a shoulder in the widest tilt and swing.
3. Mark red is only on a mark, a heart or one title word.
4. A mark sits beside the head, not over the face, and no more than two kinds show at once.
5. The card is flat: no painted place, no gradient, no cast shadow.
6. A held pose is still, apart from the idle bounce and the card's pattern.

## Build with the tools

1. **Pictures:** quote every batch with `picsart_preflight`, then generate with `picsart_generate` as
   [Pictures](#pictures) says: one base and one edit per face for each character, every new picture with an
   earlier one of the same cartoon in `imageUrls`.
2. **Characters:** cut the head, the body and the face patches by hand along the bold line, each saved as a
   transparent picture; save each character with `picsart_asset_save`, every picture in `referenceImages`.
3. **Card and marks:** shape layers in the scene, the marks parented to the character's head so they follow it.
4. **Motion:** keys with step or sharp ease-out easing; swap faces and cards on the same frame.
5. **Check:**
   - Look at each piece alone on a flat colour, then at the widest tilt, swing and squash, zoomed in.
   - Make a `picsart_scene_contact_sheet` across the film and read the holds: a pose that drifts is wrong.
6. **Render:** `picsart_scene_export` at full quality.

## Do / don't

- **Do** redraw a character as a chibi; a full-height drawing scaled down is not one.
- **Do** show a feeling three ways on one frame: the face, the mark and the card.
- **Do** hold a pose long enough to read, at least 8 frames.
- **Don't** add elbows, knees or a walk cycle.
- **Don't** ease slowly in and out or let hair trail softly: this style snaps.
- **Don't** paint a detailed background or shade with gradients.
- **Don't** cover the face with a mark or a caption.

## Originality guard

Invent the cast: names, hair, outfits and props. It must not resemble the characters, mascots or outfits of a
known anime, game or sticker set, or a named series' title lettering. Small round bodies, big eyes and drawn
reaction marks are a shared drawing convention; a copy of one series' character is not.

## Proven on

One character drawn from three pictures (a base and two face edits, all aligned at the first try): head,
body, two arm bones and laughing, blinking and shocked faces. A three-beat clip on a calm, a shock and a joy
card: an idle bounce with a blink, a shock pop with stretch, shake, raised arms, shock wedges and a sweat drop,
then a laughing hop with squash on take-off and landing and sparkles.
