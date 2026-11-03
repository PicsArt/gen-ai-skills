# Kinetic promo: variable beats and bounded validation

Use `scene://kinetic-promo-story` for an editable multi-beat typography story over
one continuous background clip. This is an independently authored adaptation of
Hyperframes kinetic-type, not copied HTML, assets or pixel/timing parity. Its six
families are hook, panel, symbols, punch, editorial and outro. Stock typography,
symbols and fractional timing simplify the source's bespoke styling and staging.

Describe the template first. It is expand-only: bootstrap a new scene or inline
into a host, never reference it directly. Each `beats` record supplies `style`,
positive `duration`, `heading`, `subheading`, `eyebrow` and `accent`. Add/reorder/remove
records; the ordered track moves later beats and sums duration. Empty/malformed
records are refused. Background consumes a single clip's content, not its audio,
transforms or looks; give video sufficient source duration. One root layer avoids
restarting footage at beat boundaries. Panel copy/decorations share a moving owner.

Apply this request with `picsart_scene_apply_template`:

```json
{"uri":"scene://kinetic-promo-story","mode":"bootstrap","parameters":{}}
```

Retain the returned scene. Run `picsart_scene_validate` with strict validation. Query
default holds at 1.5, 4, 8, 10.8, 12.8 and 14.4 seconds. Read `active` as well as
`visible`: inactive authored layers can retain their visibility flag. Get actual
IDs from the query after nesting/inline edits; do not guess generated prefixes.

The following contract records two intended checks and a rotated-containment limitation. Run it with `picsart_scene_check_contracts` and read each verdict. Retain unsupported rotated containment as inconclusive; do not silently count it as success:

```json
{
  "version":1,"timeSpace":"root","contracts":[
    {"id":"panel-copy-fits","window":{"start":3.4,"end":4.7,"step":0.25},"assert":{"kind":"contains","anchor":{"id":"beat_1__beat-owner__panel-paper"},"members":[{"id":"beat_1__beat-owner__heading"},{"id":"beat_1__beat-owner__subheading"}],"paddingPx":40}},
    {"id":"panel-exits-together","window":{"start":4.835,"end":5.3,"step":0.03333333333333333},"assert":{"kind":"translation","anchor":{"id":"beat_1__beat-owner__panel-paper"},"members":[{"id":"beat_1__beat-owner__heading"},{"id":"beat_1__beat-owner__subheading"}],"tolerancePx":0.1}},
    {"id":"tilted-heading-containment","window":{"start":10.5,"end":11.2,"step":0.25},"assert":{"kind":"contains","anchor":{"id":"beat_3"},"members":[{"id":"beat_3__beat-owner__heading"}],"paddingPx":40}}
  ]
}
```

The following motion record expects a steady panel heading and full evaluated opacity on every output frame. Run it with `picsart_scene_check_motion` after querying the actual beat ids/windows; rotation and opacity cannot establish tilted-type translation or containment. Keep unsupported channels unchecked:

```json
{
  "version":1,"timeSpace":"root","fps":30,"window":{"start":3.4,"end":4.7},"checks":[
    {"id":"heading-holds","kind":"velocity_range","target":{"id":"beat_1__beat-owner__heading"},"channel":"centerX","min":-0.1,"max":0.1},
    {"id":"heading-opaque","kind":"value_range","target":{"id":"beat_1__beat-owner__heading"},"channel":"effectiveOpacity","min":1,"max":1}
  ]
}
```

The following illustrative pixel record expects white ink and hold stability on a controlled background. Pixel records have no automated checker; inspect the rendered heading at full resolution and leave numerical paint thresholds unverified. This does not prove all glyph containment, OCR, readability or aesthetics, and cannot turn inconclusive geometry into a pass:

```json
{
  "version":1,"times":[10.5,10.8,11.1],"checks":[
    {"id":"tilted-ink","kind":"ink_presence","region":[60,160,700,270],"foreground":[255,255,255],"background":[28,44,54],"colorTolerance":18,"minPixels":8000,"maxFillFraction":0.4},
    {"id":"tilted-hold","kind":"region_stability","region":[60,160,700,270],"pixelTolerance":0,"maxChangedFraction":0}
  ]
}
```

Rebase IDs, windows, expected geometry and pixel regions/colors after editing count,
order, copy, timing, palette, dimensions or placement. Video backgrounds invalidate
flat-color/still-region assumptions. Longer text is not automatically fitted:
measure it, preserve the requested copy, and adjust typeScale or edit the structure.
Making all secondary text tiny may satisfy containment without making it readable.

Use `picsart_scene_lint_layout` over holds and seams. The hook wipe is intentionally parked
off-canvas before entering; explain that exact layer/window, not all warnings away.
Render entrances, changes, holds and final black using `picsart_scene_contact_sheet` with explicit `times` and `resolution` equal to the composition dimensions; inspect
continuous video for pacing. Test placement/paint negatives, then repair the scene
and rerun unchanged assertions. Keep sampled geometry, frame-grid motion, pixel
evidence and unverified intervals distinct in the final report.
