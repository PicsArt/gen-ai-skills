# Delivery — QC, masters, promo reframes, archive

## Technical QC — frame-by-frame, fresh eyes if possible

| Category | Look for |
|---|---|
| Visual artifacts | extra fingers, drifting objects, flicker, boiling textures, random pseudo-text on signs and screens |
| Joins | dropped frames, black frames, sound desync at seams |
| Digital errors | banding in gradients, over-compression, dead pixels |
| Titles | spelling, rights, mandatory mentions — including AI-use disclaimers where the platform or festival requires them |
| Sound | levels consistent scene to scene; nothing clipping; the bed does not swallow a line |

A QC note is either fixed (Stage 8 path on the final-res take, or a title/track
fix) or accepted in writing. The list closes before masters.

## Masters — what this surface can and cannot deliver

| Purpose | Format | On this surface |
|---|---|---|
| Streaming / online | H.264/H.265 MP4 per platform spec | yes — `picsart_media_export`, ≤1920×1920 |
| Promo / social | vertical 9:16 and square 1:1 versions | yes — reframe (below) |
| Archive master | ProRes 4444/422 HQ, max resolution | **no** — export is MP4; keep the per-shot final-res sources on Drive as the effective archive master |
| Theatrical DCP, 5.1 mixes, stems | DCP / broadcast specs | **no** — needs a post house; the handoff package is the route |

Every master variant is its own export — no credits, but a real render each —
so confirm the list with the user before rendering any of them.

## Promo reframes — 16:9 → 9:16 / 1:1

A reframe is a new composition, not a crop of convenience: re-bootstrap the locked
cut at the promo canvas (1080×1920 or 1080×1080) with `fit: "cover"` and set
`align` per shot so the subject survives the crop — faces and the action side, not
frame center. Judge the crop per shot with `picsart_media_query_layout` (free).
Where a subject moves across frame, reframe that shot with
`picsart_media_reframe_video`, which tracks the subject with an animated pan and
zoom, then check it with `picsart_media_validate_scene` and a 2–3-frame
contact-sheet spot-check before the export — then one export per variant. A promo cut is usually also *shorter* — offer a 15–30s selects-of-selects
version rather than squeezing the whole film into a phone frame.

## The project archive — the means of production

Two homes, one project: media on `picsart_drive` (its upload takes images,
video and audio only), and text and documents in the workspace project folder
(`film.json`, `docs/`, the scenes folder). Both are duplicated wherever the user
keeps their own backups.

On Drive, the media:

- Reference images and the board images.
- All selects at final resolution — the cut sources.
- The masters themselves.

In the workspace project folder, the text and documents:

- All final prompts, all versions, and the generation log.
- The asset library's descriptors and the consistency registry, with the Drive
  locations of their reference images.
- Breakdown, shotlists, the visual bible (style prefix, colour scheme and palette line).
- The cut records: shot order, trims, transitions per scene (the EDL-equivalent),
  and the approved scene documents.
- The rights notes: voice notes, music licensing status, AI-service terms,
  disclosure texts used in titles, and `docs/DISCLOSURE.md` — the per-stage list of
  AI models used, written from the generation log (festival submissions
  require it; some disqualify without it).

The test of a complete archive: could a new session, given only these two places,
regenerate a broken shot, re-cut a scene, or start the sequel with the same faces?
If any answer is no, something above is missing.
