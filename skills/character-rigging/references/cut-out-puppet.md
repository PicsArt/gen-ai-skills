# A cut-out puppet from named SVG parts

How the rig that `picsart_scene_build_model` builds from `character: {svg, ...}` behaves, and what to check after building
or changing one. The drawing's prompt, picture check and builder contract are in
[part-sheet-prompt.md](part-sheet-prompt.md). The call replies `{scene, sockets}`: the rig scene and its published
sockets ([sockets-and-props.md](sockets-and-props.md)); no 3D tool or model is involved.

## Contents

- [Host the rig](#host-the-rig)
- [Standard control set](#standard-control-set)
- [A garment over the legs](#a-garment-over-the-legs)
- [Draw order](#draw-order)
- [After building or changing a rig](#after-building-or-changing-a-rig)
- [Waving](#waving)

## Host the rig

Place the rig's `scene_ref` on its own layer with its anchor at the figure's bottom-centre and
`blending: "pass_through"`. Without it the rig draws on its own canvas and clips every piece past it: soles, hair, a
raised hand. Pose it only through parameters; placement is the layer's, as for any `scene_ref`. A
walk, jog or run is shown only from the three-quarter or side view; the front view gets the rest or idle pose and face
acting. Hands stay rigid (no finger poses) unless the drawing carries a complete matching set of hand poses.

## Standard control set

Both views declare `rig-humanoid`'s names ([rig-controls.md](rig-controls.md)), so the
catalogue presets drive a cut-out unchanged: `wave`, `point`, `think`, `walk_cycle`, `jog`, `jump`, `idle` and `acting`
(`jog` takes `view: "front"` for the front view). No preset sits: key those dials yourself.

- `headTilt` rolls the head; `headTurn` narrows the head by the turn's cosine and slides a `face` toward it, stopping where the
  far eye nears the outline (a flat approximation: no three-quarter drawing is swapped in and hair does not follow).
- `hipsTilt` rolls the pelvis and counter-rolls the spine; feet and IK hands stay on their targets. `hipsRaise` reaches
  ±3 (±180 px): down for a crouch or a sit, up for a jump. In the side view a foot target bends the knee, so a crouch is
  `hipsRaise` keyed down with the feet planted.
- `<side>HandIk`, `HandX`, `HandY` reach a hand to a point with an elbow bend. `<side>HandSpread` widens the hand.
- An elbow and a knee only flex, on every view and both sides: `LowerLegSwing` is held to 0..1 (0 straight) and `LowerArmSwing`
  to −1..1 (0 straight, either side). The IK always takes the anatomical solution (elbow back, knee forward; in front the forearm
  folds toward the midline), and a measured limit cannot open a joint past straight.
- `LowerArmSwing` is signed: the angle is |dial| × the elbow's range and the sign is the side of the picture the forearm folds
  to. Front view: + folds toward the body's midline (across the chest hanging, down onto the hip out), − the other way (out
  from the body hanging, up beside the head out). Three-quarter and side views: + folds forward (the walk, the chin), − backward;
  the near arm opens out behind, so its fold up beside the head is −, and the far arm opens forward, so its is +. A wave keys − on the near arm.
- The side and three-quarter views foreshorten an opened arm by the view's cosine; `UpperArmRaise` is the forward pitch in
  every view (in the front view it joins the swing in the cosine foreshortening).
- The front view bends in depth, so a knee or elbow only shortens: `LowerLegSwing` (90° of fold) shortens the thigh and the
  shin by the cosine of their pitch. With the foot planted (`FootIk` 1) the foot's drop decides how the fold divides: a half dial
  with a hip drop of about 2 is a crouch, a full dial at about 2.7 a sit; a full dial with the hips up and the foot target out
  of reach tucks the legs for a jump. A lifted leg shortens toward the camera (down to 0.5), so a lift of 100 rig px is reached by
  foreshortening alone. The feet never cross.
- `spineLean`: in the front view the torso shortens by the cosine of `spineRange` × the dial (20° at 1) and the head drops with it;
  it never rolls (the sideways sway is `hipsTilt`). In the side and three-quarter views it reaches 3.5 forward (70°) and −1.5 back
  (30°); an arm hangs from the world's vertical, so `UpperArmSwing` keeps an arm straight down at any lean or roll.
- The `face` option takes `brows`, `pupils`, `smile`/`frown` and `visemes` (`aa ih ou ee oh` as extra mouth drawings; the highest
  dial wins, a hard switch with no double mouth). `angry` and `surprised` mouth drawings join that switch; `browAngryLeft/Right` and
  `browRaisedLeft/Right` replace the brow from 0.5 up. `blink` closes fully to a lid line. `acting` needs a face with pupils and
  brows; without them only `look*` and `browInnerUp` are refused.
- A piece (a ball, a hat, a pouch) can carry `attachments`: `{ Ball: { at, items, farItems?, behind? } }` draws `items` around a
  point of the piece's drawing so it turns, mirrors and foreshortens with it; `behind` draws it just under the piece's art, else
  just over; the far side's copy is `farItems`. Not animatable. A torso of shapes can carry `overArm` items (a hood or collar) that
  draw over the near arm, so a sleeve's top never crosses them.
- Walk defaults and dial units: `lift` is rig px, not 0..1 (a walk about 24–40, a run up to about 100; `lift: 1` barely steps);
  the three-quarter view foreshortens `stride` and `armSwing`.
- A hand carrying a prop is not drawn by the rig: see "Hold a prop" in [sockets-and-props.md](sockets-and-props.md).

## A garment over the legs

The torso is one picture, so a dress, skirt or coat tail is its lower rows: draw one torso drawing that reaches as far down as
the garment does, with no separate skirt piece. When it reaches below the thigh root (the hip joint plus one grid step) the rig skins
it over the legs, so the legs pass behind it and the waist stays one picture; a shirt that ends above the thigh root stays one
rigid piece. A shape torso is skinned on its outline's control points, a picture torso gets a mesh at the limbs' 12 px step, and
either draws the plain picture at rest.

- **Side and three-quarter views:** two empty helpers `garmentLegFront` (the forward-most thigh's drawn turn) and
  `garmentLegBack`, pivoted at the hip joint, each with a child `...Hang` bone one thigh length down that undoes its parent's turn so
  a hem below the knee hangs vertical. Rows above the thigh root follow `garmentUpper` (a child of `spine` that carries the breath
  scale), the pelvis band `hips`, the rows below the hip joint the helpers, split by the column's share from the front edge to the
  back edge. The rig faces +x, so the front edge is the +x edge; a figure facing the other way is the host layer's mirror.
- **Front view:** a helper per leg (`garmentLegLeft`, `garmentLegRight`) takes its thigh's sideways turn and drawn shortening,
  with a hang bone under a frame that undoes both; the left half of the garment follows the left helper, the right half the right,
  blended across the centre.
- **Where it shows:** below a raised knee the hem spans both knees, so a long hem widens by about the gap between them. Keep the
  drawing wide enough for the stride it covers. A torso that sets its own `deformers` and also hangs over the legs is refused.

## Draw order

Between layers a later one draws over an earlier one. The builders order parts by role, never by document order: far limbs,
near legs, hips, torso, head, near upper arm, torso-over-arm, near hand and forearm. A chain splits only at a named seam: torso
art over the arm (a strap, vest edge, collar, hood: never a sleeve, which is drawn on the arm piece) between the upper arm and the
hand. Pose-dependent depth (the front arm swung back passes behind the torso) is a `by` track on `z`; put it on a bone, never on an art.

- A `z` within ±1, static or a keyed `by` track with no expression, only sets draw order (it is no depth for `ik`, `skin`,
  `follow_through` or preset travel) while the composition is flat. Beside a layer in depth or an orbiting camera every `z` is depth
  (warning `z_order_mixed_with_depth`).
- The cut-out front rig's arm and leg `z` follow their own swing dials, so reach with `HandIk` 1 and leave `UpperArmSwing` at 0 (a
  swing is ignored by the IK but still flips the order).
- On a document, `picsart_scene_check_contracts` with the `order` axis `paint` checks the stack; pairs a pose row reverses are left
  out, so front-view arms are checked by the build only.

## After building or changing a rig

Run the pose set, then the checks; judge frames, never a mean pixel diff (it cannot see text or shape defects).

- **Poses.** Rest; each joint at its min and max; the shipped presets (walk, jog, wave, point, think, breath) with their defaults,
  sampled across their window, not once at the midpoint (`think` aims at the rig's chin: never hand-set targets); every view; the near
  AND the far side of every limb and hand, extremes included.
- **Numbers that pass.** No hole, opening, stray fragment or flat patch wider than a hair; a shoulder cap adds 0 px outside the rest
  silhouette; a limb piece's drawn axis lies along its bone within 3°; no wrist step over 20 px per frame; the far side has the near
  side's hue, only darker; every garment region has one owner (sleeve, puff and cap on the upper arm, cuff on the forearm, strap, vest
  edge, collar and hood on `torsoOverArm`, skirt on the garment picture); a hand's length against the face is the same on every view
  and on both sides, within 10%. Proportions are the character's style (chibi, animal, robot, stylised adult); only when the brief
  names none, a realistic hand is about 0.85 × the chin-to-hairline height, its width about 0.5 × its length.
- **Joints and views.** For limbs cut at the joint, the child's end is round and centred on its pivot, continuing past it by at least
  its half-width, with the parent plain under it for the same radius (a shoulder cap is a circle on the shoulder pivot, radius at least
  the arm's half-width plus 6 px). A one-piece skinned limb ends at the wrist and the hand is its own piece; the build refuses a
  whole-arm picture whose paint passes the wrist. A side or three-quarter rig defaults the knee range to 110°, a front rig to 90°; an
  explicit `knee` limit wins.
- **Tool runs, both sides each time.** Wrist jump, foot clearance (amplitude at least 0.8 × `lift`) and a planted foot (at most 1 px per
  frame): `picsart_scene_check_motion` (`velocity_range`, `value_range`) on `leftHandArt`, `rightHandArt`, `leftFootArt` and
  `rightFootArt`. Hand over the face: `picsart_scene_lint_layout` collision hands × `headArt`, sustained at least 0.4 s; the hosted lint is geometric, so look at the frames for a hand over a speaking mouth. A part cut by
  the canvas: `picsart_scene_query_layout` `onCanvas` is `full` at every dial extreme. For an elbow outward of its shoulder, compare
  `picsart_scene_query_layout` pivots; `picsart_scene_check_contracts` `order` axis `x` compares layer centres.
- **Builder notices** (read them; they are not refusals). A far-side root whose x-offset from the clothing's painted midpoint exceeds the
  clothing's half-width lies beside the clothing: review its placement against the drawing. A garment that paints above and below the
  resting hand names the source piece: split it at the hem. An explicit one-piece sleeve cannot interleave a torso `overArm` collar
  between the upper arm and the forearm: use segmented arms.
- **By eye.** The shoulder and hip seam crops, both sides, at rest, at the extremes and at the walk's contact and passing frames; the hand
  crop (back and palm, thumb join); near and far hands of one design; the three views read as one person; the far arm moves in the
  three-quarter presets.
- **Joint deformation ladder** (a pinch or a lost volume at a fold): weight rows first (softness, cut); then a keyed `by` the dial: a
  path `morph` on a shape piece, a `push` deformer on a mesh piece; last, a corrective helper by hand, an empty layer skinned into the
  drawing's one skin, `position` and `scale` keyed `by` the dial. Soft masses (garments, muscles, belly, chest, hair, cheeks) are one
  helper bone `<bone><Mass>` the same way, driven by a `by` track or `follow_through` on the helper, never on a skinned drawing; a
  volume-keeping squash is a `<bone>Squash` parent spring with a `<bone>Mass` child.

## Waving

The robot's `wave` action and the catalogue `wave` preset follow the wave rule in `character-rigging` `references/rig-act.md` "Gesture arms": the same rows by
`viewAngle`, `HandSwing` swinging on a cut-out arm as on the catalogue rigs. Tune `amount`, or key the dials yourself under an
ease-in, hold, ease-out envelope.
