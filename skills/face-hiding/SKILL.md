---
name: face-hiding
description: Hide the faces in a video or photo by blurring or pixelating them. A face-masked gaussian_blur or pixelate follows every face frame by frame and leaves the rest of the picture sharp. Use when asked to hide, blur, pixelate, censor, anonymize or cover someone's face, to blur faces for privacy, or to hide who is in a video. Hiding a face is an effect, not a look.
metadata:
  category: authoring
  version: '1'
  ported-from: hide-faces 1 at 55.75.0
user-invocable: false
---

# Hiding faces

Two treatments hide a face. Both are **effects**, applied with `picsart_scene_apply_preset`; no look
does this, and none is needed. Never answer that nothing is made for hiding a face.

| Treatment | Preset | What the viewer sees |
|---|---|---|
| **Blur** | `effect:gaussian_blur` with a face mask | a soft, unreadable face |
| **Pixelate** | `effect:pixelate` with a face mask | the mosaic used to censor faces on TV |

**When the request names no treatment** ("hide her face", "cover her face", "make him
anonymous"), ask before applying anything: suggest blur and pixelate, in that order, in one short
message, then apply the one the user picks.

**When the request names one, apply it without asking:** "blur" is the blur; "pixelate" or
"mosaic" is the pixelation.

## Blur or pixelate the faces

Put the effect on the media layer and confine it with a `portrait` / `face_skin` mask. The mask
finds every face in each frame, so on a video the effect follows the faces as they move, and the
hair, body and background stay sharp:

```json
picsart_scene_apply_preset({
  "scene": ..., "layerId": "clip", "preset": "effect:gaussian_blur",
  "params": { "blur": 60 },
  "mask": { "provider": "portrait", "segments": ["face_skin"] }
})
```

```json
picsart_scene_apply_preset({
  "scene": ..., "layerId": "clip", "preset": "effect:pixelate",
  "params": { "pixelSize": 40 },
  "mask": { "provider": "portrait", "segments": ["face_skin"] }
})
```

Set the strength from the size of the faces, not a fixed number:

- **`blur`** about a tenth of the face's width in composition pixels. A face 600 px wide needs
  about 60; at 40 its eyes and mouth still show through. Small faces in a group shot need 20-30.
- **`pixelSize`** about a twelfth of the face's width: 40 for a face 600 px wide.

For an export, any value is fine. For live playback, a blur past 32 costs frame time on a
full-frame video, so prefer `pixelate` there.

## What the mask covers

- **Every face in the layer.** The detector does not tell people apart, so there is no way to hide
  one person's face and keep another's. When the request points at one person ("her face", "the
  man on the left") and the frames show more than one face, tell the user before exporting that
  every face gets the treatment.
- **The face, not the hair.** To hide more of the person, mask the whole person instead:
  `{ "provider": "scene", "segments": ["person"] }`. `supports.maskProviders` in
  `picsart_scene_capabilities` lists every region and the platforms that produce it.
- **One region per effect.** Applying `gaussian_blur` again replaces the layer's earlier
  `gaussian_blur`, mask included.

## Check the result

Look at two or three moments where the faces are visible, with `picsart_scene_contact_sheet` and
`times`. Look at every face, not only the largest:

- **Each face is unreadable and the rest of the frame is as it was:** the effect works. Export.
- **The whole frame is blurred:** the mask did not resolve, and the effect landed on the whole
  layer. Check that the provider and segment are spelled as `supports.maskProviders` lists them.
- **A face still shows:** it was too small or turned too far away for the detector at that moment.
  Tell the user which shots still show a face.

A masked effect runs the face detector on every frame, so a video export takes noticeably longer
than one without the mask.
