---
name: make-screen-videos
description: Turn a screen recording of an app or website into finished videos - several standalone how-to shorts for Reels, TikTok or Shorts that each teach one easy thing, a feature explainer, a promo with each request typed over its result, a timelapse of a long session, or a step-by-step 16:9 tutorial with chapters - in a style the user picks by eye, with a voice-over and captions if they want them. Use when the user has a screen recording and wants a tutorial, a how-to, a reel, a short, a promo, a walkthrough or a demo video from it, or carries on with videos already planned from one, including adding a generated shot to them.
metadata:
  uses: screen-recording-analysis, footage-analysis, speech-aware-cutting, screen-recording-layouts, screen-recording-zoom, visual-style, screen-ui-redesign, retention-hooks, scene-building-basics, quality-review, ai-presenter, voice-over-generation, spoken-captions, background-music, motion-design-craft, film-shot-generation
  optional: ai-presenter, voice-over-generation, speech-aware-cutting, spoken-captions, background-music, motion-design-craft, film-shot-generation
  imports: screen-recording-analysis, screen-recording-layouts, screen-recording-zoom, visual-style
  title: Make screen videos
  short-description: Turn a screen recording into how-to videos
  argument-hint: '[screen recording and the video you want]'
  starter-prompt: Turn my screen recording into short how-to videos.
argument-hint: '[screen recording and the video you want]'
---

# Screen video

A screen recording is mostly waiting, and what it shows is a few pixels of dense UI. The same
recording can become very different videos: a set of 20-second shorts that each show how easy one
thing is, a promo that sells, or a tutorial that keeps every step. Which one is the user's to say,
so this use case starts with a short interview, never with a draft to approve.

The kinds, each a route in `references/routes.md`:

| Kind | For | Frame | Built by |
|---|---|---|---|
| **How-to short** | one easy task, start to result: "look how easy" | 9:16 | `scripts/promo_scene.py` |
| **Feature explainer** | one feature: the problem, the feature, two or three uses | 9:16 or 16:9 | `scripts/promo_scene.py` |
| **Promo** | the best results, fast, to sell; a timelapse for a long session; a re-cut for an edited video | 9:16 | `scripts/promo_scene.py` |
| **Tutorial** | every step in order, held long enough to follow, with chapters | 16:9 | `scripts/tutorial_scene.py` |

Read picsart-video-rules first: how to talk and how to ask are there, and every question here follows its
Asking rules. One job: one or more screen recordings in; one video, or a set of standalone videos,
out.

| Stage | Gate | Skills |
|---|---|---|
| 1. Take the recording in | — | — |
| 2. The interview | ASK | — |
| 3. Read the recording | SPEND | screen-recording-analysis, footage-analysis |
| 4. The set: which videos | SHOW, ASK | screen-recording-analysis, screen-recording-layouts |
| 5. How we iterate | ASK | — |
| 6. The style | SHOW, ASK | visual-style, screen-recording-layouts |
| 7. The plan of video 1 | ASK | retention-hooks, quality-review |
| 8. The voice, when chosen | ASK, SPEND | voice-over-generation, speech-aware-cutting, spoken-captions, ai-presenter |
| 9. Build | — | screen-recording-layouts, screen-recording-zoom, scene-building-basics, visual-style, screen-ui-redesign |
| 10. Check it | — | quality-review, visual-style, screen-recording-zoom, screen-recording-layouts |
| 11. The user reviews | REVIEW | — |
| 12. The rest of the set | SPEND, REVIEW | as stages 7-11 |
| 13. Music, when wanted | ASK, SPEND, REVIEW | background-music |
| 14. Deliver | DELIVER | — |

| Read this | Before you |
|---|---|
| `references/interview.md` | ask the first question, and at every ASK in stages 2-7 |
| `references/routes.md` | write a plan, build, check or deliver: what differs by kind |
| `references/spec.md` | write a vertical video's spec or build it |
| `references/outline.md` | write a tutorial's outline or build it |
| `references/script.md` | write a presenter's lines |
| `references/record.md` | write or resume the project record |

**The challenger at each decision.** Before you go on from a decision, quality-review's challenger (the
`challenger` agent where the host has it) asks "why this?" of it: the set of videos (stage 4), the
style frames (6), the plan and its hooks before the ASK (7), the first build's UI, against the
recording's own screens (9), and every quote before its SPEND (3, 8, 12, 13). Act on its verdict as
quality-review says. A `stop`, or a `rethink` of the user's own choice, goes to the user in the next ASK,
the cheaper alternative first, before anything is spent.

