---
name: realistic-color-grade
description: Make a video's colours look more realistic and natural with the ai_realism look — take the over-processed, plastic, AI-generated look off footage with a gentle grade, a shine correction on skin and light colour grain, and choose its values per video. Use when asked to make video colors more realistic, natural or camera-like, to make AI-generated footage look real, to take the glossy or plastic look off skin, or to add subtle grain for realism.
metadata:
  category: authoring
  version: '1'
user-invocable: false
---

# Colour realism with `ai_realism`

`ai_realism` is the look for "make the colours more realistic". It runs the three passes an
editor does by hand on footage that looks too clean, too saturated or too glossy — typically
AI-generated video:

1. **A gentle grade over the whole frame** — contrast, highlights and saturation pulled down
   slightly, plus an optional white-balance nudge.
2. **A shine correction on skin** — the skin's own hue is sampled every frame inside the
   portrait segmenter's skin matte, only bright skin is keyed, and its saturation, lightness and
   contrast come down, so the plastic, over-lit look goes. White shirts and warm walls are left
   alone.
3. **Light colour grain over the whole frame**, as a camera sensor's.

Every pass is subtle on purpose. If the change is visible at a glance, it is too strong.

## When it fits

- Generated or heavily processed footage: waxy or glossy skin, punchy saturation, crushed
  highlights, no noise at all.
- A request phrased as "more realistic", "more natural", "less AI", "like it was shot on a
  camera", "less plastic".

Not the tool for:

- **A stylised grade** ("cinematic", "vintage", "teal and orange"). Use a LUT grade effect or a
  look such as `duotone`; `picsart_scene_capabilities` lists them.
- **Footage that already looks natural.** The grade and the grain add little and can flatten it.
- **A fix for one colour only** (an over-saturated sky). Use `hsl_secondary` directly, keyed on
  that colour.

## Apply it

Put the look on the **media layer itself** (an image or video layer), in reference mode, with
the values chosen for this video:

```json
picsart_scene_apply_preset({
  "scene": ..., "layerId": "clip", "preset": "look:ai_realism", "mode": "reference",
  "params": { "strength": 1, "skin": 1, "grain": 0.06 }
})
```

Anything left out takes the look's default. `picsart_scene_capabilities({ sections: ["look:ai_realism"] })`
returns every parameter with its range.

## Choose the values for this video

Look at the footage first: `picsart_media_probe` for its resolution, and `picsart_scene_contact_sheet` with `times: [t1, t2, …]` and `resolution` set to the scene's `composition.width` and `composition.height` to see the colour cast, how much skin shine there is and
whether it already has noise.

| Parameter | Default | Change it when |
|---|---|---|
| `strength` | 1 | The grade: highlights and saturation down, contrast barely, so blacks stay deep. Lower (0.4–0.7) for footage that is already soft or low in contrast; 0 skips it. |
| `temperature` | 0 | Negative (to about -0.3) to cool an orange, over-warm render; positive to warm a cold, blue one. Applies even at `strength` 0. |
| `skin` | 1 | The shine correction: bright skin's lightness and saturation down, its texture kept. 1 for glossy AI skin, about 0.5 for a light touch, 0 when nobody is in frame or the skin is already matte. In a dark scene it reaches only the brightest skin, as it should. |
| `skinHue` | 20 | Rarely. The skin's hue is sampled every frame; this is only the fallback when too little skin is visible to sample. |
| `skinHueRange` | 25 | Widen (30–40) when part of the shine stays; narrow (15–20) when lips or a warm background change too. |
| `grain` | 0.08 | 0.05–0.1 is felt rather than seen; from about 0.12 it shows on flat dark areas such as a night sky. Lower for a low-resolution source that will be scaled up (grain is per pixel, so it grows with the scale) and for footage with noise of its own; 0 for none. |

Everything else is fixed inside the look (which tones count as shine, how much the key is
softened). For control over those, see the last section.

## Traps

- **The skin pass needs a person in frame.** With nobody segmented it does nothing, so footage
  without people gets the grade and the grain only.
- **The layer must render its own media.** If the host layer also carries `effects`, or is a
  `scene_ref`, its source is drawn as a nested composition, which is never segmented, so the shine
  correction is skipped. Keep the host's own `effects` empty, and put any other effect on an
  adjustment layer above it.
- **It is a static look.** In a layer's `looks`, list it before any look that moves or pads its
  subject, or validation refuses the order.

## Check the result

Render the same moments with and without the look, each with `picsart_scene_contact_sheet` with `times: [t1, t2, …]` and `resolution` set to the scene's `composition.width` and `composition.height`, using
a frame where a face is large. Then check:

- skin shine is calmer but skin still reads as skin, not grey;
- white clothes, teeth, eyes and warm backgrounds are unchanged;
- the grain is barely visible at full size and does not shimmer as blocks;
- the whole frame has not gone flat. If it has, lower `strength`.

## Beyond the six parameters

The look expands to three effects on the media layer, in order: `adjust` (the grade),
`hsl_secondary` (the shine key and its correction) and `film_grain` (with `color` 1). To tune
what the look fixes — which brightness counts as shine, the key's blur, the grade's balance of
contrast and highlights — detach it with `picsart_scene_resolve_looks`, or `picsart_scene_apply_preset` with
`mode: "expand"`, and edit those effects. Their parameters are in `picsart_scene_capabilities`. Each
works alone too: `film_grain` with `color` 1 for grain only, `hsl_secondary` for any one colour.
