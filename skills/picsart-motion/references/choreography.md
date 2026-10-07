# Choreography — sequencing multiple elements in one beat

When more than one element moves across an A→B pair, *when* each fires is what makes it read as
designed rather than as noise or a slow train. This is the orchestration layer on top of the
per-element choices in [`motion-principles.md`](motion-principles.md) (§2 change→motion, §4
focal + stagger budgets). Values are defaults; resolve easing ids from `get_capabilities`.

## The three-phase shape of a beat
Every multi-element beat has a **setup → action → resolution** arc:

- **Setup** ~20–30% of the beat — anticipation, backdrop dim, the focal element arriving.
- **Action** ~30–40% — the main move (the matched smart-animate, the entrance).
- **Resolution** ~30–40% — supporting elements land, overshoots settle.
- **Then hold still** 100–200ms minimum before the next beat — no dead air, but a breath so the
  eye lands. (Ties to `picsart-motion-design`'s hold rules.)

## Rules for sequencing
- **One focal path.** With 3+ animated elements, **at most ⅓ are active at once.** Lead with the
  focal element (§4); the rest follow. Never fire everything together.
> **All of this is author-managed.** mp-scene has **no** stagger, follow-through, or parallax
> *primitive* — you realize them yourself by offsetting each layer's keyframe start times and
> giving deeper layers smaller `position` deltas (see [`mp-scene-vocabulary.md`](mp-scene-vocabulary.md)).

- **Stagger by tier** (from `motion-principles.md` §4): Micro 20–40ms, Standard 50–100ms,
  Dramatic 100–200ms — cascade totals under ~200/400/600ms respectively. (Offset each layer's
  first keyframe by the tier delay.)
- **Same easing family across a stagger — vary only the start time, not the curve.** A cascade
  where each item eases differently reads broken.
- **Synchronised reactions start within 50ms of each other** (they may *land* at different times —
  staggered landing is fine, staggered *starts* on a shared cause is not).
- **Depth by speed** (parallax, author-managed): foreground 1.0×, midground 0.5×, background 0.2×,
  deep bg 0.1× — give deeper layers a smaller `position` delta. Total drift <100px; never parallax text.
- **Stagger patterns** (pick by content): sequential (reading order — the default), center-out
  (radiating from a hero), wave (sine-based), reverse (bottom-to-top). Order should match how the
  eye is meant to travel.

## Recipes (concrete sequences)
Timelines are relative to the beat's start (0ms):

- **Dashboard / multi-widget load:** 0 skeletons → 100 hero metric (250ms, ease-out) → 200 widgets begin (200ms each, 60ms stagger) → 350 chart draws (300ms) → 500 all landed → 650 ambient begins.
- **Modal + content:** 0 backdrop dim (200ms) → 50 modal scales (300ms) → 200 title → 280 body → 350 actions → 400 close affordance (reading order).
- **Page transition:** current slides left + fade (300ms, ease-in) → new page enters right at 100ms (400ms, ease-out) → hero scales in → content staggers 50ms. Optional shared-element morph ~400ms.
- **List update:** rows slide up 20px + fade (200ms, ease-out), stagger 40–60ms, total <400ms for ~8 items.
- **Grid entrance:** cards scale from 95% + fade (250ms), stagger 50–80ms reading order, +20ms per new row; shadow trails the card ~50ms.
- **Nav items:** slide from side + fade (180ms, ease-out), stagger 30–50ms, total <300ms.

## The current — one dominant direction for the whole reel
Choreography isn't only per-beat; the **reel** has a direction too. Pick **one dominant
motion direction** for the cut — usually **leftward** (`−x`), matching how a UI walkthrough
advances — and let most seams and entrances flow with it. A consistent current is what makes
a multi-frame cut feel like *one camera travelling through the product* instead of a deck of
independently-animated slides.

Deviations from the current are **reserved for meaning**, not variety:
- **Upward** (`−y`) — an elevation or reveal (a result rising, a summary lifting into view).
- **Scale-up / Z-forward** — going *deeper* into the same thought (a detail, a drill-in).
- **Scale-down / Z-back** — an *arrival* or pull-back to context (a payoff landing, a
  zoom-out to the whole).

So a seam that runs against the current should be a **deliberate narrative beat**, and the
Vector Law (`transitions.md`) still governs *how* it carries. A direction change with no
meaning behind it is the "unmotivated cut" that reads as noise — pick the current early,
note it in state, and make every exception earn its reversal.

## Stillness before the climax
Before the single most important moment of a beat (the metric that lands, the headline that
completes, the result that resolves), insert a **0.3–0.75s hold where nothing moves** — a
deliberate breath between the action and its payoff. The pause is what gives the climax its
weight; motion that runs straight through the peak reads as busy and swallows the moment.
This is a *stronger, intentional* version of the 100–200ms inter-beat hold above — reserve
the full 0.3–0.75s stillness for the one climax beat, not every seam.

## For our A→B model
A "beat" is usually one pair (frame A → frame B). Map the diff (§1 of `motion-principles.md`) onto
the phases: matched moves = the **action**; `exited` layers leave in **setup**; `entered` layers
arrive in **resolution**, staggered, after the matched layers land. Keep to one focal path per
pair; let the matched elements carry continuity so new elements are the only things entering.
