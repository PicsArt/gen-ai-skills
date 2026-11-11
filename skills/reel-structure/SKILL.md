---
name: reel-structure
description: Read a reference reel's structure and format, never its content - its beats, shots, caption pattern, pace and bed into a structure sheet (or parse a written breakdown for free), its layout, captions, hook and end card into the record's format, with what the footage can match; fit the user's script to the beats, and report each beat as matched, changed, dropped or added, with the content rules checked. Use when a short should be built the way a reference reel is built or looks, including the user's own channel.
metadata:
  source: channel team breakdowns and tools/reuse_guard.py, commit 3f064f0
  local-scripts: pick_style.py, style_check.py, build_index.py
user-invocable: false
---

# Reel structure

A reference reel lends its **structure**: where its beats fall, how its shots and captions
work, how fast it talks, what sits under the voice. Its **content** stays its own. Nothing the
viewer can see or hear of the reference reaches the user's video: no words, no frames, no audio
or music. Only its pattern is copied.

The method has five steps: read the structure into a sheet, check the sheet with the user, read
the format and what the footage can match of it, map the user's script onto the beats, and report
what matched and what changed. A job with no script (cutting footage to a reference) stops after
the format.

**The user's own channel is different**: its format is the spec to reproduce, and its logo, end
card, fonts and copy are theirs (own-brand mode, `references/format.md`).

## 1. Read the structure

**A written breakdown is free.** When the user brings a beat-by-beat breakdown, parse it and skip
the read:

```
python3 scripts/sheet.py parse breakdown.md --out sheet.json
```

**A style from our library supplies its own breakdown.** When the user brought no reference and the use case
builds in a style, read `references/style-library.md` (how the one best-fitting style is picked
for the footage, how it becomes the sheet and the format with no read and no SPEND, and how it is
built) and `references/style-index.md` (one line per style); then open only the picked style's
file, `styles/<id>.md`, never the whole folder. For a Thanksgiving or Friendsgiving reel, also read
`references/skin-thanksgiving.md` (the full skin); never on other occasions.

**A reference video is read with the tools, and the read is required**: none of it is optional
when the user sends a reel to follow. Run each required analysis below. Use the tool's billing
contract and picsart-video-rules's SPEND rule: quote any charged call, then SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says).
Follow each job receipt as picsart-video-rules says.

| Order | Tool | What it gives the sheet |
|---|---|---|
| 1 | `picsart_media_probe` | length, frame size, frame rate, and whether there is audio |
| 1 | `picsart_media_segment_shots` over the whole length | the shots: holds and transitions, each with the step to sample it at |
| 2 | `picsart_media_video_stills` | at least 8 frames per shot, and every transition at its suggested step, at 480 px wide or more (never 180 px tiles); crop sheets (`crop`) of each frame, border and title, so a frame's shape (wavy, hand-drawn, doodled) is read, not guessed |
| 3 | `picsart_media_track_motion` | every card, photo and title that moves, measured (below) |
| 3 | `picsart_media_analyze_audio` | the bed's beat grid, tempo and loudness, when there is music |
| 3 | `picsart_media_transcribe` | only when someone speaks: the words' timing, for the pace and the reuse check, never to reuse them. Never on a music-only reel |
| any | `picsart_media_describe_video` with `detail: "standard"` | what each shot shows and its on-screen text, in words; optional when the use case says so, and quoted whenever it runs |

The stills are **for the user to look at only**, never an input to a generation; you read the
reference from them too.
The calls in one row of the order run at the same time.

Keep each result as it came back (as files, where you run commands), then draft the sheet from them. No video is decoded here:

```
python3 scripts/sheet.py draft --shots shots.json --transcript transcript.json \
  --describe describe.json --audio audio.json --probe probe.json --out sheet.json
```

The draft has one row per shot (a long shot is split at its sentences). A short transition is a
cut, and a long one is a move inside the shot: check each boundary on the stills. Every field
the tools cannot know is `?`. **Name every beat yourself**, from the stills (and the watch when it
ran): join rows that make one beat, and fill picture, on screen, caption and sound.

