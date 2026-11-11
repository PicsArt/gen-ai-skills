### Freeze and sticker

| Field | Value |
|---|---|
| Group | Cut-outs and stickers |
| Looks like | each clip freezes on the beat and the person lifts off it as a white-edged sticker while the picture behind dims |
| Vibe | freeze frame, sticker, pop out, cut out, main character |
| Fit | slots 3–8; mixed; solo, friends, couple, group, pet; any, party, trip, everyday, birthday; fun, playful, bold |
| Music | punchy pop with a hit on the downbeat, 110–130 BPM |
| Skin | the sticker edge takes the skin's accent colour; no words unless the user asks |
| Preview | none yet |
| Proven | yes: agent build 2026-11-08, user-approved |
| Seams | hard cuts between slots |
| Motion | a clip plays as shot for 1.2 s, then freezes for 0.9 s (`speed: 0` from that frame, with a duration); the frozen frame is exported as a still and its subject cut out (one picsart_image_remove_bg call per photo cut out (a per-image cost the build quotes before it spends)); the cut-out sits exactly over the frozen person, its layer set to 108 %, and enters with `look:zoom` (scale 0.93, length 0.3) so it grows off the frozen person; the frozen picture under it takes effect:gaussian_blur (blur 18) and effect:adjust brightness −0.45 over the same 0.3 s; a photo slot is its own frozen frame |
| Text | none |
| Look | the cut-out has `effect:stroke` width 12 in the skin's accent and `effect:drop_shadow` offset [0, 14], blur 24, #00000059; SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says) for picsart_image_remove_bg on each photo cut out, charged per photo, so quote it before building |
| Template | none |
| Ending | the last sticker holds 0.6 s longer, then a hard cut to black |
| Skills | scene-building-basics, motion-design-craft, resting-frame-rules |

- ID: freeze-sticker
- Format: freeze-frame sticker pop per clip
- Length: 8.4 s
- Cut rate: ~30 cuts/min (one slot every 2.1 s)
- Caption style: none
- Bed: punchy pop, ~120 BPM
- Layout: single
- Source: our style library

| Time (s) | Beat | What happens (picture) | Voice | On screen | Shot | Move | Caption | Sound |
|---|---|---|---|---|---|---|---|---|
| 0–1.2 | Hook | the first clip plays as shot | — | — | clip, full frame | as shot | — | bed |
| 1.2–2.1 | Freeze | the clip freezes on the beat; the person lifts off as a sticker and the picture behind dims and blurs | — | — | frozen frame + cut-out | scale up 108 % | — | bed |
| 2.1–7.8 | Run | the same play-then-freeze for each next clip, freezing on a downbeat | — | — | clips | as shot, then freeze | — | bed |
| 7.8–8.4 | Payoff | the last sticker holds, then cut to black | — | — | frozen frame + cut-out | hold | — | bed |
