# Craft rules

The rules that make motion read as designed, for every pair you author.

## Craft rules that make motion read as designed

- **Easing:** entrances `ease_out` (fast, then settle), exits `ease_in`, matched moves
  `ease_in_out`. Reserve overshoot/spring for a playful register; clean eases read
  professional. **Keep an easing budget:** two or three curves across the whole piece — one for
  functional moves (the house curve in `references/ENGINE-GOTCHAS.md`), one with overshoot for pops.
  Consistency reads as design; a new curve per move reads as noise.
- **Duration scales with the change:** bigger travel/scale → longer, but a UI element move stays
  short (~200–400ms; >400ms drags); ambient or emotional pacing is motion-intent's. Scale by
  energy — energetic tighter, calm longer (see [`MOTION-PRINCIPLES.md`](MOTION-PRINCIPLES.md) §3).
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
  **dead air** — it reads as a stall, not a pause (the "we transitioned to frame 2 and it just
  sits there" problem). Rhythm: motion → land → brief settle → next motion, never a long empty
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
  `references/TRANSITIONS.md`.)
- **Interaction simulation** belongs *before* a state change it appears to cause — the press
  fires, then the matched-animate to the next state. **Default press = the element itself pulses**
  (the **`tap_pulse` preset** — `apply_preset("motionPreset:tap_pulse")`, verified on current builds: a one-shot
  dip to ~0.92 and back, `at` = when it fires, `appliesTo` includes `shape`; resolve from
  `get_capabilities`, and only if your build lacks it compose from `scale_pop` + `opacity` keyframes —
  applied to every piece of the pressed element with the same anchor) — never an invented overlay: no
  added dots, cursors, or ripples
  that aren't in the design (designers spot invented layers immediately). A **visible tap-dot is
  opt-in**: only when the designer asks or the design language already includes one.
- **Reduced-motion variant (offer, don't auto-make):** for an accessible cut, decorative motion
  (parallax, pulses, big scale-for-flair) is dropped and meaningful motion (matched chrome, state
  changes) is replaced by a dissolve/fade — never removed. Designer-initiated at Stage 5
  (see [`MOTION-PRINCIPLES.md`](MOTION-PRINCIPLES.md) §7).