## 1. Take the recording in

- **Read the user's brief first.** Every file in the material that is not media, read in full
  before the first question, as picsart-video-rules's The user's own brief says. A brief sets the message, the
  audience and the must-shows.
- **No recording yet → open the upload in your first reply.** When the message carries no recording
  (no attachment, no link, no Drive file named), call
  `picsart_drive_upload_ask({ accept: 'video', purpose: 'your screen recording' })` in that same turn,
  with one line on what happens once it is in, and ask the interview's first question beside it.
  If the host cannot show the upload, follow picsart-video-rules's host notes.
- A link the user pasted, or a file in their Picsart Drive: bring it in as picsart-video-rules's Asset URLs
  say. Every tool below reads the recording by the URL that comes back.
- **Several recordings** are one set of material: read each, and topics may come from any of them.
  One video plays one recording.

## 2. The interview

Ask as `references/interview.md` says: one question per turn, in its order, each skipped when the
user's words or the recording already answer it. A typical run asks four to six. The questions are
where it goes, what a viewer should get from it, how many videos, who it is for, the message, the
length (only when the destination leaves a range), the sound and the ending, and whether the
account on screen is real.

- **Start reading at once when the read is free** (stage 3): the first question goes in the same
  turn as the read, so the user answers while it runs, and later questions are drafted from what it
  found ("your recording shows five things a viewer could learn").
- **When the read charges**, ask where it goes and what it is for first (skip either the user
  already said), then quote the read before any other question. Who it is for, the message and
  the rest come after the read, drafted from what it found.
- **No plan is written until the message is one sentence.** "You decide" counts: write it from the
  recording and list it as assumed.
- **The brief closes the interview**: what the user said, what you read, what you assumed, as
  picsart-video-rules says, with how to change each assumption. The confirmation is the next real decision
  (stage 4), never a yes.

The user can say "just make it" at any point: take the recommended answers, list them as assumed,
and go on to the next choice made by eye or the next charge.

## 3. Read the recording

Read it as the screen-recording-analysis skill says: the moments first, then still sheets of the moments that
matter, and for a long session its stages. The recording is never sent to a model that watches
video: never call `picsart_media_describe_video`. footage-analysis is used only for the transcript.

Read the description of each tool you will call before the first call. When picsart-video-rules's SPEND
says any of them charges, quote the whole read in one go before the first call: the moments, the
still sheets (about four per recording, one sheet of candidate results for the set), the stages
where they are needed, and the transcript when `input.hasAudio` and the voice may be kept, with one
retry in case a call fails. When none charges, say in one line that you are reading, and go on. If
the user declines, say that nothing can be built without reading the recording, and stop.

If a read fails twice, tell the user the service is down and to try again shortly. Never guess what
the recording shows. **Moments already read in this session are not read again.**

What the read decides, said in one line each and never asked:

- **The shape.** `input.orientation` sets the layout, as the screen-recording-layouts skill says: a portrait
  recording fills the frame, a square one fills its width. A tutorial needs a raw landscape
  recording; a portrait or edited one gets the vertical kinds instead (`references/routes.md`).
- **The tier**, for a promo: prompt over result, timelapse or re-cut, from `tier` and `tierReason`,
  checked on the first sheet. When the sheet disagrees, believe the sheet.
