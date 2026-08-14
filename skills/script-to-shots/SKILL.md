---
name: script-to-shots
description: Use when a user has a script, storyline, treatment or scene list and needs it cut into generation ready video chunks before anything is generated, so a failure costs 5 seconds instead of 20. Trigger phrases include "split this script into shots", "splitting a script", "chunk my scenes", "chunking scenes", "break this script into clips", "turn this script into a shot list", "cut this scene up", "how do I split this scene", "shot list from a script", "break my storyline into scenes", "turn this treatment into clips", "scene breakdown for video generation", "how many clips is this script", "how long is this scene", "how many seconds is this line", "time this dialogue", "5 second clips", "10 second clips", "fit this into 5 seconds", "this scene is too long to generate", "split this into shorter clips". Cost and failure phrases are triggers too: "cheaper retries", "make retries cheaper", "my generation keeps failing", "my 20 second clip failed", "I am burning credits on failed clips", "regenerate just the broken part", "stop wasting credits on long clips", "cheapest way to generate this scene", "which parts do I have to regenerate". So are continuity phrases: "my chunks do not cut together", "the clips do not match at the join", "the character changes between chunks", "how do I carry the last frame into the next clip", "the split is mid-word". Also use when a user pastes several pages of script and asks what to generate first. The output is a directory of standalone prompts, 1 per chunk, not a single prompt.
license: MIT
metadata: {"author": "Picsart", "version": "1.0.0", "hermes": {"category": "creative", "tags": ["picsart", "video", "script", "shot-list", "chunking", "duration", "continuity", "prompt-engineering", "cost"]}}
---

# Script to shots

You take a script, storyline, treatment or scene list and return a running order of chunks small
enough to be cheap to retry, each one written out as a complete prompt that can be generated on
its own.

**Your output is a directory of standalone prompts.** You do not generate video, you do not
call a generator, and you do not hand back a plan to be turned into prompts later. Someone opens
1 file, pastes what is in it, and gets that chunk.

## Why the chunks are small

Generation is billed per clip and it fails often. A failed 20 second clip costs 4 times a failed
5 second one, and the odds of failure rise with duration, because a longer clip gives a subject
more time to drift, a hand more time to deform and a style more time to wander.

So the question is never "how long should this scene be". It is "what is the smallest unit that
still makes sense".

| what you could ask for | what it costs when it fails |
|---|---|
| 1 clip of 20 seconds | the whole 20 seconds, regenerated whole |
| 4 clips of 5 seconds | 5 seconds, and the other 3 are still good |

Generators work in fixed units. 5, 10 and 20 seconds are the common ones, and which of them
exist depends on the model, which is why the model is the first thing you ask about.

## Rule one: never invent the script

Splitting is arithmetic on what is written. Adding a beat, a line, a location or a character
that is not on the page is a different job, and doing it quietly is the worst failure available
here, because it propagates into every chunk file and then into every generation.

If the page does not say where a scene is set, who is in it or what they are wearing, **ask**.
If the user wants those decisions made for them, that is auto mode below, where they have signed
up for it.

Never ask more than 5 questions in 1 turn, and never ask about something already on the page or
already settled by a style guide.

## Mode: interactive or auto

### Interactive mode, the default

2 hard STOP gates: the scene boundaries in stage 2, and the running order in stage 4. You
present, the user replies `continue` or edits, and only then do you carry on. Pick this unless
the user has opted out.

The running order gate matters more than it looks. It fixes how many clips get generated and
therefore what the whole job costs, so it is the last cheap moment to change your mind.

### Auto mode, opt in

Detect auto mode when the request contains `auto`, `auto mode`, `no approvals`,
`skip approvals`, `don't ask`, `no questions`, `just do it`, `yolo`, `full auto`, `end to end`
or `run all stages`. Then you run every stage without stopping, choose every missing decision
yourself, write the files, and list your assumptions in 1 line each so they can be corrected in
1 pass.

If the wording is ambiguous, ask once: *interactive, where I stop at the scene list and again at
the running order, or auto, where I write the whole set and you correct it after?*

Even in auto mode you still:

- **Announce the chunk count and the total runtime** before writing the files, in 1 line, so the
  user can stop you if the count is wrong.
- **Say what you inferred** rather than presenting an inference as something the script said.
- **Stop on genuine ambiguity.** If a scene could be 1 chunk or 4 depending on something the
  script does not settle, ask once.

### Stage behaviour

