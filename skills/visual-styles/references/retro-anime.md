# Retro 90s anime

The look of hand-painted cels shot on film and seen on a television of the time: muted, slightly warm colour,
lines a little soft, a glow round the brightest things, grain that never holds still, a 4:3 picture that
weaves a pixel or two in its gate. The drawing is ordinary anime, with flat cel colour and one shade tone on
characters and painted sets; nearly all of the look is one film pass over the finished scene. Who the characters
are comes from the story; this page holds only how they are drawn, shot and moved.

## Contents

- [What it is not](#what-it-is-not)
- [Palette](#palette)
- [The medium](#the-medium)
- [Pictures: model and settings](#pictures-model-and-settings)
- [Characters](#characters)
- [Views](#views)
- [Sheets and the cut](#sheets-and-the-cut)
- [Creatures](#creatures)
- [Sets](#sets)
- [The 4:3 gate](#the-43-gate)
- [The film pass](#the-film-pass)
- [Rates](#rates)
- [Motion habits](#motion-habits)
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

- Not [cel anime](cel-anime.md): that is a clean, bright sky scene built from shapes, with no film look at all.
  Here the film is the look: the same drawing without the pass is not this style.
- Not [painted anime](painted-anime.md): its finishing pass is a modern film grade, a blurred copy of the whole
  frame in `screen`, a warm-to-blue wash and a faint colour fringe, in 16:9. This pass lowers the colour, softens
  the line itself, lets only the highlights glow, and adds heavy grain, dust, the 4:3 gate and the weave. Run one
  pass or the other, never both.
- Not [VHS tape](vhs-tape.md): no scanlines, no tracking band, no colour split, no tape marks. This is film, not
  tape.

## Palette

The colours are the drawing's own, pulled down by the pass. Draw a little brighter than the frame should end:
the pass takes about a fifth of the saturation off and warms what is left.

| Role | Colour | Its one job |
|---|---|---|
| gate | `#000000` | the bars left and right of the 4:3 picture |
| print warmth | `#e8a86a` | the soft-light wash of the film pass, over the whole picture |
| line | a dark brown or a darker shade of the fill, never pure black | outlines |
| fields | mid-saturation colours: dusty rose, olive green, ochre, slate blue, brick | hair, clothes, sets |
| white | cream, about `#f6efe0` after the pass | gloves, collars, clouds, the brightest things, which carry the glow |
| accent | **one clear, saturated colour per film** (a red ribbon, a blue gem), on one thing | the thing the story is about |

No neon, no pure white and no pure black inside the picture. Night is a darker, bluer drawing under the same
pass, never a second pass.

## The medium

- **Flat cel colour with one shade tone.** Every part is a flat base colour plus one hard-edged darker shape of
  the same hue, away from one light. No gradient on skin or cloth, no soft shadow. Hair has one hard highlight
  band.
- **A hand-inked line** in dark brown, of slightly uneven weight, about 5 px on a 2K picture. The pass softens
  it; never blur a drawing by hand.
- **Sets are painted**, with visible brushwork and softer edges than the characters, so the flat cels sit on top
  of them.
- **The whole frame is film.** Grain, dust and the glow cover characters, sets and titles alike (the template's
  whole-frame exception).

## Pictures: model and settings

Once a cartoon is in this style, every character, creature, prop and background in it is made from the prompts
below, used as written with only the `<slots>` changed, so the look holds from the first picture to the last.
The first character's base is the only picture made without a reference. Every picture after it passes an earlier
picture of the same cartoon as its style reference (`imageUrls`): the first character's base always, and for an
edit, the picture being edited.

Every character, creature and set comes from one model and the same settings, so the cast and the places match:

| | Setting |
|---|---|
| Model | Nano Banana Pro (`gemini-3-pro-image`); Nano Banana 2 (`gemini-3.1-flash-image`) for cheap drafts |
| Resolution | 2K |
| Characters, creatures, props | 3:4 |
| Sets | 4:3, the gate's shape; 16:9 or wider when the camera pans |
| Kept the same | the style words of the base prompts, word for word; the first character's base as a reference in every later picture |

Quote every batch with `picsart_preflight` before `picsart_generate`. The prompts below are plain words: no
colour codes or numbers go inside a prompt.

## Characters

Characters are cut from generated pictures (`cast: pictures`), by the route of
[picture cut-out](picture-cutout.md) and character-rigging's `references/picture-sheets.md` and
`references/cut-any-edge.md`. A hand-inked line of uneven weight, hard highlight bands in the hair and painted
eyes are what the period's drawing has and a shape sheet draws too cleanly; the pass softens a picture's line
into the frame, while a vector line under the same blur stays even and reads as modern.

The first character's base names the style in words and is drawn without a reference. Draw it twice and keep the cleaner one: it is the style reference for the whole cartoon.

> Character from a 1990s hand-drawn TV anime, drawn as a painted animation cel photographed on film. <view and
> pose, below>. <who they are: age, hair, eyes, expression>, <outfit and its colours>. Flat cel colours with one
> hard-edged shade tone on every part, hand-inked dark brown outlines of slightly uneven weight, one hard highlight
> band in the hair, large eyes with one big and one small highlight, slim natural proportions with a small chin and
> long legs, muted mid-saturation colours with a slight warm cast, soft even light, no gradients. Full body,
> nothing held in the hands, no shadows, plain pure white background, for 2D cut-out animation.

Every later character passes the earlier bases as `imageUrls` and changes only who it is:

> A different character from the same 1990s TV anime as the reference pictures, drawn in exactly the same style:
> the same painted cel colouring with one hard shade tone, the same dark brown ink line, the same eye and hair
> highlights, the same proportions and the same pose. <who they are in a few words>: <hair, eyes, expression>.
> <outfit and its colours>. Full body, nothing held in the hands, no shadows, no text, plain pure white
> background, for 2D cut-out animation.

- Hair shape and its colour tell the cast apart; keep outfit colours muted, a dark school-uniform navy rather
  than a bright blue.
- The model adds small period details on its own (a hairband, a neckerchief); keep them if they suit and name them
  in every later edit so they stay.
- Say where long hair ends ("ends at the shoulder blades and does not touch the arm"), so it does not cover a
  part that moves.

## Views

A character that both talks to the viewer and walks is two models from two bases, used by shot.

| View | `<view and pose>` | Used for |
|---|---|---|
| Front | standing straight facing the camera, both arms straight and held clearly away from the sides, open hands, feet slightly apart | talking to the viewer, a line-up, a wave |
| Side | exact side view facing right, standing straight, the near arm hanging straight down | walking, meeting someone, talking to each other |

The side base drawn as its own prompt came back clean in profile. Made as an edit of the front base it needs
the words: `Same character, same 1990s anime cel style and outfit, full body, exact side view (profile). The whole
body faces right: the face, the chest and the toes all point to the right side of the picture. Plain pure white
background.`

## Sheets and the cut

Each piece is the base minus one short edit of it, passed with the base as the only reference:

| Piece | Edit |
|---|---|
| arm with its sleeve | `Same picture without the arm, without the hand and without the sleeve: the top is sleeveless with a small round armhole edge at the shoulder, and the side of the body and the clothes are drawn complete where the arm and hand were. Same style, same white background.` |
| hair | `Same picture without hair: a smooth bald head drawn complete, same face, same style, same white background.` A long tail of hair that sways is its own piece the same way. |
| legs under a skirt | `Same picture, with skin-coloured leggings instead of the skirt.` |
| blink | `Same picture with eyes closed, drawn as one curved ink line each, nothing else changed.` |
| mouths | `Same picture with mouth open.` and `Same picture with mouth in a small o.`: only the patch round the mouth is taken |

- When one edit removes only the sleeve, chain a second edit on its result for the arm and the hand.
- Every edit ends "nothing else changed, same style, same white background", or the shade tone can move.

## Creatures

A small animal or made-up creature, or a prop a character holds, is one picture with a character's base as the
style reference:

> A character sheet picture for a 1990s TV anime, in exactly the same painted cel style as the reference
> picture: flat colours with one hard shade tone, dark brown ink line, muted warm colours. <one creature or one
> object: its body, ears or tail held clearly apart, eyes, markings>. Three-quarter view, turned to the right.
> The whole of it is in the picture with space around it, no ground, no shadow, no characters, no text, plain pure
> white background.

A part that moves (an ear, a tail) comes from `Same picture without <the part>, drawn complete where it was.`,
and a blink from `Same picture with both eyes closed.`

## Sets

One painted picture per place, passing the first character's base as the style and scale reference:

> A hand-painted background for a 1990s TV anime, painted in gouache, visible soft brushwork, soft edges, muted
> mid-saturation colours with a slight warm cast, in the same period style as the reference picture. <the place
> and the time of day>: a wide flat floor, street or path running straight across the lower third of the picture,
> seen at eye level, <what stands behind it>, <the sky or the far wall>. The painting fills the whole picture edge
> to edge. No people, no characters, no text. Only the background.

- The first try said "painted on paper" and came back inside a painted paper border; "fills the whole picture
  edge to edge" keeps the painting to the edge. If a border still comes, crop to the painted area.
- A set drawn wider than the gate gives room for a pan; crop a 16:9 picture to the gate rather than squeezing it.

## The 4:3 gate

The picture is 4:3 inside the frame, with black bars: 1440 by 1080 in a 1920 by 1080 frame, centred. In a
vertical frame the 4:3 picture sits across the full width (1080 by 810) with black above and below, and the
captions go in the lower bar.

Build it as three nested compositions:

1. **`drawn`**: the scene itself (set, characters), 4:3, at the held rate ([Rates](#rates)).
2. **`gate`**: 4:3 at the root rate. It holds `drawn` as a `scene_ref` scaled to 1.012 with the weave on its
   position, and the print layer above it. The composition's own edge is the gate, so the picture moves under a
   window that stays still.
3. **The film**: the full frame, black, with `gate` as one `scene_ref` at the centre carrying the
   `analog_film_finish` look.

**The weave** is one position expression, about a pixel and a half each way at 1080 high. In a loop, give every
term a period that divides the loop length (3 s below):

```json
"animations": { "position": { "expression": "local t = time\nreturn value + Vec.v2(1.6*math.sin(2*math.pi*t/3) + 0.7*math.sin(2*math.pi*4*t/3 + 1.3), 1.1*math.sin(2*math.pi*2*t/3 + 0.6) + 0.5*math.sin(2*math.pi*7*t/3))" } }
```

A position expression returns a vector (`value + Vec.v2(x, y)`); a Lua table fails the frame.

## The film pass

Two layers, in this order. Numbers are for a picture 1080 high; scale `blur` and `radius` with the height.

1. **The print**, an adjustment layer inside `gate`, over the weaving picture:
   - `gaussian_blur` `blur` 1.4: the soft line. Above 2 the faces lose their eyes.
   - `glow` `threshold` 72, `radius` 28, `intensity` 0.55, `knee` 25: only what is nearly white bleeds (gloves,
     clouds, a lamp, a window). Lower the threshold and the whole frame fogs, which is painted anime's diffusion.
   - `adjust` `saturation` -0.22, `temperature` 0.1, `contrast` -0.08, `shadows` 0.1, `highlights` -0.06: muted,
     warm, with lifted blacks.
2. **The stock**, the `analog_film_finish` look on the `gate` layer in the film: `grain` 0.45, `grainSize` 2,
   `dust` 0.18, `vignette` 0.3, `tint` `#e8a86a`, `tintAmount` 0.16. Dust above about 0.3 turns a TV print into
   a damaged reel.

```json
{ "id": "print", "adjustmentLayer": true, "content": { "kind": "color", "color": "#000000" },
  "effects": [{ "id": "gaussian_blur", "params": { "blur": 1.4 } },
              { "id": "glow", "params": { "threshold": 72, "radius": 28, "intensity": 0.55, "knee": 25 } },
              { "id": "adjust", "params": { "saturation": -0.22, "temperature": 0.1, "contrast": -0.08, "shadows": 0.1, "highlights": -0.06 } }] }
```

```json
{ "id": "picture", "content": { "kind": "scene_ref", "assetId": "gate", "fit": "none" },
  "transform": { "anchor": [0, 0], "position": [240, 0] },
  "looks": [{ "look": "analog_film_finish", "params": { "grain": 0.45, "grainSize": 2, "dust": 0.18, "vignette": 0.3, "tint": "#e8a86a", "tintAmount": 0.16 } }] }
```

Keep the blur and the glow on the adjustment layer. Placed as effects on the same `scene_ref` that carries the
look, they moved the picture about 30 px down and right of the look's grain and wash, which showed as a brown
band along two edges.

## Rates

| Runs at | What |
|---|---|
| held, on threes (`drawn` at `fps` 8 under a 24 fps root, 10 under 30) | characters, hair, cloth, anything drawn |
| root rate | the weave, the grain and dust, the glow, the camera, titles |

A root that travels under a following camera stays continuous, as [cel anime](cel-anime.md#motion-on-threes)
says. Prefer a 24 fps root: it is the film's own rate.

## Motion habits

- **Held poses and few drawings.** A character holds, then moves in a few spaced poses; a talk is the mouth
  alone on a held body; a blink is two drawings.
- **One thing moves at a time** in a quiet shot: the speaker's mouth, then a hair lock, then a hand.
- **Nothing boils**; the grain and the weave are the frame's life.
- **Transitions:** a hard cut, a slow cross-dissolve of the whole picture, a fade to black and an iris on the
  last shot. A dissolve is the film's own, so it is allowed on the picture here. No wipes with shapes, no
  glitches, no zoom blurs.

## Camera

Held. A slow pan along a set wider than the gate, a slow tilt up a tall painting, one slow push in. The camera
never shakes; the weave is not a camera move and stays the same size in every shot.

## Type

A title in a heavy rounded or brush face, cream with a dark brown outline and a flat offset shadow, inside the
4:3 picture and under the film pass. Subtitles are cream with a dark outline at the foot of the 4:3 picture, or
in the lower bar of a vertical frame; they sit above the pass and stay sharp.

## Sound

A soft synth pad with an electric piano or a saxophone line, a little tape hiss under everything, and sparse
effects: steps, a door, wind. The score follows the picture.

## Scene features used

- `analog_film_finish` (look): grain, dust, vignette and the warm wash.
- `glow`, `gaussian_blur`, `adjust` (effects) on one adjustment layer.
- A nested composition `fps` for the held drawings, and `scene_ref` for the three levels.
- A position `expression` with `Vec.v2` for the weave.

Check each name with `picsart_scene_capabilities` (`look:analog_film_finish`, `effect:glow`) before writing it.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. The picture is 4:3 with black bars, and its edge does not move while the picture weaves under it.
2. Grain is visible on a flat area at the size a viewer sees it, and differs on every frame.
3. Only near-white things glow; a mid-tone wall has no haze.
4. No pure white, pure black or neon inside the picture.
5. Eyes and mouths still read after the blur.
6. Drawn things step on threes; the weave and grain do not.

## Build with the tools

1. **Pictures:** quote every batch with `picsart_preflight`, then `picsart_generate` with the settings in
   [Pictures](#pictures-model-and-settings), every later picture with the earlier bases as references.
2. **Characters:** cut as [picture cut-out](picture-cutout.md) says; save each with `picsart_asset_save`.
3. **Scene:** build `drawn` and check it with no pass first, then wrap it in `gate` and the film.
4. **Check:** a `picsart_scene_contact_sheet` across the film, one frame at full size for the grain and the
   faces, and two neighbouring frames for the weave.
5. **Render:** `picsart_scene_export` at full quality. A loop is checked at its seam: the last frame against the
   first should differ no more than two neighbouring frames do.

## Do / don't

- **Do** finish the drawing first and add the pass last, once, over the whole film.
- **Do** keep the same pass numbers in every shot: one film stock for one film.
- **Don't** add scanlines, a colour split, a date stamp or tracking noise: that is [VHS tape](vhs-tape.md).
- **Don't** stack this pass with painted anime's finishing pass.
- **Don't** weave or grain the black bars.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Rate split: drawn pieces on threes in `drawn`; weave, grain, glow, camera and titles at the root rate.
  - A finish belongs to the page: the whole-frame exception; the pass covers the 4:3 picture, titles included,
    and only subtitles stay outside it.
  - Nothing fades: a cross-dissolve and a fade to black of the whole picture are allowed, as film opticals.

## Originality guard

Invent the cast and the places. The frame must not resemble the characters, costumes, hairstyles, mascots,
machines or title lettering of a known anime series or film of the period, or restage a famous opening shot. A
warm, grainy 4:3 cel look is a shared period idea; a copy of one series' heroine or logo is not.

## Proven on

A 3-second loop: one side-view character and one painted street at dusk, both generated from the prompt words
above with no edits, the character cut from its white background. The set drifts slowly with the character over it
for a little parallax and the character breathes, both stepping on threes at 8 drawings a second under a 24 fps
root, inside the 4:3 gate with the weave and the full film pass. The generated set came with a painted paper edge,
which was cropped off: crop to the painted area before placing a set.
