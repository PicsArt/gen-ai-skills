---
name: speech-cuts
description: Choose the moments of talking footage worth keeping and cut them so no one is clipped mid-sentence - the transcript sets every in and out, the watch picks what is worth it - then read the cut as the viewer will hear it with scripts/review_cuts.py, which flags chopped words, filler and seams that open on "but" or "she", with the time to move each edge to. Use when cutting a short, a reel or highlights from an interview, podcast, vlog, talk or any footage where people speak, and when a finished cut sounds choppy.
user-invocable: false
---

# Speech cuts

A short cut from talking footage lives on its words. The framing can be perfect and the short is
still unwatchable when it opens on half a sentence or spends its first two seconds on "yeah, no,
totally". So the cut is planned from what is **said**, and checked as what is **heard**, before
anything is built.

## Read the footage

Read every source as the media-analysis skill says for talking footage: a transcript saved as
`transcript-<source id>.json`, which sets every boundary, and a watch, which picks the moments. A photo has no speech
at all: it is a beat, not a backbone.

## Plan the cut

1. **One pool of moments.** Take the watch's candidate moments from every source into one list,
   each with the source it came from: its times count on that source's clock, as the reframe
   skill says.
2. **Snap each to whole thoughts.** A clip's `in` is a sentence's first word, or a word after a
   real pause; its `out` is a sentence's last word, or a word before one. The transcript's
   `cutPoints` mark the clean ends.
3. **Order and trim to the target.** Hook first, then the points, then the payoff. Aim for the
   target length within about 15%. **When the length and a clean sentence conflict, the sentence
   wins and the length moves.** Never cut a word out of a sentence to save time: the ear hears the
   splice at once, where the eye would forgive a picture cut.
4. **Place photos at sentence edges**, never inside one, each held long enough to read.

Write the plan as the reel's clip list, the one the reframe skill's `scripts/reel_cut.py` reads,
with each spoken source's `transcript` path beside its other fields.

## Review it as heard

Run `python3 scripts/review_cuts.py reel.json` on that same file. It joins each clip's words in
play order into the **heard script**, and checks three things per clip:

| Check | Fails when | Its repair |
|---|---|---|
| Integrity | an edge cuts through a word, or the clip opens or stops mid-sentence | move that edge to the time given |
| Substance | most of the clip is filler; the opening clip is held to a stricter share | drop it, or take the sentence beside it |
| Fluency | a clip opens on a connective ("but", "so") with nothing before it, or the reel opens on a pronoun no one has been named for | move the in point back to what it refers to, or lead with another clip |

Each clip also lists the `speakers` its words carry. Use them when the reframe skill asks who a
clip should hold on.

**Then read the `script` yourself, as prose.** If it does not hold together as a paragraph, it
will not hold together as a video. The script finds the mechanical faults; whether a clean clip is
worth its seconds is your call.

Apply the repairs to the plan and run it again until it is clean. A repair changes numbers in a
plan, so it costs nothing. **The review never blocks the cut:** if every candidate is thin, build
from the strongest and say so in one line.

A clip it marks `silent` (a photo, a shot with no transcript) is a beat of silence in the heard
script. A segment the transcript returned without word times is checked only at its sentence
edges, and the review says so.
