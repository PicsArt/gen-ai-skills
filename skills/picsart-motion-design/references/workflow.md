# Stage 3 — authoring the motion

A composed scene is a set of layered frames that render identical to the design and don't
move yet. This stage makes them move — and the gap between "slideshow" and "ad" lives
entirely in the choices made here: **which elements move, how, and what carries between
frames.** The design is authored as an MP Scene throughout; every edit is a
`patch_scene` that writes a new scene document (`sceneRef` moves — always edit the latest).

The rule under everything: **motion draws the eye, so it is spent, not sprayed.** A frame
where everything animates at once reads as noise. Pick the focal element per beat, move
it, let the rest support.

## Read the design before animating it

**First, read what changed** — from tool facts, not by eye. Diff the pair with
`picsart_media_diff_layouts` (pass frame A, frame B, and the import `matchKey`s as `matchHints`);
it classifies each layer as moved / resized / restyled / content-changed / entered / exited /
unchanged with root-space deltas. If the tool is unavailable, fall back to `picsart_media_query_layout`
on A *and* B and diff by hand. Either way, **check fades yourself** — the diff sees only `visible`,
not numeric opacity, so an opacity change reads as unchanged. **Animate only what
changed; leave unchanged layers still.** The full frame-diff procedure and the
change→motion/easing/duration/reduced-motion mapping live in
[`../../picsart-motion/references/motion-principles.md`](../../picsart-motion/references/motion-principles.md).

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
  ([`motion-principles.md`](../../picsart-motion/references/motion-principles.md)): background/chrome settle first, then the hero/headline, then the CTA
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

- **Easing:** entrances `ease_out` (fast, then settle), exits `ease_in`, matched moves
  `ease_in_out`. Reserve overshoot/spring for a playful register; clean eases read
  professional.
- **Duration scales with the change:** bigger travel/scale → longer motion, but stay short
  (~200–400ms typical; >400ms drags). Scale by energy — energetic tighter, calm longer
  (see [`motion-principles.md`](../../picsart-motion/references/motion-principles.md) §3).
- **Pace to the destination's content load — a busy frame is entered SLOWLY.** The viewer must have
  time to actually see what arrives, at least the important parts. A move into a **dense** frame — a
  grid, many cards, lots of new elements — takes a **longer, wider-spaced stagger** and a **longer
  hold** than a move into a sparse one; a fast cut into a busy screen reads as a blur and nothing
  registers. A sparse destination gets a quicker pass. **Density can override the energy register:**
  "energetic" sets the character, but a packed frame still needs enough time to land — never sacrifice
  legibility for snappiness. *Example:* frame 1 is a single icon → frame 2 is a 6-card
  content grid, so the cards stagger in over a generous window (not a fast simultaneous pop) and
  frame 2 holds long enough to take all six in. (Works with *Hold to the frame's content* below.)
- **The page-CHANGE and the content REVEAL are two separate clocks — one can be fast while the other
  isn't.** When the seam is a **UI action** (a button/tab gets tapped and that *causes* the next
  screen), the **navigation move itself can be fast and snappy** — that responsiveness is exactly
  what makes it feel like a real app: press → the next screen is just *there*. A slow nav on an
  action-response reads as laggy, not cinematic. What still paces to density is the **arriving page's
  content**: after the screen lands, its items animate in with the staggered, legible entrances their
  number demands (a busy page = separately-animated items over a generous window; a simple page =
  little or nothing). So: **fast page-change ≠ fast content reveal** — a quick nav in, then content
  that settles at a speed matched to what's on the page.
- **Scroll speed is content-driven — there is no fixed value; pace it to what the viewer needs from
  the pass.** Two ends of the range, and most scrolls sit between:
  - **Scroll to READ** — the content going by *is* the point (the viewer should register what passes)
    → **slower**, legible; don't outrun the eye.
  - **Scroll to ARRIVE** — the scroll is just transit past simple/known/repetitive content to land on
    and focus **one** item → **fast through the list, then decelerate and settle** on the target
    (ease-out into the focal item; a natural flick-and-settle, not a constant-speed crawl).
  - **The go-to velocity arc (fits most scrolls): slow-in → accelerate → settle.** *Start* the scroll
    slow so the viewer registers **what the list/grid is** (its layout, what kind of content it holds),
    then **speed up** through the bulk once they've got the idea, then **decelerate and settle** on
    where it lands. A scroll that starts fast skips the "what am I looking at" beat; the slow lead-in
    gives it. It's an ease-in-out with a settle — reach for it by default. **Why: a constant-speed
    (monotone) scroll is boring** — it reads as flat and mechanical; the changing velocity is what
    keeps it alive and feels authored. **Exceptions where it
    doesn't apply:** a very **short** scroll (a couple of items — no room for three phases, just a
    quick move + settle); a **simulated UI flick** (a tap-driven scroll meant to look like a real
    thumb starts *fast* and decelerates with friction — the opposite start); and **pure get-to-X
    transit** past known content (fast-through with just the settle, skip the slow lead-in).
  A content-rich list scrolls slower than a simple one being skimmed to a target. It's a judgment on
  the content and the intent (browse-and-read vs. get-to-X), not a number to memorize — decide it per
  case and confirm on the played result.
