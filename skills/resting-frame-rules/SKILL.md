---
name: resting-frame-rules
description: Keep every element whole or gone whenever motion stops - when an animation finishes, when an element appears without moving, and on the last frame, each photo, card or title sits fully inside its frame or fully outside it, never cut by the edge. How to build entrances, exits, scrolls and zooms so they land clean, and how to check a scene with the layout tool. Use when animating photos, cards, screenshots or text in a scene, and before a scene with motion goes to REVIEW.
user-invocable: false
---

# Rest framing

**When motion stops, every element is whole or gone.** At each moment an element comes to rest, it
sits fully inside its frame or fully outside it. A photo the edge cuts while it slides reads as
movement. The same cut once it has stopped reads as a mistake: a picture cropped by accident.

An element comes to rest:

- when its animation finishes, or pauses long enough to read as a stop;
- when it appears without moving;
- on the last frame, where the video stops on whatever is still moving.

The frame is the canvas, or the composition that holds the element, such as a panel.

## What does not count as cut

- **A full bleed.** An element that spans its frame on an axis, past both edges: a background
  larger than the canvas, a band across the full width.
- **A crop inside the element's own box.** A photo `fit: "cover"` in its box, a mask, a zoom inside
  a panel. That is framing, not the edge.
- **A cut the design makes on purpose.** A phone mockup the design cuts at the bottom, a carousel
  that shows the next card's edge as a hint. Keep it only when the design or the user asked for it.

While an element moves, the edge may cut it.

## Build it so it lands clean

1. **Entrances end inside.** Start fully outside the frame, at least the element's own size past
   the edge, or start inside with opacity or scale. The last keyframe puts the whole element
   inside, with a margin.
2. **Exits end outside.** The last keyframe puts the element fully past the edge, or at opacity 0.
   End the layer there.
3. **A scroll or a pan stops on whole items.** Move the parent of the row or list, never each item.
   It stops where every item is whole or gone: the frame's edges fall in the gaps between items.
   An item larger than the frame does not fit a scroll; make it smaller or a full bleed.
4. **A zoom ends inside.** A scale-up that would push the element past the edge either ends at a
   scale that fits, or moves into a panel so the zoom crops inside the element's own box.
5. **The video ends at rest.** Every element shown on the last frame has finished moving. Never
   end on an exit or an entrance halfway through: hold the final layout, or let the exit finish
   before the end.
6. **An element larger than its frame** is a full bleed on that axis, or it is scaled down to fit.

## Check it

After the motion is authored, and after each change to it:

1. **Find the rest moments in the scene.** For each layer: the time of the last keyframe of each
   move in its `animations` or `transforms`, its `start` when it appears without moving, and the
   last frame. With `timeMode: "layer"`, keyframe times count from the layer's `start`. A layer
   with a `parentId` moves with its parent, so it rests only when the parent does too. Several
   layers that settle together share one moment.
2. **Ask the layout tool at each moment.** Call `picsart_scene_query_layout` with the scene and
   that `time`. For each layer that has come to rest then, read `onCanvas`:
   - `full` or `off`: whole or gone, as it should be;
   - `partial`: the canvas cuts it. It is a full bleed only when its `box` passes both edges of
     an axis; otherwise it is a finding.

   A layer with `clippedBy` is cut by the composition that holds it: when its `clippedBox` is
   smaller than its `box` on one side, that is a finding too.
3. **Fix each finding** with `picsart_scene_patch`, on the keyframe that ends the move, or
   on `transform.position` when the layer does not move:
   - **at the end of an entrance, or on a hold:** move it in by as much as its `box` passes the
     edge;
   - **at the end of an exit:** move it out until its `box` clears the edge;
   - **a row or list:** move the parent, so every item is whole or gone;
   - **larger than its frame:** rule 6.

   Pushing an element meant to stay on screen out of the frame is the wrong fix: move it in, or
   change what it does.
4. **Check again** at the moments you changed.

The layout tool reads geometry, not pixels. When it gives a layer no box (text on an engine that
does not measure it), or a finding is in doubt, look at `picsart_scene_contact_sheet` at that
`time`.
