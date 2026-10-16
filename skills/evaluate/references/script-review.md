# The script review

A short can be built right and still mean nothing: every line says what to click, none says why
the viewer should care, and the recording never shows the result. Review the script once it is
written and before anything is built, voiced or generated, so a video that should not be made
costs nothing.

It answers three things, each with quotes from the script:

1. **Worth making?** A viewer problem, a result the footage shows, and something the viewer can do
   after watching. Without a result on screen, the verdict is **drop**.
2. **The why**, in one sentence: the viewer's problem → what they will be able to do → the proof on
   screen. A script with no why fails.
3. **Room to improve**: the lesson's insight, a reason in every step, a length that fits the
   lesson, an ending a viewer would save, and no promise the footage does not keep.

## Run it

1. Write the plan as `scripts/script_review.py` reads it (its header lists the fields): the kind,
   the why, the takeaway, and each beat with its words, its time, and `shows`, what the still at
   that moment shows. Set `result: true` only where the still shows the change itself: the new
   picture, the value on the card, the before beside the after. A change that is only words in a
   chat reply ("brown trousers and suspenders now") is a promise, not a result. A recording that
   ends on the request sent ends before its result.
2. From this skill's folder, run `python3 scripts/script_review.py <file>`.
3. Answer its two `look` items in `answers`, quoting the line and the still:
   - `insight`: does it teach the one thing a viewer would not guess? The clicks are not the lesson;
     what the tool kept or decided is. "The coffee shot is now a close-up" shows a click; "Faces go
     close. The jumps stay wide." teaches what the assistant chose.
   - `promise`: is everything the hook and the lines claim on a still? "New outfit, done" over an
     outfit that changed only in text is a no.
4. Every no gets its fix as rewritten lines, never as advice: `beat: "old" → "new"`. Write them
   into the plan and run it again. The rounds are video-core's (Evaluation).

The script decides the rest: a step that states only the click (`step_reasons`), a beat too short
for its words, a lesson squeezed by its hook and ending (`lesson_time`), and a takeaway that never
reaches the screen. "Follow for more" is a call to action, not a takeaway: the payoff or the
ending carries a rule or a tip first ("Ask in chat for the whole list; use the card for one shot").

## The verdict

Report it in this form, with the script's `why` and `fix` lines:

```
Verdict: make | make with changes | drop
Why: <problem> → <what the viewer can do> → <the proof on screen>
Changes:
- <beat>: "<old line>" → "<new line>"  (<item>)
Rescue: <the footage that would save it>      (drop only)
```

- **make**: every item says yes. Build it.
- **make with changes** (`change`): build only once the rewrites are in and the script says yes.
- **drop** (`drop`): nothing is built or charged for it. Give the reason with the quote that shows
  it, and `rescue`: the footage that would save it, or the smaller lesson the footage does hold
  ("send one image back to fix, not the fixed image").

`open` means an item is unanswered: answer it before you report.
