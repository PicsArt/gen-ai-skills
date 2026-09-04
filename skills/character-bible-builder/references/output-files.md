# Output files

Required shape for each file written to `<root>/gen-ai/characters/<slug>/` in the project,
written below as `<bible>/`. **Keep the headings exactly as given.** Other skills read these files by
heading, notably `video-prompt-engineer`, which looks for `## Verbatim description` and takes
what is inside the fenced block under `### Short form` or `### Long form`. A renamed heading is
a broken file.

Within `## Verbatim description`, each rendering is headed `### Rendered against <style-slug>`,
because a description is only valid for the style it was written against. `## Identity` is style
independent and survives a restyle; the renderings under it do not.

Every claim carries its confidence in brackets: `[established]`, `[provisional]`, `[inferred]`,
`[unknown]`. A line with no bracket is not finished. The words mean what they mean in
`SKILL.md` stage 2, which is the same as in a style guide's `<guide>/extrapolation.md`, so a
reader moving between the 2 sets of files does not have to relearn them.

---

## `<bible>/CHARACTERS.md`

The index, and the only file some people will read. It has to stand alone.

```markdown
# <Production name> cast

<1 paragraph. What this cast is, how many characters, what the story is, in the terms someone
would use to describe it to a colleague.>

## The cast

### <Character name>

`<character-id>` | <tier> | <age> | <N> scenes | [<confidence>]

<1 paragraph, 60 to 90 words. Role in the story, then what you would see: build, face, hair,
wardrobe, posture. Ends with the 1 sentence that separates them from everyone else.>

<Repeat per character, principals first, then secondary, then background.>

## Groups and extras

<Any crowd, squad or class handled as a rule rather than as individuals, with the rule. Omit
the heading only if there are none.>

## Distinction check

| pair | verdict | why | fix |
|---|---|---|---|
| `mira-holt` and `dana-reyes` | too close | Same height band, same coat length, same hair mass | Reyes loses the coat for a short jacket, hair goes up |

<Then 1 paragraph: what still reads as close, and in which shot types it will show.>

## Scope

Source: <script name>. <N> characters, <N> confirmed by the user on <date>.
Audience: <from `<bible>/audience.md`>. Style guide: <slug, or none>.
Model: <model>.

## Confidence

| character | confidence | why |
|---|---|---|
| `mira-holt` | established | Described in 3 action lines |
| `barista` | inferred | 1 line of dialogue, no description, designed by proposal |

## Files

<1 line per file, with what a reader would open it for.>
```

The per character paragraphs are the deliverable of this file. Someone reading only
`<bible>/CHARACTERS.md` should be able to tell the cast apart.

---

## `<bible>/<character-id>.md`

1 per character. Headings in this order, all required except where marked.

```markdown
# <Character name>

`<character-id>` | <tier> | description version <N>

## Identity

- Role in the story: <what they do, who they are to the others> [confidence]
- Age: <a number or a 5 year band> [confidence]
- Scenes: <count, and which>
- Real person basis: <none, or the cleared statement from `<bible>/audience.md`>

Style independent. Everything under this heading survives a restyle and is written without
reference to how anything is drawn. Never put an outline colour, a shading step count or an eye
construction here: those belong to the style, not to the person.

## Verbatim description

Headed with the style it was written against, as `### Rendered against <style-slug>`, or
`### Rendered against no style guide` when none existed. A description is only valid for the
style it was written against, so a restyled production regenerates these and leaves
`## Identity` untouched.

**Reuse this text byte identical in every prompt. Do not paraphrase it, do not tidy it, do not
translate it into your own words. A rewritten description produces a different person, and the
shots will not cut together. If it has to change, change it here, raise the description version
in `<bible>/manifest.json`, and accept that shots made before the change will not match shots
made after it.**

### Short form

<1 fenced code block. Under 25 words. Nothing else inside the block. For shot prompts where the
word budget is tight.>

### Long form

<1 fenced code block. 60 to 90 words. Nothing else inside the block. For reference generation
and for any shot where this character is the subject. The short form must be a subset of this,
not a rewrite of it.>

