# Motion principles — deciding how a static design becomes motion

These are the **judgment defaults** you apply when turning two static frames into motion. They
sit on top of **facts you read from tools** — never from the picture. The split, per the
`picsart-motion` skill's core rule:

- **What changed between frame A and frame B is a FACT** → read it with
  `picsart_media_diff_layouts` (which resolves both frames through `picsart_media_query_layout`),
  never eyeball it (§1 below).
- **Which motion fits that change is JUDGMENT** → this sheet (§2–§14), applied with the designer. Start from §13 (decide by *purpose*) and §14 (primitive vs semantic presets) — they frame everything below.

This reference adds the *decision procedure* and the pieces `picsart-motion-design` doesn't already
cover (frame-diff, magnitude→duration, reduced-motion, productive/expressive). It does **not**
restate the craft `picsart-motion-design` already owns — the role→motion table, stagger, depth, focal
ordering, and hold rules live there. Use both: derive *what* here, author *how* there.

**Companion references:** [`authoring-flow.md`](authoring-flow.md) — **the exact end-to-end flow
(Figma design → correctly-positioned layered video); follow it in order**; [`mp-scene-vocabulary.md`](mp-scene-vocabulary.md) — **the real
presets / looks / transitions / easings you actually author with; read it first, everything below
maps onto it**; [`motion-patterns.md`](motion-patterns.md) (scenario → recipe),
[`choreography.md`](choreography.md) (sequencing several elements in one beat),
[`motion-troubleshooting.md`](motion-troubleshooting.md) (symptom → fix when a pair feels off),
[`element-motion.md`](element-motion.md) (per-element: classify by type/role/importance → how it
moves), [`studying-motion.md`](studying-motion.md) (where to study real ad motion + what to look for).

> **How the frame diff is done.** §1 routes through `picsart_media_diff_layouts` — the dedicated
> tool that resolves both frames through one `query_layout` and returns the classified delta (a
> 7-class taxonomy + a whole-pair `relationship`) deterministically. Feed it the import `matchKey`s
> as `matchHints`. It hardens the hand-diff (match layers, subtract boxes, reconcile
> frame-relative→composition and centre-vs-top-left coordinates), which stays the **fallback** when
> the tool is unavailable. Either way the geometry is a **tool-read fact** — never substitute an
> eyeballed guess. One thing the tool does *not* see is numeric opacity (§1) — check fades yourself.

---

## 1. Decide WHAT moves from the frame diff — not by eye  *(the Figma practice)*

The industry-standard way from static → motion is: **diff two states, animate only what
changed.** (Figma Smart Animate: *"if a layer's properties stay the same between two frames,
Figma won't animate that layer at all."*) Do it from tool-read facts:

1. **Diff the two frames with `picsart_media_diff_layouts`.** Pass frame **A** and frame **B**
   plus the import `matchKey`s as `matchHints`. It resolves both frames through one
   `query_layout`, pairs the layers (hints → content `id`+`kind` → geometry, **never** by raw
   layer id), and returns each layer's **class** with root-space, centre-based deltas (`dPos`,
   `travelPx`, `dScale`, `dScaleXY`, `dRotation`, `dZ`) plus a whole-pair `relationship`
   (`shared-layers` / `zoom-detail` / `in-place-emphasis` / `unrelated`) that routes
   smart-animate vs camera vs cut. This is the fact source; take the geometry from here, never
   from looking at the render.

   **Fallback (tool unavailable).** Read both frames yourself — `picsart_media_query_layout`
   on A and on B — match by `matchKey`, then name/role, then geometry, and
   compute the delta as arithmetic on the tool-read coordinates (B.box − A.box). An untagged
   element that clearly recurs is an *import gap* — fix the tagging, don't treat it as unmatched
   (see `picsart-motion-import`). Eyeballing "the header moved up a bit" is not a substitute — it will be
   wrong about distance and boundaries.

