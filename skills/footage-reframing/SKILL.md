---
name: footage-reframing
description: Put the user's own footage in a frame of another shape - landscape to a vertical reel, say - with the camera on the right person - measured once per source, checked and corrected by hand where the tool fails (a subject cut off, the wrong speaker, a late or jittery camera), then cut into a reel with scripts/reel_cut.py, so any re-cut is free. Use whenever footage is reframed or a reframe is checked - a reel or short from the user's own videos and photos, a landscape video reposted as a vertical one - or when a reframe or vertical crop misframes the subject.
user-invocable: false
---

# Reframe

A vertical crop of a landscape shot keeps about a third of its width. Centred, that third is often
a wall beside the speaker. So the subject's position is measured, never guessed, then checked and
corrected where the tool got it wrong, and the clips are cut from that path by a script.

This skill owns all reframing: the tool call, the check, the correction and the cut. A use case
that reframes loads it and keeps no reframing method of its own.

## Measure each source once

1. **Which sources need it.** A video whose shape differs from the reel's, with a person or
   another subject in it. A source already the reel's shape, and one with nothing to follow (a
   title card, a full-frame graphic, a wide shot with no subject), needs no reframe: its clips are
   `full`.
2. **Reframe it.** `picsart_media_reframe_video` with the source's Picsart-hosted `url` and the
   reel's `aspect_ratio`. It replies with a job receipt, followed as picsart-video-rules says. It
   takes minutes, so post a line first, and
   start it as soon as the source and the reel's shape are known. It does not need the cut.
   A local file or a Drive file is used by its Picsart-hosted URL, as picsart-video-rules says
   for asset URLs; every check below reads that same URL.
3. **Keep the result verbatim**, the whole reply: as `reframe-<source id>.json` where you run
   commands, else in the project record. Never pass
   `scene` and `layer_id` for this: that mode refuses a trim, and every call measures again.

**One reframe per source and shape, for the whole session.** The result covers the source's whole
length, so every clip, every re-cut and every new running order is windowed from it by the script.
Measuring again for a new cut repeats minutes of work and changes nothing. Its description says
whether it charges credits. If it does, it is a SPEND (picsart-video-rules): quote every source's reframe in
one go.

If it fails, retry it once: it is flaky, and a later try often succeeds. If it fails again, stop
and say the reframing is unavailable right now, with what is ready. Never estimate the subject's
position from a description of the video, and never frame a talking person `full` as a stand-in.

## Check and correct

The tool follows a face, or else the most salient region, frame by frame. It does not know who is
speaking, what the story needs kept, or where the platform's buttons sit. **Check every reframe
before cutting from it, and correct what fails.** Never pass a reframe on unseen, and never measure
again hoping for a better one: the same footage gives the same path.

| Failure | What it looks like | Finding |
|---|---|---|
| Subject cut off | a head, a chin or the hands past the frame's edge, or under the platform's buttons | `cut-off` |
| Wrong person | the camera on the listener, or never switching to the new speaker | `wrong-person` |
| Late or jumpy cut | the camera reaches the speaker a second into their line, or leaps where nobody new speaks | `late-cut`, `jumpy-cut` |
| Jitter or wander | the window trembles, or drifts across a speaker who sits still | `jitter`, `wander` |
| Lost detail | a product, a sign or on-screen text the story needs, outside the frame | `cut-off` on a `keep` subject |
| Soft picture | zoomed in so far the picture turns soft | `soft` |

### What to read

- **Where each subject is.** One `picsart_media_video_stills` sheet of the source, with `labels`,
  at about one still per used stretch and one at each change of speaker. Read off each person's
  box `[x, y, w, h]` in source pixels, around the head and the hands, and the box of anything that
  must stay in frame. One box per subject is enough for a seated interview. For someone who walks,
  `picsart_media_track_motion` with that box over the stretch gives the box over time.
- **Who speaks when.** The transcript the footage-analysis skill made: each turn's speaker and
  times, the speaker matched to a box on the sheet.

### With a shell

Write what you read to `framing.json`, as the script's header says, and run
`python3 scripts/reframe_fix.py check framing.json`:

```json
{
  "reframe": "reframe-talk.json", "width": 1080,
  "subjects": {"ana": {"boxes": [{"t": 0, "box": [300, 150, 300, 700]}]},
               "ben": {"boxes": [{"t": 0, "box": [1300, 150, 300, 700]}]},
               "mug": {"boxes": [{"t": 0, "box": [740, 600, 60, 80]}]}},
  "speakers": [{"who": "ana", "start": 0.3, "end": 5.8}, {"who": "ben", "start": 6.2, "end": 11.5}],
  "keep": ["mug"],
  "out": "reframe-talk.fixed.json"
}
```

