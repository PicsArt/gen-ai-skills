# Silent film

A black-and-white slapstick short as a worn projector showed it: painted street flats, a pompous clerk and one
gag, an intertitle card, an iris that opens and closes the reel. Jerky, scratched and grey.

## Finish

The `analog_film_finish` look (grain, paper, dust) on the one `scene_ref` of the reel, an iris that opens and closes it, an intertitle card and a stepped rate (see the reel notes below).

## Palette

Greyscale only: ink `#121212`, `#3a3a3a`, `#5c5c5c`, `#7a7a7a`, `#8e8e8e`, `#b9b9b9`, windows `#d9d9d4`. **No hue is
used. The hero is the one near-white `#ecebe6`, reserved for the gag props** (the peel, the lamp's glass, the
shirt front, the card's lettering) so the eye finds the joke.

## The medium

- The set is a few flat shape layers painted in grey: a backdrop, a row of buildings with windows (stroke
  `#3a3a3a`, 4 px), a pavement band, a lamp post. Nothing is shaded.
- The clerk is an ink silhouette: a coat as a closed path, a pale oval head with a dot eye, a **flat cap** (a
  low crown and a stiff peak, dark grey with an ink outline), bodied limbs (each sleeve and trouser leg one closed tapered shape growing out of the coat, a hand one shape with its forearm) in groups pivoted at the
  hip and shoulder, and a **furled umbrella** in one hand (a thin shaft, a tight cone, a knob).
- The reel is its own picture: build the whole film as one `scene` asset and place it with one `scene_ref`
  carrying the `analog_film_finish` look (grain, paper, dust). The iris and the flicker sit inside the asset, so
  the film look runs over them.
- **Flicker** is a full-frame white layer at low opacity; **scratches** are one or two thin pale vertical
  strokes that hop sideways.
- **Iris** is an ellipse with a very thick ink stroke whose size keys open at the start and closed at the end;
  everything outside the hole goes black.
- An **intertitle** is a black card with a double white rule and one line of heavy serif lettering, up for two
  seconds.

## The character

Drawn from the style's own shapes, not a generated sheet (the mechanism, saving and talking are in [shapes-character](shapes-character.md)); build once, save once to the library, place it by its `uri` in every shot.

- **Proportions:** about 6 heads tall, a pompous barrel chest over thin legs: the coat is one closed ink path.
- **Shapes:** the coat, a pale oval head with a dot eye, a flat cap, and **bodied limbs**: each sleeve and trouser leg is a closed tapered shape that starts inside the coat's silhouette and grows out of it (an upper arm about 0.4 of the torso's width, never a stroke laid across the coat), in groups pivoted at the shoulder and hip. The furled umbrella is a prop in one hand.
- **Face:** a dot eye and a moustache; the clerk does not talk (an intertitle speaks for him), so drop `mouth` and `blink`.
- **Controls:** the base set, `strut` as keyed leg rotations, a hip bob; the slip is one fast keyed rotation to flat.

## Motion habits

- Run the reel at 15 fps under a 30 fps root (12 under a 24 fps root): set it on the composition, or put the
  picture in a nested `composition` layer at that `fps`. A rate that divides the root holds every frame for the same
  time. Either way every move is stepped.
- The clerk **struts**: a high knee lift (alternating keyed leg rotations, a big forward swing and a short
  back swing), a hip bob of 20-25 px, the chin up and a slight backward lean. The gag is fast: the slip is a
  fast keyed rotation to flat, the umbrella pops open on the same beat (swap the furled drawing for an open
  canopy with two opacity keys one frame apart), the cap flies in a high arc (position keys with a raised
  midpoint) to land on the lamp, holds, and drops back.
- **Flicker and scratch hops** are the `random_hold` preset on the flicker layer's opacity and on each scratch's
  position (a different `seed` per layer). A little `wiggle` on the whole picture is the gate weave.
- Cut hard: no easing between shots, a card cut in and out, not faded.
- Cued layers use `timeMode: "layer"`.

## Type

Intertitle only: a heavy display serif, cream on the black card, one line in quotation marks.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Greyscale throughout; the only light tones are the gag props.
2. The reel runs at 15 fps under a 30 fps root (12 under 24), not at the root rate.
3. Film look, flicker and scratches are all on.
4. There is one gag with a setup, a hit and a payoff.
5. The iris opens at the start and closes at the end; a card sits in the middle.

## Build with the tools

Build the set and the actors as shape layers inside a `scene` asset; add the flicker, scratches and iris inside
it; place it with a `scene_ref` and the film-finish look. Apply `random_hold` and `wiggle` with
`picsart_scene_apply_preset` to layer ids inside the asset.

## Do / don't

- **Do** keep every move legible as a silhouette: a big stride, a big umbrella, a big cap.
- **Don't** add colour, motion blur or smooth easing; don't fade the iris, drive it by size.

## On a part sheet

When a character comes through the SVG part-sheet flow (the `character-rigging` skill), every arm and leg is two pieces, an upper and a lower, each its own group, overlapping at the elbow or knee. That is a rig requirement no style overrides: the builder refuses a sheet whose limb is one piece. Draw each limb as two round-cap strokes, upper and lower, of the same width and ink, overlapping at the joint, so the pair reads as one jointed limb.

## Originality guard

Invent the clerk, the gag and the street. No tramp look-alike: never the combination of a bowler hat, a
toothbrush moustache, baggy trousers, oversized shoes and a cane. No famous silent comic's stunt (a
cliff-hanging clock, a falling wall) and no famous title card or its lettering. The grey set, the stepped film
and the iris are the style.

## Proven on

The redrawn silent-reel film (iris in, a strutting clerk in a flat cap slips on a peel, his umbrella pops open,
the cap lands on a lamp, an intertitle, the cap drops back, iris out; 15 fps, film grain).
