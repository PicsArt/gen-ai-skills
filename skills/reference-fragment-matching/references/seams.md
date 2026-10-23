# Seams: planning fragments and joining them

Fragments look independent until their seams tear. Each one is matched in its own window, so
nothing inside a fragment checks that it ends where the next one begins. This is what does.

## Before the first fragment

Take one **global census** of the whole reference before matching any fragment:

- the canvas: size, background colour, frame rate;
- every element that recurs, and the fragments it lives in ("the input bar is in F3 to F6");
- **shared motions**: one container's motion that carries several elements, such as a feed that
  scrolls;
- **handoffs**: the same object crossing a boundary, perhaps changing form (a hero card that becomes
  a deck, then a chip).

Then write the **fragment plan**, the one source of truth every fragment reads: per fragment, its
window, its density, its named beats, its elements and the state it must start and end in.

## What each fragment records

Beside its scene, each fragment keeps a boundary record, measured from **its own render**, never
from what it meant to build:

```
boundary:
  t0: { elements: [{id, box, scale, rotation, opacity}] }
  t1: { elements: [...] }
shared:      # motions it believes reach past its own window
  - {id: "feed-scroll", channel: position, window: [a, b], carries: [ids]}
handoffs:
  - {object: "hero", leaves_as: {box, scale}, at: t, becomes: "chip1"}
assumptions: [ "the bar rests at y=642, measured in F3" ]
```

- **Measure the render, not the intent.** Track your own render at the boundary, so the two sides of
  a seam are compared like for like.
- **Never invent a shared motion inside one fragment.** If an element moves because its container
  does, record it under `shared` and animate the container.
- **Write down every assumption** about a neighbour's state, so it can be checked.

## Joining

1. **Check each seam.** The end of one fragment against the start of the next: position within
   about 3 px, scale within 1%, the same elements. A mismatch is a real defect. Measure the
   **reference** at that moment again and fix the fragment that departs from it; never split the
   difference between the two.
2. **One shared motion, once.** Matching `shared` entries from several fragments become one track
   on one container, and the copies on the elements are deleted. Duplicated curves look right in
   each fragment and drift apart in the whole.
3. **Wire each handoff** as one layer that runs across the boundary, or a swap on one frame. Never a
   crossfade, unless stills either side show the reference fades.
4. **Confirm each assumption** against the reference or the neighbour's measured boundary. One
   that does not hold sends that fragment back.

## Checking the whole clip

A fragment that matches on its own says nothing about the joined clip. Over the whole reference:

- `picsart_media_flow_diff` with `fps: "auto"`, which scores each fragment and the seams between
  them;
- `picsart_media_track_motion_diff` on each shared motion;
- `picsart_media_inventory_diff` at 3–5 moments per fragment;
- stills 0.2 s either side of every seam, looked at.
