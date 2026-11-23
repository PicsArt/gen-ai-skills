---
name: speech-aware-cutting
description: Choose the moments of talking footage worth keeping and cut them so no one is clipped mid-sentence - the transcript sets every in and out, the watch picks what is worth it - then read the cut as the viewer will hear it with scripts/review_cuts.py, which flags chopped words, filler and seams that open on "but" or "she", with the time to move each edge to. Use when cutting a short, a reel or highlights from an interview, podcast, vlog, talk or any footage where people speak, and when a finished cut sounds choppy.
user-invocable: false
---

# Speech cuts

A short cut from talking footage lives on its words. The framing can be perfect and the short is
still unwatchable when it opens on half a sentence or spends its first two seconds on "yeah, no,
totally". So the cut is planned from what is **said**, and checked as what is **heard**, before
anything is built.

## Read the footage

Read every source as the footage-analysis skill says for talking footage: a transcript kept as the
tool returned it (`transcript-<source id>.json` where you run commands), which sets every boundary, and a watch, which picks the moments. A photo has no speech
at all: it is a beat, not a backbone.

## Plan the cut

1. **One pool of moments.** Take the watch's candidate moments from every source into one list,
   each with the source it came from: its times count on that source's clock, as the footage-reframing
   skill says.
2. **Snap each to whole thoughts.** A clip's `in` is a sentence's first word, or a word after a
   real pause; its `out` is a sentence's last word, or a word before one. The transcript's
   `cutPoints` mark the clean ends. Sentence edges keep every word whole; they do not say what a
   moment is. The question the viewer holds and its answer on screen set where a clip starts and
   stops, as the retention-hooks skill's `what-a-cut-is` reference says; the transcript then sets
   the exact frame. A line said after the action, summing it up, is never the moment itself.
3. **Order and trim to the target.** Order the moments by their loops, as the retention-hooks
   skill says. Aim for the target length within about 15%. **When the length and a clean sentence
   conflict, the sentence wins and the length moves.** Never cut a word out of a sentence to save time: the ear hears the
   splice at once, where the eye would forgive a picture cut.
4. **Spend no second on dead air.** Tighten between sentences, never inside one: a wordless gap of
   more than about 0.7 s inside a clip is cut, unless the plan names the beat the viewer watches in
   it (the reaction, the play, the laugh) as a source second in the clip's `beats`. Every sentence
   between the hook and the payoff follows from the one before by "but" or "so"; one that only
   follows by "and" is the first to go. The opening keeps the retention-hooks skill's opening
   contract (the first word within about 0.5 s), and the end lands on the peak (cut within about
   1.5 s of the last word, nothing after it that softens it).
5. **Place photos at sentence edges**, never inside one, each held long enough to read.
6. **Keep what the user saw work.** A recut or a fix starts from the last version the user saw,
   never from zero. Every moment they liked stays, with the picture it had; a fix for a constraint
   (a clipped word, a pause, the length) moves an edge, never swaps the moment for another. A
   moment dropped, moved or given a new picture gets one line in the message to the user. Where
   the use case keeps the edit-pipeline record, its keepers ledger and `scripts/meaning_diff.py`
   do this, as the edit-pipeline skill says.

Write the plan as the reel's clip list, the one the footage-reframing skill's `scripts/reel_cut.py` reads,
with each spoken source's `transcript` beside its other fields (its file path, where you run commands).

## Review it as heard

Run `python3 scripts/review_cuts.py reel.json` on that same file. It joins each clip's words in
play order into the **heard script**, and checks three things per clip:

| Check | Fails when | Its repair |
|---|---|---|
| Integrity | an edge cuts through a word, or the clip opens or stops mid-sentence | move that edge to the time given |
| Substance | most of the clip is filler; the opening clip is held to a stricter share | drop it, or take the sentence beside it |
| Fluency | a clip opens on a connective ("but", "so") with nothing before it, or the reel opens on a pronoun no one has been named for | move the in point back to what it refers to, or lead with another clip |
| Context | a clip opens on an answer ("Yes", "Exactly") whose question the cut drops | move the in point back to the question |

Each clip also lists the `speakers` its words carry. Use them when the footage-reframing skill asks who a
clip should hold on.

The review also returns `context`: each name the reel says for the first time, each "she" or "that"
right after a seam, each "as I said", and each seam that jumps far in its source, with the second of
the reel it is heard at and, when the cut drops it, what the source said first. These are not faults.
They are the places a listener who knows only the reel may get lost.

It also returns `warnings`, the pace measured: `first-word` when the reel's first word is heard
after 0.5 s, `gap` for each wordless stretch over 0.7 s inside a clip that no `beats` entry names,
`tail` when the reel runs more than 1.5 s past its last word, and `softener` when its last words
soften the last line. These thresholds are working numbers, not a platform's, so they warn and
never fail a clip. Fix each, or say in one line why the cut keeps it. Once the user has shared
their retention numbers, those outrank them: a drop at a second is fixed whatever the warnings say.

**Then have the script read cold.** You know the whole footage, so you cannot hear what is missing.
Have it read on paper as the quality-review skill's cold watch says, its calls quoted first as it
says: a SPEND (quote it in one line, then get the yes with `picsart_ask`, found as picsart-video-rules says, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", else your host's own question tool, such as AskUserQuestion; never as a typed question unless both fail; only then those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says) before the first read unless every call is quoted at 0 credits. Each row a clip's time in the
reel and its heard words, so readers who know nothing read it up to each moment and say what they
understood. Check their account at each `context` time: did they know who or what it was? Where
they did not, keep the setup or lead with another clip.
Read the `script` yourself too, as prose,
for what is clunky; whether a clean clip is worth its seconds is your call.

Apply the repairs to the plan and run it again until it is clean. A repair changes numbers in a
plan, so it costs nothing. **The review never blocks the cut:** if every candidate is thin, build
from the strongest and say so in one line.

A clip it marks `silent` (a photo, a shot with no transcript) is a beat of silence in the heard
script. A segment the transcript returned without word times is checked only at its sentence
edges, and the review says so.
