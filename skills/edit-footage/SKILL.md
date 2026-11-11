---
name: edit-footage
description: Make videos from the user's own footage, or copy a reel's structure onto their script - a vertical reel, podcast clips, a highlight reel, a montage, a photo slideshow, a lesson filmed to camera, split-screen podcast shorts, channel clips from a long video or its link in the look of a short you bring, B-roll under a voice-over, an interview with B-roll, or a remix of a reference reel (a talking head or a skit included) - cut on the words, checked, choices shown as A/Bs. Use for "edit my footage", "edit my video", "make a reel from this", "clip this podcast like my shorts", "remix this reel with my script". Not for a screen recording, a short film from a script or idea with no reference reel, or rebuilding a reference's animation with the user's photos (recreate-video).
metadata:
  uses: edit-pipeline, reel-structure, footage-analysis, footage-reframing, speech-aware-cutting, retention-hooks, realistic-color-grade, background-music, scene-building-basics, spoken-captions, quality-review, film-finishing, edit-on-your-computer, screen-recording-layouts, face-hiding, photo-slideshow, caption-decorations, quick-merge-and-export, screen-recording-zoom, film-cast-design, film-shot-generation, film-cutting, ai-presenter, voice-over-generation, motion-design-craft, motion-pattern-library, scene-template-remix, custom-transitions, linked-element-motion, visual-style, resting-frame-rules, motion-review, motion-tracking-from-video, social-posting
  optional: realistic-color-grade, background-music, spoken-captions, edit-on-your-computer, face-hiding, photo-slideshow, caption-decorations, quick-merge-and-export, screen-recording-zoom, film-cast-design, film-shot-generation, film-cutting, ai-presenter, voice-over-generation, motion-design-craft, motion-pattern-library, scene-template-remix, custom-transitions, linked-element-motion, visual-style, resting-frame-rules, motion-review, motion-tracking-from-video, social-posting
  title: Edit your footage
  short-description: Edit your footage into a reel, clips or a finished video
  argument-hint: '[your footage or script, a reference, a brief]'
  starter-prompt: Cut my footage into a 30-second vertical reel.
argument-hint: '[your footage or script, a reference, a brief]'
---

# Edit your footage

Everything made from the user's own footage runs here, and so does a reference reel's structure
copied onto their script. One intake picks the **job**, and the job picks the steps. The steps
share one record, one way to resume, and the same checks; what differs is which steps a job runs
and what each one makes.

## The jobs

Pick the job from the user's words, the footage, the reference and the brief, say it back in one
line, and keep it in the record's `job`. Ask only when two jobs fit equally. A command such as
/clips or /broll names its job; anything the user says wins over its preset.

| Job | What it makes | Its steps |
|---|---|---|
| `reel`, `highlight`, `podcast-clips`, `split`, `montage`, `slideshow`, `lesson` | one or several vertical shorts from talking footage, action or photos: the best moments, cut on the words; `split` stacks two speakers in a split screen, as the reference's format sets | `references/reel-flow.md`, with `references/reel-jobs.md` |
| `broll-voiceover`, `talking-broll`, `footage-story` | one finished video to a brief or a story found in it: B-roll under a voice-over, an interview with B-roll, footage with no words | the numbered sections below, with `references/jobs.md` |
| `remix` | a reference reel's structure (beats, shots, caption pattern, pace, bed) on the user's own script or topic, as slides, voice and video | `references/remix-flow.md` |
| `channel-clips` | several clips from one long video or a link to it, each in the look of a short the user brings (their channel's or anyone's): the moments, the frame, the hook card, the captions and the end card the look has, with a cover and post copy each, in one Drive folder, then the offer to post them; a reel job that asks two things at most | `references/clips-flow.md`, with `references/reel-jobs.md` and, for a pasted campaign brief, `references/clip-briefs.md` |

`channel-clips` is picked only when your identity names it as your job, or its /channel-clips
command names it. Otherwise it is never picked: a request for clips stays `podcast-clips` or
`split`, run as their own rows say.

**Read the job's file whole before its first step**, and again when the work resumes in it. Its
steps are its own; never run another job's steps.

| Read this | Before you |
|---|---|
| `references/jobs.md` | say the job back at intake, and at every stage a job changes; start the record, or resume an old record |
| `references/reel-interview.md` | ask a reel job's interview questions |
| `references/reel-platforms.md` | place words on a reel job's frame, or deliver it |
| `references/reel-record.md` | write a reel job's own keys into the record |
| `references/film-look.md` | choose an edit job's look, at the look stage, and before any grade |

