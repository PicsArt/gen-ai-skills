# Held drawings: animating on twos

A nested composition (an inline `composition` or a `scene_ref` body) whose `composition.fps` is
LOWER than its host's rate draws on its own frame grid: every host frame shows the start of the
nested frame it falls in. `"fps": 12` inside a 24 fps scene is animation on twos, the stepped look of
hand-drawn animation, without duplicating a keyframe. The hold covers the whole composition:
keyframes, expressions (their `time` is the held one, so a wobble boils on twos), media, Lottie and
nested playback, which of its layers are live and reads between its own layers. A held frame keeps the
motion blur of its own instant. An effect's rolling seed follows the host clock (the grain is the
film, not the drawing), and sound is not held: audio inside plays on the host clock.

```json
{"id": "character", "content": {"kind": "composition",
  "composition": {"width": 1080, "height": 1080, "fps": 12},
  "layers": [{"id": "ball", "content": {"kind": "shape", "items": ["..."]},
    "animations": {"position": {"keyframes": [{"time": 0, "value": [100, 500]}, {"time": 1, "value": [900, 500]}]}}}]}}
```

An equal or higher rate, or none, holds nothing. A rate that does not divide the host's holds
unevenly (24 in 30 is a pulldown), so pick a divisor of the output rate. Put whatever must stay
smooth, such as a camera move, outside the held composition. Measure the result per frame: the ink
centroid moves only on the nested frames.

**Hold the pose, not the travel.** A drawing's pose (limb swing, bob, squash) can hold on twos; the root position
of something that travels while the camera moves cannot. A root held for two frames against a smooth camera
judders against the frame: on a 3D walk followed by the camera, held travel gave an acceleration rms of 5.7 px and
a direction flip on every frame, continuous travel 1.1 px and 28 %. So key the travel continuously (on the placed
layer or carrier, outside the held composition, or on the same rate as a camera held on the same twos), and
keep only the poses held. Check it by tracking one point on the walker per frame: the velocity must not change
sign on every frame. Held limb poses under a following camera are not proven yet; a 3D walk keyed on every frame is.

A composition content layer with no `composition` field shares its parent's coordinate space, but the layer's
origin is its centre: position it at the canvas centre (`[640, 360]` on a 1280x720 canvas) and key movement from
there, or its layers land half a frame off.
