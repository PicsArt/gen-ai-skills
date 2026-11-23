# VHS tape

A late-80s home-video look: a purple sunset with a striped sun, a title split into red, green and blue plates
that shake and tear in bursts, a PLAY mark, a date stamp, scanlines and a rolling tracking band.

## Palette

Sky `#1b0f33` to `#3d1450`, sun `#ffd25e` to `#ff3e8a`, UI white `#f2f2f2`. The title plates are pure `#ff0000`,
`#00ff00` and `#0000ff`. **The hero colour is the sun's pink-to-gold gradient, reserved for the sun** so the
only warm thing in the frame is the sunset.

## The medium

- A **gradient** background from deep violet to plum, and a **sun**: a circle with a vertical gradient fill
  (gold at the top, hot pink at the bottom) whose lower part is cut by five dark stripes (a thin rectangle with a
  `repeater` of 5, 22 px apart, in the sky colour).
- **RGB split:** the title is three text layers in pure red, green and blue in the `screen` blend, offset 5 px
  left and right of the centre, so where they agree the title is white and at the edges the colours fringe.
- **Tape UI:** "PLAY" with a triangle at the top left (a bold grotesque), a date stamp bottom left, a counter or
  speed mark bottom right, all in off-white.
- **The tape pass:** one adjustment layer with `gaussian_blur` (about 1.2) and `noise` (about 14) over everything
  below it. Over it, **scanlines** (a 2 px black bar with a `repeater`, 4 px pitch, about 28 % opacity) and a
  **tracking band**, a wide white strip at about 7 % opacity blurred by 6 px.
- **The counter ticks:** text cannot be keyed, so write one text layer per second, each with `start` n and
  `duration` 1, reading one second later than the last (`SP 0:00:14`, `SP 0:00:15`, …).

## Motion habits

- **Tracking jitter:** the `wiggle` preset on each title plate's position (a different `seed` per plate) at a small
  amount, and two short **tears** hand-keyed on top: each plate's position jumps 20-30 px sideways for two or
  three frames at two chosen moments, then returns. Put the plates in a nested `composition` with `fps` 15 (12 under a 24 fps root).
- The **PLAY** mark blinks on a slow `random_hold` step in its opacity; the tracking band rolls down the frame
  as a linear position loop; the noise level on the tape pass rises during the tears.
- Cued layers use `timeMode: "layer"`.

## Glitch look

The same tape world, broken digitally: use it when the user's words ask for "glitch", "datamosh" or a corrupted
signal. It is a variant of this style, not a style of its own: keep the palette, the plates and the tape pass.

- **Cut between shots with `glitch_cut`**, `style` `vhs_tear`, 0.3 to 0.5 s, `intensity` about 0.9, with a `tint`
  that is not in either shot's palette (a cold cyan against the violet sunset). Each shot is a clip on a `track`;
  the transition sits on the seam with `between`.
- **Bursts sit on one adjustment layer over the whole track:** `glitch` (`intensity` about 0.7) for the displacement and `channel_shift`
  (`horizontal` about 20) for the split. Drive both by one expression that is on only inside two or three
  short windows (4 to 6 frames each) and 0 elsewhere, so a burst snaps in and out with no fade.
- **Space the breaks:** a burst every 3 to 4 s at most, never within a second of the cut. The plates' own tears
  stay, so a burst reads as the signal failing on top of a worn tape.
- The second shot changes one thing the eye catches at once (the sky's hue, a new title), so the cut reads as a
  jump to another tape, not a repeat.

## Type

A condensed display face for the title (the three plates), a bold grotesque for the tape UI, upper case.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. The title is three plates, one per primary, in `screen`.
2. The tape pass (blur and noise) sits over the whole picture, with scanlines above it.
3. There are two bursts of tearing, short and sharp.
4. A tape mark and a date stamp are present, and the counter ticks once a second.
5. The sun is the only gradient-lit warm shape.

## Build with the tools

Build the three plates as three text layers with `screen` blend, apply `wiggle` to their positions, and add the
tape adjustment layer, the scanline repeater layer and the band. Check a tear frame with `picsart_scene_contact_sheet`.

## Do / don't

- **Do** keep tears short; constant shake becomes an effect, not a tape.
- **Don't** colour the plates by anything but pure red, green and blue; don't freeze the counter.

## Originality guard

Choose your own title, date and sunset. It must not copy a real video label's logo, a known synthwave album's
cover, or a famous film's title card. The split plates, the tape noise and the tracking band are the style.

## Proven on

The vhs-midnight-drive film (a striped sunset, an RGB-split title tearing in two bursts, a PLAY mark, a date
stamp, scanlines and a rolling band).

The glitch look was proven on vhs-glitch-sides (two tape shots joined by a `vhs_tear` glitch cut, with two short
glitch and channel-split bursts on an adjustment layer over the track).
