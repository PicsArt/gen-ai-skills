# The outline

The outline is every decision the tutorial needs, in one JSON object, `spec`.
`scripts/tutorial_scene.py`, in this skill's folder, turns it into the scene: the actions, the time
edit, the push and the zoom out on every action, the cards, the step lines and the chapters. You
decide what the viewer sees, reads and hears; the script does the arithmetic. Run it, and never
work out a number it gives.

## Contents

- The fields
- The words
- Pacing
- What comes back

Write its input to a file, as one JSON object `{ spec, moments, transcript?, lines? }`:

- `spec`: the object below;
- `moments`: the result of `picsart_media_screen_moments` for this recording, exactly as returned;
- `transcript`: with `narration: "own"` only, the `picsart_media_transcribe` result, as saved;
- `lines`: with `narration: "voice-over"` only, one `{ step, url, duration }` per step: the step's
  id, the voice line's URL as a Picsart tool returned it, and its length as
  `picsart_media_probe` measured it.

Then run `python3 scripts/tutorial_scene.py <file>` from this skill's folder.

The script checks its input. When it cannot build from it, it exits with one line that names the
field and what is wrong. That line is the authority: where it and this file disagree, follow the
line. The recording in the example below is made up, and so are its numbers: read yours from your
own moments and stills.

## The fields

| Field | What to put |
|---|---|
| `uri` | the recording's URL, as a Picsart tool returned it |
| `product` | what the tutorial is about, a few words, as the user confirmed it |
| `title` | the tutorial's title, one or two lines, over the opening result |
| `language` | the BCP-47 tag of every word on screen: the user's language |
| `font` | a bold face that draws every character in `language`, chosen as scene-building-basics says |
| `style`, `brand` | the style chosen at stage 6, by its id, and the brand colours mapped onto it, as the visual-style skill says. Left out, the build uses its old dark palette: always set it |
| `clip` | `"mask"`, then `"nest"` if masks fail at the check |
| `narration` | `"own"`: the user's voice kept; `"voice-over"`: generated lines; `"text"`: the step lines alone |
| `duration` | only when the uploaded copy is shorter than the recording the moments were read from |
| `intro` | the finished result the tutorial opens on: `at`, a source second where it is on screen, and `box`, its box in the recording's pixels, both from a still |
| `steps` | every step, in recording order. Each has an `id` of your own (never `intro`, never starting with `chapter_`), `actions`, the indices from `scripts/actions.py` it plays (one, or several the stills showed are one thing), and `text`, its step line |
| `steps[].typed` | `true` when the text being typed is the lesson (a formula, a command): the typing plays at 1×, not sped |
| `steps[].wait` | `true` when the wait after the step is one the viewer will face too (a render, an upload): it plays as a short sped beat, and the build reports its real length so the voice can say it. Every other wait is cut |
| `steps[].box` | only to push onto a smaller part of the response than its action's box: the field the viewer must read |
| `chapters` | each `{ title, from }`: the chapter's title and the id of the step it opens on. The first opens on the first step |

A made-up click-through: a team workspace app, 1920×1080, 45 s, no sound. Its nine actions become
nine steps in three chapters, with the step lines on screen:

```json
{
  "uri": "<the recording's URL>",
  "product": "Trellis, a team workspace app",
  "title": ["Set up your Trellis workspace"],
  "language": "en",
  "font": "<a bold face's key>",
  "clip": "mask",
  "narration": "text",
  "intro": { "at": 40.2, "box": { "x": 1500, "y": 80, "w": 380, "h": 90 } },
  "chapters": [
    { "title": "Open your settings", "from": "sidebar" },
    { "title": "Make it yours", "from": "theme" },
    { "title": "Invite your team", "from": "team" }
  ],
  "steps": [
    { "id": "sidebar", "actions": [0], "text": ["Open the sidebar"] },
    { "id": "settings", "actions": [1], "text": ["Choose Settings"] },
    { "id": "theme", "actions": [2], "text": ["Pick a theme from the menu"] },
    { "id": "compact", "actions": [3], "text": ["Scroll down and turn on compact mode"] },
    { "id": "name", "actions": [4], "text": ["Type your workspace's name"], "typed": true, "wait": true },
    { "id": "team", "actions": [5], "text": ["Open the Team page"] },
    { "id": "invite", "actions": [6], "text": ["Click Invite"] },
    { "id": "email", "actions": [7], "text": ["Type your teammate's email"] },
    { "id": "sent", "actions": [8], "text": ["The invite is on its way"] }
  ]
}
```

