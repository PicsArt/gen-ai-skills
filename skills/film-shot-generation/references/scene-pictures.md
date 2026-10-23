# Scene pictures

Every scene gets approved pictures before its first run. A scene is one place at one time of day; a
scene that moves to another room is another chain of pictures.

## The order

1. **The wide first**, at the film's frame and the image model's top resolution: the opening shot's
   cast, small in the room, compiled with `picsart_film_compile_prompt` (`kind: "scene-picture"`).
2. **The scene picture is cut from the wide**, around the opening composition at the film's ratio,
   with `picsart_scene_export` (as film-cast-design cuts views). It is free, not another generation. If the
   cut's short side falls below the video's resolution, the wide itself opens the run.
3. **A room map, only where the scene cuts between walls**: generated from the wide
   (`kind: "map"`), top-down, square, empty of people, keeping the place's colour, with its sides
   labelled. A single outdoor place with one background uses its wide as its geography.

## What the scene picture holds

It is the opening shot as designed, so it comes from the opening shot's card, not the dramatic
centre:

- the opening shot's cast only (its tags, verbatim), with their designed first action, expression,
  gaze and positions;
- the place, the composition and all three depth planes;
- every visible prop, with its count;
- the film's frame and style.

A still carries the still's language and its `negativePrompt` as the compiler returns them: no
video words, no cut list. The lettering ban goes on the wide and the scene picture, never on the
map, whose sides need their labels.

Attach each present person's identity and wardrobe views, and the user's photos of a real place.
Not the map, not props, not unrelated stills.

## Reading the map

One map per place and time of day, reused by later scenes there. Read it when it lands, and write
its sides into the scene's geography line. Read left and right from the scene picture, not the map;
use the map for which wall is behind each person. When a reverse changes the near body, the wall
behind or the pointing hand, say the change in that shot's block.

## Checking them

Look at every picture before anything is derived from it (picsart-video-rules, Asset URLs).
Then, on the board:

- **the scene picture:** the opening shot as designed, the right faces, the right room;
- **the wide:** the same room, the people small and far;
- **the map:** the room from above, sides labelled, nobody in it.

A correction is checked against what depends on it. Rebuild only what it made wrong; a change of
geometry or light reaches further than a change of a face.

The scene picture becomes the first run's `START FRAME`; the wide and the map become its place.
