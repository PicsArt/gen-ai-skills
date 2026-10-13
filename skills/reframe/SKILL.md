---
name: reframe
description: Put the user's own footage in a frame of another shape - landscape to a vertical reel, say - with the camera following the person, measured once per source, and cut it into a reel of clips back to back with scripts/reel_cut.py, so any re-cut is free. Covers which clips follow the subject and which show the whole frame, photos held as beats, a camera that swings between two people, and hard cuts. Use when a reel or short is cut from the user's own videos and photos, or when a vertical crop loses the subject.
user-invocable: false
---

# Reframe

A vertical crop of a landscape shot keeps about a third of its width. Centred, that third is often
a wall beside the speaker. So the subject's position is measured, never guessed, and the clips are
cut from that measurement by a script.

## Measure each source once

1. **Which sources need it.** A video whose shape differs from the reel's, with a person or
   another subject in it. A source already the reel's shape, and one with nothing to follow (a
   title card, a full-frame graphic, a wide shot with no subject), needs no reframe: its clips are
   `full`.
2. **Reframe it.** `picsart_media_reframe_video` with the source's Picsart-hosted `url` and the
   reel's `aspect_ratio`. It replies with a job receipt, followed as video-core says. It
   takes minutes, so post a line first, and
   start it as soon as the source and the reel's shape are known. It does not need the cut.
3. **Save the result verbatim**, the whole reply, as `reframe-<source id>.json`. Never pass
   `scene` and `layer_id` for this: that mode refuses a trim, and every call measures again.

**One reframe per source and shape, for the whole session.** The result covers the source's whole
length, so every clip, every re-cut and every new running order is windowed from it by the script.
Measuring again for a new cut repeats minutes of work and changes nothing. Its description says
whether it charges credits. If it does, it is a SPEND (video-core): quote every source's reframe in
one go.

If it fails, retry it once: it is flaky, and a later try often succeeds. If it fails again, stop
and say the reframing is unavailable right now, with what is ready. Never estimate the subject's
position from a description of the video, and never frame a talking person `full` as a stand-in.

## Cut the reel

`scripts/reel_cut.py` builds the scene. Write its input to a file and run
`python3 scripts/reel_cut.py reel.json`:

```json
{
  "width": 1080, "height": 1920,
  "sources": [
    {"id": "talk", "url": "<the url you reframed>", "reframe": "reframe-talk.json"},
    {"id": "broll", "url": "<url>", "width": 1920, "height": 1080, "duration": 31.5},
    {"id": "photo", "type": "image", "url": "<url>", "width": 1600, "height": 1200}
  ],
  "clips": [
    {"source": "talk", "in": 12.0, "out": 18.5},
    {"source": "broll", "in": 3.0, "out": 6.0, "frame": "full", "dim": 0.3},
    {"source": "photo", "duration": 2.0},
    {"source": "talk", "in": 40.2, "out": 44.0}
  ]
}
```

- `width` and `height` are the reel's. The sizes and lengths of sources with no reframe come from
  `picsart_media_probe_media`, never from memory.
- Clips play in list order, each `in` to `out` in **its own source's** seconds. A range from one
  source applied to another lands nowhere.
- A reframed source's clips default to `crop`: the camera follows the subject. Others default to
  `full`: the whole frame over a blurred copy of itself (`dim` darkens the copy), or over black
  with `"background": "black"`.
- A photo has no time of its own: its clip gives a `duration`, long enough to read and no longer.
  `full` shows all of it; `"frame": "crop"` fills the frame from its centre.
- With no `transition`, every seam is a hard cut. Keep it that way for speech: a crossfade blurs
  the clean sentence edge the cut was placed on. Add one only when the user asks for it.

It prints one JSON line, `{scene, duration, clips, notes}`. Pass `scene` on as it is: it validates
as it stands, and every clip is a plain media clip the scene editor opens. If it exits 1, its one
line on stderr says what to change.

**A re-cut is a new run.** To trim a clip, swap one, or change the order, edit the clip list and
run the script again. The reframe result stays as it is.

## Crop or full

**A clip with a person talking is `crop`.** Letterboxing a face into a third of a vertical frame is
the defect this skill exists to prevent, not a safe choice. `full` is for a clip with nothing to
follow. When a crop looks wrong, fix the crop (below), never switch the clip to `full`.

## When the camera swings

The reframe follows *a* subject in each frame, not the one speaking. On a two-person shot it can
swing from one to the other, and the crop then lands between them. The script measures that:
`notes` names each clip whose camera crosses more of the source than one person moves, with the
centre to hold:

```
clips[1]: the camera crosses 42% of the source, so it may be following two people; to hold one, cut it again with "hold": 0.773
```

Add that `hold` to the clip and run it again: the clip then holds one still window, as large as
its own crop was. The transcript says who is speaking in that clip. If the hold sits on the
listener, give `hold` that person's side instead, from 0 (the left edge) to 1 (the right). Or
choose a stretch of the speech where only the speaker is in the frame.

## Check

Before the scene is reviewed, run `picsart_media_validate_scene` on it, then
`picsart_media_contact_sheet` at each seam and in the middle of each clip. Look for: a face in
every `crop` frame, not cut by the frame's edge; and no clip that opens on a wall or a hand. Fix
what fails in one new run, as the evaluate skill says.