2. **The classes** the diff assigns — matched pairs plus enter/exit:

   | Class | Condition |
   |---|---|
   | `unchanged` | matched, and box + content identical A→B |
   | `moved` | matched, position differs |
   | `resized` | matched, size differs |
   | `restyled` | matched, style differs (z-order / rotation / visibility) |
   | `content-changed` | matched, text/number/image content differs |
   | `entered` | present in B only |
   | `exited` | present in A only |

   **Opacity is a blind spot — check it yourself.** The diff reads only `visible` (a boolean),
   not numeric opacity, so a **fade** (a CTA fading in, a backdrop dimming to 40%, an overlay
   appearing) reads as `unchanged` and slips through. Fades are the most common ad motion — read
   authored opacity at A and B from the scene and treat a change as a `restyled` layer the tool
   didn't flag.

   **A transformed element is matched — never an exit+entrance.** If the same thing is present in
   both frames but moved, resized, restyled, or reworded — a title `AI` that becomes `AI Effects`,
   a headline that gains a word, a card that slides and shrinks — that changed transform **is the
   evidence it persists**. Classify it `moved` / `resized` / `content-changed` and **smart-animate
   it A→B**; do **not** let a present-in-both element disappear and reappear, and do **not** cover
   the seam with a frame transition when a layer is shared — that is the slideshow anti-pattern
   ([`transitions.md`](transitions.md)). If the diff returns `exited` + `entered` for what is
   plainly the same element, the `matchKey`/hint is missing — **fix the tagging** (see
   `picsart-motion-import`), don't animate the wrong story.

3. **The rule:** animate only the changed classes; **leave `unchanged` layers still.** Not
   animating is a decision — a frame where everything moves reads as noise (see §4).

