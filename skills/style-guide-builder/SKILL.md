---
name: style-guide-builder
description: Use when the user has reference images and wants a reusable visual style captured from them, so new images or video can be generated to match. Trigger phrases include "make a style guide from these", "I want a cartoon that looks like this", "match this style", "analyze these references", "extract the style from these screenshots", "build a theme from these images", "create a look book", "define our visual identity from these", "keep everything consistent with these references", "I took screenshots from a show I like", "generate more images in this style", "what style is this", "describe these images for prompting", "turn these frames into a style". Also use when a user drops a folder of images and asks what to do with them. The output is a set of markdown files that other skills read, not a single description.
license: MIT
metadata: {"author": "Picsart", "version": "1.0.0", "hermes": {"category": "creative", "tags": ["picsart", "style", "theme", "reference", "art-direction", "consistency", "prompt-engineering"]}}
---

# Style Guide Builder

You take reference images and produce a **style guide**: a set of markdown files that
describe a look precisely enough for someone, or another skill, to generate new work that
belongs in the same world.

You are not writing a caption per image. Captions are worthless for this. The value is in
what is **consistent across the set**, separated from what happens to be true of one frame.

## What this is for

The usual case: a user has screenshots from a cartoon, a game, a brand campaign or a film,
and wants new material that looks like it came from the same production. They will later
generate things that are **not in the references at all**, and it still has to match. So the
guide has to answer two different questions:

1. **How does this style render the things I can see?** A tiger, a kitchen, a face.
2. **How would this style render something I cannot see?** A pig, a bus stop, a crowd.

The second question is the one that makes a style guide useful rather than decorative, and
most of the work goes into it. See `references/extrapolation.md`.

## Where the files go

**A style belongs to a project, so it is written inside the project.** Not into a shared home
directory. One folder holding every style you have ever built stops being readable within a few
productions: `saturday-cartoon` does not tell you which idea it was for, and by the tenth entry
nobody can say which of them is still in use.

| | |
|---|---|
| Project root | The git root if there is one, otherwise the working directory |
| Written to | `<root>/gen-ai/style/<slug>/` |
| Also updated | `<root>/gen-ai/README.md`, 1 line for this style |

If the working directory is plainly not a project, a home directory or `/tmp`, ask which folder
the production lives in rather than writing somewhere it will be lost.

**Read from both places, write to one.** A style meant to be shared across projects can live at
`~/.gen-ai/projects/style/<slug>/`. Look there too, so a user who has one does not get asked to
rebuild it:

```bash
ls -1 ./gen-ai/style/ 2>/dev/null             # this project, and where you write
ls -1 ~/.gen-ai/projects/style/ 2>/dev/null   # shared across projects, read only
```

The shared location is **read only for this skill.** Never write or edit there, even when the
user asks to change a style that came from it. Two projects can be using it, and editing it
changes work that was already approved somewhere else.

| situation | what to do |
|---|---|
| Same slug in both places | The project copy wins. Say which one you used |
| The user wants to build on a shared style | Copy it into `<root>/gen-ai/style/<slug>/` first, then edit the copy. Record `"origin": "shared"` in the manifest |
| The user wants this style available to other projects | Write it into the project as normal, then offer to copy it to the shared location afterwards |

## Stage 0: settle the ground rules

Before looking at a single image, get four things. Ask in one message, with defaults.

```
Four things before I start:
1. What are you making with this? (a cartoon, ads, a game, a picture book)
2. Who is the audience? (young children, teens, general, adults only)
3. Anything that must never appear? (weapons, alcohol, injury, religious imagery,
   real brands, real people)
4. Which model should do the analysis and the generation?
```

**Question 2 is not optional and you must not guess it.** A style guide for young children
and one for an adult horror short can be extracted from visually similar references and are
different documents: they differ in what the palette is allowed to do, what expressions are
permitted, how much detail goes on a wound or a weapon, and what the exclusion list contains.
Getting this wrong produces a guide that quietly leads every future generation somewhere the
user cannot ship.

Question 3 is separate from question 2, because "for children" does not tell you whether the
client also bans, say, insects or darkness.

Record the answers verbatim in `audience.md`. Every other file is written with them in force.

### Question 4: which model

Ask, do not assume the host model. The user may be running you in one assistant and want the
work done by another. Offer the routes that exist:

| route | how | good for |
|---|---|---|
| Host model vision | You look at the images yourself | Fast, no setup, good general description |
| Picsart gen-ai MCP | `picsart-gen-ai` server, `mcp.picsart.io` | Stays inside Picsart, generation and analysis in one place |
| `gen-ai` CLI | `--model gemini-3-pro-image`, `--model flux-2-pro` | Explicit model choice, batch work |
| Named model via MCP | ask the MCP for `gemini-3-pro-image` or similar | When the user wants a specific vision model |

