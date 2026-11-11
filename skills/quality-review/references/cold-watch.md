# The cold watch

Strangers who know nothing of the video watch it a few seconds at a time, with its words, and say
what they make of it. Their words are then laid against the viewer track, written before the draft
was built. It is the one check that can say whether a viewer follows the video. You, the critics
and the user all know what it means, and whoever knows fills in what the picture never shows.
The viewer track says what a stranger must get from the video, and by when.

## Contents

- What it can and cannot tell
- The viewer track
- The viewers
- What they watch
- What they are asked
- Quote it, then run it
- The comparer
- The floor, and the fixes
- On paper, before pictures

## What it can and cannot tell

It is simulated: model viewers, not people. It finds where a viewer loses the thread: a must-know
nobody got in time, a wrong belief, a question the video raises and never answers. It cannot say
what a feed will do with the video; the posted video's own numbers can (the platform's insights).
Its verdict opens "Cold watch (simulated)".

Never write that a viewer will understand the video, or that the draft is clear. Quote the floor
line, or say "no cold watch yet". A check that holds the plan (the critics, the QC inspector) finds
where the picture says something other than the plan meant; the cold watch never sees the plan, so
it finds what is missing.

## The viewer track

The writer writes it before the draft is built:
film-story-writing's viewer track for a film,
the
script's for any other short. Keep its text in the project record as `viewerTrack`, with the
`seal` `cold_watch.py` prints for it, apart from the story and the cards:
the script's viewer track for a short, kept in the project record as `viewerTrack` apart from the cards:

```text
# Viewer track

Premise: what the video is, in at most 120 words, as its maker would pitch it.

| K | By | The viewer should know |
|---|---|---|
| K1 | 2.5 | Her sister got a text saying her bank account "has been locked", and sent it on to her. |

| X | By | The viewer must not think |
|---|---|---|
| X1 | 2.5 | The text was about her own account. |

| Q | Question | Answer |
|---|---|---|
| Q1 | Whose account did the text say was locked? | Her sister's. |
```

- **4 to 8 must-knows**, each one fact a stranger needs to follow what comes next, with the second
  it must land by. Who each person is to the others, who is spoken to, and why someone decides are
  must-knows. A promise (what the video will show) is a must-know by 3 s. A caveat or a disclaimer
  is not one, unless the user asks for it.
- **1 to 3 must-not-thinks**: the wrong beliefs this video invites, never a caveat.
- **3 to 6 after-watch questions**, each with its answer. The user confirms them with the story or
  the script.

Never show the track to a viewer. A critic sees only the must-knows the gap list quotes. After a
cold watch the track changes only on the user's yes: a track that moves to fit a draft measures
nothing.

## The viewers

Three viewers, each a persona of three or four lines from the video's audience: their age, what
they use their phone for, how they watch (sound on or off), and when they swipe away. For a product
video, one of them already uses the product. Never the topic, the product's pitch, the message or
the payoff. Write them once per project, keep them in the record as `viewers` (`{id, text,
model}`), and use the same three on every draft, so two rounds compare.

Each viewer is a model that reads pictures and returns text, called with `picsart_generate`: two
on GPT's balanced model and one on Claude's Sonnet (`gpt-6.1-terra` and `claude-sonnet-5` on
2026-11-05; when `picsart_model_catalog` no longer lists one, its successor at the same tier, never
a premium one), so no single model's habits decide the floor. A model called this way knows only
what it is sent, on every host.
Never play a viewer yourself, and never give one to a worker that can read the project: whoever can
read the plan fills in what the picture never shows.

## What they watch

Forward only, a few seconds at a time, as a feed plays it: the pieces run 0–1.5 s, 1.5–3 s,
3–6 s, then every 3 s to the end (a last piece under a second joins the one before). For each piece
a viewer gets its frames, the words heard in it with their times and which voice said them, the
pauses with no words, its pace in words a second, and their own notes from the pieces before.
Never a later piece, and never another viewer's notes.

From this skill's folder, run `python3 scripts/cold_watch.py <file>` on
`{ step: "plan", track, duration }`: it checks the track and prints its `seal` and the `packets`,
the pieces. Then get, free:

- **The frames.** `picsart_scene_export` the draft with `mediaType: "image-sequence"`, `fps: 4`,
  `imageFormat: "jpeg"`, `archive: false` and `resolution` at half the scene's width and height (no
  side under 300 px): one URL per frame, in order.
- **The words.** `picsart_scene_export` it as an MP4 and run `picsart_media_transcribe` on that URL
  with `include: ["transcript", "words"]`, and `speakers` set to the number of voices when you know
  it. Diarization can hear two voices as one: when the draft's voice lines are in the record, give
  them as `voices` (`[{start, end, voice}]`, each line's place in the draft) and they name the
  voices instead. A viewer hears "voice 1", "voice 2", never a name.

## What they are asked

Keep one file for the watch: `{ step: "round", track, personas, video: { duration, fps, frames,
transcript, voices? }, replies: [], short?, promo?, cuts? }`, with `personas` the three `viewers`
and `transcript` as `picsart_media_transcribe` returned it. Run `cold_watch.py` on it. It prints
`calls`: each viewer's next call, with its `model`, its `imageUrls` (the piece's frames, 4 a second
to 3 s, then 2) and its `prompt`. Send each call verbatim with `picsart_generate`, the three at
once; add each reply to `replies` as `{viewer, packet, text}`, the text as it came; and run it
again: each next call carries that viewer's own notes, the oldest shortened when a prompt would pass
7,000 characters. Repeat until it prints `done: true`.

