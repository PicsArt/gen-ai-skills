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
- **A failed batch gets one retry, inside what the user approved.** When the voice batch (or some of its lines) fails
  because the speech model itself errors (a server error, not a refusal), take the next speech models
  `picsart_model_catalog` lists, with a voice of the same kind from each model's own voices (`picsart_model_params`),
  and quote the whole retry on each: the failed lines plus any lines of the same character that must be made again. A
  yes covers what was quoted, once (picsart-video-rules, SPEND rule 3), so a retry on another model is a new run and
  needs a new yes, whether or not the first attempt charged. The one exception is a spend limit the user stated in
  words: then switch automatically to the first model whose whole-retry quote is no higher than that limit minus
  everything already spent on this request (the lines that succeeded included, and a charge counted unless the tool says
  it was not made), generate the complete quoted set once, keep the lines that worked for the characters the failure did not touch, and say it in one line ("ElevenLabs
  failed, so these lines were made on <model>, within your limit"). Otherwise SPEND (quote it in one line, then get the yes with `picsart_ask`, found as picsart-video-rules says, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", else your host's own question tool, such as AskUserQuestion; never as a typed question unless both fail; only then those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says): ask once with the cheapest
  quote and its price, and generate nothing until the user agrees. Never mix two models inside one character's lines: a character with a failed line has all of its lines made again on the new model, in that one quoted set and never twice.
  Ask the user too when the
  retry fails. A refusal for content, a credit error or a bad input is not a model error and is not retried this way.
- **A `422 invalid_text` is the provider's content filter on that one line.** Reword only that line (a mnemonic or a blunt
  phrase is the usual cause), say so to the user in one line with the new wording, and keep every other line as it is.
