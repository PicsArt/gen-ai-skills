---
name: quick-merge-and-export
description: The shortest path from media URLs to a rendered file - merge or concatenate several videos into one with the montage template, sample frames from a scene into a contact sheet, and export any valid scene to a file. Use when asked to merge, join or concatenate clips, to preview a scene as frames, or to render a scene, and no other skill covers the job.
metadata:
  category: authoring
  version: '1'
user-invocable: false
---

# Scene quickstart

Three short jobs, each a fixed chain of tools. Every tool takes media by URL. None reads a local
path, a `file://` URI or inlined file bytes, and such a source is refused before anything renders.
For a file the user has only on their device, call `picsart_drive_upload_ask`: it opens a
drag-and-drop upload. The call itself returns no URL; the file's URL arrives on the user's next
turn, as widget context (or in their message), so read it there before going on. Pass `detected_files` when you can see the file
name, and `known_urls` to offer URLs already made in this conversation.

## Merge several videos into one

The montage template plays its clips one after another and renders one file.

1. **Probe each clip.** Call `picsart_media_probe` once per clip URL for its width, height
   and duration. Skip a clip whose exact size and duration an earlier tool result already gave. A
   missing `durationSeconds` means the duration is unknown, not zero: follow the probe's own note
   on that field.
2. **Build the parameters.** Write the clips as JSON, one object per clip with `uri`, `width`,
   `height`, `duration` from the probe, and optionally `in` and `out` (the trim, in seconds),
   `fit` (`cover`, `contain` or `fill`) and `align` (one of nine positions such as `top left` or `center`, the default).
   Then run `scripts/montage_params.py`:

   ```bash
   python3 scripts/montage_params.py --transition crossfade --transition-duration 0.4 clips.json
   ```

   It prints the complete `picsart_scene_apply_template` arguments: `uri:
   "scene://montage"`, `mode: "bootstrap"`, and `parameters` with `transition`,
   `transitionDuration` and `clips`. Omit `--width` and `--height`: the canvas matches the largest
   clip and the frame rate follows the clips. Pass both only to deliberately change the aspect
   or size. For a smaller output file, use `picsart_scene_export`'s `resolution`. Pass
   `--transition ""` for a hard cut. Use `fit` and `align` when a clip's shape differs from the
   output's, as with portrait and landscape clips in one montage.

   **Without a shell, write the script's output yourself.** The template's clips do not take the
   input shape above. Each clip becomes `duration` (`out` minus `in`) plus a `content` object
   that carries the probed asset, the trim, `fit` and `align`. A hard cut is `transition: ""` with
   `transitionDuration: 0`. Here clip 1 is trimmed to 0–4 s of a 12 s clip, then a hard cut to
   all 8 s of clip 2:

   ```json
   {"uri": "scene://montage", "mode": "bootstrap", "parameters": {
     "transition": "", "transitionDuration": 0,
     "clips": [
       {"duration": 4, "content": {"kind": "media",
         "asset": {"type": "video", "uri": "https://…/a.mp4", "width": 1080, "height": 1920, "duration": 12},
         "trim": {"in": 0, "out": 4}, "fit": "cover", "align": "center"}},
       {"duration": 8, "content": {"kind": "media",
         "asset": {"type": "video", "uri": "https://…/b.mp4", "width": 1080, "height": 1920, "duration": 8},
         "trim": {"in": 0, "out": 8}, "fit": "cover", "align": "center"}}]}}
   ```
3. **Bootstrap the scene.** Call `picsart_scene_apply_template` with those arguments,
   unchanged. These arguments are complete, so this job needs no schema or template lookup. The
   composition's duration is the sum of the clip durations: never set it by hand.
4. **Validate.** Call `picsart_scene_validate` on the returned `scene`.
5. **Render.** Call `picsart_scene_export` with the scene and `mediaType: "mp4"`. It replies with a job
   receipt: follow it as picsart-video-rules says until it reports `urls`, one merged file.

The montage is sequential: each clip starts where the one before it ends. For layers that play at
the same time, as in picture-in-picture, write overlapping layers with
`picsart_scene_patch` instead.

The rendered length is not snapped to the frame grid, so a montage of exact decimal trims can land
a frame or two short of the target. That is expected, not an error.

## Sample frames from a scene

1. Have a valid scene: one a template returned, or one written with `picsart_scene_patch`.
2. Call `picsart_scene_validate` on it.
3. Call `picsart_scene_contact_sheet` with either `times` (exact timestamps) or `frames` (that many
   evenly spaced), never both, and optionally `resolution`. It returns `frames`, each a `time` and
   a `url`: low-resolution previews, not the deliverable.

## Render a scene to a file

1. Have a valid scene, as above. A scene this skill's merge job built needs no other check.
   Otherwise confirm its shape with `picsart_scene_capabilities`, sections `["schemaSummary"]` then `["schema:<Name>"]`, or
   `["template:<uri>"]` for a template.
2. Call `picsart_scene_validate` on it.
3. Call `picsart_scene_export` with `mediaType` (`mp4`, `png` and the others it lists), and
   optionally `resolution`, `fps`, `duration` and `startTime`. Pass `fileName`, a short name from
   the scene's subject, so a file saved to Drive gets a real name. It replies with a job receipt
   by default; follow it as picsart-video-rules says until it reports `urls`.

Export renders on a server and needs a signed-in user. Follow picsart-video-rules's rule on cost before you
call it.
