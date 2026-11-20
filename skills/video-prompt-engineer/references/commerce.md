# Ecommerce and marketing

Commercial video has a constraint the rest of this skill does not: **the product has to stay
the product.** A cinematic clip that invents a detail is interesting. A product clip that
invents a detail is unusable, and often legally unusable.

## Contents

- Brand assets fail first
- Product animation
- Apparel and garment swap
- Changing the model
- Jewellery and small reflective goods
- Vehicles
- Before you finish a commercial prompt

So the governing rule for everything on this page:

> Prefer an image-to-video route from a real product photograph over text-to-video. The model
> then has the geometry, the label and the colour, and only has to move. Asking a text-to-video
> model to invent your product and then animate it will produce something that resembles it.

When you write for image-to-video, **do not redescribe the frame.** The model has it. Prompt
motion, light change and camera only. Redescribing the product is how you invite it to redraw
the product.

## Brand assets fail first

Fine text, logos, labels, badges and patterns can change during generation. Preserve approved assets and inspect them through the whole take. Where exact identity matters, plan tracked compositing from approved artwork as a separate finishing step. Do not hide or remove requested marks to make a shot easier, or claim prompt text guarantees preservation.


## Product animation

Animating a still product shot. The most common commercial request there is.

**Specify**: what moves and what does not, camera movement, how long, where the light travels.
Choose a duration supported by the endpoint and sufficient for the requested action; shorter is not a universal cure. A camera orbit and a rotating product can both expose surfaces absent from a single reference. Use approved multi-view references where supported, reduce the reveal if acceptable, or flag the uncertainty. Keep the requested motion rather than claiming camera travel avoids redrawing geometry.

When the product itself must move, name one mechanical action and its limit: `the lid hinges
open to forty-five degrees and stops`.

**Fragments**

- `Slow orbit around the product, one quarter turn, the product itself perfectly still.`
- `Locked-off camera. A single specular highlight travels across the brushed metal from left to right.`
- `Slow push-in from a medium shot to a tight detail on the texture, ending before the edge of frame.`
- `The lid hinges open to forty-five degrees and stops. Nothing else in the frame moves.`
- `Condensation beads form and one drop runs down the side of the glass.`
- `The fabric settles as though just placed, then holds completely still.`

**Possible constraints (only when compatible with the brief and model)**: `No warping of the product silhouette, no changes to the label or printed text,
no extra products appearing, preserve approved hands and markings.`

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

**Possible constraints (only when compatible with the brief and model)**: `No changes to the garment pattern, seams, hem or fit, no logo distortion, no
extra limbs, preserve approved hands and markings.`

## Changing the model

Producing the same commercial frame with models of different skin tones, ages or body types.
Standard adaptive and localised creative practice, and there are three things to get right.

### Keep everything else identical

The garment, pose, framing, background and camera stay the same, and the prompt should say so
in those words. If the pose shifts between versions, the set stops being a comparison and
becomes unusable as a campaign.

### Light for the skin

Preserve the reference skin tone and expose for the desired facial detail, highlights and background separation. Do not prescribe more light, a fixed ratio or a mandatory rim by skin-tone category. Evaluate the actual scene, material response and exposure. Treat identity and lighting changes as distinct decisions, and disclose any deviation from a requested controlled comparison.

### Language and rights

- Describe appearance in **plain, neutral, physical terms**. Skin tone, hair texture, age range,
  build. No ethnic shorthand standing in for a look, and no stereotyped wardrobe, setting or
  expression travelling along with the change.
- **Preserve approved identity references.** Do not substitute another person or infer permission for unrelated uses. Address consent, likeness rights and destination requirements when relevant to the requested use; a prompt-only repair does not authorize publication.
- Many ad platforms now require **disclosure of synthetic media**, and some restrict synthetic
  humans in regulated categories such as health and finance. Flag it once when the work is an
  ad; it is the user's call, but it should be a decision rather than a surprise.

**Fragments**

- `Identical pose, garment, framing and background. The model has deep brown skin and short natural hair.`
- `Exposed for the subject's skin, with a soft rim light separating them from the background.`
- `Mid forties, medium build, light olive skin, grey at the temples. Same wardrobe and pose as the reference.`
- `Neutral confident expression, looking just off lens.`

**Possible constraints (only when compatible with the brief and model)**: `No change to pose, garment or background, no extra limbs, no distorted faces,
preserve approved hands and markings.`

## Jewellery and small reflective goods

The hardest commercial category, because the product is mostly specular reflection and fine
geometry, both of which generators approximate.

**Specify**: macro framing, where the light is and how hard, that the stone stays faceted, that
the metal reads as metal, prong and setting count if it is visible, and a very slow movement.

**What fails**: gems turning into glowing blobs, facets smoothing over, prong count changing,
chain links merging, engraving dissolving, metal reading as plastic because the reflection is
diffuse rather than sharp.

Use a pace and duration that make the required detail readable. Inspect facets, setting geometry and reflections; no fixed duration guarantees preservation.

**Fragments**

- `Macro on the setting, the stone filling a third of frame, facets sharp and individually readable.`
- `Two hard sources at forty-five degrees, so the metal shows a bright specular line and a dark side.`
- `Extremely slow rotation, a few degrees only, the light moving across the facets.`
- `Polished yellow gold with a mirror finish, reflecting the room rather than glowing.`
- `The prong setting holds four visible prongs throughout.`

**Possible constraints (only when compatible with the brief and model)**: `No change to the stone shape or facet pattern, no change to the setting, no
glowing or emissive gems, preserve the specified finish and approved markings.`

## Vehicles

**Specify**: a turntable or orbit rather than the car driving, the surface it stands on and what
it reflects, wheel behaviour, whether badges are in frame, and the light source shape, because
a car body is a giant mirror and reads entirely through what it reflects.

The reflection is the shot. A car lit by a large soft source shows a long clean gradient down
the flank; a car lit by points shows blobs and looks synthetic.

**What fails**: wheels rotating at a speed inconsistent with the car's movement or wobbling on
their axis, badges and grille patterns morphing, body proportions shifting through a rotation,
reflections that do not match the environment, a panel gap appearing or closing.

For a showroom view, specify whether the camera or the car moves. Both can reveal unseen geometry; obtain sufficient reference coverage and check every angle.

**Fragments**

- `Slow camera orbit around a static car on a polished showroom floor, one eighth turn.`
- `Large soft overhead source, its reflection reading as one long highlight down the flank.`
- `The floor reflects the car faintly, the reflection matching the body exactly.`
- `Wheels stationary, the car parked. Only the camera moves.`
- `Badge and grille stay sharp and unchanged throughout.`

**Possible constraints (only when compatible with the brief and model)**: `No change to the body shape or panel lines, no badge or grille distortion, no
wheel wobble, preserve the specified car motion, people and markings.`

## Before you finish a commercial prompt

- **Which platform is it for.** Preserve the selected format and consult current official placement specifications when safe-zone measurements are needed. Do not assume a universal bottom-third or centred safe area; overlays vary by placement. Test the actual crop and UI.
- **Does it survive a second crop.** A vertical clip is often shown as a square or a 4:5
  thumbnail elsewhere in the same app, so a composition that only works at 9:16 will be cut.
- Is there a first frame worth stopping on, since that frame is the thumbnail.
- Does it read with the sound off, which is how most feed video is watched.
- Is there empty space where a price, a claim or a call to action has to sit.
- If the clip carries a claim about the product, say once that generated footage should not be
  the evidence for a factual claim.
