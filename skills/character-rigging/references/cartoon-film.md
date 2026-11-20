# A cartoon film, scene by scene

A short animated tale of several scenes: a few rigged characters, painted sets, props, narration and
voices. This is the order of work and the rules that keep the scenes one film. Characters are built as
[rig-build.md](rig-build.md) and [cut-out-puppet.md](cut-out-puppet.md) describe and must pass
[character-rules.md](character-rules.md).
A character or a set piece cut from one picture with `picsart_scene_cut_parts`: read "The first call" in
[cut-from-one-picture.md](cut-from-one-picture.md) before the first call, and follow it.
The join is `large-scene-assembly`'s "A film is a root of
shots that share saved rigs" (`picsart_scene_recipe` `{name: "large-scene-assembly"}`).
Voices are cast as the `voice-over-generation` skill says, and music is laid as `background-music` says.

**Style.** Pick the film's drawing style first from the style index (`picsart_scene_recipe` `{name: "visual-styles"}`, reference `references/style-index.md`; the classic cartoon is the default and comes first; offer every row whose `use` is `film`, never a shortened list), and follow the styled film flow (`references/film-flow.md` of the same recipe) for the picker, the rough cut and how each shot lands.

## 1. Plan before spending credits

- Write a scene table first: for each scene its set, who is in it, what each one does, the spoken lines
  and its length. ASK (with `picsart_ask`, found as picsart-video-rules says, for any closed choice, a multi-select included, so the options are buttons the user taps, the recommended one first; then your host's own question tool, such as AskUserQuestion; only where all fail, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) the user to agree it or change it.
- Add to the table the pictures and voice lines each scene needs, with their credit cost
  (`picsart_preflight`).
- Settle in the same turn every story question the request leaves open that changes a drawing (who
  waves to whom, which way they walk, what the room holds).
- **Animate before generating.** Build a face, an expression, a pose or a small prop in the scene first:
  rig controls, shapes parented to a bone, a transform. Propose a generation, with its prompt and cost,
  only after that attempt visibly fails, and show the failed frame; then SPEND (quote it in one line, then get the yes with `picsart_ask`, found as picsart-video-rules says, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", else your host's own question tool, such as AskUserQuestion; never as a typed question unless both fail; only then those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says).

## 2. One world for the whole film

- Keep the shared things in one place and reuse them in every scene: the sun or moon, the grade, the
  fades, the wind sway, each character's height. Give heights in metres and turn them into pixels from
  one reference figure, so a child is never drawn bigger than a parent in a later scene.
- Every voice keeps its first line's settings: the same voice, model settings and prompt tags. Level each
  new line to that speaker's approved one. Only a situational effect changes (an echo for a voice heard
  from inside).
- Before showing a new scene, compare one of its stills with a still from an earlier scene.

## 3. Sets and props

- **A set is one picture.** Do not build a room in layers.
  One generated plate, or one 2D place built with `picsart_scene_build_place`.
  Cutting the front pieces a character stands behind (bars, a table edge, a bed foot) out of that one
  picture along their drawn outlines is not served here. Draw such a front piece as its own prop over the set instead (below), never as a
  rectangle cut from the picture, or stage the character clear of it.
- **Generate only what is partly hidden and later seen whole**: a character's covered parts, or a stool
  whose seat is under a sitter until they stand. Before paying for one, try redrawing the hidden part
  from its outline.
- **A standalone prop is drawn on a transparent background**, with the set as its style reference. Where
  the image model has no transparent option, remove the background with `picsart_image_remove_bg` and
  check the alpha edges. Leave out drawn steam or smoke that the scene animates.
- **A character that runs with a prop** (a kite string, a jar): the `pick_up` preset (`aimAt` the spot, `start`,
  `duration`) crouches, reaches and rises, and the touch is at `start` + `duration` / 2: swap the stage copy for the
  held one there. Apply the `run` or `jog` first (`start` after the pick-up, `heldBy` set) and `pick_up` over it;
  the holding arm stays on the prop and the free arm pumps. Move the body at stride × steps.
- **A string, leash or rope a character holds** (a kite string, a dog's lead) is a line between two moving
  points, so it is a shape layer whose two path points are expressions: one end on the hand's grip socket,
  the other on the thing it ties to. Put the layer at `position` `[0, 0]` with `anchor` `[0, 0]` so the
  points are composition px, and read every point at `time`:
  ```json
  {"id": "string", "transform": {"position": [0, 0], "anchor": [0, 0]},
   "content": {"kind": "shape", "items": [
     {"type": "path", "closed": false, "vertices": [
       {"point": {"expression": "local p = ctx.composition:getLayer('fox'):getSocket('rightGrip', time) return Vec.v2(p.x, p.y)"}},
       {"point": {"expression": "local K = ctx.composition:getLayer('kite') local a = K:getPlacement():anchorPoint(time) local w = K:getWorldPoint(a.x, a.y, time) return Vec.v2(w.x, w.y)"}}]},
     {"type": "stroke", "color": "#3a2a1a", "width": 5}]}}
  ```
  The line follows the hand through a walk, a run and a gesture, and the kite through its own motion; no key
  of its own. Start it when the character picks the string up (the layer's `start`), and close the holding hand (`rightHandFist` 1) from then on. A string drawn from a fixed point
  stays where it was and leaves the hand: do not key it by hand.
- Check every prop's size against the characters before placing it, and scale it down when it was drawn
  too big. Small things on a table lie flat inside the table top.

## 4. Staging

- In a profile embrace only the near arms show; the far arm goes round the far side of the partner. Two
  figures that touch stand on the same floor line, or one reads as nearer the viewer.
- `parentId` carries a transform, not opacity: fade the leaf layers, not an empty parent.
- Hide a cut that cannot be animated cleanly (climbing onto an animal, stepping into a doorway) with a
  short dip to black.
- When the user moves one point of a shot, change only that point and diff the rest against the version
  before.

## 5. Time inside a scene

- Give every layer that starts after 0 `timeMode: "layer"`. Its keyframes then count from the layer's own
  start, as its `scene_ref` actions do. Without it a layer's keys are composition time, and keys written
  from 0 on a late layer leave it at its last value for its whole window.
- Check one action in a close-up still before trusting it in a wide shot.

## 6. One document per scene, joined at the end

- Build, validate and review each scene as its own scene document, with `returnSceneUrl: true` so it has
  its own `sceneUrl`. A whole film in one document is several megabytes and too big to send through the
  tools; a scene is small enough to inspect and patch.
- Join the scenes at the end with a thin root: one `scene_ref` layer per scene, or a `track` of clips
  over one `scene` asset per scene (SKILL.md, "Films are scenes of scenes"). A scene with no sound leaves
  the film silent over its window.
- **A character lives in one place.** Save it once with `picsart_scene_library_save`
  (`kind: "character"`) and place it in every scene by its `library:` uri, never as each scene's own copy.
  Part pictures it names are hosted with `picsart_upload_urls` (`picsart_upload_local_files` for files on disk), and the scene's assets point at their
  links. A link on a host the export does not allow fails by name; fix the link, never inline the rig to
  get past it.
- Save each finished scene (`picsart_scene_library_save`) as soon as it is accepted, so it survives as a
  document and not only as its render.

## 7. The review loop

Render the scene and look at stills at its extreme moments (a widest step, a full reach, each swap and
each seam) as one contact sheet (`picsart_scene_contact_sheet`). Send them to the user and fix what they
mark. Watch the whole scene once before sending the video. When a preview has an upload limit, send a
smaller export and keep the full-quality render.
