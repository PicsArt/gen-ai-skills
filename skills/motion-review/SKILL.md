---
name: motion-review
description: Review an existing scene for motion that is confusing, mistimed, distracting, broken at a seam, or unnecessarily expensive. Use when asked to critique or improve a finished animation, audit a multi-beat scene, prioritize motion fixes, or decide whether a static element should move, and before reporting that your own render, character, rig or acceptance video works.
metadata:
  category: workflow
  version: '1.0'
  ported-from: motion-review 1.0 at 55.128.2
user-invocable: false
---

# Review motion in an existing scene

Review the authored scene and the moving picture together. A valid document and a good still frame
cannot establish that a beat reads correctly in sequence. Find the few changes that would most
improve comprehension, then verify each change in the interval where it matters.

This recipe reviews an existing document. For a new beat, start with motion-intent (fetch with
`picsart_scene_recipe`, name `motion-intent`). For scene syntax and worked constructions, use
scene-animation-reference and motion-pattern-library, fetched the same way.

## Establish what the scene is trying to say

Read the brief, storyboard, reference, or editor notes when supplied. Without one, describe the
apparent message as an **inference** and avoid treating your preferred style as the intended one.

Make a short timeline map from the scene itself: composition duration and frame rate, layer
windows, track clips and transitions, motion tracks, looks, text animations, and nested
`scene_ref` content. Use `picsart_scene_inspect` for a large document; it shows authored values
and addresses, not evaluated root-time positions. Identify each visible beat's leader, the change
it should communicate, and the interval in which that change must be read. Mark every seam and
every long hold for closer inspection.

**Do not add motion simply because a layer is static.** Stillness may support reading, contrast, or
an intentional reset. A proposed addition needs a communication job and a viewer-visible change it
would clarify. Reject it when it only repeats another layer's gesture or competes with the leader.

## Gather evidence at the right scale

1. Run `picsart_scene_validate` on the document under review. Repair an invalid scene before
   judging subtle timing. A successful validation proves the document's contract, not the rendered
   beat.
2. Use `picsart_scene_query_layout` at the start, interior, landing, and hold of each suspect
   motion. Query both sides of a seam. Map nested or layer-local clocks to root time before
   comparing values. If there is an explicit geometric expectation, use
   `picsart_scene_check_contracts` over its intended window, and `picsart_scene_check_motion` for
   frame-complete motion expectations.
3. Use `picsart_scene_contact_sheet` with explicit `times` for decisive frames, including an
   interior frame rather than endpoints alone. Inspect pixels for visibility, crop, blur, text
   readability, and overlapping attention.
4. Watch the **continuous rendered interval** at its intended viewing speed when the issue is
   pacing, acceleration, causality, or a seam. Stills can suggest where to look but cannot settle
   those questions. If only stills are available, mark the temporal judgment unverified.

For reference matching, compare the reference and candidate over the same window using
`picsart_media_track_motion_diff`, `picsart_media_flow_diff`, or `picsart_media_inventory_diff` as
appropriate. These answer different questions: trajectory, flow, or visible inventory. None
judges whether an original motion choice is expressive.

## Diagnose before changing a value

Name the observed failure in scene terms, then identify the smallest responsible span or layer.

| Observation | First thing to inspect | Next decision |
|---|---|---|
| The viewer cannot tell what changed | leader, contrast, arrival order, hold | remove competing motion or reveal the needed result more clearly |
| A move feels abrupt or drifts after landing | interior pose, easing, expression tail, layer clock | correct its progress or settle at the intended root time |
| A button or pointer action feels disconnected | pointer arrival, response start, result start | align the causal event and inspect the full widget, not one child |
| The seam feels like a new slide | carrier identity, direction, overlapping windows, transition source frames | choose continuation, replacement, or an intentional reset before choosing a transition |
| Motion stutters or misses frame budget | active video count, effect area, blur, live layer windows | reduce the heaviest live layers in that window and re-check the target's playback |
| A static interval seems dead | reading demand, next action, intended pause | shorten the hold or add one purposeful change; a pause may be correct |

