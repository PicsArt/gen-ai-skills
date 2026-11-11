# The remix job: a reference's structure on the user's own script

Read this whole file when the job is `remix` (SKILL.md, The jobs). Its steps are the remix
steps of SKILL.md's flow table, in this order.

## Contents

- Not recreate-video
- The record
- Content rules
- 1. Take it in
- 2. Read the structure
- 3. The structure sheet
- 4. Map the script
- 5. Route by format
- Build in stages: slides, voice, video
- 10. Report and deliver
- When something fails


A reference reel lends its **structure**; the user's video keeps its own **content**. The
structure and length come from the reference, the channel's look from the user's house style,
and the words, people and screens from the user's script. Nothing the viewer can see or hear of
the reference reaches the result.

Read picsart-video-rules first. The method (the read, the sheet, the mapping and the report) is
the reel-structure skill's; this job decides, asks and builds.

Before acting on a stage, load the skills in its row that apply to this job, also when the work resumes there.

| Stage | Gate | Skills |
|---|---|---|
| 1. Take in the reference, the script or topic, and the house style | ASK | — |
| 2. Read the structure, or parse a breakdown for free | SPEND | reel-structure, footage-analysis |
| 3. The structure sheet and the content rules | REVIEW | reel-structure |
| 4. Map the script onto the beats, with the matched/changed report | ASK | reel-structure, retention-hooks |
| 5. Route by format | ASK | screen-recording-layouts, screen-recording-zoom, ai-presenter, photo-slideshow, film-cast-design |
| 6. `slides`: a still per beat, captions in the reference's pattern and the house style, no sound | SPEND, REVIEW | film-shot-generation, scene-building-basics, spoken-captions |
| 7. `voice`: locked voices, paced to the sheet's words per second | SPEND, REVIEW | voice-over-generation |
| 5. Route by format, from the user's own media | ASK | screen-recording-layouts, screen-recording-zoom, photo-slideshow, footage-analysis |
| 6. `slides` from the user's stills or frames, captions in the reference's pattern and the house style, no sound | REVIEW | scene-building-basics, spoken-captions |
| 7. `voice` from the user's recording, laid on the approved slides | REVIEW | speech-aware-cutting |
| 8. `video`: the format's shots, cut on the beats, allowed spans kept | SPEND, REVIEW | film-cutting, quality-review |
| 9. Finish: grade, the sound bed as the sheet says, loudness, cover | REVIEW | film-finishing, background-music |
| 10. Final report (matched, changed, checked) and deliver | DELIVER | reel-structure |

## Not recreate-video

Both start from a reference video, and share nothing else:

| | recreate-video | remix-reel-structure |
|---|---|---|
| Copies | layout, timing and motion, measured frame by frame | beats, shot grammar, caption and pacing pattern |
| Keeps from the reference | the arrangement, with the user's photos and text in its slots | nothing visible or audible |
| Makes | an editable animated scene | new footage: generated, filmed or screen, cut to the structure |
| Makes | an editable animated scene | footage the user filmed or recorded from a screen, cut to the structure |
| Matches at | the pixel and the motion | the beat: its role, its length within 15 %, its shot type, its caption timing |

**A talking head or a live-action reel comes here, never to recreate-video**: it has no layout
to rebuild, only a structure to follow. An animated promo or app ad whose look the user wants with
their own content goes to recreate-video.

## The record

Keep the project record as SKILL.md's The record says, named `edit-footage.json`. For this job it also holds
the reference (its URL or the breakdown's path), the house style's path, the script's path, the
sheet, the mapping and the report, the route, each stage's approval, the locked cast and voices,
`allowed-spans.json` once the screen clips are placed, and `openDecisions`. A later request
(`slides`, `voice` or `video`, a fix) reads it and resumes at the next stage.

## Content rules

Written here and checked by reel-structure's report at stages 4 and 10:

- no line of the reference's speech in the script: no run of 4 or more of its words;
- no still or clip of the reference as an input to the build; its stills are for the user to look at;
- no audio or music of the reference;
- the caption copy is the user's own; only its pattern (place, size, timing) is copied.

A failed rule is fixed, never waived: rewrite the line or change the input. A rule with nothing
to check is reported as not checked, never as passed.

## 1. Take it in

ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) for what is missing, in one question, with every file in one upload panel, as
picsart-video-rules says (Asset URLs):

- the reference: the video, or a written beat-by-beat breakdown of it;
- the user's script (rows of time, picture, voice line and on-screen text), or a topic to write
  one from;
- their house style, if they keep one (frame, length, captions, sound, voices, look);
- the locked cast and voices they already have;
- their own stills, footage or recorded lines, when the build uses them;
- their own screen clips, when the reel shows a phone or a screen.

Take a supplied script, cast and voices as fact; ask only what the next stage lacks. The house
style's values win over the reference's look; the reference sets only the structure and length.

**Exit:** a reference (video or breakdown), a script or topic, and the house style or "none" are
recorded.

## 2. Read the structure

**A written breakdown skips the read, and is free.** Parse it as reel-structure says.

**A video is read with the tools** as reel-structure says. Quote what the read costs, then
SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says). Read the reference's speech only for its timing and pace, never to reuse it.

**Exit:** a sheet with every beat timed and named, and the read's cost recorded.

## 3. The structure sheet

