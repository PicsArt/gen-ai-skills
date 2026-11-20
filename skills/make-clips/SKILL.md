---
name: make-clips
description: Cut one long video into several standalone clips - podcast clips from a podcast, an interview or a talk, split-screen podcast shorts in your channel's format, or channel clips from a long video or its link in the look of a short you bring, a gameplay stream included - each clip one moment that stands on its own, picked for you from what is said and what is on screen, cut on the words, the speaker kept in frame, captions and a hook on, checked. Use for "clip this podcast", "make shorts from this episode", "clip this podcast like my shorts", "clips from this stream". Not for one video from the footage - a reel that tells one story, a highlight reel, a montage, an edit to a brief or a remix of a reference reel (edit-footage) - nor for a screen recording.
metadata:
  uses: edit-pipeline, reel-structure, footage-analysis, footage-reframing, speech-aware-cutting, retention-hooks, scene-building-basics, spoken-captions, quality-review, edit-on-your-computer, screen-recording-layouts, caption-decorations, social-posting
  optional: spoken-captions, edit-on-your-computer, caption-decorations, social-posting
  title: Make clips
  short-description: Cut one long video into several ready-to-post clips
  argument-hint: '[a long video or its link, a short to copy, how many]'
  starter-prompt: Cut this podcast episode into three vertical clips.
argument-hint: '[a long video or its link, a short to copy, how many]'
---

# Make clips

When you read `picsart_scene_capabilities` or the recipe index (`picsart_scene_recipe` without `name`), pass `useCase: "make-clips"`: the answer leads with what this job reads and names the rest in one line.

One long video becomes several clips, each one moment that stands on its own. A clip cut from
talking footage lives on its words. The framing can be perfect and the clip is
still unwatchable when it opens on half a sentence. So this works transcript first: what is
**said** decides where each cut falls, the picture decides what is worth keeping, and the person
talking stays in frame. A good clip feels like it was always that length: nothing load-bearing
removed, no dead air, no half-sentence hanging off either end.

**You pick the moments, not the user.** The user usually has not watched the whole video again
and cannot judge a moment from a line of description or a pair of times; you have read every
word and looked at the picture. So the moments, their edges, the count, the length and the look
of the words on screen are your call, made from the transcript and the picture, and the user
judges the finished clips. The questions left are the few only the user can answer: the video
when none came, the rights to it, and (for `channel-clips`) the short to copy when none is known.
Never ask which moments to use, where a clip starts or ends, how long it runs, how many to make,
who it is for or which version to build: decide, and say what you decided in one line.

In the steps below a **short** is one finished clip, and a clip is one range of the source laid
in it.

## The jobs

Pick the job from the user's words, the footage and the reference, say it back in one
line, and keep it in the record's `job`. Never ask it: when two jobs fit, take the first in the
table. A command such as /clips or /split-clips names its job; anything the user says wins over
its preset.

| Job | What it makes | Its steps |
|---|---|---|
| `podcast-clips`, `split` | several vertical shorts from one long podcast, interview or talk: each one moment ranked to stand on its own, cut on the words, no moment used twice, the speaker kept in frame; `split` stacks two speakers in a split screen, as the reference's format sets | the numbered sections below, with `references/jobs.md` |
| `channel-clips` | several clips from one long video or a link to it, each in the look of a short the user brings (their channel's or anyone's): the moments, the frame, the hook card, the captions and the end card the look has, with a cover and post copy each, in one Drive folder, then the offer to post them; it asks for the look only when none is known | `references/channel-clips.md`, with `references/jobs.md` and, for a pasted campaign brief, `references/clip-briefs.md` |

`channel-clips` is picked only when your identity names it as your job, or its /channel-clips
command names it. Otherwise it is never picked: a request for clips stays `podcast-clips` or
`split`, run as their own row says.

One video from the footage is not clipping: a reel that tells one story from several moments, a
highlight reel, a montage, a photo slideshow, an edit to a brief or a remix of a reference reel
is the edit-footage use case's. Say so in one line, and start that use case where you have it.

