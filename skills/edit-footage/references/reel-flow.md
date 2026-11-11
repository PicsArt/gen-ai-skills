# The reel jobs: reel, highlight, podcast-clips, split, montage, slideshow, lesson

Read this whole file when the job is one of these seven (SKILL.md, The jobs). Its steps are the
reel steps of SKILL.md's flow table, in this order.

## Contents

- The record
- 1. Take the footage in
- 2. The interview
- 3. Read the footage
- 4. Pick the moments
- 5. Agree the passes
- 6. Plan the cut
- 7. Build the takes
- 8. Check it
- 9. The cut
- 10. Highlights, when wanted
- 11. Music, when wanted
- 12. Deliver
- When something fails

A short cut from talking footage lives on its words. The framing can be perfect and the short is
still unwatchable when it opens on half a sentence. So this works transcript first: what is
**said** decides where each cut falls, the picture decides what is worth keeping, and the person
talking stays in frame. A good short feels like it was always that length: nothing load-bearing
removed, no dead air, no half-sentence hanging off either end.

It also has to be the short the user meant. A podcast clip made to grow an audience and one made
to sell a course pick different moments and end differently, so the interview comes before the
cut, and every question in it is one the footage cannot answer.

Before acting on a stage, load the skills in its row that apply to this job, also when the work resumes there.

| Stage | Gate | Skills |
|---|---|---|
| 1. Take the footage in | ASK | — |
| 2. The interview | ASK | retention-hooks, reel-structure, motion-tracking-from-video (reference) |
| 3. Read the footage | SPEND | footage-analysis, footage-reframing |
| 4. Pick the moments | ASK | speech-aware-cutting, retention-hooks |
| 5. Agree the passes | ASK | — |
| 6. Plan the cut | — | speech-aware-cutting |
| 7. Build the takes | SPEND | footage-reframing, scene-building-basics, spoken-captions, edit-on-your-computer (on-disk), photo-slideshow, quick-merge-and-export, face-hiding, motion-design-craft (style), motion-pattern-library (style), scene-template-remix (style), custom-transitions (style), linked-element-motion (style), caption-decorations (style), visual-style (style), motion-tracking-from-video (reference) |
| 8. Check it: the framing, the QC inspector, the critics | ASK | footage-reframing, quality-review, resting-frame-rules (style), motion-review (style), motion-tracking-from-video (reference) |
| 9. The cut | REVIEW | — |
| 10. Highlights, when wanted | ASK, REVIEW | spoken-captions, caption-decorations, screen-recording-layouts |
| 11. Music, when wanted | ASK, SPEND, REVIEW | background-music |
| 12. Deliver | DELIVER | — |

| Read this | Before you |
|---|---|
| `references/reel-jobs.md` | pick the job, and at every question of stage 2 |
| `references/reel-record.md` | start or update the project record |
| `references/reel-interview.md` | ask the first question, and at every question of stage 2 |
| `references/reel-platforms.md` | state the frame and the length, and place any words |

A skill marked `(style)` loads only when the reel is built in a style from the library (stage 2,
No reference: a style), and at stage 7 only the ones the picked style's Skills field names. A
skill marked `(reference)` loads only when the user gave a reference video.

Every question here is asked as picsart-video-rules's Asking says: one per turn, the recommended answer
first, each option saying what it changes. The stage names are your bookkeeping, never the
user's.

**The challenger at each decision.** Before you go on from a decision, quality-review's challenger (the
`challenger` agent where the host has it) asks "why this?" of it: the moments you recommend (stage
4), the plan of the cut and its opener (6), the highlight lines the first time they are placed (10),
and every quote before its SPEND (3, 11). Act on its verdict as quality-review says. A `stop`, or a
`rethink` of the user's own choice, goes to the user in the next ASK, the cheaper alternative first,
before anything is spent.

