---
name: music-bed
description: Draft, generate and lay an instrumental music bed under a finished video's speech - a five-slot brief read off the video, one generation on a music model from the catalog, and the bed mixed with scripts/music_bed.py so it dips under every spoken line and returns between them, with how to move its levels. Use when a final cut gets music under it, when a brief is redrafted for a steer, or when a laid bed sits too loud or too soft.
user-invocable: false
---

# Music bed

A talking video is often nearly done and still feels dry: no energy between the lines, dead air
at the seams. A bed fixes that, as long as it stays under the voice. Drafting the brief costs
nothing; the generation charges credits.

## The brief

**Draft it on the final picture.** A bed scored on a cut that is still changing is scored twice.

Draft the brief from what the video already tells you, in two or three lines, so it can be read
whole before anything is generated.

A brief names five things, and a model guesses whatever is missing:

| Slot | From | Example |
|---|---|---|
| Genre | the transcript's tone, not its topic | warm lo-fi hip-hop |
| Instruments | the genre | mellow Rhodes, upright bass, soft vinyl crackle |
| Tempo and energy | the picture's pace | around 90 BPM, unhurried |
| Mood | what is said, and how | intimate and reflective |
| **Purely instrumental**, in positive words | always | purely instrumental throughout, carried by the instruments above |

End it with what the bed is for: "sits quietly under a speaking voice without competing with it".
`references/prompt-craft.md` has a brief for each kind of video and the mistakes that ruin one.

**Instrumental under speech, always.** Sung words fight the speech for the same ear, and both
become mush. Say it in positive words: a music model can sing a bare negation, so "no vocals" or
"no lyrics" may come back as a voice singing it. Write vocals in only when they were asked for;
they will fight the dialogue.

## Generate it

1. Pick a model from `picsart_model_catalog` with `inputType: "music"` and
   `purpose: "generate"`, and read its fields with `picsart_model_params`. Use its instrumental
   switch when it has one, and leave any `lyrics` field empty: lyrics are what a voice sings, and
   a brief put there is sung.
2. Ask for a bed **about a tenth longer than the video**, rounded up to the second, within the
   model's own limit: music models tend to come back short. The mix trims a longer bed; a shorter
   one leaves silence at the end.
3. Validate the payload with `picsart_preflight`, whose estimate is the bed's price, then call
   `picsart_generate` once.

One generation per brief. A track that misses gets a new brief, with the steer applied to the
slots it touches, and a new generation. Never fire variants hoping one lands.

## Lay it under the speech

Run `python3 scripts/music_bed.py bed.json` on the final scene:

```json
{
  "scene": "scene.json",
  "transcripts": {"talk": "transcript-talk.json"},
  "music": {"url": "<the bed's hosted URL>", "duration": 32.0}
}
```

`transcripts` names every spoken source's saved transcript by its asset id: a clip of the reel, a
voice-over layer or a presenter's take alike, nested panels and bubbles included (the scene's
own id for the source, not the nest's `rec`); media-analysis says how a source gets one.
`duration` is the bed's length, as the generation or `picsart_media_probe_media` reports it. The script adds the bed as one `audio` layer: faded in over 1 s and out over 2 s, at
volume 30 between lines and 15 under speech, dipping just before each spoken stretch and coming
back over 0.6 s after it. It prints the scene and the stretches it ducked under.

- **The speech stays on top.** When the bed competes, lower `level` and `duck` together; never
  raise the speech.
- No tool here reads a mix's loudness back, so nothing measures the bed against the voice; only
  a listener can. **Move it by note:** each note on how it sits moves `level` and `duck` together
  by about five points, and the script runs again on the same scene.
- **Never drop the speech.** Leave every clip's and voice-over's own sound as it is; the bed goes
  under it.

A different track is a new brief and a new generation, never a silent regeneration.

## One video

The bed goes into the one video, never a music version beside a silent one. **The licence
caveat** travels with it: a generated track's licence is the user's to check before a festival or
a commercial use.

**The bed never blocks the video.** A generation that fails, or a bed that cannot be laid after
one retry, leaves the scene as it was, without music.