| stage | interactive | auto |
|---|---|---|
| 0 intake | Ask, wait | Ask, then take defaults if unanswered |
| 1 classify input | Say what you got, continue | Same |
| 2 scene boundaries | Present the scene list, **STOP** | Present briefly, continue |
| 3 duration estimates | Present with the basis for each, continue | Same |
| 4 units and splits | Present the running order, **STOP** | Announce chunk count and total, continue |
| 5 inherit attributes | Do it | Do it |
| 6 continuity | Do it | Do it |
| 7 write files | Write, report | Write, report |

## Stage 0: which model, and what durations does it offer

Ask first, because the answer decides which chunk lengths exist. A plan built around 5 second
units is wrong for a model that only offers 6 and 10.

| route | how | notes |
|---|---|---|
| Host model | You write the prompts yourself | Default. No setup. You still need to know the target generator |
| Picsart gen-ai MCP | `picsart-gen-ai` server at `api.picsart.com/gen-ai/mcp` | Keeps planning and generation in 1 place |
| Picsart MCP | `picsart` server at `mcp.picsart.io/v1` | Editing and asset tools, useful for pulling the last frame of a chunk |
| `gen-ai` CLI | Explicit `--model seedance-2.0`, `--model kling-v3-pro` | Named model, batch work across many chunks |
| A named model through MCP | Ask the MCP for the model by name | When the user wants a specific model doing the writing |

If a requested route is unavailable, say so plainly and offer the next best. Do not fall back
silently.

Then ask the rest in 1 message, with defaults:

```
5 things and I can cut this up:
1. Which model is generating? (decides the chunk lengths available)
2. What durations does it offer? (suggest 5 and 10, and I will avoid 20)
3. Aspect ratio? (suggest 9:16 for a feed, 16:9 otherwise)
4. Audience, and anything that must never appear?
5. Is the dialogue generated with the picture, or recorded and laid over afterwards?
```

**Also establish whether the model generates an audio track at all**, from its documentation
rather than its name. It decides whether `<shots>/shared.md` carries an `Audio` block or says the
sound is a post step, and it is not something to leave until the chunks are written. On a model
that generates audio, every chunk needs the audio line: 9 chunks each inventing their own bed do
not cut together. Record it in `<shots>/manifest.json` as `audio`.

**And ask about the theme**, the 1 piece of music running under the whole piece. Propose one rather
than asking an open question, because an open question returns a genre and a genre is not a clause:
*suggest solo piano and low strings, 92 BPM, minor, laid over in post so it does not restart at
every cut.* The theme goes in `<shots>/shared.md` under its own heading and into
`<shots>/manifest.json` as `themeMusic`.

Music is the one attribute that copying cannot carry across chunks. Identical clauses produce
different takes, so the score restarts at every join. For a chunked set the default is a post track
with `no music` in every chunk prompt, and only a `000-single-pass.md` set can generate a theme that
truly plays throughout. See `references/inheritance.md`.

Question 5 changes the arithmetic, not just the prompt. If dialogue is added afterwards, the
picture only has to hold for the length of the line and the chunk can be cut on the action
instead. If the model is generating the speech, the line has to fit inside 1 chunk with a beat
at each end, and that is what forces most splits.

Question 4 is not optional and you must not guess it. Record the answers and carry them into
every chunk file.

If the user does not know the durations, plan in 5 and 10, say that is what you assumed, and
note it in `<shots>/manifest.json` as an open question.

## Stage 0b: is there a style guide or a character bible

**Look before you ask.** Both live in the project, and the user may not remember the slugs:

```bash
ls -1 ./gen-ai/style/ ./gen-ai/characters/ 2>/dev/null                   # this project
ls -1 ~/.gen-ai/projects/style/ ~/.gen-ai/projects/characters/ 2>/dev/null   # shared, read only
```

Name what you found. Only ask when both places come up empty:

```
Do you have a style guide or a character bible for this? If style-guide-builder has run,
give me the slug and I will take the style, palette, lighting and character descriptions
from it verbatim.
```

`<guide>/` is the chosen style directory and `<bible>/` the chosen bible directory, in the
project when it is there and the shared location otherwise. **The project copy wins when a slug
is in both**, and say which you used. Both prefixes matter, because this skill has its own
`references/` directory and a bare filename does not say which of the 3 places it is in.

Where a chosen guide or bible came from the shared location, say so once and offer to copy it
into the project. Chunk files repeat its clauses verbatim, so the day that shared copy is edited
for another production, this shot set no longer matches its own source and nothing records why.

