# Film-setup presets — genre, tone, colour scheme, delivery, camera and lens

The vocabulary behind `picsart_film_setup` and its text-choice fallback
(`picsart-film-development`, Stage 1 step 2). Every preset compiles to an exact text fragment; the
selected fragments assemble into the **style prefix** — the block pasted word for
word into every prompt of the world it belongs to. One world, one prefix. Never
paraphrase a fragment at prompt time: the value of a preset is that it is verbatim.

The server owns the exact prompt wording. Pass preset ids to the compile tools;
use this reference to choose ids and interpret the returned clauses.

## Assembly recipe

```
STYLE — <genre>. [<tone>.] [<colour scheme>.]
<camera>. <lens>.
<frame>.
```

`<tone>` is bracketed because it is present only when a tone other than Auto
is chosen (see *Tone — an era recipe*), and `<colour scheme>` only when a
scheme other than Auto is chosen (see *Colour*); Auto contributes no clause,
and so does an `Auto` camera or lens. There is no palette, focal-length,
aperture, grain or framing clause from the setup — *What the setup does not
decide*, below. A `palette 60:30:10 — …` clause
appears only when a caller passes a palette id or a colour reference to the
compiler — a shot's own colour, never the setup's.

Lock the assembled prefix in the bible (`bible.stylePrefix`) the moment the user
locks the look at Stage 1 step 2 — that answer is the lock. Changing any component afterwards is a new bible version, announced,
never a drift.

### Why these controls and not others

Three of the setup's regions answer questions nothing else in the pipeline
answers:

- **The frame** bounds every generation. A scope landscape film is a different
  brief from a vertical one, whatever the genre. It is also the one decision here
  that constrains which MODELS can be used at all, so it is not merely a look.
- **Colour is a scheme around a hue, not a palette.** The film
  decides how its colours relate — one hue, neighbours, opposites, a triad —
  and which hue it is built around; which exact colours land on which surface
  is decided per shot and per location. A palette at setup would ask the user
  to pick a whole colour world before a single location exists.
- **The rig is two decisions** (body and glass), because they are the two that
  hold for the whole film. Focal length and aperture are on the shot list: how
  wide and how deep is a per-shot framing decision, and a film-wide 35mm would
  argue with every close-up.

Each question has one owner. Camera owns the capture medium — body and stock —
and the grain, which is a property of the stock and rides in its fragment; the
shot owns its light and its framing (see below). Story period lives in the
location descriptors and scene context, never in an image-look preset.

Genre keeps `noir` and `epic` alongside `thriller` and `fantasy`, because each
names a convention the other does not imply.

**A tone is a *recipe*, not a medium clause:** picking one sets the Camera and
Lens pills to the values that make a named era of cinema, and adds one short
clause for what no pill owns. It compiles nothing a pill compiles, so the
prefix still answers each question once. It sets no colour — *Tone*, below.

## Genre — how scenes are staged and performed

The register every shot inherits.

**Ids:** `drama` · `thriller` · `noir` · `action` · `comedy` · `doc` · `epic` · `fantasy` · `horror` · `romance`

*(The sentence each id compiles to lives server-side. Pass the id to `picsart_film_compile_prompt` — or `picsart_film_compile_asset_prompt` for a character reference — and it pastes the tuned wording; never write that sentence yourself.)*

**A custom genre compiles without its id in the scene/look compiler.** The card carries `genre: "custom"`
beside `customGenre`, but the compiler has no `custom` genre and refuses it:
pass `look.customGenre` alone and leave `look.genre` out, as the web console
does. A custom tone there uses `look.tone: "custom"` plus `look.customTone`.
The asset compiler has its own top-level schema; inspect its supported fields.

**Noir and epic are their own registers, not flavours of thriller and fantasy.**
Noir owns a lighting and surface convention (slatted hard shadow, wet street,
night-for-night black) that a thriller does not have to use; epic owns scale
against a landscape, which a fantasy does not have to have. Fantasy is
therefore worded to claim only what is always fantasy's: the invented world and the
painted light, never "epic imagery" or "scale in the frame", which are epic's.

