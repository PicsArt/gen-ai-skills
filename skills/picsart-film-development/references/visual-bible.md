# References and the visual bible — optional inspiration within Stage 1

Nothing in this file is a stage or a gate. The look is locked on the console at
Stage 1 step 2; the counts and categories below are for a user who wants a
reference board beside it, and the descriptors are written at `picsart-film-assets`
step 1.

## Reference counts that actually hold

| Asset | Gather | How many |
|---|---|---|
| Lead character | face type (photos of similar people or actors), build and movement, costume **by item** (jacket separately, shoes separately), hairstyle, age markers | 10–20 |
| Supporting character | same, lighter | 5–10 |
| Key location | wides from several points, textures (walls, floor, furniture), light in this space at the needed time of day, real prototypes | 8–15 |
| Prop | the exact object or nearest analogue, material, condition (new/worn), scale in hand | 3–5 |

The character who is in 80% of scenes needs the densest board, not the thinnest —
the temptation runs the other way because everyone already "knows" the lead.

## The seven style categories

| Category | Gather |
|---|---|
| Light | stills with the needed light character: hard/soft, backlight, practicals, time of day |
| Colour and grade | stills with the palette and grading character; palettes per storyline |
| Optics and composition | wide/long lens examples, shot sizes, anamorphic, depth of field |
| Camera movement | scenes (film + timecode): handheld, static, dolly, drone |
| Image texture | film/digital, grain, defects, the era of the image |
| Cutting tempo | example scenes of editing rhythm (film + timecode) |
| Sound and music | reference tracks, atmospheres — gathered now, used at Stage 10 |

The camera is fixed on the shot list at Stage 1 step 6, before any of these
boards exist; a board informs the descriptors and the captions, never the shot
list after its yes.

## Rules for the boards

1. **One reference answers one question**, and the caption says which: "light from
   the window", "brick texture", "jacket fit".
2. **Anti-references are collected deliberately** — "like this: not allowed". They
   become the bans written (in positive form) into the prompts' constraint block.
3. Sources: film stills (ShotDeck, Film-Grab), photography, painting, the user's
   own photos of prototype places — real photos of the neighbourhood where the
   film "lives" beat any words.
4. One board = one asset or one category, captioned, in one place. The board is
   recorded in `film.json.assets[].board` / `bible.styleBoards` as a list of image
   URLs + captions — save the images to `picsart_drive`, CDN links expire.

## From boards to text

**No review session.** The boards are read, not dispositioned;
what gets approved is the asset sheet each one produced, on
`picsart_asset_review` in Stage 4 — one tile, one click. The look itself is
locked on the console at Stage 1 step 2.

**Text portraits** (characters) — the Stage 4 descriptor itself: appearance,
age, build, costume by item, movement, characteristic posture. **Location
descriptions**: architecture, textures, light, condition, atmosphere, palette of
the world. Concrete words only; "stylish" is not a word a model can hold. Each
rides onto its sheet's tile as the `prompt`, so the user approves words and
picture together.

**Film setup** — the console pass runs at Stage 1 (`picsart_film_setup`, or the
text-choice fallback from `../../picsart-film/references/presets-looks.md`). Its style
prefix is stored verbatim per world at Lock and every sheet is generated under
it. When a scheme is chosen, `bible.palette` names its colours and the materials
that carry them, and is baked into every location descriptor. With scheme Auto,
each location names its own colours. The finishing grade refines this direction.

On a short, one batch is the whole asset list and every picture generates
in one pass.
