### Light leak

| Field | Value |
|---|---|
| Group | Film and retro |
| Looks like | warm light glowing over each photo, photos melting or bursting through light into each other, the title low |
| Vibe | light leak, dreamy, golden, film glow, soft |
| Fit | slots 4–10; mixed; couple, family, friends, solo, any; trip, autumn, summer, any; warm, dreamy |
| Music | dreamy indie pop, 85–100 BPM |
| Skin | the title is the skin's, cream, low on screen |
| Preview | https://gcdn.picsart.com/picsart-mcp/247c9e21-90c3-4eaf-8276-04e0b67427f3.mp4 |
| Proven | yes: agent build 2026-11-07, match |
| Seams | `transition:crossfade(duration=0.5)` and `transition:light_leak_burst(duration=0.5)` in turn |
| Motion | each slot a slow drift, alternating direction: `look:ken_burns(motion=pan_left, scale=1.08)`, then `look:ken_burns(motion=pan_right, scale=1.08)` |
| Text | the title, low third with its bottom at y 1440 at most, cream, fading in and out over the first slot; a soft dark shadow under the cream letters keeps them readable over the glow, and the title sits clear of faces |
| Look | `look:light_leak(intensity=0.8)` on every slot |
| Template | none |
| Ending | the last photo glows out |
| Skills | motion-design-craft, scene-template-remix, visual-style |

- ID: light-leak
- Format: warm light-leak recap
- Length: 9 s
- Cut rate: ~40 cuts/min (one slot every 1.5 s)
- Caption style: the title only, low third
- Bed: dreamy indie pop, ~92 BPM
- Layout: single
- Source: our style library

| Time (s) | Beat | What happens (picture) | Voice | On screen | Shot | Move | Caption | Sound |
|---|---|---|---|---|---|---|---|---|
| 0–1.5 | Hook | a warm glowing photo, light leaking over it, the title low | — | title "<skin title>" | photo | slow drift | title, low third | bed |
| 1.5–9 | Glow | photos dissolve or burst through light into each other | — | — | photos | drift | — | bed |