| Read this | Before you |
|---|---|
| `references/jobs.md` | say the job back at step 1, start the record, and whenever you set a count, a length, a goal or an audience |
| `references/platforms.md` | state the frame and the length, place any words, or deliver |
| `references/channel-clips.md` | run any step of the `channel-clips` job: read it whole before its first step, and again when the work resumes in it |
| `references/clip-briefs.md` | read a campaign brief the user pasted |

## The flow

Every job runs these steps in this order. The row's number is the step in the text below; in
brackets are its record stage and the same step in `references/channel-clips.md`, and a step with
no number there is not that job's. `social-posting (channel-clips)` loads for that job alone.
`edit-on-your-computer (on-disk)` loads only for footage on
this computer. One with
no brackets is every job's. Before acting on a step, load
the skills in its row that are this job's, also when the work resumes there. Run the steps in one
go: after each, go straight on unless its row has a gate for this job. `ASK (unreadable)` opens
only when one video of several cannot be read.

| Stage | Gate | Skills |
|---|---|---|
| 1. Take the video in, with the rights confirmation (`intake`; channel-clips 1) | ASK | edit-pipeline, footage-analysis, edit-on-your-computer (on-disk) |
| 2. The reference: its format, matched or approximated (`reference`; channel-clips 2) | — | reel-structure |
| 3. Read the footage: the words and the picture (`log`; channel-clips 3) | SPEND, ASK (unreadable) | footage-analysis, footage-reframing, edit-on-your-computer (on-disk) |
| 4. Pick the moments (`story`; channel-clips 4) | — | speech-aware-cutting, retention-hooks |
| 5. Plan the cut (`plan`) | — | speech-aware-cutting, edit-pipeline |
| 6. Build every clip (`build`; channel-clips 5) | — | footage-reframing, scene-building-basics, spoken-captions, caption-decorations, screen-recording-layouts, edit-on-your-computer (on-disk) |
| 7. Check it: the framing, the cold watch, the QC inspector (`qc`; channel-clips 6) | SPEND | footage-reframing, quality-review |
| 8. Critics, on the first full draft (`critics`; channel-clips 6) | — | quality-review |
| 9. Review every clip at once (`review`; channel-clips 7) | REVIEW | — |
| 10. Deliver (`deliver`; channel-clips 8) | DELIVER | social-posting (channel-clips) |

A question you do ask is asked as picsart-video-rules's Asking says: one per turn, the recommended
answer first, each option saying what it changes. The step names are your bookkeeping, never the
user's. Where a method skill would ask (the structure sheet, a feasibility row, which reframe
correction, a critic's taste choice), take its recommended answer and say it in one line at the
review.

**The challenger at each decision.** Before you go on from a decision, quality-review's challenger (the
`challenger` agent where the host has it) asks "why this?" of it: the moments you picked (step
4), the plan of each cut and its opener (5), and every quote before its SPEND (3, 7). Act on its
verdict yourself: a `rethink` changes your pick before anything is built; a `stop` on a quote
goes into that SPEND, the cheaper alternative first; any other `stop` is said in one line at the
review.

The one wait in the middle is the review (step 9): every clip is built, checked and shown
together, and the user judges them all in one reply. A step the user declined has no gate.

## The record

The record is the edit-pipeline skill's, named `make-clips.json`, kept where that skill says: on
disk, in Drive or in the conversation, the same keys in each, for every job. Its `pipeline` is the
job's record stages, from `references/jobs.md`. **On every start, read it first**: when it exists
or the user pastes it back, load the edit-pipeline skill, find where to resume as it says (its
`status` where commands run), say where you resume in one line, and go on from there. Never redo a
stage the record shows as done and current. Where commands run, every `record.py` call names this
record and this use case: `record.py init make-clips.json --use-case make-clips --job <job>
--stages <the job's stages>`.

