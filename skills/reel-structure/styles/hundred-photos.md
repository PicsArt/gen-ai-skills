### Hundred photo dump

| Field | Value |
|---|---|
| Group | Fast cuts |
| Looks like | a bold title card ("2026 in 100 photos"), then up to 100 of your photos flash past full screen with a small counter in the corner |
| Vibe | 100 photos, year in photos, photo dump, recap, fast, the whole year |
| Fit | slots 30–100; mixed; any; year-end, New Year, autumn, trip, memories, any; energetic, nostalgic, fun |
| Music | fast, bright pop or dance, 120–130 BPM |
| Skin | the title is "<year> in <n> photos" (year-end), "<month> in <n> photos" (a month), "<place> in <n> photos" (trip); white on the skin's background |
| Preview | none yet |
| Proven | yes: agent build 2026-11-08, user-approved |
| Seams | hard cuts, two photos per beat |
| Motion | after the title, each photo full frame for 0.233 s (two per beat at 128 BPM), no move; clips show their best 0.233 s; the last photo holds one bar |
| Text | the title, bold sans, centre: the year builds digit by digit with `textAnimation:typewriter`, the "in <n> photos" line under it with `textAnimation:fade_in_chars`; a counter ("23/100", 48 px semi-bold, white with a dark shadow) ticks with every photo, its box right-aligned at x 1000 and top at y 270 (top right inside the band); it must read at 360 px wide |
| Look | none |
| Template | none |
| Ending | the counter reaches n on the last photo, which holds one bar |
| Skills | scene-building-basics, footage-analysis, visual-style |

- ID: hundred-photos
- Format: a title card, then a counted rapid photo dump
- Length: 26 s
- Cut rate: ~260 cuts/min after the title (two photos per beat)
- Caption style: a title card, then a running counter, top right
- Bed: fast bright pop, ~128 BPM
- Layout: single
- Source: our style library

| Time (s) | Beat | What happens (picture) | Voice | On screen | Shot | Move | Caption | Sound |
|---|---|---|---|---|---|---|---|---|
| 0–2.8 | Hook | a dark card; the year types on, "in 100 photos" under it | — | title "<year> in <n> photos" | title card | type on | title, centre | bed |
| 2.8–24.6 | Dump | photos flash past two per beat, a counter ticking in the corner | — | counter | photos, full frame | none | counter, top right | bed |
| 24.6–26 | Payoff | the last photo holds, the counter at n | — | counter "n/n" | photo, full frame | hold | counter | bed |
