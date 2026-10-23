# The routes

What differs by kind. Everything not here is the use case's own stages.

## Contents

- How-to short
- Feature explainer
- Promo: prompt over result, timelapse, re-cut
- The presenter (promo only)
- Tutorial
- Post copy

## How-to short

One easy task, from a state the viewer can reach to a visible result, so the viewer thinks "I can
do that". 15-35 s, 20 unless the brief says otherwise. 9:16.

**Finding the topics** (stage 4). Group the events into actions with the screen-recording-analysis skill's
`scripts/actions.py`, then read sheets of each action's result. A topic is a run of actions that
starts where a viewer could start (an empty chat, a blank canvas, the app's home) and ends on a
result you can see on a still. Score each by how clear its result is, how few steps it takes, and
how different it is from the others; keep the ones a beginner would want, at most eight. A topic
whose result is not on screen is not a topic: a change that is only words in the chat, or a
recording that ends on the request, has none.

**The beats**, in the retention-hooks skill's shape:

| Beat | Time | What |
|---|---|---|
| Hook | the first 2 s (retention-hooks) | a moment or a problem the viewer already feels, or the result in the middle of happening, never "how to" and never a product shot with a slogan. The words (8 or fewer, or none, never a transcript of the voice) read like a creator talking. The picture, the words, the spoken line, if any, and the payoff make one promise, as the retention-hooks skill's hook rules say |
| The task | 2-4 s | one line: what we are about to do |
| Steps | 4 s on | each action with its feature line, which says what it gets done and why that matters, the waits cut, something new every 2-3 s |
| Payoff | last 3-4 s | the result again, larger, held, under the takeaway: the rule or tip a viewer would save |
| Ending | 1.5-2.5 s | the call to action, or a cut back to the first frame |

**The build** is `promo_scene.py`, `kind: "promo"`, from `references/spec.md`: `steps` are the
topic's proposed steps (or `events` and `result` per action), each with a `label` (its feature
line), or a `prompt` where the user typed a request on screen; `hook.step` is the topic's last
step; `outro.steps` is that one step, so the ending holds the payoff; `outro.cta` the ending.
`target` is the chosen length.

**Check questions.** Does the hook open on a real moment, not the app's empty state or a product
shot? Did the viewer panel pass the hook and the draft? Can a beginner tell
what to click from each step alone? Is each feature line what the step gets done, not the clicks?
Does the short make sense with no other short before it? Is anything private left on screen that
the privacy pass did not cover?

**Review line:** "Would you stop for the first two seconds? Could someone new follow each
step? Say where it drags."

## Feature explainer

One feature: the problem it solves, the feature, then two or three uses, each ending on its result.
45-60 s on a vertical destination, 60-90 s at 16:9. Built as a how-to short is, its steps grouped by
use, with the problem stated in the hook ("Ten clicks to resize every slide?") and the feature named
in the task beat. On a 16:9 destination it is built as a tutorial (below) whose chapters are the
uses.

**Review line:** "Is the problem clear before the feature appears? Does each use end on its
result?"

## Promo: prompt over result, timelapse, re-cut

The best results, fast, to sell. 9:16, 20-40 s, 30 unless the brief says otherwise; a timelapse
runs as long as its stages and its result take. The recording decides the shape (`tier`):

| Tier | For | What the viewer sees |
|---|---|---|
| **Prompt over result** | an AI chat, or any app where a request produces a result | each request re-typed large above the recording, the wait cut, the result pushed in and held; a grid of results at the end |
| **Process timelapse** | a long working session: modelling, design, editing | the session in stepped jumps under a chapter word, then the finished result on a card over its own blurred footage |
| **Re-cut** | a video that is already edited | its screen shots re-cut under new text, a feature line over each, a grid at the end |

**The questions only a promo has**, each in its own turn after the interview's:

- **An edited video** (`tier: "recut"`, `input.edited`): say in one line that it is already edited,
  so you'd re-cut its screen shots under new text, then ASK "Re-cut it, muted" / "Re-cut it, and
  keep the sound where a shot plays untouched" (only with `input.hasAudio`) / "Stop here". On
  "Stop here", say a raw recording gives the other shapes, and stop.
- **The recording's own sound**, when `input.hasAudio` and the sound chosen was not a generated
  voice: "Mute it" / "Keep it where a clip plays at normal speed". Say what keeping it means: it
  plays only under clips at 1×, the jump cuts chop speech, and it is never transcribed, so not
  captioned. The answer is the spec's `sourceAudio`.

**The spec** is `references/spec.md`: the steps to keep (at most six), each request as the viewer
should read it or a feature line, the hook and the call to action; a timelapse's chapter words,
process box and result; a re-cut's shots. Before the hook's ASK, SHOW what the build will land on:
the sheet of the results kept; for a timelapse, sheets cropped to the process box at three moments
and to the result's box at `reveal.at` and just before `reveal.until`.