**Measure the moves; never guess them.** The stills show what moves; the motion tools measure it.
Track every move the edit adds with `picsart_media_track_motion`, as the
motion-tracking-from-video skill says:
- a push, punch-in or pan on a shot or photo: the whole frame is the target;
- a photo, card or title that slides, scales or turns, with `"mode": "similarity"` (`"corners"`
  when it skews or tilts in 3D), from automatic targets or boxes read off the stills;
- a seam that moves the picture;
- a sticker or object that leads a reveal (a title wiped in as it passes).

Each window runs from the frame before the move starts to the frame after it settles, at the
video's own frame rate. Track every window; never guess a move to save a call. Targets that
share a window go in one call. Then read each move's easing with that skill's `fit_motion.py moves --into sheet.json`:
it adds the moves to the sheet's `moves`. Set each one's `track` to the result's `resultUrl`.
Write what it measured in the beat's Move cell: from and to, how long, the delay, the curve and the
overshoot (for example "card 1 up 1625→760 px over 0.77 s from 2.10 s, ease out, no overshoot").
Keep each result, as files where you run commands, for the build and the check. A camera move filmed
in the reference's own footage goes in the Shot cell and is not tracked: the user's footage has its
own. A move the tracker cannot see, such as a wipe or a fade, is read from cropped stills, one per
frame, as that skill says. Record those observations in the beat's `stillMeasurements`: each
entry names the `target`, a `channel` of `opacity` or `reveal`, and at least two ordered `frames`
with `t` in source seconds, `source` identifying the frame, and the observed `value` from 0 to 1.
The values must change and the observations must overlap the beat. For example:

```json
{"target":"title","channel":"reveal","frames":[
  {"t":2.0,"source":"stills/title-060.png","value":0},
  {"t":2.5,"source":"stills/title-075.png","value":1}
]}
```

The Move cell describes those numbers. A `(stills)` label alone is not evidence; position,
scale and rotation still require tracking.

Every moving beat declares `motionRequirements`, listing **every** target and channel observed
in the reference, independently of the evidence collected. For a card that slides and fades:
`[{"target":"card1","channel":"position"},{"target":"card1","channel":"opacity"}]`.
The gate checks each requirement separately: matching tracked moves for position, scale and
rotation; matching frame measurements for opacity and reveal. Evidence for one target or channel
cannot cover another. Write the Move cell from this complete list, never use prose to opt out.

A sheet from a reference video passes the measured check before anything is mapped onto it:

```
python3 scripts/sheet.py validate sheet.json --measured
```

It refuses a moving beat without overlapping tracked or supported still measurements, a Move
cell with words alone, and a Move left `?`.

## 2. The sheet

One row per beat, or several rows for a long one, in this table:

```
| Time (s) | Beat | What happens (picture) | Voice | On screen | Shot | Move | Caption | Sound |
```

- **Beat** names its role: hook, stake, twist, joke run, feeling, reveal, turn, payoff, CTA,
  and the retention-hooks skill's intensifier and rehook. Join two with `+` ("Payoff + CTA").
  A reference with its own beat ("Steps") keeps that name. Consecutive rows with the same name
  (reveal, reveal (soft), reveal) stay rows in the sheet and are **one beat** to the mapping
  and the report, from the first row's start to the last row's end.
- **`soft`** in the Beat cell marks a beat that starts mid-shot with no line. Its edges are
  checked within 1 s; every other beat's within 0.5 s.
- **Voice** is the reference's words, kept only so the reuse check can compare with them, and the
  pace in words a second comes from it. **On screen** is checked for pattern only. **Caption**
  is the caption style and timing ("top, whole reel"; "word by word, centre"). **Sound** is voice
  only, bed, or effects.
- **`?` is unknown**, never a value and never an error: a `?` time, a `?` cell, or `?` with a
  note. Never guess one. The map step needs every beat timed and named, and says which are not.
- A header above the table, as `- Key: value` lines: Format (talking head, POV skit, screen
  tutorial, list, reaction), Length, Cut rate, Caption style, Layout, Bed, Loudness and Source.
  **Layout** names the mode and who sits where: `split-v (top host, bottom guest)`.
- Two more columns after Sound when the reference has a format to keep: **Frame** (the beat's
  layout, or who fills it: `split-v`, `full: guest`) and **Caption position** (`seam`, `top`,
  `centre`, `lower third`). Length,
  cut rate and loudness keep their number and the line as written (`- Cut rate: ~19 cuts/min
  (21 picture changes…)`). A file with several sheets parses with `parse --all`.

