# Cinematography

For live action and photoreal work, where the reader expects the clip to obey the grammar of a
camera. Generators respond well to this vocabulary because it is heavily represented in what
they were trained on: naming a real setup gets you closer than describing a feeling.

## Motivate the movement

A camera move should have a reason, and the reason changes which move to use. Unmotivated
movement is the most common thing that makes generated footage feel wrong even when nothing is
visibly broken.

| intent | move |
|---|---|
| Realisation, dawning understanding | Slow push-in on a face |
| Revealing context the subject cannot see | Pull back, or crane up |
| Scale, grandeur | Low angle, slow crane up |
| Unease, instability | Handheld with slight sway |
| Objectivity, observation | Locked-off, no movement at all |
| Showing an object's form | Orbit, one quarter turn or less |
| Following action | Tracking shot, matched to the subject's speed |

**A dolly and a zoom are not the same thing.** A dolly moves the camera and the perspective
changes; a zoom changes the focal length and it does not. If you want the world to feel like it
opens up, dolly. Naming `zoom` when you mean `push-in` is a frequent error and generators do
distinguish them.

One move per shot. Two moves at once is how you get the wandering, seasick look.

## Lens language

Focal length is doing two things at once: how much fits in frame, and how the depth is
compressed. The second is what people feel without naming it.

| focal length | what it does |
|---|---|
| 18 to 24mm | Wide. Bends space at the edges, exaggerates depth, feels immediate and slightly aggressive on a face |
| 35mm | Reportage. A person plus their context, honest and undramatic |
| 50mm | Roughly human perspective. Neutral and easy to overlook |
| 85mm | Portrait. Flatters a face, compresses features gently, background falls away |
| 100mm and up | Compresses hard, isolates, flattens layers into planes. Good for a face in a crowd |

Only name a focal length when the style is photographic. A flat vector cartoon has no lens, and
asking for 35mm gets you nothing or gets you photographic artefacts you did not want.

Depth of field pairs with it: `85mm, shallow depth of field at f/1.8` is a complete optical
description and a generator will honour it.

## Lighting setups worth naming

Naming a real setup is far more effective than naming a mood, because a setup determines where
every shadow falls.

| setup | how it reads |
|---|---|
| Three point, soft key | Neutral, professional, safe |
| Single hard key, no fill | Dramatic, high contrast, deep shadow on the far side |
| Rembrandt, key at forty-five degrees and above | Classic portrait, small triangle of light under the far eye |
| Butterfly, key straight above and in front | Beauty, symmetrical, small shadow under the nose |
| Split, key at ninety degrees | Half the face lit, half dark. Conflict |
| Backlit into silhouette | Shape without detail. Mystery, or anonymity |
| Practical motivated, lamps in frame | Naturalistic, grounded, the light has a source you can see |
| Golden hour, low and warm | Nostalgia, warmth, long shadows |
| Overcast, large soft source | Even, flat, documentary |
| Low key, mostly shadow with a rim | Noir, threat |

Say the direction and the hardness, not just the word. `Single hard key from camera left, sharp
shadow edge on the far cheek, no fill` is unambiguous. `Dramatic lighting` is not.

## Grades that mean something

- **Teal and orange**: warm skin against cool shadows. Contemporary studio blockbuster.
- **Bleach bypass**: desaturated, high contrast, crushed silver. Grit, war, industry.
- **Day for night**: underexposed with a cool cast and a hard rim. Reads as night without losing detail.
- **Bleak desaturation**: nearly monochrome with one colour surviving. Dread.
- **Warm film emulation with grain**: nostalgia, period, memory.
- **Clean natural colour**: documentary, honesty, the absence of a look.

Whatever you pick, reuse the exact phrase across every shot in a sequence. This is the single
biggest cause of shots that will not cut together.

## Continuity across shots

Generated shots do not know about each other, so continuity is entirely on the prompt.

- Repeat the style, grade and lighting lines **byte identically** in every shot.
- Keep **screen direction** consistent. A subject moving left to right in one shot should not
  move right to left in the next unless something turned them.
- Keep the **light direction** consistent within a scene. Key from camera left in shot one and
  camera right in shot two reads as two different places.
- Watch **eyelines**. Two people talking should look towards each other, which means opposite
  sides of frame in their respective singles.
- Do not cross the line. If shot one has A on the left and B on the right, keep the camera on
  one side of them for the rest of the scene.

## Shot progression

If you have more than one shot, the sequence should have a shape. The reliable pattern is
**wide, then medium, then close**: establish where we are, then who, then what they feel. Cutting
straight to a close-up gives the viewer nothing to hold on to.

For a reveal, invert it: close on a detail, then pull back to show what it belongs to.

## What fails

| symptom | cause |
|---|---|
| Feels floaty and aimless | Movement unmotivated, or no movement named so the model invented drift |
| Looks like a photograph that happens to move | No subject motion named |
| Shots do not cut together | Style and grade paraphrased instead of repeated |
| Space feels wrong | Two camera moves at once, or a focal length fighting the framing |
| Faces look odd on wide shots | Wide lens close to a face. Move to 85mm or back the camera off |
| Night looks like grey day | Day for night not named, no rim, no colour shift |

## Fragments

- `Slow push-in on the face, ending at a medium close-up, motivated by the realisation.`
- `Locked-off wide, observational, no camera movement at all.`
- `Handheld with slight sway, documentary, the operator following rather than leading.`
- `85mm, shallow depth of field at f/1.8, the background rendered as soft bokeh.`
- `Single hard key from camera left, sharp shadow edge on the far cheek, no fill.`
- `Practical motivated: a desk lamp in frame is the only source, warm and falling off quickly.`
- `Teal and orange grade, warm skin against cool shadows, fine 35mm grain.`
- `Day for night, underexposed and cool, a hard rim separating the subject from the dark.`
- `Wide establishing shot, then a medium, then a close-up, in that order.`