Each stage that ends in REVIEW waits for the user. The cut, the highlights and the music are
judged one at a time, in that order, and an approval opens only the next stage: an approved cut is
not an approved reel. A stage the user declined has no gate.

## The record

Keep the project record as SKILL.md's The record says, named `edit-footage.json`. The keys only these
jobs keep are in `references/reel-record.md`.

## 1. Take the footage in

- **Read the user's brief first.** Every file in the material that is not media, read in full
  before the first question, as picsart-video-rules's The user's own brief says. A brief sets the message, the
  audience and the must-shows.
- **No footage yet → find it, or ask for it, in your first reply.** When the message carries no
  file, no link and no Drive file named: where the host can search the user's own library (its
  host notes say how) and they said where or when the footage is from — a trip, a holiday, a
  dated event — run that search, and ask for the footage only when it finds nothing. Otherwise call
  `picsart_drive_upload_ask({ purpose: 'the footage for your short' })` in that same turn, with
  one line on what happens once it is in. Leave `accept` out: videos and photos are both welcome.
  If the host cannot show the upload, follow picsart-video-rules's host notes.
- A link the user pasted, or a file in their Picsart Drive: bring it in as picsart-video-rules's Asset URLs
  say. Every tool below reads the footage by the URL that comes back.
- "My clips" without naming them: ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) which files, never guess. With several files and no hint of
  an order, ask nothing: the order is yours to choose.

Sort the sources as they come in: each video is talking footage or not, and each photo is a beat.
**A photo-only request is a slideshow short**: say so in one line, build it from the pictures
(stage 7), with a music bed as its sound, as the `slideshow` job says. With no reference and no
other word on the cut, it is a Vibe Cut (Which cut, below).

**Pick the job** from `references/reel-jobs.md` (a reel, podcast clips, a highlight, a montage, a
slideshow or a lesson), say it back in one line, and keep it in the record's `job`. Ask only
when two jobs fit equally.

### Which cut

A `reel`, `highlight`, `montage` or `slideshow` with no reference reel (and not the user's own
channel as the spec) is made as one of three cuts, or matched to a reel the user sends. ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) it
once, before the interview and before anything is made: in the first reply once the sources are
sorted (their reads say whether anyone speaks), since the options depend on it. With no
footage sent yet, the upload ask comes first and this question follows when the files land.
Ask "How should your reel look?", header "Cut". Some apps show only each option's label, on one
line that cuts off after about 40 characters, so the label carries the cut's meaning in 34
characters or fewer, and the longer line after it is the option's description, for hosts that
show one. The question card is the only place the options appear: never list them in the message
too, which has at most one plain line before the card. On
footage where no one speaks (`highlight`, `montage`, `slideshow`):

- "Vibe: like top reels (Recommended)": Styled like today's top reels.
- "Clean: just the best moments": Your best moments, tight and smooth.
- "Story: best moments + text": Best moments with captions or text.
- "Match: copy a reel I send": Send a reel you love, get the same edit with your photos.

On talking footage (`reel`), two cuts and a match, since no style is made for speech yet:

- "Story: with captions (Recommended)": Best moments with captions or text.
- "Clean: just the best moments": Your best moments, tight and smooth.
- "Match: copy a reel I send": Send a reel you love, get the same edit with your clips.

Ask nothing when the user's words or the sources already choose. The first row that matches wins:

| The user said, or sent | Cut |
|---|---|
| a reel to follow: a reel link, or a video sent with "like this", "same as this", "make one like it" | Match a reel |
| their own channel or brand as the guide ("like my channel", "my usual style", a handle) | no cut: the channel is the spec, as SKILL.md says |
| captions, subtitles, text or titles on it ("add captions") | Story |
| "just cut it", "keep it simple", "no style", a plain cut | Clean |
| a look: stylish, aesthetic, cinematic, like a trend, a vibe they name | Vibe; on talking footage the word goes into the brief's `register` as SKILL.md's step 2 says, and the cut is asked |
| photos only | Vibe |
| "you decide", "just make it" | the recommended one |

