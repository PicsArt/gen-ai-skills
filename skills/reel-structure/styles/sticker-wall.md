### Sticker wall

| Field | Value |
|---|---|
| Group | Cut-outs and stickers |
| Looks like | the people from your photos, cut out with a white sticker edge, pop onto a plain white page one per beat until it is full |
| Vibe | stickers, cut out, sticker wall, playful, pop out, collage |
| Fit | slots 6–16; photos; solo, friends, group, couple, pet; any, party, birthday, everyday; fun, playful, upbeat |
| Music | bouncy pop with a clear beat, 120–140 BPM |
| Skin | the page is white for every skin; the title is the skin's, small, in the skin's background colour at the top |
| Preview | none yet |
| Proven | yes: agent build 2026-11-08, user-approved |
| Seams | hard cuts: one page, then a second page for the rest |
| Motion | each photo's subject is cut out (one picsart_image_remove_bg call per photo cut out (a per-image cost the build quotes before it spends)) and lands on the beat with `look:pop` (length 0.25, overshoot 1.15) at its own size (35–60 % of the frame) and spot, slightly tilted (−8° to 8°), never covering an earlier face; nothing moves after it lands |
| Text | the skin title at the top, y 260, `textAnimation:word_lift` over the first beat, then held; readable: on the wall's flat ground above the stickers |
| Look | every cut-out has `effect:stroke` width 14, #FFFFFF and `effect:drop_shadow` offset [0, 10], blur 18, #00000040; the page is a flat #FFFCF8 colour layer; SPEND (quote it in one line, then get the yes with your host's own question tool, such as AskUserQuestion, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", never as a typed question; only where the host has no such tool, those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says) for picsart_image_remove_bg on each photo cut out, charged per photo, so quote it before building |
| Template | none |
| Ending | the full page holds one bar, then every sticker leaves with `look:fade` (0.3 s) |
| Skills | scene-building-basics, motion-design-craft, resting-frame-rules, visual-style |

- ID: sticker-wall
- Format: cut-out stickers on a white page
- Length: 8.4 s
- Cut rate: ~110 cuts/min (one sticker lands every beat, ~0.467 s)
- Caption style: the skin title only, small, top
- Bed: bouncy pop, ~128 BPM
- Layout: single
- Source: our style library

| Time (s) | Beat | What happens (picture) | Voice | On screen | Shot | Move | Caption | Sound |
|---|---|---|---|---|---|---|---|---|
| 0–0.47 | Hook | a white page; the first cut-out person pops on with a white sticker edge | — | title "<skin title>" | cut-out on white | pop in | title, top | bed |
| 0.47–5.6 | Wall | one more cut-out pops on every beat at a new size and spot until the page is full | — | — | cut-outs on white | pop in, tilted | — | bed |
| 5.6–7.5 | Payoff | the full sticker wall holds | — | — | the whole page | hold | — | bed |
| 7.5–8.4 | Out | the stickers fade off and the page is clear | — | — | white page | fade out | — | bed |