A short breakdown (`| Time | Beat | What happens |`) parses too: its quoted lines become Voice,
or On screen when the words before them name a caption or a title.

Check the sheet, and write it as Markdown for the user:

```
python3 scripts/sheet.py validate sheet.json
python3 scripts/sheet.py markdown sheet.json --out sheet.md
```

Show the user the sheet with the stills, and fix what they correct. Then ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) whether the sheet
is the structure to copy, before anything is mapped onto it.

## 3. The format, and what the footage can match

Read how the reference looks into the record's `format`, as `references/format.md` says: the
layout and who sits where, the emphasis, the captions' style and **position**, the hook, the end
card and, for the user's own channel, the brand files. Draft it from the sheet, then fill it from
the stills:

```
python3 scripts/ref_format.py from-sheet sheet.json --source own-brand --out format.json
python3 scripts/ref_format.py check format.json
```

Then answer each element against the user's footage: reproduced, approximated (say how) or
impossible. For a reference video, an element that moves (a text animation, a card's move, a frame
that turns) says "measured" with its moves in its answer, never a look alone. Anything not reproduced: ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) with a rendered mock (one free frame of their
footage in the format) beside the reference still, and keep the answer in the block.
`ref_format.py feasibility format.json` refuses while an element is open. The reference stage is
done only with a sheet that passes `sheet.py validate` (with `--measured` for a reference video)
and no open feasibility row.

## 4. Map the script

The user's script is a table with a Time column, and a Beat column where the writer said which
reference beat a row copies. Fit it to the sheet:

```
python3 scripts/map_structure.py sheet.json script.md --spans allowed-spans.json --out mapping.json
```

- The first row opens on the reference's hook.
- A row named for a beat takes the next beat of that name. A time range on the reference's
  clock in its Beat cell, with the sheet's id ("F1 36–54 s"), carries it over the later beats
  that range covers. Beats never run backwards.
- An unnamed row between two rows of one beat joins it. Any other unnamed row is **added**: it is
  the user's own, and it is kept. When no row is named, each takes the beat its middle falls in.
- Each beat gets the reference's share of the length. Rows scale by at most 15 %, and a beat
  within 15 % of its share matches; otherwise it is **changed**, with the reason.
- **The allowed spans are placed first and never stretched**: a row over the user's own screen
  clip keeps its length.
- A beat no row takes is **dropped**, and the report says so. **No row is ever dropped.**

## 5. Report

```
python3 scripts/structure_report.py sheet.json mapping.json --transcript transcript.json \
  --media media.json
```

Add `--own-brand` for the user's own channel, with its logo, end card and fonts listed under
`brand` in the media list: they and its on-screen copy are reported "own brand, allowed".

The report has one line per reference beat (its time, the user's rows, matched / changed /
dropped, the reason), then one per added row. Below it, the content rules, each passed, failed
or not checked:

| Rule | Checks |
|---|---|
| words | no run of 4 or more of the reference's spoken words in a voice line (`scripts/reuse_guard.py`) |
| captions | the on-screen words are the user's own, short whole-caption copies included; only the caption pattern is copied |
| pictures | no still or clip of the reference is a generation input |
| sound | no audio or music of the reference is in the cut |

The media list (`media.json` where you run commands, else kept in the record) lists the reference's URL and every still or clip made from it, the URLs given to
each generation, and the audio in the cut; an empty list says none was used, and a missing list is
not checked. Without it, pictures and sound are not checked, and the report says so; never call
them passed. Likewise words and captions are not checked while the reference's Voice or On screen
cells are `?` and no `--transcript` covers the speech.

**A failed rule is fixed, not waived.** Rewrite the line, or change the input. A format label
nobody owns ("get ready with me", "GRWM", "POV", "storytime") passes on screen, and the report
names it "genre phrase, allowed"; show that line to the user. Any other phrase shared with the
reference stays only when the user chooses it: ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) whether to keep it, and pass it as
`--allow "<phrase>"`. To check a whole script file
on its own, `python3 scripts/reuse_guard.py transcript.json script.md` lists every shared run
with its line.

Show the user the report beside the sheet. When beats are changed or dropped, ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) whether to
rework the script toward the reference or keep the changes, one beat at a time.