Words that choose the cut and also say to get on with it ("just cut it", "just make it", "you
decide") end the interview as well, as picsart-video-rules's Asking says for "just make it": every
question after takes its recommended answer, said back in the brief.

Say the cut back in one line by its short name (Vibe, Clean, Story or Match), and keep it in the
record's `cut` (`clean`, `story`, `vibe` or `match`).

- **Clean Cut** is the job's own flow, as this file and `references/reel-jobs.md` give it: its
  default pace and its captions, and a talking reel's highlights question (stage 10) as main asks it,
  with "Leave it clean" as its recommended answer: words on screen are Story's.
- **Story Cut** is the same flow with its words on: a talking reel's highlights at stage 10, as
  that stage asks them, and running captions when the user asked for captions. On footage where
  no one speaks, the words are a title, as the `slideshow` job's (asked at question 4, in words),
  and a short line on each key moment, written from what it shows, placed as the spoken-captions
  skill places highlights.
- **Vibe Cut** is built in the one best-fitting style (stage 2, No reference: a style).
- **Match a reel** follows the reel the user sends: with none sent yet, ask for it with
  `picsart_drive_upload_ask({ purpose: 'the reel you want to match' })` (a link works too). The
  reel is then learned as SKILL.md's step 2 says, and the user's own footage is cut to it. When
  the only video they sent is the reel to match, ask for their footage the same way.

**Start the reads at once**, before the first question: every video's probe and transcript,
as the footage-analysis skill says, and every photo's probe. They charge nothing, and the interview's
message and ending are drafted from the transcript.

## 2. The interview

**What the user already said:** the platform, the length, the topic, what to keep. Never ask
again for any of it; say it back in one line instead. The questions below go in this order, one
per turn, and each is skipped when the user's words or the footage already answer it. "You
decide" or "just make it" ends the interview as picsart-video-rules's Asking says.

The questions, in this order with their options and headers, are in `references/reel-interview.md`:
read it before the first question. The job asks or skips each one, as `references/reel-jobs.md` says.

### The brief

Close the interview as picsart-video-rules's Asking says: what the user said, what you read in the footage
(its length, its speakers, its topic, what the transcript shows), and what you assumed, as three
short lists, then anything that does not fit together: "Three reels of 60 s from an 8-minute talk
would repeat moments." Save it to the record.

The brief has no yes-or-no of its own: it ends on the next real decision, the watch's SPEND
(stage 3).

### The reference

When the user gave a reference reel or names their own channel's shorts, learn it now, before
the watch, as SKILL.md's step 2 says: the sheet, the format, and what the footage can match. A
podcast's own channel is the spec: its layout, captions, hook and end card are reproduced. Its
moments are then picked and cut to that format.

**Match a reel, or any reel sent "like this": the reference's analysis is required**, done before
the spec is written, as the reel-structure skill reads a reference video. Run every required
analysis below, applying picsart-video-rules's SPEND rule to the tool's billing contract:
1. `picsart_media_probe`, then `picsart_media_segment_shots` over the whole reel.
2. `picsart_media_video_stills`: at least 8 frames per shot and each transition at its suggested
   step, at 480 px wide or more, never 180 px tiles. Add crop sheets of each frame, border and
   title, so a frame's shape (wavy, hand-drawn, doodled) is read rather than guessed.
3. `picsart_media_track_motion` on every card, photo and title that moves, and on whatever leads a
   reveal: automatic targets, or boxes read off the stills, in `"mode": "similarity"` (`"corners"`
   when it skews or tilts in 3D), over each move's whole window at the video's own frame rate.
   Its keyframes are the build's moves: position, scale, rotation, speed and easing. Read each
   move's easing with the motion-tracking-from-video skill's `fit_motion.py`, as that skill says.
4. `picsart_media_analyze_audio` for the beat grid when there is music.
   `picsart_media_transcribe` only when someone speaks: never on a music-only reel.
5. `picsart_media_describe_video` with `detail: "standard"` is optional here, and quoted when it
   runs.

**The spec holds the measured numbers** for each text animation, card move and frame: per move,
the target, the channel, from → to, the duration, the delay, the curve and the overshoot, and the
mechanism of each text animation (a wipe, letters one by one, a mask reveal that follows an
object). Never words alone, such as "slides in". The feasibility answer says "measured" for each.
The spec is done only when `sheet.py validate sheet.json --measured` passes (the reel-structure
skill): it refuses a moving beat with no tracked move.

### No reference: a style

A `highlight`, `montage` or `slideshow` on Vibe Cut (Which cut) is not cut plainly: the agent
picks the one style from the reel-structure skill's style library that fits best and builds the
reel to it as to a reference. **Never ask the user to choose a style**; build straight away.
Talking jobs keep the job's default pace. Read the library before this step.

1. **Read the footage.** From the probes and transcripts already running, and a look at
   each photo (`picsart_scene_contact_sheet` with `media`) and a still of each clip
   (`picsart_media_video_stills`): how many photos and clips, the subject, the occasion, the mood.
2. **Pick the best fit**, as the library says, from the footage and anything the user said, never
   one already in the record's `stylesTried`. A vibe or a style the user named in their own words
   ("make it cinematic", "polaroid") is used when one fits. Say in one line which style and why
   ("Building it as a Film memories reel: calm family photos from Thanksgiving"), and go on.
   The script's `set` is the pick and the next three styles "try another style" builds: at most one
   Text-led, and at least two from other groups, one of them motion-led, as the library says.
3. **Use it as the reference.** Its sheet and format go into the record exactly as a reference
   reel's would, as the library says, with `reference: {"style": "<id>"}`, the style in `style`
   and every style built so far in `stylesTried`. There is no reference read and no SPEND for it.
   What the footage can't reproduce is approximated as the style's own rules say (a photo fills a
   video slot) and said in one line, with no question. The record was started with the `reference`
   stage, since the cut was known first. The occasion from step 1 picks the library's skin, which sets the
   style's title and colours.
4. **The bed** is briefed from the style's Music line: its mood and tempo.

**"Try another style"** said at any later stage comes back here: the reads are kept, the next
style in the set (then the next best fit) is built from the same footage. A style the user names
is built instead of the next in line. Reuse existing assets, including cutouts and music where
they fit. Before a first build or style change, identify any new charged operations, such as
background removal or a different music bed, and quote them under picsart-video-rules's SPEND
rule. Only describe a rebuild as free when its planned operations require no credits. "Keep it
simple" or "no style" makes it a Clean Cut, at the job's default pace.

## 3. Read the footage

Quote every video's watch in one SPEND, as picsart-video-rules says. Apply that same rule to
the billing contract of each required read.
It gives no quote in advance, so say that it charges credits and that the amount is not known
before it runs.
On the yes, say in one line that you are reading the footage, and that it takes a couple of
minutes. Then start every read still open at once, as the footage-analysis skill says for talking
footage, with `references/talking-footage.md` from that skill as each watch's request, and the
brief's goal and audience in it:

- every video's watch;
- every video's measurement for the reel's frame, as the footage-reframing skill says, when the frame
  differs from the source's; that skill also checks it and corrects what the tool gets wrong. It needs only the source and the shape, so it never waits for the
  plan; when its tool charges, it goes in the same quote.
- for `split`, no measurement: the shots, one still per kind of shot, and the crops checked
  against the faces, as the footage-reframing skill's split layout says.

**The cut waits for every video's reads.** Each needs a transcript (or a clear "no speech") and a
watch. If one file of several cannot be read, say which, and ASK whether to cut from the rest: that
is the user's call, since that footage may have been the point.

**The watch and the measurement are critical.** When either fails, do as its skill says, and the
cut waits.

## 4. Pick the moments

Make one pool of moments across every source, as the speech-aware-cutting skill says, snapped to whole
thoughts and ranked for the brief's goal, audience and message. Then ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) which to build from, as a
multi-select. Header "Moments".

- Each option is one moment: what is said in a few words, its length, and why it earns a place
  ("the hook: 'I quit on a Tuesday', 7 s, opens the question the short answers").
- At most four per question, the strongest first, with "(Recommended)" on the ones you would use.
  More candidates go as a second question in the same turn.
- Offer only moments that change the short: two that say the same thing are one option.

A moment the user named in their request is in without asking; offer the rest around it. With
fewer than three moments worth offering, skip the question, say which you will use, and why.

## 5. Agree the passes

Before the first build, set how the work will go, as picsart-video-rules's Asking says. Say it in two
lines: the passes (the cut, then the highlights and the music when wanted, then the export), what
the user judges at each (the order, the edges and the framing; then the words on screen; then the
sound), and any charged operations the planned build needs. Then ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) the one thing open about it.
Header "First draft".

