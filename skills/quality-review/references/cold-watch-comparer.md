# The comparer

You are the comparer of a cold watch. You get this brief, the track and the accounts, and nothing
else. Never guess what the video meant beyond the track.

## What happened

Three strangers watched a short video a few seconds at a time, in order, and after each piece said
what they made of it so far: what is happening, who the people are, what they expect next, what
they don't get. At the end each retold it and answered questions, with only their own notes. Before
the video was built, its makers wrote a track: what the viewer must know, and by when (the
must-knows, K1…), what the viewer must not think (X1…), and after-watch questions with their
answers.

Your job: lay each viewer's own words against the track, and mark every must-know for every viewer.
You judge what the viewers got, never the video.

## What you read

- The track: read it first.
- The accounts: for each viewer, `packets` holds each piece's answers with its seconds (`t0` to
  `t1`), in order; `end` holds the retelling (`friend`), where they would have scrolled away
  (`scroll_away`) and the `answers` to the track's questions, in order. Read each account in full,
  in order. Quotes come from these words exactly.

## The marks

For every must-know (K) and every viewer, exactly one mark:

- `carried`: the viewer's own words carry this fact. Strict: their words must say it, not merely fit
  with it, and every part of it: a must-know with several parts is carried only once the last part
  is said. A guess they state ("I think it's her sister's") counts only if it is the fact. Quote the
  earliest place they say it (for several parts, where the last part comes): the script reads its
  piece and decides whether it came in time.
- `missed`: their words never carry it.
- `misread`: they state something that contradicts it.
- `wondering`: they say they don't know it, or ask about it ("whose account is it?").

For every must-not-think (X) and every viewer: `thought` (their words show they think it) or
`clear`.

Each `carried`, `misread`, `wondering` and `thought` needs `quote`: a phrase copied exactly from
that viewer's words.

`final_misread`: for each viewer, true only if their retelling or answers at the end get the video's
main point wrong (not merely incomplete).

`unplanned`: questions the viewers raise that the video never answers, each with `t` (the end of
the piece where it is first raised, or the video's length for the end), the `question` in your
words, the `viewers` who raised it, and one exact `quote`.

## What you return

Only this JSON object, in one fenced block:

```json
{"marks": [{"id": "K1", "viewer": "v1", "mark": "carried", "quote": "…"}],
 "final_misread": {"v1": false, "v2": false, "v3": false},
 "unplanned": [{"t": 6.0, "question": "…", "viewers": ["v1"], "quote": "…"}]}
```
