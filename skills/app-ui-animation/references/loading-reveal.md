# Loading placeholders → readable content

Discover `scene://skeleton-reveal` using category `ui_widget`, tags `loading` and `reveal`,
reference policy `reusable`; describe before applying. This is an authored animation, not a
network-loading component. Use `ui-card` for a static card and `text-state-swap` for two
readable states. Use a fade on an existing layer if no placeholder structure is needed.

The placeholder and content share row count, pitch and padding. The surface and both states
live under one `card` owner; keep the terminal fade there. Do not replicate exits on the
labels. Place a scene reference with `fit:"none"` for pixel-sized geometry; bootstrap to
editable layers for structural changes. Re-resolve after parameter edits to update geometry.

## Parameters and clocks

- `rows`: an ordered list of strings, not a fixed three-item layout. Empty keeps only the
  surface. Validate list item types in the caller; generic list metadata does not enforce them.
- `cardWidth`, `padding`, `rowHeight`, `rowGap`, `fontSize`, `placeholderFraction`: layout.
  The card height is `2*padding + N*rowHeight + max(0,N-1)*rowGap`; canvas adds 16px on
  each side. Short one-line copy is intended. Wrapping does not grow `rowHeight` or auto-fit.
- `surfaceColor`, `placeholderColor`, `inkColor`: palette. Check contrast on the actual host.
- `loadingDuration` L, `revealDuration` R, `holdDuration` H: loading [0,L], crossfade
  [L,L+R], reading [L+R,L+R+H], shared exit for 0.3s, then a transparent 0.1s tail.

The loading pulse is one opacity cycle, not a gradient shimmer. This is an independent scene
adaptation, not imported upstream markup or a promise of matching its pixels.

## Validation after every edit

1. Validate structure and parameter resolution with `picsart_scene_validate`.
2. Query all actual row ids and boxes, including `card__surface`, `card__loading__bar_0`, `card__content__label_0`, rebased to host scope/root time.
3. Compare independent phase expectations: zero text opacity before L, full text and zero placeholders while reading, label containment/separation, shared exit opacity and transparent tail. Run them as a contract record with `picsart_scene_check_contracts`, or use supported lint relationships and explicit observations.
4. Examine output-frame opacity through reveal and fixed reading geometry as required. Use `picsart_scene_check_motion` at the export FPS; record the exact window checked. Pulsing is intentional only during loading.
5. Lint event windows. Allow only the named intentional state-owner overlap, rebased when nested. Geometry remains present through transparency, so overlap allowances do not waive opacity requirements.
6. Inspect full-resolution loading, reveal, reading and tail frames plus continuous playback. Pixel stability is not checked automatically; visual stability alone does not prove legibility.

For default parameters (592×200, 3.3s), a readable-row contract can start with:

```json
{
  "version": 1,
  "timeSpace": "root",
  "contracts": [{
    "id": "first-row-readable",
    "window": { "start": 1.4, "end": 2.9, "step": 0.1 },
    "assert": {
      "kind": "motion_range",
      "target": { "id": "card__content__label_0" },
      "channel": "effectiveOpacity", "min": 0.9999, "max": 1
    }
  }]
}
```

This one contract is not the complete check set. Generate per-row fit, separation and phase
checks from the intended request. Rebase windows and expected geometry after parameter changes.
Use negative controls without weakening intent: overflowing copy must fail fit, late reveal
must fail the agreed reading window, and independently drifting text must fail pixel stability.
Repair, rerun, and report analysis, pixel checks and visual inspection separately.
