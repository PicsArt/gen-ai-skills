# The spec

The spec is every decision the promo needs, in one JSON object. `scripts/promo_scene.py`, in this
skill's folder, turns it into the scene: the time edit, the framing, the push onto each result,
the text and the grid. You decide what the viewer sees and reads; the script does the arithmetic.
Run it, and never work out a number it gives.

## Contents

- Shared fields
- A promo: prompt over result
- A re-cut: an edited video
- A process timelapse
- The words
- The font
- What comes back

Write its input to a file, as one JSON object `{ kind, spec, moments }`:

- `kind`: `"promo"` for prompt over result and for a re-cut, `"timelapse"` for a process
  timelapse;
- `spec`: the object below;
- `moments`: the result of `picsart_media_screen_moments` for this recording, exactly as returned. The
  build reads the recording's shape and cuts from its `input`, and each result's subject from its
  proposed steps.

Then run `python3 scripts/promo_scene.py <file>` from this use case's folder. It builds every
vertical kind: a how-to short, an explainer, a promo, a timelapse and a re-cut.

The script checks its input. When it cannot build from it, it exits with one line that names the
field and what is wrong with it. That line is the authority: where it and this file disagree,
follow the line. The recordings in the examples below are made up, and so are their numbers: read
yours from your own moments and stills.

## Shared fields

| Field | What to put |
|---|---|
| `uri` | the recording's URL, as a Picsart tool returned it |
| `product`, `audience` | what the promo is for and who it is for, a few words each, as the user confirmed them |
| `language` | the BCP-47 tag of every word on screen (`en`, `es`, `pt-BR` …): the user's language, unless they chose the recording's |
| `font` | a bold face that draws every character in `language`, as a catalog `key` or a live face's file URL: see [The font](#the-font) |
| `style`, `brand` | the style chosen at stage 6, by its id, and the brand colours mapped onto it, as the visual-style skill says. The build resolves them and colours every layer from them. Left out, the build uses its old dark palette: always set it |
| `clip` | `"mask"`: panels with rounded corners, clipped by masks. `"nest"`: each panel is a nested scene the size of the panel, with square corners. Start with `"mask"`; the use case's check says when to switch |
| `sourceAudio` | `"mute"`, the default, or `"keep"`: the recording's clips at speed 1 play its own sound. The build warns about each kept clip it speeds up. `"mute"` with a presenter |
| `duration` | only when the uploaded copy is shorter than the recording the moments were read from |
| `hook.title` | the hook, one entry per line |
| `hook.duration`, `outro.duration` | leave them out, unless a presenter's line or a generated hook shot sets the length |
| `outro.cta` | the call to action, one entry per line |
| `sfx` | a promo only, and only when the user chose sound: `{ push, outro, volume }`. `push` plays as each step's push onto its result starts, `outro` as the outro starts; each is `{ url, duration }` of a sound a Picsart tool generated. `volume` is 0–100, 35 when left out. Leave it out for silence |

## A promo: prompt over result

A made-up recording: a light-mode slide-deck app, 1440×900, 142 s, five requests, each answered in
9–21 s. The spec keeps four:

```json
{
  "uri": "<the recording's URL>",
  "product": "an AI slide-deck builder",
  "audience": "founders who pitch",
  "language": "en",
  "font": "<a bold face's key>",
  "clip": "mask",
  "target": 20,
  "hook": { "title": ["my notes were a mess.", "so I asked for a deck"], "step": "palette" },
  "steps": [
    { "id": "deck", "step": 0, "prompt": ["Turn my notes into a", "five-slide pitch deck"] },
    { "id": "timeline", "step": 1, "prompt": ["Make slide 3 a timeline", "of our first year"] },
    { "id": "palette", "step": 2, "prompt": ["Switch the whole deck to", "a forest-green palette"] },
    { "id": "chart", "step": 3, "prompt": ["Add a bar chart of", "riders per month"] }
  ],
  "outro": { "cta": ["Build your deck free"], "steps": ["deck", "timeline", "palette", "chart"] }
}
```

