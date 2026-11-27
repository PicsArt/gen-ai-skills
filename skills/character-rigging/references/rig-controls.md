# Standard control names on a rig

Part of [the character-rigging recipe](../SKILL.md); one section of it, read on its own.

**Standard control names**, shared with 3D characters: a face takes VRM expressions, a body `<vrmBone><Motion>`, hair, ears and tails `<part><Motion>` (`Sway` is a side-to-side pendulum). Any rig of the same type uses the same names
and ranges, so a preset or a keyed track moves every one of them.

| Rig | Parameter | Range | Meaning |
|---|---|---|---|
| both | `blink`, `blinkLeft`, `blinkRight`, `aa`, `happy` | 0..1 | eyes shut, one eye shut (the left eye is on + x), mouth open, smile |
| both | `headTurn`, `headNod`, `headTilt` | −1..1 | turn toward the viewer's right (0 face on, ±1 a three-quarter view; on the humanoid + toward +x the way its body faces), chin down, roll clockwise |
| both | `lookUp`, `lookDown`, `lookLeft`, `lookRight` | 0..1 | irises' direction; `lookLeft` is + x on screen (on the humanoid an eye turned away travels less across) |
| both | `ih`, `ou`, `ee`, `oh` | 0..1 | the other visemes |
| humanoid | `browInnerUp`, `browOuterUpLeft`, `browOuterUpRight`, `eyeWideLeft`, `eyeWideRight` | 0..1 | both brows' inner ends up; one brow's outer end up; one eye opened wide (a blink still shuts it) |
| face | `sad`, `angry`, `surprised`, `relaxed` | 0..1 | moods (mouth, eyes, brows); the humanoid rigs and `rig-face` carry them with `happy`. The six mood actions are `happy`, `sad`, `angry`, `surprised`, `scared` (sad + surprised + `browInnerUp`) and `sleepy` (relaxed): no `scared` or `sleepy` dial |
| humanoid | `spineLean`, `hipsRaise`, `hipsTilt` | −1..1 (`hipsRaise` −4..1) | torso lean ±20° (+ forward); hips 60 px a unit (+ up, down to 240 px for a seat); pelvis roll ±10° (+ clockwise, the + x hip drops), the legs following on their IK and the shoulders tilting against it |
| humanoid | `breath` | 0..1 | breath: the chest swells, shoulders and head rise |
| humanoid | `<side>UpperArmSwing` / `UpperArmRaise` / `UpperArmOpen` / `ShoulderRaise` / `LowerArmSwing` / `HandSwing` | −1..1 / 0..1 / 0..1 / 0..1 / −1..1 / −1..1 | arm ±80° (+ forward); raised forward and up 0..160° (0 hangs, 0.5 forward, 1 overhead; the front view draws it foreshortened); opened out to the side and up 0..180° (0 hangs, 0.5 sideways, 1 overhead; drawn foreshortened as it opens toward or away from the camera on the side and three-quarter views); shoulder lifted 15 px at 1 (the shrug); elbow ±150° (+ folds forward, toward the midline on a front view; − the other way: up beside the head on an opened near arm; on the far three-quarter arm, which opens forward, up beside the head is +); wrist ±40° |
| humanoid | `<side>UpperLegSwing` / `LowerLegSwing` / `FootSwing` | −1..1 / 0..1 / −1..1 | leg ±70°; knee 0..140° (elbow and knee limits are their bends' `min`/`max`, binding IK too); toe up ±35° |
| humanoid | `<side>HandSpread`, `<side>HandPoint`, `<side>HandFist`, `<side>HandGrip`, `<side>HandThumbsUp` | 0..1 | hand poses on a palm, four fingers and a thumb, the relaxed open hand at 0: fingers fanned (the waving hand), the index pointing, a fist, curled fingers with an opposing thumb (grip), the thumb out from curled fingers; the five share the hand (scaled to 1 above a sum of 1, the relaxed hand filling the rest), so a crossfade is two keyed weights over 0.4 s, `ease_in_out`; every pose has the same path topology, so there is no swap between duplicate hands. A grip is a silhouette, not a prop contact |
| humanoid | `held`, `heldBy`, `<side>HandToHeld`, `<side>HandHeldAt` | clip / right·left·chest·mouth·head·none / 0..1 / vec2 | the prop the character holds, who carries it (`head`, on a character built from a part sheet, wears it on the `crown`), a hand brought onto it, and where on the prop that wrist lands ([references/sockets-and-props.md](sockets-and-props.md)) |
| humanoid | `<side>HandIk`, `<side>FootIk` | 0..1 | the limb's `ik` `mix`: from the swings to the target (feet default 1, hands 0) |
| humanoid | `<side>HandX/Y`, `<side>FootX/Y` | −3 arm lengths..+3 | the target layer, rig px from the resting wrist or ankle |
| humanoid | `hairSway`, `hairRaise`, `earSway` | −1..1 | follow-through: hair swing (+ toward + x), hair raise (+ up), each hair vertex the more the farther below the outline's top; ear rim swing (+ toward + x); key them a few frames behind the head |
| humanoid | `lashes` | 0..1 (0) | two lash flicks off each upper lid's outer corner; a blink hides them |
| humanoid | `faceStyle` | whole numbers 0..1 | 0 the drawn face; 1 a soft face: bigger eyes with a shine, thin arched brows, a small nose, a smaller mouth |
| humanoid | `blush` | 0..1 (0) | a pink patch under each eye |
| humanoid | `headSize` | 0.8..1.25 (1) | head size: the whole head (features, hair, ears) scales about the neck, the body does not; the planted feet and every limb are untouched |
| humanoid | `faceShape` | whole numbers 0..2 | which skull shows: 0 round, 1 long (chin 14 px lower), 2 short (chin 14 px higher); drawings swap with `step` keys, they do not blend |
| humanoid | `hairFrontOutline`, `hairBackOutline`, `accessoryOutline` | path: a stock name or a closed outline | the hair over the crown (`cap` with a fringe, `cropped`, `quiff`, `bob` to the jaw, `ponytail`, `long` to the shoulders), the hair hanging behind the head and body (`bob`, `ponytail`'s tail), and an accessory over the hair (`bow`, `ribbon` tying the ponytail); or any closed outline in head px (crown y −228, centre line x 12, skull 232 px wide), any vertex count. The rig turns every outline with `headTurn` and swings both hair outlines by `hairSway`/`hairRaise`. A ponytail sets six values together: `hairFrontOutline` and `hairBackOutline` `"ponytail"`, `hairBack` 1, `accessoryOutline` `"ribbon"`, `accessory` 1 and `accessoryBehind` 1. `accessoryBehind` 1 puts the accessory on the back of the head: it goes behind the skull as the face turns away and swings as the stock ponytail does, whatever `hairBackOutline` binds; leave it 0 for an accessory on the front of the crown, such as `bow` |
| humanoid | `hairBack`, `accessory`, `accessoryColor` | 0..1 / 0..1 / colour | back hair and accessory shown (1) or not (0, the default); the accessory's fill |

`<side>` is `left` (the far side, behind the body) or `right` (the near side).

**The face has no mouth curl or skew.** `rig-face` moves its mouth with the visemes, `happy`, `sad`, `angry`,
`surprised`, `relaxed` and `speech`; `happy` and `sad` lift or drop both corners together, and nothing moves one
corner or tilts the mouth. A lopsided smirk or a skewed mouth is a custom `mouth` path chart with its own
outlines (see the `shapes` character's mouth in the visual-styles `shapes-character` reference).
