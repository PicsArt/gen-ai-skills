# The channel-clips job

Several clips from one long video, each in the look of a short the user brings. The job runs on
SKILL.md's stage table as a reel job, with the record and the checks every job has; this file
says what each stage makes for it and which of the table's gates it opens. It asks two things at
most: the short to copy, when none came with the video, and the go. Every other choice is made
here and said in one line.

## Contents

- What is asked, and what is not
- 1. Intake: the source, the rights confirmation, the look
- 2. The look, read into the format
- 3. Read the source
- 4. The moments and the plan message
- 5. Build every clip
- 6. Check the first clip, carry the fixes
- 7. Review the first clip
- 8. Deliver, with covers, post copy and the offer to post
- Hard limits
- After delivery

## What is asked, and what is not

| The table's gate | Here |
|---|---|
| 1. `ASK` | the look, only when none came with the video, with the rights confirmation when it is due |
| 2. `ASK (format-not-matched)` | never opens: each element the source cannot reproduce is approximated, and how is said in the plan message |
| 3. `SPEND` | only for a source with no speech, for the watch that finds its moments; a talking source is read free |
| 4. `ASK` | none: a clip keeps the speaker's own sentences whole |
| 5. `ASK`, `SPEND` | none: no grade, no music; the look decides the words |
| 6. `ASK (reel)`, 7. `ASK (reel)` | one plan message with the moments and the go: the two gates fall together |
| 7. `SPEND (someone-speaks)` | none: a clip changes no words, so there is no heard script to read cold |
| 9. `SPEND`, `ASK (reel)` | the cold watch of the first clip, quoted in the plan message's cost line and taken on the go's own option; no question after the check |
| 9. `ASK (reel)` | no question after the check |
| 11. `REVIEW`, `ASK (reel)`, `SPEND (reel)` | the first clip in the editor; its approval carries to the rest; no highlights, no music |
| 13. `DELIVER` | every clip and its cover in one Drive folder, the post copy, then the offer to post |

Where a method skill asks (the structure sheet, each feasibility row, which reframe correction,
a critic's taste choice), take the recommended answer silently and state it in the plan message
or at delivery.

## 1. Intake: the source, the rights confirmation, the look

- **Read the user's brief first**, as the reel jobs do. A pasted clipping campaign brief (a
  Whop, Discord or agency brief for clippers) is read as `references/clip-briefs.md` says, before
  anything else, and carried through every stage.
- **The source** is a file in the message, a Picsart Drive file, or a link to a page elsewhere.
  A link is brought in as the `picsart-video-rules` skill's host notes say for links from elsewhere, and
  the URL that comes back is the source from then on; a link the host cannot read is said so in
  one line, and the video is asked for as a file. A link must name one video: a channel,
  playlist, profile or search page gets one line asking for the link to one video. One line
  before a download or a long read, since each takes a while. Say the source back in one line
  once it is in: its length, who speaks, what it is about.
- **The rights confirmation, for every new video.** Before clipping a video the user did not
  record in this chat, they confirm their rights to it, and nothing of it is downloaded for
  editing, cut or bought before they do. Ask it in the first message, before any other question,
  in the user's language and close to these words:
  "Before I start, please confirm: you own this video, or its owner has given you permission
  (or a license) to edit it and publish clips from it, including any music, footage and people
  in it. Reply "yes" to confirm."
  Only a clear yes counts: "yes", "I confirm", "it's mine", "it's my podcast". "I think so",
  "it's public", "it's on YouTube" or silence is not a yes: say in one line that a public video
  is not permission, and ask once more. With the yes the user takes responsibility for what they
  clip: never judge a source by what it shows or where it comes from, and never ask again for
  that video. Record each yes at once with `record_content_rights` (the source as `link` or
  `upload`, the URL or file id as received), and keep it in your preferences memory with the date
  and the source; a yes for one video never covers another. These words are version `ai-agent-1`
  of the confirmation in the worker's `content-consent` toolset: change them only with it. On a no, do not clip it: say in
  one line that you clip only videos the user owns or has the owner's permission to use. The
  look needs no confirmation: nothing of it is cut.
- **The look.** A second link, a second file or "like my shorts" is the look: a short from the
  user's own channel is `own-brand`, anyone else's reel is `third-party`. When none came,
  ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) for it in the first message, after the one line on the source, with the options a
  short from my channel, any reel I like, and no reference, your clean default; nothing else is
  asked there. Keep a channel reference in your preferences memory so the next run needs no
  question. A look given as a link is brought in like a source; one the host cannot read comes
  as a file.
- **Start the record** with the job's stages (`references/jobs.md`) and these defaults in
  `brief.assumed`, said in one line, never asked: 9:16 at 1080×1920 and 30 fps, clips of 30 to
  60 s, three clips, the look's platform as the destination (16:9 at 1920×1080 when a brief
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
  every approximation is one line in the plan message. The format-not-matched mock never opens
  for this job.
- No reference: the `reel-structure` skill's clean default, said in one line in the plan message:
  a single frame on the speaker, word cards low, the opening line on a card, no end card.

