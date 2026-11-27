# Telestrator

Sports analysis marker work over a pitch: arrows and circles draw on in a bright marker, a pulse ring marks the
key player, a dashed run line follows a path and everything fades away when the play resets.

## Palette

Pitch greens `#2f7d3a` and `#2a7035` in stripes, white lines `#f4f4f4`, players in two team colours (`#2a6fdb` and
`#f4f4f4` with a dark outline). **The hero colour is the marker yellow `#ffe14d`, reserved for the analyst's
drawing**: arrows, circles, the ring and the run line.

## The medium

- A **top-down pitch**: striped grass, a halfway line, a centre circle, a box. Players are 28 px discs with a number.
- **Marker strokes:** 8 px yellow strokes, round caps, with a faint dark under-stroke (3 px wider, 35 % opacity) so
  they read on any green.
- **Pulse ring:** a yellow circle stroke around the player, beating outward.
- **Run line:** a dashed yellow path (length 18, gap 12) with an arrowhead at the end.

## Motion habits

- **Draw on:** every marker stroke uses `trim` end 0 to 1 over 0.5 s, arrowheads popping in as the line finishes.
- **Pulse:** the ring's scale loops 1 to 1.35 while its opacity falls to 0, using a looping track
  (`ctx:loopOut("cycle")`) at a 0.9 s period.
- **Players move** along their paths on position keys with an ease-in-out; the run line draws just ahead of the
  mover.
- **Reset:** the drawing fades out over 0.3 s together, and players glide back to their start.
- Cued layers use `timeMode: "layer"`.

## Type

A condensed display face in capitals for a player name label attached to the ring; white on a dark pill.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. All analyst drawing is the one marker yellow.
2. Strokes read on both stripes of grass.
3. The ring stays centred on its player while it moves.
4. Arrows end with a clear head.
5. Drawing and players never cover the ball's path.

## Build with the tools

Build the pitch and players as shape layers; give the ring an `attach` constraint to its player so it follows
without separate keys. Check overlap with `picsart_scene_query_layout`.

## Do / don't

- **Do** keep strokes thick enough for a phone screen.
- **Don't** use a real club's kit, crest or a league's graphics package.
- **Template rules, this style's choices** ([recipe-template](recipe-template.md#rules-that-hold-for-every-recipe)):
  - Stop time (optional): freeze the play on the key beat by ending the players' keys at that time in a nested composition while the marker strokes draw on and the ring pulses at the root rate; the ring is keyed to the frozen spot then, not attached.
  - True data: 11 discs a side, one disc = one player, numbers each used once; any distance or speed label is computed from the same position keys that move the discs; a small `schematic` tag stays in frame because the play is invented (ours).

## Originality guard

Use invented teams, numbers and plays. They must not copy a broadcaster's on-screen graphics, a league's
overlay package or a real match's tactic board. The yellow marker on a striped pitch is the style.

## Proven on

The tactics-telestrator film (a pitch with players, marker arrows and circles drawing on, a pulse ring on the key
player, a dashed run line, a fade reset).
