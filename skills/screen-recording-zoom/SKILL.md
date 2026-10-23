---
name: screen-recording-zoom
description: The house zoom for screen footage in a panel - its scale, ramp and timing as scene keyframes, focus clamping, the readability rule, and a planner that decides which clicks of a long recording get a push. Use when timing and keyframing zooms on a screen recording shown in a panel.
metadata:
  imports: screen-recording-layouts
user-invocable: false
---

# Screen zoom

The panel already frames the content column at a readable size, so the zoom is a gentle push toward
the result, not a dive into the screen. These numbers are the house zoom:

| Parameter | Value |
|---|---|
| Rest | the content column fills the panel width |
| Peak | **1.33× over rest** — never more than 1.5× over rest; a result that is mostly white (a logo on a white card) gets 1.1× |
| Ramp | **1.0 s** in; no zoom out inside a step — the next step is a new panel |
| Zoom out | **off.** For footage that stays on one screen for minutes, where the next push is not a new panel: `zoomOut`, the ramp back to rest on the same curve, and on each focus `until`, where its hold ends and the ramp starts |
| Text floor | **off.** `textFloor`, in frame px: the peak rises until the UI's text reads at least that tall, past 1.33× if it must, and still never crops the focus box more than the push allows |
| Easing | **`cubic-bezier(0.16, 1, 0.3, 1)`** — fast start, long settle |
| Start | on a `result`: **0.1 s after the measured reveal**, so the result appears, then the frame leans in. On a `click`: 0.5 s before it, so the click lands on a settled frame (`delay: -0.5`) |
| Merge | two focus events **within 2.5 s** share one push: choose their shared peak before checking whether the pans fit in the step |

Reveals are measured, never estimated: take each reveal's settle time as the screen-recording-analysis skill
says. As keyframes on the recording layer (`t` relative to the layer, `timeMode: "layer"`), with
the trim starting 1 s before the reveal:

```
t = 0      scale = rest   position = rest framing   easing: "linear"   (waiting state, held)
t = 1.1    scale = rest   position = rest framing   easing: cubic_bezier  (reveal + 0.1)
t = 2.1    scale = peak   position = peak framing                         (terminal: no easing)
```

**Run `scripts/zoom.py` for the keyframes; never work them out.** Write the recording's size, its
panel, the content column, the layer's length and each result to lean in on (its measured reveal
in layer seconds, its box, its mean luma, and the card it sits in when there is one) to a file,
and from this skill's folder run `python3 scripts/zoom.py <file>`. It prints the layer's `scale`
and `position` keyframes with their easings, how tall the UI's text reads at rest, and any push
it had to skip because too little of the step was left. Its docstring lists every field, and
`options` sets the zoom out and the text floor. Leave both off when each step gets a new panel.
The table and the example above say what it does, for a host that cannot run it.

**Easing.** Scene keyframes take the curve exactly: `easing: { kind: "cubic_bezier", control:
[0.16, 1, 0.3, 1] }`. **A keyframe's easing shapes the segment that STARTS at it**, so put the curve
on the keyframe that begins each ramp, and mark the hold's opening keyframe `easing: "linear"`
explicitly — a keyframe with no easing draws a `linear_easing_by_omission` warning. The terminal
keyframe takes no easing (`unused_easing_on_terminal_keyframe` otherwise).

**Keep the focus inside the panel.** Clamp the framing so the zoomed window stays inside the
recording; let the focus sit off-center rather than show the panel's empty edge. The rest and peak
framings use the framing formula in the screen-recording-layouts skill; `zoom.py` clamps both and applies it. A peak
capped at or below rest keeps rest's exact scale, even when that exceeds the focus crop cap; its
scale never falls below the minimum needed to cover the panel.

**Readable beats pretty.** If UI text is unreadable in the panel, frame the panel tighter or cut
the step; never ship a zoom on text nobody can read — and never fix readability by zooming harder.
The text floor is not a fix for that: it sets how far a push leans in on a whole screen that is
sharp but drawn small, and it is capped like any push. A still that is soft stays soft at any
peak. The screen-recording-layouts skill's `readability.py` measures readability before the build, and the
screen-ui-redesign skill redraws a step that cannot be framed to read.

## Planning the pushes on a long recording

A builder that pushes on its own steps decides its own pushes; keep them. When you place pushes
yourself, on footage that stays on one screen with many clicks (a screen the user edited, a
recording no builder covers), let `scripts/zoom_plan.py` decide which actions get one:

- **Zoom to what was revealed**, not the click: the bounding box of what changed, padded.
- **No push on a wide change**: a box wider or taller than 60% of the rest view gets none.
- **Never past 1:1**: the push stops where the recording would draw larger than its own pixels. A
  recording no larger than the frame has no room, and the plan says so (`would_upscale`).
- **Actions close together share one push**, held, panning from one to the next. Drop an event
  whose padded window cannot cover the view as `no_gain` before grouping. **Never back to
  rest for less than 1 s**: two pushes that close become one.
- **Lead a click** by 0.3-1.0 s, so it lands on a settled frame; follow a change by 0.1 s, as
  above. **Hold about 1.8 s** once the last action is in frame, then **zoom out slower than in**.
- **One knob, `intensity`**: `subtle`, `balanced` (the house numbers) or `punchy`. It sets the
  peak, the merge gap, the lead and the ramps together. Say which one you used; the user changes
  it in one word.

From this skill's folder, run `python3 scripts/zoom_plan.py <file>` with the recording's size,
the layer's length, the `view` it rests in (its panel, or the frame) and each measured click or
change, as the screen-recording-analysis skill reads them. It prints the `zooms` it planned, the events it
`dropped` with the reason, and `foci` and `options` that are `zoom.py`'s input: add the panel and
the content column and run `zoom.py` for the keyframes. The plan is a proposal: name its pushes
when the user reviews, and a push the user drops stays dropped when you plan again.