- "Best take, played (Recommended)": the strongest take, built and opened in the editor; the other
  takes on request.
- "All the takes, one by one": the tight, the target and the long cut, each played.
- "The shot list first": the clips, their ranges and their order in a table, before anything is
  built.

When the user said "just make it", state the passes in one line and take the recommended draft.
With several reels, the passes run for one reel at a time, the strongest first. Save the answer to
`passes`, and at each pass after this say where you are in one line: "Pass 1 of 3 · the cut".

## 6. Plan the cut

Plan as the speech-aware-cutting skill says, from the picked moments, and read the plan back with its
`scripts/review_cuts.py` until it is clean. The ending the brief named is the last clip.

**Plan two or three takes**, unless the user asked for one specific cut: a tight one, the one at
the target length, a longer one that breathes. They share every read, and a take is a clip list,
so it costs nothing.

**Mark the beats that would earn a highlight**: beside the strongest clips, the phrases the
spoken-captions skill would pick. They ride on the cut's REVIEW line, and the highlights stage opens on
them.

When the user chose the shot list first, show it now as one table, one row per clip (what it is,
its range in its source, why it is in), and ASK the decision it leaves open: which clip opens the
short, with two or three openers as the options. Build once that is settled.

## 7. Build the takes

Reuse assets already made for this footage. If the build needs new charged assets, such as
cutouts or a different music bed, quote those operations and SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says) as picsart-video-rules
says before making them. With no charged operations, build directly.

