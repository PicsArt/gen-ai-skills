# The breakdown — shot cards and the asset list

## The shot card

Every shot in the shotlist is one card. The point: the Stage 6 prompt is later
written from the cards *almost mechanically* — the book's six lines per shot
(`../../picsart-film-scenes/references/prompt-blocks.md`) are read straight off them.
Anything left vague here gets invented by the model there.

| Field | What goes in it |
|---|---|
| Scene · shot | Script scene number + shot id (`2D`). Everything is found by this id later — board, log, prompts |
| Location · INT/EXT | Which place the shot is in |
| Time of day / weather | Day, night, dawn, rain — a place at another time is another set of pictures |
| Who is in frame | Everyone, by asset tag; a changed state by its own tag (`@rasa_bloodied`) |
| Props | With tags |
| Action | One to three sentences of what physically happens — one big clear action per shot, copied from the story's paragraph (`dramaturgy.md`) |
| Line | Verbatim from the story, or a dash. "No lines" is information — it changes the shot's length |
| Feels | What the character feels — one or two words per visible face. The book's *emotion* line |
| Blocking | Who stands where **relative to the camera**: frame-left, foreground. Never "to the left of the hero" |
| Seconds | 3–8 for drama, shorter for action and reactions; a longer shot carries its reason in one line |
| Size | ECU → CU → MCU → MS → WS |
| Movement | Static, handheld, slow push-in — and what the camera **never** does |
| Lens | The FOV anchor that will go into the prompt (`../../picsart-film-scenes/references/presets-camera.md`) |
| Angle | Height and side: low looking up, eye level, three-quarter |

**Action and Line are copied from the story's paragraph, never rewritten on
the card.** The card adds the camera. When an action on a card
would tell a different story, the paragraph in `docs/story.md` is rewritten and
shown first, and the card follows it (`workflow.md`, *A story note is answered
with a paragraph*).

Two shots of the same subject in a row are two sizes apart; a look is answered
on the opposite side of frame; walking direction holds. Those three checks and
the way one shot hooks into the next are `../../picsart-film-scenes/references/seams.md`;
nothing about them is written on the card.

## The asset list

From the script, write out everything that must exist visually: **people,
places, props.**

- **Each row gets a future `@tag`.** Open the row later and its descriptor and
  pictures are there; at generation time nobody hunts.
- **Characters**: every speaking and every recognizable on-screen character.
- **Places**: every place of action; each needed time of day is its own row
  (street-day and street-night are two).
- **Props**: the objects the story is about — the flask, the deed, the car.
  Background props are not written out; they live inside the place's
  descriptor.
- **A durable change the story does to a place or a person is a row too** —
  the garage after the fire, the shirt once it is bloodied, the coat off. Read
  the script for events, not just for settings: anything that would still be
  true an hour later is a row (`@kitchen`, `@kitchen_wrecked`). Anything that
  resets — a spilled drink mopped up between scenes — is not. A person's
  changed state is a panel on their sheet with its own tag; a place's is the
  frames of the video that changed it (`../../picsart-film-scenes/references/step-6-7-selects.md` step 6).
- **In-frame text** (signs, screens, letters) is never generated in-shot:
  models write text poorly, so it is added in the edit or masked. Write around
  it or list it for the edit.

Nothing on the list is tiered and nothing is flagged as complex.
Every character gets the handbook's three pictures, every prop a plate, every
place its pictures from its scene.
