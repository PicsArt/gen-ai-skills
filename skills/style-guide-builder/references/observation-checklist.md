# Observation checklist

What to look at in each reference, and what each observation lets you conclude. Work the
aspects in this order: earlier ones constrain later ones, and a palette read before you have
established the medium will mislead you.

Record observations per image first. Synthesise afterwards. If you synthesise while looking,
you will remember the last three frames and call them the style.

## 1. Medium and rendering

The first thing to settle, because everything else is read differently depending on it.

| look at | conclude |
|---|---|
| Edge quality: is a shape bounded by a line, a colour change, or a soft gradient | Outlined cartoon, painterly, or 3D render |
| Line weight, and whether it varies along its length | Hand drawn versus vector versus digital brush |
| Line colour: black, dark brown, a darker shade of the fill, or none | A style signature, and one of the easiest to get wrong |
| Fill: flat, gradient, textured, hatched | Cel shaded versus painted versus print |
| Visible medium artefacts: paper grain, canvas, halftone, film grain, aliasing | Traditional, print, or digital, and whether grain must be added later |
| Shading: none, two-tone cel, soft airbrush, full form modelling | The single biggest driver of how "cartoon" it reads |
| Specular highlights: absent, single dot, full physical | Flat illustration versus 3D |
| Detail density: how much information per unit area, and whether it is even | Whether a generated image should be busy or sparse |
| Where detail concentrates | Almost always faces and silhouette edges. Say so if true |

## 2. Palette

Read after the medium, because a textured medium will fool a naive colour sample.

| look at | conclude |
|---|---|
| The four to eight colours doing the most work, with hex | The observed palette |
| How many distinct hues, and their spacing on the wheel | Whether the palette is analogous, complementary or scattered |
| Saturation range: the lowest and highest, not the average | The band a new colour must sit in |
| Value range: are there true blacks and true whites, or is it compressed | Contrast character |
| Shadow colour: neutral grey, the same hue darkened, or shifted towards blue or purple | A rule that generalises to every new object |
| Highlight colour: white, or tinted by the light | As above |
| Skin, if present: hue and how far it varies between characters | Whether skin is stylised or naturalistic |
| Background versus foreground saturation | Whether depth is done with colour or with value |
| Any colour used only for emphasis | An accent rule worth stating |

**Always record ranges, never averages.** The average of a two-colour palette is a colour that
appears nowhere in the references.

## 3. Lighting

| look at | conclude |
|---|---|
| Direction: where shadows fall, so where the key must be | The default setup |
| Hardness: shadow edge sharp or soft | Small source versus large source |
| Fill: how dark the darkest shadow is | Contrast, and whether shadows hold detail |
| Light colour: warm, cool, or white | Time of day and mood |
| Rim or back light: is there a separating edge | A very common cartoon signature |
| Ambient occlusion: contact shadows where objects meet | Whether the style grounds objects or floats them |
| Practical sources in frame: lamps, windows, screens | Whether light is motivated |
| Consistency across frames | One setup, or per-scene lighting |

## 4. Camera

Read only what the image supports. Much of this is unknowable from a single frame, and saying
so is better than guessing.

| look at | conclude |
|---|---|
| Shot size relative to the subject | The framing habit of the set |
| Angle: eye level, low, high, overhead | Whether the style has a point of view |
| Perspective strength: converging lines, distortion at edges | Approximate focal length. Wide, normal, long |
| Depth of field: is the background sharp | Whether to name shallow depth of field in prompts |
| Horizon placement and headroom | Composition habit |
| Aspect ratio | Only if all references agree |
| Lens artefacts: flare, chromatic aberration, vignette | Whether the style pretends to be photographic |

If the references are illustration with no photographic cues, **say that camera language does
not apply** rather than inventing a focal length. A guide that specifies 35mm for a flat vector
style will produce worse results, not better.

## 5. Subjects

Per recurring character, creature or object class.

| look at | conclude |
|---|---|
| Proportion: head to body ratio, limb length | The construction rule |
| Eyes: size, shape, sclera visible, highlight, pupil style | The strongest single style tell in character work |
| Mouth and nose: drawn, implied, or absent at rest | As above |
| Hands: fingered, mitten, hidden | Worth recording because hands are where generation fails |
| Hair or fur: strand, clump, or mass with edge detail | The surface rule that generalises to other creatures |
| Clothing: fold count, how fabric is shaded | Whether to ask for simple or complex garments |
| Silhouette readability | Whether the style depends on clear silhouettes |
| Outline treatment on subjects versus background | Often different, and often unnoticed |

## 6. Environments

| look at | conclude |
|---|---|
| How a tree is constructed: trunk, mass, leaf detail, silhouette | The rule that gives you bushes, grass and crops |
| Grass: individual blades, mass with edge marks, or flat colour | Detail floor for ground cover |
| Sky: flat, gradient, clouds, and how clouds are drawn | A large area of any wide shot |
| Water: reflection, transparency, edge treatment | |
| Architecture: line straightness, perspective rigour, window and door treatment | |
| Background simplification: how much less detail than the foreground | Depth rule |
| Crowds: are distant figures shapes, silhouettes or fully drawn | Crowd rule |
| Props: recurring objects, and how much detail each carries | |

## 7. Motion, only for sequential references

Only when the references are frames from moving footage, or a sequence.

| look at | conclude |
|---|---|
| Motion blur: present, and on subject or camera | Whether to request it |
| Held poses versus continuous movement | Animation on twos, or fluid |
| Smear frames or squash and stretch | Cartoon physics or naturalistic |
| Camera movement inferable across frames | What movement to name in a video prompt |
| Cut rhythm, if the frames are consecutive | Pacing |

## 8. Anomalies

Note per image anything that differs from the rest of the set. Anomalies are how you find the
boundary of the style, and sometimes they reveal that the user has handed you two styles rather
than one. If that happens, **say so and ask** which they want, or offer to build both. Do not
average two styles together: the result belongs to neither.
