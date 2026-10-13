---
name: screen-promo
description: Turn a screen recording of an app or website into a short vertical promo - each request typed out large over its result with the waiting cut, or a long working session sped up into a timelapse that ends on the finished result - with an on-camera presenter if the user wants one. Use when the user has a screen recording and wants a promo for TikTok, Reels or Shorts.
metadata:
  uses: screen-analysis, layouts, screen-zoom, scene-compose, evaluate, talking-head, voice-over, captions, music-bed
  optional: talking-head, voice-over, captions, music-bed
  imports: layouts, screen-zoom
---

# Screen promo

A screen recording is mostly waiting, and what it shows is a few pixels of dense UI. This turns it
into a 20–40 second vertical promo that a thumb stops for, in one of three shapes. The recording
decides which:

| Tier | For | What the viewer sees |
|---|---|---|
| **Prompt over result** | an AI chat, or any app where a request produces a result | each request re-typed large above the recording, the wait cut, the result pushed in and held; a grid of the results at the end |
| **Process timelapse** | a long working session: modelling, design, editing | the session in stepped jumps under a chapter word, then the finished result on a card over its own blurred footage |
| **Re-cut** | a video that is already edited: shots cut together, often a person on camera | its screen shots re-cut under new text, a feature line over each, a grid of what they show at the end |

A presenter on camera is an option the user adds, never the default.

Read video-core first. One job: a screen recording in, one short 9:16 promo out. A step-by-step
tutorial that keeps every step is the screen-tutorial use case: if the user asks for one, load it
when it is available to you; otherwise say a tutorial is not available here, and offer the promo.

| Stage | Gate | Skills |
|---|---|---|
| 1. Take the recording in | ASK | — |
| 2. Read the recording | SPEND | screen-analysis |
| 3. Write the spec | ASK | screen-analysis |
| 4. Build the promo | — | layouts, scene-compose |
| 5. The presenter, when chosen | SPEND | talking-head, voice-over, captions |
| 6. Check it | — | evaluate, screen-zoom, layouts |
| 7. The user reviews | REVIEW | — |
| 8. Music, when wanted | ASK, SPEND, REVIEW | music-bed |
| 9. Export and deliver | DELIVER | — |

| Read this | Before you |
|---|---|
| `references/spec.md` | write the spec or build |
| `references/script.md` | write the presenter's lines |

## 1. Take the recording in

- **No recording yet → open the upload in your first reply.** When the message carries no recording
  (no attachment, no link, no Drive file named), call
  `picsart_media_upload({ accept: 'video', purpose: 'your screen recording' })` in that same turn,
  with one line on what happens once it is in. A greeting, a question about what you do, or a brief
  with no file all count. If the host cannot show the upload, follow video-core's host notes.
- A link the user pasted, or a file in their Picsart Drive: bring it in as video-core's Asset URLs
  say. Every tool below reads the recording by the URL that comes back.
- **What the user already said:** the product, the audience, the length or the platform, a
  presenter, the sound. Never ask again for any of it. The product and the audience, if they don't
  say, you infer from the stills and confirm with the spec.
- **The format:** 9:16, 1080×1920, 30 fps. A promo or a re-cut runs 20–40 s, 30 unless the user
  asks otherwise. A timelapse runs as long as its stages and its result take.

**The ASK waits for the moments.** Call `picsart_media_screen_moments` first, after stage 2's SPEND if
it applies: the moments say what the recording is, in `tier` and `input`. Then ask only what is
still open, all in one turn:

| Ask when | The question |
|---|---|
| the presenter can be offered (below) | "No presenter" / "Use my own photo" / "Generate a presenter" |
| `input.hasAudio`, and the tier is not `recut` | the recording's own sound: "Mute it" / "Keep it where a clip plays at normal speed" |
| the tier is `recut` | what to make of an edited video (below) |
| the user named neither a length nor a platform, for a promo or a re-cut | the length: "30 s" / "20 s" / "40 s" |

When nothing is open, don't ask: say in one line what the promo will be (the tier line of stage 2),
and go on.

- **The presenter.** Offer it only when the talking-head, voice-over and captions skills are all
  available to you: a package leaves them out where a tool they need is not deployed. If they
  choose their own photo, open `picsart_media_upload({ accept: 'image', purpose: 'a portrait photo of you' })`.
  If the user asks for a presenter where those skills are not available, say that a presenter is
  not available here, and offer the promo without one.
