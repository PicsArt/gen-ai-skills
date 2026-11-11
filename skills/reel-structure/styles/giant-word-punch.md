### Giant word punch

| Field | Value |
|---|---|
| Group | Text-led |
| Looks like | one giant word fills the screen on every beat over your clip, the picture flashing hot pink behind it |
| Vibe | big words, bold text, hype, fun, loud, pink |
| Fit | slots 1–6; clips; solo, friends, couple; party, night out, birthday, any; bold, energetic, fun |
| Music | loud reggaeton or pop with strong beats, 95–125 BPM |
| Skin | the tint is the skin's accent; with no skin, hot pink #FF2D95. The words never come from the skin title |
| Preview | none yet |
| Proven | yes: agent build 2026-11-07, close |
| Seams | hard cuts every two bars |
| Motion | the clips play as shot; on every beat a new word layer replaces the last |
| Text | the words are the user's; with none, write a hype phrase of 3–6 words from what the clips show and the occasion ("BEST NIGHT EVER", "WE WERE THERE", "ONE MORE SONG"), one word per beat, the phrase repeating; a long word may split over two beats ("CORA", "CORAZÓN"). Heavy condensed block caps, as wide as the safe band allows: the resting word about 780 px wide (measure it; set the size per word), centred on x 500 so `textAnimation:word_spring`'s overshoot stays inside x 70–915, left of the right-hand buttons. Take `textAnimation:word_spring` without its fade-in, or each beat opens on a blank frame. Place it in the face-free band nearest the centre (y 700–1250); never the top strip. On every other beat the word is the accent colour with a dark stroke, otherwise near-black over the pink picture. readable: each word whole at its rest frame and at least 0.4 s on screen |
| Look | on the beats with a dark word, the clip flashes hot pink: `effect:colorize` hue of the accent, saturation 50 (the catalog's most), then `effect:adjust` shadows 0.4, highlights 0.2 and, on dark footage (a concert, a night out), exposure 1.5–1.8, so the frame reads bright pink, never dark purple. Check one pink frame: the people still show through, lighter |
| Template | none |
| Ending | the whole phrase, stacked one word per line (each line about 500 px wide), in the face-free band, holds over the clip for one bar and at least 1.6 s |
| Skills | scene-building-basics, motion-design-craft, visual-style |

- ID: giant-word-punch
- Format: giant words on the beat over clips
- Length: 8 s
- Cut rate: ~30 cuts/min (a clip every 2 bars; a word every beat)
- Caption style: one giant word per beat, centre
- Bed: reggaeton pop, ~120 BPM
- Layout: single
- Source: our style library

| Time (s) | Beat | What happens (picture) | Voice | On screen | Shot | Move | Caption | Sound |
|---|---|---|---|---|---|---|---|---|
| 0–0.5 | Hook | a clip with a giant word slamming in across it | — | word 1 | clip, full frame | as shot | giant word, centre | bed |
| 0.5–7 | Words | a new giant word every beat, the clip tinting pink on alternate beats | — | words | clips, full frame | as shot | giant word | bed |
| 7–8 | Payoff | the last word holds | — | last word | clip, full frame | as shot | giant word | bed |
