# Slapstick props: a toss and an orbit

The table of beats is in [the patterns skill](../SKILL.md#slapstick-which-preset-for-which-beat).

## A thrown or dropped prop

`toss` flies the layer from where it is placed to a landing in `flight` seconds, as a live parabola
rising `height` px above the higher of start and landing, then bounces `bounces` times. Land on a
socket, not on arithmetic: `target` is a layer id and `socket` its socket, so the prop lands on the
head wherever the head is at the landing; `x`, `y` move the landing from the socket (a lid sits above
the head's middle: `y` negative). Without `target`, `x`, `y` is a point.

```json
{ "scene": …, "layerId": "lid", "preset": "motionPreset:toss",
  "params": { "start": 0.5, "flight": 0.8, "height": 200, "target": "kid", "socket": "head", "y": -40,
              "bounces": 3, "bounceHeight": 120, "bounceTime": 0.5, "restitution": 0.35,
              "dropY": 260, "rollX": 90, "spin": 2, "bounceSpin": 0.5 } }
```

The first bounce leaves the landing for a floor `dropY` px below it and `rollX` px along (a lid off a
head falls the head's height to the floor); each next bounce is `restitution` times as high and as
far. The result returns `phases`, composition seconds: `land` (the prop reaches the target), `touch1`
to `touch4` (each floor contact; one beyond `bounces` is `land`) and `rest`. Key the thud, the
reaction (`squash` on the head, a blink, a `shake`) and the sound to them. The layer's own position
is where it is thrown from: keep it still, and keep it a layer of the target's composition.

### Falls, is dropped, lands (squash, a held prop, a whole character)

Use `toss` for anything that falls and lands; it is the one drop preset. It squashes on every contact
itself (`squash` 0 to 0.8, default 0.3; `squashLength`; each bounce squashes by the root of
`restitution` times the last), with the area kept, as `squash` does. Squash holds the contact point on
the floor, not the layer's position: set `footY` to the px from the position down to the contact point
(a ball's radius, half a 100 px box = 50, a character's feet), or the squash sinks the prop through the
floor or floats it. `bounces: 0` is one thud. `spin` and `bounceSpin` round to whole turns and `bounceSpin` turns the prop only in the air, so it is upright at every contact, its squash rests flat, and it comes to rest flat. With `footY` set the prop turns (the throw and each bounce) only while more than `reach` minus `footY` above the floor, so no turned corner dips through it, and a throw or bounce lower than that does not turn. `reach` is the prop's farthest point from its position (half the diagonal of a box); a colour layer gets it from its size and scale, any other layer takes a square about its position, so give `reach` for a tall or wide picture or a character. The layer should be upright and at its own scale at rest.

- A shape or a picture: `{ "start": 0, "flight": 0.6, "height": 1, "x": 400, "y": 500, "bounces": 2, "footY": 50 }`.
- **"The lid drops and bounces"** (a plain drop, nothing thrown): this is `toss` with `height: 1`, so it falls from rest, speeding up
  all the way down, and lands at `x`, `y` (the floor line) after `flight` seconds. It rebounds `bounces` times, each lower than the last
  (`bounceHeight`, `restitution`), squashing on every contact, and rests on the floor. `bounces: 0` is a drop with one thud and no bounce.
  Set `footY` to the px from the layer's position down to its contact point so it rests on the floor, not through it.
- A held prop let go: `holder` is the holding layer and `holderSocket` its hand socket (`holderX`,
  `holderY` offset the grip); the prop rides the hand until `start`, is let go from where the hand is, and falls to
  the landing. A holder under a parent or with a transform stack (a walk's travel) is read where it really is.
- A whole character (a cat's plop): apply `toss` to its `scene_ref` layer with `bounces` 0, `footY` its feet below the
  layer position and a strong `squash` (0.35 to 0.5); the rig squashes as one picture about its feet. Do not stack the
  `squash` preset on a layer `toss` drives, and do not give the layer a walk's travel.

## Circling stars

`orbit_around` circles the layer on an ellipse, one turn every `period` seconds, round a point or a
socket, followed live. Apply it once to each of `count` stars, `index` 0 to count - 1: their phases
spread evenly. A ring seen from slightly above is flat, `radiusY` about a third of `radius`; `depth`
makes a star larger on the near half. The star keeps its own rotation, so it stays upright (`spin`
turns it). Put the stars over the head in the layer order, or under it for a halo.

```json
{ "scene": …, "layerId": "star0", "preset": "motionPreset:orbit_around",
  "params": { "around": "kid", "socket": "head", "y": -90, "radius": 110, "radiusY": 34,
              "period": 1.2, "count": 3, "index": 0, "start": 2 } }
```

Check both in motion, not on a midpoint: `picsart_scene_contact_sheet` over the window, and for a toss the
landing against the socket's measured position at `land` (`picsart_scene_query_layout` at that second).

## Limits

`toss` and `orbit_around` place the layer in composition space. The target, a `holder` and a socket are read where they are in the composition, through their parent chain and transform stack (a walk's travel, a slide): `layer:getWorldPoint(x, y[, t])` takes a point of a layer's own space to the composition, and `layer:toParentSpace(x, y[, t])` takes a composition point into the space a layer's `position` is written in. The thrown layer may sit under a parent: the landing and the centre are brought into its parent's space where that parent stands at the landing (for a toss) or each frame (for an orbit), so a parented prop rides its parent from there on. Distances in the params (`radius`, `height`, `dropY`) are in that parent's space, so a doubled parent doubles them. The preset goes on the layer, not a shape group inside it (`preset_needs_whole_layer`: the group moves in the layer's scaled space). A read is a point in composition space, the space `getSocket`, a root layer's `position` and every authored px are in: the parent chain and transform stack place it, its depth (`z`, `rotationX`, `rotationY`) included, and it is dropped straight onto the composition's plane. This composition's camera and perspective never apply to it, in a flat and in a projective composition alike; a nested composition is a picture, so a point inside it is where that composition's own camera draws it. `toParentSpace` takes such a point back through the parent's plane, at the layer's own depth. To meet a layer under a perspective camera, give the mover the same `z` or parent it into the same plane: it then coincides with the target under every camera at every time, where another depth shows the parallax. A `cameraExempt` layer is drawn outside the camera, so a layer the camera draws meets it only while the camera is at rest.

## Dizzy stars (an orbit use)

Circle each star twice with `orbit_around` on a tilted ellipse (`radiusY` a third of `radius`) about the head socket, the same `index` and `count`: a copy with `half` `near` in a layer ABOVE the character and a copy with `half` `far` in a layer BELOW it. The two copies switch at the left and right ends of the ellipse, where they coincide (one is shown, the other hidden, never two half-transparent), so the star passes in front of the head and then behind it. Three stars at `count` 3, `period` about 1.2 s, `depth` 0.3 so the near half is larger.