## 3. Read the source

Start the free reads the moment the source URL exists, before any question, as the
footage-analysis skill says: the probe, the transcript with speakers, and, for a source that is
not in the clips' ratio and a single layout, the reframe to that ratio as the `footage-reframing` skill says, started
here because it takes minutes. A split layout takes no reframe: fixed crops per kind of shot.

A source under 20 s has no moments to find: offer the whole thing in the look, as one clip.

A source with no speech (no audio, or a transcript with no words) has nothing to cut on for
free. This is the job's one charged read: say in one line that reading the picture to find the
moments charges credits, quote it, and SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says). Its moments replace the transcript's, and the
clips carry a hook card with the user's own title and no captions. On a no, deliver the whole
video in the look, as one clip, free.

## 4. The moments and the plan message

Pick the moments from the transcript as the `speech-aware-cutting` skill says, with no watch: the
transcript is the pool. For each clip, a hook that opens a question as the `retention-hooks` skill
names it (a result, a claim, a problem said plainly), never the payoff first; in on a sentence's
first word and out on a sentence's last word, at cut points; 30 to 60 s, one complete thought
with its payoff inside; skip the intro, the sponsor read and the goodbye; no moment used twice.
A campaign brief's rules decide which moments qualify.

Then **the plan message**, one message that opens the table's two gates at once, with nothing
asked but the go:

1. One line that shows you understood the source.
2. The look, one line per element the format has: the layout, the captions, the hook card, the
   end card. An element you can only approximate says how, in the same line.
3. Your pick: three clips unless a number was given, each on one line with its time in the
   source and its hook line quoted word for word from the transcript.
4. The cost line, from the tools' own descriptions, never invented: the clips are free.
   When the cold watch of the first clip costs credits (the `quality-review` skill says how to quote it),
   say its price here; a quote of 0 needs no mention.
5. The go: ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) once, the options:
   - "Go with these three";
   - "Go, with the cold watch (N credits)" when it costs;
   - "Go, make five";
   - "Go, just the first one".

A reply that changes something (another count, a different moment, a longer clip) gets the
plan again in one message, changed, and the go asked again; an answer is not a go. "Just go" at
any point takes the pick as it stands.

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
  the transcript, at most three lines, upper case when the look's hook is; nothing is written
  that was not said. A `third-party` look lends the box, the size and the position only.
- **The end card** last, whole, muted, the user's own on `own-brand`.
- Validate each scene, and fix a fault in the input that made it, never by hand in the scene.

## 6. Check the first clip, carry the fixes

Before any export, one contact sheet per clip with a frame at each seam, inside the hook card and
inside the end card, beside the look's still at the same beat: a face whole in every frame, the
speaker not the listener in each cut, the hook card readable where the format puts it, the cards
on the seam or in the format's position and never over a face, nothing of a `third-party` look
in the picture. A fault is fixed in its input and the scripts run again: one fix round.

Then export a draft of the first clip and run the stage-9 check on it as the `quality-review` skill
says:
the cold watch when the go took it (else the review line says "no cold watch yet"), and
the QC inspector on the render with the format and the look's stills. Then, once, the critic panel on
that draft. Fix what is blocking in the inputs, once, and carry every fix to the other clips
before they are exported; a critic's taste choice is taken silently as its recommendation and
said at delivery. What remains is said in one line at delivery. Never a second round.

## 7. Review the first clip

REVIEW the first clip as the `picsart-video-rules` skill says, opened cold. Its approval approves the look
for every clip. A note applies to every clip, not only this one; a note that names a moment
changes that clip alone. Then export the rest.

## 8. Deliver, with covers, post copy and the offer to post

Create one Drive folder first, named after what the video is (the show and episode, the talk,
the subject the clips share), with `picsart_drive_create_folder`. Export every clip, and for each
one frame inside its hook card as a PNG cover, with `picsart_scene_export`, all together, then
save them into the folder with `picsart_drive_upload` (`folderUid`, up to ten files a call). An
export that fails is retried once, then said in one line.

Then DELIVER, as the reel jobs do:

- Open with your pick: the clip you would post first, and why, in one or two sentences.
- Then a numbered list in your order, one entry per clip: its time in the source and its title
  (the hook line as spoken), one line on why it works, the clip and its cover, and ready-to-paste
  post copy: a caption from the clip's hook line and what it says, then three to five hashtags
  from its subject, and a campaign's mandatory lines and handles character for character.
- Then the folder's link, and one line for anything that differs from the plan message: an
  element approximated, a clip the check left weak, a source that failed.
- Then, once, offer to post them, as the `social-posting` skill says: the user decides with the
  clips in front of them. A no ends the job; say so plainly and stop.

## Hard limits

- Clips 15 to 90 s; 30 to 60 unless the user or a brief says otherwise. The sentence wins over
  the length, every time.
- 1080×1920 at 30 fps, or 1920×1080 for a 16:9 brief; every word inside the safe band of
  `references/reel-platforms.md`. A 16:9 source for 16:9 clips takes no reframe.
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