A record named `edit-footage.json` whose `job` is `podcast-clips`, `split` or `channel-clips` is
the same project, from before clips had their own use case: continue it, never restart it, and
save it as `make-clips.json` with `useCase: "make-clips"`, its done stages kept as they are.

Beside the edit-pipeline skill's core keys, the record keeps:

- `job`: the job from The jobs, said back at step 1;
- `rights`: per source, the user's confirmation, its date and whether it was recorded;
- `brief`: `said` and `assumed`, kept apart, with the destination, the goal, the audience,
  the length and the number of shorts;
- `moments`: the picked ones, by source and range, each with why it was picked;
- `reframes`: per video, its saved reframe and its corrected file, as the footage-reframing skill says;
- `takes`: here each short's clip list, and for each short the latest approved scene URL;
- `openDecisions`.

## 1. Take the video in, with the rights confirmation

- **Read the user's brief first.** Every file in the material that is not media, read in full
  before anything else, as picsart-video-rules's The user's own brief says. A brief sets the
  message, the audience and the must-shows.
- **No video yet → ask for it in your first reply.** When the message carries no
  file, no link and no Drive file named, call
  `picsart_drive_upload_ask({ purpose: 'the video to clip', accept: 'video' })` in that same turn, with
  one line on what happens once it is in, and ask nothing else.
  If the host cannot show the upload, follow picsart-video-rules's `references/HOST.md`.
- A link the user pasted, or a file in their Picsart Drive: bring it in as picsart-video-rules's Asset URLs
  say, once the rights are confirmed. Every tool below reads the footage by the URL that comes back.
- A folder or paths on this computer, where you can run commands, also load the
  edit-on-your-computer skill at once: it makes and uploads proxies and keeps the originals here.