| read | take from it |
|---|---|
| `<guide>/manifest.json` | Which aspects are established and which are guesses. Its open questions are your questions |
| `<guide>/audience.md` | What is forbidden. **Outranks your own judgment on every chunk** |
| `<guide>/STYLE.md` | The rules that matter, if you read nothing else |
| `<guide>/palette.md` | The colour and grade line for `<shots>/shared.md`, verbatim |
| `<guide>/lighting.md` | The lighting line, and which named variant fits each scene |
| `<guide>/rendering.md` | The medium and style line |
| `<guide>/camera.md` | Shot sizes and framing habits. Check `Applicability` before writing any lens or depth of field language |
| `<guide>/motion.md` | Pacing and camera movement. Often says motion is unknown, which is the answer |
| `<guide>/negatives.md` | Merge into the exclusion line in `<shots>/shared.md` |
| `<guide>/fragments.md` | Ready made clauses. Prefer these to writing your own |
| `<guide>/characters.md` | Character descriptions, verbatim |
| `<bible>/CHARACTERS.md` | The authoritative description per character. Beats `<guide>/characters.md` where they disagree |
| `<bible>/<character-id>.md` | The `Verbatim description`, and the `Wardrobe` heading for what they wear. Paste the description rather than summarising it |

**Take these clauses verbatim.** Copy them into `<shots>/shared.md` unedited, then copy them
from there into every chunk file. Paraphrasing between chunks is the main cause of a sequence
that will not cut together, and it is invisible until you watch the joins.

If neither exists and the script has a recurring character or a look that has to hold, say once
that `style-guide-builder` would fix that properly. Do not push it twice.

## Stage 0c: does this need splitting at all

Ask this before you split anything, because for some pieces the answer is no and the whole
chunking exercise makes the result worse.

Chunking exists because a failed long generation is expensive. It has a cost of its own though:
**every boundary between separately generated clips is a place where the style, the cast or the
light can fail to match**, and nothing carries across a boundary except the lines you clone into
each file. When a piece has nothing that must land at a precise moment, one generation removes
that entire class of problem.

### What forces splitting

Any one of these, and you split as normal:

- Spoken dialogue, because lip sync has to match a specific waveform
- On-screen text appearing or changing at a set point
- Music sync, where a cut or a movement lands on a beat
- A plot beat that must be readable, such as an object changing hands
- A change of location or of cast
- The model's maximum duration, which is a limit rather than a judgment
- Photoreal human faces held in close-up, where drift is most visible

### What does not force splitting

- **Non-verbal sound.** A sigh, a gasp, a laugh, humming, an animal noise, "uhh", "ohh". None
  of it needs frame-accurate lip sync, so none of it forces a cut. Note the sound and roughly
  where it falls.
- Several beats of action, as long as no single one has to land on a specific frame
- Camera changes, which are described inside one prompt and are not a reason to split

### If nothing forces it

Say so, and offer the single-pass version instead of a pile of chunk files. A children's
cartoon of animals playing with no dialogue is the clearest case: one setting, a forgiving
style, nothing landing on a frame, and the hardest problem, keeping the animals looking like
themselves, disappears because there are no separate clips to match.

Then **the output is one file, not many**. Write `<shots>/000-single-pass.md` containing the
whole piece as one prompt with its beat structure inside, and say in `<shots>/SHOTS.md` that it
is a single generation and why. Do not also write per chunk files: two versions of the same
piece is how the wrong one gets generated.

The beat structure inside that one prompt still changes scene every 5 to 10 seconds, and still
changes the camera at every beat, exactly as the chunked version would. The difference is that
it is one generation and the shared description is stated once. The form is in
`references/single-pass.md`.

Ask what a failed long render costs before committing to it. One 60 second attempt that fails
costs what twelve 5 second clips would have, and the user may or may not mind.

## Stage 1: read what you were given

Classify the input before touching it.

| input | what it means |
|---|---|
| A script with scene headings | Boundaries are given. Go straight to stage 3 and evaluate each scene as written |
| A numbered scene list | Same, but check the numbering is not hiding 2 scenes in 1 entry |
| A treatment or prose paragraphs | Boundaries are not marked. Find them in stage 2 and confirm them |
| A 1 paragraph storyline | Boundaries do not exist yet. Propose them and expect to iterate |
| A shot list with durations already on it | Check the durations against stage 3 rather than trusting them. Guessed durations are the usual reason a set fails |
| A script plus a complaint that clips do not cut together | The joins are the job. Read `references/splitting.md` and fix continuity before re-splitting |

Say in 1 line which of these you got, because it tells the user which stages will need them.

## Stage 2: find the scene boundaries

Skip this when the input already has scene headings. Otherwise, a boundary is a change in 1 of
these, and the more of them change at once, the more certain the boundary is:

- Location
- Time of day
- Who is present
- Who is speaking
- The subject of attention

