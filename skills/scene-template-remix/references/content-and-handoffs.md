# Replace content and join an outside object to a template

Use this when an editable starter is useful but its artwork must change, or an object must travel
into a nested template. Keep the template's behavior; replace only the content or relationship
the brief calls for. No new scene fields or universal clip parameter are implied by this workflow.

## Replace the content, preserve the semantic container

Describe the template's actual parameter types first. A list of labels is not a list of clips.
Use supported parameters for ordinary edits; bootstrap/inline an expand-only starter, or expand
the intended reusable instance before structural edits. Inspect the result and patch returned
addresses, keeping an original revision.
A clip shorthand `{ assetId, duration }` takes its kind from the asset's `type`: a `scene` asset binds
a `scene_ref` clip, any other a `media` clip.

Identify the item owner, replaceable content, selection/decoration, and their geometry driver.
Put new media inside the existing item container while retaining its bounds, placement and clock.
Remove or replace the unwanted label/plate so it cannot cover the media. Probe the asset, choose
explicit fit/crop and preserve source aspect unless distortion is intended. For video also decide
trim, playback timing, short-source behavior and audio; an image substitution does not decide them.
Use the current schema and `scene-video-edits` for media syntax and supported timing.

In `marquee-selection-grid`, labels are the supplied inputs; arbitrary clips are not parameters.
Replace the chosen tile's internals, not the whole board or pointer rig. Its current selection
overlay is a sibling with matching parameter-derived geometry, not a follower of arbitrary tile
edits. Replacing internals preserves that geometry. Moving/resizing the tile itself requires
updating that relationship or introducing shared ownership, then checking selection again.
Selection refers to the rectangular tile region, not the photo's or video's visible silhouette.

For a new starter, content and its outline should share one item owner and sizing source where
the intended relationship is permanent. Do not require a new generic input API merely to support
an occasional structural customization.

## Measure the destination before constructing the approach

1. Name the join event in **root seconds** and the intended relation: identical box, center
   coincidence, edge/inset, or containment. Decide whether it holds only at arrival or afterwards.
2. Query the **assembled host**, not the standalone template, with
   `picsart_scene_query_layout({scene, time: join})`. Resolve the destination using returned ids and
   composition scopes. Also query approach, arrival and post-arrival times that matter to the
   motion. A layer not yet created need not be queried: measure the existing destination first,
   then construct the source to reach it. Conversely, an existing source can anchor a new destination.
3. Record the chosen reference, scene revision, time, box/center and intended offset. Root-space
   query geometry is not the layer's authored `transform.position`. Account for its anchor,
   enclosing placement, scale/rotation and fitting before writing parent-local coordinates.
   A root-level, center-anchored source can use the queried destination center directly; a nested
   source requires conversion into its own parent space. Do not paste root coordinates into it.
4. Map root event time to the edited layer's clock. A template delayed by 1s with unchanged speed
   reaches root 3s at local 2s; spatial scale 0.5 does **not** halve time. A source with its own start
   needs its own mapping. Trims, playback speed and nested clocks require the actual mapping from
   `scene-animation-reference`, not subtracting one start unconditionally.
5. Author the approach and re-query after assembly. Recompute when destination layout, media fit,
   owner transform or timing changes. A query is a measurement of one revision at one time, not
   a persistent binding or an automatic layout constraint.

For illustration, a measured destination box `(x=450,y=240,width=100,height=60)` has center
`(500,270)`. A center-anchored root source can arrive there with drawn size `100×60`; this does
not prescribe its source resolution, crop, or nested local placement. These numbers illustrate
the conversion, not a catalog default or measured benchmark.

## Decide what owns the object after arrival

- **Continuous relationship:** prefer one owner with child-local motion. If an object must first
  travel outside that owner's bounds, check for clipping before choosing this construction.
  Use supported one-way property binding only in compatible coordinate/clock scopes; a sibling
  Placement read is not a universal root-space lookup by flattened query id.
- **Intentional representation swap:** a root flyer may give way to content already inside the
  destination owner. Match geometry, crop/content and relevant visual state at the seam; author
  visibility/lifetimes so it neither doubles nor disappears. This is a substitution, not dynamic
  reparenting. Use it when retaining one live layer is impractical, not as the default for every join.
- **Independent motion after a momentary join:** retain separate owners and scope equality to the
  event. Do not force matching tracks through a phase that intentionally separates them.

`parentId` is not an animated reparent switch and does not inherit opacity/lifetime. A snapshot
endpoint at arrival cannot keep following a destination that continues moving. Fetch
`linked-element-motion` and `scene-animation-reference` for construction details.

## Validate the relationship, not a copied baseline

Run `picsart_scene_validate`, then query both actual targets in the assembled host. Measuring the
destination to construct an arrival is legitimate; validating only the source against its own
read-back position is not. Keep the intended relation and tolerance fixed, and compare source and
destination. Separately check that the destination itself satisfies any required host layout.

- **Same-time identical boxes:** `handoff` can use equal outgoing/incoming `moments` for two
  distinct live targets. It compares all four root-space box edges, not just position. For only
  center or one-edge alignment, use the appropriate comparisons described in the UI alignment
  reference of `linked-element-motion`; do not invent an `align` assertion or force equal sizes.
- **Cross-time substitution:** use `handoff` with the outgoing last intended visible moment and
  incoming first visible moment. A layer ending at 3s is absent at exactly 3s; use the actual last
  output frame, not an arbitrary epsilon. Matching at mathematical endpoints does not prove the
  sampled video matches. Fetch `motion-scene-continuity` for the runnable sidecar and limitations.
- **Post-arrival attachment:** check the relevant interval, not only the seam. Use edge attachment,
  containment and presence as intended. Verify initial alignment before a `translation` check;
  it preserves offsets but does not prove they were right. It does not cover changing scale/rotation.

Check each intended relationship, target ambiguity and uncovered interval using available query/lint evidence. Contract records run with `picsart_scene_check_contracts`. On a disposable copy shift only the arriving object, require the unchanged join comparison to fail, then restore and recheck. Also test drift after arrival; coincident endpoints do not establish persistent attachment.

Render before/at/after the join and inspect continuous video for crop, occlusion, duplicate paint,
gaps and motion continuity. Geometry does not prove matching pixels, velocity or semantic identity.
Deliver the editable scene and the relation/time/target/tolerance evidence, distinguishing numerical
passes from inspected visuals and unverified cases.
