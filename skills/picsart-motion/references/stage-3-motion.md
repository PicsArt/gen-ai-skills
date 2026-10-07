# Motion — stage 3, motion

## Stage 3 — the real motion design (the whole point)

This is where a slideshow becomes an ad. You **author** the motion through
`picsart_media_patch_scene` / the apply tools, then **show** it in `picsart_scene_editor` (a
panel tool, **not** a `picsart_media_*` tool): it plays the pair's MP Scene document in
the browser, free, and the designer approves it or sends it back with edit-request comments (pins
and marked stretches, each with its own instruction). Full contract in
`mp-scene-editor-widget.md` and `widget-feedback.md`; the authoring
craft is in the `picsart-motion-design` skill.

**The motion vocabulary** — what "real motion design" is made of, all per-element:

- **Entrances / exits** — fade, slide (from an edge), scale/pop, blur-in, mask-reveal.
- **Continuous** — list **scroll**, **parallax** (layers drift by depth), text **type-on**,
  counters, marquees.
- **Interaction simulation** — the **tap-dot pulse** and cursor moves that make a UI look
  driven.
- **Matched-element smart-animate** — a shared layer **morphs its transform/opacity/content
  from frame A to frame B**, so the interface *moves* between screens instead of dissolving.
- **Kinetic type** — headlines animating in word-by-word or with a character stagger; and the
  **assembling sentence**, where shared words *persist and re-position* across frames while new words
  enter (`AI` → `AI Effects` → `AI Effects made easy.`) — not a per-frame re-type, and never a cut
  (recipe: `motion-patterns.md` *"Progressive text build"*).
- **Camera** — a gentle push-in/scale on the whole comp for emphasis; or, when a connective
  through-line (a stroke, road, path, ribbon, type baseline — any content, not only a vector) runs
  off one frame's edge and continues into the next, **tile the frames into one world canvas** at the
  offset that makes the line continuous and **travel the viewport along it while the line draws on in
  sync** — one continuous shot, not a cut. (The pan is an **empty-"world"-layer rig**, not a
  `composition.camera` pan, which is a no-op in the scene player — detection + full recipe in `transitions.md`.)
- **Brand outro** — the closing logo lockup.

Craft rules: entrances ease **out**, stagger siblings (~0.05–0.12s apart) rather than
firing together, and let the matched elements carry continuity so new elements are the
only things entering at a seam. Depth sells it — background panels drift less than
foreground.

Keep the motion legible: lead with the simplest move that reads (a preset entrance, a matched
smart-animate), tune params only when the designer asks, and drop to raw keyframes only for what a
preset can't express. The designer judges the result on the played scene, not a description.

### Work pair by pair — the default rhythm

**HARD RULE — one pair at a time, and STOP for approval before the next.** Never
author, compose, or review more than **one pair (two adjacent frames, A→B)** in a single
turn. Do **not** run ahead across the whole storyboard, do **not** batch multiple pairs or
all frames at once, and do **not** author the next pair until the designer has **explicitly
approved** the current one. Present one pair → wait → only after the approval comes back do
you advance to the next. Jumping ahead — composing or motioning several pairs before the
first is approved — is the single most common failure this rhythm exists to prevent.

**This pair rhythm is for FRAME SEQUENCES (a Figma storyboard).** Uploaded assets have no frames —
they're arranged into one composition (a **grid, stack, collage, montage, or single focus** — not
one-asset-per-screen by default) and worked by the **working mode the user picked** (part by part, or
the whole motion at once — see *Working mode for uploaded assets*), never by A→B pairs.

**The preview is mandatory and self-standing — never skip it and never wait to be asked.**
"Present" means you **actually call the preview** (`picsart_scene_editor` / `picsart_media_export`)
and show the result; it does **not** mean describing the motion in prose, citing a `validate_scene`
pass, or saying it "should" look right. Advancing without a shown preview — or only previewing
because the designer *reminded* you to — is itself the violation, even if the motion turns out fine.
Every pair ends the same way: **shown preview → explicit designer yes → next.** No shown preview,
no advance; no explicit yes, no advance.

**And the preview that proves MOTION is the editor, not stills.** Contact-sheet / still exports are
fine for the Stage-2 *position* render-match, but the still renderer and the browser editor **draw some
moving things differently** (a photo scaling from its edge can look right in stills yet overlap a
sibling when it plays). So judge motion on `picsart_scene_editor` (or a played export), never a
still — `motion-troubleshooting.md` §"It looked right in the stills but wrong when it played".