- **What the recording is:** the product, what its steps get done, its own colours (for the
  style's brand), and whether there is speech.

## 4. The set: which videos

Find the candidates as `references/routes.md` says for the kind: standalone topics for how-to
shorts (each a run of actions from a state a viewer can reach to a visible result), the features
for an explainer, the steps that sell for a promo. **Every candidate comes from a still you read.**

A result that is only words in a chat reply, or that comes after the recording ends, is not on a
still: leave that candidate out, and say in one line what footage would bring it back.

SHOW one sheet of the candidates' results, then ASK which to make, as `references/interview.md`
says: a multi-select, the most teachable first, each with what the viewer learns and where it is
in the recording. A tutorial skips this stage: it keeps every step, and its outline is stage 7.

Every short stands alone: its own hook, its own payoff, its own ending. Never "part 2", never a
reference to another short.

**Will the screens read?** For the vertical kinds, once the videos are chosen, measure each moment
they will show with the screen-recording-layouts skill's `readability.py`: its box, the smallest text the viewer
must read and the words in it (from the still sheets), its event's luma, and the recommended
style's canvas. Then ASK "The screens" (`references/interview.md`), its own question, with the
measured reason: when a moment fails, or when the kind is a how-to or a promo where the UI is only
the means. A tutorial keeps the recording: it teaches where to click in the real app.

## 5. How we iterate

ASK what the user wants to see first (`references/interview.md`): stills of video 1 in three
styles, video 1 finished, or the written plan of every video. Then say the agreed plan in one line,
as picsart-video-rules's Asking says, with what costs: "Then: you pick a style on three stills, I build
short 1, you review it (free, as many rounds as you like), then I build the other four in the same
style and you review them together. Only the voice costs, quoted first." Store it in the record
and repeat its line at each pass.

## 6. The style

Choose it as the visual-style skill says. Recommend one from the recording and the brief, with its
reason; build video 1's hook frame and one step frame in it and in two styles that differ, with the
recording's colours as the brand where they fit; and SHOW them as three contact sheets on the user's
own recording. Then ASK which style, the recommended one first. Building and the contact sheet are
free. A mix ("the colours of one, the type of the other") comes through Other: build it and show
it.

The pick is the set's style. Save it in the record; every video of the set uses it.

## 7. The plan of video 1

Write the plan as `references/routes.md` says for the kind. It opens with one sentence, "This
short shows <audience> that <message>", and has one row per beat: the time, what is on screen, the
words, and why the beat is there, traced to the message. Write the words as the spec's or the
outline's words rules say and the retention-hooks skill says. **Never invent what the recording does
not show.**

**Review the script before anyone sees the plan**, as quality-review's script review says: put its
rewritten lines into the rows, and its why under the opening sentence. A `drop` is not planned:
ASK what to do with that video, with the reason quoted: "Leave it out" (recommended: the
recording never shows its result) / "Teach the smaller lesson" (the one the review names) / "I'll
record the result" (the footage its `rescue` names). The review is free, so it never asks to run.

The ASK is the hook: 2-3 drafted openings that differ in what they open on (a problem the viewer
feels, the result in the middle of happening, a before and after), each written as the retention-hooks
skill's hook rules say, each saying what it opens on. The rows are shown for correction, not for
approval: anything the user writes changes them, and their answer to the hook moves on.

**The viewer panel, before the ASK** (a vertical video). Build each drafted hook, which is free,
and run quality-review's viewer panel on its first 2 s. Rewrite a hook that fails, as the panel's
`fix` says. Offer only hooks that pass, each with the panel's one line. This comes before
anything is paid for: a hook that opens on footage not made yet is judged on its still or its
description. When no hook passes after the rounds, offer the best one and say what still
fails.

An opening the recording does not hold, such as a generated shot, is a SPEND. **The first reply
about a generated shot offers its key frames and nothing else:** stills at the hook, the turn and
the payoff, quoted on their own, shown together before any video is priced, and reused to open the
shot. No video model is read, compiled or priced until the user approves the stills. **Pictures the
user brings, a film's scene pictures included, are references for those stills, never the stills
themselves**: they are not this short's frame or its beats, so the key frames are still drafted
from them, quoted and shown first, even when the user says to go ahead. That reply says all four
to the user, in its own words, beside the quote:

- **Every key point**: a still for each generated beat (a generated hook and payoff are two stills,
  one batch, one quote), and the recording's own frame at the turn, which is free.
- **The quote covers those stills alone.** No video price, take or model in it.
- **They are shown together** as the concept before any video is priced.
- **Each approved still opens its shot** as its start frame; none is a throwaway preview.

For example: "You'll see the hook and payoff stills together, beside the recording's frame at the
turn, before any video is priced; each one you approve becomes the first frame of its shot."

An approved plan already names its hook, turn and payoff, so this reply runs no script: take the
key points from the plan, and never search for a shell or hand the script to another agent. Draft it first and
quote the draft beside the final, as picsart-video-rules's SPEND says; a crop of the recording is usually
smaller than the frame, so say so when it is the reference.
Its draft is key frames, as picsart-video-rules's SPEND rule 8 says: plan them on this plan's beats with the
film-shot-generation skill's `scripts/keyframes.py`, SHOW them before the shot is quoted, and open the shot on
the approved one. In the hook ASK, a generated opening is offered as its key frames first.
Its key frames and its shot are compiled with `picsart_film_compile_prompt` (picsart-video-rules's SPEND rule 9), with
the size and lens the recording's own plan gives that shot.

The words' language is the user's own, unless the recording's words are in another: then ask which.

## 8. The voice, when chosen

The sound was chosen in the interview. Make it as `references/routes.md` says:

- **A generated voice**: one line per beat, quoted as one batch with `picsart_preflight` after
  reading the voice model with `picsart_model_params` (picsart-video-rules, SPEND). Generate after the yes,
  probe each line's real length, and transcribe each for its captions, as the voice-over-generation and
  spoken-captions skills say. The line sets the beat's length; the picture holds.
- **The user's own voice** (`input.hasAudio`, a transcript that is not thin): kept whole, never cut
  mid-sentence, captioned from the saved transcript.
- **A presenter on camera**: the promo route only, never the default, as `references/routes.md`
  says.
- **Captions and music, or text only**: nothing to generate here.

Several videos' voice lines are one batch: one quote and one yes for the set.

## 9. Build

Build with the script for the kind, from this use case's folder. Run it; never work the scene out
yourself.

1. Write its input to a file as `references/spec.md` (vertical kinds) or `references/outline.md`
   (tutorial) says, with `style` and `brand` from stage 6 in the spec, `clip: "mask"`, and
   `moments` exactly as `picsart_media_screen_moments` returned them.
2. Run `python3 scripts/promo_scene.py <file>` or `python3 scripts/tutorial_scene.py <file>`. It
   prints one JSON line with the scene, its length, a timeline and diagnostics. The skills'
   scripts it imports ship beside it in `scripts/`.
3. If it exits with an error instead, its one line names the field it cannot build from. Fix that
   field and run it again.

Building is free and calls no tool. **Where you cannot run Python**, say that the video cannot be
built here, and stop.

A timelapse omits stages with no usable footage inside their source bounds and cut guards.

**Act on every diagnostic before you look at anything else.** An `error` means the scene is wrong:
make the change its `fix` names and build again; never patch the scene past one. A `warning` means
it plays but may read wrong: fix it when the fix keeps what the user chose, otherwise look at that
moment at the check and say it in the review line. An `error` still there after two builds: tell
the user what it says and what you changed, and stop there.

**A step to recreate** (the user chose designed UI for it): after the build, write the step's
elements and states from the still notes as the screen-ui-redesign skill says, with the step's panel as
`box` and its timeline span as `start` and `duration`, and run its `scripts/ui_beat.py`. With
`picsart_scene_patch`, remove the step's `<id>_panel` and `<id>_rim` and add the beat's
layers and assets in their place. Do it again after every build, as the covers are. The redraw is
the app's own screen, larger and cleaner, never an invented one: before the video is rendered,
compare each state's frame with its `source` still, as the screen-ui-redesign skill says.

Captions, a presenter's takes and callouts go on after the build with
`picsart_scene_patch`, as `references/routes.md` says. The build's pushes are its own; a
push you add by hand, on a scene the user edited, comes from the screen-recording-zoom skill's
`zoom_plan.py`, `balanced` unless the user asked for gentler or punchier pushes. When the user's comments change what a
video shows or says, change the spec or outline and build again; when they edited the scene in the
editor, their document replaces yours (picsart-video-rules): patch it instead.

**A generated shot goes in as a presenter's take does**: build with `hook.duration` set to its
length, then patch it in full frame with `picsart_scene_patch` (`references/routes.md`).
Never swap the script for a scene of your own. A scene worked out by hand skips the build's
diagnostics, and the stages around it still hold: key frames and SPEND before, the check and REVIEW
after.

## 10. Check it

Validate the build with `picsart_scene_validate`, then check it with quality-review, at most 8
moments to a contact sheet: the hook, the end of each beat where its push has landed, the ending,
and the moment of each warning left in. Ask the questions `references/routes.md` gives for the
kind. Then the polish pass, which quality-review runs:

- the build's colours and entrances keep to its style (visual-style's `adherence.py`);
- nothing on the visual-style skill's list of defaults that look machine-made, unless it is
  kept with a reason;
- every word and the call to action sit inside the destination's safe zone: the screen-recording-layouts skill's
  `safe_zone.py`, with the profile of each place in the brief;
- every line is held long enough to read and the picture never stalls (quality-review's `timing.py`,
  with each step's measured reveal as a change);
- the first frame is a real moment (the payoff, or the problem it solves), not a login screen or
  an empty app;
- a vertical video's draft passes quality-review's viewer panel. Its hook is judged again on the real
  frames; its `summary` goes in the review line.
- then quality-review's critic panel runs on every draft (the six `critic-*` agents where the host has
  them), with the recording's stills at each step as its source. Make its must-fixes, and ASK its `choices` before REVIEW, never applied silently.

Then grade the brief with quality-review's `checklist.py`: the message, the destinations, the length,
the hook and the ending from the record, and the plan's step lines. Fix only what it says no to.

**Private data, before anything is shown.** Run the screen-recording-analysis skill's privacy pass on every
text you read for this video, on its stills and in its transcript. With real data, cover each
hit it keeps, and each name or address you saw, with the screen-recording-layouts skill's `cover.py`, in the
style's surface colour, and patch the cards in; with a demo account, the keys, tokens and card
numbers only. A box on screen for a whole step can be cut or framed out instead. Cover again after
every build: a build drops the patched cards. Never open REVIEW with a hit uncovered; say in the
review line what was covered.

**Masks first.** The first contact sheet must include a panel. If it fails with `the authored mask
carries no clip`, masks are not rendering here (the screen-recording-layouts skill has the dated fact): build the
same spec again with `clip: "nest"` and check that build. REVIEW opens the mask build; the nest
build is the one that renders.

**Judge legibility on a still, not on softness alone**: crop a `picsart_media_video_stills` sheet
to the beat's box at that moment. If the still is sharp, the recording is legible; never push
harder to fix a soft contact sheet (screen-recording-zoom).

## 11. The user reviews

REVIEW the mask build, titled "<Product> <kind> — draft 1", with the checklist's `summary` and one
line on what to look at for this pass, as `references/routes.md` gives it ("Does the result land in the first two seconds? Is
each click readable? Say where it drags"). Each new draft's number goes up by one. Comments apply
where they point; after the third round on the same video, ask what is causing the misses (the
look, the pace or the words) instead of patching again.

## 12. The rest of the set

Build the other videos with video 1's approved style and with what the user's comments on it
taught (the pace, the words' tone, the moves). Plan and review each as stage 7 does, with every `drop` in the set asked in one turn, and its own hook asked
only when the user chose to see plans; otherwise draft the hook yourself and list it as assumed.
Their voice lines are one batch SPEND. REVIEW them one after another, and ask one "anything to
change?" for the set (picsart-video-rules).

## 13. Music, when wanted

Offer it once, after the drafts are approved, unless the sound chosen was the user's own voice or
the recording's own sound. ASK with two drafted briefs that differ in feel, as the background-music skill
says, and "No music". On a pick, the bed (and a promo's push sounds, `references/routes.md`) is one
SPEND for the set. Lay it under each video as the background-music skill says, validate and look as stage
10 does, and REVIEW, titled "<Product> <kind> — music", with one line on what to listen for. If it
fails or is declined, say so in one line and go on with the approved drafts.

## 14. Deliver

DELIVER each approved video: the mask build if masks rendered at the check, otherwise the nest
build. Check each export against its scene with quality-review's `qc.py` before you give its link. If the user edited a scene in the editor and masks do not render, export their scene; if
that fails on its masks, say so and offer the nest build, naming the edits it leaves out.

With each video, give:

- the link, its length against the target, and its status: done, done with concerns (each named),
  or blocked;
- **post copy** for the destination, as `references/routes.md` says: a title under 40 characters,
  a first caption line that hooks and a caption that says what the video shows, and 3-5 words of
  cover text taken from the payoff frame; hashtags only if asked;
- what it sounds like: silent (a track can be added when it is posted), the user's voice, a
  generated voice (AI-made: tell them to switch on the platform's AI-content label), or music;
- a tutorial's chapters, exactly as the build printed them, to paste into the description.

Then offer one next step in a sentence: another kind from the same recording (nothing is read
again), or saving this set's brief and style in the record so "make another" starts from them.
