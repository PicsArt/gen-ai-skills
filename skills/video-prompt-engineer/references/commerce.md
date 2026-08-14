# Ecommerce and marketing

Commercial video has a constraint the rest of this skill does not: **the product has to stay
the product.** A cinematic clip that invents a detail is interesting. A product clip that
invents a detail is unusable, and often legally unusable.

So the governing rule for everything on this page:

> Prefer an image-to-video route from a real product photograph over text-to-video. The model
> then has the geometry, the label and the colour, and only has to move. Asking a text-to-video
> model to invent your product and then animate it will produce something that resembles it.

When you write for image-to-video, **do not redescribe the frame.** The model has it. Prompt
motion, light change and camera only. Redescribing the product is how you invite it to redraw
the product.

## Brand assets fail first

Logos, labels, badges, embroidered marks and printed text are the first things a generator
destroys, because they are fine geometry and text, and text is what these models are worst at.

Assume any lettering in frame will degrade over a clip. Three ways out, in order of
reliability:

1. **Composite the logo afterwards.** Generate the motion clean, add the mark in post. This is
   what most production actually does and it is the only reliable answer.
2. **Keep the mark small and briefly seen.** Damage is proportional to how long and how large.
3. **Hold the mark still.** A logo on a surface that does not move survives far better than one
   on a rotating or deforming surface.

State it in the prompt either way: `the printed label stays sharp and unchanged throughout`
works better than saying nothing, and pairs with a post composite.

## Product animation

Animating a still product shot. The most common commercial request there is.

**Specify**: what moves and what does not, camera movement, how long, where the light travels.
**Keep short.** Four to six seconds. Drift grows with duration, and a product only needs one
gesture.

Prefer moving the **camera** over moving the **product**. A camera orbit around a still bottle
is far more reliable than a bottle rotating in place, because the object never has to be
re-drawn from an angle the reference never showed.

When the product itself must move, name one mechanical action and its limit: `the lid hinges
open to forty-five degrees and stops`.

**Fragments**

- `Slow orbit around the product, one quarter turn, the product itself perfectly still.`
- `Locked-off camera. A single specular highlight travels across the brushed metal from left to right.`
- `Slow push-in from a medium shot to a tight detail on the texture, ending before the edge of frame.`
- `The lid hinges open to forty-five degrees and stops. Nothing else in the frame moves.`
- `Condensation beads form and one drop runs down the side of the glass.`
- `The fabric settles as though just placed, then holds completely still.`

**Exclusions**: `No warping of the product silhouette, no changes to the label or printed text,
no extra products appearing, no hands, no text, no watermarks.`

## Apparel and garment swap

Two different jobs. Be clear which one you are writing.

**Showing a garment in motion**: name the fabric behaviour, because that is the whole point.
Weight, drape, stiffness, how it moves when the wearer does.

**Swapping a garment onto a model**: the pose, framing and lighting must stay fixed so the
garment is the only variable. Say so explicitly.

**Specify**: fabric weight and finish, pattern behaviour, seam and hem positions, fit, what the
wearer does, and that the pose is held.

**What fails**: pattern drift across a moving surface, stripes bending the wrong way around a
body, logos on chests warping, hems and cuffs dissolving, the garment merging into the
background at the silhouette, sleeve length changing mid-clip.

Patterns are the worst of these. A regular stripe or check on a moving garment is fine geometry
in motion, which is the same problem as text. Prefer plain or irregular fabrics for generated
motion, and say `the check pattern stays aligned to the weave and does not distort` when you
cannot.

**Fragments**

- `Heavy weight cotton, holding a soft fold, moving slowly and settling.`
- `Liquid silk with a high sheen, catching light along each fold as it moves.`
- `Structured wool that keeps its shape, minimal drape, the shoulder line holding.`
- `The model holds the pose exactly. Only the fabric moves.`
- `Identical pose, framing and lighting. Only the garment changes.`
- `The check pattern stays aligned to the weave and does not distort at the seams.`

**Exclusions**: `No changes to the garment pattern, seams, hem or fit, no logo distortion, no
extra limbs, no warped hands, no text.`

## Changing the model

Producing the same commercial frame with models of different skin tones, ages or body types.
Standard adaptive and localised creative practice, and there are three things to get right.

### Keep everything else identical

The garment, pose, framing, background and camera stay the same, and the prompt should say so
in those words. If the pose shifts between versions, the set stops being a comparison and
becomes unusable as a campaign.

### Light for the skin

