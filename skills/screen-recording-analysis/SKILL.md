---
name: screen-recording-analysis
description: Read a screen recording from its pixels - its shape, cuts and sound, when and where the screen changes, how long the waits are, the steps with their results, every action of a click-through with scripts/actions.py, the stages of a long working session, the shots of an already edited video - then look only at small still sheets of the moments that matter, and find private data in the text read from them with scripts/private_text.py. Use when a use case needs to know what happens in a screen recording, and when, without a model watching the video.
metadata:
  imports: screen-recording-zoom
user-invocable: false
---

# Screen analysis

A screen recording is mostly waiting, and the story is in the few pixels that change. Comparing
frames finds them: when something happens, where on screen, how long each wait is, and where one
step ends and the next begins. That needs no model that sees, so it is fast and gives the same
answer every time. Vision is spent only on still sheets of the moments that matter: to read a
request, to check a result, to pick a hook, to name a stage.

| Tool | Gives | When |
|---|---|---|
| `picsart_media_screen_moments` | the recording's events, waits, boxes and proposed steps, as one JSON | once per recording, first |
| `picsart_media_video_stills` | one image of tiled stills at the times you name, optionally cropped | each time you need to see a moment |
| `picsart_media_screen_stages` | the moments that look least like each other, with their novelty | a long working session with no waits to cut |

Whether a call charges is picsart-video-rules's SPEND; the use case asks before the read. All three take the recording's URL as a Picsart tool returned it (see
picsart-video-rules's Asset URLs).

## The moments

Call `picsart_media_screen_moments({ videoUrl })`. Leave `fps` and `width` at their defaults. It returns:

- **The input**, `input`: the recording's `width` and `height`, its `orientation` (`landscape`,
  `portrait` or `square`), whether it is already `edited` (hard cuts between shots rather than one
  screen changing), its `cutsPerMinute` and the `cuts` themselves in seconds, and `hasAudio`.
- **Events**, in time order. Each has a kind, a start, a settle time (the last change, after which
  the region holds still), the box where it changed and the core of the largest change, all in
  source pixels, and the mean brightness of that box when it settles.
  - `cut`: most of the frame changed at once, such as a new page or a new message.
  - `scroll`: the page moved.
  - `reveal`: something was drawn at once.
  - `progressive`: something was drawn over time, such as streamed text or a render.
- **Dead ranges**: `still` when nothing moves, `waiting` when only a spinner or a caret does.
- **The content box**, everything that ever changed, and **the work area**, where the changes keep
  coming (the canvas, the viewport, the chat column, without the menus around it).
- **Cuts per band**: cuts counted in horizontal bands. A split layout hides its cuts from a
  whole-frame count, because one half never changes.
- **Proposed steps.** A step opens at a cut or a page-wide change. The typing just before it is its
  lead-in, and its result is the largest change that follows. Each result has its box, its settle
  time and its subject: the textured part of the result's card, such as the photo and not the chat
  around it. A timelapse gets no proposed steps: its stages take their place.
- **A suggested tier**, `tier`: `prompt_over_result`, `timelapse` or `recut`, with the measurement
  behind it in `tierReason`.

**The proposed steps are a proposal, not a decision.** Keep, drop and reorder them after you have
looked at their stills. Never keep a step the stills do not show.

**The times are measured.** A settle time comes from the pixels, so a push timed to it lands on the
finished result. Never move it by a fixed offset ("the result is 2 s in"): reveal times vary by
seconds from step to step.

## Actions

When every step a recording shows counts, not only its results (a click-through taught step by
step), group its events into actions with the script. Write the moments, exactly as
`picsart_media_screen_moments` returned them, to a file, and from this skill's folder run
`python3 scripts/actions.py <file>`. Never group the events yourself.

- **An action is what a viewer would name**: open a menu, type a title, open a page. It comes from
  the events, not from the proposed steps. A step opens only at a page-wide change, so a menu or a
  dialog lands inside one, and a click-through with few waits is tiered `timelapse` and gets no
  steps at all.
- **Each action** has its events, a kind (`reveal`, `cut`, `typing`, `progressive`), its `at` and
  `settle`, the suggested chapter it falls in, and its `box`: where the screen responded. That box
  is what a push leans in on, because no event says where the pointer clicked. A scroll joins the
  action it leads to, and changes close in time and place are one action.
- **Chapters** are suggested where the whole page changes, the same rule the proposed steps split
  on. **Waits** are marked with the action they follow, never dropped: the use case decides how
  much of each to show.
- **Check every action on a sheet** at its settle, cropped to its box. An app's own animation reads
  as an action, and two small actions can be one thing the user would name: drop the animation,
  merge the two. Never keep an action the stills do not show.

## Stills

`picsart_media_video_stills({ videoUrl, times, crop })` returns one hosted image and each tile's time and
place in it. Look at it as picsart-video-rules says (Asset URLs).

