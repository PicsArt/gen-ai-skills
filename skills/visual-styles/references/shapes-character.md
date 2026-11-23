# Shapes character

How a `cast: shapes` style makes its people and animals: drawn from the style's own shapes, saved once, reused
everywhere. No generated sheet and no part-sheet build, so the figure never gains detail the style forbids.
Each shapes recipe's "The character" section says what the figure is made of; this page is the mechanism.

## Build it once

One `scene` asset of shape layers. Joints are parents: a torso layer at the hip, the head and the upper arms
with `parentId` the torso, each forearm with `parentId` its upper arm, each shin its thigh. Every child has a
`transform.position` (the joint in the parent's pixels) and its shape is drawn about `[0, 0]` so it turns about
the joint. Size the scene 600x1000 with the soles at y 1000 and the hip about y 620, so every figure places the
same way.

Declare the controls as `parameters` (`type` `number`, `animatable`, `min`, `max`) with the standard control
names, and bind each to a layer track with `by`:

```json
"parameters": {"spineLean": {"type": "number", "animatable": true, "default": 0, "min": -1, "max": 1}},
"animations": {"rotation": {"by": "spineLean", "keyframes": [{"at": -1, "value": -9}, {"at": 0, "value": 0}, {"at": 1, "value": 9}]}}
```

The base set: `spineLean`, `headTurn`, `blink` (the eyes' `scale` y, 1 to 0.1), `{left,right}UpperArmRaise`,
`{left,right}LowerArmSwing`, `stride` (thighs opposed) and a `mouth` chart: a closed path whose `vertices` take
`by` `mouth` with one drawing per `step` key at 0, 1, 2 (`rest`, `aa`, `oh`; every drawing needs a body, so a
shut mouth is a thin slab, never a bare line). A face-less style drops `blink` and `mouth`.

## A figure that runs, points or picks up: build it as a cut-out

The hand-built base set above is for a figure that gestures and acts in place. A figure that **runs, jogs, points or
picks something up** is drawn in the style's shapes as named SVG parts and built with the SVG cut-out builder
(`picsart_scene_build_model` with `character: {svg, view}`; `buildCutoutRigFromSvg`). It is posed by the rig-humanoid control set, hand and
foot IK included, so `run`, `jog`, `point`, `pick_up`, `walk_cycle` and the gestures drive it unchanged, with their
distances scaled to its legs as for any cut-out. There is no second preset family and no joint-angle fallback.

- **Draw one view**, side or three-quarter facing right, `data-view` on the `<svg>`: the parts `head`, `neck`, `torso`,
  `upperArmL/R`, `lowerArmL/R`, `handL/R`, `upperLegL/R`, `lowerLegL/R`, `footL/R` as groups of the style's own shapes
  (the near limbs left of their far twins), the joint markers `jointNeck` and `joint{Shoulder,Elbow,Wrist,Hip,Knee,Ankle}{L,R}`
  (one circle each, inside both parts it joins) and the `socket_*` markers. Every limb is two pieces overlapping at the joint.
  The part-sheet rules are in part-sheet-prompt (the `character-rigging` skill, `references/part-sheet-prompt.md`); run the picture
  check (`check: true`) before the build.
- **The style survives the build.** Flat fills, angular pieces and outlines stay as drawn; a stroke-only limb becomes the
  closed outline of its own stroke, filled in the stroke colour. The builder gives each arm and leg one whole-limb mesh
  (upper and lower piece skinned together), so a flat angular wedge bends at the joint as one shape. A look the build breaks
  is a defect of the builder: fix it there, never with a second gait on the figure.
- **Held prop.** Bind it as the rig's `held` clip and pick the carrier with `heldBy` (a ball in a mitt: a clip larger than the
  hand, so it shows round the mitt); `pick_up` lands the palm on the spot and the two copies swap on the touch frame, as
  the `character-rigging` skill, `references/sockets-and-props.md` describes.
- **Scene length.** The rig's `duration` is a scene parameter (default 10, up to 3600): set it to the film's length and the
  placing layer's tracks run on the host clock.
- **Run across a scrolling set:** `run` with `travel: "in_place"` and `ground_scroll` on the scenery parent, as for any rig.
- **A style whose figure has no knee or elbow is refused by the builder by name** (`missing_part` for a limb drawn as one
  piece, `missing_joint` for a missing marker): the brick toy and the shadow puppet take none of these four presets, and their
  recipes say so.
- **Stepped time** (twos, fours) is the style's: nest the figure at the style's `fps`, never bake it into a preset.

## What the figure is made of

- **Feet.** Every standing figure ends in feet that rest on the floor line: a small wedge or oval per style, a short
  foot stroke for a stroke figure. The sole is at y 1000 and the shot places that point on the floor line, never
  below it, so the legs never sink into the floor.
- **Arms of a bodied figure** grow out of the body's silhouette at the shoulder, about as thick as the style's
  tile shows them, never a thin line laid across the torso (the shared limb rule is in
  character-rules (the `character-rigging` skill, `references/character-rules.md`)).
- **Arms of a stroke figure** (stick figure, whiteboard explainer) stay strokes, because the stroke is the style.
  They start at a shoulder point below the head circle, a little off the body's line, and a raised arm is limited
  to about 150 degrees so it passes beside the head, never across it.

## Save it once

Validate (`picsart_scene_validate`), then save it with the library save (`kind` `character`; the library refuses a
character with no standard control parameter) and place it in every shot by the saved scene's `uri`:

```json
"assets": {"clerk": {"type": "scene", "uri": "<the saved sceneUrl>"}},
"layers": [{"id": "c", "transform": {"position": [640, 670], "anchor": [300, 1000], "scale": [0.8, 0.8]},
            "content": {"kind": "scene_ref", "assetId": "clerk", "fit": "none", "parameters": {"headTurn": {"keyframes": [...]}}}}]
```

Never redraw the figure per shot. A second person is the same asset mirrored (negative `scale` x) or a copy
saved with other colours. Act by keying the dials on the placing layer.

## Talk

The `lipSync:visemes` preset (`picsart_scene_apply_preset`) drives a shapes mouth. Call it with the transcript and `mouthShapes` mapping each drawing to the number the `mouth` parameter takes, `{"rest": 0, "aa": 1, "oh": 2}` (an array is refused); it merges the `mouth` track into the placing layer's `parameters` itself, so nothing is keyed by hand. Proven on the mid-century clerk: the drawn mouth swaps at the word times. A face-less figure (silhouette, stick, woodcut) cannot talk this way.

## Acting that reads

Faces are small, so act with the body: lean, an arm up, a head turn, then the mouth. Keep the figure at 40% of
the frame height or more.

## Checklist

1. Feet rest on the floor line, never sunk into it.
2. A bodied arm grows out of the torso's silhouette; a stroke arm starts below the head and a raised one passes beside it.
3. Every dial moves something visible at 1x; render a frame of each shot and look.
4. The figure was saved once and is placed by its `uri`, not redrawn.
