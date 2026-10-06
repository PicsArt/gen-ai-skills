# Asset preparation — focused prompts, ready work, scoped rebuilds

Applies to character/prop references and scene-picture dependencies. These rules
govern style prefixes, batch scheduling and rebuild scope; they do not remove
identity approval, quality floors or credit authorization.

## 1. Keep reference prompts about the reference

For neutral portraits, profiles, sheets and isolated prop plates, derive and save
`bible.assetStylePrefix` from the locked look: the medium, era where applicable,
stock/grain, colour treatment and skin/material rendering. Copy those visual
clauses without changing their meaning. Exclude narrative genre directions,
locations, scene lighting, camera movement, off-centre staging and the movie's
aspect ratio. Translate palette material names into colour values/tints rather
than asking for concrete walls or ceiling tiles behind a portrait. Do not change
`bible.stylePrefix`; scene pictures and video retain the full scene look.

Use that asset prefix consistently with the film's medium line, followed by the
specific reference task. If the full prefix already contains only compatible
visual styling, it may be reused. No new style approval is needed for this
task-specific extraction; a creative change to the locked look is different.

- Portrait: identity, face-to-neck framing, frontal gaze and neutral studio ground.
  Keep wardrobe/action out of the face description except what is actually visible.
- Profile: approved portrait as identity authority, one clear side-view request,
  head/neck framing and neutral ground. Preserve the reference's face, hair and
  rendering. Do not re-describe the character's biography, outfit or story.
- Sheet: the full identity descriptor, layout and wardrobe for a one-shot;
  approved portrait/profile for the photograph chain. Keep face
  preservation and panel boundaries explicit; do not add scene action.
- Prop: object, scale, material and necessary visible features. A device whose
  screen matters needs an explicit screen-content requirement and a check that it
  is visible; readable final lettering remains a compositor task.

Inspect the assembled prompt for contradictions BEFORE dispatch: neutral ground
versus a named scene; tight face crop versus full-body instructions; strict profile
versus frontal gaze; neutral expression versus scene panic. Fix the conflict,
not by appending another paragraph of negations. Existing template fields may be
kept, but irrelevant repeated clauses can be removed; template completeness is
not more important than a coherent reference task. Keep the selected model,
resolution and identity references unless the diagnosis requires changing them.

After a failed image, record the observed defect and its likely cause separately.
Correct a crop deterministically when the pixels already exist; otherwise change
the conflicting prompt clause/reference and retry only that image within the
authorized spend. Two consecutive failures of the same kind require reassessing
the input or method, not a third identical dispatch. If no defensible change or
authorized budget remains, set that item aside, explain why and advance other ready work.

## 2. Schedule by dependency, not the slowest item in the batch

Launch independent generated sheets and props concurrently within the
service's limits and approved spend. Check each one, obtain approval, then
lock, crop and save it. A supplied photograph follows its profile → sheet
chain, with each dependent using an actual checked result. One asset's retry
blocks only that asset's dependents.

On each completion or submitted review, persist the job/result and per-item
status, then advance eligible dependents while unrelated jobs continue. An
internal image check is not user approval. Pending approval blocks that item's
dependent stage; it does not block already-approved siblings. A failed prerequisite
blocks only its dependents. Respect required asset locks before scene/video work.

Show each completed asset immediately and review the ready subset on
`picsart_asset_review`. One generated sheet per character, all ready independent
assets quoted together, and a retry delays only its dependents. Ask again only
about outstanding or new items; preserve each already
approved asset. Keep draft and approved versions distinct. Use the render monitor for
ongoing jobs; do not duplicate dispatches to fill a board or start speculative work.

Track each dependent job's source versions at dispatch. If a source changes while
that job is running, keep its result as a candidate needing the impact check below;
do not silently accept stale work or restart the entire batch.

## 3. Rebuild only dependencies whose content became invalid

A new source version marks dependents for inspection, not automatic generation.
Record what changed and which role each downstream image takes from that source:
identity, wardrobe, geometry, lighting, expression, pose or framing. Compare the
existing images and their intended shots, then record `reuse`, `recrop`, `repair`
or `rebuild`, with a short reason and source versions. If impact is uncertain,
mark it for review; do not assume either that everything is stale or nothing is.

| Change | Inspect/rebuild scope |
|---|---|
| Expression in one scene frame | That frame and any picture needing that expression/pose. Reuse an unchanged room map; later shots may intentionally show a different emotion. |
| Identity, hair or wardrobe correction | Views, sheets and scene pictures actually showing the changed feature; unchanged geometry-only maps are not automatically invalid. |
| Room layout or anchor-object position | Map and wides relying on that geometry; check framing and eyelines before reuse. |
| Scene lighting/time of day | Pictures intended to share that illumination; retain a geometry-only map only if its role remains valid and it will not impose conflicting lighting. |
| Crop, file format or URL repair with unchanged content | Re-crop/re-host from the archived source; update references. No generative cascade. |
| Layout/panel correction on a sheet | Affected panels and crops. Reuse separate approved portrait/profile files unless their content changed. |

An uninspected or identity-defective initial scene picture is still not a valid
source for derivatives. Scoped reuse concerns already-existing material checked
against a correction; it does not justify building fresh images on a bad base.

Say the proposed scope briefly before charged work, for example: “Only the opening
expression changes; the room map and the wide stay.” Quote only the
needed generations, preserve approved originals, and never silently regenerate
existing video because an asset changed. Flag affected takes for review instead.
