# Transit map

A diagrammatic map of three coloured lines: each line draws itself, stations pop where it passes, interchanges
become dark hubs, trains run back and forth along the lines at constant speed, and the title types in.

## Palette

Paper `#f6f3ec`, ink `#222222`, lines red `#e2453c`, blue `#2f6fd6`, green `#2fa65a`. **The hero colours are the
line colours, one per line, never reused**: a colour means a line; a hub is the only dark `#222222` marker.

## The medium

- Lines are **polylines with 45- and 90-degree corners only**, 18 px stroke, round joins, in a shape layer each
  with a keyed `trim`. The same polyline is used by its stations and its train.
- **Stations** are small white circles (22 px) with a 5 px stroke in the line's colour; an **interchange** is a
  larger circle (30 px) with a dark stroke.
- **Trains** are small white rounded rectangles (34 by 16) with a 4 px stroke in the line's colour.
- Title: a condensed display face in ink, top centre. Place nothing off the grid of 40 px.

## Motion habits

- **Draw each line** with `trim` end 0 to 1 over 1.4 s with an ease in and out, lines starting about 0.8 s apart.
  A station **pops** (scale from 0 with an overshoot `[0.3, 1.45, 0.5, 1]`) at the moment the line reaches it:
  compute that time as the line's start plus 1.4 s times its distance along the line over its length.
- **Trains** start after their line is drawn and run its vertices with keys at a constant speed (260 px/s): time
  between keys is the segment length over speed. At the end they return along the same keys. Cut keys that fall
  beyond the clip's end.
- Cued layers use `timeMode: "layer"`.

## Type

A condensed display face for the title and station names, in ink; names sit beside stations on the side that
keeps clear of the lines.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. Every line uses only 45- or 90-degree angles.
2. A station pops when its line arrives, not before.
3. Interchanges are visibly different from stations.
4. Trains move at one speed on every line.
5. Line colours never appear anywhere else.

## Build with the tools

Compute station times and train keys in a script; one layer per line, per station and per train. Check the
timing with `picsart_scene_contact_sheet`, and run `picsart_scene_query_layout` to confirm stations sit on their lines.

## Do / don't

- **Do** give the trains a small hold at hubs.
- **Don't** curve a line, use gradients or add shadows.

## Originality guard

Design your own network and names. It must not copy a real city's transit map, its line colours and numbering,
or a famous network diagram's layout. The 45-degree lines, station circles and drawing-on are the style.

## Proven on

The city-lines-transit film (three lines drawing on, stations popping as they are reached, hubs, trains running,
a typed title).
