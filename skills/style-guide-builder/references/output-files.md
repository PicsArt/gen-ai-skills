# Output files

Required shape for each file written to `<root>/gen-ai/style/<slug>/` in the project. Keep the
headings exactly as given: other skills read these files, and a renamed heading breaks them.

Every rule carries its evidence in brackets: `[11/12 frames]`, `[2 frames, provisional]`,
`[inferred, no example]`. A rule with no bracket is not finished.

---

## STYLE.md

The index, and the only file some people will read. It has to stand alone.

```markdown
# <Style name>

<One paragraph. What this looks like, in the terms someone would use to describe it to a
colleague. No lists, no hedging.>

## The ten rules that matter

1. <Rule> [evidence]
...

## Scope

Built from <N> references. Intended for <what the user said in stage 0>.
Audience: <from audience.md>. Model used for analysis: <model>.

## Confidence

| aspect | confidence | why |
|---|---|---|
| palette | established | 12 of 12 frames agree |
| motion | unknown | references are stills |

## Files

<links with one line each>
```

The ten rules are the deliverable. Write them so that a person following only those ten gets
something recognisably in-style.

---

## palette.md

```markdown
# Palette

## Observed colours

| swatch | hex | role | where |
|---|---|---|---|
| ... | #RRGGBB | key light / skin / foliage / accent | which references |

## Relationships

- Hue count and spacing
- Saturation range, as a band
- Value range, and whether true black or white appear
- Shadow construction
- Highlight construction
- Warm or cool bias

## Choosing a colour that is not here

<A paragraph written as an instruction. Must be followable without seeing the references.
See SKILL.md stage 5 for the standard this has to meet.>

## Accents

<Any colour reserved for emphasis, and what earns it.>
```

Ranges, never averages. The average of a two-colour palette is a colour that appears nowhere.

---

## rendering.md

Headings: `Medium`, `Line`, `Fill and shading`, `Texture`, `Detail density`, `Edges`.

State the outline colour explicitly. Assuming black when the references use dark brown is the
most common single error in style transfer, and it is visible immediately.

---

## lighting.md

Headings: `Default setup`, `Shadows`, `Highlights`, `Variants`, `Motivation`.

Under `Variants`, name each lighting state the references show, with how many frames support
it. Do not merge them into one description.

---

## camera.md

Headings: `Shot sizes`, `Angles`, `Perspective`, `Depth of field`, `Framing habits`,
`Applicability`.

`Applicability` is required and often reads: *this style is flat illustration with no
photographic cues, so lens and depth of field language does not apply and should not appear in
prompts.* Saying that is more useful than a made-up focal length.

---

## characters.md

Per subject:

```markdown
## <Name or class>

- Proportion, features, eye construction, hands, hair or fur, clothing
- Palette, referencing palette.md roles rather than repeating hex
- Outline and shading treatment

### Construction rules

<The generalisable rules this subject reveals, written so a subject that never appears can be
built from them. See extrapolation.md.>
```

Then a final section:

```markdown
## Building a new subject

<The rules that apply to any subject of this class, ordered so someone can follow them.>
```

---

## environments.md

Headings: `Settings`, `Foliage`, `Ground and grass`, `Sky and weather`, `Water`,
`Architecture`, `Crowds and background figures`, `Props`, `Depth`.

Each says what the references show **and** the rule it implies. `Foliage` is the one to get
right: it generalises to grass, bushes, crops and hedges, which is most of any outdoor frame.

---

## motion.md

Only when references are sequential or from footage. Headings: `Animation character`,
`Motion blur`, `Camera movement`, `Pacing`.

When references are stills, write the file with one line: *references are stills, so motion is
unknown. Do not infer it.* An empty file reads as an oversight; a stated absence does not.

---

## typography.md

Only when text appears in the references. Headings: `Typefaces`, `Weight and case`,
`Placement`, `Colour`, `Effects`.

Add: *generators set type unreliably. Prefer generating without text and setting it afterwards.*

---

## negatives.md

