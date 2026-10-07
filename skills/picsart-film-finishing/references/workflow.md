# Finishing — grade, sound, master, archive

Picture lock is behind you; nothing here changes the cut. The order inside this
skill is fixed and worth saying out loud to the user: **final-res re-roll →
re-assemble → grade → export once → masters → archive.** Grading the 480p draft
wastes the grade; exporting before the grade wastes an export.

For the paid final pass, follow `../../picsart-film-scenes/references/step-2-shot-design.md`, **Native draft to
final**: use `fromDraft` only when this connection's live schema and preflight
accept it. Otherwise explicitly quote a regular final rerender and review the
changed picture before grading. Then re-assemble, grade and export once with
`picsart_media_export`, as below; a draft is not a final-resolution deliverable.

## The final-resolution pass — pay once

The final quality comes from
**re-generating every approved shot at the final resolution with its saved final
prompt, verbatim** — same blocks, same references, higher `resolution`. Preflight
the whole batch, quote the total, and dispatch only on the user's yes; this is
the film's biggest single spend and the one that must never arrive as a
surprise. Video upscaling exists on this surface; pick the upscaler
from the live catalog at the time of the pass (`picsart_model_catalog`,
`purpose: "utility"`) — none is named here, because the tools change. **The
practitioner post order is: upscale FIRST, then texture, then grade** — every
downstream correction should touch the highest-resolution pixels. Then
re-assemble the locked cut at the final canvas (≤1920×1920 —
multi-shot output cannot exceed it, whatever a single model renders).

Say the quiet part: this pass follows the approved prompts but is a **fresh
roll**. Small differences from the draft are expected and are not a bug. Where a
re-roll visibly breaks something the draft had (a face, a join), that is a Stage 8
regeneration on the final-res take — log it, fix it, move on.

## Stage 9 — colour: unify, then grade

Every generation arrives with its own baked-in grade, so the first job is
**unification** — bring neighbouring shots of each scene to one look — and only
then the creative grade. The creative tone already exists: it was baked into the
location assets in Stage 4, so the grade refines, never invents.

**Grade with scene looks.** Resolve the real looks with
`picsart_media_resolve_looks` (never a remembered look name), offer three or four
against the bible's palette line (or the locations' own colours with scheme
Auto) via the host's question interface, then apply the chosen one with
`picsart_media_apply_look` / adjust patches on the assembled scene. Setting a
look is free; it is charged only when a preview
(`picsart_media_contact_sheet`, per frame) or the export renders. Preview the
grade on a handful of frames from two or three scenes before approving it for the
film.

Scope order: per-scene unification first (`scope: "sc01"`), then the film-wide
look. **The anti-AI-look recipe** — the documented practitioner finish for
generated footage — layers in this order: upscale (above) → a film-grain /
fine-texture pass → the grade "until it reads closer to live action". Footage-
level grain at finishing is distinct from the style prefix's in-generation
grain: the prefix shapes what the model renders; this pass unifies what the
renders became. If the user has a real colorist instead, export ungraded and
hand off — see the package below.

## Stage 10 — sound: clean, bed, or hand off

What generation gave you: lip-synced dialogue in the shot, in-frame action noise,
some ambience. What it cannot give: consistent voice timbre between clips,
licensed music, a mix. The in-chat path:

- **Dialogue follows the film's voice policy** (`film.json.voicePolicy`, always
  `native` — there is nothing to decide, `picsart-film-development`). `native`: the generated voice is the performance — never
  re-recorded; between-clip timbre drift is a fact, and where it distracts,
  prefer a retake of the worse clip (Stage 8 path) over pretending a mix exists
  here.

  **Stage 10 works with what the takes gave it.** Dialogue is not replaced or
  re-voiced. Sound at Stage 10 means two things: a continuous bed under each
  scene to hide the level and tone steps at every join, and honest level
  matching shot to shot. Do not offer a voice fix; say what the film has.

  Where the user supplies a recorded voice track for a line and the mouth is on
  screen for all of it, the shot can be generated audio-driven from the start
  (an audio-to-video model from the live catalog — an audio track plus an
  optional first frame), so the lips follow that voice from the outset. Check
  the catalog for what is current rather than remembering a model id. This
  re-opens the shot, so decide it before picture lock, not here.