## The flow

Every job runs these steps in this order. The row's number is the step in the edit jobs' text
below; in brackets are its record stage and the same step in the reel and remix texts, and a job
with no number there leaves it out. A gate or skill with jobs in brackets is only theirs:
`SPEND (remix)` opens for the remix job alone, `ASK (reel/remix)` for the reel jobs and the remix,
`channel-clips` names the clips job alone, and `edit` names the edit jobs. `ASK (format-not-matched)` opens only when the footage cannot
reproduce an element of the reference's format; one reproduced exactly goes straight on.
`SPEND (someone-speaks)` opens only when someone speaks, for the heard script's cold read; a job
with no speech goes straight on. `edit-on-your-computer (on-disk)` loads only for footage on
this computer, and `ASK (gyro)` opens only when its camera also recorded gyro data. A skill
marked `(style)` loads only for a reel job on Vibe Cut (`references/reel-flow.md`, Which cut), built in
the style the agent picks from the reel-structure skill's style library with no question, and then
only those the picked style's Skills field names. A skill marked `(reference)` loads only when the user gave a reference video: its
moves are measured when it is read, and measured again on the build to check them. One with
no brackets is every job's. Before acting on a step, load
the skills in its row that are this job's, also when the work resumes there. Run the steps in one
go: after each, go straight on unless its row has a gate for this job.

| Stage | Gate | Skills |
|---|---|---|
| 1. Intake and the record (`intake`; reel 1-2, remix 1) | ASK | edit-pipeline, edit-on-your-computer (on-disk), retention-hooks (reel) |
| 2. The reference: its sheet, its format, what the footage can match (`reference`; reel 2, remix 2-3) | SPEND (remix), REVIEW (remix), ASK (format-not-matched) | reel-structure, footage-analysis (remix), motion-tracking-from-video (reference) |
| 3. Read the footage (`log`; reel 3) | SPEND, ASK (gyro) | footage-analysis, footage-reframing, edit-on-your-computer (on-disk) |
| 4. Takes, when someone speaks (`takes`) | ASK | speech-aware-cutting |
| 5. Look and sound (`look`) | ASK, SPEND | realistic-color-grade, background-music |
| 6. The map: the meaning map, the moments, or the script on the beats (`story`; reel 4, remix 4) | REVIEW (edit), ASK (reel/remix) | retention-hooks, speech-aware-cutting (reel), reel-structure (remix) |
| 7. Plan: the cut, the passes, the route (`plan`; reel 5-6, remix 5) | SPEND (someone-speaks), ASK (reel/remix) | edit-pipeline, speech-aware-cutting, screen-recording-layouts (remix), screen-recording-zoom (remix), ai-presenter (remix), photo-slideshow (remix), film-cast-design (remix) |
| 8. Build (`build`; reel 7, remix 6-8) | SPEND (remix), REVIEW (remix) | footage-reframing, scene-building-basics, spoken-captions, photo-slideshow (reel/remix), quick-merge-and-export (reel), face-hiding (reel), film-shot-generation (remix), voice-over-generation (remix), film-cutting (remix), motion-design-craft (style), motion-pattern-library (style), scene-template-remix (style), custom-transitions (style), linked-element-motion (style), caption-decorations (style), visual-style (style), motion-tracking-from-video (reference) |
| 9. The independent check and the reference match (`qc`; reel 8, remix 8) | SPEND, ASK (reel) | quality-review, footage-reframing (reel), resting-frame-rules (style), motion-review (style), motion-tracking-from-video (reference) |
| 10. Critics, on the first full draft (`critics`; reel 8, remix 8) | — | quality-review |
| 11. Review (`review`; reel 9-11, remix 6-9) | REVIEW, ASK (edit/reel), SPEND (reel) | spoken-captions (reel/remix), caption-decorations (reel), screen-recording-layouts (reel), background-music (reel) |
| 12. Finish (`finish`; remix 9) | REVIEW (remix) | film-finishing, edit-on-your-computer (on-disk), background-music (remix) |
| 13. Deliver (`deliver`; reel 12, remix 10) | DELIVER | reel-structure (remix), social-posting (channel-clips) |

