### Neon title sparkle

| Field | Value |
|---|---|
| Group | Glow and colour |
| Looks like | a dark sparkling screen, a glowing neon title buzzes on, then your photos appear in soft white frames on the dark ground |
| Vibe | neon, it's time, Christmas countdown, glowing title, sparkle, festive |
| Fit | slots 6–14; photos; any; Christmas, New Year, birthday, party, any; cosy, wow, upbeat |
| Music | sparkly pop with bells, 120–136 BPM |
| Skin | the title is the skin's short call ("it's time", "<year>", "birthday") in the skin's accent as neon |
| Preview | none yet |
| Proven | yes: agent build 2026-11-07, close |
| Seams | `flash_cut` white (intensity 0.6) on every seam, 0.133 s |
| Motion | after the title, each photo sits at 80 % scale centred on the dark ground in a soft white rounded frame, landing with `look:zoom` (scale 1.08, length 0.3), one per beat |
| Text | the neon title, centre, script 150 px, `textAnimation:neon_strike` over 1.2 s, then held glowing until the first photo; readable: the neon glow is its own outline; set on the darkest quiet part of the frame |
| Look | the title `look:glow_pulse` (period 1.2, intensity 0.7, blur 30) with `effect:glow` radius 30; each photo `look:rounded_corners` cornerRadius 40, strokeWidth 10, strokeColor #FFFFFF; the ground is the skin's background with `look:shimmer` intensity 0.3 on a dark sparkle layer |
| Template | none |
| Ending | the last photo holds, then the neon title buzzes back on over it |
| Skills | scene-building-basics, motion-design-craft, visual-style |

- ID: neon-sparkle
- Format: a neon title, then framed photos on the beat
- Length: 10 s
- Cut rate: ~65 cuts/min after the title (one photo per beat)
- Caption style: a neon title at the start and end
- Bed: sparkly pop with bells, ~128 BPM
- Layout: single
- Source: our style library

| Time (s) | Beat | What happens (picture) | Voice | On screen | Shot | Move | Caption | Sound |
|---|---|---|---|---|---|---|---|---|
| 0–2 | Hook | a dark sparkling ground; the neon title buzzes on | — | title "<skin call>" | dark ground | neon in | neon title, centre | bed |
| 2–8.5 | Photos | each photo lands in a soft white frame on the beat, a small flash between | — | — | framed photos | zoom settle | — | bed |
| 8.5–10 | Payoff | the last photo holds and the neon title returns | — | title | framed photo | hold | neon title | bed |
