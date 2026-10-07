# Motion — video generation and formats

## Video generation — opt-in, and CREDIT-GATED (the one paid capability)

Sometimes the design needs **generated footage** — a video card/element that should be real motion,
or the designer asks to generate a clip with the model they want. This is the skill's only
credit-spending path, so it is **always gated on the designer's explicit, informed consent.** Use it
only when the design genuinely needs it or the designer asks — never on your own initiative to "fill"
something. Run this flow **in order, and never skip the gate**:

1. **Show the balance FIRST.** Call `picsart_credits` and tell the designer what they have (`balance`,
   plus `nextResetDate` if the pool refills) **before** anything is chosen — this frames every cost
   decision that follows.
2. **Let the designer pick the model.** Narrow with `picsart_media_*`/`picsart_model_catalog` (plain
   data, no UI), then open **`picsart_model_choice`** with 2–3 candidates that fit the brief (exactly
   one marked `recommended`, each with a `creditsNote`); the pick returns as widget context. Don't
   pick silently when the trade-offs (duration vs resolution vs cost vs audio) are the designer's.
3. **Assemble params** with `picsart_model_params` (the model's schema) — prompt, duration, aspect,
   resolution.
4. **Get the EXACT cost — `picsart_preflight`** (free): it validates the params *and* returns
   `credits`, the dry-run price with no charge. Fix every `errors` entry before going on.
5. **Ask for consent, showing the number.** State it plainly — *"this will cost ~N credits; you have
   M"* — and wait for an explicit **yes**. **No preflight cost shown + no explicit yes = no
   generation.** This is a hard gate: the only credit-spending action in the skill, never run
   unasked. If `preflight` returns `credits: null` (pricing unavailable), say so and either get
   consent to proceed at unknown cost or stop — never charge silently.
6. **Generate** with `picsart_generate` (video defaults to `async: true` → a job handle; pass the
   project's `folderUid` so the take is filed under this design).
7. **Monitor** with `picsart_render_monitor` on the job(s) — it polls and posts the finished URL back;
   never ask the designer to wait or check.
8. **Place the result** as a `media` layer in the scene (it's real external footage — a legitimate
   video asset, the one uploaded asset that's generated rather than exported from Figma), positioned
   like any other layer, then previewed in the editor for approval as usual.

## Formats — MP Scene is the source of truth

Everything is authored and edited as an **MP Scene** — the scene format every
`picsart_media_*` edit / validate / query tool speaks, the one the scene editor plays, and the
one `sceneRef` points at. The **mp4** is *derived* from it at Stage 5 (`export`). The MP
Scene is the single editable source of truth — keep it and edit it; the mp4 is the final
render, never an editing surface.
