
# Content + visual pair

Every tweet, LinkedIn post, blog paragraph, or newsletter section gets a visual that matches its tone. Creators ship daily — this skill is the fastest path from "I have the words" to "I have the image", with aesthetic consistency across a whole week of content.

## When to Use

- Creator is about to post a tweet / thread / LinkedIn update and needs one matching image, fast
- Blogger wants inline illustrations per section of a long-form post
- Newsletter writer generates one hero visual per issue, weekly
- The user says "pair this with a visual", "illustrate this paragraph", "inline image for my post", "gimme a matching image", "visual for this tweet"
- They want a queue of 5-10 paired visuals, not a single hero

**Don't use for:** full launch asset bundles (use `prosumer-launch-kit`), product mockups (use `prosumer-product-mockups`), or single large hero images where composition matters more than speed.

## Prerequisites

Most of the time this skill runs with near-zero interview — the paragraph IS the brief. But before the first run of a new content series, lock these down once:

1. **Content source** — clipboard (`pbpaste`), stdin, a file, or interactive paste?
2. **Aesthetic** — photoreal, editorial illustration, flat vector, 3D render, retro print, hand-drawn? This becomes the "house style" for the whole queue.
3. **Palette** — brand colors or mood colors to repeat across every visual?
4. **Platform + ratio** — X/Twitter (16:9 or 3:2), LinkedIn (1.91:1 or 1:1), IG (1:1 or 4:5), blog inline (16:9 or 4:3)?
5. **Voice match** — should the visual be literal (shows the exact thing described) or conceptual (metaphor / mood)?
6. **Queue size** — one-off now, or 5-10 paired assets for the week?

After the first run, skip all of this — just pipe the paragraph and reuse the locked aesthetic.

## How to Run

```
1. FIRST-RUN SETUP  → lock aesthetic + palette + ratio once
2. QUICK PAIR       → pipe paragraph → one visual
3. QUEUE MODE       → manifest N paragraphs → N visuals in one batch
4. REVIEW           → verify voice match; regenerate misses only
5. SHIP             → per-post folder or direct to Drive
```

## Quick Reference

One week of content, one aesthetic, one batch:

```json
{
  "defaults": {
    "model": "recraftv4",
    "aspectRatio": "16:9"
  },
  "jobs": [
    {
      "id": "mon-am",
      "prompt": "editorial illustration, muted mustard and ink palette, paper grain. a small figure walking up a hand-drawn staircase made of calendar pages"
    },
    {
      "id": "tue-am",
      "prompt": "editorial illustration, muted mustard and ink palette, paper grain. two speech bubbles overlapping into a Venn diagram, shared area glowing"
    },
    {
      "id": "wed-thread",
      "prompt": "editorial illustration, muted mustard and ink palette, paper grain. a toolbox spilling open, tools reorganizing themselves mid-air into a neat grid"
    },
    {
      "id": "thu-long",
      "prompt": "editorial illustration, muted mustard and ink palette, paper grain. a single matchstick lighting a row of candles, each candle shaped like a lightbulb"
    },
    {
      "id": "fri-recap",
      "prompt": "editorial illustration, muted mustard and ink palette, paper grain. a hand placing the last piece into a half-finished jigsaw puzzle of a week calendar"
    }
  ]
}
```

The shared aesthetic preamble at the front of every prompt is what makes the week look like one series instead of five unrelated images.

## Quick Reference

| Sub-task | Model | Why |
|---|---|---|
| Default — editorial illustration, fast | `recraftv4` | Fastest, cheapest, strongest "illustration" aesthetic |
| Photoreal pair (lifestyle / scene) | `flux-2-pro` | Best photoreal fidelity when the post calls for it |
| Text-in-image (headline, quote card) | `imagen-4.0` or `ideogram-v3` | Only models that render legible in-image text reliably |
| Concept / abstract metaphor | `recraftv4` or `gemini-3-pro-image` | Strong at symbolic composition |
| Quick iteration on an existing visual | `flux-kontext-pro` (i2i with `-i`) | Fast restyle of a prior image without starting over |
| Vector / flat-graphic output | `recraftv4` with style flag or `recraft-vectorize` | True SVG output for blog headers |
| High-end hero (monthly feature article) | `flux-2-pro` or `gemini-3-pro-image` | Worth the extra credits for flagship posts |

## Procedure

