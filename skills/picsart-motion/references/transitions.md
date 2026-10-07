# Seam transitions — the fallback, not the primary path

> **A transition SYSTEM, varied with intent — never a per-seam grab-bag, never mechanical sameness.**
> Across a sequence, establish **one** base transition (the grammar that reads as intentional) and
> vary it **deliberately, only where the content earns it** — a hero reveal, the CTA, a real
> beat/time/place change. A *different* transition on every cut is **noise** (the amateur tell); the
> *same* transition on every cut is **monotone**. Aim for a consistent base with a few earned accents.
> And a transition is **not the default connective tissue**: between clips the default is a **hard
> cut**, or **motion that carries continuity** (a matched move, a continuous camera across the set, a
> staggered reveal). Add a transition for a *reason*, and **never add transitions the designer didn't
> ask for** — a transition is a decision to *propose*, not a default to sprinkle. Ten similar photos
> want one coherent treatment with maybe one accent, **not ten transitions**.

In this skill, **matched-element smart-animate is the primary "transition"**: where a
layer carries a `matchKey` into the next frame, it *animates from its state in A to its
state in B* (see `picsart-motion-design`), and the shared chrome stays on screen — that is what
makes the interface *move* rather than cut. A plain seam transition is used only when:

1. **No matched layers — but check the RELATIONSHIP first; both cases happen.**
   ("Matched" means tagged with the same `matchKey` at import — a *semantic* identity
   judgment ("this is the same button/header in both frames", even if its position, size or
   text changed), **never** raw id equality: Figma node ids differ across frames by
   construction. Before concluding "nothing is shared", re-check the import tagging — an
   untagged shared element is an import gap, not a transition case.)
   - **The frames are related without sharing layers** — B is a **zoomed-in part of A**, a
     pan/crop of the same scene, a detail view of a region. No `matchKey` matches, yet the
     right motion is a **camera move**, not a transition: scale/translate A's whole view
     *into* B's framing (a continuous push-in/zoom to that region), so the cut reads as one
     continuous shot. Author it as a transform animation (`patch_scene` on the frame's
     transform, or the camera/`zoom_through` family given its natural window).
   - **The same page at a different scroll offset — a SCROLL, and often across several frames.**
     When two or more consecutive frames are the **same layout shifted along one axis** (same
     layers, content translated up/down or sideways, previously off-screen content now in view),
     the designer drew **keyframes of one scroll**, not separate screens. **Author it as ONE
     continuous scroll** — a single scrolling layer/content moving through those offsets — **not as
     two/three frames each with its own entrance, hold, and transition.** Critically: **do not stop
     or hold on the intermediate positions** — a scroll is about *continuity*; stopping on each drawn
     waypoint breaks the motion and adds dead air. Hold only where the scroll is meant to pause — the
     start, a focal item it lands on, the end — and let it flow through everything between (ease/
     flick-and-settle; speed is content-driven — `picsart-motion-design`'s *Scroll speed is content-driven*).
     Detect it the same way as the zoom case: test whether **B is A translated** (same content, a
     positional offset). **Treat the whole run as ONE unit of content, however many frames it spans**
     — 2, 3, 4 or more consecutive same-page offsets collapse into a single scroll (one scrolling
     layer, one gesture, one approval span), never N separate frames with N−1 seams and holds. Before
     authoring, scan forward: if frame k, k+1, k+2, … are the same page scrolling, group them and
     animate the group as one continuous move, then resume normal pairing after the run ends. **How
     many frames belong to the run, whether it's genuinely one scroll or actually separate screens,
     and where it should pause are per-case judgments** — read them from the diff facts, not a fixed
     rule, and confirm on the played result.
   - **A connective through-line runs off A's edge and continues into B — ONE WORLD CANVAS,
     the camera travels the line.** Some content **exits one edge of A** (a drawn stroke, a road
     or river in a photo, a ribbon, a path, a baseline of type, a shape's contour — **any content,
     not only a literal vector**) and matching content **enters an edge of B**. Test whether a single
     2D **offset** — translate B relative to A — makes that crossing content **continuous** across the
     seam: its **position lines up** (A's off-edge point coincides with B's on-edge point) **and its
     direction is preserved** (the flow/heading carries through — for a literal line this is the
     *endpoints and tangents meet* test; for general content it's "the off-edge feature of A registers
     1:1 with the on-edge feature of B under that offset"). **If it passes, A and B are not two screens
     — they are two windows onto one larger canvas.** Author it that way: lay both frame-compositions
     into **one world canvas** at the computed offset, then **travel the viewport along the
     through-line** — **but NOT with `composition.camera`: a pan-only camera (position change, `zoom`
     unchanged) is a no-op in the scene player.** Use the **empty-"world"-layer rig** instead: parent
     everything to one `empty` layer and **animate that layer's `position`** (the world slides under a
     fixed viewport = the pan you wanted), and animate the line/content **drawing on in sync with the
     move** (trim-path/stroke reveal) so it appears **drawn as the viewport travels it**. Full recipe
     + the line/photo conventions in **§"Recipe — the connected-canvas rig"** below. No cut, no
     transition — one continuous traveling shot. **This is not the scroll case above:** scroll re-shows the *same* page
     translated; here the frames hold *different* content that a connective line stitches into a bigger
     picture. **It chains past a pair** — if each successive seam passes the same offset test, three,
     four or more frames **tile into one canvas** and the camera travels the whole chain as a single
     gesture (one approval span, like the scroll run). How many frames belong to the canvas, and the
     exact offset, are read from the geometry, not guessed — confirm on the played camera move.
   - **B is the same frame as A with highlighted part(s)** — an emphasis state: one or more
     elements spotlighted, the rest dimmed (or an annotation/callout added). **No seam at
     all**: hold the frame and animate the emphasis *in place* — the dim/overlay fades in,
     the highlighted element(s) get a subtle pop/scale/glow (staggered if several), the rest
     holds still. A transition here would read as a page change when nothing changed.
   - **The frames are genuinely unrelated** — two frames are never identical, so here a
     seam transition **is the appropriate move**: `slide`, `crossfade`, `push`, or another
     from the set below, chosen to match the cut's direction and energy. When the layers
     are available, **elevate it** with per-element motion on top — A's elements *exit*
     (staggered, by role) and B's elements *enter* (staggered, by role) over the
     transition — so the cut reads designed rather than slideshow-flat; but the transition
     itself is a legitimate choice for an unrelated pair, not a failure.
2. **The flat-frame fallback** is in play (a rasterized design, no layers) — the whole
   frame is one image, and a seam transition is all that is possible. This is the slideshow
   path, labelled as such. (The zoom-relationship check still applies even here: two flat
   frames where B is A's detail can zoom rather than dissolve.)

So reach for these deliberately, not by default. If two frames share elements and you're
choosing a crossfade, you're building a slideshow.

## Recipe — the connected-canvas rig (camera follows a drawing line)

The working build for the world-canvas case above. The **`composition.camera`
cannot carry a pure pan in the scene player** — a position-only camera does nothing — so the pan is faked by
moving the world under a fixed viewport:

1. **One empty "world" layer, everything parented to it.** Add an `empty` layer sized to the whole
   canvas and parent every frame-composition/line/photo to it. Animating the world's `position`
   slides the whole canvas past a fixed viewport — this *is* the camera pan (`composition.camera`
   won't; see [`engine-gotchas.md`](engine-gotchas.md)).
2. **Camera-follow keyframes on the world layer.** Keyframe the world's `position` so the viewport
   tracks the tip of the line as it draws — the through-line stays in frame the whole travel.
3. **Trim-path draw-on for the line.** Animate the stroke's `trim.end` 0→1 (a shape-item keyframe —
   local clock, see `engine-gotchas.md`) so the line *draws* rather than appears.
4. **Matched accel/decel across the seam so there's no pause.** Give the first segment an
   **accelerating** curve and the second a **decelerating** one, with **matched lengths and
   durations**, so the motion carries through the join at constant speed instead of stopping — the
   Vector Law (below) applied to one continuous line.

**Line & photo conventions for this rig (each prevents a visible bug):**
- **Connectors sit BELOW the photos** (lower z), so the line's tip ends **cleanly at the photo's
  border** instead of crossing over it.
- **A photo the line is ARRIVING at must NOT scale on entry** — a growing/edge-anchored scale makes
  the photo **overlap the line**, and stills hide it; only the played motion shows it (see
  [`motion-troubleshooting.md`](motion-troubleshooting.md)). **Fade it in instead, timed to the
  tip's arrival.**
- **A trim-path draws from the path's FIRST point** — check the first vertex sits at the element the
  line should start *from*. A path authored in reverse **draws backwards**; fix the vertex order,
  don't flip the trim direction blind.

## The useful set, with natural durations

Set `transition` and `transitionDuration` where the montage fallback applies; `""` is a
hard cut.

mp-scene ships **17** transitions; resolve the live set + params from `get_capabilities`.
The everyday ones:

| id | What it does | Window |
|---|---|---|
| `""` (hard cut) | no blend — legitimate for fast-cut energy | n/a |
| `crossfade` | linear opacity blend | 0.3–0.6s |
| `blur_dissolve` | crossfade through a blur | 0.5–0.8s |
| `slide` (`direction`) | source slides out, destination enters from the opposite edge | 0.3–0.6s |
| `push` (`variant`) | both move in one clean shove | 0.3–0.6s |
| `diagonal_slide` | slide along a diagonal | 0.3–0.6s |
| `zoom_through` | punch toward the viewer, destination grows in — punchy | 0.3–0.5s |
| `iris` | circular wipe open/closed | 0.4–0.7s |
| `shape_reveal` | destination revealed through a shape mask | 0.4–0.7s |
| `page_curl` / `card_flip` | page/card turns to the next screen | 0.4–0.8s |

Stylized / high-energy (use sparingly, for a deliberate beat): `bubble`, `cubes`, `free_fall`,
`kaleida`, `manga_page`, `splatter`, `movement_camera`.

For a UI-walkthrough ad, `crossfade`/`blur_dissolve` (subtle) and `slide`/`push`/`diagonal_slide`
(directional, matching a scroll or navigation) cover almost everything the fallback needs.
Reserve the punchy `zoom_through` and the stylized set for a genuine emphasis beat.

## Two duration facts (not guesses)

- **Matte/animation-driven transitions have an authored length** and read as a glitch when
  starved of it — a 3-second choreography crammed into 0.4s is not a fast version of the
  effect, it's a broken one. Give an animated transition its natural window or don't use it.
- **A directional `slide`/`push` should match the motion it stands in for** — if the next
  frame is "scroll down," a downward push reads as continuous; a random direction reads as
  a cut with extra steps.

The richer transition catalogue (shape reveals, camera whip, and their variants) is listed in
`get_capabilities` and authored through `patch_scene`, but it is rarely the right tool for
a motion-designed ad — matched-element smart-animate almost always reads better between two
real UI states. Prefer it.

## Seam continuity — matching velocity, phase and direction across the cut (the Vector Law)

*Whether* two frames read as one continuous shot or as two clips bumped together is decided
at the seam by **how the motion carries across it** — not by which transition id you pick.
This applies to **both** a matched-element smart-animate *and* a plain seam elevated with
per-element exit/enter motion. Four things must line up across the cut. If they do, the eye
never registers a boundary; if any one breaks, the cut reads as a slideshow bump even when
every individual animation is clean.

1. **Axis consistency — carry the motion on the same axis.** If A's elements exit along
   `x`, B's should continue on `x`; an exit on `y` continues on `y`; a scale-out continues
   as a scale-in. Do not answer a horizontal exit with a vertical entrance — the eye is
   tracking a direction and you broke it.

2. **Direction matching — never mirror.** Same axis *and* same sign. A leaves moving **−x**
   (drifting left, exiting the left edge) → B **enters from the right edge still moving −x**,
   so the whole picture keeps sliding left through the cut. B entering from the *left* moving
   **+x** is a mirror — it reads as a bounce-back, the single most common "cut with extra
   steps." (This is the formal version of the existing rule *"a directional slide should
   match the motion it stands in for."*)

3. **Speed equivalence — exit velocity ≈ entry velocity, via mirrored easings.** The layer
   must be moving at *roughly the same speed* on both sides of the cut. In MP Scene this is
   an **easing-direction** choice, because our easings *are* the velocity profile:
   - `ease_out` = fast→slow (fastest at its **start**), `ease_in` = slow→fast (fastest at
     its **end**), `linear` = constant, `ease_in_out` = slow at both ends.
   - So the outgoing layer's **final** segment should be **`ease_in`** (accelerating *into*
     the cut → fastest at the seam) and the incoming layer's **first** segment **`ease_out`**
     (fastest at the seam, then settling). Both fastest exactly at the seam → velocities
     match → the motion is continuous. Give both sides a **similar travel distance** over the
     transition window so the *magnitude* matches too, not just the profile.
   - **When a beat settles to REST instead of carrying through, the next beat starts from zero — so
     start it SLOW, never fast.** A fast scroll that eases to a full stop has parked the eye at
     near-zero velocity; launching the following animation fast from that rest is a whiplash that
     breaks continuity as surely as a mismatched carry (the "fast right after a slow settle" bump).
     Two clean options: either **don't fully stop** — carry the momentum through the seam (rule #3
     above) — or, if you do settle, **restart gently** (an `ease_out`/`ease_in_out` entry from the low
     speed you landed at, or a brief hold first). Reserve a fast move out of rest for a deliberate
     accent, not as the default next beat.
   - For a stronger, matched acceleration than `ease_in`/`ease_out` give, author a
     **`cubic_bezier`** on each side that are mirror images of each other (resolve the param
     shape from `get_capabilities`). There is no `expo`/`power4` token here — reproduce the
     steepness with the bezier control points.

