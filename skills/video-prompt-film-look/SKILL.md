---
name: video-prompt-film-look
description: Refine palette, contrast, grain and highlight treatment in an existing video prompt. Use for film-look requests, excessive glow, unstable grain or colour drift.
license: MIT
metadata:
  version: "1.0.0"
---

# Video Prompt: Film Look

## Scope and output

Use the supplied prompt and requested change. If no prompt is supplied, ask for it; do not invent a new brief. No generation tools, paid jobs or publication are needed.

Keep subject, action, identity, brand requirements, duration, aspect ratio, audio and references unchanged unless the request explicitly changes them. Replace conflicting in-scope wording rather than appending contradictions. If two explicit requirements conflict and the intended outcome is unclear, ask one focused question; otherwise make the smallest useful edit and label assumptions. Do not require a model choice for a model-neutral wording repair.

Return the revised full prompt in a copyable block (or only the replacement clause if requested), a short change note, assumptions only when needed, and one relevant output check. Do not claim the edit is tested or will cure a model defect. When a model is named, use its documented controls and limits; unknown capabilities remain unknown.

## Refinement decisions

Separate palette and saturation, tonal contrast, highlight roll-off, texture, and optical/finishing effects. Preserve approved brand colours and skin tone. Describe what remains legible in highlights and shadows rather than adding cinematic adjectives.

Grain, bloom and halation are different controls. Grain is texture; bloom spreads bright light; halation is a highlight-edge effect whose appearance depends on the process. Request restraint and local placement when appropriate. Do not use grain or haze to hide unstable geometry or hands.

A film-stock name is an optional reference, not proof of accurate emulation. No movement, genre or era has one universal lens, palette or exposure ratio. Translate the desired look into visible properties; do not invent stock history, processing or technical settings. Monochrome needs tonal separation between objects, not just absent colour.

When repeatability matters, propose a clean generation plus a shared post-production grade/grain treatment outside the generation prompt. Do not silently perform that edit or add paid rendering. Softness, diffusion and grain must preserve required product and facial detail. Do not add scratches, gate weave or flicker unless requested.

## Example

Original: Cinematic vintage film look on the approved portrait.

Revision: Restrained warm highlights, natural skin colour distinct from the warm background, moderate contrast with detail in bright fabric and dark clothing, and subtle fine grain without exposure flicker.

This illustrates a scoped edit, not a tested model recipe. Keep any other clauses in the actual user's prompt.

## Review

Compare start/end colour and the full take at delivery scale. Check texture crawl, clipping, halos and matching across adjacent shots.

For evidence boundaries, see [sources](references/sources.md).
