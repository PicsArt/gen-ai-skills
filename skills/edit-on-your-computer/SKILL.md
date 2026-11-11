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

## ffmpeg first

Everything below runs on `ffmpeg` and `ffprobe`. Before the proxies, check both:
`command -v ffmpeg ffprobe`. When either is missing, ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) how to go on. Recommended first:
"Install ffmpeg-full, the full ffmpeg with subtitle support", saying exactly what: on a Mac with
Homebrew, `brew install ffmpeg-full` (Homebrew's own formula, with libass for the captions; it
installs beside any other ffmpeg without replacing it, so run it as
`"$(brew --prefix ffmpeg-full)/bin/ffmpeg"` and `.../bin/ffprobe`); elsewhere, a build linked from
https://ffmpeg.org/download.html whose `ffmpeg -filters` lists `subtitles`. The other option: "Edit
without it: you upload the footage, and the finish is a full-quality export". **Never install
anything without the user's yes to this question.** A yes goes into `approvals` with the scope
`install:ffmpeg` and covers exactly that package, which the captions need too (below), so it is
never asked twice. In unattended pace, the assumed answer is the upload, but the upload needs the
user: write it to `openDecisions` and stop there. When the install fails or needs an administrator
password, say so, offer the upload, and never retry it unasked. On the upload, open
`picsart_drive_upload_ask` for the footage, leave the `proxies` stage out of the record's pipeline,
set `finish` to `export`, and go on without this skill.

## Proxies, before anything is analysed

Make a small copy of each source and analyse only those. Read each original's curve first (Log
footage, below): a log source's proxy is made through its conversion, not with this command.


```
ffmpeg -i "<original>" -map 0:v:0 -map 0:a? -vf scale=-2:720 -c:v libx264 -preset veryfast -crf 23 \
  -c:a aac -b:a 128k -fps_mode passthrough -map_metadata 0 -timecode <start> "proxy/<name>.mp4"
```

A source with no picture, such as a voice-over, needs no proxy: upload it as it is. Each proxy
keeps the original's fps, frame count and start timecode. Check that with `ffprobe` on
both files.

**Which way is up** is judged here, before the proxy, from one still in the middle of the
original (`ffmpeg -ss <middle> -i "<original>" -frames:v 1 "proxy/<name>.mid.jpg"`), as the use
case's log says. A turned source's proxy is made turned, so everything after it sees it upright:
its transpose goes first in `-vf`, before the scale (`transpose=1` for `rot90`, `transpose=2`
for `rot270`, `hflip,vflip` for `rot180`). Its `upright` goes into its `sources` row; the build
lays such a proxy as it is and never turns it again. When `upright` is turned but the
manifest's `turn` is empty (found after the proxies), the build turns the clip layer instead;
never remake the proxy, whose new URL would make the log stale. The original is never changed:
the conform turns it.

Write one row per source into `proxy/manifest.csv`: copy, original, fps, frames, start, turn. The cut list and the conform point back to the originals through it. In the record, a
source gets its `file` (the original) and its `proxy`.

Upload the proxies, never the originals, with `picsart_upload_local_files`, and use the URLs it
returns in every tool after. Then go on with the log as the use case says.

## Log footage, read before the proxies

A camera shooting a log profile (S-Log3, V-Log, C-Log, D-Log...) records a flat, grey picture meant
to be converted before anyone judges it. The scene has no camera LUT, so a log proxy stays milky in
every preview, contact sheet, describe and check, and a grade built on it is built on the wrong
picture. Read each original's curve before making its proxy:

```
ffprobe -v error -show_streams -of json "<original>" > "proxy/<name>.probe.json"
python3 scripts/log_profile.py --file "<original>" --probe "proxy/<name>.probe.json"
```

**When `python3` is missing** (on a Mac without the command-line tools, it opens an install
dialog and fails), never wait on it: make plain proxies, say in one line that the previews may
look flat if the footage is log, and put the log check in `openDecisions`. The same holds for
`log_lut.py` below. Never install it unasked.

`ffprobe` alone rarely knows: a Sony file reports its transfer as unknown and its range as full.
The script reads the camera's own metadata, inside the file and in a sidecar such as
`<name>M01.XML`. Write what it prints into the source in the record as `log`
(`gamma`, `gamut`, and `gamutAssumed` when the file names no gamut) and say the curve in one line.

**When `builtInLut` is true** (S-Log3, with S-Gamut3.Cine or S-Gamut3), write the conversion once
for the edit and make the proxy through it, so everything after sees normal colour:

