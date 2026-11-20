# The channel-clips job

Several clips from one long video, each in the look of a short the user brings. The job runs on
SKILL.md's stage table, with the record and the checks every job has; this file
says what each stage makes for it and which of the table's gates it opens. Beyond the video and
the rights confirmation every job asks, it asks one thing, and only when it is not known: the
short to copy. Every other choice is made here and said in one line.

## Contents

- What is asked, and what is not
- 1. Intake: the source, the rights confirmation, the look
- 2. The look, read into the format
- 3. Read the source
- 3a. A gameplay stream
- 4. The moments
- 5. Build every clip
- 6. Check every clip, carry the fixes
- 7. Review every clip at once
- 8. Deliver, with covers, post copy and the offer to post
- Hard limits
- After delivery

## What is asked, and what is not

| The table's gate | Here |
|---|---|
| 1. `ASK` | the rights confirmation for every new video, and in the same message the look, only when none came with the video and none is kept from an earlier run |
| 3. `SPEND` | only for a source with no speech and no play to find, for the watch that finds its moments; a talking source and a gameplay stream are read free |
| 7. `SPEND` | the cold watch, as SKILL.md's step 7 says: on every clip when it is quoted at 0 credits, else only when the user asks for it |
| 9. `REVIEW` | every clip at once in the editor; its approval approves the moments and the look |
| 10. `DELIVER` | every clip and its cover in one Drive folder, the post copy, then the offer to post |

