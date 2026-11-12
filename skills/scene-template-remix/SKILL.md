---
name: scene-template-remix
description: Select, reuse and customize scene catalog items. Use when remixing scene templates, looks, motion presets, text animations, transitions, effects or caption decorations, replacing placeholder content with media, or joining an outside object to a template.
metadata:
  category: workflow
  version: '1.7'
  ported-from: template-customization 1.7 at 55.128.2
user-invocable: false
---

# Reuse and customize a catalog item

When you read `picsart_scene_capabilities` or the recipe index (`picsart_scene_recipe` without `name`), pass `useCase: "scene-template-remix"`: the answer leads with what this job reads and names the rest in one line.

Served checks: `picsart_scene_check_contracts` runs contract records and reusable templates, `picsart_scene_check_motion` runs frame-complete motion records, and `picsart_scene_inspect` pages large sources; the one remaining limit is that pixel records have no automated checker, so inspect full-resolution rendered frames for them.

Keep the requested design; change the smallest unit that meets the brief. A rendered
demo proves one instance, not that every parameter combination works.

## Select the unit and editing mode

For a named template, describe that URI first. If the catalog vocabulary is unknown,
start with `picsart_scene_templates({facetsOnly:true})`: no template bodies or
descriptions, just the small vocabulary. Then call again with relevant filters and `detail:"full"` to read descriptions.
Its global `facets` lists the available categories, tags and reference policies, even
when no entries match. Narrow with exact filters, then compare candidate descriptions,
aspect and parameter surfaces with `picsart_scene_capabilities`, section `template:<uri>`:

- `category` is the primary purpose: `ui_widget` for UI elements, `infographic` for
  data/diagrams, `slide` for presentation layouts, `editorial` for editorial stories.
  Use the returned vocabulary for the other categories; do not invent category names.
- `tags` crosses categories (such as `photos`, `comparison` or `chat`). Every requested
  tag must match; filters combine with AND. An empty tag list means no tag restriction.
- `referencePolicy:"expand-only"` finds authored starting points for structural edits;
  `"reusable"` finds entries that allow catalog references. Omit it to consider both.
  This filter's `reusable` value means the entry omits the expand-only metadata flag.

For example, `picsart_scene_templates({category:"ui_widget",tags:["chat","input"],referencePolicy:"reusable",detail:"full"})`
finds a reusable chat input composition; `{category:"editorial",referencePolicy:"expand-only",detail:"full"}`
finds editable editorial starters. If no entry matches, remove the narrowest tag or
category and inspect facets; do not substitute an unrelated template just to get a result.
When two or more entries (or looks, presets, transitions) fit the brief and the choice
comes down to taste, build 2–6 of them on the user's content and let the user pick in
`picsart_scene_picker`, each card labelled in their terms; go on from the one they keep
and say which (picsart-video-rules, "A choice made by eye"). A technical fit (aspect,
supported modes, parameters) is yours to settle.
Read `supportedModes` before choosing an operation. An entry with
`referencePolicy:"expand-only"` is a complete authored scene starter, not a blank
scaffold or a live reusable reference. Use `bootstrap` for a new editable scene or
`inline` for an existing host; reference mode (including the default) is refused.
Zero parameters means edit the expanded layers, not invent bindings. A parameter declaration may carry `group`
(a heading an editor lists it under) and, on a vec2, `frame` (`"composition"` or `{layer}`: the value is a point in
that frame). Both are presentation only: a resolver ignores them and never moves the point. Once copied,
the scene is yours to edit, save, and reference locally like any other scene.
For effects on existing layers, list them with `picsart_scene_capabilities({sections:["effects"]})`, then read
the chosen one with `effect:<id>`.
The list tool uses metadata filters, not semantic search. If nothing fits, state the missing
behavior before authoring it; a similarly named scene is not necessarily a suitable effect.

For looks, motion presets, text animations, transitions, effects or caption decorations,
fetch the family guide before editing:
`picsart_scene_recipe({name:"scene-template-remix",reference:"references/catalog-families.md"})`.
It gives each family's discovery, parameter, deeper-edit and evidence paths. These are
different contracts: not every catalog item is a scene template or has an expansion tool.
For looks, call `picsart_scene_looks` with `facetsOnly:true`, filter by `category`, `tags` or `appliesTo`, then read the selected `look:<id>` capability section; the family guide explains role selection.

| Intent | Operation |
|---|---|
| Animate or style existing content | Apply the relevant motion, text-animation, look or effect preset; retain the existing layer and placement. |
| Reuse a composition with different inputs, when `supportedModes` includes reference | `picsart_scene_apply_template` with `mode:"reference"`; put its returned `sceneRef` in a layer's `content`. |
| Start a new standalone editable scene | `mode:"bootstrap"`; this resolves inputs into a concrete scene, not a live parameterized reference, and drops the template's declared parameters (declare the knobs you want tuned). |
| Bring editable template layers into an existing scene | `mode:"inline"` with the target `scene` and `at`; inspect the returned structure and IDs. |
| Structurally edit an already placed reference | `picsart_scene_expand_ref` for that instance; inspect diagnostics and preserve placement/timing before patching. |

A template's reference mode does not insert a layer. For example, this complete
`picsart_scene_apply_template` request returns content for a speaker overlay:

```json
{
  "uri": "scene://lower-third-card",
  "mode": "reference",
  "parameters": {
    "name": "Maya Chen",
    "role": "Creative Director",
    "cardWidth": 1400,
    "duration": 8
  }
}
```

Place that content on a host layer with `start:3` and `duration:8`; keep the host
long enough for the exit. These are parent placement fields, not invented template
parameters. The template's own duration and the parent's visible window are separate.

