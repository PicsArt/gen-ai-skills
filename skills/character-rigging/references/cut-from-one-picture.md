# A cut-out puppet from one picture

One picture of a figure (a person, an animal, a creature) becomes a paper puppet:
`picsart_scene_cut_parts` cuts each part once to its own transparent picture, meshes the parts that
bend, and saves them as a scene in the user's Drive. Bones and `ik` pose them. Part ids and the parent
tree are free-form. With aligned sheets and `rig: "humanoid-side"` it builds a side-view character
rig on the standard controls ([rig-controls.md](rig-controls.md)), with drawn poses for what the skin
cannot bend into.

Use it when the user has one finished picture of the character. A part sheet of named SVG groups is
built by `picsart_scene_build_model` instead ([cut-out-puppet.md](cut-out-puppet.md)). Every character
still passes [character-rules.md](character-rules.md).

## Contents

- [Input](#input)
- [Cut strategy](#cut-strategy)
- [Reading pixel coordinates](#reading-pixel-coordinates)
- [Cut](#cut)
- [Refusals](#refusals)
- [Cut from aligned sheets](#cut-from-aligned-sheets)
- [The first call](#the-first-call)
- [Drawn poses](#drawn-poses)
- [Who covers whom](#who-covers-whom)
- [After the cut](#after-the-cut)
- [Gate](#gate)
- [Deliver](#deliver)

## Input

Every picture is a Picsart-hosted https URL: an upload from `picsart_drive_upload_ask` (`accept: 'image'`), or a generated
image's `url`. A local path or a `data:` URI is refused. The tool cuts **a figure with a continuous dark
outline and a drawn line at each joint**, flat or softly shaded. A picture without that outline (a
photo, loose painting) does not separate into parts: draw it again to the spec below, or tell the
user it cannot be cut.

- A continuous dark outline, 3 px or more at 576 px wide, any dark hue, solid.
- Each joint is a drawn boundary: a sleeve seam, a waistband, a hem, a sock or shoe top, where a leg
  or a tail joins an animal's body.
- A person in front view stands in a neutral A-pose: arms about 35° out and clear of the body, legs
  apart, hair short or above the shoulders. An animal is in side view, its legs apart and its tail
  clear of the body.
- Soft shading is fine. Dark texture strokes, hatching and cast shadows are not: each reads as
  outline and splits a part.
- A transparent background (`picsart_image_remove_bg`).
- A drawn picture's prompt names the build, the hair and each garment with its colour, from the look the user gave
  or chose. Each character in a cast has its own main outfit colour from the style's palette; blue is never the
  default.

Ask for two pictures and pick one: one often adds what nobody asked for. Draw again rather than edit
shadows out, since an edit changes the clothes. Keep the base pose neutral and raise an arm in the rig:
an arm drawn raised above about 30° opens the flank behind it.

**An accessory as its own layer.** A masked edit of the picture adds a hat or a scarf. Pass it as
`accessory` (`image`, `mask` in picture px, the part it sits `under`): the tool keeps only what changed
inside the mask and cuts what the edit turned into background from that part.

## Cut strategy

Cut only what the shot needs. Each cut part costs its seams, a plate and a gate; an uncut part moves
only as far as its mesh stretches.

- **Uncut** (one meshed body, skinned to bones): clean up to a shoulder of about 8°, a lean of 14° and
  a head turn of 8°. Enough for breathing, a nod, a sway, talking.
- **Cut** an arm that waves or crosses the body, a leg that steps, a head that turns further. Keep the
  torso and head uncut for acting.
- **Partial cut.** Name the body in `labels.regions.rest` and seed only the parts you cut. The rest
  part keeps every unseeded region and comes back meshed; the cut parts hang from it. Seed every piece
  of a cut part (a hand behind a cuff line), or it goes to the body.
- **Plates long enough.** A turned upper arm must never come off the shoulder: gate the widest angle
  the shot uses.
- **Hidden areas.** A plate or filler is flat fill colour, which shows as a flat patch on shaded art.
  The answer's `hidden` is a mask of exactly those pixels, black where an edit may paint. Make a masked
  edit of the picture with it ("continue the shirt under the arm, same shading, no arm") and pass it
  as `fill`.
- **A part the seeds cannot reach.** Give it whole in `labels.masks` (a mask or a full-size layer).

## Reading pixel coordinates

Seeds, seams, pivots and bend points are the picture's own px. Get its size from `picsart_media_probe`.

- **Seeds.** Call the cut with `seedMap: "base"` first: a dry run that numbers the picture's fill areas
  over a 100 px grid and returns a point inside each, and the numbered picture to look at. Nothing is
  saved. Read the seeds off it.
- **Pivots and bends.** Look at the joints closely: a scene 400 px square with the picture as a
  `media` layer (`fit: "none"`, `anchor` `[0, 0]`, `position` minus the crop's top-left corner) and a
  1 px grid every 50 px over it, drawn with `picsart_scene_contact_sheet` at `resolution`
  `{width: 800, height: 800}`. A crop that size reads to a few px.

Put a **seed well inside its region**, 15 px or more from any outline (a button or a fold line is
outline too). A part split by folds or buttons needs a seed in each piece. Put a **pivot in the middle
of its joint**, not at its edge, and a **bend's `at`** on the joint's crease, halfway across the limb.
The answer's `warnings` names a pivot or a bend off its middle and the point to move it to.

## Cut

Call `picsart_scene_cut_parts`; never write a cutting script. Give each part seed points
(`labels.regions.seeds`). A limb is ONE part, seeded in every region it holds (a sleeve and a hand),
and its joints inside (an elbow and a wrist) are its `bends`. A person's leg is one part down to the
ankle, and the shoe is its own part. Name a person's parts as the standard rig's layers so its
controls fit.

**Edges.** Parts are bounded by dark outline ink by default. A paper-craft look whose pieces are edged
with a light torn rim instead of ink takes `labels.regions.edge: "light"`; `"auto"` reads the figure's
outer rim and picks one, and the answer's `summary.edge` says which: `dark`, `light`, or, when the rim is one colour, `{ colour, tolerance }`. An outline band may be up to three times its thinnest
outline along the silhouette, and two bands may meet between two areas, as wide as those areas' own outlines together; any other wider
band is a fill. See [cut-any-edge.md](cut-any-edge.md).

**Depth layers.** `bands` (with `image` alone, no `labels` or `parts`) cuts a picture into depth layers by masks you give, each with a
thin local plate under the edge of the layers in front, so the layers can drift apart (parallax) without a hole. `bands.layers` go
back to front (the first is farthest; reversed, the depth inverts); each is a `mask` (a PNG the picture's size, white where the layer
is; `maskConvention: "black_paint"` flips it) or a `polygon` of [x, y] points in picture px; at most 16. What no layer holds is the base
layer, `baseId` (default `back`). `bandPx` is the plate's width under each edge (default 40), at least the drift; `drift` is the shift
the `check` preview uses (default half of `bandPx`, at most `bandPx`). Measured on one sharp picture at 1024 px wide: 24 px of drift
left a soft smear where a band crosses bright windows, so keep close-ups to 12-16 px; soft backgrounds untested.
A picture is held to a pixel budget that shrinks with the layer count: 16 layers take up to
about 3.0 megapixels (1728 px square), 1 layer about 6.5; a larger one is refused, naming the size that fits.

**A depth map instead of masks.** `bands.depthMap` is an 8-bit grey PNG you made, the picture's size, bright = near (a colour map is
refused, a bright-far one is warned about); no model runs in the tool. It cuts only the far part, at the empty valley of the depth
histogram, as the base `far`; everything else is `ground`, never sliced, and any `layers` you add (optional then) are nearer; a mask keeps
all its px. The answer's `depth` gives the valley and each mask's median depth as numbers, never a band name. It refuses
`depth_far_unclear` when the valley is not empty, there is no second peak, the far part is under 5%, or over 8% of px sit within 0.03 of
the cut (a ramp, not a gap): then give masks. The check misses a wall, a floor ramp and a table. It counts the budget above as one
layer more, and the map is held to it too. A `depthMap` cut puts `ground` behind every mask of yours, so a layer in band `mid` cannot
come from it (`band_order`; reordering cannot help): cut `mid` with masks only, no `depthMap`.

**Where a cast stands.** `bands.floor` `{ row, horizon?, figure? }` is the floor a standing figure's feet are on: `row` the floor row
(image px), `horizon` the row it vanishes at (at least 1 px above `row`), `figure` a standing adult's height at `row` (default 0.9 of
`row - horizon`). `check` gains a fourth panel: the floor line (yellow), the horizon (cyan) and, when there is a horizon, four standing figures (magenta boxes). Look
at it once and correct the numbers: a stated `horizon` is used as given. With `depthMap`, an accepted far cut and no `horizon`, the horizon is
measured from the map and reported in `floor.measured`; it refuses `floor_unclear` when no floor line or a believable horizon is found, and then you state `horizon`.
It counts as one layer more in the budget above. What a character stands behind or on is cut as an object (a mask each, named, in
`layers`): a bench, a table's near edge, not left in the ground (a flat rug stays in the picture, see below).

**The server's depth model.** `bands.depth: true` (not with `depthMap`) has the server write the map, then cuts as above with a stricter
bar (valley at most 0.09, else `depth_far_unclear`). The answer's `depth.map` is the map (a URL, bright = near). A run takes about 3 s and
runs alone, so a second call may be refused as busy: retry. Without the model: `depth_unavailable`, give `depthMap` or masks.

**A picture as a place.** `picsart_scene_build_place` with `picture` lays the cut out as a 2D place for a camera move, with no SVG.
The place is as large as the picture and its rest frame crops it: for a large move cut a bigger picture than the shot needs. Cut two or three bands (`far`, `mid`, `ground`; `front` or `sky` only when the picture has one),
one mask each, back to front; the base is the farthest band, or the `sky` (`baseId: "sky"`, not in `layers`), which does not move.
1. **Ask for the ring.** `picture` with `width`, `height` and `layers` of only `id` and `band`, plus `travel` (`{ x: 20 }`), answers
   `bandPx` and `baseId`; with objects the ring is a few px wider (an object's order step slides it a little against its band's art under a pan), so
   ask with the object ids in `layers`. Pass them to the cut; never guess. Keep the pan to about 12-16 px on a close-up.
2. **Cut** with `bands`, that `bandPx` and `baseId`, and read its `check`. The cut grows every mask 3 px so a mask inside an edge does
   not hand the edge's dark px to the plate behind it; look at the frames at the extremes of the move.
3. **Build.** The same call with each cut layer (`id`, `content`, `transform`, and `ownBox` on an object) plus its `band`, and `floor` where the
   cast stands: the object `bands` answered as `floor` (`{ row, horizon?, figure? }`, passed whole; a bare number is refused). It becomes the
   sockets `floor`, `horizon` and `crown` (`row - figure`, the head of a standing adult) on the ground band. An `id` that is not a band name is an object
   under its band, ordered by its base (`z` is 0.02 per row of `base`: the bottom of its `ownBox`, or a stated `base`; lower in the picture is nearer). The answer is the place scene by `sceneUrl` (and `order`, each object's `{ id, base, z }`), with the `travel` the
   picture allows (finite, limited to what the ring fills): stay inside it. Key `world`'s pan as in an SVG place; a camera push does
   not replace the place's own crop.

**A character in a picture place.** From a place built with `picture` and `floor` (its `floor`, `horizon` and `crown` sockets), put the rig
on the floor with `picsart_scene_apply_preset` `motionPreset:on_floor` and `params: { at: [x, row], size?, start? }`, `at` the foot point in
picture px. It sets the character's scale by the floor law (`figure * size * (row - horizon) / (floor - horizon)`), parents it to an empty
`<id>_depth` under the ground band that carries its depth step (half a row nearer than an object whose base is that row) and undoes the
depth, so the layer's own position and scale stay plain picture px. A later `start` adds a mark the layer jumps to in one frame. Order the
work: `on_floor` first, then `acting` with `travel: "in_place"` (and `sitFeet: "planted"` for a sit, no later marks). It refuses
`layer_travels`, `acting_sits_planted`, `floor_socket_missing`, `floor_horizon_missing`, `rig_unknown`, `layer_id_taken` and
`layer_fit_stretch`. Leave flat floor pieces (a rug, a mat) in the band's picture, or give the piece `base` its far row in `picture`: cut as an object,
a rug's base is its front edge and it would hide a character standing on it. A shot over 10 s needs the rig's `content.parameters.duration`
(`on_floor` binds it) or the figure freezes at 10 s. After a `jump` with `landY`, mark the landing row with `on_floor` at the landing time. Check it with
`picsart_scene_lint_layout` `relationships: [{"kind": "on_floor", "members": [{"id": "kid"}]}]`: the foot inside the floor's picture, the drawn height the
floor law's, and the paint order against the bases of the objects it overlaps; most findings name their fix. Airborne frames of a hop are not
checked.

**Seams**, where the figure has no outline between two parts, drawn across the whole gap from outline
to outline. A person needs up to 6: each shoulder (sleeve into shirt), the hip line, between the legs
down to the crotch, and each ankle. Skip one where the picture already outlines it (a cuff, a belt).
An animal needs one where a leg or its tail runs into the body unlined. With `sheets`, a bare polyline
cuts every sheet; `{sheet, points}` cuts only that sheet (`base` is the picture), as in
[Cut from aligned sheets](#cut-from-aligned-sheets).

**Starting values**, read off the grid:

| Field | Start at |
|---|---|
| `reach` (a part behind runs under the front part, px) | foot about 0.3 × the ankle's width; hips 0.15 × the hips' width; head 0.22 × the neck's width |
| `radius` (the plate's disc about the pivot) | leave it out; 0 where the part behind runs on sideways past the joint (hips under a torso) |
| `cap` (a front part copies its parent around its pivot) | about a third of the upper arm's width at the shoulder seam |
| `spacing` | leave it out |
| filler `radius` | about 0.6 × one leg's width |

**A front view** does not hold yet at the sleeve and the elbow (a white rim or a fold at the crease):
for a film, cut a side or three-quarter view, or cast a front-facing character from a part sheet. When a
front view is cut, look at the bent elbow closely in the Gate. It is best cut partially: `rest: "body"` keeps the head, torso and skirt or shorts one
meshed body, and the arms and legs are cut. Each arm is `front` with a `cap`, its pivot near the
middle of the shoulder seam. Each leg starts at the hem, behind the body, down to the sock or shoe top,
with a knee bend. Each shoe is its own part with a small `reach`, so it stays flat on the floor.

```json
{ "image": "<the picture's url>",
  "labels": { "regions": {
    "rest": "body",
    "seams": [[[217, 372], [214, 298]], [[357, 372], [360, 298]]],
    "seeds": {
      "rightArm": [[185, 395], [155, 480], [140, 540], [120, 580]],
      "leftArm": [[390, 395], [425, 480], [440, 540], [450, 578]],
      "rightLeg": [[230, 760], [225, 835]], "leftLeg": [[345, 760], [352, 835]],
      "rightFoot": [[215, 876], [197, 948]], "leftFoot": [[365, 877], [390, 948]] } } },
  "parts": [
    { "id": "body", "pivot": [288, 560] },
    { "id": "rightArm", "parent": "body", "pivot": [208, 340], "front": true, "cap": 25,
      "bends": [{ "id": "elbow", "at": [166, 472] }, { "id": "wrist", "at": [133, 565] }] },
    { "id": "leftArm", "parent": "body", "pivot": [366, 340], "front": true, "cap": 25,
      "bends": [{ "id": "elbow", "at": [415, 470] }, { "id": "wrist", "at": [443, 565] }] },
    { "id": "rightLeg", "parent": "body", "pivot": [235, 700], "bends": [{ "id": "knee", "at": [232, 775] }] },
    { "id": "leftLeg", "parent": "body", "pivot": [340, 700], "bends": [{ "id": "knee", "at": [345, 775] }] },
    { "id": "rightFoot", "parent": "rightLeg", "pivot": [222, 878], "reach": 14 },
    { "id": "leftFoot", "parent": "leftLeg", "pivot": [352, 878], "reach": 14 } ] }
```

That is a 576 × 1024 front A-pose. The two seams are the shoulders; the hems, sock tops and shoes are
drawn, so the legs and feet need none. Each foot's pivot is the ankle, on the shoe top.

**A three-quarter view**: `front` on the near arm and leg, `cap` where the near shoulder turns in
place, `reach` where a part behind runs under a long front edge, `overlaps` for the near leg over the
far one, and a `fillers` crotch piece behind both legs. The far arm has few pixels: keep its swings to
about ±30° and give gestures to the near hand.

**A four-legged animal** in side view: `rest: "body"` keeps the head in the body; the far legs and the
tail draw behind it; each near leg is `front` with a `cap` and a seam where its top runs into the body.

The answer's `check` rebuilds the parts at rest. For a cut from the picture alone, `uncoveredPx` and
`differingPx` must both be 0; when they are not, look at its `overlay` picture: it marks the pixels. A
cut from sheets differs from the picture wherever a sheet redraws a part (an aligned cut can differ by
tens of thousands of pixels and be right), so read the `overlay` instead of the numbers: the marked
pixels must lie only on parts a sheet redrew, and `uncoveredPx` must still be 0.

## Refusals

Each names the input to change.

| Code | Fix |
|---|---|
| `seed_on_ink` | Move the seed a few px into the fill. |
| `seed_off_figure` | The seed is on the background: read its px again on the 1:1 grid. |
| `seeds_share_region` | Two parts' seeds meet in one region: add the seam between them. |
| `seam_cuts_nothing` | Draw the seam across the whole gap, outline to outline. |
| `region_unseeded` | A region larger than 2% of the figure has no seed: seed it, seam it, or name the body in `rest`. |
| `pivot_outside_part` | With `rig`, the pivot lies outside the part in front: move it to the point the message gives. |
| `order_cycle` | `overlaps` and the parent order contradict: drop or flip one overlap. |
| `part_empty` | A part or filler has no pixels: seed the part in its own region; move or widen the filler. |
| `accessory_empty` | The edit changed nothing inside `mask`: check the mask is in picture px. |
| `unsupported_image` | Not an 8-bit grey or RGB PNG: convert it. |
| `invalid_argument` | A field is malformed or a point lies outside the picture; the message says which. |

## Cut from aligned sheets

When the picture hides part of a part (the torso under the arms, the legs under a skirt), pass
`sheets`: edits of the same picture by name, each with one change (the arms removed, legs drawn
instead of the skirt, the eyes closed). Each part is then cut whole from the sheet that draws it.
Where the part in front holds a joint's pivot, the part behind runs on under it about the pivot, in its
own fill colour and hidden at rest, so two parts that only meet along an outline (a top's hem over the
trousers) both hold the joint. Seeds name their sheet (`{sheet, points}`; `base` is the picture), and `minus` cuts a
part as its sheet minus another (hair: the picture minus the bald sheet). `overlaps`, `fillers`,
`accessory`, `fill`, `rest` and a part's `cap`, `reach` and `radius` are refused with sheets.

- **Seeds.** `seedMap: "<sheet>"` numbers that sheet's areas and draws the walls between them in
  magenta. A wall with a gap (a broken rim, a hand lying on the thigh) leaves two parts in one area:
  close it with a seam on that sheet, then seed.
- **Pictures for a side rig** come from [picture-sheets.md](picture-sheets.md): every sheet a
  "Same picture ..." edit of the profile base (without arms, without the top, without hair), each thigh
  at most about two thirds as wide as the hip is deep, and always the sheet without the top. Paper
  craft takes `edge: "light"`; no outline at all: `edge: "fill"`.
- **Pivots on a flat-cut top.** A part cut flat at its top (a T-shirt sleeve at the shoulder, a leg at
  the seat seam) has no round end above its pivot: put the pivot a half-width below the cut. A
  `rig_refused` round-end refusal names a pivot both drawings cover when there is one: move it there.
- **Seams per sheet.** Cut the seat on the sheet without the top by a seam across the hip just below
  the hip pivot, with the leg's seeds below it; cut a hand off the thigh by a seam round the hand on
  the picture only. Each as `{sheet, points}`, so the hip seam leaves the picture's hand whole and the
  hand seam leaves the seat whole. A seam loop (round a hand on the thigh) closes off areas of the part
  behind it: seed each one for the part it belongs to (`{sheet, points}`), or it shows as a pale patch at
  rest. The warning "N px around [x, y] are drawn by no part" names such an area: seed that point.
- **Alignment.** A part is cut only from a sheet at 0 px shift from the picture. `alignment` gives each
  sheet's shift, and `sheet_misaligned` names a shifted one: draw that edit again.
- **Smooth edges.** Draw the picture and its sheets antialiased, no smaller than they play, on a
  transparent background. Cut every part another part overlaps from a sheet that draws it alone. Keep
  a limb one width from joint to joint, with round ends.
- **Sheets for a side rig.** Ask for each edit as "Same picture, ..." with one change, so it aligns:
  the arms removed (the torso and both legs drawn whole where the arm lay); the top removed (trousers
  or skirt drawn up to the waist, the seat whole), chained on the sheet without arms so no hand lies
  over the seat or thigh; the hair removed (the head and ear whole). In the
  picture, draw the profile standing straight, the near arm hanging with the hand beside or on the
  thigh, the legs straight, and the top's hem a clear edge over the trousers. Ask for each thigh at
  most about two thirds as wide as the hip is deep, with the hip rounded behind it: a thigh as wide as
  the hip (blocky paper-craft legs) swung back comes out behind any cloth over the hip, so the rig
  keeps that seat rigid and the thigh turns under it. So always generate the sheet without the top
  and cut the seat from it: with no seat over the hip, a top over the hip is the garment, and blocky
  thighs swung back fail its check. Paper craft or any art with a pale rim instead
  of ink: `edge: "light"`.
- **Seams per sheet.** A seam may name its sheet (`{ sheet, points }`; a bare polyline cuts every
  sheet). Cut the seat on the sheet without the top by a line across the hip just below the hip pivot,
  with the leg's seeds below it; cut the hand off the thigh on the picture by a seam round the hand.
  With `rig`, the cut gives the seat a round back over the thigh's top and runs the thigh round under it.
- **Side rig.** `rig: "humanoid-side"` also builds a profile rig on the standard controls, saved as the
  answer's `sceneUrl`. Its parts are `hips` (the root), `torso` and `leg` under the hips, `head` and
  `arm` under the torso, `foot` under the leg and an optional `hair` under the head; the arm bends
  `elbow` then `wrist`, the leg `knee`. `swaps` give the blink and mouth pictures and `features` the
  pupil and brow. A seat cut over the hip stays rigid, and so does the torso over it; the seat gets a
  round back over the thigh's top and the thigh turns under it. With no seat, a top over the hip is
  fitted as a garment, and thighs as wide as the hip fail its check when swung back. Limb pieces run
  past their joints in the picture's own pixels, so textured art shows no streak at a bent joint. A
  paper-craft side rig builds in about 11 seconds; the call stops after 30. Read `model.notices`.
- **A side-rig call.** For a profile with the sheets `noarms` (without arms) and `notop` (without the
  top), every point read off that sheet's `seedMap`:

  | Part | Seeds (`sheet`) | `pivot` and `bends` |
  |---|---|---|
  | `hips` (root) | one point in the seat, above the seat seam (`notop`) | the middle of the pelvis, above the hip joint |
  | `torso` | one point in the top (`noarms`) | the waist; `front: true` |
  | `head` | one point in the face (`base`) | the middle of the neck |
  | `arm` | one point each in the upper arm, the forearm and the hand (`base`) | the centre of the shoulder's round top; `front: true`; `elbow` midway, `wrist` at the top of the hand |
  | `leg` | one point in the thigh below the seat seam and one in the shin (`notop`) | the hip joint, on the thigh's middle line; `knee` on the knee's crease |
  | `foot` | one point in the shoe (`notop`) | the middle of the ankle |

  And two seams, each naming its sheet:
  - `{ "sheet": "notop", "points": [...] }`: a straight line across the hip just below the leg's pivot,
    from past the back of the hip to past its front. It parts the seat from the thigh.
  - `{ "sheet": "base", "points": [...] }`: a closed loop round the hand where it lies on the thigh. A
    bare loop also cuts `notop` and leaves a hole in the trousers.

  Each point seeds one part: a point given to two parts, or a leg point above the seat seam, makes the
  hips draw the whole leg.
- **Check the answer before rigging.** Look at the `hips` piece: a seat with a round back that ends just
  below the hip, never a whole leg. The leg's `platePx` is above 0, because the thigh's top runs on
  under the seat; 0 means no seat was cut. Act on every warning: move each pivot once to the point it
  names, and seed each area that "N px around [x, y] are drawn by no part" names.

## The first call

Plan the parts, dry-run every map, write the call, check it, then read the answer and fix it once.

**How the cut sees a picture.**
- **Areas.** The picture splits into areas of fill bounded by rims. `labels.regions.edge` says what a
  rim is: `dark` ink lines (the default), `light` a pale rim (paper craft, felt, a sticker's white
  border), `fill` no outline at all (pieces parted only by their fill colours: flat vector, a thin
  faint rim, soft painted edges), or `auto` when unsure ([cut-any-edge.md](cut-any-edge.md)).
- **Parts.** A part is the areas its seeds land in. An area no seed lands in goes to `rest`, or is
  reported as "N px around [x, y] are drawn by no part".
- **Sheets.** A sheet is the same picture, aligned px for px, with one thing removed, so what it covered
  is drawn whole. Seed each part on the sheet where it is most whole.
- **Seams.** A seam is a line drawn where two parts share one area (no rim between them).
- **Pivots.** A pivot is where a part turns on its parent. It lies inside both pieces, and the parent
  runs on under the child's round end; the sheets draw that hidden end.

**1. Plan the parts from the motion.** List only what moves on its own in the story (a waving arm, a
turning head, walking legs). Ask three questions of each part, and use as few sheets as you can: one
sheet can uncover several parts.

| Question | Yes → |
|---|---|
| Does something cover it in the pose? | a sheet with the cover removed; seed the part there |
| Does it share one area with its neighbour (no rim between)? | a seam on the sheet you seed it on |
| Does it lie on top of another part? | seed it on `base`; if the map shows the two as one area, a closed loop round it on `base` |

**2. Dry-run every map.** Call `seedMap` on `base` and on each sheet, in parallel, with the same `edge`.
If a whole figure comes back as one or two areas, the `edge` is wrong: change it before anything else.
Read every point off these maps, never off the picture.

**3. Write the call.**
- **Seeds:** one point per area a part owns, on the part's sheet (`{ sheet, points }`). A point serves
  one part only; a part split by a seam is seeded only on its own side.
- **Seams:** always name the sheet (`{ sheet, points }`): a bare seam cuts every sheet. A straight seam
  starts and ends on the background. A loop closes on itself, about 4 px outside the part it frees, a
  point every 15–25 px.
- **Pivots and bends:** in the middle of the joint, 8 px or more inside both pieces. A round end (a
  shoulder, a hip) pivots at the centre of its curve; a part cut flat at its top (a T-shirt sleeve, a leg
  at the seat seam) pivots a half-width below the cut.
- **`front: true`** on a part drawn over its parent (an arm over the body).

**4. Check before calling.**
- `edge` matches the rims, and the maps show each part as its own areas.
- Every point lies inside a numbered area of the sheet it names.
- No point serves two parts, and no seed sits on the wrong side of its seam.
- Every seam names a sheet; every loop is closed.
- Every pivot lies inside both pieces it joins.

**5. Read the answer, fix once.**

| What you see | Cause | Fix |
|---|---|---|
| A part carries a neighbour (hips with a whole leg) | a seed crossed a seam, or the seam is missing | move the seed, or add the seam |
| Scraps of a neighbour on a part | its loop runs inside the part | move the loop about 4 px out |
| A notch in a neighbour | the loop runs inside the neighbour | move the loop about 4 px in |
| A part cut on another sheet too | a bare seam | name the seam's sheet |
| `platePx` 0 where a part should run on under another | the sheet or seam did not uncover it | seed that part on its sheet, below the seam |
| `pivot … → [x, y]` | the joint is off its centre | move it to that point, once |
| "N px around [x, y] are drawn by no part" | an unseeded area | seed it for the part it belongs to |
| `rig_refused`: a joint outside its piece, or a round end short of 95% | the pivot at a piece's edge, or above a flat cut | move it to the pivot the refusal names; with none named, inward to the joint's centre |
| `sheet_misaligned` | the sheet drifted | generate that sheet again from the base |

A second round on the same part means a seed or seam is on the wrong sheet: check the sheet names first.

**Views.**
- **Side** (`rig: "humanoid-side"`): cut the near arm and the near leg; the rig copies them as the far
  ones. Sheets: without the arms, and without the top made from the sheet without the arms, so the seat
  and waist are whole and no hand lies over the seat or thigh.
- **Front or three-quarter:** this tool builds no rig for them. Cut both arms and both legs as parts of
  their own (a seam between the legs on the sheet without the top), and build the hierarchy yourself.
- **A skirt or dress:** no seat. The legs come out below the hem; the sheet is "without the skirt".
- **An animal, a prop, any shape:** the same three questions for each moving part.

**A side-rig call.** A profile in trousers with the sheets `noarms` and `notop` (the top removed from
`noarms`), every point read off that sheet's `seedMap`:

| Part | Seeds (`sheet`) | `pivot` and `bends` |
|---|---|---|
| `hips` (root) | one point in the seat, above the seat seam (`notop`) | the middle of the pelvis, above the hip joint |
| `torso` | one point in the top (`noarms`) | the waist; `front: true` |
| `head` | one point in the face (`base`) | the middle of the neck |
| `arm` | one point each in the upper arm, the forearm and the hand (`base`) | the centre of the shoulder's round top; `front: true`; `elbow` midway, `wrist` at the top of the hand |
| `leg` | one point in the thigh below the seat seam and one in the shin (`notop`) | the hip joint, on the thigh's middle line and above the seat seam; `knee` on the knee's crease |
| `foot` | one point in the shoe (`notop`) | the middle of the ankle |

Why each piece is there: the top covers the seat, so the hips are seeded on `notop`. Seat and thigh share
one area there, so a straight seam on `notop`, across the hip just below the leg's pivot, parts them. A
hand resting on the thigh in `base` that the map shows as one area with it is freed by a closed loop on
`base`. Check the answer before rigging: the `hips` piece is a seat with a round back that ends just
below the hip, never a whole leg, and the leg's `platePx` is above 0 (the thigh's top runs on under the
seat; 0 means no seat was cut).

## Drawn poses

A pose the skin cannot bend into (a skirt seated at 90°, which wedges; a fist) is drawn as its own
picture and passed in `poses` with the rig. Each entry names the rig `part` it replaces (`hipsArt`,
`rightHandArt`), the `control` that shows it from 0.5, the `drawing` URL, and `landmarks` (drawing
points and where each lands on the rig) or a `reference` map. A negative `reference` scale mirrors it,
and `level` levels a line (a lap) before the fit. Switch only where both drawings match or the piece is
hidden. The answer's `poses` gives each fit and its landmark errors in bone px: a large error is a
wrong landmark.

## Who covers whom

- A child draws behind its parent unless it is `front`. `overlaps` name seams that are not joints
  (the near toe over the far heel). The part in front owns the seam's outline; the part behind gets a
  plate under it, so a turned joint shows no gap.
- **Feet.** A shoe is its own part, drawn behind the trouser leg and hung from the leg's real end (the
  shin, the IK end), never from the foot target: a target out of reach leaves the leg short of it, and a
  shoe hung on the target separates from its foot ([character-rules.md](character-rules.md), section 3).
- **Legs in a front view.** Animate the hips; each standing foot stays locked on its target. The knee
  bends toward the camera, so a crouch shortens the thigh and shin; it does not swing them out.
- **Acting.** Drive the body from the hips and let the limbs follow, as [rig-controls.md](rig-controls.md)
  says. Ease every move, hold each pose a moment, and keep a breath under every hold.

## After the cut

The scene at `sceneUrl` is the parts at rest on a canvas the picture's size, in draw order: an empty
root `puppet` at the root part's pivot, then one `media` layer per part with its `anchor` at its pivot,
its `parentId`, and its `position` in its parent's px. A part with `bends` carries a mesh with a `bend`
per joint at angle 0: drive their `angle`s. Every layer names its part's hosted picture.

Add the bones the pose needs (`spine`, `neck`, foot targets) with `picsart_scene_patch`. A part moved
under an empty bone takes `position` = its pivot minus the bone's pivot. A leg's `ik` names its knee,
with `min`/`max` on the pole's side. Check each sign with one still before keying a clip.

## Gate

Key rest and every extreme pose at its own time, on a magenta (`#ff00ff`) background so anything
see-through shows, and look at them in one `picsart_scene_contact_sheet` call: rest, lean forward and
back (`spine` ±8°, `neck` ±10°), a crouch, arms forward (near arm 30°, elbow 90°), arms back, the
near hand raised beside the head, and a step. Then look closely at every joint (neck, shoulders,
elbows, wrists, hips, crotch, knees, ankles) with a crop scene. Crop one elbow bent about
90° close, on magenta: a white rim or a fold at the crease shows only there. Look for:

- a hole or an opening at a joint that rest does not have;
- a stray fragment, a part in two pieces, or a part stretched into a strip;
- a flat patch on shaded art (pass a `fill`);
- a bare edge with no outline, a fold inside a bent joint, a tilting foot or a foot off its target.

None may be wider than a hair (about 0.1% of the figure's height). Then follow
[character-rules.md](character-rules.md)'s Check.

## Deliver

The puppet or rig is already a scene in Drive at `sceneUrl`, its part pictures hosted. Place it as a
scene asset (`{type: "scene", uri: <sceneUrl>}`) on a `scene_ref` layer anchored bottom-centre with
`blending: "pass_through"`, and pose it only through parameters. The answer's `ground` is the figure's
lowest row: its soles stand there. Save an accepted character with `picsart_scene_library_save`
(`kind: "character"`) so every scene places it by its `library:` uri.
