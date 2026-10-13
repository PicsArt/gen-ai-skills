---
name: short-reel-maker
description: Cut the user's own footage - one long video, several clips, photos in the mix - into a tight vertical short for TikTok, Reels or Shorts, the way an editor does - the best moments in the right order, nobody clipped mid-sentence, the speaker kept in frame - then, if the user wants them, a few highlight lines on screen and a music bed under it, each approved on its own. Use when the user has a talk, interview, podcast, vlog, webinar or any footage of people speaking and wants a short, a reel, a clip or highlights from it ("make a reel from this", "cut a 30-second short", "find the best moments"). Not for a screen recording, a video made from a text idea, or a still resized to a new shape.
metadata:
  uses: media-analysis, speech-cuts, reframe, captions, music-bed, scene-compose, evaluate
  optional: captions, music-bed
---

# Short reel maker

A short cut from talking footage lives on its words. The framing can be perfect and the short is
still unwatchable when it opens on half a sentence. So this works transcript first: what is
**said** decides where each cut falls, the picture decides what is worth keeping, and the person
talking stays in frame. A good short feels like it was always that length: nothing load-bearing
removed, no dead air, no half-sentence hanging off either end.

| Stage | Gate | Skills |
|---|---|---|
| 1. Take the footage in | ASK | — |
| 2. Read the footage | SPEND | media-analysis, reframe |
| 3. Plan the cut | — | speech-cuts |
| 4. Build the takes | — | reframe, scene-compose |
| 5. Check it | — | evaluate |
| 6. The cut | REVIEW | — |
| 7. Highlights, when wanted | ASK, REVIEW | captions |
| 8. Music, when wanted | ASK, SPEND, REVIEW | music-bed |
| 9. Deliver | DELIVER | — |

| Read this | Before you |
|---|---|
| `references/platforms.md` | pick the length, and place any words |

Each stage that ends in REVIEW waits for the user. The cut, the highlights and the music are
judged one at a time, in that order, and an approval opens only the next stage: an approved cut is
not an approved reel. A stage the user declined has no gate.

## 1. Take the footage in

- **No footage yet → open the upload in your first reply.** When the message carries no file, no
  link and no Drive file named, call `picsart_media_upload({ purpose: 'the footage for your
  short' })` in that same turn, with one line on what happens once it is in. Leave `accept` out:
  videos and photos are both welcome. If the host cannot show the upload, follow video-core's host
  notes.
- A link the user pasted, or a file in their Picsart Drive: bring it in as video-core's Asset URLs
  say. Every tool below reads the footage by the URL that comes back.
- "My clips" without naming them: ask which files, never guess.
- **What the user already said:** the platform, the length, the topic, what to keep. Never ask
  again for any of it.
- **The format:** the platform's frame from `references/platforms.md`, 9:16 at 1080×1920 and 30
  fps when none is named. The length: what the user asked for, otherwise the platform's default.

Ask only what is still open, in one turn: the platform or the length when the user named neither
("30 s for any of them" / "15 s" / "60 s"), and, with several files and no hint of an order,
nothing: the order is yours to choose.

Sort the sources as they come in: each video is talking footage or not, and each photo is a beat.
**A photo-only request is a slideshow short**: say so in one line, cut it to the pictures, and
offer music as its sound.

## 2. Read the footage

Say in one line that you are reading the footage, and that it takes a couple of minutes.

The watch charges credits. Quote every video's watch in one SPEND, as video-core says. It gives no
quote in advance, so say that it charges credits and that the amount is not known before it runs.
Then start every read at once, as the media-analysis skill says for talking footage, with
`references/talking-footage.md` from that skill as each watch's request:

- every video's probe, transcript and watch;
- every video's measurement for the reel's frame, as the reframe skill says, when the frame
  differs from the source's. It needs only the source and the shape, so it never waits for the
  plan.
- every photo's probe, for its size.

**The cut waits for every video's reads.** Each needs a transcript (or a clear "no speech") and a
watch. If one file of several cannot be read, say which, and offer to cut from the rest: that is
the user's call, since that footage may have been the point.

**The watch and the measurement are critical.** When either fails, do as its skill says, and the
cut waits.

## 3. Plan the cut

Plan as the speech-cuts skill says, from one pool of moments across every source, and read the plan
back with its `scripts/review_cuts.py` until it is clean.

**Plan two or three takes**, unless the user asked for one specific cut: a tight one, the one at
the target length, a longer one that breathes. They share every read, and a take is a clip list,
so it costs nothing.

**Mark the beats that would earn a highlight**: beside the strongest clips, the phrases the
captions skill would pick. They ride on the cut's REVIEW line, and the
highlights stage opens on them.

## 4. Build the takes

Build each take with the reframe skill's `scripts/reel_cut.py`, from the plan file speech-cuts
wrote, and the saved measurements. The reframe skill says which clips follow their speaker, which
show the whole frame, and how the seams are cut.

## 5. Check it

Check every take as the evaluate skill says, with the reframe skill's moments: each seam and each
clip's middle. At each, the speaker is in frame and the picture is the clip the plan names. Fix
the plan or the clip and build again; building is free.

## 6. The cut

REVIEW the strongest take, titled "<Topic> short — take 1", with the shot list on the review line:
the frame and length in one line, then one line per clip (what it is, its range in its source,
why it is in), the drafted highlight phrases, and "no credits for this". Name the other takes in
one more line, so the user can ask for one.

A comment that moves a cut is planned again as the speech-cuts skill says, and where the cut
landed is said in one line. The user's own edit stands, as video-core says, even where
you would have cut it differently; flag only an edit that breaks the reel, such as a clip trimmed
to nothing.

## 7. Highlights, when wanted

With the cut approved, one ASK with the wording already drafted: the phrases, each with the moment
it lands. "Add them" / "Reword them" / "Leave it clean". A skip is settled for the session.

On a yes, place them as the captions skill says, on the approved scene (the user's, if they edited
it), in the band `references/platforms.md` gives. Check a frame at each phrase, then REVIEW, titled
"<Topic> short — highlights". Running captions are a different job: offer them only when the user
asks for captions, and then in their own band.

## 8. Music, when wanted

**Offer it once the picture is settled**: the cut approved, and the highlights too when there are
any. Never offer it bare; ASK with the brief drafted as the music-bed skill says, and three exits:
"Generate it" / "Change the brief" / "No music". A changed brief is redrafted and asked again; a skip
is settled for the session.

It is the only stage here that is paid. On a yes, the bed is a SPEND, as video-core says. Generate
it and lay it under the approved scene as the music-bed skill says, then REVIEW, titled
"<Topic> short — music", with one line on what to listen for: how the bed sits under the voices. A
note on its level moves it as the music-bed skill says; a different track goes back through the
music-bed skill's brief, with a new SPEND.

If the bed fails or is declined, say so in one line and go on with the approved picture.

## 9. Deliver

DELIVER the scene the last stage approved: the music's if there was music, else the highlights',
else the cut's. Say in one line what the short is and what it sounds like: the speakers' own
voices, with a bed under them when there is one, and the music-bed skill's licence caveat with it.
Then offer one next step: another platform's length, or another take.

## When something fails

- **A read fails.** Its skill's retry, then stop that part and say so; never guess what the footage
  holds.
- **Almost no speech.** Say so in one line, and cut as the media-analysis skill says.
- **Out of credits.** Say which part is paused and what it needs, and offer what can be done
  without it: everything but the watch and the music is free.
- **A failed export.** Retry once. If it fails again, say so, and keep the approved scene so it
  can be exported later.
