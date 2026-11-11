### Doodle book

| Field | Value |
|---|---|
| Group | Cards and frames |
| Looks like | a hand-made lyric book: each dark page has a ring binding down its left edge, one white-bordered photo at a slight tilt and a short phrase set as hand-lettered word art that fills the rest of the page, and the pages turn |
| Vibe | scrapbook book, journal, handwritten, cute, friendship, lyric book, page turn |
| Fit | slots 4–10; photos; friends, couple, family, pet, any; love, anniversary, birthday, Valentine's, Mother's Day, memories, any; cute, warm, romantic |
| Music | soft acoustic or ukulele, 90–105 BPM |
| Skin | the page is the skin's background; the word art uses the skin's text colour and its accents. With no skin (everyday): page #3B2A1F, letters in pastel yellow #F6E27F, pink #F4A6C8 and blue #93C9EE |
| Preview | none yet |
| Proven | yes: agent build 2026-11-07, close |
| Seams | `transition:page_curl` on every seam, 0.7 s |
| Motion | each page is still: a colour layer, the binding (a column of 13 small dark rings, shape layers 36 × 18 px at x 22–58, one every 140 px from y 60), one photo at 40–50 % of the width with a 16 px white border (a white rectangle behind the photo, both tilted together, −5° to 5°), and 3–5 doodles. The photo sits in the upper or lower half, left or right; the words take the other side |
| Text | one phrase per page, 6–14 words, from the user's words or written from what the photos show; a sentence may run on across pages. Break it into 4–7 lines. 1–3 key words per page in a bold display font in capitals, 120–160 px; the other words in a hand-lettered script, 50–70 px. Use three colours from the Skin, never one colour for a whole page. Lines write on one by one with `textAnimation:typewriter`, about 0.4 s each, then hold. Keep this readable: every line's box, line height included, inside y 300–1400 and x 90–1000, off the photo |
| Look | each photo a white 16 px border on a rectangle behind it (no tape frame); doodles are outline shapes from the scene's SVG-path import, 40–90 px, stroke 5 px in the accent colours: stars, hearts, a swirl, a little leaf, in the page's corners and gaps, never over a word or the photo; they hold still |
| Template | none |
| Ending | the last page holds, then a final `transition:page_curl` to a closing page, held 4.5 s: with 7 or more items the last 3 are kept for it, piled at tilts (−8°, 4°, −3°) under the skin title in the script; with fewer, the title alone among doodles. Each item is used once |
| Skills | scene-building-basics, motion-design-craft, visual-style |

- ID: doodle-book
- Format: lyric-book pages with one bordered photo and word art, turning
- Length: 27 s for 8 items: 5 pages of 4.5 s and the 4.5 s closing pile
- Cut rate: ~13 cuts/min (one page every 4.5 s)
- Caption style: word art on each page, mixed display capitals and script
- Bed: soft acoustic, ~96 BPM
- Layout: single
- Source: our style library

| Time (s) | Beat | What happens (picture) | Voice | On screen | Shot | Move | Caption | Sound |
|---|---|---|---|---|---|---|---|---|
| 0–4.5 | Hook | a dark page with the binding, a bordered photo and the first lines of the phrase writing on beside it | — | the phrase's first lines | bordered photo on a page | still | word art beside the photo | bed |
| 4.5–22.5 | Pages | each page curls over to the next photo and the next part of the phrase | — | 4–7 lines per page | bordered photos on pages | page curl | word art | bed |
| 22.5–27 | Payoff | a last page curl to a closing page: three photos piled, the title above | — | title "<skin title>" | closing page | page curl | title, top | bed |
