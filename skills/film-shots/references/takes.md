# Takes: split, judge, accept

## Split at the real cuts

Probe every take with `picsart_media_probe_media` first: its real duration, not the one asked for,
bounds its last shot. Split every take at the cuts **it actually made**, not the planned times. Look around each planned
cut on `picsart_media_contact_sheet` frames (`cut − 1/fps`, `cut`, `cut + 1/fps`, and a second
either side when the cut is not there), and set each split where the picture changes. Record the
actual times on the run. **A take whose cut count differs from the plan has failed**, before
anything else is judged.

Each shot becomes a clip bounded by its real cuts, a window over the run's own file. No trim is
applied before the user has seen it.

## Judge it before the user does

Look at 3–4 frames inside each candidate shot (around a quarter, half and three quarters), not only
its first (video-core, Asset URLs). Then check:

- identity, wardrobe and place match the approved views;
- no bad hands or teeth, extra fingers, drifting or duplicated objects, pseudo-text;
- every planned cut is there, near its time, as a hard cut: not a morph, a dissolve or a whip;
- the camera move matches the card;
- movements and eyelines carry through the internal cuts and across the run edges;
- light and colour hold with the neighbouring takes;
- every line's last word finishes before its shot ends, with its beat of silence.

Acting, lines, lip-sync and voice are judged by the user in review, and by you listening where the
host lets you. Say that the words were not checked against the script by a tool.

Say what you observed, then open the review. Never report that a take passed.

## Review

The review holds the **whole film so far** in story order: every accepted take and the new one in
its place, each shot its own clip. A retake replaces its candidate in the timeline; two versions of
one shot never play end to end, and the earlier one stays in the record, restorable. Trims and
splits the user makes there are theirs: record them, and never open a separate review for the
pieces.

## Keep a frame

A frame the user marks, or the best frame of a shot whose face is right and whose motion is wrong,
is exported at native size and kept as that cut's `FRAME REFERENCE`. Rewrite only the failed
movement.

## Accept

On acceptance: the run's take and its actual cut times go into the record, its final prompt and
token stay beside it, its clips go into the selects, and every shot in the run is `final`.