- **Crop to what you need to read.** A whole desktop at tile width shows no readable text. Crop to
  the event's box, the result's box or the content box, in source pixels.
- **One question per sheet**, up to about eight tiles: the requests, then the results, then the
  hook candidates.
- **The request:** the end of the step's lead-in, cropped to where the typing happened.
- **The result:** 0.2 s after its settle time, cropped to its box. In an edited video, never past
  the next time in `input.cuts`: a result that settles just before a cut is read 0.2 s before it,
  or the tile shows the next shot.
- Leave `tileWidth` and `columns` at their defaults unless the text is still too small to read.

Write down what each tile shows, in the words the viewer would use. Everything the use case writes
on screen comes from these notes.

## Private data

A recording of a real account shows what was on screen: emails, keys, phone numbers, a customer's
name. Find it in the text you already read; no tool watches for it.

1. Write each piece of text you read, on the still sheets and in the transcript, as one entry:
   the `text`, the recording's second `at`, its `box` in source px when it came from a still, and
   `from`. Read the corners too: an account menu, a browser's address bar, a notification.
2. From this skill's folder, run `python3 scripts/private_text.py <file>` on `{ texts }`. It
   prints each hit with its `kind` (`email`, `key`, `token`, `phone`, `card`), where it was, and
   the match masked, so you never repeat the secret. Quoted secrets may contain spaces even
   when cropped before the closing quote; card groups may have any amount of horizontal
   whitespace, with at most one line break between digits. Cards are read both as written
   and with real dates as field boundaries, and every card either reading finds is masked, so a
   card hyphen-joined to a date keeps its last group.
   Adjacent phone numbers with recognizable phone groups are kept whole rather than reporting
   a card made from their middle groups.
3. Check each hit on its still, cropped to its box: keep it, or drop it when the still shows it is
   not private (a sample address in a placeholder). The patterns miss names and street
   addresses: look for those yourself, on the same sheets.

A key or a card number is private even in a demo account.

## The tier

| Tier | The moments show | Check on a sheet |
|---|---|---|
| `prompt_over_result` | rounds of a typed lead-in, a page change, then a large result; long waits between them | the typed requests and their results |
| `timelapse` | the screen never goes still for long; the changes keep coming in one work area; few cuts | the object being worked on, early, midway and at the end |
| `recut` | `input.edited`: hard cuts between shots, many a minute, and no waits; often a person on camera, captions burned in, sound | one tile on each side of a few cuts: different shots, not one screen changing |

Take the suggested tier and its `tierReason`, and check it on the first sheet. When the sheet
disagrees, believe the sheet, and say which tier you took instead. A recording with steps but no
typed requests, such as clicking through an app, is still `prompt_over_result`: its steps have no
request to re-type, so what each shows is named in a line of its own.

## Stages of a long session

A modelling, design or editing session has no waits to cut: what matters is where the work
visibly changes.

1. `picsart_media_screen_stages({ videoUrl, count: 12 })`. Each stage is the moment least like every
   stage already chosen, after leaving out what moves all the time (a camera inset, a clock).
2. One sheet of those times, cropped to the work area. Name what each stage shows in one word, as
   the viewer would, such as "Sketch", "Inks", "Shading", "Glow" for an illustration. If the crop
   is too tight to name a stage, look at it on a full-frame sheet rather than guess.
3. Where the names change are the chapters. To see more of one chapter, call again with `chapters`
   set to the chapters' start times.
4. On one full-frame sheet, find two boxes:
   - **the process box**: the object being worked on, without the app's own panels (a timeline
     strip along the bottom, a node editor, a camera inset). The work area alone can crop the
     object, so check it;
   - **the result**: the moment the finished result is on screen, and its box. A render window can
     open on an empty checkerboard before it draws, so the result starts when the picture does.

## An edited video

A `recut` input is a finished video, not a recording: shots cut together, often a person talking
between screen clips. The unit is the **shot**, from one time in `input.cuts` to the next.

- **Keep every time inside its shot.** A step, a still or a result that crosses a cut shows the
  next shot.
- **A long shot can hold several screen clips.** A person who never stops moving keeps one event
  open across a whole shot, so nothing splits it. `picsart_media_screen_stages` separates them: call it
  with `chapters` set to the cut times, so each shot gets stages of its own, and read those times
  on a sheet.
- **Tell the screen from the person.** On one full-frame sheet, note which shots are the screen,
  which are the person on camera, and where burned-in captions sit, so text written later stays
  off them.
- **The words on screen have a language.** Note it from the stills: the captions', the app's.

## Limits

The detection thresholds were tuned on two raw recordings and seven finished shorts, as of
2026-09-30. A recording with a video playing inside it, or a dark interface with small text, may
split one event in two or merge two into one. In an edited video, the content box can take in the
person on camera rather than the screen. Check the steps and the boxes on a sheet before building
on them, and when the moments and a sheet disagree, believe the sheet.
