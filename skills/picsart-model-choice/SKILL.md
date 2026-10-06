---
name: picsart-model-choice
description: Select a Picsart model for required inputs, output format, and cost.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, model-selection, preflight, cost]
---

# Picsart model choice

Pick a Picsart model from its live catalog and schema, then preflight one real request.

## When to Use

- A task needs a model that accepts its inputs, produces its output format, and fits its cost limit.
- The user's chosen model must be checked against the required features.

## Prerequisites

- The `picsart` MCP server is connected.
- Use [the interface map](../picsart-workflows/references/interface-map.md) for SDK and CLI calls.

## How to Run

Follow the Procedure below.

## Quick Reference

### Selection rules

- Select a dedicated edit tool for background changes or enhancement.
- Check reference-image support before a character or product workflow.
- Check audio-input support before speech or music changes.
- Keep the user's model choice unless a required feature is unavailable.

## Procedure

1. Record the input type, output type, aspect ratio, and duration.
2. Use the user's model when it meets these requirements.
3. Otherwise, read `picsart_model_catalog` with the necessary input and output filters.
4. Use `picsart_list_models` when the user wants the visual model selector.
5. For a known model, read `picsart_model_params` when required parameters are unknown.
6. Use a supported aspect ratio from the brief or model default.
   If neither supplies a usable ratio, ask for the intended output format.
7. Prepare one candidate request with the actual input assets.
8. Call `picsart_preflight` with `model` and `params`.
9. Correct invalid parameters before generation.
10. Treat a null credit estimate as an unknown cost.

If the catalog is incomplete, refine the filters or increase the supported limit.

## Pitfalls

- Do not select a model from a fixed ranking.
- Model names and available features can change.
- If a hard credit cap applies and cost is unknown, do not submit.

## Verification

Return the model ID, selected parameters, estimated cost, and any unsupported requirement.