4. **First ask if the whole pair is ONE camera move — the uniform-transform test.** Before you
   author shared layers as N independent smart-animates, check whether a **single uniform
   (scale + translate) about one pivot** explains *all* their deltas. It often does, and then the
   pair is a **viewport/camera change**, not per-element motion. `diff_layouts`' `relationship`
   hints this (`zoom-detail`), but `shared-layers` does **not** rule it out — a pair can share every
   layer *and* be one camera move. Test it from the tool-read deltas:
   - Take `s = B.size / A.size` of any one matched layer. If **all** matched layers share ~the same
     `s` and `s ≠ 1`, that is the first signal.
   - Solve the pivot once: `C = (B.center − s·A.center) / (1 − s)`, then **verify `C` against a
     second, independent layer** (push its A-center through `C + s·(A.center − C)`; it must land on
     its B-center to sub-pixel).
   - **Agrees across ≥2 independent layers → author the move ONCE, not per layer** — the "one
     push-in, not forty layer moves" construct in [`motion-patterns.md`](motion-patterns.md). Two
     equivalent ways:
     - **Composition `camera` — the default for a whole-frame zoom/pan.** Author it once on
       `composition.camera` as `{ position: pivot, zoom, rotation }` (each a constant or a keyframed
       track). It maps every layer `pos → pivot + zoom·(pos − pivot)` and `scale → scale·zoom` — the
       uniform transform, exactly. Set `position` = the solved pivot `C`; keyframe `zoom` `1 → s`.
       It applies to **all** top-level layers by default; opt a layer out with **`cameraExempt: true`**
       — needed for anything authored directly in the *final/zoomed screen space* (e.g. content that
       only appears **after** the zoom, like a grid that fades in at the end). One camera reproduces
       many layers' hand-baked zoom keyframes exactly and makes per-layer drift impossible. Fidelity:
       the camera is exact when its fields are constant, or when the layers are **static across the
       camera's animated window** (let intros finish first); an animated camera over animated layers
       resamples with bounded error.
       No `expression` or AE motion-path tangents on camera fields (fails loud).
     - **A wrapping parent / nested `scene`** — group the layers under one parent and animate the
       **parent's** transform; children inherit it. Prefer this when only a **subset** should ride
       the move (the wide "canvas" group zooms while a fixed logo/chrome stays put), and set the
       **parent's `anchor` to the solved pivot `C`**. **CAVEAT: an inline `scene`'s `composition` IS
       its raster size and clips to it** — a 9682px canvas inside a 1080 inner comp gets cropped, so
       a nested scene is the *wrong* tool for a wider-than-frame zoom; use the composition `camera`
       (host coordinate space, no clip) there. Reserve the nested-scene parent for a bounded group.
     Either way, layers whose delta does **not** fit ride *on top* — with a parent they simply keep
     their own local animation inside it (inherited zoom + independent motion compose for free); the
     camera/parent carries the rest.
   - **Prefer camera/parent precisely because baking the zoom as per-layer keyframes invites a
     per-layer bug.** If you must bake it per layer, transform **every** layer's `position` by the
     *same* point formula `new = C + s·(old − C)` — including left-aligned text (its anchor is a
     point like any other; a correctly-transformed anchor already lands the scaled glyphs right).
     Do **not** special-case a left-aligned text layer with a half-width "correction": subtracting
     an *unscaled* half-width shoves it off-frame while its neighbours land correctly.
     One layer whose zoom keyframe disagrees with the shared `(C, s)` is the tell.
   - **Reveal reading:** `s < 1` (everything shrinks uniformly) **and** matched layers that were
     off-frame/clipped in A are now on-frame in B → a **zoom-out reveal** ("scale down, more comes
     into view"); `s > 1` → a push-in. The reveal need not involve scale at all — a **pure pan**
     (`s ≈ 1`, shared translate) reveals the same way. **Even one layer can indicate a viewport
     change:** a layer **clipped by the frame edge in A that sits fully inside the frame in B** is a
     strong signal the *viewport moved to bring it in* — the edge-clipping is the tell, more than the
     raw position delta. It is an **indicator, not proof**, because a lone element sliding in from
     off-screen (a normal entrance) looks identical if you watch only that layer. **Disambiguate from
     context:** if nearby content shifts by the *same* vector, it's a pan/camera move (author it as
     one); if only that one element moves while everything else holds, it's an entrance, not a camera
     move.

   **Import signal for this case:** a frame whose *content bounding box is much larger than the
   frame* (e.g. a 9682px group inside a 1080 frame) is a **viewport crop of a bigger canvas** —
   expect its neighbours to be pans/zooms of it, and note this is why off-frame/clipped layers are
   **imported, not dropped** (`picsart-motion-import`): they are exactly the content the zoom/pan reveals.

   **The through-line variant — separate frames that tile into one canvas.** The bigger-canvas case
   above is *one* oversized frame cropped. But separate frames can *also* be windows onto one canvas:
   when content **runs off an edge of A** (a stroke, a road, a path, a ribbon, a type baseline — any
   connective line, not only a vector) and matching content **enters an edge of B**, test whether a
   single 2D **offset** makes that crossing content continuous (position coincides *and* direction
   carries — for a literal line, endpoints and tangents meet). If it does, tile the frames into **one
   world canvas** at that offset and travel the viewport along the line while it **draws on in sync** —
   a continuous shot, not a cut. **The pan is NOT a `composition.camera` move** (a pan-only camera is a
   no-op in the scene player); it's an **empty-"world"-layer rig** — parent everything to one `empty` layer and animate
   *its* position. Chains past a pair if each seam passes the test. Full rig + line/photo conventions
   in [`transitions.md`](transitions.md) §"Recipe — the connected-canvas rig".

## 2. Given a change, choose the motion + easing + direction

Easing is chosen by the element's **spatial role**, not by taste; direction comes from the delta
vector. (Sources: Material, Carbon, Apple HIG.)

| Class | Motion | Easing | Direction |
|---|---|---|---|
| `moved` (matched) | **smart-animate** the delta (position/size/opacity/content A→B) | `ease_in_out` | along the delta vector |
| `resized` (matched) | scale tween | `ease_in_out` | — |
| `content-changed` | value-change / crossfade / **type-on** for text | `ease_in_out` | — |
| `entered` (B only) | entrance — slide from nearest edge / fade / pop | **`ease_out`** (arrive & settle) | from the nearest edge |
| `exited` (A only) | exit — fade / slide out | **`ease_in`** (accelerate away) | toward the nearest edge |
| `unchanged` | nothing | — | — |

