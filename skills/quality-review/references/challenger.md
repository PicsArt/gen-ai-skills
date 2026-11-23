# The challenger

A seventh critic, who does not wait for the draft. The other six judge a finished draft; by then
the direction is paid for. The challenger questions each decision as it is made, and tries to show
that the direction is wrong before more work goes into it. Its one question is "why this?".

## When it runs

At each decision point the use case names, before the work that follows it:

- the idea, as the user gave it or as you drafted it. When there is a brief, it asks "is this the
  brief's message?";
- the plan: the concept, the structure, the hook;
- the key frames and stills: the style frames, the scene pictures, each image picked, and why it
  was picked;
- the design: the UI laid over the footage or recreated from it, the first time it is built. Here
  it also asks "why does this look different from the source?" of every layout, component, colour
  or word the source stills do not have;
- the moments and the cut of a short from longer footage: it asks the retention-hooks skill's
  `what-a-cut-is` questions 1 to 3 and 6 (the viewer's question by second two, its answer on
  screen, the picture for every claim, one continuous situation);
- every SPEND, before the quote is shown: what the money buys, and whether a free or cheaper step
  would answer the same question first.

Once per decision. A decision that changed because of it is challenged once more; a decision the
user confirmed after reading its challenge is never challenged again.

## What it sees

Run it with a fresh reviewer that has not seen the conversation. When an agent named `challenger`
is in your list of agents, start it by name: it holds its brief and its answer's shape. Its whole
brief is also in this skill as `references/agent-challenger.md`: its one question, its temper and
its answer's shape. Give it only:

- the decision, in one line, and the reason given for it;
- the alternatives that were weighed, in one line each;
- the goal in one line and the destination;
- the first-principles critic's core sentence, when the critic panel has run on this video;
- the material the decision rests on: the idea's words, the plan's rows, the stills or images,
  the quote;
- the source stills, as the critic panel takes them (`references/critic-panel.md`, What they
  see), once there is a source: the real UI or footage the video depicts;
- the brief, when the user supplied one: its main message, audience and must-shows, quoted.

Never give it the conversation, this skill's other files, or a critic's note. Without the agent,
give a fresh reviewer the whole text of `references/agent-challenger.md`, the "Looking at an image"
section of picsart-video-rules's `references/HOST.md` and the list above; when you cannot start
one, run it yourself with its answer written out in full before you go on.

## What it returns

At most about 150 words:

1. `verdict`: `keep`, `rethink` or `stop`.
   - `keep`: the reason holds.
   - `rethink`: the direction can stand, but this choice is weak; a better one is named.
   - `stop`: the direction is wrong, or the next step spends money that a cheaper step should
     come before.
2. `why`: the reason, tied to the material ("the still at 0 s is a logo on a plain canvas; the
   goal is a problem the viewer feels, and nothing in it is a problem").
3. `cheaper`: the cheaper alternative, or the cheapest test that would show whether the direction
   is right: a free build, one still before a batch, a contact sheet before an export.

## Act on it

- **`keep`**: go on. Its `why` is the recommendation's reason.
- **`rethink`**, on your own choice: change it as the challenger says, or keep it and say why in
  one line. Then go on.
- **`stop`**, and a `rethink` of the user's own choice: they are the user's to decide, with the
  `why` and the `cheaper` alternative. The use case's gate says where they go.

A challenge never overrides the user. It gives them the reason to look again, once. Say in one
line what the challenger said ("Challenger: stop — four stills first, before twelve").

## Record it

A use case that keeps a project record (the edit-pipeline skill's) writes each verdict into its
`challenges` before going on: `stage` (the record stage the decision belongs to: `story` for the
moments, the map or the mapping, `plan` for the cut, its opener or the route), `decision`,
`verdict`, `why`, `cheaper` and `date`. The question the decision leads to, an ASK or a SPEND, is
asked only once the verdict is there. The record refuses to go past `story` or `plan` without it.
A challenge is never skipped on your own: only the user skips one, by name, and that goes in as
`"skipped": "user"` with their `words`. Where no script runs, write the same fields by hand.
Whether the challenger ran as an agent, as a fresh reviewer or as you from
`references/agent-challenger.md`, the entry is the same.
