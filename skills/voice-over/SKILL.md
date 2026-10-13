---
name: voice-over
description: Generate a voice-over from written lines - one voice line per script line in one voice, as one batch, the words alone with pace and energy in the model's own fields, names spelled as they sound, and every line's real length probed before anything is timed to it. Use when a video needs a generated voice, with a presenter on screen or with no face at all.
user-invocable: false
---

# Voice-over

A voice line is a generated clip of one line of the script. The lines are written by whoever needs
them (a presenter's script, a step's narration); this is how they become audio that the picture
can be timed to.

- **Voice.** One voice line per script line, in the same voice, generated with `picsart_generate`
  as one batch (video-core, SPEND). Pick the voice model with `picsart_model_catalog`, and read
  its voices and inputs with `picsart_model_params`.
- **The line is only the words.** Energy and pace go in the model's own fields, as
  `picsart_model_params` names them, never typed into the text. Spell an unusual name the way it
  sounds in the line you send, and keep its written spelling for the captions and the text on
  screen. Pass a language as its two-letter code (`en`), never a region code, unless the model's
  fields list that exact value.
- **Length.** Speech runs at about three words a second, so a 4 s step holds about twelve words.
  Probe every voice line's real length with `picsart_media_probe_media` before anything is timed to
  it. When a line is longer than the time it has, shorten the line; never stretch the picture to
  fit it. Only that line is generated again.
