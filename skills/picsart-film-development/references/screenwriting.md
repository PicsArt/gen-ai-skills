# Writing for the medium — the script rules the pipeline implies

The production pipeline starts from a final draft of the script, and
everything it establishes about cost and consistency reaches backwards into
the writing: a script line commits the
production to assets, variants, and risks long before anyone generates a
frame. Load this file whenever the film has no script yet, or a supplied
script is being adapted — beside `dramaturgy.md`, which says what a scene has
to do where this file says what the medium can afford. It turns the
pipeline's economics into writing rules.

## 1. The budget is counted in identities, not minutes

Every distinct character, location, time of day, and state is an asset that
must be designed, generated, reviewed, and stress-tested before its first
scene can render. That is the real currency of a short film:

- A short comfortably affords **2–3 faces and 1–3 rooms**. One more minute of
  runtime is nearly free; one more character is a passport, a battery, and a
  two-shot test with everyone they share frame with.
- Propose the story **inside a stated budget** ("this story fits two
  faces and two rooms — here it is inside that") — infer the budget from the
  idea, never ask the user "how many characters can we afford".
- A named extra who acts is a character. A crowd is one asset with a count.
  A photograph of a dead relative on the wall is a prop *and possibly a
  face* — notice what a sentence orders.

## 2. Write what the models are good at

Faces, hands, objects, contained rooms — close performance beats are the
medium's home turf. So is action, when it is written one big clear movement
per shot: a charge, a throw, a fall (nothing in the story is a cost flag; the
genre decides, and the video model was chosen for it).
In-frame text (signs, letters) is the one thing written around: it is a
separate task in the edit, never generated in-shot.

**Spoken performance is home turf too.** Current video models generate native
audio with lip-synced dialogue in-shot, and the film's model is *selected* for
that capability when the production picks it — so a talking character is not a
cost of any kind, and lip-sync is not a risk. Write the conversation the
story wants. Never propose a mute or non-speaking character, a voice-over
substitute, or a "visual-only" version of a scene as a way of dodging lip-sync;
if silence is the right choice, it is because the scene plays better silent. The
one audio cost that IS real lives further downstream and is a different problem:
voice timbre can drift between takes. Copy each character's saved voice description
verbatim and review the result (`workflow.md`); this is not a reason to write fewer lines.

## 3. Scenes stay put

One location, one time of day per scene. A location hop mid-scene, or dusk
falling inside a scene, silently orders another location variant (street-day
and street-night are two assets). Re-use rooms: a story that returns to the
same two spaces photographs better AND costs half as much as one that tours
five.

## 4. Beats must photograph

Dramaturgy is carried by what the camera can see change: a prop handed over,
a wardrobe change, weather, damage that persists. Each visible state change
is a state variant being ordered at script time (`@seneb_swollen` was born in
a sentence). Write them deliberately and sparingly — and know that an
internal beat with no visible correlative will not survive generation. Every
beat that matters takes the playable shape (`dramaturgy.md`): starting
condition → subject + verb + target → resistance → visible reaction → result.
"Looks emotional" is not a beat; a hand closing on empty coins is.

## 5. Dialogue economics

- **Short lines, one line per shot.** Every spoken line ends in a second of
  silence inside its clip; long speeches fragment into shots.
- **A line costs a little more than a look** — a speaking character is a locked
  asset with a voice block, and its shots carry one extra review dimension. That
  is ordinary production cost, not a risk: spend it wherever the story is
  carried by what someone says. Reaction shots are nearly free, so a written
  exchange is cheapest as line → reaction rather than line → line.
- **End beats on action, not speech** — an action gives the editor a cut
  point and the next shot a hand-off.

## 6. Language laws start in the script

The script's words flow downhill into descriptors and prompts, so the ban
dictionary applies from the first draft: never a character's age as a number
(carry it through role, clothes, condition); actions in positive form; avoid
words the filters punish. A script written inside the language laws never
needs a risky rewrite at prompt time.

## 7. The look is the console's

Tone, colour scheme, camera and lens are locked on `picsart_film_setup` before the
script is written (`workflow.md`, Stage 1); the script inherits them and never
restates them. What the script does own is the telling detail (§9).

## 8. Structure and runtime math

Idea → the story: ten lines, then every scene as what we see and hear
(`dramaturgy.md` owns the structure; this section owns the arithmetic). Count runtime in **shots, not
pages**: a scene beat is usually 1–3 shots, with dramatic coverage commonly cutting
at 3–8 seconds and action shorter. A longer hold is an authored exception, not
the default unit. No parallel storylines on a short: cross-cutting multiplies
worlds, palettes, and assets faster than it multiplies meaning.

**Write the story, not the videos.** The film generates in videos of at most
the model's ceiling (30 s on Seedance 2.5), and the edge between two videos is
joined by the camera, not by the story (`../../picsart-film-scenes/references/seams.md`,
*The video edge*): the last shot ends mid-movement, the next video
opens on a clearly different angle. So the story is written as the story
wants — scenes where the story changes place, and only there — and the video
plan (`workflow.md`, Stage 1 step 5) names each edge in one sentence. Do not
end every act on a scene change to make the edge "clean": it moves the people
to a new place every thirty seconds for no reason. Fill a video with the scene's short coverage shots and let the
model make the declared cuts; never stretch one action to the ceiling.

## 9. Design rhymes with character

Every visual choice — scar, fabric, colour, the state of the shoes —
restates who the person is and what the story does to them (a detail that
says nothing is a detail the model will vary freely). This starts in the
script's nouns: write the telling detail, not an inventory.

## A supplied script

Keep it — it is the story document, and Stage 1 step 3 is done. Read it once
for the two things the medium cannot do — in-frame text, a character's age as
a number — and say them in one line each as suggestions. Do not review it for
expense or flag complex elements and location hops beside a cheap rewrite:
that softens stories to protect renders nobody has tested.
