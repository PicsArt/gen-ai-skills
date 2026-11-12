---
name: character-rigging
description: Build and animate a 2D cartoon character in a scene — rig-humanoid and rig-face and their controls, walk_cycle, acting and drivers on a rig, two-bone IK, draw order, tapered ink lines, lip sync, a cut-out puppet built from named SVG parts, sockets, reach and held props — and the craft of morphing a shape's outline — preparing two drawings so they morph without twisting, choosing between outline keyframes, morph targets and per-vertex tracks, blend-target hygiene, timing (anticipation, overshoot, holds), volume-keeping squash, face visemes and blinks, scene-to-scene morph transitions, bending a picture over an art mesh, and explicit skin weights. Use when a cartoon character, mascot or face walks, waves or talks; when a path's outline changes shape over time — one drawing becomes another; a jelly, blob or character squashes, stretches, bounces, wobbles or breathes; a cartoon face talks (lip sync, mouth shapes), smiles or blinks; a cut is hidden by a morph; or an image, text or composition has to bend.
metadata:
  category: authoring
  version: '1.7'
  ported-from: shape-morphing 1.7 at 55.130.0
user-invocable: false
---

# Cartoon characters and shape morphing

Field names are the `path` item's (`picsart_scene_capabilities` with `sections: ["schema:ShapeContent"]`); the outline mechanics are in
[references/outline-mechanics.md](references/outline-mechanics.md).

## Named motions on a rig

A rig document can declare root `actions`, named motions an instance plays: bone tracks go in
`actions.<name>.layers`, drawing and order selectors in `actions.<name>.parameters`. Keep the
skeleton and painted weights once, with static rest transforms; place the rig once and use the
`scene_ref`'s `content.animation` to blend one action into the next (walk→idle). Set
`content.blending: "pass_through"` so limbs can reach beyond the rig's frame without canvas padding:
under pass_through the frame sizes and places, it does not clip. A layer treatment that needs a
composited result (mask, effect, non-normal blend, opacity below 1, motion blur, mesh, stroke or shadow,
adjustment or look) isolates and clips it. Action bodies have time keys, no `$eval` or expressions;
layer expressions and constraints run after the mix. Step channels switch immediately. Delayed first
keys need the `beforeFirst: "rest"` action policy. `animations` is a layer field and the action stack is
`content.animation`; root `actions` are distinct from a track content's sequential `clips`. `rig-humanoid` and
`rig-humanoid-front` (the same body from the front) declare actions: `scene-animation-reference`. The schema is `picsart_scene_capabilities` with
`sections: ["schema:SceneAction"]`; the full crossfade example is in
`picsart_scene_recipe scene-animation-reference`.

## 0. Cartoon character rigs

A 2D cartoon character starts from a catalog rig (`scene://rig-humanoid`, `scene://rig-face`) or from named SVG parts built with `picsart_scene_build_model`. Read only the section the step needs, with `picsart_scene_recipe` `{name: "character-rigging", reference: <file>}`:

| Step | Read | Covers |
|---|---|---|
| Build a character from an SVG sheet | `references/rig-build.md` | the sheet, `character: {svg, check, view, duration}`, parts, face and hands; the frozen sheet prompt is `references/part-sheet-prompt.md`; a cut-out puppet from one picture is `references/cut-out-puppet.md` |
| Place a rig in a scene | `references/rig-place.md` | the two catalog rigs, `scene_ref` placement and size, sockets and held props, the bone map, draw order, head turn; sockets and held props in full are `references/sockets-and-props.md`, the 2D head turn `references/head-turn.md` |
| Know a rig's controls | `references/rig-controls.md` | the standard control names and ranges (visemes, moods, arms, hands, held props, head) |
| Act: walk, gesture, act, drive | `references/rig-act.md` | IK, gesture arms and the wave rule, `walk_cycle`, gestures, `acting`, actions, parameter drivers, ink lines |
| Hand-built limbs, skin, pins | `references/character-motion.md`, `references/skin-weights.md`, `references/live-pins.md` | a rig no template fits |

Rules that hold on every step: animate only the rig's parameters (key them in the layer's `content.parameters`, or apply a rig preset); never write joint Lua by hand; verify a walk or a gesture on a `picsart_scene_contact_sheet`.

## 1 to 11. Morphing an outline

A path whose outline changes over time (one drawing becomes another; squash, bounce, faces, scene-to-scene morphs, bending a picture, explicit skin weights): read `references/morphing.md`; its sections are numbered 1 to 11 and each names the technique it covers. Its companions: `references/art-mesh.md` (bending a picture over a mesh), `references/layer-follow-through.md`, `references/traced-svg.md`, `references/outline-mechanics.md`.

## Tuning by hand — `picsart_scene_tune`

Open it as `motion-design-craft` describes. `rig-humanoid` and `rig-face` already declare their controls; a custom character exposes its own as `scene-building-basics` "Reusable parts" says. To keep a finished character, `picsart_scene_library_save` saves it under `Picsart Scene Library/Characters/<name>` with `name`, `kind: "character"`, `rights: "own"` (or `"licensed"` with a `license` note), and `scene` (the document or its HTTPS URL). Put render kinds (`vector`, `cutout`, `3d`, `live2d`, `spine`) in `tags`; assets and controls are derived from the scene. `previewUrl` supplies the portrait, or omit it to render one at `previewTime` (default 0); `videoUrl` is an optional demo. `pick: true` picks that version. `picsart_scene_library_list` with `kind: "character"` returns the picked version or newest, its durable `sceneUrl`, controls and version count; `tag`, `name` and `folderUid` filter it. USE a saved character with `picsart_scene_apply_template`, `uri: "library:<libraryId>"` (picked version or newest) or its `sceneUrl`: reference mode (the default) returns a `scene_ref` snippet naming its URL, which `picsart_scene_patch` adds as a layer (`add`, `kind: "layer"`); inline mode copies its body into the host as a scene asset, which makes the scene several MB larger, so keep it by reference.

## Not expressible (format findings, not rules)

- Weight-indexed in-betweens: no target "at weight 0.5"; the mid pose is a second target cross-faded
  by hand (`references/morphing.md` §3).
- Curved vertex trajectories: a vertex keyframe takes no spatial tangents (`inTangent`/`outTangent`
  are honoured on `position`/`anchor` only), so an arc needs a breakdown keyframe.
- A target's `weight.expression` reading another target's weight directly: unverified; the
  corrective pattern goes through parameters.
- No priority/override between procedural targets (VRM `overrideMouth`/`overrideBlink` block/blend):
  conflicts are authored by hand.
- `closed` is static and the hole count fixed: topology never morphs.
- No automatic volume preservation under a squash target.

## Films are scenes of scenes (no joiner tool)

A character rig or a shot is its own scene with its own Drive `sceneUrl`. The film that joins shots is just a root scene whose layers sit on a track of scene assets: `assets: [{id:"shot1", type:"scene", uri:<shot1 sceneUrl>}, ...]` and a `track` of clips that reference them in order. Build and edit each shot alone (`returnSceneUrl: true` on every edit keeps it small), then export the root; the export fetches the nested scenes server-side. Nothing to call to "join" them.