Show the sheet as a table, with one still per beat from the reference when it was read (for the
user only), and the content rules above. REVIEW it: the user corrects a beat, a time or a name,
and the sheet is fixed before anything is mapped. Read its format with it, as reel-structure's
step 3 says: the layout, the captions' position, the hook and the end card, and what the user's
material can match, each answer in the record's `format`.

**Exit:** the user approved the sheet as the structure to copy, and no format element is open.

## 4. Map the script

With a topic and no script, write the script to the sheet's beats first, one row per beat at the
sheet's pace (words a second), with retention-hooks for the hook and the payoff; then map it.

Map the script onto the beats and run the report as reel-structure says. Show the report: each
reference beat matched, changed or dropped with its reason, each added row of the user's own, and
each content rule. A failed rule is fixed in the script before this stage closes.

When a beat is changed or dropped, ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) one beat at a time whether to rework the script toward
the reference or keep the change. Keep the others in `openDecisions`.

**Exit:** the script and its mapping approved, every content rule passed or not checked with its
reason, and the report saved in the record.

## 5. Route by format

The sheet's format chooses where the shots come from. None of these is a new pipeline:

| Reference format | Shots come from | Skills |
|---|---|---|
| POV skit, live-action story | generated takes with a locked cast | film-cast-design, film-shot-generation, film-cutting |
| Talking head | a generated presenter on the locked voice | ai-presenter, voice-over-generation |
| Screen tutorial | the user's own screen clips, placed as allowed spans | screen-recording-layouts, screen-recording-zoom |
| List or countdown | a shot or still per item, with text cards | film-shot-generation or photo-slideshow, spoken-captions |
| Reaction | the reacting person (generated) and the clip reacted to | as a talking head |
| POV skit, live-action story, filmed by the user | their takes | footage-analysis, speech-aware-cutting |
| Talking head, filmed by the user | their recording of the speaker | footage-analysis, speech-aware-cutting |
| List or countdown, from the user's media | their shot or still per item, with text cards | photo-slideshow, spoken-captions |
| Reaction, filmed by the user | their recorded reaction and the clip reacted to | as a talking head filmed by the user |

A reaction's clip must be the user's own or licensed: ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) whether they hold the right to show
it before it is placed. Never put the reference itself in as the reacted-to clip.

Record the route. A format the table does not name takes the nearest row, said in one line.

## Build in stages: slides, voice, video

When the user asks for one stage by name (`slides`, `voice` or `video`, as the `story` command
passes it), build only that stage and stop at its REVIEW. Each stage opens only once the user
approved the one before it. A stage asked for early says, in one line, which approval is missing,
and offers to show that stage again. Without a named stage, the reel runs straight through.

| Stage | What it builds | Paid |
|---|---|---|
| `slides` | one still per beat of the mapped script, held for the beat's time, with its on-screen text in the reference's caption pattern, and no sound | the pictures |
| `voice` | each line spoken in the cast's locked voice, paced to the sheet's words per second, laid on the approved slides, the stills re-timed to the real lines | the voice lines |
| `video` | the route's shots, cut on the beats, each take with its line's approved voice as reference audio where the model takes it | the takes |
| `slides` from the user's media | one of their stills or a frame of their footage per beat, held for the beat's time, with its on-screen text in the reference's caption pattern, and no sound | nothing |
| `voice` from the user's recording | their recorded lines laid on the approved slides, the stills re-timed to the real lines | nothing |
| `video` from the user's footage | their takes and screen clips, cut on the beats | nothing |

### 6. Slides

Draft the stills as film-shot-generation's key frames say, a still per beat; SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says) on the batch.
Slides from the user's media take one of their stills, or a frame of their footage, per beat.
Build the slides as a scene, as scene-building-basics says, the text placed as spoken-captions says
in the house style (font, plate, safe area). REVIEW it, titled "<Reel> - slides".

### 7. Voice

SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says) on the lines as one batch, voiced as voice-over-generation says, in the locked voices.
A voice from the user's recording is received with `picsart_drive_upload_ask`, and its lines are found
with `picsart_media_transcribe`.
A line's real length moves its still, never the words. REVIEW the voiced slides.

### 8. Video

Build the route's shots as its skills say, every paid call quoted first under SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says). Cut them on
the beats as film-cutting says. Place the user's screen clips first, write `allowed-spans.json` from
where each lands, and never cut, re-time or zoom inside one. Check the cut with quality-review: the
QC inspector with the reference match, then the critic panel once with the reference stills, as
SKILL.md's steps 9 and 10 say. Then REVIEW it.

### 9. Finish

As film-finishing says: the grade from the house style, loudness, and the cover. The sound is what
the sheet's bed says: voice only stays voice only; a bed is
drafted with background-music or
the user's own track, never the
reference's music. REVIEW the finished reel.

## 10. Report and deliver

Run the report again on what was built, as reel-structure says: each beat matched, changed or
dropped, and each content rule, with the media list (the reference's URLs, every
generation
input, the audio in the cut), so pictures and sound are checked, not assumed. Say which lines are
measured and which only follow the plan.

DELIVER the master as picsart-video-rules says, with the report beside it.

**Exit:** the master delivered, the report saved in the record, every content rule passed.

## When something fails

A failed read call is retried once, then the user is offered the free route: a written breakdown.
Out of credits: no retry; say which stage paused and keep the record. A content rule that fails
after the build sends the reel back to the stage that put the reference's content in.
