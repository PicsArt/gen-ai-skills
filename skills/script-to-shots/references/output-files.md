# Output files

Required shape for each file written to `<root>/gen-ai/shots/<slug>/` in the project. Files in
that directory are written here as `<shots>/name.md`.

**Keep the headings exactly as given.** Other skills read these files by heading, and a renamed
heading breaks them. A missing heading is a defect even when the information is elsewhere in the
file.

Every duration carries its basis in brackets. A duration with no bracket is not finished.

---

## `<shots>/SHOTS.md`

The index, and the only file some people will read. It has to stand alone.

```markdown
# Shots: <script name>

<One paragraph. What this is, how many chunks, total runtime, which units were used and why.
No lists, no hedging.>

## Running order

| # | file | duration | scene | what happens |
|---|---|---|---|---|
| 001 | `001-kitchen-note.md` | 5s | 1 | Maya finds the note on the table |
| 002 | `002-maya-reads.md` | 10s | 1 | She reads it aloud, 16 words |

## Scenes and their chunks

| scene | estimate | unit | chunks | why it split |
|---|---|---|---|---|
| 1 | 14 seconds [dialogue 16 words, plus 2 gestures] | 5 and 10 | 001, 002 | Line of 16 words needs 10, the find is its own 5 |

## Totals

- Chunks: <N>
- Total runtime: <N> seconds
- At 5 seconds: <N> chunks
- At 10 seconds: <N> chunks
- Target model: <model>
- Aspect ratio: <ratio>
- Theme music: <the spec, and whether it is generated in the prompts or laid over in post. Say
  plainly when the joins will be audible.>

## Shared lines

<1 line saying that `<shots>/shared.md` holds them and that every chunk file repeats them
verbatim.>

## Open questions

<Bulleted. What the script did not settle, and what you assumed instead.>
```

The running order is the deliverable. Write it so someone can read only this table and know what
the set costs.

The `file` column holds names relative to `<shots>/`, because a reader of that table is already
in that directory. That is the 1 place a bare file name is correct.

---

## `<shots>/NNN-short-slug.md`

1 file per chunk, numbered from `001` in running order so they sort the way they play. The slug
is 2 to 4 words, lowercase, hyphenated.

This file is **standalone**. It never says "as in the previous chunk" and it never refers to
another chunk file for a fact its prompt needs.

```markdown
# 002 Maya reads the note

## Duration

10 seconds

## Prompt

<A fenced code block. The complete standalone prompt, ready to paste. Nothing above it and
nothing inside it that is not part of the prompt.>

## Motion only prompt

<A second fenced code block, present only when the first frame of this chunk is the last frame
of the previous one. Motion clauses plus the shared style and exclusion lines. No description of
the setting, wardrobe or subject, because the frame already carries them.>

## Continuity in

- Pose: <what the body is doing at the first frame>
- Position: <where in the frame and in the space>
- Expression: <the face at that instant>
- Framing: <shot size, angle, where the camera has come to rest>

## Continuity out

<The same 4 fields at the last frame. This text and the Continuity in of the next chunk are the
same sentences, word for word.>

## Estimate basis

<How the duration was reached, with the numbers. `16 words at 2.5 words per second is 6.4
seconds, plus 1 second of beats, so 7.4 seconds, which does not fit 5.`>

## Inherited from

Scene <N>. <List the attributes taken from the scene, and name the source of each: the script,
`<shots>/shared.md`, `<guide>/palette.md`, `<bible>/CHARACTERS.md`.>

## Notes

<Anything a person generating this chunk needs and the prompt cannot carry: first frame
instruction, a line that continues across the boundary, a trim handle, an inference to check.
Write `None.` rather than deleting the heading.>
```

The prompt is the second heading so it is visible without scrolling. Everything under it is
there to be read when the chunk comes out wrong.

### Clause order inside the prompt

The prompt body follows the clause order that `video-prompt-engineer` uses, and the reason for
the order is in `video-prompt-engineer/references/structure.md`:

1. Duration
2. Aspect ratio
3. Medium and style
4. Shot size
5. Camera angle
6. Camera movement
7. Lens and focal length
8. Depth of field
9. Lighting
10. Colour and grade
11. Subject motion
12. Mood
13. Pacing and cuts
14. Audio, on a model that generates it, taken from `<shots>/shared.md`. The theme first where the
    theme is being generated, then this chunk's ambience and effects
15. Exclusions

1 clause per decision, commas between them, and a number in place of an adjective wherever a
number exists. Skip lens and depth of field for flat or illustrated styles, and check
`<guide>/camera.md` under `Applicability` before adding any optical language.

Keep the prompt under roughly 120 words. Past that, generators drop clauses, and the ones they
drop are at the end, which is where the exclusions live.

**And keep it inside the model's character cap, counted per chunk.** A chunk is a standalone
generation carrying the full shared set, so the cap applies to each file separately rather than to
the set. Where a chunk does not fit, take the character `Short form` instead of the `Long form` and
move the exclusions into the negative field if the API has one, before cutting anything the shot
actually needs. Record the cap in `<shots>/manifest.json` as `promptCharLimit`, so a later reader
knows what the chunks were written against and does not lengthen one past it.

---

## `<shots>/shared.md`

The lines that every chunk repeats. This file exists so there is exactly 1 authoritative copy of
each, and so a change can be made in 1 place.

```markdown
# Shared lines

<1 paragraph: these strings are copied into every chunk file byte for byte. Changing a word here
means recopying it into every chunk, including any already generated.>

## Style and medium

<A fenced block containing the exact string.>

## Palette and grade

<A fenced block containing the exact string.>

## Lighting

<A fenced block. When the script has more than 1 lighting state, 1 named block per state, and
each chunk file names which it used.>

## Characters

<1 subsection per character, each a fenced block with the description exactly as it will appear
in a prompt. Taken verbatim from `<bible>/CHARACTERS.md` or `<guide>/characters.md` where either
exists.>

## Wardrobe

<1 fenced block per character, or per look where a character changes.>

## Theme music

<A fenced block: instruments, tempo as a number, key or mode, and what the music is doing. 1
string for the whole piece. Or the line `Theme laid over in post. Chunk prompts ask for no
music.`>

## Audio

<A fenced block with the shared audio line: ambience, effects, and whether anyone speaks. Where
the target model produces no audio track, the single line `No generated audio. Sound is a post
step.` instead.>

On a model that generates audio this block is required, and `No audio, silent clip.` is a valid
value for it. What is not valid is leaving it empty, because a chunk with no audio line gets
whatever the model invents, and 9 chunks each inventing their own bed do not cut together.

**The theme is a separate block from the audio for a reason.** Ambience and effects are per chunk
and generate correctly per chunk. Music does not: chunks generated from an identical music clause
return different takes, so the music restarts at every join no matter how carefully the clause is
copied. For a set that will be cut together, the honest default is `Theme laid over in post`, with
every chunk prompt asking for ambience and effects and `no music`. Record the theme spec here
anyway, because it is what the composer or the music generator gets.

Where the user wants the music generated per chunk regardless, keep the instruments, tempo and key
byte identical in every chunk, vary only the arrangement, and say in `<shots>/SHOTS.md` that the
joins will be audible. A `000-single-pass.md` set is the one case where the theme genuinely plays
throughout, because there is only 1 generation.

## Exclusions

<A single fenced sentence beginning with No. Merges `<guide>/negatives.md` with the usual
artefacts. Include only what is plausible for this material.>

## Aspect ratio

<A fenced block, such as `Vertical 9:16, composed for a phone held upright.`>

## Source

<Where each block came from: the script, `<guide>/fragments.md`, `<bible>/CHARACTERS.md`, or
inferred. Mark the inferred ones, because those are the ones worth checking first.>
```

Fence every string. A quoted string inside prose invites a reader to retype it with different
punctuation, and that is a paraphrase.

---

## `<shots>/manifest.json`

