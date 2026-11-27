# Watercolour storybook

A dusk landscape painted in soft washes on cream paper, with a thin ink line over it that wobbles like a pen
redrawn each time. A paper boat drifts, birds flap, one window lights up and the sung words fill in, one by one.
Made for a song: the picture changes on bar lines and the words land on beats.

## Finish

Washes are shaped by one edge effect and the paper grain goes over everything (see The medium); the ink line sits
over the washes, outside that effect, so it stays crisp.

## Palette

Dusk washes: sky `#6f86ad` to `#d99b86` to `#efc79c`, hills `#8796b4` and `#7f9566`, river `#8eaebc` to `#557a93`,
house `#e6c79c` with a roof `#a94e40`. Ink `#3b302b`. Paper cream `#f1e6d2`. Neither pure black nor pure white appears. The
warm window light is the hero: it is added on top, never mixed into the paint.

## The medium

- **Washes are fills with a brush:** `brush` with the `bristle` tip, medium size, coverage near 0.8, no streak
  amount, a different `seed` per wash. They sit inside a `scene_ref` that carries `roughen_edges` (border about 4)
  so the edges bleed a little like wet paper.
- **The paper** comes from the film finish: `analog_film_finish` with `paper` about 0.35 and light grain, placed
  on the whole picture.
- **Ink lines** are strokes drawn over the washes and kept out of the edge effect.
- **Do not use the `watercolor` effect.** It bleaches the picture to near white; bristle washes with rough
  edges and the paper finish give the look.
- **Light is added:** a radial glow with an `add` blend on the lit window, never painted into the wash.
- **Big fills must not read as stripes.** Check every large fill in a full-size still before accepting it, and
  switch it to a chalk tip with a small `size` (about 7), coverage near 0.93 and a different `angle` per wash;
  keep the bristle wash for small shapes.

## Motion habits

- **The ink line boils:** the stroke's `wave` thickness with a phase that steps on twos (12 fps) and a different
  `seed` per object, so a still thing wobbles on its own beat and not with the moving ones.
- **Show/hide keys sit one frame apart** (`1/fps` at least): the lamp and each lyric word use step keys, and a gap of
  0.001 s lands on the same frame and blends every window.
- **Birds flap on twos** (a nested 12 fps composition) while they drift across.
- **Slow drift:** the boat glides and bobs, the sun and clouds barely move; nothing is held dead still.
- **Avoid twinning:** two birds, two lamps or two boats never move in step; give each its own phase and speed.
- **Something happens in each shot** (the lamp lights, a word fills): something changes between the
  first frame and the last, and the cause comes before its reaction. List the things the viewer should take in, one thing at a
  time, and give each read time to land.
- **Each join between shots is a designed transition** that fits the story (a wash wipe, an iris, a carry-through),
  and the film is one world whose colours travel from cold to warm and whose last shot rhymes with its first.
- **Music taste:** work the tempo out from the audio instead of guessing (a ballad often runs at half-time), open the clip right on a barline
  with a short audio fade in and a fade out of about two seconds. Changes land on bar lines (at 96 bpm a bar is 2.5 s: the lamp lights on the second bar), words
  fill on beats. Karaoke: a faint cream line at about 32 % fills to full cream one word at a time on one baseline, over
  a soft dark band. Text layers centre on their ink box, so per-word layers need a baseline correction from the
  measured widths.

## Type

A light book serif in cream for the lyric, one size, on a soft dark wash band at the bottom.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Washes have soft bleeding edges; the ink line stays crisp over them.
2. Neither pure black nor pure white; the paper grain is visible.
3. The only glow is added light on the window.
4. Still things boil on their own seeds; nothing jitters in step.
5. The lyric fills on beats along one baseline, and no key action sits in its band.
6. Big fills read as a wash, not as stripes.

## Build with the tools

Build the washes as brushed fills in one scene, add the `roughen_edges` effect on the scene reference, put the ink
and the lyric outside it, place the whole thing once as an asset and add the film finish. Key the lamp, the
lyric fill and the boat; flap the birds in a nested 12 fps composition. Preview the lamp beat and the last
lyric word, then a contact sheet across a bar.

## Do / don't

- **Do** land every change on the downbeat of a bar and every word on a beat.
- **Do** add light on top of the wash.
- **Don't** use the `watercolor` effect, pure black, pure white, or a boil that moves everything together.

## Originality guard

Paint your own landscape, house and boat; write your own lyric. Do not copy a named picture book's illustrations,
a film's backgrounds or an artist's recognisable compositions. Washes, a loose ink line and a paper boat are
generic conventions.

## Proven on

The river song: a dusk hill with a house whose window lights on the second bar, a paper boat on the river, flapping
birds and the line "the river knows my name" filling word by word (7.5 s, 1280×720, reviewed).