- **The recording's own sound.** Say with the question what keeping it means: a kept sound only
  plays under clips at 1×, because the promo cuts the waits, speeds the work up, and its jump cuts
  chop speech; everywhere else the promo is silent, and a timelapse is silent until its result
  holds. The recording is never transcribed, so a kept
  voice is not captioned. The answer is the spec's `sourceAudio`. A presenter's voice replaces it
  (stage 5).
- **An edited video** (`tier: "recut"`, `input.edited`). Tell the user in one line: "This is already
  an edited video, not a raw recording, so I'd re-cut its screen shots under new text." Then ASK:
  "Re-cut it, muted" / "Re-cut it, and keep the sound where a shot plays untouched" (only when
  `input.hasAudio`) / "Stop here". On "Stop here", say that a raw screen recording gives the other
  two shapes, and stop. `references/spec.md` says how a re-cut's spec differs.

## 2. Read the recording

Read it as the screen-analysis skill says: the moments first, then still sheets of the moments
that matter, and for a long session or a long shot its stages. The recording is never sent to a
model that watches video.

**Moments already read in this session are not read again.** When this recording's moments came
in earlier in the session (a tutorial made from it hands them over, with its approved steps as
candidates), use them as they are: no SPEND and no second `picsart_media_screen_moments` call. Read
only the still sheets you still need.

Read the description of each tool you will call before the first call. When video-core's SPEND
says any of them charges, quote the whole read in one go before the first call: the moments, the
stills sheets (about four), and the stages where they are needed, with one retry in case a call
fails. When none of them charges, say in one line that you are reading the recording, and go on. If the user declines, say that the promo cannot be built without reading
the recording, and stop.

If a read fails twice, tell the user the service is down and to try again shortly. Never guess
what the recording shows.

**The tier.** Take the tier the moments suggest in `tier`, with its reason in `tierReason`, check
it on the first sheet, and tell the user in one line which shape the promo will take and why:
"Your recording is four requests and their results, so each request is typed over its result."
When the sheet disagrees, believe the sheet, and say which shape you took instead. A timelapse
gets no proposed steps from the moments: its stages take their place.

**The shape.** `input.orientation` sets the layout, as the layouts skill says: a portrait
recording fills the frame, with no card on a backdrop, and a square one fills its width. When it
isn't landscape, say so in the same line: "It's already vertical, so it fills the frame."

## 3. Write the spec

Write it as `references/spec.md` says: the steps to keep, each request as the viewer should read
it (or a feature line where nobody typed one), the hook and the call to action; for a timelapse,
the chapter words, the process box and the result; for a re-cut, the shots to keep and a feature
line for each. **Never invent what the recording doesn't show**: every step, request, feature
line and chapter comes from a still you read. If the user names a step that isn't on screen, drop
it and say so.

**The words' language** is the user's own, unless the words in the recording (in its app, in its
captions) are in another: then ask which, in this ASK. Every word on screen is in that one
language, in a face that draws its script (`references/spec.md`).

**SHOW what the build will land on, before the ASK**, so a wrong result is caught here and not at
the check:

- for a promo or a re-cut, the sheet of the results you kept;
- for a timelapse, a sheet cropped to the process box at three moments across the work, which is
  what its card will show, and a sheet cropped to the result's box at `reveal.at` and just before
  `reveal.until`, with the result's time in the recording.

Then show ONE compact table, and ASK in one turn:

- above the table, three lines to confirm: the product, the audience and the call to action;
- the table: for a promo, each step with what it shows, its prompt lines or feature line, and its
  time in the recording; for a re-cut, each shot kept with its feature line and time, then the
  shots left out; for a timelapse, each chapter word with its range in the recording, then the
  result's time;
- the hook: 2–3 candidate hooks as options;
- the words' language, only when the recording's differs from the user's: the user's language /
  the recording's;