**Every action is in a step.** The build warns `actions_left_out` for any action no step plays. Leave
one out only when a still showed it is the app's own animation, not the user's step, and say so in
the outline's table.

## The words

Everything the viewer reads or hears comes from a still you looked at. Every word is in `language`.

| Words | Rule |
|---|---|
| **Title** | What the viewer will be able to do, in the product's words: "Set up your Trellis workspace". Never a greeting |
| **Chapter titles** | As short as the screen-recording-layouts skill's landscape reference holds a chapter's title, naming what its steps get done, in the order the work happened. The build warns `title_long` past it |
| **Step lines** | One line, as long as the screen-recording-layouts skill's landscape reference holds a step line, two only when it must: the outcome and the place to look ("Pick a theme from the menu"), in the words on the screen. Never an email, a name or a key from the recording |
| **Voice lines** | One per step, 8–15 words, about 3–6 s: say "you", the outcome and where to click, in the voice-over-generation skill's way. The line can say more than the step line, never something the screen does not show. With a wait marked, say its real length: "It takes about a minute to save." |

Spoken lines follow the voice-over-generation skill for how they are said and measured. Write them for the
ear: short words, one idea a line, the stress on the last word. A generated voice is a guide, never
a customer: it never says it uses the product.

## Pacing

The script holds these; they are here so you can say why a step lasts as long as it does.

| Rule | Value | Source |
|---|---|---|
| An action's hold | its voice line's length, the picture held until the line ends; with no line, 1.8 s after the response settles | the line: the tutorial's design; the 1.8 s is the screen-recording-zoom skill's hold |
| A step's spoken length | 3–6 s, 8–15 words | Screen Tutor's tutorial skill |
| Speech rate | as the voice-over-generation skill measures it; each line's real length is probed once it is generated | the voice-over-generation skill |
| Waits | cut; a wait marked `wait` plays as a sped beat under 1 s, its real length said by the voice | shorts never wait over about 1 s; saying the real wait teaches what to expect |
| Typing | 2× unless `typed` | the speed map of the screen tools' time edit |
| The user's voice | always 1×, never cut mid-sentence; only silence is cut or sped | a sped clip's speech is pitched and chopped |
| Zoom in | starts as the screen-recording-zoom skill starts a push on a click, on its ramp and curve | the screen-recording-zoom skill |
| Zoom out | after the hold, 1.5 s, back to the whole screen, slower than in | the screen-recording-zoom skill's ramp out |
| Peak | until the response's text reads at 30 px, never cropping the box | text meant to be read is at least 30 px |
| Chapter card | 2 s, its title as short as the screen-recording-layouts skill's landscape reference holds it | **a starting number with no source**; the first dogfood sets it |
| The opening | the finished result, the first 5 s | the main message in the first 5 s |

## What comes back

The script prints one JSON line, `{ scene, duration, timeline, chapters, diagnostics }`, even when a
diagnostic is an `error`.

- `timeline`: the intro, each chapter card (`chapter_0` …) and each step by its `id`, with their
  start and end in scene seconds. A step also has `band`, `bottom` or `top`, where its line sits and
  where its captions go; `line`, its voice line's span; and `wait`, the real length in seconds of a
  wait it shows as a sped beat.
- `chapters`: the lines for the video's description, `MM:SS Title`, the first at `00:00`. The
  intro is folded into the first chapter: at 5 s it is too short to be one of its own.
- `diagnostics`: each has a `level`, a `code`, the `step` it is about when there is one, a
  `message`, and a `fix` naming the outline field to change. `chapters_few` and `chapter_short`
  say when a description would not show the chapters: it needs at least three, each at least
  10 s. `hold_waiting_range` is an `error` naming a step with no non-waiting frames to hold:
  the build succeeds using the last available waiting frames. Adjust that step's actions to
  include a settled response outside the wait, or tell the user at REVIEW.

Building is free: change the outline and run the script again.
