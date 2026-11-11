### Welcome title recap

| Field | Value |
|---|---|
| Group | Fast cuts |
| Looks like | small pictures flicking on black and growing, then a big yellow place name over the best clip that changes font on every half-beat, a letterbox closing onto it, three cards in a row whose middle one grows and fills the frame, and an ending on one long shot that fades out |
| Vibe | travel recap, trip montage, welcome to, destination, fast cuts, holiday vlog, adventure |
| Fit | slots 7–28; mixed; place, any; trip, holiday, summer, memories; upbeat, energetic, cinematic, epic, wow |
| Music | bright upbeat summer pop with a steady kick and a clear half-beat hat, 96–104 BPM (build at 100 BPM: beat 0.600 s, half-beat 0.300 s, both on the frame grid) |
| Skin | the title words follow the order in Text; title colour stays lemon yellow #EAF800 with a black stroke, "WELCOME TO" white; background is black #000000; nothing else from the skin |
| Preview | none yet |
| Proven | yes: agent build 2026-11-07, close |
| Seams | hard cuts on every seam, all on the 0.300 s half-beat grid; no transition presets |
| Motion | clips play as shot, muted, cover-cropped to 1080x1920; every photo gets `look:ken_burns(motion=zoom_in, scale=1.08)` over its own length (a photo in the title hold or the end hold gets `look:ken_burns(motion=zoom_in, scale=1.15)`); opener cards on black step up in size per cut (hard steps, no tween); letterbox bars close with keyframes; the centre card of the row grows with keyframes; nothing else moves |
| Text | Words, in this order of sources: (1) the place the user names ("my trip to Lisbon" gives LISBON); (2) else a place written readably in the media (a sign, a station name) or a landmark the agent can name for certain; (3) else no place: "MY TRIP". Never a year or filler ("TRIP 2026", "SUMMER VIBES"). Layout: "WELCOME TO", white #FFFFFF, font century-schoolbook-regular, 44 px, letter spacing 6 px, centred at y 768, with `effect:drop_shadow(blur=10, color=#000000b3, offset=[0,3])`; then the title, upper case, lemon yellow #EAF800, auto-fit to 860 px wide (cap 130 px), centred at y 922, black #000000 stroke 6 px (fill over stroke) plus `effect:drop_shadow(blur=14, color=#000000b3, offset=[0,4])`, so it reads on bright sky and water at phone size. Both come in hard (no textAnimation). The title's font swaps on every cut under it in this fixed order: luckiest-guy-regular, bebas-neue-thin, bangers, permanent-marker-regular, meddon-regular, unica-one-regular, then repeat (one text layer per font, same box, colour, stroke and shadow, hard cut). Off faces: if a face in the title-hold item lies under y 700–1020, move both lines up together to y 422 and 576, or down to y 1268 and 1422 when the face is in the upper half, and close the letterbox onto the title's new line |
| Look | none |
| Template | none |
| Ending | the last item holds 2.400 s full frame, then opacity 1 → 0 over its last 0.800 s, linear, to black; the bed fades out over the same 0.800 s |
| Skills | reel-structure, scene-building-basics, motion-design-craft, resting-frame-rules, visual-style |

- ID: travel-welcome-recap
- Format: trip recap of clips and photos with a font-swapping place title, 1080x1920, 30 fps
- Length: 8.700 s at 7 items (the minimum); 13.200 s at 28 items (the maximum)
- Cut rate: ~62 cuts/min at 7 items, ~150 cuts/min at 28 items (0.300 s half-beat cuts plus the 3.600 s title hold and the 2.400 s end hold)
- Caption style: the title only, centre, font swapping on each cut; no other words
- Bed: bright upbeat summer pop, 100 BPM
- Layout: single
- Source: our style library

Slots. Every item is shown exactly once; a clip that carries on from a card into full frame is one showing (its trim continues, it never restarts). Below 7 items pick another style. Slot names:
- O1–O5 opener cards on black, 0.300 s each, 9:16, centred at (540, 960), no border, no shadow, hard on and off; widths step evenly from 594 px (0.55) to 940 px (0.87) across however many there are (2 cards: 594, 940; 5 cards: 594, 680, 767, 853, 940).
- T title hold: the longest vertical clip (else the longest clip, else the best wide photo), full frame, 3.600 s.
- F1–F6 flash run: full-frame hard cuts of 0.300 s that take over the last part of T, while the bars close; the title font swaps on each.
- R1–R2 two cards on black after the letterbox, 0.300 s each, 9:16, centred, widths 691 px then 864 px.
- B card-row background (a wide photo), full frame; L, C, Rt the three row cards, 324x576 px each, centres (178, 960), (540, 960), (902, 960), touching, hard on 0.300 s apart; C is the second-best clip (else a photo) and grows.
- M1–M9 montage, full-frame hard cuts of 0.300 s.
- E end hold, 2.400 s with the fade.

