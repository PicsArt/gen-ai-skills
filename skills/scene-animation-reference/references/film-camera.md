# A 2D film camera: pan, push-in, parallax

A pan is a moving parent, a push-in is `camera.zoom`, parallax is depth. With the pivot left at the
centre, the focus stays centred through the zoom and nothing drifts.

1. **Pan.** Put the scenery and the actors under one empty layer, `world`
   (`content: {"kind": "empty"}`), and key its `position` to `[W/2 - focusX, H/2 - focusY]`, where
   `focus` is the composition-space point that should sit at the centre. Key `camera.position` never.
2. **Push-in.** Key `composition.camera.zoom` about the default centre pivot, on the **same times and
   easing** as the pan keys, so the focus stays centred.
3. **Parallax.** A background layer is a child of `world` at `transform.z = -D` with `D = W * 50 / 36`
   (the default `camera.distance`). At that depth it projects at half size and the pan moves it half
   as far; restore its size with `scale [2, 2]` and `anchor [0, 0]` and set `position` to `[-W/2, -H/2]`
   so it reads as authored while the camera sits at the centre. Nearer layers stay at `z = 0` and pan
   at full speed; other depths scale as `D / (D - z)`.
4. **Sky.** A layer that must not move or scale with the camera (sky, sun, clouds) is a root layer with
   `cameraExempt: true`, outside `world`.

The pan is an empty parent moved against the subject (the After Effects null); the push-in is
`camera.zoom` (the `push_in` preset does it). When the subject is a rig walking, key it with
`walk_cycle` and `steps`, and never settle it by hand afterwards: a second writer on the same tracks
is what pops at the stop.

Verify with `picsart_scene_query_layout` at two times: near layers move by the pan, the background
layer by half.