## Colour — a scheme around a hue

The setup's Colour decision is two values: a **scheme** — how the film's hues
relate — and the **hue** it is built around. That is all the setup says about
colour.

**Scheme ids:** `auto` · `monochromatic` · `analogous` · `complementary` · `triadic`

**Hue:** one of the wheel's twelve names, one per 30°, red at the top —
`red` 0 · `orange` 30 · `amber` 60 · `lime` 90 · `green` 120 · `jade` 150 ·
`teal` 180 · `sky blue` 210 · `blue` 240 · `violet` 270 · `magenta` 300 ·
`rose` 330. The compiler takes any colour word, but these twelve are what the
console sends, and a colourist's word reads better in a prompt than a degree.
The card carries the angle too, as `hueDegrees`: pre-set it to the name's
angle above, and keep whatever comes back as it was sent — a wheel turned to
130° comes back as `green` + `130`, and only the number reopens it at 130°.
The compilers never read the number.

*(The sentence each scheme compiles to lives server-side — pass `look.scheme` and `look.hue` to `picsart_film_compile_prompt`.)*

| Scheme | What it asks for |
|---|---|
| auto | nothing at film level — each shot picks its own colour |
| monochromatic | one hue, lighter and darker |
| analogous | the hue dominant, its two neighbours supporting |
| complementary | the hue dominant, its opposite used sparingly |
| triadic | three evenly spaced hues — dominant, secondary, accent |

**Rules**

- **Auto is the default and compiles to nothing.** Pre-set a scheme only when
  the material names a colour — "everything amber", "a cold blue world", "red
  against green". The scheme is the relationship; the hue is the colour named.
- **The colour is always the user's.** No tone sets it or changes it, and
  changing it never flips a tone to Auto — "IMAX, built around amber" is a film
  someone might want to make.
- **`hue` is read only beside a scheme.** A hue with scheme Auto is dropped.
- **Pass it everywhere the film's look goes** — `look.scheme` / `look.hue`
  (inside `look`) on every `picsart_film_compile_prompt`, and top-level `scheme` /
  `hue` on every `picsart_film_compile_asset_prompt`, which takes no `look` object
  and drops one without an error. Left off the asset call, the shots are graded
  to the hue while the cast's references are graded to nothing, and the cast
  arrives looking like it belongs to another film.
- **The bible's palette line is written from it.** `bible.palette` names the
  scheme's colours in the film's own materials: the dominant is the hue, the
  secondary and accent sit where the scheme puts them — analogous, the two
  neighbours; complementary, the opposite as the accent; triadic, the two hues a
  third of the wheel away; monochromatic, lighter and darker versions of the one
  hue. Name each as **a colour plus what carries it** — "amber lamplight on old
  plaster", not "amber". A bare hue tells a model nothing about the surface it
  lands on, and the palette line's job is to survive into the location
  descriptors, so the grade at finishing refines instead of inventing. With
  scheme Auto there is no film palette line; each location names its own colours.

### Palettes — the shot's colour, not the setup's

The seventeen palette presets are the shot list's `palette` value, for a shot
that needs a colour of its own (a flashback, a world the scene crosses into),
and an id the compiler accepts as `look.palette`. A card's palette is `auto` unless the
shot needs one.

| Preset | Swatches 60 · 30 · 10 |
|---|---|
| slate | #4a5a78 · #8a7a5e · #c4362b |
| sodium | #c87a3a · #1e1a18 · #3fb8c4 |
| bone | #d9cba8 · #a08a64 · #3ea9a0 |
| kitchen | #d9b26a · #6b4a32 · #6e93a8 |
| clinic | #e6e9e8 · #afbab2 · #a81e20 |
| neon | #14161c · #232a4a · #d9319b |
| pine | #2e4034 · #9aa3a0 · #d96a1e |
| fresco | #c1795a · #8a8f63 · #2e4c8f |
| teal | #2f5f66 · #a89272 · #e8621a |
| bleach | #8e9195 · #6b6b52 · #c9b23f |
| mono | #1a1a1c · #8a8a8e · #f5f5f5 |
| pastel | #e8b9bd · #f0e2bd · #cf2a34 |
| sulphur | #7c8340 · #8d9095 · #5e1f27 |
| sepia | #6b4f34 · #a8977f · #4e8b7a |
| kodachrome | #e3c9a0 · #8c9096 · #c8202f |
| lacquer | #9b1c1c · #4a3223 · #2f9c7a |
| ink | #101a2b · #4d5563 · #e8f0ff |

