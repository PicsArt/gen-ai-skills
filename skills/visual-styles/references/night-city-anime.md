# Night-city anime

An anime night in the city: a dark street lit by neon signs, a wet road that mirrors every light, rain, glowing
windows, and characters edged with the colour of the sign behind them. The characters are the same pictures a
daylight anime uses; night is a grade and a rim light put on them in the scene, never a second set of drawings.
Who the characters are comes from the story; this page holds only how the night is built, lit and moved.

## Contents

- [What it is not](#what-it-is-not)
- [Palette](#palette)
- [The medium](#the-medium)
- [Pictures](#pictures)
- [Characters](#characters)
- [Views](#views)
- [Creatures](#creatures)
- [Sets](#sets)
- [The set](#the-set)
- [Characters at night](#characters-at-night)
- [Light effects](#light-effects)
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

- Not [neon tubes](neon-tubes.md): that is a graphic of signs on a brick wall, with no one in it. Here the signs
  are the lamps of a film: they light a street, a road and the people on it.
- Not [synthwave](synthwave.md): no striped sun, no grid, no chrome title. The city is a place, seen at eye level.
- Not [firefly night](firefly-night.md): that is a dark meadow lit by drifting particles; this is hard coloured
  light from fixed signs, on wet ground.
- Not [cel anime](cel-anime.md) or [painted anime](painted-anime.md): both are daylight looks whose colour is in
  the drawing. Here the drawing's colour is pulled down and the light is added on top.
- Not the lo-fi loop in [painted anime](painted-anime.md#lo-fi-loop): that is a painted plate with rain, graded a
  little darker. Here every light is its own layer, so it can flicker, mirror in the road and rim a character.

## Palette

- **Darks are blue-violet, never black:** sky `#090820` to `#1a1342`, lifting to `#43246b` at the roofline;
  towers `#17133e` to `#1e1850`; shop fronts `#0b0922` to `#120e31`; the road `#1b1546` falling to `#06051a`.
- **Two neon accents:** magenta `#ff3d9a` and cyan `#27e0ff`, in about equal measure. Every sign, haze,
  reflection and rim is one of the two. Each tube has a white `#ffffff` core.
- **Windows** are dim blue and violet (`#1f2a68`, `#27357e`, `#352b7c`), with about one in seven lit pale
  blue-white `#cfe0ff`. Rain and ripples are a pale blue `#b9c8ff`.
- **The hero colour is a warm amber `#ffb347`** (lighter `#ffd89a` at its top), kept for the one light the story
  points at: a doorway, a lantern, a phone, an umbrella. Nothing else in the frame is warm.

## The medium

- **The cast is pictures; the city and every light are shapes.** A sign has to flicker, mirror in the road and
  light a character, so it cannot be painted into a plate.
- **A tube is two strokes** of one outline: a white core 3 px wide over a coloured tube 9 px wide (first listed
  draws on top), with the `glow` effect on the layer (`threshold` 20, `radius` about 36, `intensity` 2).
- **Every light is drawn four times:** the tube, a **haze** behind it on the wall, a **reflection** under it on the
  road and a **pool** where it lands ([Light effects](#light-effects)). The four share one opacity, so a sign
  that flickers takes its haze, reflection and pool with it.
- **Depth is focus:** the far towers are blurred (`gaussian_blur` 5), the shop row a little (1.6), the cast and
  the road are sharp.
- Sizes on this page are for a 1920 px wide frame.

## Pictures

The prompts below make every character, creature, prop and background of a cartoon in this style, from the first
picture to the last. Use them as written and change only the `<slots>`. **Every picture after the first passes
an earlier picture of the same cartoon as its style reference** (`imageUrls`): the first character's base for
characters, creatures and props, that base plus an earlier set for a set, the base itself for its views and part
edits. That reference, not the words, is what keeps the look the same across the film.

Every picture is made with Nano Banana 2 (`gemini-3.1-flash-image`) at 2K: characters, views and creatures at
9:16, sets at 16:9 (21:9 for a pan). Keep the same across all of them: the line, the shading, the proportions,
the daylight light and the plain pure white background. Each background is cut away (`picsart_image_remove_bg`)
before the picture goes in the scene.

**Characters are drawn in daylight.** Night is put on them in the scene ([Characters at
night](#characters-at-night)): a prompt that asks for night, neon or a rim light bakes one light into the picture,
and that light can then neither flicker nor change colour as the character passes another sign.

## Characters

The first character's base names the style in words. Draw it twice and keep the cleaner:

> Full-body anime character for 2D cut-out animation, <view and pose, from Views below>. <who they are: age,
> build, hair, eyes, expression>, wearing <outfit and its colours>. Modern TV anime look: clean dark line art of
> even weight, soft cel shading with gentle gradients, neutral daylight colours, soft even light from the front,
> slim natural teenage-to-adult proportions with a small head and long legs. The whole figure from the top of the hair
> to the soles, with space around it. Full body, nothing in the hands, no shadows, no ground, no text, plain pure
> white background, for 2D cut-out animation.

Every later character passes the earlier bases as `imageUrls` and changes only who it is:

> A different character from the same anime as the reference pictures, drawn in exactly the same style: the same
> line weight, the same soft cel shading, the same daylight colours and the same body proportions, in the same
> view and pose. <who they are: age, build, hair, eyes, expression>, wearing <outfit and its colours>. Full body,
> nothing in the hands, no shadows, no text, plain pure white background, for 2D cut-out animation.

- **Dress them for a wet night:** raincoats, hoods, jackets, boots and sneakers. Mid tones with one light piece
  read best once graded: a very dark outfit sinks into the street, a pure white one glows.
- Hair shape and the colour of the outfit tell the cast apart at a glance; the grade pulls every colour toward
  violet, so make the two leads differ in lightness as well as in hue.
- Say where long hair ends ("ends above the shoulder blades and does not cover the arm"), so it does not hide a
  part that moves.

## Views

Characters who meet each other on the street are side bases facing each other; a character who talks to the
viewer is a front base. Each view is its own base.

| View | `<view and pose>` | Used for |
|---|---|---|
| Side | standing in a clean side view (profile) facing <right or left>, relaxed, the near arm hanging straight down, <hands at the sides or one hand in a pocket> | two characters on the street, a walk under the signs |
| Front | standing straight facing the camera, both arms straight and held a little away from the sides, open hands, feet slightly apart | talking to the viewer, a close-up |

A second view of the same character is an edit of the first: `Same character, same anime style and outfit, full
body, exact side view (profile). The whole body faces right: the face, the chest and the toes all point to the
right side of the picture. Nothing in the hands, no shadows, plain pure white background.` Without the last
sentence on where the face, chest and toes point, the head can come back facing one way and the body the other.

Part edits, each on the base (the cut takes only the piece it needs; the rest is character-rigging's
`references/picture-sheets.md` and `references/cut-any-edge.md`):

| Piece | Edit |
|---|---|
| arm with its sleeve | `Same picture without the near arm, the hand and the sleeve: the side of the body and the clothes are drawn complete where the arm was.` |
| blink | `Same picture with eyes closed.` |
| mouth | `Same picture with mouth open.` and `Same picture with mouth in a small o.` |
| hair | `Same picture without hair.` A hood that sways is cut the same way: `Same picture without the hood: the collar is drawn complete.` |

## Creatures

A stray cat, a crow on a wire or a small made-up creature, with a character's base as the style reference:

> A picture for 2D cut-out animation, in exactly the same anime style, clean dark line art and soft cel shading
> as the reference picture. One <creature: body, ears or tail held clearly apart from the body, eyes, markings>
> alone, in side view facing <right or left>, drawn in daylight colours. The whole creature with space around it,
> no ground, no shadow, no other characters, no text, plain pure white background.

Props a character carries or stands by (an umbrella, a phone, a bicycle, a vending machine) use the same prompt
with <the prop, its colours and its view> in place of the creature, also in daylight. A prop that is itself a
light, a phone screen or a lantern, is the scene's hero light: its glow is a shape in the hero amber, not painted.

## Sets

The street is usually built from shapes ([The set](#the-set)). A place that shapes cannot draw well (a market
alley, a station platform, a bridge under a highway) is one picture, with a character's base as the style and
scale reference. The picture holds only what does not light up; every sign stays a shape on top of it.

> A background painting for an animation, in exactly the same anime style, clean dark line art and soft cel
> shading as the reference picture, at night. <the place>: a wide flat wet street or floor running straight across
> the lower third of the picture, seen from the side at eye level, <the buildings and what stands along it>, with
> <dark empty sign boards and frames where the signs hang>, <a few lit windows, dim blue>, under <the sky: a deep
> blue-violet night with no moon, or the underside of a roof>. Dark blue and violet shadows, no black, no warm
> lights. No people, no characters, no animals, no readable text.

Then add the signs, their haze, reflections and pools, the rain and the finish as on the rest of this page, and
give the plate the shop row's `gaussian_blur` so the cast stays the sharpest thing in the frame.

## The set

Three bands, back to front, with the cast's floor line at about 80 % of the frame height:

1. **Sky:** one rectangle with a vertical `gradientFill`, darkest at the top.
2. **Far towers:** plain rectangles of different heights with pin-prick windows (7 by 10 px), a mast and a red
   dot on a few roofs. One shape layer, blurred.
3. **Shop row:** fronts 260 to 400 px wide and 300 to 440 px high in three alternating darks. Each has a grid of
   small panes, an awning edge in a dull violet or blue, a shop front with shutter lines, and a roof box or
   parapet. Overhead wires are thin dark lines across the row.

Signs hang on the shop row, five or six across a frame, alternating magenta and cyan: a vertical stack of
blocks, a ring, a few bars, an empty frame. They are abstract tubes on a dark board; none holds a word.
The road is a rectangle with a vertical gradient and one thin lighter line along the floor.

## Characters at night

Characters come from an anime style whose cast is pictures, or from any look of
[picture cut-out](picture-cutout.md): the same models, the same actions. Three effects on the character's layer
make it night, in this order:

```json
"effects": [
  { "id": "adjust", "params": { "brightness": -0.2, "saturation": -0.2, "temperature": -0.3, "contrast": 0.06 } },
  { "id": "fill", "params": { "color": "#1c1650", "opacity": 0.3 } },
  { "id": "inner_shadow", "params": { "offset": [9, -2], "blur": 5, "color": "#ff3d9a" } }
]
```

- **`adjust` cools and dims** the daylight drawing; **`fill` at 0.3** pulls every colour toward the set's violet,
  so white clothes stop glowing.
- **`inner_shadow` is the rim light.** With a bright colour it paints a thin edge inside the silhouette, on the
  side the offset comes from: `[9, -2]` lights the left edge, `[-9, -2]` the right. Its colour is the sign behind
  that side of the character.
- **One rim per character,** from the nearest sign. Two characters who face each other take the two accents, each
  lit from behind.
- **The reflection** is the same model again under the character: the same actions, flipped about the floor line
  (`scale` y negative, about 0.75 of the height), opacity 0.3, the same grade and `gaussian_blur` 9. List it
  before the character.
- A flat dark ellipse (`#04031a`, opacity 0.65) sits under the feet; no other shadow.
- A character built from shapes or part sheets takes the same three effects, but the soft shading of a picture is
  what the rim reads best against, so the style's cast is `pictures`.

## Light effects

All shapes, all blended `screen`, each sharing its sign's opacity:

- **Haze:** a rounded rectangle 40 px larger than the sign on every side, in its colour at opacity 0.5,
  `gaussian_blur` 70, listed before the sign's board.
- **Reflection:** a rectangle under the sign from the floor line down about 200 px, 0.8 of the sign's width, with
  the sign's colour and `alphaStops` 0.75, 0.3 and 0 down its length, `gaussian_blur` 12.
- **Pool:** a flat ellipse on the floor line, about 3 times the sign's width and 46 px high, opacity 0.3,
  `gaussian_blur` 26.
- **Sign flicker:** one sign in a frame stutters, the others hold. Its opacity is an expression that steps at 24
  a second and dips to 0.18 at hashed moments inside one window of the loop:
  `local t = math.floor((time % 3) * 24); local h = math.sin(t * 91.7) * 43758.5; h = h - math.floor(h); if t > 22 and t < 46 and h < 0.5 then return 0.18 end; return 1`.
  On a media or text sign the `flicker_loop` look does the same.
- **Rain:** one tile of slanted streaks (a lean of 0.22 of their length) drawn over three tile heights and moved
  one tile per period. Two layers: far (110 streaks, 34 px long, 1.5 px wide, opacity 0.28, period 0.75 s) and
  near (50 streaks, 80 px, 2.5 px, 0.42, 0.5 s).
- **Ripples:** thin stroked ellipses (90 by 22 px) on the road that grow from 0.15 to full size and fade, period
  0.75 s, each on its own phase.
- **Finish,** on one adjustment layer over everything: `glow` (`threshold` 72, `radius` 28, `intensity` 0.5),
  `channel_shift` `horizontal` 0.8 (`mode` `rb`), `vignette` `fade` 35, `film_grain` `intensity` 0.07.

## Motion habits

- The city is still; the light and the water move. Rain, ripples and one flickering sign run through every shot.
- Characters move as their own style says, a little slower: held poses, small gestures, a breath and a blink.
- A character who walks under a sign changes rim colour as they pass it: swap the rim over four frames, never
  fade it slowly.
- In a loop every period divides the loop length, so the last frame flows into the first.

## Camera

Held at eye level with the floor line level, or one slow push in on a face. A walk is followed by a slow pan
along the shop row, the far towers moving at a quarter of its speed. No shake, no tilt.

## Type

A condensed sans in white with a thin magenta or cyan outline, at the foot of the frame over the dark road; a
title may be drawn as a tube sign.

## Sound

Steady rain, a low synth pad, the buzz of a tube, a tick on each flicker, wet footsteps, far traffic.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. No pure black and no warm colour outside the hero light.
2. Every sign has its haze, its reflection and its pool, and all four flicker together.
3. Every character has one rim, in the colour of the sign on that side, and a reflection under the feet.
4. No character is brighter than the signs: white clothes read as pale violet.
5. Rain crosses the whole frame, in front of the cast.
6. No sign holds a word.

## Build with the tools

1. **Cast:** make the characters as their own style says, or load saved ones. No night pictures are generated.
2. **Set:** build the three bands and the signs as shape layers; find the effects with `picsart_scene_capabilities`.
3. **Night:** add the three effects to each character's layer and place its flipped reflection under it.
4. **Check:** render a still with a flickering sign dimmed and confirm its haze, reflection and pool dimmed with
   it; make a `picsart_scene_contact_sheet` across the film.
5. **Render:** `picsart_scene_export` at full quality.

## Do / don't

- **Do** pick each rim's colour from the sign that stands behind that side of the character.
- **Do** keep the two accents in balance across the frame.
- **Do** list rain after the cast and reflections before it.
- **Don't** generate a night version of a character: grade the daylight one.
- **Don't** paint a sign into a background picture: it cannot flicker or reflect.
- **Don't** put the hero amber on a sign, or a third neon colour anywhere.

## Originality guard

Invent the street, the shop fronts and the signs. No sign copies a real shop's or brand's neon, and none holds
real or imitated lettering of any script. The city must not resemble a named film's or series' skyline, street or
vehicles. A rainy neon street at night is a shared genre idea; one production's signature place is not.

## Proven on

A 3-second loop: two characters generated as plain daylight anime pictures (side view, cut out) face each other
on a wet street, breathing, each graded for night and rimmed by the sign behind them, with five signs (one flickering), their reflections and pools, a warm doorway,
two layers of rain and ripples on the road.
