# Watching talking footage

Send this as the `question`, with the user's brief (what the short is for, its length) in one line
before it, and ask for one JSON object only:

- `moments[]`: each `{ start_s, end_s, what_happens, why_it_works, strength }`, the candidates
  worth keeping, strongest first. `strength` is `hook | strong | ok`. A moment is something a viewer
  would rewind for: a claim, a number, a laugh, a turn, a reaction.
- `dead_ranges[]`: each `{ start_s, end_s, why }`: setup, false starts, crosstalk, someone off
  screen, a long silence.
- `people[]`: each `{ who, where, when }`: a short description of each person on screen, where they
  sit in the frame (`left | centre | right`), and the ranges they are on screen. The transcript's
  speaker tags say who talks; this says who is seen.
- `shots[]`: each `{ start_s, end_s, framing }` for footage that already cuts between shots, so a
  clip never straddles a cut it did not choose.
- `register`: one line on the tone (earnest, playful, heated, instructional) and pace.

Every time here is an estimate on that source's clock. The transcript sets the cut boundaries, and
the footage-reframing skill measures where a person sits.
