---
name: motion-design-craft
description: The craft of adding motion to any scene, whatever the video — an ad or reel, a promo, a tutorial or walkthrough, an explainer, an intro, outro or title card, or one beat inside a longer edit — motion chosen per element by its role, smart-animate and morphs between frames, transitions, strokes and mask reveals, reviewed by eye in the scene editor pair by pair. Use whenever motion is added to or changed in a scene — elements animating in or out, a transition that looks wrong, a morph, a mask, an animated callout, highlight or zoom, a logo reveal, kinetic text — including inside another use case or a tutorial, not only in the `animate-design` skill's pipeline, where it is stage 3.
metadata:
  owner: motion-designer
user-invocable: false
---

# Stage 3 — authoring the motion

A composed scene is a set of layered frames that render identical to the design and don't
move yet. This stage makes them move — and the gap between "slideshow" and "ad" lives
entirely in the choices made here: **which elements move, how, and what carries between
frames.** The design is authored as a scene throughout; every edit is a
`patch_scene` that writes a new scene document (`sceneRef` moves — always edit the latest).

The rule under everything: **motion draws the eye, so it is spent, not sprayed.** A frame
where everything animates at once reads as noise. Pick the focal element per beat, move
it, let the rest support.

## Motion in any scene, not only after an import

This craft is not limited to the `animate-design` pipeline. Use it wherever a scene gets motion: a
tutorial's full-screen moments and the transitions between its parts, a promo's title card, an
animated callout or highlight over a screen recording, a logo reveal, a presenter bubble that grows
into a full frame, a morph from one clip's framing into the next. Open this skill **as soon as the
motion is being designed**, not after a first transition already looks wrong. Everything below
applies; only the inputs differ:

- **"Frames" are the two states either side of the motion.** A is the last settled state before it,
  B the first settled state after it: two beats, two parts or two layouts of the same scene. Author
  A→B pair by pair, exactly as below.
- **No import, so tag the matched elements yourself.** An element present in both states (the same
  shape, logo, panel, bubble or recording) is matched. Diff the two states with
  `picsart_scene_diff_layouts`, passing those pairs as `matchHints`, or `picsart_scene_query_layout` on
  both, and read off the delta.
- **Shape changes, borders, masks, camera moves and sound sync** follow *Craft for any motion*
  below; read [`references/ENGINE-GOTCHAS.md`](references/ENGINE-GOTCHAS.md) before the first mask.
- **The motion lives in the scene that has the layers.** When the final video is a stitch of
  rendered parts, a rendered part can only cut or dissolve into the next. Author a transition that
  carries an element across the seam in the scene that still holds both sides as layers, before it
  is rendered.
- **Recorded footage stays footage.** Animate the layers around and over a recording (its panel,
  mask, frame, callouts and text); never re-time the recording itself to fit a motion.
- **Review still happens on the moving stretch**, in `picsart_scene_editor`, pair by pair. When
  another flow called this skill, that flow's review step is where the user approves.

## Read the design before animating it

**First, read what changed** — from tool facts, not by eye. Diff the pair with
`picsart_scene_diff_layouts` (pass frame A, frame B, and the import `matchKey`s as `matchHints`);
it classifies each layer as moved / resized / restyled / content-changed / entered / exited /
unchanged with root-space deltas. If the tool is unavailable, fall back to `picsart_scene_query_layout`
on A *and* B and diff by hand. Either way, **check fades yourself** — the diff sees only `visible`,
not numeric opacity, so an opacity change reads as unchanged. **Animate only what
changed; leave unchanged layers still.** The full frame-diff procedure and the
change→motion/easing/duration/reduced-motion mapping live in
[`references/MOTION-PRINCIPLES.md`](references/MOTION-PRINCIPLES.md).

Then choose each moving element's motion by its **role**, not at random. This is the default
mapping — a starting point the designer overrides in the panel, not a law:

| Role (from import) | Default motion |
|---|---|
| headline / display text | **type-on**, or word/character **stagger** in |
| body / label text | short fade + slide-up |
| CTA / button | **scale/pop**, entering *late* (after its context), often with a tap-dot |
| hero image | subtle **scale-in / push-in**, or a mask **reveal** |
| list / feed | the content **scrolls**; rows **stagger** in |
| card / panel | **slide** from the nearest edge + fade |
| chrome (tabs, header, nav) | usually the **matched element** — persists and smart-animates; enters first, exits last |
| icon / small accent | quick **pop**, subtle |
| background | least motion — a slow **parallax** drift or gentle scale |

