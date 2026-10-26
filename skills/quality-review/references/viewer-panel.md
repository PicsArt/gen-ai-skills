# The viewer panel

Three simulated viewers look at a short's hook, then at the whole draft, before the user does.

## Contents

- What it can and cannot tell
- The viewers
- What they see
- What they are asked
- Run each viewer on its own
- Grade, and revise

## What it can and cannot tell

The panel is simulated. It catches the obvious failures: a hook that reads as an ad, a promise
nobody reads, a step nobody could follow, nothing worth keeping. It cannot predict what a feed
will do with the video. The real test is the posted video's own numbers: how many viewers stay
past the first 3 s, how many watch to the end, and how many save or send it. The platform's
insights show them. Say this with the panel's verdict, which always opens "Viewer panel
(simulated)". Never write "viewers loved it".

## The viewers

Write a brief of three or four lines for each viewer, for this video's topic and destination:

| Viewer | Who | What they test |
|---|---|---|
| **The scroller** | 15, scrolling Reels or TikTok for fun, who gives a video less than a second and has never heard of the product | whether it stops anyone at all, and whether it smells like an ad |
| **The newcomer** | a creator new to the topic who wants to get better, and saves what teaches | whether the promise is clear and the steps can be followed |
| **The user** | already uses the product and knows its words | whether it is true, and whether it shows something they did not know |

Each brief says how old they are and what they scroll for, what they know of the topic and of the
product, and what makes them scroll on. It ends: "Answer in your own words, in a sentence or two,
as you would to a friend." Never put the plan, the message, the payoff or the product's pitch in a
brief. A viewer knows only what the frames show.

## What they see

From this skill's folder, run `python3 scripts/panel.py <file>` on `{ scene }`. It reads a
builder's whole output too. It prints `frames`:

- `hook.times`: 0, 0.5, 1 and 2 s. `hook.words`: every block of words on screen in those 2 s.
- `draft.times`: the middle of each beat, at most 8, what one contact sheet renders. `draft.script`: every block of words, in
  order.

Take one `picsart_scene_contact_sheet` at `hook.times` and one at `draft.times`, both free. Add
each spoken line, if there is one, as it is heard.

**A hook made of footage that does not exist yet** (a generated shot) is judged before anything is
paid for. Show the still it would open on, or the shot's one-line description, marked "described,
not made". Judge it again on its real frames once it is made.

## What they are asked

**The hook**, on its sheet and its words only:

1. Would you stop scrolling? Yes, maybe or no, and why.
2. What do you think this video is?
3. Does it feel like an ad? No, a bit or yes.
4. What do you expect next?

**The draft**, on the whole draft's sheet and its script, asked after the hook's answers:

5. What did you learn?
6. Could you do it now? Yes, maybe or no. For a promo, ask: would you try it?
7. Would you save it, send it to someone, both, or neither?

## Run each viewer on its own

Where the host can run isolated workers in parallel, run each viewer as its own worker. Give it
only its brief, the sheets, the words and the questions. Never give it the plan, this skill or
another viewer's answers. They answer apart, so none of them anchors on another.

Where it cannot, run the viewers inline, one after another. Write out the first viewer's answers
in full before you read the second viewer's brief. Never change an answer once the next viewer
has spoken.

## Grade, and revise

You grade each answer against the plan. Set `matches` to true when what the viewer thinks the
video is, and what they expect next, is what the payoff gives. Set `learned_matches` to true when
what they learned is the message. Put the answers in as `hook` and `draft`, with the fields the
script names, and run `panel.py` again. It prints `{ ok, hook, draft, summary }`. Each failure
carries the viewers' own words and a `fix`.

| id | Passes when |
|---|---|
| `stop` | at least two in three would stop scrolling |
| `ad` | no one says it is an ad, and at most one in three says "a bit" |
| `promise` | at least two in three read the promise the payoff keeps |
| `message` | at least two in three learned the message |
| `could_do` | at least two in three could do it now (a promo: would try it) |
| `keep` | at least two in three would save it or send it |

- **A hook that fails** is changed where the failure points: the opener, the words or the promise,
  as the retention-hooks skill's hook rules say. Changing only the font or the colours does not count.
  Build it again (building is free) and run the panel again with fresh viewers, because a viewer
  who saw the old hook remembers it.
- **A draft that fails** gets its `fix`, a new build and a new panel.
- The rounds come out of picsart-video-rules's evaluation budget. When they run out, go on with the best
  version and say in one line what the panel still fails. Never spend credits on a hook the panel
  failed without saying so in the quote.
- The `summary` goes with the line that asks or opens the review.
