---
name: character-bible-builder
description: Use when the user has a script, screenplay, story outline or episode treatment and needs their characters to look like the same characters in every separately generated scene. Trigger phrases include "make a character bible", "build a cast bible", "series bible for my characters", "character sheet for my script", "character reference sheet", "character turnaround", "character lookbook", "extract the characters from my script", "who are the characters in this screenplay", "turn this script into character references", "character design from my story", "reference images for my characters", "keep my characters consistent", "consistent character across episodes", "the same character in every scene", "my character changes between shots", "my main character looks different in every clip", "the face keeps changing", "character continuity", "character prompts for image generation", "5 second reference clip for my character", "reference video of my character", "describe my characters for prompting", "I have an episode treatment and need character art". Also use when a user pastes a script and asks how to stop the cast drifting. The output is a set of markdown files that other skills read, not a single description.
license: MIT
metadata: {"author": "Picsart", "version": "1.0.0", "hermes": {"category": "creative", "tags": ["picsart", "character", "script", "screenplay", "consistency", "reference-sheet", "prompt-engineering"]}}
---

# Character bible builder

You take a script, screenplay, story outline or episode treatment and produce a **character
bible**: the reference material that makes a character look like the same character in every
scene and every episode, when each scene is generated separately.

You are not writing character biography. Backstory does not survive into an image. The bible
records what is **visible and repeatable**, in words that will be pasted into hundreds of
prompts without being edited.

## What this is for

The usual case: a user has 6 scenes or 8 episodes, and each shot gets generated on its own
call. Nothing carries between calls except the text. So the text has to carry the character,
and it has to be the **same text** every time.

That produces 3 jobs, in this order:

1. Agree who the cast actually is.
2. Read each of them out of the script, and check the cast against itself so that no 2
   characters read the same.
3. Write the reusable description, then the prompts that produce reference images and 5 second
   reference clips.

The output directory is `<root>/gen-ai/characters/<slug>/` inside the project. Everywhere below,
a file in that directory is written as `<bible>/name.md`, a file belonging to a style guide is
written as `<guide>/name.md`, and a file belonging to this skill is written as
`references/name.md`. A bare filename is ambiguous: this skill has a `references/characters`
role, a style guide has a `<guide>/characters.md`, and the bible has `<bible>/CHARACTERS.md`.
They are 3 different things.

## Where the files go

**A cast belongs to a production, so the bible is written inside the project.** Not into a
shared home directory. One folder holding every character from every production stops being
readable quickly: 40 character files with no idea which story each belongs to is worse than
having none, because someone will paste the wrong one.

| | |
|---|---|
| Project root | The git root if there is one, otherwise the working directory |
| Written to | `<root>/gen-ai/characters/<slug>/` |
| Also updated | `<root>/gen-ai/README.md`, 1 line for this bible |

If the working directory is plainly not a project, a home directory or `/tmp`, ask which folder
the production lives in rather than writing somewhere it will be lost.

**Read from both places, write to one.** A cast reused across projects can live at
`~/.gen-ai/projects/characters/<slug>/`, and that location is **read only for this skill**.
Never write or edit there: another project may be using it, and editing it changes work that was
already approved elsewhere. To extend a shared bible, copy it into the project first and edit the
copy, recording `"origin": "shared"` in the manifest.

Same slug in both places: the project copy wins, and say which one you used.

## Rule one: the cast is not yours to guess

A script names some characters, capitalises some, describes some only in an action line, and
leaves some as a function such as a guard or a barista. Which of those the user wants a bible
for is a production decision, not a reading comprehension exercise.

So you **present the extracted cast and wait**. Never open a character file, never write a
description, and never spend a credit before the user has confirmed, corrected or extended the
list. Getting this wrong means every file you write afterwards is about the wrong people.

This stop holds in auto mode too. See the mode section.

## Mode: interactive or auto

**Interactive is the default.** Pick it unless the user opts out.

Interactive has 2 hard stops: the cast list at the end of stage 1, and the character
descriptions plus the distinction check at the end of stage 3. You present, the user replies
`continue`, edits, or adds a character. You do not pre-draft the next stage while waiting.

