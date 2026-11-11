# A 2D head turn

Part of [character-rigging](../SKILL.md) "Cartoon character rigs".

`headTurn` (0 face on, ±1 a three-quarter view, + toward + x) and `headTilt`
are the one turn and tilt dials of both rigs: key them, never the features. rig-face turns its
features on their layers' transforms (`nose`, `leftEye`/`rightEye`, the brows, `mouth`, the ears),
so a drawing put in a feature layer turns the same way. A face built by hand turns the same way:

- **Depths.** Each feature turns round the head's vertical axis at its own depth `r`, starting at
  angle `φ = asin(x / r)` for its face-on `x`: `x = r · sin(φ + a)`, `a` the turn's angle (rig-face:
  40° at ±1). The nose stands proudest (rig-face 250 px on a 500 px head), then the mouth (210),
  then the eyes and brows (190); the outline moves least, by its morph. A nod moves each feature
  round the head's centre too, and a feature nodded low turns at the narrower jaw: scale `r` by the
  head's width at its new height.
- **Eyes.** The far eye is the one on the side the face turns toward: it narrows (scale x
  `cos(φ + a) / cos φ`, held at 0.55 or more), moves less and ends near the silhouette. The near
  eye keeps its width or grows a little (up to 1.08) and moves more. Both pupils lead the turn
  (rig-face: 16 px at ±1). Brows narrow with their eyes.
- **Outline.** Give the head outline a `turnRight` and a `turnLeft` morph target (the mirror),
  weighted by `max(0, ±sin a) / sin a_max`. Move the points mostly along x: the cheek and brow ridge
  push out on the face side, the jaw and chin come round more than the crown, the back flattens.
  Keep the handles, and lengthen them only where the outline flattens, so it stays round. Hair
  morphs with it, its fringe wrapping round with the face. Check every outline at a sweep of turns
  for a self-crossing: a fringe end that slides past the tip it hangs from loops there.
- **Ears.** Hang each ear on the outline's side at its height and slide it round with that side,
  not on the turning sphere: an ear placed past the 90° silhouette swings against the turn while
  the outline moves with it, and comes away from the head. The near ear widens and comes over the
  side toward the cheek, the far one narrows and tucks behind the outline; both move the way the
  face turns and touch the outline at every turn. Each ear's `z` follows the turn's sign: the near
  ear 1, over the head, the far one −1, behind it. Stand both ears just clear of the outline face on,
  so the swap at 0 changes nothing drawn.
- **Timing.** Lead with the eyes: the pupils (`look*`) a few frames before the head. Then key the
  turn past where it settles and back: to 0.95 and settle at 0.85 over about 0.2 s. Keys outside the
  dial's `min`/`max` warn, so the overshoot stays inside ±1. Hair and ears trail by a couple of
  frames (`hairSway`, `earSway` on the humanoid).
- **Profile.** Beyond about 0.8 a three-quarter drawing stops reading; swap to a profile drawing
  with `step` keys `by` the dial: its `opacity` `{"by": "headTurn", "keyframes": [{"at": 0.8, "value": 0,
  "easing": "step"}, {"at": 0.81, "value": 1}]}`, and the front features' `opacity` the reverse. A full
  turnaround needs a drawing per angle.
- **Several characters from one rig.** Set `headSize`, `hairStyle` and `faceShape` per instance (the `scene_ref` `parameters`): a child is `headSize` 1.15 with a short `faceShape`; a grown-up a long one at 0.9. They are fixed per character: do not key them across a shot (a keyed `hairStyle` pops). A different build (taller, broader) is a second rig, not a dial. Pitfall: `headSize` above about 1.2 with hairStyle 2 lifts the quiff 80 px higher, so leave headroom in the frame.
- **Verify** with a rendered sweep −1 → 0 → 1: every feature stays inside the silhouette, nothing
  jumps between frames, the features' x offsets keep the depth order, and at |turn| 1 the eye on the
  turn side is the narrower one and both pupils are offset toward the turn.