*(The sentence each id compiles to lives server-side — pass the id to `picsart_film_compile_prompt`.)*

The hexes are for *showing* a palette — a 60:30:10 chip row; the words are what
compile. `mono` is the only preset with no hue: its 10% is a value (one blown
white highlight), not a colour.

**A shot's palette must sit inside the film's scheme.** Every preset already is
a scheme (`sodium` is complementary, `mono` monochromatic), and its first swatch
is its dominant. When a palette's scheme, or its dominant, argues with the film's
scheme and hue, `picsart_film_compile_prompt` returns a warning in `notes` — the prefix
would name two different dominant colours. Do not dispatch past it: tell the
user, then drop the palette or pick one whose dominant is the film's hue.

Choosing between neighbours:

| Preset | Its nearest neighbour, and why they are not the same |
|---|---|
| teal | `sodium` is orange-dominant **night** and `slate` is blue **dusk**. Teal is cold **daylight**. |
| bleach | `clinic` is clean white daylight in a maintained building. Bleach is silver-olive grime and crushed contrast in one nobody maintains. |
| pastel | `fresco` is hot, aged, sun-bleached plaster. Pastel is cool, new and confected. |
| sulphur | `pine` is cold, natural and outdoors. This green comes out of a failing tube and makes everything under it look ill. |
| sepia | `kitchen` is warm **light** on domestic surfaces. Sepia is warm **pigment** — the colour of age, with nothing lit warmly at all. |
| kodachrome | `pastel` is cool and confected; `bone` is drained desert. This is saturated, sun-baked slide-film colour. |
| lacquer | `kitchen` is domestic, `fresco` is bleached. This is saturated pigment on studio surfaces — red lacquer, gold silk, incense haze. |
| ink | `slate` is dusk with the warmth of habitation in it. Ink is night with none: blue-black, wet concrete, one cold point of light. |

**What earns the accent** is per-film, so it is not part of a scheme or a
preset. Decide it while designing the assets and carry it in the asset
descriptors — "the accent belongs to the brothers' car" is a line in the bible,
not a clause in the prefix.

**Swatches** fill the `[HEX Values: …]` field of the modern-path portrait
template — the `imax` tone, and Auto (`../../picsart-film-assets/references/asset-sheets.md`,
*The portrait prompt*) — **only when a palette id is passed** to
`picsart_film_compile_asset_prompt`. A scheme has no swatches: with a scheme and no
palette the field is left out and named in `notes`, and the scheme clause
carries the colour.

## Tone — an era recipe

The look's second decision, between Genre and Colour. A tone is **a recipe,
not a clause**: picking one sets the Camera and Lens pills to the values that
make a named era of cinema — 1980s American drama, 1990s neon Hong
Kong — and adds **one short clause of its own** for what no pill owns: the
era's name and the optical artefacts that travel with it (halation, bloom,
chromatic aberration, lens breathing, step printing). Everything else a tone
implies is said by the pill it set, once.

A typical era-look prompt is one paragraph bundling camera body, lens model,
stock, grade, lighting, era, and sometimes ratio and framing. Compiled beside
the rig it would say "Kodak 5294" next to "35mm film stock" and "Panavision
anamorphic" next to "anamorphic glass" — two instructions for one question. So
each tone takes the bundle apart: body and stock → a Camera preset (the five
named stocks below), glass → a Lens preset (`panchro`, `kinoptik`, `cseries`
where the era names one), grain → the stock's own fragment, and the remainder
→ the tone's own clause.

**A recipe is the rig and nothing else.** Focal length and aperture are per
shot, and the colour is the user's — a tone is a way of rendering, not a
colour. Dune and Oppenheimer are both large-format IMAX and neither is blue, so
an era that dictated a palette would decide something the user had not asked
it to.