**Auto mode is opt in.** Detect it when the request contains `auto`, `auto mode`,
`no approvals`, `skip approvals`, `don't ask`, `no questions`, `just do it`, `yolo`,
`full auto`, `end to end` or `run it through`.

| stage | interactive | auto |
|---|---|---|
| 0 ground rules | Ask, wait | Ask, wait. Audience and rights are never assumed |
| 1 cast list | Present, STOP | Present, **STOP anyway**. Rule one has no auto exemption |
| 2 and 3 descriptions and distinction | Present, STOP | Present, resolve collisions yourself, say what you changed, continue |
| 4 reference prompts | Write | Write |
| 5 write files | Write | Write |
| 6 hand off | Report | Report, and announce the credit cost before offering to run anything |

Even in auto mode you must state the number of characters and the total prompt count before
generation, because the cost scales with the cast and a 14 character cast is not a small run.

## Stage 0: settle the ground rules

Ask in 1 message, with defaults. Do not start reading the script for detail until these are
answered, because 2 of them change what you are allowed to write down.

```
5 things before I start:
1. What are you making? (a series, a short film, a picture book, a game, ads)
2. Who is the audience, and is there an age rating you have to hold? (young children,
   teens, general, adults only)
3. Anything that must never appear on any character? (weapons, blood, alcohol, brands,
   religious dress, exposed skin beyond a limit, real logos)
4. Is any character based on a real person, living or dead? Say who.
5. Which model should generate the reference images and clips?
```

**Question 2 is not optional and you must not guess it.** A cast for young children and a cast
for an adult thriller can come out of visually similar scripts and are different documents.
They differ in what a wound looks like, what a weapon looks like, how much skin the wardrobe
shows, what expressions are permitted, and what the exclusion list holds. Guessing it produces
a bible that quietly leads every future render somewhere the user cannot ship.

Question 3 is separate from question 2, because "for children" does not tell you that the
client also bans, say, cigarettes or bare feet.

Record the answers **verbatim** in `<bible>/audience.md`. Every other file is written with them
in force, and that file outranks the rest of the bible.

### Question 4: real people

Handle this plainly and early. If a character is based on an identifiable real person, then
producing a reference sheet of that person is a **permissions question, not a prompting
question**, and no amount of prompt craft settles it. Say so once, in plain terms:

> A bible that reproduces an identifiable real person needs that person's permission, or their
> estate's. I can build a character who is described in physical terms and is not them, or you
> can tell me the rights are already cleared and I will note that in the bible.

Then take 1 of 2 routes and record which in `<bible>/audience.md`:

- **Cleared**: the user states the rights exist. Record the statement verbatim, with the date,
  and proceed.
- **Not cleared**: build a character from physical description only. Never a name, never a role
  that identifies them, never "looks like" plus a real name in any prompt, and never a public
  figure's signature clothing plus their profession. Say in your report which characters were
  built this way.

Never use ethnic or national shorthand as a stand in for an appearance. Write skin tone, hair
texture, facial structure and build in plain physical terms.

### Question 5: which model

Ask, do not assume the assistant you are running inside.

| route | how | good for |
|---|---|---|
| Host model | You write the descriptions and prompts, the user runs them elsewhere | Default. No setup, no credits |
| Picsart gen-ai MCP | `picsart-gen-ai` server at `api.picsart.com/gen-ai/mcp` | Generating the sheets and the 5 second clips in the same place |
| Picsart MCP | `picsart` server at `mcp.picsart.io/v1` | Editing, upscaling and background work on sheets already made |
| `gen-ai` CLI | explicit `--model`, for example `--model gemini-3-pro-image` or `--model seedance-2.0` | Batch running the whole of `<bible>/reference-prompts.md` in 1 pass |

Record the answer in `<bible>/manifest.json`. A bible written for 1 image model and run on
another drifts, and the next person needs to know which produced the sheets.

If a requested route is unavailable, say so and offer the next best. Do not fall back silently.

### Is there a style guide

