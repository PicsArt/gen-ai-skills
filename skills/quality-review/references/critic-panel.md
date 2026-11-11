# The critic panel

Six simulated critics with taste look at a draft
after its cold watch and
before the user does.
Each has one lens. Each says what is wrong, when, and how to fix it.

## Contents

- How it differs from the cold watch
- The critics
- What they see
- What each returns
- Run each critic on its own
- Merge the notes
- Fix, ask, and review

## How it differs from the cold watch

The cold watch asks strangers what they got, a few seconds at a time, and marks their words against the
viewer track: it says where viewers lose the thread (`references/cold-watch.md`). The critic panel
asks experts what is wrong and what to do about it. The critics know the video's goal, so they can
never tell whether a stranger follows it.
Run the cold watch first and give the critics its gap
list: they say why viewers lost the thread there, and what would make the draft better.
Both are
simulated. A critic's note is an opinion from the frames, not a measure of how a feed will treat
the video. Never write "the critics approved it".

## The critics

Each critic is written once: its lens, its temper, what it ignores, what it is given and the shape
of its note. Where the host has the critics as agents, they are those agents. On every host, the
same text is in this skill as `references/agent-critic-<id>.md`.

| Critic | Agent and brief | Its lens, in one line |
|---|---|---|
| **The first-principles critic** (`roots`) | agent `critic-roots`, brief `references/agent-critic-roots.md` | the core problem the video solves for its viewer |
| **The radical** (`radical`) | agent `critic-radical`, brief `references/agent-critic-radical.md` | the concept, not the execution |
| **The interface designer** (`interface`) | agent `critic-interface`, brief `references/agent-critic-interface.md` | the UI on screen, and its fidelity to the real app |
| **The story editor** (`story`) | agent `critic-story`, brief `references/agent-critic-story.md` | whether the message is true and worth the time, and why viewers lost the thread where the cold watch found they did |
| **The growth strategist** (`growth`) | agent `critic-growth`, brief `references/agent-critic-growth.md` | the first second, where viewers drop, what makes them save or send it |
| **The art director** (`art`) | agent `critic-art`, brief `references/agent-critic-art.md` | the look |

A seventh critic, the challenger, does not wait for the draft: it questions each decision as it
is made, as `references/challenger.md` says. Its earlier answers are not given to these six.

Never put the plan, the chosen hook's reasons, or another critic's lens in a brief. A critic knows
only what the next section gives.

## What they see

From this skill's folder, run `python3 scripts/critics.py <file>` on `{ scene }`. It reads a
builder's whole output too. It prints `frames`:

- `sheets`: the times every 0.5 s from the first frame to the last, split into lists of at most
  `per_sheet` times. Pass as `per_sheet` the most times one `picsart_scene_contact_sheet` call
  renders, from its description. Take one contact sheet per list; they are free.
- `words`: every block of words on screen, with when it starts and ends. Add each spoken line, if
  there is one, with its time from the transcript.

Each critic gets the same seven things and nothing else:

- every sheet of the draft;
- **the source stills**, which are required: the real UI or footage the video depicts, at its key
  moments. For a screen recording, the recording's own stills at each step, as the screen-recording-analysis
  skill takes them; for the user's footage, a still of each clip in its source; for a film, the
  locked cast sheets and scene pictures. Without them no critic can see that the draft drifted
  from what it shows, so take them before the panel runs. When the record holds a reference's
  `format`, its reference stills (the format's `evidence`) and the format itself go with them:
  a drift from the format is marked `fidelity`, so it is a must-fix unless the user approved it
  (`format:<element>`), and a push away from an own-brand format is a choice, never a fix;
- the words timeline;
- the goal in one line (the message, as the user said it);
- the destination (where it is posted, and its length);
- **the brief**, when the user supplied one with the footage (notes, guides, scripts): read in
  full, as picsart-video-rules says, with its main message, audience and must-shows quoted;
- **the look board**, when the record holds a `look`: its board's stills with their sources,
  and the brief's style words quoted. A drift from the board is marked `fidelity`, as a drift
  from the source stills is;
- **the cold watch's gap list**, when one ran: where viewers lost the thread, in their own
  words. Never the viewers' whole accounts.

## What each returns

At most about 350 words, in this shape:

1. `verdict`: one line, the critic's judgement of the whole.
2. `problems`: each with `at` (a time or a `[from, to]` range in seconds, or `"whole"` when it is
   the whole video), `what` is wrong, and the `fix`. A fix is a change someone could make: "move
   the label up 200 px, above the caption bar", not "make it pop". A problem where the draft
   differs from the source stills sets `fidelity: true`.
3. The fields its `references/agent-critic-<id>.md` names under "Your note's own fields".

Only the problems in its own lens. A critic with nothing wrong says so in the verdict and returns
no problems; it never invents one to fill the note.

## Run each critic on its own

**Where the host has the critics as agents** (its host notes say so), start the six by name, all
at once: `critic-roots`, `critic-radical`, `critic-interface`, `critic-story`, `critic-growth`
and `critic-art`. Each agent holds its own lens, temper and note shape. Give each only what the
section above gives: the sheets, the source stills, the words, the goal, the destination, and the
brief, the look board and the gap list when they exist, as files or links. Each returns its note as JSON, ready
for `notes`.

**Otherwise**, run them apart: where the host can run isolated workers in parallel, run each
critic as its own worker, all six at once. Each worker's prompt is the whole text of its `references/agent-critic-<id>.md`, then the
"Looking at an image" section of your host notes (the worker has no host notes of its own), then
what the section above gives, as files or links, and nothing else. Each returns only its JSON note.
Where it cannot, run the critics inline, one after another, the first-principles critic first,
each from its file, with its note written out in full before the next starts.

Never give a critic the plan, this skill's other files or another critic's note.

## Merge the notes

Put the six notes in as `notes`, with the fields above, and run `critics.py` again with the
scene. It checks each note's shape and prints:

- `core`: the first-principles critic's sentence. It is the yardstick: weigh every other fix
  against it. A fix that serves it is in; a fix that pulls the video away from it is out, and is
  named as dropped, with why;
- `agree`: each stretch two or more critics flagged. Read the problems in it: where they name the
  same problem, even in different words, it is a **must-fix**. Where they name different problems
  at one moment, treat each as single;
- `fidelity`: every problem marked `fidelity`, from any critic. Each is a **must-fix**, even when
  only one critic saw it: the video shows the real product, so it must look like it;
- `single`: what one critic alone flagged. Make it when it serves the core sentence and nothing
  conflicts with it;
- `choices`: each radical concept, and the first-principles critic's `wrong_problem`. **Never apply
  one silently**: a new concept or a new problem is the user's decision, not a fix. Hand them to
  the use case's next gate, with the one you recommend and its reason;
- `long` and `absent`: a note over 350 words, or a critic with no note. Cut the note to its
  problems, or run the missing critic.

**Conflicts.** Read the notes for fixes that pull opposite ways: the story editor adds a line
where the growth strategist cuts the beat, the interface designer wants a bigger label where the
art director wants none. Decide each by the core sentence, and name each conflict in the review
line with the side you took.

## Fix, ask, and review

1. Make the must-fixes, then the single fixes you kept. Build again (building is free), and run
   the rest of this skill's checks again on the new build.
2. Hand the `choices` to the use case's gate, as above. A choice that changes the concept goes
   back to the use case's plan.
3. The review line opens with the `summary`, then the core sentence, the must-fixes made, the
   conflicts and how each was decided, and what was dropped.

The rounds are picsart-video-rules's (Evaluation). Run the critics again only on a new concept, not on
each fix round, and say which must-fix is still open when the rounds run out.