Build each take with the footage-reframing skill's `scripts/reel_cut.py`, from the plan speech-aware-cutting
wrote and the measurements kept in the record. Where you cannot run commands, stop here as
picsart-video-rules says for a script that builds the scene. The footage-reframing skill says which clips follow their speaker, which
show the whole frame, and how the seams are cut.

A `split` short is built as the footage-reframing skill's split layout says, then its word cards
on the seam and its hook card with the spoken-captions skill, all from the record's `format`.
Its full-frame moments come from the locked map, never from the picture. Where you run commands
and the episode is long, upload one window per short, as edit-on-your-computer says.

A slideshow short, with no talking footage, is built as the photo-slideshow skill says when it is
among your skills: the photos as a track of clips, a blurred fill behind each one off the reel's
shape. Without it, each photo is held as a beat, as `reel_cut.py` does.

**A reel in a style** (stage 2) is where the motion is made, so it never ships as a plain cut.
Cut it first as above, its beats from the style's sheet scaled to the reel's length and its cuts
on the bed's beats, with the style's base transition as the cut's one `transition` (none for hard
cuts). Then apply the style as the library's Building it says, in its order: the accent seams,
each clip's motion, the text and its entrance, the look, then any template. Load each skill the
style's Skills field names and follow it for its part; add nothing the style does not name.

