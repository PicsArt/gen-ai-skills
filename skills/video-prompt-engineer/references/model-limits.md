# Prompt length limits by model

Checked against vendor documentation on **2026-08-16**. Caps change between model versions and
several vendors do not publish one at all, so **treat this as a starting point and confirm against
the model's own API reference** before relying on a number. A cap that moved since this file was
written is a silent failure, not an error.

## Hosted APIs

| model | prompt cap | negative prompt | notes |
|---|---|---|---|
| Kling 3.0 and 2.x | 2500 characters | Separate 2500 characters | Storyboard mode caps **each storyboard at 512 characters**, far tighter than the headline figure |
| Luma Ray, Dream Machine | 6000 characters | Not documented | Rejects anything outside 1 to 6000 |
| PixVerse | Not published. Aggregators enforce 2048 | Field exists, no limit published | PixVerse lists prompt and negative_prompt but states no length constraint on either. Its own testing reports control dropping past 80 words |
| Vidu Q2 | 3000 characters | Not documented | Providers disagree, some document 1500. Take the lower figure |
| Sora 2 | About 2000 | Not documented | Sources split on whether the unit is characters or tokens. Semantic drift reported past roughly 1500 characters |
| Hailuo 02, MiniMax | 2000 characters | Not documented | Same limit for text to video and image to video |
| Runway Gen-3, Gen-4 | 1000 characters | Not documented | Raised to 1000 from a lower figure. **The tightest full-prompt cap among the major hosted models** |
| Veo 3, Veo 3.1 | Not published | `negativePrompt` field exists | Google publishes a recommended length rather than a cap. See below |
| Seedance 2.0 | Not published | No negative field | The API schema states no length constraint |

## Open weights, run locally

These have no character cap. They have a **text encoder token limit**, which behaves differently:
the prompt is truncated at the encoder before the model ever sees it, with no error and no warning.

| model | encoder | token limit | notes |
|---|---|---|---|
| Wan 2.2 | UMT5-XXL | 512 tokens, truncated beyond | Users report quality degrading from about 320 to 350 tokens: motion slows and a grid artefact appears |
| HunyuanVideo | T5-XXL | Commonly 512 tokens | Verify against the implementation you are running |
| LTX-Video, LTX-2 | T5 v1.1-XXL | Not documented for LTX-2 | Handles 100 words or more comfortably |

512 tokens is roughly 1800 to 2000 English characters. The practical figure is lower.

## The finding that matters more than the table

**Every vendor that publishes a recommended length recommends far less than its own cap.**

| model | cap | what the vendor recommends |
|---|---|---|
| Kling | 2500 characters | 30 to 50 words on 1.6 Standard, 40 to 60 on 2.5 Turbo Pro, 60 to 100 on 2.6 and O1. 15 to 40 for image to video |
| Luma | 6000 characters | 40 to 100 words |
| PixVerse | Not published | 50 to 80 words |
| Veo 3.1 | Not published | 100 to 150 words, or 3 to 6 sentences |

100 words is around 700 characters. So the recommended length across every one of these sits at
roughly **a quarter to a third of the cap**, and clusters tightly around the 120 word craft limit
this skill already uses.

**The cap is a rejection threshold, not a target.** Writing to it produces worse output on every
model above, not merely a longer prompt. Use the cap to decide what has to be cut, never to decide
how much can be added.

## What this means in practice

- **1000 characters is the portable figure.** It fits Runway, the tightest major cap, so a prompt
  written to it runs anywhere without a rewrite. That is the default when the model is unknown.
- **512 characters is the figure for storyboard and multi-shot work on Kling**, and the tightest
  real constraint on this page.
- **Image to video wants the shortest prompts of all**, 15 to 40 words on Kling, because the frame
  already carries the subject and the prompt should only carry motion.
- **A separate negative field is free budget.** Kling gives the negative prompt its own 2500
  characters, so exclusions moved there cost nothing against the prompt. PixVerse and Veo expose
  the field without publishing a limit for it, which is still free budget. Where a model has no
  negative field, as with Seedance, the exclusions come out of the prompt budget and belong last.
- **Where no cap is published, assume one exists.** Seedance and Veo document none, which is not
  the same as having none, and an undocumented cap still truncates.

## Sources

Vendor documentation and vendor prompting guides, retrieved 2026-08-16:

- Kling AI API, Text to Video reference, and the Kling prompting guides
- Luma Labs API documentation and the Luma Agents FAQ
- PixVerse Platform documentation and PixVerse's own prompting guidance
- MiniMax platform API reference for Hailuo 02
- Runway help centre and API input parameters
- Google DeepMind Veo prompt guide and the Vertex AI Veo model reference
- fal.ai model API reference for Seedance 2.0 and Vidu Q2
- OpenAI Sora 2 prompting guide
- Hugging Face and ComfyUI Wan 2.2 encoder documentation