A paragraph break in prose is a hint, not a boundary. Dialogue attributed to a new speaker in
the same room is a boundary between chunks, not always a boundary between scenes.

Present the result as a numbered list, 1 line each, and in interactive mode **STOP**. Getting
this wrong makes every later stage wrong, and it is 1 message to check:

```
I read this as 6 scenes. Say continue, or tell me which to merge or split:
1. Kitchen, morning, Maya alone, she finds the note
2. Kitchen, continuous, Maya reads it aloud
...
```

## Stage 3: estimate the duration of each scene

Estimate from what is on the page, and **never write a bare number**. Every estimate carries
its method in brackets, the way a style guide rule carries its evidence:

- `5 seconds [dialogue, 9 words at 2.5 per second plus 1 second of beats]`
- `5 seconds [action, 2 completed gestures at about 2.5 seconds each]`
- `10 seconds [camera, a slow push across a 6 metre room]`

Dialogue is the reliable anchor. Spoken English runs at roughly 150 words per minute, so about
2.5 words per second. **Count the words in the line.** Do not judge a line by how long it feels,
because that is how a 12 word line ends up in a 5 second clip with the end cut off.

| words in the line | speech alone | with a beat at each end |
|---|---|---|
| up to 9 | under 4 seconds | fits 5 |
| 10 to 12 | around 5 seconds | needs 10 |
| 13 to 22 | 5 to 9 seconds | fits 10 |
| more than 22 | over 9 seconds | split the line |

Always add roughly 0.5 seconds before the line and 0.5 seconds after. A clip that starts
mid-word is unusable, and a clip that ends on the final consonant cannot be cut against
anything.

Action without dialogue has no word count, so it needs a different method, and you say which
method you used. The methods, with the numbers to use, are in
`references/duration-estimation.md`. Read it before estimating a scene that has no speech in it.

Present the estimates as a table with the basis in every row. In interactive mode this does not
need a STOP, because the running order gate in stage 4 covers it.

## Stage 4: choose the unit, or split

Per scene, in this order:

| the estimate | what to do |
|---|---|
| Fits 5 seconds | Ask for 5. This is the default and most scenes should land here |
| Does not fit 5, fits 10 | Ask for 10, and say in the chunk file why it is not 5 |
| Does not fit 10 | **Split it** into chunks that each fit 5, or 10 where a line forces it |
| Fits 10 but contains 2 actions | Split into 2 chunks of 5 anyway. 2 clips of 5 is a better bet than 1 of 10 |

Do not ask for 20 seconds. If the model offers it, still do not use it: 20 seconds is 4 failed 5
second clips in a single billing event with no partial recovery.

Where to put the cut, and where never to put it, is in `references/splitting.md`. The 2 rules
that always apply: **never split mid-word and never split mid-gesture**, and prefer a boundary
at a beat, a breath, a cut or a change of subject.

Then present the running order and in interactive mode **STOP**:

```
14 chunks, 80 seconds total, all 5s except 3 at 10s where a line would not fit.
Scene 3 splits into 3 chunks, scene 5 into 2. Say continue, or name a chunk to change.
```

## Stage 5: clone the attributes into every chunk

When a scene is split, **every chunk inherits the original scene's attributes**. This is the
whole point of the exercise. A chunk generated without them will not cut against its neighbours,
and the failure shows up as a wardrobe change, a light that moves or a face that is not the same
face.

The list to clone, per chunk: setting, characters present, wardrobe, time of day, lighting,
style and medium, palette and grade, camera treatment, mood, aspect ratio, audio, and the
exclusion list.

The full table, including what may legitimately differ between chunks and what must not, is in
`references/inheritance.md`.

**The shared lines are copied byte for byte.** Write them once in `<shots>/shared.md`, then copy
that text into each chunk file without touching it. Not a rewrite, not a tidy up, not a better
word for the same thing. If a shared line needs to change, change it in `<shots>/shared.md` and
recopy it into every chunk file, including the ones that already read well.

## Stage 6: continuity across the boundaries

Every chunk file states where the chunk starts and where it ends, in the same words that its
neighbours use.

- **Continuity in**: the pose, position, expression and camera framing the chunk opens on.
- **Continuity out**: the same 4 things as the chunk closes. The continuity out of chunk N and
  the continuity in of chunk N plus 1 are the same sentence, word for word.

Where the model supports image to video, say so in the chunk file: take the last frame of chunk
N and pass it as the first frame of chunk N plus 1. Then that chunk's prompt **must not
redescribe the frame**, because the model already has it. Prompt the motion only. This is the
single most reliable way to make 2 chunks cut together, and it changes what the prompt says, so
it belongs in the file rather than in your report.

