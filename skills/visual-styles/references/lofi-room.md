# Lofi room

A small room at night, held still and warm: one lamp lights an armchair where a person reads, rain runs down the window
behind them, a cup steams on a side table and the plants sway a little. Flat vector shapes under one soft pool of
amber light, built to loop without a seam. It is a calm picture that moves slowly, not a story with a plot, not a
character-acting style and not a cosy photograph.

## Palette and colour roles

| Role | Colour | Its one job |
|---|---|---|
| ground | composition background `#1a1220`, wall `#2e2238` to `#4a3040` | the dark room behind everything |
| floor, wainscot | `#2a1f2c`, `#3a2730`, rail `#6b4650` | the lower band that anchors the furniture |
| rug | `#8a4b4f`, `#a15c5a` | a soft ring of rose under the chair |
| window | sky `#1b2347`, frame `#e8cfa8`, `#d8bd96`, moon `#efe4c0`, stars `#f2e7c4`, rain `#a9bcd8`, city `#2a3262` | the one cool field in a warm room |
| chair | `#a64d33`, armrest behind the legs `#8f4230`, `#b8563a`, `#c2623f`, `#cf6f4a` | the large warm shape the person sits in |
| person | sweater `#4a6a86`, far sleeve `#3f5d78`, near sleeve the sweater `#4a6a86` with edge `#36506b`, trousers `#2f3b4f`, skin `#e0ac86`, thumb `#e8b894`, nose `#c4866a`, hair `#2b1f26` | a cool body against the warm chair |
| book | cover `#7a3b3b`, pages `#f1e6d0`, `#e8dcc4`, turning page `#fffaf0` | the brightest small shape on the person |
| plants | `#2f6b48`, `#3f7a52`, `#4f8a5c`, `#5a9566`, pots `#c2623f` | green leaves, the only green in the frame |
| accent | `#ffb866` | the lamp's light, its shade `#f2b866` and bulb `#ffd9a0`, its motes `#ffe2b0`, and the lit city windows `#ffd48a`; nothing else |
| wood and small props | shelf and table `#4f362c`, `#5c4033`, `#6b4a3a`; lamp base `#3b2a22`; pot shade `#a84f33`; cup `#7a4a35`, `#d8c9b0` | the dark furniture and the small things on it |
| person details | eye lines `#4a2f2a`, mouth `#9a5a4a`; socks and cuffs `#e8dccb` | the few marks on the figure |
| shadow | chair contact shadow `#140c16` | the one cast shadow |
| cup, steam | `#efe4d0`, `#f6ead9` | the cup and its steam |
| vignette | `#100810` | the darkened corners |

Hero colour: lamp amber. The room is warm on the chair, rug and lamp and cool in the window and the sweater, so the
person reads against the chair; amber light is the only glow.

## The medium

- Flat, clean shapes are the baseline: one fill, no outline, the depth coming from layering, a soft amber glow that
  lights the near wall and a dark vignette. Richer shading or texture is allowed if the palette, the amber-only glow and
  the frame checklist still hold.
- The lamp's light is a large radial ellipse blended additively over the room, peak alpha 0.5 falling to 0 at the
  edge (ours, tune by render). Its brightness moves by a few percent on a slow sine.
- The window is its own small world: a night sky with a moon and stars, rain streaks that wrap inside the pane, a row
  of dark towers with a few windows lit amber that twinkle on slow sines, and a pale frame with a cross.
- The person is a flat figure in side view: a torso that breathes, a head that nods a degree or two, two full arms (shoulder, elbow, forearm, each a stroked
  path: the near sleeve is the sweater's own colour from a round shoulder cap, with a darker edge only from the elbow on,
  so it grows out of the torso; the far arm starts behind the torso and comes out in front of the chest) ending in two hands holding a book, and a face with two closed eyes, a nose dot and a small mouth. The book is open; a page with a thin edge
  turns twice in the loop.
- A held prop sits inside the grip, never floating: each hand's palm and fingers lie over the book's lower edge and a
  thumb on the page face, in the book's own tilted frame, so the book cannot drift from the hands.
- Steam is three thin wisps drawn by a stroke whose trim start and end run along the path, so a wisp grows, travels
  up and ends.
- Plants sway as whole groups about their pots, a degree or two, out of phase with each other.
- Dust motes in the lamp's light drift in small slow loops (each on a closed path of whole cycles, so none ever jumps), small additive dots.

## Rates

| Held rate | Root rate |
|---|---|
| none | everything: breath, nod, plants, steam, rain, lamp, motes, page turn |

## Boil

