# Contour trail

A survey map of a walk: warm cream paper with a faint grid, two hills drawn as nested wobbly contour lines that sketch themselves on from the outside in, a pale blue lake, and a dashed red route that draws itself from a start pin over the first hill and down to a flag on the second summit. Small cream pills give the heights and name the lake. It is quiet, precise and satisfying to watch: not a route diagram on a plain map ([route-map](route-map.md)), not a transit diagram ([transit-map](transit-map.md)) and not a blueprint ([blueprint](blueprint.md)).

## Palette and colour roles

| Role | Colour | Its one job |
|---|---|---|
| paper | cream `#f3ecd9`, grid `#e6dcc2` | the map sheet |
| contours | tan `#b98a5a` 3 px; every third line (the index contour) brown `#8a5a3a` 6 px | the land |
| lake | `#a9d6e6` with a `#5b9fb8` edge; white ripple lines | the water |
| route | red `#d6453d`, dashed | the path |
| ink | `#3b2a1c` | the tag outlines and text, the flag pole |
| tags | cream `#fffaf0` | the height pills |
| pin centre | white `#ffffff` | the middle of the start pin |

Hero colour: the red of the route, the only saturated warm colour on the pale sheet.

## The medium

- **Contours** are closed wobbly rings, each a smooth blend of a few low sine bumps on a circle, stretched slightly wider than tall; every ring of one hill uses a slightly shifted bump phase so they nest without touching.
- **The grid** is 2 px lines every 180 px, barely darker than the paper.
- **The route** is a smooth curve (a spline through eight points), 9 px wide, dashed (22 px dash, 14 px gap), with a faint solid offset shadow (4 px right, 6 down, 12% black, hard-edged, drawn on with the route).
- **Tags** are 62 px tall pills with a 5 px ink outline and one line of heavy capitals.
- **No fills on the land:** hills are lines only; the lake is the one filled shape.

## Rates

| Held rate | Root rate |
|---|---|
| none | everything |

## Boil

None.

## Line width under a zoom

The contours are 3 to 6 px and the route 9 px; all stay readable under a push, the grid does not need to.

## Motion habits, and the transitions

- **The contours draw on** outside to inside, each ring over 0.7 s, starting 0.12 s after the one outside it, from 0.3 s; the second hill follows the first, and all twelve rings are on by 2.3 s.
- **The lake pops** at 0.8 s (scale 0 to 1 over 0.5 s, no overshoot); its ripples fade in over 0.4 s from 1.3 s and then pulse softly.
- **The start pin and the first two tags pop** at 1.6 to 1.8 s.
- **The route draws on** at a steady pace from 2 s to 6 s; the flag pops as it arrives, and the second height tag at 6.2 s.
- Transitions: a hard cut; none are built into the proof (see Not proven).

## Type

One very heavy sans (the proof used Archivo Black) in all capitals for the height tags at about 34 px, with a number and a short unit or place word. Keep each tag to about ten characters.

## Scene features used

Hints, not rules: closed outlines drawn with a stroke, a draw-on that reveals a line along its length, a dashed stroke, and text on a pill are enough.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Contour rings of one hill never cross each other; the two hills do not touch.
2. The route stays on the sheet, starts at the pin and ends at the flag; its dashes are even.
3. Tags sit on or just beside what they name (a summit, the lake) and are whole inside the frame.
4. The flag is on the second summit and clear of its tag.
5. The last frame has all contours, the lake, the full route, the pin, the flag and three tags (two heights and the lake label).

QC: a contact sheet across the draw-on, and the viewer's pass at normal speed for the route's pace.

## Build with the tools (a hint, optional)

Any construction that keeps the look is fine. Make each ring its own line so it can draw on on its own clock.

## Do / don't

- **Do** let the contours draw themselves in a calm sequence.
- **Do** keep the land line-only and the route the only red.
- **Do** write your own place names and heights.
- **Don't** shade the hills or add hill-shading colours.
- **Don't** run the route through the lake.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Rate split: everything runs at the root rate.
  - Nothing fades: lines draw on, pieces pop; the ripples are the one exception, fading in from 1.3 s and then pulsing in opacity.
  - Height is shadow: only the route's faint offset shadow.
  - Boil: none.

## Originality guard

Design your own terrain, route and place names. Do not copy a real map, trail or app. Nested contour lines, a lake, a dashed route that draws itself and height pills are the style.

## Proven on

A 9 s portrait clip (1080 by 1350, 24 fps): two hills of six rings each, a lake, a dashed route, a pin, a flag and three tags; rendered locally frame by frame, not on the hosted renderer.

**Not proven:** the stage editor, a landscape frame, a marker that walks along the route, a camera move, hill-shading, a transition in or out, and a font other than Archivo Black.
