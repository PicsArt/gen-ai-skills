# Cartoon fast motion: smears, multiples and speed lines

What makes a chase or a hit read as a cartoon rather than a tween. Three motion presets read the
layer's real motion and draw only on frames faster than their `threshold` (pixels per second), each
pointing along the motion. Key the move plainly; they fire on the fast frames and are gone on the
slow ones.

| Preset | Apply it to | What it draws | Use it for |
|---|---|---|---|
| `smear` | the moving layer | its drawing stretched back over the path of the last `span` seconds, thinner: exactly along a horizontal or vertical move, as near as a few degrees of lean allow on a diagonal | a body dash, a throw, a zip exit |
| `multiple` | a copy of the moving layer, beneath it, with `of` naming the mover | the copy where the mover was `lag` seconds ago, posed as it was then (an `attach` constraint with `target.lag`) | a fast wave or a run |
| `speed_lines` | an `mpscene://speed-lines` layer beneath the mover, `of` naming it | lines on the mover, trailing opposite its motion, longer with speed | a dash, a zip |

```json
{"id": "lines", "content": {"kind": "scene_ref", "sceneRef": "mpscene://speed-lines",
  "parameters": {"gap": 90, "length": 300, "spread": 150}}},
{"id": "cat_m1", "content": "…", "transform": {"position": [200, 430]}},
{"id": "cat", "content": "…", "animations": {"position": {"keyframes": ["…"]}}}
```

Then `smear` on `cat` (`length` its drawn length along the dash), `multiple` on `cat_m1`
(`{"of": "cat"}`) and `speed_lines` on `lines` (`{"of": "cat"}`).

- **Frame counts.** A smear covers 1 frame of path (`span` = 1/fps), 2 for a longer one. Multiples are
  2 or 3 copies at `lag` 1, 2 and 3 frames, opacity 0.6, 0.4 and 0.25. Let the fast part of the move
  last 3 to 7 frames: an 840 px dash in 0.25 s fires on its middle 4 to 5 frames.
- **Thresholds.** The defaults (smear 1500, multiple 1200, lines 1000 px/s) suit a 1280 px frame; scale
  them with the frame. An anticipation or a settle stays under them.
- **A turn.** `multiple` counts a turn by the arc `reach` pixels from the anchor sweeps, so a forearm
  with its anchor at the elbow, waving on a rotation track, fans out its multiples. `smear` and
  `speed_lines` follow position only.
- **Exit zip.** Ease back 30 to 50 px over 0.2 s, hold 0.1 s, then leave the frame in 1 to 3 frames on
  a `linear` key. The smear and the lines fire on those frames, and the multiples stay behind for their
  `lag`, an afterimage.
- **Dust puffs.** A few grey ellipses at the launch point that scale up and fade over 0.3 s, started on
  the launch frame.
- **With motion blur.** `motionBlur` on the mover blurs every moving frame, the slow ones too, and it is
  soft. A smear is a drawing: crisp, and only on the fast frames. Use one or the other on the same
  layer; blur reads as live action, the smear as a cartoon.

`of` is a `layer` parameter: another layer of the same composition, not the copy itself or one of its
children. What they read: `smear` reads the layer's own `animations.position` and `speed_lines` the
`of` layer's, so motion from a parent or from another preset's `transforms[]` component is not seen
by them. `multiple` attaches to the `of` layer's whole pose a `lag` back, parents and components
included, wherever the copy is parented. Keep the mover's anchor at its centre, the point the smear stretches about.
Inside a rig template the limbs are not yours to copy, so multiples of a rig's arm need the rig to draw
them. Verify by rendering frame by frame: the ink area grows only on the fast frames.
