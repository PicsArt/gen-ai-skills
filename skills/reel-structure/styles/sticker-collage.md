### Sticker collage

| Field | Value |
|---|---|
| Group | Cut-outs and stickers |
| Looks like | everyone from your photos, cut out with white sticker edges, piles into one collage over a soft copy of the best photo, a script title in the middle |
| Vibe | sticker collage, cut outs, birthday collage, scrapbook, fun |
| Fit | slots 4–9; photos; friends, group, family, couple; birthday, party, any, holiday, Christmas, year-end; fun, playful, warm |
| Music | sparkly upbeat pop, 110–125 BPM |
| Skin | the script title is the skin's ("Happy birthday", "Merry Christmas"), in the skin's text colour with its accent as a soft glow |
| Preview | none yet |
| Proven | yes: agent build 2026-11-08, user-approved |
| Seams | none: one page that builds |
| Motion | the best photo fills the frame behind, held under effect:gaussian_blur (blur 30) and effect:adjust brightness −0.4; every photo's people are cut out (one picsart_image_remove_bg call per photo cut out (a per-image cost the build quotes before it spends)) and land one per beat with `look:stomp` (length 0.3, scale 1.4), overlapping in a loose ring around the centre at 40–60 % scale, tilted −10° to 10°, faces never covered |
| Text | a script title in the centre over the collage, `textAnimation:fade_in_chars` over 0.8 s after the last sticker lands; readable: on a soft cream plate behind the script |
| Look | every cut-out has `effect:stroke` width 16, #FFFFFF and `effect:drop_shadow` offset [0, 10], blur 20, #00000052; the title has `look:glow_pulse` (period 1.6, intensity 0.5); SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says) for picsart_image_remove_bg on each photo cut out, charged per photo, so quote it before building |
| Template | none |
| Ending | the finished collage holds 1.5 s with the title glowing |
| Skills | scene-building-basics, caption-decorations, motion-design-craft, resting-frame-rules |

- ID: sticker-collage
- Format: one cut-out sticker collage that builds
- Length: 7.5 s
- Cut rate: ~50 cuts/min (one sticker lands every ~0.5 s)
- Caption style: a script title in the centre
- Bed: sparkly pop, ~118 BPM
- Layout: single
- Source: our style library

| Time (s) | Beat | What happens (picture) | Voice | On screen | Shot | Move | Caption | Sound |
|---|---|---|---|---|---|---|---|---|
| 0–0.5 | Hook | the best photo, soft and dim; the first cut-out stamps on | — | — | photo + cut-out | stomp in | — | bed |
| 0.5–4.5 | Pile | one cut-out per beat stamps on around the centre until everyone is there | — | — | cut-outs on soft photo | stomp in | — | bed |
| 4.5–6 | Title | the script title writes on in the middle | — | title "<skin title>" | the whole collage | hold | title, centre | bed |
| 6–7.5 | Payoff | the collage holds, the title glowing | — | title | the whole collage | hold | title, centre | bed |