Every question is asked as picsart-video-rules's Asking says: one per turn, the recommended answer
first, each option saying what it changes. The step names are your bookkeeping, never the user's.

## The record

The record is the edit-pipeline skill's, named `edit-footage.json`, kept where that skill says: on
disk, in Drive or in the conversation, the same keys in each, for every job. Its `pipeline` is the
job's record stages, from `references/jobs.md`. **On every start, read it first**: when it exists
or the user pastes it back, load the edit-pipeline skill, find where to resume as it says (its
`status` where commands run), say where you resume in one line, and go on from there. Never redo a
stage the record shows as done and current.

A record from before the use cases were merged is the same project: continue it, never restart
it, and save it under the new name with `useCase: "edit-footage"`. That holds for
`client-edit.json`, `cut-footage-into-reel.json` and `remix-reel-structure.json`. Where commands
run, the edit-pipeline skill's `record.py migrate` does it, and says which stages are done; by
hand, mark done what the old record shows as done, as `references/jobs.md` says.

## The edit jobs: broll-voiceover, talking-broll, footage-story

The user hands over footage, often with a brief and a brand, and expects the film they described. Most of
the work that goes wrong goes wrong between rounds: a shot swapped for a steadier one loses what
it meant, a note given once is forgotten by the next fix, and a check passes a shake it could not
see. So this runs as one pipeline, as the edit-pipeline skill says. Every stage leaves an
artifact, the project record keeps every decision, and the work resumes from the record, not from
memory. The user never has to drive the stages; they answer questions and choose between renders.

## 1. Intake and the record

- **Read everything the user sent before the first question**: the brief, the deck, the brand
  pack (logo, fonts, colours), any colour or reference reel, and their channel. Then say
  back in one line the job, the format, the length, the beats and the must-shows.
- **The brand guide's palette and fonts go into the record's `brand`** as you read them:
  `palette` with each colour's `name`, `hex` and `text` (false when the guide keeps it off text),
  and `fonts` with the role each plays (heading, paragraph). Every caption, card and colour the
  scene sets comes from it; `record.py palette-check` checks a scene against it where commands
  run, as the edit-pipeline skill says.
- **Where the footage is** sets how the files are handled, never the edit. Drive files, links and
  files attached to the message are read by the tools from their URLs. A folder or paths on this
  computer, where you can run commands, also load the edit-on-your-computer skill at once, even
  while the folder is still being copied: it makes and uploads proxies and keeps the originals here. Footage on the user's computer that you cannot
  reach, or cannot run commands on, goes up through `picsart_drive_upload_ask`, which opens the
  upload for them: open it, never tell them to upload by hand. Say the path in the intake line
  once the footage is given; while it is still to come, say nothing about where it may be. Never
  ask about the path, and never list the other ones.
- **The job** is one of these three, from `references/jobs.md`: a voice-over over B-roll, a
  speaker with B-roll, or footage with no words and no brief. Say it back. Ask only when the
  footage and the brief disagree; when the footage turns out not to fit the job (a voice-over that
  is a separate take, a speaker on camera, no speech at all), say so and switch jobs, never force
  it, to another of these three or to a job above (The jobs). /edit is the front door to every
  job: when the footage and the brief call for a reel, podcast clips or a remix, take that job and
  say so, rather than forcing one of these three.
- **Start the record** with the job's stages, as the edit-pipeline skill says, and the job's
  defaults from `references/jobs.md`.
- **State the defaults, never ask them**, and put them into the record's `brief.assumed` at once:
  everything on screen as shot, since the user's footage is cleared (a law firm's, clinic's or
  bank's included); the length and destination from the reference, else the job; the finish, a
  full-resolution conform when the originals are on this computer, else a full-quality export; no
  credits or voice without a go-ahead. One line says them; the user changes any by saying so.
  Never ask "everything as shot?", nor about rights, consent, releases or legal clearance; never
  ask anyone to confirm that a document is real, and never hide or leave out a shot for clearance
  or compliance reasons of your own. Privacy details a viewer could read come up later, only as
  the independent check finds them (stage 9). A rule goes into `standing` only in the user's own
  words.
