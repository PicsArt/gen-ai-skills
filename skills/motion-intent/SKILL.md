---
name: motion-intent
description: Choose and diagnose scene motion from communication intent before selecting presets or keyframes. Use when a user says “make this motion feel…”, asks to choreograph a scene, choose timing/easing/stagger, establish motion hierarchy, or explain why an animation feels flat, noisy, robotic, sluggish, or unfinished.
metadata:
  category: authoring
  version: '1.2'
  ported-from: motion-intent 1.2 at 55.75.0
user-invocable: false
---

# Motion by intent

Choose motion from communication intent before choosing presets or keyframes. Motion spends
attention; an element should move because the beat needs it, not merely because it can.

This recipe uses three evidence labels:

- **scene fact** — behavior defined by the format, validator, resolver, or authoring tools.
- **Motion heuristic** — a useful starting rule that must be judged in the actual scene.
- **Project choice** — a local style decision that should stay consistent inside one piece.

Do not present a heuristic or project choice as something scene enforces. Exact starting values
below are trials, not universal constants.

## Decide in this order

1. **Communication goal** — what must the viewer understand or notice?
2. **Visual leader** — which one element owns the beat, and what stays subordinate?
3. **Spatial relationship** — reveal, replace, connect, emphasize, orient, or resolve.
4. **Timing and sequence** — what precedes, overlaps, follows, and holds?
5. **Motion character** — direct, soft, restrained, playful, urgent, or continuous.
6. **Settle and readable hold** — what must become still, and for how long?
7. **Evaluation** — did the result communicate the original goal without added competition?

Only after these decisions should an author choose scene properties, presets, or keyframes.
Concrete syntax is `picsart_scene_recipe scene-animation-reference`; reusable realizations are
`picsart_scene_recipe motion-pattern-library`. When the question spans consecutive beats or a scene boundary,
route the relationship and seam decision to `picsart_scene_recipe motion-scene-continuity`.

## 1. Communication goal

| Goal | Communication job | Possible scene realization |
|---|---|---|
| **Reveal** | introduce content | an entrance preset, text animation, or explicit opacity/transform track |
| **Conceal** | remove content | an exit preset or explicit opacity/transform track |
| **Replace** | make one state become another | keep shared layers continuous; remove and introduce only what changes |
| **Connect** | show a relationship or journey | position path, parenting, anchor and rotation, or a drawn path |
| **Emphasize** | redirect attention mid-beat | a restrained scale, position, rotation, focus, or colour change |
| **Orient** | communicate direction, order, or progress | coordinated position tracks or a catalog transition such as `slide`, `diagonal_slide` or `page_curl` |
| **Resolve** | show that an action reached its intended result | return to rest, reduce amplitude, then hold if comprehension needs it |
| **Atmosphere** | keep an otherwise static interval alive | low-amplitude continuous motion that never becomes the leader |

**Motion heuristic:** one verb is usually enough for one beat. If the goal needs “reveal, emphasize,
spin, and celebrate,” split it into beats or choose the one communication job that matters.

## 2. Visual leader

Name the leader before assigning motion. Supporting elements may prepare for it, follow it, or remain
still. A useful hierarchy trial is:

| Role | Starting treatment |
|---|---|
| leader | largest or clearest change in the beat |
| support | smaller change, later start, or fewer animated properties |
| ambient | slow, low-amplitude continuity, or no motion |

These are **motion heuristics**, not amplitude requirements. A leader can also win through isolation,
contrast, or timing while moving less than its support.

For repeated items, decide whether the group is one idea or a reading order. Move the group together
for one idea; stagger its children when order itself communicates something.

## 3. Spatial relationship and property

**scene fact:** layer Placement can animate `position`, `scale`, `rotation`, `opacity`, and
`anchor`; audio can animate `volume`. Transform components add independently editable motion outside
Placement. Exact catalogs and content-kind restrictions live in `scene-animation-reference`.

Choose the minimum property set that carries the relationship:

| Property | Often communicates | Context warning |
|---|---|---|
| `position` | arrival, departure, direction, relationship | direction has cultural and layout context; right is not universally “progress” |
| `scale` | importance, proximity, emergence | large deltas can feel like a camera move or a toy-like bounce |
| `rotation` | redirection, process, instability | continuous rotation implies an ongoing state rather than a resolved beat |
| `opacity` | presence or continuity | opacity alone may be exactly right for a quiet reveal; pair it only when another property adds meaning |
| `anchor` | the point a scale or rotation acts around | animate it only when changing the pivot is itself useful |

**Motion heuristic:** one or two coordinated properties are easier to read than several unrelated
ones. When opacity and a transform describe one arrival, try ending them together first; offset them
only for a deliberate two-stage read.

### Shared-element continuity

For an element that exists in consecutive arrangements, first try keeping one layer on screen and
animating its delta. This often reads as continuity better than cross-fading two copies. A cross-fade
remains valid when identity is intentionally ambiguous, continuity is unimportant, or the states
cannot share one authored layer.

## 4. Timing and sequence

scene defines time values; it does not define an ideal pace. These are for ambient or emotional
pacing; a UI element move (a button, a card, a list row) stays at motion-design-craft's 200–400 ms. Build a small **project-choice**
palette from the brief, then test it in context. These are example starting palettes:

| Character | quick | standard | slow | Overshoot trial |
|---|---:|---:|---:|---:|
| calm / editorial | 0.5s | 0.8s | 1.6s | none |
| restrained / professional | 0.3s | 0.5s | 0.9s | none to about 3% |
| playful | 0.25s | 0.4s | 0.7s | about 10–20% on the leader only |
| energetic | 0.15s | 0.3s | 0.5s | about 15–30% when readability survives |

The names and values above are not format registers. Replace them when the project's pacing,
frame rate, travel, density, or audience calls for something else.

Useful **heuristic trials**:

- Longer travel often needs more time; preview rather than applying a fixed distance multiplier.
- Try exits shorter than entrances when removal should spend less attention, but keep them long
  enough to remain legible.
- For siblings, start with roughly `0.05–0.12s` between items and keep the whole cascade compact;
  compress or expand it to match density and reading order.
- Very short spatial moves can read as pops at common video frame rates. Around `0.15s` is a useful
  warning threshold, not a minimum enforced by scene.
- A hold should cover comprehension or reading, not satisfy a fixed ratio to motion duration.

Write the chosen palette beside the scene as a project decision. Consistent values can create a
register, but variation is justified when distance, hierarchy, or meaning changes.

## 5. Motion character and easing

**scene fact:** if an animatable keyframe segment omits easing, interpolation is linear. State
easing explicitly whenever constant-rate motion is not intended.

**Motion heuristic:** purpose and continuity choose easing; direction is only a starting clue.

| Desired read | First easing to try | Legitimate exception |
|---|---|---|
| arrive and settle | `ease_out` | `linear` for mechanical or intentionally constant motion |
| leave and accelerate | `ease_in` | `ease_out` for a release that starts abruptly and softens |
| reposition while remaining visible | `ease_in_out` | `linear` for a camera glide, progress, or conveyor-like motion |
| switch instantly | `step` | use a short eased change when continuity matters |

Overshoot is a design choice, not a separate scene semantic. Start with none, add it only to the
leader when the requested character needs it, and judge the rendered peak rather than equating a
Bézier control ordinate with an overshoot percentage. A single overshoot and a damped multi-cycle
spring communicate different things; patterns for both are in `motion-pattern-library`.

## 6. Settle and readable hold

Anticipation, action, reaction, and resolution are optional choreography tools—not mandatory phases.
A practical sequence is:

1. anticipate only when it clarifies a strong directional action;
2. perform the action;
3. let a subordinate react only if the reaction adds meaning;
4. resolve or intentionally cut away;
5. hold only as long as recognition or reading needs.

Starting with `0.1–0.2s` of stability can reveal whether a beat felt unfinished, but the correct hold
depends on frame rate, edit rhythm, and content. A hard cut at the action endpoint can also be the
intended punctuation.

## 7. Evaluate against the goal

Treat perceptual diagnoses as hypotheses and change one variable at a time.

| Question | Evidence available here |
|---|---|
| Did geometry and opacity follow the intended beat? | `picsart_scene_query_layout` at events, extrema and through the hold, compared with independent expected values |
| Did supported relationships hold at the samples? | `picsart_scene_lint_layout` with scoped targets, explicit windows and supported relationships; inspect every verdict |
| Did painted objects move as intended? | Inspect continuous exported video; painted motion is not tracked automatically (`picsart_scene_check_motion` covers evaluated geometry) |
| Is the document structurally valid? | `picsart_scene_validate` after edits |
| Does the beat read at viewing speed? | Watch it in sequence; unexecuted numerical checks remain unchecked |

Layout and validation can prove authored structure; they cannot prove that motion feels confident,
playful, elegant, or restrained. Those remain contextual judgments.

Before authoring, write a short acceptance card: **goal, target IDs/scopes, root-clock events,
expected outcome, tolerance, sample schedule, numerical check, visual check**. Pick the matching
pattern from `picsart_scene_recipe motion-pattern-library` and fetch its **Validation by pattern** reference;
it maps each construction to existing tools
and states what they cannot establish. Set targets from the design, not from the output being tested.
After execution, record measured / visually inspected / unchecked evidence separately. Fix a failed
beat and rerun its window and adjacent seams; do not widen tolerances merely to obtain a pass.

## Before calling a beat done

- [ ] The communication goal is one sentence, not an effect name.
- [ ] One leader is named; support and ambient motion are intentional, including intentional stillness.
- [ ] The property choice communicates the relationship.
- [ ] Numerical values are identified as project choices or heuristic trials unless the format defines them.
- [ ] Easing is explicit unless constant-rate motion is intended.
- [ ] The beat resolves or cuts intentionally, with enough reading time for its content.
- [ ] Validation/layout evidence does not prove a subjective feeling; describe the actual visual observation separately.
- [ ] The selected pattern's numerical and visual checks ran, or the missing evidence is explicitly listed.

Emotion-to-motion starting points and symptom diagnosis are in
[references/emotion-and-diagnosis.md](references/emotion-and-diagnosis.md).

---

The existing goal/register/emotion framing was adapted for video from LottieFiles' `motion-design`
skill (MIT © 2025 LottieFiles) and re-derived in scene vocabulary; that attribution remains for
the material already derived from it.

**Research note:** the evidence-boundary and choreography guidance added here is independently
authored for scene from general motion-design principles and local evaluation. Hyperframes was
reviewed as research inspiration; its wording, code, examples, and organization were not adopted.
