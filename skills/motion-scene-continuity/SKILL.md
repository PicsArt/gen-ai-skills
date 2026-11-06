---
name: motion-scene-continuity
description: Plan and diagnose continuity across scene beats and scene boundaries—semantic handoffs, dominant direction, shared visual carriers, causal action/reaction, intentional resets, and seam verification. Use when consecutive scenes feel like separate slides, a transition breaks momentum, a shared element must persist, or a multi-scene sequence needs a continuity review.
metadata:
  category: authoring
  version: '1.1'
  ported-from: motion-continuity 1.1 at 55.75.0
user-invocable: false
---

# Motion across beats and seams

Served checks: `picsart_scene_check_contracts` runs contract records and reusable templates, `picsart_scene_check_motion` runs frame-complete motion records, and `picsart_scene_inspect` pages large sources; the one remaining limit is that pixel records have no automated checker, so inspect full-resolution rendered frames for them.

This skill owns the relationship between consecutive beats or scenes. Use
`motion-intent` for the purpose and hierarchy inside one beat,
`scene-animation-reference` after the motion is decided and needs scene syntax, and
`custom-transitions` only when the current transition catalog cannot express an already-decided
seam.

Keep three kinds of statement separate:

- **scene fact** — behavior defined by the format, validator, resolver, or authoring tools.
- **Motion heuristic** — a useful continuity trial that must be judged in the actual sequence.
- **Project choice** — a local editorial or brand decision.

Direction, velocity matching, overlap, and holds are motion heuristics, not rules enforced by the scene format. A hard cut, crossfade, direction change, or moment of stillness can be exactly right when the
communication calls for interruption, ambiguity, atmosphere, punctuation, or a chapter reset.

## Decide each boundary in this order

### 1. Name the semantic relationship

Choose the verb before the mechanism:

| Relationship | What the viewer should understand |
|---|---|
| continuation | this is the same action, object, or journey carrying on |
| replacement | one state gives way to another |
| reveal | the previous beat causes or exposes new information |
| arrival | a subject or destination has been reached |
| interruption | a new event deliberately breaks the previous flow |
| reset | a chapter or idea has ended and a new one begins |

If the relationship is unclear, a transition name will not make it clear. State the intended
relationship in one sentence first.

### 2. Choose a contextual vector

For continuation, first try carrying the dominant travel direction or the apparent momentum through
the seam. For arrival or reset, reducing motion or changing direction may communicate the meaning
better. Reading direction, subject movement, layout, and camera logic all affect the choice; there is
no universal rule that right means progress or that matched velocity is always desirable.

Record the trial as a project decision, for example: “The card continues upward because the next
arrangement reveals content below it.” Do not describe the decision as a scene requirement.

### 3. Choose the representation

Use the smallest scene structure that preserves the intended relationship:

| Need | First scene representation |
|---|---|
| same object, new arrangement | keep one layer alive; animate its placement delta |
| whole-frame directional handoff | track transition from the current transition catalog |
| unsupported seam mechanism | custom transition definition, routed to `custom-transitions` |
| deliberate discontinuity | adjacent track clips with no transition |
| ambiguous/quiet replacement | crossfade when identity continuity is not the message |

**scene fact:** a track transition resolves the outgoing last frame and incoming first frame into
the transition's source and destination slots. It does not preserve arbitrary live animation from
the neighboring clips through the transition window. If live identity matters, prefer one persistent
layer or author the motion inside a composition that remains alive.

Two copies of an apparently shared element can be appropriate when they are not semantically the
same object, or when independent content constraints prevent one layer from spanning the interval.
Do not duplicate only to avoid planning the layer lifetime.

Two areas of one set need no cut. Lay them out in one timeline and travel the composition camera
between them: the next subject stands off-frame by construction (check every earlier frame), keeps
an idle while unseen, and is revealed by the move, with its first line landing as the camera settles.
A pull-back to a wide two-shot lets one character's reaction read during the other's line.

Only hand a custom transition to `custom-transitions` after the semantic relationship, vector
or reset, and any visual carrier are decided and the shipped catalog has been checked. The custom
definition must then pass its own full-window five-sample gate. Claims of duration independence need
two materially different durations; claims of aspect independence need 16:9 and 9:16 evidence.

### 4. Identify the visual carrier

Name the thing the eye can follow: a persistent card, edge, colour field, line, subject, or directional
flow. A carrier is optional. A deliberate reset may work because nothing crosses it.

When a carrier exists:

- keep its identity, trajectory, or visual role legible across the boundary;
- keep subordinate motion from becoming a second competing handoff;
- avoid making the carrier re-enter as if it were new unless that repetition is meaningful.

### 5. Align cause and reaction

When one action is meant to cause another, give them one authored event time. The action can prepare
before the event and each response can settle on its own schedule, but the first visible press,
response, and reveal should share the causal boundary unless the interface or story intentionally
models latency.

This is a motion heuristic. scene permits any keyframe times; causality is the author's
communication decision.

### 6. Plan stillness and readability

Stillness is part of continuity. Hold long enough for recognition, reading, or contrast with the
next action. Remove a dead gap that communicates nothing, but keep a quiet interval that lets the
sequence land. Do not use a fixed hold ratio as if it were a format constraint.

### 7. Audit the whole sequence

Review the connected sequence, not isolated clips:

- Does a direction reverse accidentally, or does the reversal communicate interruption or return?
- Does a carrier duplicate, disappear, or re-enter without explanation?
- Does a beat start before the previous leader has released attention?
- Is there a dead gap, or an intentional readable hold?
- Is one causal action followed by a visible reaction?
- Does the sequence settle or cut intentionally instead of merely running out of keyframes?