- with a presenter: the voice, whether the face is theirs or generated (for example "Warm woman,
  American" / "Calm man, British"), and where the presenter appears, "Hook only" / "Presenter in
  the steps too" (one longer take, see talking-head);
- "Looks good, make it" / "Change something". The yes covers the three lines, the table and the
  stills.

Revisions here are free; iterate until they approve.

## 4. Build the promo

Build it with the script in this skill's folder. Run it; never work the scene out yourself.

1. Write `{ kind, spec, moments }` to a file, as `references/spec.md` says, with `clip: "mask"` in
   the spec and `moments` exactly as `picsart_media_screen_moments` returned it.
2. From this skill's folder, run `python3 scripts/promo_scene.py <file>`. It prints one JSON line:
   the scene, its length, a timeline of its parts and diagnostics. It lays the recording out by
   its shape, as the layouts skill says. It frames each panel and keys each push with the layouts
   skill's `framing.py` and `panels.py` and the screen-zoom skill's `zoom.py`, which ship beside it
   in `scripts/`; run only `promo_scene.py`.
3. If it exits with an error instead, its one line names the field it cannot build from. Fix
   that field, and run it again.

Building is free and calls no tool. **Where you cannot run Python**, say that the promo cannot be
built here, and stop: the scene is too long to write by hand.

**Act on every diagnostic before you look at anything else.** Each has a `level`, a `code`, the
`layer` it is about when there is one, a `message`, and a `fix`: the change to make in the spec.

- **`error`:** the scene is wrong. Make the change its `fix` names, and build again. Never patch
  the scene to get past one.
- **`warning`:** the scene plays, but something in it may read wrong, such as a kept sound under a
  clip the build sped up. Make the fix when it keeps what the user approved. Otherwise keep the
  spec, look at that moment in stage 6, and tell the user in the review line what they will notice.

If an `error` is still there after two builds, tell the user plainly what it says and what you
changed, and stop there.

When the user's later comments change what the promo shows or says, change the spec and build
again, then add the presenter's layers again if there is one. When they edited the scene in the
editor, their document replaces yours (video-core): patch it instead of building again. Patch by
hand only for what the spec cannot say, keeping to the layouts and scene-compose skills: a new
panel's framing comes from the layouts skill's script, and its push from the screen-zoom skill's.

## 5. The presenter, when chosen

The voice lines and the on-camera takes cost credits, and nothing is generated before the yes.
Write the lines as `references/script.md` says, fitted to the built timeline. Read the inputs of
the voice model and of `kling-avatar` with `picsart_model_params`, then SPEND once for everything:
a generated portrait, only if the user chose one, as one call for four candidates (talking-head);
one voice line per script line, the same voice throughout; a take for the hook, and one on the
whole step narration if the presenter is in the steps. Quote each item with `picsart_preflight`. A
take needs its voice line and its portrait, which don't exist yet: if preflight cannot price a take
without them, give the number of takes and say that their amount is not known in advance, as
video-core's SPEND allows. Describe a generated presenter in the quote in one line (who they are,
what they wear, what is behind them), so the user can change them before paying.

An uploaded photo is checked as the talking-head skill says before the quote. When it fails, say
in one line what fails, and ASK: "Another photo" / "Generate a presenter".

The presenter's voice replaces the recording's own sound: build with `sourceAudio: "mute"`, and if
the user had kept the sound, say so in the quote.

After the yes, generate the portrait and the voice lines first, with `picsart_generate`, and tell
the user the presenter takes a few minutes. Check a generated portrait's candidates as the
talking-head skill says, SHOW the one that passes, and ASK: "Use this presenter" / "Try another". Another is the
next candidate that passed or, when none is left, a new portrait call with its own SPEND. Generate
the takes only after "Use this presenter". Then:

1. Build again with `hook.duration` set to the hook line's length, so the take fits the hook.
2. With `picsart_media_patch_scene`, add the hook take full frame over the hook, and the step take
   as a head bubble in the panel corner the step's result never reaches (talking-head). A take on
   screen plays its own line, unmuted. A voice line gets its own audio layer only where no take of
   it is on screen, such as an outro on a text card (scene-compose).
3. A screen promo is watched muted, so caption the whole voice-over, in the top band above the
   prompt bubble (captions).

If the user won't spend and had chosen more than the hook take, offer the smaller set once: the
hook take only. If they decline that too, go on without a presenter; the promo stands on its own.

## 6. Check it

The build does not pass through `picsart_media_patch_scene`, so validate it with
`picsart_media_validate_scene`, then check it with evaluate. Take the moments from the build's
timeline, at most 8 to a contact sheet:

- the hook;
- the last half second of each step, where the push has landed and the result holds;
- the outro grid;
- for a timelapse, one moment inside each chapter, and the result's hold;
- the moment each warning you left in is about.

