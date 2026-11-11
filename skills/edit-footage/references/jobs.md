# The jobs

A job sets which stages run and the defaults each starts from. Anything the user or the brief says
wins over a default. Say the job back at intake in one line.

| | `broll-voiceover` | `talking-broll` | `footage-story` |
|---|---|---|---|
| **What it is** | B-roll cut under a voice-over: a brand, law-firm or real-estate film | a speaker on camera, with B-roll between and over their lines: an interview, a chef or founder intro | footage with no speech and no brief: an event, a trip, a product or a place |
| **Stages** | all 13 | all 13 | all but `takes` |
| **Takes** | the voice-over's take | the speaker's best take of each line, and the talking segments | none |
| **Pace** | shots hold 2-4 s, never under about 1.4 s unless a one-word beat needs it; fewer, longer shots | talking segments follow the speech; B-roll holds 2-4 s; a section per part of the brief (the speaker, the work, the result), each with one long hold and a breath before the next | from the reference, else shots of 1.5-3 s on the picture's own rhythm |
| **Cuts** | on key words, about 0.1 s before the word; minor words held through | on the speaker's sentence ends; B-roll covers joins, never a face mid-line unless planned | on action and movement within the frame, or on the music's beats |
| **Music** | none unless the brief asks; offer a quiet bed as an A/B | none | a bed carries it: offered as a rendered A/B; the shot's own sound kept under it |
| **Extra checks** | no mouth moving under the voice-over | the speaker in frame; nobody cut mid-sentence | the story reads with no words |
| **Delivers** | the format asked (9:16 by default), the cut list, a full-resolution conform when chosen | the format asked (3:4 or 9:16), the cut list, a conform when chosen | the format the reference or the destination sets, the cut list |

The record's `pipeline` lists all 13 core stages for the first two jobs: `intake, reference, proxies, log,
takes, look, story, plan, build, qc, critics, review, finish, deliver`. Keep `proxies` only when
the footage is on this computer: the edit-on-your-computer skill makes them. Elsewhere, leave it
out; the finish is then a full-quality export. `footage-story` leaves out `takes`.

## Every job's record stages

The record's `pipeline` for each job, in the core order. The defaults of the reel jobs are in
`references/reel-jobs.md`, and the remix's in `references/remix-flow.md`.

| Job | `pipeline` |
|---|---|
| `broll-voiceover`, `talking-broll` | `intake, reference, proxies, log, takes, look, story, plan, build, qc, critics, review, finish, deliver` (`proxies` only for footage on this computer) |
| `footage-story` | the same, without `takes` |
| `reel`, `highlight`, `podcast-clips`, `split`, `montage`, `slideshow`, `lesson` | `intake, reference, log, story, plan, build, qc, critics, review, deliver` (`reference` only when a reference reel was given or the cut is Vibe or Match a reel, both known before the record starts; `split` always has one) |
| `remix` | `intake, reference, story, plan, build, qc, critics, review, finish, deliver` |
| `channel-clips` | `intake, reference, log, story, plan, build, qc, critics, review, deliver` (`reference` always: the look is the job) |

## An old record, carried on by hand

A record from before the merge is resumed, never restarted. Without commands, mark done what it
shows as done, each with its `reads`, as the edit-pipeline skill says, and set `useCase` to
`edit-footage` and `pipeline` to the job's row above:

| Old record | Done when it holds |
|---|---|
| `client-edit.json` | its own `stages`, as they are |
| `cut-footage-into-reel.json` | `intake`: a `brief`; `log` and `story`: `moments`; `plan`: `takes`; `build`: every take with a scene or render URL. The check, the critics and the review run again: they are free. |
| `remix-reel-structure.json` | `intake`: a reference; `reference`: an approved `sheet`; `story`: a `mapping`; `plan`: a `route`. A built stage is shown again for its REVIEW. |

## Footage with no words

With no speech and no brief, find the story in the footage: a provisional arc from what the log
shows (arrive, discover, peak, leave; before and after; a day from morning to night), its hook and
its ending, written into the record's `story` (never `brief`) and said to the user as a proposal they can change at
review. Never add a voice-over to carry it, generated or recorded, unless the user asks; picture,
the shots' own sound and music tell it. On-screen words only when a beat cannot read without them.

## A second camera

When a shoot has two cameras, give each its role in the log (the main camera, the inserts).
Inserts cut in on their role ("an old camera's shots as atmosphere"), never as coverage of the
main camera's action.