- **Ambience is the glue**: when shots of a scene differ slightly in picture, a
  continuous bed stitches them into one space. Generation audio is per-clip, so
  seams are audible; note where, and lean on the music bed to carry across them.
- **Music bed — offered ONCE, only after the cut is picked.** Scoring a cut
  that is about to change wastes the track, and a declined offer is settled for
  the session. Don't interrogate ("do you want music?") — draft the brief from
  what the film already knows (register from the bible, tempo from the cut) and
  offer three exits: generate it, tweak the vibe, or skip.
  `picsart_generate` with a music model from the live catalog
  (`picsart_model_catalog`, `mode: "audio"`, `inputType: "music"`), and
  **instrumental always under speech** — vocals fight the dialogue for the same
  perceptual channel and both lose. Mix as a separate compositor audio track,
  dialogue dominant (duck the bed under lines; at full level only when the film
  has no speech). Flag plainly that generated music's licensing is the user's
  to verify for festivals/commercial use.
- **Sound post is a team's job**: a film going to festivals or dubbing needs a
  sound post team; offer the handoff package instead of imitating one.

**Handoff package** (either stage, when a human colorist/sound team exists): the
clean cut + per-shot source URLs from selects at max quality, the shot order and
trims from `docs/`, the bible (tone, colour scheme and palette line), the sound references gathered
with the film's references, and the generation audio as-is. The media already durable on Drive and the
documents in the workspace project folder — that is the handoff.

## Stage 11 — master, QC, archive

QC on the full final export, ideally by fresh eyes, per the checklist in
`delivery.md` (artifacts, joins, digital errors, titles — titles are
made in an editor or as overlay tracks, never generated; models cannot hold clean
typographic text). Then the deliverables and the archive — the full table and
list live in `delivery.md`. The archive is not sentimental: prompts + registry +
log are **the means of production**; a sequel or a re-cut regenerates from them.

**The disclosure pack is a deliverable, not a note.** Festivals (SXSW,
Tribeca, the AI-specific festivals) require disclosure of the AI tools and
models used — incomplete disclosure disqualifies at some. Write
`docs/DISCLOSURE.md` mechanically from the generation log: every model used,
per stage (images, video, voices, music), plus the human-contribution
statement and an AI-credits block for the titles. It costs nothing and the
film cannot be submitted without it.

Gate out (the film is done): QC notes closed · masters exported and checked by
playback · archive complete (media on Drive, documents in the workspace
project folder) · `docs/DISCLOSURE.md` written · rights notes
(voices, music, AI-use disclosures where a platform requires them) gathered in
one place.

## Costs

| Free | Charged |
|---|---|
| look resolution, grade setting, scene re-bootstrap, planning, handoff assembly, every `picsart_media_export` (final and each master variant — render time and a file, **not credits**) | the final-res re-roll (every shot, video rates), grade previews (`picsart_media_contact_sheet`, per frame), music generation |

## Traps

- Grading before the final-res re-roll — grade the final pixels, not the draft's.
- Calling the final pass an upscale. It is a fresh roll; say so before it runs.
- Re-rolling the film at final resolution on the strength of the original
  forecast. Quote this batch, then wait — it is the biggest single number in
  the project.
- "One more export" per master variant nobody asked for. Exports cost no
  credits, but each is a real render and another file in the user's Drive —
  confirm the deliverable list first.
- Shipping generated music to a festival without the licensing caveat in writing.
- Archiving the film but not the prompts and registry — the film without its
  means of production cannot be revised or continued.
