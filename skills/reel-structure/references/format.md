# The format block

## Contents

- The block
- What each element holds
- Own brand and third party
- Feasibility
- The plan against the format

The record's `format` is how a reference **looks**: its layout and who sits where, its emphasis,
its captions' style and position, its hook, its end card and its brand files. The sheet keeps how
the reference **moves** (beats, shots, pace). Both are read at the reference stage, and the plan,
the build, the check, the critics and the review read `format`, so a change to it makes them
stale.

## The block

```json
"format": {
  "source": "own-brand",
  "canvas": [1080, 1920], "fps": 30,
  "layout": {"mode": "split-v", "slots": {"top": "host", "bottom": "guest"}, "seam": 960},
  "emphasis": {"kind": "full-frame", "per10s": 0.9, "hold": [3, 6]},
  "captions": {"style": {"font": "Bebas Neue", "size": 100, "color": "#111111", "box": "#FFFFFF",
               "words": [1, 3], "reveal": false}, "position": "seam"},
  "hook": {"style": {"box": "#C8161D", "color": "#FFFFFF", "size": 96},
           "position": "above-seam", "lines": [2, 3], "length": 3.2},
  "endCard": {"copy": ["LISTEN NOW", "NEW EPISODES MONDAYS & THURSDAYS"], "asset": "<url>", "duration": 3.767},
  "brand": {"logo": "<url>", "fonts": ["<url>"], "colors": ["#C8161D"]},
  "evidence": [{"element": "layout", "still": "<reference still url>", "t": 6.0}],
  "feasibility": [{"element": "layout", "verdict": "approximated", "how": "the two guests stacked", "answer": "<the user's answer>"}]
}
```

`python3 scripts/ref_format.py from-sheet sheet.json --source own-brand --out format.json` drafts
the layout, the emphasis and the caption position from the sheet's `Layout` header and its
`Frame` and `Caption position` columns. Fill the rest from the reference stills, and keep one
`evidence` row (the still and its time) for each element. `ref_format.py check` validates it.

## What each element holds

| Element | Holds | Read from |
|---|---|---|
| `layout` | `mode` (single, split-v, stacked, pip, full), `slots` (who fills top, bottom, main, inset), `seam` (pixels from the top, split-v only) | the stills; the sheet's Layout and Frame |
| `emphasis` | how a key line is lifted: `full-frame` (one person fills the frame), `zoom` or `none`; how often (`per10s`) and how long (`hold`) | the Frame column's `full: who` rows |
| `captions` | `style` (font, size, colour, box, words per card, reveal) and `position` (seam, top, centre, bottom, lower third) | the stills; the Caption position column |
| `hook` | the opening card: style, `position` (above-seam, top, centre), `lines`, `length` on screen | the first seconds' stills |
| `endCard` | its `copy` word for word, its `asset` and `duration` | the last seconds |
| `brand` | logo, fonts, colours | own brand only |

## Own brand and third party

- **`own-brand`**: the reference is the user's own channel, and **its format is the spec to
  reproduce**. Its logo, end card, fonts and end-card copy are the user's and are reused as they
  are. When the files cannot be taken from the reference, ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) for them with
  `picsart_drive_upload_ask`; never redraw a logo or invent copy. `structure_report.py
  --own-brand` reports their reuse as "own brand, allowed", with the files listed under `brand`
  in the media list.
- **`third-party`**: someone else's reel. Only its pattern is copied: the content rules bind, and
  it lends no `brand`.
- **`described`**: the user described the format in words, with no reference to look at.

Several references: `from-sheet` takes them all. The majority layout goes into `format`, and each
other one becomes an open feasibility row; never make one reference a rule for all.

## Feasibility

Before the reference stage is done, every element is answered: **reproduced** (exactly),
**approximated** (with `how`: "the two in-studio guests stacked, the host above") or
**impossible**. Anything not reproduced goes to the user before any cut: ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) with a rendered
mock (one free contact-sheet frame of the footage in the format) beside the reference still, and
keep their words in `answer`. `ref_format.py feasibility` refuses a block with an open row or a
missing answer; without commands, check the same by hand.

## The plan against the format

`record.py lock-check <record> <plan>` also checks the plan against `format`. It runs
`ref_format.py plan-check`. The plan's `layout`, and each row's or clip's `layout` or `frame`,
must be the format's mode. A full-frame piece passes when `emphasis.kind` is `full-frame`, and a
`crop` counts as `single`. The plan's caption position must be the format's. Any difference
passes only with an approval scoped `format:<element>` (`format:layout`, `format:captions`). A
caption over a face is fixed in the layout, never by leaving the format's position.
