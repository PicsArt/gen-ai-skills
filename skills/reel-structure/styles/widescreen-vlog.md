### Cinematic widescreen vlog

| Field | Value |
|---|---|
| Group | Film and retro |
| Looks like | your clips in a wide cinema band with a rich film grade, a big serif title on the first shot and a few spaced words later |
| Vibe | cinematic vlog, widescreen, movie, travel film, film look |
| Fit | slots 5–14; clips; solo, friends, couple, place; trip, everyday, winter, summer, any; cinematic, epic, stylish |
| Music | cinematic indie or chill house, 110–125 BPM |
| Skin | the first-shot title is the skin's or the user's ("LIVE YOUR LIFE", "<place>"), in the skin's accent; the later words are white |
| Preview | none yet |
| Proven | yes: agent build 2026-11-08, user-approved |
| Seams | hard cuts on the beat; on the first seam the outgoing clip pushes in (scale 1 → 1.15 over its last 0.3 s) and hard-cuts to the next, never a `zoom_through` (it draws a see-through box inside the band) |
| Motion | every clip cover-fit into a 1080 × 452 band (2.39:1) centred on black, playing as shot, 1–2 s each |
| Text | the title in a big serif, 120 px, centre of the band, at most 760 px wide (break it over two lines rather than reach the right-hand buttons), `textAnimation:word_lift`, over the first clip; one spaced word (60 px) on every third clip after it, `textAnimation:fade_in_chars` |
| Look | `look:analog_film_finish` grain 0.2, dust 0, vignette 0.3 with a warm-highlight, teal-shadow grade (realistic-color-grade) |
| Template | `scene://crop` per clip, width 1080, height 452, centred on a black backdrop |
| Ending | the last clip fades to black inside the band |
| Skills | scene-building-basics, realistic-color-grade, visual-style |

- ID: widescreen-vlog
- Format: a wide cinema band with a serif title
- Length: 14 s
- Cut rate: ~35 cuts/min (a clip every ~1.7 s)
- Caption style: a big serif title on the first shot, then a spaced word every third clip
- Bed: cinematic indie, ~120 BPM
- Layout: single
- Source: our style library

| Time (s) | Beat | What happens (picture) | Voice | On screen | Shot | Move | Caption | Sound |
|---|---|---|---|---|---|---|---|---|
| 0–2.4 | Hook | the first clip in a wide band, the big serif title lifting in | — | title "<title>" | clip, 2.39 band | as shot | title, band centre | bed |
| 2.4–12.5 | Film | clips cut on the beat in the band, a spaced word on every third | — | spaced words | clips, 2.39 band | as shot | one word, band centre | bed |
| 12.5–14 | Payoff | the last clip fades to black | — | — | clip, 2.39 band | fade out | — | bed |