Each piece asks what is happening now, who the people are, what they expect next and what they
don't get, in at most 40 words. On a short (`short: true`), the first two pieces also ask "Would
you keep watching?" and "Does it feel like an ad?". On an edit of footage (`cuts: true`), each piece
also asks where a cut felt like a jump or too fast. At the end each viewer, with only their own
notes, tells a friend what it was about in two sentences, says where they would have scrolled away
and why, and answers the track's questions in order, never shown the answers; on a short, also
"Could you do it now?" (for a promo, "Would you try it?") and "Would you save it, send it to
someone, both, or neither?"

A reply it cannot read is asked again in the next round, once; a second one is named in
`unreadable`, and that viewer goes on. When it is done it prints each viewer's `account`, `asked`
(every "don't get" answer by its time, each viewer's repeats folded), `jumps`, and `comparer`.

## Quote it, then run it

A cold watch is three calls a piece and three at the end: 3 × pieces + 3, so 36 calls for a
30-second draft (`cold_watch.py`'s `packets` are the pieces; on paper, its rows). Before round 1,
quote the viewer calls with `picsart_preflight`, each model they use. The watch runs without asking
only when the preflight shows an explicit price of 0 credits for every planned call. Every other
answer is a price to ask about, a null or missing price included: no price means the price is
unknown, never that the call is free. Say calls × price, or "price unavailable, about N calls" with
N = 3 × pieces + 3, and SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says) before round 1, unless a spend limit the user stated covers it.
Nothing is sent to find out what it costs. The exports and the transcript are free.

A credit or storage error stops the watch; never retry it. When the user says no, or the watch
stops, the review line says "no cold watch yet", and the draft still goes to the user.

The yes covers the calls it was given for. Each round after it (a rebuild, the cards read again, a
reply asked again) is covered only when the user's yes or stated limit covered its calls; otherwise
quote that round the same way and SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says) again.

## The comparer

Someone who never made the video marks each viewer's words against the track. `comparer.prompt`
holds `references/cold-watch-comparer.md`, the track and the accounts, and nothing else: never the
plan, the critics' notes, the user's notes or why the video was made this way. It is too long for a
`picsart_generate` call (prompts of 15,000 characters went unanswered on 2026-11-05). Where the host
can run isolated workers, give a fresh one `comparer.prompt` verbatim as its whole prompt, with
nothing to read. Otherwise mark them yourself, strictly, as that file says, and say "comparer
inline" in the verdict.

Put its reply, as it came, in the same file as `marks`, and run `cold_watch.py` with
`step: "gaps"`. It rejects a quote that is not in that viewer's own words, and a mark missing for
any must-know and viewer: then give the same worker its `retry_prompt`, once. A must-know is hit when a viewer's
words carry it by the end of the first piece that ends after its second. It prints `gaps` (each
must-know with its marks and quotes, each must-not-think, `asked`), `fixes` (earliest first),
`floor`, and `markdown`, the gap list. Keep the floor line and the gap list in the record with the
draft's version: the critics, the next round and the review line read them.

## The floor, and the fixes

The floor is met when every must-know is hit, in time, by at least two of the three viewers, and no
viewer's retelling at the end gets the main point wrong. On a short it also needs, at 3 s, two in
three who would keep watching and nobody who says it is an ad (one "a bit" at most), and at the end
two in three who could do it (or would try it) and two in three who would save or send it.

- **Under the floor**, fix the earliest gap first, by changing what is seen or heard: who is shown,
  who is spoken to, a line, an action, a cut. A caption that explains what the picture should show
  is not a fix. Build it again and watch the new build the same way, every piece again, with fresh
  calls, quoted as above: a fix early in the video changes what every later piece means.
- **What the viewers asked is a gap too**, even when the floor is met: each question the video
  raises and never answers goes to the maker with the viewers' words.
- **Every gap goes to the critics**, as the gap list (`references/critic-panel.md`): they say why
  viewers lost the thread there.
- The rounds come out of picsart-video-rules's evaluation budget. When they run out, go on with the
  best version and say what is still under the floor, quoting the viewers.

## On paper, before pictures

Before a film's pictures are bought, the same watch can run on the cards; before an edit of
talking footage is built, on its heard script. Give `round` `rows` in place of `video`:
`[{t0, t1, seen?, heard?, on_screen?}]`, each row a shot's or a clip's time and only what is seen,
heard or written on screen in it, never its feeling, its intent or its cause. Each row is a piece,
told in words, and its calls carry no picture. The replies go through the comparer and `gaps` as a
draft's do. It is quoted as a draft's watch is, before its first round: 3 × rows + 3 calls. Fix the
cards or the cut, then read it again with fresh calls, quoted the same way.
