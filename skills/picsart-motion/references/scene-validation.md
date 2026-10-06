# Scene validation — schema is not enough; the eye is the real check

A scene that **validates** is not a scene that is **right**. `validate_scene` proves the JSON is
*legal* — legal fields, legal values. It says nothing about whether the pixels are correct: a scene
can validate clean and still render a **blank layer** (asset failed to load / CSP-blocked), a **photo
cropped or softened**, **text wrapped** to two lines, a **headline off-frame**, **transparency baked
onto black**, or the **wrong z-order**. None of that trips the schema. **The real validator is
rendering the scene and looking at it.**

So validation is a ladder, each rung a real check. Climb it in order; do not stop at rung 1.

## Rung 1 — Schema-valid (necessary, cheap, first)
`picsart_media_validate_scene` — no `severity:error`. Fix and re-run until clean. This catches
structural mistakes fast and for free. **It is necessary, never sufficient** — treat a clean
`validate_scene` as "worth rendering," not "correct."

## Rung 2 — Boots & renders (the "validates but won't boot" traps)
A scene can pass rung 1 and still fail to *render* or to *boot the browser editor*. The known traps
(full detail in [`engine-gotchas.md`](engine-gotchas.md) / [`authoring-flow.md`](authoring-flow.md) §5):
- **Font must come from `picsart_media_list_fonts`** (a catalog `key`, or a live entry's `asset` in
  `assets[]`), never a bare CSS family name — that renders empty text.
- **Every asset Picsart-hosted** (the URLs Picsart tools return) — never `figma.com`, `data:`, or `blob:`. Those
  render server-side but are **CSP-blocked → blank** in the editor preview.
- **One track per channel**; mask addressing via the owner; shape `anchor` via a group item.

Prove it on **both** surfaces: a `contact_sheet` still (server render) **and** the editor preview
(browser boot). A clean contact-sheet is **not** proof it boots in the preview.

## Rung 3 — The eye check (the real validator — run it yourself, before the user sees it)
Render a still (`contact_sheet` at the beat, which returns its frames inline, or an `export` frame)
and **view it with your own vision** (`picsart_view_image` on a still's URL). This is the rung that catches the bug class every *tool* misses. Check:

- **Blank / missing layer** — an asset didn't load (CSP), a fill is empty, a layer is transparent.
- **Off-frame / cropped** — an element outside the canvas, a photo cut off by its `fit`.
- **Text clipped or wrapped** — a line that overflowed and wrapped, or clipped, vs intended.
- **Overlap / wrong z-order** — the leak `layout_lint` misses (it's opacity-blind), a cover that
  doesn't cover, a layer behind what it should be in front of.
- **Colour / transparency wrong** — black baked behind a cut-out, a gradient rendering flat, a dimmed
  layer (sRGB→linear opacity).
- **Matches the ground truth** — the elements/motion that *should* be there are actually there.

**Run `layout_lint` as the cheap machine pass that feeds this rung — it is not optional.** It scans
box collisions across the **whole timeline** automatically, catching overlaps at beats your single
eye-check still would miss; run it (and `query_layout` for `onCanvas`/positions) on every scene, then
look. Its opacity-blindness is a reason to **also** use your eye, never a reason to skip the lint: it
cannot see a semi-transparent leak, a failed asset, or a cropped photo — all of which are obvious to
an eye. Machine pass **and** eye, in that order; neither replaces the other.

| What it catches | Tool | Blind spot |
|---|---|---|
| Legal JSON/values | `validate_scene` | says nothing about pixels |
| Box collisions over time | `layout_lint` | boxes only, opacity-blind |
| Off-canvas / positions / z-order | `query_layout` (`onCanvas`) | geometry, **not painted pixels** |
| Blank asset, cropped photo, clipped text, wrong colour | **the eye** (render + view) | — |

## Rung 4 — Matches the ground truth (route-dependent) + user approval
What "right" *means* depends on how the material came in (see the Stage-0 triage). This is the rung
that has no single tool — it is judged, then confirmed by the user on the **moving** preview.

- **Figma design → render-match.** There is a reference image: put a `contact_sheet` still beside the
  Figma frame's image (from the Figma connector, or exported and uploaded by the user; view it with
  `picsart_view_image`) and compare — text that clipped/shifted, layers off-position, wrong z-order,
  a dropped element (a hole where the design has content). The design is the answer key.
- **Assets + a brief → brief-contract.** No reference image, so **the brief is the spec.** Before
  authoring, restate what you heard as a concrete checklist — "3 photos, 9:16, each slides up with a
  0.1s stagger, title types on over photo 1, 4s" — and get a yes on *that*. Then validate the render
  against that written contract, element by element.
- **Assets, no brief → chosen-concept.** The ground truth is the **concept the user picked** from the
  2–3 you offered (see *Propose mode*). Validate the render against that concept's stated moves.

In all three, the **user's eye on the moving preview is the final rung** — especially for the two
no-reference cases, where only the user can confirm "yes, that's what I meant." The preview is not a
courtesy; with no design to diff against, it is the only ground-truth check that exists.

## The eye works at both ends
Rung 3 validates the **output**. In **propose mode** the same eye analyzes the **input**: you must
**view the uploaded assets** (`probe_media` for dims/fps/duration, plus `picsart_view_image` to see *what*
they are — photos? a logo? screenshots? a clip?) before you can propose sensible motion. Same eye,
both ends: look at what came in to plan, look at what rendered to validate.

## The rule
**Never present a scene you have not rendered and looked at.** Schema-clean is permission to render,
not permission to ship. Render → view it yourself (rung 3) → confirm it matches the ground truth
(rung 4) → show the user. A scene shown on a `validate_scene` pass alone, un-looked-at, is the
failure this reference exists to prevent.
