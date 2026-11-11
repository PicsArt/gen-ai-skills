---
name: voice-over-generation
description: Generate a voice-over from written lines - one voice line per script line in one voice, as one batch, the words alone (a character's line also opens with an emotion tag) with pace and energy in the model's own fields, names spelled as they sound, and every line's real length probed before anything is timed to it. Use when a video needs a generated voice, with a presenter on screen or with no face at all.
user-invocable: false
---

# Voice-over

A voice line is a generated clip of one line of the script. The lines are written by whoever needs
them (a presenter's script, a step's narration); this is how they become audio that the picture
can be timed to.

- **Voice.** One voice line per script line, in the same voice, generated with `picsart_generate`
  as one batch (picsart-video-rules, SPEND). Pick the voice model with `picsart_model_catalog`, and read
  its voices and inputs with `picsart_model_params`.
- **A child character gets a child's voice, or the user is told.** List the speech model's voices with
  `picsart_model_params` and `voices: { query, limit }` (ElevenLabs): search `child`, then `kids`,
  `cartoon` and `cute`, and read the descriptions and tags. Voices in the kids or animation category come first; pick
  from the top results by description, not by position. Send the voice's `id` as `voiceId` and say which voice was
  picked by name; its `previewUrl` lets the user hear it. When the platform refuses a voice request as content
  involving minors, stop: never reword it to get past the refusal. When no listed voice reads as a child's, the
  user is told plainly: "no child voice available, using a young adult voice".
- **Character lines: `eleven-v3`, one emotion tag per line.** A character's dialogue is spoken on `eleven-v3`, each
  line opening with a tag for the mood the acting shows at that beat (`[sad]`, `[excited]`, `[whispering]`), and every
  line of that character keeps the same voice `id`. `eleven-v4-turbo` is for plain narration. The tag is the one thing
  besides the words that goes in the text.
- **The rest of the line is only the words.** Energy and pace go in the model's own fields, as
  `picsart_model_params` names them, never typed into the text. Spell an unusual name the way it
  sounds in the line you send, and keep its written spelling for the captions and the text on
  screen. Pass a language as its two-letter code (`en`), never a region code, unless the model's
  fields list that exact value.
- **Length.** Speech runs at about three words a second, so a 4 s step holds about twelve words.
  Probe every voice line's real length with `picsart_media_probe` before anything is timed to
  it. When a line is longer than the time it has, shorten the line; never stretch the picture to
  fit it. Only that line is generated again.
