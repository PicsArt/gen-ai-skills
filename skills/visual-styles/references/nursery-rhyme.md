# Nursery rhyme

A vertical 9:16 sing-along for small children: one cute round animal per sung line, standing in a soft storybook
place, with the line itself in big rounded white letters at the lower third and its key word lit on a yellow
pill. Every animal, prop and place is generated as SVG and imported as editable shape paths, split by part so the
parts move, then painted over in the scene with oil-pastel strokes: swirls that follow each round body, oval dabs
across the sky, water and grass, a thin warm outline, big glossy eyes and blush. Unlike
[simple shapes](simple-shapes.md) it has shading and texture and no human rig; unlike
[watercolour storybook](watercolour-storybook.md) it has a cast and its words are a sing-along caption, not a
quiet lyric on a band.

## Palette and colour roles

Sampled from the reference frames and held by the prompts below. All numbers are ours, tune by render.

| Role | Colour | Its one job |
|---|---|---|
| line | `#4a3a35` | the one thin warm-dark outline on every animal, prop and the caption |
| caption | `#fffaf0` | the sung words, never pure white |
| accent | `#f7c948` | **the highlight pill behind the key word of the line**, nothing else |
| accent ink | `#4a2e1e` | the key word while it sits on the pill |
| blush | soft pink | cheek ovals on every animal |
| places | pale cream-yellow day sky, soft green grass, pale blue sky and sea, navy-to-indigo night with a pale-yellow moon, teal pond, pale meadow, aqua sea floor | one gentle place per line |

Each animal takes one main colour that is not its place's main colour (a green alligator on a teal pond, a red
ladybug on a pale meadow), so it reads at a glance. Yellow stays off the backgrounds' large areas, so the pill
always reads as the word being sung.

## The medium

- **Vertical frame.** 1080x1920 at 30 fps. The animal stands in the middle band (its feet about 62-70% down), the
  caption sits at 72-80% down, and the top fifth is open sky with the sun, moon or a cloud.