- **Lock the aesthetic once, reuse everywhere.** The single biggest upgrade to a content queue is a 15-word style preamble prepended to every prompt. Without it, 5 posts = 5 different looks.
- **Go conceptual over literal.** A tweet about "compound interest" + a literal pile of coins = stock-photo vibes. "A single matchstick lighting a row of candles" = memorable.
- **Use `--json --no-input` mode in agent contexts.** Returns JSON on stdout, easy to pipe the URL straight to a scheduler (Buffer, Typefully, etc.).
- **Keep prompts short.** One aesthetic preamble + one sharp scene sentence. Long prompts dilute the visual.
- **Batch the week on Monday morning.** One manifest, one `gen-ai batch run`, done by the first coffee. Don't generate ad-hoc per post.
- **Save to Drive with a week-tagged folder** (`content-week-17`) so you can find "that post from 3 weeks ago" later.
- **Reuse the best visual as a reference (`-i`)** for the next week's set — passes the aesthetic forward without re-prompting.
- **When in doubt, regenerate — don't fix.** At 1-2 credits per shot, it's cheaper to re-roll than to negotiate with the model.

## Pitfalls

- **Inconsistent aesthetic across the week** — nobody prepended a shared style preamble. Lock it in defaults and inherit every job.
- **Too-literal prompts** — echoing the paragraph word-for-word. Step back, find the metaphor, describe the metaphor.
- **Over-long prompts** — model ignores half. Keep to one preamble sentence + one scene sentence.
- **Expecting legible in-image text from recraftv4** — switch to `imagen-4.0` / `ideogram-v3` when the visual needs to carry a headline.
- **Generating one-at-a-time for a week's worth** — 5 separate calls = 5 tabs of context switching. Batch it.
- **Leaving the queue unarchived** — three weeks later the local file is gone and the post needs a reshare. Upload or archive the approved output folder.

## Verification

Run `gen-ai whoami` to confirm authentication, then re-run the failed command with `--debug`.

### Single quick pair (the 90% case)

```bash
# macOS — paste from clipboard
pbpaste | gen-ai generate -m recraftv4 --ar 16:9 --json --no-input | jq -r '.url'

# Linux
xclip -selection clipboard -o | gen-ai generate -m recraftv4 --ar 16:9 --json --no-input | jq -r '.url' | xargs curl -L -o inline.webp

# From a file
cat post.txt | gen-ai generate -m recraftv4 --ar 16:9 --json --no-input | jq -r '.url' | xargs curl -L -o inline.webp

# Full pipeline — clipboard in, file out, opened
pbpaste | gen-ai generate -m recraftv4 --ar 16:9 --json --no-input | jq -r '.url' | xargs curl -L -o inline.webp && open inline.webp
```

With a locked aesthetic preamble prepended:
```bash
STYLE="editorial illustration, muted mustard and ink palette, paper grain, flat composition"
echo "$STYLE. $(pbpaste)" | gen-ai generate -m recraftv4 --ar 16:9 --json --no-input | jq -r '.url' | xargs curl -L -o inline.webp
```

### Queue mode — week of content in one batch

```bash
gen-ai batch run week-queue.json -c 3 -o ./content/week-17
```

Per-post output files become `./content/week-17/mon-am.webp`, `./content/week-17/tue-am.webp`, etc.

### Image + text check

For visuals that should have a legible headline baked in, switch to `imagen-4.0` or `ideogram-v3`. For everything else (metaphor, mood, illustration), `recraftv4` is faster and cheaper.

## Cost & time

| Task | Model | Credits | Time |
|---|---|---|---|
| 1× inline visual (editorial) | `recraftv4` | ~2 | ~10s |
| 1× photoreal pair | `flux-2-pro` | ~8 | ~45s |
| 1× quote card with headline | `imagen-4.0` | ~3 | ~25s |
| 1× concept illustration | `recraftv4` | ~2 | ~10s |
| **Week of 5 paired visuals (recraftv4)** | — | **~10** | **~1 min batched** |
| **Week of 5 paired + 1 hero (flux-2-pro)** | — | **~18** | **~2 min batched** |

Content-pair economics are why this workflow wins on volume — fifty posts a month = under $5 if you stick with recraftv4.

## See also

- [gen-ai-use.md](../../gen-ai-use/SKILL.md) — CLI command reference, `--json --no-input` mode, pipe patterns
- [gen-ai-workflows.md](../../gen-ai-workflows/SKILL.md) — Workflow 1 (blog-to-visuals) for full-post illustration
- [gen-ai-batch.md](../../gen-ai-batch/SKILL.md) — manifest schema, concurrency, `gen-ai batch resume <output-dir>`
- [install-gen-ai-cli-and-mcp.md](../../install-gen-ai-cli-and-mcp/SKILL.md) — set up the CLI + MCP server
- `prosumer-launch-kit` — when a single post grows into a launch day
- `prosumer-headshot-studio` — when the "visual" should be the creator themselves
