# Text/media carousel: words, convergence, occlusion, cut

## Contents

- Copy and timing
- Ownership and path
- Executable controlled validation

Use `scene://text-media-carousel` for a complete headline/media sequence, not a
generic text animation. This is independently authored scene, not imported
Hyperframes HTML, assets or exact pixel parity. Describe the template before binding.
`words` and `cards` are variable lists; empty words omit the first title and empty
cards retain typography. Later card records paint on top. `reverseSlots:true`
reverses path-slot/convergence assignment, not list paint order.

## Copy and timing

Measure each requested word as a standalone, unwrapped text layer using the chosen
fontFamily/fontWeight/fontSize and `picsart_scene_query_layout`. Use its box width divided by
fontSize for `widthEm`; supply `{text,widthEm}` records. Do not use character count.
Remeasure after copy, family or weight edits. Widths are authoring inputs, not live
auto-fit. Each word's clipping window and horizontal placement derive from those
widths plus `gapEm*fontSize`. A 1px wrap-threshold guard accommodates rounded query
widths; it does not resize the word or repair an inaccurate measurement. Query the
resulting ink height and inspect masks, especially for accents or a different font.

For N words, calculate these **local** times:

- last word start = `max(0,N-1)*wordStagger`;
- shrink start = last word start + `holdDuration`;
- hard cut = shrink start + `shrinkDuration`;
- duration = cut + `outroDuration`.

Convergence starts at last word start plus **slot index / card count × `convergenceStagger`**.
Each card converges for `convergenceDuration`. Changing count changes these slots;
it does not automatically lengthen the hold. Ensure the last word has revealed and
the last card has converged before shrinking when the brief needs a settled hold.
Card squeeze starts `imageDelayFraction*shrinkDuration` after headline shrink.
The cut is intentional: first title/cards stop, then the second title settles
from `outroScaleFrom` to 1. Sample immediately before, at and after the cut.

## Ownership and path

Headline copies share widths and timing. One sits below cards; the other is masked
to the left half above cards. Shared drift and shrink belong on their owners, not
duplicated per-word tracks. Each word owns its reveal mask and ink. In scene a
mask clip has its own transforms in the host composition's space; moving only ink
must not move its clipping window. Preserve that hierarchy when detaching/editing.

`pathKeys` is a vec2 keyframe list over [0,100], with relative spatial tangents.
`phase.rotation` carries turns and is sampled modulo 1, independently of video time.
The list constraint checks keyframe structure and the time domain, **not closure**.
For continuous wrap, match first/last positions and inspect approach/departure
direction and speed. An open curve jumps at the seam: this template has no endpoint
fade. Use the open-path carousel guide for intentionally hidden resets instead.
Depth scale is projected 2D, not perspective or automatic front/back sorting.

## Executable controlled validation

This diagnostic uses deliberately generous word boxes, a stationary solid card
and no drift, isolating painted occlusion from photo texture and circulation. It
does not demonstrate accurate word measurement or real-video playback. Apply with
`picsart_scene_apply_template`, retain its scene, then strict `picsart_scene_validate`.

```json
{"uri":"scene://text-media-carousel","mode":"bootstrap","parameters":{"width":800,"height":600,"fontSize":40,"driftDistance":0,"gapEm":0,"words":[{"text":"LEFT","widthEm":4},{"text":"RIGHT","widthEm":4}],"cards":[{"width":500,"height":120,"content":{"kind":"color","color":"#ee6644"}}],"pathKeys":[{"time":0,"value":[400,300]},{"time":100,"value":[400,300]}],"phase":{"rotation":{"expression":"return 0"}},"convergenceFrom":1,"zoom":1,"globalScale":1,"scaleDepth":0}}
```

Use `picsart_scene_query_layout` to locate the actual IDs. Standalone wrappers are
`title-below__window__drift__word_0` and `...__word_1`; their ink ends in `__ink`.
Media is `cards-owner__unit_0__card__surface_0`; `outro` is the second title.
Inline placement, reference nesting and detaching can add prefixes. Query the final
host rather than guessing. For start S and speed V, map local t to root `S+t/V`
(also account for any authored trim). Rebase dimensions for host scaling.

The following contract records the diagnostic scene's intended geometry. Run it with `picsart_scene_check_contracts` and read each verdict:

```json
{"version":1,"timeSpace":"root","contracts":[{"id":"left-window-center","window":{"start":1.2,"end":1.201,"step":0.01},"assert":{"kind":"motion_range","target":{"id":"title-below__window__drift__word_0"},"channel":"centerX","min":319.99,"max":320.01}},{"id":"right-window-center","window":{"start":1.2,"end":1.201,"step":0.01},"assert":{"kind":"motion_range","target":{"id":"title-below__window__drift__word_1"},"channel":"centerX","min":479.99,"max":480.01}},{"id":"outro-center","window":{"start":2.6,"end":4.6,"step":0.1},"assert":{"kind":"motion_range","target":{"id":"outro"},"channel":"centerX","min":399.99,"max":400.01}}]}
```

This motion record requires monotonic headline shrink in the continuous window, excluding the hard cut. Run it with `picsart_scene_check_motion` and report the checked window, without claiming continuous-time or pixel smoothness:

```json
{"version":1,"timeSpace":"root","fps":30,"window":{"start":1.9,"end":2.59},"checks":[{"id":"headline-shrinks","kind":"velocity_range","target":{"id":"title-below"},"channel":"width","min":-2000,"max":0}]}
```

The following two illustrative pixel records specify left ink over the red card and an unchanged right crop before its word appears. Pixel records have no automated checker; inspect full-resolution frames at the declared moments; leave exact numerical equality unverified. These expectations fit only this controlled stationary scene, not arbitrary changing photos or video.

```json
{"version":1,"times":[1.2],"checks":[{"id":"left-ink","kind":"ink_presence","region":[240,250,160,100],"foreground":[17,17,17],"background":[238,102,68],"colorTolerance":16,"minPixels":200,"maxFillFraction":0.5}]}
```

```json
{"version":1,"times":[0,1.2],"checks":[{"id":"right-stays-covered","kind":"region_stability","region":[410,250,180,100],"pixelTolerance":0,"maxChangedFraction":0}]}
```

Negative controls: move the outro 100px horizontally to fail its center contract;
or set `foreground:false` on the `title-above` reference's parameters to remove
the half-mask and fail right-region stability. Restore the scene and rerun the
**same** checks; do not widen tolerances. Pixel analysis requires host rendering
and its Python analysis dependency; unavailability is not a pass.

For the real customized scene, query word spacing/one-line height, convergence,
the full shrink window and cut activity at `cut-1/fps`, `cut`, `cut+1/fps`.
Run `picsart_scene_lint_layout` over those phases; interpret designed card overlap/off-canvas
arrival explicitly. Inspect rendered word reveals and both sides of the occlusion.
Geometry/z-order alone cannot prove painted clipping. With video, hold phase and
check a fixed card at two times for advancing footage; a moving box is not proof
of source-clock advancement. Render/watch the final video and distinguish these
checks from sampled stills. Keep unsupported or unexamined cases in the handoff.
