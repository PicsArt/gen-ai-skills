---
name: cut-footage-into-reel
description: Cut the user's own footage - a long video, several clips, photos - into a vertical short for TikTok, Reels or Shorts - the best moments in order, nobody clipped mid-sentence, the speaker in frame, with highlight lines and music if wanted. Use when the user has a talk, interview, podcast, vlog, webinar or other footage of people speaking and wants a reel, a short, a clip or highlights from it ("make a reel from this", "cut a 30-second short", "find the best moments"). Not for a screen recording, a video from a text idea, or resizing a still.
metadata:
  uses: footage-analysis, speech-aware-cutting, retention-hooks, footage-reframing, spoken-captions, background-music, scene-building-basics, quality-review, photo-slideshow, caption-decorations
  optional: spoken-captions, background-music, photo-slideshow, caption-decorations
---

# Short reel maker

A short cut from talking footage lives on its words. The framing can be perfect and the short is
still unwatchable when it opens on half a sentence. So this works transcript first: what is
**said** decides where each cut falls, the picture decides what is worth keeping, and the person
talking stays in frame. A good short feels like it was always that length: nothing load-bearing
removed, no dead air, no half-sentence hanging off either end.

It also has to be the short the user meant. A podcast clip made to grow an audience and one made
to sell a course pick different moments and end differently, so the interview comes before the
cut, and every question in it is one the footage cannot answer.

| Stage | Gate | Skills |
|---|---|---|
| 1. Take the footage in | ASK | — |
| 2. The interview | ASK | retention-hooks |
| 3. Read the footage | SPEND | footage-analysis, footage-reframing |
| 4. Pick the moments | ASK | speech-aware-cutting, retention-hooks |
| 5. Agree the passes | ASK | — |
| 6. Plan the cut | — | speech-aware-cutting |
| 7. Build the takes | — | footage-reframing, scene-building-basics, photo-slideshow |
| 8. Check it | — | quality-review |
| 9. The cut | REVIEW | — |
| 10. Highlights, when wanted | ASK, REVIEW | spoken-captions, caption-decorations |
| 11. Music, when wanted | ASK, SPEND, REVIEW | background-music |
| 12. Deliver | DELIVER | — |

| Read this | Before you |
|---|---|
| `references/record.md` | start or update the project record |
| `references/interview.md` | ask the first question, and at every question of stage 2 |
| `references/platforms.md` | state the frame and the length, and place any words |

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

Keep the project record as picsart-video-rules says, named `cut-footage-into-reel.json`. Its fields are in
`references/record.md`.

## 1. Take the footage in

- **Read the user's brief first.** Every file in the material that is not media, read in full
  before the first question, as picsart-video-rules's The user's own brief says. A brief sets the message, the
  audience and the must-shows.
- **No footage yet → open the upload in your first reply.** When the message carries no file, no
  link and no Drive file named, call `picsart_drive_upload_ask({ purpose: 'the footage for your
  short' })` in that same turn, with one line on what happens once it is in. Leave `accept` out:
  videos and photos are both welcome. If the host cannot show the upload, follow picsart-video-rules's host
  notes.
- A link the user pasted, or a file in their Picsart Drive: bring it in as picsart-video-rules's Asset URLs
  say. Every tool below reads the footage by the URL that comes back.
- "My clips" without naming them: ASK which files, never guess. With several files and no hint of
  an order, ask nothing: the order is yours to choose.

Sort the sources as they come in: each video is talking footage or not, and each photo is a beat.
**A photo-only request is a slideshow short**: say so in one line, build it from the pictures
(stage 7), and offer music as its sound.

**Start the free reads at once**, before the first question: every video's probe and transcript,
as the footage-analysis skill says, and every photo's probe. They charge nothing, and the interview's
message and ending are drafted from the transcript.

## 2. The interview

**What the user already said:** the platform, the length, the topic, what to keep. Never ask
again for any of it; say it back in one line instead. The questions below go in this order, one
per turn, and each is skipped when the user's words or the footage already answer it. "You
decide" or "just make it" ends the interview as picsart-video-rules's Asking says.

The questions, in this order with their options and headers, are in `references/interview.md`:
read it before the first question.

### The brief

Close the interview as picsart-video-rules's Asking says: what the user said, what you read in the footage
(its length, its speakers, its topic, what the transcript shows), and what you assumed, as three
short lists, then anything that does not fit together: "Three reels of 60 s from an 8-minute talk
would repeat moments." Save it to the record.

The brief has no yes-or-no of its own: it ends on the next real decision, the watch's SPEND
(stage 3).

## 3. Read the footage

The watch charges credits. Quote every video's watch in one SPEND, as picsart-video-rules says. It gives no
quote in advance, so say that it charges credits and that the amount is not known before it runs.
On the yes, say in one line that you are reading the footage, and that it takes a couple of
minutes. Then start every read still open at once, as the footage-analysis skill says for talking
footage, with `references/talking-footage.md` from that skill as each watch's request, and the
brief's goal and audience in it:

