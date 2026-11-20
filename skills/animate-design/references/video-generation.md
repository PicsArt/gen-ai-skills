1. **Show the balance FIRST.** Call `picsart_balance` and tell the designer what they have (the `amount`
   in `balances`, already rounded down to 2 decimals, plus `resetsAt` when the plan credits refill) **before** anything is chosen — this frames every cost
   decision that follows.
2. **Let the designer pick the model.** Narrow with `picsart_model_catalog` (`concise: false`) (plain
   data, no UI), then open **`picsart_model_choose`** with 2–3 candidates that fit the brief (exactly
   one marked `recommended`, each with a `creditsNote`); the pick returns as widget context. Don't
   pick silently when the trade-offs (duration vs resolution vs cost vs audio) are the designer's.
3. **Assemble params** with `picsart_model_params` (the model's schema) — prompt, duration, aspect,
   resolution.
4. **Get the EXACT cost — `picsart_preflight`** (free): it validates the params *and* returns
   the price in credits, a dry run with no charge. Fix every `errors` entry before going on.
5. **Ask for consent, showing the number.** State it plainly — *"this will cost ~N credits; you have
   M"* — and wait for an explicit **yes**. **No preflight cost shown + no explicit yes = no
   generation.** This is a hard gate: the only credit-spending action in the plugin, never run
   unasked. If `picsart_preflight` returns `credits: null` (pricing unavailable), say so and either get
   consent to proceed at unknown cost or stop — never charge silently.
6. **Generate** with `picsart_generate` (video defaults to `async: true` → a job handle; pass the
   project's `folderUid` so the take is filed under this design).
7. **Monitor** — `picsart_generate`'s own card follows the job(s) and posts the finished URL back;
   never ask the designer to wait or check.
8. **Place the result** as a `media` layer in the scene (it's real external footage — a legitimate
   video asset, the one uploaded asset that's generated rather than exported from Figma), positioned
   like any other layer, then previewed in the editor for approval as usual.
