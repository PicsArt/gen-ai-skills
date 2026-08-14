# Cartoon and animation

For animated work, where camera language mostly does not apply and a different vocabulary does.
The most common mistake is writing an animation prompt as though it were live action: asking for
an 85mm lens and shallow depth of field on a flat cel-shaded cartoon fights the style and
usually produces a photographic hybrid nobody wanted.

**Drop the optics. Name the drawing.**

## Establish the technique first

Everything else reads differently depending on this, so it goes early in the prompt.

| technique | what to say |
|---|---|
| Cel shaded 2D | Flat fills, two-tone shading, visible outlines |
| Painted 2D | No outlines, soft edges, brushwork visible |
| Cutout or limited | Flat shapes, hinged joints, sliding rather than redrawing |
| 3D rendered, stylised | Simplified forms, soft global light, no photographic lens |
| 3D rendered, photoreal | Then use `references/cinematography.md` instead, the camera language applies |
| Stop motion | Visible material, tiny imperfections, slight frame judder |
| Pixel art | Fixed grid, limited palette, no anti-aliasing |
| Rotoscoped | Traced over live action, so the motion is naturalistic and the drawing is not |

## Line and fill

The details that decide whether it reads as a real production or as generated:

- **Outline colour.** Assume black and you will usually be wrong. Most productions use a dark
  brown, a dark shade of the fill colour, or no outline at all. State it.
- **Outline weight.** Even, or tapering. Whether it varies between character and background,
  which it usually does.
- **Shading steps.** Two-tone cel, three-tone, or soft gradient. This single choice moves a
  drawing between decades of animation history.
- **Where detail lives.** Almost always faces and silhouette edges, almost never interiors.
- **Background versus character.** Very often a painted background with cel characters over it.
  Say so if that is the look, because a model will otherwise render both the same way.

## Motion, in animation terms

Animation motion is not a slower or faster version of live action. It has its own vocabulary and
generators respond to it.

| term | what it asks for |
|---|---|
| On ones | A new drawing every frame. Fluid, expensive, used for fast action |
| On twos | A drawing every second frame. The standard look for most 2D |
| On threes or fours | Choppier, deliberate, retro or low budget |
| Held pose | The drawing does not change at all for a beat. Very common and rarely asked for |
| Anticipation | A small movement opposite to the main one, just before it |
| Squash and stretch | Deformation on impact and acceleration. Cartoon physics |
| Follow through | Hair, cloth and ears keep moving after the body stops |
| Overshoot and settle | The pose goes slightly past its target and comes back |
| Smear | One stretched drawing bridging a fast move |
| Motion lines | Drawn streaks indicating speed, rather than blur |

**Held poses are the thing to ask for.** Generated animation drifts continuously because nothing
told it to stop. `The pose holds completely still for a beat, then the head turns` produces
something that reads as animation rather than as a morphing video.

## Camera in animation

There is a camera, but it works differently.

- Moves are usually **simple and orthogonal**: a pan across a background, a push in on a held
  drawing, a shake for impact.
- **Parallax** rather than perspective: layers sliding at different speeds across a flat scene.
- No depth of field unless the production uses it deliberately, and then it is a graded blur on
  a whole layer rather than an optical falloff.
- No lens distortion, no flare, no chromatic aberration, unless the style is deliberately
  imitating a camera.

Say `flat, no lens effects` when you want to keep photographic artefacts out.

## Characters across shots

The hardest problem in generated animation is a character who stays the same character.

- Repeat the character description **byte identically** in every shot. Height, proportion, hair,
  wardrobe, palette, in the same words.
- Anchor the eye construction, which is the strongest identity cue: size, whether sclera shows,
  the highlight.
- Keep the number of characters low. Each additional character multiplies the drift.
- If a style guide exists, take the character description from its `<guide>/characters.md` verbatim and
  do not paraphrase it. See `style-guide-builder`.

## What fails

| symptom | cause |
|---|---|
| The character morphs continuously | No held poses, and the description varies between shots |
| It looks like video, not animation | On ones by default with no held beats. Ask for twos and holds |
| Line weight changes shot to shot | Outline treatment not specified, or paraphrased |
| Outlines came back black | Outline colour not stated |
| Photographic artefacts appeared | A lens or depth of field was named on a flat style |
| Background and character look like one thing | The painted background versus cel character split not stated |
| Faces drift between shots | Eye construction not anchored |
| Movement is mushy | No anticipation, no overshoot, no settle. Everything eased evenly |

## Fragments

- `Cel shaded 2D animation, flat fills, two-tone shading, dark brown outlines of even weight.`
- `Animated on twos, with the pose holding completely still for a beat before the action.`
- `Squash on impact and a slight overshoot as the pose settles.`
- `Follow through on the hair and the coat after the body stops.`
- `Painted watercolour background, cel shaded characters over it, no outline on the background.`
- `Simple horizontal pan across the background, layers sliding at different speeds for parallax.`
- `Flat, no lens effects, no depth of field, no flare.`
- `Detail on the face and the silhouette edge only, interiors left as flat colour.`
- `Smear frame bridging the fast turn, then a clean held pose.`

## Exclusions

`No photographic depth of field, no lens flare, no chromatic aberration, no changes to the
character design, no black outlines, no text, no watermarks.`

Two of those are worth keeping even when they seem obvious. `No black outlines` matters because
a model will default to them, and `no changes to the character design` because that is the
failure that ruins a sequence rather than a single shot.
