# The breakdown: shot cards and the asset list

## The shot card

Every shot is one card, and every run prompt is later compiled from the cards almost mechanically.
Anything left vague here is invented by the model there. The shot list board holds these fields;
fill them from the story before it opens.

| Field | What goes in it |
|---|---|
| Scene · shot | The scene id and a shot id (`2D`). Everything is found by this id later |
| Place, inside or out | Which place the shot is in |
| Time of day, weather | Day, night, dawn, rain. A place at another time is another set of pictures |
| Who is in frame | Everyone, by tag; a changed state by its own tag (`@rasa_bloodied`) |
| Props | By tag |
| Action | One to three sentences of what physically happens, one big clear action, **copied from the story** |
| Line | **Verbatim from the story**, or empty. No line is information: it changes the shot's length |
| Feels | One or two words per visible face: what the character feels, held in, except the peak shot's face, unguarded, with what shows ("@teo relief, unguarded: the tears come"), on that one card only (`references/story.md`) |
| Blocking | Where each person is **relative to the camera** (frame-left, foreground), never relative to another person |
| Seconds | By film-shot-generation' duration rule |
| Size | Distance only: extreme close-up to wide |
| Arrangement | Single, two-shot, dirty single, over-the-shoulder, point of view, insert, group |
| Movement | Static, handheld, a slow push-in, and what the camera never does |
| Lens, focus, light, colour | The shot's own pills: the lens as a field-of-view anchor within the film's lens family, a focus (deep, shallow, soft or rack), a lighting setup, and a palette left on `auto` unless the shot needs a colour of its own (a flashback, a world it crosses into). A palette you pick has to fit the film's colour scheme. The light is the scene's: one setup on every card of it (`references/light.md`) |
| Composition | How the frame is organised: rule of thirds, symmetry, leading lines, a frame within a frame, negative space or layered depth. Left on `auto` unless the story asks for one (an isolated figure wants negative space); the user changes it on the card |
| Height | Camera height and angle: eye level, low, high, overhead. Sent as a value, not a pill on the board |
| Length | The board's length pill, in the durations the chosen model accepts |

- **Action and line are never rewritten on the card.** When a card would tell a different story,
  the scene's paragraph is rewritten and shown first, and the card follows.
- **An over-the-shoulder is a two-body claim.** The card names the near character and the near
  side, and both people are in its tags. A two-shot and a dirty single carry the same.
- A point of view says whose eyes the camera is; the other actor looks into the lens.
- Size says distance, not who is present. An insert is an object's shot.
- The board's values sit under the look already locked: its style line, its lens family and its
  colour scheme. Never ask the user to choose from a vocabulary the setup has not adopted.

How one shot hooks into the next, and the three checks on neighbouring cards, are film-shot-generation'.

## The asset list

From the story, everything that must exist visually: **people, places, props.**

- **Each gets a tag** (`@cal`, `@garage`, `@wrench`), and everything is found by it later.
- **People:** everyone who speaks, and everyone recognisable on screen.
- **Places:** every place of action; each time of day it is needed at is its own tag
  (`@street_day`, `@street_night`).
- **Props:** the objects the story is about, the flask, the deed, the car. Background objects live
  in the place's descriptor.
- **A lasting change is its own tag**: the garage after the fire, the shirt once bloodied, the
  coat off. Read the story for events, not just settings: anything still true an hour later is a
  tag (`@kitchen`, `@kitchen_wrecked`); a spill mopped up between scenes is not.
- **In-frame text** goes on a list for the edit, never on a card; film-shot-generation says why.

Nothing on the list is tiered or flagged as complex. Every person and prop gets its pictures, and
every place gets its pictures from its scene.
