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

## Contents

1 Plan before spending credits; 2 One world for the whole film; 3 Sets and props; 4 Staging (acting from
the plot, camera and cuts); 5 Time inside a scene; 6 One document per scene, joined at the end; 7 The review loop

## 1. Plan before spending credits

- Write a scene table first: for each scene its set, who is in it, what each one does, the spoken lines
  and its length. ASK (with `picsart_ask`, found as picsart-video-rules says, for any closed choice, a multi-select included, so the options are buttons the user taps, the recommended one first; then your host's own question tool, such as AskUserQuestion; only where all fail, the options numbered in one message; in unattended pace, never ask: write it to the project record's openDecisions with the answer you assumed, as picsart-video-rules says) the user to agree it or change it.
- Beside each beat in the table, plan its camera as you plan its acting: the shot size, the move or a
  hold, and the transition into the next scene (§4 "Camera and cuts").
- Add to the table the pictures and voice lines each scene needs, with their credit cost
  (`picsart_preflight`).
- Settle in the same turn every story question the request leaves open that changes a drawing (who
  waves to whom, which way they walk, what the room holds).
- **Animate before generating.** Build a face, an expression, a pose or a small prop in the scene first:
  rig controls, shapes parented to a bone, a transform. Propose a generation, with its prompt and cost,
  only after that attempt visibly fails, and show the failed frame; then SPEND (quote it in one line, then get the yes with `picsart_ask`, found as picsart-video-rules says, "Yes, go ahead" / "Yes, up to N credits for this task" / "No", else your host's own question tool, such as AskUserQuestion; never as a typed question unless both fail; only then those options numbered in one message; unless a spend limit the user stated covers it: N credits or an explicit no-limit ("as much as needed"), never inferred from words like "go ahead". Within it, ask nothing: quote it in one line ("About 8 credits; 12 of 20 left after this"), call it, then say what it spent and what remains, keeping a running total that includes failed calls, and stop to ask before the first call that would cross it. A money amount is asked once to restate it in credits; in unattended pace, never ask: call only with a consent or a stated spend limit already recorded, otherwise write the quote to pendingSpends and stop, as picsart-video-rules says).
- **Rig for motion, a generated picture for a pose.** The rig carries the motion: bob, squash, lean, head
  tilt, limb swings, hair. A pose or face it cannot reach by bending (a shock face, a dazed face, a dash
  with the arm thrown out) is a picture of the same character, swapped in on a beat: a cut, a squash or a
  spin, so it reads as acting, not a glitch. The rig keeps moving the swapped picture while it is on
  screen. When the expression changes the fringe, swap the whole head, not only the face.

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
- **A new angle on the same place shows the same place.** A cut to a front view, a reverse shot or a
  closer angle uses a set picture generated with the first one as its reference: the same landmarks
  (the big tree, the bushes, the path) and the same sky (the moon, the stars), the moon where the turned
  camera would see it. Compare a still of each angle side by side before animating the new one.
- **Generate only what is partly hidden and later seen whole**: a character's covered parts, or a stool
  whose seat is under a sitter until they stand. Before paying for one, try redrawing the hidden part
  from its outline.
- **A standalone prop is drawn on a transparent background**, with the set as its style reference. Where
  the image model has no transparent option, remove the background with `picsart_image_remove_bg` and
  check the alpha edges. Leave out drawn steam or smoke that the scene animates.
- **A character that runs with a prop** (a kite string, a jar): the `pick_up` preset (`aimAt` the spot, `start`,
  `duration`) crouches, reaches and rises, and the touch is at `start` + `duration` / 2 (the result's `phases.touch`): swap the stage copy for the
  held one there. The preset moves only the hand: bind `held` with `heldBy` the picking side beginning at the touch, inside the grip
  (never over the fingers), and release it at the drop (end `held`, start the stage copy at the hand), or the viewer sees the hand
  reach for the ball and leave it (validation warns `pick_up_without_prop`). When the action carries on in the next shot layer
  (a jump after the run), the prop goes with the figure (the same `held` from that layer's first frame) or is released with a beat; it is never cut
  (check a contact sheet at the pick-up, the handoff and the drop). Apply the `run` or `jog` first (`start` after the pick-up, `heldBy` set) and `pick_up` over it;
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
- **The set lives.** Nature in the place moves a little the whole time, chosen from what the place shows: tree crowns,
  bushes, flowers and grass sway and water ripples (`picsart_scene_apply_preset` `mesh:auto` with `motion` `sway` or
  `water` and a `region` on each; a shape tree or flower takes `motionPreset:sway` with a small `angle`), clouds drift a
  few px a second, and a sun turns or glows slowly. Keep it slight, felt rather than watched; a still night or an indoor set has less of it. Nothing under the
  characters' feet moves.

## 4. Staging

- In a profile embrace only the near arms show; the far arm goes round the far side of the partner. Two
  figures that touch stand on the same floor line, or one reads as nearer the viewer.
- `parentId` carries a transform, not opacity: fade the leaf layers, not an empty parent.
- Hide a cut that cannot be animated cleanly (climbing onto an animal, stepping into a doorway) with a
  short dip to black.
- When the user moves one point of a shot, change only that point and diff the rest against the version
  before.

### Acting from the plot

These hold for every character, however it was built (shapes, a rig, cut from one picture, Spine).
- Work out each character's reaction from the plot; do not wait for the user to spell it out. For each
  beat pick the mood (happy, sad, angry, worried, surprised…) and show it on the face and body: the
  rig's mood dials, brows, mouth and head ([rig-controls.md](rig-controls.md)).
  A mood comes in over about 0.3 s on the beat that causes it and stays until a later beat changes it.
  The body agrees: happy lifts the chest (`breath`), sad lowers the head (`headNod`).
- A character who speaks to or notices someone turns the head a little toward them (`headTurn` and the
  `look*` controls) a few frames before the line or gesture, and holds it.
- A gesture uses the free hand. A hand that holds something keeps holding it: never raise both arms
  when one is busy. Both arms move only when the beat needs both and neither holds anything.
- A character on screen never freezes. Give it a blink (`random_pulse` on `blink`) and a breath (`cycle`
  on `breath`) for the whole shot. A hold longer than about 1.5 s (looking at a found thing, a hug,
  watching something leave) also changes at least once a second: a head tilt or nod (`headTilt`,
  `headNod`), a glance (`look*`), a shift of the hips (`hipsTilt`).
- A hand that lets something go (a star floating off the palms, a bird flying from the hand) goes with
  it: the hands lift or open toward where it goes over the 0.3 s before it leaves, and the head and eyes
  follow it after. It leaves slowly and speeds up, on a curve, never on a straight line at one speed.
- A walk swings the arms against the legs (`walk_cycle`'s `armSwing`, 0.5 for a kid). Keep an arm still
  only while its hand holds something; never set `armSwing` 0 on an empty-handed walk.
- Something that arrives "in front of" a character (a bird landing, a ball rolling up) ends on that
  character's floor line, not nearer the viewer.
- **What hides what.** Layer order is depth: a later layer draws over earlier ones. Order the layers from
  the story: a character behind a tree or fence comes before it; a prop at the near-side feet comes after
  the character; a thing met on the character's floor line stands beside it, clear of its body. What the
  story shows (a face, a held prop) is never covered. A layer that moves in depth during a shot is two
  layers, one on each side, the first ending on the frame the second starts.
- Make expressions and small poses by animating first, as §1 "Animate before generating" says.

### Camera and cuts

Each camera choice comes from a beat. A move or a transition that no beat asks for is left out.
- **Shot size.** Wide when a scene opens in a new place; medium for action and talk; close (head and
  shoulders) for a feeling or a reaction.
- **Move only for a reason.** Follow a walk across the place; push in on a reaction; drift slowly on a
  calm beat. Hold still while characters talk or act fast, and while someone walks into a held frame.
- **One move per beat, eased.** Every camera key eases in and out, and a follow starts and stops with the
  walk. A pan moves the set less than a quarter of the frame width a second; only a pan that follows a run
  goes faster. A push adds at most about 0.6 to the zoom a second (1 to 2.2 takes 2 s). A drift changes
  the zoom by 5% at most over its beat.
- **Cut inside a scene** to change the size by at least one step (wide to medium). A smaller change reads
  as a jump. Cut when an action starts or stops, not in the middle of it.
- **Transitions carry story meaning.** A cut by default. `crossfade` (a dissolve) when time passes.
  `iris` or a `shape_reveal` wipe only for a new chapter. Inside one scene, no transition but the dip to
  black that hides a cut (above). No flashy one (`glitch_cut`, `flash_cut`, `zoom_through`) anywhere in
  the film. Hold the last pose through the transition and start the next scene's first action after it
  ends: an action under a dissolve is lost.
- **Keep screen direction across a cut.** A character who leaves on the right enters the next shot from
  the left, and one facing right at a cut still faces right after it, unless they turn on screen.
- **How.** A follow walks the rig `travel: "in_place"` and applies `ground_scroll` to the set's parent
  with the same walk numbers ([rig-act.md](rig-act.md), `ground_scroll`), so the set moves with the steps.
  A push sets `composition.camera.position` on the face and keys `camera.zoom` (`push_in` without
  `centerX`/`centerY`): the face stays where it is and grows. Framing a face far from the middle with
  `centerX`/`centerY` first moves it away, then swings it across fast. A cut keys `camera.zoom` one frame
  apart, the earlier key `"easing": "step"`. To land the face at screen point S at zoom z, set the pivot
  `camera.position` to (S − z × face) / (1 − z) for the scene. Transitions go on the join's track
  (`transitions[]`: `between`, `id`, `duration`). The camera itself is the film camera of
  `scene-animation-reference` (`picsart_scene_recipe` `{name: "scene-animation-reference"}`, reference
  `references/film-camera.md`).

### Acting from the plot

These hold for every character: built from shapes, rigged from a sheet, cut from one picture or imported
from Spine.
- Work out each character's reaction from the plot; do not wait for the user to spell it out. For each
  beat pick the mood (happy, sad, angry, worried, surprised…) and show it on the face and body: the mood
  dials, brows, mouth and head (`references/rig-controls.md`).
  A mood comes in over about 0.3 s on the beat that causes it and stays until a later beat changes it.
  The body agrees: happy lifts the chest (`breath`), sad lowers the head (`headNod`).
- A character who speaks to or notices someone turns the head a little toward them (`headTurn` and the
  `look*` controls) a few frames before the line or gesture, and holds it.
- A gesture uses the free hand. A hand that holds something keeps holding it: never raise both arms when
  one is busy. Both arms move only when the beat needs both and neither holds anything.
- Something that arrives "in front of" a character (a bird landing, a ball rolling up) ends on that
  character's floor line, not nearer the viewer.
- **What hides what.** Layer order is depth: a later layer draws over earlier ones. Order the layers from
  the story: a character behind a tree or fence comes before it; a prop at the near-side feet comes after
  the character; a thing met on the character's floor line stands beside it, clear of its body. What the
  story shows (a face, a held prop) is never covered. A layer that moves in depth during a shot is two
  layers, one on each side, the first ending on the frame the second starts.
- Make expressions and small poses by animating first, as §1 "Animate before generating" says.

## 5. Time inside a scene

- Give every layer that starts after 0 `timeMode: "layer"`. Its keyframes then count from the layer's own
  start, as its `scene_ref` actions do. Without it a layer's keys are composition time, and keys written
  from 0 on a late layer leave it at its last value for its whole window.
- A preset's `start` (`wave`, `talk_beat`, `pick_up`, `walk_cycle`) is always composition seconds, `timeMode` or not: a rig layer that
  appears at 6 s and waves 0.4 s later takes `start: 6.4`, and the result is stored on the layer's own clock. `start: 0.4` there is 5.6 s before the layer exists, and the gesture never shows.
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

**Review every character action by eye before the user sees it (required).** This covers every action
applied to a character: a pick-up, a bow, a wave, a jump, a sit, a prop handed over, a head turn while
talking. A scene that passes `picsart_scene_validate` has not been reviewed.

- **Key frames.** The start (standing), the deepest or most extreme pose, the contact (the hand on its
  target), the frames on either side of a prop attaching or leaving the hand, and the end, with more
  frames sampled across the action's window. Look at the whole figure on one `picsart_scene_contact_sheet`,
  never one frame.
- **Every part that takes part.** Then review the action part by part, not only as a whole picture. List
  each moving piece and each joint it turns about, with the seam between its pieces: waist (torso on
  seat), neck (head on shoulders), shoulder, hip, elbow, knee. At the start, the end and each extreme
  frame, look at a zoomed crop of each of those joints: `picsart_media_video_stills` with `times` and a `crop` around the joint, its box from
  `picsart_scene_query_layout`, on a render of the action.
- On every frame and crop check:
  - no gap, crack or overlap of hidden art at a seam (seat artwork showing on a thigh piece);
  - the neck stays on the shoulders when the head moves;
  - at a bow the seat turns with the trunk;
  - a part that is still in the action stays in its place;
  - no extra or doubled shape, and the silhouette reads as one body;
  - planted feet stay put (`picsart_scene_check_motion` `foot_slip`, and `foot_support` for a foot that must rest
    on something);
  - the hand touches its target (`picsart_scene_query_layout` at the contact);
  - a prop does not jump as it attaches to or leaves the hand (`picsart_scene_check_motion` `velocity_range` on
    the prop's layer across the swap).
- Fix a failure at its cause: the rig, the cut or the action's values, never with a workaround. When the
  rig cannot do the pose cleanly, use a smaller value or a different action, and tell the user which.
- Tell the user only what was done: "valid" means it passed validation, "visually checked" means these
  frames and crops were rendered and looked at. Name the actions, frames and joints you looked at.

**Review every camera move, cut and transition the same way (required).** Render the start, middle and
end of each move, the frames on either side of each cut, and the first, middle and last frame of each
transition, on one sheet. On those frames check:
- each beat's shot size matches §4 "Camera and cuts", and a close shows the face against a plain part of
  the set;
- the move is eased: what it moves (the set in a follow, the rig in a push) speeds up and slows down,
  never jumps (`picsart_scene_check_motion` `velocity_range` on that layer over the move), within the
  speed limits;
- a push keeps the face in place while it grows, and nothing the beat needs leaves the frame;
- screen direction holds across the seam, and the next scene's first action starts after the
  transition ends.

Then render the scene and look at stills at its extreme moments (a widest step, a full reach, each swap and
each seam) as one contact sheet (`picsart_scene_contact_sheet`). Send them to the user and fix what they
mark. Watch the whole scene once before sending the video. When a preview has an upload limit, send a
smaller export and keep the full-quality render.
