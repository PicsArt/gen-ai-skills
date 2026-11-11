### Three-word stack

| Field | Value |
|---|---|
| Group | Text-led |
| Looks like | three clips stacked on screen, each with one spaced-out word, then full-screen clips with a small mantra line |
| Vibe | discipline, consistency, gym motivation, routine, focus, minimal |
| Fit | slots 4–9; clips; solo; sport, everyday, New Year, any; epic, minimal, moody |
| Music | slow-building cinematic, 115–125 BPM |
| Skin | the three words and the mantra are the user's, else the agent writes them (e.g. "CONSISTENCY / DISCIPLINE / FOCUS", "1 % better every day") |
| Preview | none yet |
| Proven | yes: agent build 2026-11-07, close |
| Seams | hard cuts |
| Motion | the opener: three clips in three full-width bands (1080 × 640), each playing as shot; then each clip full frame for two beats |
| Text | one word per band, white serif caps, 54 px, letter-spaced wide, centred on x 540 at y 320, 960 and 1370 (the bottom band's word sits in its upper part, inside the safe band), `textAnimation:fade_in_chars` one band after another; later, the mantra small (40 px caps) at y 760 on every full-screen clip |
| Look | on every clip effect:adjust brightness −0.15, saturation −0.4 with `look:analog_film_finish` grain 0.25, dust 0, vignette 0.5 |
| Template | `scene://cell-cycle-grid` for the opener, three stacked cells, cycle mode with no swaps (each cell keeps its clip) |
| Ending | the last clip holds with the mantra |
| Skills | scene-template-remix, scene-building-basics, visual-style |

- ID: three-word-stack
- Format: three stacked words, then full-screen clips
- Length: 14 s
- Cut rate: ~20 cuts/min (one clip every ~3 s)
- Caption style: three spaced words, then a small mantra
- Bed: slow-building cinematic, ~120 BPM
- Layout: single
- Source: our style library

| Time (s) | Beat | What happens (picture) | Voice | On screen | Shot | Move | Caption | Sound |
|---|---|---|---|---|---|---|---|---|
| 0–3 | Hook | three clips stacked; a spaced-out word fades in on each, one after another | — | three words | three bands | as shot | one word per band | bed |
| 3–12 | Mantra | each clip full frame, the mantra small in the upper third | — | mantra | clips, full frame | as shot | mantra, upper third | bed |
| 12–14 | Payoff | the last clip holds | — | mantra | clip, full frame | as shot | mantra | bed |
