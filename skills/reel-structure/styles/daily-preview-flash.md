### Day preview flash

| Field | Value |
|---|---|
| Group | Fast cuts |
| Looks like | a burst of the day's small moments flashes past while a pink script title types in, then the day's main moments get their own quick shots in order, morning to night |
| Vibe | day in my life, my day, daily vlog, everyday moments, routine, aesthetic, soft |
| Fit | slots 12–31; mixed; solo, food, place, any; everyday, any; aesthetic, upbeat, warm |
| Music | laid-back warm pop with a soft drop, 86–90 BPM; the drop lands where the flash burst ends |
| Skin | the script line is the skin's title word (default "A day"), pink #F6BFC9; the two serif lines stay "in my" and "life", white; nothing else on screen |
| Preview | none yet |
| Proven | no |
| Seams | hard cuts on every seam, no transition |
| Motion | Every item (photo or clip) is used exactly once; never repeat or re-crop an item. Sort all N items by time of day (morning first). The run takes R = the smaller of ceil(N/2) and 16 items, the strongest ones, kept in day order; the flash burst takes the other F = N − R items, in day order. Every photo layer is fitted to cover 1080×1920, centred. Flash burst from 0.000 s: each flash item is a still frame (a clip's first frame), 0.133 s each, no move. Run, from the end of the burst: each run item 0.433 s; a photo gets `look:ken_burns(motion=zoom_in, scale=1.05)`, a clip plays its liveliest 0.433 s as shot. The last run item is the ending (see Ending). Minimum, 12 items: F 6, R 6, burst 0.000–0.800 s, run 0.800–2.967 s, ending 2.967–3.833 s. Maximum, 31 items: F 15, R 16, burst 0.000–2.000 s, run 2.000–8.500 s, ending 8.500–9.367 s. Below 12 items the agent picks another style |
| Text | three text layers, each held from its layer start to the last frame, opacity 100 %, no exit. Readable at phone size: every line has `effect:drop_shadow(blur=14, color=#000000A6, offset=0,3)`, and the pink script line also has `effect:stroke(width=3, color=#8C3F55)`. Script line: the skin word, League Script (live font asset), 140 px, #F6BFC9, centred at x 470, y 900, layer start 0.133 s, `textAnimation:typewriter(duration=0.8)`. "in my": Playfair Display Regular (live font asset), 44 px, #FFFFFF, right-aligned with its right edge at x 760, centre y 970, layer start 0.133 s, `textAnimation:typewriter(duration=0.267)`. "life": Playfair Display Regular, 88 px, #FFFFFF, centred at x 620, y 1045, layer start 0.333 s, `textAnimation:typewriter(duration=0.6)`. Off faces: the title block spans y 820–1100; before building, check every item, and when any item has a face in y 760–1160, move the whole block down so its centre sits at y 1380 for the whole reel; if a face is there too, centre it at y 560 instead. The title never moves during the reel |
| Look | none |
| Template | none |
| Ending | the last run item, the day's final moment, held 0.867 s with `look:ken_burns(motion=zoom_in, scale=1.1)` (a clip plays as shot), title still on screen; the reel ends on that frame |
| Skills | photo-slideshow, motion-design-craft, visual-style, resting-frame-rules |

- ID: daily-preview-flash
- Format: day-in-order recap of photos and clips, a flash burst of small moments first, no item shown twice
- Length: 3.833 s at the minimum of 12 items (6 × 0.133 + 5 × 0.433 + 0.867); 9.367 s at the maximum of 31 items (15 × 0.133 + 15 × 0.433 + 0.867)
- Cut rate: ~190 cuts/min at 12 items (flashes every 0.133 s, then one shot every 0.433 s)
- Caption style: the three-line title only, centre, typed in over the first second and held, shadowed
- Bed: laid-back warm pop, ~88 BPM, soft drop at the end of the flash burst
- Layout: single
- Source: our style library

| Time (s) | Beat | What happens (picture) | Voice | On screen | Shot | Move | Caption | Sound |
|---|---|---|---|---|---|---|---|---|
| 0.000–0.800 | Hook | 6 small moments of the day flash past, 0.133 s each, hard cuts, while the title types in (31 items: 15 flashes, 0.000–2.000) | — | title "<skin word>" / "in my" / "life" | photos and clips, full frame | still | title, centre, typewriter from 0.133 s | bed, quiet build |
| 0.800–2.967 | Day run | 5 main moments in day order, 0.433 s each, each a new item (31 items: 15 moments, 2.000–8.500) | — | title held | photos and clips, full frame | slow zoom in | title held | bed, drop at 0.800 |
| 2.967–3.833 | Ending | the day's final moment, held, slow zoom in (31 items: 8.500–9.367) | — | title held | the final item, full frame | slow zoom in | title held | bed to the end |
