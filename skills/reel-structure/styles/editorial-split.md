### Editorial spread

| Field | Value |
|---|---|
| Group | Text-led |
| Looks like | each photo as a page in a print magazine: photo on top, a huge number and a serif title under it, a thin rule |
| Vibe | editorial, print, magazine page, clean, minimal, numbered |
| Fit | slots 3–6; photos; any; trip, everyday, autumn, memories, any; minimal, stylish, aesthetic |
| Music | minimal chic electronic, 95–110 BPM |
| Skin | the page is a light tint of the skin's background; numbers and titles in the skin's background colour; the caption is the skin's title |
| Preview | https://gcdn.picsart.com/picsart-mcp/9b16333a-703c-4bb6-a646-b5e66c383dc5.mp4 |
| Proven | yes: agent build 2026-11-07, close |
| Seams | hard cuts between spreads; each new photo wipes up into the top half |
| Motion | the photo wipes up with `look:wipe` and then pushes slowly |
| Text | a huge condensed number with `textAnimation:slide_up_lines`, a serif italic title and a small caption with `textAnimation:fade_in_chars`; readable: on the split's flat colour half, never on the photo half |
| Look | `look:wipe` on each photo: length 0.6, direction up |
| Template | none |
| Ending | the last spread holds |
| Skills | motion-design-craft, visual-style, resting-frame-rules |

- ID: editorial-split
- Format: magazine spreads
- Length: 8 s
- Cut rate: ~30 cuts/min (one spread every 2 s)
- Caption style: number, title and caption under each photo
- Bed: minimal electronic, ~100 BPM
- Layout: single
- Source: our style library

| Time (s) | Beat | What happens (picture) | Voice | On screen | Shot | Move | Caption | Sound |
|---|---|---|---|---|---|---|---|---|
| 0–2 | Hook | a cream page: a photo in the top, a huge number and a serif title under it, a thin rule and a small caption | — | 01 + title | photo on a page | wipe in | number, title and caption under each photo | bed |
| 2–8 | Spreads | every two seconds a new spread: the photo wipes up, the number and title change | — | 02… + titles | photos on a page | wipe in, slow push | number, title and caption under each photo | bed |
