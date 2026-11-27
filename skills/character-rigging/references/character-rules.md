# Cut-out character rules

What a cut-out character must do before it acts in a film. Each rule is a fault that reviews of rigged
cartoon characters kept finding. Under each rule: what does it here today, and how to build it by hand
in the scene where no tool does it yet.

The tools: `picsart_scene_build_model` builds the cut-out rig from a part sheet, one SVG of named parts
([rig-build.md](rig-build.md), [cut-out-puppet.md](cut-out-puppet.md)), and poses it by bones and the
standard controls ([rig-controls.md](rig-controls.md)); `walk_cycle` and `acting` animate it;
`picsart_scene_inspect` (`mode: "rig"`) reads the bone map. "Cut" below means a group drawn on the sheet.
`picsart_scene_cut_parts` cuts the parts out of one finished picture instead
([cut-from-one-picture.md](cut-from-one-picture.md)); there "cut" is its cut.

## Contents

- [1. Clothes follow the body at every joint](#1-clothes-follow-the-body-at-every-joint)
- [2. Raising an arm moves the shoulder](#2-raising-an-arm-moves-the-shoulder)
- [3. Foot and shoe are one piece](#3-foot-and-shoe-are-one-piece)
- [4. Pose plan before generating](#4-pose-plan-before-generating)
- [5. Make a cover map before generating](#5-make-a-cover-map-before-generating)
- [6. Plan real motion first](#6-plan-real-motion-first)
- [Check](#check)

## 1. Clothes follow the body at every joint

This holds for every garment, not only a long dress.

- **A sleeve goes with its arm.** Draw the sleeve on the arm piece, with a round cap as wide as the
  sleeve. Never draw it on the shirt and patch the hole. A shirt with sleeves is a torso drawn without
  sleeves (rounded shoulders) plus each arm drawn whole with its sleeve, its cap under the shirt's
  shoulder. *Today:* the cut-out rig puts the sleeve on the upper arm and gives each garment region one
  owner (cut-out-puppet.md, "After building or changing a rig").
- **A trouser top bends across the hip.** It hangs on a pelvis bone (waist to hip joint), so it stays at
  the waist and does not turn with the thigh. *Today:* the cut-out rig skins a garment that reaches below
  the thigh root over the legs (`garmentLegFront`/`garmentLegBack`, with `hips` for the pelvis band;
  cut-out-puppet.md, "A garment over the legs"). A shirt that ends above the thigh root stays rigid.
  *By hand:* add an empty `pelvis` bone layer pivoted at the waist whose end is the hip joint, parent the
  thigh to that end, and `skin` the trouser top to `pelvis` and the thigh
  ([skin-weights.md](skin-weights.md)), so its rows blend from the waist to the thigh across the hip.
- **The seat belongs to the pelvis.** It is its own piece, held at the waist, bent part of the way with
  the near thigh; the thigh turns under it. *By hand:* parent the seat to `pelvis` and `skin` it with a
  small radius on `pelvis` and a wider one on the near thigh.
- **A skirt widens with the legs, and no leg shows outside it.** *Today:* the cut-out rig's garment
  helpers spread a skirt's hem with the forward and back thighs; draw it wide enough for the stride.
  Check it on the widest step of a contact sheet.
- **A shirt hem follows the torso.** It is the torso drawing's own lower rows, skinned to `spine` like the
  rest of the torso, never a separate rigid piece.
- **A pose that changes how cloth hangs is drawn.** Sitting folds a skirt over the lap and bends trousers
  across the hip; a rig cannot drape cloth. Draw the sitting lower body and swap it in mid-move (§6).
- **Sitting down in a skirt or long top:**
  - the skirt hangs straight on the way down, and takes the seated shape only as the seat takes the
    weight;
  - seated, the hem sags between the seat edge and the knee;
  - cloth never shows the thigh through it: push the cloth out along the thigh's top edge;
  - the hip folds at the crease, so the thigh's top never rises above the lap;
  - while the body leans, the far arm stays behind the body; in front it shows only as a sliver of skin
    at the waist;
  - fit the seat to the character: the seat at about knee height.

## 2. Raising an arm moves the shoulder

Past about 30° the collarbone turns up by about a third of the raise (the 2:1 shoulder rhythm). The shirt
between the neck and the shoulder is skinned to the collarbone, so its slope rises with it. The arm
rises from the shoulder top, never from the chest.

*Today:* `<side>ShoulderRaise` lifts the shoulder pivot, but nothing ties it to the raise: no preset keys
it, and the torso's slope does not follow it. Key `ShoulderRaise` with `UpperArmRaise` or
`UpperArmOpen` (0 up to about 30°, then rising with the raise). *By hand:* add an empty `collarbone`
bone layer from the neck base to the shoulder, child of `spine`; drive its `rotation` from the raise
(an expression or a `by` track: 0 below 30°, then about a third of the raise past it); parent the upper
arm to its end; and `skin` the torso's neck-to-shoulder rows to `collarbone` and `spine`.

## 3. Foot and shoe are one piece

The shoe hangs from the leg's real end, the IK end, not the IK target. A target out of reach leaves the
leg short of it, and a shoe hung on the target then separates from its foot.

*Today:* the cut-out rig parents the foot bone to the shin bone, so the shoe follows the solved leg.
*By hand* (a hand-built leg posed by foot targets, [character-motion.md](character-motion.md)): put the
shoe on the shin with an `attach` constraint at the shin's end
(`{"type": "attach", "target": {"layer": "<shin>", "position": <ankle>}, "rotate": true}`), or keep every
target within reach. Draw the sock and the leg to end along the shoe's collar, so no corner or gap shows
at the heel.

**The contact shadow stays under the feet.** It follows the feet (the foot targets), never the hips or
the character's root. As the sitter lowers onto the seat, keep the contact shadow under the soles.
The chair has its own shadow in the picture. Place it by an
expression from the placed rig's `leftFoot` and `rightFoot` sockets
(`ctx.composition:getLayer("<character>"):getSocket("leftFoot")`), the midpoint of the two at the floor
line, never by parenting it to the character layer.

**Hands and feet on both sides use the same art.** The far ones are copies of the near ones, darker.
Never take a hand from an edit that draws it in another style. *Today:* the cut-out rig draws the far
side in the near side's hue, only darker (cut-out-puppet.md, "After building or changing a rig").

## 4. Pose plan before generating

Plan the drawings before spending credits, and agree the plan with the user.

- For every move, list the parts that turn out of the picture plane: a hand that shows its palm, an arm
  swinging toward the camera, a raised arm that reshapes the shoulder. Each needs its own drawing. Parts
  that only bend in the plane do not.
- ASK (with `picsart_ask`, found as picsart-video-rules says, for any closed choice, a multi-select included, so the options are buttons the user taps, the recommended one first; then your host's own question tool, such as AskUserQuestion; only where all fail, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) every story question that picks a drawing: who they wave to, which way they walk, which
  outfits.
- List the exact edits and their credit cost (`picsart_preflight`), then SPEND (quote it in one line, then get the yes with `picsart_ask`, found as picsart-video-rules says, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", else your host's own question tool, such as AskUserQuestion; never as a typed question unless both fail; only then those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says) before generating.
  Prompts: [part-sheet-prompt.md](part-sheet-prompt.md).

## 5. Make a cover map before generating

For every part, write down what lies over it in any pose and the drawing that shows it whole. Then draw
each covered part complete, in its own group on the sheet, as if nothing covered it. Never leave a part
with a hole where something lies on it.

Make the map from the character's own picture, not from a list: a part needs a drawing only when, in this
picture, something lies over it and a move in the plot shows what is under it. A trouser cuff already over the
ankle needs no sock foot; a character who never speaks needs no mouth drawings. Write that reason beside each
drawing in the plan, before anything is generated.

| Part | Covered by | Comes from |
|---|---|---|
| far arm, far leg, far shoe | body, near limbs | copies of the near ones, darker |
| body | arms | the torso group, drawn without arms |
| head and neck | hair, collar | the head group, the neck carried down under the collar |
| trouser leg, seat | shirt hem, hand | the upper leg groups, drawn whole |
| sock foot | shoe | the lower leg group, drawn to the shoe's collar |
| skirt | hand, shirt hem | the garment group, drawn whole |

- Parts are drawn complete. No patched holes: a patch shows as a straight cut once the joint turns.
- **A hidden end stays under its cover.** When a part's hidden end (a thigh top under the hem, a shin top
  under the knee, a shoe top under the cuff, an upper arm's end under the forearm) is made from the part's own
  pixels moved along the limb, it is drawn only where the covering part lies over it at rest, inside the
  cover's outline shrunk by a few pixels.
  - Never move a copy of the whole part: it carries the part's other end along, and a second shoe shows beside
    the real one.
  - Never fill up to a fixed row: a row past the cuff's edge doubles the laces above it.
- **Past a joint, only a round end.** A part never reaches past its joint further than a disc of the limb's
  half width round the joint. This counts for its drawn pixels and its hidden end alike. A thigh top reaching far
  above the hip swings out behind the back as the leg goes forward. An upper arm's end past the elbow shows
  behind it as the forearm bends.
- **The neck is one part.** It belongs to the head piece, is drawn complete, and is carried down under the
  collar. Every body drawing (standing, seated or any other drawn pose) ends at the collar and carries
  no neck of its own. The neck's pivot sits inside the collar, so a nod or a bow never opens a gap or
  shows two necks. *By hand:* hang the neck from the `neck` bone with the head, pivot it inside the
  collar, draw it under the torso, and end every swapped-in body drawing at the same collar line.
- **Where parts join, the outline runs smooth.** No step, notch, gap or doubled line shows at any joint,
  at rest or at the extreme poses:
  - the part that goes under has a round joint end about its pivot;
  - the covering part's ink (cuff, collar, hem, shoe top) lies over the seam;
  - both outer lines match in width and colour and meet tangent;
  - parts that bend together are skinned as one mesh.

  *Today:* the cut-out rig's checks want a child's end round and centred on its pivot (cut-out-puppet.md,
  "After building or changing a rig", "Joints and views"). Check zoomed stills of every join at the
  deepest bend and at every swap frame.
- **Every limb is two pieces, whatever the style.** Upper and lower arm, upper and lower leg, each its own piece, overlapping at the joint. A one-tube, one-line or one-shape limb is refused; the style only chooses how the joint is hidden.
- **A joint bent past about 60° is a hinge, not a skin bend.** A skin bend that far pinches and loses
  volume. Draw it as two pieces with a round cap at the joint, each turned rigidly about its pivot. Check
  the widest pose zoomed in before sending.
- No baked shadows: leave the drop shadow out of the sheet and paint out what a cover casts on a hidden
  top.
- Joints come from the art: the shoulder at the centre of the arm's round top, the wrist at the top of
  the hand, the hip on the leg's middle. Every joint lies inside its part.
- An edit changes more than it was asked to. Take only what you need from it, near the part.
- *Today:* the cover map and the edits are planned by hand ([part-sheet-prompt.md](part-sheet-prompt.md)).
  From one picture, `picsart_scene_cut_parts` reports `hidden`, the pixels a turned joint shows; its plates
  and a `fill` from a masked edit cover only small turns, so a part hidden further is cut whole from a sheet.

## 6. Plan real motion first

Before keying a move, write down how a real body does it: which foot carries the weight when, where the
hips and head go, what leads and what follows. Then check it frame by frame.

- **A walk keeps one foot down.** Both feet are down for a moment at every step (double support),
  including the closing step; the back foot lifts only once the front one has landed. The hips sit only
  as high as the planted legs reach. A run is the opposite: both feet leave the ground. *Today:*
  `walk_cycle` and `acting`'s `walk` plant the feet and close with a step (`steps`, `from: "rest"`); check
  with `picsart_scene_check_motion` on the foot art and a contact sheet.
- **Size a walk on body height.** Same walk, same steps per height on screen. A short-legged character
  sized by its leg takes short, choppy steps beside an adult and reads as robotic. Every cut-out rig's leg
  is the same rig length, so scale `stride` and `lift` by each character's leg-to-height share.
- **A walking torso hardly moves.** A steady small lean, a level head. `walk_cycle`'s and `acting`'s walk
  rock the spine and head with the arm swing. If a review calls that robotic, key the walk's standard
  controls yourself with a steady `spineLean` and `headNod`, instead of the preset's walk (a second writer
  on a preset's names pops).
- **Swap a drawn pose mid-move, never on a still frame.** A wave, a turned hand or a sitting body is its own
  drawing. The rig turns part of the way toward it, the drawing takes over there and finishes the move,
  so both meet on the swap frame. A swap at the end of a move reads as a jump. *Today:* two layers with
  `step` opacity keys at the swap frame, or keyed `by` the dial ([head-turn.md](head-turn.md)).
  A rig cut from one picture fits each drawing onto its bone and shows it from 0.5 of its control:
  `picsart_scene_cut_parts`' `poses` ([cut-from-one-picture.md](cut-from-one-picture.md), "Drawn poses").
- **Nothing that is switched may look different.** On the swap frame the incoming drawing matches the
  outgoing one: the same side, size, colours, outline and joint angles. Compare the frames on either side
  of every swap before rendering.
- **Animate from a reference video** when a move is hard to key from memory (sitting down, standing up,
  a reach):
  1. Generate a short video of the same character doing the move, starting from its own picture.
  2. Take frames densely across the fast part.
  3. Measure per frame, as shares of the body's size: the waist height, the back position, and the
     cloth outline (from a colour mask).
  4. Key the rig's controls to those shares at those times.
  5. Before rendering, compare a still sheet of the rig with the reference frames, side by side.

  *Today:* `picsart_media_video_stills` takes the frames and `picsart_media_track_motion` tracks a point
  or a box; the colour mask is measured by hand. `picsart_scene_contact_sheet` gives the rig's stills.
- **Fix only the defect.** Change only the cause, and diff every animated value against the version
  before.

## 7. A limb is part of the body's silhouette

An arm grows out of a broad, rounded shoulder, and a leg out of a rounded hip, inside the same outline as
the body. It is never a thin stick or band laid on top of the body, and a folded arm is a bent limb of
the same thickness, not a sausage floating off the torso. Unless the reference draws a limb as a separate
tube, draw and judge it this way:

- **Thickness.** Measure the reference: the upper arm's width against the torso's width at the chest
  (for example about half), and the same for the thigh at the hip. The drawing keeps that ratio at every
  pose. A limb much thinner than the reference's is a defect even when its line is clean.
- **The join.** The limb's outline runs on into the body's outline at the shoulder or hip with no cut line
  across the join and no step where the pieces meet. Two pieces are fine (§5: overlap at the joint); the
  silhouette they make is one shape.
- **A hand and its arm are one shape with one outline.** One line runs under the fist and along the
  forearm to the elbow; the hand is never a second shape touching the arm's end.
- **No leftover inner lines.** When an arm is drawn out of the body's outline, delete that side's resting
  inner arm line from the body: a stray one reads as a cut across the join.
- **A folded arm.** The elbow swells out of the body's facing side, the forearm is a line across the
  chest, and one hand hangs at its end. A separate band with a fold line across it reads as a double hand.
- **Every pose drawing gets its own check.** A folded, raised or swung arm and a bent leg are each a new
  drawing, so each is cropped and compared as described in
  the `motion-review` skill ("Check each limb join").

## Check

Run the pose set and checks in cut-out-puppet.md, "After building or changing a rig": rest, each joint's
limits, the presets across their windows and both sides. Before that, look at every cut part alone on a flat
colour: a doubled shoe or a corner past a joint shows there first. Look in particular at the shoulder slope at a
full raise, the trouser top and seat at the widest step, the shoe at the heel peel and the landing, and
every swap frame. Read the bones with `picsart_scene_inspect` (`mode: "rig"`).
