### Typed message

| Field | Value |
|---|---|
| Group | Text-led |
| Looks like | a message bar over a clip; a short question types itself letter by letter and the send button pops, then photos answer it |
| Vibe | text message, chat, typing, question, remember this, cute |
| Fit | slots 3–6; mixed; couple, friends, family, any; love, anniversary, memories, birthday, any; cute, romantic, warm |
| Music | soft acoustic or bedroom pop, 80–100 BPM |
| Skin | the send button is the skin's accent colour; the bar is white |
| Preview | https://gcdn.picsart.com/picsart-mcp/7c08a81a-2020-49bd-800a-069810761237.mp4 |
| Proven | yes: agent build 2026-11-07, close |
| Seams | `transition:crossfade` between the answer photos, 0.3 s; a hard cut from the clip to the first photo |
| Motion | the clip plays as shot under the bar; the bar fades in at 0.3 s and stays until the cut; the answer photos play as shot |
| Text | the message ("remember this day?") in the default face, 54 px, centred in the white bar, which is its plate; the bar is centred left to right at y 1180; the bar is `look:chat_input(barWidth=940, barHeight=130, typeDelay=0.3, typeDuration=1.8, upload=0, mic=0, send=1, accentColor=#E07A2F)`, so the words type in and the send button pops |
| Look | none |
| Template | none |
| Ending | the best photo holds for 1.8 s |
| Skills | scene-building-basics, app-ui-animation, motion-design-craft, resting-frame-rules |

- ID: typed-message
- Format: a typed question answered by photos
- Length: 8 s
- Cut rate: ~23 cuts/min (one clip, then a photo every 1.1 s)
- Caption style: one message in a white chat bar
- Bed: soft acoustic, ~90 BPM
- Layout: single
- Source: our style library

| Time (s) | Beat | What happens (picture) | Voice | On screen | Shot | Move | Caption | Sound |
|---|---|---|---|---|---|---|---|---|
| 0–4 | Hook | a clip with a white message bar; the question types itself letter by letter and the send button pops | — | "remember this day?" | clip | as shot | message, in the bar | bed, soft key taps |
| 4–8 | Answer | photos answer the message, dissolving in one after another | — | — | photos | as shot | — | bed |
