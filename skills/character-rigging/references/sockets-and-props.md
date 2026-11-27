# Sockets, reach and held props

A placed character publishes named points (sockets) a parent reads, a `reach` constraint puts one of its parts on something, and
a humanoid or animal rig holds a prop itself. Contents: [Standard sockets](#standard-sockets) · [Reach](#reach-put-a-characters-part-on-something) · [Hold a prop](#hold-a-prop-inside-the-character).

## Standard sockets

Declared on `composition.sockets` beside the rig's parameters (a rig built from SVG parts returns them in `sockets`):

| Rig | Socket names | Drawn landmark |
|---|---|---|
| humanoid and front | `head`, `chin`, `chest` | Head interior, live face outline, deformed chest |
| humanoid and front | `leftHand`, `rightHand`, `leftGrip`, `rightGrip` | Wrist pivots and hand-local palm grip origins |
| humanoid and front | `leftFoot`, `rightFoot` | Shoe interiors |
| humanoid and front | `seat` | Underside of the pelvis, what rests on a seat |
| humanoid and front | `mouth`, `held` | The lip centre (it slides with `headTurn`); the held prop's slot origin |
| built from a part sheet | `crown` | The top of the painted head, where a worn prop sits (`heldBy: "head"`) |
| quadruped (dog, cat; `picsart_scene_build_model` `character: {animal}`) | `head`, `mouth`, `held` | The skull's centre; the front lip of the short or long muzzle; the held prop's slot origin |
| quadruped (dog, cat) | `leftHindFoot`, `leftForeFoot`, `rightHindFoot`, `rightForeFoot`, `body`, `tail` | Each paw's sole (a quadruped's sockets say Foot, never Paw); the body and tail pivots |
| face | `head`, `chin` | Face interior and live chin outline |
| place | `floor`, plus named prop anchors | Its support surface and attachment points |

A held prop fades by its own layer's `animations.opacity`, never `transform.opacity` (one constant value):
`"animations": {"opacity": {"keyframes": [{"time": 4, "value": 1}, {"time": 4.5, "value": 0}]}}`.

`heldBy` is a carrier, not a socket name: `right` carries the prop at `rightGrip`, `mouth` at `mouth`. Read the rig's `heldBy` enum:
it lists the carriers its body has (a dog: `mouth` and `none`).
An SVG-built cut-out rig (`picsart_scene_build_model` with `character: {svg}`) takes `right`, `left`, `chest`, `head` and `none`, and `mouth` when its sheet draws a `socket_mouth` point: its `held` is the same clip and slot at the same sockets (`rightGrip`, `leftGrip`, `chest`, `crown`, `mouth`, `held`), drawn over the torso and hips and under the near arm and hand, and a hand's `HandToHeld` reaches by IK.
Every built biped, from a part sheet, publishes `crown`, the top of its painted head.

A parent targets `{ "layer": "leo", "socket": "rightGrip" }`; Lua reads `ctx.composition:getLayer("leo"):getSocket("rightGrip")` and
`getSocketDirection`. The point and unit direction are in the reader's composition space. Optional time and constraint `lag` use the
reader's clock, mapped through the instance's speed, trim and hold. Every nesting level publishes its own names; `{layer, socket}`
forwards one hop.

## Reach: put a character's part on something

A `reach` on the placed character layer pulls one of its sockets onto a point of the stage, so you never convert coordinates or key the
rig's targets by hand:

```json
"constraints": [
  {"type": "reach", "socket": "seat", "target": {"layer": "bench", "socket": "top"}, "mix": 1},
  {"type": "reach", "socket": "rightHand", "target": {"layer": "ball", "position": [-60, 0]},
   "mix": {"keyframes": [{"time": 0.4, "value": 0}, {"time": 1.2, "value": 1}]}}
]
```

- **Hips onto a seat:** `seat` (the hips) has no `via`, so the part moves with everything hung from it (the whole body comes along). Step the feet
  forward on `leftFootX`/`rightFootX` so the knees bend in front of the seat.
- **A hand on a ball:** the target is any constraint target (`{layer}`, `{layer, position}`, `{layer, point}`, `{layer, socket}`) or a
  bare `{"position": [x, y]}` of the stage, keyed or not; a moving ball keeps the hand on it. Ramp `mix` from 0 so the arm starts from its pose.
- **A socket's `via`:** the hand, grip and foot sockets declare `via: {layer, parameter}`, the goal layer and the 0..1 dial that turn
  their limb on (`rightHandTarget`, `rightHandIk`). Through it the arm or leg bends to put the socket on the target, and a grip lands on
  it while the hand keeps its rest turn. A socket without `via` moves its part rigidly.
