---
name: reel-structure
description: Read a reference reel's structure and format, never its content - its beats, shots, caption pattern, pace and bed into a structure sheet (or parse a written breakdown for free), its layout, captions, hook and end card into the record's format, with what the footage can match; fit the user's script to the beats, and report each beat as matched, changed, dropped or added, with the content rules checked. Use when a short should be built the way a reference reel is built or looks, including the user's own channel.
metadata:
  source: channel team breakdowns and tools/reuse_guard.py, commit 3f064f0
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

**A reference video is read with the tools.** Every call below except the probe and the stills
may charge credits, and a tool charges only when its description says so. Quote what the read
will cost, then SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says). The calls do not depend on each other; run them at the same time,
and follow each job receipt as picsart-video-rules says.

| Tool | What it gives the sheet |
|---|---|
| `picsart_media_probe` | length, frame size, and whether there is audio |
| `picsart_media_segment_shots` over the whole length | the shots: holds and transitions |
| `picsart_media_transcribe` | the words' timing, for the pace and for the reuse check, never to reuse them |
| `picsart_media_describe_video` with `detail: "deep"` | shot types, camera moves, on-screen text style, per shot |
| `picsart_media_analyze_audio` | the bed: tempo and loudness |
| `picsart_media_video_stills` | one still per beat, **for the user to look at only**, never an input to a generation |

Keep each result as it came back (as files, where you run commands), then draft the sheet from them. No video is decoded here:

```
python3 scripts/sheet.py draft --shots shots.json --transcript transcript.json \
  --describe describe.json --audio audio.json --probe probe.json --out sheet.json
```

The draft has one row per shot (a long shot is split at its sentences). A short transition is a
cut, and a long one is a move inside the shot: check each boundary on the stills. Every field
the tools cannot know is `?`. **Name every beat yourself**, from the watch and the stills: join
rows that make one beat, and fill picture, on screen, caption and sound.

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
impossible. Anything not reproduced: ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) with a rendered mock (one free frame of their
footage in the format) beside the reference still, and keep the answer in the block.
`ref_format.py feasibility format.json` refuses while an element is open. The reference stage is
done only with a sheet that passes `sheet.py validate` and no open feasibility row.

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
