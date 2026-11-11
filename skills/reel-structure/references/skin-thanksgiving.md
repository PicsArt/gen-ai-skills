# Thanksgiving and Friendsgiving skin

The full skin for Thanksgiving and Friendsgiving reels. The skins table in style-library.md has one row
for each; this file is what to apply when the occasion read from the media or the user's words is
Thanksgiving or Friendsgiving: a family or friends' dinner, a roast or pies on a table, autumn table
decorations, a late-November date. The style keeps its structure; the skin changes the words, colours,
fonts, grade and the few marks on top. Everything here is free: no generation, no paid tool.

## Words

| | Thanksgiving | Friendsgiving |
|---|---|---|
| Title (pick one) | Happy Thanksgiving · Thankful · Grateful for you · Thanksgiving <year> | Friendsgiving · Happy Friendsgiving · Friendsgiving <year> |
| Kicker (small line under the title) | blessed beyond measure · around our table · family, food and thanks | good food, better people · our table · thankful for you all |
| List heading (Thankful list) | Thankful for | Thankful for you |
| Labels (a style with one label per photo) | the dish or the person, from what the photo shows: "the turkey", "grandma's pie", "the table", "everyone" | the friend or the dish: "the hosts", "the potluck", "the table", "the crew" |

- Put a year in a title only when the media's own date gives it (a capture date in late November).
  With no date, use a title with no year. Never a filler year.
- A title the user gives replaces the skin's. Their names for people and dishes replace the labels.
- No more than one title and one kicker on screen at once. Labels stay 2–3 words.

## Colours

| Role | Hex | Where |
|---|---|---|
| Background | #2B1608 | dark pages, title cards, the ground behind framed photos |
| Text | #FFF4E0 | titles, kickers, labels on dark |
| Accent | #C4581F | burnt orange: one word of the title, ticks, frames, a mark |
| Second accent | #E8A33D | warm amber: the glow on a title, a second mark |
| Light page | #F6EBDD | a style on a light page; text on it is #2B1608 |