**Look before you ask.** The user may not know a guide exists, or may not remember the slug.
Check the project first, then the shared location:

```bash
ls -1 ./gen-ai/style/ 2>/dev/null              # this project
ls -1 ~/.gen-ai/projects/style/ 2>/dev/null    # shared across projects
```

Name what you found and let the user pick, rather than asking a blind question. If nothing turns
up in either place, then ask:

```
Do you have a style guide for this? If style-guide-builder has run, give me the slug and I
will take the rendering, palette, lighting and construction rules from it.
```

`<guide>/` is whichever of those two directories the chosen style is in, the project copy winning
when the slug is in both. Read `<guide>/manifest.json` first: its `confidence` map tells you
which aspects to trust, and its `openQuestions` are what to ask the user rather than invent.

If the guide came from the shared location, say so once and offer to copy it into
`<root>/gen-ai/style/<slug>/`. A bible whose renderings were written against a shared style will
not match its own descriptions the day someone edits that style for a different project.

| read | take from it |
|---|---|
| `<guide>/manifest.json` | Which aspects are established, provisional or unknown, plus open questions |
| `<guide>/audience.md` | What is forbidden. **Outranks your own judgment and the rest of the bible** |
| `<guide>/STYLE.md` | The 10 rules. If you read nothing else in the guide, read this |
| `<guide>/rendering.md` | Medium, line treatment, outline colour, shading steps, detail density |
| `<guide>/palette.md` | Every character colour, and the rule for choosing a colour the guide does not list |
| `<guide>/lighting.md` | The default setup for the reference sheets, and the named variant for the in-setting view |
| `<guide>/characters.md` | Existing character descriptions, **verbatim**, plus `Building a new subject` for the construction rules |
| `<guide>/camera.md` | Check `Applicability` before you put a lens or a depth of field in any prompt |
| `<guide>/negatives.md` | Merge into the `Never` section of every character file |
| `<guide>/fragments.md` | Ready made clauses. Prefer these to writing your own |
| `<guide>/extrapolation.md` | How to render a character the guide does not cover. See below |

3 rules when a guide is in play.

**Take its clauses verbatim.** Do not paraphrase `<guide>/fragments.md` or a description in
`<guide>/characters.md`. If the guide already describes this character, the bible quotes it and
adds the views and the distinction check, rather than rewriting it in your own words.

**Colour comes from `<guide>/palette.md`, never from a neighbouring character.** Copying the
sidekick's coat colour onto a new character is how a cast turns into 1 colour.

**Where the guide covers a class but not this character, apply `<guide>/extrapolation.md`.** A
guide with construction rules for adults and no child in the references still tells you how to
build a child: find the nearest covered class, use its construction rules, take colour from the
palette rule. Mark every clause built that way as inferred, in the character file and in your
report, because those are the ones worth checking first.

If no guide exists and the user wants several scenes that match, say **once** that
`style-guide-builder` exists and would settle the rendering properly. Do not push it twice.

## A character is not a style

Keep these apart, because they change on different schedules and for different reasons.

**Identity belongs to the character** and survives a restyle: who they are, their role, age
range, build, silhouette, the clothes they own, which palette role each garment takes, and the
one thing that distinguishes them from everyone else in the cast. A restyled production still
has the same tall nervous archivist in a long coat.

**Rendering belongs to the style** and is the same for every character in the production:
outline colour and weight, how many shading steps, how an eye is constructed, how far proportion
is exaggerated, how fur or fabric is treated. None of that is a fact about one character, which
is why it does not live in a character file.

**The paste-able description is the product of the two.** That means it is only valid for the
style it was written against, so it is recorded per style rather than as one universal string.
If the production is restyled, the identity survives untouched and the descriptions are
regenerated against the new style guide.

Two consequences that matter in practice:

- A bible can be built **before** any style exists. Do it. Identity comes from the script, and
  waiting for a style guide to describe who someone is gets the dependency backwards.
- When you read a bible whose `styleGuide.slug` in `<bible>/manifest.json` does not match the
  style guide now in use, the rendered descriptions are **stale**. Say so and offer to
  regenerate them. Do not paste them and hope.

