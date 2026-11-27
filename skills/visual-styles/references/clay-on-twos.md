# Clay animation

Plasticine moved a little at a time: soft rounded lumps with a thumbprint shine, a trembling outline, and every
second frame held. Gentle and slow.

## Finish

The whole piece set on twos in one nested composition (`fps` 12 under a 24 fps root) with the `line_boil` outline boil (see Motion habits).

## Palette

Backdrop a pale gradient `#a9d6e5` to `#e8f1ef`, leaf `#6aa84f` with a vein `#3d6e2c`, body `#f2c57c`, spiral line
`#7a3e1d`. **The hero colour is the shell's burnt orange `#c0632f`, reserved for the one thing the eye should
follow** and used nowhere in the set.

## The medium

- Every lump is one shape layer of a single flat fill, made soft by three effects in this order: an
  `inner_shadow` pushed up (`offset [0, -10]`, `blur 14`, `#00000066`), an `inner_shadow` light from below
  (`offset [0, 8]`, `blur 10`, `#ffffff59`), and a `drop_shadow` (`offset [0, 10]`, `blur 16`, `#00000055`).
  Give every piece the same three.
- Shapes are fat and rounded: a body is a closed path with tangents on every point, a stalk is a thick round-cap
  stroke ending in an eye of one white ball and a dark pupil, a shell is a disc with a hand-drawn spiral stroke.
- No outline. The edge is the shade.
- The place is a few big soft shapes (a leaf, a vein) under a pale backdrop.

## The character

Drawn from the style's own shapes, not a generated sheet (the mechanism, saving and talking are in [shapes-character](shapes-character.md)); build once, save once to the library, place it by its `uri` in every shot.

- **Proportions:** about 3 heads tall: soft lumps.
- **Shapes:** a rounded-rect or ellipse for every part, limbs as thick sausages of the body's own fill with round ends that grow out of the body, a hand being the sausage's rounded end, all in **one shape layer per character** so the three clay effects run over the whole silhouette and no edge crosses a limb join; the boil rides the outer silhouette only, never an outline per part; and a faint thumbprint arc.
- **Face:** two bead eyes, brow lumps, a bean mouth; `mouth` rest, `aa`, `oh` as three bean shapes.
- **Controls:** act on twos (the 12 fps composition); squash and stretch ride `spineLean`.

## Motion habits

- **On twos is a nested composition.** Put every clay piece in one `composition` layer with `fps` 15 inside a
  30 fps root (12 inside a 24 fps root) and key it with plain keys: a linear position for the crawl, eased rotation keys that alternate
  direction for the sway of the stalks and shell. No time-floor expressions. A piece that travels under a moving camera
  keeps its root travel continuous, outside the held composition; only its poses hold (*Hold the pose, not the travel* in the `scene-animation-reference` skill's held drawings).
- **Handling jitter** is the `wiggle` preset on each lump (`frequency` 24, `amount` about 1.6, `angle` 0.6), a
  different `seed` per piece. **Outline boil** is the `line_boil` preset (`rate` 12, `amplitude` 2-2.5) on the
  leaf and the vein.
- Apply every preset to the layer ids inside the nested composition, never to the composition layer.
- Slow: a crawl of a few hundred pixels over the whole shot, with no squash at each step.
- Cued layers use `timeMode: "layer"`.

## Type

Usually none; a title is a chunky rounded sans in a plain colour on the backdrop, set late and still.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Every lump has the same three shading effects and no outline.
2. Everything stepped sits in the one nested composition at `fps` 15 (12 under a 24 fps root).
3. The shell is the only burnt orange.
4. The frame is not still: a crawl, a sway and the wiggle together.
5. Three or more small lumps of background life (a bud, a pebble, a bug).

## Build with the tools

Make the pieces as shape layers with their effects, group them in one nested `composition` layer with `fps` 15,
then apply `wiggle` and `line_boil` with `picsart_scene_apply_preset` using the nested layer ids. Put a film-grain
look on a `scene_ref` of the whole picture, not on the nested composition.

## Do / don't

- **Do** vary the lump sizes; clay reads from lumps that are not the same.
- **Don't** add a hand-written time floor, an outline, or a hard black shadow; don't put the grain look inside the
  stepped composition.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Rate split: everything drawn steps at 12 in the one nested composition (see Motion habits); the grain look and any
    camera move run at the root rate on the outer `scene_ref`.
  - Boil: the creature's outer silhouette (the `wiggle` on each lump) and the leaf and vein (`line_boil`), at the held
    rate with a fixed seed per piece; the backdrop gradient, the thumbprint arc, any title and the camera stay still.

## On a part sheet

The shapes character above is the route for this style; this note is only for a user who brings a generated sheet. When a character comes through the SVG part-sheet flow (the `character-rigging` skill), every arm and leg is two pieces, an upper and a lower, each its own group, overlapping at the elbow or knee. That is a rig requirement no style overrides: the builder refuses a sheet whose limb is one piece. Draw each limb as two pieces, upper and lower, in the same clay colour, overlapping at the joint, so the overlap reads as one soft limb with a gentle fold.

## Originality guard

Invent the creature and the world. It must not resemble a known plasticine duo or hero, his dog, a studio's
sheet of clay characters, or a named stop-motion series' set. The method (twos, trembling, soft shade) is the
style; the creature is new.

## Proven on

The clay-snail film (a snail crawling along a leaf, stalks and shell swaying, wiggle and line boil, on twos).
