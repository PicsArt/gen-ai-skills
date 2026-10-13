---
name: screen-tutorial
description: Turn a screen recording of an app or website into a 16:9 step-by-step tutorial with chapters - every step the recording shows kept in order, explained and held long enough to follow, narrated in the user's own voice or a generated one, with the chapter times ready for a video description - and a short vertical teaser from it if the user wants one. Use when the user has a screen recording and wants a tutorial, a walkthrough, a how-to or a course video.
metadata:
  uses: screen-analysis, media-analysis, speech-cuts, voice-over, captions, layouts, screen-zoom, scene-compose, evaluate, music-bed, motion-design
  optional: voice-over, speech-cuts, music-bed, motion-design
  imports: screen-analysis, layouts, screen-zoom
---

# Screen tutorial

A promo sells, so it keeps the few steps that look best and cuts the rest. A tutorial teaches, so
it keeps **every step**, in the order the recording shows them, and gives the viewer time to
follow each one. A screen recording in, a 16:9 tutorial with chapters out, about 1–5 minutes long.

Read video-core first. One job: a raw landscape screen recording in, one 16:9 tutorial out, with
its chapters as text for a description. A short vertical teaser from the same recording is offered
at the end, never built here.

| Stage | Gate | Skills |
|---|---|---|
| 1. Take the recording in | ASK | — |
| 2. Read the recording | SPEND | screen-analysis, media-analysis |
| 3. The outline: steps and chapters | ASK | screen-analysis |
| 4. The narration | ASK, SPEND | voice-over, speech-cuts, captions |
| 5. Build the tutorial | — | layouts, screen-zoom, scene-compose |
| 6. Check it | — | evaluate |
| 7. The user reviews | REVIEW | — |
| 8. Music, when wanted | ASK, SPEND, REVIEW | music-bed |
| 9. Export and deliver, with the chapters | DELIVER | — |
| 10. The 9:16 teaser, when wanted | ASK | — |

| Read this | Before you |
|---|---|
| `references/outline.md` | write the outline, the step lines or the voice lines, or build |

## 1. Take the recording in

- **No recording yet → open the upload in your first reply.** When the message carries no recording
  (no attachment, no link, no Drive file named), call
  `picsart_media_upload({ accept: 'video', purpose: 'your screen recording' })` in that same turn,
  with one line on what happens once it is in. If the host cannot show the upload, follow
  video-core's host notes.
- A link the user pasted, or a file in their Picsart Drive: bring it in as video-core's Asset URLs
  say. Every tool below reads the recording by the URL that comes back.
- **What the user already said:** the product, the length, whether to keep their voice. Never ask
  again for any of it.
- **The format:** 16:9, 1920×1080, 30 fps, as long as the steps need.

**The ASK waits for the moments.** Call `picsart_media_screen_moments` first, after stage 2's SPEND
if it applies: `input` says what the recording is. Then ask only what is still open, all in one
turn:

| Ask when | The question |
|---|---|
| the user gave no length | "As long as the steps need" / "About 2 min" / "About 5 min" |
| `input.hasAudio` | the narration, stage 4's first question |

When nothing is open, say in one line what the tutorial will be, and go on.

**What a tutorial is not built from.** A portrait recording (`input.orientation` is not
`landscape`): say a tutorial needs a desktop recording, and that a vertical promo can be made from
this one. An edited video (`input.edited`): say a tutorial needs the raw recording, before it was
cut. Stop there in both cases.

## 2. Read the recording

Read it as the screen-analysis skill says: the moments first, then still sheets of the moments that
matter. The recording is never sent to a model that watches video: never call
`picsart_media_describe_video`. The media-analysis skill is used only for the transcript.

Read the description of each tool you will call before the first call. When video-core's SPEND
says any of them charges, quote the whole read in one go before the first call: the moments, about
four still sheets, and the transcript when `input.hasAudio`, with one retry in case a call fails.
When none of them charges, say in one line that you are reading the recording, and go on. If the
user declines, say that the tutorial cannot be built without reading the recording, and stop.