```
python3 scripts/log_lut.py "work/<gamut>-709.cube" --gamut <gamut>
ffmpeg -i "<original>" -map 0:v:0 -map 0:a? -vf "scale=in_color_matrix=bt709:in_range=pc:out_range=pc,\
format=rgb48le,lut3d='work/<gamut>-709.cube':interp=tetrahedral,scale=-2:720:out_color_matrix=bt709:out_range=tv,\
format=yuv420p" -c:v libx264 -preset veryfast -crf 23 -c:a aac -b:a 128k -fps_mode passthrough \
  -map_metadata 0 -timecode <start> "proxy/<name>.mp4"
```

Decode with `in_range=pc` whatever the file's range flag says: the curve is defined on the
camera's own code values, and an expanded range lifts black and crushes grey. Write the LUT's path
into the source's `log.lut` and the proxy's `look: "rec709"` into `proxy/manifest.csv`: the conform
applies the same file to the original, so the master matches what was approved. A scene grade on
these proxies is then the look only, never a conversion.

**For any other log curve**, ask the user for the camera maker's LUT for that curve and gamut
(Panasonic, Canon, DJI and Fujifilm publish theirs); never guess a conversion. Once it is given,
make the proxies through it in the same way. Until then, make plain proxies, say that previews
will look flat until then, and put the open LUT in `openDecisions`.

Check one converted frame by eye before making the rest, beside the same frame of a plain proxy:
skin, a white shirt and a dark suit should read as they would to someone in the room.

## Gyro data, read at the proxies

Many cameras record their own motion beside the picture. Gyro stabilisation uses it and steadies a
handheld shot better than any picture analysis: a shake scan cannot tell the camera moving from
the subject moving, and gyro data records only the camera. While making the proxies, read each
original's streams and run `scripts/gyro.py` on the reading:

```
ffprobe -v error -show_streams -show_format -of json "<original>" > "proxy/<name>.probe.json"
python3 scripts/gyro.py "proxy/<name>.probe.json" --file "<original>"
```

It finds Sony's `rtmd` stream (a data stream, "Timed Metadata Media Handler", as an FX3 writes),
GoPro's `gpmd`, DJI's `djmd`, and Insta360's trailer at the end of the file. Write what it prints
into the source in the record: `gyro` (`true` or `false`) and, when true, `gyroKind`. A data
stream it does not know is not gyro data; mention it and go on. When `python3` is missing, read
the same tags and handlers in the probe JSON yourself; the Insta360 trailer then stays unknown.

A Sony `rtmd` stream does not prove motion samples: the camera writes it also in modes that record
none (an a7S III at 4K 120 fps), so the script prints `"maybe": true`. That is the probe's word
only, never written into the record, which keeps `gyro` and `gyroKind`. When Gyroflow is already
installed, confirm such a source before asking: `gyroflow "<original>" --export-metadata
"3:<abs project>/work/<name>.camera.json"`; a file with no gyroscope samples there is `gyro: false`,
and a source left with none asks nothing.

**When any source has gyro data**, ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) once, before the log, whether to stabilise its handheld
ranges with it; when every such source is still `"maybe": true`, say they may have gyro data.
Recommended first: "Steady the handheld shots with the camera's gyro data: they
come out steadier, with the frame cropped slightly (often about a tenth) so the moving edges never
show. Your originals are not changed." The other option: "Keep them as shot: no crop, the shake
stays." A yes goes into `approvals` with the scope `stabilise:gyro`; a no goes into `rejected`.
Either answer holds for the whole edit: never ask it again, also after a resume. In unattended
pace, the assumed answer is no: write it to `openDecisions` and keep the shots as shot. With gyro data,
the log's stabilising decision for each range reads the gyro data, not a shake scan.

**When the user said yes and no stabiliser is installed**, check first: `gyroflow --version` (on
macOS also the binary inside `Gyroflow.app/Contents/MacOS/`). Gyroflow is free and
open source, reads Sony, GoPro, DJI and Insta360 motion data, and runs from the command line. When
it is missing, ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) separately before installing it. Recommended first: "Install Gyroflow, the
free open-source stabiliser", saying how: `brew install gyroflow` on a Mac
with Homebrew, otherwise the download at https://gyroflow.xyz/download (the Microsoft Store on
Windows; the `.tar.gz` or the Flatpak on Linux). The other option: "Don't install: keep the shots
as shot." **Never install anything without the user's yes to this question.** A yes goes into
`approvals` with the scope `install:stabiliser` and is never asked twice; a yes to stabilising is
not a yes to installing. In unattended pace, the assumed answer is no: write it to
`openDecisions` and keep the shots as shot. When the install fails or needs an administrator
password, say so, keep the shots as shot and go on; never retry it unasked.

