---
name: captions
description: Put spoken words on screen from the transcript - word-timed captions on a generated voice-over or on the user's own talking footage, and on a cut reel, captions per clip and a few highlight phrases timed to the words they call out, placed with scripts/reel_text.py. Use when a video is watched muted and its speech must be read, or when a short's key lines should land on screen.
user-invocable: false
---

# Captions

Every word on screen comes from a transcript, with its times as the transcript gives them. **Never
rewrite the word times.**

## The transcript

1. **Probe before you transcribe.** Check `hasAudio` from `picsart_media_probe_media` first, and
   skip only when it reports `hasAudio: false`, as the media-analysis skill says.
2. Transcribe with `picsart_media_transcribe`:
   - a voice-over you generated: **each generated voice line**. It is our own clean audio, so the
     word edges are exact.
   - the user's own footage: each source once, as the media-analysis skill says. Reuse that
     transcript; never transcribe a cut.

The tool's `notes` name any segment it returned without word times. Caption that segment as one
block over its own start and end; it cannot carry a highlight.

## Captions on a voice-over

Place each line as a `captions` layer through `picsart_media_patch_scene`:
`content: { kind: "captions", transcript, timeOffset }`, where `transcript` is the tool's
`transcript` as returned (it is already shaped for a captions layer) and `timeOffset` is the
line's start in the video.

2–4 words per caption. The caption style's `offset` is measured from the frame center
(`[0, -810]` puts it at y ≈ 150 in a 1080×1920 frame); keep captions in a dark band of the
layout, never over a panel or the focus point.

**Readable over any picture, and the spoken word lit.** A caption crosses moving footage, so give
its style an outline and light the word being spoken:

```json
"style": {
  "effects": [{"id": "stroke", "params": {"width": "<px>", "color": "<outline colour>"}}],
  "decorations": [{"target": "highlighted", "place": "text", "color": "<highlight colour>"}]
}
```

Read the effect's id and params from `picsart_media_get_capabilities` (`effects`) rather than
from here; this shape passed `picsart_media_validate_scene` on 2026-10-05. One highlight colour
for the whole video, the brand's when it has one.

## Words on a cut reel

A reel cut from the user's footage plays each source in pieces, so its words are placed from the
scene the user approved, with `python3 scripts/reel_text.py words.json`:

```json
{
  "scene": "scene.json",
  "transcripts": {"talk": "transcript-talk.json"},
  "captions": {"style": {"font": {"size": 64}, "offset": [0, 440]}},
  "highlights": [
    {"clip": 0, "say": "revenue tripled", "text": "Revenue tripled"},
    {"clip": 4, "say": "nobody tells you this"}
  ]
}
```

`transcripts` maps each spoken source's asset id to its saved transcript. Ask for `captions`,
`highlights` or both. The script reads each clip's place on the reel and its trim from the scene,
so a clip the user retrimmed in the editor is read as they left it, and it prints the scene with
the new layers on top. A phrase it had to cut short comes back in `notes`.

- **Captions** become one `captions` layer per spoken clip, open while that clip plays its
  source, with the source's transcript as returned. A clip held past its `trim.out` freezes on its
  last frame, so its captions close where the trim ends. The reel ends at the composition's
  `duration`, or with none at the track layer's: captions stop there. A photo, a `muted` clip, a
  shot without a transcript or a clip past the reel's end gets none, and a highlight on a muted
  clip or one past the end is refused.
- **Highlights** all go on one `captions` layer, one segment per phrase, each on a pill the
  renderer fits to the measured words. Pass `highlightStyle` to change the look; the font follows
  the scene-compose skill.

### Choosing highlights

Highlights are a few lines worth reading, not subtitles.

- **2–4 per reel, 2–6 words each, verbatim from the transcript.** `say` is what was said;
  `text` may drop a filler word or fix its case, never change what it says.
- Pick the hook, the number, the rehook (the turn near the middle, as the story-loops skill names
  it) and the payoff: the words a viewer should remember. Skip
  greetings, filler and anything already said on screen.
- **Draft them before you place them:** each phrase with its clip, so the use case can offer
  them. The reel is complete without them.
- One at a time. The script holds each from its first word to half a second past its last,
  1.5–3 s, and never past its clip or into the next phrase.
- **Big, high-contrast, inside the platform's safe band and off the face.** The use case names
  the band. With captions on too, keep the two in different bands.

Check the result as the evaluate skill says, with a frame at each phrase's `start`.