**A reel to a reference video** gets the reference's moves as they were measured at stage 2.
Place each one on its clip or layer from its tracking result, as the motion-tracking-from-video
skill says, scaled to the clip's time. Never write a move from the sheet's words alone. Build each
move from its numbers: from and to, the duration, the curve and the overshoot, in the reference's
order and with the same stagger between cards. Build each text animation by its mechanism, not
only its timing: a title the reference wipes in behind a moving sticker is a mask that follows
that sticker, never letters fading in one by one. A frame or border that is not a plain shape is
built as it was read from the crop sheets, never a plain rounded rectangle. Mind the scene's
coordinates as the scene-building-basics skill says: a shape inside a card at `[0, 0]`, a mask in its
layer's pixels, a group's scale as a ratio.

A plain join, where the user asked only to merge their clips in a given order with no cut, is built
as the quick-merge-and-export skill says when it is among your skills; there is nothing to pick.

## 8. Check it

Check each take's framing as the footage-reframing skill says. Then check it as the quality-review skill says: at
each seam and each clip's middle, the picture is the clip the plan names. Fix the plan, the clip or the
framing and build again.

A reel in a style is also checked as the resting-frame-rules skill says (every photo and title whole
or gone when motion stops) and as the motion-review skill says, against the style: each seam,
entrance and look the style names is there and lands on its beat, and nothing else moves.

A reel in a style or to a reference ends at its length (half a second over at most, a tenth short
at most), and the clip on screen at the end holds at most 1.5 s longer than its beat. A card held 6 s at the end reads as a stalled reel.
The length is the one the user asked for, kept in the record as `brief.said.length`; else the cut
pace's; else the recipe's (the sheet's `total_length`). A 15 s reference rebuilt at the user's 25 s
stretches every beat, the last one too. Where commands run, `record.py length-check
edit-footage.json scene.json` checks both (the edit-pipeline skill).

A reel to a reference video is also checked for its motion, with the motion tools:
apply picsart-video-rules's SPEND rule to their billing contracts.
1. Export the draft.
2. Track each measured move's window on the draft with the same box as the reference's (the same
   part of the object, the same size against it), the same `mode` and the same estimator. A fast
   move that smears is tracked with `"estimator": "segmentation"` and read at
   `--min-confidence 0.2` on both sides.
3. Compare the two with `fit_motion.py diff`, which removes the starting offset, for each channel
   that moves (position, scale, rotation), as the motion-tracking-from-video skill says.
4. Compare the feel: `fit_motion.py compare` on the two tracking results, which checks where the
   peak speed comes and how big it is, the overshoot and the curve. It catches a linear move where
   the reference eases.
5. Take `picsart_media_video_stills` of the draft and the reference at the same timestamps, side by
   side, for each frame and each text animation.

A move passes when its `moveDev` (the deviation with the starting offset removed) is at most 24 px
of position in a 1080-wide frame, 0.03 of scale and 3°, and `fit_motion.py compare` passes it. The
placement (`startOffset`) is the layout, said beside it. Fix a move outside those limits and
check again while corrections make progress. If the evidence or a tool limit prevents a match,
report which part differs, by how much and why. ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) whether to accept that approximation
or change the approach before the cut's REVIEW; an unresolved difference is not a pass.

Then run the QC inspector on the take's draft, as SKILL.md's step 9 says, and fix what it
finds. Then run quality-review's critic panel (the six `critic-*` agents where the host has them) on the take the
first draft named, with the transcript's lines as the words and a still of each clip in its source
as the source stills, the reference stills beside them when a format was read. Make its must-fixes in the plan and build again. ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) its `choices` before the
cut's REVIEW, never applied silently.

## 9. The cut

REVIEW the take the first draft named, titled "<Topic> short — take 1", with the shot list on the
review line: the frame and length in one line, then one line per clip (what it is, its range in
its source, why it is in), and the drafted highlight phrases. Name the other
takes in one more line, so the user can ask for one.

A reel built in a style names it on the review's first line ("Built as a Film memories reel"),
and the review line offers "Try another style", which reuses the footage and applies the build pricing rule above.

