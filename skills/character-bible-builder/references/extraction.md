# Extracting the cast

How to find every character in a script, and how to read appearance out of a document that was
not written to describe appearance.

The output of this file is the list you present at the end of stage 1. You do not act on it
until the user has confirmed it. Rule one in `SKILL.md` has no exceptions.

## Read the whole thing first

Do not list as you go. A character introduced in scene 2 as `A WOMAN` and named in scene 9 is 1
character, and you can only see that from the far end. Reading and listing at the same time
produces duplicates and misses aliases.

If the script is long, work in passes: 1 pass for dialogue cues, 1 for action lines, 1 for
mentions inside dialogue. Merge afterwards.

## Where characters hide

| where | what it looks like | what people miss |
|---|---|---|
| Dialogue cues | A name in capitals above a speech | Nothing. This is the easy list, and it is not the whole list |
| Introductions in action lines | `MIRA HOLT, 38, steps out of the rain` | Screenplay convention capitalises a character on first appearance only. Later mentions are lowercase |
| Unnamed functional parts | `A BARISTA hands her a cup` | These get generated fresh every time and are the worst drifters, because nothing describes them |
| Mentions inside dialogue | "Tell Reyes I said no" | Reyes may never appear, or may appear 4 scenes later under another name |
| Numbered parts | `GUARD 1`, `GUARD 2` | Whether they are 2 characters or 1 character in 2 scenes. Ask |
| Voice only | `(V.O.)`, `(O.S.)`, radio, phone, narrator | A voice may still need a body later, and may not. Ask |
| Groups | `a crowd`, `the squad`, `commuters` | Handled as a rule, not as individuals. See below |
| Non-human | Animals, robots, creatures, vehicles with a personality | They need the same treatment and are often left out of the cast list |
| Younger or older versions | `MIRA, 12`, `OLD MIRA` | The same person and a separate bible entry, because they do not share a silhouette |
| Doubles and disguises | A character dressed as another, twins, a mask | 2 entries with a shared face rule, or 1 entry with 2 wardrobe variants. Ask which |

## Aliases

The same person under 2 labels is the most common extraction error, and it is expensive: you
write 2 bibles, generate 2 faces, and the drift you were hired to prevent is now in the source
material.

Flag as a possible alias when any of these hold:

- 1 label is a first name and the other is a title plus surname.
- 2 labels never appear in the same scene.
- 1 label has a description and the other has only dialogue cues.
- A nickname appears in dialogue and a formal name appears in cues.

Never merge them yourself. Present them as separate rows with `possible alias of N` in the tier
column, and ask.

## Tiers

Tier decides how much work each character gets, not how important they are to the story.

| tier | test | gets |
|---|---|---|
| Principal | Carries scenes, appears in more than 1 scene, has a face the audience learns | A full file, all 6 image views, up to 3 clips |
| Secondary | Named or described, appears in 1 to 3 scenes, seen clearly | A full file, front and full body and 1 more view, 1 turnaround clip |
| Background | Functional, 1 scene, no description, or seen at distance | 1 paragraph in `<bible>/CHARACTERS.md` and 1 front view. No clips |
| Group | A crowd, squad or class treated as a set | A rule, not files. See below |
| Voice only | No body in the script | 1 line saying so, and no prompts until the user says a body is needed |

Propose a tier per character and let the user move them. A background character the user cares
about becomes secondary the moment they say so, and that is cheaper to hear now than after the
sheets exist.

## Groups and extras

9 extras do not need 9 files. They need 1 rule that makes them belong to the same world and
differ from each other enough not to look cloned:

> Market crowd: adults 20 to 60, working clothes in the palette's muted band, no character in
> the principals' 3 accent colours, no headwear, faces not resolved beyond the second row.
> Generate 4 variants and reuse them.

Record the rule in `<bible>/CHARACTERS.md` under `## Groups and extras` and in
`<bible>/manifest.json` under `groups`. The 2 things a group rule must state are the ceiling on
detail and the ban on the principals' distinguishing features, because an extra wearing the
hero's coat is the fastest way to confuse a generator in a wide shot.

## Reading appearance out of a script

A script tells you far less than a bible needs. Sort what you find into 3 buckets and keep them
apart, because presenting a proposal as a reading is how a user approves something they never
asked for.

| bucket | source | how to present it |
|---|---|---|
| In the script | Stated in an action line, a cue or dialogue | Quote it. `"coat too big for her"` [established] |
| Implied by the script | The job, the setting, the period, the weather, what other characters say | Say what you inferred it from. `Outdoor work in winter, so layers and boots` [provisional] |
| Proposed by you | The script is silent | Say plainly that you are proposing it, and offer 1 alternative [inferred] |

Sources of implication that are usually reliable:

- **The job.** A uniform, a tool belt, hands in condition, footwear.
- **The period and place.** Settles fabric, cut, hair, glasses, whether a watch exists.
- **The weather and the season.** Settles layers, and layers dominate a silhouette.
- **What other characters say about them.** Dialogue about someone's appearance is the script
  describing them without an action line.
- **Their economic position.** Condition and fit of clothing, not brand.
- **Age relative to other characters.** Often stated as a relationship rather than a number.
  A parent of a 12 year old is 30 to 45 unless the script says otherwise.

Sources that are not reliable and should be marked inferred at best:

- A character's name. It tells you nothing about their face, and reaching for an appearance from
  a name is how a cast ends up stereotyped.
- Their moral position in the story. Villains do not have a look.
- What the user has in mind and has not said. Ask instead.

## What to ask when the script is thin

An outline or a treatment may name 6 characters and describe none. That is normal, and it is not
a reason to invent 6 people quietly. Ask for the 4 facts that carry the most:

1. Age, as a number or a 5 year band.
2. Height, relative to the other characters rather than absolute.
3. The 1 thing about them a viewer should notice first.
4. The default outfit, or permission for you to propose it.

Those 4 settle most of a silhouette. Everything else can be proposed and corrected at the stage
3 stop, which is cheaper than correcting it after a sheet has been generated.