4. **Phase alignment — the cut lands mid-motion on both sides.** The killer anti-pattern is
   **exit-to-rest then entry-from-rest**: the outgoing layer *decelerates to a stop*
   (`ease_out` into the seam) and the incoming one *starts from a standstill* (`ease_out`
   from the seam) — both at zero velocity at the cut, so there's a dead beat where nothing
   moves and the boundary becomes visible. Fix it by (a) the mirrored-easing rule above and
   (b) **overlapping the windows**: the incoming entrance must *start before the outgoing
   exit finishes* (offset its first keyframe earlier by the transition length), so at the
   instant of the cut both layers are in motion. No overlap = a dead gap = a visible seam.

**Z-axis / scale has its own sign rule.** A scale-out (zoom in, `scale` trending **up**)
must be answered by an entry that is **also** scaling up (grow-in) — that's a forward push,
one continuous dive. A receding exit (`scale` trending **down**) is answered by a shrinking
entry. **Never pair a receding exit with a grow-from-small entry** (or vice-versa): the pull
flips to a push mid-cut and the depth inverts. This is exactly what `zoom_through` does right
when both sides grow — and what it does wrong if you reverse one side.

Concrete defaults that satisfy all four (borrow, then tune on the preview): partial travel of
**~12% of the frame** on each side (≈±230px at 1920 wide) rather than a full-frame fly-through;
transition window **0.3–0.5s**; mirrored `ease_in` (out) / `ease_out` (in); windows overlapped
by the full transition length. Larger travel reads as a whip; smaller reads as a nudge.

**These are the *default*, not a mandate — a hard cut (`""`) is still legitimate** for
fast-cut energy, and a *deliberate* stillness-before-climax beat (see `choreography.md`)
intentionally violates phase alignment to land a payoff. The Vector Law governs cuts meant
to feel *continuous*; break it only on purpose, never by accident.
