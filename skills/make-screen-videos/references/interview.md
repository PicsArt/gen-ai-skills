# The interview

Every question this use case asks before the build, in order, with its options. Ask them as
picsart-video-rules's Asking says: one per turn (two only where marked), the recommended option first, and
each option's line saying what it changes. Skip any question the user's words or the recording
already answer, and say the answer back instead. Headers are at most 12 characters.

## Contents

- Where it goes
- What it is for
- How many
- Who it is for
- The message
- How long
- The sound and the ending
- Real or demo data
- The brief
- Which videos
- The screens
- What to see first
- The style
- The hook

## Where it goes

Always first, unless the user named a place.

- Question: "Where will people watch this?" · Header: `Destination`
- Options, the first recommended when the user gave no clue:
  - "Instagram Reels" — "Vertical 9:16, 15-60 s, up to 90 s when it holds. Sets the frame and where words can sit."
  - "TikTok" — "Vertical 9:16. Words keep clear of the buttons on the right and the caption below."
  - "YouTube Shorts" — "Vertical 9:16, under 60 s; up to 3 min only when asked."
  - "YouTube, a site or a course" — "Landscape 16:9, any length. Suits a full tutorial."
- Several places come through Other: the strictest safe zone of them holds.
- Then say the frame, never ask it: "Reels, so 9:16 at 1080×1920, with the words kept clear of
  the caption and buttons."

## What it is for

Always, unless the user named a kind.

- Question: "What should a viewer get from it?" · Header: `Kind`
- Options, the recommendation from the destination and the read: vertical and several distinct
  tasks gives how-to shorts; landscape and many steps gives a tutorial; one dense result gives a
  promo.
  - "Learn one quick thing per video" — "How-to shorts: each teaches one easy task, start to
    result. Your recording shows <n> of them."
  - "Understand one feature" — "An explainer: the problem, the feature, two or three uses."
  - "Want the product" — "A promo: the best results, fast, to sell."
  - "Follow every step" — "A tutorial: every step in order, with chapters. Best at 16:9."
- Asked before the read lands, add "I'll check this against the recording", and raise it again
  only if the recording disagrees.