It prints `{ok, findings}`, each finding a kind from the table with its stretch in source seconds.
`ok: true` means the reframe stands: cut from it as it is, and change nothing.

### Without a shell

Read the camera from the reframe's layer: at each keyframe, the source point at the frame's
centre is `srcW / 2 + (frameW / 2 - position x) / scale`, and the frame shows `frameW / scale`
source pixels across. A box is safe when it sits inside that window less 6% a side, 8% at the top
and 12% at the bottom. Check the moments the sheet shows, and each change of speaker.

### Correct it, smallest fix first

1. **The camera path, by hand.** With a shell, `python3 scripts/reframe_fix.py fix framing.json`.
   It holds the camera on whoever speaks, cuts to the next speaker 0.1 s before their first word
   (a reply shorter than 1.2 s keeps the shot), smooths what moves, moves the window the least that
   puts each kept box in the safe area, and caps the zoom. It writes `out` in the tool's own shape,
   and prints `before`, `after` and `notes`. `spans` take over a stretch: `follow` one subject,
   `hold` a still window, `static` for the tool's own window held, or `auto` for the tool's path.
   Without a shell, write the same path into the kept reframe yourself: per speaker turn, two
   keyframes with the same `position` (held), `position x = frameW / 2 - (centre - srcW / 2) *
   scale`; the last keyframe before a cut takes `"easing": "step"`, one frame before the cut.
