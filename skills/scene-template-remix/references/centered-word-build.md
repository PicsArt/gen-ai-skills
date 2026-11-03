# Centered word build: arrival, reflow, reading hold

Use `scene://centered-word-build` for a variable-length phrase whose words enter
from the right and push earlier words left, centering each settled prefix. This is
a composition template, not a text animator to apply to an existing paragraph.
It is independently authored from Hyperframes kinetic-center-build concepts, not
imported HTML/JS/fonts/assets or exact pixel parity. Describe it before binding.

## Measure copy and preserve ownership

Supply `words` as `{text,widthEm}` records. Measure each word as standalone unwrapped
text with `picsart_scene_query_layout` using the requested family, weight and font size;
`widthEm = measured width / fontSize`. Remeasure after changing copy/family/weight.
The width is an authoring input, not automatic font measurement. The 1px wrap guard
only accommodates rounded measurements; inspect one-line ink height and punctuation.

`phrase` owns the shared fit scale. Word positions derive from the same width metrics
and arrival clocks, while each word's nested ink owns its fade/rise/scale/blur.
Keep that ownership when editing instead of writing unrelated tracks per word.
The final measured phrase is uniformly shrunk to `width*maxWidthFraction` if needed;
it never grows above the supplied font size. There is no minimum readability size:
query effective ink size, render, and adjust copy/layout/font size with the user's
intent preserved. The source's minimum-size floor is not reproduced. A long incoming
word can overlap prior ink during its entrance; adjust `entryOffset` or timing if
that is undesirable. Settled-prefix centering is not an all-times non-overlap promise.

For N>0, settled prefix k (one-based) begins at
`firstDuration+(k-1)*pushDuration`. The full hold begins at
`firstDuration+(N-1)*pushDuration`; scene duration adds `holdDuration`.
N=0 leaves the background for `holdDuration`. One word has only first entry and hold.
Timing grows with count, unlike automatic compression into the source's fixed
two-second sequence; choose explicit durations for a fixed-length brief.

## Executable diagnostic

This controlled example intentionally uses generous 40/80/40px metric boxes and
10px gaps to make the expected positions easy to calculate independently. These
are not measured widths to reuse for real copy. Apply with `picsart_scene_apply_template`
and validate the returned scene with `picsart_scene_validate`.

```json
{"uri":"scene://centered-word-build","mode":"bootstrap","parameters":{"width":800,"height":400,"fontSize":40,"gapEm":0.25,"firstDuration":0.5,"pushDuration":0.5,"holdDuration":1,"words":[{"text":"A","widthEm":1},{"text":"B","widthEm":2},{"text":"C","widthEm":1}]}}
```

Query actual ids/scopes before comparing. Standalone ink ids are `word_0__ink`, `word_1__ink`, `word_2__ink`. Independent expected centers: at local .5 seconds, x400; at1 second, x355/425; at1.5 seconds, x330/400/470; y200 throughout. The following contract record runs with `picsart_scene_check_contracts`; preserve expected values and read each contract's verdict:

```json
{"version":1,"timeSpace":"root","contracts":[{"id":"first-centered","window":{"start":0.5,"end":0.5001,"step":0.01},"assert":{"kind":"motion_range","target":{"id":"word_0__ink"},"channel":"centerX","min":399.99,"max":400.01}},{"id":"second-prefix-left","window":{"start":1,"end":1.0001,"step":0.01},"assert":{"kind":"motion_range","target":{"id":"word_0__ink"},"channel":"centerX","min":354.99,"max":355.01}},{"id":"second-prefix-right","window":{"start":1,"end":1.0001,"step":0.01},"assert":{"kind":"motion_range","target":{"id":"word_1__ink"},"channel":"centerX","min":424.99,"max":425.01}},{"id":"final-left","window":{"start":1.5,"end":2.4,"step":0.1},"assert":{"kind":"motion_range","target":{"id":"word_0__ink"},"channel":"centerX","min":329.99,"max":330.01}},{"id":"final-middle","window":{"start":1.5,"end":2.4,"step":0.1},"assert":{"kind":"motion_range","target":{"id":"word_1__ink"},"channel":"centerX","min":399.99,"max":400.01}},{"id":"final-right","window":{"start":1.5,"end":2.4,"step":0.1},"assert":{"kind":"motion_range","target":{"id":"word_2__ink"},"channel":"centerX","min":469.99,"max":470.01}}]}
```

The next two motion records require leftward travel during pushes and a settled hold at 30fps. Run each with `picsart_scene_check_motion`, report actual coverage, and add prior-word targets for longer copy; neither sampled geometry nor endpoints prove continuous-time or optical quality.

```json
{"version":1,"timeSpace":"root","fps":30,"window":{"start":0.5,"end":1.49},"checks":[{"id":"prior-word-pushes-left","kind":"velocity_range","target":{"id":"word_0__ink"},"channel":"centerX","min":-1000,"max":0.01}]}
```

```json
{"version":1,"timeSpace":"root","fps":30,"window":{"start":1.5,"end":2.4},"checks":[{"id":"first-held","kind":"velocity_range","target":{"id":"word_0__ink"},"channel":"centerX","min":-0.01,"max":0.01},{"id":"middle-held","kind":"velocity_range","target":{"id":"word_1__ink"},"channel":"centerX","min":-0.01,"max":0.01},{"id":"last-held","kind":"velocity_range","target":{"id":"word_2__ink"},"channel":"centerX","min":-0.01,"max":0.01}]}
```

The following illustrative pixel record specifies painted hold stability. Pixel records have no automated checker; inspect full-resolution frames and report what was seen; leave numerical stability thresholds unverified. Stability alone would not prove correct copy, legibility, centering or entry blur.

```json
{"version":1,"times":[1.6,2,2.4],"checks":[{"id":"painted-hold","kind":"region_stability","region":[0,0,800,400],"pixelTolerance":0,"maxChangedFraction":0}]}
```

Negative control: move `phrase` from[400,200] to[420,200], rerun the same contracts,
then restore it and rerun unchanged. The displaced version must fail. This checks
alignment detection; a uniformly displaced phrase can still pass motion/stability.

## Validate the actual customized host

Recalculate expected prefix positions from measured widths and gaps, then apply
the shared scale and host transform. Rebind actual IDs from `picsart_scene_query_layout`.
For start S, positive speed V and untrimmed content, local t maps to root `S+t/V`;
account for trim and additional nesting before using those windows. Query entrance,
each settled prefix, intermediate pushes and final hold. Check one-line heights,
opacity/visibility and horizontal/vertical positions, not just the owner's box.
Use `picsart_scene_lint_layout` for accidental overflow; interpret transient designed overlap.

Inspect entry, push and hold frames at full resolution and watch the assembled video for rhythm. Pixel assertions are not automated; visual inspection does not establish numeric ink centering or stability thresholds. Keep default and customized evidence separate. Empty/singleton input, unequal widths, narrower canvas, delayed/scaled placement and changed playback rate need their own evidence.