Nothing boils: the shapes are clean. The only constant motion is slow and periodic.

## Line width under a zoom

There are no outlines. The camera does not move; the picture is a fixed frame.

## Motion habits, and the transitions

- Every motion repeats a whole number of times in the loop (one, two, three or four cycles in 6 s), so frame 143 flows
  into frame 0 with no seam. Pick the loop length first and size each period to divide it.
- Breath is two cycles per loop (1.2 % vertical scale on the torso); the head nod and the plants sway once;
  steam wisps run three; lamp flicker is one slow and one faster sine together; rain wraps four times.
- The page turn is a scale from 1 to -1 about the spine over about 1 s (1.6 to 2.6 s and 4.5 to 5.5 s), the page the lightest shape on the book, then it is hidden at once and reset; the next turn
  starts again from the right, so both turns go forward: two turns per loop.
- Nothing fades but light: steam is drawn by trim, the page appears and disappears by a step, the glow changes by a few
  percent and the lit city windows twinkle in opacity as light; no other opacity changes.
- Transitions between rooms: a slow push through the window, a lamp that switches off and on, or a page turn. No
  dissolves; a loop does not need to end.

## Type

None by default. If a title is wanted, a small lowercase line low in the frame in a soft geometric sans, in the page
tone `#f1e6d0`, held long enough to read.

## Scene features used

How the proof was built, optional: shape layers with groups, closed paths, rects and ellipses, `fill` and `gradientFill` (radial, with `alphaStops`), a
layer with `blendMode: "add"` for the glow and the motes, group `position`, `rotation`, `scale` and `opacity`
driven by expression tracks (`math.sin` over whole cycles of the loop), the `trim` item on a stroke for the steam, and
step easing for the hidden page. In a shape layer an earlier item draws on top of a later one, so author each layer
from front to back.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. The first and last frames match: nothing jumps at the loop point.
2. Amber appears only on the lamp, its light and the lit city windows.
3. The person reads against the chair: cool sweater on warm chair, book the lightest shape.
4. The window is the only cool field and its rain stays inside the pane.
5. The vignette darkens the corners without crushing the chair.
6. The cup, steam and plants stay clear of the person's hands and face.
7. Every motion is slow enough that a viewer feels it more than sees it.
8. The room stays flat-shape vector art: any extra shading or texture is soft, keeps the palette and the single amber
   glow, and never turns a shape into a rendered or photographic one.

QC: lean on the loop seam (compare the first and last frames), the viewer's pass at normal speed, and the amber
glow against the person's torso on a contact sheet.

## Build with the tools (how the proof was built, optional)

The proof built each object as a shape layer from back to front: wall, window, floor, rug, shelf and plants, lamp, table and cup,
chair, person, book, then the glow, the motes and the vignette on top. It gave every layer the same centred transform so
the shape points were written in composition pixels (any construction that keeps the look is fine). The loop rule holds whatever the construction: write each periodic
motion as a `math.sin` of whole cycles of the loop length, and check the seam by exporting and comparing frame 0 with the last frame.

## Do / don't

- **Do** keep the loop whole: size every period to divide the loop.
- **Do** let the lamp be the only glowing thing and the window the only cool one.
- **Do** keep every move small: a degree, a percent, a few pixels.
- **Don't** add a camera move, a fade, an outline or a second light colour.
- **Do** put a hand on every held thing: a floating prop reads as a defect.
- **Don't** put the person's face in motion: no talking, no blinking cycles that read as acting.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Rate split: everything runs at the root rate; nothing is held.
  - Nothing fades but light: steam is trimmed, the page steps, the glow changes by a few percent and the lit windows
    twinkle; no other opacity changes.
  - Height is shadow: the chair has a soft contact shadow on the floor; no other piece casts one.
  - Boil: none.

## Originality guard

Design your own room, furniture, figure and wording. It must not copy a known lofi-radio character, a published
illustration or its colour script. A lamp-lit room, a reader, a window with rain and a steaming cup are the style.

## Proven on

A 6 s portrait loop (1080 by 1350, 24 fps) of about 30 shape layers (more is fine): a lamp-lit room with a reader in an armchair turning a
page twice, a window with rain, a moon and a lit skyline, a shelf of swaying plants, a floor plant, a steaming cup on a
side table, dust motes in the lamp's light and a vignette; exported locally, not on the hosted renderer.

**Not proven:** the scene in the stage editor (not tried), a second room or a scene change, a character that looks up or speaks, a title line over the loop, a
longer loop than six seconds, a daytime variant, and a grain finish over the whole frame.
