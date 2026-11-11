### Year flip

| Field | Value |
|---|---|
| Group | Text-led |
| Looks like | big year digits on a dark screen, the last digit rolls over to the new year, then a quick recap of your year ends on "Hello <new year>" |
| Vibe | new year, year flip, countdown, goodbye 2026, hello 2027, fresh start |
| Fit | slots 8–24; mixed; any; New Year, year-end; upbeat, epic, fun |
| Music | building festive pop with a drop at the flip, 120–130 BPM |
| Skin | the digits are this year rolling to the next; text in the skin's accent (gold) on its background |
| Preview | none yet |
| Proven | yes: agent build 2026-11-07, close |
| Seams | hard cuts on the beat; `flash_cut` white (0.167 s) at the flip |
| Motion | the digits hold, then the last digit rolls up and out while the new digit rolls up into place (each 0.5 s, textAnimation:slide_up_lines on the two digit layers), on the drop; then each photo or clip full frame for one beat, as shot |
| Text | the year, heavy sans 260 px, centre; the last digit is its own layer so it can roll; "goodbye" small above it before the flip; at the end "Hello <new year>", script over caps, `textAnimation:word_lift`; readable: on the flat ground; the end line with a soft shadow |
| Look | the digits `look:glow_pulse` (period 1, intensity 0.6, blur 26) |
| Template | none |
| Ending | "Hello <new year>" over the best photo, held two bars |
| Skills | scene-building-basics, motion-design-craft, linked-element-motion, visual-style |

- ID: year-flip
- Format: a year-digit roll, then a beat-cut recap
- Length: 14 s
- Cut rate: ~110 cuts/min after the flip (one shot per beat)
- Caption style: the year digits, then Hello <new year>
- Bed: festive pop with a drop, ~125 BPM
- Layout: single
- Source: our style library

| Time (s) | Beat | What happens (picture) | Voice | On screen | Shot | Move | Caption | Sound |
|---|---|---|---|---|---|---|---|---|
| 0–2.5 | Hook | "goodbye <year>" on a dark screen, the digits glowing | — | "goodbye <year>" | dark card | hold | year, centre | bed |
| 2.5–3.5 | Flip | the last digit rolls over to the new year on the drop, a white flash | — | the new year | dark card | digit roll | year, centre | bed |
| 3.5–11.5 | Recap | the year's photos and clips cut on every beat | — | — | photos and clips | as shot | — | bed |
| 11.5–14 | Payoff | "Hello <new year>" over the best photo | — | "Hello <new year>" | photo, full frame | hold | title, centre | bed |