- A tutorial for a vertical destination gets one line ("a tutorial that keeps every step reads
  best at 16:9; on Reels I'd split it into how-to shorts") and the user's choice stands.

## How many

How-to shorts and explainers, when the read found more than one topic.

- Question: "One video, or one per topic?" · Header: `How many`
- Options:
  - "One standalone short per topic" — "<n> shorts, each with its own hook and ending, so each
    can be posted alone."
  - "One short on the best topic" — "The most teachable one; more can follow later."
  - "Let me choose the topics" — "You'll see each topic's result and pick."
- The first and the last both lead to "Which videos"; the first ticks every candidate.

## Who it is for

Always, unless the user said.

- Question: "Who is it for?" · Header: `Audience`
- Options written from the product the stills show, for example:
  - "People new to <product>" — "Every step explained, every button named the first time."
  - "People who already use <product>" — "The basics skipped, the shortcut shown."
  - "Creators who have never tried <category>" — "The result first, so it looks easy, then how."

## The message

Words, not a list: picsart-video-rules's "facts get options; ideas get words".

- Offer 2-3 drafted sentences that differ, written from the recording, and let the user pick one,
  edit one or write their own. For example: "You can turn one idea into a storyboard in under a
  minute." / "Your characters stay the same in every scene." / "You never leave the chat to make
  a film."
- Where the host's question tool carries them, they are its options, with "Write my own" left to
  Other. With nothing to draft from yet, ask in a sentence with one example.
- With several shorts this is the set's message ("making a film with AI is easy"); each short's own
  lesson comes from "Which videos".

## How long

Only when the destination and kind leave a range. Options from `references/routes.md` for the kind,
for example a how-to short on Reels:

- Question: "How long should each one be?" · Header: `Length`
- "About 20 s" — "Short enough to watch twice. Best for 'look how easy'." / "About 35 s" —
  "Room for one more step or a before and after." / "45-60 s" — "Only if each topic holds that
  long."

## The sound and the ending

These two are independent and weigh the same: ask them together, two questions in one turn.

- Question: "How should it sound?" · Header: `Sound`. Offer only what this package can make: a
  generated voice needs the voice-over-generation skill, the user's voice needs speech in the recording.
  - "A generated voice with captions" — "Holds viewers with the sound on, and captions carry it
    muted. Costs credits; I'll quote first."
  - "Captions and music, no voice" — "Free except the music. The words carry it."
  - "My own voice from the recording" — "Kept at normal speed where you speak."
  - "Silent, words on screen" — "Free. You can add a track when you post."
- Question: "What should the viewer do at the end?" · Header: `Ending`
  - "Try it in <product>" — "Shown, and said if there's a voice, in at most five words."
  - "Follow for more" — "Suits a set of shorts."
  - "Save this for later" — "Saves and shares are what short-video feeds reward."
  - "Nothing, just loop" — "The last frame cuts back to the first."
- A promo with a presenter available adds a third question in its own turn: "No presenter" /
  "Use my own photo" / "Generate a presenter" (`references/routes.md`).

## Real or demo data

Only when the first sheets show an account's data: names, emails, an inbox, a customer list, a
key, a dashboard. A blank canvas or a public page skips it, and the brief says "no account data
on screen".

- Question: "Is this a real account, or a demo one?" · Header: `Data`
- Options:
  - "Real data: cover it" — "I'll find emails, keys, phone numbers and names on screen and cover
    each before you see a draft."
  - "A demo account" — "Nothing personal to hide. A key or a card number still gets covered."
- Unsure counts as real.

## The brief

One turn that closes the interview, never a question of its own:

- **You said:** Reels; how-to shorts; people new to Picsart; "making a film with AI is easy".
- **I read in the recording:** five topics; the app's own purple and off-white; no speech.
- **I assumed:** about 20 s each; English; "Try it in Picsart"; captions in the app's colours. Say
  "35 s" or "Spanish" to change one.

Then anything that does not fit together, said with what you'll do: "Topic 4 has nine steps; at
20 s it would rush, so I'd give it 35 s." The turn ends on the next real decision.

## Which videos

After the brief, with the candidates' results shown as one sheet.

- Question: "Which shorts should we make?" · Header: `Shorts` · multi-select
- Up to four options, most teachable first: the label is the short's suggested title, the line is
  "Learns: <one line>. <start>-<end> in <recording>." More than four go as a second question in the
  same turn, or as a numbered list answered with the numbers.
- An explainer asks "Which uses should it show?" the same way; a promo "Which results sell it?",
  at most six.

## The screens

After "Which videos", for the vertical kinds, when the screen-recording-layouts skill's `readability.py` fails a
moment, or the kind is a how-to or a promo where the UI is only the means. Skip it when every
moment reads and the UI is the point (a feature explainer of the app's own screens).

- Question: "How should the app's screens look in the video?" · Header: `Screens`
- The reason first, in one line from the measures: "At Reels size the shot cards' text is about
  16 px and 30 words; viewers can't read it."
- Options, "Recreate" first when a moment fails, else "Keep" first:
  - "Recreate the UI as motion design" — "The app's own screens, colours and words, redrawn
    larger and cleaner for 9:16 and animated. Only what the recording shows."
  - "Keep the original recording" — "Real screens, cropped and pushed in; small text stays
    small."
  - "Mix: original for proof, designed for the steps" — "The steps redrawn; the result shown as
    the real screen, so viewers see it is real."
- With "Recreate", the hook and payoff still show the real result where it is the product's own
  output; say so in the brief. Store the answer in the record as `screens`.

## What to see first

- Question: "What do you want to see first?" · Header: `First look`
- Options:
  - "Short 1 in three styles, as stills" — "Pick the look by eye before anything moves. Free."
  - "Short 1, finished" — "Judge the pace and style on a real cut; the rest follow it."
  - "The written plan of every short" — "Hooks, beats and words as text, before anything is
    built."
- Then say the plan back, as stage 5 of the use case says.

## The style

After the stills: "Which style for this set?" · Header: `Style`. The three styles shown, the
recommended one first, each line its feel and why it fits ("bright UI and beginners: friendly, and
the app's colours lead").

## The hook

In the plan of each video the user chose to see: "Which opening?" · Header: `Hook`. 2-3 drafted
hooks, each line saying what it opens on ("the problem: every shot is a wide", "before and
after", "the shot list rewriting itself") and the viewer panel's verdict on it.
