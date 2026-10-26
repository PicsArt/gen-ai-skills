---
name: footage-analysis
description: Watch the user's own talking footage and turn it into facts you can build on - its moments worth keeping, who is on screen, and a transcript whose sentences set every cut - read every source at once and follow the job receipts. Use when a use case needs to know what happens in an interview, podcast, vlog, talk or any footage of people speaking, and when. A screen recording's pictures are read by the screen-recording-analysis skill; only its spoken narration is transcribed here.
user-invocable: false
---

# Media analysis

Know what the footage shows, and when, before you build on it. This skill reads people talking to
camera, an interview, a podcast or a vlog; read `references/talking-footage.md` before you watch it.
A screen recording is read from its pixels, as the screen-recording-analysis skill says. When it carries the user's own narration, that speech is
transcribed here like any talking footage, and nothing in it is watched.

## Watch

1. `picsart_media_probe` on the file: dimensions, duration, and whether it has audio. It
   reports container facts only, never what is shown.
2. `picsart_media_describe_video` with the use case's request as its `question`, asking for JSON,
   not prose. It charges credits on every call, so the use case gets consent before it runs. Read its
   `answer`.
3. Unless the probe reports `hasAudio: false`, and when the narration is worth quoting,
   `picsart_media_transcribe` the file. The probe leaves `hasAudio` out when it cannot tell, and
   that is not a no.

The probe and the watch do not depend on each other; run them at the same time. **The watch is
critical.** If it fails, or its `answer` is not the JSON you asked for, retry the same call once.
If that fails too, tell the user the service is down and to try again shortly. Never guess the
content from nothing.

**The watch and the transcript reply with a job receipt**, not the result: follow it as picsart-video-rules
says.

**With several sources, read them all at once.** Every video gets its own probe, watch and
transcript, and none waits for another. A photo gets only the probe, for its size: it has no
speech and nothing happens in it over time.

## Talking footage

When people speak, the two reads have different jobs:

- **The transcript is the only source of where a thought starts and stops.** Transcribe every
  spoken source, with `speakers: "auto"` when more than one person may speak. Save the result
  verbatim as `transcript-<source id>.json` and pass that file to the scripts that need it; keep
  only the segment list in mind, never every word.
- **The watch says what is worth keeping**: the strong moments, the dead stretches, who is on
  screen. Its sense of the audio is the gist, never a boundary.

**An empty transcript means no speech**, not a failure to retry. Nor is a thin one a transcript
to cut on: segments covering a sliver of the runtime, or none with word times. Say in one line
that the footage has almost no speech, and let the watch's moments set the boundaries.

The watch's idea of where a person sits is an estimate. Never frame a crop on it: the footage-reframing
skill measures the subject from the footage.
