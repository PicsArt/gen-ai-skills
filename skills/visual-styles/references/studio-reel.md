# Studio reel

A showreel built from type alone. Each shot is one huge word or line; the ground colour is different in every shot,
so a cut is something you can see; and a small fixed frame (corner marks, a title, a counter, a progress bar) sits
over all of it. A motion variant of kinetic type, closer to a studio's own reel than to a lyric video.

## Palette

Petrol `#10222a` (the dark ground), tangerine `#ff8a3d` (the loud ground), mint-white `#e4efe9` (the light ground),
sage grey `#7f9a96` (small print), sun yellow `#ffd23f` (a full stop, nothing else). **The hero colour is one
magenta `#e0107a`, spent once, on the closing slam**, with a small magenta node lit on the last beat before it so
the reel arrives there on purpose. One ground per shot; type is petrol on the light and loud grounds and mint-white on
the dark ones.

## The medium

- **Type carries every shot.** A condensed headline face (Anton) for lines, a wide heavy face (Rubik Mono One) for the one
  slam word, a mono face (JetBrains Mono 600) for the frame. No fourth face.
- **Flat grounds only.** A full-frame colour per shot; no gradient, no photo behind the type.
- **Each shot proves its words with a moving device.** The type does not stand alone: a number rolls up, an echo steps down the frame, a node
  lights, slats climb. The headline says it, the mechanism shows it.
- **The fixed frame.** Four corner marks, a small mono title top left, a "0N / 04" counter top right, a progress bar
  of four segments along the bottom. It never moves with a shot. Its ink follows the ground and changes only once
  the next ground fully covers the frame. Keep the shot's content out of the outer band the frame uses.
- **The echo stack.** The slam word is repeated as outline-only copies (a text stroke, no fill), **three lines at
  most**, one stepping in per beat.
- **The number shot.** A figure that rolls up like an odometer (a text expression), settles with a small pop, and
  carries one mono label.

## Motion habits

- **Pick a grid first** (120 BPM: a beat is 0.5 s, a bar 2 s). Cuts land on beats, a new shot opens on the downbeat of a bar,
  hits land on beats.
- **Every transition grows out of what is on screen:** slats climbing from the bottom, the solid word scaling until
  it fills the frame and becomes the next ground, an iris opening from a lit node, a slam. No dissolve, no stock wipe.
- **Change the kind of transition from one cut to the next.** The same kind three cuts running reads as a template.
  Slams and accents have a budget per film: one slam word, one yellow stop per line, one magenta shot.
- **Letters arrive as units:** `slide_up_lines` with `unit: "character"`, 0.4 to 0.45 s over a short distance; the
  full stop pops (scale 1.6 and back) one beat after the line.
- **Show/hide keys sit one frame apart.** A layer that blinks on and off with opacity `step` keys needs the two keys
  at least `1/fps` apart. Keys 0.001 s apart land on the same frame and blend every window together.
- **A back-eased scale can dip below zero** and a circle or stroke then draws nothing or throws; keep a floor under
  any radius or scale an overshoot curve drives.
- **Sound, if the reel has any, belongs to events:** a swell into each new shot, a quiet tone cue inside it, a hit on
  the slam. No noise whooshes, and a good share of the cuts carry no sound at all.

## Type

Headline 150 to 170 px, left aligned on a 90 px margin; the slam word about 170 px, centred; the number about 260
px, centred; frame type 14 to 22 px with wide letter spacing. Nothing else.

## Frame checklist (on top of [FRAME.md](FRAME.md))

1. One word or line leads each shot, and a moving device backs it up.
2. The ground differs from the previous shot's.
3. Magenta appears once.
4. The fixed frame is on every shot and changes ink only after the new ground covers it; no content in its band.
5. No more than three lines in the echo stack.
6. No transition kind used for three cuts running.

## Build with the tools

Lay out the shots as full-frame rectangles switched with opacity `step` keys (one frame apart), put the type on
top, and build each transition from its own layers (slats, a scaled word, an iris) on the grid. Build the fixed frame
once per ink colour and show the right one per shot. Preview the first bar, each transition and the magenta slam, then
a contact sheet.

## Do / don't

- **Do** change the ground every shot and keep the magenta for the end.
- **Do** put every cut on a beat and every shot change on a downbeat.
- **Don't** repeat a transition kind three times running, or stack a fourth echo line.
- **Don't** put a photo or a gradient behind the type, or let the frame move with a shot.

## Originality guard

Write your own words, numbers and colours. Do not copy a studio's reel, its headlines or its brand colours. Big
condensed type, a changing ground, a counter and a progress bar are generic conventions.

## Proven on

A four-shot, 8 s reel at 1280×720: a headline over petrol with a yellow full stop, a one-word slam over tangerine
with outlined echoes that zooms through into a mint-white number shot, and a closing magenta slam.
