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
| quadruped (dog, cat) | `head`, `mouth`, `held` | The skull's centre; the front lip of the short or long muzzle; the held prop's slot origin |
| quadruped (dog, cat) | `leftHindFoot`, `leftForeFoot`, `rightHindFoot`, `rightForeFoot`, `body`, `tail` | Each paw's sole (a quadruped's sockets say Foot, never Paw); the body and tail pivots |
| face | `head`, `chin` | Face interior and live chin outline |
| place | `floor`, plus named prop anchors | Its support surface and attachment points |

`heldBy` is a carrier, not a socket name: `right` carries the prop at `rightGrip`, `mouth` at `mouth`. Read the rig's `heldBy` enum:
it lists the carriers its body has (a dog: `mouth` and `none`).
An SVG-built cut-out rig (`picsart_scene_build_model` with `character: {svg}`) takes `right`, `left`, `chest` and `none`, and `mouth` when its sheet draws a `socket_mouth` point: its `held` is the same clip and slot at the same sockets (`rightGrip`, `leftGrip`, `chest`, `mouth`, `held`), drawn over the torso and hips and under the near arm and hand, and a hand's `HandToHeld` reaches by IK.

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
the near arm, so a ball held in two hands sits in front of the body and behind the near hand. Bind the prop as a clip on the rig
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
- **A hug:** `heldBy: "chest"`; the prop rides the chest and both arms wrap it with `HandToHeld`.
- **A character picks a prop up** (round props): two copies swap on the touch frame `t`. The prop stands on the stage as its own
  layer whose `duration` ends at `t`; the picker's `held` is the same drawing (its scale divided by the picker's on-screen scale)
  with `heldBy` the picking hand and opacity keyed `step` 0, then 1 at `t`. The hand gets there by a reach on its grip toward the
  spot on the floor, `mix` keyed 0 at `t` − 0.6, 1 from `t` − 0.1 to `t` + 0.1 and 0 at `t` + 0.7; the body crouches and bows by
  keys on `hipsRaise` (− down) and `spineLean` (+ forward) over the same span. A reach stops a few px short, so query the grip with
  `picsart_scene_query_layout` at `t` and lay the prop where it lands (the reach's target stays the floor spot). A cut-out rig seen
  from the side or three-quarter reaches the floor about one hand in front of its toes at full crouch and bow (`hipsRaise` −3,
  `spineLean` 3.5); facing the camera it reaches only its shins, so stand the prop on something there. Walk or carry on with `held`
  as usual.
- **One character throws or hands the prop to another:** `picsart_scene_apply_preset` with `motionPreset:pass_prop` on the giver,
  `{ "to": "<receiver layer>", "release": 1.2 }` (a throw: a wind-up, an arc `height` px high over a `flight` of 0.6 s, `spin`
  turns) or `"style": "hand"` (both hands meet between the two, a flat 0.2 s pass). The giver's held copy steps off as the next copy
  steps on (a flight layer between the grips, then the receiver's held copy in its `side` hand), so exactly one copy shows on every
  frame. A reach on each hand's grip carries the arms, taking the larger of its mix and the hand's `HandIk`; apply it again on the
  receiver to pass the prop back or on (each hand's `<layer>_<side>Reach` marker keeps its passes in the first line of its
  expression). Stand the two close enough for a hand-over: each hand reaches about 1.3 head-to-chest lengths in front of its chest;
  facing the camera, hand over with the hands nearer each other (the left kid's `left`). Pass round props: a mirrored character
  (`scale` x negative) draws the prop mirrored. For a prop that flies in from the stage, step the held clip's opacity from 0 to 1 at
  the contact frame, where the flying layer ends.
- A hand that carries the prop does not read its `HandToHeld`. `HandToHeld` turns the arm's IK on at least that much, so leave
  `<side>HandIk` at 0. The prop's animations, looks and effects ride along.
- A rig built from SVG parts holds a prop the same way, with `heldBy` `right`, `left`, `chest` or `none` (no `mouth`): the prop sits over the torso and under the near arm and hand. Read its `heldBy` enum for the carriers its sheet gives it.