**What a tone clause may not contain**: a camera body or stock, a lens choice,
a focal length or aperture, grain, any lighting, an aspect ratio, framing, a
camera move, or a named person. The first eight belong to a pill or to the
shot; the last is an IP exposure a shipped preset does not take — era looks
are often described by director or cinematographer, and the technique words
carry the look without them. Colour language in a clause is **grade
character** (saturation, how shadows and highlights split), never a list of
hues: hues are the colour scheme's. `Kodachrome` in the summer tone's clause
is a colour word, and that recipe's Camera is generic 35mm, so it is not a
second stock statement.

| Preset | Sets |
|---|---|
| auto | *(nothing)* |
| italian60 | camera `technicolor` · lens `panchro` |
| american80 | camera `5294` · lens `ana` |
| summer80 | camera `35mm` · lens `ana` |
| hongkong80 | camera `35mm` · lens `vintage` |
| neonhk90 | camera `500t` · lens `kinoptik` |
| american90 | camera `5298` · lens `ana` |
| imax | camera `imax` · lens `cseries` |

*(The sentence each id compiles to lives server-side — pass the id to `picsart_film_compile_prompt`.)*

There is no separate modern indie-drama tone: desaturated natural light,
shallow focus, anamorphic glass and warm skin against a cool environment is
what `american90` already says. A tone earns its place only with a fragment
its nearest neighbour does not imply.

**Rules**

- **Auto is the default and compiles to nothing.** The defaults below
  are already a filmic look; a tone is an opinion about an era, and no film
  holds one until someone picks it. `imax` is one choice among seven, not the
  default, because "cold and desolate" is a grade, not a neutral.