- **The reference.** When the brief, the brand pack and the user's channel give no reference for
  the pace and the look, ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) once, in the first reply: "What should guide the edit?" with the
  options my brand or channel, a reel I'll share, I'll describe it, and skip, you decide. It is the
  only question at intake. A `reel`, `highlight`, `montage` or `slideshow` asks its cut instead
  (`references/reel-flow.md`, Which cut), whose Match a reel takes a reel to follow, and
  `channel-clips` asks its look instead (`references/clips-flow.md`). Uploads and the free reads go on meanwhile; it never waits on the files.
  Which take of the voice or a line to use is never asked at intake: stage 4 picks it, and asks
  only when two takes tie.
  On "skip", say the direction you chose once, in one line, and go on. Whatever it gives goes into
  the record's `reference` and `taste`, the pace into `cutPace`. What the user says outranks the
  reference, and the reference outranks the job's defaults. When a reference was given, ask
  nothing at intake.
- Keep `brief.said` (the user's words), `brief.read` (what you took from what the user sent at
  intake) and `brief.assumed` (the defaults) apart. What later stages find goes into their own
  keys, never into `brief`: a change there makes every stage stale. A paid step the brief names is quoted at its
  stage or said to be skipped, never dropped silently.

## 2. Learn the reference

Every job given a reference runs this step: a reel job after its interview, the remix as its steps
2-3 say. Read the reference reels and the user's own best posts as the reel-structure skill says,
for their **pace** and their **format**, never their content:

- the pace: shot length, cuts per 10 s, caption style, colour, the first second and the ending,
  into the record's `cutPace` as the edit-pipeline skill says. A reference lends its devices
  apart from its tempo: when the brief names its register ("cinematic, atmospheric"), the tempo
  and `cutPace.rhythm` follow the brief, with `register` quoting its words;
- the sheet, with its Layout and each beat's Frame and Caption position;
- the format, into the record's `format`: the layout and who sits where, the emphasis, the
  captions' style and position, the hook, the end card. **The user's own channel is the spec**:
  its look is reproduced, its logo, fonts, end card and end-card words reused as given, never
  rewritten; a file you cannot take is asked for with `picsart_drive_upload_ask`. Another
  creator's reel lends its format only.
- what the footage can match: each element reproduced, approximated (say how) or impossible.
  Anything not reproduced: ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) with a rendered mock, one free frame of their footage in the
  format (`picsart_scene_contact_sheet`) beside the reference still. Everything reproduced: say so in one line and go on.

The step is done only with a sheet that passes and no element open, as the edit-pipeline skill's
gates say, and nothing is built before it is done. `record.py` refuses to mark the reference done
without its sheet and an answered format (`channel-clips`: the format alone); never mark it done by hand to get past that, since the
look, the story and everything after build on it. When there is no reference, use the job's
default pace and say so. A `highlight`, `montage` or `slideshow` on Vibe Cut is the exception: it
is built in the one best-fitting style from the reel-structure skill's style library, picked by
the agent without asking, and that style is the reference from here on, as
`references/reel-flow.md` says (No reference: a style); its sheet is free, with no read. The cut
names the style, and "Try another style" rebuilds it in the next best fit, reusing existing
assets and quoting any new charged operations as the reel flow says.

The reference keeps binding after this step. At every plan, the lock check holds the plan to the
reference's pace: every shot at or above `minHold` fails otherwise, and cuts per 10 s more than a
quarter off the reference's come back `open`. Say that before the build: a faster or slower cut is
the user's call, shown as an A/B against one at the reference's pace and recorded as an approval
scoped `format:pace`, unless a standing note of theirs already chose it. Compare the draft's
colour with the reference's too: when ffmpeg is on this computer, as the edit-on-your-computer
skill's colour comparison says; otherwise take stills of both with `picsart_media_video_stills` and
compare them by eye (brightness, saturation, warmth). A grade that drifts from the reference is
fixed at the look, before the review.

## 3. Log the footage

When the footage is on this computer, make and upload the proxies first and read the originals' gyro
data, as the edit-on-your-computer skill says. Every tool below reads the sources from their URLs.

Log every source as the footage-analysis skill says, and for each one write into the record's
`sources`:

- what happens, who speaks and when (the free transcript), and which take is the voice-over;
- **steadiness per used range**, measured on a fixed detail with texture, as the edit-pipeline
  skill's gate rules say; low texture is `open`;