- `target`: the length in seconds, 20–40, 30 unless the user asked for another.
- `steps`, in recording order. Each has an `id` of your choosing (never `hook` or `outro`, the promo's own parts) and `step`, the index of a
  proposed step in the moments. To build a step the proposal split or merged wrongly, give
  `events` (the event indices it plays) and `result` (the event it pushes onto) instead of `step`.
- `prompt`: the request, re-typed large above the recording while the step plays. A step with a
  prompt opens as the reply arrives: the bubble already carries the request, so the typing and
  the send are left out.
- `label`: for a step with no typed request, a feature line in the bubble instead, so the viewer
  has something to read (see [The words](#the-words)). A step has a `prompt` or a `label`, never
  both. With neither, it gets a taller plain panel.
- `from` and `to`: the part of the step to play, in the recording's seconds, when one long event
  holds more than the step should show. Between steps, reconciliation uses the preceding bounded
  settle and preserves the next step's first selected event.
- `hook.step`: the step whose result the hook holds on. Pick the result that looks best at a
  glance.
- `outro.steps`: the results in the end grid, up to four, in the order they should read.

## A re-cut: an edited video

A re-cut is `kind: "promo"`, written differently, because the input is shots, not rounds of a
request and its result.

- **Each step is one shot**, from one time in `input.cuts` to the next: a proposed step, or its
  `events` and `result`, never reaching past the shot's cut.
- **`from` and `to` cut inside a long shot.** A shot that shows several screens, one after the
  other, becomes one step per screen, each with its own `from` and `to` at the times the stages
  found.
- **`label`, not `prompt`.** Nobody typed a request in an edited video, so each step carries a
  feature line.
- **The person on camera is left out** unless the user kept the sound: a talking face with no
  voice reads as broken. With `sourceAudio: "keep"`, a shot of them talking can stay, as long as
  it plays whole, at speed 1.
- **`language`** is the user's, unless they chose the video's own.
- Captions burned into the video stay in its picture: keep the new text off them.

A made-up input: a 52 s, 1080×1920 video the user edited on their phone about their meal-planning
app, Pantrio, with their voice-over in Spanish, 11 hard cuts, and three shots of them at a kitchen
counter, captioned. The user chose to re-cut it muted, with the words in Spanish:

```json
{
  "uri": "<the recording's URL>",
  "product": "Pantrio, a meal-planning app",
  "audience": "busy parents who cook at home",
  "language": "es",
  "font": "<a bold face's key that draws á, é and ñ>",
  "clip": "mask",
  "sourceAudio": "mute",
  "target": 20,
  "hook": { "title": ["¿Qué cenamos hoy?", "Ya está planeado."], "step": "week" },
  "steps": [
    { "id": "scan", "step": 2, "from": 6.2, "to": 10.4, "label": ["Escanea tu despensa", "con la cámara"] },
    { "id": "week", "step": 2, "from": 10.4, "to": 15.1, "label": ["Una semana de cenas", "con lo que ya tienes"] },
    { "id": "swap", "step": 4, "label": ["¿No te apetece?", "Cámbiala en un toque"] },
    { "id": "list", "step": 8, "label": ["La lista de la compra,", "hecha sola"] }
  ],
  "outro": { "cta": ["Descarga Pantrio gratis"], "steps": ["scan", "week", "swap", "list"] }
}
```

Its twelve shots are proposed steps 0 to 11 here. The kitchen shots, 0, 6 and 11, are left out.
The shot from 6.2 to 15.1 s shows the pantry scan and then the week's plan, so it is two steps,
split where its stages changed.

## A process timelapse

A made-up recording: 23 minutes in a desktop painting app, 2560×1440, a lighthouse at dusk from a
pencil sketch to the finished painting, with the layers panel on the right and a brush bar on top.
For the details the artist zooms in on the lamp, so that chapter has a box of its own:

```json
{
  "uri": "<the recording's URL>",
  "product": "a lighthouse illustration",
  "audience": "people who follow digital painting",
  "language": "en",
  "font": "<a bold face's key>",
  "clip": "mask",
  "process": { "from": 12, "to": 1360, "count": 15, "shown": 0.6, "speed": 8, "box": { "x": 420, "y": 160, "w": 1500, "h": 1180 } },
  "labels": [
    { "from": 0, "text": ["Sketch"] },
    { "from": 190, "text": ["Flats"] },
    { "from": 470, "text": ["Shading"] },
    { "from": 905, "text": ["Details"], "box": { "x": 980, "y": 260, "w": 620, "h": 560 } },
    { "from": 1180, "text": ["Glow"] }
  ],
  "reveal": { "at": 1371, "until": 1381.5, "box": { "x": 380, "y": 60, "w": 1800, "h": 1320 }, "hold": 3 },
  "hook": { "title": ["Three pencil lines.", "Then a lighthouse."] },
  "outro": { "cta": ["Follow for the next one"], "at": [150, 600, 1100, 1375] }
}
```

All times are the recording's seconds, and all boxes its pixels.

- `process`: the work, from its first change (`from`) to just before the result (`to`).
  - `count`: how many stages it jumps through. Each chapter gets at least two.
  - `shown` and `speed`: how long each stage plays and how fast. Nearby stages share the available
    footage without replaying it; a stage with no footage inside its source bounds and cut guards
    is omitted. A stage with too little footage plays for less than `shown`. Source windows stay
    inside their shot and the recording's end.
  - `box`: the process box from the screen-recording-analysis skill. Without it, the build pads the work
    area, which can crop the object or show the app's panels.
- `labels`: the chapters, each shown from its `from` until the next one's. The first starts at 0.
  Give a chapter its own `box` when the work moves on screen during it: the user zooms in, or a
  second editor takes half the window.
- `reveal`: the finished result, played on a card over its own blurred footage. `at` and `until`
  bound it, `box` frames it, and `hold` is how long it holds. It starts when the finished picture
  is on screen, not when its window opens.
- `outro.at`: up to four moments for the end grid, in order, showing the progress. The last one is
  the result.
- A timelapse is sped up throughout, so a kept sound plays only under the result's hold.

## The words

Everything the viewer reads comes from a still you looked at. Never write a request, a result or
a chapter the recording does not show. Every word is in `language`.

| Words | Rule |
|---|---|
| **Hook** | One or two short lines, at most eight words in all, said the way a creator talks, as the retention-hooks skill's hook rules say: "my notes were a mess." "so I asked for a deck" not a slogan ("Rough notes in. A pitch deck out.") and never a greeting ("Hi, today I'll show you…"). `[]` when the picture carries the hook alone |
| **Prompt lines** | The request as the viewer should read it: the user's own words cut to the request, typos fixed, nothing private such as a name, an email or a key. About 30 characters to a line, at most three lines. Only a request the recording shows being typed |
| **Feature lines** | For a step with no typed request: what the step shows, as a claim its stills prove ("Scan your pantry with the camera"), never dressed up as a request someone typed. About 30 characters to a line, at most two lines |
| **Chapter words** | One word each, naming what its stages show, in the order the work happened |
| **Call to action** | One, in at most five words |

Every line follows four rules besides its own:

- **One anchor.** The words name one thing the viewer can already picture: the deck, the pantry,
  the invoice. A product's category ("an AI productivity tool") is not one.
- **A number, when the recording proves it.** "Five slides in 9 s" beats "fast", but only where
  the stills and the moments show it.
- **Show, don't claim.** Never a word that grades the product: amazing, seamless, powerful,
  game-changing, revolutionary, effortless. No "!". The result on screen is the claim.
- **But and so, never "and then".** Join two steps with the reason one leads to the other
  ("The palette changes, so every slide follows"), or give each its own line.

The build checks the English lines and returns a `warning` for each it catches: `words_hype`,
`words_greeting` (a hook that opens with a greeting or "in this video"), `label_clicks` (a feature
line that narrates the clicks: "Click Export, then choose PDF"; write what the step gets done
instead), `words_and_then` and `words_long` (a hook over eight words, a call to action over five).
It never checks a prompt line: those are the user's own words.

**Loops.** Write the hook and the step lines as the retention-hooks skill says. Steps stay in
recording order: the loops are in the words, never a reason to reorder the recording.

**How many steps.** A prompted step plays in about 4 s, because its waits are cut, so a 20 s
promo holds about four and a 30 s one about six. When the build comes back well short of the
target, add back a step the spec left out, or tell the user it is shorter than asked, and why.
More than six steps: keep the steps that sell the product, and say which you dropped. A video that
keeps every step is a tutorial (`references/routes.md`).

## The font

The font must draw every character of the words, accents included (scene-building-basics).

- `picsart_scene_fonts` takes `query` (part of a face's key or display name), `family`,
  `licenseType`, `page` and `pageSize`, all optional. It returns one page of its catalog (`total`,
  `page`, `pageSize`, `hasNext`), each face with its `key`, `displayName`, `style` and, for most,
  `licenseType`, and nothing about which scripts a face covers. Narrow it with `query`, `family`
  and `licenseType` rather than paging through the whole catalog, and pass only what the schema
  documents.
- The same `query` also searches the live catalog by name and returns each face in `live.fonts`,
  with its `style` and a ready-made `asset`. The build declares no font assets, so pass that
  asset's `uri`, the face's `https` `.ttf`/`.otf` file on a picsart.com host, as `font` itself.
- Pick a face whose `style` is `Bold`, since the weight is in the face (scene-building-basics), and prefer
  `licenseType: "commercial"`, since a promo is published.
- Choose for the words' script as scene-building-basics says, and prove it on the first contact sheet:
  the hook usually carries the rarest characters.

## What comes back

The script prints one JSON line, `{ scene, duration, timeline, diagnostics }`, even when a
diagnostic is an `error`. The `timeline` lists the hook, each step by its `id`, and the outro, with
their start and end in scene seconds. Each of `diagnostics` has a `level` (`error` or `warning`),
a `code`, the `layer` it is about when there is one, a `message`, and a `fix` naming the change to
make in the spec. The use case's stage 9 says how to act on each level. Building is free: change
the spec and run the script again.