- **SVG art, imported as paths.** Every animal and place is one SVG drawn by `picsart_generate` with
  `gpt-image-2.6-sunburst`, `extra` `{"outputFormat": "svg", "complexity": "medium"}` (1:1 for an animal, 9:16
  for a place; an opaque background, since a transparent one is refused for SVG). Bring it in with
  `picsart_scene_import_svg_path` `svg`: every path keeps its own fill and stroke in paint order. Ask for each
  moving part as its own `<g id>` and import each part onto its own shape layer, so the head, a flipper or the eyes
  turn about their own pivot (the bottom centre of a head's box, a flipper's shoulder corner, the eyes' centre).
- **Soft shading inside the SVG.** The prompts ask for solid colours with the shade drawn as a few overlapping
  lighter and darker shapes of the same hue, one thin warm-dark outline, round joins. No gradients, filters,
  masks, clip paths, text or transforms, so every shape imports.
- **The brushwork makes the style, and it is added in the scene.** The generated SVG is clean vector; painted over
  it, it reads as oil pastel. Two layers of strokes, both `blendMode` `soft_light`, about two thirds warm white
  `#ffffff` and one third warm dark `#2a1c18`:
  - *Over the place:* one shape layer of horizontal overlapping oval dabs (22-40 x 9-15 px, a few degrees of tilt,
    fill opacity 0.3-0.65, about 4200 per 608x1080 of frame; scale them and their count with the frame) under the
    animal and over the sky, water and ground, so every big fill turns into brick-like pastel dabs.
  - *Inside each animal part and each set piece* (barn, peaks, floe, moon, lily pad, flowers): short curved
    strokes (10-22 px long, 4-7 px wide, opacity 0.4-0.75, about one per 32 px² of the part's box) that run round
    the part's centre, so a round body shows swirls that follow its form. A big flat piece (a hill, a sand bank)
    takes them laid along the ground instead; a swirl that size reads as a vortex. Clip them to the part: turn the
    part's layer into a `composition` content of two layers, the part's shapes and the strokes, with the strokes'
    `mask.clip` a copy of the part's shapes (`mode` `alpha`). Transform, animations and `parentId` stay on the outer
    layer, so the strokes move with the part. Give the outer layer `anchor` `[0, 0]` when it has none: a
    composition anchors at its centre. Leave the eyes unpainted so they stay glossy.
  Add `film_grain` at about 0.05 on the whole frame for the paper.
- **Places are a few big parts:** sky, a back band (hills, snowy peaks, a barn), the ground or water with short
  grass or wave strokes, and one sky object. Import each as its own layer so the sun can pulse, the cloud drift,
  the waves slide and each star twinkle on its own phase.

## Prompts

Fill in the braces; keep the rest as written. Every prompt ends with the same rules line:

> Only `<path>` elements with solid fill colours; no gradients, filters, masks, clip paths, text or transforms.
> Keep it simple, under {70-120} paths.

**An animal** (1:1): "SVG for a children's sing-along cartoon, for animation. A cute round cartoon {animal},
{pose: standing facing the viewer, its right flipper raised in a wave / lying down asleep, seen from the side,
eyes shut as two small curved lines}. No background shape at all: draw nothing behind it. Soft rounded chunky
shapes, soft shading drawn as a few overlapping lighter and darker shapes of the same hue, one thin warm
dark-brown outline (#4a3a35) around each shape with round joins, big glossy eyes (white eye with a thin outline, a
large dark iris low in it, one big and one small white highlight), pink blush ovals on the cheeks. Each part is its
own `<g>` with an id: {parts}." Parts that move: a head apart from the body; each arm, flipper, wing or tail; the
eyes as one group (for the blink); legs; companions (chicks) each their own group.

**A place** (9:16): "SVG background for a vertical children's sing-along cartoon: a soft storybook {place}, no
animals, no people, no text. {three or four big elements with their colours and where they sit}. Soft gentle
colours, soft shading drawn as a few overlapping lighter and darker shapes, one thin warm dark-brown outline
(#4a3a35) on the main shapes. The lower third is calm and open. Each element is its own `<g>` with an id: {sky,
back band, ground or water, strokes, sky object}."

Places that hold the look: a daytime farm (cream sky, pale sun, round-topped red barn, low fence, green hill); a
polar sea (pale sky, two snowy peaks, blue sea with wave strokes, a flat ice floe); a bedtime sky (navy bands,
small soft stars, a big pale-yellow crescent moon, lavender clouds below); a pond at sunset (warm sky, soft hills,
teal water, lily pads, reeds); a flower meadow (pale sky with soft pastel flower dabs, a green hill, a few big
flowers); under the sea (aqua water, kelp, a sandy floor, bubbles).

Animals that hold the look: hen with chicks, penguin, sheep, alligator (two eye domes on top of the head, a long
rounded snout with a little zig-zag of teeth, a pale belly), ladybug (black head with two antennae ending in pink
dots, a big red round body with black spots), jellyfish (a pink dome with a scalloped hem and wavy tentacles).

## The animals

Generate each animal once and import it once; save the imported scene and place it by `scene_ref` in every line
it sings, so it stays the same animal.

- **Proportions:** round and chunky, a big head about as wide as the body, short stubby legs or none, no neck.
  About 45-60% of the frame width.
- **Acting is gentle:** a slow sway of the head or body (rotation 3-6 deg about the feet or neck), a squash breath
  (scale 1 +- 0.02 on a 1.5 s cycle), one blink per line (the eyes group's scale y to 0.1 for about 0.12 s), one
  gesture per line (a flipper wave of +-10 deg about the shoulder, a hop of the chicks, a hug). A sleeping animal
  has shut eyes drawn as arcs and floating `z` letters that drift up and fade.
- **Riders.** An animal resting on something that moves (a penguin on a bobbing floe, a sheep in the moon's
  hollow) takes the same bob or is parented to it (`parentId`, its position then in the parent's own coordinates).

## Motion habits

- One animal per sung line; a cut or a short slide changes the animal and the place on the line's first beat.
- Everything breathes: the sun pulses 3%, clouds drift a few pixels, waves slide, stars twinkle on their own phase,
  the ice floe or lily pad bobs. Use periods that divide the line's length so a held line loops cleanly.
- No two things move in step: give each animal, chick and star its own phase.
- Arrivals settle with a small overshoot (`ease_out` to 112%, back to 100%).

## Type

- **Face:** a heavy rounded sans (`vag-rounded-lt-black`), about 96 px at 1080 wide, centred, two short lines
  of the lyric, line spacing about 1.3x the size.
- **Caption:** fill `#fffaf0`, a text `stroke` in the line colour about 16 px with `order` `fill-over-stroke`,
  and a small `drop_shadow` (offset 0,7, blur 4, `#2a1c1866`).
- **The key word** (the animal's name, or the one word the line is about) gets its own text layer on the second
  line. On its beat a rounded rect pill (`#f7c948`, roundness about 46, the line colour at 10 px) pops behind it
  (scale 0.6, to 1.12 in 0.12 s, to 1) and the word swaps to a dark copy in `#4a2e1e` with no stroke. Text
  layers centre on their ink box, so measure each word with the font file to place the words of a line side by
  side.
- A line changes with its animal; never more than two lines on screen.

## Scene features used

`picsart_scene_import_svg_path` (`svg`, one shape layer per part), `stroke` with `lineCap` round, text `stroke`
with `order` `fill-over-stroke`, `drop_shadow`, `blendMode` `soft_light` on the brush layers, a `composition`
content with `mask.clip` (strokes clipped to a part), `film_grain`, layer `parentId` (a flipper on its body, a sheep riding the moon) and Lua `expression` tracks for the sway, breath,
bob and twinkle.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. The frame is vertical 9:16, one animal in the middle band, the caption in the lower third and clear of its face.
2. Every animal is the imported SVG with its soft shade, thin warm line, big glossy eyes and blush.
3. Oval dabs cover the place and curved strokes cover every animal part and set piece; the eyes and the caption
   stay crisp.
4. Yellow appears only as the pill behind the sung key word.
5. Something gentle moves in every frame; nothing jitters, and no two things move in step.

QC leans on the contact sheet across each line (the pill on its beat, the blink off the beat).

## Build with the tools

Generate the places and animals (one `picsart_generate` call with `items`, about 2 credits each), import each
place's parts as layers of a 1080x1920 scene, import each animal's parts as layers of its own saved scene, then
add the brush layers and the caption layers. Key the pill and the dark key word to the sung beat, the sway, breath
and twinkle as expressions. Validate, check a still at the pill beat, then a contact sheet across the line.

**The song.** One sung line per animal from `elevenlabs-music-v2` (`duration` 10, `isInstrumental` false, about
5 credits): "A vocal children's nursery rhyme song, not instrumental: one warm, clear female singer sings the
words clearly and slowly over soft ukulele, {glockenspiel / marimba / celesta}, about {70-90} bpm, a {morning /
sunset / bedtime} feeling. The singing starts right away. Lyrics, sung once: "{line}" Then the music finishes
softly." Trim to the clip with a 1 s fade out. Find when the key word is sung with `picsart_media_transcribe`
(`words`); recognition sometimes hears no words in a sung take, so listen before trusting an estimate.

## Do / don't

- **Do** generate the animals and places as SVG and import them as paths, one layer per moving part.
- **Do** light only the one key word of each line.
- **Do** paint every animal part and set piece and the whole place with the soft-light strokes; flat vector reads
  as a different style.
- **Don't** use generated raster pictures, a thick black ink line, gradients or filters in the SVG, a detailed
  hard-edged background, or one big swirl across a hill.

## Originality guard

Invent the animals, the places and every lyric; describe the look, never a channel, a song or a named character.
Round shaded animals, soft storybook places and a highlighted sing-along word are generic conventions of
children's videos.

## Proven on

Six 8 s 1080x1920 clips with a sung line each, all art generated as SVG, imported as paths and painted in the
scene: a hen whose head sways while two chicks hop on a farm, a penguin waving and blinking on a bobbing ice floe,
a sheep asleep in a swaying crescent moon with drifting `z`s, an alligator waving on a bobbing lily pad at sunset,
a ladybug hugging a swaying daisy in a flower meadow, and a jellyfish floating with swaying tentacles under the
sea. The style's preview is the penguin line laid out at 960x540.
**Not proven, so not in this recipe:** a whole song of several lines cut together, simpler egg-shaped animals
drawn closer to a hand-painted look.
