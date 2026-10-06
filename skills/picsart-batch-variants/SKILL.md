---
name: picsart-batch-variants
description: Create and compare controlled Picsart asset variants within an authorized generation budget.
version: 1.0.0
author: Picsart
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    category: creative
    tags: [picsart, mcp, batch, variants, budget]
---

# Picsart batch variants

Change one parameter across a set of tracked jobs and compare the results under a fixed budget.

## When to Use

- The user wants several variants that answer one comparison question, such as background color or camera position.
- The batch must stay within an authorized generation budget.

## Prerequisites

- The `picsart` MCP server is connected.
- Read [the interface map](../picsart-workflows/references/interface-map.md) before a batch operation.

## How to Run

Follow the Procedure below.

## Quick Reference

### CLI batch commands

- For the CLI, inspect `gen-ai batch run --help` for the installed manifest format.
- Use `gen-ai batch status` to read the local report.
- Use `gen-ai batch resume` only when new paid submissions are authorized.

## Procedure

1. Define one comparison question, such as background color or camera position.
2. Keep the source asset, model, format, and other parameters fixed.
3. Give each variant a stable ID.
4. Record the changed parameter for each ID.
5. Check each request against the selected model schema.
6. Estimate the total cost before submission.
   If cost is unknown and a hard credit cap applies, do not submit.
7. Submit only the authorized quantity.
8. For MCP or SDK, record each submitted job before the next operation.
9. Continue these existing jobs from their handles after an interruption.
10. Compare completed assets against the same acceptance criteria.

### MCP or SDK queue

For MCP or SDK, manage separate generation requests with a bounded queue.
Reserve the estimated batch cost before concurrent submissions.
Keep failed jobs within the same total budget when you authorize retries.

## Pitfalls

- Resume can submit failed jobs again.
- CLI reports omit submission handles and do not confirm live job state.
- After an ambiguous failure, establish the original job state before a retry.
- Do not assume that a `count` parameter produces controlled variations.
- Do not treat an unavailable price as zero.
- Visual preference alone does not prove better advertisement performance.

## Verification

Return the variant table, asset links, job states, and selection reasons.