- "My episode" without naming it, with several in reach: ASK (with `picsart_ask`, found as picsart-video-rules says, for any closed choice, a multi-select included, so the options are buttons the user taps, the recommended one first; then your host's own question tool, such as AskUserQuestion; only where all fail, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) which file, never guess.

**The rights confirmation, for every new video, on every host.** Before clipping a video the
user did not record in this chat, they confirm their rights to it, and nothing of it is
downloaded for editing, cut or bought before they do. ASK (with `picsart_ask`, found as picsart-video-rules says, for any closed choice, a multi-select included, so the options are buttons the user taps, the recommended one first; then your host's own question tool, such as AskUserQuestion; only where all fail, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) it in the first message once the video is
named or in, before anything else, in the user's language and close to these words:
"Before I start, please confirm: you own this video, or its owner has given you permission
(or a license) to edit it and publish clips from it, including any music, footage and people
in it. Reply "yes" to confirm."
Ask it even when the request already says the video is theirs: only a reply to this question
counts. Only a clear yes does: "yes", "I confirm", "it's mine", "it's my podcast". "I think so",
"it's public", "it's on YouTube" or silence is not a yes: say in one line that a public video
is not permission, and ask once more. With the yes the user takes responsibility for what they
clip: never judge a source by what it shows or where it comes from, and never ask again for
that video.
Record each yes at once with `record_content_rights` where the host has it, else
with `picsart_rights_record` (the source as `link` or `upload`, the URL or file id as received),
and keep it in the record's `rights` and, where the host has one, your preferences memory, with
the date and the source. A confirmation that could not be recorded stops nothing and is never
asked again. A yes for one video never covers another. Keep to these words, so the user confirms
the same thing every time. On a no, do not clip it: say in one line that you clip only videos the
user owns or has the owner's permission to use. A reference short needs no confirmation: nothing
of it is cut.

**On the yes, pick the job** from The jobs, say it back in one line, and keep it in the record's
`job`. **Start the record** with the job's stages from `references/jobs.md`, as the edit-pipeline
skill says, and its defaults in `brief.assumed`. Say in one line what you will make (the number
of clips, the frame, the length, from the user's words or the defaults) and that you are reading
the video, which takes a few minutes. Then start the reads (step 3) at once, without another
question.

## 2. The reference: its format, matched or approximated

When the user gave a reference short or names their own channel's shorts, learn it now, beside
the reads; a `split` always has one. Read the reference and the user's own best posts as the
reel-structure skill says, for their **pace** and their **format**, never their content:

- the pace: shot length, cuts per 10 s, caption style, the first second and the ending,
  into the record's `cutPace` as the edit-pipeline skill says;
- the sheet, with its Layout and each beat's Frame and Caption position;
- the format, into the record's `format`: the layout and who sits where, the emphasis, the
  captions' style and position, the hook, the end card. **The user's own channel is the spec**:
  its look is reproduced, its logo, fonts, end card and end-card words reused as given, never
  rewritten. Another creator's reel lends its format only. The moments are then picked and cut to
  that format.
- what the footage can match: **feasibility is answered here, not asked.** Each element is
  reproduced, approximated (say how: "one speaker, so the split holds two framings of the same
  person") or impossible, and every element not reproduced is one line at the review. Nothing is
  asked about it before then: the user sees the approximation in the clips themselves. Mark each
  such row `"decided": "agent"` and write no `answer`: there is none.

The step is done only with a sheet that passes and no element open, as the edit-pipeline skill's
gates say, and nothing is built before it is done. `record.py` refuses to mark the reference done
without its sheet and an answered format (`channel-clips`: the format alone); never mark it done by hand to get past that, since
the moments and everything after build on it. When there is no reference, use the job's
default look from `references/jobs.md` and say so in one line.

The reference keeps binding after this step. At every plan, the lock check holds the plan to the
reference's pace: every shot at or above `minHold`, and cuts per 10 s within a quarter of the
reference's. Plan to it; a faster or slower cut is made only when the user asks for one.

## 3. Read the footage: the words and the picture

Every clip is picked from both what is said and what is on screen. Start every read at once, as
the footage-analysis skill says, all of them free:

- every video's probe and transcript, with its speakers;
- every video's `picsart_media_analyze_audio`, its default summary: laughter, raised voices and
  the loud stretches mark moments the words alone can miss;
- **the picture, from stills**: `picsart_media_video_stills` over the whole source, about 20
  `times` spread evenly and labelled with their times, so you know who is on screen, where they
  sit, and what else is shown (a slide, a screen, a product, a game, a second camera, a black or
  frozen stretch, a sponsor's card). Where the stills show cuts between cameras, run
  `picsart_media_segment_shots` over the windows you will cut from, at step 4;
- every video's measurement for the clips' frame, as the footage-reframing skill says, when the
  frame differs from the source's; that skill also checks it and corrects what the tool gets
  wrong. It needs only the source and the shape, so it never waits for the plan;
- for `split`, no measurement: the shots, one still per kind of shot, and the crops checked
  against the faces, as the footage-reframing skill's split layout says.

Talking footage needs no paid watch here: its moments are in its words, and the stills show its
picture. Where the footage-analysis skill would watch talking footage, this use case reads it from
the transcript and the stills instead.

**The paid watch only when the picture carries the content**: the transcript has almost no
speech, or the stills show that what matters is done rather than said (a demonstration, a
recipe, a sport, a game with no commentary, a reveal). Then quote
`picsart_media_describe_video` for those videos in one SPEND (quote it in one line, then get the yes with `picsart_ask`, found as picsart-video-rules says, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", else your host's own question tool, such as AskUserQuestion; never as a typed question unless both fail; only then those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says), as picsart-video-rules says,
with the brief's goal in its request. It gives no quote in advance, so say that it charges credits
and that the amount is not known before it runs. On a no, pick from the transcript, the sound and
the stills, and say in one line what that misses.

**The cut waits for every video's reads.** Each needs a transcript (or a clear "no speech") and
its stills. If one file of several cannot be read, say which, and ASK (with `picsart_ask`, found as picsart-video-rules says, for any closed choice, a multi-select included, so the options are buttons the user taps, the recommended one first; then your host's own question tool, such as AskUserQuestion; only where all fail, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) whether to cut from the
rest: that is the user's call, since that footage may have been the point.

**The reframe measurement is critical.** When it fails, do as its skill says, and the cut waits.

## 4. Pick the moments

Make one pool of moments across every source, as the speech-aware-cutting skill says, snapped to
whole thoughts and ranked for the goal and the audience (`references/jobs.md`: grow the audience
and new viewers, unless the user's words say otherwise), each to stand on its own, no moment used
twice. A moment the user named in their request is in without asking.

**Then look at each candidate.** `picsart_media_video_stills` at its opening line, its middle and
its last line, and `picsart_media_segment_shots` over its window where the source cuts between
cameras, so you know where its shots change:

- drop or move a moment whose picture fails it: the speaker off screen or turned away, someone
  eating or talking over a black frame, a slide or a screen that cannot be read in the clip's
  frame, a sponsor's card, a frozen picture;
- rank up a moment where the picture adds to the words: a reaction, a demonstration, a laugh on
  both faces, an object held up to the camera;
- never open a clip on a camera cut that lands a frame after the first word.

Take the strongest, as many as the count (`references/jobs.md`): three unless the user or a brief
named a number, fewer when the source has fewer moments worth a clip, said so in one line. Keep
each in the record's `moments` with why it was picked. The picks are not asked: the user judges
them at the review, in the finished clips.

## 5. Plan the cut

Plan each short as the speech-aware-cutting skill says, from its moment, and read the plan back
with its `scripts/review_cuts.py` until it is clean. **One finished version per short**, never a
tight, a target and a long take to choose from: its length is the one `references/jobs.md` sets,
and the sentence wins over the length.

Each short is a whole short, not a bare range of the source:

- **The hook first**: it opens on the line that raises the question, as the retention-hooks skill
  names it (a result, a claim, a problem said plainly), never on the payoff or a slow lead-up.
  When the strongest line sits a few seconds in, open on it and lay the setup after it.
- **The filler cut**: the filler and dead air `review_cuts.py` flags inside it; nothing
  load-bearing removed.
- **The end**: on a closed thought, its payoff inside the clip; the end card where the look has
  one.
- **The words on screen**: captions on, the hook card carrying the opening line word for word,
  and the hook line highlighted; the phrases the spoken-captions skill would pick are marked in
  the plan.

## 6. Build every clip

The shorts are independent: run each stage's calls for all of them together, then the next
stage.

Build each short with the footage-reframing skill's `scripts/reel_cut.py`, from the plan
speech-aware-cutting wrote and the measurements kept in the record. Where you cannot run commands,
stop here as picsart-video-rules says for a script that builds the scene. The footage-reframing
skill says which clips follow their speaker, which show the whole frame, and how the seams are
cut.

The words, as the spoken-captions skill says: captions word-timed and on, in the band
`references/platforms.md` gives; the hook card with the opening line, at most three lines; the
hook line highlighted where it is spoken, and at most one more highlight where a line earns it,
checked as the screen-recording-layouts skill's safe zone says. A highlight look the
spoken-captions skill does not give (a box, a sticker, a marker sweep), or a decoration that does
not show or lands at the wrong time, is authored as the caption-decorations skill says. With a
format in the record, the format's caption style, hook card and end card win over these defaults.
Nothing is written that was not said.

A `split` short is built as the footage-reframing skill's split layout says, then its word cards
on the seam and its hook card with the spoken-captions skill, all from the record's `format`.
Its full-frame moments come from the locked map, never from the picture. Where you run commands
and the episode is long, upload one window per short, as edit-on-your-computer says.

Validate each scene as the scene-building-basics skill says and export a free draft of each,
named by its number and its hook line. A font the scene cannot load is surfaced; never substitute
one.

## 7. Check it: the framing, the cold watch, the QC inspector

Check each short's framing as the footage-reframing skill says. Then check it as the quality-review skill says: at
each seam and each clip's middle, the picture is the clip the plan names. Fix the plan, the clip or the
framing and build again.

Then the cold watch, as quality-review says, with `cuts: true` (the edit-pipeline skill's gate
rules), its calls quoted first as it says. When every call is quoted at 0 credits it runs on
every short without asking; otherwise it runs only on a SPEND (quote it in one line, then get the yes with `picsart_ask`, found as picsart-video-rules says, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", else your host's own question tool, such as AskUserQuestion; never as a typed question unless both fail; only then those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says) before round 1, and on a no the
review line says "no cold watch yet": strangers who know nothing watch the render a few seconds at
a time and say what they understood, who each person on screen is, and where a cut jumped.

Run the QC inspector on each short's draft as the quality-review skill says, fresh each round, with
the cold watch's gaps,
the keepers ledger and the meaning diff. With a format in
the record it also gets the format, the reference stills and the reference match: a layout other
than the format's is critical. Fix its findings within the edit-pipeline skill's fix scope:
a range moved, or a shot with the same job. Fix rounds are capped as picsart-video-rules says.

A `legible-text` finding about someone else's private details (another person's name, address or
case note readable on screen) is never fixed silently and never ignored: show it at the review,
as a rendered A/B of the shot as shot against it blurred or another range, and let the user
choose. Record the choice in `standing` with their words, so it is not raised again.

## 8. Critics, on the first full draft

Once, on the first full draft of the strongest short, run quality-review's critic panel (the six
`critic-*` agents where the host has them), with the transcript's lines as the words and a still
of each clip in its source as the source stills, the reference stills beside them when a format
was read. Make its must-fixes in the plan and build again, and carry every fix that is not about
that one moment to the other shorts. Take each of its `choices` as its recommendation, never
asked, and say each in one line at the review.

## 9. Review every clip at once

When every short is built and checked, show them all together, never one at a time: build their
drafts into one scene with `picsart_scene_apply_template` (template `scene://montage`, mode
`bootstrap`), in the order you would post them, and REVIEW it in the editor, titled
"<Topic> clips", as picsart-video-rules says. The review line names each short by its number: its
hook line quoted, where it comes from in the source, and in a few words why it is in. Then one
line for anything you approximated, a critic's choice you took, or a check you could not run.
That scene is only for the review and is never exported or delivered.

The reply judges the moments and the cuts at once. A yes approves every short: record it as an
approval scoped `moments`, and the review as done. A change is said in plain words and by number
("2 runs long", "swap 3 for the part about pricing", "start 1 on the joke"): find the words in the
transcript and move the edges yourself, build that short again, check it, and show only the
changed ones, the same way. Never answer a note with times to pick from. A note that is not about
one short applies to every short. A trim or a timeline comment on one short in the review scene
is read back onto that short: its edges planned again on the words, its own scene built again. The
user's own trim stands, as picsart-video-rules says; flag only one that breaks the short, such as a
clip trimmed to nothing.

## 10. Deliver

Only after the check, the critics and the review. Never skip one on
your own. When the user explicitly asks to skip one, say its risk in one line;
on their yes, record the skip as `skipped: user`, as the edit-pipeline skill says, and go on.
Then DELIVER every approved short, each exported from its own scene with the review's changes
made in it, each SHOWn playable with its hook line as its title, the strongest first. Say in one line
what they sound like: the speakers' own voices. A file replacing one already delivered goes
beside it; the old one is removed only on a yes. Then offer one next step: another platform's
length, or more clips from the moments left. Posting is offered for `channel-clips` alone, as the
social-posting skill says (`references/channel-clips.md`).

## When something fails

- **A read fails.** Its skill's retry, then stop that part and say so; never guess what the footage
  holds.
- **Almost no speech.** Say so in one line, and pick from the picture as step 3 says.
- **Out of credits.** Say which part is paused and what it needs, and offer what can be done
  without it, based on the remaining operations and their billing contracts.
- **A failed export.** Retry once. If it fails again, say so, and keep the approved scene so it
  can be exported later.
