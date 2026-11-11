---
name: large-scene-assembly
description: Build large editable scenes by decomposing a timeline into bounded scenes and reusable components, defining timing and asset contracts, then assembling and safely consolidating them. Use when authoring long videos, many scenes or layers, scene-by-scene designs, oversized JSON, fragile whole-document edits, reusable modules, or an editable handoff.
metadata:
  category: workflow
  version: '1.1'
  ported-from: large-scene-authoring 1.1 at 55.75.0
user-invocable: false
---

# Large scenes, small editing units

Served checks: `picsart_scene_check_contracts` runs contract records and reusable templates, `picsart_scene_check_motion` runs frame-complete motion records, and `picsart_scene_inspect` pages large sources; the one remaining limit is that pixel records have no automated checker, so inspect full-resolution rendered frames for them.

Keep one editable source of truth and a thin assembly. Decompose by meaning and ownership, not an
arbitrary layer count. A card that travels across three beats is one persistent object, not three
separate scenes just because the storyboard has three frames.

## Establish a manifest before growing the document

Record canvas/fps, ordered beats and durations, shared style tokens, component ids, assets, entry/exit
states, and the carrier (if any) across each seam. Use the compact
[scene manifest](references/scene-manifest.md) when the timeline needs a durable handoff.
The manifest is authoring documentation, not an extra field injected into the scene schema.
Record checkable intent in a separate versioned contract sidecar (`linked-element-motion`), with
stable contract ids, query target scopes and root-time phase windows. The same element may have
different relationships in different phases; document independent travel rather than forcing one
parent relationship for its whole lifetime. Preserve these contracts alongside component revisions.

Choose boundaries deliberately:

| Unit | Representation and ownership |
|---|---|
| Local semantic unit: card, label, icon | Inline `composition` or a supported parent rig; animate its common placement once. |
| Reusable independent scene | Scene asset/reference with explicit inputs, duration, dimensions and assets. |
| Sequential beats | `track` clips; record how clip windows map into source time. |
| Persistent foreground across beats | Parent-level layer spanning the interval, outside the replaced clips. |
| Shared styling | Consistent authoring tokens/parameters; do not assume implicit inheritance between documents. |

Ask `picsart_scene_capabilities` (`schema:<Name>` sections) for the exact relevant content/asset/parameter shapes. An inline composition
uses its owning document's assets; a separately referenced scene owns its own asset scope. Do not
rely on an undeclared parent asset, copied font id, or temporary URL being available in a child.

## Author → verify → assemble, incrementally

1. Build each semantic component with editable shapes, text, assets, keyframes and stable ids. Validate it with `picsart_scene_validate` and query entry, event and exit geometry with `picsart_scene_query_layout`.
2. Inspect full-resolution stills with `picsart_scene_contact_sheet`, setting `resolution` to the scene dimensions; watch continuous video for motion claims.
3. Preserve the accepted source revision and record its returned source or handle. A held handle is local to its tool surface, not a portable published URL.
4. Assemble a thin root that owns order, clip windows, seams and persistent carriers. Children own their internal layout and motion.
5. Check just before, at and after joins. Rerun supported `picsart_scene_lint_layout` relationships against independently recorded intent. Rerun contract records with `picsart_scene_check_contracts`; record uncovered assertions as unchecked.
6. Continue component by component; recheck affected joins and overall playback. Show meaningful milestones during authorized autonomous iteration.

## Keep edits bounded

- Read the source subtree or named layer before bounded `picsart_scene_patch` edits. Page the structure with `picsart_scene_inspect` (outline, then read by patch address).
- Keep stable semantic ids and distinguish definitions from instances. Query ids/scopes are for evaluated geometry, not guessed edit addresses.
- Save revisions and explicitly update parent references when a child changes. An old parent does not silently follow a new child.
- Recheck every affected instance's parameters, assets, duration and seams. Keep unrelated components unchanged.
- Split work by component ownership only when parallel work is already authorized; one integration pass assembles accepted revisions.

### Inspect authored structure before evaluating it

Page authored structure with `picsart_scene_inspect`: outline (20 rows by default, up to 100, continue with `nextOffset`), then read an exact layer or field path by patch address. Keep the source document and its manifest, and read the intended component before editing. Distinguish authored layer addresses from evaluated query ids and composition scopes; never infer edit addresses from a geometric result. Use bounded `picsart_scene_patch` edits against known ids and field paths. If the source is not available, retrieve it through its saved source URL before editing; a layout query is not a complete source inventory.

Outline rows also carry container pointers, `cameraExempt` and references, and the outline names the scope's authored camera fields. Only the root scene argument is loaded, through the guarded loader: follow an external scene deliberately, as its own `scene` argument, since the parent is not its editable body. `sceneSha256` is a canonical-JSON hash for paging, not a remote asset fingerprint; edit against immutable handles.

Inspect shared definitions in their own asset scope. Editing a shared definition affects all its instances; create an instance-specific definition and retarget only the intended consumer for a local variation. Keep the original revision and explicitly update parent references after a child changes. Revalidate and query every affected instance and seam. Source inspection cannot certify layout, media availability or motion.

## A film is a root of shots that share saved rigs

A film of N shots that act the same character is one root with N `scene_ref` layers, one per shot,
each naming the shot's saved scene by URL; each shot names the character's saved rig the same way. Save
the rig once and give every shot that one URL. An export renders the root as written and the worker
fetches each distinct URL from its allowed hosts, so a hosted rig costs one fetch however many shots use
it. A re-saved rig is a new document with a new URL: point each affected shot at it, re-save those shots, then point the root at their new URLs, or the export renders the old revision. A URL on a host the worker does not
allow fails the export by name; fix the URL, do not inline the rig to get past it.

## Consolidate without losing the sources

Consolidation means a coherent, resolvable deliverable—not indiscriminate flattening.

1. Save a named source revision and its manifest before replacing references.
2. Keep a root whose children are saved scenes referenced by URL (`scene_ref`): an export sends the root
   as authored and the renderer fetches each hosted child itself, so no body is copied into the root.
   Inline (`picsart_scene_expand_ref`, or scene assets with their scoped dependencies) only when the consumer
   cannot fetch the URLs, and say so.
3. Expansion is not a universal recursive bundler. Read its diagnostics and `stillReferenced`;
   process only the intended instance, preserve track timing, and do not delete assets still used.
4. Check for unresolved/local-only handles, unavailable assets, namespace collisions, duration
   changes, changed parameter defaults and missing fonts. A flat layer list is not proof of portability.
5. Revalidate and compare pre/post geometry at component events and seams; preview those moments.
   Run the relevant relationship lint again and watch the assembled video before claiming equivalence.

Deliver the editable root, component revisions, manifest and rendered evidence. Say what is external
and what was not verified; an MP4 alone is not an editable scene handoff.

For group vs. layout behavior use linked-element-motion (fetch with `picsart_scene_recipe`, name `linked-element-motion`);
for seam intent use motion-scene-continuity (fetch with `picsart_scene_recipe`, name `motion-scene-continuity`).

**Research note:** independently authored for scene. General motion-design research informed the
workflow; no Hyperframes implementation, wording, examples or numerical presets were adopted.
