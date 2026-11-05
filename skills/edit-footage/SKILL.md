---
name: edit-footage
description: Make videos from the user's own footage, or copy a reel's structure onto their script - a vertical reel, podcast clips, a highlight reel, a montage, a photo slideshow, a lesson filmed to camera, split-screen podcast shorts, B-roll under a voice-over, an interview with B-roll, or a remix of a reference reel (a talking head or a skit included) - cut on the words, checked, choices shown as A/Bs. Use for "edit my footage", "edit my video", "make a reel from this", "remix this reel with my script". Not for a screen recording, a short film from a script or idea with no reference reel (movie-producer), or rebuilding a reference's animation with the user's photos (recreate-video).
metadata:
  uses: edit-pipeline, reel-structure, footage-analysis, footage-reframing, speech-aware-cutting, retention-hooks, realistic-color-grade, background-music, scene-building-basics, spoken-captions, quality-review, film-finishing, edit-on-your-computer, screen-recording-layouts, face-hiding, photo-slideshow, caption-decorations, quick-merge-and-export, screen-recording-zoom, film-cast-design, film-shot-generation, film-cutting, ai-presenter, voice-over-generation
  optional: realistic-color-grade, background-music, spoken-captions, edit-on-your-computer, face-hiding, photo-slideshow, caption-decorations, quick-merge-and-export, screen-recording-zoom, film-cast-design, film-shot-generation, film-cutting, ai-presenter, voice-over-generation
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

**Read the job's file whole before its first step**, and again when the work resumes in it. Its
steps are its own; never run another job's steps.

| Read this | Before you |
|---|---|
| `references/jobs.md` | say the job back at intake, and at every stage a job changes; start the record, or resume an old record |
| `references/reel-interview.md` | ask a reel job's interview questions |
| `references/reel-platforms.md` | place words on a reel job's frame, or deliver it |
| `references/reel-record.md` | write a reel job's own keys into the record |

## The flow

Every job runs these steps in this order. The row's number is the step in the edit jobs' text
below; in brackets are its record stage and the same step in the reel and remix texts, and a job
with no number there leaves it out. A gate or skill with jobs in brackets is only theirs:
`SPEND (remix)` opens for the remix job alone, `ASK (reel/remix)` for the reel jobs and the remix,
and `edit` names the edit jobs. `ASK (format-not-matched)` opens only when the footage cannot
reproduce an element of the reference's format; one reproduced exactly goes straight on. One with
no brackets is every job's. Before acting on a step, load
the skills in its row that are this job's, also when the work resumes there. Run the steps in one
go: after each, go straight on unless its row has a gate for this job.

| Stage | Gate | Skills |
|---|---|---|
| 1. Intake and the record (`intake`; reel 1-2, remix 1) | ASK | edit-pipeline, edit-on-your-computer, retention-hooks (reel) |
| 2. The reference: its sheet, its format, what the footage can match (`reference`; reel 2, remix 2-3) | SPEND (remix), REVIEW (remix), ASK (format-not-matched) | reel-structure, footage-analysis (remix) |
| 3. Read the footage (`log`; reel 3) | SPEND | footage-analysis, footage-reframing |
| 4. Takes, when someone speaks (`takes`) | ASK | speech-aware-cutting |
| 5. Look and sound (`look`) | ASK, SPEND | realistic-color-grade, background-music |
| 6. The map: the meaning map, the moments, or the script on the beats (`story`; reel 4, remix 4) | REVIEW (edit), ASK (reel/remix) | retention-hooks, speech-aware-cutting (reel), reel-structure (remix) |
| 7. Plan: the cut, the passes, the route (`plan`; reel 5-6, remix 5) | ASK (reel/remix) | edit-pipeline, speech-aware-cutting, screen-recording-layouts (remix), screen-recording-zoom (remix), ai-presenter (remix), photo-slideshow (remix), film-cast-design (remix) |
| 8. Build (`build`; reel 7, remix 6-8) | SPEND (remix), REVIEW (remix) | footage-reframing, scene-building-basics, spoken-captions, photo-slideshow (reel/remix), quick-merge-and-export (reel), face-hiding (reel), film-shot-generation (remix), voice-over-generation (remix), film-cutting (remix) |
| 9. The independent check and the reference match (`qc`; reel 8, remix 8) | ASK (reel) | quality-review, footage-reframing (reel) |
| 10. Critics, on the first full draft (`critics`; reel 8, remix 8) | — | quality-review |
| 11. Review (`review`; reel 9-11, remix 6-9) | REVIEW, ASK (edit/reel), SPEND (reel) | spoken-captions (reel/remix), caption-decorations (reel), screen-recording-layouts (reel), background-music (reel) |
| 12. Finish (`finish`; remix 9) | REVIEW (remix) | film-finishing, edit-on-your-computer, background-music (remix) |
| 13. Deliver (`deliver`; reel 12, remix 10) | DELIVER | reel-structure (remix) |

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
  only question at intake. Uploads and the free reads go on meanwhile; it never waits on the files.
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
  into the record's `cutPace` as the edit-pipeline skill says;
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
gates say. When there is no reference, use the job's default pace and say so.

