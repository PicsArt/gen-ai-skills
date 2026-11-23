# Cut paper

Felt and paper pieces moved by hand under a camera: motion lands on twos, every pose sits a pixel or two off
where it should, like a piece nudged by a finger. Layered, shadowed, warm and a little busy.

## Finish

Everything on twos in a nested composition (`fps` 12 under a 24 fps root; far pieces `fps` 6), each piece with its offset shadow (see Motion habits); a title only if one is needed.

## Palette

Dusk, flat fills only: sky `#1f2a44`, moon `#f3e6c4`, cloud `#c9cfe0`, hills `#3b4a6b`, `#2f6b5e` and `#24503f`,
trees `#1d3d33`, bark `#6b4a35`. **The hero colour is the bird's warm orange `#e8823a` (wings `#c4612a`),
reserved for the subject** and never used on the world. For a warm daytime film swap in cream `#f3ead6`, mustard
`#d9a441`, teal `#3f9f9a` and pink `#f3a3bf`, keeping the same single hero.

## The medium

- Each object is one shape layer of flat fills with a `drop_shadow` effect (`offset [5, 7]`, `blur 9`,
  `#0000006e`): the shadow is what makes paper look layered. Every piece, character or place, uses the same
  shadow offset.
- Hills are closed paths with horizontal tangents; trees are two triangles and a trunk; clouds are a rounded
  rectangle plus two ellipses. A character is a few flat pieces (body, head, wing or limb, tail), no outline,
  a slightly different colour per piece, joints as pivots on pins so a limb turns about one point and shows a
  small overlap.
- A place is stacked paper layers (sky, far hills, near hills, trees), each with its own shadow, spaced so a
  slow slide shows them moving at different speeds.
- Full-bleed: a wall, a sky or a table fills the frame; a pattern (stripes, dots) clipped inside a piece adds
  paper you can feel.

## The character

Drawn from the style's own shapes, not a generated sheet (the mechanism, saving and talking are in [shapes-character](shapes-character.md)); build once, save once to the library, place it by its `uri` in every shot.

- **Proportions:** about 4.5 heads tall: a paper doll.
- **Shapes:** every part a closed polygon with a slightly ragged edge and a hard offset shadow copy under it; the joints are visible round pins (small circles) at shoulder, elbow, hip and knee.
- **Face:** two black dots, a mouth cut as one small paper shape; `mouth` rest, `aa`, `oh` as three cut shapes.
- **Controls:** act on fours (the 6 fps composition), so the figure steps like paper moved by hand.

## Motion habits

- **Everything on twos.** Put the stepped parts in a nested composition layer with `fps` 15 (12 under a 24 fps root; background pieces
  that should feel slower in another with `fps` 6) and key them with plain keys. No time-floor expressions. A piece that travels under a moving camera
  keeps its root travel continuous, outside the held composition; only its poses hold (*Hold the pose, not the travel* in the `scene-animation-reference` skill's held drawings).
- **Hand jitter** is the `wiggle` preset on each piece's layer id inside the nested composition, 1-2 px of
  `amount`, a different `seed` per piece. A redrawn outline is the `line_boil` preset on a piece's paths.
- Pops for things arriving (scale with a small overshoot), an ease-out for the moon rising, a bird that flies
  in on a curve, flaps a wing at about 4 Hz, lands, hops and tilts its head.
- Cued layers use `timeMode: "layer"`.

## Type

Usually none; if a title is needed, hand-lettered on a paper tag in a rounded grotesque, set late.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. A character with a face, acting, in the hero colour.
2. A full-bleed paper world: sky or wall, plus at least two overlapping layers with shadows.
3. Paper you can feel: shadow on every piece and at least one pattern or grain.
4. Three or more background-life details: twinkling stars, a drifting cloud, a moth, steam, bunting.
5. All stepped motion shares one rate, so the pieces stay in step.

## Build with the tools

Build each object as a shape layer with its shadow; group the stepped ones in a nested composition with `fps`
12; apply `wiggle` and `line_boil` with `picsart_scene_apply_preset` to the nested layer ids. Put everything in a
`scene` asset and add a light paper-grain look on the `scene_ref` of the whole.

## Do / don't

- **Do** give every scene its own dominant colour so it reads on a contact sheet.
- **Don't** fade a piece with opacity to hide it (the shadow reads as a ghost): move it off frame or cut it;
  don't blend two wall colours (mud).

## On a part sheet

The shapes character above is the route for this style; this note is only for a user who brings a generated sheet. When a character comes through the SVG part-sheet flow (the `character-rigging` skill), every arm and leg is two pieces, an upper and a lower, each its own group, overlapping at the elbow or knee. That is a rig requirement no style overrides: the builder refuses a sheet whose limb is one piece. Draw each limb as two paper pieces, upper and lower, overlapping at the joint with a pin dot there; the style shows its pinned joints, so the overlap and the pin are the look.

## Originality guard

Invent the world and the animal. It must not resemble a known clay or puppet-film hero, his dog or a studio's
plasticine character sheet, a known paper-cut film's creature, forest or title treatment, or a famous
storybook illustration's composition. The method (twos, jitter, shadows) is the style; the characters are new.

## Proven on

The moon-bird scene (dusk hills, stars, a bird that flies in, lands and hops, film grain on the `scene_ref`).
