---
name: edit-on-your-computer
description: Edit footage on the user's own computer - proxies uploaded instead of the originals, a project folder, and a full-resolution conform with ffmpeg. Use only when the footage is a folder on this machine and you can run commands.
user-invocable: false
---

# Edit on your computer

An edit runs the same way wherever its footage is: the stages, the record and the checks are the
edit-pipeline skill's. This skill adds only what changes when the footage is on this computer and
you can run commands here. Originals are large, and they are the user's masters: they never
leave this computer and are never changed. What the server reads is small copies.

Load this skill only when the footage is a folder or paths on disk and the host runs commands.
Footage given as Picsart Drive files, links or attached files is edited without it. When you
cannot run commands here after all, open `picsart_drive_upload_ask` for the footage and go on
without this skill; never ask the user to upload it by hand.

## The project folder

Keep everything for one edit in one folder beside the footage, never inside it:

| Path | Holds |
|---|---|
| `edit-footage.json` | the record, kept by edit-pipeline's `scripts/record.py` |
| `proxy/` | the proxies and `manifest.csv` |
| `work/` | copies you change (a graded file, a conformed master), never an original |
| `exports/` | each version's draft, and the final files; a new file goes beside an old one |

Quote every path you pass to a command; folder names often have spaces.

## Proxies, before anything is analysed

Make a small copy of each source and analyse only those:

```
ffmpeg -i "<original>" -map 0:v:0 -map 0:a? -vf scale=-2:720 -c:v libx264 -preset veryfast -crf 23 \
  -c:a aac -b:a 128k -fps_mode passthrough -map_metadata 0 -timecode <start> "proxy/<name>.mp4"
```

A source with no picture, such as a voice-over, needs no proxy: upload it as it is. Each proxy
keeps the original's fps, frame count and start timecode. Check that with `ffprobe` on
both files. Write one row per source into `proxy/manifest.csv`: copy, original, fps, frames,
start. The cut list and the conform point back to the originals through it. In the record, a
source gets its `file` (the original) and its `proxy`.

Upload the proxies, never the originals, with `picsart_upload_local_files`, and use the URLs it
returns in every tool after. Then go on with the log as the use case says.

## Per-short windows

A long episode cut into several shorts is uploaded as **one window per short**, not whole: from
the short's first clip to its last, plus a second each side. A whole episode is often past the
100 MB upload limit, and a variable frame rate, B-frames or a stream that starts late can make the
render jump a frame. Each window is re-encoded at a constant 30 fps from 0, a keyframe a second:

```
ffmpeg -ss <A> -to <B> -i "<original>" -vf fps=30,format=yuv420p -c:v libx264 -profile:v high \
  -crf 20 -g 30 -keyint_min 30 -sc_threshold 0 -c:a aac -b:a 128k -ar 48000 -ac 2 \
  -avoid_negative_ts make_zero -movflags +faststart "proxy/win-<short>.mp4"
```

Check each window with `ffprobe` before uploading it: `r_frame_rate` 30/1, the video and audio
`start_time` both 0, and the file under 100 MB (else narrow the window). Every time in that
short's cut is then in the window's seconds: a source second `s` is `s - A`. Write the window's
`A` and `B` beside its row in `proxy/manifest.csv`, so the conform maps back to the original.

## The conform, at the finish

When the user chose the conform, rebuild the approved version from the originals at full
resolution:

1. Read the approved version's plan. Map each shot's proxy range to its original through the
   manifest; the times are the same, since the frame counts match.
2. Cut each range from the original into `work/`, apply the grade there (a log source's camera
   LUT first, then the look), and join them in the plan's order with the approved audio.
3. Check the master against the approved version, frame for frame: the same length, the same cut
   points, the same words when both are transcribed.

A master that differs is fixed in the conform, never delivered as it is.

## The final check, on this computer

Besides the checks the use case runs on every finish, run quality-review's `qc.py` on the master's
`ffprobe` and loudness reading (`ffmpeg -af loudnorm=print_format=json -f null -`): about -14 LUFS
with true peak under -1 dBTP.

## Deliver

Put the final files in `exports/` beside any earlier ones; an old file is removed only on a yes.
The cut list names each original, not its proxy.
