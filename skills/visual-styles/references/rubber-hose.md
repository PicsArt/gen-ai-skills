# Rubber hose

An early-sound-era cartoon: limbs are tubes of one width, the body is a simple solid shape, everything bounces
on one beat. Cream paper, black ink, one mid tone.

## Finish

The character on twos in a nested composition (`fps` 12 under a 24 fps root), a title card first and an iris last (see Motion habits and "below"). The `analog_film_finish` look on the one `scene_ref` of the cartoon, light (`grain` about 0.2, with `paper` and `dust` as in "Build with the tools"), over the cream paper.

## Palette

Paper `#efe3c8`, ink `#1b1612`, mid `#7d6d57`, light `#c9b896`, white `#fbf6ea`. The look is black and cream;
eye whites and the face are the white. **The hero colour is a single tomato red `#d8452e`, reserved for one
accent on the subject** (a scarf or a flower) and used nowhere else.

## The medium

- **Limbs are strokes.** An open two-point `path` with tangents and a `stroke` of 15-17 px, `lineCap: "round"`:
  the curve is the bend, there is no joint.
- The body is one solid (a black bean or pear) with a few white details. The head is a white disc with a black
  outline, two pie-cut eyes (a small black ellipse offset inside a white one), a nose blob and a wide curved
  mouth stroke. Hands are the tube's own end swelled into a round mitten in the body colour, one shape with the arm; feet are round black shoes with a white
  highlight. Give the character an invented hat or tail.
- A place is rolling ground with a bouncing horizon, trees and houses without faces, props that bob on the beat
  (lamp post, fence, cloud). The line weight matches the limbs. Ink outline on every object, no gradients, the
  same cream paper under everything.

## The character

Drawn from the style's own shapes, not a generated sheet (the mechanism, saving and talking are in [shapes-character](shapes-character.md)); build once, save once to the library, place it by its `uri` in every shot.

- **Proportions:** about 3 heads tall: a big round head over a small oval body, tube limbs of one width.
- **Shapes:** a circle head, an oval body, limbs as thick round-cap strokes in ink with no elbows or knees; a hand is the tube's own end swelled into a round mitten in the same ink (one shape with the arm, no glove and no white), shoes are ink ovals; everything is solid ink with no separate outline.
- **Face:** pie eyes (a white circle with a black wedge cut out), a small oval nose, a grin as one arc; `mouth` rest, `aa`, `oh`.
- **Controls:** add `bounce` (a squash of the whole body on the beat) to the base set.

## Motion habits

- **One beat drives everything**: two hops a second. Limbs and body share the beat; the head follows a beat
  behind. Squash the body on landing, shrink a shadow ellipse under the feet as the body rises.
- Step the drawing on twos: put the whole character in a nested composition layer whose `fps` is 15 (12 under a 24 fps root) and key it
  with plain keys; the stepped look comes from the nested rate, not from expressions. A character that travels under
  a moving camera keeps its root travel continuous, outside the held composition; only its poses hold (`picsart_scene_recipe scene-animation-reference`, held drawings: "Hold the pose, not the travel").
- Limbs follow the body through path-vertex tracks (or `ik` on a rigged character), never a hand-keyed
  tube each time.
- Cued layers use `timeMode: "layer"`.

## Type

A fat slab display face for the title card, ink on paper in a double rounded frame; a small bold sans
subtitle with wide letter spacing.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Every moving thing is on the one beat: the character, the bobbing props, the horizon.
2. Limbs are one width everywhere; no elbows, no knees, no gloves (a hand is the tube's swelled end), no bow tie, no buttons, no ears on the head.
3. Black, cream and the one red accent: nothing else.
4. Three bobbing background pieces at least.
5. A title card opens and an iris closes (see below).

## Build with the tools

Open with a title card as a composition layer, then an **iris**: a black rectangle group with an ellipse in the
same group, `fillRule: "evenodd"`, animating the ellipse's own `size` (never the group's scale, which would scale
the stroke). Put the whole cartoon in a `scene` asset and place it with one `scene_ref` carrying a film-finish
look (light grain, paper, dust); a look cannot sit on a shape layer.

## Do / don't

- **Do** change the silhouette until nobody can say who it resembles.
- **Don't** use round mouse ears, a long-bodied cat, gloved hands, a sailor suit or a bow tie.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Rate split: the character, and any prop that bobs on the beat, on twos in the nested composition as above; the title card, the iris and any camera at the root rate; the finish look on the outer `scene_ref`.
  - Boil: only the character's contour boils (`line_boil`, held rate about 12, small amplitude, fixed seed, ours, tune by render); props, ground, title card and paper stay still.
  - Line width: no zoom, the tube width stays fixed at 15 to 17 px; a pan is allowed, a push-in is not.
  - Finish: one light grain, the single look on the `scene_ref` as above; no second grain.

## On a part sheet

The shapes character above is the route for this style; this note is only for a user who brings a generated sheet. When a character comes through the SVG part-sheet flow (the `character-rigging` skill), every arm and leg is two pieces, an upper and a lower, each its own group, overlapping at the elbow or knee. That is a rig requirement no style overrides: the builder refuses a sheet whose limb is one piece. Draw each tube limb as two tubes, upper and lower, of the same width and the same colour, the lower one's rounded end overlapping the upper's, so the overlap reads as one bendy tube.

## Originality guard

Invent the character. It must not resemble the round-eared mouse of the 1920s-30s shorts, a long-bodied black
cat chasing it, any gloved mascot, the sailor, the spinach-eater, the talking duck or another known star's
silhouette, costume or pose, or a studio's opening card or iris wording. Keep the tubes, the beat and the
squash; change the silhouette, clothes and face.

## Proven on

The bouncing hose-and-heels cartoon (title card, iris in and out, film-finish look on the `scene_ref`).