```markdown
# Off style

## Exclusions

<One sentence beginning with No, listing what would break this style.>

## Phrase positively instead

| instead of | write |
|---|---|
| no harsh shadows | soft shadows with a wide penumbra |

## Never in this style

<Bulleted, with the reference-based reason for each.>
```

Many models expose no negative field, so a ban can act as a mention. Anything that is a
physical part of a scene goes in the positive table, not the exclusion sentence.

---

## audience.md

The stage 0 answers **verbatim**, then what they forbid.

```markdown
# Audience and content rules

- Making: <answer>
- Audience: <answer>
- Never appears: <answer>
- Asked on: <date>

## What this forbids

<Concrete consequences: palette limits, expression limits, subject limits, exclusions that
must appear in every prompt.>
```

This file outranks every other file, including extrapolation. Say so in it.

---

## product.md

Only for commercial references. Product facts, kept apart from style rules, because a style
rule generalises and a product fact must not.

```markdown
# Product facts

## Geometry
<Shape, proportion, closures, materials. What must be preserved exactly.>

## Markings
<Logo placement, label typography, badge shapes, pattern repeats. Note that generators degrade
fine lettering and that these are better composited afterwards than generated.>

## Colour
<Exact product colours, separate from the palette. These are not open to the palette rule.>

## Must not change
<The list a prompt inherits as exclusions.>
```

Never let a rule in this file be used to derive a new product. It records one object.

## extrapolation.md

Follows `references/extrapolation.md` in this skill. Must contain: the construction rules per
class, at least two worked derivation chains using the actual references, and a confidence
label on every rule.

---

## fragments.md

Ready-to-paste clauses, grouped by aspect, in the order a prompt uses them. Each is a complete
clause ending in a full stop, so it can be dropped into a prompt unedited.

```markdown
# Prompt fragments

## Style and medium
- `Flat two-tone cel shaded cartoon, dark brown outlines of even weight.`

## Palette
- `Muted pastel palette, saturation held between 30 and 45 percent.`
```

Close with a **full worked prompt** for one reference image, so the user can see the fragments
assembled and judge whether the guide reproduces what they gave you.

---

## manifest.json

```json
{
  "slug": "...",
  "name": "...",
  "project": "...",
  "origin": "project",
  "createdAt": "...",
  "referenceCount": 0,
  "referencesExcluded": [{"file": "...", "why": "..."}],
  "analysisModel": "...",
  "audience": {"making": "...", "audience": "...", "neverAppears": ["..."]},
  "files": ["STYLE.md", "..."],
  "confidence": {"palette": "established", "motion": "unknown"},
  "openQuestions": ["..."]
}
```

`confidence` and `openQuestions` are what another skill reads to decide whether to trust an
aspect or ask the user. Fill them honestly; they are the machine readable version of admitting
what the references did not show.

`project` is the project folder's name, and `origin` is `project` for a style built here or
`shared` for one copied in from `~/.gen-ai/projects/style/`. With `origin: shared`, add
`"vendoredFrom"` and `"vendoredAt"`. Both fields exist so that a directory copied out of its
project still says where it came from. A style guide that has lost that is a folder of rules
with no idea what they were for.

---

## The project index

Not inside the style directory. `<root>/gen-ai/README.md` is shared with the other skills, and
each owns one section of it. Create the file if it is missing, add or update **only** the line
for this style, and change nothing else.

```markdown
# gen-ai files for <project name>

Styles, characters and shot lists for this production. Built by the gen-ai skills.

## Styles

- `style/saturday-cartoon/`: flat cel shaded, dark brown outlines, pastel palette. 12 references. 2026-08-14
```

One line: the path, a colon, the same look description as the first line of `STYLE.md`
compressed to a clause, the reference count, and the date. Someone opening this file in a year
should be able to tell which style this project uses without opening anything else.

If a `README.md` already exists in `<root>/gen-ai/` and is not this index, do not overwrite it.
Write `GEN-AI.md` alongside it instead and say so.