- **Changing the Camera or the Lens flips the tone to Auto.** The pills keep
  the values they have (that film is the user's now) and the tone's clause
  leaves the prefix, so the prefix never claims an era whose recipe was edited.
  Colour, Frame, Duration and Genre are not part of any recipe and do
  not flip it — a user who turns the colour wheel keeps their era.
- **Grain rides in the stock, not in a control.** The stock fragment already
  says it: Fuji 500T says "heavy grain" itself; the Hong Kong studio clause
  carries "vintage film texture". A film-wide framing default would paste
  "default to medium shots" into every prompt of a film whose tone says
  nothing about framing, exactly the kind of addition that breaks a tone.
- **Lighting is not carried.** Every era look comes with a lighting setup —
  neon practicals only, a golden-hour key with fluorescent fill, soft stage
  light. Lighting is per shot (`../../picsart-film-scenes/references/presets-lighting.md`),
  whose library already has `night practical`, `practicals`, `golden hour` and
  `street light` for exactly these looks.
- **Story period is not a look.** "80s settings" in an era prompt is
  when the story happens; it lives in the location descriptors and the scene
  context. The character sheets inherit the tone through the style
  prefix, but era styling of the *person* — hair, grooming, wardrobe — is the
  descriptor's job, not the tone's: the assets stage writes the cast to the
  tone's era, and when the story's period disagrees it says so once and the
  user decides (`../../picsart-film-assets/references/workflow.md`, *The conveyor*, step 1).
- **Seeding.** Pre-set a tone by writing its id and the two pills it sets.
  Expand the recipe *before* applying any pill the material names explicitly,
  so an explicit pill always wins over the recipe. An unknown id is dropped
  like any other.
- **Every tone but Auto plays a preview clip** on the console — four seconds
  each, one control (a woman at the wheel through an open driver's window).
  The colour in a tone's clip is not part of the tone. The row is clips, not
  stills, because three of these clauses name artefacts a single frame cannot
  hold: step-printed stutter, flicker, lens breathing. `Auto` compiles nothing,
  so it shows a plain gradient.

## Lighting is not a film-wide decision — it lives on the shot

There is no light control here, and there is no `light` clause in the prefix.
Lighting is the one look decision that cannot honestly be made once for a whole
film: a film has one genre and one colour scheme, but a night exterior and a
kitchen morning are not lit the same way, and no film worth making is.

A prefix clause is pasted into **every** prompt. A prefix saying `soft
motivated daylight, wrapping key from a window` would arrive at the shot
designer's Lighting block — which is built on one motivated source, its
direction named, and which side of the face is dark ([presets-lighting.md](../../picsart-film-scenes/references/presets-lighting.md)) —
and contradict it on every night, practical and firelight shot in the film. Two lighting instructions in one prompt is worse
than one, and the shot's is the one that knows what room it is in.

So lighting is decided where the scene is: the shot list's `Light` value and the
closed question that asks for it, both from [presets-lighting.md](../../picsart-film-scenes/references/presets-lighting.md). The film-wide
mood belongs in **genre** (noir
owns chiaroscuro; doc owns available light) and in **colour** — the scheme,
and the palette line the locations carry, which names what the light lands on.

## Delivery — the bounds every generation inherits

### Frame

**Every frame here is one video models render BROADLY, and that is the whole
selection rule.** Check a model's own `aspectRatio` enum with
`picsart_model_params`. Video models do not accept 2.39:1, 1.85:1 or 4:5, and
`2:1` and `3:2` exist on one or two families only. A frame the pipeline cannot
deliver comes back in whatever the model does support, while the style prefix
goes on claiming that frame for the whole film.

Ordered widest to tallest, which is also how the picker draws them (the glyphs
are true-proportion boxes, so a support-ordered list would look scrambled).

| Preset | Shown as | Renders on |
|---|---|---|
| 169 | 16:9 | every model |
| 43 | 4:3 | most models |
| sq | 1:1 | most models |
| 34 | 3:4 | most models |
| vert | 9:16 | every model |

*(The sentence each id compiles to lives server-side — pass the id to `picsart_film_compile_prompt`.)*

**16:9 is the widest frame offered, and scope is a crop in the edit.** 21:9
exists on Seedance, Luma, Hailuo, Flux and PixVerse and is deliberately NOT
offered: putting a frame that works on five model families beside frames that
work everywhere invites a director to pick the one choice that later rules out
most of their models. If the user asks for scope, say so plainly — "no video
model renders 2.39:1, and 21:9 would tie us to a handful of models; shoot 16:9
and crop to scope in the edit, which is how anamorphic dailies are handled
anyway" — rather than treating the gap as an oversight.

### Say the frame however it comes up — every spelling resolves

**You do not have to remember `vert`.** The preset id, the label and the plain
word all name the same frame, so all of these select 9:16:

```
vert · 9:16 · 9x16 · vertical · portrait · phone · tiktok · reels · shorts · story
```

Same for the rest: `16:9` / `landscape` / `widescreen` / `wide` → `169`; `1:1` /
`square` → `sq`; `4:3` → `43`; `3:4` → `34`. Case and surrounding spaces do not
matter.

**This tolerance is what keeps a pre-set honest.** A user who asks for
vertical in chat must not see the setup open on a landscape frame because the
pre-set used a spelling the ids did not match — that shows them the default
wearing the clothes of a decision. Anything genuinely unrecognisable still
falls back to the default rather than being guessed at, because a guess
presented as a decision already made is that same defect.

### Shot length — on the shot list

Shot length is a per-shot call on the shot list, whose Length value offers
exactly the durations the chosen model accepts. A film-wide shot length would
be a promise the model is free to refuse. One frame-shaped decision belongs to
the film; how long any one shot runs belongs to the shot.

### Duration — the whole film, not one shot

`duration` is the film's target running time in seconds. It is a number rather
than a preset: any positive whole number is valid, and the default is
`90`. The user may say it as a number or naturally (`47
seconds`, `1:30`, `2.5 minutes`); record it as a whole number of seconds.
This is the total the preliminary shot list is planned to hit and the
animatic later checks within ±10%; it never constrains an individual shot or the
model used to render it.

Like `handles`, Duration compiles to nothing in the style prefix. It is
stored as a number in `film.json.target.duration`, not in
`bible.setup`: runtime is a production bound, not a visual-world clause.

### Handles — the film's generation policy

The setup console does not display or return `handles`. Keep the film's
existing handle policy independently; a missing key in setup feedback does not
turn it off. When the policy changes, record the user's decision and include
its duration cost in the normal generation preflight.

The run-level rules live in `../../picsart-film-scenes/references/overview.md`: handles belong only
at the two outer ends of a generated run, not around every internal shot.
`on` requests trim room within the live model ceiling; `off` requests the
planned cut length. Handle policy contributes no STYLE clause.

## Camera — two independent decisions

What it is shot on, and how the glass renders. Both lead with **`auto`, which
compiles to nothing.** A user with no opinion about the glass says so in one
click rather than being made to invent one, and a prefix with no lens clause is
better than one with a guessed clause. How wide and how deep each shot is are
not here: focal length and aperture are per shot (*What the setup does not
decide*, below).

### Camera — what it is shot on

Owns the capture medium: body, stock, and the artefacts that come with it.

**Ids:** `auto` · `alexa` · `red` · `35mm` · `16mm` · `super8` · `camcorder` · `phone` · `technicolor` · `5294` · `500t` · `5298` · `imax`

*(The sentence each id compiles to lives server-side. Pass the id to `picsart_film_compile_prompt` — or `picsart_film_compile_asset_prompt` for a character reference — and it pastes the tuned wording; never write that sentence yourself.)*

**The last five are named stocks with their bodies, used by the tone
recipes.** Era looks name the body and the stock — "Arriflex
35 BL4, Kodak 5294", "Fuji 500T pushed two stops" — because those names carry
colour rendering, grain and highlight behaviour in words the model has seen
millions of times. Camera owns the capture medium, body and stock alike, so both
live here in one fragment, chosen by a tone or by hand; a tone never says either
name a second time in its own clause.

### Lens — how the glass renders

A lens **family**, never a focal length: how the glass draws the picture is a
film-level decision; how wide it is belongs to each shot on the shot list.

| Id | On the card |
|---|---|
| auto | Auto |
| prime | Spherical |
| ana | Anamorphic |
| vintage | Vintage spherical |
| vintage-ana | Vintage anamorphic |
| macro | Macro |
| fisheye | Fisheye |
| probe | Probe / periscope |
| tilt | Tilt-shift |
| panchro | Cooke Speed Panchro |
| kinoptik | Kinoptik ultra-wide |
| cseries | Panavision C-series |

The eight after Auto are the families; the last three are the named lenses the
tone recipes use. There is no `zoom`: a zoom is a focal-length behaviour, not a
way the glass renders, so it belongs with the focal length on the shot.
`fisheye` deliberately asks for the curvature a straight-line
shot would forbid: pick it only when the user wants the whole film warped.

*(The sentence each id compiles to lives server-side. Pass the id to `picsart_film_compile_prompt` — or `picsart_film_compile_asset_prompt` for a character reference — and it pastes the tuned wording; never write that sentence yourself.)*

**A lens describes glass; it never describes the shape of the frame.** A lens
fragment ending on *"wide compressed frame"* is a straight contradiction on a
vertical film: the model is told in one breath that the picture is wide and
that it is tall. The frame's shape belongs to the Ratio preset alone, which is
the only thing that knows what the film chose, and it says so in every prompt
already. What the glass actually does — oval bokeh, horizontal flares,
softness, distortion toward the edges — is true at any ratio, so that is all
the lens rows say. Anamorphic's squeeze is real optics, but the wide picture is
what a *projector* does with it, not what the lens renders, and a vertical film
never gets there.

**The last three are named lenses for the tone recipes**, for the same reason as the named stocks: the glass an era look names is part
of what makes its era read. Lens owns the glass, so each lives here as a normal
preset and a tone's own clause never repeats it. `kinoptik` deliberately does
not state a focal length — each shot's lens owns that.

## What the setup does not decide

### Focal length, aperture and palette — on the shot

Each is a decision a film-wide value would get wrong for most of its shots: a
film-wide 35mm argues with every close-up, a film-wide f/2.8 with every wide
that needs the room in focus, and a film-wide palette decides the colour of
locations nobody has designed yet.

- **Focal length** is the shot card's `lens` — a field-of-view anchor proposed
  from the shot size (`../../picsart-film-scenes/references/presets-camera.md`, *FOV*).
- **Aperture** is the shot's own ([presets-camera.md](../../picsart-film-scenes/references/presets-camera.md), *Aperture / depth*).
- **Palette** is the shot card's `palette`, `auto` unless the shot needs a
  colour of its own; the film's colour is its scheme and hue (*Colour*, above).

### Grain and framing — in the stock and on the shot

A grain control would compile a texture clause beside a Camera fragment that
already names one — "35mm film stock: organic grain" — and the named stocks
carry theirs outright ("Fuji 500T pushed two stops: heavy grain"), so it would
be a second answer to a question Camera owns. A framing default would compile
"default to medium shots, figure plus readable room" into every prompt of the
film, while the shot list decides size per shot from the nine-rung ladder
(`../../picsart-film-scenes/references/presets-camera.md`). Grain that a film
wants is said by its Camera preset; framing is a shot card's `size`.

### Movement — on the shot

A world-level move is pasted into **every** prompt of the film, before any shot
has a subject or a direction, so it argues with the shot list's own
`Camera move` value on every shot that has chosen one. A shot that asked for
`Orbit` would be overruled by a style prefix chosen before the shot existed.

The move is a per-shot decision, from all 50 moves in
`../../picsart-film-scenes/references/presets-camera.md` — the same library the shot
list's `Camera move` control draws, so a move means one thing across the film.

### Pacing — written, not set

There is no pacing control on any surface. A tempo scale compiles to one tempo
adjective pasted into every prompt before a beat exists — "cuts only after a
moment plays out, shots at rest" — and the films come out slow.

Rhythm is **written, never set**: the shot blocks' seconds say how many
beats a cut holds and how long each runs, and the card's `sec` says how long
the shot is. Tempo words (slow, calm, measured, brisk, urgent) do not appear
in the prefix or in a header; a shot that should feel slow has less happening
in more seconds.

## Defaults — what the setup starts from

```
genre drama · tone auto · colour auto (no scheme)
frame 169 · duration 90
camera 35mm · lens ana
```

These are a defensible film, not a placeholder: nothing is ever blocked
waiting for input, and there is no "incomplete setup" state. They are what you
state and invite correction on.

**The frame default is the one you must not leave to chance.** `169` is here
because it is the single frame every video model renders — not because the film
is landscape. A default cannot read the user's mind, but you can: the moment they
say vertical, portrait, phone, TikTok, Reels, Shorts, square, widescreen or
scope, pre-set the frame to what they said. A user who asked for vertical and got
landscape was not given a default, they were given the wrong answer.

## Infer first — never ask what the material already answers

Because everything already has a default, a pre-set is not one fewer blank to
fill — it is **a better starting point than the default**. Fill only what the
script, logline, or moodboard actually decides, each with a one-line why: a
palace-intrigue logline answers `genre`; an all-photochemical moodboard answers
`camera` (a found-footage premise answers it too — `camcorder` carries its own
noise); a script that names a period or a cinema tradition — "Hong Kong, 1994", "like a seventies Italian drama" —
answers `tone`, and the recipe is expanded into the pills before the picks are
shown; a brief that names a colour — "everything amber", "cold blue" — answers
`scheme` and `hue`.

Leave the rest alone. A wrong pre-set is worse than a default, because the user
reads it as a decision someone already made.

## Running the setup from this file

Open `picsart_film_setup` with the inferred values in `suggested.selections`
and the reason for each in `suggested.why`. On reopening, pass the locked
values as `current.selections`, including `hueDegrees`. Store submitted
`film_setup_feedback` per `widget-feedback.md`; an initial tool result is a
preview, not approval. If the console is unavailable, use the host's question
interface or a concise text choice with the same values.

Compile the accepted setup with `picsart_film_compile_prompt`, `kind: "look"`,
when its returned style prefix is empty. Map `ratio` to `look.frame`, omit a
`custom` genre id while passing `look.customGenre`, and preserve custom tone
wording. Keep the returned prefix verbatim. The asset compiler takes its colour
fields at the top level, as documented under Colour.
