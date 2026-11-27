# Action anime

A loud, fast anime look: bold dark outlines, hard two-tone shading and saturated colour, cut from one strong pose
to the next. A move is a wind-up, two or three frames of travel and a long held pose, and the effects round it
(speed lines, an impact frame, a burst, dust, a shaking camera) carry the force. Every pose of a character is a
generated picture; the effects and the grounds behind an action are shapes. Who the characters are comes from the
story; this page holds only how they are drawn, cut and moved.

## Contents

- [What it is not](#what-it-is-not)
- [Palette](#palette)
- [The medium](#the-medium)
- [Why the cast is poses](#why-the-cast-is-poses)
- [Pictures](#pictures)
- [Characters](#characters)
- [Views](#views)
- [Sheets and the cut](#sheets-and-the-cut)
- [Creatures](#creatures)
- [Sets](#sets)
- [Effects drawn as shapes](#effects-drawn-as-shapes)
- [Motion rules](#motion-rules)
- [Camera](#camera)
- [Shots](#shots)
- [Type](#type)
- [Sound](#sound)
- [Frame checklist](#frame-checklist-on-top-of-framemd)
- [Build with the tools](#build-with-the-tools)
- [Do / don't](#do--dont)
- [Originality guard](#originality-guard)
- [Proven on](#proven-on)

## What it is not

- Not a soft anime of thin tinted lines, gentle shading and puppets that move smoothly. Here the line is near
  black, the shade is hard and nothing moves smoothly.
- Not [cel anime](cel-anime.md): that is a calm sky scene built from shapes. Here the characters are pictures and
  the shapes are the effects.
- Not [manga panels](manga-panels.md): that is a black-and-white page of panels. This is one full-colour frame
  that cuts.

## Palette

Few colours, all saturated, on a near-black line.

- **Ink `#14121c`** for every outline, the deepest shadows and the dash ground. It is a blue-black, never grey.
- **Grounds:** one flat colour per beat, and the colour changes on the hit: a cold blue `#2238c8` with lines in
  `#101a6e` while waiting, a hot red `#e3182d` with lines in `#8c0b22` after the hit. White `#ffffff` for the
  impact frame and for a few of the lines.
- **One strong colour per character**, on the largest piece of the outfit, with white, ink and skin for the rest.
  Keep it away from the ground behind it: a red jacket is staged on blue, a blue one on red or yellow-free white.
- **Shade** is the same colour about 35% darker with a hard edge. No gradient, no soft shadow, no glow.
- **The hero colour is flash yellow `#ffd400`**, kept for the hit: the burst, a spark, a streak or two in the
  dash. It is on no outfit, no hair and no ground.
- **Dust** is a warm white `#f4ecdf` with an ink outline.

## The medium

- **Bold dark outlines.** About 10 px on a 2K picture, heavier on the outside of the figure than inside it, with
  pointed ends. The effect shapes carry the same ink line, 7 to 10 px at 1920 wide.
- **Hard two-tone shading.** Every colour has one light and one shade, split by a sharp edge that follows the
  form. Light comes from one side, and a thin white rim on the other side lifts the figure off the ground.
- **Eyes and hair** take one hard white highlight each.
- **No soft thing anywhere:** no blur, no gradient, no fade. A thing is there or it is cut.

## Why the cast is poses

A character is a set of drawn key poses, each one a whole picture, swapped on a cut.

- An action pose is foreshortened: a fist comes at the camera, a leg trails away, the body twists. A puppet turns
  flat pieces on joints and cannot draw that, and a shape figure cannot carry the hard shade that changes with
  every pose.
- The style does not in-between. A move is three or four drawings, so a rig that blends smoothly from one pose to
  the next works against it.
- So the cost is one picture per key pose, and a shot is planned by its poses: say which ones the story needs
  before generating any.

A calm scene (two characters talking, a walk) can use a puppet cut as [picture cut-out](picture-cutout.md) cuts
its own, drawn in this style's line and shade. Only the pieces that sway in a hold are cut loose from a pose
picture: long hair, a scarf, a coat tail.

## Pictures

Once this style is picked, the prompts below make every character, creature, prop and set of the whole cartoon.
Use each one as it is and change only the slots in angle brackets; do not reword the style words, or the look
drifts from one picture to the next.

Every new picture passes an earlier picture of the same cartoon in `imageUrls` as its style reference: the first
character's base for a new character, a creature, a prop or a set; the pose's own base for a pose or a part edit.
Only the very first base is drawn without a reference. That keeps the outline weight, the one hard shade tone,
the white rim light on one side, the flat saturated colour and the body proportions the same from the first
picture to the last.

Every picture is Nano Banana 2 (`gemini-3.1-flash-image`) at 2K: 1:1 for a pose that reaches wide (a strike, a
kick, a wind-up), 9:16 for an upright one (standing, landed), 16:9 for a set. Quote every batch with
`picsart_preflight` first.

## Characters

The first character's base names the style in words. Draw it twice and keep the cleaner:

> Action anime character for 2D cut-out animation, <view and pose, below>. <who they are: age, build, hair,
> eyes, expression>, <outfit and its colours>. Bold black outlines of varying weight, thicker on the outer edge,
> hard-edged two-tone cel shading with one flat shade tone and no blending, saturated flat colours, strong light
> from one side with a thin white rim light on the other side, long legs and a slim waist, sharp eyes. No
> gradients, no glow, no speed lines, no effects, no ground, no text. Full body, nothing in the hands, no cast
> shadows, plain pure white background, for 2D cut-out animation.

Every later character passes the earlier bases as references and changes only who it is:

> A different character from the same action anime as the reference pictures, drawn in exactly the same style:
> the same bold outlines, the same hard two-tone shading, the same rim light, the same body proportions and the
> same pose. <who they are in a few words>: <build, hair, eyes, expression>. <outfit and its colours>. No
> effects, no ground, no text. Full body, nothing in the hands, no cast shadows, plain pure white background.

- Hair shape, outfit colour and build tell the cast apart at a glance; the hero colour is never an outfit colour.
- Ask for one loose piece that streams in a fast pose (a scarf, a long coat tail, a ponytail) and say where it
  ends ("ends above the waist and does not cover the arms").
- The base shading is part of the drawing: "no cast shadows" keeps shadows off the floor, not off the figure.

## Views

A fight is shot from the side, so the side view and its action poses are the main model. A front view is only
for a stare at the viewer or a line-up.

| View | Base pose | Used for |
|---|---|---|
| Side | three-quarter side view facing right, standing low and balanced, knees bent, fists up | every action shot |
| Front | facing the camera, standing straight, arms held away from the sides, fists loose | a stare-down, a line-up |

Every action pose is an edit of the side base:

> The same character in exactly the same drawing style, same outfit, same colours and same line weight, in a new
> pose: <the pose, below>. The whole body faces right, the same way as the reference picture: the face, the chest
> and the leading fist or foot point to the right side of the picture. Full body, the whole figure inside the
> picture with space around it, no speed lines, no effects, no ground, no cast shadow, plain pure white
> background.

| Pose | Words that work | Used for |
|---|---|---|
| Ready | standing low and balanced, knees bent, fists up | the start of a shot, a stare-down |
| Wind-up | leaning back away from the target, the striking fist pulled far back by the hip, the other arm forward with an open hand, weight on the back leg, eyes on the target | the anticipation hold |
| Strike | a punch at full stretch, the striking fist thrust far forward and large in perspective, the other arm pulled back, the body leaning forward, the back leg straight, the front knee bent, the hair and the scarf streaming back | the dash and the held pose after the hit |
| Kick | a high kick at full stretch, the kicking foot far forward and large, the standing leg straight, both arms flung out for balance | the dash and the held pose after the hit |
| Landed | low on one knee, one hand flat on the ground, head down, hair and cloth still in the air | the hold after a jump or a dodge |
| Hit | thrown back, chest up, arms and legs trailing, eyes shut, mouth open | the one who takes it |

- Without "the same way as the reference picture" an edit can come back facing the other way. Mirror it rather
  than draw it again: the drawing has no writing and no one-sided mark that would give it away.
- All poses of a shot face the same way, and a character is flipped as a whole to face the other way.
- Ask for no effects and no ground in every picture: speed lines and dust drawn into a pose cannot move.

## Sheets and the cut

The outline is near black and closed, so the white background is removed by filling in from the picture's edge
up to the line; the pose keeps its whole outline. Drop specks of a few pixels left in the corners before
cropping. Check each pose alone on the blue and on the red ground: a white fringe outside the line means the
fill stopped short.

- Scale every pose of a character by the same factor, and stand each one on its soles (or its knee) on the floor
  line.
- A pose is not cut into parts: it holds whole. Only these edits are taken from it, each aligned to the pose and
  taken as a patch or a difference:

| Piece | Comes from |
|---|---|
| blink | `Same picture with eyes closed.`: only the patch round the eyes |
| a shout | `Same picture with mouth wide open, shouting.`: only the patch round the mouth |
| a talking mouth | `Same picture with mouth open.`, `Same picture with mouth in a small o.` |
| hair that sways in a hold | the pose minus `Same picture without hair: the head is drawn complete and round where the hair was.` |
| a scarf or coat tail | the pose minus `Same picture without the scarf: the neck and shoulders are drawn complete where the scarf was.`, on a mesh pinned at its root |
| an arm that moves in a calm talk | the pose minus `Same picture without the near arm, without the hand and without the sleeve: the side of the body and the clothes are drawn complete where the arm was.` |

## Creatures

A creature (a beast, a summoned spirit, a robot) is one picture per pose like a character, with a character's
base as the style reference:

> A character sheet picture for animation, in exactly the same action anime style as the reference picture: the
> same bold black outlines, the same hard two-tone shading with one flat shade tone, the same white rim light and
> saturated flat colours. One creature alone: <what it is, its body, its head, its limbs, tail or wings held
> clearly apart from the body, its eyes, its markings and their colours>, <its pose>, facing right. The whole
> creature inside the picture with space around it, no effects, no ground, no cast shadow, no other characters,
> no text, plain pure white background.

A prop (a sword, a shield, a ball, a rock that breaks) has its own picture, so it can fly, spin or shatter:

> A single prop for 2D animation, in exactly the same action anime style as the reference picture: bold black
> outlines, hard two-tone shading, flat saturated colours. <the prop, its material and colour>, seen from the
> side, alone and whole, no hands holding it, no effects, no shadow, no text, plain pure white background.

- Size a creature and a prop against the characters' bases, and use the same pose scale for all.
- A prop held in a pose is drawn in that pose's picture; the prop picture is only for when it leaves the hand.

## Sets

During an action the place disappears: the ground is one flat colour filled with speed lines, and it changes
colour on the hit. This is the style at its loudest, and it needs no picture.

A place for the calmer shots is one picture per place, with a character's base as the style and scale
reference:

> A background painting for an animation, in exactly the same action anime style as the reference picture: bold
> black outlines, flat saturated colours, hard-edged shadows, no gradients, no soft light. <the place and the
> time of day>: a wide flat floor running straight across the lower third of the picture, seen from the side at
> eye level, <what stands behind it>, <the sky or the far wall>, drawn at the size of the reference character.
> No people, no characters, no animals, no text. Only the background.

16:9 for a held shot, 9:16 for a vertical film, 21:9 for a pan. A set is not the ground of a hit: cut to the flat
colour on the dash and back to the set after the hold.

## Effects drawn as shapes

All of them are flat fills with hard edges, redrawn rather than moved.

- **Focus lines:** 45 to 60 thin wedges from outside the frame towards one point, each a three-point path, their
  tips stopping at an uneven ring that leaves the figure clear. Most are the ground's dark tone, about one in
  five white, and after a hit a few ink. They are redrawn with new angles and widths, never rotated: every four
  frames in a wait, every two frames after a hit.
- **Streaks:** for a dash, 40 to 50 long thin wedges along the direction of travel, white with a few in the
  figure's ground colour and one or two in flash yellow, on an ink ground, redrawn every frame.
- **Impact frame:** one frame of pure white with ink spikes from the point of contact and the figure over it,
  then two frames of the next shot under a `negative` adjustment layer, then the shot as it is. Three frames in
  all; more reads as a fault.
- **Burst:** a 13-point star in flash yellow with a 10 px ink outline and a smaller white star inside it, at the
  point of contact and behind the figure. It grows from 45% to 115% over three drawings on twos, holds for three
  more with each drawing's points redrawn, then is cut.
- **Dust:** puffs of three or four overlapping ellipses in warm white with an ink outline, low on the floor line
  on both sides of the feet. Each puff moves out and up a little, grows for six drawings on twos, shrinks for
  three and is cut.
- **Smear:** the pose stretched 150% along the move, with two copies behind it at 50% and 25% opacity. These
  copies are the only transparent things in the style, and they last one frame each.

## Motion rules

Every move has three parts, and the times are counted in frames at 30 fps.

1. **Anticipation:** the wind-up pose, held 20 to 30 frames. The figure does not move; the lines redraw on fours
   and the camera pushes in slowly.
2. **The move:** two to four frames. The strike pose is smeared across the frame on streaks, a new place every
   frame, then the impact frame.
3. **The held pose:** the strike or landed pose, held 40 frames or more. The burst, the dust and the shake play
   out over the first 12 to 20 frames; after that only the lines and any loose hair or cloth are alive.

- Poses cut. Nothing eases from one pose to another, and no pose fades in.
- Effects step on twos; the wait steps on fours. The figure itself never steps: it holds.
- A blink or a mouth change in a hold is a swap of a patch round the eyes or the mouth, taken from an edit of the
  pose (`Same picture with eyes closed.`, `Same picture with mouth open.`).
- The longer the hold before a move, the harder the move reads. Do not shorten a hold to fit more action in.

## Camera

- **Tilted.** The frame is rolled 4 to 8 degrees, one way in the wait and the other way after the hit. It is
  level only in the dash.
- **A slow push in the wait:** about 6% over the hold, on linear easing.
- **A snap on the hit:** the frame jumps in to about 122%, settles back to 112% over eight frames, then creeps in
  very slowly through the hold.
- **Shake on contact:** the whole frame is offset by up to 34 px at 1920 wide, a new offset every frame, dying
  out over 12 frames.
- Build the world larger than the frame (2600 by 1500 for 1920 by 1080), so a tilt or a shake never shows an
  edge. The camera is the transform of the layer that plays the world.
- A shot ends on a two-frame white flash or a hard cut. No dissolve.

## Shots

A film in this style is built shot by shot: plan the shot's poses, generate only those pictures, then move them
with the effects and the camera above. Every shot is one of three beats, and one world scene per shot.

| Beat | Poses | Length | What moves |
|---|---|---|---|
| Action | wind-up, strike (or kick), and landed or hit for the one who takes it | 2.5 to 4 s | the wait (lines on fours, slow push, tilt), the 2 to 4 frame dash on streaks, the impact frame, then the held pose under burst, dust, snap and shake |
| Calm | one pose: ready, standing, a stare | 2 to 4 s | the set or a flat ground with slow lines, a slow push, a blink patch every 2 to 3 s, a mouth patch for a line, hair or a scarf swaying on fours |
| Reaction | one pose, the face close | 1 to 2 s | a snap in to the face, a short shake, focus lines on twos, an eye or mouth patch on the beat |

- Plan the film as a list of shots with their beat and poses before generating any picture, and quote the whole
  list's pictures in one `picsart_preflight` batch. A pose already drawn is reused in a later shot, not drawn
  again.
- Two characters in one action shot are two pose pictures in the same world: the one who strikes on one side,
  the one who takes it on the other. The hit pose cuts in on the impact frame.
- Compare each new pose with the character's base before using it: the hair, the outfit and the colours must
  match. Redraw a pose that drifts; a mirrored edit is not a drift.
- Join the shots with a hard cut or a two-frame white flash. The ground colour changes on a cut, never inside a
  hold.

## Type

A heavy condensed italic sans in white with a 10 px ink outline, set on the tilt of the frame. A shouted word or
a sound word may be flash yellow and arrives in one frame at 130%, settling to 100% over three.

## Sound

Fast drums and distorted guitar or a hard synth bass, silence for the last few frames of the wind-up, a sharp
whoosh on the dash, one deep hit with a short ring-out on the impact frame, a low rumble under the shake.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Every outline is ink and closed; no grey or tinted line.
2. Every colour has exactly two tones with a hard edge between them.
3. Flash yellow is only on the hit.
4. No blur, gradient or fade anywhere; the only transparency is a smear's copies.
5. The figure is clear of the lines: no wedge crosses the face.
6. The frame is tilted in every shot but the dash.

## Build with the tools

1. **Pictures:** as [Pictures](#pictures) says: quote with `picsart_preflight`, generate with
   `picsart_generate`, every later pose an edit of the first.
2. **Poses:** remove the white up to the outline and save each as a transparent picture; save the character with
   `picsart_asset_save`, every pose in `referenceImages`.
3. **World:** one scene larger than the frame holding the grounds, the lines, the poses and the effects. Each
   redraw of the lines, the burst and the dust is its own layer with a `start` and a `duration` of two frames
   (four in a wait), and each pose is a media layer that lasts as long as its hold.
4. **Camera:** the film plays the world through a `scene_ref` layer; key its `scale`, `rotation` and `position`
   once per frame on `linear` easing, so a shake lands on every frame. The `negative` adjustment layer and the
   closing white flash sit above it.
5. **Check:** make a `picsart_scene_contact_sheet` with a time on each frame of the move, and look at the wind-up
   and the held pose at full size.
6. **Render:** `picsart_scene_export` at full quality.

## Do / don't

- **Do** plan a shot as wait, move, hold, and give the holds most of the time.
- **Do** change the ground colour on the hit.
- **Do** redraw lines, bursts and dust on each step.
- **Don't** tween between two poses or fade anything in or out.
- **Don't** rotate or scale one set of speed lines to animate it.
- **Don't** put flash yellow on a character or a set.
- **Don't** let the impact frame run longer than three frames.

## Originality guard

Invent the cast: names, hair, outfits, marks and the way they fight. It must not resemble the characters,
hairstyles, uniforms, headbands, weapons, energy attacks or signature poses of a known anime or manga series, or
a named series' title lettering or sound-word lettering. Speed lines, impact frames and a held pose after a hit
are shared craft; a copy of one series' attack, costume or framing is not.

## Proven on

A three-second punch: two pictures of one fighter (a wind-up and a strike, the strike an edit of the wind-up,
mirrored), cut from white, with every effect drawn as shapes: a held wind-up on blue, a three-frame dash with
streaks and two ghosts, a white impact frame, two inverted frames, then the held strike on red with a burst, dust
and a decaying shake.
