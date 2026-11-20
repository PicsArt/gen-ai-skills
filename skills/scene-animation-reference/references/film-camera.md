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

**Build the place once, shoot copies of it.** `picsart_scene_build_place` (`svg`, `travel`) does the band math above for
you. Draw the place as one SVG of top-level `<g id>` bands: `far` (depth -1), `mid` (-0.5), `ground` (0)
and `front` (0.25), in multiples of `D`; any band may state its own `data-depth` below 1, and `sky` stays
fixed to the frame. A nested `<g id>` with `data-hinge="x,y"` is a part that turns on that hinge (a shelf,
a door, a jar on the shelf), and the ground band states `data-floor="y"`, the line characters stand on.
Pass `travel` (`{x, y, zoom}`: the world pan each way and the furthest zoom) and plates drawn to a frame
edge are grown to cover that move. It returns the place scene (its `duration` a parameter, a `floor`
socket on the ground band), the bands, the parts and their hinges, and `travel`: the pan the art allows.
Save the place; every shot starts from a copy of it, `picsart_scene_apply_template` with `template` (the
saved scene), mode `bootstrap` and `parameters: {"duration": <the shot's>}`. Put the cast on the floor
socket, key `world` for the pan (inside the allowed travel) and `push_in` with `start` and `duration`
for the push. A part's knock settles with `settle` `{amplitude: 0.15, decay: 3, frequency: 2.5}` on
its `rotation`: the catalog default barely moves a part (0.5° after a 3.5° knock).

Draw a mid-band object to end below the floor's top edge: the ground band paints over the mid band,
so an object ending on the floor line shows its base sliding against the floor as the camera pans.

Check each shot in `picsart_scene_lint_layout`: `{"kind": "bleed", "members": [{"id": "far"}, ...]}` holds every
plate past the frame edges it bleeds at the first sample (four edges: it covers the frame) at every
sample, so no band shows a cut edge; and `{"kind": "order", "axis": "paint", "members": [front piece,
character, ground]}` holds the paint stack front to back (on `axis: "depth"` a character and the ground
tie at `z = 0` and pass whatever paints first). Scenery drawn past the frame is listed neither as
mostly off canvas nor in `edgeCut`; the front piece's overlap with the ground stays a collision marked
`depthStacked`, intended.
