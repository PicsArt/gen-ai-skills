# Shadow puppet (and red paper-cut)

Two cut-card looks that share one idea: the light or the paper behind does the colour, and the shapes are only
black or only red. Pick the black screen variant for a story, the red sheet for a folk motif or a greeting.

## Finish

Idle pieces on twos (`fps` 12 under a 24 fps root) and a flickering lamp glow (see Motion habits).

## Palette

**Screen variant.** Silhouette `#160c06` only. The screen is a radial `gradientFill` from the lamp: `#ffe2a0` at
the centre, `#f0a24c` at 0.45, `#5a1e08` at the edge. Cut holes show the screen colour; **the hero colour is the
lamp glow itself (`#ffe2a0`), reserved for the screen and the holes in the subject**. A vignette frame `#120804`.

**Red paper-cut variant.** One red sheet `#c8202a` on cream paper `#f4ead5`; gold `#d9a441` only for small caps.
**The hero colour is the red**, and everything is red or paper: a cut hole is a cream shape on top of the red.

## The medium

- **Screen:** every piece is a flat black fill with a cut hole where something must show through (a sail with a
  circle, a hat band, an eye). Characters are profile cut-outs: head, body, two arms and legs as separate
  pieces on pins, with small cut details. Scenery is black layers (rocks, boat, tree), each on its own rod. Waves
  are a row of scalloped ellipses (one ellipse and a `repeater`) over a black band, three strips at different
  sizes. **Every moving puppet has a thin control rod** (a 3 px stroke to below the frame) because the rod makes
  it a puppet.
- **Red paper-cut:** symmetry comes from a `repeater`: one petal (a path with a cut ellipse inside) repeated 12
  times at 30 degrees, a ring of tiny diamond cuts repeated 24 times at 15 degrees. A character is one red cut
  with cream holes for eyes and dress details; fur and clothes are cut patterns (dots, scallops, diamonds),
  never drawn lines. Add a soft `drop_shadow` (`offset [3, 5]`, `blur 5`) to each red layer for paper depth; list
  cut holes before the red mass (an earlier item is on top).

## The character

Drawn from the style's own shapes, not a generated sheet (the mechanism, saving and talking are in [shapes-character](shapes-character.md)); build once, save once to the library, place it by its `uri` in every shot.

- **Proportions:** about 5 heads tall, one flat silhouette.
- **Shapes:** one solid black polygon per part (head with a profile, body, arms, legs) and a thin rod stroke running from the hand and the head; no interior line.
- **Face:** none: a silhouette has no face and cannot talk; it acts by profile and gesture.
- **Controls:** drop `blink` and `mouth`; `headTurn` flips the head's profile, `spineLean` and the arm dials carry the acting.
- **No run, jog, point or pick_up:** a silhouette limb is one polygon with no elbow or knee, so the SVG cut-out builder refuses it by name (`missing_part`, `missing_joint`) and the four presets do not apply. Act by profile and gesture with the dials above.

## Motion habits

- **Screen:** a hand tremble on each puppet with the `wiggle` preset (1-2 px `amount`, own `seed` per piece),
  waves bob at different phases, the boat rocks a few degrees, a jump is a parabola with a turn across it, the
  lamp flickers (a white radial glow whose opacity is keyed or driven by `random_hold`).
- **Red paper-cut:** unfold first (scale 0.2 to 0.82 and a turn from minus 120 degrees to 0 over about 1.7 s on
  a small overshoot), then idle on twos: put the idle pieces in a nested composition layer at `fps` 15 (12 under a 24 fps root) with
  plain keys; lanterns swing, a branch sways a degree.
- Cued layers use `timeMode: "layer"`.

## Type

Screen: one quiet line in a plain bold sans, about 28 px, warm cream, bottom, fading in late. Red paper-cut: none,
or one brush-style greeting in red on cream.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. A subject whose silhouette reads alone, with a head turn or a pose acting (a face in the red variant).
2. The whole frame is the lamp screen or the cream sheet; nothing floats on blank.
3. Three or more small movers: waves, a flickering lamp, a swinging lantern, a swaying branch.
4. Screen: a rod under every moving piece. Red: a cut hole in every large shape and one soft shadow.
5. One colour of shape throughout: all black, or all red.

## Build with the tools

Build the screen as a gradient rectangle first, then the layers back to front (back wave, boat, mid wave, puppet,
front wave); a jointed arm is a group with `anchor` and `position` at the shoulder. Apply `wiggle` through
`picsart_scene_apply_preset`. For the red variant build one petal and let the repeater do the rest.

## Do / don't

- **Do** let the lamp or paper carry the colour.
- **Don't** add a second shape colour, an outline, or a drawn sky on the screen.

## On a part sheet

The shapes character above is the route for this style; this note is only for a user who brings a generated sheet. When a character comes through the SVG part-sheet flow (the `character-rigging` skill), every arm and leg is two pieces, an upper and a lower, each its own group, overlapping at the elbow or knee. That is a rig requirement no style overrides: the builder refuses a sheet whose limb is one piece. Draw each limb as two overlapping pieces in the same black, upper and lower; the shared black hides the joint, and a pin dot at the elbow or knee is optional.

## Originality guard

Draw an original tale and cast. It must not resemble a known folk-tale or epic puppet's face or costume, the stock
figures of a named puppet theatre, the shadow sequences of any famous film, a famous artist's cutting or a museum
piece, a brand's festival artwork or a known zodiac poster, or any flag, emblem or sacred figure.

## Proven on

The lamp-lit boat scene (screen variant) and the red window-flower and lantern scene (paper-cut variant).
