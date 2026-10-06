---
name: picsart-generate
description: Generate image, video, audio, or text with a verified Picsart model or preset and retain its receipt.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, generation, models, receipts]
---

# Generate

Run one schema-checked Picsart generation and keep its receipt.

## When to Use

- A Picsart workflow needs new image, video, audio, or text from a verified model.
- The result needs a receipt that later steps can save, poll, or recover.
- For a standalone terminal generation with the gen-ai CLI, use [gen-ai-use](../gen-ai-use/SKILL.md).

## Prerequisites

- The `picsart` MCP server is connected.
- Read [the interface map](../picsart-workflows/references/interface-map.md). Use the user's selected model when available. Otherwise, select a model for the required inputs and output.

## How to Run

Use [asset reuse](../picsart-asset-reuse/SKILL.md) for existing cast, props, and locations before creating replacements.

## Quick Reference

### Routes

Use one route:

- MCP: call `picsart_model_params`, then `picsart_preflight`. Submit with `picsart_generate`. Set `async: true` for media to retain a job handle. Use dedicated edit tools for remove background, change background, enhance, and vectorize.
- CLI: use `gen-ai validate --model MODEL --file payload.json`. Submit with `gen-ai generate --model MODEL --prompt-file prompt.txt --no-input --json --no-open` and verified model flags. Check `--help` before use.
- SDK: use `Model(model).validate(params)`. Use `ai.submit(model, params)` for media. Save the ID before `ai.result(model, id)`. Use `ai.generateText(model, params)` for text.

## Procedure

1. Get the model schema. Set only supported parameters. Record the prompt, model, references, output format, count, and cost limit. Validate the final payload. Check the price when the task has a spending limit. Treat an unknown price as unknown.
2. Submit within the user's authorized scope. If a hard credit cap applies and cost is unknown, do not submit.

## Pitfalls

- Do not rely on a cost flag when its implementation does not enforce the limit.
- For CLI validation, check the exit code. Successful validation can return no JSON text.

## Verification

Save the receipt before waiting. Inspect the completed output. Report the result and save status. Retry a failed submission only after you establish that it did not start a job.