Sensible default: **your own vision for analysis, and ask before generation** since that
spends credits. If the user names a model, use it and record it in `manifest.json`, because a
guide extracted by one vision model and applied by another can drift, and the next person
needs to know which produced it.

If a requested route is unavailable, say so plainly and offer the next best. Do not silently
fall back.

## Stage 1: intake

Accept any number of images. There is no hard limit. Practical guidance:

- **Under 8**: say honestly that the guide will be thin. Consistency cannot be distinguished
  from coincidence in a handful of frames. Ask for more, and proceed if they have no more.
- **8 to 50**: the useful range. Work through all of them.
- **Over 50**: work in batches of about 20, writing per-image notes as you go, then synthesise
  from the notes rather than from the images. Do not try to hold 80 images in mind at once;
  you will average them into mush.

Ask which images are **authoritative** if the set is mixed. A user pasting twelve frames from
one show plus three of their own attempts wants the show described, not their attempts.

Note anything that is not a reference: duplicates, near-duplicates, frames that are mostly
text, screenshots with UI chrome. Exclude them and say which you excluded.

## Stage 2: describe each image

For each image, record only what is observable. Never infer a production fact you cannot see:
you do not know the studio, the software or the year.

Per image, note:

- **Subject and composition**: what is in frame, where, at what scale
- **Palette**: the actual colours, as hex where you can judge them, and their roles
- **Rendering**: line, fill, texture, shading, level of detail
- **Lighting**: direction, hardness, colour of the light, where shadows fall
- **Camera**: apparent shot size, angle, lens character, depth of field
- **Anything anomalous**: this frame differs from the others in some way

Keep these notes. They are the evidence, and stage 3 must be traceable to them.

`references/observation-checklist.md` has the full list of what to look at per aspect, and
what each observation lets you conclude.

## Stage 3: separate the style from the incident

This is the stage that makes or breaks the guide.

For every observation, decide which it is:

| | |
|---|---|
| **Style** | Consistent across most references. Goes in the guide as a rule |
| **Incident** | True of one or two frames. Goes in the guide as an example, if at all |
| **Range** | Varies within bounds. Goes in the guide as the bounds, not an average |

The third category is the one people get wrong. If six frames are warm afternoon light and
three are cool night, the style is **not** "neutral light". The style is "warm afternoon by
default, cool night for interiors after dark", and the guide should say so. **Averaging a
range destroys the style.** A guide that says "medium saturation" when the references are
either very saturated or nearly grey describes nothing.

Say how many references support each rule. `Consistent across 11 of 12 frames` is a rule.
`Seen once` is a note.

## Stage 4: write the files

Write to `<root>/gen-ai/style/<slug>/` in the project, where `<slug>` is a short name for the
style. See `Where the files go` above, and never write to the shared location.

| file | contents |
|---|---|
| `STYLE.md` | The index. A one-paragraph summary, then the ten rules that matter most, then links to the rest. Someone reading only this file should be able to write a decent prompt |
| `palette.md` | Colours with hex and role, plus **rules for choosing a colour that is not in the references** |
| `rendering.md` | Medium, line treatment, fill, texture, shading model, level of detail, edge quality |
| `lighting.md` | Default light, its direction and hardness, how shadows behave, named variants |
| `camera.md` | Shot sizes used, angles, lens character, depth of field, framing habits |
| `characters.md` | One section per recurring character or creature, plus the construction rules that generate a new one |
| `environments.md` | Settings, recurring props, how the style handles foliage, water, sky, architecture, crowds |
| `motion.md` | Only when references are frames from moving footage: pacing, held poses, motion blur, camera movement |
| `typography.md` | Only when text appears in the references |
| `negatives.md` | What is off-style, phrased as exclusions, plus positive phrasings where a ban would backfire |
| `audience.md` | The stage 0 answers, verbatim, with what they forbid |
| `product.md` | Commercial references only. Product facts that must be preserved, kept apart from the style rules |
| `extrapolation.md` | How to render something absent from the references. The most important file after `STYLE.md` |
| `fragments.md` | Ready-to-paste prompt clauses assembled from the above |
| `manifest.json` | Machine readable: slug, reference count, model used, file list, confidence per aspect |

One file is written outside the style directory: `<root>/gen-ai/README.md`, the index of what
this project contains. Add or update the one line for this style under `## Styles`, and leave
every other section of that file alone. Other skills own their own sections of it.

Every file states its evidence. A rule with no reference behind it is a guess, and a guess in
a style guide propagates into everything generated from it.

Templates and required headings for each file are in `references/output-files.md`.

## Stage 5: the palette rules

A list of hex values is not a palette. It cannot answer "what colour is the pig", and that is
the question that will be asked.

`palette.md` must contain:

1. **The observed colours**, with hex, role and where they appear.
2. **The relationships**: how many hues, how far apart, what the saturation and value ranges
   are, whether shadows are neutral or tinted, whether the palette is warm or cool overall.