Fill order as the count grows: 7 items = O1, O2, T, B, L, C, Rt, and C carries on full frame as the end hold. 8–10 add O3–O5. 11–12 add R1–R2. 13 adds a separate E (C then shows full frame for 0.300 s before E). 14–22 add M1–M9. 23–28 add F1–F6 (k flash items take the last k × 0.300 s of T, inside the bar close). Fewer items always means a shorter montage and flash run, never a repeat.

Minimum build, 7 items: C1 = the longest vertical clip, C2 = the next clip, P1–P5 the photos (P2 and P5 the opener cards, P4 the widest photo as the card-row background B). The title is the place from the library's place-title rule, else "MY TRIP".
- Canvas 1080x1920, background colour layer #000000 for the whole length, under everything.
- 0.000–0.300 O1 = P2, card 594 px wide; 0.300–0.600 O2 = P5, card 940 px wide.
- 0.600–4.200 T = C1 from its 0.000 s, full frame. "WELCOME TO" on at 0.700; the title on at 1.800 in luckiest-guy-regular, its font swapping at 2.100, 2.400, 2.700, 3.000, 3.300, 3.600, 3.900.
- 2.400–4.200 letterbox: two black #000000 shape layers above media and text, full width. Top bar anchored at the top edge, height 0 → 922 px; bottom bar anchored at the bottom edge, height 0 → 998 px; both 1.800 s, ease_in_out, so the picture closes onto the title line and clips the title. 4.200–4.500 black only, all text off.
- 4.500–6.300 card row: B = P4 full frame. L = P1 on at 4.800; C = C2 from its 0.000 s on at 5.100; Rt = P3 on at 5.400. At 5.700 C (drawn above L and Rt) grows: width 324 → 562 px, height 576 → 1000 px, centre fixed, 0.200 s, ease_out.
- 6.300–8.700 end: B, L and Rt off; C2 carries on full frame from its 1.200 s (no restart) and fades opacity 1 → 0 from 7.900 to 8.700, linear.

Maximum build, 28 items: O1–O5 0.000–1.500; T 1.500–3.300 ("WELCOME TO" on at 1.600, title on at 2.700, font swap every 0.300 s); F1–F6 3.300–5.100 under the closing bars (bars 3.300–5.100); black 5.100–5.400; R1 5.400–5.700, R2 5.700–6.000; card row 6.000–7.800 (L on 6.300, C on 6.600, Rt on 6.900, C grows 7.200–7.400); C full frame 7.800–8.100; M1–M9 8.100–10.800; E 10.800–13.200, fading from 12.400. In between, each added item adds its slot's 0.300 s and shifts what follows.

| Time (s) | Beat | What happens (picture) | Voice | On screen | Shot | Move | Caption | Sound |
|---|---|---|---|---|---|---|---|---|
| 0.000–0.600 | Hook | two pictures flick by as centred cards on black, the second much bigger | — | — | photos, cards on black | cards step up in size per cut | — | bed starts on the downbeat |
| 0.600–2.400 | Welcome | the vertical clip holds full frame; "WELCOME TO" appears small, then the title lands big in yellow with a black stroke and swaps font every half-beat | — | "WELCOME TO", then the title | clip, full frame | as shot | title, centre | bed |
| 2.400–4.500 | Close | black bars close from top and bottom onto the title line while the font keeps swapping, then black | — | the title | clip, full frame | bars close, ease_in_out | title, centre | bed |
| 4.500–6.300 | Card row | a photo full frame; three cards pop on left, centre, right a half-beat apart; the centre card (a clip) grows to half the frame | — | — | photo background, photo and clip cards | centre card grows, ease_out | — | bed |
| 6.300–8.700 | Payoff | the centre clip fills the frame, holds and fades to black | — | — | clip, full frame | as shot, fade out | — | bed fades out |
