# Emotion and diagnosis

Companion to `motion-intent`. Everything in the emotion table is a **motion heuristic**: a trial
to render and judge, not a scene constraint. The diagnosis table lists hypotheses, not exclusive
causes. Change one variable at a time so the result can confirm or reject the hypothesis.

## Emotion → starting motion trials

| Requested feeling | Character to try | Path to try | Easing to try | Duration trial |
|---|---|---|---|---|
| joy, delight | one leader overshoots | curved or upward | shallow overshooting `cubic_bezier` | 0.3–0.5s |
| calm, trust | smooth and unhurried | gentle curve or no travel | `ease_in_out` | 0.8–1.6s |
| urgency | sharp and direct | straight | short `ease_out` | 0.15–0.3s |
| weight, gravity | slow and downward | drooping or settling | `ease_in_out` | 0.9–1.8s |
| impact, surprise | sudden expansion | radial outward | `ease_out`, possibly motion blur | 0.2–0.4s |
| elegance | controlled and minimal | long arc or restrained straight path | `ease_in_out`, usually no overshoot | 0.6–1.2s |
| confidence | decisive and stable | direct path with a clean stop | `ease_out` | 0.3–0.6s |
| playfulness | varied and bouncy | arcs or irregular stagger | overshooting `cubic_bezier` | 0.25–0.5s |

These associations are culturally and contextually dependent. Direction can support meaning, but it
does not own one universal meaning: upward may suggest growth or simply follow the layout; rightward
may suggest progress in one reading direction and not another. Test the scene's actual composition.

Colour and focus can carry a beat without spatial motion. `adjust` and `lut` effects can animate a
graded change; whether a success or alert colour should move is a project choice.

## Symptom → hypothesis → controlled test

Judge subjective symptoms from the beat in sequence. Layout queries and motion tracking can confirm
what changed; they cannot by themselves confirm how it feels.

| Symptom | Plausible hypothesis | First controlled test | Evidence to inspect |
|---|---|---|---|
| robotic, mechanical | unintended `linear` interpolation, one shared clock, or a path too rigid for the intended character | change only the leader's easing; if needed, test one timing offset next | same endpoints with a different midpoint; staggered channel start times |
| flat, cheap | hierarchy is unclear, or the primary gesture lacks contrast | reduce competing motion before adding another layer; then test one restrained reaction | fewer active channels; leader remains easiest to follow |
| noisy, unreadable | too many simultaneous changes or similar amplitudes | freeze nonessential motion for one preview | the message becomes readable earlier; intended leader remains dominant |
| slideshow, not a film | a shared element loses continuity across arrangements | keep one shared layer and animate its delta | the same layer remains visible across the handoff |
| sluggish | easing, duration, travel, or dead hold spends too much time | change easing only; then duration only if needed | identical endpoints arrive earlier, or static dead time disappears |
| jarring, unfinished | a cut interrupts motion, channels finish separately, or the beat needs stability | add a short trial hold or align channels, one test at a time | values remain stable before the cut; one event reads instead of two |
| dead air | the hold outlasts reading or anticipation | trim only the hold | comprehension remains while the edit gains pace |
| characterless | local choices do not form a consistent palette | write down the current durations/easings and normalize one repeated beat | repeated beats share an intentional pattern |
| two events where one was meant | fade and transform end at different times | make them co-terminous as a trial | they read as one arrival at full speed |
| glitchy bounce | overshoot is too large, too fast, or applied to too many elements | remove subordinate overshoot, then reduce the leader's rendered peak | the leader still has character without visible instability |

No row proves causation. If the first test does not change the symptom, restore it before testing the
next hypothesis.

## Character-specific failure modes

- **Calm / editorial** — may become imperceptible or too slow. Test whether another meaningful event
  completes inside a long move rather than adding motion everywhere.
- **Restrained / professional** — may become monotonous. Vary which property leads only when the
  communication job changes.
- **Playful** — may become uniformly bouncy. Try overshoot on the leader only.
- **Energetic** — may flatten hierarchy through maximum amplitude. Let each burst land or cut
  intentionally before another competes with it.

## Judging it

| Question | Cheapest useful evidence |
|---|---|
| Is timing what I authored? | `picsart_scene_query_layout` at start, decisive midpoint, landing and hold |
| Which channels compete? | Watch the beat in sequence; painted motion is not tracked automatically |
| Is the document valid? | `picsart_scene_validate` |
| Does motion read as intended? | Watch continuous exported video at viewing speed |
| Does the leader lead? | Compare timing, isolation, contrast and displacement; no single metric is sufficient |
| Is repeated viewing distracting? | Watch again in context and record the first distracting event; a fixed viewing count proves nothing |

For text, use ink ratio and centroid shift when those answer the question; mean pixel difference can
miss a localized text defect. These measurements establish visual change, not emotional quality.
