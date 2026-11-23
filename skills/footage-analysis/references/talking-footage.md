# Watching talking footage

Send this as the `question`, with the user's brief (what the short is for, its length) in one line
before it, and ask for one JSON object only:

- `moments[]`: each `{ start_s, end_s, what_happens, why_it_works, strength, kind, question,
  answer_at }`, the candidates worth keeping, strongest first. `strength` is `hook | strong | ok`.
  A moment is something a viewer would rewind for: a claim, a number, a laugh, a turn, a reaction.
  It is one question a viewer holds and sees answered in the clip: `question` says it in the
  viewer's words, and `answer_at` is the second it is answered, inside the range. `kind` is
  `action`, `conversation` or `talk`, and sets what proves a claim:
  - `action` (a game, a sport, a build): something happens, from its cause to its consequence, and
    the picture proves it. When a line sums up an action after it, the moment is the action, with
    the line at most part of it.
  - `conversation` (a podcast, an interview): the face is the picture, so the proof is the
    speaker's own story, number, name or example, said inside the range. A boast with none is no
    moment.
  - `talk` (a lecture, a keynote): one idea with its example, or the slide or the room's laugh
    that proves it.
- `dead_ranges[]`: each `{ start_s, end_s, why }`: pre-roll (mic checks, framing), false starts,
  crosstalk, someone off screen, a long silence. Story setup is never dead: when a moment leans on an
  earlier sentence (who someone is, the question it answers), its `why_it_works` names that sentence
  and its time, so the cut keeps them together.
- `people[]`: each `{ who, where, when }`: a short description of each person on screen, where they
  sit in the frame (`left | centre | right`), and the ranges they are on screen. The transcript's
  speaker tags say who talks; this says who is seen.
- `shots[]`: each `{ start_s, end_s, framing }` for footage that already cuts between shots, so a
  clip never straddles a cut it did not choose.
- `register`: one line on the tone (earnest, playful, heated, instructional) and pace.

Every time here is an estimate on that source's clock. The transcript sets the cut boundaries, and
the footage-reframing skill measures where a person sits.
