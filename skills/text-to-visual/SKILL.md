---
name: text-to-visual
description: Generate matching visuals from text via Picsart gen-ai.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    category: creative
    tags: [picsart, text-to-image, blog-visuals, og-images, content]
---

# Text to Visual

A single skill that covers every "given text, produce a matching image" workflow Picsart's `gen-ai` CLI supports. Use when the user has any kind of written content — a paragraph, a blog draft, a URL — and needs visuals generated from it. Replaces three narrower skills with one entry point and three mode references.

**Input:** text (paragraph, article, or URL). **Output:** one or more images matched to the text's tone, topic, and target placement.

## When to Use

| Mode | Trigger phrases | Reference |
|---|---|---|
| **single** | "match a visual to this paragraph", "inline image for this section", "one visual for this content" | [`references/modes/single.md`](references/modes/single.md) |
| **article-set** | "illustrate this blog post", "hero + inline visuals for an article", "full visual set for a draft" | [`references/modes/article-set.md`](references/modes/article-set.md) |
| **og** | "OG image for this URL", "open graph preview", "Twitter card image", "dynamic meta image" | [`references/modes/og.md`](references/modes/og.md) |

If the user wants product photos transformed, that's `product-photo-studio`. If they want video, that's `motion-studio`.

## Prerequisites

Picsart `gen-ai` CLI installed and authenticated:

```bash
curl -fsSL https://picsart.com/gen-ai-cli/install.sh | bash
gen-ai login
gen-ai whoami
```

Per-mode setup (caching, serverless endpoints, font choices) is documented inside each mode reference.

## How to Run

1. Identify the mode from the user's request using the table in **When to Use**.
2. Load the corresponding mode reference: `Read` `references/modes/<mode>.md`.
3. Follow the procedure described there — extract text signals, build prompt, generate.
4. Return to this SKILL.md only when switching modes mid-task.

## Quick Reference

```bash
# Single image from a prompt
gen-ai generate --model <model> --prompt "<derived from text>"

# Estimate cost first
gen-ai pricing --model <model> --count <N>

# Browse available models
gen-ai models
```

Prompt-construction patterns (how to derive a prompt from a paragraph, an article, or a URL's metadata) live in the individual mode references.

## Procedure

Shared outer loop:

1. **Extract signals** — pull subject, tone, palette hints, and target dimensions from the input text.
2. **Build prompt** — translate signals into a `gen-ai` prompt; each mode has its own template.
3. **Estimate** — `gen-ai pricing` before committing for multi-image runs.
4. **Generate** — invoke `gen-ai generate`. Stream progress.
5. **Place** — drop into the right slot: PDP, blog frontmatter, OG meta tag, social variant.

## Pitfalls

- **Don't generate from raw text.** Always extract signals first; raw paragraphs produce literal, lifeless images.
- **Match aspect ratio to placement.** OG = 1200×630, blog hero = 16:9, social = varies.
- **Cache OG images.** Don't regenerate on every page view — see `references/modes/og.md`.
- Mode-specific pitfalls live inside the individual mode references.

## Verification

```bash
# Confirm output exists and matches expected dimensions
gen-ai inspect outputs/<run>/<image>.png

# Spot-check the visual matches the source text by re-reading both side by side
```

## See also

- [`product-photo-studio`](../product-photo-studio/) — transform existing product photos
- [`motion-studio`](../motion-studio/) — video from text
- [`gen-ai-use`](../gen-ai-use/) — foundational gen-ai CLI reference
