# Light: one setup per scene, and a colour kept back

The light is chosen on the shot cards, from the board's setups (the card's `light` value). The
sentence each setup compiles to is the server's; never write it yourself. What is here is how to
choose one, and what stays the same across a scene's shots.

## Four layers, and where each one lives

| Layer | What it decides | Here |
|---|---|---|
| The film's colour | The colours of the whole film | The look, locked on the console, and carried into every place's descriptor (`references/look.md`) |
| The scene's light | One setup for the scene, set once: the source, its direction, its colour temperature, the dark side | Every card of the scene, as below |
| The scene's key picture | What that light looks like in this place | The approved scene picture: the scene's shots match it |
| A shot's change | One shot made darker, brighter or harder | How much light falls on whom, never where it comes from |

Plan the scenes' light against the story, not one scene at a time: the peak's scene reads against
its neighbours, the one hard light in a soft film, or the one warm room in a cold one.

## The scene's light, set once

- **One setup on every card of a scene.** Two shots of one scene with `window` and `practicals`
  are two rooms.
- **Choose from the place and the hour.** Read the place's descriptor first: its light line
  usually names the setup. Indoors, a source someone stands near or switches on: `window`,
  `practicals`, `firelight`, `work light`. Outdoors by day, what the sun is doing: `golden hour`,
  `open shade`, `dappled shade`, `overcast`. At night, what is there: `street light`, `moonlight`,
  `night practical`. Into the light, `silhouette` or `contre-jour`, when the shape carries the
  scene.
- **`overcast` is chosen on purpose.** It is the one setup with no dark side, and it is also what
  a shot looks like when nobody decided its light. `auto` leaves the light to the place's own
  sources and writes nothing.
- **A setup's blanks come from the place**, in `light.slots`: where the window is relative to
  camera, which lamp, the direction of the sun, what breaks it into patches. A lamp that is not in
  the room is worse than no lamp.
- **The colour temperature is one number for the scene.** "Warm" written on eight shots is eight
  guesses, and the room changes temperature across its own cuts. Set a Kelvin from the setup, the
  place and the hour, and write the same number into every shot of the scene beside its word
  ("warm tungsten, 3200 K"). The user picks the setup, never the number.

  | Word | Kelvin | Reads as |
  |---|---|---|
  | warm | 3200 K | tungsten, candles, lamps |
  | warm-neutral | 4000 K | a mixed interior, late afternoon through glass |
  | neutral | 5200 K | clean daylight, an overcast noon |
  | cool | 5600 K | open shade, north light |
  | cold | 8500 K | blue hour, moonlight, deep shade |

  A scene that mixes sources on purpose (a lamp-lit room with a cold window) gives each source its
  own number, and the difference is the point.
- **Which side of the face is dark, always said**, relative to camera: "camera-left of the face
  lit, camera-right falling dark". A source from overhead (`open shade`, `street light`,
  `overhead fall`) darkens downward instead: the brow, under the nose, under the jaw. `dappled
  shade` names where the patches fall. The dark side flips only when the camera crosses to the
  other side of the person; a join where it jumps reads as another room.

Where these are written into a prompt, and when, is film-shots'.

## A shot that departs

A shot may change how much light falls on whom: a foreground figure taken darker so the eye goes
to the face, harder contrast on a face at the peak. It never changes the source or its direction.
Say the change in plain words for that shot, and only for a reason the story gives.

## The scene picture is the scene's light

Once approved, the scene picture is the light every shot of the scene matches. A picture carries
light more firmly than any sentence, so a light changed after approval is a new scene picture, not
a new sentence.

## A colour kept back

The look's colours, its accent included, are in every frame. A colour can instead be kept out of
the film entirely until one moment, so that its first appearance means something: no green
anywhere until the plant. Use it only where the story has a thing that earns it, usually at the
peak.

- **It is a colour the look does not carry**, and it belongs to one prop or one piece of clothing,
  whose descriptor carries it.
- **Keep it out of every other descriptor.** Pictures carry colour more firmly than words, so a
  colour in any reference picture is already on screen.
- **The shots where it appears keep the film's palette on their cards.** The colour arrives with
  the thing, not with a palette of its own.
- Write it down with the film's standing decisions, with what it belongs to and where it first
  appears.