- **The transcript**, when `input.hasAudio`: `picsart_media_transcribe` the recording once, whatever
  the moments' `tier`, and save it as media-analysis says. A thin transcript is no narration
  (media-analysis): go on as if the recording were silent.
- **A long recording** is read at a lower `fps` and `width`; the result says so in its
  `diagnostics`. Say it in one line.
- **The tier does not matter here.** A click-through is often tiered `timelapse`, with no proposed
  steps. The tutorial is built from actions, not from proposed steps (stage 3).

If a read fails, do as the media-analysis skill says for a failed watch. Never guess what the
recording shows.

## 3. The outline: steps and chapters

1. Group the events into actions as the screen-analysis skill says: run `scripts/actions.py` on
   the moments. Never group them yourself.
2. Read sheets of each action's box at its settle, as that skill says. Drop what a still shows is
   the app's own animation, merge two actions that are one thing the user would name, and write
   down what each step does in the viewer's words. **Every step and every chapter comes from a
   still.** If the user names a step that is not on screen, drop it and say so.
3. **Keep every step.** A tutorial drops none of the user's steps. When it runs long, say so and
   offer to leave a whole chapter for a second video; never thin the steps out.
4. Name the chapters at the starts `actions.py` suggests, as `references/outline.md` says, and
   find the finished result for the opening: its time and its box, on a still.

**SHOW the sheets, then ASK once:** one compact table, each row a step with what it does and its
time in the recording, grouped under the chapter titles, above it the tutorial's title.
"Looks good" / "Change something". The user renames, merges and splits chapters here. Revisions are
free; iterate until they approve.

## 4. The narration

**The recording has speech** (a transcript that is not thin): ASK "Keep my voice" / "Replace it
with a generated voice". Never mix the two line by line.

- **Kept:** `narration: "own"`. The transcript goes into the build whole. Every span of speech
  plays at 1×, never cut mid-sentence: only the silent stretches are cut or sped. Check every seam
  of the build with the speech-cuts skill's `review_cuts.py` before the check in stage 6. The voice
  is captioned from the saved transcript, as the captions skill says.

**No speech, or replaced:** `narration: "voice-over"`, when the voice-over skill is available to
you. Write one line per step as `references/outline.md` says. Read the voice model with
`picsart_model_params`, then quote every line as one batch with `picsart_preflight` (video-core,
SPEND). Generate after the yes, probe each line's real length, and transcribe each line for its
captions, as the voice-over and captions skills say. **The line sets the step's length, and the
picture holds**: a line longer than its step is never shortened to fit the picture here; the build
holds the picture until the line ends.

If the user declines the voice-over, or the voice-over skill is not available to you, offer the
tutorial with the step lines on screen only, `narration: "text"`, and build that. It generates
nothing.

## 5. Build the tutorial

Build it with the script in this skill's folder. Run it; never work the scene out yourself.

1. Write `{ spec, moments, transcript?, lines? }` to a file, as `references/outline.md` says, with
   `moments` exactly as `picsart_media_screen_moments` returned it.
2. From this skill's folder, run `python3 scripts/tutorial_scene.py <file>`. It prints one JSON
   line: `{ scene, duration, timeline, chapters, diagnostics }`. It groups the actions with the
   screen-analysis skill's `actions.py`, lays the recording out in the 16:9 frame as the layouts
   skill's landscape reference says, and keys each push and zoom out with the screen-zoom skill's
   `zoom.py`; those scripts ship beside it in `scripts/`. Run only `tutorial_scene.py`.
3. If it exits with an error instead, its one line names the field it cannot build from. Fix that
   field, and run it again.

Building is free and calls no tool. **Where you cannot run Python**, say that the tutorial cannot
be built here, and stop: the scene is too long to write by hand.

**Act on every diagnostic before you look at anything else.** Each has a `level`, a `code`, the
`step` it is about when there is one, a `message`, and a `fix`: the change to make in the outline.

- **`error`:** the scene is wrong. Make the change its `fix` names, and build again. Never patch
  the scene to get past one.
