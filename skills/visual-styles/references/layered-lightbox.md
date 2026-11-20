# Layered lightbox

A shadow box lit from behind: several paper sheets cut to silhouettes stand one behind another, each darker and
more opaque than the one behind it, and the back is a bright, cool glow. Windows in the front sheets burn warm. It is
a lit paper model, not a flat parallax scene and not a glow effect over a picture.

## Palette and colour roles

| Role | Colour | Its one job |
|---|---|---|
| ground | `#0b1014` | the dark of the box behind everything |
| field | `#cfe3ea`, `#6d93a8`, `#2f4656`, `#10171d` | darkness steps, back to front: depth is how dark a sheet is |
| accent | `#ffb347` | warm light on windows only, never a sheet or the lettering |
| highlight | `#fff0c8` | the hot core of a window and of the moon |
| line | `#05090c` | cast shadows between sheets |

Value is the depth cue: a nearer sheet is always darker than the sheet behind it. Warm is spent only on light sources.

## The medium

- Each sheet is one flat cut-out silhouette in its value, opaque.
- Between sheets sits a soft cast shadow: a copy of the nearer sheet in the shadow tone, blurred and moved a few px
  up, softer for a bigger gap (blur 20, 12, 6 px for the three sheets in the proof; ours, tune by render).
- Depth blur: the farthest sheets are blurred a little more than the nearest, by a blur key per sheet.
- A window is a warm fill with a hot core and a wide halo (two radii), laid over the front sheet where it is cut; it
  flickers by a few percent on a slow cycle.
- Written lettering is cut from the front sheet: its colour is the front value and it is revealed by a mask that grows
  from the left edge.

## Rates

| Held rate | Root rate |
|---|---|
| none | everything: sheets, windows, flicker, camera |

## Boil

Nothing boils; sheets are clean paper. The only constant motion is the slow window flicker and the camera's drift.

## Line width under a zoom

There are no outlines; edges are the silhouette. A camera push scales each sheet, so shapes grow with it.

## Motion habits, and the transitions

- Sheets arrive from the back to the front, each rising 160 px into place on a back ease (0.45 s), 0.25 s apart.
- A window lights by popping (scale 0 to 1.2 to 1 in 0.3 s), one after another.
- The camera is a dolly: from 2.4 s each sheet is its own composition scaled by its own factor about the lit point
  (1.04, 1.1, 1.22 and 1.35 from back to front) with a small sideways drift in step, so the sheets separate. No fades.

## Type

One short line cut in the front value, a heavy condensed face at 100 px, revealed left to right; keep it over the bright
back sheet so it reads.

## Scene features used

Closed paths with `fill`, `gaussian_blur` (its `blur` value) per layer, nested `composition` layers scaled as the
camera, `mask.clip` with a growing rectangle, scale keys for pops and flicker, `timeMode: "layer"`.


## Frame checklist (on top of [FRAME.md](FRAME.md))

1. The sheets get darker from back to front, never out of order.
2. Each sheet has a cast shadow on the one behind and the gap sets its softness.
3. Warm appears only on lights.
4. The dolly separates the sheets by different scale factors.
5. The lettering reads against the sheet it sits on.

QC: lean on the viewer's pass at normal speed (do the sheets read as a stack), the value order on a contact sheet and the lettering contrast.

## Build with the tools

Build each sheet as a shape layer with its shadow copy beneath it; give the windows their halo, fill and core layers. Wrap
each sheet's layers in a nested composition so the camera can scale it separately, and key the dolly on those
composition layers. Check the value order and the shadows on a contact sheet.

## Do / don't

- **Do** keep the front sheet nearly black so the windows are the brightest warm thing.
- **Do** let the back glow be the brightest value in the frame.
- **Don't** add outlines, a gradient fill on a sheet or a fade.
- **Template rules, this style's choices** (the rules every recipe holds):
  - Rate split: everything runs at the root rate; nothing is held.
  - Nothing fades: sheets rise in, lights pop, lettering is revealed by a growing mask.
  - Height is shadow: the soft cast shadow between sheets, softer for a bigger gap.

## Originality guard

Design your own scene, sheets and wording. It must not copy a known paper-lantern or shadow-box artist's work. Darkness as depth, light from behind and the dolly that separates sheets are the style.

## Proven on

A 5 s portrait clip (1080 by 1350, 24 fps) of two shots: a bright sky sheet with a moon, hills, a forest ridge of small pointed trees and a
dark cabin rise into place with their cast shadows, two windows ignite and flicker; then a dolly in on the cabin with
the sheets separating while a line of lettering, kept clear of the moon, is revealed on the sky; exported on the hosted renderer.

**Not proven:** true holes cut in a sheet (the windows are lit shapes laid over the front sheet), a mottled paper
texture inside the glow, a per-sheet radial gradient on the lit sheet, and a stagger across many sheets.