## 3. Log the footage

When the footage is on this computer, make and upload the proxies first, as the
edit-on-your-computer skill says. Every tool below reads the sources from their URLs.

Log every source as the footage-analysis skill says, and for each one write into the record's
`sources`:

- what happens, who speaks and when (the free transcript), and which take is the voice-over;
- **steadiness per used range**, measured on a fixed detail with texture, as the edit-pipeline
  skill's gate rules say; low texture is `open`;
- legible text: notes, names, another firm's plaque;
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

- **Colour**: grade toward the colour reference or the brand, with the realistic-color-grade
  skill where the footage needs it. A custom camera LUT is not a scene look; when the footage is
  log, say so and grade it at the finish (stage 12).
- **Sound**: mixed in the scene as audio layers, never outside it: the voice placed on its
  lines, every audio layer given an explicit duration (one without it repeats), room tone under
  the cuts. Music follows the job's default in `references/jobs.md`; when it is offered,
  ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) with a rendered A/B, and quote any generation as the background-music skill says before
  its SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says).

## 6. The meaning map

Write the beats from the brief and the voice: for each phrase or beat, the picture's job, and the
shot that does it (hook and ending as the retention-hooks skill says). Start from the record's
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
shots hold at least the minimum, minor words are held through, no mouth moves under another
voice, and no two shots of one place and size are cut together. For a speaker, the talking
segments are cut as the speech-aware-cutting skill says. A rebuild starts from the keepers
ledger, never from zero. Run the edit-pipeline skill's `lock-check` on the plan before building,
and its meaning diff against the last version the user saw before showing anything.

## 8. Build the drafts

Build the scene as the scene-building-basics skill says: the montage, the voice, captions in the
brand font when the job has them (the spoken-captions skill), the end card. Validate it and export
a free draft, named by its version. A font the scene cannot load is surfaced; never substitute
one.

## 9. The independent check

Run the QC inspector on the render as the quality-review skill says, fresh each round, with the
keepers ledger and the meaning diff, for every job, a reel or a remix included. With a format in
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
with the meaning map beside it when it is not yet approved. Then the version: its name first, what
changed (the meaning diff's lines, one per change, a dropped keeper always among them), the check's
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
  full resolution, as the edit-on-your-computer skill says, with the grade applied there.

Then check the final master, whichever finish it is, before it is delivered:

- **Audio continuity**: no gap, click or doubled line at a cut; transcribe the master and compare
  it with the approved version's words.
- **Loudness**: about -14 LUFS with true peak under -1 dBTP, measured with the quality-review
  skill's `qc.py` where commands run. Without them it is `open`, said so in the delivery note;
  never spend credits on it.
- **Captions**: every line present, in sync, in the brand font, inside the safe zone.
- **Crop and safe zone**: nothing that matters cut off by the delivery shape or the platform's UI.
- **Grade**: matches the approved version, and holds across every cut.
- **Output spec**: the format, resolution, fps, codec and length asked.

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
