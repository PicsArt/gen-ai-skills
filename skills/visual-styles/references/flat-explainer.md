# Flat explainer

A calm business explainer in flat vector: an off-white ground, one soft colour blob behind the subject, a UI card
or a chart that builds itself, icons that pop in with a small overshoot, and one flat character with no outlines
who walks in and stands beside the idea.

## Palette

Ground `#f3efe6`, floor band `#e7e1d4`, blob `#f7d9cf`. Navy `#1f2a44` for type, hair and card headers; mustard
`#f2b134`; idle chart bars `#c9d3ea`; plant green `#3f8f6b`; a success green `#3bb273` for the check. **The hero
colour is coral `#ef6f5e`**, kept for the one bar or mark the story is about. Four to five colours in a frame.

## The medium

- **No outlines, no gradients, no glow.** Every shape is one flat colour meeting another; a raised card has one
  flat offset shadow (`#d9d2c3`, 10 px down and right) instead of a soft one.
- **Rounded geometry:** cards and bars as rounded `rect`s (roundness 8 to 22), icons from circles and short paths.
- **One soft blob** (a single large ellipse in a pale tint of the hero colour) sits behind the subject and drifts
  a few pixels. Two overlapping blobs read as a cloud, not a backdrop.
- **The floor is a flat band**; the character's feet sit inside it, not on its top edge.
- **First listed draws on top** inside a shape: list a card's header dots before the header bar.

## Characters

One flat person, made through the SVG part-sheet flow (`character-rigging`). Fill only the description slot of the
frozen part-sheet template with:

> {subject} drawn in a flat vector business-explainer style: about 6 heads tall, simple geometric proportions,
> slim rounded limbs of even width, small oval hands, simple flat navy shoes (never white: they vanish on a pale floor); a small simple face: two small solid dark
> dot eyes, short level dark eyebrows, no nose line, a small closed mouth, a soft rounded chin; {hair}; {outfit};
> NO outlines anywhere: every shape is flat colour meeting flat colour; flat shading: every part has one flat base
> colour plus at most ONE slightly darker flat shade shape of the same hue on the side away from a light at the
> upper left (no highlights, no gradients); {skin}; a limited palette of navy, mustard, coral and off-white, clean
> and calm like a modern business explainer

- The outfit takes the palette's colours, so character and set share one palette.
- **The character presents.** Make them about half the frame height. Walk them in with `walk_cycle` `from` `rest`
  and a `distance` that stops them right beside the card. As the chart builds, they raise the near arm toward it
  (`rightUpperArmRaise` about 0.36 with `rightHandPoint` 1, keyed in over 0.4 s) and tilt the head down to it
  (`headNod` about 0.45 with `lookDown` about 0.6). They hold the point for about 1.5 s, then lower it. Start the
  chart only after the walk ends, so the eye moves from the person to the idea.

## Motion habits

- **Pop with a small overshoot:** scale keys `0 → 1.08 → 1` over about 0.4 s (`ease_out`, then `ease_in_out`).
  Cards, icons and the check all enter this way, one at a time.
- **Bars grow from their base:** anchor each bar at its bottom, scale y `0 → 1.06 → 1`, staggered by 0.25 s; the
  hero bar is last and in coral.
- **Idle life:** floating icons bob 5 px on sines with different phases; the plant sways 3° about its pot; the blob
  drifts. Nothing else moves once a beat lands.
- One caption per beat in a rounded geometric bold (`gilroy-bold`), navy, bottom centre, fading in last.

## Type

Short caps captions in `gilroy-bold`, about 40 px at 1280 wide, navy on the off-white ground.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. No outline, gradient or soft shadow anywhere, on the character or the set.
2. Coral appears on one mark only: the bar, pin or button the beat is about.
3. Every entrance overshoots slightly and settles; nothing slides in linearly.
4. The character's feet sit in the floor band and stay planted when the walk stops; they point at the chart while
   it builds.
5. Something small moves in every frame (an icon bob, the plant, the blob).

## Build with the tools

Build the ground, blob, floor, card and icons as shape layers; give each bar its own layer anchored at its base.
Build the character from one part sheet, then apply `walk_cycle` to its `scene_ref` layer at the top level (a walk
that travels on its own refuses a parented layer).

## Do / don't

- **Do** share the palette between the outfit and the set, and keep one idea per beat.
- **Don't** add outlines, glows, gradients or a second hero colour.

## Originality guard

Invent the people and the product. Never imitate a known brand's illustration system, mascot, app screens or
logo, and never name one in a prompt. Flat shapes, one blob, popping UI and a calm walking figure are the style.

## Proven on

A desk explainer (8 s): a flat character walks in, stops beside a UI card and points at its chart as it builds
itself; a chat bubble and a pin pop in, a check confirms the hero bar, and the caption lands.