**Approval gates what the designer SEES, never your intention to render it.** Free calls —
`validate_scene`, `contact_sheet`, opening the editor, an export used as a preview — run
without asking: render first, show, *then* wait for the reaction. Never ask "shall I render?",
never report that a preview "needs your go-ahead", and **never tell the designer to type "go"
(or any keyword) to continue** — the designer speaks in design terms ("snappier", "approved",
"change the easing"), not in control tokens. The compose/motion/preview loop is free, so it never
gates on cost. The actions that **do** require an explicit ask are **saving to Drive** and
**generating video** — the latter behind the full cost-consent gate (show credits → preflight cost →
explicit yes; see *Video generation*). Those two aside, act on free calls without asking.

**Open with frame 1's entrance, before pair 1→2.** The reel starts with motion, not a frozen
frame — author frame 1's own elements animating **in** at `t=0` (entrances by role, staggered by
hierarchy), get that opening beat approved, and only then start pair 1→2. A static first frame that
jumps into the first transition is a slideshow tell (full craft in the `picsart-motion-design` skill,
*The opening beat*).

**First, analyze the whole frame sequence — a "pair" isn't always two frames.** Before you start
pairing, read the run with the diff tools (`picsart_media_diff_layouts` / `query_layout`, never by
eye) and find the stretches that are really **one motion across several frames**: a **scroll** (frame
k, k+1, k+2… are the same page translated along one axis), a **zoom/pan** (B is A scaled/cropped), or
a **highlight-in-place** (B is A with emphasis). Those runs collapse into a **single continuous beat
over one unit of content** — you animate the whole scroll as one gesture, not frame-by-frame with a
stop on each waypoint (full detection + authoring in [`transitions.md`](transitions.md)).
**This is a judgment that highly depends on the case** — how many frames belong to the run, whether
it's truly one scroll or genuinely separate screens, where it should pause — so decide it per design
from the tool-read facts, not from a fixed rule, and confirm on the played result. Everything below
about "pairs" applies to these grouped beats too: one is authored, shown, and approved at a time.

**Then work in the imported Figma order, from the top** — the first beat (frame 1's opening, then
1→2 or the first grouped run), then the next, and so on. "The next" always means the next in
sequence. **Never open with a middle or last beat (e.g. 8→9), and never hop between non-adjacent
ones** — not even when a later frame looks more interesting. Picking out of order is the same failure
as running ahead, pointed sideways: the storyboard is animated from the top, so the designer reviews
it the way it plays.

Author motion **one pair at a time**, screen to screen:

1. Focus **exactly one pair** — the **earliest pair not yet approved** (start at 1→2): frame A,
   the motion, frame B. Nothing beyond this pair is touched yet. (Open `picsart_scene_editor`
   on this pair to view the motion.)
2. **Propose the motion — author it, don't ask first.** Lead with the best role×energy /
   principle-based suggestion for the pair: each element's entrance/continuous motion **and** the
   matched-element smart-animate carrying shared layers A→B. A rendered proposal on screen is a far
   better prompt than a blank *"how do you want this to move?"* — so author, then show. (If the
   designer *has* stated an idea, author that instead — never impose your proposal over a stated one.)
3. **Show it moving, framed as a proposal** — open `picsart_scene_editor` **on the whole scene
   built so far** (titled for this pair) to play the motion in context (or export the whole reel):
   *"Here's f2→f3 — tell me what to change."* The designer approves or sends it back with comments.
4. **Take direction and revise.** The designer reacts to what they see — "snappier", "drop that
   element", "slower on the CTA". Fold each request into the pair and re-show. Expect a few passes;
   each maps to timing / staggering / element inventory, not a fresh design.
5. **Wait for the designer's explicit approval.** Only after it arrives do you flip that
   pair `approved: true` in `motion.json.seams` and move to the **next** pair. No approval →
   no advance, full stop.

**One decision per turn**, the running cut stays playable, and the **gate is met only
when every pair is approved**. Never self-approve by describing motion — the yes comes
from the designer, on a moving preview. Touch a shared frame and you may change both its
pairs, so re-preview the neighbour.

The panel does not latch: every edit writes a new scene document and `sceneRef` moves —
always edit the latest. And when the editor returns an **`edited` document**, that becomes the
latest — patch further changes onto it, not onto the copy you opened with.