These are hypotheses, not automatic fixes. Check the relevant recipe before changing a
representation (fetch with `picsart_scene_recipe`): app-ui-animation for a simulated interaction,
motion-scene-continuity for a seam, linked-element-motion for reflow. A preset cannot repair a
wrong semantic relationship or an incorrect layer lifetime.

## Choose the next fix

Rank findings by the viewer's likely misunderstanding, how much of the scene they affect, and the
confidence of the evidence. Resolve structural failures and missing or incorrect content first,
then causality and continuity, then timing and emphasis, then polish. When two changes could
explain the same symptom, try the smaller one and re-render its window before adding more.

For each proposed change, record:

- the layer or scoped target and root-time window;
- the intended viewer-visible result;
- the current observation and its evidence source;
- one concrete edit to test, including removing motion when it has no job;
- a numeric check where a numeric expectation exists, plus the interval to watch.

Avoid universal timing verdicts. A 0.2-second gesture can be a clear UI tap and an unreadable
title entrance, depending on frame rate, travel, density, and context. Treat timing tables as
starting trials. A rendered scene must be judged at its delivery frame rate and viewing size.

After an edit, validate again, recheck its entire beat, and inspect the neighboring seams. A
successful midpoint frame does not prove the entrance, landing, or exit. When the deliverable has
multiple output targets, verify the affected interval on each; report a target's translation
diagnostic instead of assuming equivalent output.

## Report a review

Lead with the highest-impact confirmed issue, or say that none was found. For each finding give a
scene location, root-time interval, what the viewer sees, the evidence, and the proposed edit.
Separate **measured**, **visually inspected**, and **not yet verified** claims. List rejected
motion additions when the user asked where to animate, so stillness is an explicit design choice.
Keep a short ordered set of actionable changes; do not manufacture polish findings to fill a list.

## Accept your own render before reporting it

Apply this before you call any rendered scene, character, rig or acceptance video "working". The
author of a render tends to confirm it; look for the ways it fails.

1. **Name the intended action in one sentence** ("both hands hold the ball at chest height"). Judge
   the picture against that sentence, not against your previous draft or a metric.
2. **Lint the shot's window before you show it** (`picsart_scene_lint_layout`; allow a pair meant to touch). The
   hosted lint reads layer geometry, not painted pixels: it warns on figures whose bounds overlap, on a figure
   the frame cuts, and on a layer standing farther back painted over a nearer one (`groundPaintOrder`). It cannot see a prop its own body hides or a speaking mouth under its own arm or hand; look for
   those on the contact sheet yourself, along with a prop away from its hand, a figure or key layer the frame mostly
   misses, and frames that draw nothing but the background. A warning is a defect you found before the viewer: fix it, or allow it
   knowing why.
3. **Read each line's action against its words.** For every spoken line, set the text beside the action keyed over
   it: a line that says "look" or "wave" plays that, not `idle` or `talk`. Nothing checks it.
4. **Look at the whole window.** Make a contact sheet of at least 8 frames spread across the clip,
   including interior frames (`picsart_scene_contact_sheet` for a scene, `picsart_media_video_stills` for a video), and
   open it yourself. One still or the endpoints hide mid-motion tears, drift and pops. For sync between
   two things (mouth and voice, hand and prop), track both per frame (`picsart_media_track_motion`); stills hid a mouth
   drift that per-frame tracking caught.
5. **Check what the viewer sees, not what you built.** A metric on the mechanism can pass while the
   picture is wrong: a grip socket landed within 0.55 px of the ball while the drawn hand stopped a
   hand-width short. Check the drawn result: contact between silhouettes, limbs bending the
   anatomical way, nothing passing through a body or prop, near and far parts in the right draw
   order, garments following the body without tears or flares. A mean pixel diff cannot see text
   or small parts.
6. **List defects first**, each with the frame or time where it shows, then what works. One passing
   gate is not success. A first iteration may carry minor labelled defects but no bad mistake: a
   broken anatomy, a missed contact or a stated rule broken blocks it.
7. **Deliver the moving result.** Send the labelled final video for motion, not a sheet of
   measurements; the sheet is your evidence, the video is the deliverable.

When the work matters (a change others will build on, a result shared with others), have someone other than the author
review it with fresh eyes, applying this section.
