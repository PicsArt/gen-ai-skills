# The QC inspector

An edit of the user's own footage is checked by an inspector who did not make it, from the
render alone. In a live edit of supplied footage, this independent check found what still frames and critics
never did: a voice line drifting 0.24 s, a mouth moving under the voice-over, a confidential note
readable on a desk, and a camera drift a shake gate had passed on plain paper.

## When it runs

- On every draft of an edit, before the user sees it, and on each fix after it.
- A fresh inspector each round. Never continue an earlier one: it carries the earlier render and
  its own earlier verdicts.
- Fix rounds are capped as picsart-video-rules says (Evaluation). When they run out, show the user
  what is left as an A/B; never loop again.

## What you give it

Where the host has the inspector as an agent (its host notes say so), start the agent
`qc-inspector` by name. On every host, its whole brief is in this skill as
`references/agent-qc-inspector.md`. Give it only:

- the render's URL (or its file, where you run commands) and its version name;
- the render's transcript: `picsart_media_transcribe` on the exported file, with its words;
- the script and the plan: each shot's range in the render, its source and its phrase;
- stills at every used range: `picsart_scene_contact_sheet` with the render as `media`, at each
  shot's first, middle and last frame, eight times a call. It is free;
- the steadiness of the sources' used ranges, where it was measured: the detail tracked, the
  movement per window, and whether the detail had texture. Measure each source range once, with
  `picsart_media_track_motion` on a fixed patch with texture, captions left out, keep it in the
  project record, and reuse it while the range is unchanged;
- from the project record, word for word: `standing`, `locked`, `keepers` and `cutPace`;
- when the record holds a reference's `format`: the format, its reference stills beside the
  render's frames at the same moments, and `scripts/reference_match.py <scene> <record>`'s output
  where you run commands (it reads the layout, the caption position and size, the hook and the
  end card from the scene). Without commands, the inspector reads the same from the stills;
- the meaning diff's lines against the last version the user saw, as the edit-pipeline skill's
  `scripts/meaning_diff.py` gives them;
- in a later round, the earlier rounds' findings, without your answers to them;
- the cold watch's gap list, when one ran on this draft.

Never give it the conversation, your reasons for a choice, or a critic's note. Without the agent,
run it as its own isolated worker where the host can, its prompt the whole text of
`references/agent-qc-inspector.md`, the "Looking at an image" section of your host notes and the
list above; inline otherwise, with its report written out in full before you go on.

## What it returns, and what you do with it

Keep its JSON with the version in the project record (as `qc-<version>-r<round>.json` where you run commands). Where you run commands, run
`python3 scripts/inspection.py qc-<version>-r<round>.json --record <record>` from this skill's
folder; elsewhere, read the report by the same rules. It checks the report's shape, drops anything
below major, and gives:

- `verdict`: `pass`, `fix` or `open`, recomputed from the findings;
- `blocking`: the critical findings;
- `conflicts`: findings whose fix would touch a locked row;
- `open`: what could not be checked.

Then:

1. **`blocking` and the other findings** go into the next fix round. Fix each with its
   alternative, keeping every shot's job.
2. **`conflicts`** are never fixed silently. Show the user the problem and the alternative as a
   rendered A/B, and keep the locked row unless they choose otherwise.
3. **`open`** goes to the user with the version: what could not be checked and why, with an A/B
   where a choice is involved. Never call it checked.
4. Write the verdict into the version's `gates` in the record.
