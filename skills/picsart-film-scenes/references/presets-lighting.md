# Lighting presets — the two-source setup

> **The wordings live on the server.** This file decides *which* preset to
> reach for — that judgement is the part that needs a reader. The sentence each
> id compiles to is not here: those sentences are tuned against real renders,
> and a prompt written from a remembered copy of one renders worse than a prompt
> that pastes it. Pass the id to `picsart_film_compile_prompt` and the server
> pastes the sentence.

The vocabulary behind every lighting decision in the pipeline: the shot list's
`Light` control, the review board's orb, and the text-choice fallback without
boards. Compiles into the shot block and the scene picture's prompt when the
user chose the light on the board (`prompt-blocks.md`, Part 2, *The card's own
picks*).

**There is no film-wide light.** The film setup does not carry one, by design
(`../../picsart-film/references/presets-looks.md`) — a night
exterior and a kitchen morning are not lit alike, and a light clause pasted into
every prompt of a world contradicts this block on most of them. The block's law, from the pipeline: **one
motivated source** (a second source only as described below), its direction named,
which side of the face is dark, what is protected in exposure — and **never flat
front light**.

## The seventeen setups

**One vocabulary, three surfaces.** The shot list's `Light` control, the review
board's orb and this table are the same seventeen presets, so a scene planned
from this file arrives at a board offering the same light.

Noon sun is `overhead fall`: a hard source straight down is one setup, whatever
it is called.

**The last six are exterior, because the first eleven are not.** `window` is a
thing you stand inside and look out of; `practicals`, `night practical`,
`work light` and `firelight` are all somebody switching something on. Without
the exterior six, a day exterior could honestly reach only for `overcast` —
which this file itself calls what a shot looks like when the lighting was never
decided — and the two backlight setups, and a scene on a street at six in the
evening would have no id for the light it is obviously in. Some names that sound
like setups are not new ones: `headlights` is `night practical` with its
placeholder resolved, `neon` is named inside `practicals`, and fog and storm are
atmosphere rather than a source with a direction.

**Ids:** `auto` · `window` · `practicals` · `night practical` · `work light` · `firelight` · `silhouette` · `contre-jour` · `overhead fall` · `soft cross` · `overcast` · `golden hour` · `blue hour` · `open shade` · `dappled shade` · `street light` · `moonlight`

*(The sentence each id compiles to lives server-side. Pass the id to `picsart_film_compile_prompt` and it pastes the tuned wording; never write that sentence yourself.)*

**`overcast` is the one setup with no dark side, and it is deliberate.** The
block's law below is that the shadow side is always named; overcast has none to
name, because a fully diffused sky wraps evenly. That makes it the one preset
that must be *chosen* rather than arrived at — it is the honest description of a
white-sky day, and it is also exactly what a shot looks like when the lighting
was never decided. Pick it on purpose or pick something else.

`blue hour` is its nearest neighbour and is not the same thing: it is soft
and has no HARD shadow, but the sky is brighter where the sun set, so there is
still a side to name. Overcast keeps the exception on its own.

Five take no parameters from the grid below — `auto`, `overcast`, `blue hour`,
`open shade` and `street light`, the last three because the sky overhead, the
shade you are standing in and a lamp straight up have no direction left to
choose. Everything else has one worth naming.

## Inside, outside, and the ones that do both

Not a rule, a way of finding one. Several work in either place — `firelight` is
a hearth or a campfire, `practicals` is a table lamp or a shopfront.

- **Daylight** — `window` (inside, looking out) · `overcast` · `open shade` ·
  `golden hour` · `dappled shade` · `blue hour`
- **Night and artificial** — `practicals` · `night practical` · `street light` ·
  `work light` · `firelight` · `moonlight`
- **Into the light** — `silhouette` · `contre-jour`
- **Placed, not found** — `overhead fall` · `soft cross`. Noon sun lands here:
  it is the same picture as a hard unit straight down.

## The two-source parameter grid

When the preset is tuned (one follow-up question), each source
is described with three parameters, written into the same block sentence:

| Parameter | Values | Written as |
|---|---|---|
| direction | clock positions around the subject, camera at 6 o'clock | `key from 9 o'clock` (side), `from 12` (back), `from 4–5` (near-frontal — avoid) |
| intensity | low / medium / hard | `low: shaping only` · `medium: clearly directional` · `hard: cast shadows with edges` |
| temperature | warm / neutral / cool | `warm tungsten character` · `neutral daylight` · `cool blue-hour character` — **and the Kelvin behind it** (below) |

Second source is always subordinate: `fill one stop under the key` or `rim only,
separating <subject> from the background`. If a request would make the two sources
equal and frontal, say why not (flat front light is the one ban) and offer soft
cross instead.

### Temperature carries a Kelvin, and the Kelvin is per SCENE

Three words are three buckets, and the look lives on a continuum inside them —
but worse, a word cannot hold still: `warm` written into eight shots of one room
is eight independent guesses at how warm, and the room changes temperature
across its own cuts. So the block states a number as well as the character:

| Word | Kelvin | Reads as |
|---|---|---|
| warm | 3200 K | tungsten, candle, practical lamps |
| warm-neutral | 4000 K | mixed interior, late afternoon through glass |
| neutral | 5200 K | clean daylight, overcast noon |
| cool | 5600 K | open shade, north light |
| cold | 8500 K | blue hour, moonlight, deep shade |

**Resolve it once per scene and paste the same number into every shot of that
scene**, alongside the character phrase — `warm tungsten character, 3200 K`.
Where a scene genuinely mixes sources (a tungsten interior with a cold window),
each source carries its own number and the contrast is the point; that is the
one case the two values differ inside one block.

**This never becomes a board pill.** The user picked a photograph of a lighting
setup; 5200 versus 5600 is not a choice anyone can judge from a chip, and adding
it would turn the board into a form. The word is the user's decision, the
Kelvin is yours — derived from the word, the location, and the time of day, and
written into the shot block and the scene picture's prompt when the user chose
the light on the board (`prompt-blocks.md`, Part 2, *The card's own picks*);
a light nobody chose writes nothing.

## Which side is dark — always stated

Except for `overcast` and `auto`, which have no side to name, the block always
ends by naming the shadow side relative to camera:
`camera-left of the face lit, camera-right falling dark` (or the reverse).

**Three of the exterior setups have a dark that is not a side, and they name it
anyway.** Where the source is overhead — `open shade`, `street light`, and
`overhead fall` before them — the dark runs DOWNWARD and the block says so:
`brow, under the nose and under the jaw in shadow, no side dark`. And
`dappled shade` is the one setup in the vocabulary whose shadow is a shape
rather than a direction, so it names where the shape falls:
`a hot patch across the camera-left cheek, the mouth in a gap`. The law is that
you can never leave the dark unstated, not that the dark is always lateral.
Between
shots of the same scene this line only flips when the camera crosses to the other
side of the subject per the location map — light direction is continuity, and a
join where the dark side jumps reads as a different room.

## What the user is choosing from

Sixteen of the seventeen setups carry a **generated photograph** in the shot
list's `Light` panel and the review board's orb — one girl, one wardrobe, one
framing, relit sixteen times, so the library differs in nothing but the light.
`auto` has none: it compiles to the location's own sources, so it names no light
to photograph.

There are two control plates, not one, and the reason is worth knowing: the ten
interior setups are relit from a girl in a plain room, and the six exterior ones
from the same girl moved outdoors, generated image-to-image from the first plate
so the library is one casting throughout. Indoors the relighting instruction is
"change only the light"; outdoors it cannot be, because the sky IS the source —
golden hour without an orange sky is not golden hour. So the exterior six move
the light and the sky together and hold everything else.

This matters for how a chosen id is handled. **The user picked a picture of a
sentence, and that sentence is the one the id compiles to.** So when `light`
comes back from a board, its fragment is not a starting point to reword — it is the thing the
user agreed to. Look it up, resolve its placeholders from the scene, and paste
it into the scene picture's prompt unchanged. Writing your own lighting line instead is how a shot
ends up lit differently from the tile the user chose it by.

**The placeholders, all five, and where each is resolved from:**

| Placeholder | In | Resolved from |
|---|---|---|
| `<position>` | window | where the window is in the location asset, named relative to camera — `camera-right` |
| `<named practical>` | night practical | the source the scene actually contains — `a single table lamp`, `the car's headlights`, `the vending machine` |
| `<source>` | silhouette | the bright thing behind the subject — `the doorway`, `the window`, `the sky` |
| `<direction>` | soft cross, golden hour, moonlight | a clock position from the grid above, camera at 6 — `9 o'clock`, `high at 2 o'clock and behind her` |
| `<breakup>` | dappled shade | what is breaking the sun in this location — `the leaves of a plane tree`, `a slatted canopy`, `a fire escape` |

A placeholder left unresolved reaches the model as literal angle brackets, and a
placeholder resolved to something the location does not contain is a shot lit by
a lamp that is not in the scene. Both are worse than the id alone.

**The six exterior setups carry the sky with them.** Indoors the Lighting block
can name a source and stop; outdoors the sky IS the source, so the block also
says what the sky is doing — `deep amber low where the sun is, cooling to blue
overhead` for golden hour, `flat black, nothing in it` for street light. This is
not decoration. It is the same fact as the light, and a golden hour prompt that
does not say the sky is gold gets a shot lit at noon.

## Without boards

One question per shot at most: offer the 3 setups that fit the scene's location
asset and time of day (preview = the fragment and the still). The scene's
default comes from the location descriptor's light line; only shots that deviate
need asking at all.

**Seventeen setups do not mean a longer question.** It is still three, and the
grouping above is how you get to three: an INT. scene is not offered
`golden hour`, and a night exterior is choosing between `street light`,
`moonlight` and `practicals`, not between all seventeen. Read the location
asset's own light line first — it usually names the group, and often the setup.
