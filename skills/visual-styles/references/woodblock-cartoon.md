# Woodblock cartoon

A whole cartoon in the manner of a Japanese colour woodblock print: flat colour areas inside a bold even line,
patterned surfaces (waves, cloth, clouds), skies graded from deep blue down to bare paper, a few blues, an
indigo and one red, and one sheet of paper over everything. People wear old Japan clothing. It moves like a
series of prints: every beat is one still printed pose, held while the rain falls over it, then cut to the next.
Every character, creature, prop and place is a generated picture. Who the characters are comes from the story;
this page holds only how they are printed, posed and cut together.

## Contents

- [What it is not](#what-it-is-not)
- [Palette](#palette)
- [The medium](#the-medium)
- [Why the cast is still poses](#why-the-cast-is-still-poses)
- [Pictures](#pictures)
- [Characters](#characters)
- [Views](#views)
- [Poses](#poses)
- [Part edits](#part-edits)
- [Creatures and props](#creatures-and-props)
- [Backgrounds](#backgrounds)
- [Cutting a pose](#cutting-a-pose)
- [One sheet of paper](#one-sheet-of-paper)
- [Motion habits](#motion-habits)
- [Printed effects](#printed-effects)
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

- Not [woodblock print](woodblock-print.md): that one is a landscape built from shapes (cast `shapes`): a scale
  sea from a repeater, a sun, hills and mist bars, with a figure drawn as a trapezoid robe. Here every person,
  creature and place is a generated picture in the print's look, and the cast acts through printed poses, front
  and side (cast `pictures`).
- Not [woodcut](woodcut.md): that is one black ink block with white gouge marks, no colour.
- Not [watercolour anime](watercolour-anime.md), [pastel anime](pastel-anime.md) or
  [picture cut-out](picture-cutout.md): those cut a character into a puppet that bends and walks smoothly. Here a
  body never bends: each pose is a whole picture that holds, and only the air, a blink, a mouth and loose cloth
  move inside it.
- Not the anime styles in general: faces are a few fine strokes on a pale face, not large glossy eyes.

## Palette

Few and printed. The colours are the pictures' own; name them in a prompt only to bring a later picture back in
line with the first.

| Role | Colour | Its one job |
|---|---|---|
| paper | `#efe3c8` | the ground of every picture, the bottom of every sky, faces and hands |
| line | `#2a2420` | the key block: a bold even dark line round every area; also the rain |
| deep blue | `#1f3c6b` | the top of the sky, deep water, dark cloth |
| light blue | `#4f74a3` | water, far hills, cloth patterns |
| pale blue | `#8fa9c8` | mist, near sky, snow shade |
| indigo | `#2b2b3a` | hair, a dark robe, night |
| muted green and earth | `#6f7f4f`, `#b59a72` | pine, grass, wood, roads, roofs |
| red (hero) | `#c8402e` | **the one red**: a sash or cord, a lit window, a lantern, a seal; few and small |

- Faces and hands are the paper colour, never pink.
- A second warm colour is the earth tone, never orange.
- Night is the same picture under a deep blue grade and a paper-white moon, never a redrawn picture.

## The medium

- **Flat colour inside a key line.** Every area is one flat colour with a bold dark line of even width round it.
  No shading, no highlights, no cast shadow.
- **Pattern is the texture.** Cloth carries a printed pattern (waves, checks, scattered flowers, stripes), water
  carries curling wave lines, clouds are flat bands with a lined edge.
- **The sky is graded (bokashi):** deep blue at the top fading to bare paper at the horizon.
- **Paper everywhere.** The colour sits in paper: its fibre shows in the flat areas and the light parts are bare
  paper ([One sheet of paper](#one-sheet-of-paper)).
- **Faces are strokes.** Narrow eyes, a fine nose line and a small mouth drawn with a few fine strokes on a pale
  face; hair is one flat indigo mass with a few fine lines.

## Why the cast is still poses

A character is a set of printed poses, each one a whole picture, held and then cut to the next.

- A print is a still image. A puppet that bends at its joints reads as a cut-out pretending to be a print; a held
  pose with rain falling over it reads as a print come alive.
- A pose keeps the drawing whole: the cloth pattern, the folds and the line are the printer's, not stretched over
  a mesh.
- An edit that removes a part to build a rig is the edit most likely to fail (the arm edit left a bare arm and
  reprinted the sash). A pose needs only the picture itself and small eye and mouth patches.
- So the cost is one picture per pose, and a story is planned by its poses: say which ones each shot needs before
  generating any.

## Pictures

Every character, pose, creature, prop and place in a woodblock cartoon is a generated picture, made with these
prompts and only their `<slots>` changed. Once the first character exists, **every new picture passes an earlier
picture of the same cartoon as its style reference** (`imageUrls`), so the line, the palette and the paper stay
the same from the first picture to the last.

- **Model:** Nano Banana 2 (`gemini-3.1-flash-image`), 2K. Its edits keep the size and the feet where they were,
  so a pose edit lands on the same spot as its base. Quote each batch with `picsart_preflight` first.
- **Shape:** 9:16 for a character or a pose, 1:1 for a creature or a prop, 16:9 for a place (9:16 in a vertical
  film, 21:9 for a pan).
- **References:** a later character passes the earlier bases; a pose or a part edit passes only the picture it
  changes; a creature, a prop or a place passes a character base; a second place passes the first place too.
  Only the first base has no reference.
- **Keep the same in every prompt:** the medium's sentence ("in the style of a Japanese colour woodblock print:
  flat colour areas with a bold even dark outline, printed patterns on cloth, no shading, no gradients on the
  figure, the colours of aged paper, deep blue, indigo and one red, the paper grain showing in the colour"), soft
  even light, no shadows and a plain paper background. A shorter "ukiyo-e style" comes back with shading and many
  colours.
- **Write prompts in plain words:** colours by name ("deep blue", "indigo", "red"), never codes or numbers.

## Characters

The first character's base names the style in words. Draw it twice and keep the cleaner:

> Character for 2D cut-out animation, in the style of a Japanese colour woodblock print: flat colour areas with a
> bold even dark outline, printed patterns on cloth, no shading, no gradients on the figure, the colours of aged
> paper, deep blue, indigo and one red, the paper grain showing in the colour. <view and pose, from Views or
> Poses below>. <who they are: age, build, hair style of old Japan, expression>, wearing <old Japan clothing:
> garment, its pattern and colours>. A pale paper-coloured face with narrow eyes, a fine nose line and a small
> mouth drawn in a few fine strokes; hair as one flat indigo mass with a few fine lines. Soft even light. Full
> body, nothing in the hands, no shadows, no text, no seal, plain pale aged paper background with nothing else
> printed on it.

Every later character passes the earlier bases as `imageUrls` and changes only who it is:

> A different character from the same woodblock print cartoon as the reference pictures, printed in exactly the
> same way: the same flat colours, the same bold even dark outline, the same paper and the same palette of deep
> blue, indigo and one red, the same face strokes and the same proportions. <view and pose>. <who they are: age,
> build, hair style of old Japan, expression>, wearing <old Japan clothing: garment, its pattern and colours>. No
> shading. Full body, no shadows, no text, no seal, plain pale aged paper background.

- `<old Japan clothing>` is a garment and its printed pattern, for example "a deep blue kimono with a white wave
  pattern, a red sash, white tabi socks and straw sandals" or "an indigo short kimono with a white check pattern,
  light blue hakama trousers and straw sandals". The pattern and the main colour tell the cast apart at a glance.
- Keep the red small: a sash, a cord, a lining. Two characters in one shot never both wear a large red.
- A character that holds a sword, a fan or an umbrella in most of its poses holds it in the base too ("both hands
  on a long sword", "an oiled paper umbrella over the shoulder") so every later pose keeps the same object.

## Views

A story is shot mostly from the side, so the side base and its poses are the main set. A front base is for
speaking to the viewer, a bow or a line-up.

| View | `<view and pose>` | Used for |
|---|---|---|
| Side | `Full body, exact side view (profile), the whole body faces right, standing straight, the arms hanging down, the sleeves hanging clear of the body` | meeting someone, looking out at the place, the start of every side pose |
| Front | `Full body, standing straight facing the camera, both arms held a little away from the sides, open hands, feet slightly apart` | speaking to the viewer, a bow, a line-up |

The side base can also be an edit of the front one (pass the front base):

> Same character, same woodblock print, same clothing and pattern, full body, exact side view (profile). The whole
> body faces right: the face, the chest and the toes all point to the right side of the picture. Standing straight,
> the arms hanging down. Everything else unchanged, the same paper.

A character facing left is the same picture flipped in the scene; order a left-facing picture only when the
clothing is not the same on both sides (a crest, a sash tied on one side).

## Poses

Every pose is an edit of the side (or front) base, so the feet, the size and the paper stay where they were:

> Same picture, the same character now <the pose, below>. The whole body still faces right. <what the hands
> hold, and where>. The feet <stay exactly where they are, or: move to where>. Same character, same clothing and
> pattern, same woodblock print, the same size in the picture. Everything else unchanged, the same paper.

| Pose | `<the pose>` | Held for |
|---|---|---|
| Step | `walking to the right, in mid-step, the near foot forward and flat on the ground, the far foot behind with the heel raised, the kimono hem parted a little at the front by the step, the near arm hanging with the hand by the thigh and the sleeve swinging back a little` | a walk: one of three [walk drawings](#a-walk) |
| Passing | `in the passing step, both feet close together under the body, the far foot flat and the near foot just lifted with its heel up as it swings forward, the hem closed, the sleeve swinging forward a little` | a walk: the drawing between two steps |
| Other step | `the next step of the same walk: now the other leg leads, the far foot forward and flat on the ground, the near foot behind with its heel raised, the sleeve swinging forward a little`, passed the Step picture as its reference, with `the same stride length as the reference` | a walk: the second step |
| Bow | `bowing from the hips, the back straight, the hands together in front of the knees` | a greeting, an apology |
| Look up | `the head tilted up, looking at the sky, one hand raised to the brow` | rain, a bird, a sound |
| Kneel | `kneeling on one knee, one hand flat on the ground, the head down` | the end of a fall, a defeat, a vow |
| Run | `running, the body leaning forward, one knee high, the sleeves streaming back` | flight, a chase: two run poses swapped on twos |
| Wind-up | `a wide stance, the feet planted far apart, the front knee bent, both hands raising <the weapon or thing> high above the head` | the hold before a strike or a throw |
| Strike | `the end of a downward cut: both arms stretched straight out in front of the chest toward the right side of the picture, <the weapon> straight and rigid, pointing forward to the right and slightly down, in the empty space in front, not touching the body or the clothes, the upper body leaning forward` | the hold after the blow |

- Order only the poses the plot shows; three or four poses carry most scenes.
- Say "straight and rigid" and "not touching the body" for a held weapon: without it the blade came back bent
  round the body.
- An outstretched pose can run off the picture's edge (the hands did, even with the words above). Show that pose
  in a closer shot with the cut edge on the frame's edge, not in a wide shot.
- A pose made directly as a later character's base (the prompt above with the pose in `<view and pose>`) is as
  good as an edit, when the character never stands still in the story.

## Part edits

A pose holds whole. These edits give only what moves inside a hold, each taken from the pose it changes as a
patch or a difference, and each ending `Everything else unchanged, the same paper.`

| Piece | Edit of the pose | Gives |
|---|---|---|
| eyes closed | `Same picture with eyes closed: each eye is one fine downward curved stroke.` | the blink patch |
| mouth open | `Same picture with the mouth open in a small dark oval, as if speaking.` | the talking mouth patch, swapped with the closed one |
| no arm | `Same picture with the near arm removed completely: no sleeve, no arm and no hand on the near side, nothing hangs from the shoulder. The <garment> ends in a small round armhole edge at the shoulder, and the side of the body is printed complete where the sleeve, arm and hand were: the <garment colour and pattern> continues down the side, and the <sash> is printed complete and keeps its colour.` | the long hanging sleeve with its hand (the pose minus this picture), to stir a degree or two in a hold |
| no hair | `Same picture without hair: the head is a complete smooth head in the same pale face colour and outline.` | loose hair or a topknot tail (the pose minus this picture), to stir in the wind |

- Only the patch round the eyes or the mouth is taken from a face edit, cropped with about 20 px round the
  difference, feathered 4 px, swapped in and never faded.
- A shorter "without the arm and the sleeve" took off only the sleeve, left a bare arm and reprinted the sash in
  the kimono's colour: name every part that goes and every colour that stays.
- A stirring sleeve stays under about 3 degrees; past that its pattern smears. A bigger move is the next pose.

## Creatures and props

A creature (a crane, a cat, a fox, a carp) is one picture per pose like a character, with a character's base as
the style reference:

> A creature for 2D cut-out animation, printed in exactly the same Japanese woodblock style as the reference
> picture: flat colour areas with a bold even dark outline, no shading, the same paper, deep blue, indigo and one
> red. One <creature: kind, body, colours>, <its pose: standing, wings spread in flight, leaping>, side view
> facing right. The whole creature is in the picture with space around it. Soft even light, no ground, no
> shadows, no other characters, no text, plain pale aged paper background.

- A bird in flight is two poses (wings up, wings down) swapped on twos as it drifts across; a fish leaps in two.
- `Same picture with eyes closed.` gives the blink.

A prop a character holds or a thing that stands in a place:

> One <prop: an umbrella of oiled paper, a paper lantern, a fan, a basket, a boat: its shape, pattern and colours>,
> printed in exactly the same Japanese woodblock style as the reference picture: flat colour areas with a bold
> even dark outline, no shading, the same paper and palette. Side view, the whole object with space around it.
> Soft even light, no shadows, no hands, no text, plain pale aged paper background.

A held prop is part of the pose picture; a prop on its own is for a thing that falls, floats or is thrown.

## Backgrounds

One picture per place, with a character's base as the style and scale reference:

> A background for an animated cartoon, printed in exactly the same Japanese colour woodblock style as the
> reference picture: flat colour areas with a bold even dark outline, printed patterns on water and clouds, the
> paper grain showing in the colour, deep blue, indigo, muted green, earth and one red. <the place>, in <the
> season>, at <the time of day>: a wide flat <road, bank, bridge deck or floor> running straight across the lower
> third of the picture, seen from the side at eye level, <what stands behind it: houses, pines, a river, far
> hills, mist bands across the hills>, <the sky: graded from deep blue at the top down to bare paper at the
> horizon, with flat lined cloud bands>. Plenty of empty ground in the middle. The character in the reference
> shows the style and the scale only: do not draw them. Only the background: no people, no characters, no
> animals, no rain, no text, no writing, no seal.

- The season names what changes: "pines and plum blossom" in spring, "rice fields and tall grass" in summer,
  "red maple leaves" in autumn, "snow on the roofs, the ground bare paper" in winter.
- `<the time of day>` is said by the sky only: "a dawn sky with a pale red band", "a dusk sky with heavy dark cloud
  bands", "a night sky in deep blue with a pale moon". Night can also be the day picture under a grade.
- Ask for "no rain" and add the rain as lines in the scene, so it falls.
- A second place in the same cartoon passes the first place as well as the base, so the sky and the paper match.
- Keep the ground flat and pale so the figures and their cloth patterns stay the strongest thing.

## Cutting a pose

- **Paper out by the line, not by colour.** Faces and hands are printed in the paper colour, and the paper is
  darker in the middle of a picture than at its border, so a colour key eats the face. Flood the paper in from the
  picture's edges, stopped by the dark key line (grown by 2 px to close small gaps).
- **Then the gaps:** label the enclosed areas the colour of the paper and pick by eye the ones that are gaps
  (between raised arms and the head, between a blade and the body); add them to the paper. A face, a hand and a
  bare arm stay.
- **An edge a limb runs off** is not flooded from, or the limb goes with the paper.
- The outline stays on the piece. Drop specks of a few pixels.
- Every pose of a character is scaled by the same factor and stands on its soles (or its knee) on the ground
  line, so a cut between two poses does not jump.

Check every pose alone on a strong flat colour: a paper rim or a missing face shows there and nowhere else.

## One sheet of paper

Each generated picture has its own paper, and two papers side by side read as two prints glued together.

1. Measure every picture's paper (the median of its border) and shift any picture more than three levels off the
   first place's paper by the difference.
2. Build the whole shot (place, poses, effects) in one `scene` asset. Scale the place about 3% past the frame so
   its own paper fills the margins.
3. Put the paper on that asset's one `scene_ref`: `analog_film_finish` with `paper` about 0.4, `grain` about
   0.04, `dust` 0, `vignette` 0 and `tintAmount` 0. The fibre then lies in the cloth, the sky and the effects alike,
   and it holds still.

## Motion habits

- **A series of prints.** A beat is one pose, held for a second or more; the next beat is a cut to the next pose.
  Nothing is drawn in between, and a body never bends, scales or turns on a joint.
- **What moves in a hold:** the rain or the snow, a blink, a mouth swap, a sleeve or loose hair stirring a degree
  or two, and the place drifting a few pixels sideways. A wind-up may rise a few pixels before it breaks.
- **On twos.** Everything that moves (the swaps, the rain, the drift) runs in a nested `composition` with `fps` 12
  under a 24 fps root.
- **A walk** is a few printed drawings, never a bending body: see [A walk](#a-walk). A run is two run poses
  swapped faster.
- **Action is still, then sudden.** A wind-up holds in the rain; the strike is a swap to the next pose with a
  [slash](#printed-effects) on the same drawing and a cut to a closer shot, kicked 3 px and settling over six
  frames; then a long hold in the end pose.
- One character talks at a time with a small mouth swap; the listener only blinks.
- **Transitions:** a cut on a held frame with every colour plate kicked 3 px off and settling over six frames.
  No flash, no zoom, no dissolve.

## Printed effects

The only shapes in the style, each flat and lined, inside the page asset so the paper lies over them:

- **Rain:** straight thin dark lines at one slant, about 30 px long, at about 0.8 opacity, falling on twos. Lay
  them in a tile and move the whole field one tile across and three tiles down over the loop, so it never jumps.
- **Snow:** paper-coloured dots with no outline, falling slowly on twos.
- **Petals and leaves:** small flat lined shapes (plum white, maple red), a few in frame, turning as they fall.
- **The slash:** a paper-white crescent with the key line round it, thick in the middle and pointed at both ends,
  along the path the blade takes, shown for about four drawings over the swap to the strike.
- **Mist** comes from the place picture ("mist bands across the hills"). A drawn paper-coloured band over a
  picture reads as a flat bar, not as mist.
- **The red seal:** a small red square at a corner of a title or an end card, never in a shot.

## Camera

Held, or a slow side pan along a wide place, as if unrolling a scroll. The ground line stays level. A blow, a
look or a feeling is a cut to a closer shot of the pose and back. No shake, no push in faster than a breath.

## Type

A vertical brush-style face in the line colour, inside a pale cartouche strip at the edge of the frame, with the
red seal under a title. Captions sit in the same strip; never across a figure.

## Sound

A bamboo flute, a plucked koto or shamisen, wooden clappers on a cut, wind, rain, water, cicadas, footsteps on
wood, a blade drawn. Silence is allowed, and a strike lands on one sharp sound after it.

## Scene features used

- `analog_film_finish` (`paper`, `grain`) on the page's `scene_ref`.
- A nested `composition` with `fps` 12 for the poses and the effects.
- Opacity keys for a swap: the off key at least half a frame before the on key (a gap of a thousandth of a second
  fades instead of cutting).
- A `mesh` with a skin deformer for a sleeve, loose hair or a branch that stirs.
- `fill` and `adjust` for a night grade.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. One paper over the whole frame; no two papers side by side.
2. Every area flat with the bold even line; no shading, no glow, no soft shadow.
3. Deep blue, indigo, muted green, earth and a little red.
4. The sky graded to paper at the horizon.
5. Every figure is a whole printed pose standing on the ground line; nothing bends.

## Build with the tools

1. **Plan by poses:** list each shot's poses and each pose's prompt, and quote the batch with
   `picsart_preflight`.
2. **Pictures:** `picsart_generate`, Nano Banana 2 (`gemini-3.1-flash-image`) at 2K, every later picture with the
   earlier one as reference.
3. **Poses:** cut as [Cutting a pose](#cutting-a-pose) says, each saved as a transparent picture; save each
   character with `picsart_asset_save`, every pose picture in `referenceImages`.
4. **Page:** place, poses and effects in one `scene` asset, the paper on its `scene_ref`, the poses and the rain in
   a 12 fps composition.
5. **Check:**
   - Look at every pose alone on a strong flat colour.
   - Render frames on both sides of every cut: no ghost of the last pose, no jump at the feet.
   - Make a `picsart_scene_contact_sheet` across the film.
6. **Render:** `picsart_scene_export` at full quality and 24 fps.

## Do / don't

- **Do** plan a scene by its poses before generating, and pass the earlier pictures as references.
- **Do** hold every pose for a second or more.
- **Do** repeat the medium's sentence word for word in every prompt.
- **Don't** bend a body on joints or blend one pose into the next.
- **Don't** add shading, glow, a soft shadow or a camera shake.
- **Don't** give a face anime eyes or pink cheeks: a face is a few fine strokes on paper.
- **Don't** put an effect shape outside the page asset: without the paper over it, it reads as vector.

## Originality guard

Invent the cast, the places and the patterns. They must not resemble a named print series' views, a named
master's signature compositions (the great curling wave over boats, a named mountain framed by it), a known
kabuki actor portrait, a real seal or a real person's crest. Flat printed colour, a graded sky, cloth patterns and
one red are the style.

## A walk

Four drawings make a step cycle: Step, Passing, Other step, Passing. Each is held a quarter of a second (three
frames at 12 fps), which is two steps a second.

- **Plant the feet.** The figure does not drift smoothly: it jumps at each swap so the foot that bears the weight
  stays where it landed. Measure the toe end of each sandal in the cut pictures. On a swap to Passing, the front
  foot of the last step and Passing's front foot line up. On a swap to a step, Passing's front foot and the new
  step's back toe line up. With a smooth drift the planted foot skates.
- **Rise on Passing** by about 1% of the figure's height (3 px at 335 px tall).
- Key the position with the same half-frame gap as the swaps (an off key 1/48 s before the on key), so it jumps
  and never slides.
- In a long kimono seen from the side, the two steps come back with nearly the same legs; the sleeve and the hem
  tell them apart. That reads as a walk. For trousers or bare legs, check the legs really alternate.

## Proven on

Two 3 second 960x540 loops and a 4 second walk, Nano Banana 2 at 2K. Every picture after the first base passed an earlier one as its
reference, and all came back in one print look.

- **A duel:** a swordsman in a wind-up pose and a strike pose on a bridge at dusk, in rain drawn as
  lines. He holds the wind-up, the slash crosses, the shot cuts close on the strike, holds, and cuts back. The
  first strike edit bent the blade round his body; the retry, worded as the strike above, came back with a
  straight blade but the hands past the picture's edge, so the strike is shown close with that edge on the
  frame's edge.
- **A quiet hold:** a side-view woman in a wave-pattern kimono on a riverside road in spring. She holds while her
  sleeve stirs, she blinks and plum petals fall. The first arm edit took off only the sleeve, left a bare arm and
  reprinted the red sash blue; the retry, worded as the no-arm edit above, came back right.

- **A walk (the preview):** the same woman crossing the riverside road on the [walk](#a-walk) above, the three drawings
  edited from her base, with petals falling. The first try swapped one step and one passing drawing while she
  drifted smoothly: her feet skated and the same foot always led. Planting the feet and adding the other step
  fixed both.

A front view, the run pose and a talking mouth are not proven in this look.