```json
{
  "slug": "...",
  "source": "...",
  "project": "...",
  "createdAt": "...",
  "targetModel": "...",
  "unitDurations": [5, 10],
  "promptCharLimit": 2500,
  "aspectRatio": "9:16",
  "audio": "generated",
  "themeMusic": {"spec": "...", "route": "post"},
  "dialogue": "generated",
  "styleGuide": {"slug": "...", "path": "gen-ai/style/<slug>/", "origin": "project"},
  "characterBible": {"slug": "...", "path": "gen-ai/characters/<slug>/", "origin": "project"},
  "scenes": [
    {
      "n": 1,
      "heading": "...",
      "estimateSeconds": 14,
      "estimateBasis": "...",
      "chunks": ["001", "002"]
    }
  ],
  "chunks": [
    {
      "id": "001",
      "file": "001-kitchen-note.md",
      "scene": 1,
      "duration": 5,
      "estimatedWords": 0,
      "estimateBasis": "action, 2 gestures at about 2.5 seconds each",
      "firstFrameFrom": null,
      "summary": "..."
    },
    {
      "id": "002",
      "file": "002-maya-reads.md",
      "scene": 1,
      "duration": 10,
      "estimatedWords": 16,
      "estimateBasis": "dialogue, 16 words at 2.5 per second plus 1 second of beats",
      "firstFrameFrom": "001",
      "summary": "..."
    }
  ],
  "totals": {
    "chunkCount": 2,
    "runtimeSeconds": 15,
    "at5": 1,
    "at10": 1
  },
  "inferred": ["..."],
  "openQuestions": ["..."]
}
```

`promptCharLimit` is the target model's prompt cap in characters, or `1000` when it could not be
established. Every chunk prompt is written to fit it, and a later edit that lengthens a chunk has
to be checked against it.

`audio` is `generated` when the target model produces an audio track and `none` when it does not,
which decides whether every chunk carries an audio clause or none of them do.

`themeMusic.route` is `post` when the theme is laid over the cut, `in-prompt` when it is generated
with the picture, which is only honest for a single pass set, and `none` when the piece has no
theme. `spec` is the theme string itself and is filled in even when the route is `post`, because
that string is what somebody has to hand to a composer. `dialogue` is
`generated` or `separate`, from stage 0, and is `separate` whenever `audio` is `none`. `estimatedWords` is 0 for a chunk with no
speech, never null, so a consumer can sum the column. `firstFrameFrom` is the chunk id whose last
frame opens this one, or null. Every `file` value is relative to `<shots>/`.

`styleGuide` and `characterBible` are `null` when there is none. Each `path` is relative to the
project root when the source is in the project, and the full `~/.gen-ai/projects/...` path when
`origin` is `shared`. Relative paths are what keep the project folder movable; an absolute one
breaks the moment someone else opens it.

`inferred` and `openQuestions` are what another skill reads to decide whether to trust the plan
or ask the user. Fill them honestly. They are the machine readable version of admitting what the
script did not say.

## `<shots>/000-single-pass.md`

Written instead of the per chunk files when stage 0c finds that nothing forces a split. Same
headings as a chunk file, with the beat structure inside `## Prompt` in the form given in
`references/single-pass.md`.

Headings: `Duration`, `Prompt`, `Beats`, `Estimate basis`, `Why one pass`, `Inherited from`,
`Notes`.

`Why one pass` is required and states which of the splitting triggers were checked and found
absent. Without it, a later reader assumes the chunking step was skipped by mistake.

When this file exists, no `NNN-` chunk files are written. Two versions of the same piece is how
the wrong one gets generated.

---

## The project index

Not inside the shots directory. `<root>/gen-ai/README.md` is shared with the other skills, and
each owns one section. Create the file if it is missing, add or update **only** the line for this
shot set under `## Shot sets`, and change nothing else.

```markdown
## Shot sets

- `shots/orchard-ep1/`: 9 chunks, 52 s total, for `seedance-2.0`. Style `saturday-cartoon`, cast `orchard-tales`. 2026-08-14
```

Name the model, because a shot set cut for 5 second units is not reusable on a model with a
different maximum, and that is the single fact a reader most needs before reusing it.

If a `README.md` already exists in `<root>/gen-ai/` and is not this index, do not overwrite it.
Write `GEN-AI.md` alongside it instead and say so.
