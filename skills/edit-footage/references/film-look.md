# The film's look

A look is chosen from evidence, never left at a default. In one run, a brief that said
"cinematic, vintage, atmospheric" got a lifted, milky grade and template captions twice, and the
user turned both versions down as "not good for posting". The look that worked came out of the
client's own posts and the brief's references, set side by side with the footage. This step does
that before the first draft, in four parts. Each part leaves something in the record's `look`.

## 1. The board

Make one sheet of stills from:
- every reference the brief names: the deck's reel and the colour reference;
- the client's own three most-liked posts, and any post of this same shoot;
- the brand guide's pages that show photographs.

Read them with `picsart_media_video_stills` (free): 6 to 12 stills from each reel, spread across
its length. Keep each still's URL with its source in `look.board`. A reference you cannot read
(a private link, a post that will not load) is listed with `open` and the reason. Ask the user for
the file with `picsart_drive_upload_ask`; never step through it frame by frame in their browser.
The board is the evidence for every choice below, and the critics judge the draft against it.
With no reference at all (no brief to read, no guide, no posts), the board is that one `open`
entry, `{ "open": "<why>" }`, and the look follows the taste and the footage: the spec says so
item by item.

## 2. The spec

Write what the board shows into `look.spec`, each item from the stills, never from the brief's
words alone:

| Item | Say |
|---|---|
| `blacks` | crushed (true black), neutral, or lifted (a faded floor) |
| `highlights` | how they roll off, and their colour: amber, neutral, cool |
| `palette` | the colours that carry the film, and any to pull down (a green board, a blue sky) |
| `texture` | grain, halation, gate weave: none, light or strong |
| `light` | where the light falls: the food, a face, the whole frame |
| `captions` | font, case, size, position, and a phrase or a word at a time, as the client's own posts set them |
| `second camera` | how an old camera's or a phone's shots appear: full frame, an inset, a window |
| `ending` | the brand's own ending: a card, or the logo on the last shot, in the colour its guide sets over photographs |

The brief's words decide between candidates when the board allows both: "vintage" over a lifted
or a crushed black is the board's call, not a default's.

## 3. The style lab

Build three candidate looks, each a different reading of the spec, plus the footage as it is now.
Put them on the same 6 to 8 frames: the hardest shots (the brightest, the darkest, the one with
the colour to pull down, a face). Lay them side by side as one sheet:

- **In the scene**: the looks come from `picsart_scene_looks` and
  `picsart_scene_capabilities` (`looksCompact`), applied with `picsart_scene_apply_preset` on
  the clip layers. A colour to pull down is an `hsl_secondary` keyed on it. Sample the frames
  with `picsart_scene_contact_sheet` (free).
- **On the user's computer**, where commands run: the edit-on-your-computer skill's conform
  grades the frames the same way. The local lab is optional craft; the scene route does the same
  job.

Pick the candidate nearest the board by eye, and say why in one line ("crushed blacks and amber
highlights, as the deck reel; the mint board goes grey"). In director pace, show the sheet beside
the board and ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) which look leads, the recommended one first. A generated look or picture is
a paid call: quote it and SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says) first. Prefer the free looks and stills.

## 4. The check

Before the first build, compare the chosen look with the board on numbers, where they can be
measured:

- **Measure.** Where commands run, read each still's black point, white point and mean
  saturation (`YLOW`, `YHIGH` and `SATAVG`) as the edit-on-your-computer skill's colour
  comparison says, both sides on the same 8-bit scale.
- **Compare.** Put the board's numbers and the look's into `scripts/look_check.py`:

  ```
  python3 scripts/look_check.py board.json look.json
  ```

  It prints each item as `pass` or `flag`, with the gap. A flag is fixed in the look, or kept with
  a one-line reason.
- **Without commands**, the numbers are `open`, never a pass. Lay the board and the look side by
  side with `picsart_media_video_stills` and its `compareWith`, and judge them by eye.

Write the result into `look.check` as the script printed it (`{"ok", "items"}`), or just its
`items`; `record.py` reads either. Keep the whole `look` in the record before the look stage is
marked done: it belongs to that stage, and writing it afterwards makes the plan and everything
after it stale.