This is a real production concern and not a courtesy. Darker skin needs more light and a
different key-to-fill ratio to hold detail, and it needs a separating rim or the subject flattens
against a dark background. Lighter skin blows out sooner and needs the key pulled back. A single
lighting description reused across every skin tone will underexpose some versions and overexpose
others, which is exactly the failure that makes these sets look careless.

Name it: `exposed for the subject's skin, with a rim light separating them from the background`.

### Language and rights

- Describe appearance in **plain, neutral, physical terms**. Skin tone, hair texture, age range,
  build. No ethnic shorthand standing in for a look, and no stereotyped wardrobe, setting or
  expression travelling along with the change.
- **Do not generate a likeness of an identifiable real person.** If the user asks for one, say
  plainly that it needs their permission and is a rights question, not a prompt question.
- Many ad platforms now require **disclosure of synthetic media**, and some restrict synthetic
  humans in regulated categories such as health and finance. Flag it once when the work is an
  ad; it is the user's call, but it should be a decision rather than a surprise.

**Fragments**

- `Identical pose, garment, framing and background. The model has deep brown skin and short natural hair.`
- `Exposed for the subject's skin, with a soft rim light separating them from the background.`
- `Mid forties, medium build, light olive skin, grey at the temples. Same wardrobe and pose as the reference.`
- `Neutral confident expression, looking just off lens.`

**Exclusions**: `No change to pose, garment or background, no extra limbs, no distorted faces,
no warped hands, no text.`

## Jewellery and small reflective goods

The hardest commercial category, because the product is mostly specular reflection and fine
geometry, both of which generators approximate.

**Specify**: macro framing, where the light is and how hard, that the stone stays faceted, that
the metal reads as metal, prong and setting count if it is visible, and a very slow movement.

**What fails**: gems turning into glowing blobs, facets smoothing over, prong count changing,
chain links merging, engraving dissolving, metal reading as plastic because the reflection is
diffuse rather than sharp.

Keep it slower and shorter than any other category. Three to five seconds. Every extra second
is another opportunity to lose a facet.

**Fragments**

- `Macro on the setting, the stone filling a third of frame, facets sharp and individually readable.`
- `Two hard sources at forty-five degrees, so the metal shows a bright specular line and a dark side.`
- `Extremely slow rotation, a few degrees only, the light moving across the facets.`
- `Polished yellow gold with a mirror finish, reflecting the room rather than glowing.`
- `The prong setting holds four visible prongs throughout.`

**Exclusions**: `No change to the stone shape or facet pattern, no change to the setting, no
glowing or emissive gems, no plastic-looking metal, no hands, no text.`

## Vehicles

**Specify**: a turntable or orbit rather than the car driving, the surface it stands on and what
it reflects, wheel behaviour, whether badges are in frame, and the light source shape, because
a car body is a giant mirror and reads entirely through what it reflects.

The reflection is the shot. A car lit by a large soft source shows a long clean gradient down
the flank; a car lit by points shows blobs and looks synthetic.

**What fails**: wheels rotating at a speed inconsistent with the car's movement or wobbling on
their axis, badges and grille patterns morphing, body proportions shifting through a rotation,
reflections that do not match the environment, a panel gap appearing or closing.

For a showroom rotation, favour **camera orbit with the car static**, for the same reason as the
product: nothing has to be re-drawn.

**Fragments**

- `Slow camera orbit around a static car on a polished showroom floor, one eighth turn.`
- `Large soft overhead source, its reflection reading as one long highlight down the flank.`
- `The floor reflects the car faintly, the reflection matching the body exactly.`
- `Wheels stationary, the car parked. Only the camera moves.`
- `Badge and grille stay sharp and unchanged throughout.`

**Exclusions**: `No change to the body shape or panel lines, no badge or grille distortion, no
wheel wobble, no motion of the car itself, no people, no text.`

## Before you finish a commercial prompt

- **Which platform is it for.** Ask, because it changes the framing. Every feed platform draws
  its own interface over the video: a caption and a row of action buttons, usually along the
  bottom and the right side. Anything important placed there is covered by the app, and you
  cannot see that in the file you generated. Until the per-platform measurements are added
  here, use the safe habit: keep the subject and any text well inside the centre of the frame,
  leave the bottom third and the right edge clear of anything that has to be read, and check
  the result in the app itself before signing it off.
- **Does it survive a second crop.** A vertical clip is often shown as a square or a 4:5
  thumbnail elsewhere in the same app, so a composition that only works at 9:16 will be cut.
- Is there a first frame worth stopping on, since that frame is the thumbnail.
- Does it read with the sound off, which is how most feed video is watched.
- Is there empty space where a price, a claim or a call to action has to sit.
- If the clip carries a claim about the product, say once that generated footage should not be
  the evidence for a factual claim.