- legible text: notes, names, another firm's plaque;
- **which way is up**, as `upright`: `yes`, `rot90` (it needs a quarter turn clockwise),
  `rot270` (a quarter turn anticlockwise), `rot180`, or `open`. Judge it from one still in the
  middle of the clip: writing and signs, verticals, the horizon, faces, a pour or a drip. Never
  from the file's rotation flag alone: some cameras (Sony's FX3 and A7S III among them) write
  none when held on their side. A turned source is turned before anything frames it: on this
  computer its proxy already carries the turn (the edit-on-your-computer skill's proxies), so the
  build lays it as it is; otherwise the build turns the clip layer before the reframe is
  measured. The reframe, the safe zone and every check read the turned frame. The conform turns
  the original, before its crop;
- what the shot can mean for the story, and its role (a second camera's shots may be inserts);
- whether the range needs stabilising. This is decided here, not after a check fails.

A describe of the footage charges credits: quote it and SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says), or say it is skipped and why.
The free reads never wait for it. The framing to the delivery shape is measured, checked and
corrected as the footage-reframing skill says.

## 4. Takes, when someone speaks

For a speaker, pick the best take of each line and the talking segments as the
speech-aware-cutting skill says. For a voice-over, pick its take. ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) only when two takes
are equally good and differ in what they say.

## 5. Look and sound

- **The look**: chosen from evidence, never left at a default, as `references/film-look.md` says:
  a board of stills from the brief's references and the client's own posts, a spec read from it
  (blacks, highlights, palette, texture, captions, the second camera, the ending), three
  candidate looks side by side on the hardest frames, and a check against the board. All of it
  goes into the record's `look` before this stage is done; the critics judge the draft against
  that board.
- **Colour**: grade toward the chosen look, with the realistic-color-grade skill only where
  the footage needs realism. A custom camera LUT is not a scene look. When log footage is
  on this computer, its proxies already carry the conversion to normal colour, as the
  edit-on-your-computer skill says, and the grade here is the look only. When log footage
  is anywhere else, say that previews look flat and grade it at the finish (stage 12).
- **Sound**: mixed in the scene as audio layers, never outside it: the voice placed on its
  lines, every audio layer given an explicit duration (one without it repeats), room tone under
  the cuts. Music follows the job's default in `references/jobs.md`; when it is offered,
  ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) with a rendered A/B.
  Quote any generation as the background-music skill says before its SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says).
  A track the user brings is received with `picsart_drive_upload_ask`.

## 6. The meaning map

Write the beats from the brief and the voice: for each phrase or beat, the picture's job, and the
shot that does it (hook and ending as the retention-hooks skill says). With the map, write its
viewer track, as quality-review's cold watch says: what a stranger must get, and by when, with the
questions to ask after watching; its questions are shown with the map, for correction. Start from the record's
`keepers` when there are any: a pairing the user saw work stays unless they chose otherwise. Show
With no speech and no brief, the story is provisional: infer one from what the footage shows, as
`references/jobs.md` says, and say it is a proposal.

Whenever a map, the moments or a mapping is shown, for any job with a reference format, show one
styleframe beside it: a free frame of the first beat built in the format, next to the reference
still at the same beat, so the user judges the look, not only the words.

The map is approved with the first draft, at stage 11, so the user judges a film, not a table.
Record that approval as the edit-pipeline skill says; delivery needs it.
Stop here for REVIEW only when the build cannot go on without the user's choice: two stories the
footage supports equally, or a must-show with no shot. Once approved, its rows are locked as the
edit-pipeline skill says; until then the plan follows the map as written.

## 7. Plan the cut

Plan every shot against the locked map and the record's `cutPace`: the cut lands just before its key word,
shots hold at least the minimum, each row names its `section`, the rhythm's long hold and breaths
are placed first and the quick cuts between them, minor words are held through, no mouth moves under another
voice, and no two shots of one place and size are cut together. For a speaker, the talking
segments are cut as the speech-aware-cutting skill says. A rebuild starts from the keepers
ledger, never from zero. Every shot carries its reason, as the edit-pipeline skill says. Run the
edit-pipeline skill's `lock-check` on the plan before building, and its meaning diff against the
last version the user saw before showing anything.
When someone speaks, have the heard script read
cold before the first build, as the speech-aware-cutting skill says, quoted first with its
SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says) (the row's `SPEND (someone-speaks)`; with no speech there is no read and nothing to ask): a story that does not survive
the read will not survive the build.

## 8. Build the drafts

Build the scene as the scene-building-basics skill says: the montage, the voice, captions in the
brand font when the job has them (the spoken-captions skill), the end card. Validate it and export
a free draft, named by its version. A font the scene cannot load is surfaced; never substitute
one.

## 9. The independent check

First the cold watch, as quality-review says, with `cuts: true` (the edit-pipeline skill's gate
rules), its calls quoted first as it says and a SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says) before round 1 unless every call is
quoted at 0 credits (on a no, the review line says "no cold watch yet"): strangers who know nothing watch the render a few seconds at a time and
say what they understood, who each person on screen is, and where a cut jumped.

