### Season title rush

| Field | Value |
|---|---|
| Group | Transitions and speed |
| Looks like | "welcome to my" writes itself in word by word over a slowly panning first photo, a big serif "AUTUMN" lands under it, then the photos flash past fast, slow down to one a second with warm light-leak flares every few cuts, and the last photo fades to black |
| Vibe | aesthetic, cinematic, season recap, photo dump, city walk, autumn vibes |
| Fit | slots 10–22; mixed; place, solo, any; autumn, memories, trip, everyday; cinematic, aesthetic, nostalgic, warm |
| Music | mellow cinematic indie with a soft steady beat, 110–120 BPM; the cuts keep the sheet's frame grid (flash cuts 8 frames, slow cuts 30 frames) and are not moved to the bed |
| Skin | the big word is the skin's season word in capitals (default "AUTUMN"); both text lines white with a soft dark shadow; nothing else on screen |
| Preview | none yet |
| Proven | no |
| Seams | hard cuts everywhere except `transition:light_leak_burst(duration=0.4, origin=left, tint=#ff7a2f, intensity=1)`, centred on the seam, on every 4th slow-run seam and on the seam into the last item |
| Motion | slot 1 (title): `look:ken_burns(motion=pan_left, scale=1.15)` over its whole 3.867 s; flash-run slots: held still, no move; slow-run slots: `look:ken_burns(motion=zoom_in, scale=1.06)` over each slot; last slot: `look:ken_burns(motion=zoom_in, scale=1.06)`, and a full-frame black shape layer above it fades opacity 0 → 1 over its final 0.467 s, linear, fully black on the last frame; clips play as shot with no ken_burns |
| Text | two lines, white #FFFFFF, each layer with `effect:drop_shadow(color=#000000, blur=30, offset=[0,4])`, a soft dark shadow so the words read on any photo at phone size. Line 1 "welcome to my" in font `just-another-hand-regular-8b981e4f2e80`, 130 px, lowercase: lay the whole line out centred on x 540, measure where each word sits, then make three word layers at those spots (centre y 830); "welcome" pops on at 0.067 s, "to" at 0.600 s, "my" at 1.200 s, each with `textAnimation:fade_in_chars(duration=0.033, stagger=0)`. Line 2 the season word in Playfair Display SC Bold (font asset https://pastatic.picsart.com/03200152782985793586.ttf), 180 px, capitals, letter spacing 4 px, centre x 540, centre y 990, shrunk until it is at most 900 px wide, popping on at 1.700 s with `textAnimation:fade_in_chars(duration=0.033, stagger=0)`. The title block (y 760–1080) stays off faces: if a face is inside it in any frame of slot 1's pan, move both lines up together to centre y 430 and 590. All four layers end at 3.867 s with the first photo, no exit animation |
| Look | `look:analog_film_finish(grain=0.15, grainSize=2, paper=0, dust=0, vignette=0.3, tint=#ff8a3d, tintAmount=0.15)` on every photo and clip layer |
| Template | none |
| Ending | the last item enters through the light-leak flare, holds 1.667 s with a slow push and fades to black over its final 0.467 s |
| Skills | photo-slideshow, motion-design-craft, visual-style |

- ID: autumn-season-rush
- Format: season photo recap: handwritten-plus-serif title, fast flash run, slower one-a-second run with light-leak flares, fade to black
- Length: 19.667 s at 22 items; 10.600 s at 10 items
- Cut rate: one 3.867 s title slot, then a flash run of 4–8 cuts every 0.267 s (8 frames at 30 fps), then one cut every 1.000 s, last slot 1.667 s
- Caption style: two-line title over the first slot only: lowercase handwritten words above a bold serif season word, centre, soft dark shadow
- Bed: mellow cinematic indie, ~116 BPM
- Layout: single
- Source: our style library

Slots for N items (10–22 photos or clips; canvas 1080×1920, 30 fps; every photo fills the frame, cover fit, centre crop). Every item is shown exactly once; no item repeats. Below 10 items pick another style.
- Slot 1 (title) is the widest place shot whose title block (y 760–1080) is the quietest, flattest area with no face; the last slot is the stillest wide shot with no person in it.
- Flash run F = min(8, floor((N − 2) / 2)) items, slow run S = N − 2 − F items, then the last slot.
- Slow-run seams are counted between slow-run slots, including the seam into the last slot; the cut from the flash run into the first slow slot is not one. Flares go on slow-run seams 4, 8, 12 and always on the seam into the last slot.
- Minimum, 10 items: slot 1 = item 1 (0.000–3.867); flash run = items 2–5 (cuts at 3.867, 4.133, 4.400, 4.667); slow run = items 6–9 (item 6 at 4.933, item 7 at 5.933, item 8 at 6.933, item 9 at 7.933); last slot = item 10 at 8.933, entered by the flare 8.733–9.133, black layer fading in from 10.133 to the last frame at 10.567; 10.600 s.
- Maximum, 22 items: slot 1 = item 1; flash run = items 2–9; slow run = items 10–21; last slot = item 22; the beat table below.

| Time (s) | Beat | What happens (picture) | Voice | On screen | Shot | Move | Caption | Sound |
|---|---|---|---|---|---|---|---|---|
| 0.000–3.867 | Hook | item 1 slowly pans left; "welcome" pops on at 0.067, "to" at 0.600, "my" at 1.200, the big "AUTUMN" under them at 1.700; all held to the cut | — | "welcome to my" + "AUTUMN" | item 1, full frame | pan left, scale 1.15 | title, centre (y 830 and y 990), soft dark shadow | bed starts |
| 3.867–6.000 | Flash run | hard cuts every 0.267 s through items 2–9 (cuts at 3.867, 4.133, 4.400, 4.667, 4.933, 5.200, 5.467, 5.733) | — | — | photos, full frame | held still | — | bed |
| 6.000–18.000 | Slow run | items 10–21, one a second (cuts at 6.000, 7.000 … 17.000), hard cuts except a warm light-leak flare from the left over the seams at 10.000 (9.800–10.200) and 14.000 (13.800–14.200) | — | — | photos, full frame | slow push in, scale 1.06 per slot | — | bed |
| 18.000–19.667 | Ending | a flare (17.800–18.200) brings in item 22; it pushes in slowly while a black layer fades in from 19.167 to the last frame at 19.633 | — | — | item 22, full frame | slow push in; black layer opacity 0 → 1 over 0.467 s, linear | — | bed fades out with the picture |