The design's own **hierarchy is the motion priority**: what the eye should hit first gets
the entrance; supporting elements follow.

## How finely to split — respect the design's units, don't take a mark apart

"Split into pieces that move independently" means **use the layers the design has** — not
manufacture finer structure inside a single element. Going finer than the design (splitting one
vector/instance into sub-parts to animate them separately) is the same class of overreach as
inventing a cursor or a ripple: you're adding structure the designer didn't author.

**Default: animate each element as the one unit Figma authored** (one layer / instance / vector =
one unit). Sub-dividing that unit is a bigger claim — allow it **only when all three hold**:

1. the sub-parts are **distinct content** — separate things — not the strokes/segments of one glyph
   or mark;
2. the **concept calls for it** — a set, variety, or a progressive build the message depends on;
3. it is **not the brand's identity** — a logo, wordmark, or **app icon** stays whole regardless of
   how separable its parts look.

**When it's a judgment call, keep the unit whole and OFFER the split** — let the designer choose;
never impose decomposition. *Worked example:* an AI-Playground app icon whose mark is a square,
sparkle, diamond and circle **fails #3** — it's the identity mark — so the open is a whole-icon
reveal (fade/scale the tile+shapes in together), and "the four shapes pop in one by one" is offered
as an option, not authored by default. Taking a brand mark apart on screen reads as *disassembling
the logo*, which is rarely what the designer meant.

## The opening beat — frame 1 animates IN, it never just sits there

**The reel opens with motion, not a frozen screen.** A static frame 1 that holds and then
suddenly jerks into the 1→2 transition reads as amateur — the viewer sees a still image, then a
jump. Instead, **frame 1's own elements animate in at t=0**, so the first thing on screen is the
design *assembling itself*, and by the time the 1→2 motion fires the frame already feels alive.

- **Entrances by role, staggered by hierarchy.** Same role×energy vocabulary as any entrance
  (`MOTION-PRINCIPLES.md`): background/chrome settle first, then the hero/headline, then the CTA
  last. What the eye should hit first enters first; siblings stagger ~0.05–0.12s, never in unison.
- **It's an intro, not a showcase — keep it tight.** A quick, confident assemble (energy scales
  it: energetic → snappier and shorter; calm → a softer fade-up). Don't animate *everything*; a
  couple of focal entrances plus a gentle settle on the rest reads better than a busy cascade.
- **Then hold, then transition.** Opening beat → the frame's content-derived hold (the "no dead
  air" rule still applies) → the 1→2 motion. The opening is a distinct beat *before* pair 1→2.
