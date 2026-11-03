# Motion rules and verification

## Contents

- Rigid vs independent — the rule that breaks most beats
- Fade must ride the motion
- Flat frames: zoom yes, translate no
- Entry and exit
- Camera moves
- Brightness
- Per-character text
- Verification recipes
- Derive values; don't paste them

Worked detail behind the rules in the recipe. The numbers are illustrative of the *method*, not
values to copy. Every code block below is for where you can run code; without it, check the same
property with `picsart_scene_query_layout`.

## Rigid vs independent — the rule that breaks most beats

Decide, per beat, whether the moving thing is **one object** or **many**:

- **Independent objects** (a grid of tiles, stickers being placed one at a time) — stagger their
  position and scale. The stagger *is* the effect.
- **A rigid object** (a card with a title, a wordmark lockup, a page with its logo) — every part
  must share **one** scale/position clock. Stagger the *fade* if you want a build.

Staggering a rigid object's geometry makes its parts drift out of register mid-flight: a card's
title visibly overflows its panel while both are still animating. Where you can run code, pin it in the generator:

```python
geom_t0 = {l["animations"]["scale"]["keyframes"][0]["time"] for l in parts}
assert len(geom_t0) == 1, "parts do not share one scale clock — they will drift"
```

## Fade must ride the motion

Two curves that end at different times read as two events — "a fade, then a move". Make them
co-terminous **and** give them the same easing. Measuring both as percentages of their range is the
check: at each sample the fade % and the motion % should track within a few points.

A fade that finishes at 55% of the travel is the classic symptom. Neither speeding it up nor
slowing it down fixes it; only co-termination does.

## Flat frames: zoom yes, translate no

When a beat is built from whole-frame renders rather than separate elements:

- **Zoom-in is safe** — scaling up never exposes an edge.
- **Translate is not** — moving a canvas-sized image exposes its own trailing edge, and whatever is
  behind sits at different positions, so the seam merely moves rather than disappearing.

Stitching two frames' bands into one long strip to fake a slide fails when the frames differ in
anything but position (a lighting or z-order difference between them shows as a hard seam at the
join). If a beat is a translate *plus* a state change (a slide **and** a spotlight), a flat frame
cannot carry both — either rebuild the beat from elements or ship the state change alone and say so.

## Entry and exit

- **Size entry travel** so the leading part starts just off-canvas: `travel ≥ canvas_width − leftmost_x`.
  Assert both bounds — too short means it begins on screen, far too long is dead time.
- The incoming content must be **substantially on canvas before the outgoing content has left**, or
  there is a black hole between scenes. Assert `in_start + in_span/2 ≤ out_end`.
- **Exits accelerate**: `ease_in` (slow to break away, then whipping). For differential
  acceleration give two objects different starts *and* different spans — a lighter object leaves
  first and crosses in less time.
- A reveal can avoid animating a corner radius entirely: grow a rounded window until its corners
  pass outside the canvas. Size it `≥ canvas / box` and the rounding simply leaves the frame.

## Camera moves

A camera move scales **and** translates. Remap positions through the pivot:

```python
def cam(pos, z, C):        # C = pivot, z = zoom factor
    return [C[0] + z*(pos[0]-C[0]), C[1] + z*(pos[1]-C[1])]
```

Without the translate every element shrinks where it stands, which reads as deflating rather than
receding. An element already *at* the pivot only scales — that is expected, so assert
convergence only for off-pivot elements.

To hand one scene to the next through a shared element, anchor the incoming layer **on that
element's own slot** and start it scaled so the slot lands exactly on the outgoing element. The two
are then coincident for the whole move, so the crossfade between them is invisible at any moment —
which is what frees the fade to ride the motion instead of having to finish first.

## Brightness

Opacity composites in **linear light**, so matching a measured brightness needs a gamma conversion:

```python
def s2l(v):                      # sRGB 0..255 -> linear
    v /= 255.0
    return ((v + 0.055)/1.055)**2.4 if v > 0.04045 else v/12.92

opacity = s2l(target_lum) / s2l(source_lum)
```

The naive sRGB ratio can be off by 5×. And opacity only *darkens* over a black background — over a
light backdrop it lets the backdrop through and makes a dark subject lighter. A real dim there is a
dark scrim on top.

If an asset's export already carries the design's dimming, use it and animate nothing.

## Per-character text

A text layer's `content.animations[]` pairs a per-glyph `transform` (`opacity`, `offset`, `scale`,
`rotation`) with a range `selector`:

- `basedOn: "character"`, `shape: "square"`, `smoothness: 0` for a hard blink rather than a breathe.
- `randomizeOrder` + `randomizeSeed` turn a sweep into a flicker. Stack several entries on
  **different seeds** so they never beat in lockstep.
- `offset` slides the active span `[start + offset, end + offset]` — the park/clear/full-ramp
  formulas depend on `start`/`end`/the shape, so don't guess them here. See
  `textAnimationAuthoring.rawSelector` in `picsart_scene_capabilities` for the exact math and worked
  numbers.

Verify per-glyph behaviour by splitting the text band into columns and confirming they vary
*independently* — the within-frame spread across columns should change frame to frame. Note that
equal-width columns do not align with proportional glyphs, so treat a persistently dark column as a
measurement artefact rather than a stuck glyph.

## Verification recipes

| question | cheapest answer |
|---|---|
| does the geometry match the design? | `picsart_scene_query_layout` at a time, compare boxes to the Figma numbers |
| is anything on canvas throughout? | `picsart_scene_contact_sheet` at the suspect times, `resolution` set to the scene size |
| did this element actually move? | track its distinctive colour's centroid across frames |
| does the crop match the design? | mean absolute difference against the Figma frame render |

**Do not judge position from a downscaled contact sheet.** It reliably suggests errors that
measurement disproves; two such false alarms in one build is normal. Compare at full resolution.

Where you run a generator and one of its asserts fires after you extend the timeline, check whether the *assert* is stale before
"fixing" the scene: keyframe lists grow as later beats are appended, so an assert that reads
`keyframes[-1]` starts inspecting the wrong beat. Look the keyframe up by its time instead:

```python
def kf_at(track, t):
    return next(k for k in track["keyframes"] if abs(k["time"] - t) < 1e-9)
```

## Derive values; don't paste them

Every constant that has a relationship to another should be computed from it. A ratio pasted as a
literal silently stops matching when the source measurement is refined — e.g. a zoom factor
hardcoded from a rounded width no longer matches the box it came from. Prefer
`ZOOM = BOX_A[2] / BOX_B[2]` over `ZOOM = 1.64195`.

Rounding a single dimension can also break an aspect match and visibly squash a wordmark. Keep the
precise measured values and assert the two boxes' aspects agree.
