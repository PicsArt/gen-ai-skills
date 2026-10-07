# Motion patterns — "how to animate *this*" recipe lookup

A scenario → recipe catalogue: given what an element **is** or the interaction it **simulates**,
this is a good default way to move it. These are starting points, not laws — the designer
overrides, and the durations/easing register scale with the reel's **motion personality**
([`motion-principles.md`](motion-principles.md) §6). Resolve every easing id and preset from
`picsart_media_get_capabilities`; never author a bézier or preset from memory. Every recipe below
maps to a **real mp-scene preset / transition** — see [`mp-scene-vocabulary.md`](mp-scene-vocabulary.md)
for the authoritative set (there is no `back`/`bounce` easing; overshoot = `scale_pop`/`spring`).

**Two kinds of scenario, because we make ads, not live UIs:**
- **Screen / element transitions** apply **directly** — they *are* our A→B frame motion and entrances.
- **Simulated interactions** (button press, toggle, hover) apply **only via the tap-dot / cursor
  interaction-sim** — in an ad we animate a *depicted* interaction, then the state change it
  causes; we are not wiring a real control. Author the tap-pulse *before* the state change it
  appears to trigger (see `picsart-motion-design`).

The property rule under all of them: **the primary property carries the meaning, a secondary adds
polish — two properties is the sweet spot.** (Property choice per goal is in `motion-principles.md`.)

---

## Screen / element transitions (apply directly to A→B frames)

Author each as a real **seam transition** (`slide`, `push`, `page_curl`, `crossfade`,
`zoom_through`, `iris`, `card_flip`, `shape_reveal`…) and/or **entrance presets** (`slide_in`,
`fade_in`, `reveal_in`, `zoom_in`, `flip_in`). Resolve ids from `get_capabilities`.

| Scenario | Recipe |
|---|---|
| **Page / screen transition** | Outgoing slides out + fades (~300ms, ease-in); incoming enters from the opposite edge at ~100ms delay (~400ms, ease-out); the hero scales in, then supporting content staggers ~50ms. Direction follows the navigation (a forward step moves left→right). |
| **Modal / overlay open** | Backdrop dims (~200ms) → the panel scales in at ~50ms (~300ms) → its contents enter in reading order (title ~200ms, body ~280ms, actions ~350ms). |
| **Dropdown / menu** | Scale-Y 0→100% from the anchor edge (~200ms, ease-out); items fade in ~30ms apart. |
| **Notification / toast** | `slide_in` from the nearest edge + opacity (~250ms), 3–15% overshoot via `scale_pop`; icon delayed ~50ms. |
| **List reveal** | Each row slides up ~20px + fades (~200ms, ease-out); stagger 40–60ms; whole cascade <400ms (see [`choreography.md`](choreography.md)). |
| **Grid / card reveal** | Scale from 95% + fade (~250ms); stagger 50–80ms in reading order, +~20ms per new row; shadow follows the card ~50ms later. |
| **Tab switch** | Indicator slides (~250ms) while old content fades (~150ms); new content enters from the tab's direction at ~100ms. |
| **Accordion / expander** | Arrow rotates (~150ms) + height expands (~250ms) + content fades in at ~50ms; siblings shift to make room. |

### Progressive text build (accumulating frames)
The most common storyboard case, and the one most often mis-handled as a whole-frame transition:
**B's text is a superset of A's** — a line, word, or block was *added*.

**The non-negotiable:** the newly-added text gets its **own** entrance. Never let it just appear or
ride in on the frame transition. **Diff A→B** (`picsart_media_diff_layouts`, or `query_layout` on
both as fallback) so you know which layer is `entered`, then animate that layer with `apply_text_animation` — `typewriter` / `fade_in_chars` /
`slide_up_lines` / mask-reveal (see [`mp-scene-vocabulary.md`](mp-scene-vocabulary.md)), eased
**out**. If a text block grew rather than adding a node, animate **only the new portion**, never a
re-type of the whole block.

**Caveat — the diff mislabels this pair, so don't take it at face value.** A grown string (`AI` →
`AI Effects`) is *different text*, so `diff_layouts` (and name-matching) reports `exited`+`entered`,
i.e. "cut" — the exact trap that produces a fade. Two things fix it: (1) at import, the persisting
substring is its **own layer** with a stable `matchKey` (see `picsart-motion-import`), so the shared words
are a real matched layer, not part of a monolithic node; (2) treat a prefix/superset relationship as
**matched shared words + entered new words**, overriding the diff's `exited`+`entered`. Without (1)
there is no layer to smart-animate and you *will* fall back to a transition.

How the *already-shown* text behaves depends on whether it's **connected to the new line** — part of
the same text block/group (one headline growing). If so, adding a line re-centers the block, so the
held lines classify `moved` → **smart-animate the reflow** (they shift to make room as the new line
enters). If the held text is a **separate, unrelated element**, it just holds still. Check the diff
rather than assuming.

When the connected lines should move or scale **together as a unit**, don't keyframe each line
separately — drive them with one transform:
- the composition's **`camera`** — a single animatable transform over *every* layer in that
  composition about a shared pivot (the "one push-in, not forty layer moves" construct), or
- a **parent layer wrapping a nested/inline scene** that holds the lines — animate the parent's
  `transform` and its children follow.

That shared transform is what makes a closing **group emphasis** (e.g. all lines scaling together to
reframe) one clean move; it's optional polish, not required.

## Simulated interactions (apply ONLY via tap-dot / interaction-sim)

> **`tap_pulse` IS a real preset.** `apply_motion_preset("tap_pulse")` is a **one-shot dip to ~0.92 and back** (the
> press), with an **`at`** param for *when* it fires mid-shot and `appliesTo` including `shape`. Prefer
> it for a press. Still resolve it from `get_capabilities`; **only if it isn't listed there** compose the
> press from `apply_motion_preset("scale_pop")` + `opacity` keyframes. The *appear/fade of the tap-dot
> itself* is still `opacity` keyframes either way.

| Scenario | Recipe (the depicted interaction, then its result) |
|---|---|
| **Button tap** | Tap-dot fades in (`opacity`) → target **presses** (`tap_pulse`: a one-shot dip to ~0.92 and back, `at` = the moment of contact), + a shadow/color nudge. Then fire the state change it "caused." (Build without `tap_pulse` → `scale_pop` down 0.95–0.98 → overshoot ~1.05 → settle.) |
| **Toggle / switch** | Thumb `position` slides across (120–180ms, `ease_in_out`); track colour crosses at the same time; a touch of directional `scale` (author-managed). |
| **Hover / focus emphasis** | Subtle `scale` 1.02–1.05 (or icon 1.1 + 2–5° rotate); ~100ms in, 150–200ms out. Use sparingly — an ad rarely needs hover. |
| **Success confirm** | Container pops 0.9→1.0 (`scale_pop`, ~200ms, 5–10% overshoot); a checkmark stroke draws (~150ms, ~100ms delay) + a brief `glow_pulse`. 400–500ms total. |
| **Error / rejection** | The `shake` preset: horizontal ±10–15px, 2–3 decreasing cycles, 300–400ms; pair with a colour shift, never colour-only. |
| **Loading / progress** | Spinner = `rotation` keyframes/expression, `linear`, 1000–1500ms/rev; or a `shimmer` skeleton sweep, 1500–2000ms. (Ambient — keep it under the primary motion; see [`choreography.md`](choreography.md).) |

## Exit rule (applies to all of the above)
**An exit runs ~65–75% of its entrance duration** and eases *in* (accelerates away). Don't reuse
the entrance timing for the exit — a matched entrance/exit at equal length feels sluggish leaving.