**Stabilised proxies.** Make one from each stabilised copy, as above, and upload it beside the
plain proxy: the conform checks it (below), and when the user wants to see the stabilisation in
review before the finish, render the copies then. Keep the plain proxy for the log, since the
analysis measures what the camera saw.

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
2. When the user chose gyro stabilisation, stabilise each source with gyro data first (below),
   keeping a stabilised range only when it is steadier, its choice in `stabilised.ranges`.
3. Cut each range from the file its check chose, the original or its stabilised copy, into
   `work/` at the master's frame rate. A source the log found turned (`upright` in its
   `sources` row) is turned first, before its crop: `transpose=1` for `rot90`, `transpose=2`
   for `rot270`, `hflip,vflip` for `rot180`. Count frames from each shot's scene start so the cuts
   never drift, into an intermediate that keeps 10 bits (ProRes 422 HQ). Stabilise first, then the LUT: a log source
   goes through the same LUT its proxy did (`log.lut`), decoded with `in_range=pc` as above, and
   the look the approved scene carried is baked in there or applied right after it. One shot that
   sits under or over the rest gets its own LUT with `log_lut.py --exposure`, never a lift of the
   whole edit. Look at one frame of each shot before joining them.
4. Join them in the plan's order over black, with the approved end card and captions (below), and
   the approved audio (below).
5. Check the master against the approved version, frame for frame: the same length, the same cut
   points, the same words when both are transcribed.

A master that differs is fixed in the conform, never delivered as it is. Deliver the master in the
format the brief or the reference names, at the originals' resolution; never add another size or
version nobody asked for.

### Captions at full resolution

The scene's captions are burned in at the conform, in the same font, colour, size and place,
scaled to the master. Write them as an `.ass` file with `scripts/captions_ass.py` (its usage says
the JSON it reads), and burn them with `subtitles='work/captions.ass':fontsdir='<brand font folder>'`,
so the brand's own font file is used. Two things first:

- **The font file is there.** libass quietly falls back to another font when the family is not in
  `fontsdir`, so check that the folder holds a file of the caption's family (its name, or
  `fc-scan` where present). When it does not, ask for the brand's font file with
  `picsart_drive_upload_ask`, or keep the captions `open`; never burn them in a substitute.
- **This ffmpeg has the filter** (`ffmpeg -hide_banner -filters | grep subtitles`); many builds
  lack it and `drawtext` both. `python3` missing is the same case: no `.ass` can be written.

