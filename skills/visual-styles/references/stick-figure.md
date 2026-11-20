# Stick figure

Stick figures acting a story, not explaining one: unlike [the whiteboard explainer](stick-explainer.md) there is
no white board, drawing-on, idea or chart, and unlike [continuous line](one-line.md) each figure is separate
strokes that move as a body. Figures made only of ink strokes, with a round filled head and no face, walk, run,
jump and point their way through a story on a flat coloured ground.

## Finish

The figures and whatever they touch on twos in a nested composition (`fps` 12 under a 24 fps root; see Motion habits).

## Palette

One flat ground colour per shot, the band below the ground line one step darker: apricot `#ffcf8a` over
`#f2ae68` was proven; mint `#bfe8d4` over `#9fd3bb` or sky `#a8d8f0` over `#86c1de` are its siblings, one for each
place. Ink `#161616`. Every limb, near or far, is the same ink at full opacity. **The hero colour is red `#e63946`,
kept for the one object the story turns on** (a ball, a kite, a door). A contact shadow is a flat ellipse in a
darker tint of the ground.

## The medium

- **The figure is strokes and one disc.** A filled ink disc for the head with no face; a straight torso; each arm and
  leg two segments of equal weight, with round caps and joins. Proportions for a figure of height h: head 0.19 h,
  neck 0.04 h, torso 0.37 h, thigh and shin 0.27 h each, upper arm 0.21 h, forearm 0.2 h. The line weight is
  about 2.6% of h (12 px on a 460 px figure).
- **Near over far, by draw order alone.** Draw the far arm and leg first, then the torso and head, then the near
  limbs: the far ones sit behind the torso and the near limbs on top, all in the same solid ink (no lighter colour,
  no opacity below 1). A crossing of legs or arms reads because the far limb is behind the near one and the stride
  phases differ, so the two lines meet at an angle and the bends show; keep a visible gap between the legs at the
  moment of crossing rather than a lighter colour.
- **The set is in the same stroke.** The ground line, a rock or a hill (outlined, filled with the ground
  colour), a sun as a ring with short rays, clouds as overlapping circles (fills grouped above a doubled stroke,
  so only the outer edge shows), and a breeze as two short faded strokes. No textures and no other fills.
- **Speed lines** are three short strokes behind the hip, shown only while the figure runs or leaps.

## Characters

Build the figure as one shape layer of nested groups (forward kinematics): a hip group carrying the travel, two
leg groups with their anchor at the hip and each shin group positioned at its thigh's end, and an upper-body group
turned by the lean about the hip, holding the torso, the head and two arm groups (anchor at the shoulder, each
forearm at its elbow). Each joint is a group `rotation` (0 hangs straight down; clockwise swings a limb back on
a figure facing right). Give each figure in a cast its own ground position, height or accent (a red scarf stroke,
a hat); never a face. About 5 heads tall to the circle head. Save the figure once with the library save and place it by its `uri` in every shot ([shapes-character](shapes-character.md)); it does not talk, since it has no face. Controls: `spineLean`, `headTurn`, the arm raise and swing dials, `stride`. Each foot is a short stroke on the floor line; the arms start at a shoulder point below the head circle and a raised arm stays beside the head (about 150 degrees at most), never across it.

## The character

Drawn from the style's own shapes, not a generated sheet (the mechanism, saving and talking are in [shapes-character](shapes-character.md)); build once, save once to the library, place it by its `uri` in every shot.

- **Proportions:** about 5 heads tall to the circle: a stroke body under a round head.
- **Shapes:** a circle head (stroke only), a torso stroke, two-bone arm and leg strokes of one width and round caps, a scarf or hat as the one accent; no fill.
- **Face:** none: a stick figure has no face and does not talk; its acting is the whole body.
- **Controls:** drop `blink` and `mouth`; add `hop` (a crouch, a leap, a squash) and read the pose from the leg angles.

## Motion habits

- **Planted feet come from IK on footfalls.** Plan each foot's plants (where and from when to when) and the hip's
  path. A script then solves the two-bone leg for every key (thigh and knee from the hip-to-foot distance, knee
  forward) and writes the rotations. A planted foot never slides, whatever the speed. The swing foot arcs between
  plants, lifting about 0.25 h on a walk and 0.45 h on a run.
- **Walk**: a step every 0.4 to 0.5 s, double support between steps, a small bob twice a stride, arms swinging
  against the legs with a soft elbow.
- **Run**: a step every 0.25 to 0.3 s, a short contact with a flight between, the torso leaning 15°, the elbows
  bent at about 95° and pumping.
- **Jump**: gather (the hip drops 0.12 h, the arms swing back, 0.15 s), leap on an arc with the knees tucked
  forward and the arms thrown up, land and absorb (the hip drops 0.15 h, the arms forward), then recover.
- **Point**: the near arm straight along the line to the target, the far hand back; hold it at least 0.6 s.
- **Joy**: arms in a V, two small hops.
- **On twos.** Key every pose at 1/12 s and put the figures and whatever they touch in one nested composition
  at `fps` 12 under the 24 fps root, so they step together. A figure that travels under a moving camera keeps its
  root travel continuous, outside the held composition; only its poses hold (`picsart_scene_recipe scene-animation-reference`, held drawings: "Hold the pose, not the travel").
- Hold still between beats. A stick figure reads its pose only when it stops.

## Type

None in the picture. Words, when the plan has them, are captions in a bold grotesque in ink at the foot of the
frame, or the voice-over.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Every figure part and prop is ink stroke at one weight; the only fills are the head, the hero object and the
   ground-colour props.
2. The far limbs are the same solid ink, drawn behind by order; no crossing is ambiguous (a gap or a different stride phase, not a lighter colour).
3. A planted foot does not move against the ground (check it frame by frame).
4. Each beat has a pose held long enough to read, and the hero red is only on the story object.
5. The figure is at least 40% of the frame height.

## Build with the tools

Write the set as one shape layer and the figure as nested limb groups in a 12 fps composition layer. Compute the
footfall IK and the arm poses in a script, then write them as `rotation` keyframes on the groups and a `position`
track on the hip group. Check a contact sheet at each beat (contact, passing, gather, top of the leap, landing),
and step through the run frame by frame for sliding feet.

## Do / don't

- **Do** let the whole body act a beat: lean, arms and legs together.
- **Don't** add a face, a gradient, a chart or a draw-on, or put the figure on white paper with a marker line
  (that is the whiteboard explainer).

## On a part sheet

The shapes character above is the route for this style; this note is only for a user who brings a generated sheet. When a character comes through the SVG part-sheet flow (the `character-rigging` skill), every arm and leg is two pieces, an upper and a lower, each its own group, overlapping at the elbow or knee. That is a rig requirement no style overrides: the builder refuses a sheet whose limb is one piece. Draw each limb as two strokes, upper and lower, of the same stroke width with round caps, the lower overlapping the upper at the elbow or knee, so the joint reads as one bent line.

## Originality guard

Invent the figures, their story and their world. Never copy a known stick-figure animation's characters, its
fights or its signature moves, or a webcomic's figures or captions; stroke figures, a coloured ground and
planted acting are the style.

## Proven on

The red ball (9 s, 16:9): a figure walks in, points at a red ball on a hill, runs with speed lines, leaps a
rock, lands as the ball hops, and jumps for joy, all on twos.