A comment that moves a cut is planned again as the speech-aware-cutting skill says, and where the cut
landed is said in one line. The user's own edit stands, as picsart-video-rules says, even where
you would have cut it differently; flag only an edit that breaks the reel, such as a clip trimmed
to nothing.

## 10. Highlights, when wanted

With the cut approved, ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) which words go on screen, with the phrases already drafted. Header
"Highlights".

- "<n> lines (Recommended)": each drafted phrase quoted with the moment it lands.
- "Only the hook line": one phrase, the opening one, quoted.
- "Leave it clean": the voices carry it; no words on screen.

On Clean Cut (Which cut) the same three options are asked, with "Leave it clean (Recommended)" first.

The phrases are verbatim, so a reworded one is a different line from the transcript, not an edit.
A skip is settled for the session.

On a yes, place them as the spoken-captions skill says, on the approved scene (the user's, if they edited
it), in the band `references/reel-platforms.md` gives. Check a frame at each phrase, then REVIEW, titled
"<Topic> short — highlights". Running captions are a different job: offer them only when the user
asks for captions, and then in their own band.

A highlight look the spoken-captions skill does not give (a box, a sticker, a marker sweep), or a
decoration that does not show or lands at the wrong time, is authored as the
caption-decorations skill says.

## 11. Music, when wanted

For a music-first job (`references/reel-jobs.md`), the bed was chosen and generated before stage 4;
here it is only laid under the approved scene and reviewed.
A music-first job whose bed is the user's own track (`references/reel-jobs.md`) received it before
stage 4; here it is only laid under the approved scene and reviewed.

**Offer it once the picture is settled**: the cut approved, and the highlights too when there are
any. Never offer it bare. ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) with the options below, header "Music".
Draft two briefs as the background-music skill says, each in one line that says what it sounds like
under these voices, and that differ in feel.

- "<brief one> (Recommended)": the one that fits the transcript's tone.
- "<brief two>": a different energy, such as warmer or more driving.
- "My own track": the user sends it, received with `picsart_drive_upload_ask`.
- "No music": the speakers' own voices, as cut.

A brief the user writes in their own words is drafted into the background-music skill's slots and asked
again.
A skip is settled for the session.

On a pick, the bed is a SPEND, as picsart-video-rules says. Generate
it and lay it under the approved scene as the background-music skill says, then REVIEW, titled
"<Topic> short — music", with one line on what to listen for: how the bed sits under the voices. A
note on its level moves it as the background-music skill says; a different track goes back through the
background-music skill's brief, with a new SPEND.
The user's own track is laid under the approved scene as an audio layer with an explicit duration,
under the voices, then REVIEW, titled "<Topic> short — music", with one line on what to listen for:
how the track sits under the voices.

If the bed fails or is declined, say so in one line and go on with the approved picture.

## 12. Deliver

Only after the check, the critics and the cut's REVIEW (SKILL.md's step 13). Never skip one on
your own; a user who asks to skip one is told its risk in one line, and a skip they confirm is
recorded as the edit-pipeline skill says. Then DELIVER the scene the last stage approved: the music's if there was music, else the highlights',
else the cut's. Say in one line what the short is and what it sounds like: the speakers' own
voices, with a bed under them when there is one.
Give the background-music skill's licence caveat with it.
With more reels to go, the next one starts at its first pass. Then offer one next step: another
platform's length, or another take.

## When something fails

- **A read fails.** Its skill's retry, then stop that part and say so; never guess what the footage
  holds.
- **Almost no speech.** Say so in one line, and cut as the footage-analysis skill says. The message
  and the ending are then asked in words, with an anchor.
- **Out of credits.** Say which part is paused and what it needs, and offer what can be done
  without it, based on the remaining operations and their billing contracts.
- **A failed export.** Retry once. If it fails again, say so, and keep the approved scene so it
  can be exported later.