- **Stagger, don't synchronize:** sibling elements enter ~0.05–0.12s apart, not together.
  A row of cards popping in unison looks mechanical; a stagger looks authored.
- **Depth sells it:** assign parallax by z — background drifts least, foreground most; on a
  push-in the background scales less than the foreground.
- **One focal motion per beat:** establish → (optional interaction) → smart-animate → the
  new element settles. Not five things at once.
- **Hold ≥ motion:** a frame's hold must cover the motion authored on it — a 1.2s type-on
  needs the frame to hold ≥ 1.2s (the compose step derives this; don't fight it).
- **Hold to the frame's content, then move — no dead air.** Beyond that floor, the hold is
  **derived from the frame's own context**: how much there is to read or absorb — a text-heavy
  frame needs reading time (roughly its words at a comfortable pace), a sparse or purely
  transitional frame needs only a brief beat — scaled by the film's energy (energetic →
  tighter, calm → longer). Hold long enough to cover the motion AND let the eye land, then cut
  to the next motion. A frame that keeps sitting static well past its motion and its read is
  **dead air** — it reads as a stall, not a pause. Rhythm: motion → land → brief settle → next motion, never a long empty
  stare between beats. If the reel overshoots the target duration, trim the **holds**, not the
  motion. **Default to a tight hold — the burden is on the long one:** a frame with nothing
  that needs dwelling on (no text to read, no beat that needs to land) gets only a brief pass,
  never padding. Length must be **earned** by the frame's content, not granted by default.
- **The whole reel should read as ONE continuous velocity — carry it across every beat.** A template
  feels authored when it moves at a **coherent, single velocity/rhythm from start to finish**, each
  beat flowing into the next, not a string of disconnected fast/slow chunks bumped together. That one
  flow is the through-line; individual beats vary around it only for a deliberate accent, then return
  to it. The mechanism is simple: **carry velocity across beats — don't launch a fast move out of a
  slow settle.** The end-speed of one beat should roughly set the start-speed of the next. When a beat
  **decelerates to rest** (a scroll easing to a stop, an element settling), it has brought the eye to
  near-zero speed; snapping straight into a **fast** next animation is a whiplash that **breaks the
  continuity the settle just created** — it reads as a hard restart, not a flow. After a settle, ease
  **gently** into what follows (start it slow, matching the low speed you landed at) or give a brief
  hold first; save a fast next move for when the previous beat handed it real momentum, not from rest.
  A big speed mismatch either way (slow→fast or fast→slow) reads as a bump; keep the seam smooth
  unless you're spending a deliberate accent. (This is the velocity half of the Vector Law —
  [`transitions.md`](../../picsart-motion/references/transitions.md).)
- **Interaction simulation** belongs *before* a state change it appears to cause — the press
  fires, then the matched-animate to the next state. **Default press = the element itself pulses**
  (the **`tap_pulse` preset** — `apply_motion_preset("tap_pulse")`: a one-shot
  dip to ~0.92 and back, `at` = when it fires, `appliesTo` includes `shape`; resolve from
  `get_capabilities`, and only if it isn't listed there compose from `scale_pop` + `opacity` keyframes —
  applied to every piece of the pressed element with the same anchor) — never an invented overlay: no
  added dots, cursors, or ripples
  that aren't in the design (designers spot invented layers immediately). A **visible tap-dot is
  opt-in**: only when the designer asks or the design language already includes one.
- **Reduced-motion variant (offer, don't auto-make):** for an accessible cut, decorative motion
  (parallax, pulses, big scale-for-flair) is dropped and meaningful motion (matched chrome, state
  changes) is replaced by a dissolve/fade — never removed. Designer-initiated at Stage 5
  (see [`motion-principles.md`](../../picsart-motion/references/motion-principles.md) §7).

## The authoring loop — pair by pair, in the panel

Author one pair at a time (see the `picsart-motion` skill's pairwise rhythm). You **author** the motion
through `patch_scene` / the apply tools, then open `picsart_scene_editor` **on the whole scene
built so far** (titled for the current pair) so the designer watches it play *in context* and scrubs
to the pair — not a 2-frame sub-scene — rather than exporting a video every time; reserve
`picsart_media_export` for the final deliverable and the error fallback. For each pair A→B:

0. **Propose first — don't ask up front.** Author the best role×energy suggestion for the pair
   (steps 1–4 below) and show it as a proposal; the designer then reacts with what to change. A
   rendered proposal is a better prompt than a blank "how do you want this to move?" question.
   (If the designer *has* stated an idea, author that instead — never impose your proposal over a
   stated one.)
1. **Per element in A** — choose its motion by **role and the film's energy** (the vocabulary in
   this skill), authored through `apply_motion_preset` / `patch_scene`. Lead with the simplest move
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
(contract in [`mp-scene-editor-widget.md`](../../picsart-motion/references/mp-scene-editor-widget.md)): `verdict: "needs_changes"` carries
`comments` (frame pins with `instruction`) / `timelineComments` (stretches with `text`, `start`
and `end`), which you fold into the motion via `patch_scene`; `verdict: "approved"` advances the
conveyor. When `edited` is true, use the returned `document`, not your prior copy. If both comment
sets are absent on `needs_changes` and `edited` is true, the returned document is the requested
change. Ask for clarification only when there is no edit or usable requested change.

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
  moving stretch before approving.