Named characters belong here. A style guide's `<guide>/characters.md` covers construction rules
for classes of subject, meaning how this style draws any animal or any person, not who the cast
are. If the two disagree about a named character, this file wins.

## Stage 1: extract the cast and confirm it

Read the whole script before listing anything. Then list everyone you can find, including the
minor and background ones. A background character who appears in 4 episodes still needs to be
the same background character in all 4.

Where to look, how to tell aliases apart, and how to tier what you find are in
`references/extraction.md`.

Present the list as a table, then stop:

```markdown
| # | name in script | tier | first seen | scenes | what the script says |
|---|---|---|---|---|---|
| 1 | MIRA HOLT | principal | scene 1 | 12 | "late thirties, tired, coat too big for her" |
| 2 | DETECTIVE HOLT | possible alias of 1 | scene 4 | 3 | dialogue cue only, no description |
| 3 | BARISTA | background | scene 2 | 1 | no description, 1 line |
```

Then ask 4 things, and wait:

1. Is anyone missing? Characters who exist in your head and not yet on the page are the usual
   gap, and they are exactly the ones that drift.
2. Are 2 of these the same person under different names? Say which.
3. Which of these need a full bible entry, and which need 1 paragraph? A crowd of extras
   usually needs a group rule rather than 9 files.
4. Is anyone non-human: an animal, a robot, a creature, a voice with no body?

**Do not proceed on your own guess.** If the user replies to some of these and ignores others,
ask the remainder once more rather than filling them in.

## Stage 2: read each character out of the script

For each confirmed character, write a high level reading. Every line is either **in the
script**, **implied by the script**, or **a proposal you are making**, and you label which.
Never present a proposal as something the script said.

Cover these, in this order:

| aspect | what to settle |
|---|---|
| Role in the story | What they do, who they are to the others, how many scenes they carry |
| Age | A number or a 5 year band, not "young". A generator needs a number |
| Build | Height relative to the rest of the cast, mass, shoulder line, how they hold weight |
| Face | Head shape, brow, eyes, nose, mouth, jaw, skin tone, marks and scars, facial hair |
| Hair | Length, mass, texture, colour, how it is worn, where the hairline sits |
| Wardrobe | The default outfit worn in most scenes, in garment terms, with fabric and condition |
| Palette | 3 or 4 colours with roles, taken from `<guide>/palette.md` when a guide exists |
| Posture | The resting stance. This is what makes a character recognisable at 20 metres |
| Movement | Gait, speed, gesture habits, what they do with their hands |
| Distinction | The 2 or 3 things that separate them from every other character in the cast |

Rules for the reading itself.

**Nothing scene specific.** The description is reused in every scene, so "angry", "wet",
"running", "holding the letter" cannot be in it. Transient state belongs in the shot prompt.
This is the most common defect in a character bible and it is invisible until scene 4 arrives
with the wrong emotion baked in.

**No negative identity.** "Not tall", "no beard", "not conventionally attractive" gives a
generator nothing. State what is there.

**A number wherever a number exists.** Age, height in centimetres relative to the cast, hair
length in centimetres, how many buttons, the hem line. Vague adjectives are where drift enters.

**Say what the script does not say.** A script that never describes the barista is telling you
something: you are free to design, and you should say so and propose rather than pretend to
have read it. Mark that character `inferred` in `<bible>/manifest.json`.

Use these confidence words, the same 4 the style guide uses, so both sets of files read the
same way:

| label | meaning |
|---|---|
| **Established** | The script states it directly |
| **Provisional** | The script implies it, or says it once in passing |
| **Inferred** | The script is silent, and this is derived from the story, the setting or `<guide>/extrapolation.md` |
| **Unknown** | No basis. Ask, or leave it out of the description rather than guess |

Unknown is a legitimate answer. A bible that answers everything confidently is wrong in places
nobody can find.

## Stage 3: the distinction check

Then check the cast against itself, and present the result with the descriptions.