**Masks first.** The first contact sheet must include a panel. If it fails with `the authored mask
carries no clip`, masks are not rendering here (the layouts skill has the dated fact). Build the
same spec again with `clip: "nest"` and check that build instead. Keep both: REVIEW opens the mask
build and the nest build is the one that renders, as the layouts skill says.

The questions, for a promo:

- Is each result inside its panel, and is its text readable at 1080 wide?
- Is each request fully typed before its result lands?
- Does each grid cell show the result, not the chat or the card around it?
- Is any text sitting on white?
- Does a push cut a card's header mid-word?
- Does every character of the words draw, accents included, with no box or gap?

For a portrait or square recording:

- Does it fill the frame (a square one, the frame's width), with no empty band at an edge?
- Does the text sit on the recording's quiet area, off its content and off any captions burned
  into it?

For a re-cut:

- Does each step open and end inside its own shot, never on a frame of the next one?
- Does each step show the screen, not the person on camera?
- Do the hook and each grid cell show their step's result, not the next shot?

For a timelapse:

- Does the process card show the work, not the app's panels?
- Does each chapter word match what its stages show?
- Does the result hold on the finished picture, not on an empty render window?

**Judge legibility on a still, not on softness alone.** On 2026-09-30 the Dev contact sheets drew
the playing steps much softer than the held hook, while a still of the same part of the recording
was sharp. When a step looks soft, crop a `picsart_media_video_stills` sheet to the result's box at that
moment. If the still is sharp, the recording is legible: say the sheet is soft, and never push
harder to fix it (screen-zoom). A nested panel renders softer than a masked one (layouts), so when
you deliver a nest build, say its moving steps are softer than they will be once masks render.

## 7. The user reviews

REVIEW the mask build, titled "<Product> promo — draft 1", with one line on what to look at: for a
promo, "Check each request reads before its result lands; trim anything that drags"; for a
timelapse, "Check the chapter words match the work; say where it drags"; for a re-cut, "Check each
shot opens on its own picture; trim anything that drags". With the recording's sound kept, add
where it drops out. Each new draft's number goes up by one.

## 8. Music, when wanted

A promo only; a timelapse ends on its own result. A promo that keeps the recording's own sound gets
no bed: say so and go on.

**Offer it once, after the draft is approved**, and never bare ("do you want music?"). ASK with the
bed's brief drafted as the music-bed skill says, and in the same brief two short sounds: one under
each push onto a result, one as the outro starts. Three exits: **generate it, change the brief, or
skip**. A changed brief is redrafted and asked again; a skip is settled for the session.

On a yes, the bed and the two sounds are one SPEND, as video-core says: the bed's model as the
music-bed skill picks it, the sounds from a sound-effects model in `picsart_model_catalog`, each
under 1 s, read with `picsart_model_params`. Then:

1. Build again with the spec's `sfx` set to the two sounds (`references/spec.md`), so they land on
   the build's own pushes.
2. Add the presenter's takes again, if there is one, as stage 5 does, and lay the bed under the
   scene with the music-bed skill's script, which dips it under each take's line. With no
   presenter there is no speech, and the bed plays level.
3. Validate and look at the contact sheet as stage 6 does, and REVIEW, titled
   "<Product> promo — music", with one line on what to listen for: how the bed sits under the
   voice, or under the pushes when there is no presenter. A note on its level moves it as the
   music-bed skill says; a different track goes back through the music-bed skill's brief, with a
   new SPEND.

If the bed or the sounds fail or are declined, say so in one line and go on with the approved
draft.

## 9. Export and deliver

DELIVER the approved build: the mask build if masks rendered in stage 6, otherwise the nest build
of the approved spec. If the user edited the scene in the editor and masks do not render, their
edits exist only in the mask build. Export it anyway. If the export fails on its masks, say so
plainly, and offer the nest build of the approved spec, naming the edits it leaves out.

Say what the promo sounds like when you deliver:

- no presenter, and the recording's sound muted or absent: the promo has no sound, and a track can
  be added when it is posted;
- the recording's sound kept: it plays under the clips at normal speed, and the promo is silent
  where the build sped the recording up or cut it;
- a presenter: the voice-over, captioned;
- music: the bed under everything, dipping under the presenter's lines, and a sound on each push,
  with the music-bed skill's licence caveat.

With a presenter, deliver as the talking-head skill's Check says.

The next step to offer: another platform's length, or a different hook.