Neither block contains the character's name, a scene, an emotion or an action. Those belong in
the shot prompt.

## Build

<Height relative to the rest of the cast in centimetres, mass, shoulder line, how they carry
weight, hands.> [confidence]

## Face

<Head shape, brow, eyes with colour and shape, nose, mouth, jaw, skin tone in plain physical
terms, marks and scars with size and position, facial hair.> [confidence]

## Hair

<Length in centimetres, mass, texture, colour, how it is worn, hairline.> [confidence]

## Wardrobe

<The default outfit worn in most scenes, in garment terms, with fabric, fit and condition. Then
any named variant, each as its own bullet with the scenes it belongs to.> [confidence]

## Palette

| colour | hex | role |
|---|---|---|

<Roles are things like coat, skin, hair, accent. When a style guide exists, reference the roles
in `<guide>/palette.md` rather than inventing hex, and say which colour came from
`<guide>/palette.md` rules rather than from the script.>

## Posture and movement

<Resting stance, gait, speed, gesture habits, what the hands do. The stance is what makes them
recognisable at 20 metres, so it goes first.> [confidence]

## Distinction

<The 2 or 3 things that separate this character from every other character in the cast, at
least 1 of which survives being reduced to a flat black shape. Name the characters they are
closest to.>

## Reference images

Per view: what it is for, then the prompt in a fenced block.

### Front, neutral
### Three quarter
### Profile
### Full body
### Expression range
### In the story's setting

<Optional views go after these, each under its own heading: Back, Hands, Wardrobe variant.>

## Reference videos

5 seconds each. No long form clips.

### Turnaround
### Walk
### Look

<Include only the clips this character needs. Under each, 1 line on what it is for and the
prompt in a fenced block.>

## Never

<Bulleted. What must not appear on this character, merged from `<bible>/audience.md` and, when a
style guide exists, `<guide>/negatives.md`. Each with its reason.>

## Confidence

| aspect | confidence | basis |
|---|---|---|
| age | established | scene 1 action line |
| hair | inferred | script silent, proposed and approved on <date> |

## Open questions

<What the script did not settle, phrased as a question the user can answer in 1 line. Omit the
heading if there are none.>
```

`## Identity`, `## Verbatim description` and the 2 form subheadings under it are the contract
with every other skill. If you change nothing else, keep those 4 and keep the fenced blocks
clean.

The split between the first 2 is the one to hold. `## Identity` is who the character is and
survives a restyle. `## Verbatim description` is how they are drawn in one particular style, which
is why each rendering under it is headed `### Rendered against <style-slug>`, and why a restyled
production regenerates those and leaves `## Identity` untouched.

---

## `<bible>/reference-prompts.md`

Every prompt in the bible, collected for batch running. This file duplicates what is in the
character files on purpose: 1 file to hand to a script or an operator, so nobody has to open 9
files and copy 54 blocks out of them.

```markdown
# Reference prompts

## How to run these

<1 short paragraph: the model chosen in stage 0, the route, and the flag or call that runs
these. Say the image prompts come first, because the front view of each character is the start
frame for that character's clips.>

Total: <N> image prompts and <N> video prompts across <N> characters. Every video prompt is 5
seconds.

## Shared clauses

<The style, medium and exclusion clauses that every prompt below repeats byte identical. Each a
complete clause ending in a full stop, so it can be pasted unedited. When a style guide exists,
these come from `<guide>/fragments.md` verbatim.>

## Image prompts

### <character-id>

#### Front, neutral

<Fenced block. The whole prompt, ready to run, with the description and the shared clauses
already inside it. Not a template with placeholders.>

<Repeat per view, then per character.>

## Video prompts

### <character-id>

#### Turnaround, 5 seconds

<Fenced block. Whole prompt. Names the camera, the subject motion and the exclusions.>

<Repeat per clip, then per character.>

## Running order

1. <Which prompts to run first, and what to check before spending the rest.>

## What to check before running the rest

<3 or 4 checks against the first character's sheet: does the face match across the 3 angles,
does the height read correctly against the stated band, is the wardrobe the one described, does
the silhouette differ from the character it was closest to.>
```

