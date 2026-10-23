---
name: film-story-writing
description: Write a short film's story and break it down - pre-setting the look from the idea, the ten-line story and every scene as what the viewer sees and hears, dialogue that performs action, one light per scene with its dark side and a colour kept back, and the shot cards and asset tags that come out of it. Use when a film needs its look suggested, its story written or rewritten, or its story turned into shots and assets.
user-invocable: false
---

# Film story

The story is written for the viewer, in the viewer's words. The shot list is written from the
story and never the other way round. Read these before the step they serve:

| File | Read it before you… |
|---|---|
| `references/story.md` | write or rewrite the story |
| `references/dialogue.md` | write a spoken line |
| `references/breakdown.md` | turn the story into shot cards and asset tags |
| `references/look.md` | suggest a look, or use the user's reference images |
| `references/light.md` | set a scene's light on its cards, or keep a colour back for one moment |

## Suggest the look from the idea

The look comes before the story, because genre decides how the story is told. Pre-set
`picsart_film_setup` from the idea with `suggested`, one line of `why` per value:

- **The genre the events make.** Two people fighting is action; two people talking is drama. A
  custom genre is the user's own words.
- **A tone only when the story names a period or a tradition of cinema.** A tone is an era recipe:
  it sets the rig, not the colour. Otherwise leave it on auto. The console expands a tone into its
  camera and lens pills before applying any pill you also name, so an explicit `camera` or `lens`
  wins over the tone's.
- **Only the console's own controls.** The lens is a glass family, never a focal length. Focal
  length, aperture, framing, shot length and camera movement are per-shot choices on
  `picsart_film_shotlist`; grain rides in the camera preset; pace is written per shot, never set.
  Ids the console does not have are ignored, not guessed at.
- **The colour only when the idea names one**: one line of direction as `paletteHint`, written as
  a scheme around a hue ("analogous around amber"). The console shows it as a hint and applies
  nothing; it has no palette to pre-set. The colour is the user's; suggest, never decide it.
- **The frame from the user's own words** (`vertical`, `9:16` and `tiktok` resolve the same), and
  the runtime they said. The console offers only the five frames video models render broadly
  (16:9, 4:3, 1:1, 3:4, 9:16): for scope or 21:9, shoot 16:9 and crop in the edit.
- **Where each goes.** `film` (the title) is required, and `paletteHint` is its own top-level
  argument. Genre, tone, `ratio` and `duration` all go inside `suggested.selections`, in those field
  names, never as top-level arguments: the schema allows nothing else. The `why` lines go in
  `suggested.why`, keyed the same way.

Pass only what the material answers and leave the rest on the console's defaults: a wrong prefill
reads to the user as a decision someone already made. The console's presets are its own; choose ids
from it and never write a preset's text yourself.

## Write the story

Ten lines at the top, then every scene in order, as `references/story.md` says. Before you show
it, check:

- the thing the story is about is seen in the first scene;
- who holds what, and where people are, is visible, not implied;
- the events belong to the genre;
- nothing contradicts what the user's brief fixed;
- every scene has action, and every object belongs to the world and its period.

State the identity budget you inferred ("two faces and one garage"); never ask the user to choose
it. A short affords two or three faces and one to three rooms comfortably. A crowd is one asset with
a count.

**A note about what happens is answered with the rewritten paragraph**, shown whole. Never with a
shot list, a table or options. A fixed fact the note would touch is the user's to change, not
yours.

## Break it down

Every shot becomes a card, as `references/breakdown.md` says: the action and the line copied from
the story, who and what is in frame by tag, what each visible face feels (held in, except the
peak shot's face: "@teo relief, unguarded: the tears come", the word `unguarded` and what shows,
on that one card only), the seconds and the camera. Every person, place and prop the film shows gets a tag, and every lasting change the story
makes to one gets a tag of its own.

**Write the story, not the videos.** The story is never stretched to fill a model's ceiling or
cut to fit it, and a scene never changes place to make a video edge. The edges are made by the
camera, later.

## Traps

- Writing a drama under an action look, or keeping a story after the genre changed. Rewrite the
  story first.
- A story in film words ("we open on a wide"). A reader who knows nothing about film reads it as
  the film.
- Softening a fight or a fire to protect the render. Action, crowds, water and fire are not cost
  flags.
- Vague choices: "moody", "cinematic", "looks emotional". Write what is seen.
- A shot longer than its action, to fill a run.
- Leaving out what each face feels. Every card carries it.
- Treating the user's photo of a real person as a mood reference. It is the person.
