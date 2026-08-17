# Exclusions

Never ship a video prompt without one. Write it as a single sentence beginning with No, and include only what is plausible for this shot: a long list of irrelevant prohibitions wastes the model's attention.

## Text and branding

text, logos, subtitles, watermark, watermarks, captions, on-screen text, text on screen

## Anatomy and faces

extra limbs, distorted faces, extra characters, hands, extra fingers, extra animals

## Content and safety

violence, scary imagery, scary elements, weapons

## Audio

music, narration

## Other

dialogue, copyrighted characters, talking, cuts, horror, humans, clothes, flickering, frightening imagery, morphing, camera shake, zoom

## Whole lines that work

- `color drift, photorealism, 3D render, lip-sync, captions, on-screen text, logos, watermark`
- `color, gray midtones, photorealism, 3D render, lip-sync, captions, on-screen text, logos, watermark`
- `non-photorealistic, illustrated, not a photo, no live-action, no realism`
- `no voice, dialogue, or narration`
- `camera locked, no camera movement, no zoom, subject stays fully in frame, plain static background`
- `the character performs ONLY this action, nothing else happens`
- `the <prop> stays inert and is never used , no firing, no muzzle flash, no swinging, no raising it`
- `the subject keeps facing the SAME direction for the entire video , never turns around, never rotates toward or away from the camera, no head turns past the shoulder`
- `no cuts, no camera shake, slow steady motion only, locked exposure, no on-screen text`
- `Subtle camera push-in, no flicker, no extra text, no new objects.`

## Phrase it positively instead

Many video models expose no separate negative field, so a prohibition inside the prompt can act as a mention and pull the thing you banned into frame. Use exclusions for artefacts a model adds by habit, such as text and watermarks. Use positive phrasing for anything that is a physical part of the scene.

| instead of | write |
|---|---|
| no blur | tack sharp throughout |
| no people | uninhabited, empty of figures |
| no camera shake | locked-off tripod, perfectly still |
| no clutter | a single object on an empty surface |
| no text | clean surfaces, unmarked |