Where a method skill asks (the structure sheet, each feasibility row, which reframe correction,
a critic's taste choice), take the recommended answer silently and state it at the review.

## 1. Intake: the source, the rights confirmation, the look

- **Read the user's brief first**, as SKILL.md's step 1 says. A pasted clipping campaign brief (a
  Whop, Discord or agency brief for clippers) is read as `references/clip-briefs.md` says, before
  anything else, and carried through every stage.
- **No source yet: ask for it, and only for it, in your first reply.** When the message carries
  no file, no link and no Drive file named, say in a line what the job gives (clips in the look of
  their shorts, each ready to post), then ask for the long video: paste its link, attach it, or
  pick it from Picsart Drive; and end the turn: no question about the look, the count or the rights before the video is
  in. Where the host draws an upload, open it for a video (`picsart_drive_upload_ask` with `accept:
  'video'`), as picsart-video-rules's `references/HOST.md` says.
- **The source** is a file in the message, a Picsart Drive file, or a link to a page elsewhere.
  A link is brought in as the `picsart-video-rules` skill's `references/HOST.md` says for links from elsewhere, and
  the URL that comes back is the source from then on; a link the host cannot read is said so in
  one line, and the video is asked for as a file. A link must name one video: a channel,
  playlist, profile or search page gets one line asking for the link to one video. One line
  before a download or a long read, since each takes a while. Say the source back in one line
  once it is in: its length, who speaks, what it is about.
- **The rights confirmation, for every new video**, exactly as SKILL.md's step 1 says, in the
  first message once the source is named, before any other question: its words, what counts as a
  yes, and recording each yes as that step says. Nothing of the video is downloaded for editing,
  cut or bought before the yes.
- **The look.** A second link, a second file or "like my shorts" is the look: a short from the
  user's own channel is `own-brand`, anyone else's reel is `third-party`. When none came and none
  is kept in your preferences memory, ASK (with `picsart_ask`, found as picsart-video-rules says, for any closed choice, a multi-select included, so the options are buttons the user taps, the recommended one first; then your host's own question tool, such as AskUserQuestion; only where all fail, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) for it in the same message as the rights
  confirmation, after it, with the options a short from my channel, any reel I like, and no
  reference, your clean default; nothing else is asked there. Keep a channel reference in your
  preferences memory so the next run needs no question. A look given as a link is brought in
  like a source; one the host cannot read comes as a file.
- **Start the record** with the job's stages (`references/jobs.md`) and these defaults in
  `brief.assumed`, said in one line, never asked: 9:16 at 1080×1920 and 30 fps, clips of 30 to
  60 s (a gameplay stream's: 15 to 45, as 3a says), three clips, the look's platform as the destination (16:9 at 1920×1080 when a brief
  names a YouTube-only, long-form campaign, as `references/clip-briefs.md` says), each clip ending on a closed
  thought. A campaign brief's count and length win over them; the user's words win over both.

## 2. The look, read into the format

Read the look as the `reel-structure` skill's format says, from stills and its transcript, for
free: the layout and who sits where, the captions' style and position, the hook card (its lines,
box, position, how long it stays), the end card (its copy and its length), the emphasis. Only the
format is read: no structure sheet, no script map. Nothing of the look's content reaches the
clips: not a word, a frame or a sound; its pattern does.

- `own-brand`: the format is the spec. The end card is reused as it is, cut from the short as one
  frame and saved to Drive as its asset, its copy word for word; a logo it carries the same way,
  never redrawn.
- `third-party`: the pattern only. No brand, no end card, no logo; the hook lines and caption
  words are the user's own transcript.
- **Feasibility is answered here, not asked.** Each element is reproduced, approximated (say
  how: "one speaker, so the split holds two framings of the same person") or impossible, and
  every approximation is one line at the review. Mark each such row `"decided": "agent"`, with no
  `answer`.
- No reference: the `reel-structure` skill's clean default, said in one line at the review:
  a single frame on the speaker, word cards low, the opening line on a card, no end card.

## 3. Read the source

Start the free reads the moment the rights are confirmed and the source URL exists, as SKILL.md's
step 3 says: the probe, the transcript with speakers, the sound, the stills across the source,
and, for a source that is
not in the clips' ratio and a single layout, the reframe to that ratio as the `footage-reframing` skill says, started
here because it takes minutes. A split layout takes no reframe: fixed crops per kind of shot.

The stills across the source tell you what it is: a game on screen makes it a gameplay stream,
read as 3a says, whatever words asked for the clips.

A source under 20 s has no moments to find: offer the whole thing in the look, as one clip.

A source with no speech (no audio, or a transcript with no words) has nothing to cut on for
free. This is the job's one charged read: say in one line that reading the picture to find the
moments charges credits, quote it, and SPEND (quote it in one line, then get the yes with `picsart_ask`, found as picsart-video-rules says, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", else your host's own question tool, such as AskUserQuestion; never as a typed question unless both fail; only then those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says). Its moments replace the transcript's, and the
clips carry a hook card with the user's own title and no captions. On a no, deliver the whole
video in the look, as one clip, free.

## 3a. A gameplay stream

A stream or a recording of someone playing a game: the game on screen, often the player's camera
in a corner, their voice over it or none. Its moments are plays (a win, a kill, a fail, a clutch)
and the player's reaction to them, found free, with no watch:

1. **The reads**, all at once: the probe, the transcript (the player's commentary, when they
   speak) and `picsart_media_analyze_audio` with its default summary.
2. **The loud stretches.** Save the analysis's `rms` energy curve as a file and run
   `scripts/stream_peaks.py` on it, its `frameRateHz` as `--rate`, the clip length as `--length`,
   six as `--count`. Without a shell, read the curve's largest values yourself and keep the
   windows apart.
3. **The reactions.** The transcript's lines where the player shouts, laughs or names what just
   happened ("no way", "let's go", "did you see that") mark a play just before them. A window
   with a reaction in it ranks above a louder one without.
4. **Each one by eye.** `picsart_media_video_stills` at every peak and a few seconds before it:
   the game is being played. A menu, a loading screen, a lobby, a "starting soon" screen, an ad
   or a sponsor read is dropped, however loud.

Only a stream with no loud stretch and no reaction worth a clip takes the charged read of 3.

**The cut.** In 2 to 4 s before the play, out 1 to 3 s after the reaction lands, both edges on the
player's whole words; 15 to 45 s, 30 unless the user or a brief says otherwise. The play is under
way in the first second, never a menu or a slow lead-up, and the payoff stays inside the clip.
The hook card carries the reaction line word for word; with no commentary, the user's own title.

**The frame, with no look given.** With the player's camera on screen, the camera above the game,
as the footage-reframing skill's split layout builds it with one kind of shot: `shots` one row over
the whole source, kind `stream`; `crops` `cam` (the camera's box, read once from the stills, in
source pixels) and `game` (the play's area, centred on the action: the crosshair, the player's
character, never the chat, the alerts or the overlay's frame); `halves` `{"stream": ["cam",
"game"]}`; the seam at a third of the height (640 in a 1080×1920 frame). Each crop fills its half,
so draw it in its half's shape (`cam` about 1.7 wide to 1 high, `game` about 0.85). No `full` and
no emphasis: one person. With no camera, the game alone, as one fixed crop on the action, never
the reframe, which follows faces: each clip `frame` `crop` with `hold`, the action's centre across
the source from 0 to 1, read from the stills. A look the user brings wins over both, approximated as 2 says.
The player's words go on the seam, never over the game's own counters, map or kill feed. No music:
the game's sound and the player's voice carry it.

## 4. The moments

Pick the moments as SKILL.md's step 4 says, from the transcript and the stills, with no watch:
for each clip, a hook that opens a question as the `retention-hooks` skill names it (a result, a
claim, a problem said plainly), never the payoff first; in on a sentence's first word and out on
a sentence's last word, at cut points; 30 to 60 s, one complete thought with its payoff inside;
skip the intro, the sponsor read and the goodbye; no moment used twice. A campaign brief's rules
decide which moments qualify. A gameplay stream's moments are its plays, picked and cut as 3a
says, not by the sentences alone.

Nothing is asked here: no plan to approve, no count, no go. Say in one line what you are making
(how many clips, from which parts of the video) and go straight on to the build; the user judges
the moments in the finished clips, at the review.

## 5. Build every clip

The clips are independent: run each stage's calls for all of them together, then the next
stage. Per clip, as the `footage-reframing` skill's reel cut and the `spoken-captions` skill say,
with the scripts where commands run:

- **The frame.** A single layout cuts from the reframe started at intake, checked once against
  one still per clip and per change of speaker and corrected to hold whoever speaks; the
  correction is taken without asking, and the reframe is never measured again. A split layout
  is built from fixed crops per person and per kind of shot, checked against the faces, with the
  emphasis from the transcript's turns at the format's rate.
- **The words.** Word cards, captions or highlights as the format's caption style says, in the
  nearest scene font, on the seam of a split, in the format's position on a single frame, never
  outside the safe band. The hook card carries the clip's opening sentence word for word from
  the transcript (a stream's, as 3a says), at most three lines, upper case when the look's hook is; nothing is written
  that was not said. A `third-party` look lends the box, the size and the position only.
- **The end card** last, whole, muted, the user's own on `own-brand`.
- **A gameplay stream** is framed as 3a says when no look sets the layout.
- Validate each scene, and fix a fault in the input that made it, never by hand in the scene.

## 6. Check every clip, carry the fixes

Before any export, one contact sheet per clip with a frame at each seam, inside the hook card and
inside the end card, beside the look's still at the same beat: a face whole in every frame, the
speaker not the listener in each cut, the hook card readable where the format puts it, the cards
on the seam or in the format's position and never over a face, nothing of a `third-party` look
in the picture. A fault is fixed in its input and the scripts run again: one fix round.

Then export a draft of every clip and run SKILL.md's step 7 on them as the `quality-review` skill
says:
the cold watch when it is quoted at 0 credits or the user asked for it (else the review line says
"no cold watch yet"), and
the QC inspector on each render with the format and the look's stills. Then, once, the critic
panel on the first clip's draft. Fix what is blocking in the inputs, once, and carry every fix to
the other clips; a critic's taste choice is taken silently as its recommendation and said at the
review. What remains is said in one line at the review. Never a second round.

## 7. Review every clip at once

REVIEW every clip together, as SKILL.md's step 9 says: one scene holding them all in your order,
opened in the editor, each named by its number, its hook line quoted and where it comes from.
Its approval approves the moments and the look for every clip. A note applies to every clip,
unless it names one by its number or its moment: then it changes that clip alone. Then export
them all.

## 8. Deliver, with covers, post copy and the offer to post

Create one Drive folder first, named after what the video is (the show and episode, the talk,
the subject the clips share), with `picsart_drive_create_folder`. Export every clip, and for each
one frame inside its hook card as a PNG cover, with `picsart_scene_export`, all together, each with
that folder's `folderUid`: each export's card saves its file into the folder, so make no
`picsart_drive_upload` for them (in a host that draws no result cards, save them there with it, up
to ten files a call). An export that fails is retried once, then said in one line.

Then DELIVER:

- Open with your pick: the clip you would post first, and why, in one or two sentences.
- Then a numbered list in your order, one entry per clip: its time in the source and its title
  (the hook line as spoken), one line on why it works, and ready-to-paste
  post copy: a caption from the clip's hook line and what it says, then three to five hashtags
  from its subject, and a campaign's mandatory lines and handles character for character.
- **Every clip is SHOWn itself, playable**, as picsart-video-rules's SHOW says, with its export's `url`
  and its title as the caption, then its cover. A clip is never delivered as only its times, its link
  or a line saying it is ready with nothing to play. Follow each export's receipt to its result
  before the delivery message: a clip still rendering is not delivered yet. A clip whose export
  failed twice is said so in one line, by its title.
- Then the folder's link, and one line for anything that differs from the review: an
  element approximated, a clip the check left weak, a source that failed.
- Then, once, offer to post them, as the `social-posting` skill says: the user decides with the
  clips in front of them. A no ends the job; say so plainly and stop.

## Hard limits

- Clips 15 to 90 s; 30 to 60 unless the user or a brief says otherwise. The sentence wins over
  the length, every time.
- 1080×1920 at 30 fps, or 1920×1080 for a 16:9 brief; every word inside the safe band of
  `references/platforms.md`. A 16:9 source for 16:9 clips takes no reframe.
- The source is read, cut and exported by the URL the tools returned for it, never by the
  original link.
- One reframe per source for the whole session; every cut and recut is windowed from it.
- No stage, tool, script or field name reaches the user unless they ask.

## After delivery

Free changes, all of them: a moved edge, another moment, a different title line, another order,
the look changed. Change that clip's input, run the scripts again, check and export that clip;
the reframe stays. "Open it to edit" opens that clip's scene in the editor, then exports what
they saved. A second source is a new run from intake, with the same look unless they bring
another. A transcript instead of clips: the one already read, written out.
