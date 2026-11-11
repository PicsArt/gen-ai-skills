### Peek and slide

| Field | Value |
|---|---|
| Group | Strips and swipes |
| Looks like | full-screen photos where a slice of the next one peeks in at the right edge, then pushes the last one off |
| Vibe | swipe, slide, peek, carousel feel, smooth |
| Fit | slots 4–8; photos; any; trip, everyday, autumn, summer, any; upbeat, friendly, stylish |
| Music | smooth upbeat pop, 100–115 BPM |
| Skin | no words; the slice outline is white |
| Preview | https://gcdn.picsart.com/picsart-mcp/dd6c9942-fa84-48f0-a3bc-51a4425e55ec.mp4 |
| Proven | yes: agent build 2026-11-07, match |
| Seams | `transition:slide` on every seam, 0.3 s, to the left |
| Motion | each photo a slow push; 0.767 s before the seam a rounded slice of the next photo slides in at the right edge with `look:slide` |
| Text | none |
| Look | `look:slide` on each slice: length 0.3, direction left, distance 1.2, dissolve 0; `look:rounded_corners` radius 22, white stroke 6 |
| Template | none |
| Ending | the last photo holds full frame |
| Skills | motion-design-craft, resting-frame-rules, photo-slideshow |

- ID: peek-slide
- Format: full-screen photos with a peeking next slide
- Length: 8.4 s
- Cut rate: ~43 cuts/min (one photo every 1.4 s)
- Caption style: none
- Bed: smooth pop, ~108 BPM
- Layout: single
- Source: our style library

| Time (s) | Beat | What happens (picture) | Voice | On screen | Shot | Move | Caption | Sound |
|---|---|---|---|---|---|---|---|---|
| 0–1.4 | Hook | a photo full frame; near the end of its beat a slice of the next photo peeks in at the right edge | — | — | photo, full frame | slow push, peek | — | bed |
| 1.4–8.4 | Slides | the next photo pushes the last one off to the left, and the next slice peeks in, on every beat | — | — | photos, full frame | push, peek | — | bed |