Ordering for a pair: **matched moves first, `exited` leaves as/just before the move, `entered`
arrives after the matched layers land** — so the eye follows continuity into the new content.
(This ordering + the role→motion mapping is detailed in `picsart-motion-design`; don't duplicate it —
follow it.) Easing values are authoritative from `get_capabilities`; canonical defaults in §8.

## 3. Duration from the magnitude of change

Bigger travel or scale → longer motion, but UI motion stays short. Anchors (Material v1):
**~200–400ms** typical; **>400ms feels too slow**; entrances a touch faster than on-screen
moves. Practice: a small nudge ~0.2s, a normal on-screen move ~0.3–0.4s, a large/full-screen
move up toward ~0.5s; matched smart-animate 0.4–0.8s (per `picsart-motion-design`). **Scale by energy**
(§6): energetic → the short end, calm → the long end. Never let a duration exceed what the
frame's hold covers (`picsart-motion-design`'s *Hold ≥ motion*).

**Also scale by the DESTINATION's content load.** A move into a **dense** frame (a grid, many cards,
lots of new elements) needs a **longer, wider-spaced stagger and a longer hold** than a move into a
sparse one — the viewer has to see everything, or at least the important parts, and a fast entry into
a busy screen reads as a blur. This can **override the energy register**: even at `energetic`, a
packed frame gets enough time to land. Legibility wins over snappiness (`picsart-motion-design`'s *Pace to
the destination's content load*). **But the page-change and the content reveal are separate clocks:**
when a seam is a UI action (a tap that *causes* the next screen), the navigation move itself should
be **fast/snappy** (app-like responsiveness), while the arriving page's *content* still paces to its
own density — fast nav in, then content that staggers in at the speed its element count demands.

## 4. One focal motion per beat  *(staging)*

Motion draws the eye, so spend it on **one** thing per beat, not everything at once. Rank the
changed layers by salience (size × contrast × hierarchy from the design) and lead with the
focal one; supporting elements follow, staggered. This is `picsart-motion-design`'s *one focal motion
per beat* + *stagger* — the diff (§1) just tells you which layers are candidates.

**Stagger budgets — how far apart siblings fire, and a ceiling on the cascade.** When several
siblings enter in one beat (a row of cards, list rows, nav items), fire them a fixed delay
apart, but cap the *whole* cascade so the beat still reads as one gesture, not a slow train.
Pick the tier by energy (§6):

| Tier | Delay between siblings | Whole cascade under | When |
|---|---|---|---|
| Micro | 20–40ms | ~200ms | tight, subtle — productive beats |
| Standard | 50–100ms | ~400ms | the default for most entrances |
| Dramatic | 100–200ms | ~600ms | expressive reveals, hero moments |

(`picsart-motion-design`'s existing 0.05–0.12s sits in **Standard** — this adds the cascade ceiling and
the neighboring registers.)

For sequencing several elements across a pair — the setup→action→resolution phases, sync
windows, depth ratios, and ready recipes (page transition, modal, list, grid) — see
[`choreography.md`](choreography.md).

## 5. Spatial continuity

Motion must obey the user's spatial expectation: a view that arrived by sliding down is
dismissed downward, not sideways; motion that defies physics disorients. The direction in §2
comes straight from the delta vector, which gives this for free. For pairs that *don't* share
layers (zoom-into-detail, in-place emphasis, genuinely unrelated), route per
[`transitions.md`](transitions.md) — a camera move or in-place emphasis, not a page-change
transition. (Source: Apple HIG.)

**Direction carries meaning.** Movement direction reads as intent, so let the design's meaning
pick it: **up** = growth/aspiration, **down** = settling/completion, **left** = departure,
**right** = progression/arrival, **scale-up** = emergence/importance, **scale-down** =
dismissal/removal. For a matched move the delta vector wins (continuity); for entrances/exits —
which have free direction — choose the one that matches the meaning.

**Name the motion category first.** Before picking a motion, name what the beat *does* —
revealing, concealing, transitioning, emphasizing, responding (to a simulated interaction), or
ambient. The category narrows the vocabulary before you reach for a specific move.

## 6. Energy = productive vs expressive

The motion **`energy`** register — inferred from the design at setup (no widget) — is a
productive↔expressive dial (Carbon's framework):

- **Productive** (routine, focused) — subtle, efficient, out of the way; short durations, clean
  eases, minimal decorative motion.
- **Expressive** (significant moments — an opening, a primary CTA, a hero reveal, or where the
  movement itself carries meaning) — more vibrant and visible; longer durations, more stagger,
  room for a pop/overshoot.

Match the register to the beat, not the whole reel uniformly. Energy scales the §3 durations and
the §2 easing register.

## 7. Coherence over variety — repetition with intentional accent

Variety is not richness. A reel where every element enters a different way, or every cut uses a
different transition, reads as **noise**, not craft — the amateur tell. The opposite failure is
**monotony**: the exact same move on everything, no accent. Good motion design lives between them:

- **Establish a small, consistent vocabulary** — one entrance family, one transition, one easing
  register — and **repeat it**. Repetition is what reads as intentional.
- **Break it deliberately, only where it carries meaning** — the hero reveal, the CTA, a genuine
  beat change. An accent works *because* the base is consistent; if everything is an accent, nothing is.
- **Variety must serve hierarchy, never decorate.** If a second animation doesn't mark something as
  more important, it's noise — cut it.

So: a consistent base + a few earned accents. Especially for a set of similar assets (e.g. ten
like photos), that means **one coherent treatment with maybe one accent — not a different animation
per item**. When unsure, do less: under-animating reads as calm; over-animating reads as cheap.

**Motion personality — pick one per reel (or per beat).** Rather than a bare
productive↔expressive slider, choose a named personality; it fixes the duration range, the
easing register, and how much overshoot is allowed, so motion stays consistent:

| Personality | Duration | Easing register | Overshoot |
|---|---|---|---|
| Corporate | 200–400ms | clean `ease_in_out`, no bounce | 0–3% |
| Premium | 350–600ms | slow, smooth (custom `cubic_bezier`, ≈ §8 Standard) | 0% |
| Playful | 150–300ms | `ease_out` + overshoot preset | 10–20% |
| Energetic | 100–250ms | fast `ease_out` | 15–30% |

Map `energy`: **productive ≈ Corporate / Premium; expressive ≈ Playful / Energetic.** These rows
say *which register to ask for*. **Overshoot is not an easing** — get it from the `scale_pop`
(single) or `spring` (multi) motion preset. Resolve the actual easing id / preset from
`get_capabilities`; see [`mp-scene-vocabulary.md`](mp-scene-vocabulary.md).

## 7. Reduced-motion — a paired low-motion variant  *(accessibility)*

Heavy parallax and large-object scale/pan are literal vestibular triggers (WCAG 2.3.3, MDN);
motion should never be the *only* signal. We ship video, so there's no runtime
`prefers-reduced-motion` — instead we can offer a **reduced-motion cut** as a deliverable variant
at Stage 5. The recipe (Apple's degrade-gracefully rule):

- **Decorative** motion (parallax drift, tap-pulse decoration, big scale-for-flair) → **drop it.**
- **Meaningful** motion (matched chrome carrying continuity, a state change, a hierarchy
  transition) → **don't remove — replace** the travel/scale with a **dissolve, fade, or color
  shift** of the same duration.

Classify each §1 change as essential-vs-decorative to build this: matched chrome & real state
changes = essential; pure entrances-for-flair, parallax, pulses = decorative. Keep the variant
**designer-initiated** (offer it; don't auto-produce it), like export and Drive-save.

The concrete transform for the reduced-motion cut: **remove spatial movement, keep opacity, drop
spring/overshoot, cut durations by 50%+, and never auto-play loops.** Two hard rules regardless
of the cut: **critical information is never carried by motion alone**, and any animation longer
than ~5s is pausable.

## 8. Easing — the real set, and custom curves

mp-scene's **named** easings are only `linear`, `ease_in`, `ease_out`, `ease_in_out`, `step`
([`mp-scene-vocabulary.md`](mp-scene-vocabulary.md)). For a specific feel beyond those, author a
**custom `cubic_bezier`** with control points — these reference curves (Material v1 / IBM Carbon)
are authored *as* `cubic_bezier`, they are **not** named ids:

| Feel | cubic_bezier control points | Use |
|---|---|---|
| Standard | `(0.4, 0, 0.2, 1)` | on-screen move / matched smart-animate |
| Deceleration | `(0, 0, 0.2, 1)` | entrances (§2 `entered`) |
| Acceleration | `(0.4, 0, 1, 1)` | exits (§2 `exited`) |
| Sharp | `(0.4, 0, 0.6, 1)` | temporary exit that may return |
| Carbon productive-standard | `(0.2, 0, 0.38, 0.9)` | subtle, efficient |

**Never name an easing from memory** — take the id (or confirm a custom curve is accepted) from
`get_capabilities`.

## 9. Guardrails — the quality checklist

Run before approving a pair. **CRITICAL** (never ship): linear easing on spatial movement ·
opacity-only for an important state change · a move >⅓ screen in one uninterrupted tween (add an
intermediate keyframe so it arcs) · a stagger cascade over 500ms · a cover layer (sticky header /
overlay) that doesn't fully occlude what scrolls under it — **content shows through** (use an
opaque backing, not a gradient; verify at the deepest scroll — see [`motion-troubleshooting.md`](motion-troubleshooting.md)). **HIGH** (fix unless justified):
entrance shorter than its exit (entrances should be ≥ exits) · duration off the element's type
budget (§3) · no follow-through where siblings relate · more than ~⅓ of a frame's elements active
at once · over ~20 animated elements in a frame · missing reduced-motion variant when asked.

Also: motion should read at full speed without needing slow-motion; every motion has a purpose;
it still holds up on the 100th viewing. **`validate_scene` proves structure, not that it works** —
a `data:`/`figma.com` asset (CSP-blocked → blank in the preview), a font not taken from
`picsart_media_list_fonts` (empty text), or a semi-transparent cover (leaks) can all *pass validation* and still be wrong.
Confirm on a rendered frame — but note **server-side `contact_sheet`/`export` are lenient about
asset hosting/CSP, so asset-transport failures show only in the browser editor preview**; for
assets, verify there (and default to Picsart-hosted URLs). When a pair "feels off," route the
symptom through [`motion-troubleshooting.md`](motion-troubleshooting.md) → a concrete fix.

## 10. Which property to animate

Primary property carries the meaning; a secondary adds polish — **two properties is the sweet
spot.** Prefer **transform (position/scale/rotation) + opacity**; avoid animating
width/height/margin. Defaults by goal:

| Goal | Primary | Secondary | Avoid |
|---|---|---|---|
| entrance | position | opacity | rotation |
| exit | position | opacity | scale-up |
| emphasis / button pop | scale | color | position |
| success | scale | color / opacity | position |
| error | position (shake) | color | scale-up |
| loading | rotation | opacity | position |
| toggle | position | color | rotation |

## 11. Emotion → motion

When the brief has an emotional intent, the feeling picks the path, easing, and duration (resolve
the easing id from `get_capabilities`):

| Feeling | How to author it | Duration |
|---|---|---|
| Joy / delight | overshoot via `scale_pop`/`spring`, arc path (position tangents) | 200–400ms |
| Calm | smooth `ease_in_out` (or custom `cubic_bezier`); gentle `float`/`breathe` | 500–1000ms |
| Urgency | sharp, direct `ease_out` | 100–200ms |
| Elegance | long controlled arcs, §8 Standard `cubic_bezier` | 400–700ms |
| Confidence | direct, decisive `ease_out` | 200–400ms |
| Surprise / impact | sudden expand — `scale_pop` / `zoom_in` | 150–300ms |

## 12. Core motion principles, applied (with numbers)

The core animation principles as concrete UI values:
- **Anticipation** — a small counter-move before a large action, 100–200ms, 10–20% of the main move (skip for fast feedback).
- **Staging** — dim supporting elements to 40–60% (optional 2–4px blur); the focal element enters 100–200ms after them.
- **Follow-through / overlap** — child elements trail the parent 50–150ms.
- **Slow in / slow out** — ease-out in, ease-in out, ease-in-out on-screen; linear only for rotation/progress/timers.
- **Arcs** — 10–20px perpendicular offset at the path midpoint (5px corporate, 20px+ playful), authored via `position` `inTangent`/`outTangent`.
- **Secondary action** — a supporting motion at 30–50% of the primary, 50–100ms after it.
- **Timing** — heavy elements 400–800ms, light 100–250ms; entrances run 30–50% longer than exits.
- **Exaggeration / squash-stretch** — overshoot 10–30% by personality (0% premium, 0–5% corporate) via `scale_pop`/`spring`; squash-stretch is author-managed (independent `scale` x vs y keyframes) — no primitive.
- **Appeal** — smooth curves, consistent personality; avoid jerky motion and abrupt stops.

## 13. Deciding by *purpose* — Orient / Focus / Explain / Sequence / Delight

Before choosing a motion, name the *purpose* — what the viewer should understand or notice. If a
motion serves none of these, **no animation is the right choice** (P1). The frame diff (§1) finds
*candidates*; purpose decides which are worth animating and to what end:

| Purpose | The question it answers | Typical motion |
|---|---|---|
| **Orient** | Where did this come from / go? | shared-axis move, spatial continuity (§5) |
| **Focus** | What should I notice first? | reveal, subtle scale, emphasis (§3 staging) |
| **Explain** | What changed? | morph / matched smart-animate, expand/collapse |
| **Sequence** | In what order do I read this? | stagger / cascade (§4) |
| **Delight** | Can personality improve the moment? | overshoot / `spring`, expressive secondary motion |

**Animate relationships and intent, not isolated layers** — related elements (a card, a CTA
cluster, a nav) move as one choreographed unit, not independent presets.

**The decision pipeline** (the spine under all of this):
Figma structure → semantic grouping → visual hierarchy → **motion intent** (this table) →
choreography (§4 / [`choreography.md`](choreography.md)) → **primitive preset** (§14) →
timing/easing (§3, §8) → accessibility (§7).

## 14. The preset architecture — four tiers

Presets work best as a **layered system**, not a flat effect menu. Four tiers, each mapping to a
real mp-scene surface:

| Tier | What it is | mp-scene surface |
|---|---|---|
| **1 · Primitives** | raw keyframes — fade, translate, scale, rotate, blur, trim | `patch_scene` |
| **2 · Motion presets** | a named single motion (*how* it moves) | `apply_motion_preset` / `apply_text_animation` — `slide_in`, `scale_pop`, `fade_in`, `typewriter`… |
| **3 · Component recipes** | *why* one component moves — a recipe of tiers 1–2 | a mini-recipe (the "semantic preset") |
| **4 · Composition recipes** | a whole-ad treatment | **`apply_scene_template`** — `product_ad`, `sale_ad`, `app_promo`, `before_after` |

Authoring stack, top-down: **composition recipe → component recipe → motion preset → primitive → parameters → style profile.**

A **component recipe** (tier 3) is a recipe of the tiers below, not a single engine preset:

| Component recipe | Recipe (tiers 1–2) | Intent |
|---|---|---|
| `reveal_heading` | opacity 0→1 + translateY 20→0, ease-out | introduce primary copy, don't overpower |
| `show_modal` | backdrop fade + panel `scale_pop` 0.96→1 + opacity | foreground depth + focus |
| `stagger_list` | entrance on children ~60ms apart | communicate sequence + grouping |
| `introduce_cta` | small rise/fade *after* the message settles | make the action discoverable once context lands |
| `expand_card` | size/position transform + content reveal | continuity compact → detailed |

- **Parameters** keep the vocabulary small: one `slide_in(direction, distance, duration, easing,
  delay, opacity, overshoot)` covers every variant — never a preset per direction.
- **Style profile** sits *above* choreography (= §6 personality): the *same* recipe renders
  calm / playful / cinematic by swapping durations/overshoot/stagger — intent unchanged.

**Guardrail:** tiers 1–2 resolve to real mp-scene primitives/presets via `get_capabilities`;
tiers 3–4 are **recipes/templates** (composition recipe = `apply_scene_template`; the
sticky-header-with-scroll from §9's fix is a component recipe). Never wire a recipe name as if it
were an engine preset.
