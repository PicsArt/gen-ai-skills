# Element motion — classify before you choose

Element *type* alone is not enough ("all buttons slide, all text fades" produces mush). Classify
each element on **five dimensions**, then pick motion. This is the layer between the frame diff
(§1 of [`motion-principles.md`](motion-principles.md) — *what changed*) and the purpose taxonomy
(§13 — *why*): here you decide *how strongly* and *which* preset, per element.

## The 5-dimension classification
| Dimension | Values | Controls |
|---|---|---|
| **Type** | text, button, image, icon, shape, group | the basic motion vocabulary |
| **Role** | headline, body, CTA, product, badge, nav, decoration | what the element is doing |
| **Importance** | primary, secondary, tertiary | motion **intensity/distinctiveness** |
| **Behavior** | enter, exit, emphasize, transition, ambient | the **job** of the motion |
| **Context** | hero, card, repeated list, background, foreground, grouped | **sequencing, grouping, spatial logic** |

## Two rules that govern intensity
- **Importance → distinctiveness.** The more important the element, the more distinctive its motion may be (a hero headline/CTA earns expressive timing; a tertiary badge stays quiet).
- **Information density → simplicity.** The more information an element carries, the *simpler* its motion. (Hence the text-length rule below.)

All preset names below are intents — **resolve to real mp-scene ids via `get_capabilities`** (see [`mp-scene-vocabulary.md`](mp-scene-vocabulary.md)); the mappings in *italics* show the real target.

## Buttons — controlled, direct, readable
| Situation | Motion | Avoid |
|---|---|---|
| CTA entering | fade + rise, optional scale 0.96→1 *(`slide_in` up + `scale_pop`)* | spin, large travel, constant bounce |
| Primary CTA emphasis | small pop *(`scale_pop`)* | high-frequency pulsing |
| Click/tap feedback | scale down→up *(tap-dot + `scale_pop`)* | moving the whole button away |
| Becomes available | fade/scale in | dramatic entrance |
| Success | check draw + color + subtle pop | unrelated motion |

Primary CTAs may get slightly more distinctive motion; secondary buttons stay quieter.

## Text — readability first; shorter + more important = more expressive
| Length | Intensity |
|---|---|
| 1–4 words | expressive allowed *(`typewriter`, word `slide_up_lines`, `scale_pop`)* |
| 5–15 words | moderate *(fade + 8px rise)* |
| paragraph | minimal *(`fade_in`)* |

- **Headlines:** line/mask reveal, rise, word-stagger *(`reveal_in`, `slide_up_lines`)* — attention anchors, can carry expressive timing.
- **Body:** `fade_in` or fade + ~8px rise; rarely rotate/bounce/scale.
- **Emphasized word** (distinct weight/color/size): treat as a semantic target — keyword pop / highlight sweep *(`scale_pop` on the run, or a `shimmer` sweep)*.

## Images & product
| Role | Motion |
|---|---|
| background | slow zoom / parallax / drift *(`ken_burns`, `float`; parallax = author-managed)* |
| hero / product | scale + translate + slight rotation *(`ken_burns` / `scale_pop`)* |
| gallery | stagger / horizontal slide *(`slide_in` + stagger)* |
| before / after | wipe or slider reveal *(`reveal_in` / a wipe transition)* |
| image in a card | **moves with the card as one unit** |

A product image tolerates more spatial motion than text — it's an object to observe, not text to read.

## Icons — semantic motion (reinforce meaning)
| Icon | Motion | mp-scene |
|---|---|---|
| arrow | translate / draw | `slide_in` / shape **trim** |
| check | draw or pop | shape **trim** / `scale_pop` |
| plus | rotate | `rotation` keyframes |
| heart | scale / pulse | `scale_pop` / `glow_pulse` |
| bell | small ring/shake | `shake` |
| play / search / sparkle | scale / rotate | `scale_pop` / `rotation` |
| chevron | translate **in its pointing direction** | `slide_in` (dir from the icon) |

## Decorative — support, never compete
Ambient only: float / drift / slow-rotate / parallax / breathe *(`float`, `sway`, `breathe`)*.
**Intensity hierarchy:** background = very slow · decorations = slow · product = medium · headline & CTA = intentional/focused.

## A rule-based scoring sketch
Derive a semantic record per element → map to a treatment (rule-based first, AI/learned later):
- Text / Headline / Primary / Enter / Hero → **mask-rise** *(`reveal_in` + rise)*
- Text / Body / Secondary / Enter / Hero → **fade-rise-subtle**
- Button / CTA / Primary / Enter / Hero → **cta-rise** *(`slide_in` up + `scale_pop`)*
- Image / Product / Primary / Enter / Hero → **product-pop-in** *(`scale_pop` / `ken_burns`)*
- Shape / Decoration / Tertiary / Ambient / Background → **slow-drift** *(`float`)*
