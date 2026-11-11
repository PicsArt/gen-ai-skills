# Takes: check, judge, accept

## Find the real cuts

Probe every take with `picsart_media_probe` first: its real duration, not the one asked for,
bounds its last shot. Find the cuts every take **actually made**, not the planned times. Look around each planned
cut on `picsart_scene_contact_sheet` frames (`cut − 1/fps`, `cut`, `cut + 1/fps`, and a second
either side when the cut is not there), and note each where the picture changes. Record the
actual times on the run. **A take whose cut count differs from the plan has failed**, before
anything else is judged.

These times are a check and a record, never edit points. The take goes into the cut whole, as one
clip exactly as generated (film-cutting): it is not split at its cuts, and nothing trims it unless
the user does.

## Judge it before the user does

Look at 3–4 frames inside each candidate shot (around a quarter, half and three quarters), not only
its first (picsart-video-rules, Asset URLs). Then check:

- identity, wardrobe and place match the approved views;
- no bad hands or teeth, extra fingers, drifting or duplicated objects, pseudo-text;
- every planned cut is there, near its time, as a hard cut: not a morph, a dissolve or a whip;
- the camera move matches the card;
- movements and eyelines carry through the internal cuts and across the run edges;
- every shot keeps the START FRAME's visual style; flag any drift in the existing review;
- light and colour hold with the neighbouring takes;
- every line's last word finishes before its shot ends, with its beat of silence.

Acting, lines, lip-sync and voice are judged by the user in review, and by you listening where the
host lets you. Say that the words were not checked against the script by a tool.

Keep what you observed for the review. Never report that a take passed.

## Review

The user reviews takes inside the cut, never one by one: once the takes the cut needs have landed
(the use case says when), every take in story order, each one clip, as generated, and what you
observed in each said there. A retake replaces its candidate in the timeline; two versions of one
shot never play end to end, and the earlier one stays in the record, restorable. Trims and splits
the user makes there are theirs: record them, and never open a separate review for the pieces.

## Keep a frame

A frame the user marks, or the best frame of a shot whose face is right and whose motion is wrong,
is exported at native size and kept as that cut's `FRAME REFERENCE`. Rewrite only the failed
movement.

## Accept

On acceptance: the run's take and its actual cut times go into the record, its final prompt and
token stay beside it, the take goes into the selects as one clip, and every shot in the run is `final`.