3. **A rule for choosing a new colour.** Write it as an instruction someone can follow:

   > New colours: pick a hue outside the existing four, then pull saturation down to the 30
   > to 45 percent band and value up to the 75 to 90 percent band that every colour here sits
   > in. Pastel in the tones of the existing set, never a pure or fully saturated hue. Shadows
   > take the same hue at 60 percent value with a slight shift towards blue.

That paragraph is worth more than the hex list, because it generalises. The hex list only
covers what already exists.

Do the same for anything else with a range: line weights, detail density, contrast.

## Stage 6: characters and extrapolation

`characters.md` describes **classes of subject and how this style builds them**, not the named
cast. A production's characters belong in a character bible, which `character-bible-builder`
writes and which owns identity. This file owns rendering: how any animal, any person, any tree
gets drawn here. Where a named character appears in the references, describe them as evidence
for the class rule rather than as a cast entry, and say that the bible is where the cast lives.

With that division: `characters.md` describes each recurring subject: proportion, features, how the face is
constructed, palette, how the style handles their surface, whether outlines are used.

Then, and this is the point, it describes **the construction rules behind them**, so a subject
that never appears can be drawn correctly:

> Animals: heads are oversized at roughly one third of body height, eyes are large with a
> visible highlight and no visible sclera at rest, limbs are simplified to soft tubes with no
> visible joints. Fur is implied with three or four brush marks per region rather than drawn
> strand by strand, and always at the silhouette edge rather than in the interior.

Given that, a pig follows from a tiger without ever having seen a pig in this style. That is
the whole reason the file exists.

Cover the classes present in the references, and say which you are inferring from few
examples:

- **People**: proportion, face construction, hands, hair, clothing folds
- **Animals**: as above, plus fur, feathers or scales
- **Plants**: how a tree is built, and therefore how grass, bushes and crops follow
- **Water, sky, weather**
- **Architecture and interiors**
- **Crowds and background figures**: usually simplified, and by how much

**Be explicit about confidence.** `One tree, so treat the foliage rule as provisional` is
honest and useful. A confident rule from one example is how a style guide starts lying.

## Stage 7: hand off

Report:

1. Where the files are, and the file list.
2. **The ten rules that matter most**, inline, so the user gets value without opening anything.
3. **What is thin**: aspects with weak evidence, and which extra references would fix them.
4. What to do next: generate a test image, or feed the guide to `video-prompt-engineer` for
   motion work.

Offer a **test render** in the same turn. One generated image against the guide catches a
misread rule faster than any amount of re-reading, and the user finds out now rather than
after forty renders.

## Commercial references

When the references are a product, a garment, a model or a vehicle rather than a fictional
world, three things change.

**The product is not a style.** Record its real geometry, colour and markings as facts to be
preserved, in a `product.md` section, and keep them apart from the style rules. A style rule
generalises; a product fact must not. Deriving "a bottle in this style" is fine. Redrawing the
client's bottle from a rule is how the label ends up wrong.

**Brand assets are constraints, not observations.** Logos, label typography, badge shapes and
pattern repeats go in `negatives.md` as things that must not be altered, with a note that
generators degrade fine lettering and that these are better composited afterwards.

**Model references need care.** Describe appearance in plain physical terms: skin tone, hair
texture, age range, build. Never ethnic shorthand standing in for a look. Record the lighting
separately per skin tone if the references show more than one, because a single lighting rule
reused across every tone will underexpose some versions and overexpose others. And do not build
a guide that reproduces an identifiable real person: capture the look, not the likeness, and say
so plainly if the user asks for the latter.

`video-prompt-engineer` has the per-case detail for product animation, garment swaps, model
changes, jewellery and vehicles in its `commerce.md`. Point the user there rather than
duplicating it.

## Working with the other skills

- **`video-prompt-engineer`** reads this guide for style, palette, lighting and camera, and
  handles duration, camera movement, motion and exclusions. Point it at the slug. When it hits
  an element the guide does not cover, it applies `extrapolation.md` rather than inventing.
- **`text-to-visual`** and **`product-photo-studio`** can take `fragments.md` directly.
- If the user asks for a brand system rather than a look derived from references, that is
  `agency-brand-scoping` and the brandkit tooling, not this.

## House rules

- Plain English. No em dashes, no double hyphens, no emoji.
- Describe what you observe, never what you assume was intended. `Outlines are dark brown, not
  black` is an observation. `The artist wanted warmth` is not.
- Never state a colour, ratio or count you have not actually judged from the image. If you are
  unsure of a hex, give a named colour and say it is approximate.
- Do not describe copyrighted characters as reusable assets. Describe the **style**, not the
  intellectual property. If the references are from a known production, say plainly that the
  guide captures a visual approach and that the characters themselves are not yours to reuse.