## Customize deliberately

Parameterize frequent, well-defined variations; use expanded editable structure for changes outside
that interface. Not every starter needs arbitrary clip arguments. When designing a catalog entry,
keep replaceable artwork/content inside stable semantic containers; derive selection outlines and
other companions from the same owner/geometry. Promote a recurring substitution into a supported
parameter only when its sizing, timing and media behavior have a clear, tested contract.

Read types, defaults, ranges and descriptions; retain existing bindings not being edited.
Use parameters while they express the change. Declared slots constrain bindings, not all
possible edits to detached source. Follow any supplied design-preservation contract;
otherwise preserve unrelated layout, styling, timing and assets from the user's scene.
To make a motion preset's knob a scene parameter, pass `expose` when applying it instead of promoting by hand: `picsart_scene_apply_preset` with `expose: {"distance": "heroDistance"}` keeps the preset's arithmetic as an `$eval` over the scene parameter `heroDistance`, declared from the preset's own spec (a number parameter of that name already there is shared). Number params only.

Preserve relationships by construction: shared motion belongs on the component owner, and related
dimensions/positions should derive from one parameter source. Do not detach a label into duplicate
tracks merely to customize it. Reference bindings remain reusable; `bootstrap`, `inline` and expanded
bodies are resolved copies, not live formulas linked back to the catalog parameters. For structural
edits, choose ownership, parameter derivation or per-frame binding first using
linked-element-motion (fetch with `picsart_scene_recipe`, name `linked-element-motion`), then validate the resulting relationships.

Read the actual source before bounded `picsart_scene_patch` edits. Page a large source with `picsart_scene_inspect` (outline, then read by patch address). Keep the original revision, update only intended parent references when a child changes, and read `large-scene-assembly` for definition ownership and consolidation.

List parameters support only the item shapes the template declares. Fixed slot counts
may be intentional. Longer text does not imply auto-fit, more items do not imply more
duration, and grouping does not imply automatic background growth. Measure the requested
instance, then adjust exposed sizing/timing or make the needed structural edit. Preserve
the supplied copy unless changing it is part of the request.

For replacing tile/card artwork with photos or videos, or making an outside object arrive inside
a template, read [content replacement and template handoffs](references/content-and-handoffs.md).
Through MCP: `picsart_scene_recipe({name:"scene-template-remix",reference:"references/content-and-handoffs.md"})`.
It covers destination-first layout queries when the other object does not yet exist, join-time
alignment, persistent ownership after arrival, and checks on the assembled host.

For the variable-beat kinetic promo starter, fetch the
[kinetic promo worked validation](references/kinetic-promo-story.md):
`picsart_scene_recipe({name:"scene-template-remix",reference:"references/kinetic-promo-story.md"})`.
It supplies executable default checks and distinguishes a known rotated-containment
limitation from separate rendered-ink evidence. Rebase the examples after customization.

For circulating photos/video cards, fetch the
[closed carousel worked validation](references/closed-media-carousel.md):
`picsart_scene_recipe({name:"scene-template-remix",reference:"references/closed-media-carousel.md"})`.
It covers variable card boxes, a shared phase clock, cycle seams, cards placed in depth
(far-to-near draw order), and executable geometry/motion/pixel checks. It is not an
arbitrary path.

For editable open curves and independent phase/media clocks, fetch
[open-path carousel worked validation](references/open-path-media-carousel.md):
`picsart_scene_recipe({name:"scene-template-remix",reference:"references/open-path-media-carousel.md"})`.
It distinguishes hidden endpoint resets from continuous travel and separates
card endpoint opacity from surface entry opacity; rebase its checks after edits.

For staggered word reveals with circulating media, left/right text occlusion and a
shrink-to-title cut, fetch [text/media carousel validation](references/text-media-carousel.md):
`picsart_scene_recipe({name:"scene-template-remix",reference:"references/text-media-carousel.md"})`.
It covers measured word widths, derived phase boundaries, scoped owners and controlled
pixel checks where layout alone cannot establish which text is painted.

For words arriving from the right while the settled phrase stays centered, fetch
[centered word build validation](references/centered-word-build.md):
`picsart_scene_recipe({name:"scene-template-remix",reference:"references/centered-word-build.md"})`.
It covers measured word widths, growing-prefix positions, shared fitting, push/hold
motion checks and painted stability; rebase times and targets after nesting.

## Validate the customization, not just the default

1. Validate the assembled host with `picsart_scene_validate`.
2. Query actual ids/scopes and root-time geometry with `picsart_scene_query_layout`. Use `picsart_scene_lint_layout` for supported overlap, off-canvas and relationship checks.
3. Derive expected relations and values from design intent, then bind actual targets and clock windows after nesting, retiming or count changes. Run those records with `picsart_scene_check_contracts` (a reusable `template` with `targets`, `numbers` and `clock` where intent repeats) and read pass, fail or inconclusive per contract; a verdict is not a whole-scene coverage report. Containment does not imply centering, and shared motion can preserve a wrong initial offset. Use the UI alignment negative-control method from `linked-element-motion`, then restore the intended scene.
4. Inspect full-resolution `picsart_scene_contact_sheet` images at entrance, intermediate change, hold and exit; set `resolution` to the composition dimensions. Watch continuous video for motion and record checks not run as unverified.

For a reusable handoff, test realistic variations relevant to its advertised inputs:
short/long copy, different list counts, timing and delayed/nested placement. Deliver
editable source or reference bindings, requested media, and what was actually checked.
Separate numerical passes, inspected frames and remaining limits; do not call a template
generally validated because its default render succeeded.
