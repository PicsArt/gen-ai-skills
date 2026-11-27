# Cutting a picture along its own edge

Every look bounds its pieces with something:
- a dark ink line (storybook, cartoon);
- a light rim (torn paper with white fibres, felt, a sticker's white border);
- a line of another colour (a brown or coloured outline);
- no line at all, only a change of colour (painted, flat vector).

`picsart_scene_cut_parts` separates pieces along dark lines and, with `labels.regions.edge: "light"`, along light
rims. This page is the procedure for cutting any other edge by hand (a short image script), and a light rim the tool
leaves as one area, worked out on a paper-craft look, and the mistakes made on the way. Pictures come first ([picture-sheets.md](picture-sheets.md)).

## Contents

- [Read the edge first](#read-the-edge-first)
- [Pictures](#pictures)
- [Cut, step by step](#cut-step-by-step)
- [Hidden ends and round ends](#hidden-ends-and-round-ends)
- [Covers and holes](#covers-and-holes)
- [Faces](#faces)
- [Animals](#animals)
- [The walk](#the-walk)
- [Rig](#rig)
- [Check](#check)
- [Mistakes made (do not repeat)](#mistakes-made-do-not-repeat)

## Read the edge first

Read the figure's outer rim, the band 3 to 12 px inside its silhouette. Compare its median colour with the colour
deeper inside:
- **`dark`** when the rim is dark (lightness under about 90);
- **`light`** when it is light and grey (lightness over 200, saturation under 45);
- **`change`** when it is no different from the inside;
- **its own colour** otherwise.

Look at a zoomed crop where two pieces meet and agree with the reading before cutting. One look keeps one edge
for the whole film, so every later character or prop in it is cut the same way.

| Edge | Walls are | Watch for |
|---|---|---|
| dark | pixels darker than their 8 px surroundings, or near-black | inner detail lines (a pocket, a fold) are walls too: seed both sides or close them |
| light | pixels brighter than their 8 px surroundings (by about 9) and unsaturated (under 60), or near-white | white parts of the art (a sole, a collar) read as walls: add them back by position |
| a colour | pixels within about 45 (summed channels) of that colour | a part of that same colour reads as a wall |
| change | the strongest 8 % of the smoothed colour gradient | shading steps read as walls; two touching parts of one colour have no wall: split them by a line along the drawn edge |

## Pictures

- **The base:** one picture in profile on plain white, with no floor shadow.
- **A no-arms edit:** checked at 0 px shift.
- **Drawn poses:** one edit for each pose the plot needs (a wave, a sit).
- **Legs need no sheet** when each leg piece is already drawn whole: a thigh piece whose round end lies over the
  shin, a rolled cuff over the shoe.

## Cut, step by step

1. **Figure.** Everything away from the background's colour (the median of the picture's border), closed and
   holes filled, and the largest area only.
2. **Floor shadow off.** In the lowest tenth of the figure, drop the pale cool pixels (blue at least red, every
   channel above about 205). A cast shadow is grey-blue; a white sole is warm. Look at the feet on a flat green.
3. **Walls.** The lines for the edge read above. Drop specks of texture under about 600 px, then look at the wall
   picture: every piece must be closed by a wall.
4. **Seeds.** Lay a numbered 100 px grid over the picture and read one or two points inside each piece.
5. **Pieces.** Flood the area round each piece's seeds, bounded by the walls (grown 2 px), and fill its holes.
   Then add its own edge band, the wall pixels within about 14 px. The line belongs to the piece it surrounds, so
   a piece keeps its outline when it turns.
6. **A wall with a gap.** Where two pieces of one colour meet with a faint edge, the flood runs into both. Split
   that piece by a straight line along the drawn edge (a wave arm's upper arm from its forearm, a wing from the
   body by a polygon along its outline).
7. **Tint each piece a colour and look at them together.** No piece may run into its neighbour.
8. **Body.** The body without arms comes from the no-arms edit, and the torso is the body above the jumper hem.
   The arm pieces come from the base, and a drawn pose's pieces from its own edit.
9. **Joints.** Each joint is the centre of the round end of the piece that turns on it, on that piece's axis (the
   axis and half width read from its pixels). The hip goes on the thigh's axis just under the hem. The neck pivot
   sits inside the collar.
10. **Hidden ends, round ends, holes** as below.
11. **Save each piece** as a transparent picture cropped to its box, with a 1 px soft edge, and keep its box: the
    rig places it by that box.

## Hidden ends and round ends

- **A hidden end stays under its cover.** A piece's part under the piece that covers it is made of the piece's
  own pixels moved along the limb. That covers a thigh top under the hem, a shin top under the thigh's round end,
  a shoe top under the cuff, an upper arm's end under the forearm, and a neck under the collar. Draw the moved
  pixels **only where the cover lies over it at rest**, inside the cover's outline shrunk by about 8 px.
  - Never move a copy of the whole piece: it carries the other end along, and a second shoe shows beside the
    real one.
  - Never fill up to a fixed row: a row past the cuff's edge doubles the laces above it.
- **Past a joint, only a round end.** On the side toward the neighbouring piece, keep only a disc of the limb's
  half width round the joint. This counts for the piece's own pixels and its hidden end alike. A thigh top
  reaching far above the hip swings out behind the back as the leg goes forward. An upper arm's end past the
  elbow shows behind it as the forearm bends.

## Covers and holes

- **A cover is drawn above** every piece whose hidden end it covers. A head drawn over the jumper shows its
  hidden neck over the collar.
- **A cut cover takes its whole rim.** When a cover is cut away from the piece below (a wing off a body, a
  separate eye off a face), the hole includes:
  - every pixel within about 30 px of the cover that is not the piece below's own colour;
  - any white within about 90 px;
  - all of this only inside the piece below's outline (the convex hull of its own colour).

  A rim left behind shows as a white line whenever the cover lifts.
- **Fill a hole with the colour round it plus fine grain** of the paper's strength. A mirrored tile shows a
  repeating pattern; an inpaint smears into a blur.

## Faces

A face drawn as separate pieces (eye, brow, mouth) is cut by colour:
- **Eye:** the dark blob near the eye point.
- **Brow:** the brown strip above it.
- **Mouth:** the pink line.

Fill the skin under each with the face's own skin colour and grain. Hang each piece on the head from an empty
layer at its centre, so it can be squashed, raised or widened on its own:
- **Blink:** the eye squashes to a tenth of its height for 0.07 s.
- **Brows:** they rise and tilt a little.
- **Mouth:** a smile widens it (x 1.35) and keeps its thickness (y 1.1). A mouth grown in height thickens
  into a sneer.

What the face shows, and when, is the general acting rule: [cartoon-film.md](cartoon-film.md) §4 "Acting
from the plot". The head turns on the neck pivot inside the collar.

## Animals

- **A moving part** (a bird's wing) is cut from its one picture with its whole rim, and the body under it is filled.
- **To fly, draw the wing strokes** (wings up, wings down). A cut wing turned on its shoulder reads as a folded wing
  waving.
- **Cut each flight picture whole** and match it to the standing animal by the eye and the beak: scale by the
  beak-to-eye distance and place it at the eye. The eye is the dark blob (every channel under about 110) in the
  head; the beak tip is the yellow pixel furthest forward.
- **Swap the drawings every wingbeat** (0.1 s), and glide in on raised wings. Change to the standing pieces just
  before the feet touch; the cut wing only folds the last few degrees on landing.

## The walk

- **Never key a walk by hand.** A walk keyed from made-up angles takes steps twice as long as the approved one.
- **A hand-cut puppet is not on the standard controls yet.** Its joints are plain empty layers, so the catalogue
  presets (`walk_cycle`, `wave`) do not drive it. Solve its legs every frame to the approved walk's feet with
  two-bone IK (knee forward), and key the joint angles. Hold the stance foot planted and use the walk's own step
  length and timing. A cut made by `picsart_scene_cut_parts` is mapped onto the rig and walks with `walk_cycle`.
- **The shoe is its own piece on the ankle,** so the heel peels and the planted foot stays flat.
- **Size the walk on the body's height.** Every character walks at the same pace for its height.

### Solving the legs each frame

1. **Feet first.** Each foot's ankle point follows the approved walk's feet. It is planted, then rolls over the
   toe, then swings to its next plant.
2. **Knee.** It is the point a thigh length from the hip and a shin length from the ankle. Of the two such
   points, take the one in front (knee forward).
3. **Angles.** These are measured against the rest picture's own thigh and shin directions:
   - thigh = the hip-to-knee angle minus its rest angle;
   - shin = the knee-to-ankle angle minus its rest angle, minus the thigh's;
   - shoe = the foot's roll minus both.

   Rotations are clockwise and relative to the parent joint.
4. **Key every frame** on the joints' empty layers.

## Rig

- **One root per character** at the hip, scaled to its size on screen. Its children are placed relative to the hip
  in picture pixels. An empty layer per joint carries the rotation, and each piece is an image layer under its
  joint.
- **Layer order.** The first layer in the list is drawn at the bottom. From the bottom up:
  - the set;
  - the far leg (the near leg's pieces again, about 30 px back, the same colour);
  - the near shin under the thigh, and the shoe under the cuff;
  - the torso over the thigh tops, and the head under the jumper;
  - the arm.
- **Keyframes** not driven by a parameter take `time`, not `at`. The easings are `linear`, `ease_in`,
  `ease_out`, `ease_in_out` and `step`.
- **A drawn pose is swapped in mid-move** (character-rules §6). Its pieces hang from their own joints at the
  rest shoulder. On the swap frame the rig is half way and the drawing is turned back by half. Use step opacity.

## Check

1. Every piece alone on a flat colour, zoomed: no second shoe, no strip of a neighbour, no white line, no shadow.
2. The assembled puppet at rest against the picture.
3. The widest angle of every joint: the walk's longest step both ways, the arm swing both ways, the raised arm,
   and the wing up. Zoom in at the joints.
4. Only then the video.

## Mistakes made (do not repeat)

| What showed | Why | Fix |
|---|---|---|
| a second shoe beside the real one | the shin's hidden top was a moved copy of the whole lower leg | the hidden end only inside the cover's outline |
| doubled laces above the cuff | the copy was limited to a fixed row below the cuff's edge | the same |
| a stub behind the back | the thigh's hidden top reached 270 px above the hip | only a round end past the joint |
| a white line under a raised wing | the wing's torn rim stayed on the body | the hole takes the cover's whole rim |
| a smear, then a repeating pattern, under the wing | an inpaint, then a mirrored tile | the colour round it plus grain |
| a doubled collar | the head was drawn over the jumper | the cover above the hidden end |
| a rude mouth | the smile line grown in height | the mouth only widens |
| steps twice as long as the approved walk | a walk keyed from made-up angles | the legs solved to the approved walk's feet |
| one big area from the cut tool | the look's edge is a light rim | `labels.regions.edge: "light"`; by hand if it still finds one area |
| two pieces in one area of the seed map | the light rim breaks where they meet: a gap in the magenta wall | a seam across the gap, on the sheet that shows it (`{sheet, points}`) |
| a thigh's top shows behind the top when the leg swings back | a thigh as wide as the hip, and no seat cut | thighs at most two thirds of the hip's depth; cut the seat from the sheet without the top |
