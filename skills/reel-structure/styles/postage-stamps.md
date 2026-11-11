### Postage stamps

| Field | Value |
|---|---|
| Group | Cards and frames |
| Looks like | your photos as perforated postage stamps slam onto an envelope, then a round postmark thumps over them |
| Vibe | stamps, postcard, travel mail, vintage, greetings from |
| Fit | slots 4; photos; place, any; trip, holiday, autumn, summer, any; nostalgic, playful, warm |
| Music | playful acoustic or swing, 95–115 BPM |
| Skin | the postmark reads the place or the skin's title with the year; the line under it is "greetings from <place or season>"; the envelope is a light tint of the skin's background |
| Preview | https://gcdn.picsart.com/picsart-mcp/6ae65468-b237-4503-9a5b-dff6fa72e611.mp4 |
| Proven | yes: agent build 2026-11-07, match |
| Seams | no cuts: all four stamps stay on one envelope |
| Motion | each stamp slams down with `look:stomp`, at a small angle; the postmark ring pops with `look:pop` |
| Text | postmark ring text in mono with `look:stomp`; "greetings from …" in serif italic with `textAnimation:fade_in_chars`; readable: on the stamp's flat paper border; band: the greeting strip and the postmark stay inside x 65–1015 and y 250–1440, and below y 864 their right edge stays at or left of x 940 (the right rail) |
| Look | `look:photo_frame` frame stamp_classic at scale 0.5; `look:stomp` length 0.4, scale 1.6, dissolve 0.3; `look:pop` on the postmark ring: length 0.3, overshoot 1.1 |
| Template | none |
| Ending | the four stamps and the postmark hold |
| Skills | motion-design-craft, caption-decorations, resting-frame-rules |

- ID: postage-stamps
- Format: four stamps and a postmark on an envelope
- Length: 6.6 s
- Cut rate: one stamp every 0.9 s, then a hold
- Caption style: postmark ring + "greetings from" line
- Bed: swing acoustic, ~104 BPM
- Layout: single
- Source: our style library

| Time (s) | Beat | What happens (picture) | Voice | On screen | Shot | Move | Caption | Sound |
|---|---|---|---|---|---|---|---|---|
| 0–0.9 | Hook | a photo as a perforated postage stamp slams onto a cream envelope | — | stamp 1 | stamp on paper | stamp slam | postmark ring + "greetings from" line | bed |
| 0.9–3.6 | Stamps | three more stamps slam down at small angles until four fill the envelope | — | stamps 2–4 | stamps on paper | stamp slam | postmark ring + "greetings from" line | bed |
| 3.6–6.6 | Postmark | a round postmark with the place and date thumps over them, the place name writes in below | — | postmark + greeting | stamps and postmark | stamp slam, hold | postmark ring + "greetings from" line | bed |
