**The motion vocabulary** — what "real motion design" is made of, all per-element:

- **Entrances / exits** — fade, slide (from an edge), scale/pop, blur-in, mask-reveal.
- **Continuous** — list **scroll**, **parallax** (layers drift by depth), text **type-on**,
  counters, marquees.
- **Interaction simulation** — the **tap-dot pulse** and cursor moves that make a UI look
  driven (the magenta taps in the reference).
- **Matched-element smart-animate** — a shared layer **morphs its transform/opacity/content
  from frame A to frame B**, so the interface *moves* between screens instead of dissolving.
- **Kinetic type** — headlines animating in word-by-word or with a character stagger; and the
  **assembling sentence**, where shared words *persist and re-position* across frames while new words
  enter (`AI` → `AI Effects` → `AI Effects made easy.`) — not a per-frame re-type, and never a cut
  (recipe: `MOTION-PATTERNS.md` *"Progressive text build"*).
- **Camera** — a gentle push-in/scale on the whole comp for emphasis; or, when a connective
  through-line (a stroke, road, path, ribbon, type baseline — any content, not only a vector) runs
  off one frame's edge and continues into the next, **tile the frames into one world canvas** at the
  offset that makes the line continuous and **travel the viewport along it while the line draws on in
  sync** — one continuous shot, not a cut. (The pan is an **empty-"world"-layer rig**, not a
  `composition.camera` pan, which is a v1 no-op — detection + full recipe in `references/TRANSITIONS.md`.)
- **Brand outro** — the closing logo lockup.

Craft rules: entrances ease **out**, stagger siblings (~0.05–0.12s apart) rather than
firing together, and let the matched elements carry continuity so new elements are the
only things entering at a seam. Depth sells it — background panels drift less than
foreground.

Keep the motion legible: lead with the simplest move that reads (a preset entrance, a matched
smart-animate), tune params only when the designer asks, and drop to raw keyframes only for what a
preset can't express. The designer judges the result on the played scene, not a description.