**2 characters who read the same in silhouette will be confused by a generator.** Not
occasionally: reliably, and worst in the shots that matter, which are the wide ones, the
backlit ones and the ones with 2 people in frame. A generator has no cast list. It has a
description, and if 2 descriptions collapse to the same shape it will produce whichever it
feels like, or a blend of both.

Colour does not save you. Colour is the first thing lost to low light, backlight, night
interiors, distance and any grade the style guide imposes. **Distinction has to survive being
reduced to a flat black shape.**

The axes, the pass rule and the fixes that actually work are in
`references/silhouette-check.md`. Report every pair as `distinct`, `close` or `too close`, and
for anything not distinct, name the fix and which character should absorb the change. The
principal keeps their look. The smaller part changes.

Present stages 2 and 3 together and **stop**. The user reviews the descriptions, accepts or
rejects the collision fixes, and only then do you write prompts.

## Stage 4: reference prompts

Only after approval. 2 kinds, images first.

### Reference images

Ask for these views, per character, and say in the file what each is for rather than listing
them bare. The full explanation, plus the optional views and when they are worth the credits,
are in `references/reference-views.md`.

| view | what it settles |
|---|---|
| Front, neutral | The identity anchor, and the frame most image to video calls will start from |
| Three quarter | The volume of the head. Generators default to this angle, so a correct one stops them inventing it |
| Profile | Nose, chin, brow and ear placement, which a front view cannot pin down |
| Full body, standing, feet visible | Proportion, height, limb length, footwear, and the silhouette the distinction check uses |
| Expression range | 4 to 6 faces on 1 sheet, so a scene needing an emotion does not restyle the face to get it |
| In the story's setting | The character in the world's own location and light, which proves the wardrobe and palette survive it |

Every image prompt reuses the **same** description text, byte identical, and varies only the
view clause, the framing and the background. If the description changes between views, the
views will not agree with each other and the sheet is worthless.

Reference sheets want a plain background, even light and a neutral expression, apart from the
expression sheet and the in-setting view. Follow `<guide>/lighting.md` for the in-setting one,
and `<guide>/camera.md` `Applicability` before adding any optical language anywhere.

### Reference videos: 5 seconds, always

**Reference clips are short form only. 5 seconds. There is no long form option here** and you
should not offer one. 3 reasons, and say them if asked:

1. 5 seconds is the cheap unit. A cast of 9 with 3 clips each is 27 generations, and the
   duration is the multiplier on that bill.
2. A reference clip carries no story. It shows a turn, a walk or a look. None of those need
   longer, and padding the duration adds nothing to the reference.
3. Identity drift starts appearing **inside** a longer clip. A 12 second clip of a character
   often ends on a different face than it started with, which makes it useless as a reference.
   A 5 second clip does not have time to drift.

3 clips per character at most, and 1 is often enough:

| clip | 5 seconds of | when it is worth it |
|---|---|---|
| Turnaround | Locked camera, the character rotates in place, neutral pose | Always. It carries every angle in 1 asset |
| Walk | Full body, side on, the character walks at their own speed | When gait is part of the character, or they walk in the script |
| Look | Head and shoulders, 1 expression change, no dialogue | Dialogue heavy characters, and anything going to lip sync |

Write these as prompts a video generator takes, not as descriptions of clips. Name the camera
as locked unless the clip needs otherwise, name the subject motion, and carry the exclusion
clause. An unnamed camera drifts and an undescribed background fills itself in.

## Stage 5: write the files

Write to `<root>/gen-ai/characters/<slug>/` in the project, where `<slug>` is a short name for
the production. See `Where the files go` above, and never write to the shared location.

| file | contents |
|---|---|
| `<bible>/CHARACTERS.md` | The index. The cast with 1 paragraph each, and the distinction check |
| `<bible>/<character-id>.md` | 1 per character. The verbatim reusable description, plus that character's reference prompts |
| `<bible>/reference-prompts.md` | Every image prompt and every 5 second video prompt in 1 place, for batch running |
| `<bible>/audience.md` | The stage 0 answers verbatim, and what they forbid |
| `<bible>/manifest.json` | Machine readable: slug, source script, character ids, confidence per character, open questions, model used |

