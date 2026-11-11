# The style library

Ready-made references for a reel with no reference of the user's own: each style is a structure
sheet and a look, written by us from reels many people make now and from the scene engine's own
templates and looks. A style is used exactly as a reference reel's written breakdown is: its sheet
parses for free, and nothing of the reels it was learned from (their footage, sound, words,
creators or apps) is in it or reaches the user.

This file holds the rules. The styles are in two places, and the agent never reads all of them:

- `style-index.md`: one line per style (its id, group, media and item range, subjects, occasions,
  moods and vibe words), written by `scripts/build_index.py`;
- `../styles/<id>.md` (the skill's `styles/` folder): each style's full entry, one file per style.

Read this file and the index; run the picker (Picking the style); open only the picked style's
file. "Try another style" opens one more file. Never read the `styles/` folder as a whole.

## Contents

- How an entry reads
- The groups
- Occasion skins
- Picking the style
- Using the picked style
- Building it

## How an entry reads

A new style passes `scripts/style_check.py` (its catalog calls and times) and the library's tests
before it is added; then `scripts/build_index.py` rewrites the index. Every style is available to
the picker, including styles not yet proven by an agent build. The index lists every style under
its validation status, and the ranking retains that status as `proven`. It records build history;
it does not restrict selection. A style whose build fails stays `no` until its recipe is fixed and
a new build passes. Every selected style still goes through the same build and review checks.
`style_check.py` checks against the scene engine's catalog snapshot in the skill's `data/` folder.
These three scripts run only from this skill, beside the styles and data they read: they are its
`local-scripts`, which the build never copies into a skill that imports this one's scripts.

Each style is a heading, a table of fields, then its sheet: the header lines and the beat table
of SKILL.md's section 2.

| Field | What it holds |
|---|---|
| Group | one of the groups below |
| Looks like | one plain line the user reads |
| Vibe | words a user might say for this look ("cinematic, film look"), matched against the user's own words |
| Fit | `slots A–B; media; subjects; occasions; moods`: media is `photos` (no clips), `clips` (no photos) or `mixed` (either or both) |
| Music | the bed's mood and tempo, for the background-music skill's brief; never a named song |
| Skin | what this style takes from the occasion skin (below): the title's words, colours, labels |
| Preview | our own sample reel on the Picsart CDN, or `none yet`; every preview shows the autumn skin |
| Proven | `yes: agent build <date>, match|close` once a blind agent build from this file alone graded match or close-and-shippable against its source; `yes: agent build <date>, user-approved` when the user approved that build's side by side; else `no` |
| Seams | the base transition, as one catalog `transition` id or hard cuts, and any accent seams |
| Motion | how each clip or photo moves inside its slot |
| Text | the title and any other words: entrance (`textAnimation:<name>`), place, font, colour |
| Look | the scene looks (`look:<id>`) and their parameters |
| Template | the scene template the style is built on (`scene://<id>`, with its mode), or `none` |
| Ending | how the reel ends |
| Skills | the skills that build this style, loaded at the build |

Every catalog id and template here was checked against the scene engine's catalog at 55.104.0, and
every preview was rendered on that engine with the templates' own sample photos. When one is
missing from `picsart_scene_capabilities`, build the rest of the style and say which part is
missing in one line; never swap in another id silently.

## The groups

Every style is in one group; the index names it. "Try another style" moves to another group.

| Group | What the styles share |
|---|---|
| Fast cuts | one shot per beat, full frame, energetic |
| Film and retro | a film, tape or light look over full-frame shots |
| Grids and collages | many photos on screen at once |
| Cards and frames | photos as cards, frames or shapes on a page |
| Strips and swipes | photos moving past in a row |
| Text-led | the words carry the reel; the shots sit under or around them |
| Transitions and speed | the seams carry the reel: zooms, whips, spins, speed ramps |
| Glow and colour | a light, glow or colour treatment carries the reel |
| Cut-outs and stickers | the subject cut out, or stickers and drawn marks over the shots |

## Occasion skins

A style keeps its structure and look for every occasion; the skin changes its words and colours.
The occasion comes from the free reads (dates, decorations, food, places); with none clear, use
everyday. The year is the footage's, else this year, unless the skin's row says a year only from the
media's own date. A title the user gives replaces the skin's. A row that names a skin file
(`references/skin-<occasion>.md`) has more: open that file only when the occasion is that skin's, never otherwise.

| Skin | Title | Background | Text | Accent | Bed mood |
|---|---|---|---|---|---|
| Thanksgiving | Happy Thanksgiving, else Thankful; a year only from the media's own date; full skin in `references/skin-thanksgiving.md` | #2B1608 | #FFF4E0 | #C4581F | warm acoustic |
| Christmas | Christmas <year> | #0F2A1D | #FFF4E0 | #D7263D | cosy bells and light percussion |
| Winter | Winter <year> | #0E1A2B | #F2F6FF | #9CC9FF | soft, crisp and calm |
| New Year | Hello <year> | #0B0B1F | #FFFFFF | #F5D06F | sparkling and upbeat |
| Friendsgiving | Friendsgiving; a year only from the media's own date; full skin in `references/skin-thanksgiving.md` | #2B1608 | #FFF4E0 | #E8A33D | warm acoustic, a little playful |
| Year-end | The End <year> | #0B0B1F | #F5D06F | #FFFFFF | sparkling, a little nostalgic |
| Birthday | <name>'s birthday, else Birthday <year> | #1A0F2E | #FFD84D | #FF5FA2 | upbeat and celebratory |
| Travel | <place> <year>, else My trip | #06263A | #FFFFFF | #FFB400 | sunny indie pop |
| Autumn | Autumn <year> | #1A120B | #FFF4E0 | #E07A2F | cosy and warm |
| Everyday | Recent moments | #0E0E12 | #FFFCF8 | #FF47FF | bright modern pop |

A style on a light page (Moodboard collage, Framed days, Scrapbook page, Swipe post)
uses a light tint of the skin's background or accent for the page and the skin's background colour
for its text. The style's Music line sets the tempo; the skin's bed mood colours it.

## Picking the style

The agent picks one style itself and builds it; the user is not asked to choose. The ranking is
a script, so the same request always gets the same style:

```
python3 scripts/pick_style.py read.json
```

`read.json` is the free read of the request, written from the user's words and a look at each
photo and a still of each clip (no paid read):

| Key | What goes in |
|---|---|
| `words` | every word the user said about the look, the mood, the subject or the occasion, as they said it: "cute", "cinematic", "polaroid", "selfies", "trip", "night out" |
| `place` | a place the user named ("my trip to Lisbon" → `Lisbon`), else `""`; a place counts as the word `trip` |
| `photos`, `clips` | how many of each, after dropping duplicates and unusable ones |
| `subject` | from the faces and animals in frame: a pet in most items → `pet`; one person in most → `solo`; two → `couple`; three or more → `friends` (`family` when children are in frame, the people span generations, or the user says family: never a style for children alone); no people → `place` or `food`, whichever most items show |
| `occasion` | from what is in frame: stage lights, crowds, drinks, night streets → `night out` (a stage → `concert`); landscapes, landmarks, sea, mountains, a plane or station → `trip`; a laid harvest table with a turkey, pies or roasts and several people → `thanksgiving` (`friendsgiving` when the user says so); fallen leaves, autumn colour → `autumn`; snow → `winter`; cake, candles, balloons → `birthday`; home, coffee, desk, commute, a gym → `everyday`; with no clear signal, `any` |
| `moods` | from the pictures, two or three: a pet → `cute`, `playful`; bright daylight, colour → `upbeat`, `fun`; warm light, home, food → `warm`, `cosy`; dark, neon, night → `energetic`, `bold`; soft light, mist, water → `calm`, `dreamy`; one face posing → `stylish`, `playful` |

The script applies these rules, in this order:

1. **A style fits the footage** when every item can be used once and none twice: the count is at
   least the first slot number and at most the second plus a third (over it, drop the weakest);
   its media matches (`photos` takes no clip, `clips` no photo, `mixed` either or both); and its
   subjects and occasions include the footage's or say `any`. Below a style's minimum it does not
   fit: the build never repeats an item to fill a style.
2. **The user's words win.** Among the fitting styles, keep only those whose name, Looks like,
   Vibe or Fit says the most of the user's words (spellings and plurals alike: cozy is cosy). A
   mood word no fitting style says is met by its neighbours (cute: playful, fun, warm, friendly).
   A style whose moods contradict a mood word the user said is never picked (cute, fun or playful
   never take a moody, cinematic or epic style; calm or cosy never an energetic or bold one).
3. **Then fit, not count:** each user word the style is about, in its name, Looks like or Vibe
   (3, beyond the 1 for saying it at all); the footage's occasion among the style's (2), one more
   when the style is made for it (its occasions don't say `any`); the footage's subject named (1);
   the footage's moods among the style's, counted by the share of the style's own moods they take,
   so a style that lists many moods (a broad Fit) never ranks higher for listing them. The count never breaks a tie;
   still tied, the one whose moods (or their neighbours) meet more of the footage's moods, as a share of its own, wins,
   then the one listed first. The footage's own moods only score; they never rule a style out.
   Everyday footage never gets a moody style unless the user's words name it, and with no mood
   read, everyday reads bright and calm (calm, warm).

The pick is the script's `pick`. With no full fit, the script ranks the styles that take this
many items and this media whatever their subjects and occasions, so a few photos still get the
best few-item style: a styled reel never falls back to a plain slideshow. The user's mood words
always hold. It is `null` only when no style takes this many items, or every one that does
contradicts the user's mood word: say so in one line (`unfit` says why for each) and ask for more
items or another word; never stretch a style over too few items, and never drop the user's word.
"Try another style" takes the first in the ranking from a group not tried yet (or the one tried
longest ago), never one already tried in this project: run the script again with `--exclude` and
the record's `stylesTried`, oldest first.

**The Vibe set** is the script's `set`: the pick and the next three "try another style" builds,
kept varied so the four don't all read as words over photos:
- at most one Text-led style;
- at least two styles from other groups, one of them motion-led (Cards and frames, Grids and
  collages, Fast cuts, Transitions and speed, Strips and swipes).

The pick is always the best fit, and the set follows the ranking where these rules allow. When the
user's words leave too few styles to keep them, other fitting styles fill the set; when none can, the
set is shorter.

## Using the picked style

The style is the reference, and it goes through the same gate as one the user brought:

```
python3 scripts/sheet.py parse styles/<id>.md --out sheet.json
python3 scripts/sheet.py validate sheet.json
python3 scripts/ref_format.py from-sheet sheet.json --source described --out format.json
```

The file holds the one sheet: keep it as `sheet.json`. The read in section 1 is skipped (it
costs credits and there is no video to read), and so is the question whether the sheet is the
structure to copy: the style is our own, already checked. The format and what the footage can match follow
section 3 as for any reference. The record's `reference` is `{"style": "<id>"}`, beside the
`sheet` and the `format`.

The sheet's times are the sample reel's. The user's reel keeps its beats' order and shares, and
its own length: scale the beats to it, and the cuts land on the bed's measured beats. With no
length asked, a style that times each item (its Seams or Motion) runs that time per item, so its
length follows the item count; otherwise the reel is the sheet's Length when the footage fills the
style's slots; with fewer, about 1.5 s for each photo and the best 2–4 s of each clip, between 8
and 30 s.

## Building it

The cut is built as the job says. The style is then applied in this order, each with the skill
that owns it:

| Field | How it is applied | Skill |
|---|---|---|
| Seams | the base transition as the cut's one `transition`, or none for hard cuts; accent seams patched into the track's `transitions[]` | motion-design-craft (its transitions reference), custom-transitions only for a seam the catalog does not have |
| Motion | `picsart_scene_apply_preset` with `motionPreset:<id>` or the look's loop (`ken_burns`, `shake`) on each clip | motion-design-craft, motion-pattern-library |
| Text | a text layer with `textAnimation:<name>`, in the colour the entry or the skin gives (not the visual-style skill's own text colours) and the scene's default font unless the entry names one; a title held over moving panels stays attached as linked-element-motion says | scene-template-remix, linked-element-motion, visual-style |
| Look | `picsart_scene_apply_preset` with `look:<id>`, one call per clip layer or on the whole track, then its params with `picsart_scene_patch` | scene-template-remix |
| Template | `picsart_scene_apply_template`, its slots filled with the user's photos and clips; `scene://crop` only frames a layer and needs no skill | scene-template-remix |
| Stickers or scattered words | as caption-decorations says | caption-decorations |

The job's own build skills load as its stage table says (photo-slideshow, scene-building-basics);
of the style skills, load only the ones the entry's Skills field names. A transition, motion or
look the entry does not name is never added. Where the style and the job's own defaults differ
(photos moving, a title, the pace), the style wins: its `none` means none.

- **A transition does not shorten the track.** Its window is centred on the seam and the shots
  around it hold their edge frames through it, so the track runs the sum of its shots: time each
  shot to its beat as if the seams were hard cuts.
- **Times sit on the frame grid.** Every time in a style is a whole frame at 30 fps; a beat grid
  from a BPM is rounded to the nearest frame, each beat counted from the start. Before the bed
  exists (it is made after the cut, and may cost credits), cut on the style's own BPM grid; once
  the bed's beats are measured, move each cut to the nearest measured beat, never more than 3
  frames.
- **Words stay readable and off faces.** Every title and caption reads in a 360 px wide frame:
  it keeps the plate, scrim, shadow or stroke the entry names, and a pale colour on a photo always
  has one. Before the cut is shown, look at a contact-sheet frame (`picsart_scene_contact_sheet`) at the start and middle of every span with words on screen: words over a face move up or
  down the frame to clear it, and words that don't read at that size get the entry's backing.
  A line of words stays on screen at least 1.2 s; one word on a beat may hold one beat, 0.5 s or
  more, as a punch word does.
- **Words stay inside the band.** Before the cut is shown, run the screen-recording-layouts
  skill's `scripts/safe_zone.py` on the scene with the destinations edit-footage's
  `references/reel-platforms.md` names for a reel with no platform (in a 1080×1920 frame:
  y 250–1440, x 65–1015, off the right rail), or the shape's profile when the user named one. Measure each text box with
  `picsart_scene_query_layout` first. A word outside moves in or gets smaller; a style's position
  never outranks the band. Two things are not words to read and may cross it: a word grown into a
  full-screen mask during a transition, and repeated outline rows that are the style's texture.
  The words the viewer reads stay inside.
- **A title with a place** takes it from the user's words first, then from text the photos show
  plainly (a sign, a station name); a landmark only when it is certain. With neither, the title
  has no place and no filler year ("WELCOME TO / MY TRIP", never "TRIP 2026").
- **A colour look is checked on a rendered frame** of the user's own footage before the cut is
  built on it (a contact-sheet frame). A look that solarises, posterises or crushes a face
  is dropped and the reel is built without it; say so in one line.
- **A template's own sound** (its music and sound effects) is removed; the reel's bed is ours.
- **A template's video slots** take the user's clips; with fewer clips than video slots, a photo
  fills the slot and moves as the Motion field says. Its sample assets never stay in the reel:
  every slot holds the user's footage, else the slot is removed.