- every video's watch;
- every video's measurement for the reel's frame, as the footage-reframing skill says, when the frame
  differs from the source's. It needs only the source and the shape, so it never waits for the
  plan; when its tool charges, it goes in the same quote.

**The cut waits for every video's reads.** Each needs a transcript (or a clear "no speech") and a
watch. If one file of several cannot be read, say which, and ASK whether to cut from the rest: that
is the user's call, since that footage may have been the point.

**The watch and the measurement are critical.** When either fails, do as its skill says, and the
cut waits.

## 4. Pick the moments

Make one pool of moments across every source, as the speech-aware-cutting skill says, snapped to whole
thoughts and ranked for the brief's goal, audience and message. Then ASK which to build from, as a
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
sound), and that everything is free except the music bed. Then ASK the one thing open about it.
Header "First draft".

- "The strongest take, played (Recommended)": the cut built and opened in the editor; the other
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

Build each take with the footage-reframing skill's `scripts/reel_cut.py`, from the plan file speech-aware-cutting
wrote, and the saved measurements. The footage-reframing skill says which clips follow their speaker, which
show the whole frame, and how the seams are cut.

A slideshow short, with no talking footage, is built as the photo-slideshow skill says when it is
among your skills: the photos as a track of clips, a blurred fill behind each one off the reel's
shape. Without it, `reel_cut.py` holds each photo as a beat.

## 8. Check it

Check every take as the quality-review skill says, with the footage-reframing skill's moments: each seam and each
clip's middle. At each, the speaker is in frame and the picture is the clip the plan names. Fix
the plan or the clip and build again; building is free.

Then run quality-review's critic panel (the six `critic-*` agents where the host has them) on the take the
first draft named, with the transcript's lines as the words and a still of each clip in its source
as the source stills. Make its must-fixes in the plan and build again. ASK its `choices` before the
cut's REVIEW, never applied silently.

## 9. The cut

REVIEW the take the first draft named, titled "<Topic> short — take 1", with the shot list on the
review line: the frame and length in one line, then one line per clip (what it is, its range in
its source, why it is in), the drafted highlight phrases, and "no credits for this". Name the other
takes in one more line, so the user can ask for one.

A comment that moves a cut is planned again as the speech-aware-cutting skill says, and where the cut
landed is said in one line. The user's own edit stands, as picsart-video-rules says, even where
you would have cut it differently; flag only an edit that breaks the reel, such as a clip trimmed
to nothing.

## 10. Highlights, when wanted

With the cut approved, ASK which words go on screen, with the phrases already drafted. Header
"Highlights".

- "<n> lines (Recommended)": each drafted phrase quoted with the moment it lands.
- "Only the hook line": one phrase, the opening one, quoted.
- "Leave it clean": the voices carry it; no words on screen.

The phrases are verbatim, so a reworded one is a different line from the transcript, not an edit.
A skip is settled for the session.

On a yes, place them as the spoken-captions skill says, on the approved scene (the user's, if they edited
it), in the band `references/platforms.md` gives. Check a frame at each phrase, then REVIEW, titled
"<Topic> short — highlights". Running captions are a different job: offer them only when the user
asks for captions, and then in their own band.

A highlight look the spoken-captions skill does not give (a box, a sticker, a marker sweep), or a
decoration that does not show or lands at the wrong time, is authored as the
caption-decorations skill says.

## 11. Music, when wanted

**Offer it once the picture is settled**: the cut approved, and the highlights too when there are
any. Never offer it bare. ASK with two briefs drafted as the background-music skill says, each in one line
that says what it sounds like under these voices, and that differ in feel. Header "Music".

- "<brief one> (Recommended)": the one that fits the transcript's tone.
- "<brief two>": a different energy, such as warmer or more driving.
- "No music": the speakers' own voices, as cut.

A brief the user writes in their own words is drafted into the background-music skill's slots and asked
again; a skip is settled for the session.

It is the only stage here that is paid. On a pick, the bed is a SPEND, as picsart-video-rules says. Generate
it and lay it under the approved scene as the background-music skill says, then REVIEW, titled
"<Topic> short — music", with one line on what to listen for: how the bed sits under the voices. A
note on its level moves it as the background-music skill says; a different track goes back through the
background-music skill's brief, with a new SPEND.

If the bed fails or is declined, say so in one line and go on with the approved picture.

## 12. Deliver

DELIVER the scene the last stage approved: the music's if there was music, else the highlights',
else the cut's. Say in one line what the short is and what it sounds like: the speakers' own
voices, with a bed under them when there is one, and the background-music skill's licence caveat with it.
With more reels to go, the next one starts at its first pass. Then offer one next step: another
platform's length, or another take.

## When something fails

- **A read fails.** Its skill's retry, then stop that part and say so; never guess what the footage
  holds.
- **Almost no speech.** Say so in one line, and cut as the footage-analysis skill says. The message
  and the ending are then asked in words, with an anchor.
- **Out of credits.** Say which part is paused and what it needs, and offer what can be done
  without it: everything but the watch and the music is free.
- **A failed export.** Retry once. If it fails again, say so, and keep the approved scene so it
  can be exported later.