- **Nothing is matched yet** (there's no frame before frame 1), so this beat is entrances only —
  no smart-animate, no exits.
- **Don't manufacture parts to stagger.** A sparse open (one icon on a dark ground) tempts you to
  invent motion by taking the one element apart. Whether that's allowed is a real judgment — see
  *How finely to split* below — but the default on a brand/app icon is a **whole-icon reveal**, with
  a staggered build only **offered**, never imposed.
- **Symmetric at the end:** the last frame shouldn't freeze-frame either — let it settle/hold on a
  deliberate final state (or a brand lockup) rather than snapping to a stop.

Author this as frame 1's entrance animations at `t=0`, self-check it like any pair, and get it
approved as the reel's open **before** you start pair 1→2.

## Matched-element smart-animate — the technique that makes it an ad

This is the single thing that separates motion design from a slideshow. When a layer
carries a `matchKey` into the next frame (tagged at import), you do **not** cross-dissolve
the two screens — you **animate the shared layer from its state in A to its state in B**:

- **Move the delta** — position, size, opacity, and content (a text string changing) from
  A→B, ~0.4–0.8s, **ease-in-out**.
- **Keep matched layers on screen through the transition** — never fade the shared chrome;
  its staying put *is* the continuity.
- **Elements only in A exit** (fade/slide out) as or just before the move.
- **Elements only in B enter** *after* the matched layers have arrived, so the eye follows
  continuity into the new content rather than being asked to look everywhere at once.

Miss this and shared chrome cross-dissolves — the biggest tell of "slideshow, not ad."

## Craft rules that make motion read as designed

Easing, duration, staggering, the opening beat, holds and the rest: read
[`CRAFT-RULES.md`](references/CRAFT-RULES.md) before you author the first pair.

## Craft for any motion — continuity, containers, camera, sound, checking

Learned on a narrated tutorial whose bubbles grew into full frames and shrank back; each rule fixed
a visible bug. They hold for any motion, in any scene.

**Shape and continuity**

- **A shape change is two copies, pixel-locked, cross-faded across the whole move.** When an
  element changes shape between states (a rectangle to a circle, a card to full screen), animate a
  copy in A's shape and a copy in B's shape together — shared position, scales derived from one
  fixed ratio — and cross-fade them over the full duration of the move. Never scale one shape into
  the other's footprint, and never do it in two steps (move, then reshape).
- **One of each thing on screen.** While an element travels to where its destination version sits,
  hide the destination version and reveal it on landing. Two visible copies always read as a glitch.
- **Pixel locking.** Layers that must move as one share keyframe times and derive their scales from
  one ratio, so nothing drifts against anything else mid-move. Parent them when the engine allows.

**Containers, borders and masks**

- **Borders follow their content.** A stroke, ring or frame fades in after its content lands and
  fades out as the content starts to move. A border fading at a fixed size while the content moves
  past it looks detached.
- **Clip to the inner shape.** Content inside a rounded border is clipped to the border's inner
  edge — the size minus the stroke width, the radius minus half the stroke — and fills it exactly.
  Square corners or a gap at the edge give it away at once (stroke insets: `ENGINE-GOTCHAS.md`).
- **Masks move with their layer.** An animated layer's mask carries the same transform animation, on
  the same time base. A mask is addressed through its owner (`ENGINE-GOTCHAS.md`); remember that a
  nested composition's children run on its local clock.

**Camera and time**

- **Move a camera, not the content.** For a push, pan or reframe, animate one parent transform and
  compute the framing from the size of the target region (the smart-animate zoom in
  `ENGINE-GOTCHAS.md`; a pure pan needs the empty "world" layer, since a pan-only camera does
  nothing). Every layer then stays consistent with every other. **The camera holds still while a
  caption or card is entering** — one focal move per beat.
- **Nothing sits frozen.** A hold the content needs still gets a subtle drift — a few percent of
  scale over the hold — or ambient motion (`float`, `breathe`), so the frame stays alive without
  drawing the eye. This is not padding: the hold's length still comes from its content.
- **Time is a design tool.** Compress what repeats, play at real speed what must be believed (a
  generation finishing, a real result), slow down what must be read. A starting speed map for
  footage: typing and waiting at 2–3×, a fast-forward through repetitive content at up to 3×, the
  payoff at 1–1.5×, and a moment the viewer must dwell on slowed to 0.3–0.5×.
- **Procedural secondary motion.** For continuous ambient movement (sway, bob, flicker), use an
  ambient preset (`sway`, `float`, `glow_pulse`), or where none fits a small Lua expression on
  position or rotation — a sine, not hand keyframes — with amplitude, phase and period varied per
  copy so repeated elements don't move in lockstep. Expressions do not work on camera fields.

**Camera on screen recordings**

- **Frame a region, not a guess.** The zoom that frames a button, message or result comes from the
  region's size against the recording's fitted scale, and the position from the region's centre:
  the screen-recording-layouts skill's framing formula, which holds for any frame size. On a panel in a vertical
  promo, the screen-recording-zoom skill's house zoom sets the numbers.
- **Push in on the payoff.** Start wide, hold a beat (~0.15 s), then push to the detail (~0.6 s on
  the house curve) so it lands just before the narrator names it.
- **Keep what must not be seen off screen.** Cut ~0.3 s before a warning banner or error toast
  appears; frame out internal names, emails, tokens and other people's data. When a frame can't
  avoid them, cover them with a rectangle in the UI's background colour, locked to the recording's
  transform so it moves with it.
- **Patterns** for type-on over a real screenshot, prompt cards, insets, a phone-frame pop and
  ambient depth: *Tutorial and screen-recording patterns* in
  [`references/MOTION-PATTERNS.md`](references/MOTION-PATTERNS.md).

**Sound and sync**

- **Motion lands on sound.** Anchor key moves and cuts to audio events: a narrated word (word times
  from `picsart_media_transcribe`), a beat or a hit (`beats` and `onsets` from
  `picsart_media_analyze_audio`). A move that lands with its sound feels intended; the same move
  200 ms off feels sloppy. **Cut on the voice, not the picture:** over narration, every shot starts
  on a word time, so the picture changes as the narrator says the thing.
- **Sync is local, not global.** When sound and picture drift, measure and fix each source on its
  own; one global offset fixes some sources and breaks others.

**Checking**

- **Check the middle, not just the ends.** Most motion bugs live mid-move: doubles, gaps, square
  corners, pops. For every move, look at frames at 25%, 50% and 75% of it — pass those times to
  `picsart_scene_contact_sheet` — and at a larger `resolution`, zoom into the edges and corners of
  those rendered frames, not only the editor's preview.

## The authoring loop — pair by pair, in the panel

Author one pair at a time (see the `animate-design` skill's pairwise rhythm). You **author** the motion
through `patch_scene` / the apply tools, then open `picsart_scene_editor` **on the whole scene
built so far** (titled for the current pair) so the designer watches it play *in context* and scrubs
to the pair — not a 2-frame sub-scene — rather than exporting a video every time; reserve
`picsart_scene_export` for the final deliverable and the error fallback. Before each round of
patches and each look at the frames by eye, post the one-line progress message the `animate-design` skill
describes. For each pair A→B:

0. **Propose first — don't ask up front.** Author the best role×energy suggestion for the pair
   (steps 1–4 below) and show it as a proposal; the designer then reacts with what to change. A
   rendered proposal is a better prompt than a blank "how do you want this to move?" question.
   (If the designer *has* stated an idea, author that instead — never impose your proposal over a
   stated one.)
1. **Per element in A** — choose its motion by **role and the film's energy** (the vocabulary in
   this skill), authored through `apply_preset` / `patch_scene`. Lead with the simplest move
   that reads; tune params only when asked; raw keyframes only for what a preset can't express.
2. **Author the matched-element smart-animate** for every shared layer (A→B delta).
3. **B's new elements** — give them entrances, staggered, after the matched layers land.
4. **Interaction sim** — where the transition reads as UI-driven, press the trigger element
   (`tap_pulse` on the element itself; a visible tap-dot only if the designer opts in).
5. **Play the pair in the editor** (free), and let the designer **approve** — never
   self-approve by describing it. On approval, `approved: true` on that pair; advance.
   Open the editor **without asking first**: a free preview needs no go-ahead, so never
   stop at "the render needs your approval" or ask the designer to type "go" — show the
   result and let them react to it. Approval is for what they see, not for your next
   free tool call.

Each edit is a `patch_scene` → a new `sceneRef`. Read the `scene_editor_feedback` payload
(contract in `docs/widget-specs/scene-editor.md`): `verdict: "needs_changes"` carries
`comments` / `timelineComments` — each with its own words (a pin's `instruction`, a stretch's
`text`) and where it applies — which you fold into the motion via `patch_scene`; `verdict:
"approved"` advances the conveyor. When `edited` is true, patch onto the returned `documentUrl`
(the inline `document` only when it could not be stored), not your prior copy.

## Suggesting motion

When you propose candidates, choose by **role × energy**, not a fixed list: a headline at
`energetic` gets a fast word-stagger; at `calm`, a soft fade-up. Preview each **on the
real element**, never as a named list of presets in prose — a designer judges motion by
watching it, and a still or a word ("fade_in") approves things that are wrong.

## Anti-patterns (the slideshow tells)

- **A static first frame** — the reel holds on a frozen frame 1, then jumps into the 1→2 motion.
  The open should animate in (see *The opening beat*); a still that suddenly moves is a slideshow tell.
- **Taking a mark apart** — splitting one vector/instance (a logo, an app icon) into sub-parts to
  stagger them, when the design authored it as one unit. Whole by default; offer the build (see
  *How finely to split*).
- **Everything moving at once** — no focal point; reads as noise.
- **Matched chrome cross-dissolving** instead of smart-animating — the headline tell.
- **No depth** — every layer moves at the same rate, so it reads flat.
- **Synchronized entrances** — siblings firing together look mechanical.
- **Over-animation** — motion on elements that should stay still, fighting the design's
  hierarchy.
- **Judging from a still** — a transition is invisible in one frame; always preview the
  moving stretch before approving, and check its 25/50/75% frames (see *Check the middle*).
- **Two copies on screen, a border left behind, a mask off its layer** — the continuity and
  container tells (see *Craft for any motion*).
