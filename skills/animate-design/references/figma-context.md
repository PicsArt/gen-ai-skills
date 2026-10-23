Tool results live in the context window for the rest of the session, so what you fetch is what you
pay for — in tokens, in cost, and in the model's attention. **On Claude Desktop / the MCP connector
(where this plugin runs) there is no file-offload: a big result goes straight into context or the
call errors** — a whole-page `get_metadata` on a real storyboard is ~100KB+ and overflows. So fetch
narrowly, hold little, and persist facts to state:

- **Frame INDEX once, cheaply.** Read the top-level frame list — ids, names, left→right order,
  dimensions — from the page/canvas node **without drilling into each frame's tree**. That's all you
  need to know what exists and the running order.
- **Full layer tree per PAIR, then release it.** Pull a frame's full nested tree only when you reach
  its pair, and keep at most the **current pair (A + B)** in working context — don't accumulate frame
  7's tree while authoring 2→3. **The payoff of that narrow breadth is affordable DEPTH:** because
  you're holding only one or two frames, you can retrieve *everything* about them — every sub-layer,
  exact coords, ink bounds via `use_figma`, styles — which is exactly the completeness correct
  composition needs and which you could never afford across the whole storyboard at once. Narrow
  breadth buys full depth where it matters.
- **Scan the sequence with COMPACT tools, not full metadata.** Scroll-run / matched-element / zoom
  detection rides on `picsart_scene_diff_layouts` / `query_layout`, which return small geometry
  deltas — peek ahead only as far as a run actually extends, never full-read the whole storyboard.
- **Persist resolved facts to `motion.json` / the scene doc, not the conversation.** Once a frame's
  coords, matchKeys, or the frame index are resolved, they live in state — so the next pair doesn't
  re-hold them in context, and a compacted or fresh session re-reads the file instead of re-fetching
  Figma. State is the memory; context is scratch.