**Check questions**, for a promo: is each result inside its panel and its text readable at 1080
wide? Is each request fully typed before its result lands? Does each grid cell show the result, not
the chat around it? Is any text on white? Does a push cut a card's header mid-word? For a portrait
or square recording: does it fill the frame, and do the words sit on its quiet area, off any
captions burned into it? For a re-cut: does each step open and end inside its own shot, show the
screen and not the person, and does each grid cell show its own step? For a timelapse: does the
process card show the work, not the app's panels; does each chapter word match its stages; does the
result hold on the finished picture?

**Review lines:** a promo, "Check each request reads before its result lands; trim anything that
drags"; a timelapse, "Check the chapter words match the work; say where it drags"; a re-cut, "Check
each shot opens on its own picture". With the recording's sound kept, add where it drops out.

**Music.** A promo's music brief adds two short sounds, one under each push onto a result and one
as the outro starts, each under 1 s from a sound-effects model in `picsart_model_catalog`, in the
same SPEND as the bed. Build again with the spec's `sfx` set to them, so they land on the build's
own pushes. A timelapse ends on its own result and gets no bed; a promo that keeps the recording's
sound gets none either.

## The presenter (promo only)

A presenter on camera is offered only on the promo route, only when the ai-presenter, voice-over-generation and
spoken-captions skills are all available, and never as the default. If the user asks for one where they
are not, say a presenter is not available here, and go on without one.

- **Their own photo**: open `picsart_drive_upload_ask({ accept: 'image', purpose: 'a portrait photo of you' })`,
  and check it as the ai-presenter skill says before any quote. When it fails, say what fails and
  ASK "Another photo" / "Generate a presenter".
- **The SPEND** covers everything once: a generated portrait (one call for four candidates), one
  voice line per script line in one voice, a take for the hook, and one on the step narration if the
  presenter is in the steps. Quote each with `picsart_preflight`; a take that cannot be priced
  before its voice line exists is quoted as a count with its amount not known in advance. Describe a
  generated presenter in one line in the quote. The presenter's voice replaces the recording's own
  sound (`sourceAudio: "mute"`).
- After the yes: the portrait and the voice lines first, then SHOW the portrait that passed and ASK
  "Use this presenter" / "Try another". Generate the takes only after "Use this presenter". Build
  again with `hook.duration` set to the hook line's length, add the hook take full frame and the step
  take as a head bubble with `picsart_scene_patch` (ai-presenter), and caption the whole
  voice-over in the top band (spoken-captions). Write the lines as `references/script.md` says.
- If the user won't spend, offer the hook take alone once; then go on without a presenter.

Deliver a presenter's video as the ai-presenter skill's Check says.

## Tutorial

Every step the recording shows, in order, held long enough to follow, with chapters. 16:9,
1920×1080, about 1-5 minutes. A raw landscape recording only: a portrait or edited one gets the
vertical kinds instead.

**The outline** is stage 7's plan. Group the events into actions with `scripts/actions.py`; read
sheets of each action's box at its settle; drop what a still shows is the app's own animation; merge
two actions that are one thing the user would name; and write each step in the viewer's words.
**Keep every step**: when it runs long, say so and offer to leave a whole chapter for a second
video, never thin the steps out. Name the chapters at the starts `actions.py` suggests, and find the
finished result for the opening, as `references/outline.md` says. SHOW the sheets and the outline
(each step with what it does and its time, under its chapter); the ASK is the title, two or three
drafted ones. The user renames, merges and splits chapters by saying so.

**The voice**: the user's own voice is `narration: "own"`: the transcript goes in whole, every span
of speech plays at 1×, and every seam is checked with the speech-aware-cutting skill's `review_cuts.py`
before stage 10. A generated voice is `narration: "voice-over"`, one line per step. With neither,
`narration: "text"`: the step lines on screen.

**After the build**: captions in the band each step's `timeline` entry names (`band`), as the
spoken-captions skill says; a callout on a step's box only if the user asks and the motion-design-craft skill is
available. The first draft ships with the push alone. `speech_spans` is a warning to keep and say:
the user's voice ran over two steps, so both play at 1×.

**Check questions**: does each chapter card's title match its first step? Is each step's response
inside the frame at its peak, and its text readable at 1920 wide? Is any caption or step line over
the box a push landed on? Is anything private left on screen that the privacy pass did not cover?

**Review line:** "Check each step holds long enough to follow, and say where it drags." With the
user's voice kept, add where it runs over two steps. Under the user's own voice, default to no
music.

**Deliver** the chapters exactly as the build printed them in `chapters`, as text for the video's
description:

```
00:00 Open your settings
00:15 Make it yours
00:34 Invite your team
```

## Post copy

For a vertical destination, with each video:

- **Title**, under 40 characters, the result in the viewer's words: "Storyboard a film in one chat".
- **Caption**: a first line that hooks on its own (the feed cuts the rest), then one or two lines
  that say what the video shows, step by step, and the call to action.
- **Cover text**: 3-5 words, over the payoff frame, readable as a thumbnail.
- **Hashtags** only if the user asks.

For a set of shorts, mention once at delivery that Instagram can link Reels in a series; each short
still stands alone.