- **`warning`:** the scene plays, but something may read wrong. Make the fix when it keeps what the
  user approved; otherwise keep the outline, look at that moment in stage 6, and tell the user in
  the review line. `speech_spans` is one to keep and say: the user's voice ran over two steps, so
  both play at 1×, and the tutorial is longer than its silent cut would be.

**Masks.** The opening result's card is a masked panel. The first contact sheet must include it;
if it fails with `the authored mask carries no clip`, masks are not rendering here (the layouts
skill has the dated fact). Build the same outline again with `clip: "nest"` and check that build.
REVIEW opens the mask build; the nest build is the one that renders.

**Captions and callouts** go on after the build, with `picsart_media_patch_scene`: captions in the
band each step's `timeline` entry names (`band`), as the captions skill says; a callout on a step's
box only if the user asks and the motion-design skill is available to you, as that skill says. The
first draft ships with the push alone.

When the user's later comments change what the tutorial shows or says, change the outline and
build again, then add the captions again. When they edited the scene in the editor, their document
replaces yours (video-core): patch it instead of building again.

## 6. Check it

The build does not pass through `picsart_media_patch_scene`, so validate it with
`picsart_media_validate_scene`, then check it with evaluate. Take the moments from the build's
`timeline`, at most 8 to a contact sheet:

- each chapter card;
- the last half second of each push's peak, where the response holds;
- the moment each warning you left in is about.

The questions:

- Does each chapter card's title match its first step?
- Is each step's response inside the frame at its peak, and its text readable at 1920 wide?
- Is any caption or step line over the box a push landed on?
- Is anything private on screen (an email, a key, a customer's name)? Frame it out or cover it
  before REVIEW, as the layouts skill's landscape reference says.
- Does every character of the words draw, accents included?

Judge legibility on a still, not on softness alone: crop a `picsart_media_video_stills` sheet to the
step's box at that moment. If the still is sharp, the recording is legible.

## 7. The user reviews

REVIEW the mask build, titled "<Product> tutorial — draft 1": "Check each step holds long enough to
follow, and say where it drags." With the user's voice kept, add where it runs over two steps. Each
new draft's number goes up by one.

## 8. Music, when wanted

Under the user's own voice, default to no bed: offer it only with a generated voice-over or none.

**Offer it once, after the draft is approved**, and never bare ("do you want music?"). ASK with the
bed's brief drafted as the music-bed skill says, and three exits: "Generate it" / "Change the
brief" / "No music". A changed brief is redrafted and asked again; a skip is settled for the
session.

On a yes, the bed is a SPEND, as video-core says. Generate it and lay it under the approved scene as
the music-bed skill says; its script dips it under every voice line. Validate and look at a contact
sheet as stage 6 does, then REVIEW, titled "<Product> tutorial — music", with one line on what to
listen for: how the bed sits under the voice, or under the steps when there is none. A note on its
level moves it as the music-bed skill says; a different track goes back through the music-bed
skill's brief, with a new SPEND.

If the bed fails or is declined, say so in one line and go on with the approved draft.

## 9. Export and deliver, with the chapters

DELIVER the approved build: the mask build if masks rendered in stage 6, otherwise the nest build
of the approved outline. Export once, and give the link.

Then give the chapters exactly as the build printed them in `chapters`, as text the user pastes
into the video's description:

```
00:00 Open your settings
00:15 Make it yours
00:34 Invite your team
```

Say what the tutorial sounds like: the user's own voice, captioned; a generated voice-over,
captioned; or no sound, with the steps on screen. A generated voice is AI-made: say so, and tell
the user to switch on the platform's AI-content label when they post it.

Then offer one next step: a short vertical teaser from the same recording.

## 10. The 9:16 teaser, when wanted

**Offer it only when the screen-promo use case is available to you**; otherwise offer nothing
more. The offer is the ASK: "Make a vertical teaser too" / "No, that's all". On a yes, load the
screen-promo use case with the recording's URL,
the moments already read in this session and the approved outline as its candidate steps. Its own
stages and gates take over: it picks the few steps that sell and writes its own hook. **Nothing is
read twice**: never call `picsart_media_screen_moments` again for this recording. The teaser does
not carry this tutorial's voice-over; say so in the offer when there is one.