- **Against the rig's own ik dial:** the reach turns the limb's dial up to its `mix`; an authored dial already higher is kept, and the
  limb's own target then gives way to the reach by `mix`. At `mix` 0 the rig's own dial and target pose the limb as before, so key the
  rig's targets only on limbs no reach holds.

## Hold a prop inside the character

`rig-humanoid` and `rig-humanoid-front` (and a shape-built dog or cat, by its mouth) hold a prop themselves, drawn between the torso and
the near arm, so a ball held in two hands sits in front of the body and behind the near hand (a ball in the near hand sits over that hand's palm). Bind the prop as a clip on the rig
instance and pick who carries it:

```json
"parameters": {
  "held": {"duration": 3, "transform": {"position": [590, 520]},
           "content": {"kind": "shape", "items": [{"type": "ellipse", "size": [120, 120]}, {"type": "fill", "color": "#2f9e44"}]}},
  "heldBy": "none", "leftHandToHeld": 1, "leftHandHeldAt": [5, -15],
  "rightHandToHeld": 1, "rightHandHeldAt": [-20, 20]
}
```

The `held` parameter is the prop; the `held` socket is where it sits, for a parent that reads it.

The prop's `anchor` is the grip: a point inside the prop where the hand holds it (a stick 18 x 170 centred on its own origin takes `[0, 0]`, or a point along its length such as `[0, 40]`; `[9, 120]` lies 35 px beyond its end). An anchor outside the prop makes it float away from the hand whatever the rig does.

Set `held` and `heldBy` by merging them into the rig layer's `content.parameters` (patch `content.parameters.held` and `content.parameters.heldBy` on their own); never replace the whole `parameters` object: it carries the bindings a motion preset wrote (`acting`, `walk_cycle`), and the rig stops moving.

- **One hand carries it** (a cup, a sword, a bat): `heldBy: "right"` or `"left"`. The prop rides that hand's grip and turns with it, so
  swinging the arm by its controls swings the prop. Give the clip's transform the offset from the grip.
- **Two hands on a ball held out:** `heldBy: "none"`. The prop stays where its own placement puts it, in the rig's px, keyed or still;
  each hand comes onto it by `<side>HandToHeld` at its `<side>HandHeldAt`, a point in the prop's own px (the wrist lands there: for a
  palm on a ball's side, put the point a little above the side so the hand covers it).
- **The other hand follows a carried prop:** `heldBy: "right"` and `leftHandToHeld: 1` puts the left wrist on the bat's handle while the
  right arm swings it.
- **In the mouth** (a pipe, a rose; a dog's stick): `heldBy: "mouth"`. The prop rides the `mouth` socket and turns with the head, drawn
  over the head. A humanoid takes all five carriers (`right`, `left`, `chest`, `mouth`, `none`); a dog or cat only `mouth` (its default)
  and `none`: `heldBy: "right"` on one is refused at bind, naming `right`. The animal's `held` is the same clip; it carries a stick
  crosswise in the jaws, behind the nose, so give a long prop `rotation: 90` (at 0 it lies along the muzzle).
- **Worn on the head** (a hat, a paper crane, a crown): `heldBy: "head"` on a built character. The prop rides the `crown` socket, turns and
  nods with the head, and draws over the hair. Anchor the clip at its bottom centre (its brim) so it sits on the crown; no walk, nod or startle
  slides it. A raised near hand still draws over it in a turned view. The catalog rigs have no crown: they do not declare `head`.
  Minimal call: `{ "heldBy": "head", "held": { "duration": 3, "transform": { "anchor": [70, 60] }, "content": { …the hat… } } }`.
- **A hug:** `heldBy: "chest"`; the prop rides the chest and both arms wrap it with `HandToHeld`.
- **A character picks a prop up** (round props): two copies swap on the touch frame `t`. The prop stands on the stage as its own
  layer whose `duration` ends at `t`; the picker's `held` is the same drawing (its scale divided by the picker's on-screen scale)
  with `heldBy` the picking hand and opacity keyed `step` 0, then 1 at `t`. The hand gets there by a reach on its grip toward the
  spot on the floor, `mix` keyed 0 at `t` − 0.6, 1 from `t` − 0.1 to `t` + 0.1 and 0 at `t` + 0.7; the body crouches and bows by
  keys on `hipsRaise` (− down) and `spineLean` (+ forward) over the same span. A reach stops a few px short, so query the grip with
  `picsart_scene_query_layout` at `t` and lay the prop where it lands (the reach's target stays the floor spot). A cut-out rig seen
  from the side or three-quarter bends its knees only as far as the knee folds (`hipsRaise` about −0.4 of the leg's length in 60 px
  units: sink further and the feet slide out) and bows to `spineLean` 3.5, so with its feet planted its palm reaches a shoe's height
  or two above the floor in front of its toes (a ball, not a coin); facing the camera it reaches only its shins, so stand the prop
  on something there. Walk or carry on with `held` as usual.
  The `pick_up` preset (tag `rig-motion`) keys all of that at once: `start`, `duration` (2.2 s), `side`, the spot as `aimAt` (a layer
  id) or `targetX`, `targetY` (rig px from the resting wrist, + down), and `crouch` (a cut-out rig takes the planted-feet depth from
  its own legs) and `bow` (default 3.5, a 70° bow that reaches a ball on the floor on every cut-out rig measured; where the palm already reaches
  the spot with less, set 2.4 to 2.8 for a squat and a lean instead of a near-flat fold: check the palm against the spot with
  `picsart_scene_query_layout`); the palm, a tenth of the arm past the wrist, lands on the spot. The grip closes at `start` +
  `duration` / 2, the touch: swap the two copies on that frame (the apply result's `phases.touch`). **The preset moves the hand,
  never the prop**: a `pick_up` with no `held` bound to that hand from the touch leaves the ball on the ground while the hand rises
  empty, and validation warns `pick_up_without_prop`. Every carry or hold gesture (a pick-up, a catch, a hand-over, a lift) does the
  same three things: the stage copy ends at the grip frame, `held` with `heldBy` the gripping hand begins on that frame (offset so
  the prop sits inside the closed grip, never over the fingers), and the hold ends where the hand lets go, with the stage copy
  beginning there at the hand's position (a hold that just ends mid-air makes the prop vanish; a jump or a run on that layer keeps
  the hold or releases it first). **When the action continues in a new layer** (`kid` → `kid2` for a jump, → `kid3` for the
  landing), the prop goes with the figure: bind the same `held` (same drawing, same `heldBy`) on the next layer from its first frame,
  so the copy never has a frame where no layer shows it; or release it with a beat (hold ends, stage copy begins that same frame at
  the hand). It is never cut: check a contact sheet at the pick-up, the handoff and the drop. Validation cannot see it: it reads no
  timing. **The release falls from the hand.** At the release frame the held clip ends and the stage copy begins that same frame at
  the hand's position (query the grip with `picsart_scene_query_layout` at that frame), and the fall starts there: a stage ball that
  appears and hangs, or appears away from the hand, reads as floating. **Switching hands is a gesture.** Never key `heldBy` from one
  hand to the other with the arms standing still, nor twice inside ~6 frames: the other hand reaches for the prop (a gesture on it)
  and `heldBy` is keyed once, at the grip frame (validation warns `held_prop_hand_switch`). **Hold it up with `hold_overhead`** (tag
  `rig-motion`; `start`, `duration`, `side`; once per side for two hands), never by hand-keying an overhead raise: a raise of 1 with
  the elbow straight is a stick arm that sweeps the prop across the face on the way up. The preset takes the wrist by IK out to the
  side of the head (the side the face does not point to; a front rig opens outward) and up beside it, from the rig's own anchors
  (shoulder, arm length, eye, head box): a short arm under a big head holds the prop out beside the head at shoulder height, a long
  arm at the temple, and the hand never meets the head's box or crosses the face. `wave` goes the same way. Apply a run or walk first
  and `pick_up` over it (the reverse order is refused: both drive `hipsRaise`); `pick_up` takes its names for its window and gives
  them back. Hand-keyed keys before `start` stay.
  A string or rope the character holds is a line from the hand's socket (`rightGrip`) to the prop, so it follows the hand through the
  pick-up and the run.
  Review the pick-up as cartoon-film.md §7 says before showing it: the deepest bend (waist and hips joined, no seat
  artwork on a thigh), the touch, and the frames on either side of the swap, with a zoomed crop of the waist, hips and
  knees at the deepest bend.
- **Run or jog with a prop:** pick it up first, then apply `run` or `jog` with `start` after the pick-up's last
  key (`heldBy` stays the carrying hand). The holding arm keeps its hold and only the free arm pumps; the
  crouch keys on `hipsRaise` and `spineLean` that end before `start` stay and play ahead of the stride. Move
  the body at stride × steps: `steps` above 0 makes the run stop after that many steps (every track eases to a
  standing rest over 0.3 s; 0 loops), and the layer travels `steps` × `stride` on the same clock (or `ground_scroll`
  with the same `stride`, `stepDuration` and `start`). A gesture such as `point` follows at the stop. A run that
  starts inside the pick-up's keys replaces them. Check the hand on the handle on every frame.
- **One character hands or throws the prop to another:** `picsart_scene_apply_preset` with `motionPreset:pass_prop` on the giver,
  `{ "to": "<receiver layer>", "release": 1.2 }` (a hand-over, the default: both near hands meet between the two at chest
  height and hold the prop together for `flight` seconds, then the giver lets go and the receiver keeps it at its chest until
  its next action) or `"style": "toss"` (a wind-up, an arc `height` px high over a `flight` of 0.6 s, `spin` turns). The giver's
  held copy steps off as the next copy steps on (a flight layer between the grips, then the receiver's held copy in its `side`
  hand), so exactly one copy shows on every frame. A reach on each hand's grip carries the arms, taking the larger of its mix and
  the hand's `HandIk`; the receiver's next gesture eases that reach off. Apply it again on the receiver to pass the prop back or on
  (each hand's `<layer>_<side>Reach` marker records its passes in `content.propPasses`). Stand the two close enough for a
  hand-over: a pass whose hands cannot meet is refused with `prop_hands_apart`, naming how many px closer to step, and one whose
  faces overlap where the hands meet (hair may touch) with `prop_heads_touch`, naming how many px farther apart to stand (a rig
  whose arms are too short for both passes `style: "toss"`); facing the camera, hand over with the hands nearer each other (the
  left kid's `left`). Pass round props: a mirrored character (`scale` x negative) draws the prop mirrored. For a prop that flies
  in from the stage, step the held clip's opacity from 0 to 1 at the contact frame, where the flying layer ends.
- A hand that carries the prop does not read its `HandToHeld`. `HandToHeld` turns the arm's IK on at least that much, so leave
  `<side>HandIk` at 0. The prop's animations, looks and effects ride along.
- A rig built from SVG parts holds a prop the same way, with `heldBy` `right`, `left`, `chest`, `head` or `none` (`mouth` only when its sheet draws a mouth socket): a prop in the near hand (`right`) is gripped as a sandwich: the hand behind it, and a copy of the hand cut to the half past the grip (`rightHandFingersArt`, drawn only while that hand carries it) over it, so it shows above the fingers and is never over them (size it to sit inside the hand; a hand drawn with curves is not cut, and its prop stays under the whole hand); a prop at the chest is over the torso and under the whole near arm, so a jar hugged there is behind the arm that hugs it. On the side `rig-humanoid` the near hand grips it the same way, over the palm and under the fingers and thumb (`rightHandFingers`). Read its `heldBy` enum for the carriers its sheet gives it.

## Check a hold, pick-up, throw or hand-over

After any of them, run `picsart_scene_lint_layout` over the shot before you show it: the lint reads what is drawn, so a prop that jumps, floats or vanishes is a finding no one has to spot by eye. Each code names its fix.

- `pick_up_without_prop` (a warning on the `pick_up` gesture): no prop begins in the hand at the touch, halfway through the gesture, so the viewer sees the hand reach for nothing and leave it. Bind the `held` clip so it begins at the touch frame.
- `held_prop_hand_switch` (a warning on `heldBy`): the prop changes hands in a snap, within about six frames of the last switch, or with no gesture playing at that time. Move it across with a hand-over or a gesture, and leave the carrier alone between the two.
- `heldHidden`: the prop showed under half of its drawing for 0.4 s, because the body covers it. A prop in the far hand sits behind the body by design; hold it in the near hand (`heldBy`) if it is meant to show.
- `heldOutsideHand`: the prop floated more than one of its radii from the grip, or across the body from it, for 0.4 s. Put the prop on the rig's `held` slot and key `heldBy` to the hand that carries it.
- `heldDropped`: the prop is drawn nowhere for 0.4 s or more beside a hold, neither by the hold nor by a copy of the same drawing (the stage copy before the pick-up or after the drop, the next shot's hold). The viewer sees it vanish or pop in. Bind the same `held` where the first hold ends, or keep the hold to the handoff. A prop whose drawing is a bare colour, or a scene local to a nested document, is counted in a note and not judged.