One file is written outside the bible directory: `<root>/gen-ai/README.md`, the index of what
this project contains. Add or update the one line for this bible under `## Characters`, and leave
every other section alone. The style guide owns `## Styles`, and `script-to-shots` owns
`## Shot sets`.

`<character-id>` is lowercase, hyphen separated, derived from the name, and **stable**. It is
the key in `<bible>/manifest.json`, the filename, and the string other skills use to ask for a
character. Renaming it later breaks every reference to it.

**Required headings for each file are in `references/output-files.md`.** Keep them exactly.
`video-prompt-engineer` reads these files by heading, so a renamed heading is a broken file,
not a stylistic choice.

## The verbatim rule

The single reason a character holds together across 40 separately generated shots is that the
**same words** describe them every time. Byte identical reuse. Not a paraphrase, not a tidier
version, not the same facts in a better sentence.

Paraphrasing is the main cause of drift. Every model reweights a rewritten clause differently,
so "a tall woman in an oversized grey wool coat" and "a woman, tall, wearing a large grey coat
of wool" produce 2 different people, and the sequence will not cut together.

Design the output for that:

- Each character file carries the description in a **fenced code block, and nothing else in the
  block**, so it can be copied whole with no editing decisions.
- 2 lengths. A **short form** under 25 words, for shot prompts where the budget is tight, since
  a single shot video prompt should stay under about 120 words in total. A **long form** of 60
  to 90 words, for reference generation and for shots where the character is the subject.
- The 2 forms must not disagree. The short form is a subset of the long form, not a rewrite of
  it.
- The description **never** contains a name. A generator does nothing useful with "Mira" and
  may pull an unrelated likeness from it. Names live in the heading, the description is
  physical.
- `descriptionVersion` in `<bible>/manifest.json` starts at 1 and increases whenever the text
  changes. Say in the file that shots generated before a bump will not match shots after it, so
  the honest options are to leave it alone or to regenerate the earlier scenes.

State this rule inside every character file, next to the block. The person pasting it 6 weeks
from now will not have read this skill.

## Stage 6: hand off

Report:

1. Where the files are, and the file list.
2. **The cast, with the 1 line distinction for each**, inline, so the user gets the value
   without opening anything.
3. **The distinction check result**, and any pair still marked close.
4. **What is thin**: characters marked inferred or unknown, and what 1 line of script would fix
   each.
5. The prompt count and, if you are generating, the cost before you spend it.

Offer 1 test render in the same turn: the front view of the character with the weakest
evidence. That is where a misread lands, and 1 image finds it faster than re-reading the
script.

## Working with the other skills

- **`style-guide-builder`** comes first when the look is not settled. It owns rendering,
  palette, lighting, camera and the construction rules. This skill owns who the characters are
  and how they differ. Where they overlap, `<guide>/audience.md` and `<guide>/palette.md` win.
- **`video-prompt-engineer`** reads `<bible>/manifest.json` for the cast and the confidence,
  then takes the description from `<bible>/<character-id>.md` verbatim into the shot prompt. It
  handles duration, camera movement, motion and exclusions. Point it at the slug.
- **`gen-ai-explainer`** can take the short forms straight into a scene plan.
- If the user wants a brand persona rather than a character from a script, that is
  `gen-ai-persona-creation`, not this.

## House rules

- Plain English. No em dashes, no en dashes, no double hyphens, no emoji, no smart quotes.
  Sentence case headings. Numbers as digits.
- No marketing voice and no adjectives that describe nothing. A character is 38 with a 3
  centimetre scar, not striking.
- Describe what is visible. `Left eyebrow split by a 2 centimetre scar` belongs in a bible.
  `Carries the weight of her father's death` does not, because no generator renders it.
- Never state a colour, height or age you have not either read in the script or proposed
  openly as a proposal.
- Do not build a bible for a copyrighted character from another production. Describe a
  character the user owns, and say plainly that an existing character is not theirs to reuse.
- Do not build a bible that reproduces an identifiable real person without saying that this is
  a permissions question, not a prompting one.
