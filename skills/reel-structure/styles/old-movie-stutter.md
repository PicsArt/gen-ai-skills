### Old movie stutter

| Field | Value |
|---|---|
| Group | Film and retro |
| Looks like | a washed-out black-and-white home movie in a 4:3 window on black, the picture stepping at 5 frames a second under grain, dust and a soft breathing glow |
| Vibe | old movie, black and white, vintage film, home movie, nostalgic, moody, film look |
| Fit | slots 3–8; mixed; pet, solo, couple, friends, any; everyday, memories, summer, trip, any; nostalgic, moody, cinematic, aesthetic, calm |
| Music | moody nostalgic indie with soft drums, 116–124 BPM played half-time (a hit on every other beat) |
| Skin | none: no title, no colour; the skin's bed mood only |
| Preview | none yet |
| Proven | yes: agent build 2026-11-08, user-approved |
| Seams | hard cuts |
| Motion | the picture steps at 5 frames a second inside the "film" layer (see the sheet); the "film" layer itself gets a faint gate weave `look:shake(amount=0.004, speed=5)` at the full 30 fps; a photo slot gets `look:ken_burns(motion=zoom_in, scale=1.08)` inside the 5 fps track; a clip shorter than its slot plays slowed (speed = trim length ÷ slot length, never below 0.5) |
| Text | none: no words on screen in any frame |
| Look | on the "film" layer (the 30 fps outer layer, never on the slots, so grain, dust and glow move every frame and never freeze into 5 fps steps), in this order: `look:vintage_bw(bloom=0.55, bloomBlur=40, jitter=6, grain=0.35, grainSize=3)`, then `look:analog_film_finish(grain=0.5, grainSize=2, paper=0, dust=0.6, vignette=0.35, tintAmount=0)` |
| Template | none |
| Ending | hard cut from the last slot to plain black, held 0.500 s, the music cut with it |
| Skills | scene-building-basics, photo-slideshow, motion-design-craft, visual-style |

- ID: old-movie-stutter
- Format: black-and-white home movie in a 4:3 window, picture stepped at 5 fps, a short opening then alternating long and short holds
- Length: 15.5 s for 4 items (14.1 s for 3, up to 28.3 s for 8, black included)
- Cut rate: ~12 cuts/min (holds of 1.6, 7.0, 1.4 and 5.0 s)
- Caption style: none
- Bed: moody nostalgic indie, ~120 BPM half-time
- Layout: single
- Source: our style library

**Build (one way).**
- Scene 1080×1920, 30 fps, background #000000.
- One layer "film": a scene_ref whose inline scene is 1080×810 at fps 5 (every picture holds 6 output frames, 0.200 s), placed at (540, 960) so it covers y 555–1365. Inside it, one track of the slots, hard cuts, every slot muted. Each item appears in exactly one slot; no item is ever shown twice.
- On the "film" layer, besides the two looks and the shake above, these effects in this order: `effect:black_white`, `effect:levels(outputBlack=0.2, outputWhite=0.95)` (matte lifted blacks), and `effect:adjust(brightness=0→-0.03→0.02→-0.04→0.03)` with keys every 0.200 s on step easing, the 5-value run repeated to the layer's end (the exposure flicker on each held picture, on the same 0.200 s grid as the picture steps).
- No zoom, slide, flash or blur between slots. The only moves are the gate weave, the photo push and the clips' own motion.

**Placing a portrait in the 4:3 window (pets' heads never cut).** A 3:4 or 9:16 portrait shows only a 4:3 band of itself. Every slot's media is fit cover into bounds 1080×810 with align center, and declares the source's width and height plus a crop [0, y, W, W×0.75] (W = source width). Pick y from the item's middle frame (a free ffmpeg still), using the highest point the head reaches across the slot's trim: y = head top − 0.12 × band height, clamped to 0 … (source height − band height). The head then sits at least 12 % below the window's top edge. When the whole animal is taller than the band, keep the head and let the body run off the bottom.

**Slots for 4 items** (each used once; the clips take the long holds, the longest first; a photo takes the short hold):

- Slot 1, 0.000–1.600 s (Hook): the liveliest 1.600 s of a clip (else a photo).
- Slot 2, 1.600–8.600 s (long hold): the longest clip, its first 4.200 s at speed 0.6.
- Slot 3, 8.600–10.000 s (short hold): a photo, `look:ken_burns(motion=zoom_in, scale=1.08)`.
- Slot 4, 10.000–15.000 s (long hold): the last clip, its first 5.000 s at speed 1, ending on the subject looking into the lens when it does.
- 15.000–15.500 s: black (the "film" layer ends at 15.000 s).

**Slot map for other counts** (one item per slot, never repeated):
- 3 items (the minimum): Hook 1.600 s, long hold 7.000 s, long hold 5.000 s, black 0.500 s; 14.100 s in all.
- 4 items: as above.
- 5–8 items: after the 4-item shape, each extra item adds a short hold of 1.400 s and the next a long hold of 5.000 s, inserted before the last long hold so the film always ends on a long hold; 8 items = 1.6 + 7.0 + 1.4 + 5.0 + 1.4 + 5.0 + 1.4 + 5.0 s = 27.800 s, then 0.500 s of black.
- Clips take the long holds first, the longest clip in the first long hold; photos take the Hook and the short holds. A photo in a long hold gets `look:ken_burns(motion=zoom_in, scale=1.15)`.

| Time (s) | Beat | What happens (picture) | Voice | On screen | Shot | Move | Caption | Sound |
|---|---|---|---|---|---|---|---|---|
| 0.000–1.600 | Hook | the pet looking around, washed black and white, stepping at 5 fps in a 4:3 window on black | — | — | clip | gate weave, stepped | — | bed starts on the first frame |
| 1.600–8.600 | Long hold | the longest clip slowed down, flickering exposure, dust and scratches | — | — | clip | slowed, gate weave | — | bed, first half-time hit near the cut |
| 8.600–10.000 | Short hold | the photo, pushing in slowly | — | — | photo | slow push, gate weave | — | bed |
| 10.000–15.000 | Payoff | the last clip, ending on a look into the lens | — | — | clip | gate weave | — | bed |
| 15.000–15.500 | End | hard cut to black | — | — | black | none | — | bed cut hard |