Change one variable at a time when diagnosing a seam. A smoother curve cannot repair a wrong
semantic relationship, and a more elaborate transition cannot repair duplicated identity.

## Evidence gate

### Check an explicit geometry handoff

When two authored roles should occupy the same box on opposite sides of a seam, save a named
`handoff` assertion in the contract sidecar. Unlike same-frame companion checks, it compares each
role at its own root-time moment. This complete example needs query targets `out` and `in`:

```json
{
  "version": 1,
  "timeSpace": "root",
  "contracts": [{
    "id": "card-seam",
    "description": "Incoming card occupies the outgoing card's last intended box.",
    "moments": { "outgoing": 1.99, "incoming": 2 },
    "assert": { "kind": "handoff", "outgoing": { "id": "out" }, "incoming": { "id": "in" }, "tolerancePx": 1 }
  }]
}
```

Check it as a `handoff` contract with `picsart_scene_check_contracts`, with explicit outgoing and incoming `moments`, or use `picsart_scene_query_layout` separately at those moments and compare each box edge with the independent design requirement. An outgoing layer ending at 2 seconds is not alive at exactly 2: choose its intended last visible frame, not an arbitrary epsilon. A moving last frame differs from an extrapolated endpoint. Use actual query composition scopes to disambiguate repeated ids; a handoff verdict covers only those two moments.

Read the named status and `handoff.outgoing` / `handoff.incoming`: both timestamped observations
are returned even on a pass. `maxErrorPx` is the largest absolute left/top/right/bottom edge
difference in root pixels. Thus same-center size jumps fail too. Both boxes must be usable,
on-canvas and unrotated; missing/ambiguous/rotated/unavailable geometry is inconclusive, while a
known absent role fails. One `checkedSamples` means one compared pair, not an inspected interval.

Use this only when geometry equality is the intended design. Intentional morphing, directional
travel or a chapter reset need not match boxes. Matching geometry does not establish semantic
identity, paint visibility, velocity or absence of a gap between the moments. For interval
coverage, add appropriate presence checks and inspect the rendered seam. A persistent layer can
be compared at distinct moments; comparing the same resolved target to itself at one moment is
not a meaningful handoff. `picsart_scene_diff_layouts` remains useful for exploratory deltas, but its
classification (for example `restyled`) is not a named design-contract verdict.

How it pairs layers, each pair's `matchedBy`: explicit `matchHints` first (`hint`); then the same
content id and kind, the same asset or text (`content`); then the same layer id and kind however far
it moved, a child by its own id under parents already paired, unless its content id differs (`id`);
then geometry, best IoU or nearest centre (`geometry`). An `internal` layer pairs only with an
`internal` one. Deltas are centre-based. It does not compare numeric opacity: `restyled` is a change
of visibility, rotation or paint order. Text boxes are font-metric envelopes, not glyph bounds, so
text deltas are approximate; boards whose comparable layers do not pair report `unrelated`.

The tolerance is for **edges**, not independent center/width/height tolerances: a centered width
change of 2 px moves each edge by 1 px and can pass `tolerancePx:1`. If the design specifies separate
dimension tolerances, report that unsupported intent rather than claiming this check is equivalent.
In each role observation, `available` means the query sample exists; use `matches` and the named
status to establish whether the target resolved. `available:true` with `matches:0` is not a match.

### Choose evidence for the claim

Use evidence appropriate to the claim:

1. Validate structure with `picsart_scene_validate`.
2. Query before, exactly at and after the seam. Use `picsart_scene_lint_layout` for supported presence, companion translation, containment and equal-opacity relationships in declared windows. Inspect every relationship result, even if collision findings are empty. Geometric presence does not prove paint visibility; equal evaluated opacity does not prove identity or absence of occlusion. Intentional crossfades need not match opacity. Run the same relationships as a contract record with `picsart_scene_check_contracts` when they must be replayed; retain unsupported comparisons as unchecked.
3. Inspect full-resolution `picsart_scene_contact_sheet` images of approach, seam and settled tail; set `resolution` to the scene dimensions and use at most 8 times per call.
4. Watch continuous exported video for perceived direction, velocity, causality and continuity. See `linked-element-motion` for shared ownership, resize and containment.

Validation and layout prove structure and geometry. They do not prove that a seam feels smooth,
decisive, playful, or restrained. Those remain contextual visual judgments. Record the scene,
times, and inspected artifact so a tested construction is not mistaken for universal motion law.

## Hand off to the neighboring skills

- For one beat's communication goal, leader, character, and diagnosis, use
  motion-intent (fetch with `picsart_scene_recipe`, name `motion-intent`).
- For transforms, tracks, easing, expressions, blur, and transition placement, use
  scene-animation-reference (fetch with `picsart_scene_recipe`, name `scene-animation-reference`).
- For compact, reusable constructions, use
  motion-pattern-library (fetch with `picsart_scene_recipe`, name `motion-pattern-library`).
- For a new transition definition after the relationship is decided and the catalog has been ruled
  out, use
  custom-transitions (fetch with `picsart_scene_recipe`, name `custom-transitions`).
- When velocity, path or overlap requires measurement, record the actual evidence available. `picsart_scene_check_motion` measures evaluated geometry per output frame, but painted motion in exported video is not tracked automatically; measurement informs the continuity decision but does not make it.

---

**Research note:** this guidance was independently authored for scene from general motion-design
principles and local evaluation. Hyperframes was reviewed as research inspiration; its wording,
code, examples, values, and organization were not adopted.
