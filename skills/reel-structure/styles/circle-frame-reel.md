### Circle frame and ring text

| Field | Value |
|---|---|
| Group | Cards and frames |
| Looks like | a black page with your photo in a circle, a ring of small text turning round it and a script line under it |
| Vibe | circle frame, ring text, the end, script, vintage, dreamy |
| Fit | slots 3–6; photos; couple, solo, friends, any; year-end, anniversary, love, memories, New Year, any; dreamy, romantic, nostalgic |
| Music | soft dreamy pop or lounge, 80–95 BPM |
| Skin | the ring repeats the skin's title with the year; the script line closes with the skin's ending words ("the end", "with love"); outline in a soft tint of the accent |
| Preview | https://gcdn.picsart.com/picsart-mcp/032da137-37f9-4803-be7f-5be8360e8bea.mp4 |
| Proven | yes: agent build 2026-11-07, close |
| Seams | hard cuts on the beat inside the circle |
| Motion | the circle window is 680×680, centred at x 540, y 800, and opens with `look:shape_window`; each photo a slow push inside it (100→104 %); the ring text turns slowly round |
| Text | ring text: the skin's title and year in small spaced capitals, Montserrat 30 px, letter spacing 6, #F4A6B8, repeated with • (Montserrat has no ✦) to close the ring, on a closed circular `textPath` of radius 400 round the circle's centre, `orient: true`, its offset gliding 0→700 px over the reel, fading in over 0.5 s at 0.3 s; the ring always sits at least 40 px outside the circle's outline, so no letter lies over the photo; a script line, 110 px, #F4A6B8, centred at x 540, y 1360, with `textAnimation:fade_in_chars`, changing to the closing words for the payoff; band: the ring ink spans x 120–960 and y 380–1220 (letters face outward, r 400–422) and the line stays inside y 250–1430; readable: on the flat page around the circle, never on the photo |
| Look | `look:shape_window` shape circle, outline 3, colour #F4A6B8, offset 14, length 0.5 |
| Template | none |
| Ending | the script line changes to the closing words and holds |
| Skills | motion-design-craft, caption-decorations, visual-style |

- ID: circle-frame-reel
- Format: circle window with turning ring text
- Length: 8.6 s
- Cut rate: ~30 cuts/min (one photo every 2 s)
- Caption style: ring text + a script line
- Bed: dreamy lounge, ~86 BPM
- Layout: single
- Source: our style library

| Time (s) | Beat | What happens (picture) | Voice | On screen | Shot | Move | Caption | Sound |
|---|---|---|---|---|---|---|---|---|
| 0–1.4 | Hook | a black page: a photo opens in a circle, a ring of small text turning round it, a script title under it | — | ring + script line | circle window | iris open, ring turns | ring text + a script line | bed |
| 1.4–7.4 | Photos | the photo inside the circle changes on the beat while the ring keeps turning | — | — | circle window | cut, slow push | — | bed |
| 7.4–8.6 | Payoff | the script line changes to the closing words | — | closing script line | circle window | hold | ring text + a script line | bed |
