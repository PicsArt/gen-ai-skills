# Worked examples

How a request turns into a prompt, including what to ask and what to report back.

## From a one-line idea

**In**: "make a video of a watch"

**Ask**:
```
Four things and I can write this:
1. How long? (suggest 8 seconds)
2. Landscape or vertical? (suggest 16:9)
3. Studio product shot, or worn on a wrist? (suggest studio)
4. Does the camera move? (suggest slow orbit)
```

**Out**, after "1 and 2 defaults, studio, yes orbit":

```
8 seconds, 16:9, cinematic photorealistic product film. Extreme close-up on a steel
dive watch on black slate, low angle. Slow orbit around the case, one quarter turn.
100mm macro lens, shallow depth of field, the bezel sharp and the background falling
to bokeh. Single hard key from the upper left with a soft rim behind, brushed metal
catching a moving highlight as the camera travels. Cool desaturated grade, deep
blacks. The second hand sweeps continuously. Restrained and precise. Minimal low
electronic ambience, one soft mechanical click as the highlight peaks. No text,
logos, watermarks, hands, reflections of the crew, or dust.
```

**Assumed**: 8 seconds, 16:9, studio on slate, macro lens.

**Try next**: the same prompt at 15 seconds with a second beat, the crown turning.

## From a defect report

**In**: "there is an extra hand in my video", with their prompt attached.

Diagnose first. An extra limb is almost always a missing anatomy exclusion, and often more people in frame than the duration can hold. Change the minimum:

1. Add the anatomy exclusion.
2. If more than one person is in frame for under ten seconds, say so and offer to reduce to one.
3. Leave the grade, mood and audio alone. They were not the problem.

**Report**: `Added the anatomy exclusion, which was missing. Two people in eight seconds is what produced the third hand, so I also offered a single subject version.`

## From an uninvited object

**In**: "there are objects in the background that I never described".

The background was never described, and an undescribed background is where a model puts whatever it likes. Do not ban the objects: describe the space.

**Change**: add `an empty room, bare walls, uninhabited` rather than `no furniture, no clutter, no people`. The ban can act as a mention.