When either is missing, ASK (with your host's own question tool, such as AskUserQuestion, so the options are buttons the user taps, the recommended one first; only where the host has none, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) separately how to finish. Recommended first: "Install
ffmpeg-full, the full ffmpeg with subtitle support", the same package and command as in ffmpeg
first, above (`brew install ffmpeg-full` on a Mac). The other options: "Deliver the free scene export with its captions instead", which exports
the approved scene with `picsart_scene_export` at the delivery resolution (from the proxies, so
below the originals' quality, and said so), and "Don't install: the captions stay off the master
for now". **Never install anything without the user's yes to this question.** A yes to installing
goes into `approvals` with the scope `install:ffmpeg` and is never asked twice: that scope
already approved means ffmpeg-full is installed, so use its binary rather than asking again. A yes to captions is not a yes to installing. In unattended pace, the assumed answer is the scene export: write it
to `openDecisions` and deliver that. When the install fails or needs an administrator password,
say so and never retry it unasked. On "stay off", the captions are `open`: finish the rest of the
master, say that its captions are not burned in, and stop before delivery. Never swap the brand
font for another one, and never deliver the master without its captions as if it were done.

### The voice and sound at full resolution

Take every voice from the original recording, never from a proxy or a scene export: cut its range,
remove rumble below about 80 Hz, and set its loudness in two passes (measure with
`loudnorm=print_format=json`, then apply the measured values with `linear=true`) to about -14 LUFS
with true peak under -1.5 dBTP. Place it at its scene start and pad it to the master's length with
silence, so it plays once and never repeats under the end card.

### Stabilising with Gyroflow

Gyroflow renders next to the source by default, so always give it an absolute output path in
`work/`; the original is read, never written, and a symlinked footage folder is resolved first so
nothing lands in it. One source at a time:

```
gyroflow "<original>" -p "{ 'codec': 'ProRes', 'codec_options': 'ProRes 422 HQ', 'audio_codec': 'Copy', 'output_path': '<abs project>/work/<name>.stab.mov' }"
gyroflow "<original>" --export-metadata "3:<abs project>/work/<name>.camera.json"
```

Type the braces once, as here (Gyroflow's help prints them doubled). ProRes takes every source as
it is; for an HEVC output instead (`'codec': 'H.265/HEVC'`), a 4:2:2 10-bit source needs
`'pixel_format': 'P010LE'`. Never run `--export-project`: it writes a `.gyroflow` file beside the
original, in the footage folder, whatever output path you give. When Gyroflow says the lens
is unknown, pass the lens profile's JSON file as another input after the original, with no flag
(`gyroflow "<original>" "<lens profile>.json" -p …`); never guess one. Settings saved as a preset go
in with `--preset <file>`. It exits 0 on
success, 1 when the render failed and 2 on a bad argument: on 1 or 2, keep that source as shot,
say so, and go on. When it renders but its camera data holds no gyroscope samples (a Sony source
that was only `"maybe"`), it had no motion to use: keep that source as shot.

Then check the copy with `ffprobe` against the original: the same fps, frame count and length.
Write into the source `stabilised`: its `file`, and its `crop`, the largest zoom Gyroflow applied
(1.12 keeps the middle 1/1.12 of the frame on each axis). Read the zoom from the camera data's
`zooming` fields; when they do not make it plain, measure it on one still pair: the distance
between two fixed details in the stabilised frame over the same distance in the original.

**Keep a stabilised range only when it is steadier.** Measure each used range on the stabilised
proxy as on the plain one, on the same fixed detail with texture, as the edit-pipeline skill's gate
rules say, never by a whole-frame scan: a moving subject reads as shake there. A range that is not
steadier (a gimbal shot already steady, say) stays as shot. Then run every framing and safe-zone
check on that source, the footage-reframing skill's included, on the stabilised proxy itself, not
only against the middle 1/crop of the frame: roll and lens correction move points, so a face or a
caption inside that rectangle on the plain proxy can still leave the frame. A range that fails is
kept as shot. Write each range's choice into the source's `stabilised.ranges`, never into its
`ranges` (which the log wrote, so a change there would redo every stage after it): `in`, `out`,
`use` (`stabilised` or `original`) and `shake`, the two measurements `[plain, stabilised]`. Cut
each range from the file it chose.

## Colour comparison, against the reference

When the record holds a reference and ffmpeg is on this computer, compare the draft's colour with
the reference's by measurement first. Read one frame a second of each, the draft's `exports/`
file and the reference clip:

```
ffmpeg -hide_banner -i "<file>" -vf "fps=1,format=yuv420p,signalstats,metadata=mode=print:file=-" -f null - 2>/dev/null \
  | grep -E "lavfi.signalstats.(YAVG|SATAVG)="
```

`format=yuv420p` puts both files on the same 8-bit scale first: `signalstats` reads in the input's
own bit depth, so a 10-bit draft would read about four times brighter than an 8-bit reference.
`YAVG` is then the brightness (0 to 255) and `SATAVG` the saturation. Average each over the file and
set the two side by side. The grade has drifted when either differs by more than about a tenth of
the reference's value: a draft clearly darker or flatter than the reference. Hue is judged by eye:
look at a frame of each side by side for a draft warmer, cooler or tinted another way than the
reference, since no single hue figure survives a frame whose colours sit either side of red. At the look stage the same reading, with `YLOW` (the black point) and `YHIGH` (the white point)
added to the `grep`, is taken on the board's stills and on the same frames in the chosen look;
edit-footage's `scripts/look_check.py` compares them. A
drift is fixed at the look, before the review, and said in one line when it is the user's own
choice; a figure that could not be read is `open`, never a pass. Where ffmpeg is not here, the use
case compares stills of both by eye instead.

## The final check, on this computer

Besides the checks the use case runs on every finish, run quality-review's `qc.py` on the master's
`ffprobe` and loudness reading (`ffmpeg -af loudnorm=print_format=json -f null -`): about -14 LUFS
with true peak under -1 dBTP.

## Deliver

Put the final files in `exports/` beside any earlier ones; an old file is removed only on a yes.
The cut list names each original, not its proxy.
