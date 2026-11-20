# Picture cut-out

The one style built from pictures. Every character and animal, and every set, is generated as a picture (or is
the user's own), and each character is cut along its own drawn pieces into a puppet that walks and acts in
profile across a side-on stage. Every other style builds its characters from shapes or from SVG part sheets; this
one is for any look an image model can draw: storybook, paper craft, painted, shaded, textured. The flow is the
same in every look; the look is picked first and held for the whole film.

## Contents

- [What it is not](#what-it-is-not)
- [Looks](#looks)
- [Palette](#palette)
- [The medium](#the-medium)
- [Characters: plot first, then pictures](#characters-plot-first-then-pictures)
- [Animals](#animals)
- [Sets and props](#sets-and-props)
- [Motion habits](#motion-habits)
- [Cutting a light-edged look](#cutting-a-light-edged-look)
- [Faces](#faces)
- [Moving the set](#moving-the-set)
- [Camera](#camera)
- [Type](#type)
- [Sound](#sound)
- [Frame checklist](#frame-checklist-on-top-of-framemd)
- [Build with the tools](#build-with-the-tools)
- [Do / don't](#do--dont)
- [Originality guard](#originality-guard)
- [Proven on](#proven-on)

## What it is not

- Not a shape style ([simple shapes](simple-shapes.md), [cut paper](cut-paper.md), [the classic
  cartoon](classic-cartoon.md)): those draw figures from shapes in the scene. Here every piece is a picture, with
  the texture and shading the picture has.
- Not a part-sheet style ([painted anime](painted-anime.md) and the others whose `cast` is `rig`): their
  characters are built from SVG part sheets; here they are cut from pictures.

## Looks

Any look the image model draws can be used; the table holds the ones proven so far. Pick one with the user, from
the story's mood, or take the look of the user's own picture. Every picture after the first character's base passes that base as
its reference and repeats the look's style line, so the whole film keeps one hand.

| Look | Style line for every prompt | Where the cut goes | Shapes |
|---|---|---|---|
| Storybook | `clean dark grey rounded outlines, flat soft muted colours, simple shapes, light paper texture, no gradients, no realistic shading` | the dark outline round each piece | yes |
| Paper craft | `layered torn and cut paper and felt pieces, soft pastel colours, visible paper fibres and white torn edges, each body part its own paper piece` | the white torn edge round each piece; the joints show one paper piece over another. The cut tool cuts along it with `labels.regions.edge: "light"` ([Cutting a light-edged look](#cutting-a-light-edged-look)) | no |

The cut tool reads a look only when it sees each piece as its own area. Check the first base with
`seedMap: "base"` before anything else is generated (character-rigging's `references/picture-sheets.md`), with
`labels.regions.edge: "light"` for a light-edged look. A look whose edge is neither a dark line nor a light rim comes
back as one area: it is cut by hand, never drawn again for that. A new look joins this table once a character in it
has been cut, rigged and rendered.

## Palette

The look's own colours, read off the first base and set pictures and held for the film, with one warm hero colour
kept for the object the story turns on and nowhere else. Night and interiors darken the whole picture with a
grade, never by redrawing. Brand colours take clothes and set, never the hero.

- **Storybook:** flat soft muted colours under a dark grey outline (never black). Skies and grounds are
  pale, clothes a step stronger, so the characters read on the set.
- **Paper craft:** soft pastels under white torn edges.
  - Sky `#d8ecf1` and cloud `#d2e0ed`.
  - Hills `#aed5c3` and `#cce5ca`, grass strip `#bed4a6`, path `#dcc9bc`.
  - Felt crowns `#558e5d`, trunk `#824e30`.
  - Skin `#feceb5`, hair `#b0765d`, jumper `#b8c7d2`, jeans `#7b93b0`.
  - A bird in pale blue `#beceda` with a peach chest `#fee5d3`.
  - The warm hero is the sun's yellow paper `#fedfa6`, kept off the cast and the set.

These are the colours of the pictures, not values to fill shapes with: the image model draws them. Name them in a
prompt only to bring a later picture back in line with the first.

## The medium

- **Characters and sets are pictures.** Every character, animal and set comes from a generated picture or the
  user's own, never from shapes.
- **Shapes only where the look allows** (the `Shapes` column). A hand-drawn look with an even outline and flat
  colour (storybook) takes shapes for small things and effects: a sun, a cloud, a ball, a fruit, a falling leaf,
  rain, sparkles, a speech balloon. Each is drawn in the look's outline colour and width and its palette, so it
  cannot be told from the pictures. A textured look (paper craft, painted) takes no shapes: a flat vector piece
  shows at once; there every prop is a picture.
- **Pieces you can see.** The base prompt asks for the upper arm, the forearm, the thigh and the shin as pieces
  with round ends at the joints, which is where the cut goes.
- **Side-on stage.** Each set is seen straight from the side at a child's eye level with a flat, empty path across
  its lowest fifth: the floor line.
- **No cast shadow** in any picture. A grey studio background or a floor shadow is put right with one edit
  (`Same picture on a plain pure white background, no shadow under his feet. The boy unchanged.`) before any
  sheet is made from it.

## Characters: plot first, then pictures

Characters are cut with `picsart_scene_cut_parts` in side view facing right with `rig: "humanoid-side"`, from a
base picture and its sheets, as character-rigging's `references/picture-sheets.md` lays out. The order:

1. **Plan.** The plot is approved first, with every beat per character.
2. **Pose list.** One row per beat: the move, whether it stays in the picture plane, the picture it needs. A step,
   a point, a reach or a nod bends the cut pieces; a wave toward someone, sitting, a head turned to the viewer is
   a drawn pose. Agree the list, each prompt and its cost, with the plan.
3. **Base picture**, twice, keep the cleaner:
   > A character for a cut-out animation rig, <the look's style line>: <who: age, build, hair, clothes>. Full body, side view facing right, standing straight, legs straight, the near arm hanging with the hand beside the thigh, the top's hem a clear edge over the trousers, slim thighs and a rounded hip behind them, <plain
   > clothes>, no folds. Plain white background, no shadow. For a cut-out animation rig.
4. **Look at the base before ordering any sheet.** For each part, write what lies over it in this picture and
   whether a move in the plot shows what is under it. Order a sheet only when both are true, and say why next to
   its prompt. The list below is what a sheet can give, not a list to order:
   - `Same picture without arms.`: the body under a hanging arm, when an arm swings or rises.
   - `Same picture, with white socks instead of shoes.`: the ankle under a shoe's collar, when the character
     walks and nothing else (a rolled trouser cuff, a long skirt) already covers the ankle.
   - the leggings chain: the legs under a skirt, when the character walks.
   - blink and mouth sheets: only when the plot has a close-up or speech.
5. **Plot poses**, each one edit of the base: `Same picture, he raises his near arm and waves toward something in
   front of him, open hand up at head height. Everything else unchanged. For animation.`
6. **Cut, check, save** the character with every picture in `referenceImages`.

An "only his jeans and shoes, everything else removed" edit zooms in and loses the framing: never ask for a
garment alone. A cut with sheets refuses a part's `reach`. A leg cut by hand keeps its top under the jumper hem as a
hidden end (character-rigging's `references/cut-any-edge.md`).

## Animals

An animal is one base picture in the same craft, side view, facing the character it meets, on plain white:

> A single small bird for a 2D cut-out animation, drawn in exactly the look of the reference picture:
> <the look's style line>. A
> plump little bird seen exactly from the side, facing left, standing with its wings folded, on a plain pure white
> background. No ground, no shadow, no other objects. The boy in the reference shows the style only: do not draw him.

A bird that flies needs its wing strokes drawn: one edit of its base per stroke (wings up, wings down; the
prompts are in character-rigging's `references/picture-sheets.md`). A cut wing turned on its shoulder reads as a
folded wing waving, and lifting it shows the torn rim it lay on.
- Cut each flight picture whole and match it to the standing bird by the eye and the beak: scale by the
  beak-to-eye distance, place it at the eye.
- Swap the drawings every wingbeat (0.1 s), glide in on raised wings, and change to the standing pieces just
  before the feet touch. The cut wing only folds the last few degrees on landing.

## Sets and props

> Background picture for a 2D cut-out animation, drawn in exactly the look of the reference picture:
> <the look's style line>. The boy in
> the reference shows the style and the scale only: do not draw him, or any person or animal. Scene: <the place,
> seen straight from the side at a child's eye level, its pieces sized against the character>. A flat, level
> path runs straight across the whole picture and fills the lowest fifth; keep it plain and empty. No cast
> shadows, no text, no border.

16:9 for a held shot, 21:9 for a pan. A set that changes is an edit of the same picture. A prop is one picture on a
transparent background with the set as reference, or a shape where the look allows one.

## Motion habits

- Smooth at the scene's rate; the puppets never step on twos.
- One walk pace per height. Every character breathes; a blink only when the plot has its sheet, or when the eye is
  its own paper piece (below).
- Ambient life in the set: a cloud drifts, the sun turns slowly, the grass bends in the wind, a tree sways a few
  degrees about its trunk base. Each is cut out of the set picture over a filled plate, with what lies in front of
  it put back on top, at the set's own x and y scale. The grass bends over a mesh whose top rows lean in a
  travelling wave.
- A face made of separate paper pieces (eye, brow, mouth) acts without sheets ([Faces](#faces)).
- A flying animal flaps between drawn flight poses (wings up, wings down), not a cut wing turned on its shoulder.
- A drawn pose swaps in mid-move where both drawings match.

## Cutting a light-edged look

A look whose pieces are bounded by a light rim (torn paper, felt) is cut by `picsart_scene_cut_parts` with
`labels.regions.edge: "light"`, in the seed map and in the cut. `"auto"` reads the figure's outer rim and picks dark
or light. Each piece keeps its own rim, so it keeps its outline when it turns. What the rims do not part:
- **Pieces with no rim between them** stay one area: hair over the face (one head piece anyway), a hand lying on
  the trousers. The seed map's magenta walls show the gap. Draw a seam along the outline of the piece on top, on
  the sheet that shows it (`{sheet: "base", points}` for the hand), so it cuts no other sheet. Seed every
  area the loop closes off for the part it belongs to; the cut's "drawn by no part" warning gives the point.
- **Blocky paper legs** swung back come out behind the cloth over the hip. Ask for thighs at most two thirds as
  wide as the hip is deep, and always order the sheet without the top so the seat is cut from it
  (character-rigging's `references/picture-sheets.md`).
- **An arm the colour of the jumper** shows no change against a no-arms sheet, so `minus` finds nothing. Seed its
  areas on the base instead: the rims part it from the jumper.
- **One big area for pieces that must move apart** means the rim is too faint: cut those by hand
  (character-rigging's `references/cut-any-edge.md`).

After the cut, or for a hand cut:
- **Read the edge first** from the figure's outer rim: a dark ink line, a light rim, a line of another colour, or
  no line (only a change of colour). Cut along that, never assume ink.
- **A hidden end stays under its cover, and past a joint only a round end** (character-rigging's
  `references/character-rules.md` §5).
- **A cut cover takes its whole rim.** Lifting a piece (a wing, an arm) shows what it lay on. Fill the hole and
  the cover's torn rim with the piece below's own colour plus fine grain, inside that piece's outline. A rim left
  behind shows as a white line whenever the cover lifts.
- **Fill with colour and grain**, never with a mirrored tile (a repeating pattern) or an inpaint (a smear).
- **A cover is drawn above** every piece whose hidden end it covers. A head drawn over the jumper shows its
  hidden neck over the collar.
- Look at every piece alone on a flat colour, then at every joint's widest angle, zoomed in, before any video.

## Faces

A face drawn as separate paper pieces is cut by colour: the eye is the dark blob, the brow the brown strip, the
mouth the pink line. Fill the skin under each with the face's own skin colour and grain, and hang them on the
head, each on a joint at its centre:
- **Blink:** the eye squashes to a tenth of its height for 0.07 s, every few seconds.
- **Sees something:** the brows rise about a tenth of the eye height, then settle half way.
- **Happy:** the mouth widens (x 1.35) and stays as thin as drawn (y 1.1); the eye squints a little (y 0.7). A
  mouth grown in height thickens into a sneer.
- **Looks at it:** the head turns toward what it sees, on a neck pivot inside the collar (10 to 13 deg down
  toward the ground).

## Moving the set

A set picture is still. What moves in it (clouds, the sun, the grass) is cut out, its place filled, and what lies
in front of it put back on top. The engine draws all of it: a picture bends over a `mesh` whose `points` take
whole-list keyframes by time. No tool cuts a set picture into pieces yet, so do it by hand:

1. **Name what moves** and what lies in front of each (tree crowns over a cloud).
2. **Cut each piece** and check it alone on a flat colour:
   - **Cloud:** what its white torn rim closes round. Where a tree covers the rim, the tree closes the loop.
     Take the convex hull, and save it with a feathered halo of sky about 36 px wide, so its rim and cast shadow
     go with it and its edge never shows.
   - **Sun (a round disc):** fit a circle to the bright paper and cut exactly that circle. Its cast shadow stays
     on the plate; a disc cut with its shadow carries the shadow round as it turns.
   - **Grass strip:** cut by colour (the grass paper's green well above its blue, `g - b > 40`, in the band from
     the tallest blade down to the path). Its darker back blades come with it.
   - **A halo never carries another piece.** Cut every other moving piece out of a halo, or the cloud drags the
     sun's rim along.
3. **Fill the plate:** the set with each piece's place filled with the colour round it plus grain (sky from the
   nearby sky, hills carried along each row). Fill the grass blades **and the shadow they cast** (the grass mask
   grown about 16 px), or a leaning blade shows a dark copy behind it.
4. **Front layer:** the crowns in front of a cloud, cut by colour from the set.
5. **Layer order, bottom up:** plate, sun, clouds, front layer, grass, then the characters.
6. **Scale:** a set stretched to the frame has different x and y scales (2752x1536 into 960x540 is 0.3488 and
   0.3516). Every piece takes the set's own x and y scale and position; one uniform scale shows a piece's edge twice.
7. **Motion:**
   - Clouds drift about 20 px over the clip, toward what covers them, so their cut-away part never shows.
   - The sun turns 30 deg over the clip with a slight pulse (scale 1.035 every 0.8 s); a plain disc turning
     shows only its texture.
   - Wind bends the grass over a mesh: columns every 64 px, rows at the blade tops, the middle and the base;
     the top row moves fully, the middle 0.45, the base never. Each column's offset (content px) is
     `4 + 8 sin(2 pi t / 1.7 - x / 420) + 3 sin(2 pi t / 0.9 - x / 170)`, keyed every 0.2 s `ease_in_out`, so a
     gust runs along the grass. The vertices go row by row and each grid cell is two triangles. Every key of
     `points` lists all the vertices, the moved x with the same y.
8. **Stills at the start and end of the clip**, compared with the set and zoomed in, before the video.

## Camera

Held for a short scene, a slow pan along a wide set for a walk, a slow push in for the emotional beat. The floor
line stays level.

## Type

Captions only when the plan's words are captions: a rounded serif in the look's ink (on a torn paper strip in paper craft) at the foot of
the frame, clear of the floor line.

## Sound

Soft acoustic music (ukulele, glockenspiel, felt piano), foley for the look (a paper rustle in paper craft, a soft tap of
steps), birdsong.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Every picture and shape is in the one look, with the same line, colour and texture.
2. No gap, flap or white sliver at any joint in the widest pose, and no white line where a lifted piece lay.
3. Every character stands on the floor line at its height.
4. No cast shadow and no grey background fringe round any piece.
5. The hero colour is only on the story's object.
6. A moving set piece shows no second edge, halo or shadow copy at the start or the end of the clip.

## Build with the tools

1. **Pictures:** quote every batch with `picsart_preflight`, then generate with `picsart_generate`. Use Nano Banana
   2 (`gemini-3.1-flash-image`), 2K, with the first base as reference. Characters are 9:16; sets are 16:9, or 21:9
   for a pan.
2. **Characters:** `picsart_scene_cut_parts` on the base with `seedMap: "base"` first, then with its sheets and
   `poses`, `rig: "humanoid-side"`. Save each with `picsart_asset_save`, every picture in `referenceImages`. A
   light-edged look passes `labels.regions.edge: "light"` ([Cutting a light-edged look](#cutting-a-light-edged-look)).
3. **Motion:** walks come from the rig's walk action at one pace per height, never keyed by hand. Drawn poses swap
   in mid-move. The set's moving pieces follow [Moving the set](#moving-the-set).
4. **Check:**
   - Look at every piece alone, then the widest pose of every joint, zoomed in, before any video.
   - Run `picsart_scene_check_motion` on the walk.
   - Make a `picsart_scene_contact_sheet` across the film.
5. **Render:** `picsart_scene_export` at full quality.

## Do / don't

- **Do** pick the look with the user before the first picture, and pass the first base as the reference for every
  later picture.
- **Do** order a sheet or a drawn pose only when the plot shows what it gives, and say why beside its prompt.
- **Do** look at every result before building on it: a sheet that moved, changed the face, or came back on grey
  is drawn again.
- **Don't** put a flat vector shape into a textured look (paper craft, painted).
- **Don't** fly an animal on a cut wing turned on its shoulder: draw the wing strokes.
- **Don't** grow a mouth in height to make it smile: it widens.
- **Don't** leave a cast shadow or a grey fringe in any picture.
- **Don't** fill a hole with a mirrored tile or an inpaint. Use the colour round it plus grain.
- **Don't** scale a stretched set's pieces uniformly: use the set's own x and y scale.

## Originality guard

Draw your own characters and places. A tale may be a public-domain story; its look is never a known book's or
film's illustrations, characters or title design.

## Proven on

Storybook: a four-minute fairy-tale film with two children, their parents, an old woman, birds and a duck, each
cut from a base picture and its sheets, with drawn poses for sitting, beckoning and a look at the viewer.

Paper craft: a short scene. A boy walks in on the walk preset, and a bird flies in on drawn wing strokes and lands.
The boy smiles, looks down at the bird and waves. Clouds drift, the sun turns and the grass moves in the wind. All
of it was cut by hand along the white torn edges.