2. **The tool again, only when its path is too coarse**: a fast move rounded off. Lower
   `tolerance_px` or raise `max_keyframes`. It takes no hint of whom to follow, so a wrong person
   or a cut-off subject is never fixed by running it again. A `wrong-person` that the path fix
   still leaves (a multi-camera show cut between people) goes to fixed crops per shot type, as
   [the split layout](#the-split-layout) builds them, even for a single frame.
3. **A different layout for a stretch.** When what must be seen does not fit one window (the script
   notes it: "hold one subject, or stack the two"), hold one person with a `hold` span, or stack
   the two: above the reel's track for that stretch, two media layers of the source, each `"fit":
   "cover"` with `"bounds": [1080, 960]`, a `crop` on one person and `position` `[540, 480]` or
   `[540, 1440]`.

Cut from the corrected reframe from then on, and keep both in the project record (their file names,
where you run commands). Run
the check again: what `after` still lists is either fixed in another pass or said to the user.

### Show the change

A correction the user did not ask for is shown, never described. Build the reel from both files
(each build is free), and show one `picsart_scene_contact_sheet` of each at the same moments, the
corrected one first. When the fix was a judgment call (which person to hold, a hold or a stack),
ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) which one to keep, with the two sheets as the options. A user who wants a stretch framed
otherwise moves it in `picsart_scene_editor`; read the window they chose back into a `hold` span
and run the fix again, so the next re-cut keeps it.

Without a shell the reel is not built, so neither are the two sheets. Keep both reframes in the
record, and show the change where the scene builder runs, before the first cut is reviewed. Until
then the correction is not shown, and never described in words instead.

## Cut the reel

`scripts/reel_cut.py` builds the scene. Write its input to a file and run
`python3 scripts/reel_cut.py reel.json`. Where you cannot run commands, stop here as
picsart-video-rules says for a script that builds the scene; the reframe, checked and corrected,
stays in the record for the build there:

```json
{
  "width": 1080, "height": 1920,
  "sources": [
    {"id": "talk", "url": "<the url you reframed>", "reframe": "reframe-talk.fixed.json"},
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
  `picsart_media_probe`, never from memory.
- Clips play in list order, each `in` to `out` in **its own source's** seconds. A range from one
  source applied to another lands nowhere.
- A reframed source's clips default to `crop`: the camera follows the subject. Others default to
  `full`: the whole frame over a blurred copy of itself (`dim` darkens the copy), or over black
  with `"background": "black"`.
- A photo has no time of its own: its clip gives a `duration`, long enough to read and no longer.
  `full` shows all of it; `"frame": "crop"` fills the frame from its centre.
- With no `transition`, every seam is a hard cut. Keep it that way for speech: a crossfade blurs
  the clean sentence edge the cut was placed on. Add one only when the user asks for it.
- A channel's own end card (the record's `format.endCard`) goes in `endCard`, `{url, type, width,
  height, duration}`, as the file was given: it closes the reel muted, its length snapped to the
  frame grid. Never rebuild it or rewrite its words.

It prints one JSON line, `{scene, duration, clips, notes}`. Pass `scene` on as it is: it validates
as it stands, and every clip is a plain media clip the scene editor opens. If it exits 1, its one
line on stderr says what to change.

**A re-cut is a new run.** To trim a clip, swap one, or change the order, edit the clip list and
run the script again. The reframe result stays as it is.

## The split layout

When the record's `format.layout.mode` is `split-v` (or `stacked`), the reel shows two people at
once, one above the seam and one below, each a **fixed crop** of the source. No reframe is
measured: who is on screen comes from the shot, and who speaks from the locked map or the
transcript, never from a reframe.

1. **The shots.** `picsart_media_segment_shots` on the source gives its cuts. Take one
   `picsart_media_video_stills` frame per kind of shot (the two-shot, the host's camera, ...),
   name each kind by eye, and write `shots`: per source, `[start, end, kind]` in its own seconds.
2. **The crops.** Read off the sheet a crop per person and per kind of shot, `[x, y, w, h]` in
   source pixels (`crops`); which two sit above and below the seam for each kind (`halves`); and
   a full-frame crop per person (`full`) for emphasis. Read each face's box from the same stills.
3. **Check the crops before anything is built.** With a shell,
   `python3 scripts/reframe_fix.py check-crops crops.json` with `{"crops": {...}, "faces": {"annie":
   [180, 130, 200, 230]}}`: each face inside its crop less 8% at the top, 6% a side and 12% at the
   bottom. A `cut-off` finding names the edge and the pixels to move; an `unchecked` crop has no
   face given yet. Without a shell, check the same margins by eye on the stills.
4. **Emphasis.** A full-frame moment on one person: `{source, in, out, who, from}`, where `from` is
   `map` (the locked map names it) or `transcript`. With `speakers` (the transcript's turns), the
   script refuses an emphasis whose `who` is not the one speaking.
5. **Cut it** with `reel_cut.py`, the same input plus `layout`, `shots`, `crops`, `halves`, `full`,
   `emphasis` and `speakers` (`scripts/split_layout.py`, which reel_cut.py runs for a split and is
   never run alone, has the shape in its header). It builds two tracks in
   lockstep: `top` carries the sound, `bottom` is muted, and under a full-frame piece it plays
   black. The end card closes the top track full frame. A split cuts hard: it takes no
   `transition`. When `format` is given beside it and its layout differs, the script refuses the
   cut: change the layout only with the user's `format:layout` approval.

The seam captions and the hook come next, from the spoken-captions skill.

A source whose probe shows a frame rate other than a whole 30 (or 25, 24, 60), or that came from a
download, can jump a frame in the render. Where you run commands, edit-on-your-computer re-encodes
it per short first. Without a shell, say so in one line when the cut is first shown, and check
the render's seams for a jump.

## Crop or full

**A clip with a person talking is `crop`.** Letterboxing a face into a third of a vertical frame is
the defect this skill exists to prevent, not a safe choice. `full` is for a clip with nothing to
follow. When a crop looks wrong, fix the crop (above), never switch the clip to `full`.

## When the camera swings

On a two-person shot the tool can swing from one person to the other, and the crop then lands
between them. Correcting the path with the speakers' turns, as above, fixes it for every clip. For
one clip, the script measures it: `notes` names each clip whose camera crosses more of the source
than one person moves, with the centre to hold:

```
clips[1]: the camera crosses 42% of the source, so it may be following two people; to hold one, cut it again with "hold": 0.773
```

Add that `hold` to the clip and run it again: the clip then holds one still window, as large as
its own crop was. The transcript says who is speaking in that clip. If the hold sits on the
listener, give `hold` that person's side instead, from 0 (the left edge) to 1 (the right). Or
choose a stretch of the speech where only the speaker is in the frame. A corrected path cuts
between speakers on purpose, so the script notes no swing on it.

## Check the reel

Before the scene is reviewed, run `picsart_scene_validate` on it, then
`picsart_scene_contact_sheet` at each seam and in the middle of each clip. Look for: a face in
every `crop` frame, not cut by the frame's edge; the speaker, not the listener, in each clip; and
no clip that opens on a wall or a hand. Fix what fails in the framing (`framing.json` where you run commands) and cut again, as the
quality-review skill says for one new run.
