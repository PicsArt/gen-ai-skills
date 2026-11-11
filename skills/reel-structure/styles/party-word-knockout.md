### Pink word knockout

| Field | Value |
|---|---|
| Group | Text-led |
| Looks like | one giant word at a time on the beat, flipping between a hot-pink washed frame with a black word and your plain shot with the word in pink |
| Vibe | big words, word by word, hot pink, night out, club, bold text |
| Fit | slots 1–6; mixed; friends, group, solo, any; night out, party, concert, birthday; bold, energetic, stylish |
| Music | punchy dark electro-pop with a hard kick, 130–140 BPM (build at 136 BPM: the word grid is the half beat, 0.2206 s, each swap rounded to the nearest frame from the start) |
| Skin | colours only: the wash colour #EF2C82 and the word pink #FF1088 become the skin's accent; the words stay this style's own line |
| Preview | none yet |
| Proven | yes: agent build 2026-11-07, close |
| Seams | hard cuts, no transition; media changes only on word swaps, at the times in the slot table below the sheet |
| Motion | clips play as shot at 100 % speed, muted, fit cover; each photo grows from scale 100 % to 106 % over its whole slot, linear, centred; every word slides in from 80 px right of its spot (x 620 → 540) over 0.067 s, linear, with motion blur on |
| Text | 19 words, one at a time, Anton Regular (the live font search asset), capitals, letter spacing 0, centred on x 540. Pink beats: the word #111111 on the pink wash, a flat bright ground that keeps it readable. Dark beats: the word #FF1088 with a soft shadow, `effect:drop_shadow(blur=24, color=#000000B3, offset=[0, 8])`. The three held dark words also carry `textAnimation:shake(intensity=0.25)`. Off faces: the word sits in a face-free band of the slot, never on a face (rule under the sheet). In the band: every word stays inside y 250–1440 and x 65–1015, so its size is capped at 950 px wide and its centre sits between y 700 and y 1100 |
| Look | `effect:fill(color=#EF2C82, opacity=0.45)` on the media track, on during the hook and the pink beats only: its opacity steps 0.45 ↔ 0 at each word swap (step easing). Checked on a rendered frame (party selfie, look_check.jpg): a clean pink wash with faces natural. Difference blending was dropped because it solarised faces |
| Template | none |
| Ending | the last word holds 3.1 s; the shots fade to black over 14.400–15.000 s (opacity 1 → 0, ease_in) and the word fades over 14.500–15.000 s (opacity 1 → 0, ease_in), so the word goes last |
| Skills | scene-building-basics, motion-design-craft, visual-style |

- ID: party-word-knockout
- Format: word-by-word pink wash over a few shots
- Length: 15 s
- Cut rate: ~76 word swaps/min (19 words, most on the half beat); media cuts at most 5
- Caption style: one giant word at a time, in a face-free band, alternating black word on a pink-washed frame and pink word on the plain shot
- Bed: dark electro-pop, ~136 BPM
- Layout: single
- Source: our style library

| Time (s) | Beat | What happens (picture) | Voice | On screen | Shot | Move | Caption | Sound |
|---|---|---|---|---|---|---|---|---|
| 0–0.867 | Hook | slot 1 under the pink wash (fill 0.45), no word | — | — | slot 1 | as shot | — | bed, from the downbeat |
| 0.867–3.967 | Phrase one | JUST (dark, 0.867–1.333), ONE (pink, 1.333–1.533), MORE (dark, 1.533–1.767), DRINK (pink, held 1.767–3.967) | — | JUST / ONE / MORE / DRINK | slot 1 | as shot; each word slides in 0.067 s | word, face-free band | bed |
| 3.967–7.5 | Phrase two | WE (dark, 3.967–4.200), SAID (pink, 4.200–4.400), HOME (dark, 4.400–4.633), BY (pink, 4.633–4.867), TEN (dark, held 4.867–7.500, shake 0.25) | — | WE / SAID / HOME / BY / TEN | slot 2 | photo 100 → 106 % linear | word, face-free band | bed |
| 7.5–10.6 | Phrase three | IT'S (pink, 7.500–7.933), NOW (dark, 7.933–8.367), FOUR (pink, 8.367–8.833), A.M. (dark, held 8.833–10.600, shake 0.25) | — | IT'S / NOW / FOUR / A.M. | slot 3 | as shot | word, face-free band | bed |
| 10.6–11.9 | Run | BEST (pink, 10.600–10.800), NIGHT (pink, 10.800–11.033), EVER (pink, 11.033–11.467), DO (dark, 11.467–11.700); over 11.600–11.700 the wash ramps 0 → 0.45 (ease_in) as a pink flash into IT (pink, 11.700–11.900) | — | BEST / NIGHT / EVER / DO / IT | slot 4 | photo 100 → 106 % linear | word, face-free band | bed |
| 11.9–15 | Payoff | AGAIN (dark, held 11.900–15.000, shake 0.25); shots fade to black 14.400–15.000, the word fades 14.500–15.000 | — | AGAIN | slot 4 | photo keeps growing | word, face-free band | bed, last bar rings out |

**Build notes (one way each).**

- Canvas 1080 × 1920, 30 fps, background #000000. One media track holds the slots with hard cuts and carries the fill effect; every word is its own text layer above it, start and duration exactly its beat above.
- Word sizes (font size in px): 2–3 letters (WE, BY, DO, IT, ONE, TEN, NOW) = 620; 4 letters (JUST, MORE, SAID, HOME, IT'S, FOUR, A.M., BEST, EVER) = 500; 5 letters (DRINK, NIGHT, AGAIN) = 400. Read every word's box with the layout tool: none may be wider than 1000 px; shrink that word in 5 % steps until it fits.
- **Off faces.** Before placing words, take one contact-sheet frame at the start, middle and end of each slot (free) and mark every face box. The word's centre y for that slot is 360 (upper band) when all faces sit below y 760, else 1500 (lower band) when all faces sit above y 1160. When faces fill both halves, use the band with the larger face-free height and shrink the word until its box clears every face box by 40 px. The word keeps that y for the whole slot. Check with the text-placement check after the render: no word box on a face in any frame.
- Slide-in on every word: position x 620 → 540 at its band's y, over the word's first 0.067 s, linear.

**Slots by item count.** Every item is shown once and never repeated. The first slot gets a clip when there is one, the last slot gets the item with the most faces, and the rest keep the user's order.

| Items | Media cuts (s) | Slots |
|---|---|---|
| 1 (minimum) | none | the one item runs 0–15 s, under all 19 words |
| 2 | 7.500 | 0–7.500, 7.500–15.000 |
| 3 | 3.967, 10.600 | 0–3.967, 3.967–10.600, 10.600–15.000 |
| 4 | 3.967, 7.500, 10.600 | one slot per phrase |
| 5 | 3.967, 7.500, 8.833, 10.600 | phrase three split on A.M. |
| 6 (maximum) | 1.767, 3.967, 7.500, 8.833, 10.600 | phrase one split on DRINK too |

More than 6 items: use the 6 with the most faces and movement. A clip shorter than its slot holds on its last frame (no loop, no repeat). A single photo grows 100 → 106 % across the whole 15 s.

A phone clip stored rotated (probe its rotation): set the rotation so it stands upright before fitting with cover.