Prompts here are complete and runnable. A placeholder left in this file becomes a generation
with the word `<character>` rendered into the image.

---

## `<bible>/audience.md`

The stage 0 answers **verbatim**, then what they forbid.

```markdown
# Audience and content rules

- Making: <answer>
- Audience and age rating: <answer>
- Never appears: <answer>
- Real person basis: <answer, verbatim, including any statement that rights are cleared>
- Asked on: <date>

## What this forbids

<Concrete consequences: wardrobe limits, expression limits, what a wound or a weapon may look
like, what has to appear in the exclusion clause of every prompt in
`<bible>/reference-prompts.md`.>

## Real people

<Per character with a real person basis: cleared or not cleared, what was recorded, and what
was done instead. If nothing here, write that no character is based on a real person.>

## Precedence

This file outranks every other file in this bible, including any description and any reference
prompt. Where a style guide exists, `<guide>/audience.md` outranks this file, and any conflict
between the 2 goes back to the user rather than being resolved here.
```

---

## `<bible>/manifest.json`

```json
{
  "slug": "...",
  "name": "...",
  "project": "...",
  "origin": "project",
  "createdAt": "...",
  "sourceScript": {"name": "...", "kind": "screenplay", "scenes": 0, "episodes": 0},
  "styleGuide": {"slug": "...", "path": "gen-ai/style/<slug>/", "origin": "project"},
  "model": "...",
  "audience": {
    "making": "...",
    "audience": "...",
    "ageRating": "...",
    "neverAppears": ["..."],
    "realPersonBasis": "none"
  },
  "characters": [
    {
      "id": "mira-holt",
      "name": "MIRA HOLT",
      "tier": "principal",
      "file": "mira-holt.md",
      "descriptionVersion": 1,
      "confidence": "established",
      "scenes": 12,
      "closestTo": ["dana-reyes"],
      "realPerson": null,
      "openQuestions": ["..."]
    }
  ],
  "groups": [{"id": "market-crowd", "rule": "...", "confidence": "inferred"}],
  "distinctionCheck": [
    {"pair": ["mira-holt", "dana-reyes"], "verdict": "distinct", "why": "...", "fix": "..."}
  ],
  "promptCounts": {"images": 0, "videos": 0, "videoSeconds": 5},
  "files": ["CHARACTERS.md", "mira-holt.md", "reference-prompts.md", "audience.md"],
  "openQuestions": ["..."]
}
```

`styleGuide` is `null` when there is none. Its `path` is relative to the project root when the
guide is in the project, and the full `~/.gen-ai/projects/style/<slug>/` path when `origin` is
`shared`. A relative path is what makes the project folder movable and shareable; an absolute one
breaks the moment somebody else opens it.

`confidence` per character and `openQuestions` are what another skill reads to decide whether to
trust a description or ask the user, so fill them honestly. `videoSeconds` is always 5.

`project` is the project folder's name, and `origin` is `project` for a bible built here or
`shared` for one copied in from `~/.gen-ai/projects/characters/`. Both exist so a directory
copied out of its project still says which production it came from.

`descriptionVersion` is the field that makes drift traceable. When a description changes, raise
it, and record in `<bible>/CHARACTERS.md` which scenes were generated against which version.
Without it, a cast that stopped matching gives nobody a way to find out when.

---

## The project index

Not inside the bible directory. `<root>/gen-ai/README.md` is shared with the other skills, and
each owns one section. Create the file if it is missing, add or update **only** the line for this
bible under `## Characters`, and change nothing else.

```markdown
## Characters

- `characters/orchard-tales/`: 4 characters: pip, mrs-holloway, the-fox, gran. Rendered against `saturday-cartoon`. 2026-08-14
```

The character ids matter more than the count, because an id is what another skill asks for. Name
the style the descriptions were rendered against, since that is what tells a reader months later
whether the bible still matches the look.

If a `README.md` already exists in `<root>/gen-ai/` and is not this index, do not overwrite it.
Write `GEN-AI.md` alongside it instead and say so.
