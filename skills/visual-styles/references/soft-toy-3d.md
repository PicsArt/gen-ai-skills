# Soft toy 3D

A small pastel diorama of glossy toy plastic: a board of hexagonal tiles that pop up ring by ring from the centre, a
pair of meshed gears on a panel, a few rounded boxes that squash and bounce, little round trees, all lit softly under a
lilac-to-peach sweep while the camera sways about 17 degrees either side. It is a real 3D scene, not a flat illustration of one.
A calm object to look at, not a character piece and not a product turntable.

## Palette and colour roles

| Role | Colour | Its one job |
|---|---|---|
| backdrop | `#d9cdf7` at the top to `#ffe1cf` at the bottom | the pastel sweep behind the toy |
| tiles | grass `#8ee3a8`, sand `#ffe08f`, soil sides `#ffd6bc` | the board, two soft tops over a peach side |
| stand | lilac `#b9a4f2` | the backboard and rail the gears sit on |
| gears | pink `#ff8fae` (12 teeth) and mint `#6fd8c4` (8 teeth), hubs `#ffd36e` | the one moving machine |
| boxes | rose `#ff9fbd`, lilac `#c7b4ff`, apricot `#ffc493` | the squashing toys on the tiles |
| trees | crown `#4fc27a`, trunk `#e0a07a` | small round punctuation |
| shadow | ground `#9d86c4`, shadow only | soft lilac shadows, never grey or black |
| light | key `#fff4ea`, fill `#e8dcff`, rim `#ffe9d6`, ambient `#fff1e6` over ground `#e6d6ff` | a warm key, a cool fill, a peach rim |

Hero colour: the pink gear `#ff8fae`. Everything else is a pastel kept lighter or calmer, so the one machine reads first.

## The medium

- **Plastic is a material override, not a texture.** Set roughness about 0.32 and clearcoat about 0.55 on every
  material (`materials: {"*": {...}}`; ours, tune by render). Pieces are rounded: bevelled tiles, rounded boxes, round gear hubs.
- **Light is a studio rig** (preset `studio`, key intensity about 2, fill 0.45, rim 0.8, ambient 0.35) with a soft key
  shadow (softness 0.6) and a shadow-only ground in lilac, plus one `ambient_occlusion` effect for the contact darkening.
- **The backdrop is a two-stop gradient**, lilac above to peach below. It bands a little; keep it soft.
- **The toy is one model** with its parts named so parameters can move them: tiles `hex_NN`, gears `gear_a` and
  `gear_b`, boxes `box_N`.
- **Gears mesh from one parameter.** One `turn` value in degrees drives the big gear by `+1` and the small one by
  `-1.5`, so their teeth stay engaged.
- **Squash roughly keeps volume:** a box's y scale goes from 1 to 0.55 as its x and z scales go from 1 to 1.3 (about 0.93 of
  the volume at the bottom of the press, which reads as soft, not as a leak).

## Rates

| Held rate | Root rate |
|---|---|
| none | everything: gears, squashes, camera sway |

## Boil

None: the pieces are solid and the surfaces smooth.

## Line width under a zoom

There are no outlines. The camera sways slowly, so edges stay as clean shaded forms.

## Motion habits, and the transitions

- **Build-in.** One `build` parameter from 0 to 1 over about 2.7 s pops the tiles up ring by ring from the centre: each
  tile goes from a speck to 1.06, with its height to 1.18, then settles to 1, each starting about 0.11 s later than
  the one before (0.75 of the build over 19 tiles). Bind points are linear, so an eased pop needs extra points on the curve.
- **Gears** turn at 60 degrees a second for the whole clip.
- **Boxes** press down and spring back in turn, each on a 1.6 s period a third of a period apart, the press lasting a
  third of the period on a half sine.
- **Camera** sways about +-17 degrees (0.3 radians either side of 0.5) once over the 8 s clip, and the sway closes, so the
  camera itself loops; eye height is fixed, looking a little above the board.
- Nothing fades. The build-in breaks a strict loop: the clip ends on a built toy, not on its first frame.
- Transitions between toys: the board shrinks tile by tile in reverse ring order, or the camera pushes in on the gear
  panel.

## Type

None by default. If a title is wanted, a small rounded sans in a deep lilac `#4a3a7a`, in 2D over the 3D frame.

## Scene features used

How the proof was built, optional: a 3D composition (`space: "3d"`) with one `model` layer, `materials` overrides, `parameters` with `bind` lists
(`node:<name>.scale.x[...]`, `rotation.z[...]`) driven by keyframes and expressions, a composition `camera` with an
expression for the eye, `lighting` and `environment` presets, a shadow-only `ground`, and the `ambient_occlusion`
effect. Motion blur with 8 samples smooths the squashes.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. The build starts from a speck on the centre tile on frame 0; the last frame shows the whole board.
2. The gears stay meshed in every frame: no tooth crossing.
3. The pink gear is the strongest colour; the rose box stays lighter than it.
4. Shadows are lilac and soft; no black.
5. The camera sway never lets a tree leave the frame or an object cross the panel.
6. Nothing sits outside the board's edge except the shadow (a tree peeking past it at 2 to 4 s is the known gap).

QC: lean on a contact sheet across the build-in and the viewer's pass at normal speed.

## Build with the tools (how the proof was built, optional)

The proof modelled the pieces in a modelling tool with named nodes (tiles, gears, boxes, trees) and exported one `.glb`,
then declared its parameters with `bind` lists, placed the model on a 3D composition and set the camera, lights and
ground, and checked the squashes and the build-in on a contact sheet before the final export. Any route that keeps the
palette, the plastic, the light and the frame checklist is fine.

## Do / don't

- **Do** name every moving part in the model so its parameter can find it.
- **Do** keep every colour pastel and the hero the strongest.
- **Do** keep the camera move small and slow.
- **Don't** use hard black shadows or a grey ground.
- **Don't** add a texture to fake gloss: it is the material's roughness and clearcoat.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Rate split: everything runs at the root rate; nothing is held.
  - Nothing fades: pieces pop in by scale, nothing changes opacity.
  - Height is shadow: every piece casts a soft lilac shadow on the ground and takes ambient occlusion where it touches.
  - Boil: none.

## Originality guard

Design your own board, gears, boxes and wording. It must not copy a known toy, set or product render. Pastel plastic
hex tiles, meshed gears, squashing boxes and round trees are the style.

## Proven on

An 8 s landscape clip (1280 by 720, 24 fps): a hexagonal board (19 tiles) with a two-gear panel, a few squashing boxes and
some trees (the counts are the proof's, not a rule), built from one `.glb`, lit by the studio rig with ambient occlusion and a swaying camera; baked locally
(the terminal exporter cannot play a local bake), not on the hosted renderer.

**Not proven:** the pieces come from a model `script` (a list of calls, see `scene-3d-authoring`) because `picsart_scene_build_model` has no gear, hex tile or rounded box
of its own: a hex tile is a 6-vertex `cylinder`, a rounded box a `cube` with a `BEVEL` modifier, a gear a `cylinder`
with a `cube` tooth `duplicate`d at each angle, a ring of trees `duplicate` lines, with no loops, so each is written out (a toy kit is
the real enabler); bind responses are linear, so eased pops need extra points; the build-in breaks a strict loop; the
backdrop gradient bands a little; a tree peeks past the board at 2 to 4 s; the stage editor (not tried); a
character among the toys and a second board.