Details, including what to do when a camera move has to continue across a boundary, are in
`references/splitting.md`.

## Stage 7: write the files

Write to `<root>/gen-ai/shots/<slug>/` inside the project, where `<root>` is the git root if
there is one and the working directory otherwise, and `<slug>` is a short name for the script.
Files in it are written below as `<shots>/name.md`.

**Write into the project, never into a shared home directory.** A shot list is the most
project-specific thing here: it is one script, cut one way, for one model. Collected centrally it
is unreadable within a couple of productions, and `001-cold-open.md` appearing in three shot sets
at once is how the wrong chunk gets generated. `~/.gen-ai/projects/shots/` is read only, for
picking up a set someone deliberately shared.

If the working directory is plainly not a project, a home directory or `/tmp`, ask which folder
the production lives in rather than writing somewhere it will be lost.

| file | contents |
|---|---|
| `<shots>/SHOTS.md` | The index. The full running order, each chunk with its duration, 1 line of what happens, and its file name |
| `<shots>/NNN-short-slug.md` | 1 per chunk. A complete standalone prompt, plus its duration, continuity and estimate basis |
| `<shots>/shared.md` | The style and exclusion lines that every chunk repeats verbatim |
| `<shots>/manifest.json` | Machine readable: slug, source name, target model, unit durations used, chunk list with durations and estimated word counts, total runtime, open questions |

One file is written outside the shots directory: `<root>/gen-ai/README.md`, the index of what this
project contains. Add or update the one line for this shot set under `## Shot sets`, and leave
every other section alone. `style-guide-builder` owns `## Styles` and `character-bible-builder`
owns `## Characters`.

**Required headings for every one of these files are in `references/output-files.md`.** Other
skills read these files by heading, so a renamed heading breaks them. Read that file before
writing, not after.

Each chunk file's prompt is written in the clause order that `video-prompt-engineer` uses:
duration, aspect ratio, medium and style, shot size, camera angle, camera movement, lens, depth
of field, lighting, colour and grade, subject motion, mood, pacing, audio, exclusions. The
order and the reason for it are in `video-prompt-engineer/references/structure.md`, and the
clause vocabulary is in the other files in that directory.

Number the files from `001`, in running order, so they sort the way they play.

## Stage 8: hand off

Report, and keep it short:

1. **Where the files are**, and the chunk count and total runtime.
2. **The running order**, inline, 1 line per chunk, so the user gets the shape without opening
   anything.
3. **What forced each 10 second chunk**, 1 line each. These are the expensive ones and the user
   may want to rewrite a line to get them down to 5.
4. **What is inferred rather than on the page**, so the wrong guesses can be caught before 14
   clips are generated from them.
5. **From the style guide or the bible**, when either was used: which slug, and which lines came
   from it verbatim.
6. **What to generate first.** Name 1 chunk that is representative rather than the first one, so
   a single test render tells the user whether the shared lines are right.

Offer that test render in the same turn. 1 generated chunk catches a wrong shared line faster
than reading all 14 files, and the user finds out now rather than after paying for the set.

## Working with the other skills

- **`video-prompt-engineer`** owns the prompt craft. Its `references/` directory has the clause
  vocabulary, the exclusion groups and the defect table. Point a user there when a single chunk
  is coming out wrong; come back here when the problem is the length or the joins.
- **`style-guide-builder`** produces the guide this skill reads. If a look has to hold across a
  set of chunks and no guide exists, that is the gap.
- **`gen-ai-explainer`** runs its own scene planning for explainer videos. Do not duplicate it.

## Examples

A worked example, from prose through to a finished chunk file, is in `references/examples.md`.

## House rules

- Plain English. No em dashes, no en dashes, no double hyphens, no emoji, no smart quotes.
  Sentence case headings. Numbers as digits.
- No marketing voice. Do not write `unlock`, `leverage`, `seamless`, `dive into`, `supercharge`
  or `elevate`, in the files or in your report.
- Every estimate carries its basis in brackets. An estimate with no basis is a guess, and a
  guessed duration is what the whole skill exists to remove.
- Never state a word count you have not counted.
- Qualify every filename. `references/x.md` is yours, `<guide>/x.md` is the style guide,
  `<bible>/x.md` is the character bible, `<shots>/x.md` is your output. A bare filename is
  ambiguous.
- Do not name a model or a platform inside a prompt.
- Keep each chunk prompt under roughly 120 words. Past that, generators start dropping clauses,
  and the ones they drop are at the end, which is where the exclusions live.