Friendsgiving uses the same colours with the accent swapped to the amber (#E8A33D), so the reel reads a
little lighter.

The two accents are for dark ground only (#2B1608 cards, dark pages). Over footage or a light page, every
word is #FFF4E0 over footage or #2B1608 on the light page; the accents then go on ticks, frames and marks,
never on letters.

**Words over footage.** A title or kicker held over moving footage sits on a #2B1608 scrim band behind the
whole title block, at 50 % opacity in its middle and fading to 0 at its top and bottom edges, plus a soft
dark shadow on each line. Check it on the brightest frame the words cross: every letter must read at 360 px
wide.

## Fonts

All are in the engine's font catalog (`font.family` keys):
- **Title**: `edwardianscriptitcstd-regular`, at least 150 px tall in the 1080 × 1920 frame, so it reads at
  phone size. For a title longer than 16 characters, use `kaufmannstd` at 130 px instead.
- **Kicker and labels**: `baskervillemtstd-regular` in capitals, 34–40 px, letter-spaced 0.12 em.
- **Small lines** (a list, a counter, a long caption): `montserrat`, 40–60 px.

## Grade

The skin warms the style's look; it never replaces it. On every photo and clip:
1. `effect:adjust`: temperature 0.18, tint 0.03, saturation 0.08, highlights −0.1, shadows 0.05. On a
   layer that uses `look:blur_fill`, put the adjust on a group around the layer, not on the media layer
   itself, or the blurred fill is lost.
2. The film finish: when the style already names `look:analog_film_finish`, keep its grain, dust and
   vignette and only add tint #E8A33D at tintAmount 0.12. When it names none, add
   `look:analog_film_finish`: grain 0.15, dust 0, vignette 0.3, tint #E8A33D, tintAmount 0.12.

Check the grade on one rendered frame: skin must stay natural, food warm, never orange. Halve the
temperature for a photo that is already warm (candlelight, a golden-hour window, lamp-lit rooms).

## Marks

Engine shapes only. Each mark is a shape layer whose path is imported with the scene's SVG-path import
(`d` in a 100 × 100 box), filled with a colour from the table above:

| Mark | Fill | Path (100 × 100) |
|---|---|---|
| Maple leaf | #C4581F | `M50 2 L58 24 L72 14 L68 34 L92 30 L80 46 L98 56 L74 62 L80 82 L58 70 L54 98 L46 98 L42 70 L20 82 L26 62 L2 56 L20 46 L8 30 L32 34 L28 14 L42 24 Z` |
| Oak leaf | #E8A33D | `M50 2 C60 10 68 8 66 20 C78 18 80 28 70 34 C82 38 82 50 70 52 C80 60 74 70 62 66 C64 78 56 84 52 80 L52 98 L48 98 L48 80 C44 84 36 78 38 66 C26 70 20 60 30 52 C18 50 18 38 30 34 C20 28 22 18 34 20 C32 8 40 10 50 2 Z` |
| Acorn | #8A4A1C | `M20 40 C20 20 80 20 80 40 L80 46 L20 46 Z M24 46 L76 46 C76 76 60 94 50 98 C40 94 24 76 24 46 Z M48 14 L52 14 L52 26 L48 26 Z` |
| Wheat | #E8A33D | `M49 98 L51 98 L51 30 L49 30 Z M50 4 C58 10 58 20 50 26 C42 20 42 10 50 4 Z M50 26 C60 26 64 36 52 40 C52 32 50 30 50 26 Z M50 26 C40 26 36 36 48 40 C48 32 50 30 50 26 Z M50 42 C60 42 64 52 52 56 C52 48 50 46 50 42 Z M50 42 C40 42 36 52 48 56 C48 48 50 46 50 42 Z` |

- **How many**: 2–4 marks, only on title cards, list cards and pages. Never on a full-frame photo, never
  over a face, never inside the safe band's centre where the title sits.
- **Size and place**: 90–160 px, in the corners or tucked against a frame's edge, tilted −20° to 20°.
- **Motion**: each lands with `look:pop(role=in, length=0.3, overshoot=1.15)` on the beat after the title. They then
  hold still; a tiny `look:drift(role=out, distance=0.05)` exit is allowed on the last beat.
  If the pop draws nothing on a shape layer, key the mark's scale 0 → 1.15 → 1 over 0.3 s instead.
- **Frame shapes**: a style that frames photos in a shape may use `look:shape_window` shape `scallop` or
  `heart`, with an outline in #FFF4E0.

## Bed mood

Warm acoustic: guitar or piano, 85–100 BPM. Friendsgiving is a little brighter and more playful,
100–115 BPM. The style's Music line sets the tempo inside that range.

## On each base style

These styles carry Thanksgiving and Friendsgiving in their Fit, so the picker can choose them. The skin
also applies to any other style the picker chooses for this occasion.

| Style | What the skin changes |
|---|---|
| Thankful list | heading "Thankful for" (Friendsgiving: "Thankful for you") in the title font; list lines in `montserrat`; a burnt-orange tick per line; marks on the list cards only |
| Framed window | the title in the script font above the frame; the labels are the dishes or the guests; frame and page take the light page; a leaf at one frame corner |
| Mini vlog title | the held title is "happy" in Baskerville capitals over "Thanksgiving" in the script, with the kicker below; no marks (full-frame footage) |
| Scrapbook drops | the paper takes the light page; the title above in the script; tape stays as the style has it; 2–3 leaves among the dropped photos |
| Title mosaic | the centre tile is the title in the script on #2B1608; the tiles open in black and white and turn to colour as the mosaic fills (this occasion's variant); no marks |

Cut-out styles (Sticker collage) fit Friendsgiving groups too, but each cut-out photo is a quoted spend.
The skin applies to them unchanged: the script title in the middle, the accent as its glow.