Run the QC inspector on the render as the quality-review skill says, fresh each round, with
the cold watch's gaps,
the keepers ledger and the meaning diff, for every job, a reel or a remix
included. With a format in
the record it also gets the format, the reference stills and the reference match: a layout other
than the format's is critical. Fix its findings within the edit-pipeline skill's fix scope:
a range moved, or a shot with the same job; a clash with a locked row or a keeper goes to the user
as an A/B. Fix
rounds are capped as picsart-video-rules says.

A `legible-text` finding about someone else's private details (another person's name, address or
case note readable on screen) is never fixed silently and never ignored: show it to the user
once, as a rendered A/B of the shot as shot against it blurred or another range, and let them
choose. Record the choice in `standing` with their words, so it is not raised again.

## 10. Critics, on the first full draft

Once, on the first full draft, run the critic panel as the quality-review skill says, with the
reference stills and the format among its source stills when there are any. Its
must-fixes go into the plan; its taste choices, and any shot it would swap, wait for stage 11 as
rendered A/Bs, never a silent change.

## 11. Review

Show first the strongest complete draft that passed the check, never a partial or unchecked one,
opened cold as picsart-video-rules says. Once the user has answered, the meaning map beside it when
it is not yet approved, then the version: its name first, what changed (the meaning diff's lines, one per change, a dropped keeper always among them), the check's
verdict and anything open. Every taste choice is two rendered drafts side by side; ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) which,
never in words alone. Ask only the choices that change the film; take the rest as stated
defaults. A note
that holds everywhere becomes a standing decision; a note that changes a shot's meaning needs its
A/B first. Record the approval of the version for REVIEW, and add to the record's `keepers` what
worked in it and anything the user praised, in their words.

## 12. Finish

On the finish chosen at intake:

- **The export**: export the approved scene at the delivery resolution with `picsart_scene_export`,
  which is free, its sources the full-resolution files the user gave.
- **The conform**, when the originals are on this computer: rebuild the approved cut from them at
  full resolution, as the edit-on-your-computer skill says, with the grade applied there. This is
  the finish for footage on this computer unless the user asks for the export: a scene export of
  the proxies is a draft, never the delivery. Upload nothing more for it than a check that runs
  only on the server needs (a transcript of the master), and keep the master on this computer.

Then check the final master, whichever finish it is, before it is delivered:

- **Audio continuity**: no gap, click or doubled line at a cut; transcribe the master and compare
  it with the approved version's words.
- **Loudness**: about -14 LUFS with true peak under -1 dBTP, measured with the quality-review
  skill's `qc.py` where commands run. Without them it is `open`, said so in the delivery note;
  never spend credits on it.
- **Captions**: every line present, in sync, in the brand font, inside the safe zone.
- **Crop and safe zone**: nothing that matters cut off by the delivery shape or the platform's UI.
- **Grade**: matches the approved version, and holds across every cut.
- **Output spec**: the format, resolution, fps, codec and length asked, and only those: never a
  second size or version nobody asked for.

What could not be measured is `open` and said in the delivery note, never passed. A failure is
fixed in the finish and the master checked again.

## 13. Deliver

Never before the map was approved and the check, the critics and the review ran, for any job.
Never skip one on your own. When the user explicitly asks to skip one, say its risk in one line;
on their yes, record the skip as `skipped: user`, as the edit-pipeline skill says, and go on.
Then DELIVER the files, the cut list (order, source file or link, in, out, the phrase each shot serves) and a
short note the user can pass on. A file replacing one already delivered goes beside it; the old one is
removed only on a yes.

## When something fails

- A stage's tool fails: say which stage and why, and stop there; the record keeps the place.
- The footage cannot do what the brief asks (no shot for a beat): say which beat, with the
  closest shots, and ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) which to use.
